# System Design Coach

Generated: 2026-10-28T20:07:54+00:00 UTC

> Free deterministic coaching mode. No OpenAI API key is needed. Tasks and examples are prepared from a built-in curriculum; progress is only personalized when private Gist sync is configured.

## Interview exercise: Design a news feed

**Requirements:** Serve personalized feeds with fresh posts and predictable latency.

## 45-minute interview structure

1. **5 min — Clarify:** functional and non-functional requirements, scope, traffic, latency and availability targets.
2. **5 min — Estimate:** requests/second, storage growth, bandwidth and hot-key risks. State assumptions.
3. **8 min — API and data model:** define core endpoints, identifiers, indexes, partition keys and consistency needs.
4. **12 min — Architecture:** draw clients, load balancer, services, database, cache, queue and dependencies.
5. **10 min — Deep dive:** choose one bottleneck and describe failure handling, scaling and operational visibility.
6. **5 min — Trade-offs:** state what you chose, alternatives, and why.

## Starting design

Create post, follow, read feed; post store, graph, fan-out, cache, ranking.

## Risks you must discuss

Compare fan-out-on-write/read, celebrity accounts, freshness, pagination and cache invalidation.

## Self-score (0–4 each)

- Requirements and assumptions: __ / 4
- API and data model: __ / 4
- Architecture and scale: __ / 4
- Reliability, security and observability: __ / 4
- Trade-offs and communication: __ / 4

**Readiness target:** 16/20 or higher on two different designs, with no category below 2. Record the score and the one weakest category in your dashboard.
