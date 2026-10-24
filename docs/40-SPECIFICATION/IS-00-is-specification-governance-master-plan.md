# IS-00 — IS Specification Governance & Master Plan

```text
Status: CANONICAL GOVERNANCE FOR IS PHASE (PROPOSED-CANONICAL, pending BA acknowledgement)
Phase: IS Specification — Governance only
Authoritative baseline: CD-11 SIGNED-OFF / LOCKED / CLOSED; Architecture APPROVED / CANONICAL
Authorization granted by this document:
  Business decision = NO | Architecture decision = NO | Schema = NO | API = NO
  Code = NO | Migration = NO | Programmer TASK = NO | Implementation = NO
Next work: IS-01 candidate only (not started by this document)
```

> This document defines **how the IS Specification phase will be worked**.
> It creates no business rule, changes no architecture direction, and authorizes
> no implementation. Where this document and a locked baseline conflict, the
> locked baseline wins.

---

## 1. Purpose

1.1. Establish the single governance reference for the IS Specification phase
of CRM Mitra Sarana Pratama (MitraSP).

1.2. Define the IS layer: what question IS answers, what it produces, and what
it explicitly does not produce (see §4).

1.3. Register the full IS workstream set (IS-00 through IS-FINAL) as auditable
units with explicit objective, scope, inputs, dependencies, outputs, authority,
out-of-scope, and Definition of Done (see §5, §7, §8).

1.4. Fix dependency direction and sequencing: what is sequential, what may run
in parallel, and what each workstream must receive before it starts (see §6).

1.5. Fix approval governance, escalation paths, change control, Figma boundary,
and the implementation gate so no role silently assumes another role's
authority (see §9–§13).

1.6. Record deferred items and the traceability strategy so gaps are visible
instead of filled by assumption (see §14–§15).

Out-of-scope for IS-00: any workstream content itself (domain rules, workflow
detail, permission detail, contracts, storage detail, portal detail, audit
detail, UI detail, security detail, integration detail), any schema / endpoint /
code / migration / test automation / framework choice, any Programmer TASK.

---

## 2. Current Baseline

### 2.1 Business baseline — LOCKED

| Item | Status | Canonical source |
|---|---|---|
| CD-01 Business Scope | FINAL / LOCKED | `docs/10-DECISIONS/CD-01-business-scope.md` |
| CD-02 | DEFERRED / UNVERIFIED — no canonical document; must not be reconstructed | (absent) |
| CD-03 Business Master | LOCKED | `docs/10-DECISIONS/CD-03-business-master.md` |
| CD-04 Operational Acquisition Price | LOCKED | `docs/10-DECISIONS/CD-04-operational-acquisition-price.md` |
| CD-05 Sales Transaction / Quotation | LOCKED | `docs/10-DECISIONS/CD-05-sales-transaction-quotation.md` |
| CD-06 Vendor Offer Price | LOCKED | `docs/10-DECISIONS/CD-06-vendor-offer-price.md` |
| CD-07 Multi-Workspace | LOCKED | `docs/10-DECISIONS/CD-07-multi-workspace.md` |
| CD-08 Data Ownership | LOCKED | `docs/10-DECISIONS/CD-08-data-ownership.md` |
| CD-09 Purchasing Transaction Boundary | LOCKED | `docs/10-DECISIONS/CD-09-purchasing-transaction-boundary.md` |
| CD-10 Inventory Operational Boundary | LOCKED | `docs/10-DECISIONS/CD-10-inventory-operational-boundary.md` |
| CD-11 Service / Work Order Operational Boundary | SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF, CD11-001…CD11-029) | `docs/10-DECISIONS/CD-11-service-work-order-operational-boundary.md` |

CD-11 is the canonical business baseline for the Service / Work Order scope
covered by the IS phase. It is the primary business input to IS-01…IS-09 where
Service/WO behavior is concerned.

### 2.2 Architecture baseline — APPROVED / CANONICAL

| Item | Status | Canonical source |
|---|---|---|
| Technical Architecture (TADR-01…TADR-18 + Architecture Baseline) | APPROVED / CANONICAL (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL, 2026-09-21) | `docs/30-ARCHITECTURE/ARCHITECTURE_BASELINE.md`, `docs/30-ARCHITECTURE/TADR/` |
| Architecture direction (§1–§12) | APPROVED / CANONICAL (BUSINESS AUTHORITY — ARCHITECTURE APPROVAL, 2026-09-22); implementation detail explicitly DEFERRED | `docs/30-ARCHITECTURE/ARCHITECTURE_APPROVAL_PACKAGE.md` |

This approval does not authorize implementation: coding / schema / migration /
API / UI / deployment / Programmer handoff = NO.

### 2.3 Locked human decisions recorded without formal CD number yet

Per `DECISION_REGISTER.md`: identity-link reconciliation, QR access policy, and
Business Access Model (Unit Scope / Company Scope) are LOCKED HUMAN DECISIONS
with formal CD documentation pending. IS workstreams consume them as recorded
constraints (via TADR-12/13/14/16 references) but do not re-decide, expand, or
narrow them. Customer publication model, reminder/automation policy, emergency
retroactive timestamp convention, and deployment operational context remain
UNRESOLVED / PENDING HUMAN DECISION (see §14).

### 2.4 Phase gate passed

```text
Business Baseline (CD-11 SIGNED-OFF) → Architecture Direction (APPROVED) → IS Specification (THIS PHASE)
```

Implementation is NOT authorized. No Programmer TASK exists or is created by
IS-00.

---

## 3. Source-of-Truth Hierarchy

Strict precedence. Lower levels never override higher levels.

### Level 1 — Business Authority (highest)

