# LOOM
**Life Organization & Operations Manager**

A self-hosted personal management application designed to run on your NAS, providing a unified interface for organizing multiple aspects of daily life.

## Overview

LOOM is a modern, modular web application that centralizes personal management tasks into a single, accessible interface. Built with object-oriented principles and clean architecture using Python and Flask, it's designed to be lightweight, maintainable, and extensible.

## Features

### Core Modules

- **Notes** - Markdown-based note-taking system for quick capture and organization
- **Calendar** - Visual calendar display for all scheduled events
- **Events** - Chronological list view of upcoming events
- **Todo List** - Task management with:
  - Timer-based reminders
  - Persistent weekly task table
  - Priority management
- **Recipe Manager** - Store and organize recipes with:
  - Categorization and tagging
  - Shopping list generation
  - Meal planning integration
- **Travel Planner** - Comprehensive trip organization:
  - Itinerary building
  - Packing lists (reusable templates)
  - Travel document tracking
  - Trip expense tracking

## Technology Stack

- **Backend**: Python 3.11, Flask
- **Database**: SQLite (with SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Containerization**: Docker
- **Deployment**: Docker Compose

## Installation

### Prerequisites

- Docker and Docker Compose installed on your NAS
- GitHub account for container registry access

### Deployment on NAS

1. **Clone the repository** (for development) or **pull the container** (for production):

   ```bash
   # For production - just create a directory for docker-compose
   mkdir -p /volume2/Dockerssd/loom
   cd /volume2/Dockerssd/loom
   ```

2. **Create docker-compose.yml** (already provided in the repository):

   The compose file is configured to:
   - Run on port 5001 (maps to internal port 5000)
   - Store data on your SSD at `/volume2/Dockerssd/loom/data`
   - Store logs at `/volume2/Dockerssd/loom/logs`

3. **Create a `.env` file** (optional, for custom configuration):

   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

4. **Start the application**:

   ```bash
   docker-compose up -d
   ```

5. **Access LOOM**:

   Open your browser and navigate to:
   ```
   http://<your-nas-ip>:5847
   ```

## Configuration

### Environment Variables

Create a `.env` file in the same directory as `docker-compose.yml`:

```env
SECRET_KEY=your-random-secret-key-here
DATABASE_PATH=/app/data/loom.db
FLASK_ENV=production
LOG_LEVEL=INFO
PORT=5847
```

### Volume Configuration

The application uses two main volumes:

- **Data Volume**: `/volume2/Dockerssd/loom/data` - Stores the SQLite database
- **Logs Volume**: `/volume2/Dockerssd/loom/logs` - Stores application logs

## Development

### Local Development Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/loom.git
   cd loom
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   python run.py
   ```

5. **Access the application**:

   Navigate to `http://localhost:5000`

### Building and Pushing Docker Image

1. **Build the Docker image**:

   ```bash
   docker build -t ghcr.io/yourusername/loom:latest .
   ```

2. **Push to GitHub Container Registry**:

   ```bash
   # Login to GitHub Container Registry
   echo $GITHUB_TOKEN | docker login ghcr.io -u yourusername --password-stdin

   # Push the image
   docker push ghcr.io/yourusername/loom:latest
   ```

## Project Structure

```
LOOM/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── note.py
│   │   ├── event.py
│   │   ├── todo.py
│   │   ├── recipe.py
│   │   └── travel.py
│   ├── modules/                 # Application modules (blueprints)
│   │   ├── dashboard/
│   │   ├── notes/
│   │   ├── calendar/
│   │   ├── events/
│   │   ├── todos/
│   │   ├── recipes/
│   │   └── travel/
│   ├── static/                  # Static files (CSS, JS, images)
│   │   ├── css/
│   │   └── js/
│   └── templates/               # HTML templates
│       ├── base.html
│       └── [module templates]/
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## API Documentation

### Notes API

- `GET /notes/api/notes` - Get all notes
- `POST /notes/api/notes` - Create a new note
- `GET /notes/api/notes/<id>` - Get a specific note
- `PUT /notes/api/notes/<id>` - Update a note
- `DELETE /notes/api/notes/<id>` - Delete a note

### Calendar/Events API

- `GET /calendar/api/events` - Get events (with date filters)
- `POST /calendar/api/events` - Create an event
- `PUT /calendar/api/events/<id>` - Update an event
- `DELETE /calendar/api/events/<id>` - Delete an event

### Todos API

- `GET /todos/api/todos` - Get all todos
- `POST /todos/api/todos` - Create a todo
- `PUT /todos/api/todos/<id>` - Update a todo
- `DELETE /todos/api/todos/<id>` - Delete a todo
- `GET /todos/api/todos/weekly` - Get weekly recurring todos

### Recipes API

- `GET /recipes/api/recipes` - Get all recipes
- `POST /recipes/api/recipes` - Create a recipe
- `GET /recipes/api/recipes/<id>` - Get a specific recipe
- `PUT /recipes/api/recipes/<id>` - Update a recipe
- `DELETE /recipes/api/recipes/<id>` - Delete a recipe
- `GET /recipes/api/shopping-list` - Get shopping list
- `POST /recipes/api/shopping-list/from-recipe/<id>` - Add recipe to shopping list

### Travel API

- `GET /travel/api/trips` - Get all trips
- `POST /travel/api/trips` - Create a trip
- `GET /travel/api/trips/<id>` - Get trip details
- `PUT /travel/api/trips/<id>` - Update a trip
- `DELETE /travel/api/trips/<id>` - Delete a trip
- `POST /travel/api/trips/<id>/itinerary` - Add itinerary item
- `POST /travel/api/trips/<id>/packing-list` - Create packing list
- `POST /travel/api/trips/<id>/expenses` - Add expense

## Security Considerations

- Change the `SECRET_KEY` in your `.env` file to a random, secure value
- LOOM is designed for home network use only
- Access via NAS IP and port (not exposed to the internet by default)
- No authentication is built-in (relies on network security)
- For internet access, consider:
  - Setting up a VPN to your home network
  - Adding authentication middleware
  - Using a reverse proxy with SSL/TLS

## Backup

The database is stored in `/volume2/Dockerssd/loom/data/loom.db`. Regular backups of this file are recommended:

```bash
# Example backup script
cp /volume2/Dockerssd/loom/data/loom.db /volume2/Dockerssd/loom/backups/loom-$(date +%Y%m%d).db
```

## Troubleshooting

### Application won't start

1. Check Docker logs:
   ```bash
   docker-compose logs loom
   ```

2. Verify volumes exist and have correct permissions:
   ```bash
   ls -la /volume2/Dockerssd/loom/
   ```

### Database errors

1. Ensure the data directory is writable
2. Check database file permissions
3. Review logs at `/volume2/Dockerssd/loom/logs/loom.log`

### Can't access from browser

1. Verify the container is running:
   ```bash
   docker ps | grep loom
   ```

2. Check port 5847 is not blocked by firewall
3. Verify firewall rules on NAS
4. Try accessing: http://<nas-ip>:5847

## Contributing

This is a personal project, but suggestions and improvements are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Roadmap

- [ ] Enhanced calendar UI with drag-and-drop
- [ ] Mobile-responsive improvements
- [ ] Export/import functionality
- [ ] Calendar sync with external calendars
- [ ] Email notifications for reminders
- [ ] Dark mode theme
- [ ] Multi-user support with authentication
- [ ] RESTful API improvements
- [ ] Progressive Web App (PWA) support

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**LOOM** - Your life, organized.
