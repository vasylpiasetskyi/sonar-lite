# Rule: Database

- UUID primary keys on every table.
- Every table has `created_at` and `updated_at`.
- Add explicit indexes on frequently-queried columns (e.g. `user_id` + `recorded_at` for time-series lookups).
- Use foreign key constraints — don't enforce relational integrity only in application code.
- All schema changes go through Alembic migrations. Never hand-edit the database.
