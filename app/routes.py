from flask import Blueprint, request, jsonify, render_template
from tasks.long_task import long_time_task
from celery.result import AsyncResult
from tasks.celery import celery
from app.models import TaskRecord
from app import db

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json() or {}
    duration = data.get('duration', 10)
    # 先生成 task_id
    import uuid
    task_id = str(uuid.uuid4())
    # 先写入数据库
    record = TaskRecord(task_id=task_id, duration=duration, status='pending')
    db.session.add(record)
    db.session.commit()
    # 再分发任务，指定 task_id
    task = long_time_task.apply_async(args=[duration], task_id=task_id)
    return jsonify({'task_id': task.id}), 202

@bp.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    """
    查询任务状态和结果。
    """
    task = AsyncResult(task_id, app=celery)
    response = {
        'task_id': task_id,
        'state': task.state,
        'result': task.result if task.state == 'SUCCESS' else None
    }
    return jsonify(response) 