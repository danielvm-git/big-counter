---
type: Dimension
title: Boundaries
description: >
  Counts distinct interaction boundaries — each external system, service, or
  medium the story crosses.
tags: [functional, intrinsic, existing]
timestamp: 2026-07-03T00:00:00Z
---

# Boundaries (Dimension 1)

Each distinct external system, service, or interaction medium the story
touches adds complexity. A boundary is a crossing point where data or control
flows between systems.

## Identity Rule

**One element per distinct interaction medium.** A REST API call, a message
queue read, a file import, and a database query are each distinct media. Two
calls to the same API count as one element (same medium).

## Decision Table

| Count of distinct boundaries | Size | Points |
|------------------------------|------|--------|
| 0                            | N/A  | 0      |
| 1                            | XS   | 1      |
| 2                            | S    | 2      |
| 3                            | M    | 3      |
| 4                            | L    | 5      |
| 5+                           | XL   | 8      |

## Examples

**Story:** "Fetch order data from the ERP, validate against the CRM, and push
to the warehouse system."

- Element 1: ERP (REST API) — boundary
- Element 2: CRM (REST API) — boundary
- Element 3: Warehouse (message queue) — boundary
- Count: 3 → Size M → 3 points

## Relationships

- Crosses boundaries to interact with [Domain Entities](/dimensions/domain-entities.md)
- Distinct from [Interface Elements](/dimensions/interface-elements.md) (human-facing UI vs system boundaries)
