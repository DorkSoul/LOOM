"""
Travel Routes - Trip planning, itineraries, packing lists, expenses
"""
from flask import render_template, request, jsonify
from datetime import datetime
from app.modules.travel import travel_bp
from app.models.travel import Trip, Itinerary, PackingList, PackingItem, TravelExpense
from app import db

@travel_bp.route('/')
def index():
    """Travel planning page"""
    return render_template('travel/index.html')

# Trip routes
@travel_bp.route('/api/trips', methods=['GET'])
def get_trips():
    """Get all trips"""
    status = request.args.get('status')

    query = Trip.query

    if status:
        query = query.filter_by(status=status)

    trips = query.order_by(Trip.start_date.desc()).all()
    return jsonify([trip.to_dict() for trip in trips])

@travel_bp.route('/api/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    """Get a specific trip with all details"""
    trip = Trip.query.get_or_404(trip_id)

    trip_data = trip.to_dict()
    trip_data['itineraries'] = [i.to_dict() for i in trip.itineraries]
    trip_data['packing_lists'] = [p.to_dict() for p in trip.packing_lists]
    trip_data['expenses'] = [e.to_dict() for e in trip.expenses]

    return jsonify(trip_data)

@travel_bp.route('/api/trips', methods=['POST'])
def create_trip():
    """Create a new trip"""
    data = request.get_json()

    trip = Trip(
        name=data['name'],
        destination=data['destination'],
        description=data.get('description'),
        start_date=datetime.fromisoformat(data['start_date']).date(),
        end_date=datetime.fromisoformat(data['end_date']).date(),
        status=data.get('status', 'planning'),
        budget=data.get('budget')
    )

    db.session.add(trip)
    db.session.commit()

    return jsonify(trip.to_dict()), 201

@travel_bp.route('/api/trips/<int:trip_id>', methods=['PUT'])
def update_trip(trip_id):
    """Update a trip"""
    trip = Trip.query.get_or_404(trip_id)
    data = request.get_json()

    trip.name = data.get('name', trip.name)
    trip.destination = data.get('destination', trip.destination)
    trip.description = data.get('description', trip.description)
    trip.status = data.get('status', trip.status)
    trip.budget = data.get('budget', trip.budget)

    if 'start_date' in data:
        trip.start_date = datetime.fromisoformat(data['start_date']).date()

    if 'end_date' in data:
        trip.end_date = datetime.fromisoformat(data['end_date']).date()

    db.session.commit()

    return jsonify(trip.to_dict())

@travel_bp.route('/api/trips/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    """Delete a trip"""
    trip = Trip.query.get_or_404(trip_id)
    db.session.delete(trip)
    db.session.commit()

    return '', 204

# Itinerary routes
@travel_bp.route('/api/trips/<int:trip_id>/itinerary', methods=['POST'])
def create_itinerary(trip_id):
    """Add itinerary item to trip"""
    trip = Trip.query.get_or_404(trip_id)
    data = request.get_json()

    itinerary = Itinerary(
        trip_id=trip.id,
        day_number=data['day_number'],
        date=datetime.fromisoformat(data['date']).date(),
        title=data['title'],
        description=data.get('description'),
        location=data.get('location'),
        start_time=datetime.fromisoformat(data['start_time']).time() if data.get('start_time') else None,
        end_time=datetime.fromisoformat(data['end_time']).time() if data.get('end_time') else None,
        notes=data.get('notes')
    )

    db.session.add(itinerary)
    db.session.commit()

    return jsonify(itinerary.to_dict()), 201

# Packing list routes
@travel_bp.route('/api/packing-lists', methods=['GET'])
def get_packing_lists():
    """Get all packing lists including templates"""
    templates_only = request.args.get('templates_only', 'false').lower() == 'true'

    query = PackingList.query

    if templates_only:
        query = query.filter_by(is_template=True)

    packing_lists = query.all()
    return jsonify([pl.to_dict() for pl in packing_lists])

@travel_bp.route('/api/trips/<int:trip_id>/packing-list', methods=['POST'])
def create_packing_list(trip_id):
    """Create packing list for trip"""
    trip = Trip.query.get_or_404(trip_id)
    data = request.get_json()

    packing_list = PackingList(
        trip_id=trip.id,
        name=data.get('name', f'{trip.name} Packing List'),
        is_template=data.get('is_template', False)
    )

    db.session.add(packing_list)
    db.session.flush()

    # Add items if provided
    if 'items' in data:
        for item_data in data['items']:
            item = PackingItem(
                packing_list_id=packing_list.id,
                item_name=item_data['item_name'],
                category=item_data.get('category'),
                quantity=item_data.get('quantity', 1),
                notes=item_data.get('notes')
            )
            db.session.add(item)

    db.session.commit()

    return jsonify(packing_list.to_dict()), 201

# Expense routes
@travel_bp.route('/api/trips/<int:trip_id>/expenses', methods=['POST'])
def create_expense(trip_id):
    """Add expense to trip"""
    trip = Trip.query.get_or_404(trip_id)
    data = request.get_json()

    expense = TravelExpense(
        trip_id=trip.id,
        description=data['description'],
        amount=data['amount'],
        category=data.get('category'),
        date=datetime.fromisoformat(data['date']).date(),
        currency=data.get('currency', 'USD'),
        notes=data.get('notes')
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify(expense.to_dict()), 201
