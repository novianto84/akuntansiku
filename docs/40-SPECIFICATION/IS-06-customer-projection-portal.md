# IS-06 — Customer Projection & Portal

```text
Document ID: IS-06
Title: Customer Projection & Portal
Version: v1.3 (additive v1.2→v1.3: HBA-DECISIONS-16 manual intake replaces automatic elevation for Unit Portal; HBA-DECISIONS-17 short permanent QR code screen-only; panel queue approve/reply/ignore. No new business rule beyond those locked records.)
Status: LOCKED / CANONICAL — BUSINESS AUTHORITY APPROVAL 2026-10-12 (HBA chat: kunci IS-06; v1.3 additive HBA-DECISIONS-16/17/18; settled v1.2 content retained, automatic elevation superseded by manual intake)
Authority: AI Manager / Lead Architect (specification author); Business Authority owns business rules
Scope: Customer-facing read behavior, eligibility, scope, visibility, and projection boundaries
Implementation: NO schema, API endpoints, code, UI implementation, storage design, serving infrastructure,
  framework, provider, migration, deployment, or Programmer TASK
Readiness: LOCKED — HBA D-01A RESOLVED; residual open items are architecture/mechanism and out-of-scope gates
```

> This specification defines **what customer-facing reads may represent and under which scope and
> eligibility conditions**. It does not define how publication, projection, authentication, or serving
> is implemented. Canonical business and approved architecture sources remain authoritative.

## 1. Document Control

| Field | Value |
|---|---|
| Document | IS-06 — Customer Projection & Portal |
| Version / status | v1.3 / LOCKED / CANONICAL — BUSINESS AUTHORITY APPROVAL 2026-10-12 |
| Governance | IS-00 — IS Specification Governance & Master Plan |
| Specification owner | AI Manager / Lead Architect |
| Business-rule authority | Human / Business Authority |
| Primary inputs | IS-01, IS-02, IS-03 v1.4, IS-04 v1.1, IS-05 v1.1, IS-07 v1.1, IS-11 v1.1 |
| Architecture inputs | AB-01 v1.0; TA-01 v1.1; TADR-07, TADR-11, TADR-12, TADR-13, TADR-14, TADR-16 |
| Business inputs | CD-11 §§17–22; BD-SR-004; locked human identity, QR, and Business Access Model decisions indexed in `DECISION_REGISTER.md` |
| Implementation authority | None; implementation is not authorized by this document |
| Amendment log | 2026-09-30 — controlled reconciliation under HBA authorization `AUTHORIZE MILESTONE 6 DOCUMENTATION RECONCILIATION`: materialized HBA decision **D-01A = RETAIN** (previously presented customer-facing content remains available as the historical record of what was presented; current authoritative condition remains distinguishable); recorded **OQ-02** publication permission as already canonical; restated freshness as a **semantic requirement (D-01B)** with no numeric SLA; separated business resolution from architecture/mechanism work in §28. No new business rule, no `PUBLISH` state/action, no new permission model, no new actor, no numeric freshness value. **2026-10-11 — additive materialization of HBA-DECISIONS-13 (2026-10-08):** three locked access tiers (Internal CRM, Customer Portal, Unit Portal) stated explicitly; Unit Portal described only as recorded there (one Unit from QR scan, read-only, no price; Google-only login; after login, name + company + phone number are requested; email is taken automatically from Google; automatic elevation to Customer Portal when that email is registered as PIC). Prior two-tier wording and L-28 are marked **SUPERSEDED by HBA-DECISIONS-13** for Unit Portal and are not deleted. No business rule beyond that locked record. **2026-10-12 — additive v1.2→v1.3 (HBA-DECISIONS-16/17/18):** automatic elevation REPLACED by manual intake (name + company-text free text + phone, email auto; PENDING queue; manual link only, no email-match elevation); QR fixed as short permanent code, screen-only rollout; dashboard panel queue (approve/link, reply in-CRM, ignore). Prior automatic-elevation wording retained above as superseded history, not deleted. |

### Classification convention

Every substantive requirement is classified in §28 as:

- **LOCKED-SUPPORTED** — directly stated by a canonical business decision or approved architecture direction.
- **DERIVED-SUPPORTED** — follows directly from cited canonical requirements without creating or changing a rule.
- **OPEN/DEFERRED** — remains unresolved by its owning business/architecture gate and is not decided here.

There are **zero UNSOURCED** requirements in this locked document. Requirement IDs `L-xx`, `D-xx`, and `O-xx`
identify the classification and source rows in §28.

## 2. Purpose

IS-06 specifies the customer-safe, read-only projection of internal service information: what is eligible
to appear, which identity/scope may see it, how company portal and Unit QR views differ, how the
projection relates to authoritative operational records, and which customer-facing behaviors remain
open. It consumes domain ownership, lifecycle, access, evidence, audit, and workspace rules; it does not
redefine them. [L-01–L-28]

## 3. Scope

In scope:

- Company-scoped verified-PIC portal reads and Unit-scoped controlled QR reads.
- Customer-safe content allowlist and exclusions.
- Conceptual eligibility conditions for service execution and evidence.
- Read-only representation of WO / Visit / Report and customer-safe service history.
- Negative authorization/scope paths, correction interaction, audit and API boundaries.
- Explicit publication/serving **mechanism** (architecture), the resolved business expectation (**HBA D-01A = RETAIN**), and the semantic freshness requirement (**D-01B**), plus related OPEN/DEFERRED items.

These requirements use canonical identity and authorization semantics. They do not establish a new
customer authorization model. [L-04–L-10, L-16, L-26–L-28]

## 4. Non-Scope

IS-06 does not own or redefine Company, Contact/PIC, Unit, WO, JOB, Visit, Report, evidence objects,
operational states, internal history, correction/history, identity verification, workspace isolation,
or audit semantics. It specifies no implementation of QR tokens/URLs, authentication or authorization
libraries, APIs/endpoints, databases/queries, caches, snapshots, queues, storage, providers, frameworks,
or deployment. It creates no customer-specific lifecycle, second Report, correction workflow, publication
approval layer, or independent source of historical truth. [L-01–L-03, L-17–L-21, L-24–L-26]

