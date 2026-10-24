# TADR-03 — Component Subtype Structure

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

How should Unit components be structured so that the strict operational subtypes
ENGINE, GENERATOR, BOX_CHASIS each have subtype-specific technical structure,
future registry types stay spec-less, and no generic shortcut is created?

## Authoritative Inputs

- CD-11 §4 (strict operational subtype architecture; other categories
  registry/future) — SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF).
- Finalization task constraint: do not create a generic JSON/EAV/
  component-specs shortcut.

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): subtype-specific structures per
ENGINE / GENERATOR / BOX_CHASIS sharing a Unit-rooted base (identity, parent
link, lifecycle state). Registry/future types (PUMP, ATS, SYNCHRONOUS_PANEL,
TRANSFORMER) receive no operational specification architecture until field or
business requirements exist. All subtype shapes are placeholders — no field,
threshold, or specification is invented.

## Alternatives Considered

- **Generic component record (JSON/EAV-style):** flexible; explicitly excluded by
  the governing constraint (documented, not pursued).
- **Single structure with optional fields:** one structure to maintain; rejected —
  it invites cross-subtype field leakage and weakens subtype enforcement.

## Trade-offs

Three maintained structures cost more modeling effort but enforce the business
subtype boundary; placeholders avoid inventing specs at the cost of leaving
implementation planning with open field design.

## Business Rules Preserved

Strict subtype architecture; Unit as parent asset; replacement record requirements
(old/new/date/reason/relationship) attach to the subtype structures, not to a
generic bag.

## Dependencies / Deferred Decisions

Subtype field/business requirements: UNRESOLVED gate (non-blocking; placeholders
suffice for finalization).

## Security Impact

Subtype structures carry no separate access semantics; Unit-rooted scoping applies.

## Audit / Traceability Impact

Component replacement history references specific subtype structures, keeping
replacement traceability exact.

## Operational Impact

None decided; placeholder shapes impose no runtime cost.

## Reversibility

Medium: structure shapes are cheap to revise before implementation.

## Open Questions

- Which subtype fields (if any) are needed for the first implementation slice —
  requires field/business requirements (Human gate).

## Approval Boundary

Requires Human approval of the subtype-specific direction. Authorizes no schema,
code, migration, or Programmer handoff.
