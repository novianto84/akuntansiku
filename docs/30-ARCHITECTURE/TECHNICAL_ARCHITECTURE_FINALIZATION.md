# Technical Architecture Finalization Report — Brainstrom CRM

```text
TECHNICAL ARCHITECTURE STATUS: APPROVED / CANONICAL
HUMAN APPROVAL: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
IMPLEMENTATION AUTHORIZATION: NO
SCHEMA FINALIZATION: NO
MIGRATION AUTHORIZATION: NO
CODING AUTHORIZATION: NO
```

This document is a technical architecture proposal. It does not approve architecture,
schema, implementation, programmer handoff, or migration, and it does not change any
business decision. Traceability chain preserved:

```text
Human Decision
    ↓
Canonical CD
    ↓
Technical Requirement
    ↓
TADR (PROPOSED)
```

Downstream artifacts (`Implementation Specification`, `Implementation`, `Migration`,
`Test`, `Audit Result`) are not created here because they are not authorized.

> **Status clarification added 2026-09-26 (documentation amendment).** This report's §1 records `CD-11` as
> `SIGNED-OFF / LOCKED / CLOSED` (BA SIGN-OFF — CD-11 Business Finalization, CD11-001…CD11-029), while its
> §"Changed" line and the `HUMAN APPROVAL GATE` summary retain the earlier classification
> `HUMAN-ACCEPTED` / "Treated As LOCKED: NO". The earlier lines describe the state this report worked from and
> are **superseded for current governance interpretation on that point only**: `CD-11` is `SIGNED-OFF / LOCKED /
> CLOSED` per `CD-11` §32, `ARCHITECTURE_LOCK.md`, `DECISION_REGISTER.md` (row `CD-11`) and
> `AI_CONTEXT_INDEX.md` §6. No date for the status raise is recorded in this repository. All other report
> content is preserved unchanged.

---

## 1. Executive Status

- **Current business baseline:** CD-01 = FINAL / LOCKED; CD-03 through CD-10 = LOCKED;
  CD-11 = SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF — CD-11 Business Finalization,
  CD11-001…CD11-029); CD-02 = DEFERRED / UNVERIFIED (no canonical
  document present; not reconstructed).
- **Governance context obeyed:** `AI_CONTEXT_INDEX.md`, `AI_OPERATING_RULES.md`,
  `ARCHITECTURE_LOCK.md`, `DECISION_REGISTER.md`.
- **Technical architecture status:** APPROVED / CANONICAL (18 TADRs, all APPROVED
  by HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21).
- **Implementation authorization:** NO. No coding, schema, migration, API, UI,
  deployment change, or Programmer handoff is authorized by this document.

---

## 2. Revalidation vs Prior Preparation

The prior Technical Architecture Preparation work exists only as conversational content,
not as a persisted repository artifact (see GAP-F1). It was revalidated against the
canonical baseline rather than reproduced:

- **Retained:** canonical Company/roles/Contact; WO lifecycle with 1 WO = 1 Unit and
  the correction path; INTERIM/CONTINUATION/FINAL as report classifications and
  Outstanding as monitoring; single-write operational records with derived projections;
  hybrid audit direction (version records + append-only governance trail).
- **Changed:** CD-11-derived constraints are classified HUMAN-ACCEPTED, never LOCKED;
  the TADR set is re-derived from the 18 mandated decision areas (count not presupposed);
  QR mechanism preference softened to alternatives pending access-policy resolution.
- **Rejected:** use of `BD-1…BD-7` / `DD-01…DD-09` as canonical identifiers (see GAP-F2);
  descriptive gate names are used instead.
- **Unresolved:** identity-link business semantics; QR access policy; customer publication
  model; reminder/automation policy; emergency retroactive convention; deployment
  operational context; plus content-deferred items (thresholds, checklist contents, N/A
  taxonomy, acknowledgement evidence, Outstanding surfacing).

The preparation work is not treated as approved architecture.

---

