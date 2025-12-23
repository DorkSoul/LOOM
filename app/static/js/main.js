// LOOM - Main JavaScript

// Sidebar Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const mainContent = document.querySelector('.main-content');

    // Check if we're on mobile
    function isMobile() {
        return window.innerWidth <= 768;
    }

    // Initialize sidebar state
    function initializeSidebar() {
        if (isMobile()) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('expanded');
        } else {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('expanded');
        }
    }

    // Toggle sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('collapsed');
        sidebar.classList.toggle('active');
        sidebarToggle.classList.toggle('active');
        mainContent.classList.toggle('expanded');

        // Show/hide overlay on mobile
        if (isMobile()) {
            sidebarOverlay.classList.toggle('active');
        }
    }

    // Event listeners
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            if (isMobile()) {
                toggleSidebar();
            }
        });
    }

    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(initializeSidebar, 250);
    });

    // Initialize on page load
    initializeSidebar();

    // Close sidebar when clicking a link on mobile
    const sidebarLinks = sidebar.querySelectorAll('.sidebar-menu a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (isMobile() && sidebar.classList.contains('active')) {
                toggleSidebar();
            }
        });
    });
});

// Utility function for API calls
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Format date utilities
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Show notification (can be enhanced with a toast library)
function showNotification(message, type = 'info') {
    alert(message); // Simple implementation, can be replaced with toast library
}

// Confirm action
function confirmAction(message) {
    return confirm(message);
}

// Export utilities
window.loom = {
    apiCall,
    formatDate,
    formatDateTime,
    showNotification,
    confirmAction
};
