# HBA DECISION RECORD — WP-11 F-20/F-21 Clarifications (DRAFT private, SUBMITTED to Manager queue)

```text
Record ID:      HBA-DECISIONS-05
Date:           2026-10-05
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — clarifications as stated by HBA in session 2026-10-05
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record.
```

> This record captures HBA clarifications stated in session 2026-10-05 on top of
> the WP-11 package (`WP-11_HBA_DECISION_PACKAGE_F20-F24.md`, recorded 2026-10-05).
> It does not itself edit any canonical document. Canonical materialization and
> package decision-sheet completion are separate, explicitly-scoped steps.

---

## 1. F-20 — DRAFT cap + self-cancel + private per account (RECORDED)

**HBA statements (2026-10-05):**

- Limit 10 DRAFTs per user is enough ("limit 10 untuk drafts, saya rasa cukup").
- Only the creator can cancel their own DRAFT ("hanya yang buat yang bisa batalkan").
- Reason stated by HBA: each DRAFT is stored in the creator's own account, so
  nobody else can see or cancel it except themselves.

**Reading:** DRAFT = private per account. Create / edit / delete = creator only.
Cap 10 = personal per user. No expiry (per prior F-20 recording). Competing
DRAFTs from the same Published Revision do NOT cancel each other.

## 2. F-21 — DRAFT private; SUBMITTED visible to Manager waiting-approval queue (RECORDED)

**HBA statements (2026-10-05):**

- Only the DRAFT maker can view it ("yang bisa lihat hanya yang membuat draft").
- Only the maker can delete it ("yang bisa menghapus juga hanya yang membuat draft").
- HBA question answered in session: submit goes to the Manager-role waiting
  approval queue — if the Manager cannot see it, approval is impossible. Hence:
  BEFORE submit the DRAFT belongs to the maker only; AFTER submit it MUST appear
  in the Manager waiting-approve queue.

**Reading (consistent with package §F-21 as recorded):**

- DRAFT (pre-submit): creator-only visibility. Nobody else (including
  Manager/Admin, other internal users, customer) sees it.
- SUBMITTED and above: visible to the Manager role via the waiting-approval
  queue so approval can proceed. Customer never sees a pending revision
  (R-37 unchanged).
- If SUBMITTED were invisible to everyone, the approval queue would deadlock —
  stated by HBA as the reason for the split.

## 3. Boundary

- This record modifies no canonical document, changes no document status,
  creates no business rule beyond the HBA statements above, and authorizes
  no implementation.
- The bridge package decision sheet + rationale fields remain to be completed
  from this record (separate step).
- WP-11 is NOT finalized and NOT authorized for build on the strength of this
  record; the package stays NON-CANONICAL preparation until HBA confirms the
  remaining items (F-23 attachment snapshot, decision sheet).

## 4. Cheapest next step

Complete the package decision sheet from §§1–2 above, then a corrective spec
pass on the stale spec text the decisions override — no new build until then.