1. Explicit Human / BA decisions and BA Sign-Off.
2. CD-01 (FINAL/LOCKED), CD-03…CD-11 (LOCKED; CD-11 SIGNED-OFF/CLOSED).
3. `DECISION_REGISTER.md` as authority index and gate tracker — it records
   status; it does not itself create decisions.
4. Locked human decisions pending formal CD documentation (§2.3), exactly as
   recorded — no extension by inference.

CD-02 is DEFERRED / UNVERIFIED and absent. It is not an input to any IS
workstream and must not be reconstructed from evidence, code, schema, or
practice.

### Level 2 — Approved Architecture

1. `ARCHITECTURE_APPROVAL_PACKAGE.md` (§1–§12) — approved direction.
2. `ARCHITECTURE_BASELINE.md` — approved baseline.
3. TADR-01…TADR-18 as approved.

Architecture constrains *how* IS may specify (module seams, identity-link
separation, controlled QR, workspace/commerce boundaries, Accurate 5
transitional boundary, no cross-database FK, deferred accounting scope).
Architecture never overrides Level 1.

### Level 3 — Existing Evidence / Historical (lowest)

Discovery documents, audit documents (`docs/90-AUDIT/`), existing-system
analysis, legacy technical artifacts, prior prototypes/implementations.

Allowed use: explain context, surface gaps/conflicts, check compatibility.
Forbidden use: establishing a business rule, narrowing/broadening a locked
rule, filling a deferred item, or overriding Level 1/2. Any conflict found in
Level 3 material is escalated per §10–§11, not resolved by preference.

---

## 4. IS Layer Definition

### 4.1 The IS question

> **"Bagaimana sistem harus berperilaku dan apa yang harus disediakan oleh
> sistem agar approved business rules dan approved architecture dapat
> diwujudkan secara konsisten?"**

Every IS workstream must be able to trace each specified behavior/requirement
upward to either (a) a locked business rule, (b) an approved architecture
direction, or (c) an explicitly marked specification-level resolution that
alters neither (see §10).

### 4.2 Layer boundaries

| Layer | Owned by | Answers | IS relationship |
|---|---|---|---|
| Business rule | Business Authority (Human/BA) | *What* the business requires; operational boundaries, approvals, visibility rights, lifecycle semantics | IS **consumes**; never creates or modifies. Ambiguity → `BA DECISION REQUIRED`. |
| Architecture direction | Architecture (approved by Human/BA) | *What shape* the system takes; module seams, identity model, integration posture, deferred scope | IS **consumes**; never re-decides. Conflict → `ARCHITECTURE DECISION REQUIRED`. |
| System specification (IS) | AI Manager / Lead Architect (specification author) | *How the system must behave and what it must provide* to realize the above consistently: entities, lifecycles, permissions, contracts, storage/portal/audit/UI/security/integration requirements | This phase. Testable, reviewable, traceable. |
| Implementation | AI Programmer (only after gate, §13) | *How it is built*: code, schema, migrations, framework use, deployment execution | IS **defers**; IS must be implementation-agnostic except where architecture already constrains it. |

### 4.3 IS is / IS is not

IS **is**: behavior requirements, data requirements + logical model, lifecycle
and guard requirements, permission/visibility requirements, contract
requirements (not final endpoints in IS-00), storage/retention/access
requirements, projection/portal requirements, audit/correction requirements,
functional UI requirements, security/edge-case requirements, integration/
deployment/migration requirements, and cross-workstream consistency.

IS **is not**: business decision document, architecture decision document,
coding task, source code, migration script, deployment execution, test
automation, product/framework/library selection, or Programmer TASK creation.

---

## 5. Workstream Registry

Canonical registry. IDs are stable. Scope summaries here; full per-workstream
charter in §7.

| ID | Title | Kind |
|---|---|---|
| IS-00 | IS Specification Governance & Master Plan | Governance (this document) |
| IS-01 | Domain & Data Model Specification | Specification |
| IS-02 | Workflow & State Transition Specification | Specification |
| IS-03 | Access, Identity & Permission Specification | Specification |
| IS-04 | API & Service Contract Specification | Specification |
| IS-05 | Evidence, Attachment & Storage Specification | Specification |
| IS-06 | Customer Projection & Portal Specification | Specification |
| IS-07 | Audit, History & Correction Specification | Specification |
| IS-08 | UI/UX Functional Specification | Specification |
| IS-09 | Security, Validation & Edge Cases | Specification |
| IS-10 | Integration, Deployment & Migration Specification | Specification |
| IS-11 | Workspace & Tenant Isolation | Specification |
| IS-FINAL | Implementation-Ready Specification (consolidation) | Consolidation + gate |

No workstream may be skipped, merged, or reordered without a recorded
governance amendment to IS-00. IS-FINAL is not a new specification layer; it
is the consistency-checked consolidation that becomes the implementation input.

---

## 6. Dependency Map

### 6.1 Canonical sequence (default path)

```text
IS-00 (governance — DONE when this document is acknowledged)
  ↓
IS-01  Domain / Data
  ↓
IS-02  Workflow / State transitions
  ↓
IS-03  Access / Identity / Permission
  ↓
IS-04  API / Service contracts
  ↓
IS-05  Evidence / Attachment / Storage
  ↓
IS-06  Customer Projection / Portal
  ↓
IS-07  Audit / History / Correction
  ↓
IS-08  UI Functional
  ↓
IS-09  Security / Validation / Edge cases
  ↓
IS-10  Integration / Deployment / Migration
  ↓
IS-FINAL (consolidation + implementation-readiness check)
```

