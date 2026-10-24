# BD-SR-003 — SR Content Boundary V1 (O-03)

```text
Decision ID: BD-SR-003
Title: SR Content Boundary V1 — Request vs JOB vs Commitment (O-03)
Mode: Business Decision
Status: LOCKED — V1 (BUSINESS AUTHORITY APPROVAL 2026-09-23)
Business Authority Approval: YES (HANDPROMPT — LOCK O-03 SR CONTENT BOUNDARY V1, 2026-09-23)
Implementation Authorization: NO
```

> Defines what may live in an SR and what may not be mistaken for JOB, Scope of Work,
> or work commitment. Consumes BD-SR-001, BD-SR-002, BD-SRWO-001 unchanged.
> Historical documents are untouched. No new entity, status, workflow, schema, or UI
> is created. O-04/O-05/O-10/O-11 and V2 remain out of scope.

---

## 1. Content definitions (LOCKED — V1)

1. **Requested Need** — need/request statement in the requester's language. Answers
   "why does this SR exist". Always a request, never a commitment.
2. **Requested Scope** — picture of the desired work extent. Even when worded
   finally (e.g. "Ganti fuel filter."), while inside an SR its status stays
   **request**, never JOB.
3. **Reference Item / Service** — lookup pointers to item/service masters (Fuel
   Filter, Major Overhaul, Inspection, …) aiding understanding/estimation. Never a
   commitment; never a JOB; never auto-converted into a JOB.
4. **Free Text / Description** — narrative: complaints, customer/operator info,
   communication results, early context, suspected causes, requests, follow-up notes.
   Status **as-reported**, not final technical fact.
5. **Preliminary Technical Information** — unverified early technical info. May be
   recorded in SR as as-reported initial info, but **SR is not a technical execution
   record**. Official technical findings come only from Visit/WO/Report per existing
   canonical rules (CD-11 §§13–14, 17–18).
6. **Commercial Information** — commercial info as context only (need estimates,
   price requests, customer budget, quotation references, negotiation notes). Official
   quotations, binding approvals/commitments, final figures, and transactions stay in
   the relevant commercial documents/processes. SR never becomes a quotation or
   transaction record.
7. **Customer Agreement / Context** — informal consent context (e.g. "Customer setuju
   via WA, siap dijadwalkan"). Never a system action, never a JOB, never auto-creates
   a WO or an assignment. WOs are still formed by a `CREATE_WO` holder (O-06).
8. **JOB** — exists only inside a WO (`1 JOB = exactly 1 WO`). No SR Job, no JOB in
   SR, no JOB as SR child, no Additional Work entity, no SR→JOB auto-conversion.

## 2. SR → WO boundary (LOCKED — V1)

> **SR provides request context. WO establishes work.**

When a WO is created: (1) the `CREATE_WO` holder reads the SR; (2) understands need,
requested scope, references, technical/commercial/agreement context; (3) establishes
JOBs from work actually agreed/authorized; (4) never via blind copy or
auto-conversion; (5) JOB content may equal, narrow, widen, or differ from the SR;
(6) no V1 rule compares SR text with JOBs. `source_sr_id` remains lineage/source
reference, not proof of identical content.

## 3. Boundary matrix (LOCKED — V1)

| Content | SR | JOB |
|---|---|---|
| Requested Need | Yes | No |
| Requested Scope | Yes | No |
| Reference Item/Service | Yes | No |
| Free Text / Description | Yes | No |
| Preliminary Technical Information | Limited | Not as preliminary info |
| Commercial Context | Yes, as information | Not an SR function |
| Customer Agreement/Context | Yes, as context | Not automatically JOB |
| Final Work / Commitment | No | Yes, via WO |
| Technical Execution Record | No | Lives in execution/Visit/Report |
| Formal Commercial Commitment | No | Not a JOB function |

*End of BD-SR-003.*
