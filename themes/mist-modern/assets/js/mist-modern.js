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

    // Mobile navigation enhancements
    initMobileNavigation();

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

  function initMobileNavigation() {
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navLinks = document.querySelectorAll('.navbar-nav a');

    if (!navbarToggle || !navbarCollapse) return;

    // Ensure proper Bootstrap data attributes
    navbarToggle.setAttribute('data-toggle', 'collapse');
    navbarToggle.setAttribute('data-target', '.navbar-ex1-collapse');
    navbarToggle.setAttribute('aria-expanded', 'false');
    navbarToggle.setAttribute('aria-controls', 'navbar-collapse');

    // Function to collapse navbar
    function collapseNavbar() {
      if (navbarCollapse.classList.contains('in')) {
        navbarCollapse.classList.remove('in');
        navbarToggle.setAttribute('aria-expanded', 'false');
        navbarToggle.classList.remove('collapsed');
      }
    }

    // Function to toggle navbar
    function toggleNavbar() {
      const isExpanded = navbarCollapse.classList.contains('in');
      
      if (isExpanded) {
        navbarCollapse.classList.remove('in');
        navbarToggle.setAttribute('aria-expanded', 'false');
        navbarToggle.classList.add('collapsed');
      } else {
        navbarCollapse.classList.add('in');
        navbarToggle.setAttribute('aria-expanded', 'true');
        navbarToggle.classList.remove('collapsed');
      }
    }

    // Handle toggle button clicks
    navbarToggle.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      toggleNavbar();
    });

    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        // Only close if it's a valid navigation link and we're on mobile
        if (window.innerWidth < 768 && !link.getAttribute('href').startsWith('#')) {
          setTimeout(collapseNavbar, 100); // Small delay to ensure smooth transition
        }
      });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
      if (window.innerWidth < 768 && 
          navbarCollapse.classList.contains('in') && 
          !navbarCollapse.contains(e.target) && 
          !navbarToggle.contains(e.target) &&
          !e.target.closest('.navbar')) {
        collapseNavbar();
      }
    });

    // Improve toggle button accessibility
    navbarToggle.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        e.stopPropagation();
        toggleNavbar();
      }
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navbarCollapse.classList.contains('in')) {
        collapseNavbar();
      }
    });

    // Close menu when window is resized to desktop
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 768 && navbarCollapse.classList.contains('in')) {
        collapseNavbar();
      }
    });

    // Ensure proper initial state
    if (window.innerWidth >= 768) {
      navbarCollapse.classList.remove('in');
      navbarToggle.setAttribute('aria-expanded', 'false');
    }
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
