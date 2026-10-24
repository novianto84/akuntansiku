# IS-02 Technical Decomposition (Technology-Neutral)

```text
Document: IS-02 Technical Decomposition
Type: Technical architecture decomposition — READ ONLY
Status: TECHNICAL DECOMPOSITION READY FOR ARCHITECTURE REVIEW (pending acceptance)
Scope: Technology-neutral building blocks faithful to IS-02 Service Execution Specification
Authority: AI Manager / Lead Architect. Business rules owned by Business Authority; unchanged here.
Inputs: IS-02 §§1–23; CD-11; BD-SR-011; BD-WORKMODEL-001; BD-WORKTYPE-001; TADR-01…18
  (esp. TADR-02 aggregates, TADR-04 transition boundaries, TADR-07 single-write ownership,
  TADR-08/09 audit/correction, TADR-11/12 evidence/projection, TADR-13/14 identity/authorization,
  TADR-16 QR); IS-00 escalation; IS-01 where authoritative.
Implementation: NO SQL, NO migrations, NO models/controllers/endpoints/routes, NO UI,
  NO programmer tickets.
```

> "What technical building blocks must exist" — never "how to code it". Classification per
> technical requirement: **LOCKED** (explicit canonical source) · **DERIVED** (direct technical
> consequence, derivation stated) · **OPEN** (needs a business decision) · **DEFERRED** (another
> workstream). OPEN/DEFERRED business rules are never converted into technical requirements.

---

## 1. Executive Summary

The decomposition yields 14 conceptual objects under single-write ownership, four state machines
(WO, Visit, Report-readiness, SR-interaction), 21 technical invariants, 9 consistency boundaries,
12 authorization rules, and 16 audit event families — all traced to IS-02/CD-11/BD/TADR sources.
No new entity, state, role, approval, or template axis is introduced. The rejected template names
bind zero technical behavior. Verdict: **TECHNICAL DECOMPOSITION READY FOR ARCHITECTURE REVIEW** (§30).

## 2. Canonical Technical Boundary

Single-write ownership (TADR-07): WO owns execution (assignment, Visits, JOB states, outcomes,
report consolidation); SR owns request history; Report is a derived consolidation, never an
independent store; projections are read-only derivatives (TADR-12). Each lifecycle transition is
its own consistency boundary with guardable invariants (TADR-04). No cross-aggregate mutation:
state changes propagate as events/references, never as direct writes into another owner's records.

## 3. Domain Object Inventory

| Object | Purpose | Parent/Owner | Key relationships | Source | Class |
|---|---|---|---|---|---|
| SR | Historical request record | Request domain (owner) | Optional lineage to WO | BD-SR-001/011 | CANONICAL DOMAIN OBJECT |
| WO | Execution + lifecycle owner | Service aggregate (TADR-02) | 1 Unit; 1 Primary + N Supporting; N Visits; 1 Report | CD-11 §§2,5,7 | CANONICAL DOMAIN OBJECT |
| JOB | Single scope concept with execution state | WO | Exactly 1 WO; UNCHECKED/CHECKED; Added-marker | BD-WORKTYPE-001; CD-11 §12 | CANONICAL DOMAIN OBJECT |
| Visit | Physical-arrival execution record | WO | Exactly 1 WO; check-in/out; outcome; findings/HM/evidence | CD-11 §10 | CANONICAL DOMAIN OBJECT |
| Report | Per-WO consolidation (Summary + Visit History) | WO (derived) | Exactly 1 WO; references N Visits | CD-11 §18 | CANONICAL DOMAIN OBJECT |
| Checklist execution | Scope-state record | WO (via Visit events) | JOB state transitions | CD-11 §§8,12,13 | CANONICAL DOMAIN OBJECT |
| Test-Run execution | Test-run record (+N/A path) | WO (via Visit) | Visit; reviewer validation | CD-11 §13 | CANONICAL DOMAIN OBJECT |
| HM capture | Meter-reading record | Visit | Visit + audit trail | CD-11 §14 | CANONICAL DOMAIN OBJECT |
| Evidence | Artifact + classification + approval/publication state | Visit (collection point) | photo_type / approval_state / policy_version | CD-11 §17; TADR-11 | CANONICAL DOMAIN OBJECT |
| Finding | BEFORE/DURING/AFTER observation | Visit | Flows to Report; never auto-JOB | CD-11 §13 | CANONICAL DOMAIN OBJECT |
| Outcome | Per-Visit verdict + reason | Visit (+JOB scope) | COMPLETED / NOT_PERFORMED / ON HOLD | CD-11 §11 | CANONICAL DOMAIN OBJECT |
| Correction | Numbered correction cycle + lineage | WO | WAITING-APPROVAL loop; REOPEN lineage | CD-11 §§2,28; TADR-09 | CANONICAL DOMAIN OBJECT |
| Customer acknowledgement | Optional ack record + absence reason | Visit/WO | Never a closure prerequisite | CD-11 §19 | CANONICAL DOMAIN OBJECT |
| Assignment | Responsibility event record | WO | 1 Primary + N Supporting; reason + audit | CD-11 §§7–8 | TECHNICAL SUPPORT RECORD |
| Audit/Event | Append-only trail entries | Platform (TADR-08) | ref to every boundary crossing | CD-11 §28; TADR-08 | TECHNICAL SUPPORT RECORD |
| Checklist/Test-Run catalogues; N/A taxonomy; extra evidence categories; publication mechanism | — | — | — | IS-02 §20 | FUTURE / DEFERRED |

