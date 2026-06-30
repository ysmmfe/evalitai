# Contributing to Evalitai

## Branches

- `main` — stable, deployable
- `feat/<description>` — new features
- `fix/<description>` — bug fixes
- `chore/<description>` — tooling, deps, config

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org):

```
feat: add hallucination metric evaluator
fix: correct score aggregation on partial runs
chore: update ruff to 0.5.0
docs: add RAG integration example
```

## Running locally

```bash
make dev      # start full stack
make migrate  # run migrations
make seed     # load demo data
make test     # run tests
make lint     # run all linters
```

## Before committing

Pre-commit hooks run automatically on `git commit`. To run manually:

```bash
uv run pre-commit run --all-files
```

## Code style

- Python: formatted by ruff, types checked by mypy (strict)
- TypeScript: eslint + tsc
- No comments explaining what the code does — only why, when non-obvious
