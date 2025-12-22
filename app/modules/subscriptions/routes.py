"""
Subscriptions Routes - Subscription tracking and renewal reminders
"""
from flask import render_template, request, jsonify
from datetime import datetime
from app.modules.subscriptions import subscriptions_bp
from app.models.subscription import Subscription
from app import db

@subscriptions_bp.route('/')
def index():
    """Subscriptions page"""
    return render_template('subscriptions/index.html')

@subscriptions_bp.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    """Get all subscriptions"""
    active_only = request.args.get('active_only', 'false').lower() == 'true'

    query = Subscription.query

    if active_only:
        query = query.filter_by(is_active=True)

    subscriptions = query.order_by(Subscription.next_billing_date).all()
    return jsonify([sub.to_dict() for sub in subscriptions])

@subscriptions_bp.route('/api/subscriptions/<int:subscription_id>', methods=['GET'])
def get_subscription(subscription_id):
    """Get a specific subscription"""
    subscription = Subscription.query.get_or_404(subscription_id)
    return jsonify(subscription.to_dict())

@subscriptions_bp.route('/api/subscriptions', methods=['POST'])
def create_subscription():
    """Create a new subscription"""
    data = request.get_json()

    subscription = Subscription(
        name=data['name'],
        description=data.get('description'),
        cost=data['cost'],
        currency=data.get('currency', 'USD'),
        billing_cycle=data['billing_cycle'],
        custom_cycle_days=data.get('custom_cycle_days'),
        next_billing_date=datetime.fromisoformat(data['next_billing_date']).date(),
        reminder_days_before=data.get('reminder_days_before', 3),
        category=data.get('category'),
        is_active=data.get('is_active', True),
        auto_renew=data.get('auto_renew', True),
        website_url=data.get('website_url'),
        notes=data.get('notes')
    )

    db.session.add(subscription)
    db.session.commit()

    return jsonify(subscription.to_dict()), 201

@subscriptions_bp.route('/api/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    """Update a subscription"""
    subscription = Subscription.query.get_or_404(subscription_id)
    data = request.get_json()

    subscription.name = data.get('name', subscription.name)
    subscription.description = data.get('description', subscription.description)
    subscription.cost = data.get('cost', subscription.cost)
    subscription.currency = data.get('currency', subscription.currency)
    subscription.billing_cycle = data.get('billing_cycle', subscription.billing_cycle)
    subscription.custom_cycle_days = data.get('custom_cycle_days', subscription.custom_cycle_days)
    subscription.reminder_days_before = data.get('reminder_days_before', subscription.reminder_days_before)
    subscription.category = data.get('category', subscription.category)
    subscription.is_active = data.get('is_active', subscription.is_active)
    subscription.auto_renew = data.get('auto_renew', subscription.auto_renew)
    subscription.website_url = data.get('website_url', subscription.website_url)
    subscription.notes = data.get('notes', subscription.notes)

    if 'next_billing_date' in data:
        subscription.next_billing_date = datetime.fromisoformat(data['next_billing_date']).date()

    db.session.commit()

    return jsonify(subscription.to_dict())

@subscriptions_bp.route('/api/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    """Delete a subscription"""
    subscription = Subscription.query.get_or_404(subscription_id)
    db.session.delete(subscription)
    db.session.commit()

    return '', 204

@subscriptions_bp.route('/api/subscriptions/reminders', methods=['GET'])
def get_reminders():
    """Get subscriptions that need reminders"""
    active_subscriptions = Subscription.query.filter_by(is_active=True).all()

    reminders = [
        sub.to_dict() for sub in active_subscriptions
        if sub.should_send_reminder()
    ]

    return jsonify(reminders)

@subscriptions_bp.route('/api/subscriptions/<int:subscription_id>/renew', methods=['POST'])
def renew_subscription(subscription_id):
    """Mark subscription as renewed and update next billing date"""
    subscription = Subscription.query.get_or_404(subscription_id)

    # Update to next billing date
    subscription.next_billing_date = subscription.get_next_billing_date()

    db.session.commit()

    return jsonify(subscription.to_dict())
