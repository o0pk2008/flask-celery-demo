from . import db
from datetime import datetime

class TaskRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(64), unique=True, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 默认 pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)