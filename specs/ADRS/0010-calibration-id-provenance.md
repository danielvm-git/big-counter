# 0010 — Every result carries a provenance block keyed by an explicit calibration_id

**Status:** accepted (2026-07-02)

Multiple legitimate events change scores over time: the double-feed fix (ADR-0004), ruler evolution (ADR-0005), threshold tuning (Phase 5), and LLM model changes. Velocity monitoring breaks silently if a chart mixes numbers produced under different calibrations. Every result therefore carries a provenance block: `calibration_id` plus its components — `counter_version` (package semver), `ruler_version` (whitepaper evolution version), `provider`, `model_id` (exact snapshot, e.g. gpt-4o-2024-05-13), sampling params (temperature/seed), and timestamp.

`calibration_id` is an explicit human-set label (not a hash), bumped on **any score-affecting change**: ruler definition, prompt text, decision-table thresholds, or model. Two BCP numbers are comparable if and only if their `calibration_id` matches; velocity tooling segments series by it. A calibration bump is exactly an ADR-0004-style re-baseline event and gets a one-line note in the changelog explaining the expected shift.

## Consequences

- The provenance block is a field of the typed result model from its first commit (Phase 1 refactor), so no historical results ever lack it.
- CI can enforce the bump: a diff touching prompts/, thresholds, or pinned model without a calibration_id change fails review.
- Consumers (API, MCP, SDK, comparison tool) expose provenance verbatim — stripping it is a defect.
