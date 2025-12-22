"""
Recipes Module - Recipe management and meal planning
"""
from flask import Blueprint

recipes_bp = Blueprint('recipes', __name__, template_folder='templates')

from app.modules.recipes import routes
