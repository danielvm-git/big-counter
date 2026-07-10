# PLAN: BCP Plus — Full 13-Dimension Counter

## Goal
Extend the existing `bcp-agent` (flow-ciandt/bcp-agent) from a 3-dimension simplified counter into a full 13-dimension BCP Plus counter with per-dimension prompt architecture, targeting aggregate CV ≈ 10%.

## Technology Decision
**Python** — we are building on top of `bcp-agent` which is Python/LangChain. The CONVENTIONS.md TypeScript template was generated for a different project intent; it will be updated to reflect Python conventions.

## Strategy: Minimal-Change Extension

1. **Copy** `bcp-agent` code verbatim into this project
2. **Add** 7 functional + 3 non-functional dimensions as new prompt templates + scoring steps
3. **Keep** existing 3 dimensions untouched (they work, just incomplete)
4. **Add** stability testing harness (run N iterations, measure CV)
5. **Iterate** prompts until CV ≈ 10% per dimension

## Missing Dimensions to Add

### Functional (7 missing)
| # | Dimension | Scoring |
|---|-----------|---------|
| 3 | Roles / Permissions | S(2) → L(5) |
| 4 | Solution Variabilities | S(2) → XL(8) |
| 6 | Domain Entities | XS(1) → XL(8) |
| 7 | New Domain Entities | M(3) → L(5) |
| 8 | Background Processes | M(3) → XL(8) |
| 9 | Notifications | XS(1) per notification |
| 10 | Audits | XS(1) per entity |

### Non-Functional (3 missing)
| # | Dimension | Scoring |
|---|-----------|---------|
| 11 | Quality Attributes | XS(1) → XL(8) |
| 12 | Security & Compliance | XS(1) → XL(8) |
| 13 | UX & Accessibility | XS(1) → XL(8) |

## Implementation Phases

### Phase 1: Bootstrap — Copy, Fix Routing & Verify Baseline
- Copy `bcp-agent` into `src/` (done)
- Install deps, run existing tests (done)
- Behavior-preserving refactor: extract the 3 existing dimensions into Dimension Modules (ADR-0007) with itemized Dimension Scores, generic calculator loop, typed result model with provenance block (ADR-0010), StepLogger deleted — current inputs kept (including the Test-Plan double-feed, deliberately) so pinned test totals prove the refactor moved nothing
- Add Element Router (step 3.5) per ADR-0001/0002/0003 + retry-then-fail semantics (ADR-0008) + parse-or-raise contract (ADR-0009) + single orchestration function with Confidence Verdict — entry points become transport adapters
- Independent (any time): ProviderConfig value object; kill os.environ mutation in MCP HTTP server
- Build stability harness per specs/stability-harness.md (record / report / replay modes, deterministic sampling per ADR-0011)
- Run stability test on existing 3 dimensions (post-Router) → establish CV baseline (ADR-0004)

### Phase 2: Add Functional Dimensions 6–10 (Entities, Processes, Notifications, Audits)
- These are structurally simpler (count-based or XS per occurrence)
- Write prompt templates, extend BCPCalculator steps, add tests
- Measure per-dimension CV

### Phase 3: Add Functional Dimensions 3–4 (Roles, Variabilities)
- These require more complex prompt logic (decision trees)
- Write prompt templates with explicit decision criteria from whitepaper
- Measure per-dimension CV

### Phase 4: Add Non-Functional Dimensions 11–13
- Quality Attributes, Security & Compliance, UX & Accessibility
- Gate by "exceeds standard expectations" condition
- Measure per-dimension CV

### Phase 5: Stability Tuning
- Run 25-iteration protocol across all 13 dimensions
- For dimensions with CV > 20%: tune decision-table thresholds (ADR-0006), sharpen Router identity rules — prompt prose rewrites are the last resort
- Target aggregate CV ≈ 10%

### Phase 6: Package & Offer Back
- Polish, document, add comparison tool
- Write the BCP Plus whitepaper evolution — normative ruler definitions from specs/CONTEXT.md + ADRs (ADR-0005)
- Ship BCP Ruler as OKF bundle with interactive graph (docs/bcp-ruler/)
- Serialize BCP results as OKF bundles (e10)
- Prepare PR/extension proposal for flow-ciandt/bcp-agent

### Phase 7 (post-release): Domain Knowledge Input (e11)
- Optional OKF domain bundle as BCP scoring reference material
- Entity dimensions, Roles/Permissions, NFR dimensions benefit from domain ground truth

## Key Architectural Decisions
1. **Per-dimension prompts** (whitepaper recommendation) — each dimension gets its own Jinja2 template, not a single chain
2. **Step 3 (Break Elements) prompt stays as-is; a new Element Router (step 3.5) owns dimension classification** — every Complexity Element gets exactly one dimension; all sizers consume only routed elements (see specs/ADRS/0001–0003, specs/CONTEXT.md invariants)
3. **Separate NFR gating** — NFR dimensions only score when requirements exceed standard expectations
4. **Maturity score surfaced** as confidence indicator alongside BCP total
5. **Stability harness** runs N iterations per story, measures CV% per dimension

## Success Criteria
- [ ] All 13 dimensions scored per story
- [ ] Per-dimension CV < 20% for intrinsic, < 25% for maturity-dependent
- [ ] Aggregate CV ≈ 10–15%
- [ ] The 3 original dimensions' scoring rules (weights, bucketing) unchanged and covered by updated unit tests; real-story score shifts expected, explained by the double-feed fix, and documented in the Phase 1 baseline report (ADR-0004)
- [ ] No element is counted in two dimensions — golden-fixture tests assert the Router's partition, element counts, and expected splits for mixed sentences
- [ ] CLI, API, MCP, SDK entry points all work with 13 dimensions
