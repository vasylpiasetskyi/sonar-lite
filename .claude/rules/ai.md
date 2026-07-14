# Rule: AI

- All LLM calls go through the `ai` domain service only — no other domain or router calls an LLM SDK directly.
- Use structured prompts and always request JSON output.
- Validate the AI response against an expected schema. On invalid/malformed output, retry once; if it still fails, fail gracefully with a clear error — never fabricate a fallback response.
- Store prompt templates separately from the code that calls them.
- Every AI-facing response must state: recommendations are informational only, not medical advice.
