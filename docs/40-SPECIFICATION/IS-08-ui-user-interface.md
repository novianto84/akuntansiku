# IS-08 — UI & User Interaction Specification (V1)

```text
Document ID: IS-08
Title: UI & User Interaction Specification (V1)
Version: 1.2 (additive v1.1→v1.2: addendum HBA-DECISIONS-29/30/31/34 — revisi tampilan detail Unit arah D (empat permukaan) + permukaan Kotak Masuk pemberitahuan diskusi. Settled v1.1 content unchanged; no new business rule beyond those recorded HBA decisions.)
Status: APPROVED — HBA approval 2026-10-01 (see docs/90-AUDIT/IS08-APPROVAL-DECISIONS-01.md)
Authority: AI Manager / Lead Architect (specification author). Business Authority owns all rules.
Scope: Implementation-relevant UI behavior required for MitraSP CRM V1 internal operations.
  Customer/PIC external portal UI is GATED by IS-06 and is NOT defined here.
Sources: CD-11 (SIGNED-OFF/LOCKED/SIGNED); CD-01..CD-10 (LOCKED); BD-SR series (LOCKED);
  BD-WORKTYPE-001 + CD-11 Appendix A; BD-WORKMODEL-001 + CD-11 Appendix B; IS-01, IS-02,
  IS-03, IS-04, IS-05, IS-07, IS-11 (LOCKED/APPROVED); Architecture Baseline; TADR-01..18.
Implementation: NO code, no HTML/CSS/js, no component library, no framework, no screen mock,
  no API wiring. Technology-neutral. Cosmetic styling is explicitly OUT OF SCOPE.
```

> This document states *what UI behavior must exist and must never show* for V1. It does NOT
> prescribe visual design. UI must render the canonical lifecycle and vocabulary exactly as the
> business-domain specifications define them, and must never reintroduce deprecated terms.

---

## 1. Scope

In scope: UI behavior for internal MitraSP CRM operation — master data, SR, WO, JOB/SCOPE,
Visit, Report, Approval/Closure, evidence capture, history/audit views. Out of scope (GATED):
customer/PIC external portal (IS-06), notification surface, and all visual design.

## 2. Canonical Vocabulary Constraints (UI MUST NOT REINTRODUCE DEPRECATED TERMS)

These are hard UI constraints derived from CD-11 and reconciliation (§5 Prompt 1 = SETTLED):

1. **WO lifecycle shown must be exactly:** `DRAFT → OPEN → IN_PROGRESS → WAITING APPROVAL → CLOSED`;
   terminal `CANCELLED`. No `ASSIGNED`, no `ON PROCESS`, no `COMPLETED`, no `ON GOING` as a WO
   lifecycle state.
2. **UNASSIGNED** is rendered as a *condition/badge on the assignment*, never as a WO lifecycle
   state.
3. **ON PROCESS** appears only as a *Visit type* (second and subsequent visits), never as a WO status.
4. **INTERIM / CONTINUATION / FINAL** appear only as *report/work-stage classifications*, never as
   lifecycle or Visit types.
5. **Report FINAL** is achievable only when the WO is CLOSED.
6. **SR Requested Scope** is displayed as a *request context*, never labeled or structured as a JOB.
7. **JOB** is always shown inside exactly one WO (its owning WO).
8. **Visit completion** is displayed as an independent event that does not, by itself, close the WO.

## 3. UI Actor / Access Behavior

- UI surfaces are role- and scope-filtered per IS-03 authorities and IS-11 workspace/company
  scoping. A user sees exactly the surfaces their authority permits — no silent cross-workspace
  or cross-company browsing surface.
- Workspace selection is required before transactional operations (IS-11 active-workspace model).
- External (customer/PIC) UI is out of scope here and fully GATED by IS-06 (still DRAFT).

## 4. SR UI Behavior (V1)

- SR capture requires **Requester** plus **(Need OR Requested Scope)** (IS-04 A1 precondition).
- SR lifecycle rendered: **OPEN → CLOSED** (follow-up activity keeps SR OPEN; closure requires
  reason per BD-SR-002). V1 `CLOSE_SR` action is limited to Manager/Admin per final Human decision.
- SR list/detail shows history and any follow-up; creation from SR to WO is explicit and shows a
  `CREATED_FROM` lineage reference; SR remains OPEN when a WO is created from it.
- **Requested Scope UI is context, not JOB.** No "SR Job child" UI, no auto-conversion affordance.

## 5. WO UI Behavior (V1)

- Render the canonical lifecycle (§2.1). No artificial `ASSIGNED`/`COMPLETED`/`SKIP_TEMPORARY`
  status UI.
