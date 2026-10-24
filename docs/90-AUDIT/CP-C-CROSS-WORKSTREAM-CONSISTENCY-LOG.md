# CP-C — CROSS-WORKSTREAM CONSISTENCY LOG (IS-01 … IS-10)

```text
Artifact:       CP-C consistency log (the artifact IS-00 §13 item 2 requires)
Date:           2026-10-03
Author:         Hermes (AI Manager / Lead Architect) — read-only consistency pass
Authority:      Produced under the standing HBA direction in session 2026-10-03
Mode:           READ ONLY. No document modified. No status changed. No code changed.
Implementation: NO code / schema / migration / UI / deployment change.
Scope:          Consistency between the specification set (IS-01…IS-10), the locked
                business decisions, the approved architecture, and the implementation
                as it actually stands today.
```

> This log exists because `IS-00 §13` requires a CP-C cross-workstream consistency check
> **with a log** before implementation authorization, and no such artifact existed
> anywhere in the repository. It closes that formal gap. It creates no business rule,
> approves nothing, and authorizes nothing.

---

## 1. Method

Read-only comparison, three axes:

| Axis | Compared |
|---|---|
| A | Locked business decisions (`CD-11`, `BD-SR-*`, `BD-WORKTYPE/WORKMODEL`, `CD-01…CD-10`) vs the IS set |
| B | The IS set vs the approved architecture (TADR-01…18, Architecture Baseline) |
| C | The IS set vs the implementation actually present in `crm/app` and `crm/ui` |

Axis C carries the most value: every divergence below was found by reading running code
and the live development database, not by reading documents against each other.

---

## 2. Result summary

| Class | Count |
|---|---|
| Document-to-document contradictions found | **0** |
| Locked-rule divergences found in the implementation | **5** (C-1 … C-5), of which **C-1 and C-3 were reproduced by live execution** |
| Implementation gaps against locked event duties | **1 systemic** (C-2) |
| Documents carrying stale status vs the decision record | **3** (outside CP-C scope — reported in §5) |

No document-to-document contradiction was found: the IS set, the locked decisions and the
approved architecture agree with each other. **Every divergence found is between the
specifications and what the code actually does.** That is the single most important
finding of this pass, and it is the reason the earlier `IS-08 §10` (evidence) and
`IS-02 §4` (clock) gaps were invisible from the document side.

### Priority ordering (my assessment, not a decision)

**C-3 is the one finding that carries a data-boundary risk** rather than a process or UX
risk, and it is a breach of the isolation invariant that the whole multi-tenant model
rests on. It should be corrected **before** the trace store (C-2) and the evidence
mechanism (C-4), because those two add more rows to tables that the list paths do not
filter. C-1 is a smaller, well-bounded correction. C-5 is cosmetic but cheap to fix
alongside C-2.

### Reproduction artifacts

Both live-execution probes ran against a **copy** of the development database; the real
`crm/data/crm.db` was not touched. Scripts kept at:
`/home/anto/.hermes/cache/scratch/cpc_c1_proof.py`, `.../cpc_c3_proof.py`.

---

## 3. Findings

### C-1 — Mandatory check-out is not enforced (locked rule, not enforced) — **REPRODUCED**

| Item | Detail |
|---|---|
| Rule | `IS-02 §4` / `CD-11 §10`: check-in/out per Visit are both **mandatory**; a Visit cannot COMPLETE without check-out |
| Reality | `app/exec/visit.py::complete` performs no check-out precondition |
| Evidence A | Live dev DB (`crm/data/crm.db`): **3 COMPLETED Visits with both `check_in_at` and `check_out_at` NULL** — visit ids 4 (WO 3), 5 (WO 4), 6 (WO 7) |
| Evidence B | **Live execution on a copy of the dev DB**: created a fresh Visit (id 9) with no check-in, then called `complete()` directly — it returned `state=COMPLETED` with `check_in_at=NULL` and `check_out_at=NULL`. The mandatory check-out gate does not exist |
| Severity | Rule violation reachable by the normal API path; already present in seeded data |
| Owner | Implementation correction (domain), under authorization |