Checklist rows are state records of JOBs, not a second JOB entity [DERIVED from CD-11 §§8,12:
UNCHECKED/CHECKED exhaust scope truth without per-action entities].

## 4. Cross-Domain Relationship Map

SR —optional lineage (`source_sr_id`)→ WO —owns→ JOB (execution state via Visit events);
WO —collects→ Visit (check-in/outcome/findings/HM/evidence/checklist-states) —consolidated-by→
Report (Summary + Visit History). Checklist/test-run/HM/evidence/findings/outcome attach at Visit
granularity and roll up through Report without duplication. Correction lineage overlays the WO
(numbered cycles; REOPEN same identity; RE-CREATE new identity with `CREATED_FROM`). Acknowledgement
attaches to Visit/WO as evidence-grade record. Audit observes every boundary crossing. No ERD/schema.

## 5. WO Technical Decomposition

One WO concept with optional lineage (no "WO-from-SR" entity) [LOCKED BD-SR-011]. Technical needs:
identity; lifecycle state holder (DRAFT/OPEN/IN_PROGRESS/WAITING APPROVAL/CLOSED + CANCELLED);
Unit binding (exactly 1 before CLOSED); assignment event log; 1..N JOB collection (minimum enforced
at Submit/OPEN, DRAFT exempt); `source_sr_id` nullable reference; workspace ownership (CD-07/08).
[LOCKED CD-11 §§2,4,5,7; BD-WORKMODEL-001 §3; BD-SR-011]

## 6. SR→WO Technical Decomposition

- **Consistency constraints [BD-SR-001/011, reconciled to final Human decision]:** SR remains independent and is `OPEN` after WO creation; only `CLOSED` is terminal. WO independently created; `source_sr_id` optional (NULL = direct); no transformation/copy semantics.
- **Transaction boundary [BD-SR-011 atomicity, reconciled]:** official WO formation + source reference/lineage + required audit are one business-atomic unit. The SR has no state transition in this unit. A saved DRAFT is not an official Related WO and remains outside official-WO formation.
- **DRAFT routing [final Human decision; CD-11 §DRAFT]:** where existing visibility permissions allow, an active source-associated DRAFT may be shown separately. A Create WO request by an authorized non-creator routes to the existing DRAFT; show details only if existing visibility permissions allow, otherwise follow existing WO access handling without exposing draft details. Only its creator may continue it. Do not create another active DRAFT. The official Related WO appears when WO reaches `OPEN`.
- **Official-WO uniqueness/integrity [BD-SR-011 V1 scope, preserved]:** at most one official WO per SR; preserve the existing source-reference duplicate guard and atomic uniqueness enforcement. A duplicate official-WO attempt resolves to the existing WO (read + redirect, never a second official WO). DRAFT routing does not replace or weaken that guard.
- **Audit [BD-SR-011 §12; TADR-08]:** actor, server timestamp, SR id, WO id, ordinary WO-creation action, and lineage.