## 3. Architecture Overview

### Domain / Module Map

- **Identity** (Company + Contact/PIC + CompanyRole links) — global/shared.
- **Asset** (Unit + Component subtype structures) — CRM-owned/shared registry.
- **Service** (ServiceRequest intake, WO, Assignment, ServiceExecution, findings,
  evidence, checklist, test/run, material usage, component replacement, review,
  correction) — workspace-owned, WO-rooted.
- **Commercial / Sales** (Quotation, SalesOrder, Fulfillment) — workspace-owned;
  fulfillment does not mutate inventory.
- **Purchasing** (PR, PO, Receiving, acquisition-event capture) — workspace-owned
  transactions; offer data is reference only.
- **Inventory** (ItemMaster shared identity; per-workspace balances and movements;
  adjustment/opname) — quantity-only.
- **Price Intelligence** (VendorOffer + AcquisitionReference + provenance/version
  history) — shared intelligence with role-based visibility overlay.
- **Visibility / Projection** (Customer/QR/Unit/Technician/Outstanding projections +
  reviewer curation + publication state) — derived only.
- **Platform** (workspace context, per-workspace numbering, templates, enforcement
  points, background jobs, file serving, observability) — cross-cutting, policy-free.

### Major Boundaries

CRM operational transactions vs. Inventory operational records vs. external
Accounting/Accurate authority; internal vs. customer-safe information;
workspace-owned transactions vs. shared masters/intelligence.

### Source-of-Truth Model

WO/execution records own service facts; Unit owns asset parenthood; Inventory owns
quantity; Company owns identity; Reviewer owns curation. All views are derived.

### Integration Boundary

```text
CRM
 ↕
Integration Boundary
 ↕
Accurate
```

No API contract, field mapping, synchronization design, or migration plan is made here.

---

## 4. Aggregate / Domain Model

Candidate aggregates and ownership boundaries. No implementation schema is produced.

| Aggregate | Ownership | Key invariant | Source-of-truth role |
|---|---|---|---|
| Company | Identity | one canonical identity; no role-duplicate masters | identity |
| Contact / CompanyRole | under Company identity | never merged into Company fields | relationship |
| Identity-Link | under Contact/Company | per-company state; no cross-company grant | access-link state (business semantics LOCKED; formal CD documentation pending) |
| Unit (+ Components) | Asset (CRM-owned/shared) | asset parenthood for WO history | asset registry |
| WorkOrder | Service (workspace-owned) | at most 1 Unit; exactly 1 before CLOSED (CD-11 §5) | operational service fact |
| Execution artifacts (findings/HM/evidence/checklist/test/material/replacement) | WO | condition-driven requiredness | execution facts |
| Review / Correction | governance over WO | no CLOSED without Manager/Admin review; no overwrite | governance trail |
| MaterialUsage | WO | operational record; reference-only to inventory | WO consumption fact |
| InventoryOperation | Inventory (workspace-owned) | quantity-only movement authority | quantity authority |
| Quotation → SO → Fulfillment | workspace commercial | partial semantics; no terminal REVOKED | commercial facts |
| PR → PO → Receiving | workspace commercial | PO immutable after Issued; per-event receiving | commercial facts |
| VendorOffer / AcquisitionReference | shared intelligence | immutable versions; usage pinned to version used | price reference |
| Projections (Unit/Customer/QR/Technician/Outstanding) | none (derived) | traceable to source; publication-gated | derived only |

---

## 5. Transaction Architecture

- **Consistency boundaries** are per lifecycle transition. Invalid transitions are
  rejected (e.g. OPEN → CLOSED bypassing review, any transition into or out of
  CANCELLED except OPEN / IN_PROGRESS → CANCELLED, CLOSED → CANCELLED,
  CANCELLED → REOPEN, direct edit of CLOSED). Superseded WO states (`ASSIGNED`,
  WO-status `COMPLETED`, WO-status `ON PROCESS`, `CLOSE_WO`) and superseded
  cancel states (`CANCEL_PENDING_APPROVAL` / `CANCEL_*`) are not valid transition
  endpoints (CD-11 §§2, 9, 30; TADR-04).
