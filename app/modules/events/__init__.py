"""
Events Module - Chronological event list view
"""
from flask import Blueprint

events_bp = Blueprint('events', __name__, template_folder='templates')

from app.modules.events import routes
