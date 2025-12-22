"""
Todos Routes - Task management with reminders
"""
from flask import render_template, request, jsonify
from datetime import datetime
from app.modules.todos import todos_bp
from app.models.todo import Todo, TodoReminder
from app import db

@todos_bp.route('/')
def index():
    """Todos page"""
    return render_template('todos/index.html')

@todos_bp.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    status = request.args.get('status')
    priority = request.args.get('priority')

    query = Todo.query

    if status:
        query = query.filter_by(status=status)

    if priority:
        query = query.filter_by(priority=priority)

    todos = query.order_by(Todo.priority.desc(), Todo.due_date).all()
    return jsonify([todo.to_dict() for todo in todos])

@todos_bp.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    data = request.get_json()

    todo = Todo(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'pending'),
        due_date=datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')) if data.get('due_date') else None,
        is_weekly=data.get('is_weekly', False),
        week_day=data.get('week_day'),
        category=data.get('category')
    )

    db.session.add(todo)
    db.session.commit()

    # Create reminders if specified
    if 'reminders' in data:
        for reminder_data in data['reminders']:
            reminder = TodoReminder(
                todo_id=todo.id,
                reminder_time=datetime.fromisoformat(reminder_data['reminder_time'].replace('Z', '+00:00')),
                message=reminder_data.get('message')
            )
            db.session.add(reminder)

        db.session.commit()

    return jsonify(todo.to_dict()), 201

@todos_bp.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo"""
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()

    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.priority = data.get('priority', todo.priority)
    todo.status = data.get('status', todo.status)

    if 'due_date' in data and data['due_date']:
        todo.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))

    if 'completed_at' in data:
        if data['completed_at']:
            todo.completed_at = datetime.utcnow()
        else:
            todo.completed_at = None

    db.session.commit()

    return jsonify(todo.to_dict())

@todos_bp.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()

    return '', 204

@todos_bp.route('/api/todos/weekly', methods=['GET'])
def get_weekly_todos():
    """Get weekly recurring todos"""
    weekly_todos = Todo.query.filter_by(is_weekly=True).order_by(Todo.week_day).all()
    return jsonify([todo.to_dict() for todo in weekly_todos])