## 7. JOB / Scope Technical Decomposition

JOB needs: identity; exactly-one-WO parent link; execution state (UNCHECKED/CHECKED); Added-During-
Execution marker (+Added by/at) present only for actually-performed work [LOCKED CD-11 §12; App. A].
Planned vs actual vs added vs skipped vs incomplete are *projections over checklist state + Visit
outcomes*, not subtypes [DERIVED from CD-11 §§11–12: the two-state checklist plus three outcomes
exhaust the combinations]. Execution records (Visit events) reference JOBs; JOBs never reference
execution internals. No `issued_jobs`/`additional_jobs` objects exist anywhere in this decomposition.

## 8. Visit Technical Decomposition

Distinct execution-level object under WO [LOCKED CD-11 §10]: identity; WO parent (exactly 1);
system-determined type (INITIAL/ON PROCESS); sequence/order within WO; check-in/out timestamps
(server); actor + attendance set; location/GPS (nullable, non-blocking); outcome + reason;
contained findings/HM/evidence/checklist-states. Continuation/interim/final are narrative/report
classifications, never Visit states [LOCKED CD-11 §20; BD-WORKMODEL-001 §4]. Not a WO, Report, or JOB.

## 9. Report Technical Decomposition

One-per-WO derived consolidation [LOCKED CD-11 §18]: identity; WO parent (exactly 1); aggregation
references to N Visits (never copies); readiness flag (NON-FINAL → FINAL iff WO CLOSED); submission
and approval references; customer-safe vs internal partitions (see §19); correction lineage (refresh
from current Visit data; no per-correction versions Phase 1). No Report-per-Visit object exists.

## 10. Work Model × Service Type

Both axes are **classifying attributes of WO execution**, not containers or lifecycles [LOCKED
BD-WORKMODEL-001 §§1–2; CD-11 §16]. Work Model (SERVICE / INSPEKSI / EMERGENCY TROUBLESHOOT) selects
the execution pattern (planned-scope execution vs condition recording with minor-action allowance vs
urgent-response sequence with minimum gate). Service Type (six canonical types) classifies service
nature (incl. Inspection/Troubleshoot minor-repair note; Emergency-as-type). Technical behavior they
control: which entry path is legal (emergency direct-IN_PROGRESS), which gates apply (minimum
critical gate for emergency), and which completion semantics hold (diagnosis-alone ≠ completion).
No third axis exists; rejected template names have zero representation [LOCKED BD-WORKMODEL-001 §8].
Behaviors beyond this (thresholds, detailed definitions) are OPEN per CD-11 §16 — marked, not modeled.

## 11. Checklist / Test-Run

Parent: WO scope frame; execution records attach at Visit granularity and reference JOBs (§7).
Item record needs: result/state (done / N/A + reason); reviewer-validation reference; evidence
linkage where applicable [LOCKED CD-11 §13]. Structure (mandatory + N/A path + validation) is
modelled; item catalogue and N/A taxonomy stay abstract placeholders owned by F-1/OQ-04
[DEFERRED]. No N/A-category business rules are modelled.

## 12. Hour Meter

Per-Visit capture record: value/context + audit reference [LOCKED CD-11 §14]. Enforced rules:
min-one per relevant Visit; once-per-Visit (not a mandated pair); N/A + open reason + reviewer
validation; excluded from emergency critical gate. PM/inspection extras are abstract extension
points, unfilled [OPEN F-1]. No additional HM policy modelled.

## 13. Evidence / Photo

Three technically separated state dimensions on one artifact record [LOCKED CD-11 §17]:
(1) **type** (`photo_type`, contextual classification only); (2) **approval_state** (reviewer
workflow); (3) **publication/visibility state** (policy + curation outcome). Capture is
event-driven with opt-out + mandatory reason; requirements configurable. Serving mechanism and
storage technology are explicitly unmodelled [DEFERRED IS-05/IS-06]; final taxonomy beyond the
locked floor is unmodelled [OPEN OQ-05].

