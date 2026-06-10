/**
 * PoweraFix - Main JavaScript
 * Handles all interactive functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initMobileMenu();
    initDropdowns();
    initBeforeAfterSlider();
    initGalleryLightbox();
    initGalleryFilter();
    initFAQ();
    initContactForm();
    initSmoothScroll();
    initScrollAnimations();
    initStickyNavbar();
});

/**
 * Navbar functionality
 */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    // Add scrolled class on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

/**
 * Mobile menu toggle
 */
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');
    
    if (!mobileMenuBtn || !navMenu) return;

    mobileMenuBtn.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
        document.body.classList.toggle('menu-open');
    });

    // Close menu when clicking on a link
    const navLinks = navMenu.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            mobileMenuBtn.classList.remove('active');
            document.body.classList.remove('menu-open');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!navbar.contains(e.target) && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            mobileMenuBtn.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    });
}

/**
 * Dropdown menus
 */
function initDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('.nav-link');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (!link || !menu) return;

        // Toggle on click for mobile
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 1024) {
                e.preventDefault();
                dropdown.classList.toggle('active');
            }
        });

        // Show on hover for desktop
        dropdown.addEventListener('mouseenter', function() {
            if (window.innerWidth > 1024) {
                menu.style.opacity = '1';
                menu.style.visibility = 'visible';
                menu.style.transform = 'translateY(0)';
            }
        });

        dropdown.addEventListener('mouseleave', function() {
            if (window.innerWidth > 1024) {
                menu.style.opacity = '0';
                menu.style.visibility = 'hidden';
                menu.style.transform = 'translateY(10px)';
            }
        });
    });
}

/**
 * Before/After image slider
 */
function initBeforeAfterSlider() {
    const sliders = document.querySelectorAll('.before-after-slider');
    
    sliders.forEach(slider => {
        const handle = slider.querySelector('.slider-handle');
        const afterImage = slider.querySelector('.after-image');
        
        if (!handle || !afterImage) return;

        let isDragging = false;

        const updateSlider = (x) => {
            const rect = slider.getBoundingClientRect();
            let percentage = ((x - rect.left) / rect.width) * 100;
            percentage = Math.max(0, Math.min(100, percentage));
            
            afterImage.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
            handle.style.left = `${percentage}%`;
        };

        // Mouse events
        handle.addEventListener('mousedown', () => isDragging = true);
        document.addEventListener('mouseup', () => isDragging = false);
        document.addEventListener('mousemove', (e) => {
            if (isDragging) updateSlider(e.clientX);
        });

        // Touch events
        handle.addEventListener('touchstart', () => isDragging = true);
        document.addEventListener('touchend', () => isDragging = false);
        document.addEventListener('touchmove', (e) => {
            if (isDragging) updateSlider(e.touches[0].clientX);
        });

        // Click to position
        slider.addEventListener('click', (e) => {
            updateSlider(e.clientX);
        });
    });
}

/**
 * Gallery lightbox
 */
function initGalleryLightbox() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox');
    
    if (!lightbox) return;

    const lightboxImage = document.getElementById('lightboxImage');
    const lightboxCaption = document.getElementById('lightboxCaption');
    const lightboxClose = document.getElementById('lightboxClose');
    const lightboxPrev = document.getElementById('lightboxPrev');
    const lightboxNext = document.getElementById('lightboxNext');

    let currentIndex = 0;
    const items = Array.from(galleryItems);

    const openLightbox = (index) => {
        currentIndex = index;
        const item = items[index];
        const img = item.querySelector('img');
        const title = item.querySelector('.gallery-title');
        
        lightboxImage.src = img.src;
        lightboxImage.alt = img.alt;
        lightboxCaption.textContent = title ? title.textContent : '';
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    const closeLightbox = () => {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    };

    const showPrev = () => {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        openLightbox(currentIndex);
    };

    const showNext = () => {
        currentIndex = (currentIndex + 1) % items.length;
        openLightbox(currentIndex);
    };

    // Open lightbox on click
    items.forEach((item, index) => {
        item.addEventListener('click', () => openLightbox(index));
    });

    // Close lightbox
    lightboxClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
    });

    // Navigation
    lightboxPrev.addEventListener('click', showPrev);
    lightboxNext.addEventListener('click', showNext);

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') showPrev();
        if (e.key === 'ArrowRight') showNext();
    });
}

