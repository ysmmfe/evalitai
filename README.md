# EvalitAI

> Self-hosted evaluation platform for LLM-based systems.

EvalitAI answers one question: **did this change improve or regress my AI system's behavior?**

You send events (input, output, context) via a JSON API. EvalitAI evaluates them using deterministic rules and an LLM judge, then shows you what improved, what regressed, and why — compared to a baseline run.

Think of it as unit tests + snapshot tests for AI, with a dashboard.

## How it works

1. Instrument your system to emit events on each LLM call
2. Define evaluation criteria in natural language
3. Run an evaluation against a suite of cases
4. Mark a run as baseline
5. Deploy your change, run again, see the diff

## Getting started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- At least one LLM provider API key (OpenAI, Anthropic, or Gemini)

### Running locally

```bash
git clone https://github.com/ysmmfe/evalitai.git
cd evalitai

# Copy and edit environment variables
cp infra/.env.example .env

# Start all services (Postgres, Redis, MinIO, API, worker, web)
docker compose --env-file .env -f infra/docker-compose.yml up
```

Open `http://localhost:3000`.

### Running migrations

Migrations run automatically when the API container starts. To run them manually:

```bash
make migrate
```

To generate a new migration after changing models:

```bash
docker run --rm \
  --network infra_default \
  -v "$(pwd)/apps/api:/app" \
  -w /app \
  -e DATABASE_URL="postgresql+asyncpg://evalitai:evalitai@postgres:5432/evalitai" \
  python:3.12-slim \
  bash -c "pip install uv -q && uv sync --group dev -q && uv run alembic revision --autogenerate -m 'describe your change'"
```

> **Note:** Run migration commands from inside Docker. Connecting to the Dockerized Postgres directly from Windows via asyncpg has a known compatibility issue with the Windows event loop.

### Dev commands

| Command | Description |
|---|---|
| `make dev` | Start full stack |
| `make stop` | Stop all containers |
| `make migrate` | Run pending migrations |
| `make test` | Run unit + integration tests |
| `make lint` | Run ruff, mypy, eslint, tsc |
| `make e2e` | Run Playwright end-to-end tests |

## Stack

- **Backend** — Python 3.12, FastAPI, SQLAlchemy 2.0 async, Alembic, Arq
- **Frontend** — Next.js, TypeScript, Tailwind, shadcn/ui
- **Database** — PostgreSQL 16
- **Queue** — Redis 7
- **Storage** — MinIO (S3-compatible)
- **LLM judge** — any provider via LiteLLM (OpenAI, Anthropic, local models)

## Status

Under active development. Not production-ready.

See [open issues](https://github.com/ysmmfe/evalitai/issues) for the current roadmap.