## 14. Findings

Observation records (BEFORE/DURING/AFTER + Condition/Action always; Diagnosis/Recommendation
conditionally mandatory) attached to Visits, projected into Reports and customer-safe output
through the §19 gate [LOCKED CD-11 §13]. No finding lifecycle, no auto-derivation into work
[LOCKED BD-WORKTYPE-001 §4 R5]. Outstanding overlay stays a monitoring concept with surfacing
rules unmodelled [OPEN OQ-06].

## 15. Outcome

Per-Visit verdict record: value (COMPLETED / NOT_PERFORMED / ON HOLD) + managed reason
(`Lainnya`→Keterangan) + affected JOB scope + Visit link [LOCKED CD-11 §11]. Continuation is
represented by a subsequent Visit (time-out) or ON HOLD (blocked-external) — no second workflow
object [LOCKED CD-11 §11; BD-WORKMODEL-001 §4]. Emergency uses the same outcome set
[LOCKED BD-WORKMODEL-001 §5]. Finalization implication: outcome enables submission, never closure
[DERIVED from BD-WORKTYPE-001 §4 R7]. No reason categories modelled beyond canonical lists.

## 16. Correction / Reopen

Numbered correction-cycle records with before/after lineage on the WO [LOCKED CD-11 §28; TADR-09]:
WAITING-APPROVAL loop events (request-correction / direct-edit-with-reason / direct-close-with-reason);
CLOSED-only REOPEN events (same identity); RE-CREATE events with `CREATED_FROM` (new identity);
CANCELLED as absorbing terminal. Unlimited count is a no-maximum constraint, not an object
[LOCKED CD-11 §28]. No second report system; no uncontrolled editing (only the single audited
sideroute exists).

## 17. Approval / Closure

Submission event (explicit, technician) → review coverage record → approval decision event →
automatic CLOSED consequence [LOCKED CD-11 §§2,19; TADR-04: `WAITING APPROVAL → CLOSED` only via
authorized approval]. Rejection routes to the correction loop (§16). Actor authorization per §23;
technician self-approval barred as invariant (§21-15). No additional layers modelled.

## 18. Customer Acknowledgement

Optional record: present flag + absence/refusal reason + alternative handover/presence evidence
reference [LOCKED CD-11 §19]. Never wired to closure gating [LOCKED]. Alternative-evidence *types*
are an unfilled placeholder [OPEN OQ-16]. No portal design (IS-06).

## 19. Customer-Safe Projection

Two information planes with a gate between them [LOCKED CD-11 §§20–22; TADR-12]: internal canonical
plane (everything) vs projection plane (allowlisted, reviewer-curated, no-price, scoped). The gate
conjunction (CLOSED + FINAL + Verified PIC + scope + policy + eligibility) is modelled as a
read-guard, not a data copy [DERIVED from TADR-12 derived-only projections]. UNIT-scoped QR and
company-scoped verified-PIC portal are scope rules on the projection plane [LOCKED]. Serving
mechanism unmodelled [DEFERRED IS-06]. The architecture must make price/internal leakage
structurally impossible (separate planes), not merely discouraged.

## 20. State Machine Decomposition

| Object | State | Entry condition | Allowed transitions | Guard | Actor |
|---|---|---|---|---|---|
| WO | DRAFT | Creator persists | →OPEN; discard | Creator-owned | Creator |
| WO | OPEN | Submit (≥1 JOB) | →IN_PROGRESS; →CANCELLED | Official record | Creator (CREATE_WO) |
| WO | IN_PROGRESS | Responsible person assigned | →WAITING APPROVAL; →CANCELLED | Assignment present | ASSIGN_WO holder |
| WO | WAITING APPROVAL | Explicit technician submit | →CLOSED; →CORRECTION_REQUIRED(loop); direct EDIT/CLOSE sideroutes | Mandatory review coverage | Reviewer (Mgr/Admin) |
| WO | CLOSED | Approval event | →IN_PROGRESS (REOPEN only) | Approved Report | System on approval |
| WO | CANCELLED | Request→attention→execution | — (absorbing) | OPEN/IN_PROGRESS origin; full trace | Sales/Tech request; Admin/Mgr executes |
| Visit | OPEN | Creation + check-in | →COMPLETED | Assigned technician; server timestamp | Any assigned technician |
| Visit | COMPLETED | Check-out + outcome recorded | Correction events only | Outcome rules (§15) | Assigned technician |
| Report | NON-FINAL | WO exists | →FINAL | — | System derivation |
| Report | FINAL | WO CLOSED | REOPEN re-derivation | CLOSED event | System derivation |
| SR (interaction) | OPEN | SR created; remains OPEN after WO creation | →CLOSED | CLOSE_SR authority + reason (BD-SR-005/002) | Admin or Manager |

