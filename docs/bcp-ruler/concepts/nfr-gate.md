---
type: Concept
title: NFR Gate
description: >
  The bottom rung of each NFR Sizer's rubric — a requirement judged a standard
  expectation scores N/A (0 points) with a one-line rationale.
tags: [core, nfr]
timestamp: 2026-07-03T00:00:00Z
---

# NFR Gate

The NFR Gate is the bottom rung of each NFR [Sizer's](/concepts/sizer.md)
decision table. It applies to Dimensions
[11](/dimensions/quality-attributes.md), [12](/dimensions/security-compliance.md),
and [13](/dimensions/ux-accessibility.md).

## How It Works

1. The [Element Router](/concepts/element-router.md) routes **every** distinct
   NFR requirement to its dimension — routing is never gated
2. The Sizer evaluates each routed element against the decision table
3. A requirement judged a "standard expectation" hits the NFR Gate:
   - Size: N/A
   - Points: 0
   - Rationale: one line explaining why it's standard
4. Gated requirements stay visible in output for CV tuning

## Standard Expectations

What counts as "standard" is domain-dependent. Examples:

| NFR Dimension | Standard Expectation |
|--------------|---------------------|
| Quality Attributes | "System is available during business hours" |
| Security & Compliance | "Use HTTPS," "hash passwords" |
| UX & Accessibility | "Form is usable," "buttons have labels" |

## Design Rationale

Gating is a **sizing judgment**, never a routing one. The Router does not
decide what's standard — each Sizer does, via its decision table. This keeps
the Router's job simple (extract + classify) and makes gating decisions
auditable per-element.

## Relationships

- Applied by NFR [Sizers](/concepts/sizer.md) during scoring
- Standard expectations may be informed by a domain knowledge OKF bundle
  (future: [Domain Knowledge Input](/dimensions/))
- Gated elements remain in [Dimension Scores](/concepts/dimension-module.md)
  for CV measurement
