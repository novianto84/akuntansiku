# TADR-17 — Deployment Topology

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

Which deployment topology candidates fit security, maintainability, backup,
availability, cost, future scale, integration, and customer access — comparing
managed/shared hosting, VPS, self-hosted, hybrid, and containerized deployment —
without deploying anything or inferring business operational requirements?

## Authoritative Inputs

- CD-01 S5 (supporting capabilities implying hosted customer/technician access).
- Deployment operational context gate: UNRESOLVED (no formal identifier; business
  resourcing context is Human input).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21) (technical criteria only): containerized
deployment on VPS-or-equivalent as the candidate direction — reproducible builds,
clear backup story, TLS-terminated customer access, scaling headroom. Product,
sizing, and cost decisions are NOT made here. Nothing is deployed, provisioned,
or configured by this record.

## Alternatives Considered

- **Managed/shared hosting:** lower ops burden; weaker isolation/observability
  control and scaling headroom.
- **Self-hosted:** maximum control; highest ops burden and availability risk
  without dedicated capacity.
- **Hybrid:** split internal/external hosting; most moving parts at this stage.

## Trade-offs

Containerized VPS balances reproducibility and control against ops capacity
needs; the right answer depends on business cost/ops context only the Human can
provide.

## Business Rules Preserved

None altered. One-platform/one-database posture is unaffected by topology choice.

## Dependencies / Deferred Decisions

Deployment operational context: UNRESOLVED (non-blocking for the proposal;
required before any selection).

## Security Impact

Topology determines TLS posture, secret handling, backup encryption, and network
exposure; each candidate carries a different hardening checklist (deferred to
selection).

## Audit / Traceability Impact

Deployment choice must preserve audit-log integrity and retention posture (with
TADR-18).

## Operational Impact

Backup/restore verification, health checks, and availability posture follow from
the selected topology; none implemented here.

## Reversibility

Medium: containerization keeps future moves cheap; data gravity dominates later.

## Open Questions

- Business cost/operations capacity context (Human input).
- Product and sizing selection (post-context planning).

## Approval Boundary

Requires Human operational context, then approval of any selection. Authorizes no
provisioning, deployment, configuration change, or Programmer handoff.
