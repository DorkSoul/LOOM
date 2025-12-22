"""
Events Routes - Chronological list view of events
"""
from flask import render_template, request, jsonify
from datetime import datetime
from app.modules.events import events_bp
from app.models.event import Event

@events_bp.route('/')
def index():
    """Events list page"""
    return render_template('events/index.html')

@events_bp.route('/api/events/upcoming', methods=['GET'])
def get_upcoming_events():
    """Get upcoming events in chronological order"""
    limit = request.args.get('limit', 50, type=int)

    events = Event.query.filter(
        Event.start_time >= datetime.utcnow()
    ).order_by(Event.start_time).limit(limit).all()

    return jsonify([event.to_dict() for event in events])

@events_bp.route('/api/events/past', methods=['GET'])
def get_past_events():
    """Get past events"""
    limit = request.args.get('limit', 50, type=int)

    events = Event.query.filter(
        Event.start_time < datetime.utcnow()
    ).order_by(Event.start_time.desc()).limit(limit).all()

    return jsonify([event.to_dict() for event in events])