This sequence is the **default review order**, not a claim that every byte of
each workstream strictly requires the previous workstream's final text.

### 6.2 Sequential vs parallel — binding interpretation

**Strictly sequential (must complete as input before the dependent starts
normative specification):**

- IS-01 → IS-02: workflow guards reference domain entities, ownership, and
  identity boundaries. IS-02 normative transitions must not be drafted before
  IS-01 entity/ownership definitions are stable.
- IS-01 + IS-02 → IS-03: permission rules attach to entities (IS-01) and
  transitions/approvals (IS-02). IS-03 normative matrix must not be drafted
  before both are stable.
- IS-01 + IS-02 + IS-03 → IS-04: service boundaries and authorization
  enforcement points presuppose domain, lifecycle, and permission outputs.
  IS-04 contract drafting starts only after IS-01/02/03 are stable; no final
  endpoints are fixed in IS-00 (§7, IS-04).
- IS-03 + IS-04 → IS-06: portal eligibility, scope (Unit vs Company), and
  no-price / customer-safe rules presuppose the permission model and service
  responsibilities.
- ALL of IS-01…IS-10 → IS-FINAL: consolidation requires every input
  workstream reviewed and internally consistent.

**Parallelizable with explicit guards (may overlap once the stated inputs are
stable; overlapping work before that is exploratory notes only, not normative
specification):**

- IS-05 ∥ IS-06 (after IS-01/02/03 stable): evidence eligibility/storage-access
  rules and customer-projection rules both depend on domain/workflow/permission
  but not strictly on each other. Joint checkpoint required on:
  `photo_type = contextual classification, NOT visibility control` and the
  customer-serving restriction, so IS-05 and IS-06 cannot diverge.
- IS-07 ∥ IS-05/IS-06 (after IS-01/02 stable): audit/correction modeling needs
  entity + lifecycle event inventory; it does not need IS-05/IS-06 final text,
  but must reconcile with them at the joint checkpoint (evidence replacement,
  projection freshness, official-result vs controlling history).
- IS-08 UX exploration ∥ IS-01…IS-07: Figma/prototype and screen-behavior notes
  may proceed in parallel at any time as **non-normative input**; IS-08
  normative specification starts only after IS-01…IS-07 are stable, and Figma
  never overrides locked rules (§12).
- IS-09 runs as a **continuous verification lane** alongside IS-01…IS-08 and
  then finalizes as its own workstream after IS-08: abuse/invalid-transition /
  race / isolation cases are collected early, but the normative IS-09
  specification is written once the behaviors it constrains exist.
- IS-10 ∥ IS-04…IS-09 (after IS-01/02/03 + architecture inputs stable):
  environment/deployment/migration/Accurate-5-boundary requirements need the
  domain/workflow/permission shape but not the final UI text; final IS-10
  reconciliation happens before IS-FINAL.

**Joint checkpoints (mandatory regardless of parallel execution):**

1. CP-A (after IS-01/02): entity + lifecycle event inventory frozen enough for
   IS-03/05/07 to reference.
2. CP-B (after IS-03): permission/visibility/scope model frozen enough for
   IS-04/05/06 to reference.
3. CP-C (before IS-FINAL): cross-workstream consistency pass over
   IS-01…IS-10; unresolved blocking decisions must be NONE.

### 6.3 Dependency table (normative)

| Workstream | Direct upstream (normative input) | May overlap with (guarded) |
|---|---|---|
| IS-01 | IS-00, Level 1 (CD-01, CD-03…CD-11; Decision Register gates), Level 2 (TADR-01/02/07 + Baseline) | IS-08 exploratory UX notes |
| IS-02 | IS-01 (+ CD-11 canonical; TADR lifecycle direction) | IS-08 exploratory; IS-09 case collection |
| IS-03 | IS-01, IS-02 (+ locked identity/QR/access-model decisions; TADR-12/13/14/16) | IS-08 exploratory; IS-09 case collection |
| IS-04 | IS-01, IS-02, IS-03 | IS-10 (env/integration reqs) |
| IS-05 | IS-01, IS-02, IS-03 (eligibility/approval/access inputs) | IS-06, IS-07 (joint checkpoint) |
| IS-06 | IS-01, IS-02, IS-03, IS-04; IS-05 (joint checkpoint) | IS-05, IS-07 |
| IS-07 | IS-01, IS-02; IS-03/05/06 (reconciliation) | IS-05, IS-06 |
| IS-08 | IS-01…IS-07 (normative); Figma as UX input only | Exploratory UX at any time (non-normative) |
| IS-09 | IS-01…IS-08 (behaviors under test) + Level 2 | Continuous collection from IS-01 onward |
| IS-10 | IS-01/02/03 + Level 2 (Accurate 5 / env posture); reconcile with IS-04…IS-09 | IS-04…IS-09 |
| IS-FINAL | All of IS-01…IS-10 reviewed + consistent | — (strictly last) |

---

## 7. Workstream Scope

Template fields per workstream: Objective · Scope (includes) · Inputs ·
Dependencies · Outputs · Approval authority · Out-of-scope · Definition of Done
(exit criteria to become a valid input downstream). Approval authority here
means **specification acceptance authority**, not business/architecture
decision authority (see §9).

### IS-01 — Domain & Data Model Specification

- **Objective:** Define the logical domain/data requirements that all later
  workstreams reference: entities, relationships, ownership, identity
  boundaries, lifecycle-relevant data, canonical references, integrity rules,
  component/subtype rules.
- **Scope (includes):** Company / Contact / PIC / Unit / Component; Service
  Request; Work Order; Report; Visit; Evidence; Outcome; Conclusion; customer
  projection concepts (as concepts only — portal behavior belongs to IS-06);
  domain coverage for CD-01/03…CD-11-relevant entities at logical level.
