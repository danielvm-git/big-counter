# 0002 — The Router emits canonical elements; sizers never dedup

**Status:** accepted (2026-07-02)

Intra-dimension deduplication (e.g., Boundaries' "count once per distinct medium") could live in each sizer or in the Element Router. We decided the Router owns it — not as 13 dedup rulebooks, but as one Identity Rule per dimension baked into its extraction schema ("Boundary = one distinct medium crossed", "Notification = one distinct notification event"), so elements are canonical by construction. Sizers are pure: they size exactly what they receive, making `sizer output count == router output count` a mechanically assertable invariant in golden-fixture tests.

## Considered Options

- **Sizers dedup (rejected)** — keeps existing step-4 prompt text in place, but splits element identity across 13 prompts, makes sizer counts unpredictable, weakens fixture assertions, and adds a CV instability source.
- **Router extracts at identity granularity (chosen)** — identity is inseparable from extraction; one line per dimension in the Router prompt; sizing rubrics (the bulky XS–XXXL tables) stay in sizers.

## Consequences

- Boundaries' "count once per medium" rule migrates from `step4_flow_bcp_boundaries.jinja2` into the Router prompt.
- Notification-like dimensions must have identity rules that prevent over-collapsing (two emails to different recipients = two elements).
- Router prompt quality becomes doubly load-bearing (exclusivity + identity); golden fixtures must assert both the partition and the element counts.