- **Atomicity / non-atomicity:** the WO ↔ inventory chain is deliberately non-atomic
  per business rule. WO MaterialUsage records and InventoryOperation movements are
  recorded independently with mutual references and non-blocking reconciliation
  visibility for dangling halves. No reservation mechanism is introduced.
- **Correction / revision:** governed correction only. WO correction follows the
  WAITING APPROVAL correction loop (REQUEST CORRECTION → CORRECTION_REQUIRED →
  resubmission) pre-CLOSED and REOPEN (CLOSED → IN_PROGRESS, same number/Report)
  post-CLOSED with numbered unlimited cycles; RE-CREATE yields a new WO with
  `CREATED_FROM` lineage (CD-11 §§2, 28; TADR-09). The WAITING APPROVAL direct-EDIT
  sideroute (mandatory reason + full audit linkage) is the only business-locked
  direct-edit path. Commercial and price records use
  version/revision chains. Receiving corrections use revision plus compensating
  movement, never silent edit.
- **Reconciliation:** partial conversions, partial receiving, and outstanding
  remainders are computed additively; nothing auto-completes.

---

## 6. Security Architecture

- **Authentication:** internal local authentication plus external identity-provider
  linking. Account lifecycle is bound to the identity-link, not to the Contact itself.
- **Identity linking:** per-company VERIFIED / PENDING / REVOKED states with no
  cross-company grant. Business semantics are LOCKED (formal CD documentation
  pending); the mechanism proposal (TADR-13) must not change business meaning.
- **Authorization:** action-level checks plus workspace-scope guard, kept separate
  from business visibility policy. Role ≠ visibility policy. No business permission
  matrix is locked here.
- **Workspace isolation:** application-level guards as primary enforcement with a
  negative-test acceptance strategy; database-level defense-in-depth remains an
  unevaluated option.
- **Customer / external visibility:** mediated, projection-scoped access only.
  Internal file paths, internal-only fields, acquisition prices, vendor intelligence,
  and internal commercial information are never exposed externally.

---

## 7. Data / Projection Architecture

- **Operational source records:** WO/execution records, commercial documents,
  inventory movements, price-intelligence versions, manual reminder records.
- **Read models:** Unit history, Customer view, QR view, Technician history,
  Outstanding, Sales/Purchase views, Inventory history — all DERIVED.
- **Materialized projections:** candidate for customer-facing and QR views
  (evidentiary stability); live queries for internal/operational views.
- **Customer-safe publication:** allowlist from the locked exclusion list plus
  reviewer curation gate. The business expectation is resolved (**HBA D-01A = RETAIN**:
  previously presented content remains available as the historical record); the
  snapshot/serving **mechanism** remains an architecture matter.
- **QR-scoped access:** resolution rooted at exactly one Unit; cross-unit access is
  structurally impossible, not merely UI-filtered.

---

## 8. File / Evidence Architecture

- **Evidence ownership:** WO/execution context owns evidence instances.
- **Storage abstraction:** content-addressed internal store; internal paths never
  exposed to external users.
- **Immutable originals:** post-completion files are never overwritten; replacement
  creates a new file plus linkage. Derivatives never mutate originals.
- **Review / publication states:** internal-only vs. approved-for-customer, gated by
  reviewer curation; QR serving additionally unit-bound.
- **Mediated serving:** all external file access passes through scope-bound mediation.

---

## 9. Automation Architecture

- **Background jobs (candidate needs):** projection/snapshot refresh, Outstanding-view
  refresh, photo processing, notification delivery, scheduled maintenance/health.
- **Reminders:** manual reminder by Admin/Manager/Sales is the business baseline.
  Automatic reminder generation and intervals are not locked.
- **Notifications:** delivery mechanism is a proposal only; no automatic behavior is
  enabled by architecture.
