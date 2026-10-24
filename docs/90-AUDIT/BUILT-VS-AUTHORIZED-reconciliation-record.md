# Built vs. Authorized — Reconciliation Record

**Record type:** Operational reconciliation record; not a new business decision or implementation specification  
**Status:** MATERIALIZED — 2026-10-03  
**Authority:** Human Business Authority instruction (2026-10-03): "saya izinkan pekerjaan backend yang sudah berjalan dicatat sebagai diizinkan, dan tulis catatan rekonsiliasi yang memisahkan sudah-dibangun dari sudah-diizinkan."  
**Decision IDs:** No new decision ID created. This record references existing decisions and documents the current state of built vs. authorized work.
**Amendment 2026-10-08:** HBA confirmed in session ("setuju (WP-02..07, migrasi v2..v9, UI internal)") that WP-02–WP-07 domain modules, migrations v2–v9, and the internal UI are AUTHORIZED. This amendment records that clarification; it creates no new business rule.

---

## Purpose

This record separates two distinct concepts that are often conflated:

- **BUILT:** Code, schema, migrations, tests, and infrastructure that physically exist in the repository.
- **AUTHORIZED:** Business decisions, technical approvals, and implementation scopes that have been formally approved by Human Business Authority.

**Key principle:** Built ≠ Authorized. The existence of code does not imply authorization for that code. Conversely, authorization for a business decision does not imply implementation has occurred.

---

## Section 1: BUILT — What Physically Exists

### 1.1 Backend Code (Python)

| Module | Location | Description |
|---|---|---|
| `app/config.py` | `crm/app/config.py` | Environment-driven config loader (CRM_DB, CRM_HOST, CRM_PORT) |
| `app/db.py` | `crm/app/db.py` | SQLite connection factory + workspace-scope contract seam |
| `app/health.py` | `crm/app/health.py` | Liveness/readiness endpoints |
| `app/server.py` | `crm/app/server.py` | HTTP server (stdlib http.server), ~59KB |
| `app/interfaces.py` | `crm/app/interfaces.py` | Contract stubs (identity, audit, evidence, service) |
| `app/migrations/` | `crm/app/migrations/` | Reversible migration runner + versioned migrations |
| `app/access/` | `crm/app/access/` | Authentication, authorization, identity, session |
| `app/company/` | `crm/app/company/` | Company, Contact, PIC Link |
| `app/unit/` | `crm/app/unit/` | Unit, Location, Component, Replacement |
| `app/sr/` | `crm/app/sr/` | Service Request |
| `app/wo/` | `crm/app/wo/` | Work Order |
| `app/exec/` | `crm/app/exec/` | Visit, History, Report, Approval |
| `app/material/` | `crm/app/material/` | Material seam, usage |
| `app/reporting/` | `crm/app/reporting/` | History, outstanding, reminder |
| `app/customer/` | `crm/app/customer/` | Customer-facing logic (WP-08) |

### 1.2 Migrations

| Version | File | Description |
|---|---|---|
| v1 | `migrate.py` (built-in) | `create_app_metadata` table |
| v2–v9 | `migrate.py` (built-in) | Domain tables (SR, WO, Unit, Company, etc.) |
| v10 | `v10_customer_snapshots.py` | Customer snapshots table (WP-08) |

### 1.3 Tests

- 40+ test files in `crm/tests/`
- Coverage: unit, integration, server, migrations, characterization
- Test frameworks: stdlib `unittest`

### 1.4 WP Delivery Packages

| WP | Date | Status | Key Deliverables |
|---|---|---|---|
| WP-01 | — | PASS | Foundation (config, db, migrations, health, server) |
| WP-02–WP-07 | — | PASS | Domain modules (SR, WO, Unit, Company, Material, Exec) |
| WP-08 | 2026-10-01 | PASS | Customer snapshot, auth context, serving logic, migration v10 |

### 1.5 UI

- `crm/ui/` exists with README
- UI implementation status: separate from backend; not detailed here

---

## Section 2: AUTHORIZED — What Has Been Formally Approved

### 2.1 Business Decisions (CD)

| ID | Status | Scope |
|---|---|---|
| CD-01 | FINAL / LOCKED | Business scope and boundary authority |
| CD-02 | DEFERRED / UNVERIFIED | No current canonical document |
| CD-03 | LOCKED | Business master |
| CD-04 | LOCKED | Operational acquisition price |
| CD-05 | LOCKED | Sales transaction quotation |
| CD-06 | LOCKED | Vendor offer price |
| CD-07 | LOCKED | Multi-workspace |
| CD-08 | LOCKED | Data ownership |
| CD-09 | LOCKED | Purchasing transaction boundary |
| CD-10 | LOCKED | Inventory operational boundary |
| CD-11 | SIGNED-OFF / LOCKED / CLOSED | Service work order operational boundary |

### 2.2 Business Decisions (BD)