- **Inputs:** Level 1 (CD-01, CD-03…CD-11 incl. CD11-001…029; Decision Register
  incl. locked identity/QR/access-model records); Level 2 (Architecture
  Baseline domain boundaries; TADR-01/02/07; workspace/ownership direction);
  Level 3 only for gap-spotting.
- **Dependencies:** IS-00. No normative dependence on later workstreams.
- **Outputs:** `docs/40-SPECIFICATION/IS-01-domain-data-model.md` (or
  equivalent): entity catalog, relationship/ownership map, identity-boundary
  statement, integrity requirements, open business/architecture questions log.
- **Approval authority:** AI Manager / Lead Architect for specification
  acceptance; Human/BA acknowledgement that no business rule was altered.
- **Out-of-scope:** Physical database schema; table/column specification;
  database product selection; framework/library selection; API endpoints;
  migration scripts; any business-rule invention.
- **Definition of Done:** (1) every entity/relationship traces to Level 1/2 or
  is marked `SPEC-OPEN`; (2) ownership + identity boundaries stated;
  (3) integrity rules stated without physical design; (4) CP-A inventory
  available for IS-02/03/05/07; (5) no schema/product/framework content
  present; (6) review confirms CD-11/architecture unchanged.

### IS-02 — Workflow & State Transition Specification

- **Objective:** Specify WO / Visit / Report lifecycles, approvals,
  cancellation, correction, reopen, re-create, emergency lane, validation
  gates, transition guards, outcome behavior, ON HOLD behavior.
- **Scope (includes):** All items above; canonical CD-11 lifecycle as primary
  input; guard conditions stated as requirements (actor + authority + state
  preconditions), not as code.
- **Inputs:** IS-01 (entities/ownership); Level 1 CD-11 canonical (primary) +
  CD-01/07/08 boundary rules + Decision Register deferred items (reminder
  policy, emergency timestamp convention — consumed as open, not decided);
  Level 2 lifecycle/architecture direction.
- **Dependencies:** IS-01 (strict). CP-A must be available.
- **Outputs:** `docs/40-SPECIFICATION/IS-02-workflow-state-transitions.md`:
  lifecycle definitions, transition tables with guards, approval/cancel/
  correction/reopen/re-create/emergency-lane requirements, ON HOLD semantics,
  escalation-tagged ambiguities.
- **Approval authority:** AI Manager / Lead Architect (specification); BA for
  any business ambiguity found (separate decision, not inside IS-02).
- **Out-of-scope:** API design; permission-matrix detail (IS-03); UI flow
  implementation; notification-interval invention (reminder policy is
  deferred — IS-02 states the hook/requirement shape only, content-agnostic).
- **Definition of Done:** (1) every transition has actor/authority/guard;
  (2) approval, cancel, correction, reopen, re-create, emergency lane each
  specified or explicitly deferred with tag; (3) ON HOLD behavior specified or
  escalated; (4) no invented thresholds/intervals; (5) IS-03-ready.

### IS-03 — Access, Identity & Permission Specification

- **Objective:** Specify authentication requirements, identity linkage,
  Contact/PIC handling, Verified PIC Link, Company scope, internal roles,
  customer PIC, approval authority, self-approval prevention, cross-company
  isolation, permission matrix, visibility boundaries.
- **Scope (includes):** All items above; Unit Scope vs Company Scope semantics
  exactly as locked (no extension); Google-only + application-based PIC
  registration + Manager/Admin approval as recorded constraints.
- **Inputs:** IS-01, IS-02; Level 1 (CD-03/07/08 + locked identity/QR/
  access-model records; CD-11 approval/correction authority); Level 2
  (TADR-12/13/14/16 + Baseline external-access boundary).
- **Dependencies:** IS-01 + IS-02 (strict). CP-A required; CP-B is this
  workstream's output.
- **Outputs:** `docs/40-SPECIFICATION/IS-03-access-identity-permission.md`:
  identity-link requirements, role/authority catalog, permission matrix,
  scope/visibility boundaries, isolation requirements, self-approval bar,
  escalation-tagged gaps.
- **Approval authority:** AI Manager / Lead Architect (specification);
  Human/BA for any access/visibility rule not already locked.
- **Out-of-scope:** Authentication/authorization implementation; product or
  library selection; endpoint definitions (IS-04); portal UX (IS-08);
  inventing access rights for deferred items (e.g., publication mechanism).
- **Definition of Done:** (1) permission matrix covers every IS-02 transition;
  (2) Unit/Company scope stated without expansion; (3) cross-company isolation
  stated; (4) self-approval prevention stated; (5) CP-B frozen for IS-04/05/06.

### IS-04 — API & Service Contract Specification

- **Objective:** Specify service boundaries, API responsibilities,
  request/response requirements, validation behavior, error behavior,
  authorization enforcement points, idempotency requirements where applicable,
  transaction boundaries — **without fixing final endpoints in advance**.
- **Scope (includes):** All items above, derived from IS-01/02/03; contract
  requirements stated capability-by-capability.
- **Inputs:** IS-01, IS-02, IS-03; Level 2 (module seams TADR-01; integration
  posture; no cross-DB FK; Accurate 5 transitional boundary as constraint).
- **Dependencies:** IS-01/02/03 (strict). Developed after CP-B.
- **Outputs:** `docs/40-SPECIFICATION/IS-04-api-service-contracts.md`:
  service-responsibility map, per-capability contract requirements, validation/
  error/idempotency/transaction requirements, enforcement-point map.
