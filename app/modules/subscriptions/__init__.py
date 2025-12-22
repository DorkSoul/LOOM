"""
Subscriptions Module - Renewal reminders and tracking
"""
from flask import Blueprint

subscriptions_bp = Blueprint('subscriptions', __name__, template_folder='templates')

from app.modules.subscriptions import routes
