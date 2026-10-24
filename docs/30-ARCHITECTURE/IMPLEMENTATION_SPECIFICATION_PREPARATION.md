# Implementation-Specification Preparation Report

> Status: PREPARATION ONLY — READ / PROPOSE
> Persistence: PERSISTED FROM PRIOR CONVERSATION
> Implementation Authorization: NO
> Schema Finalization: NO
> Coding: NO
> Migration: NO
> API Contract Finalization: NO
> UI Implementation: NO
> Deployment: NO

## IMPLEMENTATION-SPECIFICATION PREPARATION REPORT

**Mode:** READ / PROPOSE ONLY
**Technical Architecture:** APPROVED / CANONICAL (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
**Implementation Authorization:** NO
**Schema / Migration / API / UI / Coding / TASK-001 / Programmer handoff:** NO — all prohibited until explicit Human authorization.

> Technical Architecture approval does not equal implementation authorization.

This report prepares the bridge from APPROVED Technical Architecture to FUTURE Implementation Specification. It does not cross that bridge. No schema, API contract, UI spec, migration, code, or TASK-001 is created here.

> **Status clarification added 2026-09-26 (documentation amendment).** This report was written under the
> governance status in force at that time, when `CD-11` was `HUMAN-ACCEPTED`. `CD-11` was subsequently raised to
> **SIGNED-OFF / LOCKED / CLOSED** by explicit BA sign-off (CD-11 Business Finalization, CD11-001…CD11-029;
> `CD-11` §32, which also requires the earlier wording to be read according to the new status until the
> administrative update follows). The current status is recorded in `ARCHITECTURE_LOCK.md`,
> `DECISION_REGISTER.md` (row `CD-11`) and `AI_CONTEXT_INDEX.md` §6. Accordingly, this report's statements that
> describe `CD-11` as `HUMAN-ACCEPTED` or "explicitly NOT LOCKED", and the corresponding prohibition on
> treating `CD-11` as LOCKED, are **superseded for current governance interpretation on that point only**. No
> date for the status raise is recorded in this repository. The report's content is otherwise preserved
> unchanged, including its §15 risk classification and its recommendation about formal CD documentation.

---

### 1. Executive Summary

1. **Canonical foundation is sufficient for preparation, insufficient for implementation.** CD-01 FINAL/LOCKED, CD-03…CD-10 LOCKED, three chat-LOCKED access gates (identity-link reconciliation, QR CONTROLLED ACCESS, Business Access Model — formal CD documentation pending), CD-11 HUMAN-ACCEPTED (explicitly NOT LOCKED), TADR-01…TADR-18 APPROVED, Architecture Baseline APPROVED. Implementation remains unauthorized.
2. **Service domain is the largest constrained zone.** CD-11 gives a stable operational boundary (lifecycle, 1 WO = 1 Unit, assignment, findings/HM/evidence/checklist/test, review, correction, views, workspace), but its HUMAN-ACCEPTED status plus explicit F-1 deferral means service-execution mechanics must not be finalized. Canonical service rules are derivable as implementation requirements; F-1 mechanics are Classification D and block their dependent specs.
3. **Security/access model is business-LOCKED and must propagate verbatim.** Google-only external auth; Google Identity ≠ Contact/PIC ≠ Verified PIC Link ≠ Company Access; LOGIN ≠ COMPANY ACCESS; QR ≠ COMPANY ACCESS; Verified PIC = sole basis of Company Scope; no anonymous data; Unit Scope vs Company Scope; no-price rule; applicant ≠ approver with bypass prohibition; cross-company isolation. These are Classification A (derivable) implementation requirements, not future choices.
4. **Most technical "how" is Classification B.** Architecture fixes direction (modular monolith, aggregate ownership, per-transition guards, one relational DB with app-level isolation, hybrid audit, two-sided material/inventory, mediated file serving, hybrid projections, link-entity, three-layer authz, disabled-by-default jobs, QR indirection, containerized-VPS candidate, full-spectrum observability) but deliberately leaves mechanism detail (exact tables/columns/indexes, routes/payloads, components, providers, token formats, queue, storage class, thresholds) unspecified. Those need future Implementation Specification; they are not Human business decisions.
5. **Genuine Human decisions remaining are few and named.** Customer publication model (snapshot-vs-live expectation + publication/permission mechanism), reminder/automation policy, emergency retroactive timestamp convention (and completion deadline), deployment operational context, plus content-deferred business inputs (checklist contents, N/A taxonomy, subtype field requirements, acknowledgement fallback evidence, Outstanding surfacing rules, offer-visibility matrix content, permission-matrix content). Everything else is specification choice or deferred technical evaluation.
6. **Out-of-scope and deferred-future must not be reopened.** Journal/GL/COA/COGS/FIFO/Average/valuation/tax engine/costing/revenue recognition are outside CRM authority (Classification E). Full Finance/Accounting/Tax is DEFERRED future scope, not permanently excluded — architecture must not foreclose it, and current-phase specs must not implement it.
7. **Recommended next gate is descriptive only:** Human review of this report + formal CD documentation of the three chat-LOCKED gates + Human decision on whether to resolve F-1 and the partly-blocking publication/automation gates before authorizing any Implementation Specification workstream. No implementation action is recommended.

---

### 2. Canonical Inputs Read

All files read directly; no implementation treated as authoritative.

**Business decisions (`docs/10-DECISIONS/`):**

- `CD-01-business-scope.md` — FINAL / LOCKED
- `CD-03-business-master.md` — LOCKED
- `CD-04-operational-acquisition-price.md` — LOCKED
- `CD-05-sales-transaction-quotation.md` — LOCKED
- `CD-06-vendor-offer-price.md` — LOCKED
- `CD-07-multi-workspace.md` — LOCKED
- `CD-08-data-ownership.md` — LOCKED
- `CD-09-purchasing-transaction-boundary.md` — LOCKED
- `CD-10-inventory-operational-boundary.md` — LOCKED
- `CD-11-service-work-order-operational-boundary.md` — HUMAN-ACCEPTED, Implementation Authorization NO (explicitly NOT LOCKED)
- CD-02 — DEFERRED / UNVERIFIED, no canonical document present, not reconstructed.

**Governance (canonical location is repository root, not `docs/30-ARCHITECTURE/` as the task text suggests — see §15):**

- `AI_CONTEXT_INDEX.md` (root)
- `AI_OPERATING_RULES.md` (root)
- `ARCHITECTURE_LOCK.md` (root) — authority index only
- `DECISION_REGISTER.md` (root) — registers CD statuses + 3 LOCKED Human gates (formal CD pending) + 4 pending gates

**Technical architecture (`docs/30-ARCHITECTURE/`):**

- `ARCHITECTURE_BASELINE.md` — APPROVED / CANONICAL (2026-09-21), Implementation NO
- `TECHNICAL_ARCHITECTURE_FINALIZATION.md` — read as supporting evidence/context (proposal record; approval recorded in Baseline + TADRs)
- `TADR/TADR-01.md` … `TADR-18.md` — all APPROVED (HUMAN FINAL 2026-09-21), each with Implementation/Schema/Migration/Coding NO

**Repository tree inspected:** `docs/` contains `10-DECISIONS/`, `20-WORKSTREAMS/`, `30-ARCHITECTURE/` (Baseline + TADR/ + Finalization), `90-AUDIT/`, plus Accurate-5 reference files. `app.py`, current DB/schema, historical commits are evidence only per every CD governance clause. Not used as authority.

**Authority order applied:** Human decisions / LOCKED Business Architecture > Human Final Technical Approval > Baseline > TADR-01…18 > ARCHITECTURE_LOCK > DECISION_REGISTER > AI_CONTEXT_INDEX > historical/evidence > chat memory. Conflicts reported, not reconciled by assumption.

---

### 3. Architecture → Implementation Traceability

Pattern applied per domain (Business Decision → TADR → Implementation Requirement → Spec Candidate → Human Decision? → Allowed?):

| # | Domain | Business source (status) | TADR direction (APPROVED) | Implementation Requirement (derived, not finalized) | Future Spec Candidate | Human? | Allowed now? |
|---|---|---|---|---|---|---|---|
| 1 | Workspace | CD-07 LOCKED, CD-08 LOCKED | TADR-01,05,06,14 | Isolation must be enforced + negatively tested; no auto cross-workspace movement; no combined global transaction report | IS-01 | No (except ops context = C) | Spec later, not now |
| 2 | Company/Prospect/Customer/Vendor | CD-03 LOCKED | TADR-02,07 | Single Company identity; Prospect/Customer/Vendor are roles, not separate masters | IS-02 | No | Spec later |
| 3 | Contact/PIC | CD-03 LOCKED, CD-08 | TADR-02,07 | Contact separate 1-N under Company; supports multiples/primary/role; survives link revocation | IS-02 | No | Spec later |
| 4 | Google Identity | LOCKED Human gate (CD pending) | TADR-13 | Google-only external sign-up/in; sign-up grants nothing; email match NOT required | IS-03 | No (locked) | Spec later |
| 5 | Verified PIC Link | LOCKED Human gate | TADR-13,02 | Application → PENDING → Manager/Admin approval → VERIFIED per-company; REVOKED supported; no cross-company grant | IS-03 | No (locked) | Spec later |
| 6 | Authorization/visibility | CD-01 S3, CD-06 Q8, CD-11 §25, Access Model LOCKED | TADR-14 | Three layers (authN/authZ/visibility); two external tiers only (Unit vs Company Scope) | IS-04 | Partly (matrix content = C) | Direction locked; content spec later |
| 7 | Unit | CD-11 §4 (ACCEPTED) | TADR-02,07 | Asset parent; WO binds exactly-1 before COMPLETED/CLOSED; CRM-owned/shared registry | IS-05 | No | Spec later |
| 8 | Components | CD-11 §4 (ACCEPTED) | TADR-03 | ENGINE/GENERATOR/BOX_CHASIS subtype-specific placeholders; no generic JSON/EAV; registry types spec-less | IS-05 | Yes (fields = C) | Placeholders only |
| 9 | Work Order | CD-11 §§2,3,6 (ACCEPTED) | TADR-02,04,07 | Optional request; Manager/Admin official creation; DRAFT→ASSIGNED→IN_PROGRESS→COMPLETED→CLOSED; CANCELLED pre-COMPLETED only | IS-06 | No | Spec later |
| 10 | Service execution | CD-11 §§9,28 + F-1 | TADR-04 | Manual Start Work + timestamp; QR/GPS optional evidence; emergency retroactive allowed, convention deferred | IS-07 | — | D (F-1); see §7 |
| 11 | Findings | CD-11 §§10,12 (ACCEPTED) | TADR-02,07 | BEFORE/DURING/AFTER mandatory all types; Condition+Action always; Diagnosis/Recommendation conditional | IS-08 | No | Spec later |
| 12 | Checklist/test/run | CD-11 §§17,18 (ACCEPTED) | TADR-01,04 | Mandatory all types; N/A+Reason with reviewer validation (principle); exact rules deferred | IS-08 | Yes (contents/taxonomy = C) | Principle locked; content deferred |
| 13 | Hour meter | CD-11 §11 (ACCEPTED) | TADR-02 | Minimum one HM (initial/start OR final/end); N/A+open-reason + reviewer validation | IS-08 | Yes (exact N/A = C; F-1 PM/inspection extras = D) | Minimum locked; extras deferred |
| 14 | Participants | CD-11 §8 (ACCEPTED) | TADR-02,04 | 1 Primary + 0..N Supporting; primary = accountability; all actuals in history | IS-06/08 | No | Spec later |
| 15 | Materials | CD-11 §13, CD-04 (LOCKED) | TADR-10,04 | WO record = Item+Qty+Harga Perolehan per Unit; non-stock recordable w/o stock-out; non-atomic flow | IS-09 | No | Spec later |
| 16 | Inventory Operation | CD-10 LOCKED | TADR-04,10,07 | Qty-only authority; receiving→+N immediate; adjustment controlled; no reservation; AVAILABLE vs DAMAGED/QUARANTINE | IS-10 | No | Spec later |
| 17 | Purchasing | CD-09 LOCKED | TADR-02,04 | PR optional; PO mandatory; per-event receiving; emergency-purchasing ≠ emergency-service | IS-11 | No | Spec later |
| 18 | PR | CD-09 LOCKED | TADR-02,04 | Skippable; broad initiators (permission detail open); cancellable with reason | IS-11 | No | Spec later |
| 19 | PO | CD-09 LOCKED | TADR-04,09 | Draft→Issued→Received→Completed; immutable after Issued; revision-based correction; offer-linked but price-independent | IS-11 | No | Spec later |
| 20 | Receiving | CD-09 LOCKED | TADR-04 | Per-event record; partial accept/reject; remainder outstanding (no auto-complete); acquisition event on receipt+actual price | IS-11 | No | Spec later |
| 21 | QR | CD-11 §26 (ACCEPTED) + CONTROLLED gate LOCKED | TADR-16 | Permanent + unit-scoped; same QR on Unit/Invoice/Surat Jalan → same Unit; SCAN→sign-in→CHECK→UNIT DATA; no anonymous data | IS-12 | No (policy locked; token mechanics = B) | Spec later |
| 22 | Files/photos | CD-11 §§16,25 (ACCEPTED) | TADR-11 | Condition-driven evidence (nameplate/HM/before/after mandatory; during/replacement/damage/test conditional); reviewer-curated publication; immutable originals; mediated serving | IS-13 | Partly (publication model = C) | Direction locked; publication mechanics gated |
| 23 | Audit trail | CD-08, CD-05/06/09/10/11 | TADR-08,18 | Required fields: actor, timestamps, before/after, reason, reviewer, approval state, links; tamper-evident; dual-time capture for retroactive | IS-14 | No | Spec later |
| 24 | Versioning | CD-04/05/06/08/09 | TADR-08 | Hybrid: immutable versions (commercial/price) + append-only governance trail (WO); v1 preserved; usage pinned to version used | IS-14 | No | Spec later |
| 25 | Correction/revision | CD-11 §§22,23 (ACCEPTED), CD-08 | TADR-09,04 | WO: REOPEN→CORRECTION→REVIEW→CLOSED; no overwrite; no post-COMPLETED CANCELLED; commercial/price: version chains | IS-14 | No | Spec later |
| 26 | Read models/projections | CD-11 §§24,25,26,28A,30 (ACCEPTED) | TADR-12,07 | One history/multiple views; derived-only; hybrid freshness (live internal, snapshot customer/QR); source-linked | IS-15 | Partly (snapshot-vs-live = C) | Direction locked; expectation gated |
| 27 | Notifications/jobs | CD-11 §27 (ACCEPTED), CD-01 S5 | TADR-15 | Manual reminder baseline; every policy-unresolved job disabled-by-default behind Human flag; idempotent/observable | IS-16 | Yes (automation policy = C) | Framework only; no enabled automation |
| 28 | Observability | CD-08, CD-11 | TADR-18 | Full-spectrum telemetry + end-to-end traceability; leakage prohibition (no prices/intelligence/notes/tokens/secrets in logs) | IS-17 | No | Spec later |
| 29 | Numbering | CD-05, CD-07 Q11 (LOCKED) | Platform (TADR-01) | Per-workspace sequences; annual reset; immutable; never reused; exact syntax OPEN | IS-18 | No (syntax = B, not business) | Spec later |
| 30 | Reporting | CD-07 Q16, CD-05, CD-11 | TADR-12,06 | Workspace-scoped operational reporting; no combined global transaction report; negative test required | IS-15 | No | Spec later |
| 31 | External portal | Access Model + QR gates LOCKED | TADR-12,13,14,16,11 | Two-tier serving; customer-safe allowlist + reviewer curation; no prices; mediated scope-bound serving | IS-12 | Partly (publication model = C) | Direction locked; mechanics gated |
| 32 | Security boundaries | All LOCKED + gates | TADR-13,14,16,18,06 | Invariants in §9; isolation violation = first-order security event; sealed secrets; QR-abuse monitoring | Cross-cutting | No | Requirements locked; mechanisms spec later |

Business vs technical separation is preserved per row: the left columns state what the system must mean (business), the middle-right states how software may implement it (technical direction), without inventing exact code/DB/API mechanism.

---

### 4. Classification A — Derivable

Already sufficiently determined to be translated into Implementation Specification later without introducing a business decision. Stated as business rule → derived technical requirement. No mechanism finalized here.

**A-1. Workspace isolation:** Business: one platform, per-company workspace, no automatic cross-workspace movement, no combined global transaction reporting (CD-07). Technical: app-level guard on every read/write path + negative tests (cross-write/read/numbering-reuse/global-report must fail) (TADR-06). `IMPLEMENTATION-SPEC CANDIDATE`, not final schema/middleware.

**A-2. Company identity:** Business: one canonical Company; Prospect/Customer/Vendor are roles; no duplicate masters (CD-03). Technical: Company as identity-root aggregate; Contact/CompanyRole under Company (TADR-02/07).

**A-3. Contact separation:** Business: Contact/PIC 1-N under Company, multiples/primary/role supported, not merged into Company fields (CD-03). Technical: Contact survives link revocation; link entity separate (TADR-02/13).

**A-4. Identity chain:** Business (LOCKED Human, CD pending): Google-only external; sign-up grants nothing; application → PENDING; Manager/Admin approval → VERIFIED; email match NOT required; Google Identity ≠ Contact/PIC ≠ Verified PIC Link ≠ Company Access; no cross-company grant. Technical: link-entity lifecycle with per-company VERIFIED/PENDING/REVOKED, session revocation propagation (TADR-13).

**A-5. Self-approval prohibition:** Business: applicant cannot approve own PIC application. Technical: verification authority distinct from creation; no auto-approval; direct-URL/API bypass must not enable self-approval (TADR-13 §Security).

**A-6. Access invariants:** Business (LOCKED): LOGIN ≠ COMPANY ACCESS; QR ≠ COMPANY ACCESS; Verified PIC = sole basis of Company Scope; no data without Google sign-in (no preview); Unit Scope (unit identity, owner company, address, work/material history; never PIC details/lists, other units, company data, or prices) vs Company Scope (all Units of that Company + histories + PIC per customer-safe visibility); QR on Unit/Invoice/Surat Jalan = same Unit; explicit no-price rule. Technical: three-layer enforcement + two-tier projection serving (TADR-12/13/14/16).

**A-7. QR policy:** Business (CONTROLLED, LOCKED): SCAN → SIGN UP/IN → CHECK ACCESS → UNIT DATA; permanent + unit-scoped; customer-safe only. Technical: DB-backed indirection decoupling permanent identity from rotatable secret; unit-rooted resolution; cross-unit browsing structurally impossible (TADR-16).

**A-8. WO lifecycle (HUMAN-ACCEPTED baseline):** Business: optional request; Manager/Admin official creation; DRAFT→ASSIGNED→IN_PROGRESS→COMPLETED→CLOSED; CANCELLED pre-COMPLETED only; 1 WO = 1 Unit bound before COMPLETED/CLOSED; 1 Primary + 0..N Supporting; manual Start Work + timestamp; COMPLETED = core work done (photos/material/test/HM/unit/checklist/detail completable during review); mandatory Manager/Admin review before CLOSED with return-for-correction; acknowledgement OPTIONAL and never blocks CLOSED. Technical: per-transition guard matrix rejecting ASSIGNED→CLOSED, COMPLETED→CANCELLED, direct edit of CLOSED (TADR-04); WO as execution/lifecycle owner aggregate (TADR-02/07). Authority note: HUMAN-ACCEPTED, not LOCKED — spec must cite it as such, never upgrade it.

**A-9. Findings/evidence principle:** Business: BEFORE/DURING/AFTER mandatory all types; Condition+Action always; Diagnosis/Recommendation conditional; evidence condition-driven (nameplate/HM/before/after mandatory; during/replacement/damage/test conditional); N/A + open-reason + reviewer validation as principle. Technical: WO-owned execution artifacts; mediated file serving; immutable originals (TADR-02/11). Exact taxonomies are C/D, not A.

**A-10. HM minimum:** Business: minimum one HM — initial/start OR final/end (CD-11 §11 governs; F-1 must not modify it). Technical: HM as WO-owned execution fact with dual-time capture support (TADR-08). PM/inspection extras are D.

**A-11. Material/inventory split:** Business: WO usage = Item+Qty+Harga Perolehan per Unit, no computed totals required, no journal; inventory = qty-only authority, no reservation/valuation/costing; non-stock/customer-owned/direct-purchase recordable without stock-out; flow need not be atomic (CD-04, CD-10, CD-11 §13). Technical: two-sided paired records with mutual references + attention-only reconciliation; no phantom entries; terminology "Harga Perolehan (per Unit)" (TADR-04/10).

**A-12. Sales semantics:** Business: 1 Quotation → N SO (partial conversion, remainder outstanding, traceable); 1 SO → N fulfillments (partial, backorder, traceable, never mutates stock, no reservation); SO standalone allowed; PARTIALLY_CONVERTED state; CLOSED terminal (auto on all-items-converted with reason COMPLETED, no approval; manual via sales request + reason + Manager/Admin approval); no REVOKED; revision = new version with base+suffix, prior immutable. Technical: additive conversions, computed remainders, revision chains (TADR-04/09).

**A-13. Purchasing semantics:** Business: PR optional (emergency may skip PR but never PO+receiving+reason); PO mandatory, Draft→Issued→Received→Completed, immutable after Issued, revision-based correction; per-event receiving with partial accept/reject, remainder outstanding, no auto-complete; acquisition event on receipt + actual price (PO price initial, corrected at receiving, versioned). Technical: same guard + revision substrate (TADR-04/09).

**A-14. Price intelligence:** Business: Offer (Exclude/Include/Final from one original+basis; NET_FINAL distinct) ≠ Acquisition (actual-event reference, multiple per item/vendor, immutable, shared); provenance preserved (vendor/item/price/basis/date/source/version); no ranking/recommendation/pricing engine; latest-offers count OPEN; Q8 dynamic role-based visibility overlay via Admin config without touching ownership/records/history. Technical: versioned intelligence aggregates; visibility as policy overlay separate from action rights (TADR-09/14).

**A-15. Ownership/governance:** Business: shared masters/intelligence vs workspace-owned transactions per CD-07/08; master creation by any workspace (immediately shared), modification via suggest + Admin approval with global effect; used masters nonaktif/arsip never hard-delete; duplicates via business process (no auto-matching); merge process required (technical detail open); no private notes. Technical: single-write ownership map; derived views read-only by construction (TADR-07); hybrid audit (TADR-08); governed correction flow (TADR-09).

**A-16. Views principle:** Business: ONE OPERATIONAL HISTORY, MULTIPLE CONTEXTUAL VIEWS; Unit view unit-scoped; Customer view aggregates customer's WOs each tied to its own Unit; QR view unit-scoped; no duplicate history; no cross-unit leakage; Outstanding = monitoring/attention, never overdue/SLA/escalation/blocking; INTERIM/CONTINUATION/FINAL = report classifications with BEFORE/DURING/AFTER, never parallel lifecycle. Technical: projections derived-only, source-linked + freshness/publication metadata (TADR-07/12).

**A-17. Numbering/reporting ownership:** Business: per-workspace numbering with separate sequences, annual reset, immutable, never reused (exact syntax OPEN); templates per workspace; pipeline/approval/reporting per workspace. Technical: platform enforcement point + negative tests (TADR-01/06).

**A-18. Observability/audit discipline:** Business: revision-only correction; reviewer accountability; history preserved. Technical: hybrid audit with mandatory trail fields; full-spectrum telemetry with leakage prohibition and tamper-evident handling (TADR-08/18).

---

### 5. Classification B — Specification Required

Architecture fixes the boundary; exact mechanism needs future Implementation Specification. Do NOT implement now. Each is a specification choice, not a business decision.

- **B-1. Module physical layout:** Modular-monolith direction APPROVED (TADR-01); package/directory naming, seam-ownership checklist mechanics, and import discipline need spec.
- **B-2. Aggregate record shapes:** Ownership map APPROVED (TADR-02/07); logical concepts (Company, Contact, CompanyRole, Verified PIC Link, Unit, Component subtypes as placeholders, WO, execution artifacts, MaterialUsage, InventoryOperation, PR/PO/Receiving, Offer/AcquisitionReference, projections) are `IMPLEMENTATION-SPEC CANDIDATES` — no tables/columns/keys/indexes/constraints/ORM models finalized.
- **B-3. Guard composition:** Per-transition matrix + workspace guard + domain-policy composition APPROVED in principle (TADR-04/06/14); exact middleware/policy-evaluation order, error taxonomy, and negative-test suite need spec.
- **B-4. Database product + predicates:** One relational DB + app-level scoping APPROVED (TADR-05); product/version selection and whether store-level scoping predicates are added (defense in depth) are deferred technical evaluations for planning.
- **B-5. Company↔Workspace usage-marker shape:** Required by CD-08 Q4 but form expressly deferred; needs spec (TADR-02/06 open question).
- **B-6. Suggest/approve mechanics:** Suggest + Admin approval + global effect LOCKED (CD-08); exact workflow states, matrix mechanics, and merge/nonaktif/arsip technical procedures need spec.
- **B-7. Transaction plumbing:** Paired-record pattern + causal receiving→stock link APPROVED (TADR-04); exact reference fields, ordering tolerance, and reconciliation-view queries need spec (surfacing rules themselves are business-gated; see C).
- **B-8. Correction-context mechanics:** REOPEN→CORRECTION→REVIEW→CLOSED flow APPROVED (TADR-09); presentation/UX, concurrency (no lost updates on guarded transitions), and version-graph handling need spec.
- **B-9. File/storage mechanics:** Content-addressed internal store + per-file metadata (owner, evidence class, review/publication state, immutability flag) + mediated serving + immutable originals APPROVED (TADR-11); storage class (object vs filesystem), metadata record shape, derivative pipeline, retention windows need spec. No paths/URLs finalized.
- **B-10. Projection mechanics:** Hybrid freshness + source-link + publication metadata APPROVED (TADR-12); refresh cadence/staleness monitoring, snapshot identity scheme, and event-driven upgrade path need spec (business expectation gated; see C).
- **B-11. AuthN mechanics:** Link-entity + lifecycle-bound sessions APPROVED (TADR-13); OAuth/token/session/provider mechanics, invitation UX, and revocation-propagation implementation need spec.
- **B-12. QR mechanics:** DB-backed indirection + unguessable identifier + unit-rooted resolution APPROVED (TADR-16); exact token format, URL structure, rotation/expiry mechanics, reprint coordination, abuse-rate thresholds need spec. No token/URL finalized.
- **B-13. Job substrate:** Disabled-by-default framework with idempotent/status-visible/retry-explicit jobs APPROVED (TADR-15); queue/backoff/dead-letter choice, transport, scheduling substrate need spec. No job enabled here.
- **B-14. Observability substrate:** Scope APPROVED (TADR-18); telemetry backend, dashboard/alert ownership, retention storage, debug-verbosity gating need spec. No thresholds with business meaning invented.
- **B-15. Numbering syntax:** Per-workspace/annual-reset/immutable rules LOCKED; exact syntax/format needs spec (CD-05 OPEN/DEFERRED).
- **B-16. Deployment selection:** Containerized-VPS candidate direction APPROVED as technical criteria only (TADR-17); product/sizing/cost/TLS/backup-encryption/hardening checklist need spec after Human ops context (see C).
- **B-17. API capabilities (conceptual only):** Capabilities that will eventually be required include: PIC-link application submission; PIC-link approval/rejection/revocation; workspace-scoped CRUD + lifecycle transitions for Quotation/SO/fulfillment/PR/PO/receiving/WO; suggest/approve master change; offer/acquisition recording + version retrieval; inventory movement + adjustment + opname; material-usage recording; file capture/review/publish/replace; manual reminder creation; QR-scoped unit/company views. Expressed as "API capability required: …" — no routes, methods, payloads, status codes, or middleware finalized.
- **B-18. UI capabilities (conceptual only):** Internal PIC review queue; Manager/Admin approval; unit service history; restricted external Unit Scope view; Verified PIC Company Scope view; WO lifecycle board; correction/review queue; Outstanding attention view; revision history views. No layouts, buttons, field order, routes, components, CSS, or mobile behavior finalized.

---

### 6. Classification C — Human Decision Required

Missing detail affects business meaning, policy, authority, or externally visible behavior and cannot be inferred. No final answer proposed as decided. Specification choices are excluded (they are §5).

- **C-1. Customer publication model** (affects TADR-11/12): snapshot-vs-live business expectation ("what the customer saw is fixed" vs live) + any technical publication/permission mechanism + customer-safe filtering/curation mechanism + Customer View aggregation/filter implementation. Partly blocking.
- **C-2. Reminder/automation policy** (affects TADR-15): whether any automatic reminder generation is wanted at all; intervals; surfacing behavior. Manual-only baseline LOCKED; anything automatic needs explicit policy. Partly blocking for enabling jobs (non-blocking for framework).
- **C-3. Business permission-matrix content** (affects TADR-14/09/04): detailed RBAC permissions, approver lists, suggest/approve authority matrix, correction/reopen authority beyond "Manager/Admin", material-take authority. Role structure (ADMIN/MANAGER/FINANCE/KASIR) is retained but permission content is separate design work per CD-01 S3. Partly blocking for enforcement completeness.
- **C-4. Vendor Offer visibility configuration:** CD-06 Q8 gives Admin the toggle mechanism but the actual per-role visibility settings are business operations content, not locked. Needs Human/ Admin policy input during spec.
- **C-5. Emergency retroactive timestamp convention** (CD-11 §9/§28 DEFERRED): ex-post declaration + reviewer validation sketched but convention not formulated. Also retroactive completion deadline (no numerical SLA locked).
- **C-6. Deployment operational context:** Business cost/operations-capacity context (Human input) required before any topology selection (TADR-17). No formal BD identifier; do not infer.
- **C-7. Component subtype field requirements:** Which fields (if any) ENGINE/GENERATOR/BOX_CHASIS need for first slice (TADR-03 gate). Placeholders suffice until Human provides requirements.
- **C-8. Checklist contents + Test/Run + HM/evidence N/A taxonomy:** Mandatory-with-N/A+Reason principle is canonical; exact checklist items, exact N/A rules/examples/closed-vs-open reason lists, PM-specific and inspection-specific HM extras, and acknowledgement fallback evidence type are all DEFERRED business content.
- **C-9. Minor/Major threshold:** No duration/hour thresholds locked (CD-11 §5). If business wants any threshold, it is a new decision.
- **C-10. Outstanding surfacing rules:** Which states appear, where, and for whom (TADR-04/10/12 open question). Outstanding ≠ Overdue principle is canonical; surfacing detail is business-owned.
- **C-11. Service Type detailed definitions:** Conceptual boundaries LOCKED (PM, Inspection/Troubleshoot incl. minor repair, Minor/Major, Emergency as type not flag, Commissioning/Testing); detailed definitions DEFERRED.
- **C-12. Formal CD documentation of chat-LOCKED gates:** Identity-link reconciliation, QR CONTROLLED ACCESS, Business Access Model, and self-approval invariant are LOCKED Human decisions recorded in DECISION_REGISTER/TADRs but formal CD documents are pending. Spec phase should not proceed on chat memory alone; Human should confirm formal CDs.
- **C-13. CD-11 promotion question:** CD-11 is HUMAN-ACCEPTED, not LOCKED. Whether/when it becomes LOCKED/FINAL is a Human decision. Specs citing CD-11 must preserve its current status.

Emergency nominal thresholds, document-template content, warehouse/bin OWNERSHIP detail beyond "one warehouse; bin deferred" (CD-10), and Accurate migration/integration runtime role (CD-01 OPEN) are likewise Human/business-owned if ever taken up — not inferred.

---

### 7. Classification D — Deferred / F-1

Explicitly deferred by canonical architecture. Do NOT attempt to close. Deferred ≠ missing requirement for AI to fill.

**F-1 Boundary — Service execution clarification (DEFERRED. Technical Architecture remains APPROVED / CANONICAL. F-1 remains DEFERRED and constrains only the affected implementation-specification slices. No F-1 resolution has been authorized by this report.):**

1. **Already canonical (CD-11, HUMAN-ACCEPTED + TADR-02/04/07/11/12):** 1 WO = 1 Unit; main lifecycle; CANCELLED pre-COMPLETED only; correction path; 1 Primary + 0..N Supporting; manual Start Work + timestamp; BEFORE/DURING/AFTER findings; Condition+Action always; minimum one HM (initial/start OR final/end); mandatory checklist + test/run with N/A+Reason principle; condition-driven evidence (mandatory vs conditional sets); mandatory Manager/Admin review before CLOSED with return path; reviewer-curated customer-safe subset; acknowledgement OPTIONAL; QR permanent + unit-scoped; manual reminder baseline; emergency retroactive formalization required before CLOSED; Outstanding as monitoring; INTERIM/CONTINUATION/FINAL as report classes; one-history/multiple-views.
2. **Remains deferred (must NOT be invented or resolved here):** arrival scan requirements; mandatory start time; mandatory GPS; OFF/RUNNING/AFTER-REPAIR state model; PM-specific initial+final HM requirement; inspection-specific HM rules beyond canonical minimum; SKIP_TEMPORARY behavior; mandatory photo-slot model; other deferred service execution mechanics. F-1 must not modify CD-11; CD-11 remains authority for HM minimum.
3. **Implementation specs that must NOT be written until F-1 is resolved:** any service-execution step enforcement (arrival/start/GPS/state gates), PM/inspection HM enforcement beyond the minimum, SKIP_TEMPORARY lifecycle handling, photo-slot schema/validation, OFF/RUNNING/after-repair workflow. Writing these now would pre-decide F-1.
4. **Service architecture that can proceed independently of F-1:** aggregate map (WO-rooted), lifecycle guard skeleton for canonical states, correction flow, material/inventory separation, file/projection direction with content-agnostic containers, Outstanding as attention overlay (no timers), review/curation ownership. Content-agnostic containers must stay empty where F-1 content is missing.

**Other D items (deferred, non-F-1):** customer publication snapshot-vs-live + mechanism; reminder/automation intervals; emergency timestamp convention + completion deadline; subtype fields; checklist contents; N/A taxonomy; acknowledgement fallback detail; Outstanding surfacing; offer latest-count; MOQ/quantity-break/pack; currency-conversion operations; PPN rate (11% example math only; source = future Tax/Accounting); retur-penggantian detail; transfer/reservation/opening-balance formal; approval-matrix technical detail; post-transition inventory architecture; formula/precision; retention windows; telemetry substrate; QR token/URL/rotation mechanics; OAuth/session mechanics; storage class. None blocks architecture approval; each blocks its dependent spec slice.

---

### 8. Classification E — Out of Scope

Explicitly outside CRM authority. Do not reopen. (Distinct from DEFERRED future scope: Full Finance/Accounting/Tax is DEFERRED per CD-01 — architecture must not foreclose it, but current-phase specs must not implement it.)

- Accounting journal; General Ledger; COA dependency; COGS posting; inventory valuation / stock valuation; costing engine / costing method (FIFO/Average/HPP/material/labor/service costing); landed cost; weighted average; valuation layers; cost allocation.
- Tax engine / tax accounting / tax ledger / filing / reconciliation; locked tax rates.
- AP / AR financial flows; payment workflow; AP aging; financial closing.
- Revenue recognition.
- Automatic acquisition calculation; automatic COGS; summed/aggregate stock value; Quantity × Unit Price totals (CD-04: no requirement); vendor ranking/recommendation/selection/"best vendor"; pricing engine / selling-price recommendation; automatic approval; automatic escalation/penalties/blocking; automatic reminder generation (baseline is manual).
- Reservation mechanism (CD-10 Q11 excludes); separate-DB / separate-port topology (CD-07 Q13 rejects); combined global transaction reporting (CD-07 Q16 prohibits); public-bucket-by-default file sharing; direct-filesystem-path serving; direct-URL-to-record QR; generic JSON/EAV component shortcut; cancel-and-recreate as post-completion correction; in-place overwrite of completed/closed records.

---

### 9. Security & Authorization Translation

Implementation requirements derived from canonical architecture (business rule → technical requirement). No mechanism finalized.

- **Identity:** Business: Google-only external sign-up/in; Google Identity ≠ Contact/PIC ≠ Verified PIC Link ≠ Company Access; sign-up alone grants no Company/PIC/Unit access; PIC registration = application → PENDING (supporting evidence may be requested, no fixed taxonomy); Manager/Admin approval establishes Verified PIC Link; email need not be company email; email/domain matching is NOT authorization. Technical: link-entity lifecycle (request → verify → revoke) separate from Contact; per-company VERIFIED/PENDING/REVOKED; lifecycle-bound sessions with revocation propagation; provider mechanics extensible (TADR-13).
- **Access:** Business: LOGIN ≠ COMPANY ACCESS; QR ≠ COMPANY ACCESS; Verified PIC Link → basis for Company Scope (sole basis — login, QR possession, company-name knowledge, prior unit views never yield it). Technical: three separated layers — authentication (who, TADR-13), authorization (what actions, action-level domain-policy checks composed with workspace guard), visibility (which fields/intelligence: Vendor Offer overlay + customer-safe filtering) (TADR-14).
- **Cross-company isolation:** Business: Verified PIC for Company A grants nothing for Company B; per-company states; no cross-company grant. Technical: scope-checked cross-aggregate references; Company Scope queries rooted at (verified-link × company); isolation violation = first-order security event with telemetry (TADR-06/13/14/18).
- **QR:** Business: no data without authentication — scanning without sign-in yields NO DATA (no preview); authenticated non-verified user yields restricted Unit Scope only (unit identity, owner company, address, work/material history; never PIC details/lists, other units, company-level data, or prices); Verified PIC of owner Company yields Company Scope; same QR across Unit/Invoice/Surat Jalan → same Unit. Technical: unguessable DB-backed indirection; permanent identity decoupled from rotatable secret; unit-rooted resolution making cross-unit browsing structurally impossible; scope-bound mediated serving; rotation/revocation lifecycle; abuse monitoring (TADR-16 + TADR-11/12/18).
- **Self-approval:** Business: applicant cannot approve own PIC application. Technical: verification authority distinct from creation; Google Identity and PIC status confer no approval authority; no auto-approval on submission; direct-URL/API bypass must not enable self-approval; approval/rejection/revocation events audited with actor + timestamp + company scope (TADR-13 + TADR-08/18).
- **Workspace + visibility hardening:** Application-level workspace guard on every path (allowlisted shared-master references only); Vendor Offer overlay toggles visibility without touching ownership/records/history/provenance; customer-safe exclusion list (internal notes, acquisition prices, vendor intelligence, internal/commercial info) + reviewer curation gate; file serving mediated + approved-only + unit-bound; projections enforce allowlist + unit scoping; logs must never contain prices/intelligence/notes/tokens/secrets; provider/observability secrets sealed (TADR-06/11/12/14/18).
- **Correction privilege:** REOPEN/CANCEL-class transitions restricted to Manager/Admin-class authority (role content itself business-owned, see C-3); no direct-edit path on completed/closed records (TADR-09/08).

---

### 10. Proposed Implementation-Specification Workstreams

PROPOSED labels only. NOT created, NOT approved. Grouping follows canonical seams (TADR-01 module map + TADR-02 aggregate map + CD ownership split). A better grouping is not justified at this stage — the task-suggested IS-01…IS-18 already mirrors the approved module/aggregate boundaries; the only adjustment is making the security/access spine explicit across IS-03/04/12 rather than a separate workstream (to avoid duplicating the LOCKED two-tier model).

- **IS-01 Workspace & Tenant Isolation** — one-platform/one-DB posture; guard + negative-test acceptance; usage-marker shape; numbering/reporting scoping.
- **IS-02 Company / Relationship / Contact** — Company identity; Prospect/Customer/Vendor roles; Contact 1-N; suggest/approve governance; lifecycle nonaktif/arsip; duplicate/merge business process interface.
- **IS-03 Identity & Verified PIC Link** — Google-only flow; application→PENDING→approval→VERIFIED; per-company states; revocation + session propagation; self-approval prohibition; evidence-request (taxonomy-free) handling.
- **IS-04 Authorization & Visibility** — three layers; action checks + workspace guard composition; Vendor Offer overlay administration; customer-safe filtering + reviewer curation; Unit vs Company Scope enforcement.
- **IS-05 Unit & Component** — asset registry; 1-WO-per-Unit binding rule; subtype placeholders (ENGINE/GENERATOR/BOX_CHASIS); replacement record (old/new/date/reason/relationship); registry-type deferral.
- **IS-06 Work Order Core** — request optionality; creation authority; lifecycle + guard matrix; assignment (1+0..N); CANCELLED boundary; emergency retroactive formalization (convention deferred).
- **IS-07 Service Execution** — Start Work + timestamps; execution-step containers kept content-agnostic pending F-1; **no spec writing until F-1 resolved** for F-1 mechanics.
- **IS-08 Findings / Checklist / Test / HM** — BEFORE/DURING/AFTER; Condition/Action; conditional Diagnosis/Recommendation; mandatory checklist/test with N/A+Reason principle; HM minimum; N/A taxonomy and contents deferred.
- **IS-09 Material Usage** — WO-side Item+Qty+Harga Perolehan per Unit; non-stock class; mutual references to inventory; reconciliation attention (non-blocking).
- **IS-10 Inventory Operation** — qty-only movements; receiving handoff; adjustment/opname discipline; negative-stock approval; status model; traceability fields; no reservation/valuation.
- **IS-11 Purchasing / PR / PO / Receiving** — PR optionality; PO lifecycle + immutability; per-event receiving with partial accept/reject; acquisition-event capture + versioned correction; vendor invoice as operational reference.
- **IS-12 QR / External Portal** — CONTROLLED flow; permanent unit-scoped indirection; two-tier resolution; customer-safe + no-price serving; same-QR identity rule.
- **IS-13 File / Photo** — evidence classes; condition-driven requiredness; review/publication states; immutable originals + replacement linkage; mediated scope-bound serving; derivatives pipeline.
- **IS-14 Audit / Versioning / Correction** — hybrid mechanism; mandatory trail fields; governed correction flows (WO + commercial/price); dual-time capture; tamper-evidence.
- **IS-15 Read Models / Reporting** — derived-only views (Unit/Customer/QR/Technician/Outstanding/Sales/Purchase/Inventory); hybrid freshness; source links; workspace-scoped reporting; no global transaction report.
- **IS-16 Notification / Background Jobs** — disabled-by-default framework; manual-reminder flows; idempotent/observable jobs; policy-flag gating; no enabled automation.
- **IS-17 Observability / Traceability** — telemetry scope; leakage prohibition; security-event classes; end-to-end traceability; retention/alert ownership deferred.
- **IS-18 Numbering / Document Identity** — per-workspace sequences; annual reset; immutability; no-reuse; syntax specification; revision-suffix conventions (quotation) and version chains.

---

### 11. Workstream Dependencies

Prerequisites; dependencies on other workstreams, on Human decisions, on F-1; independent-proceed assessment. No implementation tasks created.

| Workstream | Prerequisites | Depends on | Human-decision dependency | F-1 dependency | Can proceed independently? |
|---|---|---|---|---|---|
| IS-01 Isolation | CD-07/08, TADR-05/06 | IS-04 (guard composition), IS-18 (numbering) | Deployment ops context (C-6) for topology only, not for guard spec | None | Yes — guard + negative-test spec |
| IS-02 Company/Contact | CD-03, TADR-02/07 | IS-01, IS-14 (audit/correction) | Permission-matrix content (C-3) for enforcement completeness | None | Yes — identity/relationship spec |
| IS-03 Identity-Link | LOCKED identity gate, TADR-13 | IS-02, IS-14 (link audit) | Formal CD doc (C-12); evidence standard already LOCKED | None | Yes — lifecycle spec (mechanics = B) |
| IS-04 AuthZ/Visibility | Access Model LOCKED, TADR-14 | IS-01, IS-03, IS-12/13/15 (serving points) | Matrix content (C-3); visibility config (C-4); publication model (C-1) for customer tier | None | Direction yes; completeness gated by C-1/C-3 |
| IS-05 Unit/Component | CD-11 §4 (ACCEPTED), TADR-03 | IS-01, IS-02 | Subtype fields (C-7) | None for placeholders/binding; F-1 does not touch asset structure | Yes — placeholders + binding rule |
| IS-06 WO Core | CD-11 §§2,3,6,22,23 (ACCEPTED), TADR-04 | IS-01, IS-05, IS-14 | Retroactive convention (C-5); matrix content (C-3) | Partial: lifecycle skeleton yes; execution-step gates no | Skeleton yes; F-1-gated steps no |
| IS-07 Execution | CD-11 §§9,28 (ACCEPTED) | IS-06 | Retroactive convention (C-5) | **BLOCKED for F-1 mechanics** | Only content-agnostic containers |
| IS-08 Findings/etc | CD-11 §§10–12,16–18 (ACCEPTED) | IS-06/07, IS-13 | Contents + N/A taxonomy + acknowledgement evidence (C-8) | HM extras + photo slots blocked | Principle yes; content no |
| IS-09 Material | CD-04, CD-11 §13, TADR-10 | IS-06, IS-10, IS-14 | None (terminology locked) | None | Yes |
| IS-10 Inventory | CD-10, TADR-04/10 | IS-01, IS-14 | Approval-matrix detail (C-3); bin/location detail deferred | None | Yes |
| IS-11 Purchasing | CD-09, CD-04/06 | IS-01, IS-10, IS-14 | Approver lists, thresholds, templates (deferred) | None | Yes |
| IS-12 QR/Portal | CONTROLLED + Access Model LOCKED, TADR-16 | IS-03, IS-04, IS-05, IS-13/15 | Publication model (C-1) for served content | None | Mechanism spec yes; content gated by C-1 |
| IS-13 Files | CD-11 §§16,25, TADR-11 | IS-04, IS-06, IS-12 | Publication model (C-1) | Photo-slot model blocked (F-1) | Custody/serving yes; publication mechanics gated |
| IS-14 Audit/Correction | CD-08 + revision chains, TADR-08/09 | All transactional WS | Retention windows (B, planning) | None | Yes |
| IS-15 Views/Reporting | CD-11 §§24,25,26,28A,30, TADR-12 | IS-04, IS-06/09/10/11 | Snapshot-vs-live (C-1); Outstanding surfacing (C-10) | None | Internal views yes; customer/QR snapshots gated |
| IS-16 Jobs/Notify | CD-11 §27, TADR-15 | IS-15, IS-04 | Automation policy (C-2) to enable anything | None | Framework only; enablement gated |
| IS-17 Observability | TADR-18 | IS-14, IS-01 | Alert thresholds with business meaning (Human-owned) | None | Yes — scope spec |
| IS-18 Numbering | CD-05/07, platform | IS-01, IS-14 | None (syntax = B) | None | Yes |

Dependency map summary: IS-01/02/03/05/09/10/11/14/17/18 form the independently-speccable spine. IS-04/12/13/15 converge on C-1 (publication model). IS-16 converges on C-2. IS-06/07/08 converge on F-1 + C-5/C-8. No workstream requires CD-02, accounting, or implementation authorization to be specified.

---

### 12. Human Decision Register

Only genuine Human Authority items. Specification choices (§5) are not repeated here.

**HD-01 — Customer publication model**

- Topic: snapshot-vs-live expectation; publication/permission mechanism; customer-safe filtering/curation mechanism; Customer View aggregation implementation.
- Why architecture doesn't decide: TADR-11/12 approve hybrid direction on technical criteria only; business expectation of "what customer saw" vs live explicitly reserved (CD-11 §25/§33 + Finalization gates).
- Business impact: defines what customers are entitled to see and whether published history can change after the fact — evidentiary and trust commitment.
- Technical impact: determines snapshot infrastructure vs live queries, refresh/staleness policy, publication-state machine (partly blocking TADR-11/12, IS-12/13/15, IS-04 customer tier).
- What must be decided: live vs snapshot (or hybrid expectation per view); who can publish/unpublish; what curation actions exist.
- Prohibited until decision: publication-state mechanics, snapshot infrastructure, customer/QR served-content finalization beyond the LOCKED exclusion list + no-price rule.

**HD-02 — Reminder / automation policy**

- Topic: whether any automatic reminder generation exists; intervals; surfacing/escalation behavior.
- Why: CD-11 §27 locks manual baseline only; automatic generation + interval DEFERRED; TADR-15 disabled-by-default by design.
- Business impact: creates operational obligations and customer-contact commitments.
- Technical impact: gates enabling any auto job (IS-16); framework spec may proceed regardless.
- What must be decided: auto vs manual-only; if auto, which events and what intervals.
- Prohibited until decision: enabling/scheduling any automatic job; any SLA-like timer.

**HD-03 — Emergency retroactive timestamp convention (+ completion deadline)**

- Topic: ex-post declaration + reviewer validation convention; retroactive completion deadline (no numerical SLA currently locked).
- Why: CD-11 §§9/28 + §33 expressly defer; TADR-08 provides dual-time capture only.
- Business impact: determines evidentiary validity of emergency work performed before formal WO.
- Technical impact: event-time vs record-time precedence, validation workflow (IS-06/07/14).
- What must be decided: declaration format, reviewer validation criteria, completion deadline if any.
- Prohibited until decision: retroactive timestamp precedence logic; any deadline/escalation.

**HD-04 — Deployment operational context**

- Topic: business cost/operations-capacity context for topology selection.
- Why: no formal BD identifier; TADR-17 candidate-only by design; resourcing is Human input.
- Business impact: cost, availability, and operational-burden commitment.
- Technical impact: gates product/sizing/TLS/backup/hardening selection (IS-01/17 scope).
- What must be decided: budget, ops capacity, hosting constraints.
- Prohibited until decision: any provisioning/deployment/selection; any implementation-plan sizing.

**HD-05 — Business content inputs (checklist, N/A taxonomy, subtype fields, thresholds, acknowledgement evidence, Outstanding surfacing, service-type definitions)**

- Topic: checklist contents; exact N/A rules/taxonomy; ENGINE/GENERATOR/BOX_CHASIS field requirements; Minor/Major thresholds (if any); acknowledgement fallback evidence type; Outstanding surfacing rules; detailed service-type definitions.
- Why: CD-11 §§5/11/16/17/18/21/28A + §33 defer content while locking principles; TADR-03/04/12 use content-agnostic containers.
- Business impact: defines field-level work obligations and evidentiary standards.
- Technical impact: container shapes, validation rules, surfacing queries (IS-05/06/08/15).
- What must be decided: each content item by the business owner when needed; absence means containers stay empty.
- Prohibited until decision: inventing thresholds, mandatory fields, closed reason lists, SLA-like rules.

**HD-06 — Permission / visibility administration content**

- Topic: detailed RBAC matrix; approver lists; suggest/approve matrix; material-take authority; per-role Vendor Offer visibility settings.
- Why: CD-01 S3 + CD-08 + CD-06 Q8 reserve content as separate/ Admin-operated design; TADR-14 layering approved without content.
- Business impact: who may do/see what — authority delegation.
- Technical impact: enforcement completeness (IS-04); Admin toggle UX data model.
- What must be decided: matrix content and initial visibility settings.
- Prohibited until decision: hardcoding any permission matrix; assuming visibility defaults.

**HD-07A — Formal Documentation of Existing LOCKED Human Decisions**

Documentation/governance formalization only. No new business decision is created here.

- Topic: formal CD documentation for already-LOCKED Human decisions (identity-link reconciliation, QR CONTROLLED ACCESS, Business Access Model + self-approval invariant), as recorded in DECISION_REGISTER.md / TADRs / Baseline with formal CD documentation pending.
- Why: DECISION_REGISTER records LOCKED status but notes formal CD pending. This entry only tracks the documentation formalization; it does not decide business content.
- Rules covered (only as already established by canonical sources; not broadened): Identity-Link / PIC verification model; QR Access model (CONTROLLED); Business Access Model (Unit Scope / Company Scope + no-price rule + access invariants); Self-Approval Prohibition.
- Business impact: determines the documentary authority future specs cite.
- Technical impact: traceability citations; no mechanism change.
- What must be done: Human authorship/confirmation of the pending formal CDs.
- Prohibited until done: citing chat memory as canonical.

**HD-07B — CD-11 Status / Promotion Decision**

Genuine Human Decision. CD-11 is NOT promoted by this report.

- Topic: whether `CD-11 — Service Work Order Operational Boundary`, currently HUMAN-ACCEPTED, should later be formally promoted to LOCKED.
- Why: ARCHITECTURE_LOCK does not promote CD-11; HUMAN-ACCEPTED is not equivalent to LOCKED or FINAL.
- Business impact: determines the documentary authority future service specs cite.
- Technical impact: traceability citations; no mechanism change; no F-1 service-execution content is added or resolved here.
- What must be decided: Human decision on CD-11 promotion, if and when raised.
- Prohibited until decision: treating CD-11 as LOCKED; treating HUMAN-ACCEPTED as LOCKED.

No other Human decisions are manufactured. All §5 items remain specification choices for the future spec phase, not business gates.

---

### 13. Implementation Authorization Gate

> Technical Architecture approval does not equal implementation authorization.

The HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21) approves TADR-01…TADR-18 and the Architecture Baseline as canonical planning input. It authorizes nothing beyond documentation.

