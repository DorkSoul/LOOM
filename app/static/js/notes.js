/**
 * Notes Module - Google Keep style masonry layout
 */

let masonryGrid = null;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    loadNotes();
    initEventListeners();
});

// Initialize event listeners
function initEventListeners() {
    document.getElementById('newNoteBtn')?.addEventListener('click', openNewNoteModal);
    document.getElementById('closeModal')?.addEventListener('click', closeModal);
    document.getElementById('cancelBtn')?.addEventListener('click', closeModal);
    document.getElementById('saveNoteBtn')?.addEventListener('click', saveNote);

    // Close modal on outside click
    document.getElementById('noteModal')?.addEventListener('click', (e) => {
        if (e.target.id === 'noteModal') closeModal();
    });
}

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
    card.dataset.noteId = note.id;

    // Convert markdown to HTML for display (limit preview length)
    const contentLength = (note.content || '').length;
    const previewLength = Math.min(contentLength, 400);
    const contentHtml = note.content ? renderMarkdown(note.content.substring(0, previewLength)) : '';

    // Build card content
    card.innerHTML = `
        ${note.is_pinned ? '<span class="pinned-badge">📌</span>' : ''}
        <h3>${escapeHtml(note.title)}</h3>
        <div class="note-preview">${contentHtml}</div>
        ${renderMeta(note)}
    `;

    // Click to open note
    card.addEventListener('click', () => openNote(note.id));

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

// Render markdown to HTML
function renderMarkdown(markdown) {
    if (typeof marked === 'undefined') {
        return escapeHtml(markdown);
    }
    return marked.parse(markdown, { breaks: true });
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

// Open existing note
async function openNote(noteId) {
    try {
        const note = await window.loom.apiCall(`/notes/api/notes/${noteId}`, 'GET');

        document.getElementById('modalTitle').textContent = 'Edit Note';
        document.getElementById('noteId').value = note.id;
        document.getElementById('noteTitle').value = note.title || '';
        document.getElementById('noteContent').value = note.content || '';
        document.getElementById('noteCategory').value = note.category || '';
        document.getElementById('noteTags').value = Array.isArray(note.tags) ? note.tags.join(', ') : (note.tags || '');
        document.getElementById('notePinned').checked = note.is_pinned || false;
        document.getElementById('noteModal').classList.add('active');
    } catch (error) {
        console.error('Error loading note:', error);
        window.loom.showNotification('Failed to load note');
    }
}

// Close modal
function closeModal() {
    document.getElementById('noteModal').classList.remove('active');
}

// Save note (create or update)
async function saveNote() {
    const noteId = document.getElementById('noteId').value;
    const title = document.getElementById('noteTitle').value.trim();
    const content = document.getElementById('noteContent').value;
    const category = document.getElementById('noteCategory').value.trim();
    const tagsInput = document.getElementById('noteTags').value.trim();
    const isPinned = document.getElementById('notePinned').checked;

    if (!title) {
        window.loom.showNotification('Please enter a title');
        return;
    }

    const noteData = {
        title,
        content,
        category: category || null,
        tags: tagsInput || null,
        is_pinned: isPinned
    };

    try {
        if (noteId) {
            // Update existing note
            await window.loom.apiCall(`/notes/api/notes/${noteId}`, 'PUT', noteData);
            window.loom.showNotification('Note updated');
        } else {
            // Create new note
            await window.loom.apiCall('/notes/api/notes', 'POST', noteData);
            window.loom.showNotification('Note created');
        }

        closeModal();
        await loadNotes();
    } catch (error) {
        console.error('Error saving note:', error);
        window.loom.showNotification('Failed to save note');
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
