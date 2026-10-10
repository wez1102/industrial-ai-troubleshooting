.DEFAULT_GOAL := help
.PHONY: up down db-shell db-reset help install run lint format typecheck test-unit ci migrate migration

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
	uv run ruff format .
	uv run ruff check . --fix

typecheck: ## Static type checking
	uv run mypy

test-unit: ## Unit tests with coverage
	uv run pytest -m unit --cov=plantassist --cov-report=term-missing --cov-report=xml

ci: lint typecheck test-unit ## Run everything CI runs

up: ## Start local services (Postgres) and wait until healthy
	docker compose up -d --wait

down: ## Stop local services (keeps data)
	docker compose down

db-shell: ## Open psql inside the Postgres container
	docker compose exec postgres psql -U plantassist -d plantassist

db-reset: ## Stop services and DELETE the database volume
	docker compose down -v


migrate: ## Apply all database migrations
	uv run alembic upgrade head

migration: ## Create a migration: make migration m="describe the change"
	uv run alembic revision --autogenerate -m "$(m)"
