---
type: Concept
title: Dimension Module
description: >
  The code shape of one Dimension — prompt file + expected response shape +
  decision-table scoring — as pure functions with no LLM I/O.
tags: [core, architecture]
timestamp: 2026-07-03T00:00:00Z
---

# Dimension Module

A Dimension Module is the code shape of one [Dimension](/dimensions/)
implemented as three pure functions:

1. **`build_variables()`** — prepares the Jinja2 template variables from
   routed elements (and optionally domain knowledge)
2. **`validate()`** — parses and validates the LLM's structured response
3. **`score()`** — applies the decision table to produce a [Dimension Score](#dimension-score)

## Design

- **No LLM I/O** — the module never calls an LLM. The calculator renders the
  prompt, calls the provider, feeds the response to `validate()`, then passes
  the parsed result to `score()`. This separation enables offline replay: raw
  responses recorded by the stability harness can be re-scored against new
  decision-table thresholds at zero API cost.
- **Pure functions** — deterministic given the same inputs
- **ADR-0007** — the Architecture Decision Record that established this pattern

## Dimension Score

The output of `score()` is an itemized list of per-element
`(element, size, points, rationale)` plus the subtotal — never a bare number.
This is forced by two invariants:

- **Count preservation** (invariant #5) is only assertable when per-element
  sizes are visible
- **NFR Gate** requires a per-element rationale for gated (N/A) requirements

## Relationships

- Implements one [Dimension](/dimensions/)
- Used by the [Sizer](/concepts/sizer.md) pipeline step
- Recorded responses feed the stability harness replay corpus
