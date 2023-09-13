# Бронирование отелей
Это репозиторий к курсу о бэкенд разработке на Python с упором на изучение FastAPI и работы с SQLAlchemy, Celery, Redis, Docker, а также многими другими библиотеками и технологиями.

Это репозиторий к тарифам "С поддержкой" и "Персональный", предполагающий наличие моих решений практических задач и с комментариями к коду.

## Запуск приложения
Для запуска FastAPI используется веб-сервер uvicorn. Команда для запуска выглядит так:  
```
uvicorn app.main:app --reload
```  
Ее необходимо запускать в командной строке, обязательно находясь в корневой директории проекта.

### Celery & Flower
Для запуска Celery используется команда  
```
celery --app=app.tasks.celery:celery worker -l INFO -P solo
```
Обратите внимание, что `-P solo` используется только на Windows, так как у Celery есть проблемы с работой на Windows.  
Для запуска Flower используется команда  
```
celery --app=app.tasks.celery:celery flower
``` 

### Dockerfile
Для запуска веб-сервера (FastAPI) внутри контейнера необходимо раскомментировать код внутри Dockerfile и иметь уже запущенный экземпляр PostgreSQL на компьютере.
Код для запуска Dockerfile:  
```
docker build .
```  
Команда также запускается из корневой директории, в которой лежит файл Dockerfile.

### Docker compose
Для запуска всех сервисов (БД, Redis, веб-сервер (FastAPI), Celery, Flower, Grafana, Prometheus) необходимо использовать файл docker-compose.yml и команды
```
docker compose build
docker compose up
```
Причем `build` команду нужно запускать, только если вы меняли что-то внутри Dockerfile, то есть меняли логику составления образа.

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