# Rule: API

- Follow REST conventions; keep paths stable once published.
- Every endpoint declares a `response_model` — never return a raw dict.
- Use a consistent error response shape across all endpoints.
- Paginate list endpoints.
