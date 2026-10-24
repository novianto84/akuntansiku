# IS-FINAL — MitraSP CRM Implementation Specification — Consolidated Package

```text
Document ID: IS-FINAL
Title: Implementation Specification Package — Consolidated Final (V1)
Version: 1.0 (initial consolidation under SPECIFICATION COMPLETION EMPOWERMENT, Prompt 1)
Status: CONSOLIDATION — READY FOR FINAL REVIEW & HBA ACCEPTANCE
Authority: AI Manager / Lead Architect (consolidation author). Business Authority owns all rules,
  acceptance of canonical/approved statuses, and build authorization.
Purpose: Single package proving the implementation specification is sufficient, coherent,
  traceable, and free of implementation-destructive gaps; and identifying the isolated HBA
  decisions and the build gate.
Sources: IS-00..IS-12 set as inventoried here; CD-01..CD-11 (LOCKED/SIGNED); BD-SR series,
  BD-WORKTYPE, BD-WORKMODEL (LOCKED); Architecture Baseline + Approval Package + TADR-01..18
  (APPROVED); Decision Register; Architecture Lock; AI Operating Rules; Prompt-1 baseline.
Implementation: NO code/schema/migration/API/UI/deployment. This is the final specification gate.
```

> This document does not restate every § of the IS set. It proves completeness, resolves none of
> the HBA decisions itself (it isolates them), and links each implementation-critical behavior to
> its owning specification.

---

## 1. Specification Inventory & Authority Status

| IS | File | Exists? | Status | Gate |
|---|---|---|---|---|
| IS-00 | is-specification-governance-master-plan.md | ✅ | PROPOSED-CANONICAL | **pending BA acknowledgement** |
| IS-01 | domain-data-model-specification.md | ✅ | SPECIFICATION | acknowledgement required |
| IS-02 | service-execution-specification.md | ✅ | READY FOR DECOMPOSITION | pending BA acceptance |
| IS-02-TD | IS-02-technical-decomposition.md | ✅ | READY FOR ARCH REVIEW | pending acceptance |
| IS-03 | access-identity-permission.md | ✅ | **LOCKED/CANONICAL** | — |
| IS-04 | api-service-contract.md | ✅ | **LOCKED/CANONICAL** | — |
| IS-05 | IS-05-evidence-attachment-storage.md | ✅ | **LOCKED/CANONICAL** | — |
| IS-06 | IS-06-customer-projection-portal.md | ✅ | DRAFT/PROPOSED (v1.1) | **HBA D-01A = RETAIN materialized; OQ-02 already canonical; serving mechanism = architecture** |
| IS-07 | IS-07-audit-history-correction.md | ✅ | **LOCKED/CANONICAL** | — |
| IS-08 | IS-08-ui-user-interface.md | ✅ (new, this phase) | PROPOSED — draft for review | final gate |
| IS-09 | IS-09-security-edge-cases.md | ✅ (new, this phase) | PROPOSED — draft for review | final gate |
| IS-10 | IS-10-deployment-migration.md | ✅ (new, this phase) | PROPOSED — draft for review | final gate |
| IS-11 | IS-11-workspace-tenant-isolation.md | ✅ | **APPROVED/CANONICAL** | — |
| IS-FINAL | this file | ✅ | CONSOLIDATION | ready for review |

## 2. Domain Invariants (Consolidated, SETTLED — do not reopen)

From CD-11, BD series, reconciliation:
- **SR** = formal initial request/need; sources incl. customer/PIC, technician recommendation,
  Sales, Coordinator, Manager, permitted channels; SR may or may not become a WO; **Requested Scope
  in SR is NOT a JOB**; SR has no Job child; SR may be skipped where a valid direct WO path exists.
