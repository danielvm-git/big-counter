# BCP Plus Counter

Calculates Business Complexity Points for a user story by extracting countable elements once, routing each to exactly one of 13 dimensions, and sizing them per dimension.

## Ruler evolution mandate

The BCP Plus whitepaper is authored by this project's owner: dimensions, categories, and sizes MAY be redefined when it improves precision and repeatability. Three constraints are hard: (1) the original BCP philosophy — universal, tech-decoupled, stable over time, "different people arrive at the same result"; (2) NFR dimensions stay; (3) SNAP compatibility stays. The evolved ruler is documented as a whitepaper evolution in Phase 6.

## Language

**Complexity Element**:
One atomic, countable thing found in a story (a boundary crossing, a business rule, a UI element, a notification, …) that contributes points to exactly one Dimension. Elements are semantic, not textual: one sentence may yield elements in different Dimensions (aspect splitting), but each aspect of complexity is counted exactly once.
_Avoid_: item, entry, finding

**Aspect Splitting**:
The Router may split one sentence into multiple Complexity Elements when it carries distinct aspects ("Only admins can approve refunds over $1,000" → an authorization element in Roles/Permissions + a threshold-condition element in Business Rules). Over-splitting is the failure mode to guard in golden fixtures.

**Solution Variability** (dim 4):
One axis of alternative solution paths (e.g., payment-method selection). Identity rule: one element per distinct variability axis, not per branch. Conditions whose sole job is selecting which path executes are priced inside the Variability; conditions that validate or transform within a path are Business Rules (selection-vs-transformation boundary).
_Avoid_: counting each branch as its own element

**SNAP Compatibility**:
The whitepaper's Exhibit 5 maps all 14 SNAP subcategories onto combinations of BCP Plus dimensions (many-to-many). Element identity stays BCP-dimension-based; SNAP reconciliation happens through that mapping table, and NFR size criteria use SNAP-style countable inputs (ADR-0006).

**Confidence Verdict**:
Every result carries a verdict derived from the Maturity Score per whitepaper Exhibit 10: `reliable` (maturity > 3), `moderate` (maturity = 3), `low` (maturity < 3, surfaced as a warning). Any element in the `unclassified` bucket caps the verdict at `moderate`. The counter always returns a BCP — blocking low-maturity stories is team governance (whitepaper recommendation 4), never the counter's job. Stability targets (aggregate CV ≈ 10–15%) apply to `reliable` stories; `low` stories are expected noisy and reported separately, not tuned against.
_Avoid_: provisional, countable (earlier working terms)

**Specificity Precedence**:
The Router routes each aspect to the most specific Dimension that claims it (Roles/Permissions, Notifications, Audits, Background Processes, …). **Business Rules is the residual Dimension** — it receives conditional logic only when no specific Dimension owns that aspect.
_Avoid_: letting Business Rules absorb authorization, notification, or audit aspects

**Dimension**:
One of the 13 perspectives of the BCP ruler (3 existing: Boundaries, Interface Elements, Business Rules; 10 planned per PLAN.md).
_Avoid_: category, step, perspective

**Element Router**:
The single upstream pass (new Step 3.5) that takes the story plus Step 3 output and emits canonical Complexity Elements, each tagged with its one owning Dimension.
_Avoid_: classifier, splitter, break-elements (that name stays with Step 3)

**Identity Rule**:
The per-Dimension definition of what makes one Complexity Element distinct (Boundary = one distinct medium; Notification = one distinct notification event; Audit = one entity). Lives in the Router's extraction schema — one line per Dimension — so elements are canonical by construction; there is no separate dedup step anywhere.
_Avoid_: dedup rule, uniqueness check

**Sizer**:
A per-Dimension step that assigns a Size/Score to the Complexity Elements routed to it. Sizers never read raw story text and never merge, split, or drop elements.
_Avoid_: scanner, detector, scorer

