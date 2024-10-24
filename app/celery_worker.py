from time import sleep
from celery import Celery
from app.config import settings

celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery.task
def background_task(data):
    sleep(30)
    return {"status": "Task Completed", "data": data}
