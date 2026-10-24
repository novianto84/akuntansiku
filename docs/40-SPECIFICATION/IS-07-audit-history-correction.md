# IS-07 — Audit, History & Correction Specification

```text
Document ID: IS-07
Title: Audit, History & Correction Specification
Version: 1.2 (additive v1.1→v1.2: addendum HBA-DECISIONS-30/31/34 — diskusi WO bukan peristiwa audit; transisi penanda terbitan adalah peristiwa audit. Settled v1.1 content unchanged; no new audit family beyond those recorded HBA decisions.)
Status: LOCKED / CANONICAL — BUSINESS AUTHORITY APPROVAL (review: PASS WITH MINOR FINDINGS → S-01 RESOLVED; MUST/SHOULD FIX 0; UNSOURCED 0)
Lock record: settled normative content authoritative as reviewed; OPEN/DEFERRED items remain unresolved.
Scope: Audit ownership; event families; append-only/history semantics; correction lineage;
  reopen behavior; state-history separation; Report refresh relationship; authorization and
  evidence interaction; retention/open gates.
Authority: AI Manager / Lead Architect. Business Authority owns all rules.
Sources: CD-11 §§2,9,18,28 (CD11-006/007/008/012); IS-01 §12/H-01…H-06; IS-02 §§14,19 +
  decomposition §16; AB-01; TA-01 v1.1 §§16–17; TADR-08/09; BD-SR-011 §12; IS-03 denials.
ID basis: BA authorization for IS-07 at docs/40-SPECIFICATION/IS-07-audit-history-correction.md.
Implementation: NO subsystem/tech/code/TASK-001. Technology-neutral.
```

> IS-07 owns audit event definitions, history semantics, and correction lineage. IS-04/IS-05
> reference them. IS-07 never owns any domain lifecycle (WO/Visit/Report/SR all keep theirs).

---

## 1. Scope

What is recorded, how history stays trustworthy, and how correction/reopen lineage works —
for service execution and, by reference pattern, anywhere the same principles apply. Excludes:
lifecycle ownership (kept by owners); retention windows (planning); storage tech; UI.

## 2. Audit Ownership

The audit plane observes; it never owns, mutates, or substitutes for business state (AB-01 §N;
TADR-08). Exactly one definitional owner for audit semantics: this specification. No competing
audit-event or correction-lineage definitions may exist in IS-04/IS-05 (joint interface rule).

## 3. Event Families

WO creation with SR source reference + duplicate attempt (no SR status change); JOB establishment; assignment/Take-Over/Self-Add
(+refusal reasons); Visit create/check-in/check-out/COMPLETED/correction; checklist CHECK
transitions; Added-JOB entries; findings/HM/evidence capture + opt-outs (+reasons); outcome
recording (+reasons); submission; review decisions; Final Conclusion draft/modification/official;
acknowledgement presence/absence (+reason); cancellation chain; reopen/re-create lineage;
link establishments (identity + requester); evidence approval/eligibility/supersession/retention
actions (objects owned by IS-05); authorization denials. (Decomposition §24; CD-11 §28.)

## 4. Append-Only Semantics

Events are never edited or deleted; corrections are new events with lineage. Minimum per event:
actor, server timestamp, action, object (+scope/lineage ids), reason where canonical,
before/after where canonical, correlation identifiers for cross-event lineage (TA-01 §17 pattern,
cited not redesigned).

## 5. History Semantics

Point-in-time truth is derivable from ordered events on stable identity pointers (no snapshot
mechanism invented; BD-G01-G02 §6 pattern cited). Correction history is controlling data
(CD-11 §28): within correction history, the current position is the latest non-superseded event.
Official results (approved Report, official Conclusion) are distinct from the controlling trail.
General current-state ownership (WO/Visit/Report/SR) remains with the domain owners; audit
observes and reconstructs, never substitutes them (§8).

## 6. Correction Lineage

Numbered cycles, unlimited count (no technical maximum — CD-11 §28). Pre-CLOSED: WAITING-APPROVAL
loop events (request-correction / audited direct-edit with mandatory reason / direct-close with
reason). Post-CLOSED: REOPEN (CLOSED-only, same identity) vs RE-CREATE (new identity,
`CREATED_FROM`, no assignment carry). Minor/substantive sub-typing: OPEN (OQ-09) — single
correction object, no sub-types modeled.