- **WO** = authorized/assigned work; lifecycle `DRAFT→OPEN→IN_PROGRESS→WAITING APPROVAL→CLOSED`,
  terminal `CANCELLED` (only from OPEN/IN_PROGRESS). `ASSIGNED` not a state; `UNASSIGNED` is a
  condition; `IN_PROGRESS` requires responsible person; WO may exist without Unit then require Unit
  before closure; **no fake Unit**.
- **JOB** belongs to exactly one WO; **no Issued/Add/Corrective Job separate entities**; SCOPE is a
  JOB property; nothing but a real WO owns a JOB. Added-During-Execution is a marker.
- **Finding/Diagnosis/Recommendation are not JOB.**
- **Visit:** types INITIAL / ON PROCESS (system-determined); Visit completion does NOT close the WO;
  1 WO → 1 Report → N Visits.
- **Report:** exactly one per WO, assembled from Visits; FINAL only when WO CLOSED; no FINALIZE
  action; Final Conclusion technician-drafts, approver settles.
- **Approval/Closure:** four phases distinct; APPROVE REPORT ⇒ WO=CLOSED; no CLOSE_WO; no
  self-approval; technician never approves/closes own WO.
- **Continuation** is not a new WO (narrative, same WO); ON HOLD is a distinct outcome.

## 3. Dependency Graph (final, toward build)

```text
IS-00 (acknowledgement)
  ├─ IS-01 (entities)
  │    ├─ IS-02 (service behavior) → IS-02-TD (decomposition)
  │    ├─ IS-03 (access/identity) → IS-09 (security edges)        [matrix content OPEN: HD-06]
  │    ├─ IS-04 (API contracts) ← IS-02/03
  │    ├─ IS-05 (evidence) · IS-07 (audit) — LOCKED, parallel
  │    └─ IS-11 (workspace isolation) — APPROVED, parallel
  └─ IS-06 (customer portal) → [HD-01 serving mechanism: architecture] → IS-08 (UI incl. gated portal)
                                              └→ IS-10 (deployment/migration)
                                                    │
                                  IS-FINAL  →  BUILD AUTHORIZATION  →  WP-01…WP-10
```

**Critical path:** IS-00 → IS-01 → IS-02 → IS-02-TD → IS-FINAL → BUILD AUTHORIZATION.
**Parallelizable:** HD-06 decision, IS-06 finalization (HD-01 serving mechanism: architecture; OQ-02 already canonical), acceptance gates of the new
IS-08/09/10. **Deferred/non-blocking:** automatic reminders, HD-07A formal CD, SR-V2 backlog,
F-1/OQ content items (see §8).

## 4. Implementation-Critical Behavior — Owning Spec Map

| Behavior | Owning spec(s) | Block |
|---|---|---|
| AuthN/AuthZ + access scopes + PIC/Company | IS-03, IS-09 | HD-06 content |
| Tenant/workspace isolation guards | IS-11 | — |
| SR lifecycle/closure/lineage | IS-01, IS-02, IS-04 (A1–A3) + BD-SR | — |
| WO lifecycle/JOB/assignment/emergency | IS-02, IS-04 (A4–A6) + CD-11, BD-WORK* | — |
| Visit/evidence | IS-02, IS-04 (A7–A12), IS-05 | — |
| Report/approval/closure/reopen | IS-02, IS-04 (A9–A11), IS-07 | — |
| Customer portal/QR projection | IS-06 (gated), IS-08, IS-09 | HD-01 serving mechanism (architecture); OQ-02 canonical |
| Evidence/file | IS-05 | — |
| Audit/history/correction | IS-07 | — |
| Data model / invariants | IS-01 | acknowledgement |
| API/service contracts | IS-04 | — |
| UI behavior | IS-08 (new) | — |
| Security/edge | IS-09 (new) | — |
| Deployment/migration | IS-10 (new) | — |

## 5. Authorization Blueprint (Consolidated)

- Identity → role authority → workspace/company scope → business-role authority (IS-03/11/09).
- Locked authorities enforced: V1 `CLOSE_SR` Admin+Manager; no self-approval; technician not
  approver of own WO; external Google-only; LOGIN≠Company Access; non-PIC Unit Scope not browsing;
  no price leakage.
