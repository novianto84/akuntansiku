# HBA DECISION RECORD — Build Authorization, Technician Clock, Evidence V1, Gate Openers

```text
Record ID:      HBA-DECISIONS-03
Date:           2026-10-03
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decisions as stated by HBA in session 2026-10-03
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record. Execution tracked in §6.
```

> This record captures the HBA decisions stated in session 2026-10-03. It does not
> itself edit `IS-00`, `IS-FINAL`, `DECISION_REGISTER.md`, `ARCHITECTURE_LOCK.md`, or
> any other document. Those edits are a separate, explicitly-scoped step (§6).

---

## 1. Decision — Authorization for work already executed

**HBA decision: issue the implementation authorization NOW, on the basis of the
existing repository state, and acknowledge the governance failure.**

### What HBA stated

- The work is already running; the authorization is not present.
- Taking the audit trail into account, HBA chooses to **issue the authorization now**
  and to **acknowledge the error**.

### What this decision is and is not

| Aspect | Reading |
|---|---|
| Nature | Acknowledgement of the actual state, recorded now — **not** retroactive legitimation of unauthorized work |
| Error acknowledged | The **governance layer** never produced a durable build-authorization artifact; the `EXECUTE BUILD — WORK PACKAGE [ID]` instruction survives in no repository or bridge file, so no authorization can be reconstructed from evidence |
| Effect on the existing code | The already-built backend (`crm/app`, WP-01…WP-10) and the internal UI are recorded as **built and now covered by an authorization issued at this date** |
| Effect on future work | Work that has not yet started requires an authorization **before** it starts |
| Effect on business rules | None. No business rule is created, changed, or reinterpreted |

### Verified basis (independently checked in session)

- `.opencode/ledger/governance-gate.jsonl` — 818 events; event types are
  `ENVELOPE_*`, `GATE_INITIALISED`, `LAUNCHER_*`, `HASH_PRIMITIVE_*`, `RESULT_*`,
  `ORCH_*`, `EXECUTION_PROVIDER_CHANGED`. **No implementation-authorization event type
  exists**, and none was recorded.
- No file in `/home/anto/akuntansiku` or the bridge workspace contains the
  `EXECUTE BUILD — WORK PACKAGE [ID]` instruction.
- `ARCHITECTURE_LOCK.md` §"Implementation Authorization" reads **NO**;
  `DECISION_REGISTER.md` carries `implementation NOT authorized` on the SR rows.

---

## 2. Decision — Technician clock (Visit start / finish)

**HBA decision: use server timestamps only. No manual input, no manual edit. The value
is informational only, not a KPI. No audit-trail events are required for technician
start and finish.**

### What HBA stated

- The technician clock is a **system** concern in V1 — not an evidence concern.
- Start is taken from the server timestamp at the moment work starts.
- Finish is taken from the server timestamp at the moment the technician submits.
- No input and no edit by the user.
- It is information only, not a KPI, so the exposure is not critical.
- No audit-trail requirement is imposed for the start/finish pair.

### Conformance note

This **complies** with the locked rule rather than departing from it:
`IS-02 §4` / `CD-11 §10` require *"server timestamp; no free timestamp editing
(corrections via controlled audited mechanism)"*. The present implementation
(`app/exec/visit.py::check_in` / `check_out`) instead stores a **caller-supplied**
timestamp verbatim and accepts `None` — a divergence from the locked rule. The decision
above removes the divergence.

### Derived implementation shape (flagged for confirmation, not a business decision)

| Item | Derived treatment |
|---|---|
| `check_in_at` | Server timestamp at check-in; client-supplied value ignored or rejected |
| `check_out_at` | Server timestamp at check-out where check-out occurs; otherwise the submission timestamp |
| The `check_out` action | **Not removed** by this decision; it keeps its role, with its timestamp server-set |
| Audit events for check-in / check-out | **Deferred, not waived** — see the note below |
| Actor recording | Unchanged — visit creator / attendance records as today |
| Effect of the current defect | The permanent check-out block (a `NULL` check-in timestamp) disappears, because the server always stamps |