- **Approval authority:** AI Manager / Lead Architect (specification).
- **Out-of-scope:** Final endpoint paths/methods; schema; implementation;
  framework/library selection; test automation.
- **Definition of Done:** (1) every IS-02 transition and IS-03 enforcement
  need has a contract home; (2) error/validation/idempotency requirements
  stated per capability; (3) no final endpoint list presented as locked;
  (4) IS-05/06/10-ready.

### IS-05 — Evidence, Attachment & Storage Specification

- **Objective:** Specify photo/evidence, attachment, evidence type,
  eligibility, approval state, retention requirements, upload behavior,
  replacement/correction behavior, emergency evidence gate, storage
  requirements, access boundary, customer-serving restriction.
- **Scope (includes):** All items above, with the binding constraint:
  **photo_type is contextual classification, not visibility control;
  technician does not determine customer visibility.**
- **Inputs:** IS-01, IS-02, IS-03; Level 1 (CD-11 evidence/approval/report
  rules); Level 2 (file/attachment direction; access-boundary posture).
- **Dependencies:** IS-01/02/03 (strict for normative text); joint checkpoint
  with IS-06/07.
- **Outputs:** `docs/40-SPECIFICATION/IS-05-evidence-attachment-storage.md`:
  evidence taxonomy requirements, eligibility/approval-state rules, lifecycle
  (upload/replace/correct) requirements, retention/access requirements,
  emergency-gate requirements.
- **Approval authority:** AI Manager / Lead Architect (specification).
- **Out-of-scope:** Storage implementation/product selection; migration;
  customer-visibility decisions beyond the recorded restriction (portal
  eligibility lives in IS-06); inventing retention periods where business has
  not set them (state as `BA DECISION REQUIRED`).
- **Definition of Done:** (1) photo_type/visibility separation stated;
  (2) eligibility + approval-state coverage for every evidence-requiring
  transition; (3) replacement/correction path specified or escalated;
  (4) no storage product/implementation content; (5) reconciled with IS-06/07.

### IS-06 — Customer Projection & Portal Specification

- **Objective:** Specify customer projection, customer-safe data, eligibility,
  report FINAL gating, Verified PIC gating, company scope, QR behavior, portal
  access, unit-scoped public QR, company-scoped portal, internal-only
  exclusion, no-download requirement, projection freshness behavior.
- **Scope (includes):** All items above; explicit no-price rule for the
  customer portal as recorded; CONTROLLED QR (no anonymous access) as recorded.
- **Inputs:** IS-01…IS-05 (esp. IS-03 scope model, IS-04 responsibilities,
  IS-05 serving restriction); Level 1 (CD-11 customer-safe publication
  sections — consumed as bounded, with the publication *mechanism* recorded as
  deferred); locked QR/access-model decisions; Level 2 (TADR-12/14/16).
- **Dependencies:** IS-01/02/03/04 normative; IS-05 joint checkpoint.
- **Outputs:** `docs/40-SPECIFICATION/IS-06-customer-projection-portal.md`:
  projection-eligibility rules, scope rules (unit vs company), QR/portal
  access requirements, exclusion list, freshness requirements, deferred items
  (publication mechanism where not locked).
- **Approval authority:** AI Manager / Lead Architect (specification);
  Human/BA for the deferred customer-publication-mechanism decision.
- **Out-of-scope:** Portal implementation; QR-code generation implementation;
  inventing publication/permission mechanics for the deferred decision;
  relaxing no-price / no-anonymous-access / customer-safe constraints.
- **Definition of Done:** (1) eligibility traceable to report FINAL + Verified
  PIC + scope; (2) exclusions + no-download stated; (3) freshness behavior
  stated or escalated; (4) deferred mechanism explicitly tagged, not designed
  around; (5) reconciled with IS-05/07.

### IS-07 — Audit, History & Correction Specification

- **Objective:** Specify audit trail, actor, timestamp, action, object, reason,
  before/after, correction cycles, controlling history, official result,
  approval history, reopen history, re-create lineage, direct-edit audit
  linkage.
- **Scope (includes):** All items above; audit coverage for every mutating
  behavior in IS-02…IS-06; correction-cycle numbering; official-result vs
  controlling-history distinction.
- **Inputs:** IS-01, IS-02 (event inventory); IS-03/05/06 (reconciliation);
  Level 1 (CD-11 correction/reopen/re-create rules); Level 2 (auditability
  direction).
- **Dependencies:** IS-01/02 (strict); reconcile with IS-03/05/06 at joint
  checkpoint.
- **Outputs:** `docs/40-SPECIFICATION/IS-07-audit-history-correction.md`:
  audited-event catalog, per-event field requirements (actor/timestamp/action/
  object/reason/before-after), history/lineage requirements, direct-edit
  linkage requirements.
- **Approval authority:** AI Manager / Lead Architect (specification).
- **Out-of-scope:** Audit-storage implementation; log-product selection;
  inventing timestamp conventions for the deferred emergency-retroactive item
  (state requirement shape only, convention escalated).
- **Definition of Done:** (1) every IS-02 transition + IS-05/06 customer-facing
  event has audit coverage; (2) correction/reopen/re-create lineage specified;
  (3) before/after + reason captured where business requires; (4) reconciled
  with IS-05/06.

### IS-08 — UI/UX Functional Specification

- **Objective:** Specify role-based experience, screen behavior, field
  behavior, validation messages, progressive disclosure, mobile-first
  Technician flow, Admin/Manager/Sales/Coordinator flow, Customer PIC
  experience — functionally, not as implementation.
- **Scope (includes):** All items above; Figma prototype consumed strictly as
  UX input (see §12).