/**
 * Gallery filter
 */
function initGalleryFilter() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    if (filterBtns.length === 0 || galleryItems.length === 0) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const filter = this.dataset.filter;
            
            // Update active button
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Filter items
            galleryItems.forEach(item => {
                const category = item.dataset.category;
                
                if (filter === 'all' || category === filter) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeIn 0.5s ease';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

/**
 * FAQ accordion
 */
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const icon = item.querySelector('.faq-icon');
        
        if (!question || !answer) return;

        question.addEventListener('click', function() {
            const isOpen = this.getAttribute('aria-expanded') === 'true';
            
            // Close all other items
            faqItems.forEach(otherItem => {
                const otherQuestion = otherItem.querySelector('.faq-question');
                const otherAnswer = otherItem.querySelector('.faq-answer');
                const otherIcon = otherItem.querySelector('.faq-icon');
                
                otherQuestion.setAttribute('aria-expanded', 'false');
                otherAnswer.style.maxHeight = '0';
                otherAnswer.style.padding = '0 20px';
                if (otherIcon) otherIcon.textContent = '+';
            });
            
            // Toggle current item
            if (!isOpen) {
                this.setAttribute('aria-expanded', 'true');
                answer.style.maxHeight = answer.scrollHeight + 'px';
                answer.style.padding = '20px';
                if (icon) icon.textContent = '−';
            }
        });
    });
}

/**
 * Contact form handling
 */
function initContactForm() {
    const form = document.getElementById('contactForm');
    
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Basic validation
        if (!data.firstName || !data.lastName || !data.email || !data.message) {
            showNotification('Täytä kaikki pakolliset kentät', 'error');
            return;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            showNotification('Anna kelvollinen sähköpostiosoite', 'error');
            return;
        }
        
        // Simulate form submission
        showNotification('Viesti lähetetty! Otamme yhteyttä pian.', 'success');
        form.reset();
        
        // In production, you would send this data to your server
        console.log('Form data:', data);
    });
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-message">${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 16px 24px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 12px;
        animation: slideIn 0.3s ease;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
    `;
    
    document.body.appendChild(notification);
    
    // Close button
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.remove();
    });
    
    // Auto remove
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

/**
 * Smooth scroll for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Scroll animations
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.service-card, .pricing-card, .value-card, .team-card, .testimonial-card, .gallery-item');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Add animation class styles
document.head.insertAdjacentHTML('beforeend', `
    <style>
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
    </style>
`);

/**
 * Sticky navbar on scroll
 */
function initStickyNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.scrollY;
        
        // Add/remove scrolled class
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Hide/show on scroll direction
        if (currentScroll > lastScroll && currentScroll > 200) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScroll = currentScroll;
    });
}

/**
 * Lazy loading for images
 */
if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
}

/**
 * Parallax effect for hero sections
 */
function initParallax() {
    const heroSections = document.querySelectorAll('.hero, .service-hero');
    
    window.addEventListener('scroll', function() {
        const scrolled = window.scrollY;
        
        heroSections.forEach(hero => {
            const rate = scrolled * 0.3;
            hero.style.backgroundPositionY = `${rate}px`;
        });
    });
}

// Initialize parallax if not on mobile
if (window.matchMedia('(min-width: 768px)').matches) {
    initParallax();
}

/**
 * Counter animation for stats
 */
function animateCounters() {
    const counters = document.querySelectorAll('.about-stat-number, .stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current) + '+';
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target + '+';
            }
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(counter);
                }
            });
        });
        
        observer.observe(counter);
    });
}

// Initialize counter animation
animateCounters();
