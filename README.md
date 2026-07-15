# Sonar Lite

A simplified AI-powered health platform, built as a simulation of working inside an AI-native HealthTech startup (Sonar Health) with Claude Code as an AI pair-programmer.

**Status:** Sprint 4 complete — full backend (CRUD, Dashboard & Analytics, AI summary) plus a React dashboard frontend are live.

## Architecture

FastAPI backend, layered `router → service → repository → PostgreSQL`, no business logic in routers. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full domain split (metrics / analytics / ai / dashboard) and folder layout.

## Features

- `POST /metrics`, `GET /metrics` (filter + pagination), `GET /metrics/{id}`, `PATCH /metrics/{id}`, `DELETE /metrics/{id}` — CRUD for the 5 tracked health metrics (weight, sleep, heart rate, steps, water). See [docs/BUSINESS_RULES.md](docs/BUSINESS_RULES.md).
- `GET /health`, `GET /health/db` — liveness and DB-connectivity checks.
- `GET /dashboard` — latest reading, 7d/30d averages + trend, and an overall health score per metric, for the demo user. `ai_summary` is always `null` here (see `POST /ai/summary` below).
- `POST /ai/summary` — rule-based recommendations (always returned) plus an on-demand, LLM-generated summary. Uses a mock AI provider by default (no `OPENAI_API_KEY` configured yet); degrades gracefully to `ai_summary: null` with `ai_summary_error` set if generation fails, rather than failing the request.

## How to Run

```bash
docker compose up --build
```

This brings up PostgreSQL and the backend (migrations run automatically on container start). The API is then available at `http://localhost:8000`.

## Running Tests Locally

Tests run against their own `sonar_lite_test` database — completely separate from
the `sonar_lite` database used for local dev/debugging, so running the suite never
reads or clobbers your own dev data.

```bash
docker compose up -d db
cd backend
uv sync
uv run alembic upgrade head                                       # migrates sonar_lite (dev)
DATABASE_URL=postgresql+asyncpg://sonar:sonar@localhost:5432/sonar_lite_test \
  uv run alembic upgrade head                                     # migrates sonar_lite_test
uv run pytest
```

`sonar_lite_test` is created automatically on the `db` container's first startup
(via `docker/init-test-db.sql`) — no manual `CREATE DATABASE` needed for a fresh clone.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The backend must be running separately (`docker compose up -d` from the repo root) — CORS is configured for `http://localhost:5173` specifically.

## Trade-offs

- No real authentication yet — every request uses a single hardcoded demo user id. Fine for a personal MVP, would need real accounts before this could serve more than one user.
- Business-rule thresholds (sleep, heart rate, etc. from [docs/BUSINESS_RULES.md](docs/BUSINESS_RULES.md)) are not yet enforced anywhere — Sprint 1 only validates that values are plausible numbers. Analytics and recommendations land in Sprint 2/3.
- Tests run against a real Postgres instance (not SQLite) to keep UUID/enum behavior realistic, which means a database must be running to run the test suite — slightly more setup than a pure-unit suite, judged worth it for this project's goals.

## What's Next

See [docs/ROADMAP.md](docs/ROADMAP.md) and [docs/TASKS.md](docs/TASKS.md).
