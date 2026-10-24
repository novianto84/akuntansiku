# IS-01 — Domain & Data Model Specification

```text
Status: SPECIFICATION / IS-01 — ACKNOWLEDGED & ACCEPTED by HBA (2026-10-07, per HBA-DECISIONS-08); acceptance recorded; implementation still requires separate authorization
Workstream: IS-01 Domain & Data Model Specification
Authority: AI Manager / Lead Architect (specification author). Business Authority decides business rules;
  approved architecture is consumed, not modified.
Dependencies: IS-00 (governance); Level 1 business baseline (CD-01 FINAL/LOCKED, CD-03…CD-10 LOCKED,
  CD-11 SIGNED-OFF / LOCKED / CLOSED, locked human decisions per Decision Register);
  Level 2 approved architecture (Approval Package §1–§12, Baseline, TADR-01…TADR-18 APPROVED).
Date: 2026-09-22
Implementation prohibition: NO schema. NO tables/columns/types/keys. NO migrations. NO ORM models.
  NO API endpoints. NO code. NO UI implementation. NO Programmer TASK. NO database product selection.
  Completion of IS-01 does NOT authorize implementation.
```

> This document specifies the **business/domain model**: what business objects exist, what they mean,
> how they relate, who owns them, and what information must conceptually be represented.
> It does not specify how any of this is implemented.
> Where this document and a locked baseline conflict, the locked baseline wins.

---

## 1. Document Status

| Field | Value |
|---|---|
| Workstream | IS-01 Domain & Data Model Specification |
| Governance | `docs/40-SPECIFICATION/IS-00-is-specification-governance-master-plan.md` |
| Specification authority | AI Manager / Lead Architect (acceptance per IS-00 §7/§8) |
| Business authority | Human / BA (all business rules, all OPEN items) |
| Architecture authority | Approved direction consumed unchanged (TADR-01…TADR-18, Baseline, Approval Package) |
| Inputs | Level 1 + Level 2 (see §3); Level 3 evidence used for gap-spotting only |
| Downstream consumers | IS-02 (workflow), IS-03 (permission), IS-05/IS-07 (evidence/audit) — via CP-A entity/event inventory |
| Implementation | PROHIBITED by this document (see header) |
| Amendment log | 2026-09-25 — documentation reconciliation: OQ-01 closed and the §14 E-35 reconciliation note added (template axis REJECTED/unused). 2026-09-25 — five residual OQ-01 status references aligned (Step 5 finding S5-02). 2026-09-26 — wording reconciliation under documentation authorization: §14 E-35 pointer made current (OQ-01 closed), E-34 "WO type" phrase replaced, §14 conflict-note "§4.2" reference qualified to `IS-00` §4.2, and this log row added. |

Classification labels used throughout:

- `LOCKED` — explicitly established by a canonical source cited in Source.
- `DERIVED` — logical consequence of locked rules that changes no meaning; if disputable, it is OPEN instead.
- `OPEN` — requires a decision by the stated owner; never silently treated as decided.
- `CONFLICT` — sources disagree; flagged per IS-00 §10/§11, not resolved here.

---

## 2. Purpose

IS-01 answers: *"What business objects/entities exist, what do they mean, what relationships exist
between them, what lifecycle/ownership boundaries exist, and what business information must
conceptually be represented?"*

It exists so that IS-02 (lifecycle guards), IS-03 (permission matrix), IS-04 (contracts),
IS-05/IS-06 (evidence/projection), and IS-07 (audit) all reference the **same** entities,
ownership, and identity boundaries — instead of each redefining them.

It explicitly does NOT answer how the model is stored, served, or built (no tables, no endpoints,
no code, no product choices).

---

## 3. Source of Truth / Inputs

Documents actually inspected for IS-01:

