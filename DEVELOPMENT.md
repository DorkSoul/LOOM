# LOOM Development Guide

## Project Architecture

LOOM follows a modular, object-oriented architecture using Flask blueprints. Each feature module is self-contained with its own models, routes, and templates.

### Architecture Overview

```
Flask Application (app/__init__.py)
    ├── Database (SQLAlchemy)
    ├── Blueprints (Modules)
    │   ├── Dashboard
    │   ├── Notes
    │   ├── Calendar
    │   ├── Events
    │   ├── Todos
    │   ├── Recipes
    │   ├── Travel
    │   └── Subscriptions
    └── Static Assets
```

## Directory Structure Explained

### `/app`
Main application package containing all application code.

- **`__init__.py`**: Application factory that creates and configures the Flask app
- **`config.py`**: Configuration classes for different environments

### `/app/models`
Database models using SQLAlchemy ORM. Each model represents a database table.

- **`note.py`**: Note model for markdown notes
- **`event.py`**: Event model for calendar events
- **`todo.py`**: Todo and TodoReminder models
- **`recipe.py`**: Recipe, RecipeIngredient, RecipeTag, ShoppingListItem models
- **`travel.py`**: Trip, Itinerary, PackingList, PackingItem, TravelExpense models

### `/app/modules`
Flask blueprints for each feature module. Each module contains:

- **`__init__.py`**: Blueprint initialization
- **`routes.py`**: API endpoints and route handlers

### `/app/static`
Static assets (CSS, JavaScript, images)

- **`css/style.css`**: Main stylesheet
- **`js/main.js`**: Utility functions and API helpers

### `/app/templates`
Jinja2 HTML templates

- **`base.html`**: Base template with navigation
- **`[module]/index.html`**: Module-specific templates

## Adding a New Module

### Step 1: Create the Model

Create a new file in `/app/models/`:

```python
# app/models/your_module.py
from datetime import datetime
from app import db

class YourModel(db.Model):
    __tablename__ = 'your_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }
```

### Step 2: Create the Blueprint

Create a new directory in `/app/modules/your_module/`:

```python
# app/modules/your_module/__init__.py
from flask import Blueprint

your_module_bp = Blueprint('your_module', __name__, template_folder='templates')

from app.modules.your_module import routes
```

```python
# app/modules/your_module/routes.py
from flask import render_template, request, jsonify
from app.modules.your_module import your_module_bp
from app.models.your_module import YourModel
from app import db

@your_module_bp.route('/')
def index():
    return render_template('your_module/index.html')

@your_module_bp.route('/api/items', methods=['GET'])
def get_items():
    items = YourModel.query.all()
    return jsonify([item.to_dict() for item in items])

@your_module_bp.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    item = YourModel(name=data['name'])
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201
```

### Step 3: Register the Blueprint

Update `/app/__init__.py`:

```python
from app.modules.your_module import your_module_bp

app.register_blueprint(your_module_bp, url_prefix='/your_module')
```

### Step 4: Create the Template

Create `/app/templates/your_module/index.html`:

```html
{% extends "base.html" %}

{% block title %}Your Module - LOOM{% endblock %}

{% block content %}
<div class="your-module">
    <h2>Your Module</h2>
    <div id="items-list"></div>
</div>
{% endblock %}
```

### Step 5: Update Navigation

Add a link in `/app/templates/base.html`:

```html
<li><a href="{{ url_for('your_module.index') }}">Your Module</a></li>
```

## Database Migrations

When you add or modify models, you may need to recreate the database:

### Development (Auto-create)

The application automatically creates tables on startup using:

```python
with app.app_context():
    db.create_all()
```

### Production (Manual Migration)

For production, consider using Flask-Migrate:

```bash
# Initialize migrations (first time only)
flask db init

# Create a migration
flask db migrate -m "Add your_model table"

# Apply the migration
flask db upgrade
```

## API Design Patterns

### RESTful Endpoints

Follow these patterns for consistency:

