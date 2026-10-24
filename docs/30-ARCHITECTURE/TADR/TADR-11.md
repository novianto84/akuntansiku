# TADR-11 — File / Photo Architecture

```text
Status: APPROVED
Human Approval: APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21)
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
```

## Problem / Architectural Question

How are evidence files stored, owned, reviewed, published, retained, and served —
covering object storage vs. filesystem, metadata, ownership, publication and
review state, retention, replacement, immutability, access control,
customer-safe serving, and QR access — without ever exposing internal paths?

## Authoritative Inputs

- CD-11 §16 (mandatory vs. conditional evidence; condition-driven; N/A + Reason) —
  SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF).
- CD-11 §25 (approved photos; reviewer curation) — SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF).

## Approved Direction

APPROVED — HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL (2026-09-21): content-addressed internal store (storage
class left to implementation planning); per-file metadata (owner context,
evidence class, review state, publication state, immutability flag); originals
immutable post-completion with replacement-as-new-file linkage; mediated,
scope-bound serving for all external access (customer-safe subset + unit-bound
QR serving). Internal file paths are never exposed.

## Alternatives Considered

- **Direct filesystem paths served to clients:** simplest; rejected — exposure and
  scope-bypass risk.
- **Public bucket object per file as default:** easy sharing; rejected as default —
  publication must be reviewer-gated, not addressable by default.

## Trade-offs

Mediated serving adds a serving layer but makes scope enforcement (customer-safe,
unit-bound) structural rather than conventional.

## Business Rules Preserved

Condition-driven evidence requiredness; N/A + open-reason with reviewer validation
(principle; exact taxonomy deferred); reviewer-curated publication; QR unit scope.

## Dependencies / Deferred Decisions

Customer publication **business expectation resolved — HBA D-01A = RETAIN**. The approved file/photo
serving direction remains partly dependent on **architecture/mechanism** work (publication-state/serving
mechanics, including preserving the previously presented historical record). Business Access Model
(LOCKED): mediated serving enforces the same
two tiers — unit-scope serving for any authenticated user versus company-scope
serving for a verified PIC; no price-bearing or internal content is servable
through either tier. N/A taxonomy/examples: DEFERRED (generic pattern only).

## Security Impact

File access is a first-order external-attack surface: unguessable internal
references, scope-bound mediation, approved-only customer serving, QR unit
binding, abuse monitoring hooks (see TADR-18).

## Audit / Traceability Impact

File lifecycle (capture → review → approve → publish/replace) is trail-linked to
its owning WO/execution context; originals preserved as evidence.

## Operational Impact

Derivative processing (e.g. thumbnails) runs as background jobs (TADR-15) that
never mutate originals; retention windows deferred to implementation planning.

## Reversibility

Medium: store choice and URL shapes are costly to change after external exposure.

## Open Questions

- Storage class selection (implementation planning).
- Retention windows and derivative lifecycle (possible future business input).

## Approval Boundary

Requires Human approval of the mediated-serving direction. Authorizes no storage
provisioning, code, schema, migration, or Programmer handoff.