- **Disabled-by-default behavior:** every job whose business policy is unresolved
  exists only as a disabled candidate behind an explicit Human policy flag. No
  numeric SLA, timer, escalation, or auto-blocking is invented.

---

## 10. Deployment / Operations

- **Candidate deployment topology:** managed/shared hosting, VPS, self-hosted,
  hybrid, containerized deployment — compared on security, maintainability, backup,
  availability, cost, future scale, integration, and customer access. Nothing is
  selected as final; deployment operational context remains an unresolved gate and
  cost/operations capacity is Human input. Nothing is deployed by this document.
- **Operational assumptions:** one platform, one database (business-locked);
  workspace-scoped operations; reviewer-gated publication.
- **Observability:** application logs, audit logs, security events, background-job
  status, integration failures, health checks, metrics, alerts, end-to-end
  traceability from record to projection to published view. Log-leakage prohibition:
  no acquisition prices, vendor intelligence, internal notes, tokens, or secrets
  in logs.
- **Backup / recovery (architectural level):** encrypted backups, workspace-scoped
  restores with no cross-workspace mixing, restore verification cadence deferred to
  implementation planning. No backup system is implemented here.

---

## 11. TADR Register

All 18 TADRs are PROPOSED with Human Approval REQUIRED and Implementation
Authorization NO. Full records live in `docs/30-ARCHITECTURE/TADR/`.

| TADR | Title | Blocking status |
|---|---|---|
| TADR-01 | Application / Module Boundaries | Non-blocking |
| TADR-02 | Domain / Aggregate Boundaries | Non-blocking |
| TADR-03 | Component Subtype Structure | Non-blocking (placeholder shapes) |
| TADR-04 | Transaction Boundaries | Non-blocking |
| TADR-05 | Database Strategy | Non-blocking |
| TADR-06 | Workspace Isolation Enforcement | Non-blocking |
| TADR-07 | Source-of-Truth Ownership | Non-blocking |
| TADR-08 | Audit / Versioning Mechanism | Non-blocking |
| TADR-09 | Correction / Revision Mechanism | Non-blocking |
| TADR-10 | Material vs Inventory Separation | Non-blocking |
| TADR-11 | File / Photo Architecture | Partly blocking (serving/evidence mechanism; business expectation resolved — HBA D-01A = RETAIN) |
| TADR-12 | Read Models / Projections | Non-blocking (business expectation resolved — HBA D-01A = RETAIN; serving/refresh mechanism remains architectural) |
| TADR-13 | Authentication / Identity-Link | READY FOR HUMAN ARCHITECTURE APPROVAL (gate resolved; status PROPOSED) |
| TADR-14 | Authorization / Visibility Enforcement | Partly blocking (business permission content) |
| TADR-15 | Background Jobs / Notifications | Partly blocking (reminder/automation policy) |
| TADR-16 | QR Mechanism | READY FOR HUMAN ARCHITECTURE APPROVAL (gate resolved; status PROPOSED) |
| TADR-17 | Deployment Topology | Non-blocking (proposal; ops context unresolved) |
| TADR-18 | Observability / Traceability | Non-blocking |

TADR-08 and TADR-09 are kept separate (mechanism vs. governed flow). TADR-11 and
TADR-12 are kept separate (evidence custody vs. derived views). No TADR is added,
removed, merged, or split.

---

## 12. Deferred / Unresolved Register

### Blocking

Resolved by LOCKED HUMAN DECISIONS (formal CD documentation pending):

- **Identity-link reconciliation** (impacts TADR-13). RESOLVED: Google-only
  external sign-up/sign-in; sign-up grants no access; application-based PIC
  registration yielding PENDING; Manager/Admin approval; no email-match
  requirement; Google Identity ≠ Contact/PIC ≠ Verified PIC Link ≠ Company
  Access; no cross-company grant. TADR-13 assessed READY FOR HUMAN
  ARCHITECTURE APPROVAL.
