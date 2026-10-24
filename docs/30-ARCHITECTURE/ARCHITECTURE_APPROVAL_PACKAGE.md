# ARCHITECTURE APPROVAL PACKAGE — CRM Mitra Sarana Pratama (MitraSP)

```text
Status: APPROVED / CANONICAL (BUSINESS AUTHORITY — ARCHITECTURE APPROVAL)
Business Baseline: CD-11 SIGNED-OFF / LOCKED / CLOSED (plus CD-01, CD-03…CD-10 LOCKED)
Technical Direction: TADR-01 … TADR-18 APPROVED (HUMAN FINAL TECHNICAL ARCHITECTURE APPROVAL — 2026-09-21),
  aligned to CD-11 via TADR Direction Update + Architecture Baseline Alignment
Implementation Authorization: NO
Schema Finalization: NO
Migration Authorization: NO
Coding Authorization: NO
Programmer Handoff: NO
```

Tujuan dokumen: memberi Business Authority satu ringkasan arsitektur yang cukup
lengkap untuk menjawab: **"Apakah architecture direction ini sudah sesuai dengan
business baseline yang saya LOCK?"** Dokumen ini menyetujui **direction**, bukan
implementation detail. Tidak ada keputusan baru di dalamnya; yang belum
diputuskan ditandai DEFERRED / IS SPECIFICATION LATER.

Sumber kebenaran: CD-11 SIGNED-OFF / LOCKED / CLOSED menang atas semua konflik.

---

# SECTION 1 — ARCHITECTURE BASELINE

## 1.1 Domain boundaries (modular monolith, TADR-01)

Satu deployable unit dengan seam modul: Identity, Asset, Service,
Commercial/Sales, Purchasing, Inventory, Price Intelligence,
Visibility/Projection, Platform. Tidak ada service-split. Future
Accounting/ERP tidak ditutup (deferred scope, bukan permanent exclusion).

## 1.2 Company Master, Contact/PIC, relationship (CD-03; TADR-02/07)

- Company = identity root; satu identitas canonical; tanpa duplikasi master per role.
- Contact / CompanyRole berada di bawah identitas Company; tidak dilebur ke field Company.
- Tidak ada relasi permanen Customer–Technician; tidak ada relasi technician pada Customer Profile.
- Identity-Link (Google Identity → Contact/PIC → Verified PIC Link → Company)
  dimodelkan terpisah dari Contact agar revokasi tidak merobek histori relasi.

## 1.3 Unit & Component model (CD-11 §§5, 15; TADR-03)

- Unit = parent asset; CRM-owned/shared registry; tanpa fake Unit Master.
- `1 WO → 1 Unit`: WO boleh dibuat sebelum Unit diketahui, tetapi sebelum CLOSED
  WO harus terikat ke exactly 1 Unit (EXISTING / NEW / NOT YET DETERMINED dengan
  aturan validasi masing-masing).
- Component subtypes operasional strict: ENGINE, GENERATOR, BOX_CHASIS —
  masing-masing struktur subtype-spesifik; tipe lain registry/future tanpa
  spesifikasi operasional. Replacement mencatat old/new component, date, reason,
  relationship.

## 1.4 Service Request & Work Order (CD-11 §§2–7; TADR-02/04)

- Service Request OPTIONAL; WO dapat dibuat tanpa Request. Pekerjaan
  reguler/baru yang substansial via `Service Request → Commercial/Approval → New WO`.
- WO workspace-owned; lifecycle canonical lihat Section 2.
- Material usage = operational record WO (Item + Quantity + Harga Perolehan per
  Unit; tanpa total/valuasi/accounting); alur take → stock-out → WO record
  non-atomic; non-stock/customer-owned/direct-purchase tercatat tanpa stock-out
  (CD-10 inventory authority; TADR-10).

## 1.5 Report, Visit, Evidence (CD-11 §§10, 17, 18; TADR-11/12)