### C-2 — The event/audit duty is unenforced across the whole system

| Item | Detail |
|---|---|
| Rule | `IS-02 §19` / `IS-07 §3` list the minimum business events: DRAFT persist/submit; assignment/reassignment/Take-Over/Self-Add (+refusal reasons); Visit create/check-in/check-out/COMPLETED/correction; checklist CHECK; Add-JOB; findings/HM/evidence capture + opt-outs; outcome recording; submission; review decisions; Final Conclusion; acknowledgement; cancellation chain; reopen/re-create; link establishment; authorization denials. `IS-04 §5` assigns an explicit *audit event emission duty* to every service. `IS-07 §4` requires actor + server timestamp per event. `IS-11 §15` adds isolation-relevant events (scope resolutions, **rejections**, deactivation/archive) and states **I-10: rejections are audited** |
| Reality | Exactly **one** event family is written: `wo_approval_events` (SUBMIT / REQUEST_CORRECTION / EDIT / CLOSE / REOPEN) from `app/exec/approval.py`. Nothing else emits events — not `wo/wo.py` (create/open/start/cancel/add_job), not `wo/assignment.py`, not `exec/visit.py`, not `exec/report.py` (only `report_revisions`), not `app/sr/*`, not `app/company/*`, not `app/unit/*` |
| Second-order effect | `BD-SR-002 §3` (SR closure reason) explicitly says to follow the existing audit pattern (actor, server timestamp, reason). That pattern is not implemented anywhere SR closure happens — `app/sr/sr.py::close` writes columns on the SR row, no event. The same is true for `BD-SR-011` lineage, `IS-04 A6` assignment changes (reason is *validated* — `AssignmentError` — but never *recorded* as an event), and `A11` cancellation (columns only) |
| Severity | Systemic. The system cannot reconstruct "who did what, when" for any operation outside approval |
| Owner | Implementation work package, under authorization |

### C-3 — Cross-workspace isolation is unenforced on list paths and on workspace-less tables — **REPRODUCED**

| Item | Detail |
|---|---|
| Rule | `IS-11 §2` (workspace/tenant model; read/write scoping; guard requirements), `IS-11 §15` + invariant **I-10** (isolation-relevant events and rejections audited). Architecture: one DB with **app-level isolation** (TADR-05) — meaning the application, not the engine, must enforce every boundary |
| Reality (1) | `WorkspaceGuard` only **resolves** the caller's active workspace; the `list_*` helpers call `WorkspaceGuard(conn).active_workspace(user_id)` and then issue an **unfiltered** `SELECT * FROM <table> ORDER BY id`. Nothing compares the caller's workspace to the rows returned |
| Reality (2) | `internal_users` has **no workspace-membership table at all** — only a single `default_workspace_id`. There is no durable record of which workspaces a user may act in, so membership cannot be enforced even in principle today |
| Reality (3) | `service_requests`, `units`, `contacts`, `visits`, `report_revisions`, `reminders`, `wo_approval_events` and most other tables have **no `workspace_id` column**. Only `work_orders` and `customer_snapshots` are directly scoped. `units` reaches a workspace only through `companies.primary_workspace_id`; SRs reach it only through the optional `company_id` |
| Evidence A | **Live execution on a copy of the dev DB** (two workspaces seeded: WS1 and a new WS2 with its own Manager and company): `list_companies(user_ws1)` returned **all three** companies including the WS2 company; `get(user_ws1, company_ws2)` **succeeded** and returned "PT Tenant Dua" |
| Evidence B | **Live execution, WS3 actor**: `list_wos(user_ws3)` returned **all 7 WOs of workspace 1** (`workspaces: [1,1,1,1,1,1,1]`), while `get(user_ws3, wo_1)` was correctly blocked with `CrossScopeError` |
| Interpretation | The **object-level guard is correct where the object carries a workspace id** (`get` on a WO is blocked). The failure is that the **collection paths are not filtered**, and the tables without a workspace column have nothing to filter on. This is the exact opposite of the safe shape and it is a **data-boundary breach**, not a UX defect |
| Severity | **Highest finding in this log.** One DB + app-level isolation means this is the only barrier, and it does not hold on list paths |
| Owner | Implementation correction + explicit negative-path tests, under authorization |

