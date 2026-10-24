# IS-02 — Service Execution Specification

```text
Document: IS-02 Service Execution Specification
Type: Specification (business/functional)
Status: SPECIFICATION — READY FOR TECHNICAL DECOMPOSITION — ACKNOWLEDGED & ACCEPTED by HBA (2026-10-07, per HBA-DECISIONS-08)
Scope: Complete service-execution behavior after WO exists (V1)
Authority: AI Manager / Lead Architect (specification author). Business Authority owns all business rules.
Precedence: newer LOCKED/APPROVED → earlier LOCKED/APPROVED → approved technical clarification → historical material.
Implementation: NO code, NO schema/migration, NO API routes, NO UI, NO programmer tasks.
```

> IS-02 specifies *how the system must behave* during service execution from already-approved
> business decisions. It creates no business policy. Rule classification is mandatory per rule:
> **LOCKED** (explicit canonical source) · **DERIVED** (direct logical consequence, sources stated) ·
> **OPEN** (business rule required but undecided) · **DEFERRED** (intentionally later workstream).
> Canonical axes: **Work Model** (SERVICE / INSPEKSI / EMERGENCY TROUBLESHOOT — BD-WORKMODEL-001)
> × **Service Type** (six types — CD-11 §16). There is no template axis: `FULL_SERVICE /
> INSPECTION_ONLY / EMERGENCY` were never locked as templates (BD-WORKMODEL-001 §8/C-table closes
> IS-01 OQ-01 template axis as REJECTED); IS-02 binds no guard to those names.

---

## 1. IS-02 Executive Summary

IS-02 covers WO preparation → execution start → Visit execution → JOB/scope recording →
checklist/test-run → HM → evidence → findings → outcome → report → review/approval/closure →
correction/reopen, plus acknowledgement, customer-safe output, and the emergency lane. All gate
structures are LOCKED; content-level details (checklist items, taxonomies, mechanisms) are tagged
OPEN/DEFERRED without invention. SR→WO formation (BD-SR-011) is consumed as entry context; post-creation
lifecycle is identical for direct and SR-based WOs. Verdict: **IS-02 READY FOR TECHNICAL DECOMPOSITION**
(see §23).

## 2. Canonical Execution Model

```text
WO (DRAFT→OPEN→IN_PROGRESS→WAITING APPROVAL→CLOSED; CANCELLED terminal)   [LOCKED CD-11 §2]
 └── 1 Report (NON-FINAL → FINAL iff WO CLOSED)                            [LOCKED CD-11 §18]
      └── N Visits (OPEN→COMPLETED each; INITIAL / ON PROCESS)             [LOCKED CD-11 §10]
           ├── check-in/out (mandatory, server timestamp)                  [LOCKED CD-11 §10]
           ├── JOB checklist states (UNCHECKED / CHECKED)                  [LOCKED CD-11 §12]
           ├── findings BEFORE/DURING/AFTER                                [LOCKED CD-11 §13]
           ├── HM (min-one rule)                                           [LOCKED CD-11 §14]
           ├── evidence (event-driven + opt-out)                           [LOCKED CD-11 §17]
           └── outcome COMPLETED / NOT_PERFORMED / ON HOLD                 [LOCKED CD-11 §11]
```

Execution completes → technician explicit submit → mandatory Manager/Admin review →
APPROVE ⇒ CLOSED (automatic; no CLOSE_WO) or correction loop; Report FINAL iff CLOSED.
[LOCKED CD-11 §§2,18,19]

## 3. WO Preparation & Assignment

- **DRAFT** is creator-owned pre-submission storage, not an official WO, outside the operational
  workflow; exempt from the 1-JOB minimum. [LOCKED CD-11 §2; BD-WORKMODEL-001 §3]
- **Official WO (from Submit/OPEN)** contains 1..N JOBs; 1 JOB belongs to exactly 1 WO.
  [LOCKED BD-WORKMODEL-001 §3 (C-01 supersession of BD-WORKTYPE-001 minimum wording)]
- **Assignment is an event/condition, not a lifecycle state.** No ASSIGNED state; UNASSIGNED is a
  condition. Exactly 1 Primary + 0..N Supporting per WO with equal operational rights (Primary =
  accountability). [LOCKED CD-11 §§2,7]
