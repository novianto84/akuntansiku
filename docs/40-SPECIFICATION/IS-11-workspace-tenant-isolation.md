# IS-11 — Workspace & Tenant Isolation

```text
Document ID: IS-11
Title: Workspace & Tenant Isolation
Version: 1.1 (controlled correction v1.0→v1.1: F-01 wording + F-02 citation; no content revision)
Status: APPROVED / CANONICAL — BUSINESS AUTHORITY APPROVAL
Approval: Business Authority approval of reviewed v1.1 content following PASS — READY FOR BUSINESS AUTHORITY APPROVAL regression verdict. Status/governance only; substantive content unchanged.
Scope: Workspace/tenant isolation; company/workspace scoping; guard requirements;
  read/write scoping; cross-workspace prohibition; negative paths; invariants; audit.
Authority: AI Manager / Lead Architect (specification author). Business Authority owns all rules.
Sources: AB-01 v1.0 (APPROVED/CANONICAL); TA-01 v1.1; CD-07 + CD-08 (LOCKED);
  TADR-05 + TADR-06 (APPROVED); Decision Register; Architecture Lock; IS-00 governance.
ID basis: BA FINAL DECISION assigning IS-11 (resolves IS-01 numbering collision;
  IS-01 remains Domain & Data Model).
Implementation: NO schema/SQL/migration/API/UI/code/TASK-001. Technology-neutral.
```

> Required behavior and guarantees — never implementation mechanisms. Business requirement →
> technical requirement → implementation mechanism are kept distinct; this document covers the
> first two layers only.

---

## 1. Purpose

Specify the isolation guarantees that let one platform and one database serve multiple
workspaces (e.g. PKP vs Non-PKP) and multiple companies without data or operations leaking
across boundaries, while preserving explicitly shared masters and intelligence.

## 2. Scope

In scope: workspace/tenant model; company scoping; read/write scoping; guard requirements;
cross-workspace prohibition; negative paths; invariants; failure expectations; isolation audit;
acceptance criteria. Out of scope: portal mechanics (IS-06 territory); general permission-matrix
content (deferred business content); storage/auth products; topology.

## 3. Canonical Sources

CD-07 Q1–Q18 (LOCKED); CD-08 ownership model (LOCKED); TADR-05 (one-DB strategy, app-enforced
scoping primary); TADR-06 (per-path guards + authz composition + negative tests); AB-01 §§C–D
(single writer, directional dependencies); TA-01 §§8–9,14,25–26 (layers, modules, scoping
integrity); Decision Register / Architecture Lock (status index; implementation not authorized).

## 4. Terminology

**Workspace / Business Context** — tenant boundary owning transactions, documents, numbering,
templates, approvals, reporting, stock (CD-07 Q2). **Shared master/intelligence** — identity or
reference data usable across workspaces (CD-07 Q4–Q9; CD-08). **Workspace-owned record** —
transactional data belonging to exactly one workspace (CD-08). **Active workspace** — the
workspace context selected via login before transacting (CD-07 Q13). **Usage marker** — record
that a shared master is used by a workspace (CD-08 Q4; shape OPEN).

## 5. Actors and Authority Boundaries

Internal roles per canonical role structure (detail matrix deferred business content): actors
operate within the active workspace; cross-workspace operation requires no silent elevation path
(none exists). External (Verified PIC) access is company-scoped per locked access decisions and
never crosses workspace transaction boundaries; portal mechanics deferred. Identity vs
authentication vs authorization vs scope vs role authority keep canonical meanings (no redefinition).

## 6. Workspace / Tenant Model

One platform, one database; workspace chosen via login before transactions (CD-07 Q1, Q13).
PKP and Non-PKP are distinct workspaces (Q3). HARD CONSTRAINT: no transaction automatically
moves or mixes across workspaces (Q17). No journal/GL/ledger in scope (Q18). Per-workspace:
transactions, documents, numbering sequences, templates, approvals, pipeline stages/activities,
operational reporting (Q2, Q10–Q12, Q15–Q16).

## 7. Company Scoping Boundary

Company/Customer master is shared without duplicate identity; customer↔workspace usage is a
recorded marker (CD-07 Q4; CD-08 Q4). Contact/PIC shared with workspace-specific context deferred
open (CD-08 Q5). Rules: (a) shared identity never implies cross-workspace transaction visibility;
(b) usage marker shape is implementation design (OPEN); (c) no fake Company to satisfy scoping
(BD-G01-G02: Company relationship NULL until verified; no Company fabricated for any reason).

## 8. Cross-Tenant Prohibition

The following are prohibited as required behaviors (CD-07 Q17; TADR-06): automatic movement or
mixing of any transaction across workspaces; reading or writing another workspace's owned records
through any path (direct, related-object traversal, alternate reference, numbering/sequence
reuse, report aggregation); combined global transaction reporting (Q16). Shared masters and
intelligence are the only cross-workspace-visible data, exactly as allowlisted (§§9–10).

## 9. Read Scoping Requirements

Every read resolves scope before returning data: workspace-owned records default to active-workspace
scope; shared records resolve per allowlist (masters, offers, acquisition references, price history
+ provenance); customer↔workspace usage constrains company-context reads. No read path may omit
scope resolution. (TADR-06 primary enforcement; TADR-05 app-enforced scoping.)

