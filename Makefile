# Makefile for Task Planner Library

.PHONY: install test lint clean build

install: ## Install dependencies
	poetry install

test: ## Run tests
	poetry run pytest

lint: ## Run linting
	poetry run ruff check .

clean: ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info

build: clean ## Build package
	poetry build
