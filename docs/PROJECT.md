# Sonar Lite — Project Definition

## What it is

Sonar Lite is a simplified AI-powered health platform. It collects health metrics, computes trends and a health score, and generates AI-assisted recommendations.

It is **not** a medical device and **not** a diagnostic tool. Every AI-generated response must state that its recommendations are informational only, not medical advice.

## User

Single demo user for MVP (Sprints 1-5). No real registration flow — a fake or hardcoded auth is acceptable. Real authentication is deferred to Sprint 6 — see [ROADMAP.md](ROADMAP.md).

## Core value loop

1. User records a metric (weight, sleep, heart rate, steps, water).
2. Backend computes trends and a health score from recorded history.
3. User sees rule-based recommendations immediately, and can request an AI-generated summary on demand.

## Priorities (in order)

1. Working product
2. Good UX
3. Clean architecture
4. Testing
5. Performance

Avoid overengineering. Prefer shipping a complete MVP over a perfect one.
