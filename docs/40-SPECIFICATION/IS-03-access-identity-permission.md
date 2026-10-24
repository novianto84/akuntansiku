# IS-03 — Access, Identity & Permission Specification

```text
Document ID: IS-03
Title: Access, Identity & Permission Specification
Version: 1.4 (additive v1.3→v1.4: V-4 restated to HBA-DECISIONS-16 manual intake — automatic elevation retired to superseded history; settled content unchanged. No new business rule beyond those locked records.)
Status: LOCKED / CANONICAL — BUSINESS AUTHORITY APPROVAL 2026-10-12 (HBA chat: audit+selaraskan semua kanonik; v1.4 = V-4 manual intake, settled v1.3 unchanged)
Lock record: settled normative content authoritative as reviewed; OPEN/DEFERRED items remain unresolved; O-v1.1-01 remains observation only.
Scope: Identity-link lifecycle; role/authority catalog; permission-matrix structure;
  UNIT vs COMPANY scope enforcement; QR/CONTROLLED-access consumption; Verified PIC Link
  lifecycle; self-approval boundary; cross-company isolation; guards + negative paths;
  invariants; audit implications; acceptance criteria.
Authority: AI Manager / Lead Architect (specification author). Business Authority owns all rules.
Sources: IS-01 §§6.2,8 (E-07…E-10, R-03); IS-02 + decomposition + AB-01 + TA-01 v1.1;
  locked identity/QR/access-model human decisions (formal CD pending HD-07A — cited via
  Decision Register, never fabricated); TADR-12/13/14/16 (APPROVED); CD-01 S3; CD-03; CD-06 Q8;
  CD-08; CD-11 §§2,4,7,9,19,21,22; BD-SR-005 (LOCKED V1); BD-SRWO-001 (O-06).
ID basis: BA authorization for IS-03 at docs/40-SPECIFICATION/IS-03-access-identity-permission.md.
Implementation: NO schema/SQL/migration/API/UI/code/TASK-001. Technology-neutral.
```

> Requirements classified LOCKED-SUPPORTED (explicit canonical source) or OPEN/DEFERRED-SUPPORTED
> (explicitly marked, never resolved here). Target: zero UNSOURCED normative requirements.

---

## 1. Scope and Boundaries

Specifies *who may act, on what scope, through which verified relationship* — and the structures
that enforce it. Covers external identity, link lifecycle, internal roles/authorities, scope tiers,
and guard/negative-path behavior. Excludes: permission-matrix **content** (OPEN, HD-06); visibility
configuration values (OPEN, C-4); publication mechanism (deferred, IS-06); provider/session
mechanics (deferred technical detail); any implementation technology.

## 2. Terminology (canonical, not redefined)

**Google Identity** (who, external, Google-only) ≠ **Contact/PIC** (recorded person under a Company)
≠ **Verified PIC Link** (per-company grant lifecycle) ≠ **Company Access** (consequence: UNIT_SCOPE
vs COMPANY_SCOPE). **Authentication** (who) / **authorization** (what actions) / **business
visibility** (which fields) are three separate layers (TADR-14). Invariants: LOGIN ≠ COMPANY ACCESS;
QR ≠ COMPANY ACCESS; sign-up alone grants nothing (locked decisions; IS-01 E-07…E-10).

## 3. Source Hierarchy

AB-01 (baseline) → LOCKED human decisions (identity-link, QR CONTROLLED ACCESS, Business Access
Model + no-price rule + self-approval invariant; formal CDs pending — cited as
"LOCKED HUMAN DECISION, formal CD pending HD-07A" per register convention) → CD-01 S3 / CD-03 /
CD-06 Q8 / CD-08 / CD-11 → IS-01 entities → IS-02 guards → TADR-12/13/14/16 direction. Older
material never overrides. No chat-memory citations.

## 4. Actors and Authorities

- **External:** anonymous (no data, not even preview — CONTROLLED ACCESS); authenticated
  non-PIC (UNIT_SCOPE only, QR context); verified PIC (COMPANY_SCOPE for linked Companies only).
- **Internal roles** (structure per CD-01 S3; content deferred): Admin (unrestricted operational
  authority — BD-SR-005); Manager (CREATE_WO + ASSIGN_WO default V1, review/approval authority);
  Sales (CREATE_WO default); Coordinator (ASSIGN_WO default; no default CREATE_WO V1); Technician
  (execution; CREATE_WO only if granted; never approves, never self-closes); Finance/Kasir (structure
  retained; no execution authority invented here).
