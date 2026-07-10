---
type: Dimension
title: New Domain Entities
description: >
  Counts domain entities created by the story. Mutually exclusive with Domain
  Entities per entity — a new entity scores only here, never in both.
tags: [functional, planned]
timestamp: 2026-07-03T00:00:00Z
---

# New Domain Entities (Dimension 7)

Every new domain entity the story introduces adds complexity. Creating an
entity is inherently more complex than touching an existing one — it requires
defining structure, validation, persistence, and lifecycle.

## Identity Rule

**One element per distinct new entity.** An entity is "new" if this story
introduces it to the domain model. Even if the story also reads/validates/
persists the new entity, it scores only here — dim 7's higher floor (M)
already prices in the full creation cost.

## Decision Table

| New entities created | Size | Points |
|---------------------|------|--------|
| 0                   | N/A  | 0      |
| 1                   | M    | 3      |
| 2                   | L    | 5      |
| 3+                  | XL   | 8      |

Note the higher floor: even a single new entity starts at M(3), reflecting the
inherent cost of introducing structure, validation, and lifecycle.

## Examples

**Story:** "Add refund processing that updates the Order status, creates a
Refund record, and adjusts Customer loyalty points."

- Refund: new entity → dim 7 → M → 3 points
- Order, Customer: existing → dim 6 (not here)

## Relationships

- Mutually exclusive with [Domain Entities](/dimensions/domain-entities.md)
  per entity — an entity is either existing or new, never both
- New entities often require new [Interface
  Elements](/dimensions/interface-elements.md) and [Business
  Rules](/dimensions/business-rules.md) — those are separate elements
