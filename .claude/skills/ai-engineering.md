# Skill Notes: AI Engineering

- Version prompt templates in code, not inline strings scattered across services.
- Always request structured (JSON) output from the LLM.
- Use a low temperature for deterministic health-summary generation.
- Retry once on invalid output, then fail gracefully — don't loop indefinitely.
- Log prompt/response pairs for observability; avoid logging PII where possible.