The following remain **prohibited** unless a later explicit Human authorization is provided:

```text
Coding
Schema finalization
Migration
API contract finalization
UI implementation
Deployment / provisioning
Programmer handoff
TASK-001 creation
```

No Programmer handoff exists. No TASK-001 is created by this report. Any Implementation Specification work (IS-01…IS-18 or any regrouping) requires a separate Human authorization gate after review of this report and HD-01 through HD-07B.

---

### 14. Traceability Matrix

| Area | Canonical Source | Current Rule | Classification | Future Spec Needed | Human Decision? | F-1 Dependency |
|---|---|---|---|---|---|---|
| Workspace | CD-07/08 LOCKED; TADR-01/05/06 | One platform/DB; no auto-movement; no global report | A (rules) / B (mechanics) | IS-01 guard + negative tests + marker shape | Ops context only (HD-04) | No |
| Company/Prospect/Customer/Vendor | CD-03 LOCKED; TADR-02/07 | Single identity; roles not masters | A / B | IS-02 aggregates | No | No |
| Contact/PIC | CD-03 LOCKED; TADR-02/07/13 | Separate 1-N; survives revocation | A / B | IS-02 | No | No |
| Google Identity | LOCKED gate; TADR-13 | Google-only; sign-up grants nothing; no email-match | A / B | IS-03 lifecycle + session mechanics | Formal CD (HD-07A) | No |
| Verified PIC Link | LOCKED gate; TADR-13 | Application→PENDING→approval→VERIFIED per-company; no cross-grant | A / B | IS-03 | Formal CD (HD-07A) | No |
| Authorization/visibility | CD-01 S3; CD-06 Q8; Access Model LOCKED; TADR-14 | Three layers; two tiers; invariants | A / B | IS-04 composition + matrix data model | Yes (HD-01/06) | No |
| Unit | CD-11 §4 ACCEPTED; TADR-02/07 | Asset parent; exactly-1 before COMPLETED/CLOSED | A (as ACCEPTED) / B | IS-05 | No | No |
| Components | CD-11 §4 ACCEPTED; TADR-03 | Subtype placeholders; no generic shortcut | A-principle / B-shape | IS-05 field spec | Yes (HD-05) | No |
| Work Order | CD-11 §§2,3,6,22 ACCEPTED; TADR-02/04 | Lifecycle; authority; CANCELLED boundary | A (as ACCEPTED) / B | IS-06 guards | Retro convention (HD-03) | Skeleton no; steps yes |
| Service execution | CD-11 §§9,28 + F-1; TADR-04 | Manual start; emergency formalization; convention deferred | D (F-1 items); A (canonical skeleton) | IS-07 (containers only) | F-1 gate (DEFERRED; no resolution authorized by this report) | **Yes — blocked** |
| Findings | CD-11 §§10,12 ACCEPTED | BEFORE/DURING/AFTER; Condition+Action; conditional Dx/Rx | A / B | IS-08 | No | No |
| Checklist/test/run | CD-11 §§17,18 ACCEPTED | Mandatory + N/A+Reason principle; exact rules deferred | A-principle / C-content | IS-08 | Yes (HD-05) | No (photo slots = F-1) |
| Hour meter | CD-11 §11 ACCEPTED (+F-1) | Minimum initial OR final; N/A+reviewer principle | A-minimum / D-extras | IS-08 | Exact N/A (HD-05) | PM/inspection extras yes |
| Participants | CD-11 §8 ACCEPTED | 1 Primary + 0..N Supporting | A / B | IS-06/08 | No | No |
| Materials | CD-04 LOCKED; CD-11 §13; TADR-10 | Item+Qty+Harga/Unit; non-stock class; non-atomic | A / B | IS-09 paired records | No | No |
| Inventory Operation | CD-10 LOCKED; TADR-04/10 | Qty-only; receiving→stock; controlled adjustment; no reservation | A / B | IS-10 | Matrix detail (HD-06) | No |
| Purchasing | CD-09 LOCKED; TADR-02/04 | PR optional; PO mandatory; per-event receiving | A / B | IS-11 | No | No |
| PR | CD-09 LOCKED | Skippable; reason-required cancel | A / B | IS-11 | No | No |
| PO | CD-09 LOCKED; TADR-04/09 | Lifecycle; Issued-immutability; revision correction | A / B | IS-11 | No | No |
| Receiving | CD-09 LOCKED; TADR-04 | Per-event; partial accept/reject; acquisition event | A / B | IS-11 | No | No |
| QR | CD-11 §26 ACCEPTED + CONTROLLED LOCKED; TADR-16 | Permanent unit-scoped; controlled flow; same-QR rule | A-policy / B-mechanics | IS-12 token/URL/rotation | Formal CD (HD-07A) | No |
| Files/photos | CD-11 §§16,25 ACCEPTED; TADR-11 | Condition-driven; curated; immutable originals; mediated serving | A-direction / B-mechanics | IS-13 (+HD-01 for publication) | Yes (HD-01) | Photo slots yes |
| Audit trail | CD-08 et al.; TADR-08/18 | Mandatory fields; tamper-evident; dual-time | A / B | IS-14 | No | No |
| Versioning | CD-04/05/06/08/09; TADR-08 | Hybrid; v1 preserved; usage pinned | A / B | IS-14 | No | No |
| Correction/revision | CD-11 §§22,23 ACCEPTED; CD-08; TADR-09 | REOPEN→CORRECTION→REVIEW→CLOSED; no overwrite | A (as ACCEPTED) / B | IS-14 | No | No |
| Read models/projections | CD-11 §§24,25,26,28A,30 ACCEPTED; TADR-12/07 | One history/multiple views; hybrid freshness; source-linked | A-direction / B-mechanics | IS-15 | Yes (HD-01 + surfacing HD-05) | No |
| Notifications/jobs | CD-11 §27 ACCEPTED; TADR-15 | Manual baseline; disabled-by-default framework | A-baseline / B-substrate | IS-16 | Yes (HD-02) | No |
| Observability | CD-08/11; TADR-18 | Full-spectrum; leakage prohibition | A-scope / B-substrate | IS-17 | Thresholds if business-meaningful | No |
| Numbering | CD-05/07 LOCKED | Per-workspace; annual reset; immutable; no-reuse; syntax open | A-rules / B-syntax | IS-18 | No | No |
| Reporting | CD-07 Q16; TADR-12/06 | Workspace-scoped; no global transaction report | A / B | IS-15 | No | No |
| External portal | Access Model + QR LOCKED; TADR-12/13/14/16/11 | Two tiers; customer-safe + no-price; mediated | A / B | IS-12 | Yes (HD-01) | No |
| Security boundaries | All LOCKED + gates; TADR-06/13/14/16/18 | Invariants (§9); isolation violation = security event | A | Cross-cutting in every IS | No | No |

