# TADR-02 — Domain / Aggregate Boundaries

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

What are the conceptual aggregates, who owns each, what are their invariants and
transaction scopes, and how do they reference each other — without producing any
implementation schema?

## Authoritative Inputs

- CD-03 (Company/roles/Contact).
- CD-07 + CD-08 (workspace ownership, shared masters, governance).
- CD-11 §§2, 5, 7, 10, 15, 18 (canonical WO lifecycle; Unit boundary 1 WO = 1 Unit;
  assignment; visit model; replacement; report) — SIGNED-OFF / LOCKED / CLOSED
  (BA SIGN-OFF — CD-11 Business Finalization, CD11-001…CD11-029).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): the aggregate map in §4 of the Finalization
Report — Company (identity root); Contact/CompanyRole (under Company); Identity-Link
(under Contact/Company, semantics unresolved); Unit + Components (asset registry);
WorkOrder (execution + lifecycle owner); execution artifacts (WO-owned); Review /
Correction (governance); MaterialUsage (WO record) vs. InventoryOperation
(inventory movement); commercial aggregates (workspace-owned); price-intelligence
versions (shared); projections (derived, ownerless).

## Alternatives Considered

- **Coarser aggregates (e.g. Service blob containing WO + history + views):**
  simpler; rejected — it would merge transactional source with derived views and
  invite a second source of truth.
- **Finer aggregates (every artifact independent):** more explicit; rejected for now —
  ownership would fragment and transaction scoping would fight the business rule that
  WO owns execution.

## Trade-offs

WO-rooted ownership concentrates service complexity in one aggregate (heavier
aggregate, clearer invariant enforcement) versus distributing it (lighter pieces,
weaker guarantees).

## Business Rules Preserved

Single Company identity; Contact separation; 1 WO = 1 Unit with binding resolved
before CLOSED (CD-11 §5); assignment model; condition-driven evidence; no parallel lifecycle.

## Dependencies / Deferred Decisions

TADR-03 (component structure detail). Subtype field requirements remain an
unresolved gate; aggregate shapes stay placeholders where specs are absent.

Identity-link reconciliation gate — RESOLVED by LOCKED HUMAN DECISION; see TADR-13 and DECISION_REGISTER.md.

## Security Impact

Ownership defines authorization attachment points; cross-aggregate references are
always scope-checked (workspace, unit).

## Audit / Traceability Impact

Aggregate map is the skeleton every audit trail hangs on; correction chains
reference aggregate identities.

## Operational Impact

Conceptual only at this stage; no runtime cost is decided.

## Reversibility

Medium: aggregate boundaries can be redrawn before implementation at low cost;
after implementation, costly.

## Open Questions

- Exact suggestion/approval matrix mechanics (business-deferred, CD-08 open).
- Record shape of the Company ↔ Workspace usage marker (design-deferred, CD-08 Q4).

## Approval Boundary

Requires Human approval of the aggregate map. Authorizes no schema, code,
migration, or Programmer handoff.
