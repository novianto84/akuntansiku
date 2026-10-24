# TADR-14 — Authorization / Visibility Enforcement

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

How are authentication, authorization, and business visibility separated, and what
candidate enforcement architecture realizes them — without equating role with
visibility policy and without silently locking a business permission matrix?

## Authoritative Inputs

- CD-01 S3 (role structure ADMIN/MANAGER/FINANCE/KASIR; RBAC detail is separate
  design work).
- CD-06 Q8 (dynamic role-based Vendor Offer visibility via Admin configuration;
  ownership/history/provenance unchanged).
- CD-11 §25 (customer-safe inclusion/exclusion; reviewer curation) —
  SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): three separated layers — authentication
(who, with TADR-13); authorization (what actions, action-level checks at
domain-policy enforcement points composed with the workspace guard); business
visibility (which intelligence/fields are visible: Vendor Offer policy overlay
plus customer-safe filtering). The detailed RBAC/permission matrix content stays
business-owned and is NOT locked here. Business Access Model (LOCKED): the
visibility layer enforces exactly two external tiers with no third tier —
UNIT SCOPE for any authenticated user in QR context (unit identity, owner
company, address, work/material history; never PIC details or PIC lists, never
other units or their histories, never company-level data, never prices) versus
COMPANY SCOPE for a verified PIC of that Company (all its Units held in the CRM
plus histories, with PIC display per customer-safe visibility). Invariants
enforced: LOGIN ≠ COMPANY ACCESS; QR ≠ COMPANY ACCESS; only a Verified PIC
Link yields Company Scope.

## Alternatives Considered

- **Pure role checks everywhere:** simpler; rejected — it conflates role with
  visibility policy and cannot express the CD-06 Q8 overlay or reviewer curation.
- **Hardcoded permission matrix now:** complete-looking; rejected — it would
  silently lock business content.

## Trade-offs

Three layers cost policy-surface maintenance but keep ownership, action rights,
and visibility independently changeable — matching how the baseline changes them
independently.

## Business Rules Preserved

Role structure as-is; Q8 semantics (toggle visibility without touching ownership,
records, history, acquisition, or provenance); customer-safe exclusion list;
reviewer curation.

## Dependencies / Deferred Decisions

Business permission-matrix content: business-owned, open (partly blocking for
enforcement completeness, not for the layered direction). Business Access Model:
LOCKED (two scopes plus access invariants above; formal CD documentation pending).

## Security Impact

Least-privilege attachment points at domain policy; visibility layer prevents
price-intelligence and internal-data leakage independent of action rights.

## Audit / Traceability Impact

Authorization decisions on guarded actions and visibility-policy changes
(Admin toggles) are audit events.

## Operational Impact

Visibility-policy administration is a business operation surface; no policy
content invented.

## Reversibility

Medium: layering is structural but content stays data-driven.

## Open Questions

- Permission-key naming and matrix content (business-owned, future decision).
- Guard composition mechanics with TADR-06 (implementation planning).

## Approval Boundary

Requires Human approval of the layered direction. Authorizes no matrix content,
code, schema, migration, or Programmer handoff.
