# TADR-12 — CONTROLLED AMENDMENT RECORD

## Status Reconciliation: HBA D-01A = RETAIN

```text
Record ID:      TADR-12-AMEND-01
Subject:        TADR-12 — Read Models / Projections
Nature:         CONTROLLED AMENDMENT — status reconciliation only
Created:        2026-09-30
Authorization:  HBA — "AUTHORIZE MILESTONE 6 DOCUMENTATION RECONCILIATION"
Decision basis: HBA D-01A = RETAIN (FINAL / LOCKED)
Technical direction changed: NO
Original approval history altered: NO
Implementation authorized by this record: NO
```

---

## 1. Purpose

This record reconciles **status wording** in `TADR-12 — Read Models / Projections` with the
subsequent Human Business Authority decision **D-01A = RETAIN**.

It is a **documentation/status reconciliation**. It is **not** a new architecture decision, and it
does **not** modify the technical direction approved on 2026-09-21.

---

## 2. Original Approval Preserved

| Field | Value |
|---|---|
| Original status | APPROVED |
| Original approval | HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — **2026-09-21** |
| Approved direction (unchanged) | Hybrid — live queries for internal/operational views; **materialized reviewer-gated snapshots** for Customer and QR views (evidentiary stability: *what the customer saw is fixed*); every projected row carries its source link plus freshness/publication metadata |
| Original approval history | **UNCHANGED** — not rewritten, not erased, not superseded |

The wording "Snapshot vs. live as a business expectation is NOT decided here" in the Approved
Direction remains an accurate **scoping statement**: TADR-12 as an architecture record did not decide
that business expectation. It was subsequently decided by HBA, not by architecture.

---

## 3. Subsequent HBA Business Decision

| Field | Value |
|---|---|
| Decision | **HBA D-01A = RETAIN** |
| Status | FINAL / LOCKED |
| Established | 2026-09-30 |
| Semantics | Previously presented customer-facing content remains available as the **historical record of what was presented**; the current authoritative condition remains **distinguishable** from that historical customer-facing record; RETRACT semantics do not apply; the historical record must remain reproducible |
| Related | **D-01B** — semantic freshness requirement only; **no numeric freshness SLA** |

**Business expectation vs architecture mechanism (explicitly distinguished):**

| Aspect | Owner | Status |
|---|---|---|
| Whether previously presented content remains available (RETAIN) | **Business / HBA** | **RESOLVED** — D-01A |
| Semantic freshness guarantee (no intentional presentation of known-obsolete content) | **Business / HBA** | **RESOLVED** — D-01B |
| Snapshot materialization implementation | Architecture | OPEN — architecture |
| Refresh cadence / policy | Architecture | OPEN — architecture |
| Propagation timing | Architecture | OPEN — architecture |
| Cache duration | Architecture | OPEN — architecture |
| Replication behavior | Architecture | OPEN — architecture |
| Drift handling / monitoring | Architecture | OPEN — architecture |
| Serving mechanism (incl. no-download mechanism) | Architecture | OPEN — architecture |

---

## 4. Changes Applied to TADR-12

| # | Section | Before | After | Nature |
|---|---|---|---|---|
| 1 | Approved Direction (after the "NOT decided here" sentence) | *(no note)* | Additive note: "Subsequent HBA business decision (2026-09-30) — HBA D-01A = RETAIN" + statement that the approved technical direction is unchanged and that refresh/propagation/cache/replication/drift/serving remain architectural; pointer to this record | Additive only — original sentence retained verbatim |
| 2 | Dependencies / Deferred Decisions | "Customer publication model gate (partly blocking: snapshot-vs-live expectation, publication mechanism)." | "Customer publication model: the **business expectation is RESOLVED by HBA D-01A = RETAIN** … The publication/serving **mechanism** … remains an architecture decision. No longer partly blocking on the business-expectation aspect." | Status reconciliation |
| 3 | Open Questions | "Snapshot refresh cadence and staleness policy (gated on business expectation)." | "Snapshot refresh cadence and staleness policy (**architecture/mechanism**; the business expectation is resolved — HBA D-01A = RETAIN)." | Status reconciliation |

**Nothing else in TADR-12 was modified.** No technical direction, alternative, trade-off, business
rule, security impact, audit impact, or approval boundary was altered.

---

## 5. Related Status Reconciliation Outside TADR-12

The TADR matrix row for TADR-12 lives in
`docs/30-ARCHITECTURE/TECHNICAL_ARCHITECTURE_FINALIZATION.md` (not in TADR-12 itself):

| Section | Before | After |
|---|---|---|
| TADR matrix | `| TADR-12 | Read Models / Projections | Partly blocking (customer publication model) |` | `| TADR-12 | Read Models / Projections | Non-blocking (business expectation resolved — HBA D-01A = RETAIN; serving/refresh mechanism remains architectural) |` |

Recorded here for traceability because it is the TADR-12 status statement.

---

## 6. Hash / Traceability

TADR-12 has **no `.sha256` companion file**. Traceability is provided by:

| Artifact | Reference |
|---|---|
| Original record | `docs/30-ARCHITECTURE/TADR/TADR-12.md` |
| Original approval | 2026-09-21 (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL) — preserved in file header |
| Decision basis | HBA D-01A = RETAIN (2026-09-30) |
| Authorization basis | `AUTHORIZE MILESTONE 6 DOCUMENTATION RECONCILIATION` |
| Cross-indexes | `ARCHITECTURE_LOCK.md`, `AI_CONTEXT_INDEX.md` reference TADR status — their consistency is noted as follow-up, not modified here |

### Governed hash changes in the same execution

| File | Old SHA-256 | New SHA-256 |
|---|---|---|
| `DECISION_REGISTER.md` | `64d99ab7a1090b7ee5bab6b31aef47913e6888490a597fbc434b0ab695109323` | `d6d3262e5e38ea801a44948c6d2dea722a7ffbf1aec74ac6327fac8c849c1c44` |

`DECISION_REGISTER.md.sha256` was regenerated and verifies (`sha256sum -c` → OK).

---

## 7. Explicit Non-Changes

| Item | Status |
|---|---|
| TADR-12 technical direction | **UNCHANGED** |
| TADR-12 original approval history (2026-09-21) | **UNCHANGED** |
| TADR-12 status (APPROVED) | **UNCHANGED** |
| New TADR created | **NO** |
| New architecture decision created | **NO** |
| New business decision created | **NO** |
| `PUBLISH` state or action introduced | **NO** |
| Numeric freshness / SLA introduced | **NO** |
| Implementation authorized | **NO** |

---

*End of TADR-12 controlled amendment record.*
