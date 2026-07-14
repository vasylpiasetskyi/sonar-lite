# Skill Notes: FastAPI

- Prefer async endpoints.
- Use dependency injection (`Depends`) for repositories and services — don't instantiate them inline in a route.
- Keep Pydantic schemas separate from ORM models.
- Always set `response_model` on the route decorator.
- Keep routers thin — delegate to a service call immediately.
