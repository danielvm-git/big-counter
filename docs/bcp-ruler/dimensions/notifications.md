---
type: Dimension
title: Notifications
description: >
  Counts distinct notification events — emails, push notifications, SMS, Slack
  messages, in-app alerts triggered by the story.
tags: [functional, planned]
timestamp: 2026-07-03T00:00:00Z
---

# Notifications (Dimension 9)

Every distinct notification event — an outbound message to a user or external
system triggered by story behavior — adds complexity at XS(1) per event.

## Identity Rule

**One element per distinct notification event.** "Send email on approval AND
send email on rejection" = 2 elements (two distinct events, even if same
channel). "Notify via email and SMS for the same event" = 2 elements (two
channels). A notification template with variable content counts once.

## Decision Table

| Notification events | Size | Points |
|---------------------|------|--------|
| 0                   | N/A  | 0      |
| 1                   | XS   | 1      |
| 2                   | XS   | 2      |
| 3                   | XS   | 3      |
| 4+                  | S    | 2 per event |

Scoring: XS(1) each for up to 3 events; S(2) each beyond that.

## Examples

**Story:** "Send email confirmation on refund approval. Send email on refund
rejection with reason. Notify admin via Slack for refunds over $1,000."

- Element 1: approval confirmation email → XS → 1
- Element 2: rejection email → XS → 1
- Element 3: admin Slack notification → XS → 1
- Count: 3 → Total 3 points

## Relationships

- Notification-triggering conditions route here, not to [Business
  Rules](/dimensions/business-rules.md) (specificity precedence)
- The UI that triggers the notification scores in [Interface
  Elements](/dimensions/interface-elements.md)
- Choice of notification channel (variability) scores in [Solution
  Variabilities](/dimensions/solution-variabilities.md)
