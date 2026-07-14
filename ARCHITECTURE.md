# Sonar Lite — Architecture

## Target model

Layered monolith with a logical domain split. One FastAPI application, one deployable unit — but the service layer is organized into clearly bounded domains rather than one generic `services/` bag.

```
Frontend
  ↓
REST API (routers — thin, no business logic)
  ↓
Domain Services
  ├── metrics      — record/query raw health metrics (CRUD)
  ├── analytics    — 7d/30d aggregates, trends, health score
  ├── ai           — prompt construction, LLM calls, structured-output validation
  └── dashboard    — composes metrics + analytics + ai for the frontend's single dashboard call
  ↓
Repository Layer (one repository per entity, no business logic)
  ↓
PostgreSQL
```

## Rules

- Business logic never lives in routers — routers only validate input shape, call a service, and return a response model.
- The `ai` domain is isolated: no direct LLM SDK calls from any other domain or from routers.
- `dashboard` is a composition layer only — it aggregates other domains' outputs, it does not own its own business rules.
- Dependency direction is one-way: routers → services → repositories → DB. Services may call other services (e.g. `dashboard` calls `metrics`, `analytics`, `ai`). Repositories never call services.

## Folder layout (for when code starts)

```
backend/app/
├── api/
├── services/
│   ├── metrics/
│   ├── analytics/
│   ├── ai/
│   └── dashboard/
├── repositories/
├── models/
├── schemas/
└── core/
```
