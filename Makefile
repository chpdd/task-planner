# Makefile for Task Planner

# Variables
DC = docker compose
DC_DEV = $(DC)
DC_PROD = $(DC) -f docker-compose.yml
DC_TEST = $(DC) -f docker-compose.yml -f docker-compose.test.yml

.PHONY: dev prod test down build help logs shell lint clean db-shell

default: dev

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  dev      Run development environment (with hot reload)"
	@echo "  prod     Run production verification (strict build)"
	@echo "  test     Run tests"
	@echo "  build    Build/Rebuild all images"
	@echo "  down     Stop all containers"
	@echo "  logs     Follow logs for all services"
	@echo "  shell    Enter the web container shell"
	@echo "  lint     Run code linting (ruff)"
	@echo "  clean    Remove all containers, networks, and volumes"

dev: ## Run development environment
	$(DC_DEV) up --build

prod: ## Run production verification
	$(DC_PROD) up --build

test: ## Run tests
	$(DC_TEST) up --build --exit-code-from web

down: ## Stop containers
	$(DC) down --remove-orphans

build: ## Build images
	$(DC) build

logs: ## Follow logs
	$(DC) logs -f

shell: ## Enter web container
	$(DC_DEV) exec web bash

lint: ## Run linting
	$(DC_DEV) run --rm web poetry run ruff check .

lint-watch:
	$(DC_DEV) run --rm web poetry run ruff check . -w


clean: ## Nuke everything
	$(DC) down -v --remove-orphans --rmi local

db-shell: ## Enter Postgres shell
	$(DC) exec postgres psql -U admin -d task_planner_db
