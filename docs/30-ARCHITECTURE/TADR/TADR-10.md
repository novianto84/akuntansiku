# TADR-10 — Material vs Inventory Separation

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

How do WO MaterialUsage records and InventoryOperation movements relate —
preserving "Inventory = quantity authority" and "Material Usage = WO operational
record" — across the non-atomic flow and the non-stock/customer-owned/
direct-purchase case, without introducing valuation, costing, or accounting?

## Authoritative Inputs

- CD-11 §13 (operational record; non-atomic flow; non-stock recordable without
  stock-out) — SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF).
- CD-04 R1–R5 (Harga Perolehan as operational reference; no aggregates, costing,
  or accounting).
- CD-10 (quantity-only authority; no reservation/valuation/costing).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): two-sided modeling. The WO side records
Item + Quantity + Harga Perolehan per Unit as the operational fact. The inventory
side records workspace stock movements with full traceability. The two reference
each other but neither controls the other. Non-stock / customer-owned /
direct-purchase usage is a first-class usage class with no linked movement and
no phantom stock entry. Terminology discipline: "Harga Perolehan (per Unit)";
avoid "Acquisition Cost"/"Material Cost" as primary terms.

## Alternatives Considered

- **Single unified material-movement record:** one write, always consistent;
  rejected — it cannot represent the non-stock class and collapses the
  WO-record vs. inventory-authority separation the baseline requires.
- **Forced balancing entries for non-stock usage:** rejected — phantom movements
  falsify inventory authority and smuggle in valuation semantics.

## Trade-offs

Two-sided records tolerate real-world ordering gaps at the cost of a
reconciliation surface; terminology discipline is convention-dependent and needs
review-checklist enforcement.

## Business Rules Preserved

Conceptual chain WO → Material Usage → Inventory Operation; non-atomic flow;
non-stock class; quantity-only inventory; full accounting exclusion.

## Dependencies / Deferred Decisions

TADR-04 (paired-record transaction pattern). No blocking gate.

## Security Impact

Material-take authority (who may record usage / trigger stock-out) is enforced
with TADR-14; no separate material-security model invented.

## Audit / Traceability Impact

Mutual references make each usage jointly auditable from WO side and movement
side; non-stock usages remain auditable as WO facts.

## Operational Impact

Reconciliation attention for dangling halves; no totals, aggregates, or costing
computations anywhere in the flow.

## Reversibility

Medium: record separation is structural once data exists.

## Open Questions

- Reconciliation surfacing rules detail (Outstanding surfacing gate — business-owned).

## Approval Boundary

Requires Human approval of the two-sided direction. Authorizes no schema, code,
migration, costing, or Programmer handoff.
