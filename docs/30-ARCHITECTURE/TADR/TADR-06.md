# TADR-06 — Workspace Isolation Enforcement

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

How is workspace isolation technically enforced — one platform, one database,
workspace-owned transactions, shared masters only where explicitly allowed, no
automatic cross-workspace movement, no combined global transaction reporting —
and how is it tested?

## Authoritative Inputs

- CD-07 (Q1–Q3 platform/workspace; Q4–Q9 shared masters/intelligence; Q10–Q12,
  Q15–Q16 workspace-owned data; Q13 one database; Q17 hard constraint; Q18 no
  journal/GL/ledger).
- CD-08 (ownership model; global vs. workspace-owned classification).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): application-level workspace-scope guard on
every write and read path as primary enforcement, composed with authorization
middleware/domain policy (TADR-14). Shared-master references (Company, Contact,
Vendor, Item, Offer, AcquisitionReference) are explicitly allowlisted; everything
else defaults to active-workspace scope. Required acceptance evidence at
implementation planning: negative tests — attempted cross-workspace write, read,
numbering reuse, and global-transaction report must all fail.

## Alternatives Considered

- **Plus database-level scoping predicates:** defense in depth; unevaluated option
  (see TADR-05), not selected now.
- **Convention/documentation only:** rejected — a hard business constraint needs
  enforceable, testable mechanism.

## Trade-offs

Application guards are portable and testable but depend on covering every path;
adding store-level predicates later would strengthen guarantees at platform cost.

## Business Rules Preserved

All CD-07/CD-08 ownership and constraint rules, especially Q17 and Q16. No tenant
IDs, permission keys, or schema shapes are defined here.

## Dependencies / Deferred Decisions

Record shape of the Company ↔ Workspace usage marker: DEFERRED (CD-08 Q4).
No blocking gate.

## Security Impact

Workspace isolation is the primary tenant-security boundary; its violation class
(cross-workspace read/write) is a first-order security event (see TADR-18).

## Audit / Traceability Impact

Every cross-scope reference (shared-master use inside a workspace transaction) is
a traceable event distinguishing shared intelligence from workspace activity
(CD-08 Q16).

## Operational Impact

Negative-test suite becomes a permanent regression asset; no runtime timers or
automation involved.

## Reversibility

High pre-implementation; structural post-implementation.

## Open Questions

- Exact guard composition with authorization middleware (implementation planning).
- Store-predicate adoption (implementation planning evaluation).

## Approval Boundary

Requires Human approval of the enforcement direction. Authorizes no code, schema,
migration, or Programmer handoff.
