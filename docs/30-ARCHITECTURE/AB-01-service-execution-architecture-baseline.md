# AB-01 — Service Execution Architecture Baseline

```text
Document: AB-01 Service Execution Architecture Baseline
Version: 1.0
Status: APPROVED / CANONICAL — BUSINESS AUTHORITY APPROVAL
Approval: Business Authority administrative/governance approval of the v1.0 DRAFT baseline as reported (30/30 self-check passed; no contradiction; no business decision changed). Approval is status/governance only; no content revision.
Sources: CD-11 (SIGNED-OFF/LOCKED/CLOSED); BD-SR-001/002/003/004/005/010/011 (LOCKED V1);
  BD-SRWO-001 (LOCKED V1); BD-WORKMODEL-001 (APPROVED/CANONICAL); BD-WORKTYPE-001 Rev.A;
  IS-02 Service Execution Specification; IS-02 Technical Decomposition;
  AR-01 Architecture Review (ARCHITECTURE READY FOR BASELINE); TADR-01…18 (APPROVED);
  IS-00; IS-01 (where authoritative); Decision Register (authority index).
Review reference: AR-01 (response-track review, READ ONLY, no files modified).
```

> Consolidation only — no redesign, no new business decision, no implementation content
> (no schema, tables, migrations, API, payloads, code, UI, infra, framework, queues, cache).
> Precedence: newer LOCKED/APPROVED → earlier LOCKED/APPROVED → approved technical
> clarification → historical material (traceability only). Where a source below says OPEN,
> AB-01 records OPEN.

---

## A. Architecture Status

AB-01 v1.0 consolidates the reviewed service-execution architecture into the single
architectural source of truth for subsequent specification and implementation work. Status:
**APPROVED / CANONICAL — BUSINESS AUTHORITY APPROVAL** (see the header block and §T). "Ready
for baseline" (AR-01) was the review verdict, not the approval. No contradiction between
sources was found during consolidation (§V).

*Internal status-label alignment 2026-09-25 (E4):* the §A status label and the footer are
aligned to the header/registry treatment (APPROVED / CANONICAL). The header's approval
narrative — which describes the approved v1.0 draft — is historical and retained unchanged.
No content, rule, or status meaning was modified; see
`docs/90-AUDIT/UI-BASELINE-APPROVAL-AND-RECONCILIATION-RECORD.md`.

## B. Domain Boundary

Canonical domain objects: SR (request/history) · WO (execution + lifecycle owner) · JOB
(single scope concept) · Visit (occurrence under WO) · Report (per-WO consolidation) ·
customer-safe projection (derived plane) · audit/event records (append-only observer).
Technical-support records (per decomposition §3): Assignment event log; audit/event entries.
Future/deferred: catalogue/taxonomy/mechanism placeholders (see §O). Support records are
never business entities. One JOB concept only: Issued/Additional/Initial Job language stays
terminology for the same JOB/SCOPE — no `issued_jobs`, `additional_jobs`, or second lifecycle.

## C. Ownership Architecture

- SR owns SR interaction lifecycle. WO owns WO lifecycle. JOB establishment/state is owned
  through the WO. Visit owns Visit execution records. **Report is the canonical business
  consolidation of execution evidence but is derived in storage from Visits** (§K).
  Customer-safe projection is derived from canonical internal data. Audit is append-only
  observation and never a business-state owner.
- Principle: **one business fact has one authoritative writer.** No second writer for convenience.

## D. Dependency Direction

Approved chains: **SR → WO → JOB** and **WO → Visit → Report → Customer-Safe Projection**;
audit observes. Read/reference dependency is not ownership; no reverse-write dependency is
permitted. The graph is acyclic once ownership and read-reference are distinguished (AR-01 §4:
WO↔Report approval-read, JOB↔Visit state-event duality, and sibling independence documented).

## E. Lifecycle Ownership

- SR interaction (`OPEN` / `CLOSED`; only `CLOSED` terminal; no V1 reopen).
- WO (DRAFT→OPEN→IN_PROGRESS→WAITING APPROVAL→CLOSED + terminal CANCELLED; no ASSIGNED state;
  COMPLETED/ON PROCESS never WO states; no CLOSE_WO action).
- Visit (OPEN→COMPLETED, independent; COMPLETED finalizes nothing; INITIAL/ON PROCESS only).
- Report readiness (NON-FINAL→FINAL iff WO CLOSED; refresh-from-Visits; no per-correction versions).
- Correction/reopen (WAITING-APPROVAL loop + single audited direct-edit sideroute; CLOSED-only
  REOPEN same identity; RE-CREATE with `CREATED_FROM`; numbered unlimited cycles).
