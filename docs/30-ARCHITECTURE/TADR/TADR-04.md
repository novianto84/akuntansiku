# TADR-04 — Transaction Boundaries

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

Where are consistency boundaries for WO, assignment, service execution,
completion, review, correction, material usage, inventory operation, purchasing,
and receiving — given that material usage plus stock-out is deliberately
non-atomic — without changing any business rule to ease transaction design?

## Authoritative Inputs

- CD-11 §§2, 6, 7, 9, 10, 18, 28, 30 (canonical WO lifecycle, assignment,
  emergency lane, cancellation, visit model, report finalization, correction/
  reopen/re-create records, supersession/purge list) — SIGNED-OFF / LOCKED /
  CLOSED (BA SIGN-OFF — CD-11 Business Finalization, CD11-001…CD11-029).
- CD-09 (PO lifecycle, per-event receiving).
- CD-10 (receiving-to-stock handoff; adjustment discipline).
- CD-05 (partial conversion/fulfillment semantics).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): each lifecycle transition is its own
consistency boundary guarded by an invariant transition matrix. The WO ↔
inventory chain uses paired independent records (MaterialUsage + InventoryOperation)
with mutual references and non-blocking reconciliation visibility for dangling
halves. Receiving-to-stock is causally linked but separately recorded. Commercial
conversions and fulfillments are additive; remainders are computed, never
auto-completed.

CD-11 Direction Alignment (2026-09-22; business baseline SIGNED-OFF / LOCKED /
CLOSED — no business rule changed here): the invariant transition matrix this
TADR proposes MUST represent exactly the canonical WO lifecycle
(CD11-001; CD-11 §2):

```text
DRAFT → OPEN → IN_PROGRESS → WAITING APPROVAL → CLOSED
```

plus terminal `CANCELLED` (CD11-010; CD-11 §9), subject to:

- `IN_PROGRESS` is the canonical WO status for work that has started. `ASSIGNED`
  is NOT a WO status; `UNASSIGNED` is a condition, not a lifecycle state.
- `COMPLETED` is NOT a WO status (it is a Visit lifecycle state / work outcome
  term, CD-11 §§10–11). `CLOSE_WO` is NOT a separate action/state — approval of
  the report closes the WO automatically (`APPROVE REPORT ⇒ WO = CLOSED`).
- `ON PROCESS` is NOT a WO status; it is valid only as a Visit Type (second and
  subsequent visits; CD-11 §10). It MUST NOT appear in the WO transition matrix.
- Transition guards MUST reflect: `OPEN → IN_PROGRESS` only with an assigned
  responsible person (WO without Technician stays `OPEN`/unassigned);
  `IN_PROGRESS → WAITING APPROVAL` only via explicit Technician submit;
  `WAITING APPROVAL → CLOSED` via authorized approval (automatic on approve);
  reviewer sideroutes during `WAITING APPROVAL` (REQUEST CORRECTION →
  CORRECTION_REQUIRED; direct EDIT with mandatory reason; direct CLOSE with
  mandatory reason) are business-locked sideroutes, not new states invented here.
- Cancellation guards MUST reflect CD-11 §9: only from `OPEN` / `IN_PROGRESS`;
  `CLOSED` cannot be cancelled; `CANCELLED` is terminal, cannot be cancelled
  again, cannot REOPEN. No `CANCEL_PENDING_APPROVAL` / `CANCEL_*` states
  (superseded, CD-11 §30).
- REOPEN applies only to `CLOSED` (returns to `IN_PROGRESS`, same number/Report;
  CD-11 §28) and is governed with TADR-09. RE-CREATE yields a new WO/Report with
  `CREATED_FROM` lineage, not a transition of the existing WO.
- Visit lifecycle (`OPEN → COMPLETED`, CD-11 §10) is a SEPARATE matrix from the
  WO lifecycle: Visit `COMPLETED` closes neither the WO nor the Report.
- No schema, table, migration, API, UI, or code is specified here; only the
  direction that each canonical transition above is its own consistency boundary
  with guardable invariants.

## Alternatives Considered

- **Atomic WO + stock-out transaction:** simpler consistency; rejected — it
  contradicts the explicit business rule that the flow need not be atomic.
- **Reservation mechanism to bridge the gap:** rejected — CD-10 Q11 excludes
  reservation; inventing it would be a silent business-rule change.
- **Eventual merge of dangling halves by background auto-resolution:** rejected —
  auto-resolution would silently decide business facts; attention-only surfacing
  is the proposed behavior.

## Trade-offs

Paired records tolerate ordering gaps and offline/field realities at the cost of
a reconciliation surface that must be monitored (as attention, not blocking).

## Business Rules Preserved

Non-atomic material flow; no reservation; partial receiving/conversion semantics;
PO immutability after Issued; fulfillment never mutates stock. WO lifecycle
terms per CD-11 canonical baseline only (CD11-001; superseded terms in CD-11 §30
— `ASSIGNED`, WO-status `COMPLETED`, WO-status `ON PROCESS`, `CLOSE_WO`,
`CANCEL_*` states — MUST NOT appear as WO states in any transition matrix
derived from this direction).

## Dependencies / Deferred Decisions

TADR-05 (database strategy), TADR-06 (workspace scoping of each boundary).
No deferred business detail blocks this proposal.

## Security Impact

Transition guards are authorization-adjacent: state changes require the acting
role's authority (enforced with TADR-14).

## Audit / Traceability Impact

Every boundary crossing is a trail event (actor, timestamp, before/after,
reason); mutual references make WO ↔ inventory pairs jointly auditable.

## Operational Impact

Reconciliation attention views must be operable without becoming blockers;
no timers or escalation invented.

## Reversibility

Medium: boundary placement is cheap to adjust pre-implementation.

## Open Questions

- Reconciliation surfacing rules detail (Outstanding surfacing gate — business-owned).

## Approval Boundary

Requires Human approval of the boundary placement. Authorizes no code, schema,
migration, or Programmer handoff.