- **Authority:** CREATE_WO (Sales default; Manager default V1; Technician grantable; others
  configurable) and ASSIGN_WO (default Manager + Coordinator) are distinct; every assignment change
  needs reason + audit; allowed unless WO is CLOSED/CANCELLED. Includes Manager Take Over and
  per-WO Technician Self-Add (request → evidence → approval). [LOCKED CD-11 §§4,7]
- **Readiness before execution [DERIVED from CD-11 §§2,5,7]:** WO is OPEN (official, ≥1 JOB);
  Unit posture resolved to EXISTING/NEW-field-identified or NOT-YET-DETERMINED with reason +
  Manager/Coordinator approval (binding before CLOSED); a responsible person assigned before
  IN_PROGRESS (OPEN may sit unassigned, visible on Sales/Coordinator/Manager dashboards).
- WO-from-SR and direct WO share identical post-creation rules; `source_sr_id` is lineage only.
  [LOCKED BD-SR-011 §§2,8]

## 4. Execution Start / Check-in

- **Transition into execution:** OPEN → IN_PROGRESS occurs on assignment of a responsible person;
  IN_PROGRESS without one is prohibited. Technician-created emergency WO goes directly IN_PROGRESS.
  [LOCKED CD-11 §2]
- **Check-in/out per Visit are both mandatory;** a Visit cannot COMPLETE without check-out.
  Server timestamp; no free timestamp editing (corrections via controlled audited mechanism).
  Default method manual button + GPS/location; GPS best-effort NULL-able, never blocking, never
  fabricated; collection transparently disclosed. [LOCKED CD-11 §10]
- **Technician identity [DERIVED]:** Visit creator auto-marked present; may mark other assigned
  technicians present; attendance per Technician, check-in/out per Visit (CD-11 §10). No per-scope
  per-technician attribution: display `Recorded by`, never `Completed by` (CD-11 §8).
- **Emergency entry path:** §17 applies; standard minimum gate replaces no other control.

## 5. Visit Execution Model

- **Purpose [LOCKED CD-11 §10]:** one physical arrival = one Visit Record; the operational source
  of execution truth. Multiple same-day arrivals are separate records. A Visit is never a new WO
  or a new Report.
- **Types [LOCKED]:** INITIAL (first) / ON PROCESS (second and onward), system-determined;
  technician never chooses. FINAL is not a Visit Type; ON PROCESS ≠ WO IN_PROGRESS.
- **Lifecycle [LOCKED]:** OPEN → COMPLETED, independent of WO lifecycle. COMPLETED Visit closes
  neither WO nor Report and finalizes nothing; COMPLETED Visits lock normally with controlled
  correction available. Any assigned technician may create a Visit.
- **Multiple visits [LOCKED CD-11 §§10–11; BD-WORKMODEL-001 §4]:** permitted. Same unfinished work
  continuing for lack of Visit time proceeds on the next Visit of the same WO — operational
  *continuation* (narrative only, not a type/status/outcome). Blocked-pending-external-party work
  uses ON HOLD instead (§11).
- **Final visit:** no FINAL Visit Type exists. "Lastness" is an emergent property: the Visit after
  which scope is COMPLETED, submitted, approved, and WO CLOSED. [DERIVED from CD-11 §§10,18]
- **Report relation [LOCKED CD-11 §18]:** 1 WO → 1 Report → N Visits; Report consolidates without
  manual duplication; corrections refresh from current Visit data.

## 6. JOB / Scope Execution

- **Canonical model [LOCKED BD-WORKTYPE-001 §§2–4; BD-WORKMODEL-001]:** one JOB concept; SCOPE is
  the WO work list; Finding/Diagnosis/Recommendation/Outcome are never JOBs and auto-generate
  nothing; performed Recommendations become JOBs at performance time with applicable provenance.
