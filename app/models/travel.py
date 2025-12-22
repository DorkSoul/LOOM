"""
Travel Model - Trip planning and management
"""
from datetime import datetime
from app import db

class Trip(db.Model):
    """Trip model for travel planning"""
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='planning')  # planning, confirmed, completed, cancelled
    budget = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    itineraries = db.relationship('Itinerary', backref='trip', lazy=True, cascade='all, delete-orphan')
    packing_lists = db.relationship('PackingList', backref='trip', lazy=True, cascade='all, delete-orphan')
    expenses = db.relationship('TravelExpense', backref='trip', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Trip {self.name}>'

    def to_dict(self):
        """Convert trip to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'destination': self.destination,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status,
            'budget': self.budget,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Itinerary(db.Model):
    """Daily itinerary for trips"""
    __tablename__ = 'itineraries'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Itinerary Day {self.day_number} - {self.title}>'

    def to_dict(self):
        """Convert itinerary to dictionary"""
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'day_number': self.day_number,
            'date': self.date.isoformat(),
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

class PackingList(db.Model):
    """Packing lists for trips (reusable templates)"""
    __tablename__ = 'packing_lists'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    is_template = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to packing items
    items = db.relationship('PackingItem', backref='packing_list', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<PackingList {self.name}>'

    def to_dict(self):
        """Convert packing list to dictionary"""
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'name': self.name,
            'is_template': self.is_template,
            'created_at': self.created_at.isoformat(),
            'items': [i.to_dict() for i in self.items]
        }

class PackingItem(db.Model):
    """Individual items in packing lists"""
    __tablename__ = 'packing_items'

    id = db.Column(db.Integer, primary_key=True)
    packing_list_id = db.Column(db.Integer, db.ForeignKey('packing_lists.id'), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True)  # clothing, toiletries, electronics, documents, etc.
    quantity = db.Column(db.Integer, default=1)
    is_packed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<PackingItem {self.item_name}>'

    def to_dict(self):
        """Convert packing item to dictionary"""
        return {
            'id': self.id,
            'packing_list_id': self.packing_list_id,
            'item_name': self.item_name,
            'category': self.category,
            'quantity': self.quantity,
            'is_packed': self.is_packed,
            'notes': self.notes
        }

class TravelExpense(db.Model):
    """Track expenses for trips"""
    __tablename__ = 'travel_expenses'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)  # accommodation, food, transport, activities, etc.
    date = db.Column(db.Date, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<TravelExpense {self.description} - {self.amount}>'

    def to_dict(self):
        """Convert expense to dictionary"""
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'description': self.description,
            'amount': self.amount,
            'category': self.category,
            'date': self.date.isoformat(),
            'currency': self.currency,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }
