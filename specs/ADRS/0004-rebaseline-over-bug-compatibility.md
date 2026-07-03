# 0004 — Re-baseline scores instead of preserving bug-compatible totals

**Status:** accepted (2026-07-02)

Fixing the Test-Plan double-feed (the same story section fed to both UI Elements and Business Rules sizers) changes real-story scores for the 3 original dimensions. We decided correctness wins over historical comparability: scoring *rules* (XS=1/S=2/M=3/XL=8 weights, ceil(n/5) UI bucketing) stay pinned by updated unit tests, but real-story totals are re-baselined once, after the Element Router lands. PLAN.md success criterion #4 is reworded accordingly, and Phase 1's CV baseline moves to *after* the Router — measuring a 25-iteration baseline on a pipeline already known to double-count would spend API budget on numbers we've decided to invalidate.

## Consequences

- Historical BCP numbers from the pre-Router counter are not comparable to BCP Plus numbers; any consumer of past scores must be told once.
- Expected direction of shift: slightly down (Test Plan content stops being counted twice); the Phase 1 baseline report must explain observed shifts against this expectation.
- Unit tests keep exact-total assertions but against updated FakePromptHandler fixtures reflecting the routed pipeline.
