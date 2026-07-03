# 0009 — PromptHandler parses or raises; the raw_response sentinel is eliminated

**Status:** accepted (2026-07-02)

PromptHandler currently returns `{"raw_response": <text>}` when LLM output fails to parse, and three modules (PromptHandler, BCPCalculator, CLI formatters) share knowledge of that magic key. With ADR-0008 the calculator must *distinguish* parse failure to trigger retry, so the contract becomes explicit: `process_prompt` returns parsed JSON or raises a typed `ResponseParseError` carrying the raw text. Callers stop sniffing dict keys; raw text travels only inside error objects.

Failure handling by stage kind:
- **Required dimension** — catch → retry once → error result naming the dimension (ADR-0008).
- **Non-required stage** (Story Type, Maturity, INVEST) — annotate-and-continue: store an explicit per-stage error in the result, never retry (not worth the API call). A failed Maturity stage forces the Confidence Verdict to `low` — a verdict computed without a maturity score is not `reliable` by definition.

## Consequences

- "Resilient-looking" fallback behavior disappears from PromptHandler — resilience policy is the calculator's job, where stage kind is known.
- CLI/API formatters lose their `raw_response` branches; error rendering reads structured error objects instead.
