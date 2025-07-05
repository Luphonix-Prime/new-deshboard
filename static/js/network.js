class NetworkAnimation {
    constructor() {
        this.canvas = document.getElementById('network-bg');
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.connections = [];
        this.mouse = { x: 0, y: 0 };
        this.animationId = null;
        this.isHovering = false;
        this.nodes = [];

        this.init();
        this.setupEventListeners();
        this.animate();
        this.setupInteractiveEffects();
    }

    init() {
        this.resizeCanvas();
        this.createParticles();
        this.createNetworkNodes();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        const particleCount = Math.floor((this.canvas.width * this.canvas.height) / 12000);
        this.particles = [];

        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.8,
                vy: (Math.random() - 0.5) * 0.8,
                radius: Math.random() * 2 + 1,
                opacity: Math.random() * 0.6 + 0.2,
                baseOpacity: Math.random() * 0.6 + 0.2,
                pulse: Math.random() * Math.PI * 2,
                pulseSpeed: 0.02 + Math.random() * 0.02
            });
        }
    }

    createNetworkNodes() {
        const nodeCount = Math.floor((this.canvas.width * this.canvas.height) / 80000) + 8;
        this.nodes = [];

        for (let i = 0; i < nodeCount; i++) {
            this.nodes.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 4 + 3,
                opacity: 0.7,
                connections: [],
                pulse: Math.random() * Math.PI * 2,
                pulseSpeed: 0.015 + Math.random() * 0.01
            });
        }
    }

    setupEventListeners() {
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.createParticles();
            this.createNetworkNodes();
        });

        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
            this.isHovering = true;

            // Create mouse trail particles
            if (Math.random() < 0.3) {
                this.particles.push({
                    x: this.mouse.x + (Math.random() - 0.5) * 20,
                    y: this.mouse.y + (Math.random() - 0.5) * 20,
                    vx: (Math.random() - 0.5) * 2,
                    vy: (Math.random() - 0.5) * 2,
                    radius: Math.random() * 2 + 1,
                    opacity: 0.8,
                    life: 60,
                    maxLife: 60,
                    isMouse: true
                });
            }
        });

        window.addEventListener('mouseleave', () => {
            this.isHovering = false;
        });
    }

    setupInteractiveEffects() {
        // Framework and control card hover effects
        const cards = document.querySelectorAll('.framework-card, .control-item, .feature-card, .dashboard-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.createHoverEffect(card);
            });

            card.addEventListener('click', () => {
                this.createClickRipple(card);
            });
        });

        // Button click effects
        const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-success');
        buttons.forEach(button => {
            button.addEventListener('click', () => {
                this.createButtonBurst(button);
            });
        });

        // Form submission effects
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', () => {
                this.createFormSubmissionWave();
            });
        });
    }

    updateParticles() {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const particle = this.particles[i];

            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;

            // Update pulse effect
            if (particle.pulse !== undefined) {
                particle.pulse += particle.pulseSpeed || 0.02;
                particle.opacity = particle.baseOpacity + Math.sin(particle.pulse) * 0.3;
            }

            // Handle special particle types
            if (particle.life !== undefined) {
                particle.life--;
                particle.opacity = (particle.life / particle.maxLife) * 0.8;

                if (particle.life <= 0) {
                    this.particles.splice(i, 1);
                    continue;
                }
            }

            // Mouse interaction effect
            if (this.isHovering) {
                const dx = this.mouse.x - particle.x;
                const dy = this.mouse.y - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) {
                    const force = (100 - distance) / 100;
                    particle.vx += (dx / distance) * force * 0.02;
                    particle.vy += (dy / distance) * force * 0.02;
                    particle.opacity = Math.min(1, particle.opacity + force * 0.5);
                }
            }

            // Boundary checking with wrap-around
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;

            // Velocity damping
            particle.vx *= 0.999;
            particle.vy *= 0.999;
        }
    }

    updateNodes() {
        for (let i = 0; i < this.nodes.length; i++) {
            const node = this.nodes[i];

            // Update position
            node.x += node.vx;
            node.y += node.vy;

            // Update pulse
            node.pulse += node.pulseSpeed;
            node.opacity = 0.7 + Math.sin(node.pulse) * 0.3;

            // Boundary checking
            if (node.x < 0 || node.x > this.canvas.width) node.vx *= -1;
            if (node.y < 0 || node.y > this.canvas.height) node.vy *= -1;

            // Keep nodes within bounds
            node.x = Math.max(0, Math.min(this.canvas.width, node.x));
            node.y = Math.max(0, Math.min(this.canvas.height, node.y));
        }
    }

    drawConnections() {
        this.ctx.strokeStyle = 'rgba(139, 92, 246, 0.2)';
        this.ctx.lineWidth = 1;

        // Connect nearby nodes
        for (let i = 0; i < this.nodes.length; i++) {
            for (let j = i + 1; j < this.nodes.length; j++) {
                const dx = this.nodes[i].x - this.nodes[j].x;
                const dy = this.nodes[i].y - this.nodes[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 150) {
                    const opacity = (150 - distance) / 150 * 0.5;
                    this.ctx.strokeStyle = `rgba(139, 92, 246, ${opacity})`;
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.nodes[i].x, this.nodes[i].y);
                    this.ctx.lineTo(this.nodes[j].x, this.nodes[j].y);
                    this.ctx.stroke();
                }
            }
        }

        // Connect particles to nearby nodes
        this.particles.forEach(particle => {
            this.nodes.forEach(node => {
                const dx = particle.x - node.x;
                const dy = particle.y - node.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 80) {
                    const opacity = (80 - distance) / 80 * 0.3;
                    this.ctx.strokeStyle = `rgba(192, 132, 252, ${opacity})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(node.x, node.y);
                    this.ctx.stroke();
                }
            });
        });
    }

    drawParticles() {
        this.particles.forEach(particle => {
            this.ctx.globalAlpha = particle.opacity;

            // Different colors for different particle types
            if (particle.isMouse) {
                this.ctx.fillStyle = '#c084fc';
                this.ctx.shadowColor = '#c084fc';
                this.ctx.shadowBlur = 15;
            } else if (particle.isBurst) {
                this.ctx.fillStyle = '#a855f7';
                this.ctx.shadowColor = '#a855f7';
                this.ctx.shadowBlur = 12;
            } else {
                this.ctx.fillStyle = '#8b5cf6';
                this.ctx.shadowColor = '#8b5cf6';
                this.ctx.shadowBlur = 8;
            }

            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.shadowBlur = 0;
        });
        this.ctx.globalAlpha = 1;
    }

    drawNodes() {
        this.nodes.forEach(node => {
            this.ctx.globalAlpha = node.opacity;
            this.ctx.fillStyle = '#6b3a96';
            this.ctx.shadowColor = '#6b3a96';
            this.ctx.shadowBlur = 20;

            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
            this.ctx.fill();

            // Inner glow
            this.ctx.globalAlpha = node.opacity * 0.5;
            this.ctx.fillStyle = '#c084fc';
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, node.radius * 0.6, 0, Math.PI * 2);
            this.ctx.fill();

            this.ctx.shadowBlur = 0;
        });
        this.ctx.globalAlpha = 1;
    }

    createHoverEffect(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        // Create hover particles
        for (let i = 0; i < 6; i++) {
            const angle = (i / 6) * Math.PI * 2;
            this.particles.push({
                x: centerX + Math.cos(angle) * 30,
                y: centerY + Math.sin(angle) * 30,
                vx: Math.cos(angle) * 2,
                vy: Math.sin(angle) * 2,
                radius: Math.random() * 2 + 1,
                opacity: 0.8,
                life: 40,
                maxLife: 40,
                isBurst: true
            });
        }
    }

    createClickRipple(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        // Create expanding ripple effect
        for (let i = 0; i < 12; i++) {
            const angle = (i / 12) * Math.PI * 2;
            this.particles.push({
                x: centerX,
                y: centerY,
                vx: Math.cos(angle) * 4,
                vy: Math.sin(angle) * 4,
                radius: Math.random() * 2 + 1,
                opacity: 1,
                life: 80,
                maxLife: 80,
                isBurst: true
            });
        }
    }

    createButtonBurst(button) {
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        // Create intense burst effect for buttons
        for (let i = 0; i < 20; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 5 + 2;
            this.particles.push({
                x: centerX,
                y: centerY,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                radius: Math.random() * 3 + 1,
                opacity: 1,
                life: 100,
                maxLife: 100,
                isBurst: true
            });
        }
    }

    createFormSubmissionWave() {
        // Create a wave effect across the screen
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: this.canvas.height + 50,
                vx: (Math.random() - 0.5) * 4,
                vy: -Math.random() * 6 - 2,
                radius: Math.random() * 3 + 2,
                opacity: 0.9,
                life: 120,
                maxLife: 120,
                isBurst: true
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.updateParticles();
        this.updateNodes();
        this.drawConnections();
        this.drawNodes();
        this.drawParticles();

        this.animationId = requestAnimationFrame(() => this.animate());
    }

    cleanup() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        window.removeEventListener('resize', this.resizeCanvas);
        window.removeEventListener('mousemove', this.setupEventListeners);
        window.removeEventListener('mouseleave', this.setupEventListeners);
    }
}

// Navbar scroll effects and smooth scrolling
class NavbarEffects {
    constructor() {
        this.navbar = document.querySelector('.navbar');
        this.lastScrollY = 0;
        this.isScrolling = false;

        this.init();
    }

    init() {
        this.setupScrollEffects();
        this.setupSmoothScrolling();
        this.setupIntersectionObserver();
    }

    setupScrollEffects() {
        let ticking = false;

        const updateNavbar = () => {
            const scrollY = window.pageYOffset || document.documentElement.scrollTop;

            if (scrollY > 50) {
                this.navbar.classList.add('scrolled');
                this.navbar.classList.remove('navbar-transparent');
                this.navbar.classList.add('navbar-solid');
            } else {
                this.navbar.classList.remove('scrolled');
                this.navbar.classList.add('navbar-transparent');
                this.navbar.classList.remove('navbar-solid');
            }

            // Navbar hide/show on scroll
            if (scrollY > this.lastScrollY && scrollY > 200) {
                this.navbar.style.transform = 'translateY(-100%)';
            } else {
                this.navbar.style.transform = 'translateY(0)';
            }

            this.lastScrollY = scrollY;
            ticking = false;
        };

        const requestTick = () => {
            if (!ticking) {
                requestAnimationFrame(updateNavbar);
                ticking = true;
            }
        };

        window.addEventListener('scroll', requestTick, { passive: true });

        // Initial state
        updateNavbar();
    }

    setupSmoothScrolling() {
        // Enhanced smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));

                if (target) {
                    const offsetTop = target.offsetTop - 120; // Account for fixed navbar

                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Smooth scrolling for step navigation
        document.querySelectorAll('.step').forEach(step => {
            step.addEventListener('click', () => {
                const targetSection = step.getAttribute('data-target');
                if (targetSection) {
                    const target = document.querySelector(targetSection);
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }

    setupIntersectionObserver() {
        // Intersection observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');

                    // Add staggered animation delays for grid items
                    const gridItems = entry.target.querySelectorAll('.framework-card, .control-item, .feature-card, .dashboard-card');
                    gridItems.forEach((item, index) => {
                        item.style.setProperty('--stagger-delay', index);
                        item.classList.add('animate-stagger');
                    });
                }
            });
        }, observerOptions);

        // Observe elements for scroll animations
        document.querySelectorAll('.frameworks-grid, .controls-grid, .features-grid, .dashboard-grid, .process-steps').forEach(el => {
            el.classList.add('animate-on-scroll');
            observer.observe(el);
        });
    }
}

// Initialize animation
let networkAnimation;
document.addEventListener('DOMContentLoaded', () => {
    if (networkAnimation) {
        networkAnimation.cleanup();
    }
    networkAnimation = new NetworkAnimation();
});

// Initialize navbar effects and network animation when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new NetworkAnimation();
    new NavbarEffects();

    // Add smooth scroll behavior to page load
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in-out';

    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Cleanup on page unload
window.addEventListener('unload', () => {
    if (networkAnimation) {
        networkAnimation.cleanup();
    }
});