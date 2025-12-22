"""
Dashboard Module - Main dashboard and overview
"""
from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

from app.modules.dashboard import routes
