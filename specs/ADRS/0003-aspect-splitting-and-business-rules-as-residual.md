# 0003 — Aspect splitting with Business Rules as the residual dimension

**Status:** accepted (2026-07-02)

Real story sentences mix aspects owned by different dimensions ("Only admins can approve refunds over $1,000" = authorization + threshold logic). We decided exclusivity is over *elements, not sentences*: the Router may split one sentence into multiple Complexity Elements, each routed to the most specific dimension that claims its aspect (Specificity Precedence), with Business Rules receiving conditional logic only as the residual — when no specific dimension owns the aspect.

## Considered Options

- **Whole sentence → Business Rules** — starves Roles/Permissions (and Notifications/Audits/Background Processes), since most such aspects arrive wrapped in rule-shaped sentences; rejected.
- **Whole sentence → the specific dimension** — genuine decision logic escapes Business Rules and stories get undersized; rejected.
- **Aspect splitting + residual precedence (chosen)** — each aspect counted exactly once, deterministic tie-break instead of per-run judgment (a CV-noise source).

## Consequences

- Over-splitting becomes the new failure mode: golden fixtures must pin expected element splits for mixed sentences like the refund example.
- The Business Rules sizer prompt must state it is residual, so it stops claiming authorization/notification/audit aspects it prices today.
