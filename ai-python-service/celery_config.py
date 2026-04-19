# celery_config.py
import os
from dotenv import load_dotenv
from celery import Celery

# Load env variables first
load_dotenv()

# Force the 127.0.0.1 fallback
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')

celery_app = Celery(
    'unified_student_ecosystem',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['tasks'] # Explicitly tell Celery where to find your tasks
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)