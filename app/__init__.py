"""
LOOM Application Factory
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """
    Application factory pattern
    """
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.getenv('DATABASE_PATH', '/app/data/loom.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.modules.notes import notes_bp
    from app.modules.calendar import calendar_bp
    from app.modules.events import events_bp
    from app.modules.todos import todos_bp
    from app.modules.recipes import recipes_bp
    from app.modules.travel import travel_bp
    from app.modules.subscriptions import subscriptions_bp
    from app.modules.dashboard import dashboard_bp

    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(todos_bp, url_prefix='/todos')
    app.register_blueprint(recipes_bp, url_prefix='/recipes')
    app.register_blueprint(travel_bp, url_prefix='/travel')
    app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')

    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    return app