## 10. Write Scoping Requirements

Every write carries and validates its workspace (or shared-master governance path): workspace-owned
writes bind to the active workspace and reject foreign scope; master creation from any workspace is
immediately shared (CD-08 Q1) via suggest + admin approval for modifications (Q2) with global
effect once approved (Q3); used masters deactivate/archive, never hard-delete (Q11–Q13); no
automatic duplicate matching (Q14); merge only via proven business process (Q15; technicals OPEN);
no private vendor notes (Q17).

## 11. Authorization-Boundary Guard Requirements

A workspace-scope guard stands on every read and write path, composed with authorization
(TADR-06 + TADR-14): identity → role authority → workspace/company scope → business-role authority.
Guards reject before side effects; rejections are audited. No guard may be bypassed for convenience;
no silent elevation; no cross-company grant (locked access decisions).

## 12. Negative-Path Requirements

The following attempts MUST be rejected (as security/authorization behavior, technology-neutral):
(a) reading another workspace's owned data; (b) reading another company's data outside permitted
scope; (c) writing/updating outside permitted scope; (d) presenting an identifier from another scope
(ID manipulation); (e) reaching foreign data via related objects or alternate references; (f) sequence/
number reuse across workspaces; (g) requesting combined cross-workspace transaction reports;
(h) moving a transaction across workspaces. Rejection is explicit (never silent wrong-scope success).

## 13. Isolation Invariants

I-1 active-workspace scope is the default for all transactional reads/writes. I-2 only allowlisted
shared data crosses workspaces. I-3 no automatic cross-workspace movement. I-4 no combined global
transaction reporting. I-5 numbering sequences are workspace-independent. I-6 master changes take
global effect only via suggest + admin approval. I-7 used masters are never hard-deleted. I-8 no
automatic duplicate matching or merge. I-9 scope guards precede side effects on every path.
I-10 rejections are audited. I-11 shared visibility never implies transaction visibility.
I-12 CD-06 Q8 admin visibility overlay is a reserved future path at its own gate; creates no IS-11 rule
and changes nothing until decided.

## 14. Failure / Rejection Expectations

Guard failure → explicit rejection referencing the governing rule + audit of the attempt; never
partial writes, never wrong-scope success, never silent downgrade to another scope. Technical
(persistence/downstream) failure → no state fabrication, no guard bypass on retry (TA-01 §21
pattern, cited not redesigned).

## 15. Audit Implications

Isolation-relevant events (scope resolutions, rejections, master suggest/approve/global-effect,
usage-marker records, deactivation/archive, merge actions) follow the append-only pattern (actor,
server timestamp, object, scope, reason, before/after). No new audit subsystem.

## 16. Dependency Boundaries

Upstream: AB-01, TA-01, CD-07/08, TADR-05/06, locked access decisions. Downstream consumers: every
workspace-scoped specification and implementation plan. IS-11 constrains but does not design them.
Portal/permission-matrix content remain with their owning gates.

## 17. Acceptance Criteria

AC-1 every read/write path states its scope rule. AC-2 negative paths (a)–(h) each have an explicit
rejection expectation. AC-3 shared-vs-owned classification covers every data class in §9–10 with a
canonical citation. AC-4 no mechanism (product/framework/auth tech/topology) is prescribed. AC-5
invariants I-1…I-12 are each traceable. AC-6 OPEN/DEFERRED list is explicit. AC-7 IS-01 collision
absent (this artifact is IS-11; IS-01 untouched).

## 18. Traceability

§6→CD-07 Q1–Q3,Q13,Q17–Q18; §7→CD-07 Q4/CD-08 Q4–Q5 + BD-G01-G02 (no-fake-Company rule); §§8–9→CD-07 Q14,Q16–Q17/TADR-06; §10→CD-08
Q1–Q3,Q6–Q8,Q11–Q15,Q17; §11→TADR-06+TADR-14/AB-01 §D; §12→CD-07 Q16–Q17/TADR-06; §13→as cited per
invariant; §15→TADR-08 pattern; actors→AB-01/TA-01 (no new roles).

## 19. OPEN / DEFERRED Items

OPEN (carried, unsolved): numbering format per workspace; workspace-selection mechanism;
customer↔workspace relation shape; contact workspace-specific context; suggest/approval matrix
detail; merge/deactivation technicals; CD-06 Q8 visibility overlay (own gate). DEFERRED:
permission-matrix content; portal mechanics; deployment context. None blocks IS-11 (all are
content/mechanism details around locked structures).

## 20. Self-Audit / Completeness Check

Identity: IS-11 unique ✅ · IS-01 intact ✅ · no collision ✅. Scope: isolation/read/write/negative
paths explicit ✅ · no foreign domain absorbed ✅. Architecture: AB-01/TA-01/single-writer
preserved ✅ · no new authority ✅ · technology-neutral ✅. Governance: IS-00 registry updated
(separate edit) ✅ · canonical artifacts untouched ✅ · prep numbering stays historical ✅ ·
traceability complete ✅. Prohibited: no schema/SQL/migration/API/UI/code/TASK-001/IS-02+ ✅.

---

*End of IS-11 v1.0 DRAFT.*
