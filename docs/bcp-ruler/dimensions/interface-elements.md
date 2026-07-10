---
type: Dimension
title: Interface Elements
description: >
  Counts human-facing UI elements — both static (display) and dynamic
  (interactive) — bucketed in groups of 5.
tags: [functional, intrinsic, existing]
timestamp: 2026-07-03T00:00:00Z
---

# Interface Elements (Dimension 2)

Counts human-facing UI components the story requires. Elements are classified
as **Static** (labels, read-only fields, images) or **Dynamic** (inputs,
buttons, dropdowns, modals, date pickers).

## Identity Rule

**One element per distinct UI component.** A form with 3 input fields and 1
button = 4 Dynamic elements. A read-only table = 1 Static element.

## Decision Table

| Static count | Size | Points | Dynamic count | Size | Points |
|-------------|------|--------|--------------|------|--------|
| 0           | N/A  | 0      | 0            | N/A  | 0      |
| 1–5         | XS   | 1      | 1–5          | XS   | 1      |
| 6–10        | S    | 2      | 6–10         | S    | 2      |
| 11–15       | M    | 3      | 11–15        | M    | 3      |
| 16–20       | L    | 5      | 16–20        | L    | 5      |
| 21+         | XL   | 8      | 21+          | XL   | 8      |

Scoring: `ceil(count / 5)` maps count to size bucket. Static and Dynamic are
scored independently, then summed.

## Examples

**Story:** "Add a refund form with order ID lookup, refund amount input, reason
dropdown, and submit button."

- Static: 3 (order details display, confirmation message, help text) → 3 ≤ 5 → XS → 1
- Dynamic: 4 (order ID field, amount field, reason dropdown, submit button) → 4 ≤ 5 → XS → 1
- Total: 2 points

## Relationships

- Distinct from [Boundaries](/dimensions/boundaries.md) (system-facing vs human-facing)
- UI that triggers [Notifications](/dimensions/notifications.md) or
  [Audits](/dimensions/audits.md) — those dimensions score the notification/audit,
  not Interface Elements
