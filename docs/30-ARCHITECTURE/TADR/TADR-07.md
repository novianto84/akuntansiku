# TADR-07 — Source-of-Truth Ownership

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

For each important object — who owns it, who can modify it, what it controls,
what references it, and what must not control it — so that no competing source
of truth is introduced?

## Authoritative Inputs

- CD-03 (Company identity; Contact separation).
- CD-07 + CD-08 (workspace vs. shared ownership).
- CD-10 (inventory quantity authority).
- CD-11 §30 (one operational history, multiple contextual views) — SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): WO owns service execution; Unit owns asset
parenthood; Inventory owns quantities; Company owns identity; Reviewer owns
curation. Service history, customer views, QR views, technician views, and
Outstanding views are derived projections that reference — never duplicate —
operational records. MaterialUsage references but never controls
InventoryOperation.

## Alternatives Considered

- **Writable history/projection stores (dual-write):** faster reads in spots;
  rejected as default — independently editable copies create competing sources of
  truth with undetectable divergence.
- **Unit-owned execution (WO subordinate to Unit registry):** rejected — the
  business rule makes WO the operational owner and Unit the asset parent; the
  direction matters for modification rights.

## Trade-offs

Single-write discipline concentrates write-path design effort but eliminates an
entire class of divergence bugs and audit ambiguity.

## Business Rules Preserved

Canonical Company identity; Unit asset parenthood; inventory quantity authority;
one-history/multiple-views principle; reviewer curation ownership.

## Dependencies / Deferred Decisions

TADR-12 (projection mechanics). No blocking gate.

## Security Impact

Ownership defines who may mutate what; derived views are read-only by
construction, shrinking the writable attack surface.

## Audit / Traceability Impact

Single-write lineage makes every projected row traceable to exactly one source
record plus (for customer-facing output) a curation event.

## Operational Impact

Write-path contention is owned by few aggregates; read scaling stays a
projection concern.

## Reversibility

Low once data exists (migration of authority is costly) — hence proposed, not
imposed, and gated on Human approval.

## Open Questions

- None structural; mechanics deferred to TADR-12.

## Approval Boundary

Requires Human approval of the ownership map. Authorizes no schema, code,
migration, or Programmer handoff.