- **Inputs:** IS-01…IS-07 (normative behaviors to surface); Figma prototype
  (UX reference only); Level 1/2 constraints (visibility, approval, scope).
- **Dependencies:** Normative text after IS-01…IS-07 stable; exploratory UX
  notes may precede (non-normative, clearly labeled).
- **Outputs:** `docs/40-SPECIFICATION/IS-08-ui-functional.md`: per-role screen/
  field/validation behavior, progressive-disclosure rules, message catalog
  requirements, prototype-deviation log (each deviation dispositioned: adopt
  as usability-only, escalate as business question, or reject per CD-11).
- **Approval authority:** AI Manager / Lead Architect (specification);
  Human/BA for any business question the prototype surfaces.
- **Out-of-scope:** UI implementation; component/framework selection; visual
  design decisions presented as business rules; any prototype-driven business
  rule invention.
- **Definition of Done:** (1) every IS-02/03/05/06 behavior has a UI home;
  (2) validation messages trace to IS-02/04/09 rules; (3) prototype deviations
  fully dispositioned; (4) no implementation content.

### IS-09 — Security, Validation & Edge Cases

- **Objective:** Specify authorization enforcement, data isolation, validation,
  abuse cases, invalid transitions, race conditions, duplicate submission,
  stale data, concurrent edits, attachment abuse, customer boundary, audit
  integrity, security-sensitive failure modes.
- **Scope (includes):** All items above, as requirements + required system
  responses (reject/contain/audit), not as code.
- **Inputs:** IS-01…IS-08; Level 2 (isolation/security posture); Level 1
  boundaries (workspace ownership CD-07/08, approval authority CD-11).
- **Dependencies:** Collection lane from IS-01 onward; normative text after
  IS-08 (strictly: the behaviors under test must exist first).
- **Outputs:** `docs/40-SPECIFICATION/IS-09-security-validation-edge-cases.md`:
  threat/abuse catalog, per-case required behavior, isolation/integrity
  requirements, failure-mode requirements.
- **Approval authority:** AI Manager / Lead Architect (specification);
  independent review lane reserved for AI Auditor at IS-FINAL/implementation.
- **Out-of-scope:** Security implementation; penetration testing; test
  automation; inventing business policy to close a security gap (escalate
  instead).
- **Definition of Done:** (1) every IS-02 transition has invalid-transition
  coverage; (2) isolation + customer-boundary + audit-integrity requirements
  stated; (3) race/duplicate/stale/concurrent/attachment-abuse cases covered;
  (4) unresolved items tagged to owner, none silently closed.

### IS-10 — Integration, Deployment & Migration Specification

- **Objective:** Specify Accurate 5 boundary, external integration
  requirements, environment requirements, deployment requirements, migration
  strategy, backup/restore requirements, operational considerations —
  as requirements, not execution.
- **Scope (includes):** All items above; Accurate 5 as transitional authority
  for accounting/inventory; hard constraint: **no cross-database foreign key**.
- **Inputs:** IS-01/02/03 (+ IS-04…IS-09 for reconciliation); Level 1
  (CD-09/10/11 boundaries; CD-01 exclusions); Level 2 (integration/deployment
  posture); Decision Register (deployment operational context — deferred, not
  decided).
- **Dependencies:** IS-01/02/03 + Level 2 for normative start; reconcile with
  IS-04…IS-09 before IS-FINAL.
- **Outputs:** `docs/40-SPECIFICATION/IS-10-integration-deployment-migration.md`:
  integration-boundary requirements, environment/deployment requirements,
  migration-strategy requirements, backup/restore + operational requirements,
  deferred-context log.
- **Approval authority:** AI Manager / Lead Architect (specification);
  Human/BA for deployment-context and any accounting-scope decisions.
- **Out-of-scope:** Migration scripts; deployment execution; integration code;
  accounting-engine design (deferred future scope); inferring deployment
  requirements where no decision exists.
- **Definition of Done:** (1) Accurate 5 boundary + no-cross-DB-FK stated;
  (2) env/deployment/migration/backup requirements stated or explicitly
  deferred with tag; (3) no execution artifacts; (4) IS-FINAL-ready.

### IS-FINAL — Implementation-Ready Specification

- **Objective:** Consolidate IS-01…IS-10 into one internally consistent,
  approved, implementation-derivable package. No new specification content
  originates in IS-FINAL except consistency resolutions that alter neither
  business nor architecture baselines (each logged).
- **Scope (includes):** Cross-workstream consistency check; terminology
  unification; requirement-ID assignment; traceability matrix (requirement →
  CD/TADR source); gap/escalation register close-out; implementation-scope
  derivation statement.
- **Inputs:** All of IS-01…IS-10 (reviewed revisions) + IS-00 governance +
  Level 1/2 baselines.
- **Dependencies:** All IS workstreams (strictly last).
- **Outputs:** `docs/40-SPECIFICATION/IS-FINAL-implementation-ready-specification.md`
  (+ requirement/traceability annexes as needed): consolidated specification,
  consistency log, unresolved-blocking-decisions statement (= NONE required),
  implementation-scope derivation.
- **Approval authority:** Human/BA acknowledgement (or delegated acceptance
  per project governance) that IS-FINAL is the implementation input; AI Auditor
  independent review lane before any implementation authorization.
- **Out-of-scope:** Implementation itself; Programmer TASK creation (a
  separate, explicitly authorized step after IS-FINAL approval); any silent
  baseline change.
- **Definition of Done:** §13 gate satisfied (IS-FINAL approved; blocking
  decisions NONE; scope deterministically derivable). Until then IS-FINAL is
  DRAFT, and implementation remains unauthorized.

---

## 8. Definition of Done