- `CORRECTION_REQUIRED` is a correction/review loop marker, not a lifecycle state. **Completing a
  Visit never closes the WO.**

## F. SR → WO Boundary (O-11 / BD-SR-011, reconciled to final Human decision)

Ordinary `CREATE_WO` with an SR source reference creates a new independent WO; it is
not a special conversion action and never transforms/copies the SR. Only existing
`CREATE_WO` holders may create it; SR must be `OPEN`; no automatic JOB (actor
establishes each JOB explicitly). WO formation, source reference/lineage, and audit
remain within the approved atomic/failure boundary; no SR status changes. A saved
DRAFT is not an official Related WO and is outside official formation. If an active
source-associated DRAFT exists, do not create another active DRAFT; route to it.
Continue Draft is creator-only under CD-11 §DRAFT. The official Related WO appears
when the WO reaches `OPEN`. Preserve the existing V1 at-most-one-official-WO-per-SR
duplicate guard; attempts resolve to the existing official WO. The SR remains `OPEN`
and editable under its existing permission while the WO exists; lineage is optional
`source_sr_id` (NULL = direct WO). Identical post-creation lifecycle for direct WOs;
append-only audit; no new approval entity/layer.

## G. JOB / Visit / Report Separation

JOB defines work/scope (1 WO : N JOBs; 1 JOB : exactly 1 WO). Visit records occurrences (1 WO : N
Visits; completion finalizes nothing). Report consolidates (≤1 per WO; never per Visit; never a
second JOB). No hidden additional-job object exists anywhere in this baseline.

## H. Report Clarification (AR-01 Reconciliation 1, carried forward)

**Report is canonical in business meaning, but derived in storage:** content derived/recomputed
from authoritative Visit data; no second independent store owning the same facts; no independent
direct-write path contradicting Visit-owned evidence. Documentation clarification, not a decision.

## I. WO ↔ Report Approval (AR-01 Reconciliation 2, carried forward)

**Approval is a WO-domain action consuming Report content as a read dependency.** Report never owns
WO approval; future design must never invert this arrow.

## J. Closure / Correction / Reopen

Execution completion, report readiness, approval, closure, correction, and reopen are six distinct
phases (IS-02 §13). Correction never duplicates Report; lineage stays on the WO with refresh from
authoritative evidence; reopen is CLOSED-only; numbering/lineage deterministic. No new correction
entities.

## K. Work Model × Service Type

Distinct classification axes whose combination determines execution semantics where specified:
Work Model ∈ {SERVICE, INSPEKSI, EMERGENCY TROUBLESHOOT} × Service Type ∈ {six CD-11 §16 types}.
**No third workflow/template axis.** Historical labels FULL_SERVICE / INSPECTION_ONLY / EMERGENCY
have zero architectural representation (BD-WORKMODEL-001 §8; AR-01 §8).

## L. Authorization Architecture

CREATE_WO · JOB establishment · assignment (ASSIGN_WO) · Visit execution · submission ·
approval/closure (Manager/Admin, never technician, never own WO) · correction/reopen/cancel ·
evidence review · acknowledgement (non-gating presence record). Guards co-located with owning
domains; no new roles/entities; authorization never bypasses another domain's state guard.

## M. Customer Data Isolation

Two planes: canonical/internal (authoritative everything) vs customer-safe projection (allowlisted,
reviewer-curated, priceless, scoped). Unit-scoped public QR (CONTROLLED ACCESS, no anonymous);
company-scoped verified-PIC portal; no cross-company grant; technician never chooses visibility;
internal notes/prices/vendor intelligence never cross planes. Serving mechanism deferred to IS-06.

## N. Audit Architecture

Append-only observer; never a state owner; never mutates. The technical decomposition
(§24: WO creation with SR source reference, duplicate attempt, JOB establishment,
assignment, check-in/out, HM, evidence/opt-out, submission, approval, correction, reopen,
closure, cancellation, acknowledgement, publication-approval changes) remains authoritative
with actor, server timestamp, object, reason, and before/after where canonical. No separate
SR status-change event is caused by WO creation. No second audit subsystem.

## O. Invariants (architecture constraints, not suggestions)

1. One SR → ≤1 official WO (V1). 2. Only CLOSED SR is immutable. 3. `source_sr_id = NULL` = direct WO.
4. No official WO without formation guards. 5. WO formation + source reference/lineage + audit are atomic; SR status remains OPEN. 6. DRAFT is not an official Related WO; an active DRAFT cannot be duplicated and only its creator may continue it. 7. No auto SR→JOB. 8. JOB ∈ exactly 1 WO. 9. Visit ∈ exactly 1 WO. 10. Report ∈ exactly 1 WO. 11. ≤1 Report/WO.
12. WO → N Visits. 13. Visit completion ⇏ closure. 14. Approval before CLOSED. 15. No self-close.
16. Ack ⇏ closure. 17. Priceless projection. 18. No technician-chosen visibility. 19. Unit-scoped QR.
20. Identical post-creation lifecycle (direct ≡ SR-origin). 21. No template dimension.

