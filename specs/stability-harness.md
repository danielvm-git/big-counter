# Stability Harness — `run_stability.py` design

Referenced by CONVENTIONS.md and PLAN.md Phases 1/5; specified here. Serves two masters: the CV measurement protocol (whitepaper Exhibits 9–10) and ADR-0007's offline threshold replay.

## Modes

### 1. Record (live runs)

```bash
python run_stability.py <story.md> --iterations 25 [--provider openai] [--out tests/results/stability/]
```

Runs the full pipeline N times. Persists one JSONL record per iteration under
`tests/results/stability/<story-slug>/<calibration_id>/run-NNN.jsonl` containing:

- **Raw LLM response text per stage and per dimension** — this is the Replay Corpus; without it ADR-0007's offline tuning is impossible
- Parsed elements from the Router, with dimension tags (and the unclassified bucket)
- Per-dimension: element count, itemized Dimension Score, subtotal
- Maturity score, Confidence Verdict, total BCP
- Retry events (which dimension, which attempt) — ADR-0008's prompt-quality signal
- Full provenance block (ADR-0010): calibration_id, model_id, sampling params
- Wall time and token usage per call (Phase 5 cost accounting)

### 2. Report

```bash
python run_stability.py --report tests/results/stability/<story-slug>/<calibration_id>/
```

Emits per story:

- **Per-dimension CV of subtotal** — the headline metric (targets: <20% intrinsic, whitepaper Exhibit 9)
- **Per-dimension CV of element count** — separates routing flap (Router problem) from sizing flap (decision-table problem); a dimension can only be diagnosed with both
- Aggregate CV, maturity-bucketed per Exhibit 10 (`reliable`/`moderate`/`low` reported separately; targets apply to `reliable` only)
- Retry rate per dimension; unclassified-bucket frequency

### 3. Replay (offline, zero API cost)

```bash
python run_stability.py --replay <corpus-dir> --thresholds <thresholds-file>
```

Re-runs `validate` + `score` (pure, ADR-0007) over recorded raw responses with candidate decision-table thresholds; emits the same report. Guards:

- Refuses to replay across model_ids (ADR-0011 — corpus is per-model)
- Refuses if the corpus calibration_id's *prompt* component differs from current prompts (recorded responses answer the old prompt; only thresholds may vary in replay)

## Invariant checks (every mode)

Each record is validated against the CONTEXT.md invariants: exclusive ownership, count preservation (router count == sized count per dimension), sum integrity (total == Σ subtotals). Violations fail the run loudly — the harness is also the invariants' production auditor.

## Out of scope

Sprint-level velocity aggregation and dashboards — the harness measures the counter, not the team.
