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

```bash
git clone https://github.com/ysmmfe/evalitai.git
cd evalitai
cp .env.example .env   # add your LLM provider key
docker compose up
```

Open `http://localhost:3000`.

## Stack

- **Backend** — Python 3.12, FastAPI, SQLAlchemy, Arq
- **Frontend** — Next.js, TypeScript, Tailwind, shadcn/ui
- **Database** — PostgreSQL
- **Queue** — Redis
- **LLM judge** — any provider via LiteLLM (OpenAI, Anthropic, local models)

## Status

Under active development. Not production-ready.

See [open issues](https://github.com/ysmmfe/evalitai/issues) for the current roadmap.
