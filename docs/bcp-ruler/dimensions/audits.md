---
type: Dimension
title: Audits
description: >
  Counts audit-trail requirements — entities whose state changes must be
  logged, tracked, or made traceable.
tags: [functional, planned]
timestamp: 2026-07-03T00:00:00Z
---

# Audits (Dimension 10)

Every entity requiring an audit trail adds complexity at XS(1) per entity.
Audit requirements include change logging, user-action tracking, data-lineage
recording, and compliance-mandated traceability.

## Identity Rule

**One element per distinct entity requiring audit.** "Audit all changes to
Order and Refund" = 2 elements. An entity that needs auditing in multiple
contexts within the same story counts once.

## Decision Table

| Audited entities | Size | Points |
|-----------------|------|--------|
| 0               | N/A  | 0      |
| 1               | XS   | 1      |
| 2               | XS   | 2      |
| 3               | XS   | 3      |
| 4+              | S    | 2 per entity |

Scoring: XS(1) each for up to 3 entities; S(2) each beyond that.

## Examples

**Story:** "Log all refund state changes. Track who approved each refund. Log
loyalty-point adjustments."

- Element 1: Refund entity audit → XS → 1
- Element 2: loyalty-point audit → XS → 1
- Who-approved is part of Refund audit (not a separate entity)
- Count: 2 → Total 2 points

## Relationships

- Audit-logging conditions route here, not to [Business
  Rules](/dimensions/business-rules.md) (specificity precedence)
- The entities being audited score in [Domain
  Entities](/dimensions/domain-entities.md) or [New Domain
  Entities](/dimensions/new-domain-entities.md)