Lihat Section 3 dan Section 6. Prinsip: Visit = sumber operasional; Report =
konsolidasi; satu operational history dengan multiple contextual views
(Unit View unit-scoped; Customer View agregat WO customer yang masing-masing
tied to its own Unit; QR View unit-scoped).

## 1.6 Customer access & QR/access boundary (CD-11 §§21–22; TADR-12/13/14/16)

Lihat Section 5 dan Section 7. Prinsip: CONTROLLED ACCESS
(SCAN QR → SIGN UP/SIGN IN Google-only → CHECK ACCESS → UNIT DATA; tanpa akses
anonim); dua tier — UNIT SCOPE untuk authenticated user, COMPANY SCOPE hanya
untuk Verified PIC; harga/nilai dalam bentuk apa pun tidak tampil di portal
eksternal.

## 1.7 Audit/history (CD-11 §28; TADR-08/09/18)

Setiap aksi koreksi/pembatalan/reopen/re-create mencatat actor, server
timestamp, action, object, reason, before/after bila relevan. Correction history
= controlling data (bukan sekadar audit) dengan penomoran siklus. Trail
tamper-evident; observability full-spectrum dengan leakage prohibition (tanpa
harga akuisisi, vendor intelligence, internal notes, token, secret di log).

## 1.8 Accurate 5 boundary (CD-01/04/10)

Accurate 5 = existing/transitional reference, bukan permanent runtime lock.
CRM tidak pernah posting/menilai: tanpa journal, GL, COA, COGS, FIFO/Average,
valuation, tax engine, costing, revenue recognition. Inventory quantity-only;
acquisition price operational reference only.

Hubungan konseptual antar domain: Company (identitas) → Unit (asset parent) →
WO (fakta operasional workspace-owned, execution + lifecycle owner) → Visit/
Evidence/HM/Outcome (fakta eksekusi WO-owned) → Report (konsolidasi, FINAL saat
CLOSED) → Projection turunan (customer/QR/unit/technician/Outstanding, derived
only, reviewer-curated). MaterialUsage (WO) ↔ InventoryOperation (inventory)
berpasangan dengan mutual reference tanpa saling mengontrol. Commercial
(Quotation→SO→Fulfillment; PR→PO→Receiving) workspace-owned dengan semantik
parsial aditif.

**Tidak ada database schema dalam dokumen ini.**

---

# SECTION 2 — SERVICE / WO ARCHITECTURE

Canonical lifecycle (CD11-001; CD-11 §2):

```text
DRAFT → OPEN → IN_PROGRESS → WAITING APPROVAL → CLOSED
```

plus `CANCELLED` sebagai terminal cancellation state (CD11-010; CD-11 §9).

- **DRAFT**: milik creator, pre-Submit, belum official, belum masuk workflow.
- **OPEN**: WO resmi submitted; boleh tanpa Technician (operationally unassigned,
  terlihat di dashboard Sales/Coordinator/Manager); TIDAK BOLEH masuk
  IN_PROGRESS tanpa responsible/assigned person.
- **Assignment = event/condition, bukan WO status.** Tidak ada state `ASSIGNED`;
  `UNASSIGNED` adalah condition. `OPEN → IN_PROGRESS` terjadi saat
  Technician/responsible person ditugaskan (otoritas `ASSIGN_WO`: Manager +
  Coordinator default; setiap perubahan perlu reason + audit). Per WO: tepat
  satu Primary + nol/lebih Supporting dengan hak operasional setara (Primary =
  akuntabilitas utama). Manager Take Over dan Technician Self-Add (request →
  evidence → approval) adalah mekanisme assignment, bukan state.
- **Responsible person requirement**: tidak boleh ada pekerjaan berjalan tanpa
  penanggung jawab; WO `IN_PROGRESS` terlihat di dashboard Sales, Technician,
  Manager, Coordinator.
- **Emergency lane** (CD-11 §6): Technician-created WO langsung `→ IN_PROGRESS`,
  `Work → Minimum Critical Validation → WAITING APPROVAL → Authorized Approver →
  CLOSED`; Technician tidak approve (termasuk WO sendiri); tanpa auto-close.
