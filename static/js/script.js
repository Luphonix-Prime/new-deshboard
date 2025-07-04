/**
 * CyberSecure Framework Dashboard
 * Interactive functionality for the cybersecurity framework dashboard
 */

// Global state
let searchTerm = '';
let expandedFrameworks = new Set();
let allSections = [];

// DOM elements
const searchInput = document.getElementById('search-input');
const clearButton = document.getElementById('clear-search');
const searchStats = document.getElementById('search-stats');
const noResults = document.getElementById('no-results');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    setupEventListeners();
    indexAllSections();
    updateSearchStats();
    
    // Add loading completion
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 100);
});

/**
 * Theme management
 */
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

/**
 * Event listeners setup
 */
function setupEventListeners() {
    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);
    
    // Search functionality
    searchInput.addEventListener('input', handleSearch);
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            clearSearch();
        }
    });
    
    clearButton.addEventListener('click', clearSearch);
    
    // Framework expansion state persistence
    window.addEventListener('beforeunload', saveExpandedState);
    loadExpandedState();
}

/**
 * Search functionality
 */
function handleSearch(e) {
    searchTerm = e.target.value.toLowerCase().trim();
    
    if (searchTerm) {
        clearButton.style.display = 'block';
        performSearch();
    } else {
        clearSearch();
    }
}

function performSearch() {
    const frameworks = document.querySelectorAll('.framework-card');
    let totalMatches = 0;
    let frameworksWithMatches = 0;
    
    frameworks.forEach(framework => {
        const sections = framework.querySelectorAll('.section-card');
        const frameworkTitle = framework.querySelector('.framework-details h2').textContent.toLowerCase();
        const frameworkDescription = framework.querySelector('.framework-description').textContent.toLowerCase();
        let frameworkMatches = 0;
        
        // Check if framework name or description matches
        const frameworkNameMatch = frameworkTitle.includes(searchTerm) || frameworkDescription.includes(searchTerm);
        
        sections.forEach(section => {
            const sectionTitle = section.querySelector('.section-header h3').textContent.toLowerCase();
            const sectionDescription = section.querySelector('.section-description').textContent.toLowerCase();
            const controlTags = section.querySelectorAll('.control-tag');
            
            let sectionMatch = sectionTitle.includes(searchTerm) || 
                             sectionDescription.includes(searchTerm) ||
                             frameworkNameMatch;
            
            // Check individual control tags
            let controlMatches = 0;
            controlTags.forEach(tag => {
                const controlText = tag.textContent.toLowerCase();
                if (controlText.includes(searchTerm) || frameworkNameMatch) {
                    tag.style.display = 'block';
                    tag.classList.add('highlighted');
                    highlightSearchTerm(tag, searchTerm);
                    sectionMatch = true;
                    controlMatches++;
                } else {
                    tag.style.display = 'none';
                    tag.classList.remove('highlighted');
                }
            });
            
            if (sectionMatch) {
                section.style.display = 'block';
                section.classList.add('highlighted');
                frameworkMatches++;
                totalMatches++;
                
                // Highlight section title and description
                highlightSearchTerm(section.querySelector('.section-header h3'), searchTerm);
                highlightSearchTerm(section.querySelector('.section-description'), searchTerm);
            } else {
                section.style.display = 'none';
                section.classList.remove('highlighted');
            }
        });
        
        if (frameworkMatches > 0 || frameworkNameMatch) {
            framework.style.display = 'block';
            frameworksWithMatches++;
            
            // Auto-expand frameworks with matches
            if (!framework.classList.contains('expanded')) {
                const frameworkId = framework.getAttribute('data-framework');
                toggleFramework(frameworkId);
            }
            
            // Highlight framework title
            if (frameworkNameMatch) {
                highlightSearchTerm(framework.querySelector('.framework-details h2'), searchTerm);
                highlightSearchTerm(framework.querySelector('.framework-description'), searchTerm);
            }
        } else {
            framework.style.display = 'none';
        }
    });
    
    updateSearchStats(totalMatches, frameworksWithMatches);
    
    // Show no results if nothing found
    noResults.style.display = totalMatches === 0 ? 'block' : 'none';
}

function highlightSearchTerm(element, term) {
    if (!element || !term) return;
    
    const originalText = element.getAttribute('data-original') || element.textContent;
    element.setAttribute('data-original', originalText);
    
    const regex = new RegExp(`(${escapeRegex(term)})`, 'gi');
    const highlightedText = originalText.replace(regex, '<mark style="background: var(--warning-color); color: white; padding: 2px 4px; border-radius: 4px;">$1</mark>');
    element.innerHTML = highlightedText;
}

function removeHighlights() {
    const highlightedElements = document.querySelectorAll('[data-original]');
    highlightedElements.forEach(element => {
        const originalText = element.getAttribute('data-original');
        element.textContent = originalText;
        element.removeAttribute('data-original');
    });
}

