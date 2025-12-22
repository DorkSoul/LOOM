"""
Travel Module - Trip planning and management
"""
from flask import Blueprint

travel_bp = Blueprint('travel', __name__, template_folder='templates')

from app.modules.travel import routes
