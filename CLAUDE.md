# Evalitai — Claude Code Project Context

Evalitai is an **open-source, self-hosted continuous evaluation platform for LLM-based systems**. It works like unit tests + snapshot tests for AI: developers send events (input, output, context) via a simple JSON API, and the platform evaluates them using deterministic metrics and an LLM judge, then reports what improved or regressed between versions.

The central product question is: **"did this change improve or regress behavior?"**

## Project nature

- **Open source** — MIT licensed, community contributions welcome
- **Self-hosted** — users run their own instance via `docker compose up`
- **Bring your own keys** — LLM provider keys (OpenAI, Anthropic, etc.) live in the user's `.env`; Evalitai never holds or proxies provider credentials
- **Single-tenant by design** — one instance = one user or one team; no multi-org complexity
- **Portfolio project** — built to demonstrate AI engineering skills at a senior/staff level: LLM evaluation, async pipelines, product thinking, and full-stack execution

---

## Stack

| Layer | Choice |
|---|---|
| Backend API | Python 3.12 + FastAPI + Pydantic v2 |
| Frontend | Next.js (App Router) + TypeScript + Tailwind + shadcn/ui + Recharts |
| Database | PostgreSQL 16 (JSONB for event payloads) |
| Queue / Cache | Redis + Arq (swappable to Postgres SKIP LOCKED via env flag) |
| LLM abstraction | LiteLLM (unified client for hosted + self-hosted open-source judges) |
| Object storage | S3-compatible (MinIO locally, R2/S3 in production) |
| Auth | Optional single-user password (dashboard) — no multi-tenant auth needed |
| Observability | structlog + Sentry (optional) + Prometheus |
| ORM / Migrations | SQLAlchemy 2.0 async + Alembic |

---

## Monorepo layout

```
apps/
  api/        # FastAPI backend + Arq workers
  web/        # Next.js dashboard
packages/
  sdk-python/ # Future: pip-installable ingestion client
infra/        # Docker Compose, Dockerfiles, deploy config
docs/         # Architecture docs, ADRs
examples/     # curl, chatbot-demo, rag-demo
tests/
  unit/
  integration/
  e2e/        # Playwright
```

---

## Dev commands

```bash
make dev        # Start full stack via Docker Compose
make migrate    # Run alembic upgrade head
make seed       # Load demo data (idempotent)
make test       # Run all tests (unit + integration, mocked judge)
make lint       # ruff + mypy + eslint + tsc
make e2e        # Playwright E2E tests
```

---

## Core concepts (critical to understand before touching data models)

### EvaluationCase vs Event
- **EvaluationCase** — a stable logical test case identified by `case_key` (e.g., `"password-reset-flow"`). It persists across system versions. This is what makes version comparison coherent.
- **Event / EventVersion** — a concrete execution of a case against a specific `system_version`. Immutable after creation.
- Without the case/event split, "compare versions" has no stable identity to anchor the diff.

### Two-layer evaluation model
1. **Deterministic metrics** (`output_format`, `must_include`, latency, prohibited terms) — run first, confidence = 1.0, cheap.
2. **LLM-as-a-judge metrics** (`overall_quality`, `hallucination`, `context_adherence`, etc.) + **custom criteria** (free-text natural language rubrics) — run after, produce `score` + `confidence` + `rationale` + cited `evidence`.

### Score ≠ Confidence
Every `EvaluationResult` has both. Low confidence → goes to human review queue, never counted as a regression.

### Versioned judge
`EvaluatorModelVersion` pins `provider + model + params + prompt_template_hash`. Comparisons are only valid between runs that used the **same** judge version. Changing any of those fields creates a new version automatically.

### ComparisonReport
Diff of `(case_key × metric)` between current run and baseline. Classification:
- **regression**: `delta <= -threshold AND confidence >= floor AND !unstable`
- **improvement**: symmetric
- **stable**: everything else

---

## Key invariants (never break these)

- `EventVersion` is **immutable** after creation — no updates, ever.
- `EvaluationResult` is **immutable** — reprocessing creates a new row, never overwrites.
- User content in judge prompts is always inside **labelled delimited blocks** — never interpolated raw (prompt injection defense).
- LLM provider keys come **only from environment variables** — never stored in the database or logged.

---

## Idempotency

Ingestion is idempotent. Key = `idempotency_key` field (client-supplied) or SHA-256 of `(project_id, case_key, normalized_payload)`. Same key + same payload → `200 deduped: true`. Same key + different payload → `409`.

---

## API conventions

- Base path: `/v1`
- Auth: optional single-user password via `EVALITAI_PASSWORD` env var; if unset, API is open (trusted local network)
- Errors: `{ "error": { "code", "message", "details" } }`
- Ingestion response: `202 Accepted` (async) — never block on evaluation
- Validation errors: `422` with JSON Pointer `details`

---

## Security rules

- Never log LLM provider keys or raw event payloads.
- Validate and reject payloads above the configured size limit (413).
- PII redaction (opt-in per project) runs **before** persistence and before data is sent to the judge.

---

## Testing approach

- **Unit tests**: schema validation, deterministic evaluators, judge output parsing (mocked), criteria resolution, classification rule.
- **Integration tests**: full pipeline with ephemeral Postgres + Redis + mocked judge.
- **E2E tests** (Playwright): happy path — ingest v1 → baseline → ingest v2 → view comparison with at least one highlighted regression.
- Minimum 80% line coverage on `apps/api` core. Regression classification rule: 100% branch coverage.

---

## Agent usage for this project

| Task | Agent |
|---|---|
| New feature planning | `ecc:planner` |
| After writing/modifying Python | `ecc:python-reviewer` |
| After writing/modifying TypeScript/React | `ecc:react-reviewer` or `ecc:typescript-reviewer` |
| Database schema or query changes | `ecc:database-reviewer` |
| Auth, ingestion, or judge dispatch code | `ecc:security-reviewer` |
| Build or type errors | `ecc:build-error-resolver` |
| React build failures | `ecc:react-build-resolver` |
| Dead code / cleanup | `ecc:refactor-cleaner` |

---

## GitHub issues

All issues tracked at https://github.com/ysmmfe/evalitai/issues

**Revised critical path** (single-tenant, self-hosted):
#01 → #02 → #03 → #04 → #05 → #06 → #07 → #11 → #12 → #13 → #14 → #15 → #16 → #20 → #21 → #23 → #24 → #25 → #26 → #27 → #28 → #29 → #30 → #31 → #32 → #33 → #34 → #35 → #37 → #39 → #40 → #41 → #42

**Dropped from MVP** (single-tenant makes these irrelevant): #08 auth complexity, #09 tenancy scoping, #10 hashed API keys, #48 isolation tests, #49 audit log, #46 rate limiting.

**Simplified**: auth is a single `EVALITAI_PASSWORD` env var checked by middleware — replaces #08 and #10 entirely.

Parallelizable: #07 (seed), #18/#19 (after #16), #45 (after #03), #52 (after #16).

Phase 2: #43, #44, #47, #50, #51, #17 (batch).
