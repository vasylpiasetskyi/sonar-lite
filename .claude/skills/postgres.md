# Skill Notes: PostgreSQL

- Index columns used in `WHERE`/`ORDER BY`, especially time-series queries filtered by user + date.
- Prefer database constraints over app-only validation for data integrity.
- Use `TIMESTAMPTZ` for all timestamp columns.