- **DRAFT** may exist with zero JOB (formation state). The transition to OPEN (official) requires
  **≥1 JOB**.
- Assignment surface: show responsible person; `UNASSIGNED` shown as a condition; no
  `IN_PROGRESS` submission while unassigned (IN_PROGRESS requires a responsible person).
- **Unit posture:** a WO may initially exist without a Unit where allowed; UI must require Unit
  before CLOSURE and must never present a fabricated/placeholder Unit (no-fake-Unit rule).
- Cancellation UI only from OPEN/IN_PROGRESS, terminal CANCELLED; CLOSED never cancellable.
- **One WO → one Report → N Visits**; the WO detail shows its Report and its Visit list.
- Emergency WO path: vocabulary per BD-WORKMODEL-001 (`Troubleshoot` for initial Emergency JOB);
  diagnosis alone does not equal completion.

## 6. JOB / SCOPE UI Behavior (V1)

- JOB is displayed as belonging to exactly one WO.
- **SCOPE** is a JOB property/state, never a separate JOB entity or separate menu item.
- No separate "Issued Job", "Add Job", or "Corrective Job" entities/menus.
- **Added During Execution** is a marker/flag (actually-performed, discovered during execution),
  not a separate JOB type.
- Finding / Diagnosis / Recommendation are **not JOB**; they render as report/record content
  attached to the appropriate Visit/Report, never as new JOB rows.
- JOB CHECK state transitions and Added-JOB entry require the executing actor (IS-04 A8); UI must
  gate these actions appropriately.

## 7. Visit UI Behavior (V1)

- Visit types rendered: **INITIAL** (first) and **ON PROCESS** (second & subsequent); system-determined,
  never user-chosen; `FINAL` never a Visit type.
- Check-in / check-out capture; attendance (auto-mark present for creator; assigned actors may be
  marked). Outcome set per CD-11 §11 (COMPLETED / NOT_PERFORMED / ON HOLD) with required reasons.
- Visit completion shows it closes the Visit, not the WO.
- Acknowledge (optional, non-gating) may be present.

## 8. Report UI Behavior (V1)

- Exactly **one Report per WO**, assembled from current Visit data (no per-Visit Report, no manual
  duplication UI).
- Report stage rendered; **FINAL only after WO CLOSED**. No "FINALIZE REPORT" action.
- **Final Conclusion:** technician drafts; approver accepts/corrects/establishes; technician can
  never set it unilaterally. History keeps draft/modification/final/actor/timestamp.

## 9. Approval / Closure UI Behavior (V1)

- Four phases remain distinct (never merged): execution-complete → report-readiness → approval →
  closure (`APPROVE REPORT ⇒ WO = CLOSED`).
- Approval UI is restricted to Manager/Admin and must prevent self-approval and
  approval-by-the-technician-of-own-WO (separation-of-duties invariant).
- Actions available during WAITING APPROVAL: REQUEST CORRECTION / direct-EDIT with reason /
  direct-CLOSE with reason. Show mandatory review coverage (checklist, photos, material, test,
  HM, Unit, findings).
- Exhibit the correction loop (pre-CLOSED) and REOPEN (CLOSED-only, numbered cycles) surfaces per
  CD-11 §§2,28.

## 10. Evidence Capture UI (V1)

- Evidence capture slots per IS-05 locked floor; opt-out-with-reason must be available.
- Show per-Visit evidence linkage and approval/publication states as defined by IS-05/IS-06 gate.
- No price/accounting/internal-commercial values in any customer-facing understanding (customer
  portal is IS-06-gated; internal UI may show operational values per role).

## 11. History / Audit UI (V1)

- Service History: date, WO, Unit, technician, findings, action, material, component replacement,
  HM, photos, test result, recommendation (CD-11 §20). One operational history with multiple
  contextual views (Unit View; Customer View; QR Unit view all scope-gated per IS-06).
- **Outstanding** is a monitoring/attention concept, never overdue/SLA/escalation/blocking; no
  overdue timer in Phase 1.
- Audit/correction lineage surfaces follow IS-07 (correction cycles, draft/approve, actor
  attribution "Recorded by", state-history separation). No invented lifecycle terms.

## 12. UI Acceptance Criteria

- AC-1: every screen renders the canonical vocabulary (§2) with zero deprecated terms.
- AC-2: WO lifecycle transitions are only DRAFT/OPEN/IN_PROGRESS/WAITING APPROVAL/CLOSED/CANCELLED.
- AC-3: SR Requested Scope is never shown as a JOB; JOB always shown in exactly one WO.
- AC-4: customer/public portal surfaces are absent or clearly marked as IS-06-gated (not built in V1
  ahead of that gate).