No other states exist [LOCKED CD-11 §§2,9–11,28,30; TADR-04]. CORRECTION_REQUIRED is a loop marker
within WAITING APPROVAL handling, not a WO state [DERIVED from TADR-04 sideroute direction].

## 21. Technical Invariants

All 21 required invariants remain traced in §28 and unchanged outside this reconciliation. SR-specific invariants are: one SR → at most one official WO in V1; only a `CLOSED` SR is immutable; `source_sr_id = NULL` means a direct WO; no official WO without formation guards; WO formation + source reference/lineage + audit are atomic while SR remains `OPEN`; a DRAFT is not an official Related WO; an active DRAFT routes the authorized Create WO request to the existing draft, and only its creator may continue it; no auto-JOB. Other invariants remain: 1-JOB-1-WO; Visit∈1WO; Report∈1WO; ≤1 Report/WO; WO→N Visits; Visit-completion⇏closure; approval-before-CLOSED; no self-close; ack⇏closure; priceless projection; no technician-chosen visibility; unit-scoped QR; identical post-creation lifecycle; no template dimension.

## 22. Transaction / Consistency Boundaries

| Operation | Consistency requirement | Why | Business source |
|---|---|---|---|
| SR-referenced WO formation | Atomic unit (official WO + source reference/lineage + audit); SR remains OPEN | Forbids partial official formation/lineage; no SR status change | BD-SR-011 §§9–10; TADR-04 |
| Duplicate protection | Atomic official source-reference uniqueness; active DRAFT routes to existing draft | V1 max-one official WO; no second active DRAFT (BD-SR-011 + final Human decision) | BD-SR-011 §§9–10 |
| JOB establishment | Part of formation guard (≥1 at OPEN) | WO validity (BD-WORKMODEL-001 §3) | BD-WORKMODEL-001 C-01 |
| Approval→closure | Automatic consequence, single event | APPROVE⇒CLOSED (CD-11 §2) | CD-11 §2; TADR-04 |
| Correction submission | Event with reason + lineage | Controlling history (CD-11 §28) | CD-11 §28; TADR-09 |
| Reopen | CLOSED-only, identity-preserving | Lineage integrity | CD-11 §28 |
| Cancellation | Request→attention→execution chain | Governed termination | CD-11 §9 |
| Customer acknowledgement | Independent record, decoupled from closure | Optional principle | CD-11 §19 |
| Evidence approval/visibility | Reviewer-gated state changes | Curation control | CD-11 §§17,21 |

No engine/technique prescribed. (Material/inventory non-atomic pairing noted as out of IS-02 scope;
owned by TADR-04/10.)

## 23. Authorization Decomposition

