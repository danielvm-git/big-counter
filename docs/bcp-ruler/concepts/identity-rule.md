---
type: Concept
title: Identity Rule
description: >
  Per-Dimension definition of what makes one Complexity Element distinct,
  enforced by the Element Router.
tags: [core, domain-model]
timestamp: 2026-07-03T00:00:00Z
---

# Identity Rule

An Identity Rule is the per-[Dimension](/dimensions/) definition of what
constitutes one distinct [Complexity Element](/concepts/complexity-element.md).
It lives in the [Element Router's](/concepts/element-router.md) extraction
schema — one line per Dimension — so elements are canonical by construction.
There is no separate dedup step anywhere.

## Per-Dimension Identity Rules

| Dimension | Identity Rule |
|-----------|--------------|
| [Boundaries](/dimensions/boundaries.md) | One element per distinct interaction medium |
| [Interface Elements](/dimensions/interface-elements.md) | One element per distinct UI component |
| [Roles/Permissions](/dimensions/roles-permissions.md) | One element per distinct authorization gate |
| [Solution Variabilities](/dimensions/solution-variabilities.md) | One element per distinct variability axis (not per branch) |
| [Business Rules](/dimensions/business-rules.md) | One element per distinct conditional logic expression |
| [Domain Entities](/dimensions/domain-entities.md) | One element per distinct existing entity |
| [New Domain Entities](/dimensions/new-domain-entities.md) | One element per distinct new entity |
| [Background Processes](/dimensions/background-processes.md) | One element per distinct background process |
| [Notifications](/dimensions/notifications.md) | One element per distinct notification event |
| [Audits](/dimensions/audits.md) | One element per distinct audited entity |
| [Quality Attributes](/dimensions/quality-attributes.md) | One element per distinct QA requirement |
| [Security & Compliance](/dimensions/security-compliance.md) | One element per distinct security/compliance requirement |
| [UX & Accessibility](/dimensions/ux-accessibility.md) | One element per distinct UX/accessibility requirement |

## Specificity Precedence

When an aspect could fit multiple Dimensions, the [Element
Router](/concepts/element-router.md) applies specificity precedence: the most
specific Dimension claims it. [Business
Rules](/dimensions/business-rules.md) is the residual — it receives conditional
logic only when no specific Dimension owns that aspect.
