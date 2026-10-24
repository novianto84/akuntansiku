# ARCHITECTURE BASELINE — Brainstrom CRM

```text
Status: APPROVED / CANONICAL (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

This baseline summarizes what is currently stable enough to serve as authoritative
input for future Implementation Planning. It is not an implementation
specification, schema, API contract, UI specification, or deployment plan. It
creates no business decision and changes no status. Traceability:

```text
Human Decision → Canonical CD → Technical Requirement → TADR (APPROVED)
```

---

## 1. Business Scope

* **CRM scope (CD-01 FINAL/LOCKED):** Company/Customer, Contact/PIC, relationships,
  Unit/asset registry, Service/WO/SPK, technician workflow, service history,
  material usage, customer-facing history, reminders, supporting capabilities
  (auth, RBAC design-separate, audit, files/photos, notifications, QR, search,
  operational reporting).
* **Explicit exclusions from CRM authority:** journal, GL, COA, COGS, FIFO/Average,
  valuation, tax engine, costing, revenue recognition (CD-01/04/05/06/09/10/11).
  Finance/Accounting/Tax are DEFERRED future scope, not permanently excluded.
* **Accounting boundary:** CRM never posts or values; Accurate 5 remains
  existing/transitional reference, not a permanent runtime lock (CD-10).
* **Inventory boundary:** quantity-only operational authority; no reservation,
  valuation, or costing (CD-10).
* **Purchasing boundary:** PR optional; PO required and immutable after Issued;
  per-event receiving with partial accept/reject; emergency purchasing ≠
  emergency service (CD-09).
* **Service/WO boundary:** 1 WO = 1 Unit (bound before CLOSED);
  lifecycle DRAFT → OPEN → IN_PROGRESS → WAITING APPROVAL → CLOSED plus
  terminal CANCELLED (cancellation only from OPEN / IN_PROGRESS);
  correction via WAITING APPROVAL loop pre-CLOSED and REOPEN (CLOSED only)
  post-CLOSED with numbered unlimited cycles (CD-11, SIGNED-OFF / LOCKED /
  CLOSED).
* **External access boundary:** Google-only; application-based PIC registration;
  Manager/Admin approval; applicant ≠ approver; Unit Scope vs Company Scope;
  CONTROLLED QR; customer-safe only; explicit no-price rule (LOCKED HUMAN
  DECISIONS, formal CD documentation pending).
* **Workspace boundary:** one platform, one database; workspace-owned
  transactions/numbering/templates/approvals/reporting/stock/WO; shared masters
  and intelligence only where explicitly allowed; no automatic cross-workspace
  movement; no prohibited combined global transaction reporting (CD-07/08).

## 2. Canonical Business Decisions

| Decision | Status | Source |
|---|---|---|
| CD-01 Business Scope | FINAL / LOCKED | `docs/10-DECISIONS/CD-01-business-scope.md` |
| CD-02 | DEFERRED / UNVERIFIED — not reconstructed | (no canonical document) |
| CD-03 Business Master | LOCKED | `docs/10-DECISIONS/CD-03-business-master.md` |
| CD-04 Acquisition Price | LOCKED | `docs/10-DECISIONS/CD-04-operational-acquisition-price.md` |
| CD-05 Sales/Quotation | LOCKED | `docs/10-DECISIONS/CD-05-sales-transaction-quotation.md` |
| CD-06 Vendor Offer | LOCKED | `docs/10-DECISIONS/CD-06-vendor-offer-price.md` |
| CD-07 Multi-Workspace | LOCKED | `docs/10-DECISIONS/CD-07-multi-workspace.md` |
| CD-08 Data Ownership | LOCKED | `docs/10-DECISIONS/CD-08-data-ownership.md` |
| CD-09 Purchasing | LOCKED | `docs/10-DECISIONS/CD-09-purchasing-transaction-boundary.md` |
| CD-10 Inventory | LOCKED | `docs/10-DECISIONS/CD-10-inventory-operational-boundary.md` |
| CD-11 Service/WO | SIGNED-OFF / LOCKED / CLOSED | `docs/10-DECISIONS/CD-11-service-work-order-operational-boundary.md` |
| Identity-Link reconciliation | LOCKED HUMAN DECISION (formal CD documentation pending) | HUMAN explicit; recorded in `DECISION_REGISTER.md` |
| QR Access Policy (CONTROLLED) | LOCKED HUMAN DECISION (formal CD documentation pending) | HUMAN explicit; recorded in `DECISION_REGISTER.md` |
| Business Access Model | LOCKED HUMAN DECISION (formal CD documentation pending) | HUMAN explicit; recorded in `DECISION_REGISTER.md` |
| Self-approval prohibition | LOCKED business invariant (formal CD documentation pending) | HUMAN explicit; recorded in TADR-13 |

No status is raised by this baseline alignment itself. CD-11 SIGNED-OFF / LOCKED /
CLOSED (BA SIGN-OFF — CD-11 Business Finalization, CD11-001…CD11-029) is recorded
as the governing business baseline for all service-domain direction.

## 3. Technical Architecture Summary

| TADR | Subject | Current Status | Baseline Role |
|---|---|---|---|
| TADR-01 | Application / Module Boundaries | APPROVED | Modular-monolith direction |
| TADR-02 | Domain / Aggregate Boundaries | APPROVED | Aggregate ownership map |
| TADR-03 | Component Subtype Structure | APPROVED | Subtype-specific placeholders; no generic shortcut |
| TADR-04 | Transaction Boundaries | APPROVED | Per-transition guards; non-atomic paired records |
| TADR-05 | Database Strategy | APPROVED | One-DB strategy; product unde decided |
| TADR-06 | Workspace Isolation Enforcement | APPROVED | App-level guards + negative tests |
| TADR-07 | Source-of-Truth Ownership | APPROVED | Single-write ownership map |
| TADR-08 | Audit / Versioning Mechanism | APPROVED | Hybrid direction |
| TADR-09 | Correction / Revision Mechanism | APPROVED | Governed correction flow |
| TADR-10 | Material vs Inventory Separation | APPROVED | Two-sided modeling |
| TADR-11 | File / Photo Architecture | APPROVED | Mediated serving; immutable originals |
| TADR-12 | Read Models / Projections | APPROVED | Hybrid freshness; source-linked |
| TADR-13 | Authentication / Identity-Link | APPROVED | Link-entity direction; SoD invariant recorded |
| TADR-14 | Authorization / Visibility Enforcement | APPROVED | Three layers; two-tier visibility |
| TADR-15 | Background Jobs / Notifications | APPROVED | Disabled-by-default framework |
| TADR-16 | QR Mechanism | APPROVED | Revocable indirection; unit-rooted |
| TADR-17 | Deployment Topology | APPROVED | Candidate direction only |
| TADR-18 | Observability / Traceability | APPROVED | Full-spectrum scope; leakage prohibition |

No TADR status is raised by this baseline itself; TADR-01–18 are APPROVED by the
explicit HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21). Previous stale line in TADR-13
Proposed Direction ("BLOCKED pending reconciliation") has been corrected to
reference the resolved reconciliation; TADR-13 status remains PROPOSED.

## 4. Architectural Invariants

**Identity:** Google-only external authentication; email/domain matching is not
authorization; Google Identity ≠ Contact/PIC ≠ Verified PIC Link ≠ Company
Access; sign-up ≠ automatic PIC; applicant ≠ approver; no self-approval;
approval only by authorized internal Manager/Admin other than applicant; Google
Identity/PIC status are not approval authority; no automatic approval.
**Access:** LOGIN ≠ COMPANY ACCESS; QR ≠ COMPANY ACCESS; Verified PIC = basis
of Company Access; no anonymous external data; authenticated non-PIC →
Unit Scope; verified PIC → Company Scope; cross-company Company Scope
prohibited; Unit Scope is not a browsing mechanism; non-PIC sees no PIC
details/lists; external portal shows no prices/accounting values.
**QR:** QR identifies the Unit; QR on Unit/Invoice/Surat Jalan resolves to the
same Unit; QR is not a separate document scope; no preview before login.
**Service (canonical only; F-1 excluded):** 1 WO = 1 Unit; lifecycle
DRAFT → OPEN → IN_PROGRESS → WAITING APPROVAL → CLOSED plus terminal CANCELLED;
correction via WAITING APPROVAL loop pre-CLOSED and REOPEN (CLOSED only, numbered
unlimited cycles) post-CLOSED; 1 primary + 0..N supporting; BEFORE/DURING/AFTER
findings; mandatory checklist and test/run with N/A + Reason (exact rules
deferred); minimum one HM: initial/start OR final/end; Manager/Admin review
before CLOSED; reviewer-curated customer information. INTERIM/CONTINUATION/FINAL
are report classifications; Outstanding is monitoring, not SLA/overdue.
**Material/Inventory:** WO → Material Usage → Inventory Operation (non-atomic);
inventory quantity authority only; acquisition price operational reference only;
no valuation/costing/HPP/COGS/journal.
**Purchasing:** PR optional; PO required, immutable after Issued, revision-based
correction; per-event receiving with partial accept/reject; emergency
purchasing ≠ emergency service.
**Workspace:** isolation enforced; no automatic cross-workspace movement; no
prohibited combined global transaction reporting.

## 5. Aggregate / Boundary Summary

Company (identity root, PROPOSED map); Contact/CompanyRole (under Company,
PROPOSED); Verified PIC Link (under Contact/Company, per-company states,
business LOCKED / mechanism PROPOSED); Unit + Components (asset registry,
PROPOSED shapes); WorkOrder (execution/lifecycle owner, PROPOSED);
Service execution artifacts (WO-owned, PROPOSED); MaterialUsage vs
InventoryOperation (separated, PROPOSED); Purchase Request / Purchase Order /
Receiving (workspace-owned, PROPOSED); Workspace (isolation boundary, PROPOSED);
External Access / QR (two-tier visibility, business LOCKED / mechanism PROPOSED).
No entity, table, or schema is created by this baseline.

## 6. Deferred Business Decisions

### F-1 — Service Execution Clarification: DEFERRED — HUMAN DECISION NOT REQUESTED YET

Unresolved, with no LOCK/REMOVE/inference/reinterpretation: arrival scan;
mandatory start time; mandatory GPS; OFF / RUNNING / after-repair steps; PM HM
initial + final requirement; inspection HM optional; SKIP_TEMPORARY only interim;
photo slots. F-1 must not modify CD-11. CD-11 remains authority for HM:
initial/start OR final/end. F-1 is a deferred clarification, not a technical
blocker from contradiction — but final approval cannot be claimed while required
clarification is unresolved.

Customer publication business expectation: **RESOLVED — HBA D-01A = RETAIN** (previously presented
customer-facing content remains available as the historical record; current authoritative condition
remains distinguishable). D-01B is semantic freshness only, with no numeric SLA. Snapshot/materialization,
refresh, propagation, cache, replication, drift, and serving remain architecture/mechanism work.
Other business-deferred items: reminder/automation policy; emergency retroactive timestamp convention;
Outstanding surfacing rules; subtype field requirements; N/A taxonomy; checklist
contents; acknowledgement evidence; self-approval formal CD documentation;
formal CD documentation of chat-LOCKED decisions.

## 7. Deferred Technical Decisions

OAuth/token/session mechanics; exact database implementation and product;
evidence/file storage mechanics; QR token/URL/rotation/expiry mechanics;
invitation UX; exact enforcement middleware; snapshot-vs-live mechanics;
notification mechanism and scheduling; retention windows; deployment selection;
telemetry substrate. None resolved here.

## 8. Maturity

LOCKED washing applied per item: CD-01/03–10 LOCKED; access-model gates LOCKED
(formal CD documentation pending); CD-11 SIGNED-OFF / LOCKED / CLOSED; TADR-01–18 APPROVED
(HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21); F-1 and lists above DEFERRED;
anything else UNKNOWN. No other category used.

## 9. Implementation Authorization

> **NOT AUTHORIZED**

Stable for planning input: business scope, boundaries, invariants, aggregate map,
and TADR directions as APPROVED. Insufficient for implementation: F-1 and deferred
items open; no specification, schema, contract, or test exists. Gaps are stated,
not filled.

---

*Baseline artifact status: APPROVED / CANONICAL (HUMAN FINAL TECHNICAL
ARCHITECTURE APPROVAL — 2026-09-21). It authorizes nothing beyond documentation;
implementation remains unauthorized.*
