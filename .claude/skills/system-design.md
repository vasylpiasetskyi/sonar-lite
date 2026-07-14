# Skill Notes: System Design

Think about:

- What happens at 10x the data volume.
- What should be cached — analytics aggregates are a natural candidate.
- What fails first under load.
- How a failure in the `ai` domain should degrade gracefully — the dashboard should still render without an AI summary.
