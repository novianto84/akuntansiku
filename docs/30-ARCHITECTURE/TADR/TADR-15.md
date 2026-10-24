# TADR-15 — Background Jobs / Notifications

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

Which background-job and notification needs exist (reminders, projection refresh,
Outstanding refresh, email, photo processing, scheduled maintenance) and how are
they architected so that manual reminder remains the baseline and no automatic
behavior is silently enabled?

## Authoritative Inputs

- CD-11 §§20, 23, 24, 28, 30 (Outstanding as monitoring/attention, overdue timer
  nonaktif; manual reminder, automatic generation/interval disabled; emergency
  retroactive convention without numeric SLA; SLA history preservation;
  supersession/purge list incl. numeric SLA / H-1 / overdue / escalation as
  retired active rules) — SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF — CD-11
  Business Finalization, CD11-001…CD11-029; SLA decision CD11-011).
- CD-01 S5 (notification as supporting capability, detail open).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): a job framework whose every policy-unresolved
job exists only as a disabled-by-default candidate behind an explicit Human
policy flag. Manual-reminder flows proceed without automation. Every job is
idempotent, status-visible, retry-explicit, and failure-observable (TADR-18), and
embeds no business policy (no intervals, thresholds, escalation, or auto-blocking).

CD-11 Direction Alignment (2026-09-22; business baseline SIGNED-OFF / LOCKED /
CLOSED — no business rule changed here; NO SLA reactivated). Consistency review
outcome: the disabled-by-default direction above is already consistent with the
canonical baseline and is CONFIRMED (not redirected). For the record, the
baseline constraints this direction honors (CD11-011; CD-11 §§20, 28, 30):

- Numeric SLA for P1: DISABLED as an active rule. H-1: DISABLED. Overdue
  calculation: DISABLED. Escalation automation: DISABLED. No job, timer,
  threshold, or automation enabled under this TADR may reintroduce any of them
  as active behavior.
- Outstanding remains a monitoring/attention concept only — never overdue, SLA,
  escalation, or blocking (CD-11 §20). Outstanding-view refresh jobs (if any)
  refresh attention surfacing only.
- Timestamps and history are RETAINED: SLA-related history that exists
  (e.g. preserved across REOPEN cycles, CD-11 §28) stays lestari/auditable;
  retention is an audit property, not an activation of SLA behavior.
- Legacy/old SLA values, if encountered, are future-reference / historical
  context ONLY (CD-11 §30) — they MUST NOT be interpreted or served as active
  thresholds by any job or notification path.
- Manual reminder by Admin/Manager/Sales remains the business baseline
  (CD-11 §23); automatic reminder generation and intervals remain disabled
  Phase 1. No schedule, interval, threshold, or escalation invented here.

## Alternatives Considered

- **Enable auto-reminders now:** convenient; rejected — silent business behavior.
- **No job framework:** avoids unused scaffolding; rejected — projection refresh,
  photo derivatives, and maintenance need a home later; retrofit cost higher.

## Trade-offs

Framework-with-disabled-jobs costs scaffolding without immediate behavior, but
guarantees automation can never precede policy.

## Business Rules Preserved

Manual-reminder baseline; numeric SLA / H-1 / overdue / escalation DISABLED as
active rules (CD11-011; retired per CD-11 §30, old values future-reference
only); timestamps/history retained as audit property; Outstanding stays non-SLA
monitoring; no numeric timers invented; nothing reactivated.

## Dependencies / Deferred Decisions

Reminder/automation policy gate (partly blocking for enabling any auto job;
non-blocking for the framework direction).

## Security Impact

Job runners operate under scoped service authority; notification content passes
through the same visibility filtering as interactive views.

## Audit / Traceability Impact

Job runs, policy-flag changes, and delivery attempts are observable and traceable;
policy enablement itself is an audited business action.

## Operational Impact

Queue/backoff/dead-letter posture deferred to implementation planning; no
schedule invented here.

## Reversibility

High: jobs are additive and flag-gated.

## Open Questions

- Transport and scheduling substrate (implementation planning).
- Which jobs (if any) the business wants enabled first (Human policy gate).

## Approval Boundary

Requires Human approval of the disabled-by-default direction. Authorizes no
enabled automation, code, schema, migration, or Programmer handoff.