**Dimension Module**:
The code shape of one Dimension: prompt file + expected response shape + decision-table scoring, as pure functions (`build_variables`, `validate`, `score`). No LLM I/O — the calculator renders, calls, and hands the parsed response back, so recorded responses replay offline during Phase 5 threshold tuning. (ADR-0007)
_Avoid_: step (that's the pipeline-stage concept), handler

**Dimension Score**:
The itemized output of `score()`: per-element `(element, size, points, rationale)` plus the subtotal — never a bare number. Forced by the invariants: count preservation (5) is only assertable when per-element sizes are visible, and the NFR Gate requires a per-element rationale.
_Avoid_: returning bare ints from sizers

**Size**:
The XS–XXXL label (Fibonacci-weighted) a Sizer assigns to one Complexity Element.

**Domain Entity** (dim 6) / **New Domain Entity** (dim 7):
Mutually exclusive per entity: an entity is either existing-and-touched (dim 6) or new (dim 7), never both. A new entity scores only in dim 7, even if the story also reads/validates/persists it — dim 7's higher floor (M) already prices that in. Router identity rule: one element per entity; a `new` flag decides the dimension.

**Story Type**:
Step 0's whole-story classification (Functional | Non-Functional), used for portfolio analysis only — it never gates or contributes to BCP.
_Avoid_: calling this "NFR detection" — it is unrelated to the NFR Dimensions

**NFR Dimensions**:
Dimensions 11–13 (Quality Attributes, Security & Compliance, UX & Accessibility), which score individual requirements within a story.
_Avoid_: "non-functional detector" (that's Step 0 / Story Type)

**NFR Gate**:
The bottom rung of each NFR Sizer's rubric: a requirement judged a standard expectation gets Size N/A and 0 points, with a one-line rationale. The Router routes every distinct NFR requirement regardless — gating is a sizing judgment, never a routing one, so gated requirements stay visible in output for CV tuning.
_Avoid_: filtering, threshold check

**CV (Coefficient of Variation)**:
Stability metric: stddev/mean of a dimension's subtotal across N repeated runs of the same story. Measures consistency, NOT correctness — a stable double-count has low CV. Measured twice per dimension: CV of subtotal (sizing flap) and CV of element count (routing flap).

**Calibration**:
The complete score-affecting configuration: ruler version + prompt set + decision-table thresholds + pinned model snapshot + sampling params. Identified by an explicit `calibration_id` carried in every result's provenance block; BCP numbers are comparable iff their calibration_id matches. Any score-affecting change bumps it (a re-baseline event). (ADR-0010, ADR-0011)
_Avoid_: version (ambiguous — counter semver ≠ calibration)

**Replay Corpus**:
Raw LLM responses recorded per stability-harness iteration, tagged with model_id. Enables offline re-scoring against new decision-table thresholds (ADR-0007) at zero API cost. Never replayed across models. See specs/stability-harness.md.

## Relationships

- A **Story** is broken by Step 3 into structured sections (unchanged from bcp-agent).
- The **Element Router** produces zero or more **Complexity Elements** from the Story + Step 3 output.
- Each **Complexity Element** belongs to exactly one **Dimension** (single-valued enum field, assigned by the Router only).
- Each **Dimension** has exactly one **Sizer**; a Sizer sizes only the Elements routed to its Dimension.
- Total BCP = sum over Dimensions of that Dimension's subtotal.

## Invariants (HARD GATE)

1. **Exclusive ownership** — every Complexity Element has exactly one Dimension. Enforced structurally (single enum field set in one pass), not by prompt etiquette.
2. **No re-extraction** — Sizers receive only their routed Elements as input; no Sizer prompt receives the raw story. (Step 4's current prompt violates this — it re-reads `{{story}}`; must be fixed. Steps 5–6 already comply.)
3. **Sum integrity** — `total_bcp` equals the sum of all dimension subtotals in `breakdown`; no element's points appear in two subtotals. A total missing any dimension is never emitted: validation failure retries once, then the run returns an error result naming the failed dimension (ADR-0008).
4. **Coverage over silence** — an Element the Router cannot confidently place goes to an explicit `unclassified` bucket (surfaced in output, scored 0), never silently dropped and never duplicated into two dimensions.
5. **Count preservation** — a Sizer sizes exactly the Elements routed to it: output count equals input count. Canonicalization is the Router's job (via Identity Rules), so any count mismatch downstream is a defect, assertable in golden-fixture tests.
6. **Criteria-defined sizes** — every Size in every Dimension is defined by enumerable, countable criteria (a decision table), never adjectives or holistic "extent" judgment. Sizing is classification of counted facts. (ADR-0006)

## Legal state transitions

Story → step3-broken → routed → sized (per dimension) → totaled.
An Element's `dimension` field is written once by the Router and is immutable afterward — no Sizer may reassign or re-derive it.

## Example dialogue

> **Dev:** "The Test Plan mentions the user gets an email — Interface or Notifications?"
> **Domain expert:** "The **Element Router** decides, once. If it routes it to Notifications, the Interface **Sizer** never sees it — it can't count what it wasn't given."

## Flagged ambiguities

- "Non-Functional" was overloaded: Step 0 classifies the *whole story* (Functional/Non-Functional) for analysis; dimensions 11–13 score *individual NFR requirements*. Resolved: **Story Type** vs **NFR Dimensions** — distinct concepts, no data flow between them.
- Dims 6 vs 7 could be read as additive (creation cost + usage cost). Resolved per whitepaper: mutually exclusive per entity (Reading A).

- "Step 3 stays as-is" (PLAN.md Decision #2) was ambiguous between "Step 3's prompt is untouched" and "the extraction architecture is untouched." Resolved: the prompt is untouched; the Router is a new, additive step after it. See ADR-0001.
- Interface Elements today returns bare counts (`Static: N, Dynamic: N`), not itemized elements — it must become itemized to satisfy invariant 3's auditability. The bucketing math (`ceil(n/5)`) is unchanged.