- AC-5: no cosmetic/styling specification present (out of scope); UI behavior only.
- AC-6: every UI rule above has a canonical citation.

## 13. Dependency / Open Items

- Depends on: IS-01 entities, IS-02 behavior, IS-03 authorities, IS-04 contracts, IS-05 evidence,
  IS-07 audit, IS-11 scoping.
- **GATED / deferred:** external customer portal UI (IS-06, still DRAFT), notification UI, automatic
  reminder surface, and any publication/consent **mechanism** (architecture). Publication permission
  (OQ-02) is already canonical; the D-01A business expectation is resolved (RETAIN).
- No new business rule is created by this UI specification.

## 13a. Deviation Log (O-10)

`IS-00` §14 item `O-10` required any Figma-prototype business-rule question to be logged and
dispositioned here, so a design prototype can never silently override a canonical rule.

**Entry: none. No deviation arose.**

- No Figma prototype exists in the repository; none was produced for this specification.
- Consequently no prototype question was ever raised against a business rule, and no rule was
  overridden, reinterpreted, or set aside by a design artifact.
- This section is recorded so the `O-10` deliverable is explicitly accounted for rather than
  silently absent.

If a prototype is later produced, its business-rule questions MUST be logged here before any
implementation relies on them.

## 14. Traceability

§2→CD-11 §§1–20 + Appendices A/B + BD-WORKTYPE/WORKMODEL; §4→BD-SR series + IS-04 A1–A3; §5→CD-11
§§2–9 + IS-04 A4–A6 + BD-SR-011 + no-fake-Unit; §6→BD-WORKTYPE-001 + Appendix A + IS-04 A8; §7→CD-11
§§10–14 + IS-02 Visit section; §8→CD-11 §18 + IS-02 Report section; §9→CD-11 §§2,19,28 + IS-02 Approval;
§10→IS-05; §11→CD-11 §20 + IS-07.

## 15. Self-Audit

Authorized by Prompt 1 mandate (specification completion) ✅ · vocabulary SETTLED preserved ✅ · no
code/mock/framework/styling ✅ · no new business rule ✅ · external portal correctly gated (IS-06) ✅ ·
OPEN items explicit ✅ · traceability complete ✅ · O-10 deviation-log item accounted for (2026-10-01,
no deviation arose) ✅.

---

## Addendum HBA-DECISIONS-29 / -30 / -31 / -34 (2026-10-24) — revisi tampilan detail Unit + permukaan Kotak Masuk

- **Detail Unit menjadi empat permukaan berurutan.** (1) **Profil Unit** — gabungan Tentang +
  Nameplate + Perlengkapan, dikelompokkan berjudul; field kosong tampil kosong, tidak dikarang.
  (2) **Riwayat** — histori per aktivitas; peristiwa menjadi urutan dasar, tanggal dokumen menjadi
  penanda; dokumen yang diunggah belakangan berdiri di urutan terakhir di dalam grup induknya
  (HBA-DECISIONS-30). **Tanggal dokumen = waktu unggah berkasnya** (HBA 2026-10-24: "tanggal
  dokumen dari tanggal di undah"); WO yang belum punya berkas tampil tanpa penanda — tanggal
  peristiwa tidak dipinjam untuk mengisinya. (3) **Ruang Diskusi** — percakapan internal tingkat WO (bukan ruang bebas
  tingkat Unit). (4) **Galery & berkas** — dua kolom: kolom kiri berkas tingkat Unit (sertifikat,
  manual book, gambar), kolom utama berkas yang melekat pada induk dokumen (WO/SR) dibingkai nomor
  induk, dipisah per aktivitas.
- **Kotak Masuk.** Satu permukaan pemberitahuan **di dalam aplikasi** dengan angka jumlah pesan
  diskusi yang belum dibaca pada menu. Pemberitahuan hanya di dalam aplikasi; tidak ada kanal luar
  (HBA 2026-10-24). §1 "notification surface" yang semula di luar lingkup kini masuk lingkup sebatas
  ini.
- **Panggilan pekerja** tampil sebagai sebutan di dalam pesan diskusi. UI tidak boleh menampilkannya
  sebagai perintah kerja, persetujuan, atau item audit.
- **Penanda terbitan** tampil hanya sebagai kendali bagi Manager/Admin; UI tidak menyediakan pilihan
  visibilitas bagi pengunggah atau teknisi (§10 tetap).
- Vocabulary §2 tidak berubah; nol aturan bisnis baru di luar rekaman HBA di atas.

---

*End of IS-08 v1.2 (addendum HBA-DECISIONS-29/30/31/34, 2026-10-24).*

