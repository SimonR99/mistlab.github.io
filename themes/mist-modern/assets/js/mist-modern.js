/* MIST Lab Modern Theme JavaScript */

(function () {
  "use strict";

  // DOM ready function
  function ready(fn) {
    if (document.readyState !== "loading") {
      fn();
    } else {
      document.addEventListener("DOMContentLoaded", fn);
    }
  }

  ready(function () {
    initializeEnhancements();
  });

  function initializeEnhancements() {
    // Enhanced navbar scroll effect
    initNavbarScrollEffect();

    // Smooth scrolling for anchor links
    initSmoothScrolling();

    // Initialize animations
    initScrollAnimations();

    // Initialize tooltips
    initTooltips();

    // Initialize performance optimizations
    initPerformanceOptimizations();

    // Initialize publication filters (simplified)
    setTimeout(initPublicationFilters, 1000); // Delay to ensure page is fully loaded
  }

  function initNavbarScrollEffect() {
    const navbar = document.getElementById("main-navbar");
    if (!navbar) return;

    let ticking = false;

    function updateNavbar() {
      if (window.scrollY > 50) {
        navbar.classList.add("navbar-scrolled");
      } else {
        navbar.classList.remove("navbar-scrolled");
      }
      ticking = false;
    }

    function requestNavbarUpdate() {
      if (!ticking) {
        requestAnimationFrame(updateNavbar);
        ticking = true;
      }
    }

    window.addEventListener("scroll", requestNavbarUpdate, { passive: true });
  }

  function initSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
          const navHeight =
            document.querySelector(".navbar-fixed-top")?.offsetHeight || 0;
          const targetPosition = target.offsetTop - navHeight - 20;

          window.scrollTo({
            top: targetPosition,
            behavior: "smooth",
          });
        }
      });
    });
  }

  function initScrollAnimations() {
    // Check if Intersection Observer is supported
    if (!("IntersectionObserver" in window)) {
      // Fallback: just add the animation class immediately
      document
        .querySelectorAll(".modern-card, .feature-card")
        .forEach((card) => {
          card.classList.add("animate-fadeInUp");
        });
      return;
    }

    const observerOptions = {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    };

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate-fadeInUp");
          // Stop observing once animated
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe all cards and elements that should animate
    document
      .querySelectorAll(".modern-card, .feature-card, .hero-content")
      .forEach((element) => {
        observer.observe(element);
      });
  }

  function initTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof $ !== "undefined" && $.fn.tooltip) {
      $('[data-toggle="tooltip"]').tooltip();
    }
  }

  function initPerformanceOptimizations() {
    // Preload critical assets
    preloadCriticalAssets();

    // Lazy load images
    initLazyLoading();
  }

  function preloadCriticalAssets() {
    // Preload important fonts
    const fontPreload = document.createElement("link");
    fontPreload.rel = "preload";
    fontPreload.href =
      "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap";
    fontPreload.as = "style";
    document.head.appendChild(fontPreload);
  }

  function initLazyLoading() {
    // Simple lazy loading for images
    if ("IntersectionObserver" in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const img = entry.target;
            if (img.dataset.src) {
              img.src = img.dataset.src;
              img.classList.remove("lazy");
              imageObserver.unobserve(img);
            }
          }
        });
      });

      document.querySelectorAll("img[data-src]").forEach((img) => {
        imageObserver.observe(img);
      });
    }
  }

  // Simplified Publication Filters
  function initPublicationFilters() {
    // Only run on publications page
    if (!window.location.pathname.includes("/publications/")) return;

    const filterButtons = document.querySelectorAll("[data-filter]");
    const publications = document.querySelectorAll(".publication");

    if (filterButtons.length === 0 || publications.length === 0) return;

    // Add click handlers to all filter buttons
    filterButtons.forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault();

        // Remove active class from all buttons
        filterButtons.forEach((btn) => btn.classList.remove("active"));

        // Add active class to clicked button
        this.classList.add("active");

        // Get filter type
        const filterType = this.getAttribute("data-filter");

        // Filter publications
        filterPublications(filterType, publications);
      });
    });
  }

  // Advanced filtering with multiple filter types
  function filterPublications(filterType, publications) {
    // Track active filters across multiple categories
    if (!window.activeFilters) {
      window.activeFilters = { year: "all", topic: null, type: null };
    }

    // Determine which filter category this is
    const filterButton = document.querySelector(
      `[data-filter="${filterType}"]`
    );
    const isYearFilter =
      filterButton && filterButton.classList.contains("filter-link");
    const isTopicFilter =
      filterButton && filterButton.classList.contains("filter-topic");
    const isTypeFilter =
      filterButton && filterButton.classList.contains("filter-type");

    // Update active filters
    if (isYearFilter) {
      window.activeFilters.year = filterType;
    } else if (isTopicFilter) {
      // Toggle topic filter (can be deselected)
      window.activeFilters.topic =
        window.activeFilters.topic === filterType ? null : filterType;
    } else if (isTypeFilter) {
      // Toggle type filter (can be deselected)
      window.activeFilters.type =
        window.activeFilters.type === filterType ? null : filterType;
    }

    // Update button states
    updateFilterButtonStates();

    let visibleCount = 0;

    publications.forEach((pub, index) => {
      const pubText = pub.textContent.toLowerCase();

      // Get the year from the heading
      const year = getPublicationYear(pub);

      // Check all active filters
      const passesYearFilter = checkYearFilter(year, window.activeFilters.year);
      const passesTopicFilter =
        !window.activeFilters.topic ||
        checkTopicFilter(pubText, window.activeFilters.topic);
      const passesTypeFilter =
        !window.activeFilters.type ||
        checkTypeFilter(pubText, window.activeFilters.type);

      const shouldShow =
        passesYearFilter && passesTopicFilter && passesTypeFilter;

      // Show or hide publication with animation
      if (shouldShow) {
        pub.style.display = "block";
        pub.style.opacity = "0";
        pub.style.transform = "translateY(20px)";

        setTimeout(() => {
          pub.style.transition = "all 0.3s ease";
          pub.style.opacity = "1";
          pub.style.transform = "translateY(0)";
        }, visibleCount * 30);

        visibleCount++;
      } else {
        pub.style.transition = "all 0.2s ease";
        pub.style.opacity = "0";
        pub.style.transform = "translateY(-10px)";

        setTimeout(() => {
          pub.style.display = "none";
        }, 200);
      }
    });

    // Handle year headings
    updateYearHeadings();

    // Show no results message if needed
    showNoResultsMessage(visibleCount);
  }

  function getPublicationYear(pub) {
    let element = pub;
    while (element && element.previousElementSibling) {
      element = element.previousElementSibling;
      if (element.tagName === "H3") {
        return element.textContent.trim();
      }
      if (element.tagName === "UL") {
        let prevElement = element.previousElementSibling;
        while (prevElement) {
          if (prevElement.tagName === "H3") {
            return prevElement.textContent.trim();
          }
          prevElement = prevElement.previousElementSibling;
        }
        break;
      }
    }
    return "";
  }

  function checkYearFilter(year, yearFilter) {
    switch (yearFilter) {
      case "all":
        return true;
      case "recent":
        return year === "2024" || year === "2025";
      case "2020-2023":
        return ["2020", "2021", "2022", "2023"].includes(year);
      case "2016-2019":
        return ["2016", "2017", "2018", "2019"].includes(year);
      case "before-2016":
        const yearNum = parseInt(year);
        return yearNum && yearNum < 2016;
      default:
        return year === yearFilter;
    }
  }

  function checkTopicFilter(text, topicFilter) {
    switch (topicFilter) {
      case "ai-ml":
        return (
          text.includes("neural") ||
          text.includes("learning") ||
          text.includes("ai") ||
          text.includes("machine learning") ||
          text.includes("reinforcement") ||
          text.includes("gnn") ||
          text.includes("cognitive") ||
          text.includes("intelligence") ||
          text.includes("deep") ||
          text.includes("network")
        );
      case "swarm":
        return (
          text.includes("swarm") ||
          text.includes("multi-robot") ||
          text.includes("collective") ||
          text.includes("decentralized") ||
          text.includes("distributed") ||
          text.includes("consensus")
        );
      case "vision":
        return (
          text.includes("vision") ||
          text.includes("visual") ||
          text.includes("camera") ||
          text.includes("event-based") ||
          text.includes("perception") ||
          text.includes("image")
        );
      case "aerospace":
        return (
          text.includes("space") ||
          text.includes("satellite") ||
          text.includes("aerospace") ||
          text.includes("spacecraft") ||
          text.includes("exploration") ||
          text.includes("darpa") ||
          text.includes("orbit") ||
          text.includes("mission")
        );
      case "safety":
        return (
          text.includes("safety") ||
          text.includes("control barrier") ||
          text.includes("guardrails") ||
          text.includes("secure") ||
          text.includes("fault") ||
          text.includes("robust")
        );
      case "hri":
        return (
          text.includes("human") ||
          text.includes("worker") ||
          text.includes("interaction") ||
          text.includes("user") ||
          text.includes("interdisciplinary") ||
          text.includes("cognitive")
        );
      case "robotics":
        return (
          text.includes("robot") ||
          text.includes("robotic") ||
          text.includes("autonomous") ||
          text.includes("manipulation") ||
          text.includes("navigation") ||
          text.includes("planning") ||
          text.includes("control")
        );
      default:
        return true;
    }
  }

  function checkTypeFilter(text, typeFilter) {
    switch (typeFilter) {
      case "conference":
        return (
          text.includes("conference") ||
          text.includes("proceedings") ||
          text.includes("symposium") ||
          text.includes("workshop")
        );
      case "journal":
        return (
          text.includes("journal") ||
          text.includes("transactions") ||
          text.includes("letters") ||
          text.includes("magazine") ||
          text.includes("ieee") ||
          text.includes("acm")
        );
      case "workshop":
        return (
          text.includes("workshop") ||
          text.includes("arxiv") ||
          text.includes("preprint") ||
          text.includes("misc")
        );
      default:
        return true;
    }
  }

  function updateFilterButtonStates() {
    // Clear all active states except year filter
    document
      .querySelectorAll(".filter-topic, .filter-type")
      .forEach((btn) => btn.classList.remove("active"));

    // Set active states based on current filters
    if (window.activeFilters.topic) {
      const topicBtn = document.querySelector(
        `[data-filter="${window.activeFilters.topic}"].filter-topic`
      );
      if (topicBtn) topicBtn.classList.add("active");
    }

    if (window.activeFilters.type) {
      const typeBtn = document.querySelector(
        `[data-filter="${window.activeFilters.type}"].filter-type`
      );
      if (typeBtn) typeBtn.classList.add("active");
    }
  }

  function updateYearHeadings() {
    const yearHeadings = document.querySelectorAll(".publications-content h3");
    yearHeadings.forEach((heading) => {
      const nextElement = heading.nextElementSibling;
      if (nextElement && nextElement.tagName === "UL") {
        const yearPubs = nextElement.querySelectorAll(".publication");
        let hasVisiblePubs = false;

        yearPubs.forEach((pub) => {
          if (pub.style.display !== "none") {
            hasVisiblePubs = true;
          }
        });

        heading.style.display = hasVisiblePubs ? "block" : "none";
      }
    });
  }

  function showNoResultsMessage(visibleCount) {
    let noResultsMsg = document.querySelector(".no-publications-message");

    if (visibleCount === 0) {
      if (!noResultsMsg) {
        noResultsMsg = document.createElement("div");
        noResultsMsg.className = "no-publications-message";
        noResultsMsg.innerHTML = `
          <div style="text-align: center; padding: 4rem 2rem; color: #6b7280; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 20px; margin-top: 2rem; border: 2px dashed var(--space-teal);">
            <i class="fa fa-search" style="font-size: 4rem; margin-bottom: 1.5rem; color: var(--space-teal); opacity: 0.6;"></i>
            <h3 style="color: var(--space-navy); margin-bottom: 1rem; font-size: 1.5rem;">No publications found</h3>
            <p style="font-size: 1.1rem; margin-bottom: 2rem; color: #64748b;">Your current filters don't match any publications. Try adjusting your selection or clear all filters.</p>
            <button onclick="clearAllFilters()" class="btn-modern btn-modern-primary" style="padding: 12px 30px; font-size: 1rem;">
              <i class="fa fa-refresh"></i> Clear All Filters
            </button>
          </div>
        `;
        document
          .querySelector(".publications-content")
          .appendChild(noResultsMsg);
      }
      noResultsMsg.style.display = "block";
    } else if (noResultsMsg) {
      noResultsMsg.style.display = "none";
    }
  }

  // Utility functions
  function debounce(func, wait, immediate) {
    let timeout;
    return function () {
      const context = this;
      const args = arguments;
      const later = function () {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      const callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
    };
  }

  function throttle(func, limit) {
    let inThrottle;
    return function () {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => (inThrottle = false), limit);
      }
    };
  }

  // Global clear all filters function
  window.clearAllFilters = function () {
    // Reset all filter states
    window.activeFilters = { year: "all", topic: null, type: null };

    // Reset all filter buttons
    document
      .querySelectorAll(".filter-link, .filter-topic, .filter-type")
      .forEach((btn) => btn.classList.remove("active"));
    const allButton = document.querySelector('.filter-link[data-filter="all"]');
    if (allButton) allButton.classList.add("active");

    // Show all publications
    const publications = document.querySelectorAll(".publication");
    publications.forEach((pub, index) => {
      pub.style.display = "block";
      pub.style.opacity = "0";
      pub.style.transform = "translateY(20px)";

      setTimeout(() => {
        pub.style.transition = "all 0.3s ease";
        pub.style.opacity = "1";
        pub.style.transform = "translateY(0)";
      }, index * 20);
    });

    // Show all year headings
    const yearHeadings = document.querySelectorAll(".publications-content h3");
    yearHeadings.forEach((heading) => {
      heading.style.display = "block";
    });

    // Remove no results message
    const noResultsMsg = document.querySelector(".no-publications-message");
    if (noResultsMsg) {
      noResultsMsg.remove();
    }
  };

  // Export utilities for global use
  window.MISTLab = {
    debounce: debounce,
    throttle: throttle,
    filterPublications: filterPublications,
    clearAllFilters: window.clearAllFilters,
  };
})();
