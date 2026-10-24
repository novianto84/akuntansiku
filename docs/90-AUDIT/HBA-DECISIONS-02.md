# HBA DECISION RECORD — Publication, Permission Matrix, Reminder

```text
Record ID:      HBA-DECISIONS-02
Date:           2026-10-02 (AMENDED — publication model revised by HBA)
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         DECISIONS RECORDED as stated by HBA in session 2026-10-02
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record.
```

---

## 1. Publication Model (was HD-01 / OQ-02) — DECIDED (AMENDED)

**HBA decision: B+ — Google-login required, two-tier access.**

**Amendment (2026-10-02):** HBA revised the publication model. Login is **required** (Google account). Two access tiers based on email→PIC linkage.

### Access tiers

| Tier | Who | What they see |
|---|---|---|
| **Unit visitor** | Logged-in Google user, email NOT linked as PIC | **Only** the unit they scanned: unit profile + CLOSED WO history for that unit |
| **Customer portal** | Logged-in Google user, email IS linked as PIC of a Company | **Full customer portal**: all units of that Company, all WO history, SR, reports |

### What this settles

| Aspect | Outcome |
|---|---|
| QR/barcode | Printed on unit and on invoice — both scan to the same portal |
| Login | **Required** — Google account (not anonymous) |
| Unit visitor (no PIC link) | Read-only, per-unit, CLOSED history only |
| Customer portal (PIC link) | Read-only, per-Company, all units + WO + SR + reports |
| Write actions | **None** — read-only for both tiers |
| Scope isolation | Unit visitor: one unit only. Customer portal: one Company only. |

### What this means for WP-08

WP-08 is **UNBLOCKED**. The publication model is:

- Google OAuth login (ExternalGoogleProvider — currently a fail-closed stub, needs implementation)
- Email → PIC → Company resolution (reuse `app/access/identity` + `app/company/pic_link`)
- Two rendering modes:
  - **Unit visitor mode**: no PIC link, single-unit view
  - **Customer portal mode**: PIC-linked, multi-unit, multi-WO view
- Both modes: read-only, no pricing, no internal notes

### Clarification (2026-10-02, HBA)

**Customer portal is strictly read-only.** No write actions of any kind in V1.

- Customer CAN read: unit profile, WO history (CLOSED), SR, report FINAL
- Customer CANNOT edit: no data modification, no cancellation, no internal notes
- Customer CANNOT create SR via portal (that is a write action)

**Future possibilities (NOT V1):**
- "Contact us" button → open WhatsApp chat to our number
- "Request Service" button → simple SR form (write action — requires separate decision)

### Still OPEN (not decided)
- Whether customer portal shows pricing/quotation (recommend: no)
- Whether the portal is a separate service or part of the CRM backend
- Whether Google OAuth is the only login method or email/password also allowed

---

## 2. Permission Matrix (was HD-06) — DECIDED

**HBA decision: A — approve the matrix already enforced in code.**

The permission matrix is already implemented in `app/access/authz.py` and verified by 374 tests. HBA approves it as-is. No code change required.

The matrix will be documented as a formal record (read-only snapshot of the enforced rules) — this is a documentation act, not a code change.

---

## 3. Reminder Automation (was HD-07A) — DECIDED

**HBA decision: A — manual only. Dashboard is the reminder surface.**

| Aspect | Outcome |
|---|---|
| Automatic reminders | **Disabled** — no scheduler, no auto-send |
| Manual reminders | Created by Admin/Manager/Sales via UI (already implemented) |
| Dashboard role | **Primary reminder surface** — open WOs, outstanding items, overdue tasks appear on dashboard |
| Future automation | Not in V1. Could be WP-11 if needed. |

---

## 4. Summary of decisions

| Question | Decision | Effect |
|---|---|---|
| Publication (HD-01/OQ-02) | **B+** — Google login, two-tier (unit visitor / customer portal) | WP-08 unblocked, scope expanded |
| Permission matrix (HD-06) | **A** — approve current code | No code change |
| Reminder (HD-07A) | **A** — manual only, dashboard as reminder | No code change |

## 5. Next step

WP-08 (unit portal + customer portal) can now be specified and built. The spec should cover:
- Google OAuth integration
- Email → PIC → Company resolution
- Two rendering modes (unit visitor vs customer portal)
- Data visibility rules per tier
- Security (no cross-company leakage, no pricing)
- Deployment (separate service or part of CRM backend)

Awaiting HBA authorization to proceed with WP-08 spec + build.
