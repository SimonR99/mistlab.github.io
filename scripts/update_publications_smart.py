#!/usr/bin/env python3
"""
MIST Lab Publication Updater - Single File Version

Features:
- Single file for both input and output (in-place updates)
- Updates incomplete entries (missing key fields)
- Creates file from scratch if it doesn't exist
- Properly detects removed entries and re-adds them
"""

import argparse
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import sys
import os

import requests
from scholarly import scholarly
from tqdm import tqdm

# Suppress ALL logging before importing scholarly
logging.getLogger("scholarly").setLevel(logging.CRITICAL)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("httpcore").setLevel(logging.CRITICAL)

# Disable urllib3 warnings
import urllib3
urllib3.disable_warnings()

# Configure our own logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False

class BibTexParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.entries: Dict[str, Dict] = {}
        self.title_to_key: Dict[str, str] = {}
        self.normalized_titles: Dict[str, str] = {}
        self.parse_file()
    
    def normalize_title(self, title: str) -> str:
        normalized = re.sub(r'[^\w\s]', '', title.lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized
    
    def generate_key(self, title: str, authors: str, year: str) -> str:
        if authors:
            first_author = authors.split(' and ')[0].strip()
            if ',' in first_author:
                last_name = first_author.split(',')[0].strip().lower()
            else:
                author_parts = first_author.split()
                last_name = author_parts[-1].lower() if author_parts else 'author'
        else:
            last_name = 'author'
        last_name = re.sub(r'[^\w]', '', last_name)
        title_words = [w for w in title.lower().split() if len(w) > 3]
        title_word = re.sub(r'[^\w]', '', title_words[0]) if title_words else 'paper'
        year = year or str(datetime.now().year)
        base_key = f"{last_name}{year}{title_word}"
        key = base_key
        counter = 1
        while key in self.entries:
            key = f"{base_key}{counter}"
            counter += 1
        return key
    
    def parse_file(self):
        if not Path(self.file_path).exists():
            return
        try:
            content = Path(self.file_path).read_text(encoding='utf-8')
            entry_pattern = r'@(\w+)\s*\{\s*([^,\s]+)\s*,([^@]*?)(?=\n\s*@|\n\s*$)'
            entries = re.findall(entry_pattern, content + '\n@', re.MULTILINE | re.DOTALL)
            for entry_type, key, body in entries:
                fields: Dict[str, str] = {}
                field_text = body.strip()
                current_field = None
                current_value: List[str] = []
                brace_count = 0
                for line in field_text.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    m = re.match(r'^(\w+)\s*=\s*\{(.*)$', line)
                    if m and brace_count == 0:
                        if current_field:
                            val = ' '.join(current_value).rstrip(',').rstrip('}')
                            fields[current_field.lower()] = val
                        current_field = m.group(1)
                        current_value = [m.group(2)]
                        brace_count = m.group(2).count('{') - m.group(2).count('}') + 1
                    else:
                        if current_field:
                            current_value.append(line)
                            brace_count += line.count('{') - line.count('}')
                if current_field:
                    val = ' '.join(current_value).rstrip(',').rstrip('}')
                    fields[current_field.lower()] = val
                self.entries[key] = {'type': entry_type.lower(), 'fields': fields}
                if 'title' in fields:
                    norm = self.normalize_title(fields['title'])
                    self.title_to_key[norm] = key
                    self.normalized_titles[norm] = fields['title']
        except Exception as e:
            logger.error(f"Error parsing BibTeX file: {e}")
    
    def find_entry_by_title(self, title: str) -> Optional[Tuple[str, Dict]]:
        norm = self.normalize_title(title)
        if norm in self.title_to_key:
            key = self.title_to_key[norm]
            return key, self.entries[key]
        # fuzzy match
        words = set(norm.split())
        for existing_norm, key in self.title_to_key.items():
            overlap = len(words & set(existing_norm.split()))
            if overlap / min(len(words), len(existing_norm.split())) >= 0.8:
                return key, self.entries[key]
        return None
    
    def is_complete(self, entry_key: str) -> bool:
        if entry_key not in self.entries:
            return False
        entry = self.entries[entry_key]
        fields = entry['fields']
        if entry['type'] == 'misc':
            has_venue = any(f in fields for f in ('journal','booktitle','publisher'))
            has_id    = any(f in fields for f in ('doi','isbn','issn','url'))
            if not (has_venue or has_id):
                return False
        if not all(fields.get(f) for f in ('title','author','year')):
            return False
        has_venue = any(fields.get(f) for f in ('journal','booktitle','publisher'))
        has_id    = any(fields.get(f) for f in ('doi','isbn','issn','url'))
        return has_venue or has_id
    
    def get_all_titles(self) -> Set[str]:
        return set(self.title_to_key.keys())

class PublicationEnricher:
    def __init__(self):
        self.crossref_base_url = "https://api.crossref.org/works"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MIST-Lab-Publication-Updater (mailto:admin@mistlab.ca)'
        })
        self.cache: Dict[str, Optional[Dict]] = {}
    
    def get_crossref_data(self, title: str, authors: str, year: str) -> Optional[Dict]:
        key = f"{title}_{year}"
        if key in self.cache:
            return self.cache[key]
        try:
            clean_title = re.sub(r'[^\w\s]', ' ', title)
            clean_title = re.sub(r'\s+', ' ', clean_title).strip()
            params = {'query': clean_title, 'rows': 5}
            if year.isdigit():
                params['filter'] = f'from-pub-date:{year},until-pub-date:{year}'
            resp = self.session.get(self.crossref_base_url, params=params, timeout=10)
            resp.raise_for_status()
            items = resp.json().get('message', {}).get('items', [])
            for item in items:
                if 'title' in item and item['title']:
                    if self._titles_match(title, item['title'][0]):
                        self.cache[key] = item
                        return item
            self.cache[key] = items[0] if items else None
            return self.cache[key]
        except Exception:
            self.cache[key] = None
            return None
    
    def _titles_match(self, t1: str, t2: str) -> bool:
        a = re.sub(r'[^\w\s]', ' ', t1).lower().split()
        b = re.sub(r'[^\w\s]', ' ', t2).lower().split()
        if not a or not b:
            return False
        overlap = len(set(a) & set(b))
        return overlap / min(len(a), len(b)) >= 0.7
    
    def enhance_publication(self, pub_data: Dict) -> Dict:
        enhanced = pub_data.copy()
        cr = self.get_crossref_data(
            pub_data.get('title',''),
            pub_data.get('authors',''),
            pub_data.get('year','')
        )
        if cr:
            # --- DOI & URL ---
            doi = cr.get('DOI')
            if doi:
                enhanced['doi'] = doi
                if not enhanced.get('url'):
                    enhanced['url'] = f"https://doi.org/{doi}"
            # --- Venue ---
            container = cr.get('container-title', [])
            event = cr.get('event', {})
            if container:
                c0 = container[0]
                if any(k in c0.lower() for k in ('proceedings','conference','symposium','workshop','icml','neurips','cvpr','iccv')):
                    enhanced['entry_type'] = 'inproceedings'
                    enhanced['booktitle']   = c0
                else:
                    enhanced['entry_type'] = 'article'
                    enhanced['journal']     = c0
            elif event.get('name'):
                enhanced['entry_type'] = 'inproceedings'
                enhanced['booktitle']   = event['name']
            # --- ISBN & ISSN ---
            isbns = cr.get('ISBN', [])
            if isbns:
                enhanced['isbn'] = isbns[0]
            issns = cr.get('ISSN', [])
            if issns:
                enhanced['issn'] = issns[0]
            # --- Pages & numpages ---
            pages = cr.get('page')
            if pages:
                enhanced['pages'] = pages
                if '-' in pages:
                    try:
                        s,e = pages.split('-',1)
                        enhanced['numpages'] = str(int(e)-int(s)+1)
                    except ValueError:
                        pass
            # --- Publisher & address ---
            if 'publisher' in cr:
                enhanced['publisher'] = cr['publisher']
            if 'publisher-location' in cr:
                enhanced['address']   = cr['publisher-location']
            # --- Volume & issue ---
            if 'volume' in cr:
                enhanced['volume'] = str(cr['volume'])
            if 'issue' in cr:
                enhanced['number'] = str(cr['issue'])
            # --- Month ---
            dp = cr.get('published-print',{}).get('date-parts',[])
            if dp and dp[0] and len(dp[0])>1:
                m = dp[0][1]
                months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
                if 1<=m<=12:
                    enhanced['month'] = months[m-1]
            # --- Keywords ---
            subj = cr.get('subject',[])
            if subj:
                enhanced['keywords'] = ', '.join(subj[:5])
            # --- Event location & series ---
            if event.get('location'):
                enhanced['location'] = event['location']
            if event.get('acronym'):
                enhanced['series']   = event['acronym']
        # Fallback entry type
        if not enhanced.get('entry_type'):
            if enhanced.get('journal'):
                enhanced['entry_type'] = 'article'
            elif enhanced.get('booktitle'):
                enhanced['entry_type'] = 'inproceedings'
            else:
                enhanced['entry_type'] = 'misc'
        return enhanced