## 5. Source & Traceability Rules

1. Follow IS-00 §3 precedence: locked business sources and approved architecture outrank this draft;
   canonical repository documents outrank chat reconstruction.
2. Consume IS-03 for identity, authorization and customer scope; IS-04 for service/API contract ownership;
   IS-05 for evidence eligibility and serving boundary; IS-07 for audit/history/correction semantics; and
   IS-11 for workspace isolation. None is redefined here.
3. CD-11 §§18, 20–22 and CD11-020/021 are the customer-safe, Report, history, QR and no-price business
   basis. BD-SR-004 §3 separately fixes zero external/customer exposure for SR.
4. TADR-12 provides the projection direction and conjunction; TADR-11 provides the evidence-serving
   direction; TADR-13/14/16 provide the identity/scope/QR boundaries. Their approved direction does not
   resolve deferred publication or serving mechanics.
5. Every normative requirement has a source/classification row in §28. A missing source is not filled
   by convention, industry practice, or inference; it remains OPEN or is reported as a source gap.

## 6. Customer Access Model

External access preserves the canonical chain **Google Identity → Contact/PIC → Verified PIC Link →
Company**. Google-only sign-up/sign-in authenticates identity; it does not itself create PIC status,
Company membership, authorization, or Company scope. A Verified PIC Link is per-company and may be
VERIFIED, PENDING, or REVOKED; Company scope follows a verified link only for its linked Company.
Revocation ends that link's access while preserving Contact and service history. [L-04, L-05]

**SUPERSEDED by HBA-DECISIONS-13 (2026-10-08) — retained, not deleted.** The prior wording of this section stated that the existing two external scopes remain distinct and that "No third external tier is introduced." That two-tier statement, and IS-06 L-28 as previously written, are superseded for this scope. They are not removed.

**Locked three access tiers (HBA-DECISIONS-13).** Exactly three access tiers are locked:

1. **Internal CRM** — the internal operational plane. It is not an external customer tier.
2. **Customer Portal** — company-scoped external access through a Verified PIC Link (prior COMPANY_SCOPE).
3. **Unit Portal** — one Unit resulting from a QR scan; read-only; no price. Login is Google-only. After login, the portal requests manual name + manual company-text (free text, never a picker) + phone number; email is taken automatically from Google (HBA-DECISIONS-16). The intake is a claim, never a grant: it lands PENDING in the dashboard queue, and until manual link by the configured link authority the subject holds UNIT_SCOPE only. No automatic elevation by email match. Contact and architecture remain attached to the CRM backend. The prior two-tier model is SUPERSEDED for this scope.

The two external scopes that remain inside those tiers stay distinct:

- **UNIT_SCOPE (Unit Portal):** an authenticated user in a QR context may receive only the resolved Unit's permitted customer-safe data and history. The view is read-only and contains no price. QR is not Company access. Google-only login does not itself create Customer Portal access. After login, manual name + manual company-text (free text, no picker/autofill) + phone number are requested; email comes automatically from Google. The intake lands PENDING in the dashboard panel queue (approve/link, reply asking for more proof recorded in-CRM only, ignore); until manual link the subject holds this UNIT_SCOPE only — no automatic elevation by email match (HBA-DECISIONS-16/18).
- **COMPANY_SCOPE (Customer Portal):** a Verified PIC may receive the customer-safe company-scoped view for the linked Company, subject to applicable workspace boundaries. A Google identity, QR possession, Company-name knowledge, or prior Unit view does not confer this scope — Company scope follows only a manual link + approval by the configured link authority (HBA-DECISIONS-16).

No access tier beyond the three locked by HBA-DECISIONS-13 is introduced. [L-04, L-07, L-09, L-28, D-01, D-04; HBA-DECISIONS-13]

## 7. Customer Projection Architecture Boundary

### Internal Canonical Plane

The internal operational plane remains authoritative for Company, Contact/PIC, Unit, WO, JOB, Visit,
Report, SR, evidence objects, operational state, correction/history, and internal information. Their
respective domain specifications retain ownership and write authority. [L-01, L-02]

### Customer Projection Plane

The customer-facing portal and QR experience is a **derived, customer-safe, read-only projection** of
eligible authoritative content. It is not a second source of truth, writer, lifecycle owner, replacement
for internal records, or independent correction mechanism. Projected content remains traceable to its
authoritative source; reads do not change that source. [L-01–L-03]

The projection is a filtered customer view, not a copy of all internal history. Existence in the internal
plane alone never makes content customer-visible. [L-11–L-16, D-03]

## 8. Company-Scoped Portal

The portal is a Company-scoped read experience. A Verified PIC may see only customer-safe information
authorized for that PIC's verified Company scope and permitted workspace context. It must not expose
global Company lists, other customers or companies, internal operational directories, or records outside
the authorized scope. [L-04, L-06, L-10, D-02, D-04, D-06]

The Company's Unit/service history is an aggregation of eligible records tied to their Units, not a
cross-company or cross-workspace transaction view. PIC display, if present, remains subject to the
canonical customer-safe visibility boundary. [L-09, L-10, D-02, D-04]

The portal must not expose acquisition price or other prices in any form; vendor intelligence; internal
notes; correction, cancellation, or administrative reasons; or other internal/commercial information
excluded by CD-11 §21. [L-13, L-14]

## 9. Unit QR Customer View

QR remains permanent and Unit-scoped. The same QR associated with a Unit, Invoice, or Surat Jalan
resolves to that same Unit. Resolution is Unit-rooted; the QR view cannot browse to another Unit or
Company. Per HBA-DECISIONS-17 the code is a short random code, one per Unit, purely permanent (no
expiry/rotation), leak-accepted with uncontrolled reprint, rollout screen-only (print anytime).
Token format detail beyond that, URL structure, and serving infrastructure are not specified here. [L-07, L-08, L-09, O-01]

