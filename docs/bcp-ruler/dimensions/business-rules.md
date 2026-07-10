---
type: Dimension
title: Business Rules
description: >
  The residual dimension for conditional logic — receives validation,
  transformation, and decision rules not claimed by more specific dimensions.
tags: [functional, intrinsic, existing, residual]
timestamp: 2026-07-03T00:00:00Z
---

# Business Rules (Dimension 5)

Business Rules is the **residual dimension** — it receives conditional logic
only when no specific Dimension claims that aspect. Rules that involve
authorization go to [Roles/Permissions](/dimensions/roles-permissions.md);
notification-triggering rules go to [Notifications](/dimensions/notifications.md);
audit-logging rules go to [Audits](/dimensions/audits.md).

## Identity Rule

**One element per distinct conditional logic expression** — a validation rule,
a transformation rule, or a decision rule. Conditions whose sole job is
selecting which [Solution Variability](/dimensions/solution-variabilities.md)
path executes are priced inside the Variability, not here
(selection-vs-transformation boundary).

## Decision Table

| Rule complexity                        | Size | Points |
|----------------------------------------|------|--------|
| Simple validation (required field)     | XS   | 1      |
| Single-condition rule                  | S    | 2      |
| Multi-condition rule (AND/OR)          | M    | 3      |
| Complex rule (nested, dependent)       | L    | 5      |
| Algorithm / state machine              | XL   | 8      |

## Examples

**Story:** "Validate that refund amount ≤ original order total AND order status
is 'delivered'."

- Element 1: amount validation (multi-condition AND) → M → 3 points

**Story:** "Only admins can approve refunds over $1,000."

- The "only admins" aspect routes to [Roles/Permissions](/dimensions/roles-permissions.md)
- The "$1,000 threshold" aspect routes here → S → 2 points

## Relationships

- **Residual** — receives only what no specific dimension claims
- Conditions selecting variability paths belong to
  [Solution Variabilities](/dimensions/solution-variabilities.md), not here