### 8.1 Universal DoD (every IS workstream incl. IS-FINAL)

A workstream is DONE only when all of the following hold:

1. **Output exists** at its canonical path under `docs/40-SPECIFICATION/`.
2. **Traceability:** every normative statement traces to Level 1/2 or is
   explicitly tagged (`BA DECISION REQUIRED` /
   `ARCHITECTURE DECISION REQUIRED` / `SPEC-OPEN` / deferred reference).
3. **No invention:** no new business rule, no architecture re-decision, no
   deferred-item resolution by assumption.
4. **No implementation:** no schema, endpoint finalization (except as IS-04
   permits at contract level), code, migration, product/framework selection,
   or Programmer TASK.
5. **Self-review:** author pass confirms terminology consistent with IS-01 and
   prior workstreams; conflicts with CD-11/architecture explicitly checked.
6. **Handoff readiness:** downstream workstream can consume it without
   re-interpreting locked rules (exit criteria in §7 met; checkpoints CP-A/B/C
   observed).

### 8.2 Per-workstream exit emphasis

- IS-01 DONE → IS-02/03/05/07 may start normative work (CP-A).
- IS-02 DONE → IS-03 normative matrix may start.
- IS-03 DONE → IS-04/05/06 normative work may start (CP-B).
- IS-04 DONE → IS-06/10 reconciliation may complete.
- IS-05 + IS-06 + IS-07 DONE + reconciled → IS-08 normative text may complete.
- IS-08 DONE → IS-09 normative text may complete.
- IS-01…IS-10 DONE + CP-C passed → IS-FINAL consolidation may complete.
- IS-FINAL DONE + approved → implementation *planning* may be proposed;
  implementation itself only on separate explicit authorization (§13).

---

## 9. Approval Governance

Authority separation is binding. No role silently assumes another role's
authority.

| Decision kind | Owner | Scope | Notes |
|---|---|---|---|
| Business rule | Business Authority (Human / BA) | Operational boundaries, approvals, visibility/publication rights, lifecycle semantics, thresholds, intervals, classifications with business meaning | Only BA creates/changes. AI surfaces gaps with options; never decides. CD-11 changes require BA sign-off, not IS edit. |
| Architecture direction | Architecture authority (Human-approved; Lead Architect proposes) | Module seams, identity-model shape, integration posture, deferred-scope posture, TADR content | TADR-01…18 already approved. Any IS-found conflict → `ARCHITECTURE DECISION REQUIRED`; IS does not edit architecture. |
| IS Specification (system behavior/detail) | AI Manager / Lead Architect (author); Human/BA acknowledgement | Behavior/detail requirements within business+architecture baselines; `SPEC-OPEN` resolutions that alter neither baseline | Specification acceptance per §7/§8. Escalation per §10. |
| Implementation | AI Programmer — **only after §13 gate** | Code, schema, migrations, tests, technical execution from IS-FINAL | No implementation from a single workstream; no anticipation of IS-FINAL. |
| Independent review / verification | AI Auditor | Correctness, security, isolation, authorization, auditability, regression, boundary verification | Lane reserved at IS-FINAL review and post-implementation; auditor does not re-decide business/architecture. |

Records of authority: business changes → CD / Decision Register; architecture
changes → TADR / Baseline / Approval Package amendment; specification
acceptance → workstream DoD + IS-FINAL approval; implementation authorization →
separate explicit Human authorization (never inferred from IS progress).

---

## 10. Decision Escalation

Apply exactly; do not resolve ambiguity with assumption.

| Finding during IS | Tag | Handling |
|---|---|---|
| Business ambiguity (rule missing, two readings of a CD, deferred item needed now) | `BA DECISION REQUIRED` | Log with: source text, why it blocks, options (no recommendation presented as decision), affected workstreams. Halt normative text in the affected area; continue only in unaffected areas. |
| Architecture conflict (IS requirement cannot be written within approved direction; TADR gap/contradiction) | `ARCHITECTURE DECISION REQUIRED` | Log with: TADR section, conflict statement, impact. Do not edit architecture silently. Continue only where direction is sufficient. |
| Specification ambiguity (wording/organization/detail choice that changes neither business nor architecture baseline) | Resolve within IS | Resolve, record the resolution + rationale in the workstream; keep it reversible. If any doubt whether a baseline is affected, escalate instead. |
| Implementation choice (product, framework, code shape, migration detail, endpoint spelling) | Defer | Defer to implementation planning / Programmer unless the approved architecture already constrains it. IS states the requirement, not the choice. |

Every escalation entry records: date, raising workstream, verbatim source (if
any), affected requirement IDs, and current status (OPEN / ANSWERED /
SUPERSEDED). IS-FINAL may not be approved while any blocking entry is OPEN.

---

## 11. Change Control

1. **Conflict with CD-11:** CD-11 wins. Do not edit CD-11. Log the conflict,
   tag `BA DECISION REQUIRED` if a business change is genuinely needed, and
   write IS text conformant with CD-11 as it stands.
2. **Conflict with approved architecture:** do not silently change
   architecture. Mark `ARCHITECTURE DECISION REQUIRED`, log per §10, and write
   IS text conformant with the approved direction as it stands.
3. **Change needing a business-rule change:** `BA DECISION REQUIRED`, even if
   discovered via technical work. Technical convenience never justifies a rule
   change.
4. **Change needing an architecture change:** `ARCHITECTURE DECISION REQUIRED`
   via TADR/Baseline amendment path; IS workstreams wait for the amended
   direction in the affected area.
5. **IS-internal correction:** allowed within IS (terminology, organization,
   non-baseline detail) with a log entry; must remain reversible and must not
   mask a business/architecture issue as an editorial fix.
