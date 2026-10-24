# TADR-13 — Authentication / Identity-Link

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

How should authentication (local plus external identity provider) and the
identity-link lifecycle be architected — preserving Google Identity → Contact/PIC
→ Verified PIC Link → Company with per-company VERIFIED / PENDING / REVOKED
states and no cross-company grant — when the formal CD traceability of that
chain is currently missing?

## Authoritative Inputs

- Baseline instruction chain (Google Identity → Contact/PIC → Verified PIC Link
  → Company; VERIFIED/PENDING/REVOKED; company-scoped isolation; no cross-company
  grant) — business meaning LOCKED by explicit HUMAN decision (formal CD
  documentation pending).
- CD-03 (Contact/PIC structure; future customer/vendor access) — partial support.
- DECISION_REGISTER: identity-link reconciliation recorded as LOCKED HUMAN DECISION.

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): link-entity lifecycle (link request →
verification → revocation) modeled
separately from the Contact, so a Contact survives revocation and per-company
states are natural. Local authentication remains for internal users; external
provider (e.g. Google OIDC pattern) is mechanism detail. Sessions are
lifecycle-bound with revocation propagation. Future providers stay extensible.
**Identity-link reconciliation is RESOLVED by LOCKED HUMAN DECISION (see
Dependencies); this proposal must not change business meaning.**

## Alternatives Considered

- **Identity attributes on Contact:** simpler; disfavored — revocation would tear
  contact history linkage and per-company states fit awkwardly.
- **External-provider-owned linkage only:** less to build; documented — business
  link-states would be unrepresented.

## Trade-offs

A separate link entity costs a small governance surface (verification UX,
authority) but keeps identity lifecycle independent of relationship data.

## Business Rules Preserved

The full chain and its states exactly as instructed; no cross-company grant. If
Human reconciliation changes the business meaning, this TADR is revised — the
business rule is never bent to fit the mechanism.

## Dependencies / Deferred Decisions

Identity-link reconciliation: RESOLVED by LOCKED HUMAN DECISION (formal CD
documentation pending). Locked business semantics now governing this TADR:
Google-only external sign-up/sign-in; sign-up alone grants no Company/PIC/Unit
access; PIC registration is an application yielding PENDING; supporting evidence
may be requested with no fixed exhaustive taxonomy; Manager/Admin approval
establishes the Verified PIC Link; Google email need not be a company email and
email/domain matching is NOT the requirement; Google Identity ≠ Contact/PIC ≠
Verified PIC Link ≠ Company Access; no cross-company grant. Assessment:
**APPROVED** — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21).
Business Access Model (LOCKED): approval establishes the
Verified PIC Link as the SOLE basis of Company-level access (COMPANY SCOPE: all
Units of that Company held in the CRM, plus histories and PIC display per
customer-safe visibility); login alone, QR possession, company-name knowledge,
or prior unit views never yield Company Scope. Still TECHNICAL PROPOSAL /
DEFERRED (not finalized here):
OAuth implementation details, token handling, session architecture, and provider
mechanics. Status of this TADR is APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21); the listed mechanics remain deferred technical detail.

## Security Impact

Verification authority must be distinct from link creation; revocation must
propagate to sessions; provider secrets follow sealed handling (see TADR-18).
Applicant ≠ approver (LOCKED business invariant): approval of a PIC application
may only be performed by an authorized internal Manager/Admin other than the
applicant. Google Identity is not approval authority; PIC status is not approval
authority; no automatic approval occurs upon submission; direct-URL/API bypass
must not enable self-approval.

## Audit / Traceability Impact

Link lifecycle events (request/verify/revoke, actor, timestamp, company scope)
are first-class audit events.

## Operational Impact

Verification workload sits with the designated business authority, not with
automation; no auto-verification invented.

## Reversibility

Medium: link model is structural once identities exist.

## Open Questions

- Verification authority and evidence standard: RESOLVED by the LOCKED identity-link reconciliation (Manager/Admin approval establishes the Verified PIC Link; supporting evidence may be requested with no fixed exhaustive taxonomy).
- Provider selection and session/token mechanics (post-reconciliation planning).

## Approval Boundary

Human reconciliation of business meaning is complete (LOCKED HUMAN DECISION);
this record is APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL —
2026-09-21). Authorizes no provider integration, code, schema, migration, or
Programmer handoff.
