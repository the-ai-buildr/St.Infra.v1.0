# St.Infra.v1.0 — Streamlit Data App Template

## What this project is
Reusable Streamlit + PostgreSQL template for rapid data-app development.
Auth via `streamlit-authenticator`. DB migrations via Alembic. File uploads via GCS.
Containerised with Docker Compose locally; deployed to GCP Cloud Run via Terraform.

## Stack
| Layer | Technology |
|---|---|
| UI | Streamlit 1.x (`app/main.py`, port 8501) |
| Auth | streamlit-authenticator (`app/auth.py`) |
| ORM | SQLAlchemy 2.x — sync + async (`app/db/session.py`) |
| Migrations | Alembic (`alembic/`) |
| Database | PostgreSQL 16 (service name `postgres` inside Docker) |
| Settings | pydantic-settings → single `settings` object (`app/config.py`) |
| File uploads | google-cloud-storage (`app/storage.py`) |
| Infra | Terraform (`terraform/`) → Cloud Run + Cloud SQL + GCS + Secret Manager |

## Key commands
| Command | What it does |
|---|---|
| `make setup` | `uv sync --dev` + pre-commit install |
| `make up` | Start Docker stack (background) |
| `make dev` | Start Docker stack (foreground, live logs) |
| `make down` | Stop containers |
| `make migrate` | `alembic upgrade head` inside app container |
| `make revision m="..."` | Autogenerate a new migration |
| `make seed` | Insert dev data (test@local.dev / dev1234) |
| `make test` | Run pytest |
| `make check` | fmt + lint + test (CI simulation) |
| `make db-shell` | psql prompt inside postgres container |
| `make fmt` | ruff format |
| `make lint` | ruff check --fix |
| `make deploy IMAGE_TAG=v1` | Build prod image, push to Artifact Registry, apply Terraform |

## Architecture decisions
- **Single settings import**: always `from app.config import settings` — never read env vars directly
- **Pages**: create `app/pages/foo.py`, then register `st.Page(...)` in `app/main.py` nav list
- **DB models**: inherit `Base` from `app/db/base.py`; run `make revision m="..."` then `make migrate`
- **File uploads**: call `upload_file()` / `get_signed_url()` from `app/storage.py`; set `GCS_BUCKET_NAME` in `.env`
- **Auth**: `require_login()` at top of each protected page returns `(name, username)`; swap `_DEV_CREDENTIALS` in `app/auth.py` for DB-backed loader in production
- **Sync vs async DB**: use `get_db()` context manager in Streamlit pages (sync); use `AsyncSessionLocal` in agent/API handlers (async)

## MCP servers (configured in .claude/settings.json)
- **postgres**: direct SQL access to the dev database — use for querying schema, debugging migrations, checking seed data
- **filesystem**: scoped file access to project root — reduces permission prompts during rapid development
- **AGENT_CLI_URL**: custom agent endpoint (set in `.env`) — add as `"type": "sse"` MCP server once deployed

## Dev credentials
- URL: http://localhost:8501
- Email: test@local.dev
- Password: dev1234
