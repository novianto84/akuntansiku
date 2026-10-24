# HBA DECISION RECORD — Submit=Checkout final, pengesahan modul, izin edit aditif, otorisasi eksekusi (2026-10-08)

```text
Record ID:      HBA-DECISIONS-10
Date:           2026-10-08
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decisions as stated by HBA in group chat 2026-10-08
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record. Execution is a separate governed step.
```

> This record captures the HBA decisions stated in the group chat session 2026-10-08.
> It does not itself edit any canonical specification document. Canonical
> materialization (if needed) is a separate, explicitly-scoped step.

---

## Decisions (verbatim intent)

1. **Submit = auto checkout (FINAL, no further confusion).** HBA states: "Jam keluar itu adalah jam pada saat submit. itu saja. jangan dibikin bingung lagi." Reading: `check_out_at` = server timestamp at the moment of submit, applied to all OPEN visits. No per-visit vs active-visit distinction. LOCK.

2. **Auto stamp + GPS approved.** HBA states auto stamp and GPS are included in the submit=checkout approval. Verified basis (checked 2026-10-08): `crm/app/exec/approval.py::submit` already stamps `check_out_at = CURRENT_TIMESTAMP` onto OPEN visits that are checked-in but not checked-out; `crm/app/exec/visit.py` and `crm/app/migrations/migrate.py` (visits table: `check_in_at`, `check_out_at`) contain NO gps/latitude/longitude column. Therefore: auto stamp = already implemented shape, CONFIRMED. GPS = approved in principle but NOT YET IMPLEMENTED — requires a separate additive migration; no GPS column is created by this record.

3. **Reminder module — APPROVED.** Manual-only reminder as implemented is authorized under the locked manual baseline (Admin/Manager/Sales). No scheduler, no auto-send.

4. **Outstanding module — APPROVED without overdue.** Outstanding as monitoring/attention concept only. No overdue timer, no SLA, no escalation.

5. **Material module — APPROVED without price.** Quantity-only usage recording plus PENDING→LINKED inventory seam. CRM never values or prices; no valuation/costing.

6. **Exec module — APPROVED under CD-11.** Visit/Report/Approval/Closure flow as implemented is authorized under CD-11 WO operational boundary. No business rule created or changed.

7. **Stale index/control documents — HBA permits additive correction.** `ARCHITECTURE_LOCK.md` §Implementation Authorization and stale `DECISION_REGISTER.md` rows may be corrected additively (no history rewrite).

8. **Corrective spec — APPROVED and execution AUTHORIZED.** HBA states: "Saya sahkan spec korektifnya, dan saya otorisasi eksekusinya." Covers the C-3/C-2/C-5 corrective packages (cards `t_9fdb5c92`, `t_074bbe2c`) and the WP-11 corrective spec pass. Execution proceeds through the governed path.

## Boundary

- This record modifies no canonical document, changes no document status, creates no business rule beyond the HBA statements above.
- GPS implementation (additive migration for location columns) is NOT authorized by this record beyond the in-principle approval; it needs its own scoped execution step.
- Portal publication/serving mechanism (IS-06 O-01/O-02) remains OPEN — deferred architecture task, not a V1 blocker for embedded serving.

## Cheapest next step

Execute the authorized C-3/C-2/C-5 + C-1 closure work through the governed path, then apply the additive stale-document corrections. GPS migration scoped separately after V1 is running.

*End of decision record.*
