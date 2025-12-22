"""
Calendar Module - Visual calendar display
"""
from flask import Blueprint

calendar_bp = Blueprint('calendar', __name__, template_folder='templates')

from app.modules.calendar import routes
