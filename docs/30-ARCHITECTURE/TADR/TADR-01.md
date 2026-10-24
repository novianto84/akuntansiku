# TADR-01 — Application / Module Boundaries

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

How should application code be organized into modules so that business boundaries
(CD-01 workstreams, CD-07 one-platform/multi-workspace) are the primary driver,
technology trends are not, and a future Accounting workstream is not foreclosed?

## Authoritative Inputs

- CD-01 (business scope, CRM-first workstream, deferred Finance/Accounting).
- CD-07 (one Sales Tools / CRM Platform, per-company workspace, one database).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): a modular monolith with
domain / application / infrastructure separation. Candidate modules: Identity,
Asset, Service, Commercial/Sales, Purchasing, Inventory, Price Intelligence,
Visibility/Projection, Platform. Single deployable unit.

## Alternatives Considered

- **Service-split now:** independent scalability; rejected as premature — it would
  distribute the deliberately non-atomic WO ↔ inventory chain across network
  boundaries and split seams whose business requirements are still stabilizing.
- **Layered-only without modules:** simplest start; rejected — business boundaries
  would be unrepresented and accounting-leakage drift harder to detect.

## Trade-offs

Modular monolith keeps deployment simple and matches the locked one-platform
choice, at the cost of discipline-dependent modularity (seam erosion is the main
risk; seam ownership plus review checklist mitigates).

## Business Rules Preserved

CD-01 scope and workstream separation; CD-07 one-platform constraint. No scope
change of any kind. Future Accounting/ERP destination not foreclosed.

## Dependencies / Deferred Decisions

None blocking. Checklist contents and N/A taxonomy affect only container shapes
inside the Service module, not the module map.

## Security Impact

Smaller blast radius per module; enforcement points (workspace guard, visibility
policy) attach to module seams rather than scattered call sites.

## Audit / Traceability Impact

Audit trail recorded per module seam; traceability chain CD → requirement → TADR
preserved per module.

## Operational Impact

Single topology to operate, monitor, and back up. No distributed-transaction
operations burden.

## Reversibility

High: a later service split remains possible along the same seams.

## Open Questions

- Module physical-layout naming (implementation planning, not decided here).
- Whether database-level scoping predicates complement module guards (see TADR-05).

## Approval Boundary

Requires Human approval of the modular-monolith direction. Authorizes no code,
schema, migration, or Programmer handoff.
