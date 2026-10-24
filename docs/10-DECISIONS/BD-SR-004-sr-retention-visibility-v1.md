# BD-SR-004 — SR Retention / Visibility V1 (O-04)

```text
Decision ID: BD-SR-004
Title: SR Retention / Visibility V1 — Retention, Assignment-Based Visibility, Integrity (O-04)
Mode: Business Decision
Status: LOCKED — V1 (BUSINESS AUTHORITY APPROVAL 2026-09-23)
Business Authority Approval: YES (HANDPROMPT — FINALIZE O-04 + BA clarification on assignment-based visibility and pre-terminal editability, 2026-09-23)
Implementation Authorization: NO
```

> Locks O-04 per final BA clarification, reconciled to the explicit SR V1 lifecycle
> decision. Historical records/data are untouched. No new entity, field, workflow,
> retention engine, schema, or UI is created.

---

## 1. Retention (LOCKED — V1)

- No special retention period for SR in V1. SRs are kept as long as CRM data is kept.
- No new month/year figures. No retention engine, archival subsystem, or auto-purge.
- Special retention may be addressed in a later decision/version if needed.

## 2. Internal visibility — assignment/relevance principle (LOCKED — V1)

- Internal SR visibility follows **assignment/relevance**: an internal user may see
  SRs relevant to their work/responsibilities. Uniform all-roles-see-all-SRs is
  NOT the V1 rule.
- Conceptual (non-exhaustive, non-schema) reading:
  - Manager/Admin: internal access per workspace authority;
  - Sales: SRs relevant to their customers/requests;
  - Coordinator: SRs relevant to coordination/work assignment;
  - Technician: SRs relevant to assignments/work involving them.
- This is an **access principle**, not a DDL/schema decision. No SR-specific
  assignment entity is created for O-04. No complex V1 permission matrix is created
  here (see O-05 proposal track).

## 3. External visibility (LOCKED — V1)

- **SR is not exposed to Verified Customer PIC in V1.** No SR portal view, no
  customer-visible SR field, no public SR, no QR SR, no anonymous SR access.
- Revisit only when a publication / customer-safe classification mechanism is
  decided in a later version.

## 4. Content visibility (LOCKED — V1)

- All SR content is treated as internal in V1. No `customer_visible` field. No
  per-content visibility classification.

## 5. Historical integrity and editability (LOCKED — V1, reconciled lifecycle)

- While `OPEN`, SRs **may be completed and corrected** per applicable internal
  authority, so follow-up and completion can proceed. Follow-up and WO creation are
  activities; neither adds an SR status.
- Creating or saving a WO DRAFT does not close or terminalize the SR. The SR remains
  `OPEN` after WO creation.
- Once `CLOSED`, SR content is **immutable**. No V1 reopen. No in-place correction
  of a CLOSED SR. Genuinely needed historical corrections use a suitable separate
  record/history — never silent edits of a terminal SR.

## 6. Deletion (LOCKED — V1)

- SRs must not be deleted in V1: no hard delete, no soft-delete-then-purge, no bulk
  deletion, no automatic deletion.

*End of BD-SR-004.*
