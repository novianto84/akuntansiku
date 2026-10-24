# IS-04 — API & Service Contract Specification

```text
Document ID: IS-04
Title: API & Service Contract Specification
Version: 1.1 (controlled correction v1.0→v1.1: M-01 §7 wording aligned to TA-01 v1.1; no content revision)
Status: LOCKED / CANONICAL — BUSINESS AUTHORITY APPROVAL (review: NEEDS CORRECTION → M-01 RESOLVED; MUST/SHOULD FIX 0; UNSOURCED 0)
Lock record: settled normative content authoritative as reviewed; OPEN/DEFERRED items remain unresolved.
Scope: Service boundaries; business-action catalog + contracts; authorization hooks;
  I/O and validation responsibility; transaction, concurrency/idempotency, and error
  expectations; read contracts; evidence/audit interfaces (by reference only).
Authority: AI Manager / Lead Architect. Business Authority owns all rules.
Sources: IS-01 entities; IS-02 guards + decomposition §§10–12,20–24; AB-01; TA-01 v1.1
  §§10–12,20–24; IS-03 authorities/scopes (consumed, not redefined); IS-11 scoping;
  BD-SR-001/002/005/011 (SR commands); CD-11; TADR-02/04/07/08/12/14.
ID basis: BA authorization for IS-04 at docs/40-SPECIFICATION/IS-04-api-service-contract.md.
Implementation: NO endpoints/paths/schemas/frameworks/code/TASK-001. Technology-neutral.
```

> Contracts state *what each business action requires and guarantees* — never endpoint paths,
> payload schemas, or framework mechanics. Evidence objects are owned by IS-05; audit events by
> IS-07 — referenced here, never redefined (joint interface rule).

---

## 1. Scope

Business-action service contracts for SR, WO, JOB, Visit, Report, evidence (by reference),
correction/reopen/cancel, acknowledgement, and reads. Out of scope: endpoint/path/schema design,
auth/session mechanics, storage/serving tech, UI, permission-matrix content (OPEN HD-06).

## 2. Service Boundaries

One service per owning aggregate (TA-01 §9 modules): SR service · WO service (incl. JOB scope
states) · Visit service · Report derivation service (read-compute, never direct-write) ·
evidence service (contract surface only; objects IS-05) · audit emission (events defined IS-07) ·
projection read service (gated reads; mechanism IS-06) · identity/access evaluation (IS-03).
Cross-service calls are reference reads or owned commands; no service writes another's state.

## 3. Business-Action Catalog

| # | Action | Owner | Authority hook (IS-03) | State preconditions |
|---|---|---|---|---|
| A1 | CREATE_SR | SR service | BD-SR-005 matrix | Requester + (Need OR Scope) |
| A2 | FOLLOW_UP_SR (activity; SR stays OPEN) | SR service | BD-SR-005 | SR OPEN |
| A3 | CLOSE_SR | SR service | BD-SR-005 + BD-SR-002 reason | SR OPEN; Manager or Admin only in V1 |
| A4 | CREATE_WO (optional SR reference) | WO service | Existing CREATE_WO authority + BD-SR-011 guards | SR OPEN; active DRAFT routes to existing draft; official-WO duplicate guard; ≥1 JOB at OPEN |
| A5 | Direct CREATE_WO | WO service | CREATE_WO | ≥1 JOB at OPEN |
| A6 | Assignment / Take-Over / Self-Add | WO service | ASSIGN_WO + reason | WO not CLOSED/CANCELLED |
| A7 | Visit create/check-in/check-out/complete | Visit service | Assigned actor | WO IN_PROGRESS; outcome rules |
| A8 | JOB CHECK transitions + Added-JOB entry | WO service | Executing actor | Actually-performed only (IS-05 objects by ref) |
| A9 | Submit (→WAITING APPROVAL) | WO service | Explicit technician act | Work/report declared done |
| A10 | Approve / request-correction / direct-edit / direct-close | WO service | Manager/Admin; ≠ technician/own | WAITING APPROVAL + review coverage |
| A11 | REOPEN / RE-CREATE / Cancel | WO service | Reviewer / governed chain | CLOSED-only / new identity / OPEN-IN_PROGRESS origin |
| A12 | Acknowledge (optional) | Visit service | Presence recorder | — (non-gating) |

## 4. Authorization Expectations

Every contract carries actor + authority + state preconditions resolved against IS-03
authorities and IS-11 workspace/company scope; denial follows IS-03 §9. V1 `CLOSE_SR` is Admin + Manager per the final Human decision; `CREATE_WO` and all other
permissions follow existing canonical authority. Remaining matrix cells beyond locked
authorities stay OPEN (HD-06) — contracts expose the hook, never an invented value.

