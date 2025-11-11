# 1) Builder — содержит компиляторы, собирает /.venv
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder
WORKDIR /app

# Устанавливаем только в билдере
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      gcc build-essential python3-dev libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Кэш зависимостей
COPY pyproject.toml uv.lock ./
# создаём виртуальное окружение и устанавливаем зависимости (внутри .venv)
RUN uv sync --locked --no-install-project
# Установим проект в .venv
COPY src ./src
COPY alembic ./alembic
RUN uv sync --locked

# 2) Final — минимальный runtime, копируем только .venv
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS runtime
WORKDIR /app

# Скопировать только готовое окружение и нужное содержимое
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/alembic /app/alembic
COPY pyproject.toml ./

ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000
CMD ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
