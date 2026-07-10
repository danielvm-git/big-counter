---
type: Concept
title: Complexity Element
description: >
  One atomic, countable thing found in a story that contributes points to
  exactly one Dimension.
tags: [core, domain-model]
timestamp: 2026-07-03T00:00:00Z
---

# Complexity Element

A Complexity Element is one atomic, countable unit of complexity extracted from
a user story. Elements are semantic, not textual — one sentence may yield
elements in different [Dimensions](/dimensions/) ([Aspect
Splitting](#aspect-splitting)), but each aspect of complexity is counted
exactly once.

## Properties

- **Owned by exactly one Dimension** — enforced structurally (single enum
  field), not by prompt etiquette
- **Extracted once** by the [Element Router](/concepts/element-router.md)
- **Sized once** by the owning dimension's [Sizer](/concepts/sizer.md)
- **Immutable dimension assignment** — no Sizer may reassign

## Aspect Splitting

The Router may split one sentence into multiple Complexity Elements when it
carries distinct aspects:

> "Only admins can approve refunds over $1,000"

→ Element A: authorization gate → [Roles/Permissions](/dimensions/roles-permissions.md)
→ Element B: threshold condition → [Business Rules](/dimensions/business-rules.md)

Over-splitting is the failure mode to guard in golden fixtures.

## Relationships

- Routed to exactly one [Dimension](/dimensions/) by the [Element
  Router](/concepts/element-router.md)
- Sized by exactly one [Sizer](/concepts/sizer.md)
- Never dropped — unclassifiable elements go to an explicit `unclassified`
  bucket (scored 0)
