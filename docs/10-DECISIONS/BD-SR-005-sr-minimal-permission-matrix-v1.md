# BD-SR-005 — SR Minimal Permission Matrix V1 (O-05)

```text
Decision ID: BD-SR-005
Title: SR Minimal Permission Matrix V1 (O-05)
Mode: Business Decision
Status: LOCKED — V1 (BUSINESS AUTHORITY APPROVAL 2026-09-23)
Business Authority Approval: YES (HANDPROMPT — O-05 FINAL CLARIFICATION & LOCK, 2026-09-23)
Implementation Authorization: NO
```

> Locks the V1 SR permission matrix as reconciled to the explicit Human decision.
> Existing `CREATE_WO` grants are unchanged. V1 `CLOSE_SR` is Manager + Admin only.
> No new role, approval workflow, field, entity, schema, or UI is created. Relevance
> stays a business principle (BD-SR-004 §2) with technical enforcement deferred to
> implementation/security design. Future Close SR configurability is a separate
> Configuration Panel concern and does not change V1 authority.

---

## 1. Role authorities (LOCKED — V1, as reconciled by explicit Human decision)

### 1.1 Admin — unrestricted operational authority

Admin holds full operational authority in the CRM, including READ_SR, CREATE_SR,
EDIT_SR, FOLLOW_UP_SR, CLOSE_SR, CREATE_WO, and other operational authority already
defined in governance (cf. CD-11 cancellation execution, mandatory review, curation,
configuration: §§9, 17, 19). Nothing in canonical governance restricts Admin; this
decision records — not expands — that standing for SR V1.

### 1.2 Manager

Retains all LOCKED authority: CREATE_WO + ASSIGN_WO (O-06) and full SR activity,
including CLOSE_SR in V1. No additional approval layer.

### 1.3 Sales

Retains existing authority (default CREATE_WO per CD-11 §4) and performs SR activity
per relevance and applicable authority; Sales has no CLOSE_SR authority in V1.

### 1.4 Coordinator

Coordinator does NOT hold default CREATE_WO in V1: no canonical decision/document
grants it (CD-11 §4 grants Sales default + Technician grantable + others configurable;
Coordinator is not among the grantees), and O-05 must not expand CREATE_WO to fill
the matrix. Coordinator performs SR activity per relevance and established authority;
Coordinator has no CLOSE_SR authority in V1.

### 1.5 Technician

- CREATE_SR: ALLOWED. A Technician creating an SR is only **recording a Request** —
  never creating a JOB, establishing official work, auto-creating a WO, or changing SR
  lifecycle. `SR provides request context; WO establishes work` (BD-SR-003 §2).
- EDIT_SR / FOLLOW_UP_SR: ALLOWED where relevant.
- CLOSE_SR: NOT ALLOWED in V1.
- WO creation remains governed only by the existing `CREATE_WO` authority; it is not
  granted by a separate SR-conversion action.

## 2. Permission matrix (LOCKED — V1)

✅ allowed · ⚠️ allowed with condition · ❌ not allowed.

| Action | Admin | Manager | Sales | Coordinator | Technician | Customer PIC |
|---|---|---|---|---|---|---|
| READ_SR | ✅ unrestricted | ✅ workspace/relevance | ⚠️ relevance | ⚠️ relevance | ⚠️ relevance | ❌ |
| CREATE_SR | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| EDIT_SR | ✅ | ✅ | ⚠️ relevance | ⚠️ relevance | ⚠️ relevance | ❌ |
| FOLLOW_UP_SR | ✅ | ✅ | ✅ | ✅ | ⚠️ relevance | ❌ |
| CLOSE_SR | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

No action on a `CLOSED` SR by any role (immutable, BD-SR-004 §5). Customer PIC has
no SR action of any kind in V1 (BD-SR-004 §3). A saved WO DRAFT may be visible only
under existing visibility authority; only its creator may continue it (CD-11 §DRAFT).

`CREATE_WO` remains governed by the existing canonical WO authority model. There is
no separate SR conversion action/permission. Historical `CONVERT_SR` terminology and
records are not renamed, migrated, or modified.

## 3. Transition authority (LOCKED — V1, consistent with reconciled BD-SR-001)

| Transition | Allowed role | Conditions |
|---|---|---|
| OPEN → CLOSED | Admin, Manager only | `closure_reason` mandatory (BD-SR-002) |

`FOLLOW_UP_SR` records activity while the SR remains `OPEN`; it does not create a
status or transition. Creating/continuing a WO does not change SR status.

## 4. WO relationship (not an SR action or transition)

A WO may reference its originating SR via the existing source-reference lineage
(BD-SRWO-001 O-07). The SR remains `OPEN`. A saved DRAFT is not an official Related
WO; the official relationship is presented when the WO reaches `OPEN` under CD-11
rules. Draft continuation remains creator-only. Existing `CREATE_WO` authority and
BD-SR-011 duplicate/atomicity rules remain separate from `CLOSE_SR`.

## 5. V1 Close SR configurability boundary

V1 Close SR authority is Admin + Manager only. A future Configuration Panel may make
authorization configurable as a separate configuration concern; that future
possibility does not change V1 permissions, Create WO authority, or lifecycle
semantics.

## 6. Consistency record

- Admin remains unrestricted in the SR permission model.
- Manager retains existing `CREATE_WO`/`ASSIGN_WO` authority and is additionally one
  of the only V1 `CLOSE_SR` roles under the final Human decision.
- Sales, Coordinator, and Technician retain their unrelated permissions; none has
  `CLOSE_SR` in V1. No other grant is changed.
- `CREATE_WO` is still governed by the existing canonical authority model and is
  independent from `CLOSE_SR`.
- Human-approved lifecycle semantics are `OPEN → CLOSED`; a WO relationship does not
  change the SR status. `CONVERT_SR` remains unchanged only in historical records/data.

*End of BD-SR-005.*
