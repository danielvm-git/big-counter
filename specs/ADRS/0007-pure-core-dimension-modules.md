# 0007 — Dimension modules are pure; the calculator owns all LLM I/O

**Status:** accepted (2026-07-02)

Each of the 13 dimensions becomes a module owning its prompt file, expected response shape, and decision-table scoring — but as pure data plus deterministic functions (`build_variables`, `validate`, `score`); only the calculator talks to PromptHandler. The forcing function is Phase 5 tuning: the 25-iteration stability protocol records LLM responses, and ADR-0006 tuning means adjusting decision-table thresholds — with pure `score()`, recorded responses replay against new thresholds offline (zero API cost per experiment). A self-executing `dimension.size(prompt_handler, elements)` shape was rejected: it fuses scoring to the call, so every threshold experiment re-burns API budget, and every scoring test pays fake-provider choreography.

## Consequences

- The calculator keeps a small generic orchestration loop (render → call → validate → score); per-dimension knowledge leaves the loop entirely — adding dimensions 4–13 adds modules, not branches.
- Golden fixtures test `score()` as a table lookup: exact assertions, no fakes.
- Steps 0–2 (Story Type, Maturity, INVEST) and Step 3/Router are pipeline stages, not Dimensions — they stay bespoke; only the 13 dimensions get this module shape (one adapter is a hypothetical seam; the dimensions are thirteen real ones).
