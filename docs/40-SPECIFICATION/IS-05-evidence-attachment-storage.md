# IS-05 — Evidence, Attachment & Storage Specification

```text
Document ID: IS-05
Title: Evidence, Attachment & Storage Specification
Version: 1.1 (controlled correction v1.0→v1.1: F-01 DERIVED markings; no content revision)
Status: LOCKED / CANONICAL — BUSINESS AUTHORITY APPROVAL (targeted regression: F-01 RESOLVED; MUST/SHOULD FIX 0; UNSOURCED 0)
Lock record: settled normative content authoritative as reviewed; OPEN/DEFERRED items remain unresolved.
Scope: Evidence/attachment concepts, objects, lifecycle, categories (locked floor),
  visibility semantics, Unit/WO/Visit/Report relationships, storage abstraction,
  locked retention rules, audit interface (by reference), IS-06 serving boundary.
Authority: AI Manager / Lead Architect. Business Authority owns all rules.
Sources: CD-11 §17 (CD11-014/016); IS-01 E-31; IS-02 §9 + decomposition §13;
  AB-01; TA-01 v1.1 §§13,18; IS-03 scopes (consumed); IS-11; TADR-11; BD-WORKTYPE-001 §4 R4.
ID basis: BA authorization for IS-05 at docs/40-SPECIFICATION/IS-05-evidence-attachment-storage.md.
Implementation: NO vendor/tech/bucket/schema/code/TASK-001. Technology-neutral.
```

> IS-05 owns evidence definitions. IS-04/IS-07 reference them; nothing here redefines audit
> events (IS-07) or contracts (IS-04). Beyond-floor taxonomy stays OPEN (OQ-05).

---

## 1. Scope

What counts as evidence, how artifacts live (capture → review → eligibility → retention), how
they attach across the service chain, who may see them where, and what storage must guarantee
in the abstract. Excludes: serving/delivery mechanics (IS-06); taxonomy beyond the locked floor
(OPEN); storage products/tech; permission-matrix content.

## 2. Terminology

**Artifact** (photo/file + metadata) · **photo_type** (contextual classification only, never
visibility) · **approval_state** (reviewer workflow) · **publication state** (policy + curation
outcome) · **eligible evidence** (approved + policy-passing subset usable in Report/projection) ·
**opt-out** (`No Evidence` + mandatory reason where permitted). Three state dimensions are
technically separate (TA-01 §13).

## 3. Ownership

Evidence is collected at the **Visit** (collection point) under WO ownership; curation/approval
owned by Manager/Admin reviewers; retention governed by the single-retention rule. No competing
owner; no technician-owned visibility.

## 4. Object Relationships

Artifact → exactly one Visit (collection); referenced by Report eligible subset (never copied as
authority); traceable to WO and Unit through the Visit chain. Replaced-component/damage/test
artifacts link to their subject records (component replacement, test-run) by reference
(DERIVED from CD-11 §15 replacement records + §17 conditional categories; structural
reference only, no new rule).

## 5. Lifecycle

Capture (event-driven at execution) → reviewer approval workflow → eligibility determination
(photo_type + approval_state + policy_version) → Report/projection surfacing (eligible only) →
retention under the single rule. Originals immutable; correction via new capture + supersession
linkage (DERIVED from no-in-place-overwrite of completed records + correction-as-controlling-data;
no silent replacement). Non-eligible artifacts stay stored, internally visible per permission.

## 6. Categories Within Locked Scope

Mandatory: nameplate, hour meter, before, after. Conditional: during, replaced component, damage,
test result (driven by actual events/conditions, never free choice). NOT globally mandatory Phase 1:
on CHECKED scope the field appears but upload is optional with opt-out + mandatory reason
(CD-11 §17). Same rules govern Added-scope artifacts. Beyond-floor categories: OPEN (OQ-05).

## 7. Visibility / Access Boundaries

Technician never selects visibility. Reviewer curation + policy determine eligibility; customer-safe
surfacing additionally gated (IS-03 scopes + allowlist; priceless; IS-06 mechanics excluded).
Internal-only artifacts never cross planes. Q8 overlay values remain OPEN at their own gate.

## 8. Unit / WO / Visit / Report Relationships

Collection at Visit granularity; consolidation references (never duplicates) into the per-WO Report;
Unit-level history aggregates eligible artifacts per Unit through the WO chain (DERIVED from
CD-11 §20 Unit View; aggregation only, no new store). No per-asset
duplicate stores.

## 9. Storage Abstraction

Storage must guarantee: durability (DERIVED from single-retention rule + history-preservation
duties; property only, no technology); Visit association; immutable originals with supersession
linkage; single retention rule application; permission-scoped reads; audit of lifecycle transitions
(events defined by IS-07). No vendor, product, bucket, filesystem, CDN, MIME-implementation, or
topology decisions.

## 10. Retention Requirements (Where Locked)

One retention rule for all evidence (no Before/During/After lifecycles). Retention windows remain
planning detail (OPEN). Deletion/purge mechanics: none locked; nothing inferred.

## 11. Audit Interface (IS-07 owned — reference only)

Capture, opt-out (+reason), approval transitions, eligibility changes, supersession linkage, and
retention actions emit IS-07 event families. Interface dependency recorded; definitions live in
IS-07. No competing event model here.

## 12. Publication / Serving Boundary with IS-06

IS-05 ends at eligibility + retention. Serving, delivery, freshness, snapshot-vs-live, and
no-download mechanics belong to IS-06. The customer publication **business expectation is RESOLVED —
HBA D-01A = RETAIN**; the serving/freshness/snapshot **mechanism** remains architecture. No serving
behavior specified here.

## 13. Open / Deferred Section

OPEN: beyond-floor categories (OQ-05); retention windows; Q8 values. DEFERRED: serving/delivery/
freshness/snapshot mechanics (IS-06); storage products/tech; provider mechanics; deployment.

## 14. Traceability

§§2–6 → CD-11 §17 + IS-01 E-31 + BD-WORKTYPE-001 §4 R4. §5 correction linkage DERIVED (stated
parents). §7 → CD-11 §§17,21 + IS-03 scopes. §§9–10 → single-retention rule (LOCKED) + windows
(OPEN). §§11–12 → IS-07 / IS-06 ownership. Classification: LOCKED/DERIVED except §13 items.

## 15. Acceptance Criteria

AC-1 three state dimensions separated. AC-2 floor categories + opt-out rules exact. AC-3 no
technician visibility choice. AC-4 originals immutable with supersession linkage. AC-5 no
vendor/tech/prescribed. AC-6 OPEN items marked. AC-7 zero UNSOURCED. AC-8 joint checkpoint passed.

## 16. Self-Audit

Authorized path ✅ · DRAFT ✅ · owns evidence only (no audit/contract redefinition) ✅ · no OPEN
resolved ✅ · no vendor/tech ✅ · no TASK-001 ✅ · traceability complete ✅ · neutral ✅ ·
single-file scope ✅.

---

*End of IS-05 v1.0 DRAFT.*
