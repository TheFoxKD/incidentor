# Incidentor API

Мини-сервис для учёта инцидентов (создание, просмотр, изменение статуса) с REST API на FastAPI + PostgreSQL.

## Стек

- Python 3.14, FastAPI, SQLAlchemy 2.x, Alembic
- PostgreSQL 17
- Dishka (dependency injection)
- Structlog (структурированные логи)
- Docker, Docker Compose, Makefile, uv

## Запуск (Docker Compose)

```bash
cp .env.example .env
make build
make up
```

После старта:
- API доступен на <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- Health-check: `GET http://localhost:8000/healthz`

Остановить сервисы:

```bash
make down
```

### Полезные make-цели

| Команда | Описание |
| --- | --- |
| `make build` | Сборка образов |
| `make up` | Поднять стек (api + postgres) |
| `make down` | Остановить/удалить сервисы |
| `make logs` | Тейлить логи API |
| `make format` | `ruff format` внутри контейнера |
| `make lint` | `ruff check` + `mypy` |
| `make test` | `pytest` |
| `make makemigrations name="add_feature"` | Alembic revision (autogenerate) |
| `make migrate` | Alembic upgrade head |
| `make shell` | Bash внутри контейнера API |

## Конфигурация окружения

Переменные задаются через `.env` / env vars (см. `.env.example`). Базовые значения:

```
APP_SERVICE_NAME=incidentor
APP_ENVIRONMENT=development
APP_HOST=0.0.0.0
APP_PORT=8000

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

## Миграции БД

```bash
make makemigrations name="init"
make migrate
```

Первичная миграция уже создана: `alembic/versions/0001_initial_incidents.py`.

## Эндпоинты

| Метод | Путь | Описание |
| --- | --- | --- |
| `GET /healthz` | | Проверка доступности БД |
| `POST /api/v1/incidents` | | Создать инцидент |
| `GET /api/v1/incidents?status=new` | | Список инцидентов (фильтр по статусу) |
| `PATCH /api/v1/incidents/{id}` | | Обновить статус инцидента |

### Примеры запросов

Создание инцидента:

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

## Тестирование

```bash
make test
```

(Пока тесты не добавлены — цель зарезервирована.)

## Структура проекта

```
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

Структурированные JSON-логи через structlog со следующими ключами: `timestamp`, `level`, `service`, `environment`, `event`, `module`, `exc_info` (при ошибках).

## Дополнительно

- DI управляется через Dishka (`src/core/dependencies.py`).
- Конфигурация `ruff` и `mypy` находится в `pyproject.toml` (`select = ["ALL"]` специально для строгой статики — при необходимости скорректируйте под проект).
