---
okf_version: "0.1"
type: Methodology
title: BCP Plus — 13-Dimension Business Complexity Counter
description: >
  A methodology for counting Business Complexity Points (BCP) across 13
  independent dimensions, producing repeatable, tech-decoupled complexity
  estimates from user stories. Designed for co-production by humans and AI
  agents.
tags: [bcp, complexity, estimation, methodology, agent-consumable]
timestamp: 2026-07-03T00:00:00Z
---

# BCP Plus

BCP Plus extends the original BCP (Business Complexity Points) methodology from
3 to 13 dimensions, following the principle that **different people should
arrive at the same result** when counting complexity — the estimate must be
universal, tech-decoupled, and stable over time.

## Core Pipeline

1. **Story Input** — A user story (markdown) enters the pipeline.
2. **Step 3: Break Elements** — The story is broken into structured sections
   (actors, data, business rules, etc.).
3. **Element Router (Step 3.5)** — Every atomic [Complexity
   Element](/concepts/complexity-element.md) is extracted and assigned to
   exactly one [Dimension](/dimensions/). One element, one dimension — no
   double-counting.
4. **Sizers** — Each dimension's [Sizer](/concepts/sizer.md) scores only the
   elements routed to it, using criteria-defined decision tables.
5. **Total BCP** — Sum of all dimension subtotals.

## The 13 Dimensions

### Functional (existing — from original BCP)

| # | Dimension | Scoring |
|---|-----------|---------|
| 1 | [Boundaries](/dimensions/boundaries.md) | XS(1) per interaction medium |
| 2 | [Interface Elements](/dimensions/interface-elements.md) | Static N→ceil(N/5), Dynamic N→ceil(N/5) |
| 5 | [Business Rules](/dimensions/business-rules.md) | XS(1) → XL(8) per condition |

### Functional (new in BCP Plus)

| # | Dimension | Scoring |
|---|-----------|---------|
| 3 | [Roles / Permissions](/dimensions/roles-permissions.md) | S(2) → L(5) |
| 4 | [Solution Variabilities](/dimensions/solution-variabilities.md) | S(2) → XL(8) |
| 6 | [Domain Entities](/dimensions/domain-entities.md) | XS(1) → XL(8) |
| 7 | [New Domain Entities](/dimensions/new-domain-entities.md) | M(3) → L(5) |
| 8 | [Background Processes](/dimensions/background-processes.md) | M(3) → XL(8) |
| 9 | [Notifications](/dimensions/notifications.md) | XS(1) per notification |
| 10 | [Audits](/dimensions/audits.md) | XS(1) per entity |

### Non-Functional (new in BCP Plus)

| # | Dimension | Scoring |
|---|-----------|---------|
| 11 | [Quality Attributes](/dimensions/quality-attributes.md) | XS(1) → XL(8) |
| 12 | [Security & Compliance](/dimensions/security-compliance.md) | XS(1) → XL(8) |
| 13 | [UX & Accessibility](/dimensions/ux-accessibility.md) | XS(1) → XL(8) |

## Key Concepts

- [Complexity Element](/concepts/complexity-element.md) — One atomic, countable
  thing found in a story.
- [Element Router](/concepts/element-router.md) — The single upstream pass that
  assigns every element to exactly one dimension.
- [Identity Rule](/concepts/identity-rule.md) — Per-dimension definition of what
  makes one element distinct.
- [Sizer](/concepts/sizer.md) — Per-dimension step that assigns a Size/Score to
  routed elements.
- [Dimension Module](/concepts/dimension-module.md) — The code shape of one
  dimension: prompt + response shape + decision-table scoring.
- [NFR Gate](/concepts/nfr-gate.md) — The bottom rung of each NFR Sizer:
  standard expectations score 0.
- [Maturity Score](/concepts/maturity-score.md) — Confidence indicator
  accompanying every BCP total.

## Hard Invariants

1. **Exclusive ownership** — every Complexity Element has exactly one Dimension.
2. **No re-extraction** — Sizers receive only routed Elements; no raw story access.
3. **Sum integrity** — total_bcp == sum of all dimension subtotals.
4. **Coverage over silence** — unclassifiable elements go to an explicit
   `unclassified` bucket, never dropped.
5. **Count preservation** — a Sizer sizes exactly the Elements routed to it.
6. **Criteria-defined sizes** — every Size is defined by countable criteria, not
   holistic judgment.

## Confidence & Stability

Every result carries a **Confidence Verdict** derived from the Maturity Score:
- `reliable` (maturity > 3) — targets CV < 20% per dimension
- `moderate` (maturity = 3) — acceptable variance
- `low` (maturity < 3) — surfaced as a warning; expected noisy

## SNAP Compatibility

The BCP Plus whitepaper maps all 14 SNAP subcategories onto combinations of BCP
Plus dimensions (many-to-many). NFR dimension sizes use SNAP-style countable
inputs.

## Citations

[1] BCP Plus whitepaper (this project's owner)
[2] [Open Knowledge Format v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
[3] [Original BCP methodology](https://github.com/flow-ciandt/bcp-agent)