### C-4 — The evidence floor is absent from the implementation

| Item | Detail |
|---|---|
| Rule | `CD-11 §17` / `IS-05 §6`: mandatory categories nameplate, hour meter, before, after; conditional during/replaced component/damage/test result; on CHECKED scope optional upload with opt-out + **mandatory reason**; publication control `photo_type + approval_state + policy_version`; technician never selects visibility; one retention rule. `IS-08 §10` requires the UI surface |
| Reality | No evidence table, no endpoint, no service. `app/interfaces.py` carries a docstring-only stub. The **only** photo columns anywhere are `emergency_wo_validation.before_photo` / `after_photo` (emergency lane, E-21) — a separate, narrower mechanism that does not cover the general floor and has no opt-out/reason path |
| Severity | Locked obligation not met; already decided by HBA (2026-10-03) to enter V1 |
| Owner | Implementation work package, after the general event store (C-2) |

### C-5 — Acknowledgement is a no-op

| Item | Detail |
|---|---|
| Rule | `IS-04 A12`: Acknowledge (optional, non-gating), owner Visit service, authority "presence recorder". `IS-07 §3` registers *acknowledgement presence/absence (+reason)* as an event family; `IS-07 §12` leaves the alternative types OPEN (OQ-16) |
| Reality | `app/exec/visit.py::acknowledge` stores nothing and emits nothing — its own comment says it is recorded "as a no-op marker returned to the caller". The contract action exists but produces no durable record |
| Severity | Medium — optional and non-gating by design, so it breaks no lifecycle rule; but a contract action that silently records nothing is a false affordance |
| Owner | Implementation correction (record + event), under authorization |

---

## 4. What was checked and found consistent

| Check | Result |
|---|---|
| WO lifecycle vocabulary (`DRAFT → OPEN → IN_PROGRESS → WAITING APPROVAL → CLOSED`, `CANCELLED` terminal, `CORRECTION_REQUIRED` as pre-CLOSED loop) vs `migrate.py` CHECK and IS-08 §2 | **CONSISTENT** |
| `UNASSIGNED` as a condition, `ON PROCESS` as Visit type only, no deprecated lifecycle terms | **CONSISTENT** (also verified in the rendered UI, 76 assertions) |
| Visit type system-determination (INITIAL first / ON_PROCESS after) vs IS-02 §4 | **CONSISTENT** (`app/exec/visit.py::_determine_visit_type`) |
| `1 WO → 1 Report → N Visits` vs schema (`reports.work_order_id UNIQUE`) | **CONSISTENT** |
| Report FINAL only as a consequence of WO closure, no FINALIZE action vs IS-02 §12, IS-08 §8 | **CONSISTENT** (`report.py::mark_final`, called from approval) |
| Separation of duties (technician never approves/closes own WO) vs IS-08 §9, CD-11 | **CONSISTENT** (`approval.py::_require_approval_authority`) |
| `≥1 JOB` at OPEN vs BD-WORKTYPE-001 / BD-WORKMODEL-001 | **CONSISTENT** (`wo.py::open_wo`) |
| Unit must exist before CLOSED (no fake Unit) | **CONSISTENT** (`approval.py` unit precondition) |
| SR lifecycle OPEN → CLOSED only, WO creation leaves SR OPEN, no auto-JOB vs BD-SR-001/003/011 | **CONSISTENT** (`app/sr/sr.py`) |
| `CLOSE_SR` = Manager/Admin in V1 vs BD-SR-005 | **CONSISTENT** |
| No price / valuation / accounting value anywhere (CD-10) | **CONSISTENT** (code + rendered UI) |
| Workspace-scope contract seam declared vs TADR-06 / IS-11 §1 | **CONSISTENT** |

