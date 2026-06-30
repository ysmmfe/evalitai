.DEFAULT_GOAL := help

.PHONY: help dev stop migrate seed test lint e2e

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  dev      Start full stack (API, worker, web, Postgres, Redis, MinIO)"
	@echo "  stop     Stop all containers"
	@echo "  migrate  Run database migrations (alembic upgrade head)"
	@echo "  seed     Load demo data"
	@echo "  test     Run unit + integration tests"
	@echo "  lint     Run ruff, mypy, eslint, tsc"
	@echo "  e2e      Run Playwright end-to-end tests"

dev:
	docker compose -f infra/docker-compose.yml up

stop:
	docker compose -f infra/docker-compose.yml down

migrate:
	docker compose -f infra/docker-compose.yml exec api alembic upgrade head

seed:
	docker compose -f infra/docker-compose.yml exec api python -m seeds.run

test:
	docker compose -f infra/docker-compose.yml exec api pytest tests/unit tests/integration

lint:
	docker compose -f infra/docker-compose.yml exec api ruff check . && mypy .
	cd apps/web && pnpm lint && pnpm tsc --noEmit

e2e:
	cd tests/e2e && pnpm playwright test
