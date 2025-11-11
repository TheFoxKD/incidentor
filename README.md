# Incidentor API

Мини-сервис для учёта инцидентов (создание, просмотр, изменение статуса) с REST API на FastAPI + PostgreSQL.

## Контакты

- Telegram: [t.me/thefoxdk](https://t.me/thefoxdk)
- Email: [krishtopadenis@gmail.com](mailto:krishtopadenis@gmail.com)

## Содержание

- [Контакты](#контакты)
- [Запуск](#запуск-docker-compose)
- [Стек](#стек)
- [Make-команды](#make-команды)
- [Конфигурация окружения](#конфигурация-окружения-env)
- [Миграции БД](#миграции-бд-alembic)
- [Эндпоинты и примеры](#эндпоинты-и-примеры)
- [Структура проекта](#структура-проекта)
- [Логи](#логи)
- [Примечания](#примечания)

## Запуск (Docker Compose)

```bash
cp .env.example .env
```

```bash
make build
```

При первом запуске необходимо выполнить миграции:
```bash
make migrate
```

```bash
make up
```

После старта:

- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- Health: `GET /healthz`

Остановка:

```bash
make down
```

## Стек

- Python 3.14, FastAPI, SQLAlchemy 2.x, Alembic
- PostgreSQL 17
- Dishka (dependency injection)
- Structlog (структурированные логи)
- Docker, Docker Compose, Makefile, uv

## Make-команды

| Команда | Описание |
| --- | --- |
| `make build` | Сборка образов |
| `make up` | Поднять стек (api + postgres) |
| `make down` | Остановить/удалить сервисы |
| `make makemigrations name="add_feature"` | Alembic revision (autogenerate) |
| `make migrate` | Alembic upgrade head |
| `make shell` | Bash внутри контейнера API |

## Конфигурация окружения (.env)

```text
APP_SERVICE_NAME=incidentor
APP_ENVIRONMENT=development

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=incidentor
POSTGRES_USER=incidentor
POSTGRES_PASSWORD=incidentor

DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800
```

## Миграции БД (Alembic)

```bash
make makemigrations name="init"
```

```bash
make migrate
```

Автогенерация создаст файл в `alembic/versions/` на основе текущих моделей.

## Эндпоинты и примеры

| Метод | Путь | Описание |
| --- | --- | --- |
| GET | /healthz` |  Проверка доступности БД |
| POST | /api/v1/incidents` | Создать инцидент |
| GET | /api/v1/incidents?status=new` | Список инцидентов (фильтр по статусу) |
| PATCH | /api/v1/incidents/{id}` | Обновить статус инцидента |

Создание:

```bash
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{"description": "Самокат недоступен", "source": "operator"}'
```

Обновление статуса:

```bash
curl -X PATCH http://localhost:8000/api/v1/incidents/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

Список с фильтром:

```bash
curl "http://localhost:8000/api/v1/incidents?status=new"
```

## Структура проекта

```text
src/
  api/                # FastAPI роутеры и endpoints
  core/               # Настройки, DI, логирование, lifespan
  db/                 # SQLAlchemy factories
  models/             # ORM модели и базы
  repositories/       # Доступ к БД
  schemas/            # Pydantic схемы API
  services/           # Бизнес-логика
alembic/              # Миграции БД
Dockerfile
docker-compose.yml
Makefile
```

## Логи

Структурированные JSON-логи через structlog со следующими ключами:
`timestamp`, `level`, `service`, `environment`, `event`, `module`, `exc_info` (при ошибках).

## Примечания

- DI управляется через Dishka (`src/core/dependencies.py`).
- Конфигурация `ruff`/`mypy` в `pyproject.toml`