---

## 5. Out-of-scope observations (status drift — reported, not resolved here)

These are document-status inconsistencies, not cross-workstream contradictions. They are
recorded because they are the same failure class that produced the earlier misreadings.

| # | Observation |
|---|---|
| D-1 | `ARCHITECTURE_LOCK.md` §"Implementation Authorization" reads **NO**, while the backend and UI exist and HBA has now issued an authorization. This file is an authority *index* designed to be read as current status |
| D-2 | `DECISION_REGISTER.md` still lists `BRIDGE_CONTRACT.md` final acceptance as **PENDING**; the contract header records **ACCEPTED WITH EXPLICIT RESIDUALS** (2026-09-26, receipt sha256 `27fe1db7…`) |
| D-3 | `DECISION_REGISTER.md` still shows reminder/automation, emergency retroactive timestamp and deployment context as UNRESOLVED/PENDING; HBA decided all three on 2026-10-01 (`HBA-DECISION-RECORD-01`) |
| D-4 | `IS-01` and `IS-02` headers still carry "acknowledgement required" / "pending BA acceptance"; `IS-09` and `IS-10` remain PROPOSED, to be raised via the IS-FINAL acceptance gate. These are acceptance acts, not defects |
| D-5 | `IS-FINAL` header still reads "READY FOR FINAL REVIEW & HBA ACCEPTANCE" although HBA approved it on 2026-10-03; the document itself has not been updated |

**Read-only rule applied:** none of D-1…D-5 was edited. Each requires HBA edit permission.

---

## 6. Consequences for the implementation gate (IS-00 §13)

| # | Gate requirement | State after this log |
|---|---|---|
| 1 | IS-01…IS-10 DONE per §7–§8 | **NOT YET** — IS-01, IS-02 acceptance pending; IS-09, IS-10 PROPOSED (D-4) |
| 2 | CP-C consistency check complete **with log** | **MET by this artifact** — the log now exists |
| 3 | Unresolved blocking decisions = NONE | **PARTIAL** — blocking items are decided by HBA but not materialized (D-2, D-3); permission-matrix content (HD-06) decided 2026-10-02, not yet recorded |
| 4 | IS-FINAL approved | **MET** (HBA, 2026-10-03) — header not yet updated (D-5) |
| 5 | Scope deterministically derivable from IS-FINAL | **PARTIAL** — derivable for the corrected scope; the CP-C findings above must be dispositioned before it is fully deterministic |

**Net effect:** one gate requirement is closed outright (item 2), and this log supplies the
evidence that makes items 3 and 5 dispositionable. Items 1 and 4 need HBA acceptance acts
and a header update.

---

## 7. Recommended dispositions (proposals only — not decisions)

| Finding | Recommended disposition | Authority needed |
|---|---|---|
| C-1 | Correct in the domain: enforce check-out before COMPLETE, with the server clock | HBA authorization (already indicated 2026-10-03) |
| C-2 | Build the general event store and fill the event families whose implementation exists; carry the rest as owned debt | HBA authorization |
| C-3 | Correct the actor-authority helpers to verify workspace membership; add explicit negative-path tests | HBA authorization |
| C-4 | Build the evidence mechanism on the event store | HBA authorization (decided in principle 2026-10-03) |
| C-5 | Make Acknowledge record a durable presence/absence marker (types remain OPEN, OQ-16) | HBA authorization |
| D-1…D-5 | Materialize/correct status in the index and control documents | HBA edit permission |

C-3 is the one finding in this log that carries a data-boundary risk rather than a
process or UX risk, and it is therefore the one I would not let sit behind the others.

---

## 8. Boundary

This log:

- modified no document, changed no status, created no business rule;
- authorized no implementation;
- reports divergences and proposes dispositions; it decides none of them;
- does not close the implementation gate — it closes one of its five requirements and
  reports the rest.

*End of CP-C consistency log.*
