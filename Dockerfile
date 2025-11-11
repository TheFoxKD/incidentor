FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder
WORKDIR /app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      gcc build-essential python3-dev libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project
COPY src ./src
COPY alembic ./alembic
RUN uv sync --locked

FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS runtime
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/alembic /app/alembic
COPY pyproject.toml ./

ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000
# Development server
CMD ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
