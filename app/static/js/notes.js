// Notes Module - Masonry Layout with CRUD operations

let masonryInstance = null;
let currentNotes = [];

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNotes();
    initializeEventListeners();
});

// Initialize masonry layout
function initializeMasonry() {
    const grid = document.querySelector('#notes-list');

    if (!grid) return;

    // Destroy existing instance if it exists
    if (masonryInstance) {
        masonryInstance.destroy();
    }

    // Initialize Masonry
    masonryInstance = new Masonry(grid, {
        itemSelector: '.note-card',
        columnWidth: '.note-card-sizer',
        percentPosition: true,
        gutter: 16,
        transitionDuration: '0.3s'
    });

    // Layout after images load (if any)
    if (typeof imagesLoaded !== 'undefined') {
        imagesLoaded(grid, function() {
            masonryInstance.layout();
        });
    }
}

// Initialize notes module
async function initializeNotes() {
    await loadNotes();
    await loadCategories();
}

// Load all notes from API
async function loadNotes(filters = {}) {
    try {
        let url = '/notes/api/notes';
        const params = new URLSearchParams();

        if (filters.search) params.append('search', filters.search);
        if (filters.category) params.append('category', filters.category);

        if (params.toString()) {
            url += '?' + params.toString();
        }

        const response = await window.loom.apiCall(url, 'GET');
        currentNotes = response;
        renderNotes(response);
    } catch (error) {
        console.error('Error loading notes:', error);
        window.loom.showNotification('Failed to load notes', 'error');
    }
}

// Load unique categories for filter dropdown
async function loadCategories() {
    try {
        const response = await window.loom.apiCall('/notes/api/notes', 'GET');
        const categories = [...new Set(response.filter(n => n.category).map(n => n.category))];

        const select = document.getElementById('categoryFilter');
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Render notes with masonry layout
function renderNotes(notes) {
    const container = document.getElementById('notes-list');

    // Clear container
    container.innerHTML = '';

    // Add sizer element for masonry columnWidth
    const sizer = document.createElement('div');
    sizer.className = 'note-card-sizer';
    container.appendChild(sizer);

    // Sort: pinned first, then by date
    const sortedNotes = [...notes].sort((a, b) => {
        if (a.is_pinned && !b.is_pinned) return -1;
        if (!a.is_pinned && b.is_pinned) return 1;
        return new Date(b.created_at) - new Date(a.created_at);
    });

    // Render each note
    sortedNotes.forEach(note => {
        if (!note.is_archived) {
            container.appendChild(createNoteElement(note));
        }
    });

    // Initialize or re-layout masonry
    setTimeout(() => {
        initializeMasonry();
    }, 100);
}

// Create a note element with random size variation
function createNoteElement(note) {
    const noteDiv = document.createElement('div');
    noteDiv.className = 'note-card';
    noteDiv.dataset.noteId = note.id;

    // Generate random size within specified range
    const height = getRandomNoteHeight();
    noteDiv.style.setProperty('--note-height', `${height}px`);

    // Create note content
    const content = `
        ${note.is_pinned ? '<span class="pinned-badge">📌 Pinned</span>' : ''}
        <div class="note-content-wrapper">
            <h3>${escapeHtml(note.title)}</h3>
            <div class="note-content">${formatNoteContent(note.content)}</div>
            ${note.category ? `<span class="category-badge">${escapeHtml(note.category)}</span>` : ''}
            ${note.tags ? `<div class="note-tags">${renderTags(note.tags)}</div>` : ''}
            <div class="note-meta">
                <span>${window.loom.formatDate(note.created_at)}</span>
                <div class="note-actions">
                    <button class="btn-icon" onclick="editNote(${note.id})" title="Edit">✏️</button>
                    <button class="btn-icon" onclick="togglePin(${note.id})" title="${note.is_pinned ? 'Unpin' : 'Pin'}">📌</button>
                    <button class="btn-icon" onclick="deleteNote(${note.id})" title="Delete">🗑️</button>
                </div>
            </div>
        </div>
    `;

    noteDiv.innerHTML = content;

    // Click to edit (but not on buttons)
    noteDiv.addEventListener('click', function(e) {
        if (!e.target.closest('.note-actions') && !e.target.closest('button')) {
            editNote(note.id);
        }
    });

    return noteDiv;
}

// Get random height within specified range
function getRandomNoteHeight() {
    const minHeight = 150;
    const maxHeight = 600;
    // Weight towards smaller/medium sizes like Google Keep
    const weights = [150, 200, 250, 300, 350, 400, 450, 500, 550, 600];
    const weightedWeights = [3, 3, 2, 2, 1, 1, 0.5, 0.5, 0.3, 0.3]; // More likely to be smaller

    const totalWeight = weightedWeights.reduce((a, b) => a + b, 0);
    let random = Math.random() * totalWeight;

    for (let i = 0; i < weights.length; i++) {
        random -= weightedWeights[i];
        if (random <= 0) {
            return weights[i];
        }
    }

    return 300; // fallback
}

// Format note content (support for markdown-like formatting)
function formatNoteContent(content) {
    if (!content) return '';

    // Truncate if too long for preview
    let preview = content.length > 300 ? content.substring(0, 300) + '...' : content;

    // Basic markdown support
    preview = preview.replace(/\n/g, '<br>');
    preview = preview.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    preview = preview.replace(/\*(.*?)\*/g, '<em>$1</em>');

    return preview;
}

// Render tags
function renderTags(tagsString) {
    if (!tagsString) return '';

    // Handle if tags is already an array or convert string to array
    let tags;
    if (Array.isArray(tagsString)) {
        tags = tagsString;
    } else if (typeof tagsString === 'string') {
        tags = tagsString.split(',').map(t => t.trim()).filter(t => t);
    } else {
        return '';
    }

    return tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('');
}

// Initialize event listeners
function initializeEventListeners() {
    // New note button
    document.getElementById('newNoteBtn')?.addEventListener('click', openNewNoteModal);

    // Modal controls
    document.getElementById('closeModal')?.addEventListener('click', closeModal);
    document.getElementById('cancelBtn')?.addEventListener('click', closeModal);
    document.getElementById('saveNoteBtn')?.addEventListener('click', saveNote);

    // Close modal on outside click
    document.getElementById('noteModal')?.addEventListener('click', function(e) {
        if (e.target.id === 'noteModal') {
            closeModal();
        }
    });

    // Search functionality
    let searchTimeout;
    document.getElementById('searchNotes')?.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            loadNotes({ search: e.target.value, category: document.getElementById('categoryFilter').value });
        }, 300);
    });

    // Category filter
    document.getElementById('categoryFilter')?.addEventListener('change', function(e) {
        loadNotes({ search: document.getElementById('searchNotes').value, category: e.target.value });
    });
}

