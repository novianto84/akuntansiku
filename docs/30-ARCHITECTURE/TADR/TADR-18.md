# TADR-18 — Observability / Traceability

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

What observability and traceability is architecturally required — application
logs, audit logs, security events, background-job status, integration failures,
health checks, metrics, alerts, end-to-end traceability — and what leakage rules
govern it?

## Authoritative Inputs

- CD-08 (governance trail expectations).
- CD-11 (review/correction/Outstanding visibility needs) — SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF).
- AI_OPERATING_RULES §10 (traceability chain down to Test/Audit).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): structured application, audit, security,
job, integration, and health telemetry with metrics plus alerts, and end-to-end
traceability from operational record → projection → published view. Log-leakage
prohibition: no acquisition prices, vendor intelligence, internal notes, tokens,
secrets, or customer-external data in logs. Security events include auth
failures, privilege changes, isolation violations, and QR-abuse signals.

## Alternatives Considered

- **Minimal logging:** cheaper; rejected — audit-grade traceability and isolation-
  violation detection are baseline requirements, not options.
- **Verbose debug-by-default:** easier troubleshooting; rejected as default —
  leakage and volume risk; debug verbosity stays environment-gated (mechanics at
  implementation planning).

## Trade-offs

Full-spectrum telemetry costs volume and retention planning but is the only
posture consistent with revision-only correction, workspace isolation, and
external-visibility guarantees.

## Business Rules Preserved

No business rule altered; observability exposes compliance with rules rather
than creating new ones.

## Dependencies / Deferred Decisions

None blocking. Retention windows and alert thresholds with business meaning
(e.g. any future SLA-like threshold) remain Human-owned and are not invented.

## Security Impact

Telemetry is itself sensitive: leakage rules, sealed secret handling for
observability credentials, tamper-evident audit-log handling.

## Audit / Traceability Impact

This TADR is the auditability backstop: every governance-relevant event class
has a required home; missing links must be reported per operating rules.

## Operational Impact

Dashboard/alert ownership and on-call posture deferred to implementation
planning; no schedule or threshold invented here.

## Reversibility

High: telemetry coverage is additive.

## Open Questions

- Retention windows and storage mechanics (implementation planning).
- Alert routing and ownership (implementation planning).

## Approval Boundary

Requires Human approval of the observability scope. Authorizes no
instrumentation code, infrastructure, or Programmer handoff.