def generate_bibtex_entry(key: str, data: Dict) -> str:
    entry_type = data.get('entry_type','misc')
    lines = [f"@{entry_type}{{{key},"]
    order = [
        'title','author','year','month',
        'journal','booktitle','publisher','address',
        'volume','number','pages','series',
        'doi','url','isbn','issn',
        'keywords','location','note'
    ]
    for field in order:
        if field == 'author':
            val = data.get('authors','')
        elif field == 'year':
            val = data.get('year','0000')
        elif field=='note' and data.get('citations',0)>0:
            val = f"Cited by {data['citations']}"
        else:
            val = data.get(field,'')
        if val:
            lines.append(f"  {field:<12} = {{{val}}},")
    if lines[-1].endswith(','):
        lines[-1] = lines[-1][:-1]
    lines.append("}")
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='Update MIST Lab publication database')
    parser.add_argument('--file','-f',default='out_scholar.bib',
                        help='BibTeX file to update (default: out_scholar.bib)')
    parser.add_argument('--author-id',default='TVHJJ9wAAAAJ',
                        help='Google Scholar author ID')
    parser.add_argument('--max-updates',type=int)
    parser.add_argument('--verbose','-v',action='store_true')
    args = parser.parse_args()

    if not args.verbose:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    if not Path(args.file).exists():
        logger.info(f"Creating new file: {args.file}")
        with open(args.file,'w',encoding='utf-8') as f:
            f.write("% MIST Lab Publications\n")
            f.write(f"% Created on {datetime.now():%Y-%m-%d %H:%M:%S}\n")
            f.write("% Source: Google Scholar profiles with CrossRef enhancement\n\n")

    parser_obj = BibTexParser(args.file)
    incomplete = [(k,e) for k,e in parser_obj.entries.items() if not parser_obj.is_complete(k)]
    logger.info(f"Found {len(parser_obj.entries)} entries, {len(incomplete)} incomplete")

    logger.info("Fetching publications from Google Scholar...")
    try:
        author = scholarly.search_author_id(args.author_id)
        scholarly.fill(author, sections=['publications'])
        pubs = author.get('publications',[])
    except Exception as e:
        logger.error(f"Failed to fetch publications: {e}")
        return

    to_process: List[Tuple[Dict,str]] = []
    for pub in pubs:
        bib = pub.get('bib',{})
        title   = bib.get('title','')
        authors = bib.get('author','') or pub.get('author','')
        year    = bib.get('pub_year', '') or pub.get('year', '') or '????'
        existing = parser_obj.find_entry_by_title(title)
        status = 'new' if existing is None else 'update'
        if status == 'new' or (status=='update' and not parser_obj.is_complete(existing[0])):
            to_process.append((pub, status))

    if not to_process:
        logger.info("All publications are complete!")
        return

    logger.info(f"Processing {len(to_process)} publications")
    enricher = PublicationEnricher()
    existing_keys = set(parser_obj.entries.keys())
    processed = 0

    pbar = tqdm(to_process, desc="Updating", file=sys.stdout)
    for pub, status in pbar:
        scholarly.fill(pub)
        bib = pub.get('bib',{})
        title   = bib.get('title','')
        authors = bib.get('author','') or pub.get('author','')
        year    = bib.get('pub_year', '') or pub.get('year', '') or '????'
        # <-- use pub_url instead of bib['url']
        pub_data = {
            'title': title,
            'authors': authors,
            'year': year,
            'citations': pub.get('num_citations', 0),
            'url': pub.get('pub_url', '')
        }
        enriched = enricher.enhance_publication(pub_data)
        existing = parser_obj.find_entry_by_title(title)

        if status=='update' and existing:
            key = existing[0]
            logger.info(f"  Updating {key}")
            content = Path(args.file).read_text(encoding='utf-8')
            pattern = rf'@\w+\{{{re.escape(key)},.*?\n\}}\n+'
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            Path(args.file).write_text(content, encoding='utf-8')
        else:
            key = parser_obj.generate_key(title, authors, year)
            while key in existing_keys:
                key += 'a'

        with open(args.file, 'a', encoding='utf-8') as f:
            f.write(generate_bibtex_entry(key, enriched))
            f.write('\n\n')
        existing_keys.add(key)
        processed += 1
        if args.max_updates and processed >= args.max_updates:
            break
        time.sleep(0.5)

    pbar.close()
    final = BibTexParser(args.file)
    complete = sum(1 for k in final.entries if final.is_complete(k))
    logger.info(f"Done! {processed} processed. Complete entries: {complete}/{len(final.entries)}")

if __name__ == "__main__":
    main()
