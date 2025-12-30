/**
 * Notes Module - Google Keep style masonry layout
 */

let masonryGrid = null;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    loadNotes();
});

// Load notes from API
async function loadNotes() {
    try {
        const response = await window.loom.apiCall('/notes/api/notes', 'GET');
        renderNotes(response);
    } catch (error) {
        console.error('Error loading notes:', error);
    }
}

// Render notes with masonry layout
function renderNotes(notes) {
    const container = document.getElementById('notes-list');
    container.innerHTML = '';

    // Add grid sizer for masonry
    const sizer = document.createElement('div');
    sizer.className = 'grid-sizer';
    container.appendChild(sizer);

    // Render each note
    notes.forEach(note => {
        if (!note.is_archived) {
            container.appendChild(createNoteCard(note));
        }
    });

    // Initialize masonry
    initMasonry();
}

// Create note card element
function createNoteCard(note) {
    const card = document.createElement('div');
    card.className = 'note-card';

    // Random height between 150-600px (weighted toward smaller)
    const heights = [150, 200, 250, 300, 350, 400, 500, 600];
    const weights = [25, 20, 20, 15, 10, 5, 3, 2]; // Prefer smaller notes
    const height = getWeightedRandom(heights, weights);
    card.style.height = `${height}px`;

    // Build card content
    card.innerHTML = `
        ${note.is_pinned ? '<span class="pinned-badge">📌</span>' : ''}
        <h3>${escapeHtml(note.title)}</h3>
        <p>${escapeHtml(note.content || '').substring(0, 200)}</p>
        ${renderMeta(note)}
    `;

    return card;
}

// Render note metadata
function renderMeta(note) {
    let meta = '<div class="note-meta">';

    if (note.category) {
        meta += `<span class="category-badge">${escapeHtml(note.category)}</span>`;
    }

    if (note.tags && Array.isArray(note.tags) && note.tags.length > 0) {
        meta += '<div class="tags">';
        note.tags.forEach(tag => {
            meta += `<span class="tag">${escapeHtml(tag)}</span>`;
        });
        meta += '</div>';
    }

    meta += '</div>';
    return meta;
}

// Get weighted random value
function getWeightedRandom(values, weights) {
    const total = weights.reduce((a, b) => a + b, 0);
    let random = Math.random() * total;

    for (let i = 0; i < values.length; i++) {
        random -= weights[i];
        if (random <= 0) return values[i];
    }

    return values[0];
}

// Initialize Masonry layout
function initMasonry() {
    if (typeof Masonry === 'undefined') {
        console.error('Masonry library not loaded');
        return;
    }

    const grid = document.getElementById('notes-list');

    // Destroy existing instance
    if (masonryGrid) {
        masonryGrid.destroy();
    }

    // Create new masonry instance
    masonryGrid = new Masonry(grid, {
        itemSelector: '.note-card',
        columnWidth: '.grid-sizer',
        percentPosition: true,
        gutter: 16
    });

    // Re-layout after images load (if any)
    if (typeof imagesLoaded !== 'undefined') {
        imagesLoaded(grid, () => {
            masonryGrid.layout();
        });
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
