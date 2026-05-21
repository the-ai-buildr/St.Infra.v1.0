# Developer Setup Guide

## Prerequisites

| Tool | Install |
|---|---|
| Python 3.12+ | [python.org](https://www.python.org/downloads/) or `pyenv install 3.12` |
| uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Docker Desktop | [docs.docker.com](https://docs.docker.com/get-docker/) |
| Node.js 18+ (for MCP servers) | [nodejs.org](https://nodejs.org/) |
| gcloud CLI (GCP only) | [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install) |
| Terraform >= 1.5 (GCP only) | [developer.hashicorp.com](https://developer.hashicorp.com/terraform/install) |

---

## Local Setup

```bash
git clone <repo-url>
cd St.Infra.v1.0

cp .env.example .env
# AUTH_COOKIE_KEY is the only value you should set:
python -c "import secrets; print(secrets.token_hex(32))"
# Paste the output into .env as AUTH_COOKIE_KEY

make setup    # uv sync --dev + pre-commit install
make up       # docker compose up -d
make migrate  # alembic upgrade head (runs inside container)
make seed     # seed dev credentials
```

Open http://localhost:8501 — log in with `test@local.dev` / `dev1234`.

### Hot Reload

The app container bind-mounts `./app/` — any file save triggers an instant Streamlit
reload. No rebuild needed during development.

### Running tests without Docker

Tests require a live Postgres. Start the Postgres container only:

```bash
docker compose up -d postgres
make test
```

Or run against a fully local Postgres (update `DATABASE_URL` in `.env` to point to it).

---

## Claude Code MCP Servers

The `.claude/settings.json` configures two MCP servers that activate in Claude Code sessions:

**postgres** — gives Claude direct SQL query access to your dev database:
```json
"postgres": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
}
```
Requires Node.js / npx. The `DATABASE_URL` env var is read from your shell environment
(set it in `.env` and `source .env`, or use `direnv`).

**filesystem** — scoped file access to the project root, reducing permission prompts:
```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
}
```

Update the filesystem path in `.claude/settings.json` if your local path differs.

The **Stop hook** auto-runs `ruff format` and `ruff check --fix` at the end of every
Claude session, keeping diffs clean automatically.

---

## First-Time GCP Setup

### 1. Create a GCP project

```bash
gcloud projects create YOUR_PROJECT_ID --name="Streamlit App"
gcloud config set project YOUR_PROJECT_ID
```

Enable billing on the project at https://console.cloud.google.com/billing.

### 2. Authenticate

```bash
gcloud auth login
gcloud auth application-default login   # used by Terraform
```

### 3. Configure Terraform

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Edit `terraform/terraform.tfvars`:
```hcl
project_id      = "YOUR_PROJECT_ID"
region          = "us-central1"
environment     = "dev"
db_password     = "a-strong-password"
auth_cookie_key = "paste-your-32-byte-hex-here"
image_tag       = "latest"
```

> `terraform.tfvars` is gitignored — never commit it.

### 4. Provision infrastructure

```bash
make tf-init    # download providers
make tf-plan    # review what will be created (first run ~15 resources)
make tf-apply   # provision (takes ~5–10 minutes for Cloud SQL)
```

Expected outputs:
```
service_url               = "https://streamlit-app-xxxx-uc.a.run.app"
cloud_sql_connection_name = "project:region:instance"
uploads_bucket            = "project-dev-uploads"
artifact_registry_repo    = "us-central1-docker.pkg.dev/project/streamlit-app"
```

### 5. Build and deploy

```bash
# Authenticate Docker to push to Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

make deploy IMAGE_TAG=v1
```

### 6. Run production migrations

After first deploy, run Alembic against Cloud SQL using Cloud SQL Auth Proxy:

```bash
# Install proxy
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.12.0/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy

# Start proxy in background
./cloud-sql-proxy YOUR_CONNECTION_NAME --port 5433 &

# Run migrations
DATABASE_URL="postgresql+psycopg2://appuser:PASSWORD@localhost:5433/streamlit_app" \
  uv run alembic upgrade head
```

---

## Environment Promotion

| Env | How to deploy |
|---|---|
| `local` | `make up` + Docker Compose |
| `dev` | `make deploy IMAGE_TAG=dev-sha` + `environment = "dev"` in tfvars |
| `staging` | Separate tfvars file with `environment = "staging"`, larger DB tier |
| `production` | `db_tier = "db-g1-small"`, `deletion_protection = true`, `min_instances = 1` |

Use separate Terraform workspaces or state files per environment:
```bash
terraform workspace new staging
terraform workspace select staging
terraform apply -var-file=staging.tfvars
```

---

## Troubleshooting

**`make migrate` fails with "could not translate host name postgres"**
→ The app container isn't running. Run `make up` first.

**`streamlit-authenticator` login loop**
→ `AUTH_COOKIE_KEY` in `.env` is too short or missing. It must be a 32-byte hex string.

**Terraform: "API not enabled"**
→ `google_project_service` resources in `main.tf` enable APIs automatically, but may take
30–60s to propagate. Re-run `make tf-apply`.

**Cloud Run: 500 on startup**
→ Check logs: `gcloud run services logs read streamlit-app --region us-central1`
→ Most common cause: `DATABASE_URL` env var not set correctly or Cloud SQL proxy not attached.