- **QR access policy** (impacts TADR-16). RESOLVED as CONTROLLED ACCESS:
  SCAN → SIGN UP/SIGN IN → CHECK ACCESS → UNIT DATA; no anonymous access;
  permanent unit-scoped QR; customer-safe visibility mandatory. TADR-16
  assessed READY FOR HUMAN ARCHITECTURE APPROVAL.
- **Business Access Model (Unit Scope / Company Scope)** (impacts TADR-12, 13,
  14, 16). RESOLVED by LOCKED HUMAN DECISION: no data without Google
  sign-up/sign-in; QR on Unit/Invoice/Surat Jalan resolves to the same Unit;
  authenticated non-PIC users receive UNIT SCOPE only; verified PIC receives
  COMPANY SCOPE; explicit customer-portal no-price rule; invariants LOGIN ≠
  COMPANY ACCESS, QR ≠ COMPANY ACCESS, Verified PIC = basis of Company Access.

### Partly Blocking

- **Customer publication model** (impacts TADR-11, TADR-12). Includes snapshot vs.
  live expectation and any technical publication/permission mechanism.
- **Reminder / automation policy** (impacts TADR-15). Includes automatic generation,
  intervals, and surfacing behavior.

### Non-Blocking but Unresolved

- Emergency retroactive timestamp convention
- Deployment operational context
- Minor/Major threshold
- Checklist contents
- N/A taxonomy/examples
- Acknowledgement alternative evidence
- Outstanding surfacing rules

None of the above is silently resolved. Where possible the architecture uses
content-agnostic containers and disabled-by-default behavior.

### Governance Gaps (preserved findings)

- **GAP-F1:** the prior Technical Architecture Preparation Report was not persisted
  as a repository artifact. Classification: `DOCUMENTATION / TRACEABILITY GAP`. It is
  not a business architecture blocker. No missing preparation document is fabricated.
- **GAP-F2:** historical/informal `BD-1…BD-7` / `DD-01…DD-09` are not canonical
  identifiers. Descriptive gate names are used. No new BD/DD identifiers are created
  to replace them. The underlying unresolved gates remain valid where documented.

---

## 13. Traceability Matrix

`CD → Technical Requirement → TADR`. Every row ends at a PROPOSED TADR; downstream
artifacts are not authorized.

| Canonical source | Technical requirement | TADR |
|---|---|---|
| CD-01 (scope/workstreams) | module seams; platform capabilities | TADR-01, TADR-17, TADR-18 |
| CD-03 (Company/roles/Contact) | identity/role/contact aggregates | TADR-02, TADR-07 |
| CD-04 (acquisition boundary) | reference-only price semantics | TADR-10 |
| CD-05 (sales/quotation) | partial conversion; CLOSED model; non-mutating fulfillment | TADR-02, TADR-04, TADR-09 |
| CD-06 (offer/provenance/visibility) | versioned intelligence; role-based visibility overlay | TADR-09, TADR-14 |
| CD-07 (workspace) + CD-08 (ownership) | one platform/DB; ownership split; no cross-workspace movement | TADR-05, TADR-06, TADR-07 |
| CD-08 (immutability/governance) | revision-only correction; suggest/approve; audit trail | TADR-08, TADR-09, TADR-18 |
| CD-09 (purchasing) | PO immutability; per-event receiving; acquisition event | TADR-02, TADR-04 |
| CD-10 (inventory) | quantity-only authority; movement traceability | TADR-04, TADR-10 |
| CD-11 (WO boundary, SIGNED-OFF / LOCKED / CLOSED) | lifecycle; assignment; evidence; checklist/test; material; review; views | TADR-02, TADR-03, TADR-04, TADR-11, TADR-12, TADR-15, TADR-16 |
| Identity-link gate (LOCKED HUMAN DECISION) | authentication/link model; application-based PIC registration; Manager/Admin approval | TADR-13 (READY FOR HUMAN ARCHITECTURE APPROVAL; status PROPOSED) |
| QR access policy gate (LOCKED: CONTROLLED ACCESS) | QR check-access flow; customer-safe-only serving | TADR-16 (READY FOR HUMAN ARCHITECTURE APPROVAL; status PROPOSED) |
| Business Access Model (LOCKED HUMAN DECISION) | two-tier unit/company scopes; QR identity; no-price rule; access invariants | TADR-12, TADR-13, TADR-14, TADR-16 (status PROPOSED) |

