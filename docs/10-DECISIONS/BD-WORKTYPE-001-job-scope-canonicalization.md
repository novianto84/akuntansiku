# BD-WORKTYPE-001 Rev.A — JOB / SCOPE Canonicalization

```text
Decision ID: BD-WORKTYPE-001 Rev.A
Title: JOB / SCOPE Canonicalization
Mode: Business Decision
Status: APPROVED / CANONICAL — BUSINESS AUTHORITY APPROVAL
Business Authority Approval: YES (2026-09-23)
Implementation Authorization: NO
Supersedes: all prior work-model drafts (same-day rule, 24h timeout, automatic new WO,
  automatic ON HOLD, automatic Add Job proposals — all withdrawn, none ever canonical)
```

> Single canonical business concept for work within a Work Order. This decision establishes
> terminology authority for JOB/SCOPE alongside (never replacing) CD-11. CD-11 historical
> content is untouched; the operative amendment lives in `CD-11-Appendix-A-job-scope-terminology.md`.

---

## 1. Purpose

Menetapkan vocabulary bisnis yang sederhana dan konsisten untuk merepresentasikan pekerjaan
dalam Work Order tanpa menciptakan beberapa entity/concept yang sebenarnya merupakan
pekerjaan yang sama.

## 2. Canonical Vocabulary (APPROVED)

- **JOB** — *pekerjaan yang menjadi bagian dari sebuah Work Order. JOB dapat belum selesai;
  status pelaksanaannya ditentukan oleh mekanisme execution/checklist yang berlaku.* One work
  concept regardless of origin, timing of discovery, or nature. Context/attributes (origin,
  nature) may qualify a JOB; they never subclass it. A WO may have zero or more JOBs — no
  minimum cardinality is locked. A JOB, where present, belongs to exactly one WO.
- **SCOPE** — *daftar/lingkup pekerjaan yang ditetapkan untuk sebuah WO.* A structure/list,
  not a JOB kind. JOBs live in/relate to it. No `Scope Item` entity without an explicit
  business requirement (none exists).
- **ADDED DURING EXECUTION** — marker/context/provenance (never an entity): the JOB surfaced
  during execution **and was actually performed**. Never for planned, suggested, found-but-undone
  work.
- **FINDING** — condition/fact found. Not a JOB.
- **DIAGNOSIS** — technical analysis/conclusion. Not a JOB; important to completion but not
  completion itself.
- **RECOMMENDATION** — suggested but not-yet-performed action. Not a JOB. Performed later, it
  is represented as a JOB at performance time under applicable provenance rules.
- **OUTCOME** — result/verdict of a Visit or execution (incl. ON HOLD). Not a JOB.

## 3. Terminology Mapping (APPROVED)

| Legacy / conversational term | Canonical treatment |
|---|---|
| Issued Job | Not separate → JOB (pre-execution-scope context). Conversational label only |
| Add Job | Not entity → JOB + Added During Execution marker. "Add Job" survives only as historical wording |
| Corrective Job | Not separate → JOB + nature/category = Corrective, only where needed |
| Current / Planned / Pending Job | Not business concepts — do not use. Unfinished SCOPE JOBs use checklist state + ON HOLD |
| Task | Not a synonym of JOB. "Task" keeps only its existing canonical denials (no auto-task creation, CD-11 §11) and its implementation-task sense |
| Scope Item | No new entity without explicit business requirement |

Historical occurrences ("Add Job" in CD-11 record, IS-01 E-27) remain valid period text,
interpretable via this mapping. No LOCKED document is silently rewritten.

## 4. Business Rules (APPROVED)

1. One WO contains zero or more JOBs; one JOB belongs to exactly one WO (no minimum locked).
2. A SCOPE JOB may be CHECKED (done + evidence) or UNCHECKED (unfinished).
3. An unfinished SCOPE JOB whose obligation continues in the same WO follows ON HOLD
   (reason mandatory; next Visit, same WO; WO stays IN_PROGRESS + indicator). ON HOLD is an
   outcome about an unfinished SCOPE JOB — primarily issued/predefined obligation, especially
   SERVICE — never a synonym of Recommendation, never a WO state.
4. A JOB surfacing during execution exists as a JOB **only if actually performed**, carrying
   the Added During Execution marker. Planned/Pending/UNCHECKED "Add Job" in any implicit or
   explicit form is prohibited.
5. Finding/Diagnosis/Recommendation never are, imply, or auto-generate JOBs, ON HOLD, or new WOs.
6. A performed Recommendation becomes a JOB at performance time (with applicable provenance
   marker), never retroactively. No automatic Finding → Scope transform.
7. No automatic WO creation from Recommendation; no automatic closure from JOB completion;
   closure only via approval (`APPROVE REPORT ⇒ WO = CLOSED`).

## 5. Relations (APPROVED)

```text
WO → SCOPE → JOB → CHECKED / UNCHECKED (→ ON HOLD → next Visit, same WO)
Finding → Diagnosis → Recommendation            (terminal as data)
Finding → Diagnosis → performed work → JOB (+ Added During Execution marker)
WORK MODEL ≠ SERVICE TYPE ≠ JOB ≠ SCOPE
```

Work Model (SERVICE / INSPEKSI-VISIT / EMERGENCY TROUBLESHOOT — definitions per approved
reconciliation) describes the WO execution pattern; Service Type (CD-11 §16, unchanged)
classifies nature of service; both stay orthogonal to JOB. Emergency carries multiple ordinary
JOBs across multiple visits; no same-day/24h rule; no auto-closure. Inspection outputs never
convert into JOBs by themselves. Emergency technical objective is complete when the assigned
troubleshooting objective is achieved per work conditions (diagnosis alone is not automatic
completion); submission (`→ WAITING APPROVAL`) and formal closure (approval `→ CLOSED`,
Report FINAL) follow the canonical lifecycle unchanged.

## 6. Acceptance Criteria (APPROVED)

JOB is one work concept; SCOPE is the WO work list; no Issued/Add/Corrective Job entities; no
Task synonym; Added During Execution is a marker; SCOPE JOBs may be unfinished and use ON HOLD;
Finding/Diagnosis/Recommendation are not JOBs and auto-generate nothing; performed
Recommendations become JOBs at performance time; Work Model and Service Type stay separate from
JOB; no automatic WO creation or closure; historical/audit meaning preserved; no redundant
entities; no LOCKED-governance change outside the amendment mechanism.

## 7. Deferred (NOT decided by this decision)

JOB nature/category formal field + value list; full JOB status enumeration beyond
CHECKED/UNCHECKED/ON HOLD; Issued↔scope-checklist technical mapping verification (IS-02);
source/ownership attribute shape (IS-05); final DB schema; API contracts; UI layout;
permission detail.

## 8. Authority & Traceability

- Approves: BA approval 2026-09-23 (proposal BD-WORKTYPE-001 Rev.A FINAL PROPOSED).
- Operative CD-11 amendment: `docs/10-DECISIONS/CD-11-Appendix-A-job-scope-terminology.md`.
- Resolves: IS-01 OQ-01 (work-model/template readiness — work-model axis decided; template
  mechanics remain IS-02 detail).
- Authorizes: IS-02 consumption of JOB/SCOPE vocabulary. Authorizes nothing else:
  schema / migration / API / UI / deployment / Programmer handoff = NO.

*End of BD-WORKTYPE-001 Rev.A — APPROVED / CANONICAL.*
