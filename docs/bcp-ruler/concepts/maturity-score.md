---
type: Concept
title: Maturity Score
description: >
  Confidence indicator accompanying every BCP total — derived from story
  specificity, domain clarity, and requirement precision.
tags: [core, quality]
timestamp: 2026-07-03T00:00:00Z
---

# Maturity Score

Every BCP result carries a Maturity Score (1–5) that indicates how much
confidence to place in the complexity estimate. It is derived from story
quality factors — not from the counter's performance.

## Scale

| Score | Verdict | Meaning |
|-------|---------|---------|
| 5     | reliable | High-specificity story with clear domain context |
| 4     | reliable | Well-specified story, minor ambiguities |
| 3     | moderate | Adequately specified; some interpretation needed |
| 2     | low      | Vague story; significant assumptions required |
| 1     | low      | Barely specified; estimate is directional only |

## Confidence Verdict

The verdict gates how stability targets apply:

- **`reliable`** (maturity > 3) — targets CV < 20% intrinsic, < 25%
  maturity-dependent
- **`moderate`** (maturity = 3) — acceptable variance, no CV target applied
- **`low`** (maturity < 3) — surfaced as a warning; expected noisy; reported
  separately from reliable stories; never tuned against

## Design

- Any element in the `unclassified` bucket caps the verdict at `moderate`
  (regardless of maturity score)
- The counter always returns a BCP total — blocking low-maturity stories is
  team governance, never the counter's job
- Stability targets apply only to `reliable` stories

## Relationships

- Included in every [BCP Result](/dimensions/)
- Affects which stories are included in stability (CV) measurements
- Unclassified elements degrade the verdict regardless of maturity