## 7. Reopen / Correction Behavior

REOPEN returns CLOSED → IN_PROGRESS preserving number/Report/assignment linkage and prior history.
No second Report is created on correction or reopen (Report refreshes from current Visit data —
IS-02 §12). CANCELLED is absorbing terminal (no reopen; CLOSED never cancelled).

## 8. State-History Separation

Lifecycles (SR/WO/Visit/Report-readiness) are owned exclusively by their domains; audit records
their transitions but never drives, duplicates, or substitutes them. No audit-owned state machine
exists.

## 9. Report Refresh / Recompute Relationship

Report derivation re-reads authoritative Visit data on every correction/reopen event; no
per-correction Report versions Phase 1; readiness flips only on WO CLOSED (IS-02 §12). Refresh is
a read consequence, never a write into execution records.

## 10. Authorization Interaction

Denials (IS-03 §9–10) are first-class auditable events with actor, target, and governing rule.
Applicant≠approver actions (link approvals, evidence reviews) record both sides. Authorization
itself stays with IS-03 authorities; audit only observes.

## 11. Evidence Interaction (IS-05 objects — reference only)

Capture/opt-out/review/eligibility/supersession/retention events are defined here as event shapes;
the objects and state dimensions they describe are owned by IS-05. Interface dependency recorded;
no object redefinition.

## 12. Retention / Open Gates

Dual time capture (event-time + record-time) proceeds; precedence convention OPEN (O-04).
Retention windows are planning detail (OPEN). Outstanding surfacing OPEN (OQ-06). Acknowledgement
alternative types OPEN (OQ-16). None blocks audit structure.

## 13. Traceability

§§2–5 → TADR-08 + CD-11 §28 + IS-01 H-01…H-06. §6 → CD-11 §§2,28 (CD11-007/008) + TADR-09.
§7 → CD-11 §§18,28. §8 → AB-01 §N. §§9–11 → IS-02 §§12,19 + IS-05/IS-03 ownership.
§12 → O-04/OQ-06/OQ-16 + planning. Classification: LOCKED/DERIVED except §12 items.

## 14. Acceptance Criteria

AC-1 ownership exclusive to audit plane. AC-2 all §3 families defined with minimum fields.
AC-3 append-only + controlling-history demonstrable. AC-4 no lifecycle owned or duplicated.
AC-5 no second Report on correction/reopen. AC-6 OPEN gates marked. AC-7 zero UNSOURCED.
AC-8 joint checkpoint passed.

## 15. Self-Audit

Authorized path ✅ · DRAFT ✅ · owns audit/lineage only (no lifecycle, object, or contract
redefinition) ✅ · no OPEN resolved ✅ · no subsystem/tech ✅ · no TASK-001 ✅ · traceability
complete ✅ · neutral ✅ · single-file scope ✅.

---

## Addendum HBA-DECISIONS-30 / -31 / -34 (2026-10-24) — diskusi bukan audit; penanda terbitan diobservasi audit

- **Diskusi Work Order bukan peristiwa audit.** Pesan diskusi adalah catatan komunikasi internal:
  ia tidak masuk keluarga peristiwa §3, tidak menjadi bagian trail pengendali (§5), dan tidak pernah
  dipakai sebagai pengganti perintah kerja atau persetujuan (HBA: "hanya berupa catatan"). Satu
  pemilik definisi audit (§2) tidak berubah; IS-01/IS-03 tidak menambah model audit tandingan.
- **Pemberitahuan panggilan bukan audit.** Pemberitahuan dalam aplikasi adalah permukaan UI (IS-08),
  bukan peristiwa audit.
- **Transisi penanda terbitan berkas tingkat Unit diobservasi audit.** Penetapan dan pencabutan
  penanda terbitan oleh Manager/Admin (objek milik IS-05) mengikuti pola peristiwa approval/
  eligibility/supersession yang sudah ada: aktor, waktu server, objek, keadaan sebelum/sesudah.
  Objeknya tetap milik IS-05; bentuk peristiwanya milik dokumen ini.
- Nol keluarga peristiwa baru dan nol peredefinisian audit di luar itu.

---

*End of IS-07 v1.2 (addendum HBA-DECISIONS-30/31/34, 2026-10-24).*

