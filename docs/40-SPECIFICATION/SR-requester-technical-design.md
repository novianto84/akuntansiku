# SR Requester Identity & Company Boundary — Technical Design V1

```text
Document title: SR Requester Identity & Company Boundary — Technical Design V1
Document type: Technical Design
Scope: V1
Status: TECHNICAL PROPOSAL — APPROVED
Related business decisions: O-01 SR Lifecycle (BD-SR-001); O-02 SR Closure Reason
  (BD-SR-002); O-03 SR Content Boundary (BD-SR-003); O-04 SR Retention & Visibility
  (BD-SR-004); O-05 SR Minimal Permission Matrix (BD-SR-005); O-10 SR Minimal Form
  (BD-SR-010); O-06/O-07 SR→WO (BD-SRWO-001); G-01/G-02 Identity Boundary (BD-G01-G02)
```

> This document defines technical representation only. It does not create or modify
> business policy.

---

## 1. Problem Statement

An SR must represent three things that must not be forced into one field/entity:
(1) who brought the request at intake; (2) which canonical Contact that person is
currently established to be, if any; (3) which Company is the verified business
context. Merging any two corrupts the third: intake-into-Contact fabricates
membership; Contact-into-intake loses history on change; either-into-Company
derives relationships from claims.

## 2. Domain-to-Technical Mapping

| Domain Concept | Technical Representation | Nullable | Mutable | Meaning |
|---|---|---|---|---|
| Requester | snapshot + optional Contact reference | — | partly | Who brought the request (concept) |
| requester_snapshot | immutable intake record on SR | No | No | Who-according-to-SR-at-intake |
| requester_contact_id | FK → contacts.id | Yes | governed only | Currently-known identity per identity system |
| SR.company_id | FK → companies.id | Yes | governed only | Verified business context, independent of requester |

## 3. Proposed SR Data Structure (conceptual — not migration/code)

```text
SR
├── requester_snapshot (immutable intake representation)
├── requester_contact_id → contacts.id [NULLABLE] (current linkage)
├── company_id → companies.id [NULLABLE] (verified business context)
├── O-10 request fields (need/scope/description/reference/commercial/agreement)
└── audit/event references (existing activity_logs pattern)
```

Snapshot answers intake truth; the FK answers current identity; company answers
business context. Each has exactly one job.

## 4. Requester Snapshot Design

Needed because the FK is mutable-by-governance while intake truth is forever: without
a snapshot, "who reported at creation" becomes unanswerable after any Contact change.
Minimum retained: reporter name + contact channel/detail as given. Immutable from
creation; never overwritten by later Contact renames, number changes, status changes,
relationship moves, merges, or deactivation. The snapshot is not a Contact, not a
Contact-master duplicate — it is historical evidence. (Example field shapes, if used
at implementation time, are implementation considerations, not locked schema.)

## 5. Current Identity Linkage

```text
requester_contact_id = NULL
        ↓
governed internal linking
        ↓
requester_contact_id = Contact
```

The FK represents **current known identity**, never identity-at-intake.

| From | To | Allowed | Condition |
|---|---|---|---|
| NULL | Contact | YES | Governed internal action + audit |
| Contact A | Contact B | YES, correction only | Governed action + audit |
| Contact | NULL | NO | — |

Past events are never deleted; corrections append new events.

## 6. Historical Integrity

> Historical truth of intake lives in immutable snapshot. Current identity linkage
> lives in FK. Linkage changes are represented by audit/event history.

"Who was the Requester when the SR was created" is always answered by the snapshot,
regardless of later Contact renames, number changes, status changes, relationship
moves, or linkage corrections.

## 7. Requester vs Company Independence

```text
Requester = source of request
Company   = business context
```

No automatic implication in either direction. Expected representations:

- **Case 1** (existing Contact + own Company): snapshot = reporter; FK → own Contact;
  company_id → own Company.
- **Case 2** (Technician reporter, customer Company): snapshot = technician
  (FK NULL — technician is not that Company's Contact); company_id = known customer
  Company. Technician gains no membership.
- **Case 3** (unverified individual, no Company): snapshot = individual; FK NULL;
  company_id NULL. Valid; proceeds to WO under applicable authority.
- **Case 4** (non-representative reporter, confirmed Company): snapshot = reporter
  (FK NULL); company_id = confirmed Company context. Reporter does not become Contact.

Unconfirmed claimed Company stays narrative (BD-SR-003) and never populates company_id.

## 8. Security Boundary

Requester snapshot grants no access. `requester_contact_id` alone grants no Company
access. `SR.company_id` is not a credential. Claimed Company grants nothing. External
access follows only the canonical chain (Google Identity → Contact/PIC → Verified PIC
Link → Company). **SR identity linking is not a grant of external Company access.**

## 9. Authorization / Governance Boundary

> Requester identity linking is a governed internal action and must be audited. A
> dedicated approval workflow applies only where the applicable authorization policy
> requires it. Linking a Requester never grants Company access by itself.

No new approval workflow or entity is created.

## 10. Audit Requirements

Minimum for each identity-link action (existing pattern, no new table): actor, server
timestamp, SR, previous linkage, new Contact, action, reason/context where needed.
History is append-only.

## 11. Deduplication Boundary

No automatic identity matching; no automatic merge; duplicate names possible; human
review required before linking; reuse existing Contact when confidently identified;
never create a Contact merely to satisfy SR structure; no fake Contact; no fake
Company. V1 only.

## 12. Individual Customer Boundary

`Requester = Individual + Company = NULL` is valid; SR and WO proceed under business
authority/rules. No fake Company, no fake Contact, no special `IndividualCustomer`
entity. Individual external/Company/PIC access stays out of V1 scope.

## 13. Implementation Impact

Current codebase (as inspected): Company, Contact, SR, WO are not implemented modules;
therefore no migration now, no schema patch now, no changes to customers/vendors,
users, or accounting masters, and no new Requester table. When SR/Company/Contact are
implemented, this note is the constraining technical reference. No implementation code
is created by this note.

## 14. Non-Goals / Explicitly Rejected

`Requester` entity ❌ · requester as access credential ❌ · `customers` as Company
identity root ❌ · `vendors` as Company identity root ❌ · fake Contact ❌ · fake
Company ❌ · automatic dedup/merge ❌ · automatic Requester → Company derivation ❌ ·
Company → Requester derivation ❌ · separate Additional/Add/Issued Work concept ❌ ·
new approval workflow solely for requester linking ❌.

## 15. Technical Risks

Residual V1 risk: intake name collision / duplicate person names before identity
linking. Mitigation: human review, existing-Contact lookup, no auto-merge, immutable
snapshot, audit trail. Risk accepted as stated; not larger than this.

## 16. Decision Status

> **Technical recommendation: APPROVED for future V1 implementation.**

> This approval does not create a new business decision and does not modify the
> Decision Register.

*End of technical design note.*
