"""
Event Model - Calendar events and scheduling
"""
from datetime import datetime
from app import db

class Event(db.Model):
    """Event model for calendar and scheduling"""
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    all_day = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(7), default='#3788d8')  # Hex color code
    recurring = db.Column(db.Boolean, default=False)
    recurrence_rule = db.Column(db.String(100), nullable=True)  # RRULE format
    reminder_minutes = db.Column(db.Integer, nullable=True)  # Minutes before event
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Event {self.title}>'

    def to_dict(self):
        """Convert event to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'all_day': self.all_day,
            'category': self.category,
            'color': self.color,
            'recurring': self.recurring,
            'recurrence_rule': self.recurrence_rule,
            'reminder_minutes': self.reminder_minutes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