- **Cancellation boundary** (CD-11 §9): hanya dari `OPEN`/`IN_PROGRESS`;
  `CLOSED` tidak dapat di-cancel; `CANCELLED` terminal, tidak dapat di-cancel
  lagi, tidak dapat REOPEN. Tanpa tombol Approve/Reject formal dan tanpa status
  `CANCEL_PENDING_APPROVAL`/`CANCEL_*`.
- **Approval boundary** (CD-11 §§2, 18, 19): Technician submit eksplisit
  (`IN_PROGRESS → WAITING APPROVAL`); review Manager/Admin mandatory sebelum
  CLOSED; `APPROVE REPORT ⇒ WO = CLOSED` otomatis (tanpa action `CLOSE_WO`);
  Technician tidak menutup WO sendiri; customer acknowledgement OPTIONAL dan
  bukan prerequisite CLOSED.
- **Correction boundary** (CD-11 §2): selama `WAITING APPROVAL` reviewer dapat
  REQUEST CORRECTION → CORRECTION_REQUIRED, EDIT langsung (reason mandatory),
  atau CLOSE langsung (reason mandatory). Lihat Section 4.
- **Reopen/re-create boundary** (CD-11 §28): REOPEN hanya untuk `CLOSED`
  (kembali `IN_PROGRESS`, nomor/Report sama, assignment dipulihkan, histori
  lestari, multi-cycle diizinkan); RE-CREATE menghasilkan WO/nomor/Report/
  history baru dengan lineage `CREATED_FROM` (tanpa carry assignment otomatis).
- Istilah superseded yang TIDAK BOLEH muncul sebagai WO state (CD-11 §30):
  `ASSIGNED`, WO-status `COMPLETED`, WO-status `ON PROCESS`, `CLOSE_WO`,
  `CANCEL_*` states, `SKIP_TEMPORARY`, Visit Type `FINAL`.

**Tidak ada implementation detail dalam section ini.**

---

# SECTION 3 — REPORT / VISIT ARCHITECTURE

Model sumber (CD11-017/019/020; CD-11 §§10, 18):

```text
1 WO
  └── 1 Report (Hybrid Summary + Visit History)
        ├── Visit 1
        ├── Visit 2
        └── Visit N
```

- Setiap kedatangan fisik = 1 Visit Record (multiple visits sehari = record
  terpisah). Visit bukan WO baru. Creator otomatis hadir; attendance per
  Technician; check-in/out per Visit (wajib; server timestamp; GPS
  diupayakan-otomatis tetapi NULL-able dan tidak memblokir).
- Visit lifecycle: `OPEN → COMPLETED` — TERPISAH dari WO lifecycle. Visit
  `COMPLETED` tidak menutup WO dan tidak memfinalkan Report. Visit COMPLETED
  terkunci normal; koreksi terkendali tetap tersedia.
- Visit Type (sistem-determined; Technician tidak memilih):
  `INITIAL` (visit pertama) dan `ON PROCESS` (visit kedua dst).
  **`ON PROCESS ≠ WO IN_PROGRESS`** — keduanya hidup di level berbeda.
  **`FINAL` bukan Visit Type** — finality ditentukan via
  Visit → Report → Submit → Approve → WO CLOSED.