| ID | Status | Scope |
|---|---|---|
| BD-WORKTYPE-001 Rev.A | APPROVED / CANONICAL | JOB / SCOPE canonicalization |
| BD-WORKMODEL-001 | APPROVED / CANONICAL | Work Model definitions (SERVICE / INSPEKSI / EMERGENCY TROUBLESHOOT) |
| BD-SRWO-001 | LOCKED — V1 | SR→WO V1 scope |
| BD-SR-001 | LOCKED — V1 | SR Lifecycle V1 (OPEN → CLOSED) |
| BD-SR-002 | LOCKED — V1 | SR Closure Reason V1 |
| BD-SR-003 | LOCKED — V1 | SR Content Boundary V1 |
| BD-SR-004 | LOCKED — V1 | SR Retention/Visibility V1 |
| BD-SR-005 | LOCKED — V1 | SR Minimal Permission Matrix V1 |
| BD-SR-010 | LOCKED — V1 | SR Minimal Form V1 |
| BD-SR-011 | LOCKED — V1 | Create WO from SR V1 |
| BD-G01-G02 | LOCKED — V1 | Identity Boundary V1 |

### 2.3 Technical Architecture

| Item | Status | Scope |
|---|---|---|
| Technical Architecture Approval | APPROVED / CANONICAL | TADR-01 … TADR-18 + Architecture Baseline |
| Architecture Approval Package | APPROVED / CANONICAL | Architecture direction (§1–§12) |
| UI Baselines (SR V1, WO V1) | HUMAN-APPROVED | UI behaviour only |
| Multilingual-ready UI/architecture | HUMAN-APPROVED DIRECTION | V1 default Bahasa Indonesia |

### 2.4 Governance Controls

| Item | Status |
|---|---|
| HD-4 (delegated audit control authority) | CANONICAL (recorded) |
| RC-1 (exactly-one-definition) | ADOPTED |
| RC-3 (schema completeness) | ADOPTED |
| G1-D phase verdict | ACCEPTED with limitations |
| mitrasp-falsifier standing scope | APPROVED with strict scope |

### 2.5 Human Decisions (HD)

| ID | Status | Scope |
|---|---|---|
| HD-4 | CANONICAL | Delegated audit control authority |
| D-01A | FINAL | Customer publication model = RETAIN |
| D-01B | — | Semantic freshness |
| D-02 | — | Resolves SD-8 |
| D-03 | — | Verbatim passing policy |
| D-04 | — | RC-1 / RC-3 adoption |
| D-05 | — | G1-D acceptance |
| D-6 | — | mitrasp-falsifier scope |
| D-7 | — | SOUL.md revision |

---

## Section 3: GAP ANALYSIS — Built vs. Authorized

### 3.1 Built AND Authorized (Aligned)

These items have both physical implementation AND formal authorization:

| Item | Built Evidence | Authorization Evidence |
|---|---|---|
| WP-01 Foundation | `crm/app/config.py`, `db.py`, `health.py`, `server.py` | Technical Architecture Approval (TADR-01…TADR-18) |
| SR V1 Lifecycle | `crm/app/sr/` | BD-SR-001 (LOCKED — V1) |
| SR Closure Reason | `crm/app/sr/` | BD-SR-002 (LOCKED — V1) |
| SR Permission Matrix | `crm/app/access/` | BD-SR-005 (LOCKED — V1) |
| SR Minimal Form | `crm/app/sr/` | BD-SR-010 (LOCKED — V1) |
| Create WO from SR | `crm/app/wo/` | BD-SR-011 (LOCKED — V1) |
| SR→WO V1 | `crm/app/sr/`, `wo/` | BD-SRWO-001 (LOCKED — V1) |
| Identity Boundary V1 | `crm/app/access/` | BD-G01-G02 (LOCKED — V1) |
| Customer publication model | `crm/app/customer/` | D-01A = RETAIN (FINAL) |
| HD-4 governance controls | `docs/10-DECISIONS/HD-4-*.md` | D-1 (2026-09-26) |
| WP-02–WP-07 domain modules | `crm/app/` modules | HBA clarification 2026-10-08 — AUTHORIZED (see header amendment) |
| Migrations v2–v9 | `migrate.py` | HBA clarification 2026-10-08 — AUTHORIZED as part of domain implementation |
| Internal UI implementation | `crm/ui/` | HBA clarification 2026-10-08 — AUTHORIZED (internal UI) |

### 3.2 Built but Authorization Status Needs Clarification — RESOLVED 2026-10-08 for WP-02–WP-07 / migrations v2–v9 / internal UI

The WP-02–WP-07, migration v2–v9, and internal UI items below were clarified by HBA on 2026-10-08 ("setuju (WP-02..07, migrasi v2..v9, UI internal)") and are now recorded as AUTHORIZED in §3.1. Remaining item(s) below still need an explicit source:

| Item | Built Evidence | Authorization Status |
|---|---|---|
| WP-08 Customer snapshots | `crm/app/customer/`, `v10_customer_snapshots.py` | D-01A = RETAIN + OQ-02 canonical; WP-08 MANIFEST claims PASS |

### 3.3 Authorized but NOT Built (or Partially Built)

These items have formal authorization but implementation is incomplete or not started:

| Item | Authorization | Implementation Status |
|---|---|---|
| Reminder/automation policy | UNRESOLVED / PENDING | `app/reporting/reminder.py` exists; policy not locked |
| Emergency retroactive timestamp | UNRESOLVED / PENDING | Not implemented |
| Deployment operational context | UNRESOLVED / PENDING | Not implemented |
| F-1 (architecture) | DEFERRED | Not implemented |
| C-1/C-2 (documentation cleanup) | DOCUMENTATION CLEANUP | Not implemented |

### 3.4 Built but NOT Explicitly Authorized (Potential Gap)

These items exist in code but lack explicit authorization in canonical documents:

| Item | Built Evidence | Risk |
|---|---|---|
| `app/reporting/reminder.py` | Code exists | Reminder policy is UNRESOLVED; code may implement unapproved behavior |
| `app/reporting/outstanding.py` | Code exists | No explicit BD/authorization found |
| `app/material/` | Code exists | CD-10 (inventory boundary) is LOCKED but implementation authorization not explicit |
| `app/exec/` | Code exists | CD-11 (WO boundary) is LOCKED but implementation authorization not explicit |

---

## Section 4: Reconciliation Actions

### 4.1 Immediate Actions (No New Authorization Needed)

1. **This record** documents the current state; no new decisions created.
2. **WP-01 through WP-08** are recorded as built and aligned with existing authorizations.
3. **SR V1 decisions (BD-SR-001…011, BD-SRWO-001)** are recorded as built and aligned.

### 4.2 Actions Requiring Human Clarification — RESOLVED 2026-10-08 for items 1–3

Items 1–3 below were clarified by HBA on 2026-10-08 ("setuju (WP-02..07, migrasi v2..v9, UI internal)") and are recorded as AUTHORIZED. Item 4 remains open:

1. ~~**WP-02–WP-07 domain modules**~~ — RESOLVED: AUTHORIZED per HBA clarification 2026-10-08.

2. ~~**Migration v2–v9**~~ — RESOLVED: AUTHORIZED as part of the domain module implementation per HBA clarification 2026-10-08.

3. ~~**UI implementation (internal)**~~ — RESOLVED: AUTHORIZED for the internal UI per HBA clarification 2026-10-08. (Customer/PIC portal remains DRAFT-gated and is NOT covered.)

4. **Reminder/outstanding/material/exec modules:** Confirm whether these modules are authorized under existing BD decisions, or if they represent unauthorized scope expansion.

### 4.3 Items Requiring New Human Decisions

These items cannot be resolved by reconciliation and require new HBA decisions:

1. **Reminder/automation policy** — UNRESOLVED
2. **Emergency retroactive timestamp convention** — UNRESOLVED
3. **Deployment operational context** — UNRESOLVED
4. **F-1 (architecture)** — DEFERRED
5. **C-1/C-2 (documentation cleanup)** — DOCUMENTATION CLEANUP

---

## Section 5: Traceability

| Built Item | Authorization Source | Gap? |
|---|---|---|
| WP-01 Foundation | Technical Architecture Approval | No |
| SR V1 modules | BD-SR-001…011, BD-SRWO-001 | No |
| Identity Boundary V1 | BD-G01-G02 | No |
| Customer publication | D-01A = RETAIN | No |
| WP-02–WP-07 | Technical Architecture Approval (implied) | Clarification needed |
| WP-08 | D-01A + OQ-02 | No |
| Migrations v2–v9 | Implied by domain authorization | Clarification needed |
| UI | UI baselines (implementation auth?) | Clarification needed |
| Reminder policy | UNRESOLVED | Yes — new decision needed |
| Emergency timestamp | UNRESOLVED | Yes — new decision needed |
| Deployment context | UNRESOLVED | Yes — new decision needed |

---

## Section 6: Conclusion

The majority of built backend code aligns with existing authorizations. The primary gaps are:

1. **Documentation gaps:** Some built modules lack explicit per-module authorization documents (relying on implied authorization from Technical Architecture Approval).
2. **Unresolved business decisions:** Reminder policy, emergency timestamp, and deployment context remain UNRESOLVED and require new HBA decisions.
3. **Potential unauthorized scope:** Some modules (reminder, outstanding, material, exec) may implement behavior beyond what is explicitly authorized in canonical BD documents.

**Recommendation:** HBA should review Section 4.2 and 4.3 to clarify authorization status for the identified gaps. No code changes are required for this reconciliation record.

---

**End of record.**
