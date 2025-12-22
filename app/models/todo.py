"""
Todo Model - Task management with reminders
"""
from datetime import datetime
from app import db

class Todo(db.Model):
    """Todo model for task management"""
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    due_date = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_weekly = db.Column(db.Boolean, default=False)  # For weekly recurring tasks
    week_day = db.Column(db.Integer, nullable=True)  # 0-6 for Monday-Sunday
    category = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to reminders
    reminders = db.relationship('TodoReminder', backref='todo', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Todo {self.title}>'

    def to_dict(self):
        """Convert todo to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_weekly': self.is_weekly,
            'week_day': self.week_day,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'reminders': [r.to_dict() for r in self.reminders]
        }

class TodoReminder(db.Model):
    """Timer-based reminders for todos"""
    __tablename__ = 'todo_reminders'

    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todos.id'), nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(200), nullable=True)
    is_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<TodoReminder for Todo {self.todo_id}>'

    def to_dict(self):
        """Convert reminder to dictionary"""
        return {
            'id': self.id,
            'todo_id': self.todo_id,
            'reminder_time': self.reminder_time.isoformat(),
            'message': self.message,
            'is_sent': self.is_sent,
            'created_at': self.created_at.isoformat()
        }