CD-02 has no row (DEFERRED/UNVERIFIED, not reconstructed). Finance/Accounting/Tax full scope is DEFERRED future (not E); CRM-phase accounting semantics are E.

---

### 15. Risks / Ambiguities / Contradictions

1. **Path discrepancy (documentation, non-blocking):** Task §3 cites `docs/30-ARCHITECTURE/ARCHITECTURE_LOCK.md`, `DECISION_REGISTER.md`, `AI_CONTEXT_INDEX.md`; canonical locations are repository root (`ARCHITECTURE_LOCK.md`, `DECISION_REGISTER.md`, `AI_CONTEXT_INDEX.md`, plus `AI_OPERATING_RULES.md`). Root files were read as authority. Future task prompts should cite root paths to avoid confusion. No business impact.
2. **CD-11 status risk:** CD-11 is HUMAN-ACCEPTED, not LOCKED. Any spec or code that cites CD-11 service rules as "LOCKED" would be LOCKED-washing. Mitigation: every IS citing CD-11 must label it HUMAN-ACCEPTED until HD-07B resolves otherwise.
3. **Chat-LOCKED gates without formal CDs:** Identity-link, QR CONTROLLED, and Business Access Model are LOCKED Human decisions recorded in DECISION_REGISTER/TADRs/Baseline, but formal CD documents are pending. Risk of traceability erosion if specs cite chat memory. Mitigation: HD-07A formal documentation before spec authorization.
4. **F-1 misread risk:** F-1 is a deferred clarification, not a defect or a license to infer. Any spec that enforces arrival/GPS/state/HM-extra/photo-slot behavior before F-1 resolution would silently create business rules. Mitigation: IS-07/IS-08 F-1-gated slices stay as empty content-agnostic containers.
5. **Snapshot-vs-live + automation drift risk:** TADR-12/15 directions are technically sound only while publication/automation gates stay closed. Enabling snapshots on an assumed expectation or enabling any auto job before HD-01/HD-02 would be silent business-rule creation. Mitigation: disabled-by-default + publication mechanics gated.
6. **Offer-visibility vs workspace-visibility tension (apparent, not a contradiction):** CD-07 Q14 makes shared data auto-visible; CD-06 Q8 overlays Admin-configured role-based Vendor Offer visibility without changing ownership. Preserved as: general shared visibility default + Q8 overlay for offer price intelligence specifically. Spec must implement both, not collapse one into the other.
7. **No contradictions found** between LOCKED CDs and APPROVED TADRs at the rule level. Stale-line correction noted in Baseline §3 (TADR-13 "BLOCKED" line corrected to resolved reconciliation) is already handled; TADR-13 status is APPROVED with mechanics deferred.
8. **Accurate-5 reference risk:** Accurate 5 is reference/knowledge/existing authority during transition, never a runtime lock (CD-10) and never an automatic requirement source (CD-01 S4). Specs must not import Accurate parity requirements or stock-authority permanence.
9. **Scope-creep vectors:** Totals/aggregates (CD-04 R3 deferred, not prohibited forever), NET/FINAL pricing math, and reporting convenience are the most likely places for valuation/costing/journal leakage. TADR-10 terminology discipline + review checklists are the control; specs must carry explicit accounting-exclusion acceptance criteria.