- **GET** `/api/resource` - List all resources
- **POST** `/api/resource` - Create a new resource
- **GET** `/api/resource/<id>` - Get a specific resource
- **PUT** `/api/resource/<id>` - Update a resource
- **DELETE** `/api/resource/<id>` - Delete a resource

### Response Format

```python
# Success (200/201)
return jsonify(resource.to_dict()), 201

# No content (204)
return '', 204

# Error (400/404/500)
return jsonify({'error': 'Error message'}), 400
```

### Request Handling

```python
# Get JSON data
data = request.get_json()

# Get query parameters
page = request.args.get('page', 1, type=int)
search = request.args.get('search')

# Validate required fields
if not data.get('required_field'):
    return jsonify({'error': 'Missing required field'}), 400
```

## Testing

### Manual Testing

1. Start the application:
   ```bash
   python run.py
   ```

2. Use curl or Postman to test API endpoints:
   ```bash
   # Create a note
   curl -X POST http://localhost:5000/notes/api/notes \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Note", "content": "Test content"}'

   # Get all notes
   curl http://localhost:5000/notes/api/notes
   ```

### Automated Testing (Future Enhancement)

Create a `tests/` directory with pytest:

```python
# tests/test_notes.py
def test_create_note(client):
    response = client.post('/notes/api/notes', json={
        'title': 'Test Note',
        'content': 'Test content'
    })
    assert response.status_code == 201
```

## Frontend Development

### JavaScript API Calls

Use the utility function in `/app/static/js/main.js`:

```javascript
// GET request
const notes = await window.loom.apiCall('/notes/api/notes');

// POST request
const newNote = await window.loom.apiCall('/notes/api/notes', 'POST', {
    title: 'New Note',
    content: 'Content here'
});

// DELETE request
await window.loom.apiCall(`/notes/api/notes/${id}`, 'DELETE');
```

### CSS Styling

Use the CSS variables defined in `/app/static/css/style.css`:

```css
/* Use existing color variables */
.my-element {
    color: var(--primary-color);
    background: var(--card-background);
    border: 1px solid var(--border-color);
}
```

## Code Style Guidelines

### Python

- Follow PEP 8
- Use docstrings for functions and classes
- Use type hints where appropriate
- Keep functions focused and single-purpose

### JavaScript

- Use modern ES6+ syntax
- Use async/await for asynchronous operations
- Keep functions pure when possible
- Use meaningful variable names

### HTML/CSS

- Use semantic HTML5 elements
- Follow BEM naming convention for CSS classes
- Keep templates modular and reusable
- Ensure responsive design

## Performance Considerations

### Database Queries

- Use `.all()` only when you need all results
- Use `.limit()` for large datasets
- Add indexes for frequently queried columns
- Use eager loading with `joinedload()` for relationships

### Frontend

- Minimize DOM manipulation
- Use event delegation for dynamic content
- Lazy load images and heavy resources
- Cache API responses where appropriate

## Security Best Practices

1. **Never commit sensitive data**
   - Use environment variables for secrets
   - Keep `.env` in `.gitignore`

2. **Validate user input**
   - Sanitize all user inputs
   - Validate data types and formats
   - Use parameterized queries (SQLAlchemy handles this)

3. **Error handling**
   - Don't expose stack traces to users
   - Log errors securely
   - Return generic error messages

## Debugging

### Enable Debug Mode

In development, set in `.env`:

```env
FLASK_ENV=development
```

### View Logs

```bash
# Development
# Logs appear in console

# Production (Docker)
docker-compose logs -f loom

# Or check log file
tail -f /volume2/Dockerssd/loom/logs/loom.log
```

### Database Inspection

```python
# In Python shell
from app import create_app, db
from app.models import Note

app = create_app()
with app.app_context():
    notes = Note.query.all()
    print([n.to_dict() for n in notes])
```

## Contributing Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test thoroughly

3. Commit with clear messages:
   ```bash
   git commit -m "Add: Feature description"
   ```

4. Push and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Container Registry](https://docs.github.com/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

---

Happy coding! Build something amazing with LOOM.
