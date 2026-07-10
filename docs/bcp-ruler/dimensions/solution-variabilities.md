---
type: Dimension
title: Solution Variabilities
description: >
  Counts alternative solution paths — distinct axes of variability where the
  system must behave differently based on context.
tags: [functional, planned]
timestamp: 2026-07-03T00:00:00Z
---

# Solution Variabilities (Dimension 4)

Each distinct axis of alternative solution behavior adds complexity. A
variability is a dimension of choice — payment method, shipping provider,
notification channel — where the system branches.

## Identity Rule

**One element per distinct variability axis, not per branch.** "Payment by
credit card, PayPal, or bank transfer" = 1 element (payment-method axis), not
3. Conditions whose sole job is selecting which path executes are priced inside
the Variability; conditions that validate or transform within a path are
[Business Rules](/dimensions/business-rules.md) (selection-vs-transformation
boundary).

## Decision Table

| Variability axes | Size | Points |
|-----------------|------|--------|
| 0               | N/A  | 0      |
| 1               | S    | 2      |
| 2               | M    | 3      |
| 3               | L    | 5      |
| 4+              | XL   | 8      |

## Examples

**Story:** "Support refunds via original payment method (credit card, PayPal)
or store credit."

- Element 1: refund-method axis (credit card / PayPal / store credit) → 1 axis → S → 2 points

**Story:** "Notify users via email, SMS, or push based on preference; process
payment via Stripe or Braintree based on region."

- Element 1: notification-channel axis → 1 axis
- Element 2: payment-gateway axis → 1 axis
- Count: 2 → Size M → 3 points

## Relationships

- Path-selection conditions belong here; path-internal validation belongs to
  [Business Rules](/dimensions/business-rules.md)
- Variability in notification channels does NOT double-count with
  [Notifications](/dimensions/notifications.md) — the notification itself scores
  there; the choice-of-channel scores here
