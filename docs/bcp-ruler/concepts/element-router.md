---
type: Concept
title: Element Router
description: >
  The single upstream pass (Step 3.5) that extracts Complexity Elements from
  a story and assigns each to exactly one Dimension.
tags: [core, pipeline]
timestamp: 2026-07-03T00:00:00Z
---

# Element Router

The Element Router is the single upstream pass (Step 3.5 in the BCP pipeline)
that takes the story plus Step 3 output (broken sections) and emits canonical
[Complexity Elements](/concepts/complexity-element.md), each tagged with its
one owning [Dimension](/dimensions/).

## Design

- **Runs once** — before any Sizer
- **Output is canonical** — elements are defined here by construction; there
  is no separate dedup step anywhere
- **Uses [Identity Rules](/concepts/identity-rule.md)** — one line per
  Dimension defining what makes one element distinct
- **Specificity precedence** — routes each aspect to the most specific
  Dimension that claims it
- **[Business Rules](/dimensions/business-rules.md) is the residual
  dimension** — receives conditional logic only when no specific Dimension owns
  that aspect

## Coverage Guarantee

An element the Router cannot confidently place goes to an explicit
`unclassified` bucket (surfaced in output, scored 0), never silently dropped
and never duplicated into two dimensions.

## Relationships

- Consumes Step 3 output (broken sections)
- Produces [Complexity Elements](/concepts/complexity-element.md) for all
  [Sizers](/concepts/sizer.md)
- Governed by [Identity Rules](/concepts/identity-rule.md) per Dimension
