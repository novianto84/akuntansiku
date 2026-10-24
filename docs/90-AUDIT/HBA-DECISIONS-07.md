# HBA DECISION RECORD — Authorisasi perbaikan penuh C-3 (isolasi workspace pada list path)

```text
Record ID:      HBA-DECISIONS-07
Date:           2026-10-07
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decision as stated by HBA in group chat 2026-10-07
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record. Authorization granted; execution is a separate governed step.
```

> This record captures the HBA decision stated in the group chat session 2026-10-07.
> It does not itself edit any canonical specification document. Canonical
> materialization (if needed) is a separate, explicitly-scoped step.

---

## Decision

**HBA decision: authorize the FULL corrective fix of CP-C finding C-3**
("Cross-workspace isolation is unenforced on list paths and on workspace-less
tables — REPRODUCED", `docs/90-AUDIT/CP-C-CROSS-WORKSTREAM-CONSISTENCY-LOG.md` §3).

### What HBA stated

- "saya izinkan perbaikan penuh" (full fix authorized).
- Asked whether the decision can be locked — recorded and final below.

### Approved fix scope (as presented to HBA in the session)

1. Filter every collection/list path by the caller's active workspace
   (companies, work orders, and all list helpers currently issuing unfiltered
   `SELECT *`).
2. Add workspace scoping to the workspace-less tables that have a derivable
   workspace path (`service_requests`, `units`, `contacts`, `visits`,
   `report_revisions`, `reminders`, `wo_approval_events`, and the remaining
   tables named in the finding), to be mapped exactly during implementation.
3. Add a durable workspace-membership table per user (replacing reliance on
   `internal_users.default_workspace_id` alone, so membership can actually be
   enforced).
4. Add explicit negative-path tests proving cross-workspace denial on every
   list path.

### What this decision is and is not

| Aspect | Reading |
|---|---|
| Nature | Implementation authorization for a corrective work package |
| Effect on locked rules | None — enforces the IS-11 isolation invariant (I-10 / TADR-05: one DB, app-level isolation); no business rule created, changed, or reinterpreted |
| Effect on audit duties | None waived — isolation-relevant events and rejections remain audited per IS-11 §15 |
| Scope boundary | The full fix as presented. Any expansion beyond it requires a new authorization |

### Cheapest next step

Register the work package (kanban) and execute it through the governed path
(`.opencode/bin/opencode-governed run --agent mitrasp-manager`), with the
negative-path tests as the acceptance evidence.

---

## Not decided by this record

- Exact final column mapping per workspace-less table (deferred to the
  implementation proposal, additive and reversible).
- Canonical materialization wording in IS-11 / TADR documents (separate
  explicitly-scoped step).
- The parallel C-1 / C-2 / C-4 / C-5 corrections from the same CP-C log
  (each still needs its own HBA decision).

*End of decision record.*
