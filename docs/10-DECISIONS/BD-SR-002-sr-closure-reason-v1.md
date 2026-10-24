# BD-SR-002 — SR Closure Reason V1 (O-02)

```text
Decision ID: BD-SR-002
Title: SR Closure Reason V1 — Managed List + Closure Rules (O-02)
Mode: Business Decision
Status: LOCKED — V1 (BUSINESS AUTHORITY APPROVAL 2026-09-23)
Business Authority Approval: YES (HANDPROMPT — LOCK O-02 CLOSURE REASON SR V1, 2026-09-23)
Implementation Authorization: NO
```

> Minimal closure-reason rules for the sole V1 SR closure transition, `OPEN → CLOSED`.
> The explicit Human decision leaves WO creation independent of SR closure. Historical
> records/terminology are untouched. No new approval, KPI, SLA, reopen, schema, or UI
> is created by this documentation reconciliation.

---

## 1. Managed closure reason list (LOCKED — V1, complete — no others exist)

| Reason (code / label) | Meaning | Keterangan |
|---|---|---|
| `DUPLICATE` / Duplikat | SR ganda atas kebutuhan yang sama dan sudah tercakup SR lain | Optional; may record the retained SR |
| `WITHDRAWN` / Ditarik kembali | Peminta/customer membatalkan request | Optional |
| `DECLINED` / Ditolak | Diputuskan tidak melanjutkan request | Optional |
| `OTHER` / Lainnya | Alasan di luar tiga reason di atas | **Mandatory** |

The list applies to the sole transition into CLOSED: `OPEN → CLOSED`.

## 2. Closure rules (LOCKED — V1)

- `closure_reason` is **mandatory** on `OPEN → CLOSED`.
- `Keterangan` is mandatory **only** when reason = `OTHER / Lainnya`; otherwise it
  may be empty.
- Closure reason is **immutable** once the SR is `CLOSED`.
- `CLOSED` stays terminal. No reopen in V1.
- Creating a WO, saving a WO DRAFT, or forming an official WO does not close the SR
  and does not require a closure reason. The SR remains `OPEN` until separately closed.

## 3. Audit (pattern only — no new schema/database)

Follow the existing audit pattern (cf. CD-11 §28): actor, server timestamp,
closure action/event, SR-ID as object, closure reason, keterangan where present.
WO source-reference/history is recorded under the applicable existing lineage/audit
rules; there is no separate SR conversion status or action.

*End of BD-SR-002.*
