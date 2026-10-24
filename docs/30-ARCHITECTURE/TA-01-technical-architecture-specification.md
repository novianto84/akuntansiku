# TA-01 — Technical Architecture Specification

```text
Document ID: TA-01
Title: Technical Architecture Specification (Service Execution)
Version: 1.1 (controlled revision; no content revision beyond AR-TA01 cleanup)
Status: DRAFT / PROPOSED (not approved, not canonical)
Revision history: v1.0 — initial TA-01 specification. v1.1 — controlled cleanup following
  AR-TA01: TA-AR-01 resolved (§11), TA-AR-02 resolved (§12); TA-AR-03 retained as
  detailed-design observation; TA-AR-04 retained as IS-06 deferred decision.
Source baseline: AB-01 v1.0 APPROVED / CANONICAL — BUSINESS AUTHORITY APPROVAL
  (docs/30-ARCHITECTURE/AB-01-service-execution-architecture-baseline.md)
Scope: Technology-neutral technical architecture for AB-01 service execution.
Owner: AI Manager / Lead Architect. Approval state: awaiting review (no approval manufactured).
```

> AB-01 wins over technical convenience. No business rule is created or altered here. No SQL,
> migrations, table schema, API contracts, UI, framework code, ORM, or deployment content.
> OPEN/DEFERRED items are carried, never solved. Implementation is NOT authorized (gate: §29).

---

## A. Document Control

ID TA-01 · v1.1 · PROPOSED · baseline AB-01 v1.0 (APPROVED/CANONICAL) · scope §1 above ·
owner AI Manager/Lead Architect · approval: none (review pending).

## 7. Architecture Principles

- **Single Writer:** every authoritative business fact has exactly one technical ownership
  boundary (AB-01 §C). Convenience duplication is prohibited.
- **Dependency Direction:** SR → WO → JOB; WO → Visit → Report → Customer-Safe Projection;
  audit observes (AB-01 §D).
- **No Reverse Write:** downstream objects consume upstream information by reference and must
  never become its writer (AB-01 §§C–D).
- **Derived Report:** canonical in business meaning, derived in storage; no second store or
  independent write path (AB-01 §H).
- **Append-Only Audit:** observer/history only; never owns or mutates business state (AB-01 §N).
- **Projection Isolation:** customer-safe data derives from canonical data and can never become
  an alternative source of truth (AB-01 §M).

## 8. Logical Architecture

| Layer | Responsibility | Prohibited |
|---|---|---|
| Interface (unspecified technology) | Present use-cases; collect actor input | Business-rule decisions; direct persistence writes |
| Authentication boundary | Establish identity (Google external; local internal) | Authorization decisions |
| Authorization/policy boundary | Enforce actor/action/scope guards at §14 points | Business-rule invention; cross-company grants |
| Application/use-case | Orchestrate one business action per command (§10) | Cross-aggregate writes; hidden side effects |
| Domain/business-rule | Own state machines, guards, invariants (§13, §21) | New states/entities/roles/approvals |
| Persistence | Durable records per ownership (§C); atomic units per §11 | Second writers; second Report store |
| Projection | Gated read-derivation to customer-safe plane | Writes; serving-mechanism lock-in (IS-06) |
| Audit | Append-only event capture (§17) | Mutation; ownership |
| Evidence/file | Artifact + metadata + state dimensions (§18) | Visibility choice by technician; storage-tech lock-in |
| Integration | External seams (§23) | Cross-database FKs for convenience |
| Background processing | Non-critical async only (§22) | Async critical transitions (atomicity) |

Only layers justified by AB-01/TADR usage are included; each prohibition traces to a baseline rule.

## 9. Module Boundaries

Modules mirror canonical ownership: Company · Contact/PIC · SR · WO · JOB · Visit · Report ·
Unit (+ENGINE/GENERATOR/BOX_CHASIS strict subtypes) · customer-safe projection · audit ·
identity/access. Components PUMP/ATS/SYNCHRONOUS_PANEL/TRANSFORMER stay registry-only
(AB-01 via CD-11 §15). Module boundaries never create business entities: JOB stays one concept
across all screens/workflows; no per-workflow JOB variants.

## 10. Command / Query Boundaries

