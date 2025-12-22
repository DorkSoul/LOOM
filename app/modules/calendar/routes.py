"""
Calendar Routes - Calendar view and event management
"""
from flask import render_template, request, jsonify
from datetime import datetime, timedelta
from app.modules.calendar import calendar_bp
from app.models.event import Event
from app import db

@calendar_bp.route('/')
def index():
    """Calendar page"""
    return render_template('calendar/index.html')

@calendar_bp.route('/api/events', methods=['GET'])
def get_events():
    """Get events for calendar view"""
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    query = Event.query

    if start_date:
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        query = query.filter(Event.start_time >= start_dt)

    if end_date:
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        query = query.filter(Event.start_time <= end_dt)

    events = query.order_by(Event.start_time).all()
    return jsonify([event.to_dict() for event in events])

@calendar_bp.route('/api/events', methods=['POST'])
def create_event():
    """Create a new event"""
    data = request.get_json()

    event = Event(
        title=data['title'],
        description=data.get('description'),
        location=data.get('location'),
        start_time=datetime.fromisoformat(data['start_time'].replace('Z', '+00:00')),
        end_time=datetime.fromisoformat(data['end_time'].replace('Z', '+00:00')) if data.get('end_time') else None,
        all_day=data.get('all_day', False),
        category=data.get('category'),
        color=data.get('color', '#3788d8'),
        recurring=data.get('recurring', False),
        recurrence_rule=data.get('recurrence_rule'),
        reminder_minutes=data.get('reminder_minutes')
    )

    db.session.add(event)
    db.session.commit()

    return jsonify(event.to_dict()), 201

@calendar_bp.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an event"""
    event = Event.query.get_or_404(event_id)
    data = request.get_json()

    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.location = data.get('location', event.location)

    if 'start_time' in data:
        event.start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))

    if 'end_time' in data:
        event.end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00')) if data['end_time'] else None

    if 'all_day' in data:
        event.all_day = data['all_day']

    if 'category' in data:
        event.category = data['category']

    if 'color' in data:
        event.color = data['color']

    db.session.commit()

    return jsonify(event.to_dict())

@calendar_bp.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event"""
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()

    return '', 204
