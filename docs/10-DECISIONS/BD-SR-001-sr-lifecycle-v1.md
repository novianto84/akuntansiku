# BD-SR-001 — SR Lifecycle V1 (O-01)

```text
Decision ID: BD-SR-001
Title: SR Lifecycle V1 — Statuses, Transitions, Terminality (O-01)
Mode: Business Decision
Status: LOCKED — V1 (BUSINESS AUTHORITY APPROVAL 2026-09-23)
Business Authority Approval: YES (HANDPROMPT — LOCK O-01 SR LIFECYCLE V1, 2026-09-23)
Implementation Authorization: NO
```

> Final V1 lifecycle for Service Request. This section incorporates the explicit Human
> decision superseding the earlier O-01 state model. WO creation is governed by
> `CREATE_WO` and source-reference lineage (BD-SRWO-001); it does not create an SR state.
> Historical terminology/data remain untouched.

---

## 1. SR Statuses — canonical V1

| SR Status | Meaning | Entry trigger | Allowed next status | Terminal? |
|---|---|---|---|---|
| OPEN | Request recorded and remains active until separately closed | SR created; remains OPEN when a WO is created | CLOSED | No |
| CLOSED | Request explicitly closed with a closure reason | Authorized Close SR from OPEN | — | **Yes** |

Follow-up, clarification, negotiation, proposal, and WO creation are activities/events
while the SR is `OPEN`, not SR statuses. The SR and WO are distinct entities. WO
lineage/reference is not a status. A saved WO `DRAFT` is not an official Related WO;
show an official Related WO only when the WO reaches `OPEN` under canonical WO rules.

## 2. Transitions V1 — complete list (no others exist)

1. `OPEN → CLOSED`

Prohibited: any transition out of `CLOSED`; no reopen in V1. Creating or continuing a
WO, including a saved DRAFT, does not change the SR status.

## 3. WO relationship and authority boundary

- A normal `CREATE_WO` action may reference the originating SR (`source_sr_id`, per
  BD-SRWO-001 O-07); the WO remains independent and the SR remains `OPEN`.
- Official WO formation follows canonical WO rules and the BD-SR-011 guards. The
  official Related WO relationship is presented once the WO is `OPEN`.
- A WO `DRAFT` is separate from an official Related WO. Where existing permissions
  allow visibility, it may be displayed as a draft; only its original creator may
  continue it (CD-11). An active DRAFT is resumed rather than duplicated.
- No separate SR conversion state/action is part of this lifecycle. Historical
  labels/records remain unchanged.

## 4. Terminality

- `CLOSED` is the only terminal SR status.
- No reopen in V1; no transition out of `CLOSED`.

## 5. V1 scope boundary

Closure-reason taxonomy (O-02); SR content/fields (O-03); SR permission matrix (O-05);
retention/visibility (O-08); KPI (O-09); SR form (O-10); detailed WO creation guards,
transaction/failure semantics, and relationship binding (O-11); reopen, multi-WO per
SR, snapshots, intermediate statuses, and other V2 matters remain governed or deferred
by their respective sources.

*End of BD-SR-001.*
