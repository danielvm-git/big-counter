---
type: Dimension
title: Security & Compliance
description: >
  NFR dimension — counts security and compliance requirements (authentication,
  encryption, data protection, regulatory) that exceed standard expectations.
tags: [non-functional, planned, nfr]
timestamp: 2026-07-03T00:00:00Z
---

# Security & Compliance (Dimension 12)

Counts Non-Functional Requirements related to security and regulatory
compliance — authentication, authorization architecture, encryption, data
protection, audit compliance, regulatory frameworks (GDPR, PCI-DSS, SOC2,
HIPAA) — but only when they **exceed standard expectations**.

## Identity Rule

**One element per distinct security or compliance requirement.** "Encrypt data
at rest AND mask PII in logs" = 2 elements. Even implicit requirements ("this
handles payment data" implies PCI-DSS) count as elements. Each NFR is routed
regardless; the [NFR Gate](/concepts/nfr-gate.md) decides at sizing time.

## Decision Table

| Security / Compliance scope       | Size | Points |
|-----------------------------------|------|--------|
| Standard expectation              | N/A  | 0      |
| Modest above standard             | XS   | 1      |
| Significant above standard        | S    | 2      |
| Demanding                          | M    | 3      |
| Highly demanding                   | L    | 5      |
| Extreme / regulatory-mandated     | XL   | 8      |

**Standard expectation examples:** "Use HTTPS," "hash passwords," "log access
attempts." **Above standard:** "Field-level encryption for PII," "PCI-DSS
Level 1 compliance," "SOC2 Type II audit trail."

## NFR Gate

Same gating semantics as [Quality Attributes](/dimensions/quality-attributes.md):
standard expectations score N/A (0 pts). The Router routes every distinct
requirement; gating is sizing-only. Regulatory-mandated requirements (PCI-DSS,
GDPR) typically score above standard by default.

## Examples

**Story:** "Refund processing must encrypt PII at rest and in transit.
PCI-DSS Level 1 compliance required for payment data handling."

- Element 1: PII encryption (at rest + in transit) → above standard → S → 2
- Element 2: PCI-DSS L1 compliance → regulatory-mandated → XL → 8
- Total: 10 points

## Relationships

- Authorization logic (who can do what) scores in [Roles /
  Permissions](/dimensions/roles-permissions.md) — Security & Compliance is
  about architectural security properties, not business authorization rules
- Compliance-mandated audits may trigger [Audits](/dimensions/audits.md)
  elements — those score separately
