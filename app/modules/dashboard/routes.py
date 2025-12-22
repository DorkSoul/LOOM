"""
Dashboard Routes
"""
from flask import render_template, jsonify
from datetime import datetime, timedelta
from app.modules.dashboard import dashboard_bp
from app.models import Note, Event, Todo
from app import db

@dashboard_bp.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard/index.html')

@dashboard_bp.route('/api/overview')
def overview():
    """Get dashboard overview data"""
    today = datetime.utcnow().date()
    week_from_now = today + timedelta(days=7)

    # Get upcoming events
    upcoming_events = Event.query.filter(
        Event.start_time >= datetime.utcnow(),
        Event.start_time <= datetime.combine(week_from_now, datetime.max.time())
    ).order_by(Event.start_time).limit(5).all()

    # Get pending todos
    pending_todos = Todo.query.filter_by(status='pending').order_by(Todo.priority.desc()).limit(5).all()

    # Get recent notes
    recent_notes = Note.query.filter_by(is_archived=False).order_by(Note.updated_at.desc()).limit(5).all()

    return jsonify({
        'upcoming_events': [e.to_dict() for e in upcoming_events],
        'pending_todos': [t.to_dict() for t in pending_todos],
        'recent_notes': [n.to_dict() for n in recent_notes]
    })
