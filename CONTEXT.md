# CONTEXT.md — Indeks Operasional (NON-KANON)

**Status:** INDEKS OPERASIONAL — bukan kanon, bukan sumber kebenaran.
**Pemegang:** Manager Agent (review & update)
**Terakhir disusun:** 2026-10-05 oleh @personal-assistant (draft pertama, menunggu review Manager)

---

## Aturan Pemakaian

File ini **hanya pointer**. Setiap entri merujuk ke dokumen kanon yang berisi keputusan sebenarnya.
Tidak ada keputusan bisnis, aturan, atau otoritas yang dibuat di sini.
Jika ada konflik antara file ini dan dokumen kanon, **dokumen kanon menang**.

---

## Dokumen Kanon Utama (WAJIB BACA)

| Dokumen | Peran | Path |
|---|---|---|
| `AI_OPERATING_RULES.md` | Aturan operasional AI | `/home/anto/akuntansiku/AI_OPERATING_RULES.md` |
| `ARCHITECTURE_LOCK.md` | Otoritas arsitektur & status implementasi | `/home/anto/akuntansiku/ARCHITECTURE_LOCK.md` |
| `DECISION_REGISTER.md` | Register keputusan & gate status | `/home/anto/akuntansiku/DECISION_REGISTER.md` |
| `AI_CONTEXT_INDEX.md` | Indeks konteks proyek (brainstorm CRM) | `/home/anto/akuntansiku/AI_CONTEXT_INDEX.md` |

---

## Status Implementasi Saat Ini

**Sumber kanon:** `ARCHITECTURE_LOCK.md` §Implementation Authorization + `DECISION_REGISTER.md` §Pending Human Decision Gates

- **Implementasi ISSUED 2026-10-03** (HBA-DECISIONS-03 §1) — untuk pekerjaan yang sudah dieksekusi (WP-01…WP-10 backend + internal UI).
- Pekerjaan yang belum dimulai butuh otorisasi baru sebelum mulai.
- Arsitektur teknis: APPROVED / CANONICAL (TADR-01…TADR-18 + Architecture Baseline, 2026-09-21).
- CD-11: SIGNED-OFF / LOCKED / CLOSED (BA SIGN-OFF).
- CD-02: DEFERRED / UNVERIFIED — jangan rekonstruksi.

---

## Kategori Keputusan (Pointer ke DECISION_REGISTER.md)

### LOCKED — Keputusan Bisnis

| ID | Status | Sumber Kanon |
|---|---|---|
| CD-01 | FINAL / LOCKED | `docs/10-DECISIONS/CD-01-business-scope.md` |
| CD-03…CD-10 | LOCKED | `docs/10-DECISIONS/CD-03…CD-10` |
| CD-11 | SIGNED-OFF / LOCKED / CLOSED | `docs/10-DECISIONS/CD-11-service-work-order-operational-boundary.md` |
| BD-WORKTYPE-001 Rev.A | APPROVED / CANONICAL | `docs/10-DECISIONS/BD-WORKTYPE-001-job-scope-canonicalization.md` |
| BD-WORKMODEL-001 | APPROVED / CANONICAL | `docs/10-DECISIONS/BD-WORKMODEL-001-work-model-definitions.md` |
| BD-SRWO-001 | LOCKED — V1 | `docs/10-DECISIONS/BD-SRWO-001-sr-to-wo-v1.md` |
| BD-SR-001…005, 010, 011 | LOCKED — V1 | `docs/10-DECISIONS/BD-SR-*.md` |
| BD-G01-G02 | LOCKED — V1 | `docs/10-DECISIONS/BD-G01-G02-identity-boundary-v1.md` |
| HD-4 | CANONICAL (recorded) | `docs/10-DECISIONS/HD-4-delegated-audit-control-authority.md` |

### PENDING — Human Decision Gates

| Gate | Status | Sumber Kanon |
|---|---|---|
| Reminder / automation policy | DEFERRED by HBA | `HBA-DEC-RECORD-01` Decision 1 |
| Emergency retroactive timestamp | DECIDED by HBA | `HBA-DEC-RECORD-01` Decision 2 |
| Deployment operational context | DEFERRED by HBA | `HBA-DEC-RECORD-01` Decision 3 |
| Identity-link reconciliation | LOCKED HUMAN DECISION | Lihat `DECISION_REGISTER.md` §Pending |
| QR access policy | LOCKED HUMAN DECISION | Lihat `DECISION_REGISTER.md` §Pending |
| Business Access Model | LOCKED HUMAN DECISION | Lihat `DECISION_REGISTER.md` §Pending |
| Customer publication model | DECIDED — HBA D-01A = RETAIN | CD-11 §§20–21 + TADR-12 |

---

## Arsitektur Teknis (Pointer ke DECISION_REGISTER.md §Technical Architecture)

| Item | Status | Sumber Kanon |
|---|---|---|
| Technical Architecture Approval | APPROVED / CANONICAL | `docs/30-ARCHITECTURE/ARCHITECTURE_BASELINE.md` + `TADR/` |
| Architecture Approval Package | APPROVED / CANONICAL | `docs/30-ARCHITECTURE/ARCHITECTURE_APPROVAL_PACKAGE.md` |
| F-1 | DEFERRED — NON-BLOCKING | — |
| C-1/C-2 | DOCUMENTATION CLEANUP — NON-BLOCKING | — |

---

## Spesifikasi Sistem (IS)

**Sumber kanon:** `docs/40-SPECIFICATION/`

| ID | Nama | Status |
|---|---|---|
| IS-00 | IS governance / master plan | SPECIFICATION — non-LOCKED |
| IS-01…IS-11 | Spesifikasi teknis | SPECIFICATION — non-LOCKED |

---

## Audit & Evidence

**Sumber kanon:** `docs/90-AUDIT/`

- `00-INDEX.md` — indeks audit
- `SR-V1-reconciliation-record.md` — rekonsiliasi SR V1
- `BUILT-VS-AUTHORIZED-reconciliation-record.md` — rekonsiliasi built vs authorized
- `UI-BASELINE-APPROVAL-AND-RECONCILIATION-RECORD.md` — baseline UI
- `G1-D-ACCEPTANCE-AND-CONTROL-ADOPTION-RECORD.md` — penerimaan G1-D
- `HBA-DECISION-RECORD-01-REMINDER-TIMESTAMP-DEPLOYMENT.md` — keputusan HBA
- `HBA-DECISIONS-02.md`, `HBA-DECISIONS-03.md` — keputusan HBA lanjutan

---

## Prinsip Traceability

```
Human Decision → CD / BD / DD → Technical Requirement → TADR → Implementation Specification → Implementation → Test → Audit
```

Setiap link yang hilang harus dilaporkan. Jangan pilih sumber secara diam-diam saat konflik.

---

## Catatan untuk Agen

- Baca `AI_CONTEXT_INDEX.md` Level 0 dulu sebelum task apa pun.
- Jangan implementasikan apa yang belum diotorisasi Human.
- Jangan rekonstruksi CD-02.
- File ini diupdate oleh Manager Agent saat ada perubahan status keputusan atau otorisasi implementasi.