function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function clearSearch() {
    searchInput.value = '';
    searchTerm = '';
    clearButton.style.display = 'none';
    
    // Reset all visibility and highlights
    const frameworks = document.querySelectorAll('.framework-card');
    const sections = document.querySelectorAll('.section-card');
    const controlTags = document.querySelectorAll('.control-tag');
    
    frameworks.forEach(framework => {
        framework.style.display = 'block';
    });
    
    sections.forEach(section => {
        section.style.display = 'block';
        section.classList.remove('highlighted');
    });
    
    controlTags.forEach(tag => {
        tag.style.display = 'block';
        tag.classList.remove('highlighted');
    });
    
    removeHighlights();
    noResults.style.display = 'none';
    updateSearchStats();
    
    searchInput.focus();
}

function updateSearchStats(matches = null, frameworks = null) {
    if (matches !== null && frameworks !== null) {
        if (matches === 0) {
            searchStats.textContent = 'No sections found';
        } else if (matches === 1) {
            searchStats.textContent = `Found 1 section across ${frameworks} framework${frameworks !== 1 ? 's' : ''}`;
        } else {
            searchStats.textContent = `Found ${matches} sections across ${frameworks} framework${frameworks !== 1 ? 's' : ''}`;
        }
    } else {
        const totalSections = allSections.length;
        const totalFrameworks = document.querySelectorAll('.framework-card').length;
        searchStats.textContent = `${totalSections} sections across ${totalFrameworks} frameworks`;
    }
}

/**
 * Framework accordion functionality
 */
function toggleFramework(frameworkId) {
    const framework = document.querySelector(`[data-framework="${frameworkId}"]`);
    const content = document.getElementById(`content-${frameworkId}`);
    
    if (!framework || !content) return;
    
    const isExpanded = framework.classList.contains('expanded');
    
    if (isExpanded) {
        framework.classList.remove('expanded');
        expandedFrameworks.delete(frameworkId);
    } else {
        framework.classList.add('expanded');
        expandedFrameworks.add(frameworkId);
    }
    
    // Smooth scroll to framework if expanding
    if (!isExpanded) {
        setTimeout(() => {
            framework.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest'
            });
        }, 200);
    }
}

/**
 * State persistence
 */
function saveExpandedState() {
    localStorage.setItem('expandedFrameworks', JSON.stringify([...expandedFrameworks]));
}

function loadExpandedState() {
    try {
        const saved = localStorage.getItem('expandedFrameworks');
        if (saved) {
            const frameworks = JSON.parse(saved);
            frameworks.forEach(frameworkId => {
                toggleFramework(frameworkId);
            });
        }
    } catch (e) {
        console.warn('Could not load expanded state:', e);
    }
}

/**
 * Section indexing for search
 */
function indexAllSections() {
    const sections = document.querySelectorAll('.section-card');
    allSections = Array.from(sections).map(section => ({
        element: section,
        title: section.querySelector('.section-header h3').textContent.toLowerCase(),
        description: section.querySelector('.section-description').textContent.toLowerCase(),
        framework: section.closest('.framework-card').getAttribute('data-framework'),
        controls: Array.from(section.querySelectorAll('.control-tag')).map(tag => tag.textContent.toLowerCase())
    }));
}

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
    }
    
    // Ctrl/Cmd + / to toggle theme
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        toggleTheme();
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        if (document.activeElement === searchInput) {
            clearSearch();
        }
    }
});

/**
 * Utility functions
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Performance optimization for search
const debouncedSearch = debounce(performSearch, 200);

// Replace direct performSearch calls with debounced version for better performance
searchInput.addEventListener('input', function(e) {
    searchTerm = e.target.value.toLowerCase().trim();
    
    if (searchTerm) {
        clearButton.style.display = 'block';
        debouncedSearch();
    } else {
        clearSearch();
    }
});

// Export functions for global access (needed for onclick handlers)
window.toggleFramework = toggleFramework;

// Add loading state management
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Enhanced accessibility
document.addEventListener('keydown', function(e) {
    // Enter key on framework headers
    if (e.key === 'Enter' && e.target.closest('.framework-header')) {
        const frameworkCard = e.target.closest('.framework-card');
        const frameworkId = frameworkCard.getAttribute('data-framework');
        toggleFramework(frameworkId);
    }
});

// Add focus management for framework headers
document.querySelectorAll('.framework-header').forEach(header => {
    header.setAttribute('tabindex', '0');
    header.setAttribute('role', 'button');
    header.setAttribute('aria-expanded', 'false');
    
    header.addEventListener('click', function() {
        const isExpanded = this.closest('.framework-card').classList.contains('expanded');
        this.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
    });
});

// Console welcome message for developers
console.log(`
🔐 CyberSecure Framework Dashboard
Built with security professionals in mind.

Keyboard shortcuts:
- Ctrl/Cmd + K: Focus search
- Ctrl/Cmd + /: Toggle theme
- Escape: Clear search
- Enter: Expand/collapse framework (when focused)

Frameworks included: NIST CSF, ISO/IEC 27001/27005, COBIT 2019, RBI Cybersecurity, PCI-DSS v4.0, HIPAA, ISO 27001 (Enterprise/SaaS), CERT-IN
`);