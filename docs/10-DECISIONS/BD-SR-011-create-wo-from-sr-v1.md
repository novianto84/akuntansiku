# BD-SR-011 — Create WO from SR V1 (O-11)

```text
Decision ID: BD-SR-011
Title: Create WO from SR — Business & Technical Boundary V1 (O-11)
Mode: Business Decision
Status: LOCKED — V1 (BUSINESS AUTHORITY APPROVAL 2026-09-23)
Business Authority Approval: YES (HANDPROMPT — BA APPROVAL O-11, atomicity + duplicate conversion clarifications, 2026-09-23)
Implementation Authorization: NO
```

> O-11 governs ordinary WO creation using an SR as reference. The explicit Human decision
> reconciles this document with SR V1 lifecycle `OPEN → CLOSED`; the SR is never
> converted into a WO. Existing WO authority, formation guards, failure handling,
> duplicate constraints, lineage, and audit intent are preserved except where they
> necessarily depended on the superseded SR status transition. Historical data remain untouched.

---

## 1. Definition

When starting from an SR, the actor invokes the existing `CREATE_WO` action (UI label:
`Create WO`) and may reference the SR as context/source. This forms a **new,
independent WO**; there is no separate `CREATE_WO_FROM_SR` business action or
permission. The SR is never converted, transformed, or copied. It remains a distinct
request entity and stays `OPEN` when a WO is created.

## 2. Trigger

Explicit actor initiation from an SR in an allowed state (§4). No automatic,
scheduled, or event-driven initiation exists.

## 3. Actor

Only CREATE_WO holders per BD-SR-005 §2–3 (Admin unrestricted; Manager and Sales by
default; Coordinator/Technician only if granted). Requester status, Company linkage,
and Customer PIC confer no `CREATE_WO` authority.

## 4. Preconditions

- **SR prerequisite:** status `OPEN`. Before starting a new WO preparation, check for
  an active source-associated WO DRAFT and for an already-formed source-associated WO.
  An active DRAFT is resumed, not duplicated; an official WO follows the existing
  source-reference duplicate guard in §9.
- **WO prerequisite:** all applicable WO rules satisfiable at formation (responsible
  person for IN_PROGRESS, Unit posture, workspace context).
- **JOB prerequisite:** actor establishes ≥1 JOB at formation from agreed work —
  never auto-derived (see §6).
- **Assignment prerequisite:** follows canonical assignment rules (ASSIGN_WO);
  assignment itself is an event after WO formation, not part of WO creation.

A `CLOSED` SR is ineligible (terminal, no reopen V1).

## 5. Agreement / assignment boundary

The operative basis is **B: the internal authorized actor holds a valid basis to
establish the work** (customer request + follow-up understanding, agreement context
where present, or genuine Manager assignment instruction). Not A (customer approval
is not universally required — requiring it would contradict O-06 direct WO), not C
(no explicit approval record is canonically required to form a WO; the mandatory
pre-CLOSED review remains the quality gate). No new approval layer is created.

## 6. SR content → WO content

| SR Field/Content | WO Handling | Rule |
|---|---|---|
| Requested Need | Reference only (visible during preparation) | Never transferred as WO data |
| Requested Scope | Reference only | Never auto-JOB; actor re-establishes |
| Description | Reference only | Context, not WO content |
| Reference Item/Service | Reference/inspiration only | Selectable view; each JOB re-established by actor |
| Requester | Available via lineage (SR), not copied | No requester field auto-filled on WO |
| Company | Derived via Unit binding / SR reference, not copied as claim | No Company from unverified claims |
| Location | Re-established for WO/Unit as needed | WO/Unit location is its own fact |
| Commercial notes | Reference only | Never WO data |
| Agreement context | Reference (basis note) | Supports §5-B basis; creates no obligation |

No blind-copy rule exists in either direction; no text-comparison rule exists (V1).

## 7. JOB creation boundary