| Command | Owner | Inputs | Validation | Transaction | State change | Audit | Reads downstream |
|---|---|---|---|---|---|---|---|
| CREATE_WO (optional SR reference) | WO service (+SR read) | SR ref; WO data; ≥1 JOB | Existing CREATE_WO authority + SR OPEN + WO guards | Atomic WO formation + source reference/lineage + audit | WO OPEN; SR remains OPEN; lineage | Full event | SR content (reference) |
| Direct WO creation | Service | WO data; ≥1 JOB | Authority + formation guards | Single unit | WO OPEN | Event | — |
| JOB establishment | Service | Agreed work basis | No auto-derivation | Part of formation | JOBs under WO | Event | SR (reference only) |
| Assignment | Service | Person + role | ASSIGN_WO + reason | Single unit | Responsibility set | Event + before/after | — |
| Visit create/start/complete | Service | WO; check-in/out; outcome | Assigned actor; outcome rules | Per-Visit unit | Visit OPEN→COMPLETED | Events | JOB states |
| Visit submission | Service | Declaration | Explicit act | Single unit | →WAITING APPROVAL | Event | Report readiness |
| Report readiness | Service (derived) | Visit data | Recompute rule | Derived, no write tx | NON-FINAL→FINAL on CLOSED | — | Visits |
| Approval | Service | Review coverage | Manager/Admin; ≠ technician/own | Atomic consequence | ⇒CLOSED + FINAL | Event + reason | Report content |
| Closure | System consequence | Approval event | — | Same unit as approval | CLOSED | Event | — |
| Correction | Service | Reviewer decision | Reason (all sideroutes) | Event + lineage | Loop continuation | Event + before/after | Current Visits |
| Reopen | Service | CLOSED WO | Post-CLOSED governance | Identity-preserving | →IN_PROGRESS | Lineage event | — |
| Cancellation | Service | Request→attention→execution | OPEN/IN_PROGRESS origin; trace | Chain unit | CANCELLED | Full chain | — |
| Acknowledgement | Service | Presence/absence | Reason if absent | Independent record | Ack stored (non-gating) | Event | — |

Queries (reads) never mutate; projections read through the §15 gate. No endpoints defined.

## 11. Transaction Architecture

- **SR→WO:** one atomic unit (official WO formation + source reference/lineage + audit succeed/fail together; the SR remains `OPEN`; DRAFT is outside the official-WO unit).
- **Duplicate protection:** the existing atomic uniqueness enforcement at the persistence boundary remains the primary requirement for V1 at-most-one-official-WO-per-SR. An active source-associated DRAFT also cannot be duplicated; route to the existing DRAFT under the approved UI behavior. Concurrent official-WO attempts must not produce duplicates, and attempts that lose the race resolve against the already-established official WO per the canonical block-and-show rule. Detection-before-creation is only a read/UX fast-path, never the concurrency guarantee. No engine, constraint syntax, locking, ORM, framework, or other mechanism is prescribed here.
- **JOB establishment:** inside the formation unit (≥1 at OPEN); later Added-JOB entries are own
  audited units.
- **Approval→closure:** single-event atomic consequence (no window for APPROVED-but-open).
- **Correction/reopen:** each submission an audited unit with lineage; reopen preserves identity.
- Async-afterward allowed only for: projection refresh reads, non-critical notifications/reminders
  (manual baseline), observability emission — never for the units above.

## 12. Concurrency / Idempotency

Principles (no user-visible behavior invented; architecture-level requirements only —
mechanism selection is detailed-design territory):
duplicate submissions must not create duplicate business transitions; concurrent
formation-unit writes must be mutually exclusive in effect; repeated equivalent requests must
converge to one valid business outcome; approval/closure has a single valid consequence;
correction/reopen/cancellation semantics stay deterministic (numbered-cycle ordering).
Visit races resolve through per-Visit ownership (one Visit record per arrival; no shared mutable
execution row); the correction loop remains the only post-approval path per reopen rules.
No idempotency-key mechanism is mandated; no serialization, locking, database, queue/message,
framework, or API mechanism is mandated. Where a choice needs business meaning, mark OPEN —
none required for V1 baseline.

## 13. State Enforcement

Each canonical machine enforced at its owning domain (§9 modules): requester = authorized actor;
validation = domain guard evaluation (AB-01 §§E–F + TADR-04 matrix); persistence = owning
aggregate store; side effects allowed = audit event + derived refresh reads only; audit event per
transition (§17). Machines: SR interaction, WO lifecycle, Visit lifecycle, Report readiness,
correction/reopen — exactly as AB-01 §E. No additional states.

## 14. Authentication and Authorization Architecture

Chain preserved: Google identity → Contact/PIC → Verified PIC Link → Company (TADR-13) plus
internal roles. Enforcement points: identity (auth boundary) · role (policy boundary) · company
scope (projection + write scoping) · unit scope (QR + execution context) · action authorization
(per-command guards §10) · projection access (gate §15). No cross-company mechanism; IS-06
mechanics untouched.

## 15. Customer-Safe Projection

Source of truth = internal canonical plane; projection owned as derived-read plane; generation =
recompute-on-read or gated refresh (mechanism deferred to IS-06); access = scoped readers (unit /
company) through the conjunctive gate (CLOSED + FINAL + Verified PIC + scope + policy +
eligibility); visibility enforced by curation state, never by technician input; leakage prevented
structurally (prices/internal categories absent from the plane). QR unit-scoped; PIC portal
company-scoped; no cross-grant.

## 16. Report Architecture

Authoritative Visit data → derivation/recomputation into the Report view → readiness flag flips on
CLOSED → approval consumes content (read) → correction refreshes from current Visits. Independent
conflicting writes prevented by construction (no Report store accepts direct writes; single writer
= derivation from Visit-owned facts). Never a second source of truth.