Customer access follows CONTROLLED ACCESS: scan → Google sign-up/sign-in → access check → permitted
customer data. No anonymous customer data or pre-login preview is available. An authenticated non-PIC
in QR context receives UNIT_SCOPE only. If the user has a Verified PIC Link to the Unit's Company, the
existing Business Access Model permits COMPANY_SCOPE through that link; the QR itself grants no wider
scope. [L-04, L-05, L-07, D-01]

The QR view may present only the authorized, eligible customer-safe history of the resolved Unit. It is
not a Unit directory or cross-unit navigation mechanism. [L-07, L-09, L-11, D-02, D-03]

## 10. Customer-Safe Data Allowlist

The allowlist is limited to the customer-safe content identified by CD-11 §21. Where otherwise eligible,
it may include:

| Allowlisted content | Condition |
|---|---|
| Date | Customer-safe projection eligibility applies |
| Technician | Customer-safe projection eligibility applies |
| Summary / work performed | Customer-safe projection eligibility applies |
| Photos | Approved and eligible under IS-05; reviewer curation applies |
| Replaced component | Customer-safe projection eligibility applies |
| Material quantity | Only where agreed/appropriate; quantity only |
| Recommendation | Customer-safe projection eligibility applies |

[L-11, L-12, L-21]

This is a bounded allowlist. A field's presence in a Report, Visit, Unit history, or internal record does
not add it to the customer allowlist. No extra customer-facing history fields are introduced by IS-06.
[L-11, D-03]

## 11. WO / Visit / Report Projection

Customer-facing representation does not change internal lifecycle ownership:

- **WO** remains the operational service/lifecycle authority.
- **Visit** remains the authority for visit execution facts.
- **Report** remains the per-WO report domain and consolidation of Visit data; it is not a second Visit
  record or an independent customer report.
- Customer projection is read-only and does not create or modify WO, Visit, or Report state.

[L-17–L-20]

Internal lifecycle and customer representation are distinct. The customer representation may show only
allowlisted, eligible content from a Report that meets the canonical eligibility boundary. It must not
expose work-in-progress or non-final execution content. [L-16, L-17, L-19]

Report remains customer-visible only according to the canonical eligibility boundary: Report FINAL only
when WO is CLOSED; Visit COMPLETED, outcome completion, WAITING APPROVAL, or CORRECTION_REQUIRED does
not make Report FINAL. IS-06 creates no customer-specific Report lifecycle or second Report. [L-17,
L-19]

## 12. Unit / Service History Projection

Customer-safe history is a filtered view over the one authoritative operational history. Through Unit
QR it remains Unit-scoped; through verified portal access it remains Company-scoped, with each included
service record tied to its own Unit and subject to workspace isolation. [L-01, L-07, L-09, L-10, D-02,
D-03, D-04]

History contains only the eligible allowlisted customer-safe content in §10. Internal history does not
become customer history merely because it exists. History reflects authoritative domain/projection
outcomes after correction or reopen, without becoming a separate historical source of truth. [L-01,
L-11, L-16, L-25, D-03, D-05]

Content previously presented to a customer remains available to that customer as the **historical record
of what was previously presented** (**HBA D-01A = RETAIN**). The current authoritative condition remains
distinguishable from that historical customer-facing record. The serving/storage mechanism (snapshot
materialization, refresh, cache, replication, drift monitoring) is an architecture decision and is not
settled here. [O-05]

## 13. Evidence / Photo Projection

IS-05 owns evidence definitions, evidence objects, approval state, retention, and eligibility. IS-06
consumes only the evidence subset IS-05 determines customer-visible under the canonical eligibility
model, including evidence type, approval state, applicable policy, reviewer curation, and
customer-visible eligibility. [L-21]

`photo_type` is contextual classification, not the customer-visibility authority. Technician selection
does not determine visibility. Non-eligible evidence may remain stored and internally visible under
internal permissions, but is not surfaced to customers. IS-06 specifies consumption/serving behavior
only and does not redefine evidence ownership or review. [L-21]

## 14. Projection Eligibility Gate

The conceptual customer projection gate is the applicable conjunction of:

1. WO is **CLOSED**.
2. Its Report is **FINAL**.
3. The requester satisfies the identity/access requirement for the requested scope.
4. The requested Company or Unit is within that identity's authorized scope.
5. Applicable policy and reviewer-curation requirements are satisfied.
6. Each item of content, including evidence, is customer-visible eligible.

For **COMPANY_SCOPE**, the identity requirement is a Verified PIC Link for the target Company. For
**UNIT_SCOPE** via QR, it is Google-authenticated access in the one resolved Unit context; the applicable
scope does not become Company scope absent the Verified PIC Link. Both paths remain subject to CLOSED,
FINAL, applicable policy, content eligibility, and their correct scope. [L-04, L-05, L-07, L-09, L-15,
L-16, D-01]

This gate consumes existing lifecycle, identity, scope, policy, and eligibility decisions. It is not a
new approval layer, publication authority, or permission model. [L-15, L-16, O-01]

## 15. Negative Paths / Denials

IS-03 authorization and IS-11 workspace/scope guards remain the semantic authority. The following
customer-facing attempts are denied by those existing rules; IS-06 creates no second authorization
engine or special bypass. Rejection behavior follows the owning specifications. [L-27]