**Deferral note (recorded, with consequence).** `IS-07 §3` registers
`Visit create/check-in/check-out/COMPLETED/correction` as event families, and `IS-07 §4`
requires actor + server timestamp per event. The decision above does **not** waive that
obligation; it **defers** the check-in/check-out pair. The consequence, stated so it is
not lost: with no event trail for the pair, a wrong clock has **no audited correction
path**, while `IS-02 §4` requires corrections to run through a controlled audited
mechanism. HBA's stated reason for accepting this is that the value is informational and
not a KPI. The deferral must be carried as **owned debt**, not recorded as "not
required".

**Enforcement divergence (verified in code, 2026-10-03).** `IS-02 §4` also requires that
a Visit **cannot COMPLETE without check-out**. `app/exec/visit.py::complete` performs no
such check, and the active development database holds **three COMPLETED Visits with both
`check_in_at` and `check_out_at` NULL** (visit ids 4, 5, 6). This is a second divergence
from the same locked rule and is independent of the timestamp-source defect.

**Derived shape for `check_out` (recommended, pending HBA confirmation).** The
`check_out` action is retained; only its timestamp source changes. `submit` then
requires that check-out has occurred, which preserves the locked rule *and* gives the
technician the single-button experience HBA described. HBA's literal phrasing (finish
timestamp taken purely at submit, check-out no longer meaningful) would **soften** the
locked mandatory-check-out rule and therefore requires the change path
(proposal → HBA decision → canonical recording → build), not a direct edit.

The treatment of `check_out` is a derived interpretation of the HBA statement and is
flagged for confirmation; it creates no business rule.

---

## 3. Decision — Evidence in V1

**HBA decision: evidence enters V1.**

### What this covers

- The **locked floor** becomes the default: nameplate, hour meter, before, after.
- **Opt-out with a mandatory reason** on CHECKED scope (CD-11 §17; IS-05 §6).
- The **Dynamic Configuration Panel remains deferred** — the configuration domain is
  left as a named seam, not built.
- **Storage**: evidence capture and opt-out reasons are recorded through the **general
  trace/event table built first** (see §4), because IS-07 §11 defines capture and
  opt-out as event shapes.

### Why this is consistent with canon (not merely a preference)

CD-11 §17 makes evidence event-driven and not globally mandatory in Phase 1, but when a
scope is marked complete without evidence the **reason is mandatory**. Evidence and its
opt-out reasons are customer-safe-eligible content for a CLOSED WO. Without a place to
store them, that part of the locked rule cannot be satisfied — so building the mechanism
is required by the locked rule, not added by choice.

---

## 4. Decision — Ordering: general trace/event table first

**HBA decision (accepted): the general trace/event table is built before the evidence
work.**

### Verified basis

- `app/exec/approval.py` is the **only** module writing events
  (`wo_approval_events`: SUBMIT / REQUEST_CORRECTION / EDIT / CLOSE / REOPEN).
- No events are written by: `wo/wo.py` (open, start, cancel, add_job),
  `wo/assignment.py` (assign, take-over, self-add approve/refuse), `exec/visit.py`
  (create, check-in, check-out, complete), or `exec/report.py` (ensure, assemble,
  mark_final — only `report_revisions` exists).
- `IS-07 §3` registers event families for all of the above.
- `app/interfaces.py` carries a docstring-only `Audit` seam reserved since WP-01 and
  never filled.
- `wo_approval_events` **cannot** be reused as the general store: its `event_type`
  CHECK is fixed to five approval values and `work_order_id` / `actor_user_id` are
  NOT NULL.

### Consequence

A new, additive general trace/event table (new migration; no existing table altered)
is the cheapest correct shape. Scope of event families to be filled is recorded in §6.

---

## 5. Decision — Gate openers

**HBA decision: acknowledge the specification master plan, and approve the consolidated
specification.**

| Act | Target | Effect |
|---|---|---|
| Acknowledgement | `IS-00` (master plan / implementation gate) | The governance document used as the implementation gate is acknowledged by HBA |
| Approval | `IS-FINAL` (consolidated implementation specification) | Approved as the implementation input |

