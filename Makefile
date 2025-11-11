SHELL := /bin/bash

PROJECT_NAME := incidentor
COMPOSE := docker compose
SERVICE := api

.PHONY: help build up down logs lint format test makemigrations migrate shell

help:
	@echo "Available targets:"
	@echo "  build           Build docker images"
	@echo "  up              Start services in foreground"
	@echo "  down            Stop services"
	@echo "  makemigrations  Autogenerate Alembic migration (use name=message)"
	@echo "  migrate         Apply database migrations"
	@echo "  shell           Run shell inside API container"

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up

down:
	$(COMPOSE) down


makemigrations:
	$(COMPOSE) run --rm $(SERVICE) uv run alembic revision --autogenerate -m "${name}"

migrate:
	$(COMPOSE) run --rm $(SERVICE) uv run alembic upgrade head

shell:
	$(COMPOSE) run --rm $(SERVICE) bash