## 17. Audit Architecture

Events for every §10 command plus state flips, linkage establishments, and publication-state
changes. Metadata: actor, server timestamp, target/reference (incl. SR↔WO lineage ids), reason
where canonical, before/after where canonical, correlation/trace identifiers for cross-event
lineage. Observer-only; append-only; existing pattern (no new subsystem).

## 18. Evidence / File Architecture

Artifact record + three state dimensions (type / approval_state / publication state, AB-01 via
CD-11 §17) linked to Visit (collection) and surfaced in Report (eligible subset). Event-driven
capture + opt-out-with-reason preserved. Technician visibility choice structurally absent.
Taxonomy beyond the locked floor and storage/serving technology explicitly unmodelled.

## 19. Unit / Component Architecture

Unit → ENGINE → GENERATOR → BOX_CHASIS as strict subtype relationships (no generic EAV/JSON core).
PUMP / ATS / SYNCHRONOUS_PANEL / TRANSFORMER remain registry-only Phase 1 (no promotion without
approval). Subtype field requirements stay OPEN placeholders.

## 20. Service Execution Flow

SR → WO (governed formation) → JOBs (explicit establishment) → Visit(s) (execution records) →
Report (consolidation) → Approval → Closure; correction → reopen → additional execution/evidence →
Report refresh → re-approval/closure per canonical rules. One WO → one Report → N Visits throughout.

## 21. Error / Failure Architecture

Business rejection (guard failure: unauthorized, invalid transition, missing prerequisite, duplicate
blocked) vs technical failure (persistence/downstream/async faults) distinguished at the
application layer: rejections carry the governing rule reference and audit the attempt; technical
failures never fabricate state transitions and never bypass guards on retry. No user-facing message
catalogue invented (IS-08 territory).

## 22. Async / Background Processing

Candidates for async: projection refresh reads; observability emission; manual-reminder delivery
baseline. Each: reason (non-critical path); consistency (reads may lag; never authoritative);
retry (safe: read-only/idempotent); idempotency (required); failure (logged, non-blocking).
Business-critical transitions (§11 units) are never async. No queue technology selected.

## 23. Integration Boundaries

Google identity (auth seam) · Accurate 5 (accounting/inventory authority, unchanged) ·
email/notification (manual-reminder baseline; automation deferred) · file/object storage (seam only,
no tech) · QR generation (unit-scoped identity seam; rotation/expiry deferred) · future mobile app
(consumer of projection plane + command layer, undesigned). No integration APIs designed; no
cross-database FKs for convenience.

## 24. Observability

Application logs, audit records (business semantics, §17), error tracking, correlation IDs, and
request tracing where useful; operational monitoring. Telemetry kept separate from business audit
semantics (never merged, never substituted).

## 25. Data Integrity

Identifiers unique per owning aggregate; uniqueness for source-referenced-WO-per-SR and Report-per-WO;
references as lineage (never cross-owner writes); ownership per §C; company/unit scoping on writes
and reads; lifecycle states from the closed table only; historical records immutable post-terminal;
audit append-only; projections derived. No SQL schema produced.

## 26. Security Boundaries

Authentication (external/internal separation) · authorization (guards at owners) · tenant/company
isolation (workspace + no cross-grant) · unit-scoped QR · projection isolation (priceless,
curated) · internal-data confinement · evidence access via approval states · audit integrity
(append-only, correlation) · session/token security and secret handling (mechanisms deferred to
detailed design; no products selected).

## 27. Open / Deferred Items

All 11 AB-01 §Q items carried with identical status and impact (IS02-O01…O12): none solved, none
converted, none blocking TA-01 — abstract placeholders and unmodelled seams as specified in §§8,
11–13, 15, 18–19, 22–23 above.

## 28. Traceability (AB-01 → TA-01)

Domain boundaries → §9 · ownership → §§8–9 · dependency direction → §§8–10 · lifecycle → §13 ·
transactions → §11 · authorization → §§10,14 · projection → §15 · Report derivation → §16 ·
audit → §17 · evidence → §18 · invariants → §§11–13,15–16,25 · OPEN/DEFERRED → §27. Drift
detectable per mapping; any deviation requires governance decision, never silent adjustment.

## 29. Implementation Gate

TA-01 authorizes nothing. Next: Technical Architecture Review → resolve contradictions → detailed
design → design/approval gates → implementation. No instruction to code in this task.

## 30. Final Self-Check

AB-01 preserved section-by-section (§§C–Q mapped above) ✅ · no new business decision ✅ · no new
entity/state/role/approval ✅ · no template axis ✅ · one JOB ✅ · no schema/API/UI/migration/code ✅ ·
precedence respected (older material never overrides) ✅ · OPEN/DEFERRED intact ✅ · traceability
complete ✅.

---

*End of TA-01 v1.0 DRAFT.*
