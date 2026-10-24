# IS-10 — Implementation, Deployment & Migration Requirements (V1)

```text
Document ID: IS-10
Title: Implementation, Deployment & Migration Requirements (V1)
Version: 1.0 LOCKED/CANONICAL — BUSINESS AUTHORITY APPROVAL 2026-10-13 (HBA-DECISIONS-22)
Status: LOCKED / CANONICAL — BUSINESS AUTHORITY APPROVAL 2026-10-13 (HBA chat: kunci IS-10; supersedes PROPOSED). Prior status retained as history: PROPOSED — DRAFT FOR REVIEW (to be raised via IS-FINAL acceptance gate).
Authority: AI Manager / Lead Architect (specification author). Business Authority owns deployment
  authorization, production data mutation, and production deployment. Technical stack choice where
  approved architecture has NOT fixed it is recorded as a genuine required technical/HBA decision.
Scope: Implementation boundaries; environment requirements; migration/rollback requirements;
  data origin; deployment requirements; runtime config; baseline declaration linkage; the
  technology decisions genuinely needed but NOT yet fixed by canonical/approved architecture.
Sources: Architecture Baseline + Approval Package §§1–12; TADR-01..18 (APPROVED); IS-11 (APPROVED);
  IS-03, IS-05, IS-07 (LOCKED); CD-01/CD-07/CD-08 (LOCKED); Prompt-1 baseline inspection
  (git status of /home/anto/akuntansiku). Existing ERP container is EVIDENCE, NOT architecture.
Implementation: NO code/schema/migration/API/UI/deployment/rollout. Technology-neutral.
```

> Defines the *requirements* for placing MitraSP CRM V1 into an environment and migrating data,
> and explicitly records which technology decisions remain open. It does NOT select a stack, does
> NOT copy the ERP deployment, and does NOT authorize any rollout.

---

## 1. Boundary: Existing ERP is a Baseline, not a Template

The existing repository `/home/anto/akuntansiku` is the **ERP "Akuntansiku"** (Flask-like Python
single-file `app.py`, SQLite, container `erp-msp` on port 8000). Per Prompt-1 §11, it is treated as
`EXISTING APPLICATION BASELINE` — potential reusable foundation/infrastructure/component only after
explicit domain analysis. It is **NOT** the MitraSP CRM architecture and its deployment shape must
not be adopted by assumption.

**Reusable (candidate, needs analysis):** generic patterns (auth/session, file serving, basic
hosting) if and only if they satisfy IS-11/IS-09/IS-03. **Incompatible / not to reuse as-is:**
accounting/GL/tax engine, ERP auth model, ERP single-file coupling, ERP database shape.

## 2. Technology Decision Requirement (Genuinely Open)

Canonical/approved architecture is **technology-neutral by explicit choice**: TADR-05 "product
unde decided" (database); TADR-17 "candidate direction only" (topology); IS-11 §17 "no
product/framework/auth tech/topology prescribed". **Therefore the following are genuine technical
decisions NOT derivable from business authority and MUST be recorded, not invented:**

| Tech decision | Need | Status | Decision owner |
|---|---|---|---|
| Database product & migration tool | One-DB strategy (TADR-05); schema foundation | OPEN — not fixed | Architecture/technical (post-approval); confirm within approved envelope |
| Application runtime / language / modular-monolith structure | TADR-01 modular monolith | OPEN | Architecture/technical |
| Deployment topology / hosting | TADR-17 candidate only | OPEN — deployment context is an HBA/architecture decision | Business + Architecture (deployment context) |
| External IdP wiring (Google) | IS-03/IS-09 Google-only | OPEN (mechanism) | Architecture/technical |

These are **not business rules**; recording them is required so a Programmer does not guess. They
are bundled in the HBA DECISION BATCH for the deployment-context item and technical decisions where
the mandate requires.

## 3. Environment Requirements (V1)

- A **development** and a **test/staging** environment, separable from production, each with
  isolated data. No production data in dev/test.
- Workspace/company isolation must be exercisable (IS-11 negative paths) in test.
- Deterministic, repeatable environment provisioning (config-as-code) — mechanism open.

## 4. Migration Requirements (V1)

- **Reversible migrations:** every schema change must be forward-and-reversibly defined and runnable
  against non-production with a documented rollback path. No production migration without explicit
  HBA authorization.
- **Data origin:** MitraSP CRM does not inherit ERP transactional data by default. Shared masters
  (Company/Contact/PIC, and any explicitly-shared master per CD-07/CD-08) may be sourced only after
  ownership analysis; transactional/service data starts on the CRM side. No silent mapping of ERP
  `customers`/`projects`/`approvals`/`assets` onto CRM entities.
- Migration to production records before-state, forward state, rollback state, and validation
  evidence; reversible before irreversible commit.

## 5. Deployment Requirements (V1)

- The deployment shape for CRM is **not** the ERP container. It must satisfy the approved
  architecture (modular-monolith seams, workspace isolation, security boundaries) for its own
  environment.
- Production deployment, production data mutation, and go-live are **Human Business Authority**
  authorizations; not granted by this document.
- Runtime configuration: secrets, IdP credentials, and environment-specific values must not be
  committed to the repository baseline; injection mechanism open.

## 6. Baseline Declaration Linkage

- IS-FINAL §Baseline (Prompt-1 §14 / Prompt-2 prerequisite) records branch, commit, modified and
  untracked files so that any Programmer change is objectively distinguishable. IS-10 consumes that
  declaration; build must start from a declared baseline, not from a dirty working tree.

## 7. Deployment / Migration Acceptance Criteria

- AC-1: dev/test environments exist with isolated, non-production data. AC-2: all migrations are
  reversible and rollback-tested in test. AC-3: no ERP transactional data is silently imported;
  any master-source decision is evidenced. AC-4: deployment shape is CRMs own, not the ERP's.
  AC-5: no production deployment/mutation occurs under this specification. AC-6: open tech decisions
  are explicitly recorded (not invented). AC-7: baseline declaration is linked.

## 8. Open / Decision Items

- Technology decisions (§2); deployment context; migration of shared masters; runtime product
  choices. None authorize rollout; all are recorded for the HBA/architecture decision batch.

## 9. Traceability

§1→Prompt-1 §11 + repo inspection (branch `master`, commit `137c6d5`, dirty tree); §2→TADR-05/17 +
IS-11 §17 + Architecture Baseline; §3→IS-11 + IS-09; §4→CD-07/CD-08 ownership + IS-07 hoops;
§5→TADR-17 + authority model; §6→Prompt-1 §14/§10.

## 10. Self-Audit

Authorized by Prompt 1 mandate ✅ · no stack/topology/rollout chosen ✅ · ERP treated as baseline not
template ✅ · real open tech decisions recorded, not invented ✅ · production gated to HBA ✅ ·
no code/schema/migration/API/UI ✅.

---

*End of IS-10 v1.0 LOCKED/CANONICAL (HBA 2026-10-13, HBA-DECISIONS-22). Prior DRAFT wording retained above as history.*
