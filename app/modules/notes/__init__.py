"""
Notes Module - Markdown note-taking
"""
from flask import Blueprint

notes_bp = Blueprint('notes', __name__, template_folder='templates')

from app.modules.notes import routes
