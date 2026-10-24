# IS-08 APPROVAL PREPARATION — AUDIT & DECISION PACKAGE

```text
Record ID:      IS08-APPROVAL-PREP-01
Date:           2026-10-01
Author:         Hermes (AI Manager / Lead Architect) — evidence and options only
Authority:      Human Business Authority owns every decision listed below
Status:         READ-ONLY PREPARATION. No document modified. No status changed.
Implementation: NO code / schema / migration / UI / deployment change.
```

> This record does not approve IS-08. It states what approving it would mean, what
> conflicts exist, and which choices belong to HBA. Nothing here is executed.

---

## 1. What IS-08 is

`/home/anto/akuntansiku/docs/40-SPECIFICATION/IS-08-ui-user-interface.md`

| Property | Value |
|---|---|
| Version | 1.0 |
| Status | **PROPOSED — DRAFT FOR REVIEW** |
| Length | 171 lines, 15 sections |
| Scope | UI *behavior* for internal CRM operation |
| Explicitly out of scope | Customer/PIC portal UI (gated by IS-06), notification surface, **all visual design** |
| Implementation content | None — no HTML/CSS/JS, no component library, no framework, no mock |

Its job is to state what the UI **must show and must never show** — not how it looks.

---

## 2. Audit — is IS-08 sound?

Verified against the canonical corpus and the implemented codebase.

| Check | Method | Result |
|---|---|---|
| §2.1 WO lifecycle matches canon | Compared to `migrate.py` CHECK constraint | **MATCH** — `DRAFT/OPEN/IN_PROGRESS/WAITING_APPROVAL/CLOSED/CANCELLED` |
| §2 deprecated terms excluded from code | Grepped `app/` for `ASSIGNED`, `ON PROCESS`, `COMPLETED`, `SKIP_TEMPORARY` | **CLEAN** — every hit is a comment *forbidding* the term |
| §7 Visit types | Compared to `visit.py` + schema | **MATCH** — `INITIAL` / `ON_PROCESS` only; `FINAL` never a type |
| §8 Report FINAL only after CLOSED | Read `report.py::mark_final` | **MATCH** — enforced; no FINALIZE action exposed |
| §9 separation of duties | Read `approval.py::approve_report` | **MATCH** — reviewer must be Manager/Admin, not the technician |
| §9 reopen numbered cycles | Read `approval.py::reopen` | **MATCH** — CLOSED-only, numbered, unlimited |
| §11 Outstanding not overdue/SLA | Read `reporting/outstanding.py` | **MATCH** — attention-only, no timer |
| §4/§5 SR and WO citations | Checked `BD-SR-*`, `CD-11 §§2–9` exist | **EXIST** |
| §11 history citation | Checked `CD-11 §20` | **EXISTS** |
| §12 AC-1..AC-6 | Each acceptance criterion is testable | **TESTABLE** |

**Audit verdict: IS-08 is internally consistent, canonically traceable, and matches the
implemented behaviour. No contradiction found.**

---

## 3. FINDING 1 (P1) — the portal conflict

### What HBA chose

Answer 4 = **B: portal pelanggan included** in the first UI build.

### What IS-08 says

> §1: *"Out of scope (GATED): customer/PIC external portal (IS-06)…"*
> §3: *"External (customer/PIC) UI is out of scope here and fully GATED by IS-06 (still DRAFT)."*
> §13: *"GATED / deferred: external customer portal UI (IS-06, still DRAFT)…"*
> §12 AC-4: *"customer/public portal surfaces are absent or clearly marked as IS-06-gated."*

### The conflict

The chosen scope includes the portal. IS-08 explicitly excludes it and requires it to be
absent. **These cannot both hold.**

### Why it exists

IS-06 (`IS-06-customer-projection-portal.md`) carries status:

> **DRAFT / PROPOSED — NOT LOCKED**

The portal's behaviour was deliberately left unapproved while its business expectation was
open. That expectation is now resolved (HBA D-01A = RETAIN), so the gate can be lifted — but
only by an explicit HBA act.

