---
type: Dimension
title: UX & Accessibility
description: >
  NFR dimension — counts user experience and accessibility requirements
  (usability, localization, WCAG compliance, UX complexity) that exceed
  standard expectations.
tags: [non-functional, planned, nfr]
timestamp: 2026-07-03T00:00:00Z
---

# UX & Accessibility (Dimension 13)

Counts Non-Functional Requirements related to user experience and
accessibility — usability standards, localization/internationalization,
WCAG compliance, assistive-technology support, UX complexity beyond basic
form design — but only when they **exceed standard expectations**.

## Identity Rule

**One element per distinct UX or accessibility requirement.** "WCAG 2.1 AA
compliance AND RTL language support AND screen-reader optimization" = 3
elements. Each NFR is routed regardless; the [NFR
Gate](/concepts/nfr-gate.md) decides at sizing time.

## Decision Table

| UX / Accessibility scope           | Size | Points |
|------------------------------------|------|--------|
| Standard expectation               | N/A  | 0      |
| Modest above standard              | XS   | 1      |
| Significant above standard         | S    | 2      |
| Demanding                           | M    | 3      |
| Highly demanding                    | L    | 5      |
| Extreme / full certification       | XL   | 8      |

**Standard expectation examples:** "The form should be usable," "buttons should
have labels," "the page should be responsive." **Above standard:** "WCAG 2.1
AA compliance," "support for 5 languages with RTL," "screen-reader-optimized
navigation," "keyboard-only operation for all workflows."

## NFR Gate

Same gating semantics as [Quality Attributes](/dimensions/quality-attributes.md):
standard expectations score N/A (0 pts). Basic usability is table stakes;
formal accessibility standards, localization, and specialized UX patterns
score.

## Examples

**Story:** "Refund form must support WCAG 2.1 AA. RTL layout for Arabic
locale. Keyboard-navigable refund workflow."

- Element 1: WCAG 2.1 AA → above standard → S → 2
- Element 2: RTL support → above standard → S → 2
- Element 3: keyboard navigation → above standard → S → 2
- Total: 6 points

## Relationships

- The form UI itself scores in [Interface
  Elements](/dimensions/interface-elements.md) — UX & Accessibility captures
  the NFR layer on top
- Accessibility affecting all interfaces (not just one form) is a single
  element here, not per-interface
