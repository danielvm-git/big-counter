# 0008 — Validation failure retries once, then fails the run; no partial totals

**Status:** accepted (2026-07-02)

Today a required step whose LLM response fails shape validation is silently skipped with a warning, so `total_bcp` can be an undercount indistinguishable from a valid count — the worst failure mode for velocity monitoring. We decided: on validation failure the calculator re-calls that dimension's prompt once (malformed output is mostly sampling noise); if the retry also fails, the run returns an explicit error result naming the failed dimension and carrying the raw response — never a partial total. A BCP total is defined as the sum over all dimensions (invariant 3); a partial sum is not a smaller BCP, it is not a BCP. The Confidence Verdict is not used for this: `low` means "immature story," a fact about the story — pipeline failures must not poison that signal.

## Consequences

- Retry policy lives once in the calculator's generic loop, not in 13 dimension modules.
- Per-dimension retry rate becomes a measurable prompt-quality signal in Phase 5 (frequent retries = prompt defect).
- The currently-pinned skip behavior in tests/unit/test_bcp_calculator.py (raw_response ⇒ skip, still total) is a deliberate behavior change under ADR-0004's re-baseline stance.
