# TADR-16 — QR Mechanism

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

What technical mechanism realizes a PERMANENT, UNIT-SCOPED QR that opens only
that Unit's customer-safe history — comparing signed opaque token, random
identifier, rotating token, database-backed token, URL indirection, and
revocation models — under the LOCKED CONTROLLED ACCESS policy (SCAN QR →
SIGN UP / SIGN IN via Google → CHECK ACCESS → UNIT DATA, no data without login)?

## Authoritative Inputs

- CD-11 §26 (QR permanent + unit-scoped; customer-safe history of that Unit only;
  access mechanism DEFERRED) — SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF).
- QR access policy: LOCKED as CONTROLLED ACCESS (formal CD documentation pending).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21) (technical criteria only): database-backed
indirection with unguessable identifier, decoupling permanent QR identity from
rotatable secret so abuse response (rotation/revocation) does not break
permanence. Resolution is unit-rooted: a token resolves to exactly one Unit and
its customer-safe projection; cross-unit browsing is structurally impossible.
**CONTROLLED ACCESS is the locked policy applied here: no data of any kind is
shown before Google sign-up/sign-in, including no public preview.**

## Alternatives Considered

- **Signed opaque token (stateless):** no lookup; key-rotation story required,
  revocation harder.
- **Random identifier without indirection:** simplest; rotation breaks permanence
  unless aliased.
- **Rotating token:** best abuse-resistance; conflicts with PERMANENT unless a
  permanent-identity-plus-alias design is added.
- **Direct URL to record:** rejected — enumerable, unscoped, unrevocable.

## Trade-offs

Indirection costs a lookup per scan but buys revocability with permanence; signed
tokens invert that trade. All options require abuse-rate monitoring (TADR-18).

## Business Rules Preserved

Permanence; unit scope; customer-safe-only content; no cross-unit portal.

## Dependencies / Deferred Decisions

QR access policy: RESOLVED by LOCKED HUMAN DECISION — CONTROLLED ACCESS
(formal CD documentation pending). Locked business flow now governing this
TADR: SCAN QR → SIGN UP / SIGN IN (Google-only external model) → CHECK ACCESS
→ UNIT DATA; no anonymous access from scan alone; QR permanent and unit-scoped
to exactly one Unit; authorized users receive customer-safe information only,
with internal operational, price, acquisition-price, accounting, and other
excluded internal data never exposed. Assessment: **APPROVED** — HUMAN FINAL
TECHNICAL ARCHITECTURE APPROVAL (2026-09-21).
Still TECHNICAL PROPOSAL / DEFERRED (not finalized here): QR token format, URL
structure, rotation/expiry mechanics, and serving infrastructure. Customer
publication model gate continues to constrain served content (with TADR-11/12).
Business Access Model (LOCKED): QR printed on a Unit, Invoice, Surat Jalan, or
other Unit-related document is the SAME QR resolving to the SAME Unit identity —
no separate invoice/delivery scope exists unless the HUMAN decides otherwise.
Resolution outcome is two-tiered: an authenticated user who is NOT a verified PIC
of the owning Company receives UNIT SCOPE only (that Unit's customer-safe data,
no browsing); a verified PIC of the owning Company receives COMPANY SCOPE via
TADR-13/14. Knowing a QR, a company name, or a unit number never yields Company
Scope. Status of this TADR is APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21); the QR token/URL/rotation mechanics remain deferred technical detail.

## Security Impact

Unguessable identifiers; scope-bound resolution; revocation/rotation story;
abuse monitoring; no internal paths or identifiers leaked in QR payloads.

## Audit / Traceability Impact

Token issuance/rotation/revocation and scan-side access events are traceable
within privacy bounds set by the locked CONTROLLED ACCESS policy and
customer-safe rules.

## Operational Impact

Identifier lifecycle operations (issue/rotate/revoke/reprint coordination) are
business operations; mechanics deferred to implementation planning.

## Reversibility

Medium: token shapes and payload formats are costly to change after physical QR
labels are printed and distributed.

## Open Questions

- Two-tier (unit-scope / company-scope) resolution detail (implementation planning).
- Rotation/reprint coordination procedure (post-policy planning).

## Approval Boundary

Requires Human access-policy decision FIRST, then approval of the mechanism.
Authorizes no token issuance, label printing, code, schema, migration, or
Programmer handoff.
