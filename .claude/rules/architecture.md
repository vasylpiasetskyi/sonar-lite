# Rule: Architecture

- Follow `Router → Service → Repository → DB`. Dependency direction is one-way; repositories never call services.
- No business logic in routers — validate input shape, call a service, return a response model.
- Use dependency injection for services and repositories.
- Keep services small and focused on one domain: `metrics`, `analytics`, `ai`, `dashboard`.
- Don't blur domain boundaries — `dashboard` composes the others, it doesn't own business rules.
