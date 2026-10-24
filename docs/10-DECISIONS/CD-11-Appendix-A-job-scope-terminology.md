# CD-11 Amendment Appendix A — JOB / SCOPE Terminology

```text
Parent document: docs/10-DECISIONS/CD-11-service-work-order-operational-boundary.md
  (SIGNED-OFF / LOCKED / CLOSED — historical content UNCHANGED by this appendix)
Authority: BD-WORKTYPE-001 Rev.A — APPROVED / CANONICAL (BA APPROVAL 2026-09-23)
Status: APPROVED / CANONICAL appendix (operative clarification + single usage restriction)
```

This appendix resolves the §12 `TIDAK → UNCHECKED` branch against the approved rule that
`Added During Execution` applies only to JOBs actually performed. It adds operative meaning;
it does not rewrite, delete, or reinterpret any historical CD-11 sentence.

## A.1 Usage restriction on CD-11 §12 (`TIDAK → UNCHECKED`)

The CD-11 §12 input branch `Sudah dikerjakan? TIDAK → UNCHECKED` records a **scope entry
yang belum CHECKED** only. It never creates an Add Job. A JOB with Added During Execution
context exists solely upon actual performance, consistent with BD-WORKTYPE-001 Rev.A §4
Rule 4 (Planned/Pending/UNCHECKED "Add Job" prohibited in any implicit or explicit form).

## A.2 Terminology normalization (CD-11 §§1, 3, 11, 12)

Historical occurrences of the name "Add Job" in the CD-11 record are valid period text and
remain readable. Operatively they are read per BD-WORKTYPE-001 Rev.A §3:

- "Add Job" → JOB + Added During Execution marker (actually performed only).
- "Added During Execution scopes" (CD-11 §11) → JOBs carrying the marker.
- "Scope Execution Checklist" → the SCOPE frame; checklist entries are scope entries
  carrying UNCHECKED / CHECKED state.

## A.3 What this appendix does NOT do

- Does not alter CD-11 lifecycle, approval, closure, evidence, HM, review, cancellation,
  reopen/re-create, publication, reminder, or workspace rules.
- Does not create schema, API, UI, or implementation obligations.
- Does not resolve IS-01 OQ items beyond the work-model axis (recorded in BD-WORKTYPE-001 Rev.A §8).

*End of CD-11 Amendment Appendix A.*