- **Remaining matrix cells (approver lists, suggest/approve detail, material-take, visibility
  overlays) = OPEN (HD-06)** — contracts expose hooks, never invented values.

## 6. API & Evidence & Audit (Consolidated Reference)

- API: IS-04 business-action catalog A1–A12, service-per-aggregate ownership, no endpoint/path/
  schema design, technology-neutral.
- Evidence: IS-05 locked floor (capture slots, opt-out-with-reason, eligibility, mediation).
- Audit: IS-07 append-only events emitted by every IS-04 action; state-history separation; no
  competing models.

## 7. Acceptance Criteria (Consolidated)

- Each IS has its own AC (see the document). Externally: zero UNSOURCED requirement; consistent
  SETTLED vocabulary; no deprecated lifecycle terms; canonical dependencies coherent; open cells
  explicit; technology remains neutral where not decided.

## 8. Known Deferred / Non-Blocking Items

- Automatic reminders & interval policy (CD-11 §23) — can remain disabled.
- HD-07A formal CD documents (identity-link/QR/Business Access Model) — semantics locked, doc pending.
- SR-V2 multi-channel intake — backlog, non-V1.
- F-1 service-execution detail (OQ-15), checklist/evidence/subtype taxonomy extras, overdue timer —
  deferred per owning specs.
- Acknowledgment / continuation / emergency retroactive timestamp refinements — deferred where
  CD-11 already covers the base rule.

## 9. Repository Baseline (Prompt-1 §10 / §14 declaration)

Inspection of `/home/anto/akuntansiku` (read-only):
- Branch `master`; commit `137c6d5` "Metode HPP jadi setting global perusahaan, berlaku semua item,
  terkunci setelah transaksi".
- Modified: `app.py`, `public/app.js`, `opencode.json`, `.gitignore`.
- Untracked: `docs/` (entire canonical/spec tree incl. all IS), `AI_CONTEXT_INDEX.md`,
  `AI_GOVERNANCE_CANONICAL.md(.sha256)`, `AI_OPERATING_RULES.md`, `ARCHITECTURE_LOCK.md`,
  `BRIDGE_CONTRACT*.md(/.sha256)`, `DECISION_REGISTER.md(.sha256)`, `_sandbox_ops_activation/`,
  `.opencode/`.
- Application files present: `app.py` (≈258 KB, ~3282 lines), `public/{index.html,app.js,styles.css}`
  (app.js ≈190 KB), `requirements.txt`, `Dockerfile`, `docker-compose.yml` (container `erp-msp`
  maps 8000). DB `data/database.db` ≈586 KB, 68 tables — **ERP schema, not CRM.**
- **Implication:** the working tree is NOT a clean baseline. Build must start only from a declared,
  object-differentiable baseline per IS-10 §6. Nothing was reset/cleaned/deleted/committed.

## 10. HBA DECISION BATCH (isolated genuine decisions)

| ID | Question | Affects | Consequence | Blocks V1? |
|---|---|---|---|---|
| HD-06 | Full permission-matrix content (approver lists, suggest/approve detail, material-take, admin overlays) | IS-03/04/09/08 | Chosen → enables route/UI guards; undecided → those routes can't activate | Affected areas — isolate |
| HD-01 | Customer publication **mechanism**: snapshot vs live serving (business expectation RESOLVED — HBA D-01A = RETAIN) | IS-06/08/09 | Mechanism choice only; retention of previously presented content is already decided (RETAIN) | Portal/QR publication only |
| OQ-02 | Publication permission model / approval layer | IS-06/09 | Already canonical under CD-11 §21 + IS-03 §7 + IS-01 R-27; no new permission model or approval layer | No new HBA decision |
| Tech stack (IS-10 §2) | DB product, runtime/module structure, topology, IdP wiring | IS-10, WP-01 | Must be chosen to define buildable foundation; not a business rule | **WP-01 foundation** |
| Deployment context | Environment/shape of production CRM | IS-10, go-live | Needed before any rollout | Go-live only |

