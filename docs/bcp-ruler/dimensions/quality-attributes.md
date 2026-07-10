---
type: Dimension
title: Quality Attributes
description: >
  NFR dimension — counts quality attribute requirements (performance,
  reliability, scalability, maintainability) that exceed standard expectations.
tags: [non-functional, planned, nfr]
timestamp: 2026-07-03T00:00:00Z
---

# Quality Attributes (Dimension 11)

Counts Non-Functional Requirements related to system qualities —
performance, reliability, scalability, availability, maintainability,
observability — but only when they **exceed standard expectations**.

## Identity Rule

**One element per distinct quality attribute requirement.** "Response time
< 200ms AND 99.9% uptime" = 2 elements. Each NFR is routed regardless; the
[NFR Gate](/concepts/nfr-gate.md) decides at sizing time whether it scores.

## Decision Table

| QA requirement scope              | Size | Points |
|-----------------------------------|------|--------|
| Standard expectation (table stakes)| N/A  | 0      |
| Modest above standard             | XS   | 1      |
| Significant above standard        | S    | 2      |
| Demanding                          | M    | 3      |
| Highly demanding                   | L    | 5      |
| Extreme / unprecedented           | XL   | 8      |

**Standard expectation examples:** "The page should load," "the system should
be available during business hours," "errors should be logged."

## NFR Gate

A requirement judged a standard expectation scores N/A (0 points) with a
one-line rationale. The Router routes every distinct NFR requirement
regardless — gating is a sizing judgment, never a routing one. Gated
requirements stay visible in output for CV tuning.

## Examples

**Story:** "Refund processing must complete within 2 seconds. The system must
handle 10,000 refunds/hour during peak."

- Element 1: latency SLA (2s) → above standard for refund processing → S → 2
- Element 2: throughput (10K/hr) → above standard → S → 2
- Total: 4 points

## Relationships

- NFR requirements that also relate to security go to [Security &
  Compliance](/dimensions/security-compliance.md)
- NFR requirements about user interaction go to [UX &
  Accessibility](/dimensions/ux-accessibility.md)
