# Sonar Lite — Tasks

## Sprint 0 — Docs & `.claude` config

- [x] PROJECT.md
- [x] BUSINESS_RULES.md
- [x] ARCHITECTURE.md
- [x] ROADMAP.md
- [x] TASKS.md
- [x] .claude/CLAUDE.md
- [x] .claude/INTERVIEW_MODE.md
- [x] .claude/rules/*.md
- [x] .claude/skills/*.md

## Sprint 1 — Health Metrics CRUD

- [x] Backend project scaffold (FastAPI, SQLAlchemy, Alembic, Postgres via docker compose)
- [x] Metrics domain: models, schemas, repository, service, router

## Sprint 2 — Dashboard & Analytics

- [x] 7d/30d aggregates and trend calculation
- [x] Health score calculation
- [x] Dashboard composition endpoint

## Sprint 3 — AI

- [x] Rule-based recommendation engine
- [x] AI prompt layer + structured AI summary endpoint

## Sprint 4 — Charts & frontend

- [x] React app scaffold, dashboard, forms
- [x] Trend charts

## Sprint 5 — Tests

- [x] Unit tests for services — done incrementally via TDD since Sprint 1, not deferred to this sprint.
- [x] API tests for routers — same, done incrementally since Sprint 1.
- [x] AI layer mocked in tests — `MockAIProvider` used throughout; `OpenAIProvider`'s own test mocks the SDK client, no real network call anywhere in the suite.
- [x] Edge-case sweep — closed the specific gaps flagged as Minor in Sprints 2-3 code review (PATCH validation boundary, migration column types/enum values, LLM-supplied-disclaimer-is-ignored regression guard, trend dead-band boundary). Backend suite: 88 tests.

## Sprint 6 — Authentication

- [x] User registration/login (email + password, bcrypt-hashed)
- [x] JWT bearer-token request authentication
- [x] Replace `DEMO_USER_ID` with the authenticated user's id across services and routers — the constant and its module no longer exist
- [x] Old demo data deleted (confirmed disposable) rather than migrated — a fresh account replaces it