> This table records decision/approval items from the earlier specification-baseline stage; statuses
> must be read using the current DECISION_REGISTER and later HBA decisions. Customer publication business
> expectation is now resolved (HBA D-01A = RETAIN); OQ-02 is already canonical; HD-06 remains separate
> internal authority content. These statuses do not create or reopen business decisions.

## 11. Final Readiness Gate

| # | Criterion | Status |
|---|---|---|
| 1 | Required specifications exist | ✅ all IS-00…IS-11 + IS-08/09/10/IS-FINAL now exist (08/09/10 added this phase) |
| 2 | Authority status clear | ⚠️ IS-00/01/02/08/09/10 pending acceptance; 03/04/05/07/11 approved/locked |
| 3 | No unresolved contradiction | ✅ SETTLED semantics consistent; no canonical conflict found |
| 4 | Implementation-critical behavior defined | ✅ (owning-spec map, §4) |
| 5 | Permission behavior defined | ⚠️ structure locked; content HD-06 open |
| 6 | Tenant boundaries defined | ✅ IS-11 |
| 7 | API behavior defined | ✅ IS-04 |
| 8 | Evidence behavior defined | ✅ IS-05 |
| 9 | Audit behavior defined | ✅ IS-07 |
| 10 | UI behavior defined where required | ✅ IS-08 (portal gated) |
| 11 | Security edge behavior defined | ✅ IS-09 |
| 12 | Deployment/migration requirements defined | ✅ IS-10 |
| 13 | Dependency graph defined | ✅ §3 |
| 14 | Acceptance criteria defined | ✅ per IS + §7 |
| 15 | Repository baseline declared | ✅ §9 |
| 16 | IS-FINAL complete | ✅ this document |
| 17 | Genuine HBA decisions isolated | ✅ §10 |

**Build authorization boundary (status summary):**
1. Human acceptance/authorization remains applicable to the specification package as required by the
   current governance process.
2. Tech-stack/build gates for WP-01 and affected internal HD-06 permission areas remain separately
   scoped.
3. Customer portal business expectations are resolved (D-01A = RETAIN; D-01B semantic freshness;
   OQ-02 canonical). Portal serving/snapshot/refresh mechanisms remain architecture work, not an
   unresolved HBA business decision. Implementation still requires the applicable explicit build
   authorization.

## 12. Build Gate Statement

```text
SPECIFICATION PACKAGE: CONSOLIDATED
IMPLEMENTATION-CRITICAL SPECIFICATION: COMPLETE
DEPRECATED VOCABULARY: EXCLUDED
CANONICAL CONFLICTS: NONE FOUND
GENUINE HBA DECISIONS: ISOLATED (5)
STATUS (per Prompt-2 precondition):
    READY FOR PROMPT 2 — FINAL BUILD GATE + WP-01
    (contingent on HBA acceptance of the acceptance-gates and resolution of the §10 batch)
```

- **NOT** `SPECIFICATION READY FOR BUILD` yet — because IS-00/01/02 acceptance and the §10 decision
  batch (specifically tech stack blocking WP-01) are owned by Human Business Authority, not by
  Hermes within its envelope.
- **NOT** `NOT READY` — the entire Hermes-authorable completeness work is now done; remaining items
  are genuine HBA items, correctly isolated and bundled.

---

## 13. NO-IMPLEMENTATION CONFIRMATION

This phase produced **specification documents only** (IS-08, IS-09, IS-10, IS-FINAL). It did **not**
- modify application source code, schema, or configuration;
- create migrations, API, UI, or program entry points;
- run a Programmer, deploy anything, or mutate repository data/files beyond the four new spec docs;
- commit, reset, clean, or delete any repository content;
- create or change any business rule.

*End of IS-FINAL v1.0.*
