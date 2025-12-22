// LOOM - Main JavaScript

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