## 5. Input / Output Responsibility

Input: owning service validates presence, scope, and state eligibility; referenced objects
(SR content, evidence, Contacts) are read by reference, never copied as authority. Output: the
owned state change + lineage references (`source_sr_id`, `CREATED_FROM` where canonical) + audit
event emission duty (event defined by IS-07). No blind-copy semantics anywhere (BD-SR-011).

## 6. Validation Responsibility

Owning service validates: authority held; object in eligible state; guards satisfied (JOB minimum,
outcome reasons, evidence opt-out reasons, closure reasons); scope membership (workspace/company).
Validation failure → business rejection carrying the governing rule (TA-01 §21), audited attempt.

## 7. Transaction Expectations

Per TA-01 §11 units, restated as contract obligations: A4 atomically forms the official WO
with source reference/lineage and required audit; the SR remains OPEN and a DRAFT is outside
official Related WO presentation. Preserve atomic uniqueness enforcement for the existing
at-most-one-official-WO-per-SR guard. An active source-associated DRAFT routes to the existing
DRAFT and cannot produce another active DRAFT; Continue Draft remains creator-only under CD-11.
Detection-before-creation is only a UX/read fast-path; it does not replace concurrency protection.
A6–A9 remain single units; A10 approval⇒closure single consequence; A11 lineage-preserving
units. No engine/technique prescribed.

## 8. Concurrency / Idempotency Expectations

Per TA-01 §12 (requirements, mechanisms deferred): no duplicate transitions on retry/double-submit;
mutually exclusive formation effects; convergence on existing WO for raced source-linked WO creation; per-Visit
ownership for Visit races; deterministic reviewer-action ordering at detailed design (TA-AR-03).

## 9. Error Semantics

Business rejection (unauthorized / invalid transition / missing prerequisite / duplicate blocked /
guard unmet) vs technical failure (persistence/downstream faults: no fabricated transitions, no
guard bypass on retry). Rejections reference the governing rule; no message catalogue invented.

## 10. Read Contracts

Reads never mutate. Projection reads pass the conjunctive gate (CLOSED + FINAL + Verified PIC +
scope + policy + eligibility); QR reads resolve exactly one Unit; internal reads resolve workspace
scope. Serving mechanics deferred to IS-06.

## 11. Evidence Interfaces (IS-05 owned — reference only)

Contracts A7/A8/A10 consume IS-05 definitions: capture slots (locked floor), opt-out-with-reason,
approval/publication states, Visit linkage, eligible subsets. Interface dependency recorded; if
IS-05 has not finalized a referenced definition, this contract carries the reference as OPEN and
invents nothing. No second evidence model exists in this document.

## 12. Audit Interfaces (IS-07 owned — reference only)

Every action A1–A12 emits the corresponding IS-07 event family (actor, server timestamp, object,
reason, before/after where canonical). Interface dependency recorded; event definitions live in
IS-07. No competing event model exists here.

## 13. Dependency / Open-Gate Section

Depends on IS-01/02/03 (LOCKED) + IS-05 object definitions (interface) + IS-07 event definitions
(interface). OPEN carried: HD-06 matrix content; C-4 values; provider/session mechanics; IS-06
serving; deployment; F-1/OQ content items where they touch contracts (checklist taxonomy, evidence
categories, subtype fields, ack types, correction definitions, retroactive convention).

## 14. Traceability

§§2–3 → TA-01 §§9–10 + IS-02 §18 + BD-SR series + CD-11. §§4,6 → IS-03 + IS-11 + TADR-14.
§§7–8 → TA-01 §§11–12 + BD-SR-011. §9 → TA-01 §21. §10 → AB-01 §M + IS-06 boundary. §§11–12 →
IS-05/IS-07 ownership (reference). Classification: LOCKED/DERIVED except §13 OPEN items.

## 15. Acceptance Criteria

AC-1 every cataloged action has owner/authority/preconditions. AC-2 no endpoint/path/schema/tech
present. AC-3 evidence/audit appear only as references. AC-4 OPEN cells marked, never filled.
AC-5 zero UNSOURCED requirements. AC-6 joint checkpoint with IS-05/IS-07 passed.

## 16. Self-Audit

Authorized path ✅ · DRAFT ✅ · ownership boundaries respected (no evidence/audit redefinition) ✅ ·
no OPEN resolved ✅ · no endpoints/schemas/tech ✅ · no TASK-001 ✅ · traceability complete ✅ ·
neutrality intact ✅ · single-file scope (this document only) ✅.

---

*End of IS-04 v1.0 DRAFT.*