| # | Document | How used |
|---|---|---|
| 1 | `docs/40-SPECIFICATION/IS-00-is-specification-governance-master-plan.md` | Governance, DoD, escalation, and workstream charter for IS-01 (read; author is this document's predecessor) |
| 2 | `docs/10-DECISIONS/CD-11-service-work-order-operational-boundary.md` | Read in full (561 lines). Primary business input for all Service-domain entities (§§1–32, CD11-001…CD11-029) |
| 3 | `docs/30-ARCHITECTURE/ARCHITECTURE_APPROVAL_PACKAGE.md` | Read in full (458 lines, §1–§12). Approved direction incl. domain boundaries, service/report/visit architecture, projection, evidence, access, SLA posture, TADR matrix, deferred list |
| 4 | `docs/30-ARCHITECTURE/ARCHITECTURE_BASELINE.md` | Read in full (195 lines). Business scope, canonical decision table, TADR summary, invariants, deferred business/technical lists |
| 5 | `DECISION_REGISTER.md` | Read in full. Decision status table (CD-01…CD-11), three LOCKED human decisions (identity-link, QR CONTROLLED ACCESS, Business Access Model), four UNRESOLVED gates, architecture approval record |
| 6 | `ARCHITECTURE_LOCK.md` | Read in full. Authority index confirming CD-11 SIGNED-OFF and architecture APPROVED; implementation NOT authorized |
| 7 | CD-01, CD-03, CD-04, CD-05, CD-06, CD-07, CD-08, CD-09, CD-10 | Read in full via structured extraction (status, entities, relationships, boundaries, deferred items per document). CD-02 confirmed absent — never reconstructed, never an input |
| 8 | TADR-01, 02, 03, 04, 07, 08, 10, 11, 12, 13, 14, 16 | Read in full via structured extraction. Remaining TADRs (05, 06, 09, 15, 17, 18) consumed via Approval Package §9 matrix + Baseline summaries (mechanism direction only; no domain content added beyond those summaries) |
| 9 | `AI_OPERATING_RULES.md`, `AI_CONTEXT_INDEX.md` | Operating and authority context |

Not used as authority: any code, schema, database content, `app.py`, Accurate 5 artifacts,
screenshots, chat memory, or industry practice (per CD-01/CD-03/CD-11 evidence clauses).

Terminology rule applied: newest canonical decision wins. CD-11 supersessions (§30) are honored;
superseded terms (`ASSIGNED` / `COMPLETED` as WO states, `ON PROCESS` as WO status, `FINAL` as
Visit Type, `SKIP_TEMPORARY`, `CLOSE_WO`, `CANCEL_*`, `Customer tidak meminta`, old outcome
DONE/CONTINUE/WAITING) do not appear as active concepts anywhere in this specification.

---

## 4. Domain Modeling Principles

**P-01 — Locked baseline wins (IS-00 §3, §11).** Every entity, relationship, and boundary traces
to Level 1/2 or is tagged OPEN/CONFLICT. Level 3 material never establishes a concept.

**P-02 — No invention (handover §4.1).** Gaps are labeled OPEN with an owner; convenient
assumptions are prohibited. `DERIVED` is used only where the consequence is direct and
meaning-preserving.

**P-03 — Logical model only (handover §4.3).** Entities are described by business meaning,
purpose, ownership, and conceptual relationships. No storage, type, key, index, or product
language appears. (Self-check: this document contains no DDL, no column, no ORM, no endpoint.)

**P-04 — Company is the identity root (CD-03 LOCKED; TADR-02/07).** Roles (Prospect/Customer/
Vendor) and Contacts attach to one canonical Company identity. No parallel Customer-Master vs
Vendor-Master identities.

**P-05 — Identity ≠ membership ≠ access (locked human decisions; TADR-13/14).** Google Identity,
Contact/PIC, Verified PIC Link, and Company Access are four distinct concepts. Authentication
(who) / authorization (what actions) / business visibility (which fields) are three separate
layers. No concept in this model merges them.

**P-06 — Unit is the asset parent; WO owns execution (CD-11 §5; TADR-02/07).** The Unit is the
parent asset. The WO is the operational owner of service execution — execution artifacts are
WO-owned, not Unit-subordinated. Neither side is collapsed into the other.

**P-07 — Strict component subtypes, no generic core (TADR-03 APPROVED; CD-11 §15).** Engine,
Generator, Box/Chassis are strict operational subtypes with subtype-specific structure. The core
model is not EAV/JSON/generic-bag; registry/future types stay spec-less until business
requirements exist.

**P-08 — One operational history, multiple contextual views (CD-11 §20; TADR-07/12).**
Projections (customer, QR, unit, technician, Outstanding) are derived, reference-never-duplicate,
read-only-by-construction views over one operational history. They are concepts in this model,
not separate stores.

**P-09 — Controlled curation, not actor-chosen visibility (CD-11 §§17, 18, 21; TADR-11/12).**
`photo_type` is contextual classification; publication control is `photo_type + approval_state +
policy_version` plus reviewer curation. No technician/customer self-selection of visibility exists
in this model.

**P-10 — Workspace owns transactions; identity/assets/intelligence are shared (CD-07/08 LOCKED;
TADR-01/06).** Every transactional entity carries workspace ownership; masters and price
intelligence are shared with governed modification (suggest + admin approval; immutable history).

**P-11 — Quantity-only operations; no financial semantics (CD-01/04/10/11).** The domain contains
operational quantities and operational price *references* (Harga Perolehan per Unit, Vendor Offer,
Final). It contains no journal, GL, valuation, costing, HPP/COGS, or tax engine concepts.

**P-12 — Deferred stays deferred (IS-00 §14).** Reminder/automation, publication mechanism,
retroactive-timestamp convention, deployment context, F-1 clarifications, subtype fields, N/A
taxonomy, checklist contents, and minor/substantive correction definitions appear here as OPEN
placeholders with owners — never as decided content.

---

## 5. Domain Landscape

Conceptual map (ownership in parentheses; detail in §6–§7):

```text
ORGANIZATION                    IDENTITY & ACCESS              ASSET
Company (identity root,         Google Identity (external)     Unit (asset parent, shared registry)
 shared master)                   → Contact/PIC (under         ├── Engine (strict subtype)
 ├── Prospect Role (relationship)   Company, shared)           ├── Generator (strict subtype)
 ├── Customer Role (relationship) → Verified PIC Link          ├── Box/Chassis (strict subtype)
 ├── Vendor Role (relationship)     (per-company lifecycle)    ├── Registry components
Workspace (transaction boundary)  → Company Access (derived)     (Pump/ATS/SyncPanel/Transformer,
                                                                   spec-less Phase 1)
                                Unit Location (separate
SERVICE (WO workspace-owned)      from Company address)
Service Request (optional)      EVIDENCE & EXECUTION (WO-owned)
Work Order (execution+lifecycle   Visit → Outcome / Findings / HM /
 owner; 1 WO = 1 Unit)              Checklist / Test-Run / Evidence /
 ├── Assignment (event,             Component Replacement
 │    1 Primary + N Supporting)   Report (1 per WO; consolidation)
 ├── Visit (1 WO → 1 R → N V)     Final Conclusion (draft → official)
 ├── Emergency lane (same WO,
 │    direct IN_PROGRESS)         CUSTOMER PROJECTION (derived,
 ├── Cancellation/Reopen/           reviewer-curated, gated)
 │    Re-create records            Customer Projection / QR View /
COMMERCIAL (workspace-owned)      Unit View / Outstanding overlay
Quotation → Sales Order         AUDIT (controlling, not log-only)
 → Fulfillment                    Correction cycles (numbered) /
PR → PO → Receiving                Approval history / Lineage
PRICE INTELLIGENCE (shared)       REFERENCE / REGISTRY
Vendor Offer → Acquisition        Item Master / Warehouse /
 Reference → Price History          Reason lists / Dynamic
Material Usage (WO-side) ↔          Configuration (governance
 Inventory Operation (inv-side)     concept, content deferred)
 non-atomic pair
```

Module-seam correspondence (TADR-01, informational only): Organization→Identity seam;
Contact/Link→Identity; Unit/Components→Asset; Service family→Service; Commercial family→
Commercial/Sales + Purchasing; Material/Inventory→Inventory; Offer/Reference→Price
Intelligence; Projection family→Visibility/Projection; Audit family→Platform (audit trail).

---

## 6. Entity Catalogue

For each entity: business meaning, purpose, lifecycle relevance, ownership/context, key conceptual
relationships, phase relevance, authority (`LOCKED` / `DERIVED` / `OPEN`), source.

### 6.1 Organization & workspace

**E-01 — Company.** The single canonical business identity (identity/master, not a giant table).
Purpose: anchor for roles, contacts, units, transactions, and access. Lifecycle: identity persists;
roles attach/detach over time. Ownership: shared master (CD-07/08). Relations: Company→Roles,
Company→Contacts (1-N), Company→Units, Company→Workspace-usage marker (shape OPEN). Phase 1
required. `LOCKED` (CD-03; CD-07 Q4; CD-08).

**E-02 — Prospect Role.** Business role/relationship on a Company (potential customer), not a
separate identity. Purpose: pre-customer pipeline identity. Ownership: follows Company; pipeline
activity workspace-owned (CD-07 Q15). Phase 1 required (as role concept; transition rules OPEN).
`LOCKED` as concept (CD-03); transition/detail `OPEN` (OQ-11).

**E-03 — Customer Role.** Business role/relationship on a Company; domain-separated from Vendor
role. Purpose: sales/service counterparty. One Company may hold Customer and Vendor roles
simultaneously (CD-03). Phase 1 required. `LOCKED` (CD-03).

**E-04 — Vendor Role.** Business role/relationship on a Company; domain-separated. Purpose:
purchasing counterparty; anchor for Vendor Offers. Phase 1 required. `LOCKED` (CD-03).

**E-05 — Workspace (Business Context).** The company-context boundary for transactions
(PKP vs Non-PKP are distinct workspaces on one platform, one database). Purpose: ownership,
numbering, template, approval, reporting, stock, and WO scoping. Relations: owns all
transactional entities; relates to shared masters via usage marker. Phase 1 required.
`LOCKED` (CD-07 Q1–Q3/Q10–Q16; CD-08).

**E-06 — Company↔Workspace Usage Marker.** Record that a shared Company is used by a workspace
("customer ini dipakai workspace ini"). Purpose: trace shared-master usage without duplicating
identity. Exact shape deferred (TADR-02 open question; CD-08 Q4). Phase 1 required as concept.
Concept `LOCKED` (CD-08 Q4); record shape `OPEN` (OQ-12).

### 6.2 Identity & access

**E-07 — Google Identity.** The external authenticated identity (Google-only sign-up/sign-in).
Purpose: prove *who* the external user is — nothing more. Lifecycle: independent of Company
membership. Ownership: external provider; referenced by link request. Relations: 1 external
identity → N link requests (one per Company); email/domain matching is NOT a requirement and
email need not be a company email. Phase 1 required. `LOCKED` (locked human decision; TADR-13).

**E-08 — Contact / PIC.** A person related to a Company (name, role/position, primary flag,
communication history), separate from Company and separate from any login. Purpose: business
person-record usable across roles (sales, purchasing, future customer access). Relations:
Company→Contact 1-N (CD-03); Contact→Verified PIC Link (link is separate so revocation never
tears relational history). Phase 1 required. `LOCKED` (CD-03; CD-08 shared).

**E-09 — Verified PIC Link.** The per-company access grant linking Google Identity → Contact/PIC
→ Company, with lifecycle states VERIFIED / PENDING / REVOKED. Purpose: the SOLE basis of
Company-level (COMPANY_SCOPE) access. Lifecycle: application → PENDING (supporting evidence may
be requested, no fixed taxonomy) → Manager/Admin approval → VERIFIED; revocation → REVOKED with
session propagation (mechanism deferred). Self-approval prohibited (applicant ≠ approver; only an
authorized internal Manager/Admin other than the applicant; no auto-approval). No cross-company
grant. Phase 1 required. `LOCKED` (locked human decisions; TADR-13/14; CD-11 §§21–22).

**E-10 — Company Access (derived).** The access consequence of E-09, not a stored grant: UNIT_SCOPE
(any authenticated user in QR context: unit identity, owner company, address, work/material
history; never PIC details/lists, other units, company-level data, or prices) vs COMPANY_SCOPE
(verified PIC only: all Units of that Company in the CRM + histories + PIC per customer-safe
visibility; never prices). Invariants: LOGIN ≠ COMPANY ACCESS; QR ≠ COMPANY ACCESS. Phase 1
required. `LOCKED` as semantics (locked human decision); tier mechanics `DERIVED` (TADR-12/14/16).

### 6.3 Asset

**E-11 — Unit.** The parent asset / business object (initial primary domain: genset; extensible to
other asset categories). Purpose: anchor for components, location, WOs, history, QR identity.
Lifecycle: registry lifecycle (incl. NEW-unit identification in the field → Manager/Coordinator
validation → official Unit Master; no fake Unit Master). Ownership: CRM-owned/shared registry
(CD-11 §25). Relations: Unit→Components, Unit→Location, Unit→WOs (each WO bound to exactly 1
Unit before CLOSED), Unit→QR identity (same QR on Unit/Invoice/Surat Jalan resolves to same
Unit). Phase 1 required. `LOCKED` (CD-11 §5; TADR-02/03/07).

**E-12 — Engine.** Strict operational component subtype of Unit with subtype-specific structure.
Purpose: carry engine identity (incl. serial number) and replacement history. No cross-subtype
field leakage. Phase 1 required (structure placeholders; field requirements OPEN). Architecture
`LOCKED` (TADR-03; CD-11 §§6, 15); field content `OPEN` (OQ-03).

**E-13 — Generator.** Strict operational component subtype of Unit (same treatment as E-12).
Phase 1 required. `LOCKED` architecture / `OPEN` fields (same sources).

**E-14 — Box / Chassis.** Strict operational component subtype of Unit (same treatment).
Phase 1 required. `LOCKED` architecture / `OPEN` fields (same sources).

**E-15 — Registry Components (Pump, ATS, Synchronizing Panel, Transformer).** Reference/registry
concepts in Phase 1 — NOT equivalent primary Unit component types. Purpose: future extensibility
without operational specification. No operational rules attach unless canonical documentation
explicitly says so. Registry/reference. Architecture `LOCKED` (TADR-03; CD-11 §15).

**E-16 — Unit Location.** The whereabouts of a Unit (location label, address text, optional
latitude, optional longitude) — conceptually SEPARATE from Company address. Purpose: field-service
routing/attendance context; never collapsed into Company address. Phase 1 required. `LOCKED`
(CD-11 §§10, 20 via check-in/location rules; handover-principle confirmed against CD-11 — no
merged-address concept exists in any canonical source).

**E-17 — Component Replacement.** The record of a replacement event: old component, new component,
replacement date, reason, replacement relationship. Purpose: preserve asset genealogy without
altering component architecture. Attached to subtype structures (TADR-03). Phase 1 required.
`LOCKED` (CD-11 §15).

### 6.4 Service

**E-18 — Service Request.** An OPTIONAL recorded request for service. Purpose: intake for
substantial new/regular work via `Service Request → Commercial/Approval → New WO` (not Add Job).
Lifecycle: independent of WO; a WO may exist with no Request. Ownership: workspace (service
transaction). Phase 1 required as concept. `LOCKED` (CD-11 §3).

**E-19 — Work Order (WO) / SPK.** The operational service record and execution+lifecycle owner:
canonical lifecycle DRAFT → OPEN → IN_PROGRESS → WAITING APPROVAL → CLOSED plus terminal
CANCELLED (CD11-001/010). Purpose: the single operational fact of a service job for exactly one
Unit. Creation postures: EXISTING UNIT / NEW UNIT / UNIT NOT YET DETERMINED (reason mandatory +
Manager/Coordinator approval; identity resolved before CLOSED). WO without Technician may sit in
OPEN (visible to Sales/Coordinator/Manager); IN_PROGRESS requires a responsible person.
Technician-created WOs follow the same lifecycle (auto-Primary; no separate category; no
auto-close). Phase 1 required. `LOCKED` (CD-11 §§2, 4, 5).

**E-20 — Assignment (event, not a state).** The responsibility allocation on a WO: exactly one
Primary Technician + zero or more Supporting, with equal operational rights (Primary = primary
accountability only). Purpose: answer "who is responsible" without a lifecycle state (there is no
`ASSIGNED` state; `UNASSIGNED` is a condition). Authority (`ASSIGN_WO`: default Manager +
Coordinator) is distinct from assignment itself; every change needs reason + audit. Includes
Manager Take Over (self-assignment with actor/action/timestamp/audit) and Technician Self-Add
(per-WO request → evidence → approval; refusal reason mandatory; never a profile relationship).
No permanent Customer–Technician relation exists. Phase 1 required. `LOCKED` (CD-11 §§2, 7, 8).

**E-21 — Emergency Lane (WO posture, not a separate WO type).** Technician-created WO going
directly to IN_PROGRESS with Minimum Critical Validation (Unit SN mandatory; Engine/Generator SN
mandatory *if applicable*; Before photo mandatory no-N/A; After photo mandatory no-N/A),
then standard WAITING APPROVAL → authorized approver → CLOSED; technician never approves
(including own WO); no auto-close. N/A is system-determined from Unit subtype; applicable-but-
unknown SN must NOT be N/A. Phase 1 required. `LOCKED` (CD-11 §6; CD11-004/028/029).

**E-22 — Visit.** One physical arrival = one Visit Record; multiple same-day arrivals are separate
records. Model: 1 WO → 1 Report → N Visits. Purpose: the operational source of execution truth.
Lifecycle OPEN → COMPLETED, SEPARATE from WO lifecycle (COMPLETED visit closes neither WO nor
Report; COMPLETED visits lock normally with controlled correction available). Any assigned
technician may create a Visit; creator auto-present; attendance per Technician; check-in/out per
Visit (both mandatory; server timestamp; GPS best-effort NULL-able, never blocking, never
fabricated). Phase 1 required. `LOCKED` (CD-11 §10).

**E-23 — Visit Type.** System-determined classification: INITIAL (first visit of a WO) /
ON PROCESS (second and subsequent visits). The technician never chooses it. `FINAL` is NOT a
Visit Type; `ON PROCESS` is never a WO status. Phase 1 required. `LOCKED` (CD-11 §10; CD11-017/025).

**E-24 — Work Outcome.** Per-Visit result: COMPLETED (all scope incl. checked Added scopes done +
check-out) / NOT_PERFORMED (reason mandatory from managed list, `Lainnya`→note mandatory;
administratively finished for that Visit; optional recommendation is a note only — creates no
task/WO, changes nothing) / ON HOLD (reason mandatory; obligation continues in the SAME WO;
WO stays IN_PROGRESS with "Ada pekerjaan ON HOLD" indicator; no HOLD workflow/states).
`SKIP_TEMPORARY` prohibited. Phase 1 required. `LOCKED` (CD-11 §11; CD11-013/026).

**E-25 — Reason (managed list + Lainnya + Keterangan).** The controlled vocabulary for
NOT_PERFORMED / ON HOLD (/ opt-out evidence) reasons via Dynamic Configuration. Canonical
defaults: NOT_PERFORMED — "Customer tidak mengijinkan" (the phrase "Customer tidak meminta" is
superseded and MUST NOT be used), "Tidak ada akses", "Kondisi lapangan", "Waktu tidak
mencukupi", "Lainnya"; ON HOLD — "Spare part belum tersedia", "Menunggu customer", "Kondisi
lapangan", "Masalah teknis", "Lainnya". Standard reasons need no note; `Lainnya` mandates
Keterangan. Phase 1 required. `LOCKED` defaults (CD-11 §11; CD11-024); list evolution
`DERIVED`-governed (via Dynamic Configuration, content future).

**E-26 — Scope Execution Checklist.** The work-scope record with states UNCHECKED / CHECKED only
(no IN_PROGRESS state). Purpose: scope truth without per-action Activity entities (there is NO
Activity entity per technician action). Partial work lives in Visit notes/findings; scope stays
UNCHECKED until truly done; scopes span visits; CHECKED stays CHECKED under retest (retest logged
on the next Visit). No per-technician attribution (`Recorded by`, never `Completed by`).
Phase 1 required. `LOCKED` (CD-11 §§8, 12).

**E-27 — Add Job (Added During Execution).** Minor work discovered/performed during execution only —
never substantial/regular/new work (that path is Service Request → new WO). Carries `Added During
Execution` + `Added by` + `Added at` (administrative timestamp; no execution timestamp in Phase 1);
entry via existing work category where available else free description; `Sudah dikerjakan?`
YA→CHECKED / TIDAK→UNCHECKED; same evidence rules as normal scope; all Added scopes must be
CHECKED before Visit Outcome DONE/COMPLETED. Phase 1 required. `LOCKED` (CD-11 §12).
*Terminology alignment (BD-WORKTYPE-001 Rev.A, APPROVED / CANONICAL 2026-09-23): read "Add Job"
above as JOB + Added During Execution marker (actually performed only); the `TIDAK → UNCHECKED`
branch records a scope entry yang belum CHECKED only — see `docs/10-DECISIONS/CD-11-Appendix-A-job-scope-terminology.md`.
Historical E-27 wording is preserved; no entity or rule is altered by this note.*

**E-28 — Finding (Before / During / After).** Mandatory observations for all Service Types:
Condition + Action always required; Diagnosis required on abnormality/failure/troubleshooting;
Recommendation required where follow-up should be suggested (never fabricated). Purpose: the
clinical record distinguishing observation phases. Phase 1 required. `LOCKED` (CD-11 §13).

**E-29 — Hour Meter (HM) Record.** The technician-reported meter reading stored on the Visit
record + audit trail, captured once per Visit (not a mandated start+end pair; capture point
follows workflow/template). Minimum one HM (initial/start OR final/end) must exist; relevant +
available → mandatory; unavailable/irrelevant → `N/A` + open reason with reviewer validation
(never a free pass; never silently zero). HM is NOT an emergency critical gate. Phase 1 required.
Rule `LOCKED` (CD-11 §14; CD11-015); exact N/A rules `OPEN` (OQ-04; F-1).

**E-30 — Checklist & Test/Run Record.** Mandatory execution artifacts for all Service Types; where
impossible: `N/A + Reason` with reviewer validation. Purpose: prove execution completeness.
Exact N/A rules and checklist contents follow later decisions — not invented here. Phase 1
required as concept. Existence `LOCKED` (CD-11 §13); contents `OPEN` (OQ-04; F-1).

**E-31 — Evidence / Photo.** Event/condition-driven artifacts (mandatory: nameplate, hour meter,
before, after; conditional: during, replaced component, damage, test result) — NOT globally
mandatory: on CHECKED scope the field appears but upload is optional with `No Evidence / Opt Out`
+ mandatory reason. Requirements configurable via Dynamic Configuration. `photo_type` is
contextual classification ONLY (single retention rule for all evidence; no Before/During/After
retention lifecycles). Publication control is `photo_type + approval_state + policy_version` +
reviewer curation; the technician never selects visibility; non-eligible evidence stays stored
and internally visible per permission, never on the Customer Report. Recognized critical evidence
floor: unit/engine/generator serials, before-service and after-service condition. Phase 1
required. `LOCKED` (CD-11 §17; CD11-014/016); additional critical categories `OPEN` (OQ-05).

**E-32 — Report.** The per-WO consolidation: Hybrid Summary (WO, Company/Customer, Unit,
type/template, Work Scope Summary, Findings, Work Result, Parts/Materials, eligible Evidence,
Final Conclusion) + Visit History (visit no., date, attendance, check-in/out, outcome, visit
summary) — with NO manual duplication by the technician (Visit = source, Report = consolidation).
Finalization: NON-FINAL → FINAL ONLY on WO CLOSED (Visit COMPLETED, Outcome DONE,
WAITING APPROVAL, CORRECTION_REQUIRED never finalize; no FINALIZE REPORT action; no automatic
per-correction revisions; corrections refresh from current Visit data). Exactly 1 Report per WO.
Phase 1 required. `LOCKED` (CD-11 §§10, 18, 20; CD11-017/019/020).

**E-33 — Final Conclusion.** The official result statement: technician drafts → approver
accepts/corrects/establishes → the approved version at approval time is the official conclusion.
History preserves draft, modification, final, actor, timestamp. The technician can never set it
unilaterally. Phase 1 required. `LOCKED` (CD-11 §18; CD11-018).

**E-34 — Service Type.** The work classification: PM; Inspection/Troubleshoot; Emergency Service;
Minor Service; Major Service; Commissioning/Testing. Conceptual bounds LOCKED: PM =
planned/preventive; Inspection/Troubleshoot = investigation/diagnosis (may do minor repair if
parts available; the WO classification does not change); Minor/Major = small/large repair; Emergency = emergency/
urgent situation (a TYPE, not a flag); Commissioning/Testing = commissioning/testing work.
Installation and Corrective Repair are NOT separate types. No duration/hour thresholds locked;
detail definitions follow. Phase 1 required. Values `LOCKED` (CD-11 §16); thresholds/detail `OPEN`.

**E-35 — Workflow Template (handover-claimed; UNVERIFIED).** The handover prompt (§6) asserts
approved templates `FULL_SERVICE` / `INSPECTION_ONLY` / `EMERGENCY`. No such names were found in
any canonical document inspected (CD-11 speaks of "template-scoped visit structure" CD11-019 and
"tipe/template WO" without naming templates; see §3 verification grep). Therefore these template
names are classified `OPEN` — IS-01 neither adopts nor rejects them; the BA decision was raised as
OQ-01 and is closed 2026-09-25 (documentation reconciliation — see the note immediately below).
Claiming them as LOCKED would itself be invention.

*Documentation reconciliation 2026-09-25 (OQ-01 closed):* the template axis is answered by
existing approved decisions — `BD-WORKMODEL-001` §8/§10 (template axis closed as
REJECTED/unused; no template names adopted) and `AB-01` ("No third workflow/template axis"; no
template dimension). The CD-11 phrasings referenced above ("template-scoped visit structure",
"tipe/template WO") remain unchanged and are recorded as a documentation-only reconciliation
item in `docs/90-AUDIT/UI-BASELINE-APPROVAL-AND-RECONCILIATION-RECORD.md`. No template name,
alias, entity, Visit Type, or third classification axis is adopted by this clarification.

**E-36 — Cancellation Record.** The governed cancellation case: OPEN/IN_PROGRESS → request +
notes (Sales/Technician, reason + notes) → Manager attention/inbox (reason validation) →
authorized Admin/Manager execution → terminal CANCELLED (default authority Admin + Manager,
configurable). CLOSED can never be cancelled; CANCELLED can never be cancelled again or
REOPENed. No Approve/Reject buttons, no `CANCEL_*` states. WO/history/report are never deleted;
investigation support is attention/category/notes/history/audit only (no investigation workflow
Phase 1). Mandatory trace: requester, reason/notes, reviewer/attention, executor, timestamp,
audit trail. Phase 1 required. `LOCKED` (CD-11 §9; CD11-010).

**E-37 — Reopen / Re-create Lineage.** Post-CLOSED governance: REOPEN applies to CLOSED only
(back to IN_PROGRESS; same number/Report; assignment restored; SLA history preserved; multi-cycle
allowed Phase 1) vs RE-CREATE (new WO/number/Report/history with `CREATED_FROM` lineage; no
automatic assignment carry; Company kept; Unit may change). Correction history is controlling
data with numbered cycles (count unlimited — no technical maximum). Phase 1 required. `LOCKED`
(CD-11 §§2, 28; CD11-006/007/008).

### 6.5 Material, inventory, price intelligence

**E-38 — Material Usage (WO-side).** The operational record on a WO: Item + Quantity + Harga
Perolehan per Unit — with NO quantity×price computation, NO totals, NO valuation, NO accounting
(no journal). Flow take → stock-out → WO record is deliberately NON-atomic (paired independent
records with mutual reference + attention-only reconciliation for dangling halves; no background
auto-resolution). Non-stock / customer-owned / direct-purchase usage is a first-class class with
NO linked movement and NO phantom stock entry. Follows the WO's workspace. Phase 1 required.
`LOCKED` (CD-11 §§25, 26; CD-04 R2; TADR-04/10).

**E-39 — Inventory Operation (inventory-side).** The workspace-owned stock movement record
(item, qty, direction, source, time, workspace, reference document, actor, reason where
adjustment) under quantity-only authority: no reservation, no valuation/costing/HPP/COGS/journal,
no FIFO/Average, no formal opening-stock mechanism; stock decreases on WO take; sources are
receiving, adjustment, customer return, technician return (conceptual transfer; inter-warehouse
transfer not needed Phase 1); statuses AVAILABLE vs DAMAGED/QUARANTINE; one warehouse (bin
deferred); negative stock only with approval; opname → compare → adjustment as needed; item/
location/warehouse lifecycle AKTIF–NONAKTIF–ARSIP with history preserved. References but never
controls Material Usage. Phase 1 required. `LOCKED` (CD-10; TADR-10).

**E-40 — Inventory Item (Item / Spare Part Master).** The shared item identity (global master;
stock balances and movements stay per-workspace). Purpose: anchor for offers, acquisition
references, material usage, and movements. Modification via suggest + admin approval; used items
deactivate/archive, never hard-delete; no automatic duplicate matching (business process + merge
where proven). Registry/reference + Phase 1 required. `LOCKED` (CD-07 Q6; CD-08; CD-01 S5).

**E-41 — Vendor Offer (Harga Penawaran).** Shared sales intelligence: one offer = one original
price + one basis (EXCLUDE_PPN / INCLUDE_PPN / NET_FINAL; NET_FINAL ≠ EXCLUDE_PPN) → three
representations (Exclude/Include/Final; for NET/FINAL only Final is filled) — never three
independent prices. Generic math `Include = Exclude × (1 + Rate)`; the PPN rate itself is NOT
locked (example 11% is math only; rate source is future Tax/Accounting). Corrections are new
records/versions (v1 preserved; usage links the version used); lifecycle ACTIVE → INACTIVE →
ARCHIVED without destructive deletion. Sales use: factual comparison on Final + original context
shown; no ranking/recommendation/"best vendor"; offer is a quotation reference, never automatic
selling price; no pricing engine. Cross-workspace visible; per-role visibility dynamically
controlled by Admin `Access / Visibility Policy → Vendor Offer` WITHOUT changing ownership/
sharing/records/history/acquisition/provenance (Q8 FINAL). Phase 1 required. `LOCKED` (CD-06;
CD-08); latest-N count, MOQ/quantity-break, currency conversion `OPEN` (OQ-13).

**E-42 — Acquisition Price Reference (Harga Perolehan).** The shared operational reference of
actual procurement events (per item/vendor, plural, immutable, shared) — explicitly NOT book
value, NOT valuation. Purpose: provenance-carrying reference for material usage. Corrections are
new versioned records (old preserved). Phase 1 required. `LOCKED` (CD-04 R1; CD-06; CD-08).

**E-43 — Price History / Provenance.** The immutable chain per price fact: vendor, item, original
price, basis, derived/final, currency (original kept), unit, effective date, validity, source,
version/correction links, usage links. Purpose: audit-grade price genealogy. Shared intelligence
(price ever offered/obtained) is distinct from workspace activity (workspace W used price X on
document Y). Phase 1 required. `LOCKED` (CD-06; CD-08 Q8/Q16).

### 6.6 Commercial (sales / purchasing)

**E-44 — Quotation.** The workspace-owned sales offer document: lifecycle
DRAFT → OPEN → PARTIALLY_CONVERTED → CLOSED (no separate REVOKED state). Partial conversion
allowed (selected items convert; remainder stays outstanding; further conversion possible; history
traceable). Full item conversion auto-closes (CLOSED, closure_reason=COMPLETED, no approval, not
waiting for fulfillment/delivery/service/invoice/accounting). Manual close = Sales request +
mandatory reason + mandatory Manager/Admin approval → CLOSED with reason + approval history kept.
CLOSED is terminal (never reopens; number never reused). Negotiation revisions are NEW
documents/versions (same base number + suffix/version; prior revision immutable; lineage
traceable). PPN informative/reference only. Cross-workspace transactions prohibited; numbering/
reporting workspace-specific with annual reset. Phase 1 required. `LOCKED` (CD-05).

**E-45 — Sales Order (SO).** The workspace-owned order: from a Quotation (price may differ/
override) or standalone (quotation optional; no mandatory predecessor pipeline/activity/
reference). Requires no approval. Phase 1 required. `LOCKED` (CD-05 Q3 + Sales Order).

**E-46 — Fulfillment.** The workspace-owned SO fulfillment record: multiple/partial supported;
remainder stays outstanding/backorder (never auto-completed); NEVER mutates inventory and creates
NO reservation (Accurate 5 remains current stock authority; no FIFO/valuation from this concept).
Phase 1 required. `LOCKED` (CD-05 Q2).

**E-47 — Purchase Request (PR).** The OPTIONAL purchase-need record (initiators: Technician,
Coordinator, Sales, Manager, Purchasing, Admin). Emergency purchasing may skip PR (still needs PO
+ receiving + emergency reason) — and emergency purchasing ≠ emergency service. Permission detail
deferred. Phase 1 required as concept. `LOCKED` as optional concept (CD-09); nominal
thresholds/approver detail `OPEN`.

**E-48 — Purchase Order (PO).** The mandatory vendor-purchase record: lifecycle
Draft → Issued → Received → Completed; official at Issued; IMMUTABLE after Issued
(change/cancel via revision). May reference a Vendor Offer (price negotiable/different) or none.
Mirrors SO-standalone: PO may exist without PR. Price follows PO rules; acquisition price
corrected at receiving when actual differs. Phase 1 required. `LOCKED` (CD-09).

**E-49 — Receiving.** The per-event workspace-owned receipt record for one PO: partial supported
(6 now + 4 later); remainder outstanding without auto-complete; accept/reject recorded separately
(accept 8 + reject 2 damaged; replacement/return follows). Valid receiving adds stock immediately;
receiver inputs price data; old records immutable. Phase 1 required. `LOCKED` (CD-09).

**E-50 — Acquisition Event.** The moment goods are received AND actual price is available: the PO
price (initial basis) is corrected by versioned record when receiving price differs. Purpose: the
birth event of Acquisition Price References. Phase 1 required. Concept `DERIVED` from CD-09 +
CD-04 (no new rule: it names the intersection both documents already describe).

### 6.7 Projection, history, governance

**E-51 — Customer Projection (derived view concept).** The customer-safe, reviewer-curated,
eligibility-gated derivative of operational history — NEVER a second store. Content allowlist:
date, technician, summary/work performed, approved photos, replaced component, material quantity
only where agreed/appropriate, recommendation. NEVER included: internal notes,
correction/cancellation/administrative reasons, acquisition price, vendor intelligence, any other
internal/commercial information. No prices in ANY form on the external portal. No-download honored
(mechanism deferred). Business expectation **RESOLVED — HBA D-01A = RETAIN** (previously presented
customer-facing content remains available as the historical record); freshness is a **semantic
requirement (D-01B)** with no numeric SLA; serving/snapshot **mechanism** remains architecture. Phase 1 required as concept. Allowlist/exclusions `LOCKED`
(CD-11 §§20, 21; CD11-020/021; TADR-12); mechanism `OPEN` (OQ-06).

**E-52 — QR Identity (unit-rooted access concept).** The permanent, unit-scoped identity printed
for a Unit (same QR on Unit/Invoice/Surat Jalan resolves to the same Unit — no separate
invoice/delivery scope). Purpose: entry point to the QR View under CONTROLLED ACCESS
(SCAN QR → SIGN UP/SIGN IN Google-only → CHECK ACCESS → UNIT DATA; NO anonymous access, not
even preview). Serves UNIT_SCOPE to authenticated non-PIC, COMPANY_SCOPE to verified PIC;
never prices/internal data; cross-unit browsing structurally impossible. Phase 1 required.
`LOCKED` (CD-11 §22; locked QR decision; TADR-16); token/format/rotation mechanics deferred
(TADR-16, not domain content).

**E-53 — Outstanding (monitoring overlay).** The attention/monitoring concept over WOs (incl.
ON HOLD indicators) — explicitly NOT overdue/SLA/escalation/blocking. Numeric SLA, H-1, overdue
computation, and escalation automation are DISABLED Phase 1 (old SLA values are future-reference
history only). Timestamps/history persist as audit properties (incl. across REOPEN). Manual
reminder (Admin/Manager/Sales) is the baseline; automatic generation + intervals are not locked.
Phase 1 required as concept. `LOCKED` (CD-11 §§11, 20, 23; CD11-011; TADR-15); surfacing rules `OPEN`.

**E-54 — Correction / Approval / Lineage Records (controlling data).** The governed-trail family:
every correction/cancellation/reopen/re-create captures actor, server timestamp, action, object,
reason, before/after where relevant; correction history is CONTROLLING data with numbered cycles
(unlimited); approval chain (review mandatory pre-CLOSED; re-CLOSED binds reviewer identity;
technician never approves; self-approval prohibited); official-result chain (draft → modification
→ final → approved); reopen lineage (same identity) vs re-create lineage (`CREATED_FROM`, new
identity); the single business-locked direct-edit sideroute (reviewer EDIT during WAITING
APPROVAL with mandatory reason + full audit linkage; no direct edit on CLOSED). Distinction
minor vs substantive correction: business definitions NOT invented here. Phase 1 required.
`LOCKED` (CD-11 §§2, 28; CD11-006/007/008/012; TADR-08/09).

**E-55 — Reminder (manual baseline).** The human-issued follow-up record (Admin/Manager/Sales).
Automatic behavior is disabled Phase 1 (see E-53). Phase 1 required as manual concept;
automation `OPEN` (OQ-07).

**E-56 — Dynamic Configuration (governance concept).** The business-owned configurability domain
referenced across CDs: reason lists, evidence requirement configurability (type/field/workflow),
visit check-in method, cancellation authority, `CREATE_WO`/`ASSIGN_WO`/Self-Add approval grants,
N/A validation, Vendor-Offer visibility policy. Purpose: name WHERE variability lives without
deciding any value. Every value/content inside is deferred design detail. Existence-as-concept
`DERIVED` (it names the union of configurability clauses in CD-05/06/09/11 + Approval Package
§10); all contents `OPEN`.

**E-57 — Warehouse / Stock Location (operational context).** One warehouse; bin/detail deferred;
workspace-owned stock; inter-warehouse transfer not needed Phase 1. Registry/reference.
`LOCKED` as boundary (CD-10 Q9–Q10/Q15–Q16); detail `OPEN`.

Entity count: 57 numbered concepts (E-01…E-57) across 7 families. No storage, type, key, or
product language is used for any of them.

---

## 7. Relationship Model

Notation: `A → B (cardinality)` = conceptual association as established. Each entry carries
lifecycle dependency and authority. Cardinality stated ONLY where a canonical source establishes
it; otherwise explicitly "not established".

**R-01 — Company → CompanyRole (Prospect/Customer/Vendor).** One Company carries zero or more
roles; Customer + Vendor may coexist on one Company; no dual identities (Customer-ABC vs
Vendor-ABC prohibited). Lifecycle: roles attach/detach; identity persists. `LOCKED` (CD-03).

**R-02 — Company → Contact/PIC (1-N).** One Company has multiple Contacts/PICs (CD-03 §Contact:
`Company └── Contact/PIC 1-N`). Contact lives at Company-identity level, usable across roles;
contact workspace-specific context OPEN. `LOCKED` cardinality + placement (CD-03); workspace
context `OPEN` (OQ-12).

**R-03 — Google Identity → Contact/PIC → Verified PIC Link → Company.** Chain of four DISTINCT
concepts (never merged). One external identity may hold links to multiple Companies — strictly
one link-state machine per Company (VERIFIED/PENDING/REVOKED), no cross-company grant. Lifecycle:
link application → PENDING → approval → VERIFIED; revocation → REVOKED without tearing Contact
history. `LOCKED` (locked identity decision; TADR-13).

**R-04 — Company → Unit (ownership context).** Units are the shared/CRM-owned registry used by
Companies; the Company↔Workspace usage marker (E-06) records which workspace uses which Company.
Whether a Unit is "owned by" vs "serviced for" a Company is a usage context, not a second
identity. `LOCKED` as registry posture (CD-11 §25; CD-08); per-unit commercial ownership detail
`OPEN` (OQ-11).

**R-05 — Unit → Component (1 Unit → strict Engine/Generator/Box-Chassis subtypes).** Parent-child
with subtype-specific structures; replacement events (E-17) attach per subtype. Registry types
(E-15) are not operational children in Phase 1. Lifecycle: components replaced, never silently
mutated (old/new/date/reason/relationship). `LOCKED` (TADR-03; CD-11 §15).

**R-06 — Unit → Unit Location (1-1 conceptual).** Each Unit has its own location, separate from
Company address. Coordinates optional. Cardinality `DERIVED` (one whereabouts per asset is the
direct reading of "Unit location … separate from Company location"; no source states two
concurrent locations — if contested, OPEN).

**R-07 — Service Request → Work Order (0/1 → N, optional).** A WO may reference at most one
originating Request path; most WOs have none (Request optional). Substantial work follows
Request → Commercial/Approval → New WO. Lifecycle: Request independent; WO lifecycle unaffected
by Request state. Cardinality upper bound `DERIVED` (one intake path per WO follows from "pekerjaan
reguler/baru … via Service Request → … → New WO (bukan Add Job)"; multiple-request merge is OPEN).
Base optionality `LOCKED` (CD-11 §3).

**R-08 — Work Order → Unit (N WOs → exactly 1 Unit, bound before CLOSED).** 1 WO = 1 Unit.
Creation postures EXISTING / NEW (field-identified → validated → officialized; technician never
creates the official master) / NOT YET DETERMINED (reason + approval; resolved before CLOSED).
No fake Unit. Lifecycle dependency: CLOSED requires binding. `LOCKED` (CD-11 §5; CD11-004).

**R-09 — Work Order → Visit (1 → N).** Via exactly 1 Report (R-10): 1 WO → 1 Report → N Visits.
Visits never exist without their WO; Visit COMPLETED never closes WO/Report. Lifecycle: Visit
OPEN → COMPLETED independent of WO lifecycle. `LOCKED` (CD-11 §§10, 18).

**R-10 — Work Order → Report (1 → exactly 1).** One consolidation per WO; no per-correction
revisions Phase 1; Report FINAL iff WO CLOSED. `LOCKED` (CD-11 §18; CD11-020).

**R-11 — Report → Visit (1 → N, consolidation, not duplication).** Report references Visit
records (history section) and summarizes them; technician enters nothing twice. `LOCKED`
(CD-11 §18; TADR-12).

**R-12 — Visit → Outcome / Findings / HM / Checklist-state / Test-Run / Evidence (1 → N each).**
The Visit is the collection point of all execution facts (E-24, E-28…E-31). Lifecycle: facts
frozen with Visit COMPLETED (controlled correction only). `LOCKED` as collection role (CD-11
§§10–14, 17, 20); per-fact optionality per evidence/HM rules.

**R-13 — WO → Assignment (1 WO → 1 Primary + 0..N Supporting, as events).** Equal operational
rights; Primary = accountability. Changes require `ASSIGN_WO` + reason + audit; allowed unless
WO is CLOSED/CANCELLED. `LOCKED` (CD-11 §§2, 7).

**R-14 — Contact/PIC → Verified PIC Link (1 contact → N per-company links).** Link is a separate
concept so revocation preserves Contact + relational history. `LOCKED` (TADR-13; CD-11 §§21–22).

**R-15 — WO → Material Usage (1 → N) ↔ Inventory Operation (paired, non-atomic).** WO-side usage
records reference inventory-side movements and vice versa; neither controls the other; dangling
halves surface as attention (never auto-resolved, never blocking). Non-stock class has no
counterpart. `LOCKED` (CD-11 §26; CD-04; TADR-04/10).

**R-16 — Quotation → Sales Order (1 → N, partial).** Selected items convert; remainder
outstanding; further conversion allowed; history traceable. SO-standalone allowed (no mandatory
predecessor). `LOCKED` (CD-05 Q1/Q3).

**R-17 — Sales Order → Fulfillment (1 → N, partial/additive).** Remainder outstanding/backorder;
never auto-completed; never touches inventory. `LOCKED` (CD-05 Q2).

**R-18 — PR → PO (0/1 → 1, optional).** PO may exist without PR; emergency may skip PR (PO +
receiving + reason still required). `LOCKED` (CD-09).

**R-19 — PO → Receiving (1 → N per-event).** Partial + split accept/reject; remainder
outstanding; no auto-complete. `LOCKED` (CD-09).

**R-20 — Receiving → Inventory Operation (causal, separately recorded).** Valid receiving is the
stock-add cause (E-39), recorded as its own movement — paired-pattern, not a single record.
`LOCKED` (CD-09 handoff principle; CD-10 Q2; TADR-04).

**R-21 — Receiving → Acquisition Event → Acquisition Price Reference (versioned correction).**
PO price is the initial basis; receiving-time actuals correct by new version. `LOCKED` (CD-09
Acquisition; CD-04 R1).

**R-22 — Vendor Role → Vendor Offer (1 → N, versioned) → Price History.** Offers version
(ACTIVE → INACTIVE → ARCHIVED); usage links the version used; offer ≠ acquisition price.
`LOCKED` (CD-06).

**R-23 — Unit → QR Identity (1 → 1 conceptual).** One permanent unit-scoped identity per Unit;
same QR across Unit/Invoice/Surat Jalan. Token/format mechanics are NOT domain content
(deferred, TADR-16). Identity-per-unit `LOCKED` (CD-11 §22; TADR-16).

**R-24 — Operational History → Projections (1 history → N derived views).** Unit View
(unit-scoped), Customer View (per-customer aggregate; each entry tied to its own Unit), QR View
(unit-scoped), technician/Outstanding overlays. Views reference, never duplicate; customer/QR
views additionally gated (E-51). `LOCKED` as one-history/multiple-views (CD-11 §20; TADR-07/12).

**R-25 — WO → Correction/Approval/Lineage Records (1 → N cycles, numbered, unlimited).**
Pre-CLOSED WAITING-APPROVAL loop vs post-CLOSED REOPEN (same identity) vs RE-CREATE
(`CREATED_FROM`, new identity). CANCELLED is terminal lineage (no reopen). `LOCKED` (CD-11
§§2, 9, 28; TADR-09).

**R-26 — Workspace → Transactional entities (1 → N ownership).** WO, Service Request, Quotation,
SO, Fulfillment, PR, PO, Receiving, stock/movements, material usage (via WO), service history
(via WO), numbering/templates/approvals/reporting — all workspace-owned. Shared masters +
intelligence referenced, never moved automatically. `LOCKED` (CD-07/08; CD-05/09/10/11 workspace clauses).

**R-26 (amended 2026-10-03; refined 2026-10-09 per HBA-DECISIONS-14):** Single-Pending rule governs the numbered/submitted revision workflow only (SUBMITTED, APPROVED, REJECTED, CORRECTED). At most one revision may occupy that pipeline per WO at any time. A DRAFT is unnumbered and pre-workflow, and is therefore OUTSIDE the Single-Pending count. DRAFTs coexist across users (creator-scoped; cap 10 per user as personal hygiene monitoring, no expiry, per the 2026-10-03 HBA decision). Per the 2026-10-09 HBA refinement, one user holds at most one active DRAFT per WO: a new DRAFT request by the same user for the same WO routes to that user's existing active draft (creator-only continuation; only the creator may cancel it). Competing DRAFTs across users do NOT cancel each other. Only the approved version is formally recorded; per-user draft scribbles are not individually recorded. INV-30 is REVOKED. The 24-hour clause of INV-28 is REVOKED.

**R-27 — Company → Customer Projection (gated derivation).** Customer-visible data for a Company
exists ONLY through the E-51 gate conjunction (CLOSED + FINAL + Verified PIC + Company Scope +
Policy + Eligibility). No direct Company→public-data association exists. `LOCKED` (CD-11
§§18, 21; CD11-020/021; TADR-12).

Relationship count: 27 (R-01…R-27). Cardinality is marked established only where a source states
it (R-02, R-08, R-09, R-10, R-13, R-16, R-17, R-23); R-06/R-07 bounds are DERIVED and flagged as
such; all else state no invented cardinality.

---

## 8. Identity vs Business Entity Boundaries

This section exists because merging any two of these concepts would silently create business
rules (access grants, ownership claims, approval rights) that were never decided.

| Concept | Answers | Decided by | Must never be read as |
|---|---|---|---|
| Google Identity (E-07) | *Who* is at the keyboard (external) | Locked human decision (Google-only) | Company membership, PIC status, access, or approval authority |
| Contact / PIC (E-08) | *Which person* relates to a Company | CD-03 (1-N under Company) | A login, a membership, or an access grant |
| Verified PIC Link (E-09) | *Whether* that person may act for that Company, and in what state | Manager/Admin approval (applicant ≠ approver) | A profile attribute (it is a separate lifecycle concept so revocation preserves history) |
| Company Access (E-10) | *What scope* follows: UNIT vs COMPANY | The Link state + locked scope definitions | A third tier, a cross-company grant, or anything QR/login alone can yield |
| Company (E-01) | *Which business identity* everything anchors to | CD-03 single identity | A login domain or an email domain (email matching is NOT the requirement) |
| Internal role authority (ASSIGN_WO, CREATE_WO, approver) | *Who inside* may do what (CD-01 S3 roles; CD-11 authorities) | CDs + Dynamic Configuration grants | External identity or PIC status (neither is approval authority; no auto-approval) |
| Unit (E-11) | *Which asset* work/history/projection attach to | CD-11 registry posture | Ownership of the work (execution is WO-owned) or a browsing handle (unit scope is not browsing) |

Boundary rules (`LOCKED` unless noted):

1. Sign-up alone grants nothing — no Company, no PIC, no Unit access (locked human decision).
2. PIC registration is an application (→ PENDING), never self-executing.
3. Approval requires an authorized internal Manager/Admin OTHER than the applicant; Google
   Identity and PIC status are never approval authority; no automatic approval; no direct-URL/API
   bypass (TADR-13 security; IS-03 will specify enforcement, this section only fixes the concepts).
4. Revocation ends access without deleting history: Contact, relational, and service history
   survive link revocation (TADR-13 link-entity separation; TADR-07 single-write lineage).
5. No permanent Customer–Technician relation and no technician relation on the Customer Profile
   exist in this model (CD-11 §7) — technician participation is per-WO assignment (E-20) and
   per-Visit attendance (E-22) only.
6. Internal notes, correction/cancellation/administrative reasons, acquisition prices, and vendor
   intelligence are internal-only categories that never cross into projection concepts (CD-11 §21).

---

## 9. Asset Model

**Parent (E-11).** The Unit is the parent asset and the QR identity anchor. Genset is the initial
primary asset domain; the model stays open to other asset categories WITHOUT generic typing:
new categories arrive as new strict subtypes (same pattern as E-12…E-14), never by converting the
core into EAV/JSON (explicitly excluded alternative, TADR-03).

**Strict operational subtypes (E-12 Engine / E-13 Generator / E-14 Box-Chassis).** Each carries
subtype-specific structure (placeholders in IS-01 — field requirements are OPEN, OQ-03) sharing a
Unit-rooted base (identity, parent link, lifecycle state). Uses in this model: serial-number
identity (incl. emergency-gate applicability logic, E-21), replacement genealogy (E-17), and
applicability-driven N/A (system-determined from Unit subtype — E-21, CD11-029).

**Registry-only concepts (E-15).** Pump, ATS, Synchronizing Panel, Transformer are Phase 1
registry/reference entries. Promotion to operational subtype requires explicit canonical
documentation — which does not currently exist. (This preserves the handover §6 instruction
exactly as bounded: "unless canonical documentation explicitly says otherwise" — it does not.)

**Location (E-16).** Separate concept from Company address (label + address text + optional
lat/long). Never merged.

**Genealogy (E-17).** Replacement = old + new + date + reason + relationship, per subtype.
Component architecture itself is untouched by replacement events.

**Extensibility rule (`DERIVED`, TADR-03).** Adding an asset category = adding a strict subtype
under Unit-rooted base + its own replacement/serial semantics. Reusing E-15 names as operational
subtypes, or adding generic spec bags, would contradict TADR-03 and is therefore NOT part of
this model.

---

## 10. Service Domain Model

Conceptual chain (lifecycle detail belongs to IS-02; permission detail to IS-03 — this section
fixes only what the concepts are and how they bound each other):

```text
[Service Request]? ──optional intake──▶ [Work Order] ──binds──▶ [Unit ×1]
        │                                   │
        │ (substantial work only;            ├── Assignment events (1 Primary + N Supporting)
        │  never Add Job)                   ├── Visit ×N (each: Outcome, Findings, HM,
        │                                   │            Checklist-state, Test/Run, Evidence)
        ▼                                   ├── Material Usage ×N (↔ Inventory, non-atomic)
[Commercial/Approval]                       ├── Report ×1 (Summary + Visit History)
                                                ├── Final Conclusion (draft → official)
                                                └── Cancellation / Reopen / Re-create records
```

**Boundaries preserved (`LOCKED`, CD-11):**

- B-01. Request optional; WO standalone-capable (E-18/E-19). No fake Unit to satisfy a relation;
  unbound WOs use NEW / NOT YET DETERMINED postures with validation, never fabrication (E-08…R-08).
- B-02. Exactly 1 Report per WO; N Visits per WO; Visit is source, Report is consolidation; no
  manual duplication (E-22, E-32, R-09…R-11).
- B-03. Visit lifecycle independent of WO lifecycle; COMPLETED visit finalizes nothing (E-22).
- B-04. Report FINAL iff WO CLOSED; no FINALIZE action; no per-correction auto-revisions (E-32).
- B-05. Review mandatory pre-CLOSED; `APPROVE REPORT ⇒ WO = CLOSED` automatically; no `CLOSE_WO`;
  technician never closes own WO; customer acknowledgement optional, never a CLOSED prerequisite
  (CD-11 §§2, 19 — IS-02 guards, IS-03 authority).
- B-06. Correction pre-CLOSED via WAITING-APPROVAL loop (incl. the single audited direct-edit
  sideroute with mandatory reason); post-CLOSED via REOPEN only; unlimited numbered cycles;
  CANCELLED terminal (E-36/E-37/E-54).
- B-07. Emergency is a lane on the same WO concept (direct IN_PROGRESS + minimum critical gate),
  and emergency purchasing is a DIFFERENT concept (E-47) — never mixed (CD-11 §§6, 24).
- B-08. Evidence opt-out and N/A paths always carry mandatory reasons + reviewer validation;
  missing HM is never zero; applicable-but-unknown serials are never N/A (E-29/E-31).
- B-09. INTERIM / CONTINUATION / FINAL are report/work-stage classifications (with
  BEFORE/DURING/AFTER findings phases) — never lifecycles, never Visit Types (CD-11 §20).

**No new lifecycle rules are created here.** State names, transitions, guards, and authority
matrices belong to IS-02/IS-03; any term not in CD-11 §30-surviving vocabulary appearing there
must be escalated, not normalized.

---

## 11. Customer Projection Domain

The model contains TWO disjoint information worlds with a governed gate between them:

**World A — internal operational data.** Everything: WIP visits, non-eligible evidence, internal
notes, correction/cancellation/administrative reasons, acquisition prices, vendor intelligence,
commercial/pricing data, full histories, PIC lists. Visible only under internal permission
(IS-03). This world is the single operational history (TADR-07).

**World B — customer-visible projection (E-51/E-52).** The reviewer-curated, eligibility-gated
derivative: allowlisted content only; no prices in any form; no-download honored. Two scopes:
UNIT_SCOPE (authenticated non-PIC, this Unit only) and COMPANY_SCOPE (verified PIC, all Units of
that Company + histories + PIC per customer-safe visibility).

**The gate (conjunction, `LOCKED`).** Nothing reaches World B unless ALL hold: WO CLOSED +
Report FINAL + Verified PIC Link + Company Scope + Policy (`photo_type + approval_state +
policy_version` + reviewer curation) + Eligibility. Technician determination plays no role;
internal-only categories can never pass regardless of state.

**What IS-01 does NOT decide (all `OPEN`, OQ-06/owner BA):** publication mechanism (snapshot vs
live), refresh cadence/staleness policy, no-download serving mechanism, Outstanding surfacing
rules. The gate above is complete as business logic; the deferred items are mechanism/expectation
only — IS-06 will specify requirements around them without filling them.

**Quantity vs price (`LOCKED`, CD-11 §21).** Material *quantity* appears only where appropriate/
agreed (reviewer-curated); material/purchase/acquisition/HPP/margin/accounting *values* never
appear in any external projection (TADR-12/14).

---

## 12. Audit / History / Correction Concepts

The domain requires history as **controlling data**, not as a passive log (TADR-08/09; CD-11 §28):

- **H-01 — Governed trail fields.** Every correction/cancellation/reopen/re-create event carries:
  actor, server timestamp(s), action, object, reason, before/after where relevant, reviewer,
  approval/review state, traceability links. (`LOCKED` requirement shape; TADR-08.)
- **H-02 — Numbered correction cycles.** Correction history carries cycle numbering; cycle count
  is unlimited (no technical maximum). Pre-CLOSED cycles run the WAITING-APPROVAL loop
  (REQUEST CORRECTION → CORRECTION_REQUIRED → resubmission; Report stays NON-FINAL); post-CLOSED
  cycles run REOPEN (→ IN_PROGRESS). (`LOCKED`, CD11-008; TADR-09.)
- **H-03 — Controlling vs official.** Correction history controls what is current; the
  draft → modification → final → approved chain fixes what is official (Final Conclusion,
  approved Report). Corrections never silently orphan or replace sanctioned results. (`LOCKED`,
  CD-11 §§2, 18, 28.)
- **H-04 — Lineage identity rules.** REOPEN preserves identity (number/Report/assignment
  restored); RE-CREATE mints identity with `CREATED_FROM` lineage (no assignment carry; Company
  kept; Unit may change); CANCELLED ends identity (no reopen). (`LOCKED`, CD-11 §§9, 28.)
- **H-05 — Tamper-evidence + the single sideroute.** Trails are tamper-evident; no direct-edit
  path exists on CLOSED records. The sole exception — reviewer EDIT during WAITING APPROVAL with
  mandatory reason — rides the same trail with full audit linkage (never a bypass). (`LOCKED`,
  TADR-08/09.)
- **H-06 — Dual time capture.** Event-time plus record-time capture proceeds for (retroactive)
  emergency work; the precedence convention itself is OPEN (OQ-08; TADR-08 dependency).

Retention windows, trail-storage mechanics, and observability substrate are NOT domain content
(deferred technical decisions; TADR-08/18) — IS-07 will state audit requirements, never mechanisms.

---

## 13. Phase 1 vs Future Extensibility

**Phase 1 required domain concepts (normative for IS-02+):** E-01…E-14, E-16…E-34, E-36…E-55
(Company/roles/workspace/marker-concept, identity chain, Unit + strict subtypes + location +
replacement, full Service family incl. emergency lane, material/inventory/price/commercial
families, projection concepts, Outstanding, correction/lineage records, manual reminder).

**Registry / reference concepts (named, bounded, non-operational Phase 1):** E-15 (Pump/ATS/
SyncPanel/Transformer), E-57 (warehouse/bin detail), E-40 item master extendability,
E-06 marker record shape, E-56 configuration contents.

**Future / extensible concepts (pattern fixed, content absent):** additional asset subtypes
(§9 rule), future Accounting/ERP scope (CD-01 deferred — never foreclosed), future providers
beyond Google (TADR-13 extensibility, business decision required first), event-driven projection
upgrades (TADR-12 future), opening-stock formalization / transfers / reservations (CD-10 deferred).

**Explicitly out-of-scope concepts (MUST NOT appear downstream as domain facts):** journal/GL/
COA/COGS/FIFO/Average/valuation/costing/tax engine/revenue recognition (CD-01/04/05/06/09/10/11);
inventory reservation (CD-10 Q11); auto-completion of remainders (CD-05/09); auto-approval and
self-approval (locked prohibition); anonymous/public preview access (locked CONTROLLED ACCESS);
cross-company grants; cross-workspace transactions and combined global transaction reporting
(CD-07/08); all §30-superseded CD-11 terms; CD-02 content of any kind.

Extensibility is protected WITHOUT overbuilding: placeholders (§9 subtypes, E-56 domains) carry
no invented fields, thresholds, or mechanics.

---

## 14. Open Questions / Decision Register

Every unresolved domain matter found during IS-01. Ownership = BA unless stated. IS-01 decides
none of them.

| ID | Question | Why it matters | Affected domain | Source | Next owner |
|---|---|---|---|---|---|
| OQ-01 | Are `FULL_SERVICE` / `INSPECTION_ONLY` / `EMERGENCY` approved workflow templates, and what do they govern? (No canonical source found; CD-11 has only "template-scoped visit structure" + "tipe/template WO".) | IS-02 cannot bind guards to templates that may not exist | Service (E-35) | Handover §6 claim vs grep-verified absence in all canonical docs | CLOSED 2026-09-25 (documentation reconciliation) — answered by existing approved decisions: BD-WORKMODEL-001 §8/§10 (template axis REJECTED/unused) + AB-01; no template names adopted |
| OQ-02 | Customer publication mechanism + permission model (snapshot-vs-live expectation, serving mechanics) | IS-06 normative content unblocked on the business side; only the serving **mechanism** remains architecture | Projection (E-51) | **RESOLVED 2026-09-30 (documentation reconciliation): business expectation = HBA D-01A = RETAIN; publication permission already canonical (CD-11 §21 + IS-03 §7); mechanism remains architecture (TADR-11/12)** | — |
| OQ-03 | Subtype field requirements (which fields, if any, for Engine/Generator/Box-Chassis first slice) | Placeholders suffice for IS-01 but IS-02 validation gates need field truth | Asset (E-12…E-14) | TADR-03; Approval Package §10 | BA (business requirements) |
| OQ-04 | N/A taxonomy + checklist/Test-Run contents + exact N/A validation rules | IS-02 cannot write enforceable gates without them | Service (E-25, E-30) | CD-11 §§11, 13, 14; F-1; TADR-01/11 deferred | BA DECISION REQUIRED |
| OQ-05 | Additional business-critical evidence categories beyond serials + before/after (if any) | Adding categories without approval = invented rule | Evidence (E-31) | CD-11 §17; CD11-014 | BA DECISION REQUIRED |
| OQ-06 | Projection freshness/staleness policy + no-download mechanism + Outstanding surfacing rules | IS-06/IS-09 normative content blocked in these areas | Projection (E-51, E-53) | TADR-12; Approval Package §10–§11 | BA (expectation) + architecture (mechanism) |
| OQ-07 | Reminder / automation policy (generation + intervals) | Disabled Phase 1 is LOCKED; any enablement needs policy first | Reminder (E-55) | Decision Register (UNRESOLVED); CD-11 Q27/deferred | BA DECISION REQUIRED |
| OQ-08 | Emergency retroactive timestamp convention (event-time vs record-time precedence) | Dual capture proceeds; precedence undecided | Audit (H-06) | Decision Register (UNRESOLVED); TADR-08 | BA DECISION REQUIRED |
| OQ-09 | Minor vs substantive correction: business definitions and content rules | Both must be representable; neither defined | Correction (E-54) | CD11-007; Approval Package §4 ("tidak dikarang") | BA DECISION REQUIRED |
| OQ-10 | Deployment operational context | IS-10 requirements cannot assume facts | Cross-cutting | Decision Register (UNRESOLVED) | BA DECISION REQUIRED |
| OQ-11 | Prospect→Customer transition rules; Company numbering/role codes; per-unit commercial ownership detail; data migration/merge | Identity model complete; operational detail missing | Organization (E-02, E-04) | CD-03 deferred; CD-08 open | BA DECISION REQUIRED |
| OQ-12 | Company↔Workspace usage-marker record shape; Contact workspace-specific context; suggest/approval matrix detail; merge/deactivation mechanics | Referenced by R-02/R-04/R-26; shapes deferred | Organization (E-06) | CD-08 open; TADR-02 open | BA (business) + IS (shape, later) |
| OQ-13 | Latest-N vendor offers count; MOQ/quantity-break/pack; currency conversion; authority matrix detail; PPN rate source | Price intelligence usable but bounded | Price (E-41) | CD-06 deferred | BA DECISION REQUIRED |
| OQ-14 | Purchasing detail: emergency/small nominal thresholds; doc-number formats; approver lists; revision-chain mechanics; warehouse/location detail; return-replacement detail | PO/Receiving concepts complete; operating detail missing | Purchasing (E-47…E-49) | CD-09 deferred | BA DECISION REQUIRED |
| OQ-15 | F-1 Service Execution Clarification (arrival scan, mandatory start time/GPS, OFF/RUNNING/after-repair steps, PM HM initial+final, inspection HM optionality, photo slots, SKIP_TEMPORARY-interim scope) | DEFERRED non-blocking clarification; must not modify CD-11 | Service execution | Baseline §6 (F-1 DEFERRED) | BA — decision NOT yet requested |
| OQ-16 | Customer acknowledgement alternative evidence types; invitation UX | Optional-ack path needs no mandatory type (LOCKED), but alternatives unlisted | Service (CD-11 §19) | CD-11 §19; Approval Package §10 | BA DECISION REQUIRED |

`CONFLICT` items found: NONE — no canonical-vs-canonical contradiction was encountered in IS-01
scope. (OQ-01 was a handover-claim vs canonical-absence, handled as OPEN per `IS-00` §4.2 (layer
boundaries) at authoring and closed on 2026-09-25 by documentation reconciliation — see E-35 in
§14; it was never a conflict between canonical sources.)

---

## 15. Traceability Matrix

Major concept → authoritative source. (Minor/derived concepts cite inline in §6.)

| Concept | Source | Authority |
|---|---|---|
| Company | CD-03 (single identity); CD-07 Q4; CD-08 | LOCKED |
| Prospect / Customer / Vendor roles | CD-03 (roles on Company; Customer+Vendor coexistence) | LOCKED |
| Contact / PIC | CD-03 (1-N under Company); CD-08 (shared) | LOCKED |
| Google Identity (external, Google-only) | Locked human decision; TADR-13 | LOCKED (formal CD pending) |
| Verified PIC Link (VERIFIED/PENDING/REVOKED; applicant≠approver; no cross-grant) | Locked human decisions; TADR-13; CD-11 §§21–22 | LOCKED (formal CD pending) |
| UNIT_SCOPE vs COMPANY_SCOPE (+ invariants) | Locked Business Access Model decision; TADR-12/14/16; CD-11 §§21–22 | LOCKED (formal CD pending) |
| Workspace (ownership/numbering/template/approval/reporting) | CD-07; CD-08 | LOCKED |
| Shared vs workspace-owned partition | CD-07 Q4–Q16; CD-08 ownership model | LOCKED |
| Unit (parent asset; no fake master) | CD-11 §5; TADR-02/03/07 | LOCKED |
| Engine / Generator / Box-Chassis (strict subtypes) | TADR-03; CD-11 §§6, 15 | LOCKED (fields OPEN) |
| Registry components (Pump/ATS/SyncPanel/Transformer) | TADR-03; CD-11 §15 | LOCKED (as spec-less) |
| Unit Location (separate from Company address) | CD-11 §§10, 20 (field/location handling); no merged concept in any source | LOCKED (separation) |
| Component Replacement (old/new/date/reason/relationship) | CD-11 §15; TADR-03 | LOCKED |
| Service Request (optional) | CD-11 §3 | LOCKED |
| Work Order (lifecycle; creation postures; 1 WO = 1 Unit) | CD-11 §§2, 4, 5 (CD11-001…006) | LOCKED |
| Assignment (1 Primary + N Supporting; ASSIGN_WO; Take Over; Self-Add) | CD-11 §§2, 7, 8 | LOCKED |
| Emergency lane + minimum critical gate | CD-11 §6 (CD11-004/028/029) | LOCKED |
| Visit (1 WO → 1 R → N V; OPEN→COMPLETED; check-in/out) | CD-11 §§10, 18 (CD11-017/019/025) | LOCKED |
| Visit Type INITIAL / ON PROCESS (system-determined) | CD-11 §10 | LOCKED |
| Outcome COMPLETED / NOT_PERFORMED / ON HOLD + reason model | CD-11 §11 (CD11-013/024/026) | LOCKED |
| Checklist UNCHECKED/CHECKED; Add Job minor-only | CD-11 §§8, 12 | LOCKED |
| Findings BEFORE/DURING/AFTER; Checklist+Test/Run mandatory | CD-11 §13 | LOCKED (contents OPEN) |
| Hour Meter (min-one; N/A + reason; never zero) | CD-11 §14 (CD11-015) | LOCKED (exact N/A rules OPEN) |
| Evidence (event-driven; opt-out + reason; photo_type≠visibility; single retention) | CD-11 §17 (CD11-014/016); TADR-11 | LOCKED |
| Report (1 per WO; Summary + History; FINAL iff CLOSED) | CD-11 §§10, 18, 20 (CD11-017/019/020) | LOCKED |
| Final Conclusion (draft → official; history) | CD-11 §18 (CD11-018) | LOCKED |
| Service Types (6; Installation/Corrective excluded; no thresholds) | CD-11 §16 | LOCKED (detail OPEN) |
| Cancellation (terminal; OPEN/IN_PROGRESS only) | CD-11 §9 (CD11-010) | LOCKED |
| Reopen (CLOSED-only, same identity) / Re-create (CREATED_FROM, new identity) | CD-11 §§2, 28 (CD11-006/007/008) | LOCKED |
| Review mandatory; ack optional | CD-11 §§2, 19 | LOCKED |
| Customer-safe allowlist/exclusions; quantity-if-agreed; no price; no-download | CD-11 §§20, 21 (CD11-020/021); TADR-12/14 | LOCKED (mechanism OPEN) |
| QR permanent + unit-scoped; CONTROLLED ACCESS | CD-11 §22; locked QR decision; TADR-16 | LOCKED (formal CD pending; mechanics deferred) |
| Manual reminder baseline; automation disabled | CD-11 §23; CD11-011; TADR-15 | LOCKED (policy OPEN) |
| Outstanding = monitoring (SLA numeric/H-1/overdue/escalation disabled) | CD-11 §§11, 20; Baseline §4 | LOCKED |
| Material Usage (Item+Qty+Harga Perolehan; non-atomic; non-stock class) | CD-11 §§25, 26; CD-04 R2; TADR-04/10 | LOCKED |
| Inventory Operation (qty-only; no reservation/valuation) | CD-10; TADR-10 | LOCKED |
| Vendor Offer (basis model; immutability; Q8 visibility FINAL) | CD-06 | LOCKED |
| Acquisition Reference (operational; ≠ valuation) + Provenance/History | CD-04; CD-06; CD-08 | LOCKED |
| Quotation / SO / Fulfillment | CD-05 | LOCKED |
| PR / PO / Receiving / Acquisition Event | CD-09 (+ CD-04 R1) | LOCKED |
| Correction/approval/lineage controlling records | CD-11 §§2, 28 (CD11-006/007/008/012); TADR-08/09 | LOCKED |
| INTERIM/CONTINUATION/FINAL as classifications | CD-11 §20 | LOCKED |
| Superseded terms (must not reappear) | CD-11 §30 | LOCKED (as prohibitions) |
| Workflow templates FULL_SERVICE/INSPECTION_ONLY/EMERGENCY | NO canonical source found | CLOSED 2026-09-25 (OQ-01, documentation reconciliation — template axis REJECTED/unused: `BD-WORKMODEL-001` §8/§10; `AB-01`) |

---

## 16. IS-01 Definition of Done

IS-01 is DONE if and only if all of the following hold (IS-00 §7/§8 + handover §7.16):

1. **Entities inventoried.** §6 catalogues 57 concepts (E-01…E-57) across 7 families; meanings,
   purposes, and lifecycle relevance are explicit per entity.
2. **Relationships documented.** §7 defines 27 relationships (R-01…R-27) with cardinality stated
   only where established, ownership stated, lifecycle dependency stated, and authority labeled.
3. **Boundaries clear.** Identity-vs-entity separation (§8), asset model (§9), service boundaries
   (§10), projection worlds + gate (§11), audit concepts (§12), and Phase 1 vs future vs
   out-of-scope (§13) are each explicit.
4. **LOCKED / DERIVED / OPEN distinguished.** Every entity (§6), relationship (§7), and boundary
   claim carries its label; DERIVED items (R-06/R-07 bounds, E-10 tier mechanics, E-50, E-56
   existence, §9 extensibility rule) change no baseline meaning and are flagged as such.
5. **Traceability exists.** §15 maps every major concept to its source; inline citations cover the
   rest; requirement IDs for downstream use begin at IS-02 (IS-01 produces the CP-A entity/event
   inventory, not normative requirements).
6. **No implementation introduced.** No tables/columns/types/keys/indexes, no migrations, no ORM,
   no endpoints/payloads, no code, no UI, no product/framework/storage selections, no Programmer
   TASK. (Verified by text search for DDL/type/endpoint language — none present.)
7. **No business rule invented.** Defaults (reasons, emergency gate, evidence floor, scope tiers)
   are quoted from canonical sources; everything else is OPEN (§14, items OQ-01…OQ-16; OQ-01 closed
   2026-09-25 by documentation reconciliation, 15 items remain OPEN).
8. **Unresolved decisions surfaced.** §14 lists all 16 with owner BA (or BA + architecture for
   OQ-06/OQ-12); zero silent resolutions; zero CONFLICT items found (OQ-01 handled as OPEN at
   authoring and closed 2026-09-25 by documentation reconciliation, §14 E-35).
9. **Consistency verified.** IS-00 governance obeyed (layer separation §4 of IS-00; CP-A inputs
   ready: entity catalogue + event inventory in §§6–7 + correction lineage); CD-11 and approved
   architecture unchanged (no edit proposed to any canonical document); superseded vocabulary
   absent (verified against CD-11 §30 list).
10. **Anti-drift audit passed.** Appendix A records the §8 handover checklist item-by-item.

### Appendix A — Anti-Drift Self-Audit (handover §8)

**Governance.** IS-00 obeyed (this document follows the IS-01 charter: objective/scope/inputs/
dependencies/outputs/authority/out-of-scope/DoD)? YES. Implementation avoided (no schema, API,
UI, code, TASK — verified)? YES. Programmer TASK created? NO.

**Business rules.** CD-11 decisions preserved (lifecycle, postures, emergency gate, visit/report,
evidence, HM, review, cancellation/reopen/re-create, publication boundary, workspace)? YES —
each with section citation. Newer decision reverted to older version? NO (superseded §30 terms
checked absent; "Customer tidak mengijinkan" used, "Customer tidak meminta" absent). "Does not
request" vs "does not permit" distinction preserved? YES (§6 E-25). `ON PROCESS` preserved as
Visit Type only, never WO status? YES (E-23, R-terms; WO status uses IN_PROGRESS).

**Asset.** Unit as parent? YES (E-11, §9). Engine/Generator/Box-Chassis as strict subtypes?
YES (E-12…E-14, §9). Generic EAV/JSON core avoided? YES (explicitly excluded, §9 + §13).

**Service.** SR/WO boundary (optional request; substantial work via Request, minor via Add Job)?
YES (E-18/E-27, B-01). 1 WO → 1 Report → N Visits? YES (E-22/E-32, R-09…R-11). INTERIM/
CONTINUATION/FINAL as classifications only? YES (E-51 context, B-09).

**Evidence.** photo_type vs visibility separated? YES (E-31, P-09, §11 gate). Approval-state
governance preserved? YES (`photo_type + approval_state + policy_version` + curation).
Serial + before/after critical floor preserved? YES (E-21, E-31).

**Access.** Google Identity → Contact/PIC → Verified PIC Link → Company chain? YES (E-07…E-10,
R-03, §8). No cross-grant? YES. Self-approval prohibition (applicant ≠ approver)? YES (E-09, §8.3).

**Customer.** Internal vs customer-visible worlds separated? YES (§11). Quantity-if-agreed without
price? YES (E-51). Unit-scoped QR? YES (E-52, R-23).

**Deliberate UNCERTAIN → OPEN (historical).** Workflow template names (OQ-01): handover asserts
approval, no canonical source found — recorded OPEN, not adopted at authoring; **closed 2026-09-25**
by documentation reconciliation (§14 E-35): the template axis is REJECTED/unused (`BD-WORKMODEL-001`
§8/§10; `AB-01`). All other handover §6 principles verified LOCKED against cited sources (see §15).

---

## Addendum HBA-DECISIONS-22 (2026-10-13) — kanon v16/v17 + timing snapshot

- Migrasi v16 (profil perusahaan sendiri) + v17 (lokasi visit) adalah KANON per perintah HBA (a). Detail teknis ikut paket eksekusi terotorisasi, bukan dokumen ini.
- Timing salinan pelanggan (customer snapshot): dibuat saat WO ditutup yaitu saat manager approve (`approve_report` / CLOSED) per perintah HBA (c). Wording lama yang bertentangan retained sebagai riwayat superseded, tak dihapus.
- Nol aturan bisnis baru di luar perintah HBA-DECISIONS-22.

## Addendum HBA-DECISIONS-30 / -31 / -32 / -34 (2026-10-24) — diskusi internal WO, rujukan dokumen unit, penanda terbitan berkas unit

- **Diskusi internal Work Order (konsep baru).** Pesan per WO: satu pesan satu baris dengan penulis dan
  waktu server; penanda terbaca per pengguna, dan ketiadaan penanda itulah yang berarti belum dibaca.
  Diskusi adalah **catatan**: bukan perintah kerja, bukan persetujuan, bukan bagian trail audit
  (IS-07 addendum). Ruangnya terbatas pada WO, bukan ruang bebas tingkat Unit. Setiap pengguna internal
  boleh membaca dan menulis (IS-03 addendum), dan setiap pengguna internal boleh dipanggil di dalam
  pesan; panggilan menimbulkan pemberitahuan **di dalam aplikasi saja**.
- **Rujukan dokumen unit (SPK / Invoice / Project).** **Satu kolom bebas** pada Unit (HBA: "satu kolom
  saja"), disimpan apa adanya. Menutup usulan tiga kolom terpisah di HBA-DECISIONS-30.
- **Penyerahan unit.** Unit membawa tanggal penyerahan serta lampiran dokumen/gambar penyerahan.
  Rujukan, tanggal, dan lampiran penyerahan **tidak** diproyeksikan ke portal pelanggan (IS-06 addendum).
- **Penanda terbitan berkas tingkat Unit.** Dokumen (sertifikat, manual book) dan gambar unit bersifat
  internal sampai ada penanda terbitan yang ditetapkan **Manager/Admin**; pengunggah tidak pernah
  menetapkan visibilitas (IS-05 addendum). Susunan galeri: berkas tingkat Unit berdiri di kolom
  tersendiri, berkas yang melekat pada dokumen induk (WO/SR) berdiri di kolom utama dan dibingkai
  nomor induknya.
- Bingkai bukti: HBA menetapkan Visit adalah bagian dari WO sehingga bingkai WO dipandang setara;
  pencatatan asal Visit di titik pengambilan tetap usulan teknis OPEN, bukan aturan bisnis.
- Nol aturan bisnis baru di luar HBA-DECISIONS-30, -31, -32, dan -34.

## Addendum HBA-DECISIONS-36 (2026-10-24) — registri gambar merek & perlengkapan

- **Gambar merek.** Satu gambar per jenis (mesin / generator / module controller / genset) dan per
  merek, dalam lingkup workspace; unggahan berikutnya menggantikan yang lama. Gambar dipakai untuk
  menampilkan logo pada kartu Unit sesuai merek yang tercatat, bukan data baru tentang unitnya.
- **Gambar perlengkapan.** Satu gambar per butir perlengkapan dari daftar yang sudah tertutup;
  tidak menambah butir maupun kategori baru.
- Keduanya berada di bawah otoritas kurasi peninjau (Manager/Admin) seperti berkas unit lainnya;
  peran lapangan hanya membaca. Taksonomi jenis berkas di luar lantai terkunci tetap OPEN (OQ-05).
- Nol aturan bisnis baru di luar rekaman HBA-DECISIONS-36.

---

*End of IS-01 + Addendum HBA-DECISIONS-30/31/32/34/36 (2026-10-24). Next candidate (not started):
**IS-02 WORKFLOW & STATE TRANSITION SPECIFICATION** — awaiting explicit Business Authority
instruction. STOP.*

