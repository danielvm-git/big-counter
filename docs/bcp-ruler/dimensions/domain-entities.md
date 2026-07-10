---
type: Dimension
title: Domain Entities
description: >
  Counts existing domain entities touched (read, validated, updated) by the
  story. Mutually exclusive with New Domain Entities per entity.
tags: [functional, planned]
timestamp: 2026-07-03T00:00:00Z
---

# Domain Entities (Dimension 6)

Every existing domain entity the story interacts with adds complexity. An
entity is a business concept with identity and lifecycle — Order, Customer,
Invoice, Product — not a database table (though it often maps to one).

## Identity Rule

**One element per distinct existing entity.** An entity is existing if it
already exists in the domain model before this story. If the story creates a
new entity, that entity scores in [New Domain
Entities](/dimensions/new-domain-entities.md), not here — dims 6 and 7 are
**mutually exclusive per entity**.

## Decision Table

| Existing entities touched | Size | Points |
|--------------------------|------|--------|
| 0                        | N/A  | 0      |
| 1                        | XS   | 1      |
| 2                        | S    | 2      |
| 3                        | M    | 3      |
| 4                        | L    | 5      |
| 5+                       | XL   | 8      |

## Examples

**Story:** "Add refund processing that updates the Order status, creates a
Refund record, and adjusts Customer loyalty points."

- Order: existing entity → dim 6
- Customer: existing entity → dim 6
- Refund: new entity → dim 7 (not here)
- Count (dim 6): 2 → Size S → 2 points

## Relationships

- Mutually exclusive with [New Domain Entities](/dimensions/new-domain-entities.md)
  per entity — a new entity scores only in dim 7
- Entities may be the subject of [Audits](/dimensions/audits.md) — the audit is
  a separate element scored in that dimension