- **Recording without a second concept [LOCKED CD-11 §12 + Appendix A]:**
  - *Planned scope:* SCOPE checklist entries UNCHECKED → CHECKED (no IN_PROGRESS state). Partial
    work lives in Visit notes/findings; scope stays UNCHECKED until truly done; scopes span Visits;
    CHECKED stays CHECKED under retest (retest logged on next Visit).
  - *Actual work:* CHECKED entries (+ evidence handling §9).
  - *Added scope:* JOB surfacing during execution exists as a JOB **only if actually performed**,
    carrying the Added During Execution marker (`Added by`, `Added at` = administrative timestamp;
    no execution timestamp Phase 1). Entry via existing work category where available else free
    description; `Sudah dikerjakan?` YA→CHECKED; the TIDAK branch records an unchecked scope entry
    only and never creates a JOB. Same evidence rules as normal scope; all Added scopes must be
    CHECKED before Visit Outcome DONE/COMPLETED. Minor-only outside the emergency response
    sequence (CD-11 §12); within one, BD-WORKMODEL-001 §1.3 applies.
  - *Skipped scope:* no SKIP concept exists (`SKIP_TEMPORARY` prohibited, CD-11 §§11,30). Work not
    done on a Visit is recorded via Outcome: NOT_PERFORMED (administratively finished for that
    Visit; optional recommendation is a note only) or ON HOLD (obligation continues same WO).
  - *Incomplete scope:* UNCHECKED + applicable ON HOLD outcome (§11).
  - *Outcome/reason:* §11; reason from managed list, `Lainnya`→Keterangan mandatory, standard
    reasons need no note (CD-11 §11; CD11-024).

## 7. Checklist & Test-Run

- **LOCKED STRUCTURE (CD-11 §13):** checklist + Test/Run mandatory for all Service Types; where
  impossible, `N/A + Reason` with reviewer validation. No per-action Activity entity.
- **OPEN CONTENT:** exact checklist items, Test/Run items, and exact N/A rules/taxonomy follow later
  decisions (F-1/OQ-04) — not invented here. IS-02 provides content-agnostic containers only.

## 8. Hour Meter

- **LOCKED (CD-11 §14; CD11-015):** minimum one HM (initial/start OR final/end); captured once per
  Visit (no mandated start+end pair; capture point follows workflow/template); relevant + available
  → mandatory; unavailable/irrelevant → `N/A` + open reason with reviewer validation (never a free
  pass, never silently zero); stored on Visit record + audit trail. **HM is not an emergency
  critical gate.**
- **OPEN:** exact N/A rules; PM initial+final extras; inspection-specific optionality (F-1; Baseline §6).

## 9. Evidence & Photos

- **LOCKED (CD-11 §17; CD11-014/016):** event/condition-driven (mandatory: nameplate, hour meter,
  before, after; conditional: during, replaced component, damage, test result) — never free choice.
  NOT globally mandatory Phase 1: on CHECKED scope the field appears but upload is optional with
  `No Evidence / Opt Out` + mandatory reason; note optional when evidence exists. Requirements
  configurable (type/field/workflow) via Dynamic Configuration.
- **Visibility [LOCKED]:** `photo_type` is contextual classification ONLY (single retention rule; no
  Before/During/After lifecycles). Publication control = `photo_type + approval_state +
  policy_version` + reviewer curation; technician never selects visibility; non-eligible evidence
  stays stored and internally visible per permission, never on the Customer Report.
- **OPEN:** additional business-critical categories beyond serials + before/after (OQ-05).

## 10. Findings

- **LOCKED (CD-11 §13):** BEFORE/DURING/AFTER mandatory for all Service Types. Condition + Action
  always required; Diagnosis required on abnormality/failure/troubleshooting; Recommendation required
  where follow-up should be suggested (never fabricated). Diagnosis alone is not automatic completion
  in emergency response (BD-WORKMODEL-001 §5).
- **Visit relation [DERIVED]:** findings attach to the Visit record (§10 collection role) and flow
  into Report consolidation (§18) without re-entry.
- **Unresolved findings [LOCKED BD-WORKTYPE-001 §4 R5 + CD-11 §11]:** never auto-generate JOBs,
  ON HOLD, tasks, or WOs. Continuation happens only via explicit ON HOLD outcome or new business WO.
- **Customer-safe presentation:** findings reach the customer only through the §16 gate
  (reviewer-curated, allowlisted).