| Attempt | Required customer-facing outcome | Source |
|---|---|---|
| 1. Anonymous access, including preview | Deny all customer data before Google authentication | IS-03 §§4, 9–10; TADR-16; locked QR decision |
| 2. Authenticated but unverified identity | No Company scope; outside QR context, no customer data; in QR context, UNIT_SCOPE may apply to the resolved Unit only | IS-03 §§4, 7, 9; TADR-16 |
| 3. Revoked PIC link | Deny Company access based on that link; revocation does not delete history | IS-03 §§5, 10; TADR-13 |
| 4. Verified PIC requests another Company | Deny; no cross-company grant exists | IS-03 §§5, 7, 10; TADR-13/14 |
| 5. Verified PIC requests another workspace's transaction | Deny foreign workspace-owned data | IS-11 §§8–12; IS-03 §7 |
| 6. Direct access to unauthorized WO | Deny when company/unit/workspace scope or eligibility is not satisfied | IS-03 §§7, 9; IS-11 §§9, 11–12; IS-04 §10 |
| 7. Direct access to unauthorized Unit | Deny unless it is the authorized Company scope or the single QR-resolved Unit | IS-03 §§7, 9–10; TADR-16 |
| 8. Direct access to unauthorized Report | Deny unless source WO, Company/Unit scope, FINAL status, and customer eligibility all pass | IS-03 §9; IS-04 §10; TADR-12 |
| 9. Direct access to unauthorized evidence | Deny unless IS-05 eligibility and applicable customer scope both pass | IS-05 §§5, 7, 12; IS-03 §9; TADR-11 |
| 10. QR attempt to browse beyond its Unit | Deny; QR resolves to exactly one Unit | IS-03 §§7, 10; TADR-16 |
| 11. Attempt to access internal-only information | Deny customer exposure | CD-11 §21; IS-03 §9; IS-05 §7; TADR-12/14 |
| 12. Attempt to expose price or commercial/internal intelligence | Never include it in customer output | CD-11 §21; IS-03 §7, 9; TADR-12/14 |
| 13. Invalid, unavailable, or ineligible customer projection | Do not present it as eligible customer information; use the owning authorization/contract failure behavior | IS-03 §9; IS-04 §§9–10; IS-11 §14 |

The table specifies semantic denial only. It does not prescribe status codes, error payloads, messages,
URL behavior, endpoint structure, or authorization implementation. [L-26, L-27]

## 16. Correction / Reopen Interaction

The customer projection reflects authoritative domain outcomes. It does not create a correction workflow,
edit internal records, create a second Report, or establish an alternate WO. [L-01, L-03, L-19, L-25]

IS-07 rules remain intact: reopen applies only to CLOSED; correction uses numbered cycles with no
canonical maximum; lineage and history are preserved; the same Report remains associated with the WO;
the Report is derived/refreshed from current authoritative Visit data and is FINAL only when the WO is
CLOSED. RE-CREATE is a new WO/Report/history with its canonical `CREATED_FROM` lineage, not an IS-06
correction. [L-19, L-25]

When an authoritative correction/reopen outcome means CLOSED or FINAL no longer holds, that content
does not meet the current projection eligibility conjunction. Content previously presented remains
available as the historical record of what was presented (**HBA D-01A = RETAIN**); the current
authoritative condition remains distinguishable. Refresh/propagation mechanism remains an architecture
decision. [D-05, O-05]

## 17. Audit Interaction

IS-07 owns audit event definitions, event fields, append-only semantics, controlling history, and
correction lineage. IS-06 does not create a second audit system, own audit state, reconstruct domain
state independently, or replace IS-07. Customer access/read or QR scan observations, when required,
follow applicable IS-07 event definitions and the canonical QR traceability boundary; exact event
semantics are not invented here. [L-24]

## 18. API / Contract Boundary

IS-06 states customer-facing functional read requirements only. IS-04 remains the authority for service
responsibilities, read contracts, authorization enforcement hooks, validation, and failure semantics.
IS-06 does not prescribe REST, GraphQL, RPC, endpoint naming, request/response shape, framework,
authentication library, or database query. [L-26]

Customer reads remain non-mutating and scope-/eligibility-gated under the IS-04 contract boundary.
[L-03, L-16, L-26]

## 19. Publication & Serving — Mechanism (Architecture)

**Business expectation RESOLVED — HBA D-01A = RETAIN.** Previously presented customer-facing content
remains available as the historical record of what was presented, and the current authoritative condition
remains distinguishable from that record.

**Serving/storage mechanism remains an architecture decision.** No decision is made here about snapshot
versus live serving, cache architecture, replication, queue, database, serving infrastructure, framework,
provider, refresh mechanism, or publication-state mechanics. Those remain outside IS-06's
technology-neutral behavior specification. **No publication state and no `PUBLISH` action exists.** [O-01]

The customer-visible requirement remains constrained by the allowlist, reviewer-curation boundary,
eligibility gate, scope rules, no-price rule, and canonical no-download requirement. IS-06 does not create
a new publication authority. [L-11–L-16, L-22, O-01, O-03]

## 20. Freshness — Semantic Requirement (D-01B)

**Semantic requirement (D-01B — resolved).** Customer-facing projection must not intentionally continue
presenting content known to no longer satisfy the customer projection eligibility gate after the system
knows the authoritative condition has changed.

**No numeric freshness value, SLA, refresh interval, cache duration, propagation delay, or consistency
promise is established.** Refresh, propagation, cache, replication, and drift monitoring remain
**architecture decisions** (TADR-12/18). The outstanding register item O-02 therefore denotes unfinished
**architecture/mechanism** work only, never an unresolved business decision. [O-02]

No customer-facing Outstanding dashboard, status list, or history treatment is made canonical here.
Outstanding remains the monitoring/attention concept already defined by CD-11; its customer surfacing is
**OPEN / DEFERRED — OQ-06**. [O-06]

## 21. Publication Permission — Already Canonical

**Already canonical — no outstanding HBA decision.** IS-06 does not invent a publication permission,
additional approval step, publication-state authority, or new actor. Existing Manager/Admin reviewer
curation (CD-11 §21) and IS-05 evidence eligibility remain in force; the customer-facing outcome
continues to obey the existing IS-03 authorization scope and eligibility rules. Publication permission
was never an unresolved business decision. [L-15, L-21, O-03]

