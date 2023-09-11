# pet_project
fast-api

# Полезные команды
1. uvicorn app.main:app --reload 
2. celery -A app.tasks.celery_config:celery worker --loglevel=INFO --pool=solo
3. celery -A app.tasks.celery_config:celery flower
4. pytest -v -s #запуск тестов

# Линтеры
1. black path/ --diff --color
2. flake8 path/
3. isort path/
4. autoflake path/ -r
5. pyright path/