### Options

| Option | Meaning | Consequence | Further authorization |
|---|---|---|---|
| **A** | Approve IS-08 as-is; portal deferred to a later increment | First build covers internal only. Portal comes after IS-06 is approved | None beyond IS-08 |
| **B** | Approve IS-08 **and** IS-06, then write the portal UI spec | Portal included, as chosen. Requires an additional UI-behaviour spec for the portal (IS-08 does not cover it) | Approving IS-06 + authoring a portal UI spec |
| **C** | Approve IS-08 with a recorded deviation allowing the portal | Portal included without approving IS-06 | **NOT RECOMMENDED** — builds portal UI on unapproved behaviour |

Option C is listed only for completeness. It would place implementation ahead of the
specification gate that IS-00 §13 exists to enforce.

---

## 4. FINDING 2 (P2) — what approval actually grants

IS-00 §13 states:

> *"Implementation authorization is a separate explicit Human decision. It is NOT granted by
> IS progress, by any single workstream, or by this document."*

So approving IS-08 does **not** authorize building UI. Two separate acts exist, and HBA must
say which one is being given.

| Act | Effect |
|---|---|
| Approve IS-08 | The specification stops being a draft. Build is still not authorized |
| Authorize UI build | Work may start, within the approved specification |

The UI baselines (`REV7-SR`, `REV1-WO`) carry the same caution in their own record:
*"UI approval ≠ canonical amendment ≠ implementation authorization."*

---

## 5. FINDING 3 (P3) — the promised deviation log is missing

`IS-00 §14`, item `O-10`, states the IS-08 deliverable includes:

> *"Logged + dispositioned in IS-08 deviation log"* — for Figma prototype business-rule questions.

IS-08 contains **no deviation log**, and **no Figma prototype exists** in the repository.

Two readings, both cheap to settle:

| Reading | Action |
|---|---|
| No deviation ever arose (nothing to log) | Add one line to IS-08 recording that explicitly |
| The deliverable was overlooked | Author the deviation log section |

This is a documentation-completeness gap, not a business decision. It blocks nothing.

---

## 6. FINDING 4 (P3) — styling is still undecided

HBA chose React + TypeScript as the **architecture** decision and deliberately separated
styling as its own decision. Styling remains **undecided**.

It does not block IS-08 approval — IS-08 explicitly excludes visual design (§1, AC-5). It
does become blocking at the first real screen, because a screen must be styled somehow.

---

## 7. What approval would change

| Item | Before | After approval |
|---|---|---|
| IS-08 header status | `PROPOSED — DRAFT FOR REVIEW` | `APPROVED` |
| IS-08 version | 1.0 | 1.0 (no content change) or 1.1 (if the deviation log is added) |
| Portal UI behaviour | Unspecified and gated | Unchanged, unless Finding 1 option B is chosen |
| Build authorization | Not granted | **Still not granted** — separate act |
| Canonical business rules | Unchanged | Unchanged |

---

## 8. Evidence basis

- `docs/40-SPECIFICATION/IS-08-ui-user-interface.md` (read in full)
- `docs/40-SPECIFICATION/IS-06-customer-projection-portal.md` (header status)
- `docs/40-SPECIFICATION/IS-00-is-specification-governance-master-plan.md` §§13, 14
- `docs/40-SPECIFICATION/IS-FINAL-implementation-specification.md` §§10–12
- `docs/10-DECISIONS/CD-11-*.md` §§11, 20, 21, 22
- `crm/app/migrations/migrate.py`, `crm/app/exec/{visit,report,approval}.py`,
  `crm/app/reporting/outstanding.py`, `crm/app/wo/wo.py`
- `docs/90-AUDIT/UI-BASELINE-APPROVAL-AND-RECONCILIATION-RECORD.md`

---

## 9. Boundary

This record:
- modified no document;
- changed no status;
- approved nothing;
- created no business decision;
- authorized no implementation.

Every decision in §§3–6 belongs to HBA.

*End of preparation record.*
