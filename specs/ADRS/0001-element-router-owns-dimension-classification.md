# 0001 — A single Element Router owns dimension classification

**Status:** accepted (2026-07-02)

Scaling from 3 to 13 dimensions with independent per-dimension extraction passes cannot guarantee an element is counted in exactly one dimension — N independent LLM calls over shared story text have no mechanism to agree on ownership, and the 3-dimension baseline already double-feeds the Test Plan section to both UI Elements and Business Rules. We decided to add one new step (Element Router, Step 3.5) that emits atomic Complexity Elements each tagged with exactly one owning dimension; all sizers (existing 3 and new 10) consume only their routed elements and never re-read the story. Step 3's prompt stays untouched; the only edits to existing code are the calculator's input-plumbing for steps 4–6 and removing `{{story}}` from the step 4 prompt.

## Considered Options

- **Prompt-level exclusion rules in 13 independent scanners** — minimal diff, but exclusivity is hoped-for, not structural; untestable (can't assert two independent LLM calls won't overlap); rejected.
- **Full Step 3 redesign into a typed extraction schema** — strongest structure, but contradicts the minimal-change strategy and breaks the existing 3-dimension tests; rejected as more change than inevitable.
- **Additive Element Router (chosen)** — the smallest change that makes exclusivity a structural property (a single-valued enum field written once) and testable with golden fixtures.

## Consequences

- One extra LLM call per story (+latency/cost); acceptable against a 6→14+ call pipeline.
- The Router becomes the single point of classification error — golden-fixture tests must assert its partition directly.
- Interface Elements sizer must return itemized elements (not bare counts) so subtotals are auditable against routed inputs.
- PLAN.md Decision #2 ("Step 3 stays as-is") is narrowed, not reversed: the prompt is untouched, the architecture around it is extended.
