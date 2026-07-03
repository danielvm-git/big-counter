# 0011 — Models are pinned per calibration; a model change is a recalibration event

**Status:** accepted (2026-07-02)

The BCP philosophy demands a ruler "stable and unchangeable over time," but an LLM counter inherits drift from its model. Policy: each calibration pins an exact model snapshot (never a floating alias like "gpt-4o") and deterministic sampling — temperature 0 and a fixed seed where the provider supports it, recorded in the provenance block (ADR-0010). Phase 5 CV targets are claims about one calibration, not about the counter in the abstract.

When a pinned model must change (deprecation, cost, quality), that is a **recalibration event**, run as a protocol, never a config edit:
1. Run the golden fixture corpus and the 25-iteration stability protocol on the candidate model.
2. Compare per-dimension CV and mean scores against the current calibration; tune decision-table thresholds if needed (fresh recorded responses — the replay corpus is per-model and never replays across models).
3. Publish a new `calibration_id` with a migration note stating the observed mean shift, so velocity series can be bridged deliberately or restarted.

## Consequences

- Deterministic sampling is the cheapest variance reduction available and becomes the default everywhere, including the comparison tool.
- Recorded-response corpora are tagged with model_id; cross-model replay is rejected by the harness.
- Provider deprecation timelines become an operational risk to track — pinning exact snapshots means migrations are scheduled work, not surprises.
