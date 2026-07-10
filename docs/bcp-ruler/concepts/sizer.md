---
type: Concept
title: Sizer
description: >
  A per-Dimension step that assigns a Size/Score to the Complexity Elements
  routed to it using criteria-defined decision tables.
tags: [core, pipeline]
timestamp: 2026-07-03T00:00:00Z
---

# Sizer

A Sizer is a per-[Dimension](/dimensions/) step that receives only the
[Complexity Elements](/concepts/complexity-element.md) routed to its dimension
and assigns a Size (XS–XXXL, Fibonacci-weighted) and Points to each.

## Constraints

- **Never reads raw story text** — invariant #2: no re-extraction
- **Never merges, splits, or drops elements** — invariant #5: count
  preservation (output count == input count)
- **Returns itemized [Dimension
  Scores](/concepts/dimension-module.md#dimension-score)** — per-element
  `(element, size, points, rationale)` plus subtotal, never a bare number
- **Uses criteria-defined decision tables** — invariant #6: every Size is
  defined by countable criteria, not holistic judgment

## NFR Sizers

Dimensions [11–13](/dimensions/) (Quality Attributes, Security & Compliance,
UX & Accessibility) have an additional [NFR Gate](/concepts/nfr-gate.md): a
requirement judged a standard expectation scores N/A (0 pts) with a one-line
rationale. Routing happens regardless; gating is sizing-only.

## Relationships

- Receives elements from the [Element Router](/concepts/element-router.md)
- Implements the [Dimension Module](/concepts/dimension-module.md) pattern
- Gated by [NFR Gate](/concepts/nfr-gate.md) for NFR dimensions
