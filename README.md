# pet_project
fast-api

# Полезные команды
1. uvicorn app.main:app --reload 
2. celery -A app.tasks.celery_config:celery worker --loglevel=INFO --pool=solo
3. celery -A app.tasks.celery_config:celery flower