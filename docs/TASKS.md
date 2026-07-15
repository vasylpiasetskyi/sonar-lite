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

- [ ] React app scaffold, dashboard, forms
- [ ] Trend charts

## Sprint 5 — Tests

- [ ] Unit tests for services
- [ ] API tests for routers
- [ ] AI layer mocked in tests

## Sprint 6 — Authentication

- [ ] User registration/login (real accounts, password hashing or OAuth)
- [ ] Session/JWT-based request authentication
- [ ] Replace `DEMO_USER_ID` with the authenticated user's id across services and routers
- [ ] Migration plan for metrics currently recorded under the demo user
