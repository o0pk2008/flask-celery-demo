from celery import Celery
import sys
import os

# 确保可以导入 config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import celery_config

celery = Celery('tasks', broker=celery_config.CELERY_BROKER_URL, backend=celery_config.CELERY_RESULT_BACKEND)

# 可选：自动发现 tasks 目录下的任务
celery.autodiscover_tasks(['tasks']) 
import tasks.long_task  # <--- 关键：强制导入你的任务模块

print("已注册任务：", celery.tasks.keys())