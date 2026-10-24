# BD-SRWO-001 — SR → WO V1 Scope (O-06 Authority + O-07 Lineage)

```text
Decision ID: BD-SRWO-001
Title: SR → WO V1 Scope — Manager Authority (O-06) + SR→WO Lineage (O-07)
Mode: Business Decision
Status: LOCKED — V1 (BUSINESS AUTHORITY DECISION 2026-09-23)
Business Authority Approval: YES (O-06/O-07 V1 prompt, 2026-09-23)
Implementation Authorization: NO
```

> V1 scope lock. Fills two previously open items (prior audit O-06, O-07) without
> reopening any LOCKED decision. Historical documents are untouched; operative effect
> is this document plus the register entry. The §DO-NOT-CHANGE list (17 items) from
> the deciding prompt remains in full force and is not repeated here except where
> directly referenced.

---

## 1. O-06 — Manager CREATE_WO & ASSIGN_WO (LOCKED — V1)

For CRM V1, **Manager holds default authority for `CREATE_WO` and `ASSIGN_WO`**.

Manager may:

1. create a WO with an SR source reference (entry-point label: `Create WO`);
2. create WO directly without SR where the work is genuinely established by Manager
   instruction (a work-establishing instruction, not general information/guidance);
3. determine/establish JOBs within the WO (subject to the 1..N minimum on official WO,
   BD-WORKMODEL-001 §3);
4. assign technicians per the canonical assignment rules (CD-11 §§2, 7–8).

Flows (unchanged semantics, either entry path):

```text
Manager instruction (work-establishing) → WO → JOB → Assignment → Execution
SR context → Create WO → WO (source reference) → JOB → Assignment → Execution
```

### 1.1 Consistency basis (no conflict)

- `ASSIGN_WO` default Manager + Coordinator: verbatim CD-11 §7 ("Hanya pemegang
  `ASSIGN_WO` (default Manager + Coordinator)").
- `CREATE_WO`: CD-11 §4 holds Sales as default, Technician as grantable, and
  "role lain configurable". This decision fills that configurability slot with a BA
  default for Manager. It does not remove Sales default, Technician grantability, or
  any other configuration — it only establishes Manager default for V1.
- No additional approval layer validates Manager authority itself. All other
  canonical gates still apply to Manager-created WOs unchanged: same lifecycle,
  responsible-person requirement for IN_PROGRESS, 1..N JOBs, Unit binding before
  CLOSED, mandatory Manager/Admin review before CLOSED, technician never approves
  (CD-11 §§2, 4–6, 19; BD-WORKMODEL-001 §3).

## 2. O-07 — SR → WO lineage V1 (LOCKED — V1)

For CRM V1, **a WO carries an optional reference to its source SR**:

```text
WO.source_sr_id = optional (conceptual; no storage/column decision is made here)
```

- WO from SR: `SR-001 → WO-015` with `source_sr_id = SR-001`.
- Direct WO: `Manager instruction → WO-016` with `source_sr_id = NULL`.
  NULL means direct WO, not SR-based.

### 2.1 Relationship model (conceptual, V1)

```text
SR ───────────────→ WO
       optional
WO: 0..1 source SR (NULL = direct)
SR: source/reference/lineage for WO; never a parent/container of WO
JOB: lives only in WO (1 JOB = exactly 1 WO, unchanged)
```

### 2.2 Terminology (LOCKED — V1)

Use the UI label `Create WO`. The phrase `WO dibuat berdasarkan SR` may describe
context/reference, but not a separate business action or permission. Never wording
that implies SR transforms into WO. SR remains a distinct `OPEN` request; WO remains
the independent work/execution record and references the SR where applicable.

### 2.3 Consistency basis (no conflict)

- SR optional + substantial path `Request → Commercial/Approval → New WO` (CD-11 §3);
  WO-side optionality and at-most-one originating request path per WO (IS-01 R-07,
  optionality LOCKED, upper bound DERIVED) — this decision consumes both unchanged.
- `CREATED_FROM` lineage stays reserved for WO re-create (CD-11 §28) and is NOT
  reused here; the SR→WO link is a source reference, not identity lineage.
- Blind-copy prohibition preserved: JOBs are established from agreed work at WO
  creation, never auto-copied from SR references (cf. BD-WORKTYPE-001 §4 Rules 5–6).

## 3. V1 scope limitation (NOT a permanent rule)

For V1, **one SR is supported to yield one WO** in the source relationship. This is a
V1 delivery scope limit, explicitly NOT a permanent business rule. The architecture
must NOT be locked as "one SR may forever yield only one WO". Multi-WO from one SR
(`SR-001 → WO-015, WO-021`) may be considered for V2 if business need arises.

V1 explicitly excludes: dedicated relationship entity; multi-WO relationship model;
approval snapshot; conversion snapshot; relationship type; any other complex mechanism.
(Conversion/approval snapshots stay deferred, as in the prior audit.)

## 4. Preserved constraints (unchanged, for the record)

Manager-created and SR-based WOs alike remain subject to: canonical WO lifecycle
(DRAFT→OPEN→IN_PROGRESS→WAITING APPROVAL→CLOSED + CANCELLED terminal); DRAFT-not-WO
with 1..N JOB minimum from OPEN/submit; 1 WO = 1 Unit before CLOSED; assignment
events with reason + audit; Visit/Report/Evidence/HM/finding rules; mandatory review;
separate SR/WO histories; SR Closed ≠ WO Closed. No new Service Type, Work Model,
status, Visit Type, timer, SLA, threshold, score, routing, or automatic rule is
created by this decision.

*End of BD-SRWO-001.*
