# OKF Integration Plan

Leverages [Open Knowledge Format (OKF v0.1)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
— a vendor-neutral, markdown+YAML-frontmatter knowledge representation format
designed for co-production by humans and AI agents — across three integration
points.

## Integration 1: BCP Ruler as OKF Bundle ★★★★★

**Epic:** e09 (existing, new story e09s02)
**Type:** Documentation artifact — zero code changes
**When:** Phase 6 (can be drafted now)

Ship the 13-dimension BCP Plus methodology as a self-documenting, browsable,
agent-consumable OKF bundle alongside (or replacing) the static whitepaper.

### Bundle structure

```
bcp-ruler/
├── index.md                        # BCP Plus methodology overview + version
├── dimensions/
│   ├── index.md                    # All 13 dimensions with subtotals
│   ├── boundaries.md
│   ├── interface-elements.md
│   ├── business-rules.md
│   ├── roles-permissions.md
│   ├── solution-variabilities.md
│   ├── domain-entities.md
│   ├── new-domain-entities.md
│   ├── background-processes.md
│   ├── notifications.md
│   ├── audits.md
│   ├── quality-attributes.md
│   ├── security-compliance.md
│   └── ux-accessibility.md
├── concepts/
│   ├── index.md                    # Domain glossary
│   ├── complexity-element.md
│   ├── element-router.md
│   ├── identity-rule.md
│   ├── sizer.md
│   ├── dimension-module.md
│   ├── nfr-gate.md
│   └── maturity-score.md
└── viz.html                        # Interactive graph (generated via OKF visualizer)
```

### Why

- Makes the BCP methodology **agent-consumable** — another AI agent can read the
  OKF bundle and understand scoring rules without consulting a PDF
- The OKF `viz.html` gives an **interactive force-directed graph** of all 13
  dimensions, their identity rules, and cross-relationships — more useful than a
  static whitepaper
- Version-controlled alongside the code; calibration_id changes are visible as
  diffs in the bundle
- Proves BCP methodology is vendor-neutral — anyone can produce/consume OKF

### Implementation

- Author markdown files following the OKF v0.1 spec
- Run `python -m reference_agent visualize --bundle ./bcp-ruler/` to generate viz.html
- Commit the bundle to the repo under `docs/bcp-ruler/`
- Link from README and whitepaper

---

## Integration 2: BCP Results Output as OKF ★★★★☆

**Epic:** e10 (new)
**Type:** Feature — ~100 lines of Python + tests
**When:** Phase 6 (after e09 or bundled with it)

After scoring a story, the BCP counter can optionally output results as an OKF
bundle, giving instant visual graph debugging of element→dimension routing and
making results portable, version-controllable artifacts consumable by downstream
tools.

### Bundle structure

```
results/<story-slug>-<calibration_id>/
├── index.md                        # Total BCP, maturity, confidence verdict
├── story.md                        # Original story as a concept
├── elements/
│   ├── index.md                    # All Complexity Elements
│   ├── elem-001.md                 # type: Complexity Element
│   │                               # dimension: Boundaries
│   │                               # size: M, points: 2
│   │                               # Links to its owning dimension
│   └── elem-NNN.md
├── dimensions/
│   ├── index.md                    # Per-dimension subtotals
│   ├── boundaries.md               # Sized elements + subtotal + rationale
│   └── ...
├── provenance.md                   # calibration_id, model_id, sampling params
└── viz.html                        # Graph: story → elements → dimensions → scores
```

### Why

- **Visual Router debugging** — the graph view immediately shows which elements
  went to which dimensions; misrouted elements are visually obvious
- Results become **portable artifacts** that any OKF consumer can ingest
- Perfect pairing with the **stability harness** — adding `--output-okf` to
  `run_stability.py` gives visual diffing of Router behavior across iterations
- CONTEXT.md **invariants** (exclusive ownership, count preservation, sum
  integrity) map naturally to OKF graph edges — violations become visible
  anomalies in the graph

### Implementation outline

1. New module `src/bcp/okf_serializer.py`:
   - `serialize_result(result: BCPResult, out_dir: Path) -> None`
   - Writes markdown+frontmatter files per the OKF v0.1 spec
   - Links elements to their owning dimension concepts
2. CLI flag: `--output-okf <dir>` on `run_cli.py`
3. Stability harness flag: `--output-okf <dir>` on `run_stability.py`
4. Optional: embed the OKF visualizer or shell out to generate viz.html

### Stories

| Story | Title | BCPs |
|-------|-------|------|
| e10s01 | OKF serializer for BCPResult | 3 |
| e10s02 | CLI + harness integration + tests | 2 |

---

## Integration 3: Domain Knowledge as BCP Input ★★★☆☆

**Epic:** e11 (new)
**Type:** Feature — new capability, ~200–300 lines + tests
**When:** Post-release (after e09)

The BCP agent optionally consumes an OKF domain knowledge bundle as reference
material, transforming scoring from "guess from story text" to "reason with
domain ground truth."

### How it works

The user (or an automated pipeline) produces an OKF bundle describing their
domain — entities, roles, APIs, quality standards, compliance requirements. The
BCP agent loads this bundle and uses it as reference context during scoring.

### Dimension-by-dimension impact

| Dimension | How OKF helps |
|-----------|---------------|
| 3 — Roles/Permissions | Cross-reference mentioned roles against the known role catalog; detect unauthorized access patterns |
| 4 — Solution Variabilities | Identify variability axes already documented in the domain |
| 6 — Domain Entities | Confirm entity is existing — look up in the bundle's entities/ |
| 7 — New Domain Entities | Confirm entity is truly new — absence from bundle is evidence |
| 11 — Quality Attributes | Compare story requirements against "standard expectations" in bundle; operationalizes the NFR Gate |
| 12 — Security & Compliance | Load compliance requirements from bundle as decision-table inputs |
| 13 — UX & Accessibility | Load accessibility standards from bundle for baseline comparison |

### Bundle structure (example)

```
acme-knowledge/
├── index.md
├── entities/
│   ├── index.md
│   ├── order.md                   # type: Domain Entity
│   ├── customer.md
│   └── refund.md                  # type: Domain Entity, status: new
├── roles/
│   ├── index.md
│   ├── admin.md                   # type: Role, permissions: [...]
│   └── agent.md
├── quality/
│   ├── index.md
│   └── sla.md                     # type: Quality Standard
├── compliance/
│   ├── index.md
│   └── pci-dss.md                 # type: Compliance Requirement
└── viz.html
```

### Implementation outline

1. New module `src/bcp/okf_loader.py`:
   - `load_bundle(path: Path) -> OKFBundle` — parses all .md files into typed concepts
   - `query_entities(bundle, name: str) -> list[Concept]`
   - `query_roles(bundle, name: str) -> list[Concept]`
   - `query_standards(bundle, tag: str) -> list[Concept]`
2. New optional parameter on all entry points: `--knowledge-bundle <path>`
3. Per-sizer integration: each sizer that benefits from domain knowledge receives
   the loaded bundle as optional context injected into the prompt `build_variables()`
4. Prompt template updates: conditionally include domain context sections

### Stories

| Story | Title | BCPs |
|-------|-------|------|
| e11s01 | OKF bundle loader with typed query API | 3 |
| e11s02 | Inject domain knowledge into Entity dimensions (6, 7) | 3 |
| e11s03 | Inject domain knowledge into Roles/Permissions (3) + NFR (11–13) | 3 |
| e11s04 | CLI/API/MCP integration + golden-fixture tests | 3 |

---

## Dependencies

```
e09 (whitepaper + upstream)
├── e09s01: Whitepaper evolution document
└── e09s02: BCP Ruler as OKF bundle (NEW — doc only, no code deps)

e10 (OKF results output — NEW)
└── depends_on: [e02]  (needs BCPResult model from e01s03 + Router from e02)

e11 (Domain knowledge input — NEW)
└── depends_on: [e05, e06, e07]  (needs all sizers to exist)
```

## Risk assessment

| Risk | Mitigation |
|------|------------|
| OKF v0.1 is a draft spec — may evolve | Pin to v0.1 in bundle frontmatter; format is minimal enough that breaking changes are unlikely |
| OKF reference agent depends on Google ADK | We only need the OKF *format*, not the agent. We write our own lightweight parser/serializer (OKF is just markdown+YAML) |
| Domain knowledge bundles may not exist for target orgs | e11 is gated behind `--knowledge-bundle` flag; absent bundle = current behavior preserved |
