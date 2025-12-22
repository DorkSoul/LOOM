"""
LOOM - Life Organization & Operations Manager
Main application entry point
"""
import os
import logging
from app import create_app, db

# Configure logging
log_dir = os.getenv('LOG_DIR', '/app/logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'loom.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create Flask application
app = create_app()

# Initialize database
with app.app_context():
    db.create_all()
    logger.info("Database initialized successfully")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting LOOM on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