## P. Consistency Boundaries

SR→WO atomicity · duplicate protection · JOB establishment · approval→closure consequence ·
correction/reopen lineage · cancellation chain · acknowledgement decoupling ·
evidence approval/visibility gating. No additional transaction boundaries for convenience.

## Q. OPEN / DEFERRED Items (isolated; unsolved)

| ID | Description | Arch. impact | Status | Blocks impl.? | Source |
|---|---|---|---|---|---|
| IS02-O01 | Checklist/Test-Run contents + N/A taxonomy | Abstract placeholders | OPEN | No | F-1/OQ-04 |
| IS02-O02 | Evidence categories beyond floor | Open dimension | OPEN | No | OQ-05 |
| IS02-O03 | Subtype fields | Unfilled extension points | OPEN | No | OQ-03 |
| IS02-O04 | Ack alternative types | Placeholder reference | OPEN | No | OQ-16 |
| IS02-O05 | Publication mechanism/freshness/no-download | Serving absent by design | DEFERRED | No | IS-06 |
| IS02-O06 | Reminder automation | No scheduler objects | DEFERRED | No | OQ-07 |
| IS02-O07 | Emergency retroactive convention | No precedence logic | OPEN | No | OQ-08 |
| IS02-O08 | Minor/substantive correction | No sub-typing | OPEN | No | OQ-09 |
| IS02-O09 | Outstanding surfacing | No overlay | DEFERRED | No | OQ-06 |
| IS02-O10/11 | Purchasing/deployment details | Out of scope | DEFERRED | No | OQ-10…14 |
| IS02-O12 | SR representation mechanics | Consumed, unmodelled | DEFERRED | No | IS-04+ |

## R. Traceability (Decision → Specification → Decomposition → Baseline)

O-11 boundary → BD-SR-011 → IS-02 §§3,18 → Decomp §§6,20–24 → AB-01 §F. JOB concept →
BD-WORKTYPE-001 → IS-02 §6 → Decomp §7 → AB-01 §§B,G. WO/Visit/Report → CD-11
§§2,10,18 → IS-02 §§3,5,12 → Decomp §§5,8,9 → AB-01 §§E,G,H. Work Model × Service Type →
BD-WORKMODEL-001 + CD-11 §16 → IS-02 §2 → Decomp §10 → AB-01 §K. Lifecycle ownership →
CD-11 + TADR-04 → IS-02 §18 → Decomp §20 → AB-01 §E. Correction/reopen → CD-11 §28 +
TADR-09 → IS-02 §14 → Decomp §16 → AB-01 §J. Authorization → CD-11 + BD-SR-005 →
IS-02 guards → Decomp §23 → AB-01 §L. Projection → CD-11 §§20–22 + access decisions →
IS-02 §16 → Decomp §19 → AB-01 §M. Audit → CD-11 §28 + TADR-08 → IS-02 §19 → Decomp
§24 → AB-01 §N. Invariants → Decomp §21 → AB-01 §O.

## S. Change Control

Post-approval, implementation documents MUST reference AB-01 and MUST NOT: redefine business
semantics; alter lifecycle ownership; introduce a second writer; introduce a new JOB concept;
bypass customer-data isolation; or solve OPEN/DEFERRED items without the owning governance
decision. Architectural changes route through the existing decision/change-control process (no new
mechanism invented here).

## T. Self-Check Result

Domain: no overlap ✅ · one JOB ✅ · Report wording reconciled ✅. Ownership: single writer ✅ ·
no reverse-write ✅ · audit observer-only ✅. Lifecycle: SR/WO/Visit/readiness/correction all
preserved ✅ · Visit-completion⇏closure ✅. Dependency: chains preserved ✅ · projection derived ✅ ·
approval not inverted ✅. Classification: Work Model + Service Type ✅ · no third axis ✅.
Customer access: QR unit-scoped ✅ · portal company-scoped ✅ · no cross-grant ✅ · projection
isolated ✅ · notes/price protected ✅. Governance: no new decision ✅ · OPEN/DEFERRED intact ✅ ·
no implementation detail ✅ · precedence respected ✅ · traceability included ✅. **30/30 pass.
No contradiction found between sources.**

---

*End of AB-01 v1.0 — APPROVED / CANONICAL.*
