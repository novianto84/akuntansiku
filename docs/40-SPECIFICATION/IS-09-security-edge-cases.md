# IS-09 — Security & Edge-Case Specification (V1)

```text
Document ID: IS-09
Title: Security & Edge-Case Specification (V1)
Version: 1.0 (LOCKED/CANONICAL per HBA-DECISIONS-21, 2026-10-13)
Status: LOCKED / CANONICAL — locked by HBA 2026-10-13 ("IS-09 dikunci jadi aturan tetap")
Authority: AI Manager / Lead Architect (specification author). Business Authority owns all rules
  and all security/authentication architecture decisions.
Scope: Implementation-critical security & edge behavior for V1: authentication, authorization,
  tenant/company isolation, public/customer projection, QR/public access, token/session behavior,
  evidence/file handling, abuse/rate limiting, audit/security boundary, invalid/expired/revoked
  access, cross-company access prevention.
Sources: IS-03 (LOCKED), IS-11 (APPROVED), IS-05 (LOCKED), IS-07 (LOCKED), IS-06 (DRAFT), CD-11
  (SIGNED), locked Human decisions (identity-link, QR CONTROLLED, Business Access Model),
  TADR-06, TADR-12, TADR-13, TADR-14, TADR-16, Architecture Approval Package & Baseline.
Implementation: NO crypto/AuthN products, NO framework, NO code, NO topology, NO token-format
  design. Technology-neutral. Any security policy beyond the authority below → HBA DECISION BATCH.
```

> States the security *guarantees and accepted edge behaviors* V1 must satisfy. It lists boundary
> and negative-path expectations, not implementation mechanisms. No new security policy is created
> where the underlying authority is absent.

---

## 1. Authority Boundaries

- **External identity = Google-only** (locked Human decision; Architecture Baseline §External
  access). No other external IdP in V1.
- **email/domain matching ≠ authorization** (Architecture Baseline, Identity invariant).
- **Google Identity ≠ Contact/PIC ≠ Verified PIC Link ≠ Company Access**; sign-up ≠ automatic PIC;
  applicant ≠ approver (no self-approval); no automatic approval.
- Authentication/security architecture changes are **Human Business Authority** decisions; this
  document records requirements and does not alter that boundary.

## 2. Authentication / Session Behavior (V1)

- External users authenticate with Google identity; session established only after successful
  login. `LOGIN ≠ COMPANY ACCESS`; a session alone grants no Company access.
- **Token/session behavior:** sessions must support expiry, revocation (incl. when identity-link or
  access is revoked), and invalid/expired handling with an explicit rejection. No silent
  re-grant of a revoked session. Exact token format/lifetime is implementation design (not locked).
- Technical sessions (internal users) follow the same expiry/revocation principle.

## 3. Tenant / Company / Workspace Isolation (Security)

- Security boundary composes **identity → role authority → workspace/company scope → business-role
  authority** (IS-03, IS-11, TADR-06, TADR-14). No guard bypass for convenience.
- **Cross-company prevention:** a session scoped to Company A must never read/write Company B data
  through any path (direct, related-object traversal, alternate reference, sequence reuse).
- No silent elevation; no cross-company grant; no automatic cross-workspace movement (IS-11 §8).

## 4. Public / Customer Projection Security (IS-06 gated)

- **Anonymous access: none.** QR scan / public link always routes to SIGN UP / SIGN IN
  (Google-only), then CHECK ACCESS, then UNIT DATA (CD-11 §22). No anonymous external data.
- **No preview before login.** QR is a Unit identifier, not a document scope; resolves exactly one
  Unit on Unit/Invoice/Surat Jalan (validated to point to the same Unit).
- Verified PIC sees only its linked Company's data (Company Scope), never other companies; non-PIC
  authenticated external user → Unit Scope only, which is **not a browsing mechanism** (cannot
  browse other Units/companies).
- **No price leakage:** external/customer-facing output never shows acquisition price, pricing,
  vendor/commercial intelligence, internal notes, or correction/cancellation/administrative
  reasons (CD-11 §21). Quantity is only per agreed/approved policy. Publication/curation **mechanism**
  is an architecture decision; publication permission (OQ-02) is already canonical; the customer
  publication business expectation is resolved (HBA D-01A = RETAIN).

## 5. QR / Public-Access Security

- QR is **permanent + unit-scoped**, **revocable** (TADR-16) — a revoked QR grants no access.
- Contributes to access resolution only as a Unit pointer; it never grants Company access and never
  bypasses identity/scope checks. No anonymous QR read of protected content.

