# HBA DECISION RECORD — Submit = Check-out (single button, server timestamp)

```text
Record ID:      HBA-DECISIONS-04
Date:           2026-10-05
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decision as stated by HBA in session 2026-10-05
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record.
```

> This record captures the HBA decision stated in session 2026-10-05. It does not
> itself edit `IS-02`, `CD-11`, `DECISION_REGISTER.md`, or any other canonical
> document. Canonical materialization (if needed) is a separate,
> explicitly-scoped step.

---

## Decision

**HBA decision: no separate check-out button. The submit action automatically
records the server finish timestamp, so the check-out obligation remains
fulfilled.**

### What HBA stated

- Tidak butuh tombol khusus untuk check-out; submit = checkout.
- Tombol submit otomatis mencatat waktu selesai dari server sehingga kewajiban
  check-out tetap dipenuhi.

### What this decision is and is not

| Aspect | Reading |
|---|---|
| Nature | UI/UX simplification: one button (submit); check-out obligation fulfilled behind the scenes via server timestamp |
| Effect on locked rule | None — the LOCKED mandatory check-out rule (CD-11 §10; IS-02 §4: check-in wajib, check-out wajib, Visit tidak dapat COMPLETED tanpa check-out, server timestamp) is PRESERVED, not waived |
| Effect on business rules | None. No business rule created, changed, or reinterpreted |
| Effect on code | None by this record. The derived implementation shape below is flagged, not authorized |

### Verified basis (checked against canon + real code, 2026-10-05)

- Canon: `docs/10-DECISIONS/CD-11-service-work-order-operational-boundary.md`
  §"Check-in / Check-out" (check-in wajib; check-out wajib; Visit tidak dapat
  COMPLETED tanpa check-out; server timestamp); `docs/40-SPECIFICATION/
  IS-02-service-execution-specification.md` §4 (check-in/out per Visit both
  mandatory; a Visit cannot COMPLETE without check-out).
- Code: `crm/app/exec/visit.py::check_out` (per-Visit) vs
  `crm/app/exec/approval.py::submit` (per-WO, IN_PROGRESS → WAITING_APPROVAL) —
  different levels; `visit.complete` currently enforces no check-out
  precondition (known divergence, HBA-DECISIONS-03 §2).
- Prior record: `HBA-DECISIONS-03` §2 (technician clock = server timestamp
  only) — consistent with this decision, not contradicted.

### Derived implementation shape (flagged for authorization, not a decision)

Submit (per WO) stamps the server finish time onto the open Visit(s) as their
`check_out_at`, satisfying the mandatory check-out precondition before
completion/submit proceeds. No separate check-out button in the UI. The
`check_out` domain action is retained (not removed); only its trigger changes
to automatic-at-submit. Requires explicit implementation authorization before
any code/schema change (HBA-DECISIONS-03 §1 covers already-built work only;
new work needs authorization BEFORE it starts).

### Cheapest next step

Explicit implementation authorization for this small derived change, then a
single scoped edit (submit auto-stamps server `check_out_at`) with test —
no canonical amendment needed since the locked rule is preserved.

---

## Not decided by this record

- Whether auto-stamp applies per open Visit or only the active one (deferred to
  implementation proposal).
- Canonical materialization of this record into IS-02/CD-11 wording (additive
  only; needs explicit scope).
