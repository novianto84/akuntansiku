# TADR-05 — Database Strategy

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

What database, transaction-model, isolation, indexing-philosophy, and concurrency
strategy should be proposed — honoring the business-locked one-database choice —
without producing any DDL, migration, or table design?

## Authoritative Inputs

- CD-07 Q13 (one database; separate-DB and separate-port approaches not chosen) —
  LOCKED at business level.
- CD-07 Q17 (no automatic cross-workspace movement) and Q16 (no combined
  transaction reporting).
- CD-08 (suggest/approve governance; global effect of approved master changes).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): one relational database with
application-enforced workspace scoping plus invariant guards (TADR-04/TADR-06) as
the primary isolation mechanism. Transaction model follows the per-transition
consistency boundaries of TADR-04. Indexing philosophy (query-driven, projection-
supporting) and concurrency approach (conflict-safe correction chains, no lost
updates on guarded transitions) are stated as philosophy only. No
`CREATE TABLE`, `ALTER TABLE`, migration, or SQL of any kind is produced.

## Alternatives Considered

- **Database-level scoping predicates as well (defense in depth):** stronger
  barrier; kept as an unevaluated option for implementation planning —
  platform-dependent, not selected now.
- **Separate database per workspace:** contradicts locked Q13 (documented only,
  not pursued).

## Trade-offs

Application-level enforcement is portable and directly testable but relies on
call-path coverage; database-level predicates would add a second barrier at the
cost of platform coupling.

## Business Rules Preserved

One-database business choice; workspace ownership split; global effect of
approved master changes; no cross-workspace transaction movement.

## Dependencies / Deferred Decisions

None blocking. Technical evaluation of scoping-predicate support: DEFERRED to
implementation planning.

## Security Impact

Database is the last line of defense only if predicates are added later; for now
isolation is enforced above the store (see TADR-06).

## Audit / Traceability Impact

Single store keeps the governance trail in one place; no cross-store
reconciliation risk.

## Operational Impact

One backup/restore domain (see TADR-17/TADR-18 for backup architecture).

## Reversibility

Low-medium: store choice is costly to reverse after implementation, which is why
only strategy — not product selection — is proposed here.

## Open Questions

- Concrete database product/version selection (implementation planning).
- Whether scoping predicates are adopted (implementation planning evaluation).

## Approval Boundary

Requires Human approval of the strategy. Authorizes no product selection, schema,
migration, code, or Programmer handoff.
