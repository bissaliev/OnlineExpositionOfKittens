#!/bin/bash

# Ожидаем доступности базы данных
/app/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Postgres is up - executing command"

# Выполняем миграции
python manage.py migrate

# Сборка статики
python manage.py collectstatic --no-input

# Загрузка фикстур
python manage.py loaddata fixtures/users
python manage.py loaddata fixtures/breeds
python manage.py loaddata fixtures/cats
python manage.py loaddata fixtures/ratings

# Запуск сервера
exec gunicorn --bind 0:8000 cats_exposition.wsgi