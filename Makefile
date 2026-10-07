.DEFAULT_GOAL := help
.PHONY: help install run lint format typecheck test-unit ci

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies and git hooks
	uv sync --locked
	uv run pre-commit install

run: ## Start the dev server with auto-reload
	uv run uvicorn plantassist.main:create_app --factory --reload

lint: ## Lint and check formatting (no changes)
	uv run ruff check .
	uv run ruff format --check .

format: ## Auto-fix lint issues and format code
	uv run ruff check . --fix
	uv run ruff format .

typecheck: ## Static type checking
	uv run mypy

test-unit: ## Unit tests with coverage
	uv run pytest -m unit --cov=plantassist --cov-report=term-missing --cov-report=xml

ci: lint typecheck test-unit ## Run everything CI runs
