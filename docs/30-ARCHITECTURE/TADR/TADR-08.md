# TADR-08 — Audit / Versioning Mechanism

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

Which versioning/audit mechanism best preserves completed-record protection,
correction history, reviewer accountability, and timestamp integrity — comparing
immutable version records, append-only audit log plus current projection, audit
sidecar, temporal validity, and hybrid — without selecting a final mechanism
without justification?

## Authoritative Inputs

- CD-08 (price/master history immutability; suggest/approve; nonaktif/arsip).
- CD-11 §§2, 9, 18, 28, 30 (WAITING APPROVAL correction sideroutes; cancellation
  boundary; report finalization; correction/cancellation/reopen/re-create records
  with numbered cycles as controlling data; supersession/purge list) —
  SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF — CD-11 Business Finalization,
  CD11-001…CD11-029; CD11-006, CD11-008, CD11-010, CD11-012).
- CD-04/CD-06/CD-09/CD-10 version-chain language (v1 lestari; revision semantics).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21) (technical criteria only): hybrid —
immutable version records for commercial and price domains; append-only
governance trail for WO correction/review; event-time plus record-time capture
for emergency retroactive work. Required trail fields regardless of mechanism:
actor, timestamp(s), before-version, after-version, reason, reviewer,
approval/review state, traceability links.

## Alternatives Considered

- **Immutable version records alone:** matches CD language natively; weaker
  governance-trail narrative for multi-step WO correction.
- **Append-only log plus projection alone:** strongest replay; projection
  lag/divergence risk and heavier operations.
- **Audit sidecar alone:** simplest retrofit; dual-write divergence and
  truth-ambiguity risk — weakest fit for the one-history principle.
- **Temporal validity alone:** expresses offer validity and retroactive display
  well; confusable with business effective-dates and incomplete for correction
  governance.

## Trade-offs

Hybrid fits each domain's existing business language and keeps correction native,
at the cost of operating two patterns (version chains + governance trail).

## Business Rules Preserved

Revision-governed correction (revision chains plus the single business-locked
WAITING APPROVAL direct-EDIT sideroute, which itself requires mandatory reason
and full audit linkage per TADR-09); preserved history everywhere the baseline
demands it;
reviewer accountability. Emergency timestamp precedence convention is NOT decided
here (Human gate).

## Dependencies / Deferred Decisions

TADR-09 (correction flow that rides this mechanism). Emergency retroactive
timestamp convention: UNRESOLVED (non-blocking; dual capture proceeds).

## Security Impact

Trail must be tamper-evident; no direct-edit path may exist on CLOSED records.
The single business-locked exception — direct EDIT during WAITING APPROVAL with
mandatory reason — rides this same trail with full audit linkage (actor,
timestamp, reason, before/after) and never bypasses the governed flow
(see TADR-09).

## Audit / Traceability Impact

This TADR is the core auditability proposal: complete before/after lineage with
reviewer binding on every correction.

## Operational Impact

Version-graph growth and trail retention are capacity considerations for
implementation planning; no retention windows invented here.

## Reversibility

Medium: trail content is forever; mechanism internals remain replaceable
pre-implementation.

## Open Questions

- Retention windows and trail-storage mechanics (implementation planning).
- Whether store-level immutability features are adopted (implementation planning).

## Approval Boundary

Requires Human approval of the hybrid direction. Authorizes no schema, code,
migration, or Programmer handoff.