## 11. Outcome

- **Capture [LOCKED CD-11 §11]:** per-Visit COMPLETED (all scope incl. checked Added scopes done +
  check-out) / NOT_PERFORMED (reason mandatory; administratively finished; rec = note only) /
  ON HOLD (reason mandatory; obligation continues same WO; WO stays IN_PROGRESS + "Ada pekerjaan
  ON HOLD" indicator; no HOLD workflow/states).
- **Reasons [LOCKED]:** managed list + `Lainnya`→Keterangan mandatory; defaults: NOT_PERFORMED
  ("Customer tidak mengijinkan" — "Customer tidak meminta" is superseded and must not be used;
  "Tidak ada akses"; "Kondisi lapangan"; "Waktu tidak mencukupi"; "Lainnya"); ON HOLD ("Spare part
  belum tersedia"; "Menunggu customer"; "Kondisi lapangan"; "Masalah teknis"; "Lainnya").
- **FINAL conditions [DERIVED]:** work is finally done when scope COMPLETED outcomes hold across
  Visits with all SCOPE CHECKED — but *closure* additionally requires submission → mandatory review →
  approval → WO CLOSED (§13). Outcome alone never closes a WO (BD-WORKTYPE-001 §4 R7).
- **Emergency outcomes:** same outcome set; diagnosis-alone ≠ completion (BD-WORKMODEL-001 §5).

## 12. Report Model

- **LOCKED (CD-11 §18; CD11-017/019/020):** exactly 1 Report per WO — Hybrid Summary (WO,
  Company/Customer, Unit, type/template, Work Scope Summary, Findings, Work Result,
  Parts/Materials, eligible Evidence, Final Conclusion) + Visit History (number, date,
  attendance, check-in/out, outcome, summary). No per-Visit Report. No manual duplication.
- **Interim/continuation [LOCKED CD-11 §20]:** INTERIM/CONTINUATION/FINAL are report/work-stage
  classifications (with BEFORE/DURING/AFTER), never lifecycles or Visit Types.
- **Final [LOCKED]:** NON-FINAL → FINAL only on WO CLOSED. Visit COMPLETED, Outcome DONE,
  WAITING APPROVAL, CORRECTION_REQUIRED never finalize. No FINALIZE REPORT action; no automatic
  per-correction revisions; corrections refresh from current Visit data.
- **Final Conclusion [LOCKED]:** technician drafts → approver accepts/corrects/establishes; the
  approved version at approval time is official. History keeps draft, modification, final, actor,
  timestamp. Technician can never set it unilaterally.

## 13. Review / Approval / Closure

Four distinct phases — never merged [LOCKED CD-11 §§2,19]:
1. **Execution completion:** technician explicit submit (IN_PROGRESS → WAITING APPROVAL).
2. **Report readiness:** Report NON-FINAL, assembled from current Visits.
3. **Approval:** mandatory Manager/Admin review (checklist, photos, material, test, HM, Unit,
   findings); reviewer may REQUEST CORRECTION → CORRECTION_REQUIRED, EDIT directly during WAITING
   APPROVAL (reason mandatory), or CLOSE directly (reason mandatory).
4. **Closure:** `APPROVE REPORT ⇒ WO = CLOSED` automatically. No CLOSE_WO permission/action; no
   normal APPROVED-but-still-OPEN state; technician never closes own WO.

## 14. Correction / Reopen

- **Pre-CLOSED [LOCKED CD-11 §§2,28]:** WAITING-APPROVAL loop (incl. the single audited reviewer
  direct-edit sideroute with mandatory reason). Correction history is controlling data with numbered
  cycles; count unlimited (no technical maximum).
- **Post-CLOSED [LOCKED]:** REOPEN applies to CLOSED only (back to IN_PROGRESS; same number/Report;
  assignment restored; SLA history preserved; multi-cycle allowed Phase 1). RE-CREATE mints new
  WO/number/Report/history with `CREATED_FROM` lineage (no assignment carry; Company kept; Unit may
  change). CANCELLED is terminal (no reopen; CLOSED never cancelled; cancellation only from
  OPEN/IN_PROGRESS via request + Manager attention + authorized Admin/Manager execution — CD-11 §9).
- Every correction/cancellation/reopen/re-create event captures actor, server timestamp, action,
  object, reason, before/after where relevant (CD-11 §28; TADR-08/09).

## 15. Customer Acknowledgement

- **LOCKED (CD-11 §19):** OPTIONAL, never a CLOSED prerequisite. If unavailable/refused, record
  reason and provide suitable alternative handover/presence evidence.
- **OPEN:** alternative evidence types (OQ-16; Approval Package §10). No mandatory alternative type
  is locked.

## 16. Customer-Safe Output (business rules only; mechanism is IS-06)

- **Allowlist [LOCKED CD-11 §21]:** date, technician, summary/work performed, approved photos,
  replaced component, material quantity only where agreed/appropriate, recommendation.
- **Exclusions [LOCKED]:** internal notes, correction/cancellation/administrative reasons,
  acquisition price, vendor intelligence, any other internal/commercial information. **No prices in
  any form** (locked access-model decision).
- **Scope [LOCKED]:** reviewer-curated (Manager/Admin); UNIT_SCOPE (authenticated non-PIC, this Unit
  only) vs COMPANY_SCOPE (verified PIC, all Units of that Company + histories + PIC per
  customer-safe visibility). No-download honored (mechanism deferred).
- **QR [LOCKED CD-11 §22]:** permanent, unit-scoped; same QR on Unit/Invoice/Surat Jalan resolves
  to the same Unit; CONTROLLED ACCESS (Google-only sign-up/in → CHECK ACCESS → UNIT DATA; no
  anonymous access, not even preview).

## 17. Emergency Execution

- **Work Model [LOCKED BD-WORKMODEL-001 §§1–2]:** EMERGENCY TROUBLESHOOT = initial response to
  urgent faults; initial JOB vocabulary `Troubleshoot` (Diagnosis is analysis/result, never a JOB
  name); diagnosis + necessary action/repair within the same response sequence is part of the
  response, not an exception; follow-up that becomes new business (quotation, approval, spare part,
  major work, new visit as new work) → new WO, generally SERVICE. No separate TROUBLESHOOT model.
- **Lane [LOCKED CD-11 §6; CD11-004/028/029]:** technician-created WO directly → IN_PROGRESS
  (auto-Primary; same lifecycle; no separate WO category; no auto-close); Minimum Critical
  Validation only (Unit SN mandatory; Engine/Generator SN mandatory *if applicable*; Before + After
  photos mandatory, no N/A). N/A is system-determined from Unit subtype; applicable-but-unknown SN
  must NOT be N/A. Technician never approves, including own WO. Work Summary, HM, outcome detail
  are not critical gates.
- **No separate emergency lifecycle [DERIVED]:** submission and closure follow the canonical
  lifecycle unchanged (BD-WORKMODEL-001 §5).
- **Purchasing separated [LOCKED CD-11 §24; CD-09]:** emergency service ≠ emergency purchasing
  (which still needs PO + receiving + reason; PR skippable).
- **OPEN:** retroactive timestamp convention + completion deadline (no numeric SLA locked —
  Decision Register gate; IS-00 O-04). Dual time capture (event-time + record-time) proceeds;
  precedence undecided (IS-01 H-06/OQ-08).

## 18. State & Guard Matrix

| Situation | Allowed | Guard | Actor | Result |
|---|---|---|---|---|
| WO DRAFT persist | Yes | Creator-owned session | Creator | Draft stored; not official; exempt 1-JOB |
| WO Submit (DRAFT→OPEN) | Yes | ≥1 JOB established | Creator (CREATE_WO holder) | Official WO at OPEN |
| Assignment (OPEN→IN_PROGRESS) | Yes | Responsible person designated (1 Primary + N Supporting); reason + audit on changes | ASSIGN_WO holder (default Manager + Coordinator); Manager Take Over permitted | WO IN_PROGRESS |
| Execution start | Yes | §3 readiness (OPEN, ≥1 JOB, Unit posture, responsible person) | Assigned technician(s) | Work may begin |
| Visit start (check-in) | Yes | Assigned to WO; per-Visit record created; type system-set | Any assigned technician | Visit OPEN |
| Visit completion (check-out) | Yes | Check-out done; outcome recorded (+reason where mandatory); Added scopes CHECKED for DONE | Assigned technician (Primary not required) | Visit COMPLETED (WO/Report unaffected) |
| Continuation (time ran out) | Yes | No blocking condition; same WO | Technician | Next Visit, same WO (narrative continuation) |
| ON HOLD | Yes | Blocking external condition; reason mandatory | Technician records; WO stays IN_PROGRESS + indicator | Obligation continues same WO |
| Interim report info | Yes | Classification only (no state change) | System derivation | INTERIM marking; nothing finalizes |
| Submission | Yes | Technician declares work/report done (explicit) | Technician | IN_PROGRESS → WAITING APPROVAL |
| Approval | Yes | Mandatory review coverage (CD-11 §19 scope) | Manager/Admin (never technician, never own WO) | APPROVE ⇒ CLOSED; Report FINAL |
| Correction | Yes | Reviewer decision + reason (request/direct-edit/close) | Authorized reviewer | CORRECTION_REQUIRED loop; Report stays NON-FINAL |
| Reopen | Yes, CLOSED only | Post-CLOSED governance | Authorized reviewer | CLOSED → IN_PROGRESS, same identity |
| Closure | Automatic on approval | Approval event | System on approval | WO CLOSED; Report FINAL |
| Cancellation | OPEN/IN_PROGRESS only | Request + notes → Manager attention → authorized execution; full trace | Sales/Technician request; Admin/Manager executes | Terminal CANCELLED |
| Emergency execution | Yes | Lane §17 (direct IN_PROGRESS + minimum gate) | Technician (creator auto-Primary) | Standard lifecycle thereafter |

No other states or transitions exist. Anything not listed is prohibited unless a canonical
source is cited. [LOCKED CD-11 §§2,9–11,28,30]

## 19. Audit / Event Requirements

Append-only; existing pattern (actor, server timestamp, action, object, reason,
before/after where relevant; TADR-08). Minimum business events [LOCKED CD-11 §28;
BD-SR-011 §12; TADR-08/09]:
DRAFT persist/submit; assignment/reassignment/Take-Over/Self-Add (incl. refusal reasons);
Visit create/check-in/check-out/COMPLETED/correction; checklist CHECK transitions; Add-JOB
entries; findings/HM/evidence capture + opt-outs (+reasons); outcome recording (+reasons);
submission; review decisions (approve/request-correction/direct-edit/close + reasons);
Final Conclusion draft/modification/official; acknowledgement presence/absence (+reason);
cancellation request/attention/execution; reopen/re-create lineage (`CREATED_FROM`);
SR→WO lineage (`source_sr_id`); material usage records. No new audit subsystem.

## 20. OPEN / DEFERRED Register

| ID | Topic | Status | Why Open | Blocking? | Owning Gate |
|---|---|---|---|---|---|
| IS02-O01 | Checklist/Test-Run exact contents + N/A taxonomy | OPEN | No canonical item catalogue (F-1/OQ-04) | No (structure specified) | BA |
| IS02-O02 | Evidence categories beyond serials+before/after | OPEN | Only floor locked (OQ-05) | No | BA |
| IS02-O03 | Component subtype field requirements | OPEN | Placeholders only (OQ-03) | No | BA |
| IS02-O04 | Ack alternative evidence types | OPEN | No mandatory type locked (OQ-16) | No | BA |
| IS02-O05 | Publication/projection mechanism + freshness + no-download serving | DEFERRED | Mechanism belongs to IS-06/architecture; customer publication expectation resolved (HBA D-01A = RETAIN); D-01B is semantic freshness only, no numeric SLA | No for IS-02 | Architecture / IS-06 |
| IS02-O06 | Reminder/automation policy | DEFERRED | Disabled Phase 1 locked; enablement needs policy (OQ-07) | No | BA |
| IS02-O07 | Emergency retroactive timestamp convention | OPEN | Dual capture proceeds; precedence undecided (OQ-08) | No | BA |
| IS02-O08 | Minor vs substantive correction definitions | OPEN | Both representable; neither defined (OQ-09) | No | BA |
| IS02-O09 | Outstanding surfacing rules | DEFERRED | Monitoring-only locked; surfacing business-owned (OQ-06) | No | BA |
| IS02-O10 | Offer/MOQ/currency/PPN-rate-source; purchasing thresholds/formats | DEFERRED | Out of execution scope (OQ-13/14) | No | BA |
| IS02-O11 | Deployment operational context | DEFERRED | Out of execution scope (OQ-10) | No | BA |
| IS02-O12 | SR technical representation details | DEFERRED | Approved proposal consumed; mechanics are implementation detail | No | IS-04+ |

## 21. Traceability Matrix

| IS-02 section | Source | Class |
|---|---|---|
| §§2–4 lifecycle/assignment/DRAFT | CD-11 §§2,4,5,7,8; BD-WORKMODEL-001 §3 | LOCKED |
| §5 Visit model | CD-11 §10; App. B §B.2 | LOCKED |
| §6 JOB/scope | BD-WORKTYPE-001 §§2–4; App. A; CD-11 §12; BD-WORKMODEL-001 §§1,5 | LOCKED |
| §§7–9 checklist/HM/evidence | CD-11 §§13,14,17 | LOCKED structure / OPEN content |
| §10 findings | CD-11 §13; BD-WORKTYPE-001 §4 R5; BD-WORKMODEL-001 §5 | LOCKED |
| §11 outcome | CD-11 §11; BD-WORKTYPE-001 §4 R7 | LOCKED (+DERIVED final-conditions) |
| §12 report | CD-11 §§18,20 | LOCKED |
| §13 review/closure | CD-11 §§2,19 | LOCKED |
| §14 correction/reopen | CD-11 §§2,9,28; TADR-08/09 | LOCKED |
| §15 acknowledgement | CD-11 §19 | LOCKED (+OPEN types) |
| §16 customer-safe | CD-11 §§20–22; locked access decisions | LOCKED rules / DEFERRED mechanism |
| §17 emergency | CD-11 §§6,16,24; BD-WORKMODEL-001 §§1–2,5 | LOCKED (+OPEN convention) |
| §18 guards | CD-11 §§2,9–11,28,30 (see rows) | LOCKED |
| §19 audit | CD-11 §28; BD-SR-011 §12; TADR-08/09 | LOCKED |
| Work Model × Service Type axes | BD-WORKMODEL-001; CD-11 §16 | LOCKED (no template axis) |

No template-named rule appears anywhere in this specification (verified by construction).

## 22. Self-Check

1. No SR→JOB shortcut ✅ (§6: reference-only; explicit establishment). 2. No SR transformation ✅
(BD-SR-011 consumed; §3). 3. O-11 atomicity intact ✅ (§§3,18: both-or-neither; DRAFT-insufficient;
duplicate block-and-show). 4. Direct ≡ SR-based post-creation ✅ (§3). 5. One JOB concept ✅ (§6).
6. Visit ≠ WO ✅ (§5). 7. One Report per WO ✅ (§12). 8. Multi-Visit ✅ (§5). 9. Visit COMPLETED
finalizes nothing ✅ (§5). 10. No self-close ✅ (§13). 11. Ack not prerequisite ✅ (§15).
12. Visibility not technician-controlled ✅ (§§9,16). 13. No price in customer-safe output ✅ (§16).
14. QR unit-scoped ✅ (§16). 15. Portal company-scoped via verified PIC ✅ (§16). 16. Emergency keeps
critical controls ✅ (§17: minimum gate; never approves own; no auto-close). 17. No new entity ✅
(§§6–7: no Activity/Additional/Issued entities; §20 carries placeholders only). 18. No new lifecycle
state ✅ (§18 closed list; §30-superseded terms absent). 19. No silent fill ✅ (§20 register; OPEN
content explicitly unfilled). 20. Newer canonical never overridden by older material ✅ (§21;
reconciliation items of the boundary audit acknowledged: template premise rejected, stale A-8 line
non-authoritative, OQ-01 closed administratively on 2026-09-25).

## 23. IS-02 Readiness Verdict

**IS-02 READY FOR TECHNICAL DECOMPOSITION**