- **Authorities (LOCKED-SUPPORTED):** CREATE_WO (CD-11 §4; BD-SRWO-001 O-06); ASSIGN_WO (CD-11 §7);
  approval/review (CD-11 §§2,19); cancellation execution Admin/Manager (CD-11 §9); reviewer curation
  of customer-facing data (CD-11 §21); Q8 visibility administration via Admin configuration (CD-06 Q8).
  LINK_CUSTOMER (HBA-DECISIONS-16): authority to link a Unit Portal contact intake to a Company/PIC —
  configurable value, default Manager, never hardcoded (see §5 / §8).

## 5. Identity-Link Lifecycle

States VERIFIED / PENDING / REVOKED per Company; strictly one state machine per Company per
external identity; no cross-company grant (locked decisions; TADR-13; IS-01 E-09). Flow:
application (Unit Portal contact intake per HBA-DECISIONS-16: Google sign-up, manual name + manual company-text + phone, email automatic from Google → PENDING queue; PIC registration otherwise; supporting evidence may be requested, no fixed taxonomy) → PENDING →
link-authority approval (configurable authority, default Manager; applicant ≠ approver; no auto-approval) → VERIFIED; revocation → REVOKED
with session propagation (mechanism deferred). Google email need not be a company email; email/domain
matching is never the requirement. Link entity separate from Contact so revocation preserves
relational/service history (TADR-13; IS-01 R-03). Contact-less or Company-less individuals cannot
enter this chain (BD-G01-G02: servable internally as UNVERIFIED requesters; no V1 external access).

### 5.1 Unit Portal contact intake (HBA-DECISIONS-16, manual)

- Intake: Google sign-up → manual name + manual company-text (free text, not a Company picker) + phone; email automatic from Google.
- Company-text is a claim, not a grant: it never itself creates Company scope or PIC status.
- Intake lands in a PENDING queue for the link authority. Until manual link: UNIT_SCOPE only (the single QR-resolved Unit).
- Link is manual by the configured link authority only. No auto-approval, no automatic elevation by email match.
- Company match + Contact creation + link decision are the link authority's manual acts (implementation via governed path).

## 6. Authorization Boundaries

Action checks at domain-policy enforcement points composed with the workspace guard (TADR-14 +
IS-11): every command in the IS-02/TA-01 command table carries actor + authority + state
preconditions (CREATE_WO, ASSIGN_WO, approval, cancellation, evidence review per §4). Enforcement
location: owning domain (authorization belongs near the owner — TA-01 §14). No domain bypasses
another's state guard. Role/weapon separation: Google Identity and PIC status are never approval
authority (TADR-13).

## 7. Scope Model

- **UNIT_SCOPE** (authenticated non-PIC, QR context): unit identity, owner company, address,
  work/material history; never PIC details/lists, other units, company-level data, or prices.
- **COMPANY_SCOPE** (verified PIC only): all Units of that Company in the CRM + histories + PIC
  per customer-safe visibility; never prices in any form (explicit no-price rule).
- Company scope never crosses workspace transaction boundaries (IS-11) **[DERIVED from CD-07 Q2
  (transactions per workspace) + Q17 (no cross-workspace movement)].** QR resolves to exactly one
  Unit with cross-unit browsing structurally impossible (TADR-16). Scopes are consequences of link
  state, not stored grants (IS-01 E-10).

## 8. Permission Structure (content OPEN)

Structure (LOCKED-SUPPORTED as structure): action × object × scope × state-guard matrix shape with
cells filled only from locked authorities (§4, §10); everything else explicitly
**OPEN / AWAITING BUSINESS AUTHORITY DECISION (HD-06)**. LINK_CUSTOMER cell (HBA-DECISIONS-16):
configurable link authority, default Manager, never hardcoded — HBA edits the value via the dynamic
panel, not the programmer. Q8 overlay: Admin-configured per-role
Vendor Offer visibility without changing ownership/records/history/provenance (CD-06 Q8; values
OPEN per C-4). Hardcoding any matrix content is prohibited (TADR-14).

## 9. Access Guards

Guards reject before side effects; rejections audited (IS-11 I-9/I-10 pattern, cited not redesigned).
The following guards apply on the **external access plane only** and do not override or restrict
established internal-role authorities (§4): unauthenticated → nothing; authenticated-non-PIC
outside QR context → nothing beyond login; cross-company attempt → deny (no grant exists to honor); technician approve/close-own → deny;
self-approval → deny (applicant ≠ approver invariant); unpublished/non-eligible content → deny;
prices/internal categories → never leave the internal plane.

## 10. Negative Paths

(a) anonymous access incl. preview; (b) authenticated user reaching another company's scope;
(c) non-PIC reaching PIC lists/company-level data; (d) technician self-approval or own-WO approval;
(e) applicant approving own link; (f) visibility choice by technician; (g) price in any external
output; (h) cross-workspace operation via scope confusion; (i) QR resolving beyond its Unit;
(j) revoked link retaining access (session must propagate — mechanism deferred). Each MUST be
denied; (j)-denial is **DERIVED** from locked revocation semantics (REVOKED ends the grant;
mechanism itself deferred), not a new rule.

