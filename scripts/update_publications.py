#!/usr/bin/env python3
"""
MIST Lab Publication Updater

This script automatically fetches publications from Google Scholar profiles
and generates BibTeX content for the lab website.

Usage:
    python scripts/update_publications.py [--dry-run] [--output OUTPUT_FILE]
"""

import argparse
import os
import sys
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
import re

from scholarly import scholarly, ProxyGenerator
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PublicationUpdater:
    """Main class for updating publications from Google Scholar."""
    
    def __init__(self):
        self.lab_members = {
            'giovanni_beltrame': {
                'name': 'Giovanni Beltrame',
                'scholar_id': 'TVHJJ9wAAAAJ',  # Direct Scholar ID from profile URL
                'search_terms': ['Giovanni Beltrame', 'G Beltrame'],
                'affiliation': 'Polytechnique Montreal',
                'highlight': True  # Whether to highlight this author in publications
            }
            # Future lab members can be added here:
            # 'member_name': {
            #     'name': 'Full Name',
            #     'scholar_id': 'SCHOLAR_ID',
            #     'search_terms': ['Name variations'],
            #     'affiliation': 'Polytechnique Montreal',
            #     'highlight': False
            # }
        }
        # Track used keys to prevent duplicates
        self.used_keys = set()
        
    def setup_proxy(self) -> bool:
        """Setup proxy to avoid being blocked by Google Scholar."""
        try:
            # Try to use FreeProxies (optional, may help with rate limiting)
            pg = ProxyGenerator()
            success = pg.FreeProxies()
            if success:
                scholarly.use_proxy(pg)
                logger.info("Proxy setup successful")
                return True
        except Exception as e:
            logger.warning(f"Proxy setup failed, continuing without proxy: {e}")
        
        return False
    
    def find_author_profile(self, member_info: Dict) -> Optional[Dict]:
        """Find author profile on Google Scholar."""
        # If we have a direct Scholar ID, use it directly
        if member_info.get('scholar_id'):
            logger.info(f"Using direct Scholar ID for {member_info['name']}: {member_info['scholar_id']}")
            try:
                # Get author profile directly by ID
                author_profile = scholarly.search_author_id(member_info['scholar_id'])
                logger.info(f"Found profile: {author_profile.get('name')} - {author_profile.get('affiliation')}")
                return author_profile
            except Exception as e:
                logger.warning(f"Failed to get profile by ID '{member_info['scholar_id']}': {e}")
                logger.info("Falling back to search method...")
        
        # Fall back to search method
        logger.info(f"Searching for {member_info['name']} on Google Scholar...")
        
        for search_term in member_info['search_terms']:
            try:
                # Search for the author
                search_query = scholarly.search_author(search_term)
                
                for author in search_query:
                    # Check if this is likely the right person
                    if (member_info['affiliation'].lower() in author.get('affiliation', '').lower() or
                        any(term.lower() in author.get('name', '').lower() 
                            for term in member_info['search_terms'])):
                        
                        logger.info(f"Found profile: {author.get('name')} - {author.get('affiliation')}")
                        return author
                
                time.sleep(2)  # Be respectful to Google Scholar
                
            except Exception as e:
                logger.warning(f"Search failed for '{search_term}': {e}")
                time.sleep(5)  # Wait longer on error
        
        logger.error(f"Could not find profile for {member_info['name']}")
        return None
    

    
    def clean_text(self, text: str) -> str:
        """Clean text for BibTeX format."""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Fix common encoding issues
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def generate_bibtex_key(self, pub_info: Dict, author_name: str) -> str:
        """Generate a unique BibTeX key for a publication."""
        bib = pub_info.get('bib', {})
        
        # Extract last name
        first_author = author_name.split()[-1].lower()
        
        # Extract year (handle both string and integer)
        year_raw = bib.get('pub_year', datetime.now().year)
        if isinstance(year_raw, int):
            year = str(year_raw)
        else:
            year = str(year_raw).replace(',', '') if year_raw else str(datetime.now().year)
        
        # Extract first meaningful word from title
        title = self.clean_text(bib.get('title', ''))
        title_words = [word for word in title.lower().split() 
                      if len(word) > 3 and word not in ['the', 'and', 'for', 'with', 'from']]
        title_word = title_words[0] if title_words else 'paper'
        
        base_key = f"{first_author}{year}{title_word}"
        
        # Remove special characters
        base_key = re.sub(r'[^a-zA-Z0-9]', '', base_key)
        
        # Handle duplicates by appending a counter
        key = base_key
        counter = 2
        while key in self.used_keys:
            key = f"{base_key}{counter}"
            counter += 1
        
        # Mark this key as used
        self.used_keys.add(key)
        
        return key
    
    def publication_to_bibtex(self, pub_info: Dict, member_info: Dict) -> str:
        """Convert a publication to BibTeX format."""
        bib = pub_info.get('bib', {})
        
        # Determine publication type
        venue = bib.get('venue', '').lower()
        if 'journal' in venue or 'transactions' in venue or 'letters' in venue:
            entry_type = 'article'
        elif 'conference' in venue or 'workshop' in venue or 'symposium' in venue:
            entry_type = 'inproceedings'
        elif 'book' in venue:
            entry_type = 'book'
        else:
            entry_type = 'misc'
        
        # Generate BibTeX key
        key = self.generate_bibtex_key(pub_info, member_info['name'])
        
        # Start BibTeX entry
        bibtex_lines = [f"@{entry_type}{{{key},"]
        
        # Title
        title = self.clean_text(bib.get('title', ''))
        if title:
            bibtex_lines.append(f"  title        = {{{title}}},")
        
        # Author
        author = self.clean_text(bib.get('author', ''))
        if author:
            bibtex_lines.append(f"  author       = {{{author}}},")
        
        # Year
        # Handle both string and integer years
        year_raw = bib.get('pub_year', '')
        if isinstance(year_raw, int):
            year = str(year_raw)
        elif year_raw:
            year = str(year_raw).replace(',', '')
        else:
            year = ''
        if year:
            bibtex_lines.append(f"  year         = {{{year}}},")
        
        # Venue-specific fields
        venue_clean = self.clean_text(bib.get('venue', ''))
        if venue_clean:
            if entry_type == 'article':
                bibtex_lines.append(f"  journal      = {{{venue_clean}}},")
            elif entry_type == 'inproceedings':
                bibtex_lines.append(f"  booktitle    = {{{venue_clean}}},")
            else:
                bibtex_lines.append(f"  publisher    = {{{venue_clean}}},")
        
        # Pages
        pages = bib.get('pages', '')
        if pages:
            bibtex_lines.append(f"  pages        = {{{pages}}},")
        
        # Volume
        volume = bib.get('volume', '')
        if volume:
            bibtex_lines.append(f"  volume       = {{{volume}}},")
        
        # Number
        number = bib.get('number', '')
        if number:
            bibtex_lines.append(f"  number       = {{{number}}},")
        
        # URL (from Google Scholar)
        scholar_url = pub_info.get('author_pub_url', '')
        if scholar_url:
            full_url = f"https://scholar.google.com{scholar_url}"
            bibtex_lines.append(f"  url          = {{{full_url}}},")
        
        # Citation count (as a note)
        citations = pub_info.get('num_citations', 0)
        if citations and citations > 0:
            bibtex_lines.append(f"  note         = {{Cited by {citations}}},")
        
        # Close entry (remove last comma)
        if bibtex_lines[-1].endswith(','):
            bibtex_lines[-1] = bibtex_lines[-1][:-1]
        
        bibtex_lines.append("}")
        
        return '\n'.join(bibtex_lines)
    
    def update_publications(self, output_file: str = 'out.bib', dry_run: bool = False, live_update: bool = True) -> bool:
        """Main method to update publications."""
        logger.info("Starting publication update...")
        
        # Reset used keys tracker for fresh start
        self.used_keys.clear()
        
        # Setup proxy (optional)
        self.setup_proxy()
        
        all_bibtex_entries = []
        
        # Initialize the output file with header if live updating
        if live_update and not dry_run:
            self._initialize_output_file(output_file)
        
        # Process each lab member
        for member_key, member_info in self.lab_members.items():
            logger.info(f"Processing {member_info['name']}...")
            
            # Find author profile
            author_profile = self.find_author_profile(member_info)
            if not author_profile:
                continue
            
            # Fetch publications with live updates
            publications = self.fetch_publications_live(author_profile, member_info, output_file, dry_run, live_update)
            all_bibtex_entries.extend(publications)
        
        if not all_bibtex_entries:
            logger.error("No publications found to update")
            return False
        
        # Handle dry run output
        if dry_run:
            self._show_dry_run_results(all_bibtex_entries)
            return True
        
        # If not using live updates, write everything at once
        if not live_update:
            return self._write_final_output(all_bibtex_entries, output_file)
        
        # For live updates, finalize the file
        self._finalize_output_file(output_file, len(all_bibtex_entries))
        return True
    
    def _initialize_output_file(self, output_file: str):
        """Initialize the output file with header."""
        header = f"""% MIST Lab Publications
% Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
% Source: Google Scholar profiles
% Status: Updating in progress...

"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(header)
            logger.info(f"📝 Initialized {output_file} for live updates")
        except Exception as e:
            logger.error(f"Failed to initialize {output_file}: {e}")
    
    def _append_to_output_file(self, output_file: str, bibtex_entry: str):
        """Append a single BibTeX entry to the output file."""
        try:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(bibtex_entry + '\n\n')
            return True
        except Exception as e:
            logger.warning(f"Failed to append to {output_file}: {e}")
            return False
    
    def _finalize_output_file(self, output_file: str, total_count: int):
        """Update the header with final status."""
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update the header
            updated_content = content.replace(
                "% Status: Updating in progress...",
                f"% Status: Complete - {total_count} publications fetched"
            )
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logger.info(f"✅ Finalized {output_file} with {total_count} publications")
        except Exception as e:
            logger.warning(f"Failed to finalize {output_file}: {e}")
    
    def fetch_publications_live(self, author_profile: Dict, member_info: Dict, 
                               output_file: str, dry_run: bool, live_update: bool) -> List[str]:
        """Fetch publications with live updates to file."""
        logger.info(f"Fetching publications for {author_profile.get('name')}...")
        
        try:
            # Fill in the author profile with complete information
            author = scholarly.fill(author_profile)
            bibtex_entries = []
            
            total_pubs = len(author.get('publications', []))
            logger.info(f"Found {total_pubs} publications to fetch")
            
            # Get all publications
            for i, pub in enumerate(author.get('publications', []), 1):
                try:
                    logger.info(f"📖 Fetching publication {i}/{total_pubs}...")
                    
                    # Get detailed publication information
                    filled_pub = scholarly.fill(pub)
                    
                    # Convert to BibTeX
                    bibtex_entry = self.publication_to_bibtex(filled_pub, member_info)
                    bibtex_entries.append(bibtex_entry)
                    
                    title = filled_pub.get('bib', {}).get('title', 'Unknown title')
                    year_raw = filled_pub.get('bib', {}).get('pub_year', 'Unknown year')
                    year = str(year_raw) if year_raw else 'Unknown year'
                    
                    # Live update to file
                    if live_update and not dry_run:
                        if self._append_to_output_file(output_file, bibtex_entry):
                            logger.info(f"✅ {i}/{total_pubs}: {title} ({year}) → Added to {output_file}")
                        else:
                            logger.warning(f"⚠️  {i}/{total_pubs}: {title} ({year}) → Failed to write")
                    else:
                        logger.info(f"✅ {i}/{total_pubs}: {title} ({year})")
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logger.warning(f"❌ Failed to fetch publication {i}: {e}")
                    continue
            
            logger.info(f"✅ Successfully processed {len(bibtex_entries)}/{total_pubs} publications for {member_info['name']}")
            return bibtex_entries
            
        except Exception as e:
            logger.error(f"Failed to fetch publications: {e}")
            if "login" in str(e).lower() or "captcha" in str(e).lower():
                logger.error("Google Scholar is requiring login/captcha. This usually means:")
                logger.error("1. Too many requests (rate limiting)")
                logger.error("2. Google's anti-bot measures are active")
                logger.error("3. Try again later or use a VPN")
            return []
    
    def _show_dry_run_results(self, bibtex_entries: List[str]):
        """Show dry run results."""
        header = f"""% MIST Lab Publications
% Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
% Source: Google Scholar profiles

"""
        bibtex_content = header + '\n\n'.join(bibtex_entries) + '\n'
        
        print("DRY RUN - Would write the following content:")
        print("=" * 60)
        print(bibtex_content)
        print("=" * 60)
        print(f"Total publications: {len(bibtex_entries)}")
    
    def _write_final_output(self, bibtex_entries: List[str], output_file: str) -> bool:
        """Write all entries at once (non-live mode)."""
        header = f"""% MIST Lab Publications
% Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
% Source: Google Scholar profiles

"""
        
        bibtex_content = header + '\n\n'.join(bibtex_entries) + '\n'
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(bibtex_content)
            
            logger.info(f"Successfully wrote {len(bibtex_entries)} publications to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write to {output_file}: {e}")
            return False

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='Update MIST Lab publications from Google Scholar')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be done without making changes')
    parser.add_argument('--output', default='out.bib',
                       help='Output BibTeX file (default: out.bib)')
    parser.add_argument('--no-live-update', action='store_true',
                       help='Disable live file updates (write all at once at the end)')
    parser.add_argument('--watch', action='store_true',
                       help='Show live updates in a separate terminal (tail -f style)')
    
    args = parser.parse_args()
    
    # Determine live update mode
    live_update = not args.no_live_update
    
    if args.watch and live_update and not args.dry_run:
        print(f"📺 Watch mode: You can monitor live updates with:")
        print(f"   tail -f {args.output}")
        print(f"   # Or in another terminal:")
        print(f"   watch -n 1 'tail -10 {args.output}'")
        print()
    
    updater = PublicationUpdater()
    success = updater.update_publications(args.output, args.dry_run, live_update)
    
    if success:
        if not args.dry_run:
            if live_update:
                print(f"✅ Publications successfully updated in {args.output} (live mode)")
                print(f"📊 Final file: {args.output}")
            else:
                print(f"✅ Publications successfully updated in {args.output}")
        else:
            print("✅ Dry run completed successfully")
        sys.exit(0)
    else:
        print("❌ Failed to update publications")
        sys.exit(1)

if __name__ == '__main__':
    main() 