// Open new note modal
function openNewNoteModal() {
    document.getElementById('modalTitle').textContent = 'New Note';
    document.getElementById('noteId').value = '';
    document.getElementById('noteTitle').value = '';
    document.getElementById('noteContent').value = '';
    document.getElementById('noteCategory').value = '';
    document.getElementById('noteTags').value = '';
    document.getElementById('notePinned').checked = false;
    document.getElementById('noteModal').classList.add('active');
}

// Open edit note modal
async function editNote(noteId) {
    try {
        const note = await window.loom.apiCall(`/notes/api/notes/${noteId}`, 'GET');

        document.getElementById('modalTitle').textContent = 'Edit Note';
        document.getElementById('noteId').value = note.id;
        document.getElementById('noteTitle').value = note.title || '';
        document.getElementById('noteContent').value = note.content || '';
        document.getElementById('noteCategory').value = note.category || '';
        document.getElementById('noteTags').value = note.tags || '';
        document.getElementById('notePinned').checked = note.is_pinned || false;
        document.getElementById('noteModal').classList.add('active');
    } catch (error) {
        console.error('Error loading note:', error);
        window.loom.showNotification('Failed to load note', 'error');
    }
}

// Close modal
function closeModal() {
    document.getElementById('noteModal').classList.remove('active');
}

// Save note (create or update)
async function saveNote() {
    const noteId = document.getElementById('noteId').value;
    const noteData = {
        title: document.getElementById('noteTitle').value,
        content: document.getElementById('noteContent').value,
        category: document.getElementById('noteCategory').value || null,
        tags: document.getElementById('noteTags').value || null,
        is_pinned: document.getElementById('notePinned').checked
    };

    if (!noteData.title) {
        window.loom.showNotification('Please enter a title', 'error');
        return;
    }

    try {
        if (noteId) {
            // Update existing note
            await window.loom.apiCall(`/notes/api/notes/${noteId}`, 'PUT', noteData);
            window.loom.showNotification('Note updated successfully', 'success');
        } else {
            // Create new note
            await window.loom.apiCall('/notes/api/notes', 'POST', noteData);
            window.loom.showNotification('Note created successfully', 'success');
        }

        closeModal();
        await loadNotes();
    } catch (error) {
        console.error('Error saving note:', error);
        window.loom.showNotification('Failed to save note', 'error');
    }
}

// Toggle pin status
async function togglePin(noteId) {
    try {
        const note = currentNotes.find(n => n.id === noteId);
        if (!note) return;

        await window.loom.apiCall(`/notes/api/notes/${noteId}`, 'PUT', {
            is_pinned: !note.is_pinned
        });

        await loadNotes();
    } catch (error) {
        console.error('Error toggling pin:', error);
        window.loom.showNotification('Failed to update note', 'error');
    }
}

// Delete note
async function deleteNote(noteId) {
    if (!await window.loom.confirmAction('Are you sure you want to delete this note?')) {
        return;
    }

    try {
        await window.loom.apiCall(`/notes/api/notes/${noteId}`, 'DELETE');
        window.loom.showNotification('Note deleted successfully', 'success');
        await loadNotes();
    } catch (error) {
        console.error('Error deleting note:', error);
        window.loom.showNotification('Failed to delete note', 'error');
    }
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Make functions globally accessible
window.editNote = editNote;
window.deleteNote = deleteNote;
window.togglePin = togglePin;
