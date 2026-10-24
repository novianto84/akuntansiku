# TADR-12 — Read Models / Projections

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

Which information is transactional source vs. derived projection across Unit
history, Customer view, QR view, Outstanding, Technician history, Sales/Purchase
views, and Inventory history — and which freshness strategy (live query,
materialized projection, event-driven projection, hybrid) fits each, without
duplicating operational history?

## Authoritative Inputs

- CD-11 §§2, 10, 17, 18, 20, 21, 22, 28, 30 (WO lifecycle/closure; visit model;
  evidence eligibility; report model/finalization/Final Conclusion; service
  history views; customer-safe visibility/publication; QR scope; correction
  records; supersession/purge list) — SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF
  — CD-11 Business Finalization, CD11-001…CD11-029; report/publication decisions
  CD11-018, CD11-020, CD11-021).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21) (technical criteria only): hybrid — live
queries for internal/operational views; materialized reviewer-gated snapshots for
Customer and QR views (evidentiary stability: what the customer saw is fixed).
Every projected row carries its source link plus freshness/publication metadata.
Snapshot vs. live as a business expectation is NOT decided here (customer
publication model gate).

> **Subsequent HBA business decision (2026-09-30) — HBA D-01A = RETAIN.**
> The business expectation referenced above has since been established by the Human
> Business Authority: previously presented customer-facing content remains available as the
> historical record of what was presented, and the current authoritative condition remains
> distinguishable from that record. This note does not alter the approved technical direction
> above; the hybrid/materialized-snapshot direction and "what the customer saw is fixed" remain
> as approved. Refresh, propagation, cache, replication, drift monitoring, and serving mechanism
> remain architectural. See `docs/90-AUDIT/TADR-12-AMENDMENT-D01A-RETAIN.md`.

CD-11 Direction Alignment (2026-09-22; business baseline SIGNED-OFF / LOCKED /
CLOSED — no business rule changed here; no API contract or UI specification is
created). The hybrid direction above is retained, constrained against the
canonical baseline as follows (direction only):

- Source model (CD11-017, CD11-019, CD11-020; CD-11 §§10, 18): exactly
  `1 WO → 1 Report → N Visits`. The Report is Hybrid Summary + Visit History
  (no manual duplication of Visit data by Technician). Visit is the operational
  source; Report is the consolidation. Projection design MUST preserve this
  source chain and MUST NOT treat Report and Visit as independent sources.
- Eligibility-gated customer projection (CD11-014, CD11-020, CD11-021; CD-11
  §§17, 18, 21): customer-facing projections serve ONLY eligible data —
  reviewer-curated, approved/eligible Evidence (non-eligible Evidence stays
  stored internal-only per permission), and Report content that is official/live
  per governance. The customer sees the latest official/live information per
  governance, never work-in-progress internals.
- Customer visibility is NEVER Technician-determined (CD-11 §§17, 21):
  publication control is `photo_type + approval_state + policy_version` plus
  reviewer (Manager/Admin) curation; Technician has no visibility choice. The
  projection layer MUST enforce this structurally, not as UI convention.
- Customer-access eligibility conjunction (CD11-018, CD11-020, CD11-021; CD-11
  §§2, 18, 21, 22): customer access remains subject to `CLOSED` (WO closed via
  approval) + `FINAL` (Report FINAL occurs ONLY on `WO CLOSED`; Visit
  COMPLETED / outcome DONE / WAITING APPROVAL / CORRECTION_REQUIRED never
  finalize) + Verified PIC + company scope + policy + eligibility. The
  projection direction MUST treat all of these as gating inputs, none of which
  is decided or waived here.
- No-download requirement (CD11-021) remains in force as a business-locked
  constraint the serving direction MUST honor (mechanism deferred to IS
  Specification; nothing is specified here).
- Internal-only exclusion (CD-11 §21): internal notes, correction/cancellation/
  administrative reasons, acquisition price, vendor intelligence, and other
  internal/commercial information MUST NEVER reach the customer view. The
  customer-safe allowlist plus reviewer curation is the enforcement basis
  (with TADR-11 for file serving, TADR-14 for visibility tiers).

## Alternatives Considered

- **Live query everywhere:** always fresh, simplest; risks post-publication
  mutation visibility and load on the transactional store.
- **Materialized everywhere:** stable and fast; refresh-policy burden and
  staleness risk for operational views.
- **Event-driven everywhere:** lowest lag; highest complexity for the value at
  this stage.

## Trade-offs

Hybrid gives freshness where it matters and stability where evidence matters, at
the cost of a refresh policy plus drift/staleness monitoring for snapshots.

## Business Rules Preserved

One operational history; 1 WO → 1 Report → N Visits source chain; per-view
scoping (each customer entry stays unit-tied; QR strictly one Unit);
Outstanding as monitoring overlay, never lifecycle; eligibility-gated
customer projection (CLOSED + FINAL + Verified PIC + company scope + policy +
eligibility); Technician never determines visibility; no-download requirement
honored; reviewer curation before publication; no internal-only leakage.

## Dependencies / Deferred Decisions

Customer publication model: the **business expectation is RESOLVED by HBA D-01A = RETAIN**
(previously presented customer-facing content remains available as the historical record of what
was presented; the current authoritative condition remains distinguishable). The publication/serving
**mechanism** (snapshot materialization, refresh, cache, replication, drift monitoring) remains an
architecture decision. No longer partly blocking on the business-expectation aspect. Business Access
Model (LOCKED): the QR projection serves
UNIT SCOPE to any authenticated user (unit identity, owner company, address,
work/material history) and COMPANY SCOPE aggregate only to a verified PIC of
that Company; PIC details/lists are visible only within Company Scope per
customer-safe visibility; no price of any kind (material, purchase, acquisition,
HPP, margin, accounting value) appears in any external projection. Kept separate
from TADR-11 because this record governs derived views while TADR-11 governs
evidence custody.

## Security Impact

Projection layer enforces the customer-safe allowlist and unit scoping;
cross-unit leakage prevention is structural (unit-rooted queries).

## Audit / Traceability Impact

Source-links plus publication events make every published row reproducible;
snapshot identity supports "what was shown when" evidence.

## Operational Impact

Refresh cadence and staleness monitoring are operable concerns; no cadence or
threshold invented here.

## Reversibility

Medium: freshness strategy can evolve; published snapshot history persists.

## Open Questions

- Snapshot refresh cadence and staleness policy (**architecture/mechanism**; the business expectation is resolved — HBA D-01A = RETAIN).
- Event-driven upgrade path (future, if scale demands).

## Approval Boundary

Requires Human approval of the hybrid direction. Authorizes no projection
infrastructure, code, schema, migration, or Programmer handoff.