Broader permission-matrix content remains OPEN under IS-03/HD-06 and is not populated or re-decided by
this specification. [O-09]

## 22. SR Non-Exposure

**BD-SR-004 — SR has zero external/customer exposure in V1.** SR must not appear in the customer portal,
Unit QR history, or as a customer-facing history object. SR content remains internal; SR technical
mechanics are irrelevant to IS-06. [L-23]

## 23. Workspace / Tenant Isolation

Customer-facing reads consume IS-11 isolation requirements. Workspace-owned service/transaction records
must remain within their owning workspace; company scope does not authorize cross-workspace transaction
reads. Shared Company identity does not create cross-workspace transaction visibility. Unit scope,
Company scope, authenticated identity scope, and workspace scope compose; none overrides another.
[L-06, L-09, L-10, D-04]

IS-06 does not redefine tenant/workspace ownership, shared-master rules, usage-marker shape, or
enforcement mechanics. [L-26]

## 24. Dependencies

| Dependency | IS-06 consumes | Authority retained by |
|---|---|---|
| IS-01 | Domain concepts, ownership, projection concept, Unit and Company relationships | IS-01 |
| IS-02 | WO/Visit/Report lifecycle and service execution semantics | IS-02 |
| IS-03 | Google identity, Verified PIC Link, three locked access tiers (Internal CRM, Customer Portal, Unit Portal; prior two-tier wording superseded by HBA-DECISIONS-13), authorization and denial semantics | IS-03 |
| IS-04 | Read contracts, service boundaries, validation and failure behavior | IS-04 |
| IS-05 | Evidence objects, eligibility, approval, reviewer curation, customer-visible evidence | IS-05 |
| IS-07 | Audit events, history and correction/reopen lineage | IS-07 |
| IS-11 | Workspace and tenant isolation | IS-11 |
| AB-01 / TA-01 | Single-writer ownership, projection direction, access and no-reverse-write boundaries | Architecture sources |
| CD-11 / BD-SR-004 | Customer-safe content, no-price rule, report/QR/history boundaries, SR non-exposure | Business sources |

## 25. OPEN / DEFERRED Register

Status of each item is stated per row. OPEN rows may represent architecture/mechanism work or unrelated/out-of-scope business gates. **None represents an unresolved decision about D-01A, D-01B, or OQ-02.**

| ID | Item | Status / treatment in IS-06 | Source / owner |
|---|---|---|---|
| O-01 | Publication/serving **mechanism** (architecture). Business expectation **RESOLVED — HBA D-01A = RETAIN**. | OPEN — **architecture/mechanism**; no serving mechanism selected | ARCHITECTURE_APPROVAL_PACKAGE §11; TADR-12/18; HBA D-01A |
| O-02 | Freshness **mechanism** (architecture). Semantic requirement **resolved — D-01B**. | OPEN — **architecture/mechanism only; no outstanding HBA business decision**; no numeric value, SLA, cadence, cache duration, or propagation promise | IS-01 §14 OQ-06; TADR-12/18; D-01B |
| O-03 | **OQ-02 — Publication permission: ALREADY CANONICAL** | **RESOLVED — canonical**; no new permission, publication authority, or approval layer | CD-11 §21; IS-03 §7; IS-01 R-27 |
| O-04 | No-download serving mechanism | Requirement is retained; serving mechanism remains undecided | CD-11 §21; IS-01 §11; TADR-11/12; HD-01 / OQ-06 |
| O-05 | Previously presented customer-facing content during/after correction or reopen | **RESOLVED — HBA D-01A = RETAIN**: retained as the historical record of what was presented; current authoritative condition remains distinguishable | IS-07 §§7, 9; TADR-12; HBA D-01A |
| O-06 | Customer surfacing of Outstanding | OPEN / DEFERRED; no customer Outstanding dashboard or history behavior is established | IS-01 §14 OQ-06; IS-02 §20; IS-07 §12; Business Authority |
| O-07 | Formal CD documentation for locked identity-link, QR and Business Access Model decisions | Semantics remain locked and are consumed as recorded; documentation formalization remains pending | IS-03 §§3, 14; Decision Register HD-07A |
| O-08 | Evidence categories beyond the canonical locked floor | IS-06 does not add categories; consume only IS-05 eligibility when established | IS-05 §§6, 13; OQ-05; Business Authority |
| O-09 | Broader permission-matrix content | Customer scope rules are consumed as locked; unrelated matrix cells remain open | IS-03 §§8, 14; HD-06; Business Authority |

## 26. Invariants

Each invariant is normative only within the named canonical boundary and is individually traceable.

