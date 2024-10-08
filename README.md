# OnlineExpositionOfKittens

## Онлайн выставка котят

## Описание

**Cats API** — это RESTful API для управления данными о котиках, породах, рейтингах, а также аутентификацией пользователей. Проект реализован с использованием Django, Django REST Framework (DRF), и JWT-аутентификации через Djoser. Проект настроен для работы в контейнерах `Docker`(API-проект, Nginx, PostgreSQL). Инфраструктура собирается и запускается с помощью docker-compose. Для проверки работоспособности проекта написаны тесты, подготовлены фикстуры. Процессы (выполнение миграций, сборка статики, загрузка фикстур) автоматизированы с помощью bash-скриптов.

## Технологии

- `Python 3.12`
- `Django 5.1`
- `Django REST Framework 3.15`
- `Django Filter`
- `Djoser (JWT)`
- `Gunicorn`
- `Nginx`
- `PostgreSQL`
- `pytest`
- `Docker`
- `Swagger (drf_yasg)`

## Функциональность

### Основные модели

- **Cat** — котик с полями: имя, цвет, описание, дата рождения, хозяин, порода, средний рейтинг.
- **Breed** — порода котика.
- **Rating** — рейтинг котика, который могут ставить пользователи (1-5).

### Эндпоинты

- `GET /api/cats/` — список всех котиков с фильтрацией по цвету, породе, владельцу и рейтингу.
- `GET /api/cats/{id}/` — информация о котике по ID.
- `POST /api/cats/` — создание нового котика (для авторизованных пользователей).
- `PATCH /api/cats/{id}/` — редактирование данных котика (только владельцем).
- `DELETE /api/cats/{id}/` — удаление котика (только владельцем).
- `GET /api/breeds/` — список всех пород котиков.
- `GET /api/breeds/{id}/` — информация о породе по ID.
- `POST /api/breeds/` — создание новой породы котика (для администратора).
- `PATCH /api/breeds/{id}/` — редактирование данных породы котика (только администратором).
- `DELETE /api/breeds/{id}/` — удаление породы котика (только администратором).
- `GET /api/cats/{id}/rating/` — просмотр всех оценок котика.
- `POST /api/cats/{id}/rating/` — добавить оценку котику (нельзя оценивать своего котика).
- `PATCH /api/cats/{id}/rating/{id}` — изменить оценку котику.
- `DELETE /api/cats/{id}/rating/{id}` — удалить оценку котику.

### Аутентификация

Проект использует JWT для аутентификации пользователей. Аутентификация настраивается через Djoser:

- `POST /auth/jwt/create/` — получение JWT-токена.
- `POST /auth/jwt/refresh/` — обновление JWT-токена.
- `POST /auth/jwt/verify/` — проверка валидности токена.

### Фильтрация

Котиков можно фильтровать по следующим параметрам:

- Порода: `?breed=<breed_name>`
- Владелец: `?owner=<username>`
- Цвет: `?color=<color>`
- Средний рейтинг: `?rating=<min_rating>`

### Права доступа

- Только пользователи с токеном авторизации могут создавать или редактировать котиков и рейтинги.
- Изменять данные котика может только его владелец.
- Оценивать котика не может его владелец.
- Создавать, изменять и удалять породы котиков может только администратор.

## Тестирование

Проект поддерживает тесты с использованием `pytest`. Чтобы запустить тесты, выполните команду:

```bash
pytest
```

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:bissaliev/OnlineExpositionOfKittens.git
cd OnlineExpositionOfKittens/
```

Настройка переменных окружения
Создайте файл .env в корне проекта и укажите в нем следующие переменные:

```env
SECRET_KEY=<ваш секретный ключ>
DB_NAME=catmen
POSTGRES_USER=catmen
POSTGRES_PASSWORD=catmen
DB_HOST=db
DB_PORT=5432
```

Запуск проекта в Docker
Проект настроен для работы в контейнерах `Docker`. Чтобы запустить проект, выполните:

```bash
cd infra/
docker compose up --build
```

[Перейти на сайт](http://localhost/api/v1/cats/)

Документация доступна по следующему пути:

[http://localhost/api/v1/docs/](http://localhost/api/v1/docs/)

### Автор

[Биссалиев Олег](https://github.com/bissaliev)
