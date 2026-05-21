# Streamlit App Template

A production-ready Streamlit data-app template with PostgreSQL, authentication,
file uploads, and one-command GCP deployment via Terraform.

## Architecture

```
Browser
  └─▶ Cloud Run (Streamlit, port 8501)
        ├─▶ Cloud SQL  (PostgreSQL 16, private IP)
        ├─▶ Cloud Storage  (file uploads)
        └─▶ Secret Manager  (credentials)
```

| Layer | Technology |
|---|---|
| UI | Streamlit 1.x |
| Auth | streamlit-authenticator |
| ORM | SQLAlchemy 2.x (sync + async) |
| Migrations | Alembic |
| Database | PostgreSQL 16 |
| Settings | pydantic-settings |
| File uploads | google-cloud-storage |
| Container | Docker / Docker Compose |
| Infra | Terraform → GCP (Cloud Run + Cloud SQL + GCS) |
| Package manager | uv |
| Linter | Ruff |
| CI | GitHub Actions |

---

## Local Development — Quickstart

**Prerequisites:** Python 3.12+, [uv](https://docs.astral.sh/uv/), Docker Desktop

```bash
cp .env.example .env        # defaults work out of the box for local dev
make setup                  # uv sync + pre-commit install
make up                     # start Postgres + Streamlit (background)
make migrate                # run Alembic migrations
make seed                   # insert dev user
```

Open **http://localhost:8501** and log in with `test@local.dev` / `dev1234`.

Use `make dev` instead of `make up` for foreground mode with live logs (Ctrl+C to stop).
The app hot-reloads when you edit any file under `app/`.

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `POSTGRES_USER` | Postgres username | `postgres` |
| `POSTGRES_PASSWORD` | Postgres password | `postgres` |
| `POSTGRES_DB` | Database name | `streamlit_app` |
| `POSTGRES_HOST` | Hostname (Docker: `postgres`) | `postgres` |
| `POSTGRES_PORT` | Port | `5432` |
| `AUTH_COOKIE_KEY` | 32-byte hex for cookie signing | — |
| `APP_ENV` | `local` / `staging` / `production` | `local` |
| `AGENT_CLI_URL` | External agent MCP endpoint | — |
| `GCP_PROJECT_ID` | GCP project ID | — |
| `GCP_REGION` | GCP region | `us-central1` |
| `GCS_BUCKET_NAME` | GCS bucket for file uploads | — |
| `CLOUD_SQL_CONNECTION_NAME` | Cloud SQL connection name | — |
| `DATABASE_URL` | Full sync DB URL (auto-assembled if blank) | — |
| `ASYNC_DATABASE_URL` | Full async DB URL (auto-assembled if blank) | — |

Generate `AUTH_COOKIE_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Adding a Page

1. Create `app/pages/my_page.py`:
   ```python
   import streamlit as st

   def render() -> None:
       st.title("My Page")
   ```

2. Register it in `app/main.py`:
   ```python
   my_page = st.Page("pages/my_page.py", title="My Page", icon=":material/star:")
   pg = st.navigation([home_page, my_page])
   ```

---

## Adding a Database Model

1. Create `app/models/my_model.py` (create the `models/` directory if needed):
   ```python
   from sqlalchemy import String
   from sqlalchemy.orm import Mapped, mapped_column
   from app.db.base import Base

   class MyModel(Base):
       __tablename__ = "my_models"
       id: Mapped[int] = mapped_column(primary_key=True)
       name: Mapped[str] = mapped_column(String(255))
   ```

2. Import the model in `alembic/env.py` so autogenerate sees it:
   ```python
   import app.models.my_model  # noqa: F401
   ```

3. Generate and apply the migration:
   ```bash
   make revision m="add my_model"
   make migrate
   ```

---

## File Uploads (GCS)

Set `GCS_BUCKET_NAME` in `.env`. In a Streamlit page:

```python
import streamlit as st
from app.storage import upload_file, get_signed_url

uploaded = st.file_uploader("Upload a file")
if uploaded:
    uri = upload_file(uploaded.getvalue(), f"uploads/{uploaded.name}", uploaded.type)
    st.success(f"Uploaded: {uri}")
    url = get_signed_url(f"uploads/{uploaded.name}", expiry_minutes=60)
    st.markdown(f"[Download link]({url})")
```

---

## GCP Deployment

See [`docs/dev-setup.md`](docs/dev-setup.md) for first-time GCP project setup.

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# Edit terraform.tfvars — set project_id, db_password, auth_cookie_key

gcloud auth application-default login
make tf-init
make tf-plan     # review resources to be created
make tf-apply    # provision Cloud Run, Cloud SQL, GCS, Secret Manager

make deploy IMAGE_TAG=v1   # build prod image + deploy
terraform -chdir=terraform output service_url
```

---

## Make Command Reference

| Command | Description |
|---|---|
| `make setup` | Install dependencies and pre-commit hooks |
| `make up` | Start Docker stack (background) |
| `make dev` | Start Docker stack (foreground, live logs) |
| `make down` | Stop Docker stack |
| `make logs` | Tail app container logs |
| `make migrate` | Run Alembic migrations (inside container) |
| `make revision m="..."` | Autogenerate a new migration |
| `make seed` | Seed dev data |
| `make shell` | Python REPL inside app container |
| `make db-shell` | psql prompt inside postgres container |
| `make test` | Run pytest |
| `make fmt` | Format code with ruff |
| `make lint` | Lint and auto-fix with ruff |
| `make check` | fmt + lint + test (CI simulation) |
| `make push` | Build prod image and push to Artifact Registry |
| `make tf-init` | `terraform init` |
| `make tf-plan` | `terraform plan` |
| `make tf-apply` | `terraform apply` |
| `make deploy IMAGE_TAG=v1` | Build, push, and deploy to Cloud Run |
| `make clean` | Stop containers and delete volumes |

---

## Project Structure

```
.
├── app/
│   ├── main.py          # Streamlit entry point + navigation
│   ├── auth.py          # streamlit-authenticator wrapper
│   ├── config.py        # pydantic-settings (single source of truth)
│   ├── storage.py       # GCS upload/download helpers
│   ├── pages/           # Add page modules here
│   └── db/
│       ├── base.py      # SQLAlchemy DeclarativeBase
│       └── session.py   # Sync + async session factories
├── alembic/
│   ├── env.py           # Migration runner (reads settings)
│   └── versions/        # Migration files (auto-generated)
├── terraform/           # GCP infrastructure as code
├── tests/               # pytest — conftest.py + smoke tests
├── scripts/
│   └── seed.py          # Dev data seeder
├── .claude/
│   └── settings.json    # Claude Code permissions + MCP servers + hooks
├── .streamlit/
│   └── config.toml      # Streamlit server + theme config
├── .github/workflows/
│   └── ci.yml           # Lint + test on every push
├── CLAUDE.md            # AI session context (loaded by Claude Code)
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── pyproject.toml
└── Makefile
```