| Action | Actor | Object(state) | Guard | Result |
|---|---|---|---|---|
| CREATE_WO | Existing canonical CREATE_WO holders (Sales default; Manager default in V1; Technician when granted; Admin; other roles only where configured under CD-11 §4) | —/SR(OPEN) | Existing authority held; active DRAFT routes to existing draft; official-WO duplicate guard unchanged | WO DRAFT→OPEN (≥1 JOB); SR stays OPEN |
| JOB establishment | WO creator (CREATE_WO holder) | WO(pre-official) | Agreed work basis; no auto-derivation | JOBs under WO |
| Assignment | ASSIGN_WO holder (Mgr/Coord default) | WO(not CLOSED/CANCELLED) | Reason + audit | Responsibility set |
| Visit execution | Assigned technician(s) | WO(IN_PROGRESS); Visit(OPEN) | Check-in/out + outcome rules | Execution records |
| Report submission | Technician | WO(IN_PROGRESS) | Explicit declaration | WAITING APPROVAL |
| Approval | Manager/Admin (≠ technician, ≠ own WO) | WO(WAITING APPROVAL) | Mandatory review coverage | CLOSED + FINAL (or correction) |
| Correction | Authorized reviewer | WO(WAITING APPROVAL) | Reason (all sideroutes) | Loop continuation |
| Reopen | Authorized reviewer | WO(CLOSED) | Post-CLOSED governance | IN_PROGRESS, same identity |
| Cancellation | Sales/Tech request; Admin/Mgr executes | WO(OPEN/IN_PROGRESS) | Attention + full trace | CANCELLED |
| Evidence review | Manager/Admin reviewer | Evidence/Visit | Coverage rules | Approval/publication states |
| Customer acknowledgement | Customer-side presence | Visit/WO | Reason if absent | Ack record (non-gating) |

Canonical roles/permissions only; nothing invented [LOCKED CD-11 §§2,4,7,9,19; BD-SR-005; BD-SRWO-001].

## 24. Audit / Event Decomposition

| Event | Object | Actor | Minimum audit information | Immutable? |
|---|---|---|---|---|
| CREATE_WO (optional SR reference) | WO + SR reference | Existing CREATE_WO holder | Actor, server ts, SR id, WO id, source lineage; no SR status transition | Yes |
| Duplicate attempt | SR | Requestor | Actor, ts, SR id, existing WO ref | Yes |
| JOB establishment | JOB/WO | Creator | Actor, ts, JOB identity, basis | Yes |
| Assignment (+Take-Over/Self-Add) | WO | ASSIGN_WO holder | Actor, ts, before/after, reason | Yes |
| Visit check-in/out/COMPLETED | Visit | Technician | Actor, server ts, GPS, outcome+reason | Yes |
| HM capture | Visit | Technician | Value/context, ts | Yes |
| Evidence capture/opt-out | Evidence/Visit | Technician (+reviewer) | Artifact/type or reason, ts, states | Yes |
| Report submission | WO | Technician | Actor, ts | Yes |
| Approval/correction | WO | Reviewer | Decision, reason, before/after | Yes |
| Reopen/re-create | WO | Reviewer | Lineage (`CREATED_FROM`), reason | Yes |
| Closure | WO | System-on-approval | Approval ref, ts | Yes |
| Cancellation | WO | Requestor/executor | Full chain trace | Yes |
| Acknowledgement | Visit/WO | Customer-side + recorder | Presence/absence + reason | Yes |
| Evidence/publication approval changes | Evidence | Reviewer | State transitions + policy version | Yes |

Existing append-only pattern (TADR-08); no new subsystem [LOCKED CD-11 §28; BD-SR-011 §12].

## 25. Open / Deferred Technical Impact

| Business Open/Deferred Item | Technical Impact | Can Decomposition Proceed? | Owning Specification |
|---|---|---|---|
| Checklist/Test-Run catalogue + N/A taxonomy | Item/record shapes stay abstract placeholders | Yes | BA content → IS-02 update |
| Evidence taxonomy beyond floor | Category enum stays open-ended (locked floor fixed) | Yes | BA (OQ-05) |
| Subtype fields | Component extension points unfilled | Yes | BA (OQ-03) |
| Ack alternative types | Placeholder reference type | Yes | BA (OQ-16) |
| Publication/projection mechanism + freshness + no-download | Serving layer wholly unmodelled; gate modelled (§19) | Yes | IS-06 |
| Reminder automation | No scheduler/generator objects | Yes (manual baseline only) | BA (OQ-07) |
| Emergency retroactive convention | Dual timestamps captured; precedence unmodelled | Yes | BA (OQ-08) |
| Minor/substantive correction definition | Single correction object; no sub-typing | Yes | BA (OQ-09) |
| Outstanding surfacing | Monitoring overlay unmodelled | Yes | BA (OQ-06) |
| Purchasing/deployment details | Out of execution scope entirely | Yes | BA (OQ-10…14) |
| SR technical representation details | Consumed as approved; mechanics unmodelled | Yes | IS-04+ |