- Work Outcome per Visit: `COMPLETED` / `NOT_PERFORMED` (reason wajib;
  recommendation optional note) / `ON HOLD` (reason wajib; kewajiban berlanjut
  di WO yang sama; WO tetap `IN_PROGRESS` dengan indikator "Ada pekerjaan
  ON HOLD"). `ON HOLD` adalah outcome Visit, bukan WO status.
- Report = konsolidasi tanpa duplikasi manual: Summary (WO, Company/Customer,
  Unit, tipe/template, Work Scope Summary, Findings, Work Result,
  Parts/Materials, eligible Evidence, Final Conclusion) + Visit History.
- Finalisasi: `NON-FINAL → (WO CLOSED) → FINAL`. Visit COMPLETED, Outcome DONE,
  WAITING APPROVAL, CORRECTION_REQUIRED tidak memfinalkan. Tanpa aksi FINALIZE
  REPORT dan tanpa revisi/versi Report otomatis per koreksi; Report memakai data
  Visit terkini. Hanya `WO CLOSED → Report FINAL`.
- Final Conclusion: Technician mengisi draft; Approver menerima/mengoreksi/
  menetapkan; yang disahkan saat approval = official conclusion; histori
  menyimpan draft, modification, final, actor, timestamp.

Rantai konseptual: WO → Report → Visit → Evidence / HM / Outcome / Conclusion,
dengan Visit sebagai sumber operasional dan Report sebagai konsolidasi resmi.

---

# SECTION 4 — CORRECTION / HISTORY

Direction (TADR-09 di atas substrate TADR-08; CD11-006/007/008/012; CD-11
§§2, 18, 28):

- **Minor correction dan substantive correction** keduanya harus dapat
  direpresentasikan; definisi/content bisnisnya tidak dikarang di sini.
- **Correction cycle**: pre-CLOSED via loop WAITING APPROVAL (REQUEST
  CORRECTION → CORRECTION_REQUIRED → resubmission; Report tetap NON-FINAL);
  post-CLOSED via REOPEN (`CLOSED → IN_PROGRESS`).
- **Numbered cycles**: correction history = controlling data dengan penomoran
  siklus; **jumlah cycle tidak dibatasi business rule** — arah teknis tidak
  boleh mengenakan maksimum.
- **Controlling history**: setiap cycle mencatat actor, server timestamp,
  action, object, reason, before/after bila relevan; histori SLA lama lestari
  melewati REOPEN.
- **Approval chain**: review mandatory pre-CLOSED; re-CLOSED mengikat identitas
  reviewer; Technician tidak approve; self-approval dilarang.
- **Official result**: rantai draft → modification → final → approved official
  conclusion tetap tertelusur; koreksi tidak boleh orphan/mengganti diam-diam
  hasil yang sudah disahkan.
- **Reopen**: hanya `CLOSED`; nomor/Report sama; assignment dipulihkan.
- **Re-create lineage**: WO/nomor/Report/history baru dengan `CREATED_FROM`;
  kontinuitas berbasis lineage, bukan identitas.
- **Audited direct-edit sideroute**: satu-satunya direct edit yang diizinkan
  bisnis — EDIT reviewer selama `WAITING APPROVAL` dengan mandatory reason —
  berjalan di atas substrate controlling-history yang sama (audit linkage
  penuh), bukan bypass. Tidak ada direct-edit path pada `CLOSED`.

**Tidak ada schema audit. Tidak ada field database.**

---

# SECTION 5 — CUSTOMER PROJECTION

Boundary (CD11-020/021; CD-11 §§17, 18, 21, 22; TADR-12 dengan TADR-11/14/16):

Customer-facing result hanya tersedia bila SELURUH gate terpenuhi:

```text
CLOSED + FINAL + Verified PIC + Company Scope + Policy + Eligibility
```

- `CLOSED` = WO closed via approval; `FINAL` = Report FINAL (hanya pada WO
  CLOSED); Verified PIC = Company access via Verified PIC Link; Company Scope =
  unit-scoped company data; Policy = `photo_type + approval_state +
  policy_version` + kurasi reviewer; Eligibility = data eligible saja
  (evidence non-eligible tetap tersimpan internal-only).
- **Technician tidak menentukan customer visibility** — kontrol publikasi oleh
  reviewer (Manager/Admin); Technician tidak memilih visibility.
- **Internal-only tidak masuk projection**: internal notes,
  correction/cancellation/administrative reasons, acquisition price, vendor
  intelligence, informasi internal/komersial lain.
- **No-download requirement tetap berlaku** (mekanisme deferred ke IS
  Specification; tidak ditentukan di sini).
- **QR tetap unit-scoped** (satu QR = satu Unit; QR di Unit/Invoice/Surat Jalan
  adalah QR yang sama menuju Unit yang sama).
- **Portal tetap company-scoped** (UNIT SCOPE untuk authenticated non-PIC;
  COMPANY SCOPE hanya untuk Verified PIC; LOGIN ≠ COMPANY ACCESS;
  QR ≠ COMPANY ACCESS; tanpa harga dalam bentuk apa pun).

**Mekanisme download prevention tidak ditentukan.**

---

# SECTION 6 — EVIDENCE / RETENTION

(CD11-014/016/028; CD-11 §§6, 17; TADR-11):

- **Evidence eligibility**: ditentukan event/kondisi aktual — mandatory:
  nameplate, hour meter, before, after; conditional: during, replaced
  component, damage, test result. Evidence TIDAK globally mandatory: saat scope
  CHECKED, upload optional dengan `No Evidence / Opt Out` + reason WAJIB.
  Requirement configurable via Dynamic Configuration.
- **Photo type = contextual classification** (Before/During/After dkk.),
  bukan lifecycle retention terpisah.
- **Single retention rule** untuk seluruh evidence.
- **Approval state + policy governance**: kontrol publikasi `photo_type +
  approval_state + policy_version`; publikasi dikurasi reviewer; Technician
  tidak memilih visibility.
- **Emergency critical evidence gate** (minimum; bukan full validation):
  1. Unit Serial Number — wajib.
  2. Engine Serial Number — wajib **jika applicable**.
  3. Generator Serial Number — wajib **jika applicable**.
  4. Foto Sebelum — WAJIB, tanpa N/A.
  5. Foto Sesudah — WAJIB, tanpa N/A.
- **N/A component hanya jika component memang non-applicable** berdasarkan
  subtype Unit Master (system-determined, bukan operator opt-out).
  **Applicable tetapi SN unknown: N/A prohibited** — SN wajib diperoleh sebelum
  submit.

---

# SECTION 7 — ACCESS / SECURITY ARCHITECTURE

(TADR-13/14/16; CD-11 §§7, 21, 22; LOCKED HUMAN DECISIONS):

```text
Google Identity → Contact/PIC → Verified PIC Link → Company
```

Link states per-company: **VERIFIED / PENDING / REVOKED**.

- Google-only external sign-up/sign-in; sign-up sendiri tidak memberi akses
  Company/PIC; registrasi PIC = application → PENDING; approval Manager/Admin
  membentuk Verified PIC Link (verified PIC = SATU-SATUNYA basis Company access).
- **No cross-company grant.** Google email tidak harus company email;
  pencocokan email/domain BUKAN syarat.
- **Customer scope company-based**: UNIT SCOPE (unit identity, owner company,
  address, work/material history; tanpa PIC details/lists, tanpa unit lain,
  tanpa data company-level, tanpa harga) vs COMPANY SCOPE (semua Unit milik
  Company tersebut di CRM + histori + PIC per customer-safe visibility).
- **QR unit-scoped** (resolusi unit-rooted; cross-unit browsing mustahil
  struktural; CONTROLLED ACCESS tanpa preview sebelum login).
- **Technician tidak mengatur customer visibility; Technician tidak approve**
  (termasuk WO sendiri).
- **Self-approval rule**: applicant ≠ approver; approval hanya oleh internal
  Manager/Admin selain applicant; tanpa auto-approval; tanpa bypass via
  direct-URL/API.
- Authorization tiga lapis terpisah (TADR-14): authentication (who) /
  authorization (what actions, action-level + workspace guard) / business
  visibility (which fields). Matriks RBAC detail business-owned, tidak dikunci
  di sini.

**Tidak ada authentication implementation.**

---

# SECTION 8 — SLA / AUTOMATION

(CD11-011; CD-11 §§20, 23, 28, 30; TADR-15 — CONFIRMED consistent):

Untuk P1:

- **Numeric SLA: DISABLED** sebagai active rule.
- **H-1: DISABLED. Overdue calculation: DISABLED. Escalation automation:
  DISABLED.**
- Outstanding = konsep monitoring/attention — bukan overdue/SLA/eskalasi/
  blocking.
- **Timestamp/history tetap disimpan** (termasuk lestari melewati siklus
  REOPEN) sebagai properti audit, bukan aktivasi perilaku SLA.
- Nilai SLA lama, bila ditemui, = future-reference / historical context ONLY;
  tidak boleh diinterpretasikan/disajikan sebagai threshold aktif.
- Manual reminder (Admin/Manager/Sales) = baseline; automatic generation dan
  interval disabled Phase 1.

**Tidak ada timer yang diaktifkan. Tidak ada queue/job design.**

---

# SECTION 9 — TADR MATRIX

| TADR | Decision | Current Direction | Status |
|------|----------|-------------------|--------|
| TADR-01 | Application / Module Boundaries | Modular monolith; seams: Identity, Asset, Service, Commercial/Sales, Purchasing, Inventory, Price Intelligence, Visibility/Projection, Platform | APPROVED |
| TADR-02 | Domain / Aggregate Boundaries | Aggregate map; WO owns execution + lifecycle; 1 WO = 1 Unit, binding resolved before CLOSED | APPROVED |
| TADR-03 | Component Subtype Structure | Subtype-specific ENGINE/GENERATOR/BOX_CHASIS; registry/future tanpa spec; tanpa generic JSON/EAV | APPROVED |
| TADR-04 | Transaction Boundaries | Per-transition guards; canonical WO matrix + CANCELLED; paired non-atomic MaterialUsage↔InventoryOperation | APPROVED |
| TADR-05 | Database Strategy | One relational DB; app-enforced workspace scoping; philosophy only (tanpa DDL/produk) | APPROVED |
| TADR-06 | Workspace Isolation Enforcement | App-level guards + negative tests; shared-master allowlist | APPROVED |
| TADR-07 | Source-of-Truth Ownership | Single-write ownership map; views derived only | APPROVED |
| TADR-08 | Audit / Versioning Mechanism | Hybrid: immutable version records (commercial/price) + append-only governance trail (WO) | APPROVED |
| TADR-09 | Correction / Revision Mechanism | Governed flow: WAITING APPROVAL loop + post-CLOSED REOPEN; numbered unlimited cycles; audited direct-edit sideroute | APPROVED |
| TADR-10 | Material vs Inventory Separation | Two-sided modeling; Harga Perolehan (per Unit) operational reference; tanpa costing/accounting | APPROVED |
| TADR-11 | File / Photo Architecture | Mediated serving; immutable originals; reviewer-gated publication; QR unit-bound | APPROVED |
| TADR-12 | Read Models / Projections | Hybrid freshness; 1WO→1R→NVisits; eligibility-gated customer projection; no-download honored | APPROVED |
| TADR-13 | Authentication / Identity-Link | Link-entity lifecycle; SoD applicant≠approver; mekanisme OAuth/token/session deferred | APPROVED |
| TADR-14 | Authorization / Visibility Enforcement | Tiga lapis; two-tier UNIT/COMPANY scope; matriks konten business-owned | APPROVED |
| TADR-15 | Background Jobs / Notifications | Disabled-by-default framework; manual-reminder baseline; SLA tetap disabled | APPROVED |
| TADR-16 | QR Mechanism | DB-backed indirection; revocable + permanent; unit-rooted; CONTROLLED ACCESS | APPROVED |
| TADR-17 | Deployment Topology | Candidate direction (containerized VPS-or-equivalent); tanpa seleksi/provisioning | APPROVED |
| TADR-18 | Observability / Traceability | Full-spectrum telemetry; leakage prohibition; threshold bisnis tidak diciptakan | APPROVED |

Status yang dipakai hanya yang ada: APPROVED (HUMAN FINAL TECHNICAL
ARCHITECTURE APPROVAL — 2026-09-21). Tidak ada status baru.

---

# SECTION 10 — DEFERRED TO IS SPECIFICATION

**Architecture Direction Locked** (diputuskan; tinggal dirinci di IS):
canonical lifecycle + guards; assignment model; visit/report model; governed
correction + numbered cycles; eligibility-gated projection + two-tier scopes;
mediated file serving; disabled-by-default jobs; workspace isolation via
app-guards; hybrid audit/versioning; two-sided material/inventory; modular
monolith seams; SLA-disabled.

**Implementation Detail Deferred** (belum diputuskan; dilarang dikarang):

- database product/version; schema detail; table/column; migration strategy
- API contract; endpoint; guard composition mechanics (exact middleware)
- authentication implementation (OAuth/token/session mechanics)
- QR token format; QR URL structure/mechanics; rotation/expiry/reprint procedure
- storage architecture; evidence storage class; derivative lifecycle
- retention implementation (windows, mechanics)
- projection refresh mechanism/cadence; snapshot/retention **mechanism** (business expectation
  resolved: HBA D-01A = RETAIN); staleness policy (semantic only, D-01B)
- no-download serving mechanism; publication-state mechanics
- job/queue mechanism (transport, scheduling, backoff/dead-letter);
  reminder/automation policy (Human policy gate)
- telemetry substrate; retention log; alert routing/ownership
- detailed UI specification (termasuk correction-context presentation,
  reconciliation surfacing rules — Outstanding surfacing gate business-owned)
- exact permission implementation; permission-key naming; RBAC matrix content
  (business-owned)
- deployment selection/sizing/cost; invitation UX; acknowledgement alternative
  evidence; emergency retroactive timestamp convention; subtype field
  requirements; N/A taxonomy/examples; checklist contents; Minor/Major
  thresholds

Jika suatu item sudah diputuskan dalam TADR, ia tidak tercantum sebagai
undecided — daftar di atas hanya berisi yang memang deferred.

---

# SECTION 11 — ARCHITECTURE RISKS / OPEN ITEMS

## Non-blocking (dapat diselesaikan pada IS Specification)

- Customer publication **mechanism** (business expectation resolved: HBA D-01A = RETAIN; gate: TADR-11/12).
- Reminder/automation policy (gate: TADR-15).
- Emergency retroactive timestamp convention; deployment operational context.
- Outstanding surfacing rules; N/A taxonomy; checklist contents; subtype
  fields; acknowledgement evidence.
- Formal CD documentation atas LOCKED HUMAN DECISIONS (identity-link, QR
  CONTROLLED ACCESS, Business Access Model, self-approval invariant).
- Pointer nomor section CD-11 lama pada beberapa baris input TADR (otoritas
  status sudah benar; pemetaan ulang menunggu verifikasi).
- `IMPLEMENTATION_SPECIFICATION_PREPARATION.md` masih merefleksikan status
  pra-sign-off (dilestarikan sebagai artefak historis; bukan baseline aktif).

## Blocking

`Architecture Approval Blocker: NONE` — tidak ada blocker yang mencegah
Architecture Approval. Implementation detail yang belum ditentukan bukan
blocker (disengaja deferred ke IS Specification).

---

# SECTION 12 — APPROVAL CHECKLIST

Untuk Business Authority:

- [ ] Business baseline reflected correctly
- [ ] CD-11 unchanged
- [ ] TADR direction correctly represented
- [ ] No conflicting active terminology
- [ ] Domain boundaries understood
- [ ] Security/access boundary understood
- [ ] Customer projection boundary understood
- [ ] Deferred technical details explicitly separated
- [ ] No implementation decision accidentally introduced
- [ ] No business rule invented

Persetujuan atas package ini = persetujuan **direction**. Tidak mengotorisasi
implementation, coding, schema, migration, API, UI, deployment, atau Programmer
handoff. Tahap berikut (IS Specification) menunggu keputusan eksplisit Business
Authority setelah approval ini.