6. **IS-00 amendment:** sequence/registry/governance changes require an
   explicit recorded amendment to this document, not a silent deviation in a
   workstream.

---

## 12. UI / Figma Boundary

1. UI exploration (including Figma prototyping) may run in parallel at any
   time as **non-normative input**.
2. Figma is permitted as: UX reference, usability-discussion aid, and input to
   IS-08.
3. Figma is **not** a source of business rules and cannot change CD-11 or any
   locked decision.
4. On prototype-vs-CD-11 conflict: CD-11 wins; the prototype yields.
5. Where the prototype needs an undecided rule: log a design/specification
   question tagged per §10 (`BA DECISION REQUIRED` if business; otherwise a
   `SPEC-OPEN` item). Do not invent a business rule to fit the prototype.
6. IS-08 maintains a prototype-deviation log; every deviation is dispositioned
   (adopt as usability-only / escalate / reject) before IS-08 is DONE.

---

## 13. Implementation Gate

Implementation authorization is a separate explicit Human decision. It is NOT
granted by IS progress, by any single workstream, or by this document.

All of the following are required before any implementation authorization:

1. Required IS workstreams (IS-01…IS-10) DONE per §7–§8.
2. Cross-workstream consistency check complete (CP-C) with log.
3. Unresolved blocking decisions = NONE (all `BA/ARCHITECTURE DECISION
   REQUIRED` entries blocking implementation are ANSWERED or formally waived
   by the owning authority with recorded scope).
4. IS-FINAL approved as the implementation input.
5. Implementation scope deterministically derivable from IS-FINAL (a Programmer
   can decompose it without re-deciding business or architecture).

Until then: **AI Programmer must not start coding on the basis of any single
IS workstream.** No schema, migration, API, UI, deployment change, or TASK
implying authorization is permitted.

---

## 14. Open / Deferred Items

Carried forward explicitly — IS workstreams consume these as constraints/gaps,
never as decided content. (Sources: Decision Register; CD-11 deferred-details;
Architecture Approval Package deferred scope.)

| # | Item | Current state | IS handling |
|---|---|---|---|
| O-01 | CD-02 content | DEFERRED / UNVERIFIED, absent | Not an input. Never reconstructed. If needed, `BA DECISION REQUIRED`. |
| O-02 | Customer publication mechanism / permission model | **Business expectation DECIDED — HBA D-01A = RETAIN**; publication permission already canonical; serving/mechanism remains architecture | IS-06 specifies eligibility/scope/exclusions around it; the serving **mechanism** itself is tagged, not designed. |
| O-03 | Reminder / automation policy (generation + intervals) | UNRESOLVED / PENDING HUMAN DECISION | IS-02 states hook/shape content-agnostically; no intervals invented. |
| O-04 | Emergency retroactive timestamp convention | UNRESOLVED / PENDING HUMAN DECISION | IS-02/IS-07 state requirement shape only; convention escalated. |
| O-05 | Deployment operational context | UNRESOLVED / PENDING HUMAN DECISION | IS-10 states requirements; no inferred deployment facts. |
| O-06 | Identity-link / QR / access-model formal CD documentation | LOCKED HUMAN DECISIONS, formal CD pending | Consumed exactly as recorded (TADR-12/13/14/16); IS does not extend them. |
| O-07 | Accounting/finance/tax scope (GL, COA, COGS, valuation, tax engine, revenue recognition) | DEFERRED future scope per CD-01/04/05/06/09/10/11 | Excluded from IS normative scope; Accurate 5 remains transitional authority (IS-10). |
| O-08 | Architecture items F-1 (deferred, non-blocking), C-1/C-2 (documentation cleanup) | As approved | Untouched by IS; implemented scope must not depend on them silently. |
| O-09 | Final API endpoints; DB product; physical schema; framework/library; storage product; test automation | Explicitly deferred to post-IS-FINAL | IS-00 forbids fixing them (see §7 per-workstream out-of-scope). |
| O-10 | Figma prototype business-rule questions (to be logged during IS-08) | Not yet raised | Logged + dispositioned in IS-08 deviation log; prototype never overrides. |

---

## 15. Traceability Strategy

15.1. **Requirement IDs:** each normative statement in IS-01…IS-10 carries a
stable ID (`IS-<ws>-<nnn>`, e.g., `IS-02-014`). Non-normative notes/examples
carry no ID.

15.2. **Source linkage:** each requirement cites its Level 1/2 source
(CD section / CD11-xxx item / TADR section / locked-decision record) or its
escalation tag (`BA/ARCHITECTURE DECISION REQUIRED`, `SPEC-OPEN`, deferred
reference). Requirements without a source or tag fail review.

15.3. **Chain preserved:**

```text
Human Decision → CD / Decision Register → TADR / Baseline → IS-xx-yyy → (post-gate) Implementation → Test → Audit
```

IS-FINAL ships the consolidated matrix (requirement → source → covering
workstream → downstream consumer). Missing links are reported as gaps, not
bridged by inference.

15.4. **Registers maintained across the phase:** escalation log (§10), change
log (§11), prototype-deviation log (§12), deferred-item log (§14). IS-FINAL
closes or carries each entry explicitly; no entry is silently dropped.

15.5. **Non-authority statement:** this document and all IS workstream
documents record and specify; they do not promote, modify, or supersede CD-11,
any locked CD, or any approved TADR. Canonical business/architecture documents
remain authoritative for their contents.

---

*End of IS-00. Next candidate (not started): **IS-01 DOMAIN & DATA MODEL
SPECIFICATION** — awaiting explicit Business Authority instruction. STOP.*
