from flask_login import login_required
from flask import make_response, jsonify, request

from server.model import db
from server import app
from server.model.Task import Task


@app.route('/tasks', methods=['get'])
@login_required
def get_tasks():
    filters = request.values
    if filters is None:
        tasks = Task.query.all()
    else:
        user_id = filters['userId']
        week_id = filters['weekId']
        tasks = Task.query.filter_by(user_id=user_id, week_id=week_id)
    result = {
        "success": True,
        "total": tasks.count(),
        "tasks": [task.serialize() for task in tasks]
    }
    response = make_response(jsonify(result), 200)
    return response


@app.route('/tasks/<task_id>')
@login_required
def read_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task is None:
        response = make_response(jsonify({}), 404)
    else:
        result = {
            "task": task.serialize()
        }
        response = make_response(jsonify(result), 200)
    return response


@app.route('/tasks', methods=['post'])
@login_required
def create_task():
    task = Task(request.values)
    db.session.add(task)
    db.session.commit()

    result = {
        'success': True,
        'task': task.serialize()
    }
    response = make_response(jsonify(result), 200)
    return response


@app.route('/tasks/<task_id>', methods=['delete'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    result = {'success': True}
    response = make_response(jsonify(result), 200)
    return response


@app.route('/tasks/<task_id>', methods=['put'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    new_task = Task(request.values)
    task.name = new_task.name
    task.status = new_task.status
    task.project = new_task.project
    task.progress = new_task.progress
    task.description = new_task.description
    task.risk = new_task.risk
    task.eta = new_task.eta
    db.session.commit()

    result = {'success': True}
    response = make_response(jsonify(result), 200)
    return response
