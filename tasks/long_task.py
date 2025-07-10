from .celery import celery
import time

from app import create_app, db
from app.models import TaskRecord

app = create_app()

@celery.task(bind=True)
def long_time_task(self, duration=10):
    with app.app_context():
        record = db.session.query(TaskRecord).filter_by(task_id=self.request.id).first()
        print(f"任务 {self.request.id} 查到记录: {record}")
        if record:
            record.status = 'running'
            db.session.commit()
            print(f"任务 {self.request.id} 状态已更新为 running")
        try:
            time.sleep(duration)
            if record:
                record.status = 'success'
                db.session.commit()
                print(f"任务 {self.request.id} 状态已更新为 success")
            return {'status': 'Task completed!', 'duration': duration}
        except Exception as e:
            if record:
                record.status = 'failed'
                db.session.commit()
                print(f"任务 {self.request.id} 状态已更新为 failed")
            raise e
        finally:
            db.session.remove()  # 只在最后 remove 一次