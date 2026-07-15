# Sonar Lite — Roadmap

- **Sprint 0 (current):** Docs & `.claude` config — no code.
- **Sprint 1:** Health Metrics CRUD (metrics domain, repository, DB schema, migrations, basic REST API).
- **Sprint 2:** Dashboard & Analytics (7d/30d aggregates, trends, health score calculation, dashboard composition endpoint).
- **Sprint 3:** AI (prompt layer, structured AI summary, rule-based recommendation engine wired in before AI).
- **Sprint 4:** Charts & frontend polish (React dashboard, trend charts, forms, loading/error states).
- **Sprint 5:** Tests — in practice, unit/API/AI-mocked tests were written incrementally via TDD starting in Sprint 1, not deferred to here. This sprint closed the remaining edge-case gaps flagged in prior code reviews.
- **Sprint 6:** Authentication (real user accounts, replace the hardcoded demo user with per-request identity).