| ID | Invariant | Source / requirement |
|---|---|---|
| I-01 | Customer Company access is limited to the verified Company scope. | IS-03 §§5, 7; `L-04` |
| I-02 | Unit QR access remains limited to one resolved Unit. | CD-11 §22; TADR-16; `L-07`, `L-09` |
| I-03 | Workspace isolation applies to every customer read. | IS-11 §§8–12; `L-10`, `D-04` |
| I-04 | Anonymous users receive no customer data or preview. | Locked QR decision; IS-03 §§4, 9; `L-05` |
| I-05 | Verified PIC is required for Company scope; Google identity alone is insufficient. | TADR-13/14; IS-03 §§2, 5, 7; `L-04`, `L-05` |
| I-06 | No cross-company customer exposure or grant exists. | IS-03 §§5, 7, 10; `L-06` |
| I-07 | Internal-only information is never included in customer output. | CD-11 §21; `L-13` |
| I-08 | No price, in any form, is exposed externally. | CD-11 §21; TADR-12/14; `L-14` |
| I-09 | Customer content stays within the CD-11 allowlist and its stated conditions. | CD-11 §21; `L-11`, `L-12` |
| I-10 | Evidence visibility follows IS-05 eligibility and reviewer curation, never technician choice. | CD-11 §17; IS-05 §§5–7; `L-15`, `L-21` |
| I-11 | Customer projection is read-only. | AB-01 §§C–D; TADR-07; `L-01`, `L-03` |
| I-12 | Customer projection is not a second source of truth or lifecycle owner. | AB-01 §§C–D; IS-01 §11; `L-01`, `L-02` |
| I-13 | SR has zero external/customer exposure. | BD-SR-004 §3; `L-23` |
| I-14 | QR is permanent, Unit-scoped, controlled, and not anonymous. | CD-11 §22; TADR-16; `L-05`, `L-07`, `L-08` |
| I-15 | IS-07 remains the sole owner of audit definitions and history semantics. | IS-07 §§2, 8; `L-24` |
| I-16 | WO, Visit, and Report state remain owned by their respective domains. | IS-01 §§10–12; AB-01 §§C–E; `L-17–L-20` |
| I-17 | Publication **mechanism**, Outstanding surfacing, and no-download serving **mechanism** remain open as architecture/other gates; publication **permission** is canonical; correction-time serving is **resolved (HBA D-01A = RETAIN)**; freshness is a **semantic requirement (D-01B)**. | IS-00 §14; IS-01 §§11,14; `O-01–O-06`; HBA D-01A; D-01B |
| I-18 | Customer/company/Unit scope never overrides workspace isolation. | IS-03 §7; IS-11 §§8–12; `L-10`, `D-04` |

## 27. Acceptance Criteria

These criteria review the completeness and source fidelity of IS-06; they are not implementation tests.

| ID | Acceptance criterion |
|---|---|
| AC-01 | Company portal is specified as Company-scoped and requires a Verified PIC Link for the linked Company. |
| AC-02 | Unit QR is specified as permanent, Unit-rooted, controlled, Google-authenticated, and unable to browse beyond its Unit. |
| AC-03 | Customer-safe content uses only the CD-11 allowlist and preserves the material-quantity condition. |
| AC-04 | WO, Visit, and Report ownership and internal lifecycle are preserved; no customer lifecycle or second Report is introduced. |
| AC-05 | CLOSED / FINAL and path-appropriate identity/scope/policy/content eligibility are all represented in the projection gate. |
| AC-06 | Evidence visibility consumes IS-05 eligibility, approval, policy, and reviewer-curation boundaries; technician selection is not authority. |
| AC-07 | All 13 required negative-path categories are covered using IS-03 / IS-11 semantics. |
| AC-08 | Company, Unit, identity, and workspace isolation are explicit and composed without cross-scope access. |
| AC-09 | Internal-only, price, vendor-intelligence, and other CD-11 exclusions are explicit; the allowlist is not broadened. |
| AC-10 | Correction/reopen reflects authoritative domain outcomes and preserves IS-07 ownership; prior-presentation handling is **resolved (HBA D-01A = RETAIN)** — previously presented content remains available as the historical record. |
| AC-11 | Audit event and history ownership remains with IS-07. |
| AC-12 | BD-SR-004 zero external exposure is explicit for both portal and QR history. |
| AC-13 | Publication/serving **mechanism** remains an architecture decision; freshness is a **semantic requirement without numeric SLA (D-01B)**; publication **permission** is already canonical; prior-presentation handling is **resolved (HBA D-01A = RETAIN)**. |
| AC-14 | No implementation mechanics, endpoints, infrastructure, provider, framework, schema, or implementation test is prescribed. |
| AC-15 | Every normative requirement, invariant, and OPEN gate is traceable; classification totals reconcile and UNSOURCED = 0. |

## 28. Traceability Matrix & Requirement Classification Register

This register classifies all normative requirements used by §§2–24. Requirement counts below count the
rows in this register; subclauses do not create uncounted requirements.

### LOCKED-SUPPORTED — 28

