# Rule: Backend

- FastAPI, async by default.
- Pydantic v2 schemas are separate from SQLAlchemy ORM models — never return an ORM model directly.
- SQLAlchemy 2.x style, migrations via Alembic only.
- Use correct HTTP status codes (201 on create, 404 on missing, 422 on validation error, etc.).
- Validate all input/output at the API boundary via Pydantic models.
- Use structured logging — no bare `print()`.
