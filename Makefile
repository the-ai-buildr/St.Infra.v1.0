.PHONY: setup up down dev logs migrate revision shell db-shell seed test fmt lint check \
        push tf-init tf-plan tf-apply deploy clean

GCP_REGION   ?= us-central1
GCP_PROJECT_ID ?=
IMAGE_TAG    ?= latest
REPO         = $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT_ID)/streamlit-app/app

# ── Setup ─────────────────────────────────────────────────────────────────────
setup:
	uv sync --extra dev
	uv run pre-commit install

# ── Docker (local) ────────────────────────────────────────────────────────────
up:
	docker compose up -d

down:
	docker compose down

dev:
	docker compose up

logs:
	docker compose logs -f app

# ── Database ──────────────────────────────────────────────────────────────────
migrate:
	docker compose exec app uv run alembic upgrade head

revision:
	docker compose exec app uv run alembic revision --autogenerate -m "$(m)"

shell:
	docker compose exec app uv run python

db-shell:
	docker compose exec postgres sh -lc 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

seed:
	docker compose exec app uv run python scripts/seed.py

# ── Quality ───────────────────────────────────────────────────────────────────
fmt:
	uv run ruff format .

lint:
	uv run ruff check --fix .

test:
	uv run pytest -v

check: fmt lint test

# ── GCP deployment ────────────────────────────────────────────────────────────
push:
	docker build --target prod -t $(REPO):$(IMAGE_TAG) .
	docker push $(REPO):$(IMAGE_TAG)

tf-init:
	cd terraform && terraform init

tf-plan:
	cd terraform && terraform plan

tf-apply:
	cd terraform && terraform apply

deploy: push
	cd terraform && terraform apply -var="image_tag=$(IMAGE_TAG)" -auto-approve

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean:
	docker compose down -v
