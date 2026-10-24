# BD-SR-010 — SR Minimal Form V1 (O-10)

```text
Decision ID: BD-SR-010
Title: SR Minimal Form V1 — Fields, Guards, Lifecycle Behavior (O-10)
Mode: Business Decision
Status: LOCKED — V1 (BUSINESS AUTHORITY APPROVAL 2026-09-23)
Business Authority Approval: YES (G-01/G-02 lock unblocked O-10; BA-approved O-10 revised proposal + create guard, 2026-09-23)
Implementation Authorization: NO
```

> Minimal SR form: what must be recorded at intake, what may follow, and how the form
> behaves per lifecycle state. Consumes BD-SR-001…BD-SR-005, BD-SRWO-001, BD-G01-G02,
> BD-WORKTYPE-001, BD-WORKMODEL-001 unchanged. No new status, workflow, entity,
> schema, or UI is created. Field *representation* (technical) is deferred to
> implementation/security design; only business content + guards are locked here.

---

## 1. Minimal fields (LOCKED — V1)

| Section | Field | Required | Purpose | Editable |
|---|---|---|---|---|
| Request | Requested Need (text) | ✅ (or Scope — at least one) | Why the SR exists | OPEN per BD-SR-005 |
| Request | Requested Scope (text) | Optional | Desired extent; stays request even if finally worded | OPEN per BD-SR-005 |
| Request | Description / narrative (long text) | Optional | Complaints, comms, context, suspicions, follow-up notes (as-reported) | OPEN per BD-SR-005 |
| Request | Reference Item/Service (lookup, multi) | Optional | Understanding pointer; never commitment/JOB | OPEN per BD-SR-005 |
| Identity | **Requester** (known identity/contact OR new intake entry, UNVERIFIED) | ✅ required | Who brought the request; ≠ Created By; ≠ authorization | OPEN per BD-SR-005 |
| Identity | Created By (system actor) | System | Internal user recording the SR | Audit append-only |
| Context | Company | Optional, **NULL valid** | Related company if known; existing verified relationship → fill per relationship; mere claim → NULL + narrative only; individual → NULL; never fake | OPEN |
| Context | Location (text) | Optional | Site/location if relevant | OPEN |
| Commercial | Commercial notes (text) | Optional | Estimates/budget/quotation refs/negotiation — information | OPEN |
| Commercial | Agreement context (text) | Optional | Informal consent — context, never action | OPEN |
| Closing | Closure reason + Keterangan | Mandatory only on OPEN → CLOSED | BD-SR-002 | Once; immutable after |
| System | SR number, status, timestamps, audit | System-generated | Identity, lifecycle, audit | Official transitions + append-only |

## 2. Create guard (LOCKED — V1)

```text
CREATE SR VALID IF: Requester REQUIRED
  AND (Requested Need OR Requested Scope) REQUIRED (at least one)
  AND Company OPTIONAL
```

No `Company OR Contact required` rule: Requester itself is the required identity
context. Requester MUST exist; it NEED NOT be a Verified PIC. Valid: verified PIC
with company; UNVERIFIED newcomer with claimed/known company context; individual
with NULL company. Invalid: empty requester.

## 3. Identity rules applied (from BD-G01-G02, restated not changed)

- Requester ≠ Created By (both may coincide, e.g. technician-found needs).
- New requesters are UNVERIFIED intake entries; creating one never auto-creates a
  Verified PIC, Contact membership, Company relationship, access, or WO authority.
- Verification/promotion only via authorized actor, existing-contact check first,
  no duplicates, canonical Verified PIC Link mechanics, applicant ≠ approver,
  no auto-merge/delete, history never rewritten.
- `Company = PT XYZ` on claim alone is prohibited as a relationship.

## 4. Lifecycle behavior (applies BD-SR-001/002/004/005, reconciled to final Human decision)

- OPEN: create + full pre-terminal edit; `OPEN → CLOSED` is the only status transition.
- Follow-up and WO creation are activities; neither changes the SR status.
- Creating/forming a WO or saving a WO DRAFT leaves the SR `OPEN`.
- CLOSED: fully read-only (content + closure reason immutable); SR persists as history;
  no reopen V1; no delete V1.

*End of BD-SR-010. O-10 is LOCKED — V1.*
