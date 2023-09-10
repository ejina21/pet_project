from celery import Celery
from app.config import settings

celery = Celery(
    "tasks",
    broker=f"{settings.REDIS_SCHEME}://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks"]
)