---
type: Dimension
title: Roles / Permissions
description: >
  Counts authorization complexity — distinct roles, permission checks, and
  access-control rules referenced by the story.
tags: [functional, planned]
timestamp: 2026-07-03T00:00:00Z
---

# Roles / Permissions (Dimension 3)

Every distinct authorization concern adds complexity. This includes role-based
access checks, permission gates, and access-control conditions — even when
expressed implicitly ("only admins can…", "restricted to managers").

## Identity Rule

**One element per distinct authorization gate.** "Only admins and managers"
= 2 elements (two roles checked). "Only authenticated users" = 1 element (one
gate). A role checked in multiple places within the same story counts once.

## Decision Table

| Distinct authorization gates | Size | Points |
|------------------------------|------|--------|
| 0                            | N/A  | 0      |
| 1                            | S    | 2      |
| 2                            | M    | 3      |
| 3+                           | L    | 5      |

## Examples

**Story:** "Only admins can approve refunds; managers can view all refunds;
agents can only view their own."

- Element 1: admin approval gate → 1 gate
- Element 2: manager view gate → 1 gate
- Element 3: agent scope restriction → 1 gate
- Count: 3 → Size L → 5 points

## Relationships

- Authorization conditions route here, not to [Business
  Rules](/dimensions/business-rules.md) (specificity precedence)
- Role-based UI visibility: the UI element counts in [Interface
  Elements](/dimensions/interface-elements.md); the permission check counts here