---

## 14. Readiness Assessment

No ranking or scoring is used.

| Gate | Status | Note |
|---|---|---|
| Business baseline preserved | PASS | no LOCKED rule changed |
| Domain boundaries coherent | PASS | mapped without invention |
| Source of truth defined | PASS | single-write plus projections |
| Transaction boundaries defined | PASS | non-atomic chain respected |
| Audit/correction proposed | PASS | TADR-08/TADR-09 PROPOSED |
| External visibility controlled | OPEN — architecture/mechanism | Business expectation resolved (HBA D-01A = RETAIN); serving/control mechanism remains open |
| Security covered | PASS | architecture level only |
| Workspace isolation covered | PASS | enforcement proposed |
| Deferred items contained | PASS | content-agnostic boundaries |
| CD-02 not reconstructed | PASS | untouched |
| Decisions traceable | PASS | matrix plus TADRs |
| Human approval boundary preserved | PASS | stops at approval gate |
| Identity-link architecture | PASS | business gate LOCKED; TADR-13 READY FOR HUMAN ARCHITECTURE APPROVAL |
| QR policy | PASS | CONTROLLED ACCESS LOCKED; TADR-16 READY FOR HUMAN ARCHITECTURE APPROVAL |
| Business Access Model | PASS | two-tier scopes + QR identity + no-price rule LOCKED; reflected in TADR-12/13/14/16 |
| Programmer handoff / schema / migration | NOT APPLICABLE | not authorized |

---

## 15. Human Approval Gate

```text
==================================================
HUMAN APPROVAL GATE
==================================================
Technical Architecture Status:     APPROVED / CANONICAL
Business Baseline Changed:          NO
New Business Decisions Introduced:  NO
CD-11 Treated As LOCKED:            NO (HUMAN-ACCEPTED)
CD-02 Reconstructed:                NO
TADRs Requiring Human Approval:     TADR-01 … TADR-18 (APPROVED — 2026-09-21)
Blocking Gates:                     RESOLVED — Identity-link reconciliation (TADR-13 READY);
                                    RESOLVED as CONTROLLED — QR access policy (TADR-16 READY);
                                    RESOLVED — Business Access Model (TADR-12/13/14/16 updated)
Partly Blocking:                    Customer publication serving/evidence mechanism (TADR-11/12;
                                    business expectation resolved — HBA D-01A = RETAIN);
                                    Reminder/automation policy (TADR-15)
Non-Blocking:                       TADR-01..10, TADR-14, TADR-17, TADR-18
Governance Gaps:                    GAP-F1 (documentation/traceability gap);
                                    GAP-F2 (non-canonical identifier issue)
Implementation Authorization:       NO
Coding / Migration Authorization:   NO
Architecture Approved:              YES (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
NEXT STEP:                          POST-APPROVAL ARCHITECTURE / IMPLEMENTATION-SPECIFICATION PREPARATION
==================================================
```

---

## Persistence Status

- Files persisted under `docs/30-ARCHITECTURE/` (this report) and
  `docs/30-ARCHITECTURE/TADR/` (TADR-01 … TADR-18).
- No file under `docs/10-DECISIONS/`, no governance file, no application code,
  database, schema, migration, API, UI, deployment configuration, infrastructure,
  or test was modified.
- Explicit implementation boundary: this report and its TADRs authorize nothing
  beyond documentation. Technical Baseline, Implementation Planning, TASK-001,
  Programmer work, coding, schema, migration, and deployment remain unauthorized.
