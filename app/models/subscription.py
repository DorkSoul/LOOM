"""
Subscription Model - Renewal reminders and tracking
"""
from datetime import datetime, timedelta
from app import db

class Subscription(db.Model):
    """Subscription model for tracking recurring services"""
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cost = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    billing_cycle = db.Column(db.String(20), nullable=False)  # weekly, monthly, quarterly, annual, custom
    custom_cycle_days = db.Column(db.Integer, nullable=True)  # For custom billing cycles
    next_billing_date = db.Column(db.Date, nullable=False)
    reminder_days_before = db.Column(db.Integer, default=3)  # Days before renewal to send reminder
    category = db.Column(db.String(50), nullable=True)  # streaming, software, utilities, etc.
    is_active = db.Column(db.Boolean, default=True)
    auto_renew = db.Column(db.Boolean, default=True)
    website_url = db.Column(db.String(500), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Subscription {self.name}>'

    def get_next_billing_date(self):
        """Calculate next billing date based on cycle"""
        if self.billing_cycle == 'weekly':
            return self.next_billing_date + timedelta(weeks=1)
        elif self.billing_cycle == 'monthly':
            # Approximate monthly as 30 days
            return self.next_billing_date + timedelta(days=30)
        elif self.billing_cycle == 'quarterly':
            return self.next_billing_date + timedelta(days=90)
        elif self.billing_cycle == 'annual':
            return self.next_billing_date + timedelta(days=365)
        elif self.billing_cycle == 'custom' and self.custom_cycle_days:
            return self.next_billing_date + timedelta(days=self.custom_cycle_days)
        return self.next_billing_date

    def get_reminder_date(self):
        """Get the date when reminder should be sent"""
        return self.next_billing_date - timedelta(days=self.reminder_days_before)

    def should_send_reminder(self):
        """Check if reminder should be sent today"""
        today = datetime.utcnow().date()
        reminder_date = self.get_reminder_date()
        return today >= reminder_date and today < self.next_billing_date

    def to_dict(self):
        """Convert subscription to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cost': self.cost,
            'currency': self.currency,
            'billing_cycle': self.billing_cycle,
            'custom_cycle_days': self.custom_cycle_days,
            'next_billing_date': self.next_billing_date.isoformat(),
            'reminder_days_before': self.reminder_days_before,
            'reminder_date': self.get_reminder_date().isoformat(),
            'category': self.category,
            'is_active': self.is_active,
            'auto_renew': self.auto_renew,
            'website_url': self.website_url,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