| ID | Requirement | Canonical source(s) |
|---|---|---|
| L-01 | Customer projection is a derived, read-only view over authoritative operational information; no second source of truth. | AB-01 §§C–D, M; TA-01 §§7–8, 15; IS-01 §11; TADR-07/12 |
| L-02 | Company, Contact/PIC, Unit, WO, JOB, Visit, Report, SR, evidence, state, correction/history, and internal information remain owned by their domains. | IS-01 §§6–12; AB-01 §§B–C; TA-01 §§9, 13, 16, 18 |
| L-03 | Customer-facing projection does not write or change canonical records or state. | AB-01 §§C–D; TA-01 §§7–8, 15; IS-04 §10 |
| L-04 | Company portal scope is based only on a Verified PIC Link for the Company; only its authorized Company scope is visible. | Locked Business Access Model; IS-03 §§2, 5, 7; TADR-13/14 |
| L-05 | External access is Google-only and controlled; login alone yields no Company authorization and there is no anonymous data or preview. | Locked identity/QR decisions; IS-03 §§2, 4, 9; TADR-13/16 |
| L-06 | No cross-company Company-scope access or grant. | IS-03 §§5, 7, 10; TADR-13/14 |
| L-07 | QR access is Unit-scoped; authenticated non-PIC QR access is UNIT_SCOPE only. | CD-11 §22; IS-03 §§4, 7; locked Business Access Model; TADR-16 |
| L-08 | Unit QR identity is permanent; copies on Unit-related documents resolve to the same Unit. | CD-11 §22; IS-01 E-52/R-23; TADR-16 |
| L-09 | Unit QR resolution is Unit-rooted and does not allow cross-Unit browsing. | IS-03 §§7, 10; TADR-12/16 |
| L-10 | Customer reads respect workspace isolation and do not expose foreign workspace-owned transactions. | IS-03 §7; IS-11 §§5, 8–12; CD-07 Q17; TADR-05/06 |
| L-11 | Allowlist is date, technician, summary/work performed, approved photos, replaced component, conditional material quantity, recommendation. | CD-11 §21; CD11-021; IS-01 E-51; IS-02 §16 |
| L-12 | Material quantity is customer-safe only where agreed/appropriate; quantity does not authorize price exposure. | CD-11 §21; IS-01 §11; TADR-12/14 |
| L-13 | Internal notes, correction/cancellation/administrative reasons, vendor intelligence, and other internal/commercial information are excluded. | CD-11 §21; IS-01 §§8, 11; TADR-12/14 |
| L-14 | No prices in any form are exposed to customers. | CD-11 §21; locked Business Access Model; IS-03 §7; TADR-12/14/16 |
| L-15 | Reviewer curation is retained; technician does not choose customer visibility. | CD-11 §§17, 21; IS-03 §4; IS-05 §§3, 7; TADR-11/14 |
| L-16 | Applicable projection eligibility includes CLOSED + FINAL + correct identity/scope + policy + content eligibility. | IS-01 §11; IS-02 §16; IS-04 §10; TADR-12 §§48–64 |
| L-17 | WO remains operational/lifecycle authority; customer view creates no WO state. | IS-01 §§6.4, 10; IS-02 §§2, 18; AB-01 §§C–E |
| L-18 | Visit remains execution authority; completion does not close WO or finalize Report. | CD-11 §§10, 18; IS-01 §§6.4, 10; IS-02 §§5, 12 |
| L-19 | Report is one per WO, consolidates Visit data, is FINAL iff WO is CLOSED, and is not a separate customer report. | CD-11 §18; IS-01 §§6.4, 10; IS-02 §12; AB-01 §§E, G–I |
| L-20 | Report refreshes from authoritative Visits after correction; projection does not write Report state. | CD-11 §§18, 28; IS-02 §§12, 14; IS-07 §§7, 9; TA-01 §16 |
| L-21 | Evidence customer visibility follows IS-05 eligibility including type, approval, policy, reviewer curation; non-eligible content stays internal. | CD-11 §17; IS-05 §§2, 5–7, 12; TADR-11/12 |
| L-22 | Canonical no-download requirement remains in force; its serving mechanism is not settled here. | CD-11 §21; IS-00 §7 IS-06 charter; IS-01 §11; TADR-12 |
| L-23 | SR has zero external/customer exposure in V1. | BD-SR-004 §§3–4; IS-02 context; Decision Register |
| L-24 | IS-07 owns audit definitions/history; IS-06 creates no competing audit system. | IS-07 §§2, 8, 10; IS-04 §12; TADR-08/16 |
| L-25 | Correction/reopen/re-create follows IS-07/CD-11 lineage and does not create another Report or alternate WO. | CD-11 §28; IS-02 §14; IS-07 §§6–9; TADR-09 |
| L-26 | IS-04 owns service/API contracts; IS-06 does not specify endpoint/protocol/implementation. | IS-00 §7 IS-06 charter; IS-04 §§1–2, 9–10; TA-01 §10 |
| L-27 | Unauthorized scope/object, invalid eligibility, anonymous, cross-company, and cross-workspace attempts are denied under existing IS-03/IS-11 guards. | IS-03 §§9–10; IS-11 §§11–14; IS-04 §§4, 9–10 |
| L-28 | **Current (HBA-DECISIONS-13/16/17, 2026-10-08/11):** exactly three access tiers are locked — Internal CRM, Customer Portal, and Unit Portal. Unit Portal is one Unit from a QR scan (short permanent code per HBA-DECISIONS-17), read-only, with no price; login is Google-only; after login, manual name + manual company-text (free text) + phone number are requested; email is taken automatically from Google; the intake lands PENDING and Company scope follows only manual link + approval (no automatic elevation — HBA-DECISIONS-16/18). No customer-specific lifecycle is introduced. **Superseded wording (retained, not deleted):** "No third external scope or customer-specific lifecycle is introduced; company and Unit access retain the existing two-tier model." That prior two-tier statement is SUPERSEDED by HBA-DECISIONS-13 for Unit Portal. | HBA-DECISIONS-13/16/17/18; prior sources retained: IS-03 §§2, 5, 7; IS-01 §§6.2, 11; TADR-14/16 |

### DERIVED-SUPPORTED — 6

| ID | Requirement | Parent source(s) and direct derivation |
|---|---|---|
| D-01 | An authenticated non-PIC may receive only Unit QR scope; lack of Verified PIC Link cannot be treated as Company authorization. | IS-03 §§2, 7, 9 + TADR-16 §72–75; UNIT_SCOPE and COMPANY_SCOPE are distinct, so QR authentication cannot elevate to Company scope. |
| D-02 | Company/Unit histories contain only records inside their corresponding scope; global customer/company or cross-Unit browsing is excluded. | IS-03 §7 + TADR-12 §§90–95; contextual views are scoped and do not become global directories. |
| D-03 | Every customer-facing history item must independently meet the content allowlist and applicable eligibility gate. | CD-11 §21 + IS-01 §11 + TADR-12 §§48–72; derived view cannot widen its source eligibility. |
| D-04 | A Verified PIC's Company scope remains constrained by workspace isolation for workspace-owned transactions. | IS-03 §7 (explicitly DERIVED from CD-07 Q2/Q17) + IS-11 §§8–12; Company identity sharing does not grant foreign transaction visibility. |
| D-05 | When correction/reopen means CLOSED or FINAL no longer holds, affected content does not satisfy the current projection gate. Content previously presented remains available as the historical record of what was presented (HBA D-01A = RETAIN), and the current authoritative condition remains distinguishable. | CD-11 §§18, 28 + IS-07 §§7, 9 + TADR-12 §58–64 (current conjunction not met) + HBA D-01A (prior-presentation handling). |
| D-06 | A customer-facing read that cannot establish authorized identity, Company/Unit scope, workspace, or eligibility is not represented as an authorized successful projection. | IS-03 §9 + IS-04 §§9–10 + IS-11 §§11–14; guards require denial when applicable predicates fail. |

### OPEN / DEFERRED — 7

