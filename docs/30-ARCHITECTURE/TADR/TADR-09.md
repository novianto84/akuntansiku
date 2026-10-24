# TADR-09 — Correction / Revision Mechanism

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

How is the governed correction flow (REOPEN → CORRECTION → REVIEW → CLOSED for
WO; revision semantics for commercial/price records) technically realized so that
post-completion correction is never a direct overwrite without controlled history?

## Authoritative Inputs

- CD-11 §§2, 9, 10, 18, 28, 30 (WAITING APPROVAL correction sideroutes;
  cancellation boundary; visit correction discipline; report finalization;
  correction/cancellation/reopen/re-create records; supersession/purge list) —
  SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF — CD-11 Business Finalization,
  CD11-001…CD11-029; correction decisions CD11-006…CD11-008, CD11-010, CD11-012).
- CD-08 (immutability; lifecycle nonaktif/arsip instead of hard delete).
- CD-05/CD-06/CD-09 (revision chains; PO immutability after Issued).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): correction as a first-class governed flow —
REOPEN creates a correction context on a CLOSED record; CORRECTION
records changes as new versions (never silent in-place mutation — the WAITING
APPROVAL direct-EDIT sideroute is the single audited exception, see alignment
below); REVIEW re-applies the
mandatory pre-CLOSED review; re-CLOSED binds reviewer identity. CANCELLED stays
outside correction reach at the guard level (cancellation only from OPEN /
IN_PROGRESS; CANCELLED terminal, never REOPEN — TADR-04). Commercial and price
corrections reuse the same versioning substrate (TADR-08).

CD-11 Direction Alignment (2026-09-22; business baseline SIGNED-OFF / LOCKED /
CLOSED — no business rule changed here). The governed-flow direction above is
retained, clarified against the canonical baseline as follows (direction only;
no schema, storage mechanism, or implementation detail is decided here):

- Two distinct correction scopes MUST be representable (CD11-007): minor
  correction and substantive correction. Their business definitions/content are
  NOT invented here; the architecture direction is only that the flow substrate
  MUST NOT assume a single correction kind.
- Pre-CLOSED correction loop (CD11-006, CD11-008; CD-11 §§2, 18): during
  `WAITING APPROVAL`, REQUEST CORRECTION → CORRECTION_REQUIRED → resubmission.
  The Report stays NON-FINAL throughout this loop; Visit `COMPLETED`, outcome
  DONE, `WAITING APPROVAL`, and CORRECTION_REQUIRED do NOT finalize the Report.
- Numbered, unlimited cycles (CD11-008; CD-11 §28): correction history is
  CONTROLLING data (not merely audit sidecar) with numbered cycles; the business
  rule sets NO maximum cycle count, so the technical direction MUST NOT impose
  one. Every cycle records actor, server timestamp, action, object, reason, and
  before/after where relevant (CD11-012).
- Post-CLOSED REOPEN (CD-11 §28): REOPEN applies ONLY to `CLOSED` (returns to
  `IN_PROGRESS`, same WO number/Report, assignment restored, new target
  editable, prior history preserved). `CANCELLED` is terminal and can NEVER
  REOPEN; `CLOSED` can never be cancelled. The stale formulation "CANCELLED
  unavailable post-COMPLETED" is SUPERSEDED — `COMPLETED` is not a WO status and
  the boundary is: cancellation only from `OPEN` / `IN_PROGRESS` (CD11-010).
- RE-CREATE is NOT a correction transition: it yields a new WO/number/Report/
  history with `CREATED_FROM` lineage (CD-11 §28); continuity is lineage-based,
  not identity-based.
- Official/approved-result history MUST remain traceable: draft Final Conclusion,
  approver modification/established final, and the approved official conclusion
  (CD-11 §18) form one traceable chain with actor/timestamp; correction MUST
  NEVER orphan or silently replace the approved result.
- Direct edit during `WAITING APPROVAL` (CD-11 §2: authorized reviewer may EDIT
  directly with mandatory reason): where the implementation stage permits it,
  the direction REQUIRES a clear audit linkage (actor, timestamp, reason,
  before/after) on the same controlling-history substrate — direct edit is an
  audited sideroute of the governed flow, never a bypass of it. No direct-edit
  path on `CLOSED` records is opened by this direction.

## Alternatives Considered

- **In-place edit with audit log entry:** simpler UX; rejected — it normalizes
  overwrite as the primary path and weakens the revision-only business rule.
- **Cancel-and-recreate for corrections:** clean slate; rejected post-completion —
  it breaks history continuity and misuses CANCELLED against its locked boundary.

## Trade-offs

First-class correction flow costs more design (states, permissions, UX) but keeps
history continuous and the CANCELLED boundary intact.

## Business Rules Preserved

REOPEN → CORRECTION → REVIEW → CLOSED (post-CLOSED scope); WAITING APPROVAL
correction loop (REQUEST CORRECTION → CORRECTION_REQUIRED → resubmission);
numbered unlimited correction cycles as controlling data; no direct overwrite
except the business-locked WAITING APPROVAL direct-EDIT sideroute which itself
requires mandatory reason plus full audit linkage; CANCELLED boundary
(cancellation only from OPEN/IN_PROGRESS; CANCELLED terminal, never REOPEN);
reviewer authority; reason-required discipline.

## Dependencies / Deferred Decisions

TADR-08 (versioning substrate). Kept separate from TADR-08 because this record
governs the flow and authority while TADR-08 governs the storage mechanism.

## Security Impact

Correction authority is a privilege boundary: only Manager/Admin roles may
authorize REOPEN/CANCEL-class transitions (role content itself business-owned).

## Audit / Traceability Impact

Correction contexts link original → correction → review → re-closure as one
traceable chain with reviewer binding.

## Operational Impact

Returned-for-correction work surfaces in Outstanding attention views; no blocking
or escalation invented.

## Reversibility

Medium: flow shape is cheap to adjust pre-implementation.

## Open Questions

- Correction-context presentation and UX (implementation planning, non-authoritative).

## Approval Boundary

Requires Human approval of the flow realization. Authorizes no code, schema,
migration, or Programmer handoff.