**No JOB is ever auto-created from Requested Scope, References, or any SR content.**
At WO preparation the system presents SR content as read-only reference; the actor
defines every JOB explicitly before the WO becomes official. Example: SR "Genset
tidak bisa start / Check genset dan perbaiki bila perlu / ref Fuel Filter" yields
zero automatic JOBs — the actor establishes e.g. `Inspect Starting System` (and only
`Replace Fuel Filter` if actually agreed), each as a deliberate act.

## 8. Direct WO interaction

Direct WO (`source_sr_id = NULL`) is unaffected: identical lifecycle, guards, and
rules after creation. The only difference is lineage absence.

## 9. SR relationship and transaction boundary

WO formation, the originating-SR reference (`source_sr_id`), and the required audit
lineage follow the existing BD-SR-011 atomicity boundary: they succeed or fail
together. The SR is not part of the WO state transition and remains `OPEN`; there is
no SR lifecycle transition on WO creation. A saved WO `DRAFT` is not an official
Related WO and does not close or change the SR. Where existing permissions allow
visibility it may be shown separately; only the original draft creator may continue
it, consistent with CD-11 §DRAFT. An active source-associated DRAFT is resumed rather
than duplicated. The official Related WO is presented when the WO reaches `OPEN`.

## 10. Failure / rollback & duplicate guard

- **A (creation fails):** SR remains `OPEN`; no partial WO persists as official and no incomplete lineage is committed.
- **B (WO without complete JOBs):** preparation remains a DRAFT; it is not an official Related WO and the SR remains `OPEN`.
- **C (WO + ≥1 JOB + guards met):** WO becomes official (`OPEN`), its SR reference/lineage is recorded, and the SR remains `OPEN`.
- **D (user cancels before save):** nothing changes on either side.
- **E (active source-associated DRAFT exists):** do not create another active DRAFT; route to the existing DRAFT. Only its creator may Continue Draft.
- **F (official WO with `source_sr_id` already exists):** block another source-associated WO under the existing V1 duplicate guard and surface its Related WO.
- **G (SR is `CLOSED`, retry):** blocked — terminal, no reopen V1.

## 11. Conceptual UI flow (non-visual)

SR Detail → `Create WO` (existing `CREATE_WO` authority and SR `OPEN`) → WO
preparation (SR content shown as reference; actor defines JOBs + WO data) → official
WO formation with source reference/audit lineage → Related WO shown when WO is `OPEN`.
The SR remains `OPEN`; the UI never presents this as a conversion.

## 12. Audit & lineage

Minimum: actor, server timestamp, SR id, WO id, ordinary WO-creation action, and
`source_sr_id` lineage — existing pattern, append-only. The SR remains editable while
`OPEN` under BD-SR-004; only separately closing it makes it immutable.

## 13. Security boundary

WO creation remains restricted to existing `CREATE_WO` holders; requester/Company/PIC
confer no WO authority. SR lineage grants no external access; existing access
governance applies unchanged. Draft visibility and continuation remain subject to
existing permissions and CD-11 creator ownership.

## 14. Resolved constraints retained under the final Human decision

- **Atomicity:** WO formation, source reference/lineage, and required audit succeed or
  fail together under the existing approved boundary. No SR status change is part of
  that transaction; the SR remains `OPEN`. A DRAFT is not an official Related WO.
- **Official-WO duplicate guard:** retain the existing V1 source-reference rule of at
  most one official WO per SR and surface the existing WO rather than creating another.
- **Active-DRAFT behavior:** when an active source-associated DRAFT exists, do not
  create another active DRAFT; route to the existing DRAFT. Continue Draft is only for
  its original creator under CD-11 §DRAFT. No takeover/transfer/claim is introduced.
- **Failure handling and lineage:** preserve the existing all-or-nothing WO formation,
  source-reference lineage, and append-only audit requirements; failure leaves the SR
  `OPEN` and does not create a partial official WO.

*End of decision. O-11 remains LOCKED — V1 as reconciled by explicit Human decision.*