---

### 16. Recommended Next Gate

**Descriptive recommendation only — no implementation action.**

Human Authority should review:

1. This preparation report for completeness, correct classification, and absence of invented requirements.
2. **HD-07A / HD-07B:** (a) HD-07A — whether to issue formal CD documents for the already-LOCKED gates (identity-link reconciliation, QR CONTROLLED ACCESS, Business Access Model + self-approval invariant) as documentation formalization only; (b) HD-07B — confirm CD-11 remains HUMAN-ACCEPTED (not LOCKED) going into spec phase unless the Human later promotes it.
3. **Sequencing decision:** Whether to (a) authorize independently-speccable workstreams first (IS-01/02/03/05/09/10/11/14/17/18 spine), while (b) holding publication-convergent specs (IS-04/12/13/15) pending HD-01, job enablement pending HD-02, and F-1-gated execution slices pending F-1 — or instead resolve HD-01/HD-02/F-1 first. Either path is architecture-consistent; the choice is a Human governance decision, not a technical inference.
4. **F-1 handling:** Confirm F-1 remains DEFERRED (no F-1 resolution has been authorized by this report), and that no spec work pre-decides it — or explicitly request F-1 clarification as a new business gate.
5. Only after the above: a separate, explicit Human authorization naming which IS workstream(s) may be specified, in what order, and under what acceptance criteria. That authorization — not this report and not the architecture approval — is the sole trigger for any Implementation Specification, schema, API, UI, migration, code, TASK-001, or Programmer handoff.

**STOP.** No Implementation Specification files created. No schema, API, UI, migration, code, TASK-001, or Programmer handoff produced or claimed. F-1 not resolved. Implementation readiness not claimed.

---

*Report based solely on canonical inputs listed in §2 under the authority order in the task brief. Historical code/DB/screenshots/prototypes treated as evidence only. Uncertainty, deferrals, and Human gates stated explicitly; nothing filled by technical plausibility.*
