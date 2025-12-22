"""
Notes Routes - CRUD operations for notes
"""
from flask import render_template, request, jsonify
from app.modules.notes import notes_bp
from app.models.note import Note
from app import db

@notes_bp.route('/')
def index():
    """Notes list page"""
    return render_template('notes/index.html')

@notes_bp.route('/api/notes', methods=['GET'])
def get_notes():
    """Get all notes"""
    category = request.args.get('category')
    search = request.args.get('search')

    query = Note.query.filter_by(is_archived=False)

    if category:
        query = query.filter_by(category=category)

    if search:
        query = query.filter(Note.title.contains(search) | Note.content.contains(search))

    notes = query.order_by(Note.is_pinned.desc(), Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@notes_bp.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@notes_bp.route('/api/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    data = request.get_json()

    note = Note(
        title=data.get('title', 'Untitled'),
        content=data.get('content', ''),
        category=data.get('category'),
        tags=','.join(data.get('tags', [])) if isinstance(data.get('tags'), list) else data.get('tags'),
        is_pinned=data.get('is_pinned', False)
    )

    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201

@notes_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update an existing note"""
    note = Note.query.get_or_404(note_id)
    data = request.get_json()

    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.category = data.get('category', note.category)

    if 'tags' in data:
        note.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']

    if 'is_pinned' in data:
        note.is_pinned = data['is_pinned']

    if 'is_archived' in data:
        note.is_archived = data['is_archived']

    db.session.commit()

    return jsonify(note.to_dict())

@notes_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()

    return '', 204