## 6. Evidence / File Handling Security

- Evidence objects follow IS-05 (locked) with immutable originals and mediated serving (TADR-11).
- Uploads/attachments are scoped to the owning Visit/Unit/Company; access to an attachment is
  subject to the same identity+scope+authorization gate as the owning object.
- Customer-facing evidence exposure is only the curated/approved subset (IS-05 eligibility +
  IS-06 publication gate). No raw internal evidence in external context.

## 7. Invalid / Expired / Revoked Access Edges

- Attempts with invalid session, expired token, revoked identity-link, revoked PIC status, revoked
  Company access, or revoked QR → explicit denial + audit of the attempt (per IS-07).
- **Revocation takes effect on access:** a revoked link must not continue to grant scope. Exact
  propagation timing is implementation design, but the guarantee (no silent continued grant) is fixed.
- A revoked/expired state never silently downgrades to a broader scope.

## 8. Abuse / Rate Limiting

- HBA-DECISIONS-21 (2026-10-13, LOCKED) angka tetap: **login 5x gagal → kunci 2 jam**;
  **scan QR kode invalid 5x gagal → kunci 2 jam per alamat** (per alamat peminta).
  Ini angka HBA, bukan desain implementasi; tak ada aturan bisnis baru selain angka ini.
- Rate limiting is **required** only where abuse can threaten the above guarantees — login,
  QR resolution, evidence upload, and any identity/access boundary. Scope/thresholds are
  implementation design, *kecuali angka HBA di atas yang override untuk login + QR invalid
  (HBA-19 tanpa-rate-limit SUPERSEDED; wording lama retained sebagai riwayat)*; the requirement
  is that abuse attempts at these boundaries must be detectably bounded. Ratio/edge details
  beyond locked policy → HBA/technical decision if needed.

## 9. Audit / Security Boundary (IS-07 by reference)

- Security-relevant events (denials, scope resolutions, revocations, expiry, identity-link changes,
  QR revoke) are emitted to the IS-07 append-only audit (actor, server timestamp, object, reason,
  before/after). No second/competing audit model.

## 10. Security Negative-Path Requirements (V1 MUST REJECT)

(a) accessing another company's data; (b) cross-workspace read/write; (c) unsigned/unauthenticated
external read of protected projection; (d) anonymous QR content read; (e) accessing another Unit
from a Unit-scoped session; (f) self-approval / technician-approving-own-WO;
(g) price/internal leakage in external output; (h) providing an identifier from another scope.
Each has an explicit rejection expectation; none may silently succeed.

## 11. Security Acceptance Criteria

- AC-1: Google-only external identity; no other external IdP. AC-2: LOGIN≠Company Access enforced.
- AC-3: cross-company/cross-workspace negative paths (a),(b) and QR/scope negatives (c)–(e) reject
  explicitly and audit. AC-4: no price leakage guarantee holds (g). AC-5: no security policy
  introduced without a cited authority; OOTB "security product" choices absent. AC-6: revocation
  semantics (no silent continued grant) documented. AC-7: all negative paths reference IS-03/IS-11.

## 12. Open / HBA-gated Items

- **Publication mechanism/curation** is an **architecture decision**; **publication permission (OQ-02)**
  is **already canonical** and is not an open HBA decision. The customer publication business expectation
  is resolved (HBA D-01A = RETAIN); when the mechanism resolves, this spec is updated.
- **Approver lists / full permission-matrix content (HD-06)** remain OPEN (IS-03); this spec
  assumes the lockdown and never invents a value.
- Any security policy beyond the above, or any choice of IdP/token/rate-limit product, is either
  technical decomposition (after approval) or an HBA decision if it alters the security boundary.

## 13. Traceability

§1→Architecture Baseline (Identity/QR/Access) + IS-03; §3→IS-11 + TADR-06/14; §§4–5→CD-11 §§21–22 +
IS-06 + TADR-16; §6→IS-05 + TADR-11; §7→IS-03 + IS-07; §9→IS-07 + TADR-08; §10→IS-11 §12 +
Architecture Baseline invariants.

## 14. Self-Audit

Authorized by Prompt 1 mandate ✅ · no product/framework/IdP/token/topology ✅ · no new security policy
beyond cited authority ✅ · OPEN items (publication **mechanism**, HD-06) explicit, never filled silently; publication permission (OQ-02) canonical, D-01A resolved ✅ ·
negative paths present ✅ · STRICT authority preservation (auth changes = HBA) ✅.

---

*End of IS-09 v1.0 LOCKED (HBA-DECISIONS-21).*
