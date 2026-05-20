.PHONY: setup up down logs migrate revision shell seed test fmt lint clean

setup:
	uv sync
	uv pip install pre-commit
	uv run pre-commit install

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f app

migrate:
	alembic upgrade head

revision:
	alembic revision --autogenerate -m "$(m)"

shell:
	docker compose exec app python

seed:
	@echo "Seeding user test@local.dev"
	@# TODO: actual seed script when db is ready
	@echo "Seeded user test@local.dev with password dev1234"

test:
	pytest

fmt:
	ruff format .

lint:
	ruff check --fix .

clean:
	docker compose down -v
