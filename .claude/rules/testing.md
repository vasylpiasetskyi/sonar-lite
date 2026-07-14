# Rule: Testing

- Unit test services; API test routers.
- Always mock the AI layer in tests — never call a real LLM in CI.
- Cover the boundary values of every threshold in `BUSINESS_RULES.md` (e.g. sleep at exactly 6h and 9h, heart rate at exactly 45 and 100).