| ID | OPEN item | Canonical source / owner |
|---|---|---|
| O-01 | Publication/serving **mechanism** (architecture), including snapshot/materialization implementation. Business expectation resolved by HBA D-01A = RETAIN. | ARCHITECTURE_APPROVAL_PACKAGE §§10–11; TADR-12/18; HBA D-01A |
| O-02 | Freshness **mechanism** (architecture); semantic requirement resolved by D-01B. No timing or propagation commitment. | IS-01 §14 OQ-06; TADR-12/18; D-01B |
| O-04 | Technical no-download serving mechanism. | CD-11 §21; TADR-11/12; HD-01 / OQ-06 |
| O-06 | Whether/how Outstanding is surfaced to customers. | IS-01 §14 OQ-06; IS-02 §20; IS-07 §12; Business Authority |
| O-07 | Formal CD documentation for locked identity, QR, and Business Access Model decisions. | IS-03 §§3, 14; Decision Register HD-07A; formalization pending, semantics remain locked |
| O-08 | Any evidence categories beyond the established locked floor. | IS-05 §§6, 13; OQ-05; Business Authority |
| O-09 | Broader permission-matrix cells not fixed by the locked three-tier access boundary (Internal CRM, Customer Portal, Unit Portal; prior two-scope wording superseded by HBA-DECISIONS-13). | IS-03 §§8, 14; HD-06; HBA-DECISIONS-13; Business Authority |

Classification totals: **LOCKED-SUPPORTED = 28; DERIVED-SUPPORTED = 6; OPEN/DEFERRED = 7; UNSOURCED = 0.**

Register truthfulness note: the reduction from 9 to 7 reflects two items that are genuinely settled — O-03
(publication permission, already canonical) and O-05 (prior-presentation handling, **HBA D-01A = RETAIN**).
O-02 remains counted OPEN because it represents unfinished **architecture/mechanism** work; its wording no
longer implies an unresolved HBA business decision. Other OPEN rows retain their stated scope and owner;
this reconciliation closes only the D-01A/D-01B/OQ-02 status questions.

## 29. Cross-Spec Consistency

| Source | Consistency check | Result |
|---|---|---|
| IS-03 v1.4 | Google Identity is not Company authorization; manual intake + manual link only (no email-match elevation); UNIT_SCOPE / COMPANY_SCOPE; configurable link authority default Manager; denials and no cross-company access | Consistent; scopes consumed, not redesigned |
| IS-04 v1.1 | Read-only gated reads; IS-04 owns contracts and validation/error behavior | Consistent; no API ownership conflict |
| IS-05 v1.1 | Evidence ownership, eligibility, reviewer curation, customer serving boundary | Consistent; no evidence definition reintroduced |
| IS-07 v1.1 | Audit ownership, current domain state, correction cycles, Report refresh and lineage | Consistent; no second audit/history/correction model |
| IS-11 v1.1 | Workspace and company isolation, read scoping, explicit rejection | Consistent; workspace scope composes with customer scope |
| IS-01 | Domain ownership, projection concept, allowlist, eligibility and OPEN gates | Consistent; path-specific access gate preserves QR UNIT_SCOPE and Company Verified PIC scope |
| IS-02 | WO / Visit / Report lifecycle and customer-safe output | Consistent; no lifecycle or report duplication |
| AB-01 | Single writer, derived projection, QR/portal split, audit observer | Consistent |
| TA-01 v1.1 | Projection read boundary and deferred implementation | Consistent; no technology prescribed |
| CD-11 | §§17–22 evidence, Report, history, allowlist, QR, scope, exclusions, no-download | Consistent |
| BD-SR-004 | SR zero external visibility | Consistent; explicit non-exposure retained |
| TADR-07/11/12/13/14/16 | Ownership, evidence serving, projection gate, identity, visibility and QR direction | Consistent; deferred gates preserved |

**Cross-spec result: zero identified contradictions.** Ownership conflicts: none. Lifecycle conflicts: none.
Access conflicts: none; UNIT_SCOPE and COMPANY_SCOPE remain distinct. Visibility conflicts: none; allowlist,
curation, no-price, and SR exclusion retained. Projection/source-of-truth conflicts: none. API conflicts:
none. Audit conflicts: none. Publication/serving **mechanism** remains an architecture decision; freshness
is a **semantic requirement**; publication permission is **canonical**; correction-time serving is
**resolved (HBA D-01A = RETAIN)**.

## 30. Drafting Conclusion

IS-06 v1.3 specifies a technology-neutral, read-only customer projection under the existing identity,
Company/Unit scope, workspace isolation, customer-safe allowlist, lifecycle, evidence, and audit
boundaries. Unit Portal intake is manual (HBA-DECISIONS-16/18), QR is a short permanent code shown
screen-only (HBA-DECISIONS-17). The business expectation for previously presented customer-facing content is **resolved
(HBA D-01A = RETAIN)**; publication permission is **already canonical**; freshness is a **semantic
requirement (D-01B)**. Remaining open items are architecture/mechanism and out-of-scope gates. This
document is **LOCKED / CANONICAL** as approved above.

## Addendum HBA-DECISIONS-22 (2026-10-13) — kanon v16/v17 + timing snapshot

- Migrasi v16 (profil perusahaan sendiri) + v17 (lokasi visit) adalah KANON per perintah HBA (a). Wording lama retained; nol aturan bisnis baru.
- Timing salinan pelanggan: dibuat saat WO ditutup yaitu saat manager approve (`approve_report` / CLOSED) per perintah HBA (c). Wording lama yang bertentangan retained sebagai riwayat superseded.
- Perluasan panel konfigurasi + kaitan Google HBA ke manager dicatat sebagai perintah (d)(e); rincian ikut eksekusi terotorisasi.

**IS-06 v1.3 LOCKED (HBA 2026-10-12) + Addendum HBA-DECISIONS-22 (2026-10-13).**
