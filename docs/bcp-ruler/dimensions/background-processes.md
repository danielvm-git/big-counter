---
type: Dimension
title: Background Processes
description: >
  Counts asynchronous or scheduled work — jobs, queues, cron tasks, event
  handlers that run outside the request-response cycle.
tags: [functional, planned]
timestamp: 2026-07-03T00:00:00Z
---

# Background Processes (Dimension 8)

Every distinct asynchronous or scheduled job adds complexity. Background
processes introduce concerns around retry logic, idempotency, monitoring, and
failure handling that synchronous code does not.

## Identity Rule

**One element per distinct background process.** A "send email" job and a
"recalculate analytics" job are two elements. A single job type triggered by
multiple events counts once.

## Decision Table

| Background process complexity              | Size | Points |
|--------------------------------------------|------|--------|
| Fire-and-forget (no retry/state)           | M    | 3      |
| With retry or state tracking                | L    | 5      |
| Multi-step workflow / saga / orchestration  | XL   | 8      |

## Examples

**Story:** "After refund is approved, asynchronously update inventory and send
confirmation email. If inventory update fails, retry 3 times."

- Element 1: inventory update job (with retry) → L → 5 points
- Element 2: confirmation email job (fire-and-forget) → M → 3 points
- Count: 2 → Total 8 points

## Relationships

- Background processes often trigger [Notifications](/dimensions/notifications.md)
  — the notification itself scores there
- State-tracking processes may touch [Domain
  Entities](/dimensions/domain-entities.md) — the entity scores there