## 26. Cross-Domain Dependency Matrix

| From → To | Dependency | Nature |
|---|---|---|
| SR → WO | Lineage + atomic formation | Creation-time, one-way |
| WO → JOB | Ownership + formation guard | Structural |
| WO → Visit | Collection ownership | Structural |
| Visit → Report | Consolidation reference | Derivational (read) |
| Visit → Outcome/Findings/HM/Evidence/Checklist | Containment | Structural |
| WO → Report | Finalization trigger (CLOSED) | Event |
| Reviewer → WO/Evidence/Report | Approval/curation decisions | Event |
| Correction → WO/Report | Lineage overlay | Event |
| Customer → Acknowledgement | Presence record | Event |
| Projection → WO/Report/Evidence | Gated read derivation | Read-only |

No reverse (downstream→upstream) write dependency exists — enforcing single-write ownership (§2).

## 27. Architectural Risks

| Risk | Consequence | Mitigation Principle | Source |
|---|---|---|---|
| Accidental SR→JOB coupling | Ghost scope; violates one-concept JOB | JOB establishment only by actor act; reference-only SR presentation | BD-SR-003/011 |
| Duplicate WO race | Two official WOs linked to one SR | Atomic source-reference uniqueness + resolution to existing official WO; active DRAFT routes to existing draft | BD-SR-011 §§9–10 + final Human decision |
| Visit/Report lifecycle confusion | Premature finality | Separate matrices; FINAL-iff-CLOSED | CD-11 §§10,18; TADR-04 |
| Customer data leakage | Internal/price exposure | Separate planes + gate conjunction | CD-11 §§20–22 |
| Technician-controlled visibility | Policy bypass | Reviewer-only publication states | CD-11 §§17,21 |
| Correction lineage loss | Untraceable history | Numbered controlling cycles | CD-11 §28; TADR-09 |
| State transition bypass | Invalid lifecycles | Closed transition table (§20) | TADR-04 |
| Inconsistent approval/closure | APPROVED-but-open | Automatic consequence on approval | CD-11 §2 |
| Duplicate Report | Split consolidation | ≤1 Report invariant + derived object | CD-11 §18 |
| Template-axis reintroduction | Phantom execution dimension | Zero representation; Work Model × Service Type only | BD-WORKMODEL-001 §8 |

Implementation mitigations (code) are out of scope by design.

## 28. Traceability Matrix

Every section traces as cited inline: §§5–9,13–19 → CD-11 sections + BD/TADR as noted (all LOCKED
except flagged OPEN/DEFERRED placeholders); §6 → BD-SR-011 (LOCKED); §10 → BD-WORKMODEL-001 + CD-11
§16 (LOCKED); §§20–24 → CD-11 + TADR-04/08/09 + BD-SR-011/005 (LOCKED); §25 → IS-02 §20 owners.
DERIVED items state derivations (§§3,5,8,15,19,20-CORRECTION_REQUIRED). No untraced requirement exists.

## 29. Decomposition Completeness Check

1. Every IS-02 LOCKED rule represented ✅ (§§5–19). 2. Every DERIVED rule consequenced ✅ (§28).
3. Every OPEN stays OPEN ✅ (§25). 4. Every DEFERRED stays DEFERRED ✅ (§25). 5. No new business
decision ✅. 6. No new lifecycle state ✅ (§20 closed table). 7. No untraced entity ✅ (§3 classes).
8. One JOB ✅ (§7). 9. Visit≠WO ✅ (§8). 10. One Report/WO ✅ (§9). 11. O-11 atomicity ✅ (§6).
12. Identical post-creation lifecycle ✅ (§5). 13. Projection separated ✅ (§19). 14. No technician
visibility choice ✅ (§§13,19). 15. Priceless output ✅ (§19). 16. No template axis ✅ (§10).
17. No premature fixing ✅ (§25 placeholders).

## 30. Final Verdict

**TECHNICAL DECOMPOSITION READY FOR ARCHITECTURE REVIEW**
