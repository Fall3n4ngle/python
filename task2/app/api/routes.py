from flask import jsonify, request, Blueprint
from werkzeug.exceptions import BadRequest, NotFound
from extensions import db
from app.models.todo import Todo

api_bp = Blueprint('api', __name__)

@api_bp.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todos_list = [{"id": todo.id, "title": todo.title, "complete": todo.complete, "description": todo.description} for todo in todos]
    return jsonify(todos_list)

@api_bp.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()

    if 'title' not in data or 'description' not in data:
        raise BadRequest('Title та description є обов\'язковими полями.')

    new_todo = Todo(title=data['title'], complete=data.get('complete', False), description=data['description'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "Todo created successfully"}), 201

@api_bp.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        raise NotFound('Todo не знайдено за вказаним id.')

    todo_data = {"id": todo.id, "title": todo.title, "complete": todo.complete, "description": todo.description}
    return jsonify(todo_data)

@api_bp.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        raise NotFound('Todo не знайдено за вказаним id.')

    data = request.get_json()

    if 'title' not in data or 'description' not in data:
        raise BadRequest('Title та description є обов\'язковими полями.')

    todo.title = data['title']
    todo.complete = data.get('complete', False)
    todo.description = data['description']
    db.session.commit()
    return jsonify({"message": "Todo updated successfully"})

@api_bp.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)

    if not todo:
        raise NotFound('Todo не знайдено за вказаним id.')

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted successfully"})
