# Skill Notes: Docker

- One service per container: backend, frontend, db.
- Configure via `.env`, not hardcoded values.
- Add a healthcheck on the db service so the backend waits for it to be ready.
- Use a named volume for Postgres data persistence.
