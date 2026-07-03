# 0006 — Every size in every dimension is defined by enumerable criteria, no adjectives

**Status:** accepted (2026-07-02)

Judgment-driven sizing ("moderate logic", "complex decision-making", sized "by extent") is the dominant variance source for both LLM and human counters. The whitepaper evolution makes criteria-defined sizing normative: each size in each dimension is defined by countable facts (number of conditions, nesting depth, branches per axis, distinct data sources), so sizing is classification against a decision table, never holistic judgment. Boundaries already works this way (ownership/validity/durability criteria) and is the repo's most repeatable dimension; Business Rules and Solution Variabilities are rewritten to match; NFR dimensions adopt SNAP sub-category countable inputs as their size definitions, making SNAP compatibility structural rather than reconciled after the fact.

## Consequences

- Phase 5 tuning changes meaning: instead of rewriting prompt prose for high-CV dimensions, tune the decision-table thresholds against real stories.
- A decision table can misprice edge cases holistic judgment would catch — accepted: consistent, calibratable bias beats unrepeatable accuracy for velocity monitoring (bias can be corrected; variance cannot).
- Golden fixtures can assert sizes exactly, since sizing is deterministic given the counted facts.