### Honest status note (reported, not worked around)

The gate in `IS-00 §13` lists five requirements. These two acts address the acceptance
requirements; the remaining items are **not yet satisfied**:

| # | Requirement | State after these acts |
|---|---|---|
| 1 | IS-01…IS-10 DONE per §7–§8 | **NOT YET** — IS-01 carries "acknowledgement per IS-00 §7/§9 required"; IS-02 carries "pending BA acceptance of this verdict"; IS-09 and IS-10 remain PROPOSED (their headers raise them via the IS-FINAL acceptance gate) |
| 2 | CP-C cross-workstream consistency check complete **with log** | **NOT YET** — no CP-C log artifact exists |
| 3 | Unresolved blocking decisions = NONE | **PARTIAL** — blocking items already decided by HBA but not materialized (permission-matrix content; publication model; reminder; timestamp; deployment) |
| 4 | IS-FINAL approved | **MET** by this decision |
| 5 | Scope deterministically derivable from IS-FINAL | **TO BE ESTABLISHED** in the authorization text |

**Therefore:** the IS-FINAL approval is recorded as an HBA decision, but the gate is not
yet formally closed. The CP-C log must be produced, and IS-01 / IS-02 require their own
acknowledgement, before an authorization can claim the gate path is satisfied. If HBA
prefers not to wait, the alternative is an explicit scoped waiver with the consequence
recorded — the two options were put to HBA; **this record states the full-gate path was
chosen**, and the residual items above remain open.

---

## 6. Not decided by this record

| Item | Owner |
|---|---|
| Permission to edit the stale index/control documents (`ARCHITECTURE_LOCK.md` §Implementation Authorization; `DECISION_REGISTER.md` historical rows incl. the `BRIDGE_CONTRACT` PENDING line and the three decided-but-unmaterialized gates) | HBA |
| Acknowledgement of `IS-01` and `IS-02` | HBA |
| Approval of `IS-06` (customer portal specification) | HBA |
| Selection of the publication/serving **mechanism** and freshness mechanism (IS-06 O-01/O-02) | HBA / architecture |
| Retroactive status of work already executed, beyond the acknowledgement in §1 | HBA |
| Whether the technician-clock derived shape in §2 (in particular the `check_out` treatment) is confirmed | HBA |
| Whether the event families filled in the first trace increment are exactly Visit + WO cancellation, or wider | HBA |

---

## 7. Execution plan (derived — tracked here, not a business decision)

Steps to be executed once §6 items are settled. Each step is additive and reversible.

| Step | Content | Basis |
|---|---|---|
| E-1 | **Produce the CP-C cross-workstream consistency log** (IS-00 §13 item 2) — a read-only consistency pass over IS-01…IS-10 with the log as its artifact | IS-00 §§8, 13 |
| E-2 | **Authorize + build the general trace/event table** (new migration; no existing table altered), filling the `interfaces.py` `Audit` seam for the event families whose implementation already exists | §4 |
| E-3 | **Fix the technician clock** — server-set check-in/check-out timestamps; client value ignored/rejected; no audit events for the pair | §2 |
| E-4 | **Build the evidence mechanism** — locked floor as default, opt-out + mandatory reason on CHECKED scope, storage via E-2's table, configuration panel deferred as a named seam | §3 |
| E-5 | **Write the authorization record for work already executed**, naming the scope that exists and the date of issuance | §1 |
| E-6 | **Materialize the decided-but-unrecorded HBA decisions** (permission-matrix content, publication model, reminder, WO timestamp, deployment) and correct the stale index/control documents — *pending HBA edit permission* | §6 |

E-1 is read-only and can be produced without further authorization. E-2 and E-3 are the
two items HBA identified as cheapest and most urgent.

---

## 8. Boundary

This record:

- modified no canonical document;
- changed no document status;
- created no business rule;
- authorized nothing beyond the HBA statements above;
- reports the residual gate items rather than declaring the gate closed.

*End of decision record.*
