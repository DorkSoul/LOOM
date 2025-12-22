"""
Todos Module - Task management
"""
from flask import Blueprint

todos_bp = Blueprint('todos', __name__, template_folder='templates')

from app.modules.todos import routes