## 11. Invariants

V-1 applicant ≠ approver; no auto-approval. V-2 LOGIN ≠ COMPANY ACCESS; QR ≠ COMPANY ACCESS.
V-3 sign-up grants nothing. V-4 exactly three locked access tiers — Internal CRM, Customer Portal, and Unit Portal — and no tier beyond those three. **Current (HBA-DECISIONS-16/18):** Unit Portal is one Unit from a QR scan, read-only, with no price; login is Google-only; after login, manual name + manual company-text (free text) + phone are requested; email is taken automatically from Google; the intake lands PENDING and Company scope follows only manual link + approval — no automatic elevation by email match. **Superseded history (retained, not deleted):** the prior "exactly two external tiers (no third)" wording (superseded by HBA-DECISIONS-13, 2026-10-08) and the v1.2–v1.3 automatic-elevation wording (superseded by HBA-DECISIONS-16, 2026-10-11). This restatement adds no business rule beyond the locked records and is consistent with the IS-06 §6 realignment. V-5 no cross-company grant.
V-6 no-price external rule. V-7 email/domain matching never required. V-8 revocation ends access
without deleting history. V-9 identity ≠ membership ≠ access (four distinct concepts). V-10 no
anonymous data. All implementation-free; all LOCKED-SUPPORTED (locked decisions; TADR-13/14/16;
IS-01 E-07…E-10).

## 12. Audit Implications

Link lifecycle events (application/approval/revocation with actor, server timestamp, company scope);
authorization denials (actor, target, rule); scope-tier resolutions; Q8 configuration changes;
reviewer curation actions — all append-only on the existing pattern (TADR-08; no new subsystem).
Session-propagation mechanics deferred.

## 13. Dependencies

Upstream: IS-01 entities, IS-02 guards, AB-01/TA-01 boundaries, IS-11 scoping. Downstream:
IS-04 (enforcement points), IS-05/06 (eligibility/access inputs), IS-10 (isolation posture).
IS-03 unblocks IS-04/05/06/10 normatively.

## 14. OPEN / DEFERRED Items

OPEN (HD-06): full permission-matrix content; approver lists; suggest/approve detail; material-take
authority. LINK_CUSTOMER value configurable (default Manager) — HD-06 content, HBA-editable via panel.
OPEN (C-4): per-role visibility values. DEFERRED: publication mechanism (IS-06);
provider/session/token mechanics; revocation-propagation mechanism; deployment context. Formal-CD
issuance (HD-07A) is documentation formalization, not content. None blocks IS-03 structure.

## 15. Acceptance Criteria

AC-1 four concepts + three layers distinguishable in every flow. AC-2 link lifecycle states and
no-cross-grant demonstrable. AC-3 every §10 negative path denied. AC-4 matrix shape complete with
OPEN cells explicitly marked (zero hardcoded content). AC-5 invariants V-1…V-10 each traceable.
AC-6 no mechanism prescribed. AC-7 formal-CD citations use the pending convention (no fabrication).

## 16. Traceability

§§2,5,7,10–11 → locked human decisions (register) + IS-01 E-07…E-10 + TADR-13/14/16, with
explicit DERIVED markings where applicable (§7 workspace-boundary sentence: DERIVED from CD-07
Q2+Q17; §10(j) denial: DERIVED from locked revocation semantics). §4 → CD-01 S3,
CD-06 Q8, CD-08, CD-11 §§2,4,7,9,19,21, BD-SR-005, BD-SRWO-001. §6 → TADR-14 + TA-01 §14. §8 →
TADR-14 (structure yes / content no). §9 → locked decisions + IS-11. §12 → TADR-08 pattern.
No fabrication; no chat-memory citation.

## 17. Self-Audit

Artifact at authorized path ✅ · LOCKED v1.4 (HBA 2026-10-12 audit; V-4 manual intake; settled v1.3 unchanged) ✅ · no OPEN resolved (matrix content, link-authority value configurable default Manager, visibility
values, mechanisms all tagged) ✅ · no rule invented (revocation denial is locked semantics;
mechanism deferred) ✅ · no prep numbering ✅ · no schema/API/UI/code/TASK-001 ✅ · zero UNSOURCED
normative requirements (full pass: every "MUST/never/only" traces above) ✅ · negative paths
explicit ✅ · invariants implementation-free ✅ · alignment preserved (single-writer, direction,
neutrality, append-only) ✅ · no unauthorized file modified (single-file creation) ✅.

---

*End of IS-03 v1.4 LOCKED (HBA 2026-10-12).*
