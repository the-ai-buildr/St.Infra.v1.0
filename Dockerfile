# ── base ──────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

# ── dev ───────────────────────────────────────────────────────────────────────
FROM base AS dev

RUN uv sync --frozen --dev
RUN uv run pip install "watchdog[watchmedo]" --quiet

COPY . .

# ── prod ──────────────────────────────────────────────────────────────────────
FROM base AS prod

RUN uv sync --frozen --no-dev

COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

CMD ["uv", "run", "streamlit", "run", "app/main.py", \
     "--server.port", "8501", \
     "--server.address", "0.0.0.0", \
     "--server.runOnSave", "false"]
