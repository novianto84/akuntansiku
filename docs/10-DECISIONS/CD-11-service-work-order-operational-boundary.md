# CD-11 — Service / Work Order Operational Boundary

```text
Decision ID: CD-11
Title: Service / Work Order Operational Boundary
Mode: Business Architecture
Status: SIGNED-OFF / LOCKED / CLOSED
Business Authority Sign-off: YES (BA SIGN-OFF — CD-11 Business Finalization)
Implementation Authorization: NO
```

Sumber: business discovery CD-11 (Q1–Q30) sebagaimana telah direkonsiliasi dan
difinalisasi melalui Visit Outcome Brainstorming, handover Visit/Scope/Add Job/
Evidence/Report/Customer Publication, reconciliation B1–B4/C1–C10, finalisasi
O1–O5 beserta klarifikasi aplikabilitas O5, dan BA SIGN-OFF resmi.
Sifat dokumen: canonical business baseline. Tidak ada reinterpretasi AI,
tidak ada business rule baru di luar keputusan BA, tidak ada implementation
assumption.
Kode, schema, database, dan analisis terdahulu tetap **reference/evidence**,
bukan sumber keputusan.
CD-01 sampai CD-10 tidak diubah oleh dokumen ini.

## 1. Business Purpose

CD-11 mengatur operational boundary Service / Work Order:

* Service Request
* Work Order (WO)
* assignment / responsibility
* emergency work
* Visit execution
* Visit Type
* work outcome (COMPLETED / NOT_PERFORMED / ON HOLD)
* reason model
* scope checklist / Add Job
* evidence
* hour meter
* Report / Final Conclusion
* approval / correction
* cancellation / reopen / re-create
* customer-safe publication
* QR unit-scoped history
* workspace boundary

Tidak mencakup accounting/costing/HPP. Material usage murni operational.
Acquisition price murni operational reference.

## 2. Canonical WO Lifecycle (CD11-001)

```text
DRAFT → OPEN → IN_PROGRESS → WAITING APPROVAL → CLOSED
```

* `IN_PROGRESS` adalah nama status canonical untuk pekerjaan yang sudah mulai
  berjalan. `ON PROCESS` BUKAN status WO (istilah tersebut hanya valid sebagai
  Visit Type, lihat §10).
* Tidak ada lifecycle state `ASSIGNED` yang terpisah.
* `UNASSIGNED` adalah condition, bukan lifecycle state.
* `CLOSED` adalah final administrative closure state. Tidak ada status primer
  `MANAGER_CLOSED`; closure type/reason dapat membedakan perilaku
  administrative close.
* `CANCELLED` terminal dan berbeda dari `CLOSED` (lihat §9).

### DRAFT

* Draft tersimpan di aplikasi internal dan milik user yang membuatnya.
* Sebelum Submit, Draft belum menjadi official WO dan belum masuk
  operational workflow.
* Creator Draft adalah pihak yang melanjutkan dan Submit Draft tersebut.

### OPEN

* WO resmi dibuat/submitted.
* WO tanpa Technician boleh berada di `OPEN` (operationally unassigned) dan
  terlihat pada dashboard Sales, Coordinator, Manager.
* WO TIDAK BOLEH masuk `IN_PROGRESS` tanpa responsible/assigned person.

### Assignment → IN_PROGRESS

* Saat Technician (atau responsible person) ditugaskan: `OPEN → IN_PROGRESS`.
* WO `IN_PROGRESS` terlihat pada dashboard Sales, Technician, Manager,
  Coordinator.
* Technician-created Emergency WO langsung `→ IN_PROGRESS` (lihat §6).

### WAITING APPROVAL

* Technician menyatakan pekerjaan/report selesai (Submit eksplisit) dan
  menunggu review/approval; `IN_PROGRESS → WAITING APPROVAL`.
* Approval dilakukan terhadap hasil pekerjaan / Report.
* `APPROVE REPORT ⇒ WO = CLOSED` (otomatis). Tidak ada permission/action
  terpisah `CLOSE_WO`. Tidak ada kondisi normal APPROVED tetapi WO masih OPEN.
* Technician tidak menutup WO sendiri.
* Authorized reviewer juga dapat: REQUEST CORRECTION → CORRECTION_REQUIRED;
  EDIT langsung selama WAITING APPROVAL → reason mandatory;
  CLOSE langsung → reason mandatory.

## 3. Service Request

Service Request bersifat **OPTIONAL**. Request dapat direkam jika ada, tetapi
WO dapat dibuat tanpa Service Request. Pekerjaan reguler/baru yang substansial
mengikuti jalur `Service Request → Commercial / Approval → New WO`
(bukan Add Job).

## 4. WO Creation Authority

* Sales default memegang `CREATE_WO`.
* Technician dapat diberikan `CREATE_WO` (configurable/grantable);
  role lain configurable.
* Technician-created WO mengikuti lifecycle yang sama, tanpa kategori WO
  terpisah; dapat langsung `IN_PROGRESS` (mendukung emergency);
  Technician otomatis menjadi Primary; Technician tidak memilih Technician
  lain saat creation; assignment role berwenang dapat assign/reassign
  kemudian; administrative review tetap ada; tidak ada auto-close.

## 5. Unit Boundary & Identification

WO boleh dibuat sebelum Unit diketahui, tetapi sebelum `CLOSED` WO harus
terikat ke `exactly 1 Unit`. Prinsip: 1 WO = 1 Unit. Unit adalah parent asset.
Tidak ada fake Unit Master.

Saat pembuatan WO:

```text
EXISTING UNIT / NEW UNIT / UNIT NOT YET DETERMINED
```

* **EXISTING UNIT:** Sales memilih Unit Master yang sudah ada.
* **NEW UNIT:** data awal boleh belum lengkap; Technician mengidentifikasi/
  melengkapi informasi unit di lapangan; Technician TIDAK membuat official
  Unit Master; Manager/Coordinator memvalidasi; sistem kemudian
  mengofficialkan/membuat Unit Master dan menautkan WO.
* **UNIT NOT YET DETERMINED:** hanya bila Sales tidak dapat menentukan unit
  target; reason mandatory; memerlukan approval Manager/Coordinator karena
  memengaruhi assignment; identitas unit wajib resolved sebelum CLOSED.

## 6. Emergency WO

Technician boleh `Create → IN_PROGRESS → Work → Minimum Critical Validation
→ WAITING APPROVAL → Authorized Approver → CLOSED`. Technician tidak boleh
approve (termasuk WO-nya sendiri).

Minimum Critical Validation (hanya ini; bukan full validation):

1. Unit Serial Number — wajib.
2. Engine Serial Number — wajib **jika applicable** ( dimiliki/terpasang
   sesuai subtype Unit).
3. Generator Serial Number — wajib **jika applicable**.
4. Foto Sebelum — **WAJIB, tidak ada N/A**.
5. Foto Sesudah — **WAJIB, tidak ada N/A**.

Komponen yang tidak applicable dicatat `N/A` secara **system-determined**
berdasarkan subtype Unit Master, bukan operator opt-out. Komponen yang
applicable tetapi SN belum tersedia/diketahui **tidak boleh N/A**; SN wajib
diperoleh sebelum submit. Work Summary, HM, outcome detail, dan field lain
bukan critical gate minimum (tetap dapat dipakai workflow, diperiksa
Approver, menjadi bagian Report, atau diwajibkan via konfigurasi).

## 7. Assignment / Responsibility

Authority (permission peran) dan Assignment (tanggung jawab atas WO tertentu)
adalah konsep terpisah.

* Assignment boleh terjadi setelah Submit. Tidak ada Assignment SLA Phase 1.
* Perubahan assignment diizinkan selama WO bukan CLOSED/CANCELLED.
* Hanya pemegang `ASSIGN_WO` (default Manager + Coordinator) yang boleh
  assign/reassign. Setiap perubahan assignment memerlukan reason + audit.
* Per WO: satu atau lebih technician; tepat satu Primary Technician;
  nol atau lebih Supporting. Primary dan Supporting memiliki hak operasional
  yang setara; Primary hanya menyatakan akuntabilitas utama. Tidak ada
  privilege operasional terpisah.
* Penambahan/penghapusan technician dan penggantian Primary memakai otoritas
  `ASSIGN_WO` yang sama.
* Tidak ada relasi Customer-Technician permanen; tidak ada relasi technician
  pada Customer Profile.

### Manager Take Over

Prinsip: tidak boleh ada pekerjaan berjalan tanpa penanggung jawab. Manager
boleh mengambil alih pekerjaan (Take Over / Self-Assignment): Manager otomatis
menjadi assigned responsible person tanpa membuat account Technician baru dan
tanpa mengubah role; sistem mencatat actor, action, timestamp, dan audit
trail. Setelah itu WO dapat masuk `IN_PROGRESS`.

### Technician Self-Add

Technician yang sudah terlibat dalam WO dapat meminta penambahan diri
(Request Add Self → Evidence → Approval → keanggotaan resmi). Approval
authority configurable; evidence dipertahankan; reason penolakan mandatory;
request bersifat per-WO, bukan relasi profil technician.

## 8. Technician Assignment Record

Primary Technician adalah technical PIC / accountability utama dan tercatat
sebagai actual participant bersama Supporting Technicians dalam service
history. Checklist tidak mengatribusikan pelaksanaan scope per technician;
jika actor ditampilkan gunakan `Recorded by`, bukan `Completed by`.

## 9. Cancellation (CD11-010)

`CANCELLED` berbeda dari `CLOSED`. Cancellation hanya untuk WO `OPEN` /
`IN_PROGRESS`. `CANCELLED` tidak dapat di-cancel lagi; `CLOSED` tidak dapat
di-cancel; `CANCELLED` tidak dapat REOPEN.

Flow (tanpa tombol Approve/Reject formal; tanpa status
`CANCEL_PENDING_APPROVAL` / `CANCEL_APPROVED` / `CANCEL_REJECTED`):

```text
OPEN / IN_PROGRESS
→ Cancellation Request + Notes (Sales/Technician; alasan + notes)
→ Manager Attention / Inbox (validasi alasan)
→ Authorized Admin/Manager executes cancellation
→ CANCELLED
```

Default cancellation authority: Admin + Manager; configurable melalui dynamic
authority/permission configuration. Wajib tercatat: requester, reason/notes,
reviewer/attention, executor, timestamp, audit trail. WO/history/report tidak
dihapus. Kemungkinan investigasi atas cancellation tertentu hanya didukung
melalui attention/category/notes/history/audit — TIDAK ada investigation
workflow Phase 1.

## 10. Visit Model & Visit Type

Setiap kedatangan fisik Technician ke lokasi untuk suatu WO menciptakan
**1 Visit Record**:

```text
1 WO
  └── 1 Report
        ├── Visit 1
        ├── Visit 2
        └── Visit N
```

* Multiple visits pada hari yang sama adalah record Visit terpisah.
* Visit bukan WO baru. Setiap assigned Technician dapat membuat Visit.
* Creator Visit otomatis ditandai hadir; dapat menandai assigned technician
  lain yang hadir. Attendance per Technician; check-in/out per Visit
  (bukan per Technician).

### Visit Lifecycle

```text
OPEN → COMPLETED
```

* Semua assigned Technician dapat mengedit selama OPEN; Primary/Supporting
  memiliki hak operasional yang setara.
* Creator (atau assigned technician) dapat menandai COMPLETED; Primary tidak
  diwajibkan. Visit COMPLETED tidak menutup WO dan tidak memfinalkan Report.
* Visit COMPLETED terkunci secara normal; mekanisme koreksi terkendali tetap
  tersedia.

### Check-in / Check-out

* Check-in wajib; check-out wajib; Visit tidak dapat COMPLETED tanpa
  check-out. Server timestamp; timestamp tidak dapat diedit bebas (koreksi
  via mekanisme terkendali/audit).
* Metode default: tombol manual + GPS/location; configurable melalui
  Admin Panel → Service / WO → Visit Configuration.
* GPS diupayakan otomatis; kegagalan/ketidaktersediaan GPS tidak memblokir
  check-in/out; GPS boleh NULL. Jangan substitusi lokasi palsu/terakhir
  diketahui. Pengumpulan lokasi wajib diungkapkan secara transparan.

### Visit Type

```text
INITIAL   — Visit pertama dalam satu WO
ON PROCESS — Visit kedua dan seterusnya dalam WO yang sama
```

Ditentukan otomatis oleh sistem; Technician tidak memilih bebas. `FINAL`
BUKAN Visit Type. Finality pekerjaan ditentukan melalui
Visit → Report → Submit → Approve → WO CLOSED, bukan melalui Visit Type.
(`ON PROCESS` di sini adalah Visit Type dan tidak boleh dibaca sebagai
WO status `IN_PROGRESS`.)

## 11. Work Outcome

```text
COMPLETED / NOT_PERFORMED / ON HOLD
```

`SKIP_TEMPORARY` dilarang sebagai status pekerjaan.

### COMPLETED

Seluruh scope WO selesai (termasuk Added During Execution scopes yang CHECKED)
dan check-out selesai.

### NOT_PERFORMED

Pekerjaan tidak dilakukan pada kesempatan/Visit tersebut. Reason WAJIB
(dari managed list; `Lainnya` → Keterangan wajib). Pekerjaan dianggap selesai
secara administratif untuk Visit tersebut dan tidak otomatis dibawa sebagai
task baru. Recommendation for Next Session bersifat optional, hanya note,
tidak otomatis membuat task/WO dan tidak mengubah WO menjadi pending.

### ON HOLD

Pekerjaan belum selesai dan tetap menjadi kewajiban dalam WO yang sama.
Reason WAJIB. Dilanjutkan pada Visit berikutnya dalam WO yang sama.
Histori Visit mencatat outcome; WO tetap `IN_PROGRESS` dengan indikator
sederhana **"Ada pekerjaan ON HOLD"**. ON HOLD adalah outcome pada Visit,
bukan lifecycle status WO baru — tidak ada workflow ON HOLD → PENDING,
RESUME, atau HOLD APPROVAL.

### Reason Model

`Reason List + Lainnya + Keterangan`: Technician memilih dari daftar;
`Lainnya` tersedia dan mewajibkan Keterangan; reason standar tidak mewajibkan
keterangan tambahan. Daftar dikelola via Dynamic Configuration.

Default NOT_PERFORMED: Customer tidak mengijinkan; Tidak ada akses; Kondisi
lapangan; Waktu tidak mencukupi; Lainnya. (Gunakan `Customer tidak
mengijinkan`; frasa `Customer tidak meminta` tidak dipakai.)
Default ON HOLD: Spare part belum tersedia; Menunggu customer; Kondisi
lapangan; Masalah teknis; Lainnya.

## 12. Scope Execution Checklist & Add Job

Tidak ada entity Activity untuk setiap aksi technician. Gunakan Scope
Execution Checklist dengan state `UNCHECKED` / `CHECKED` (tanpa state
IN_PROGRESS). Pekerjaan parsial didokumentasikan pada Visit notes/findings;
scope tetap UNCHECKED hingga benar-benar selesai; scope dapat dikerjakan
lintas Visit; yang sudah CHECKED tetap CHECKED walau di-retest (retest
tercatat pada Visit berikutnya).

Add Job hanya untuk pekerjaan minor yang ditemukan/dikerjakan saat eksekusi
(bukan pekerjaan reguler/baru/substansial): ditandai `Added During Execution`
(+ `Added by` Technician, `Added at` otomatis sebagai timestamp administratif,
bukan timestamp eksekusi; tidak ada field execution timestamp Phase 1).
Input `Sudah dikerjakan?` YA → CHECKED, TIDAK → UNCHECKED. Metode entry:
kategori pekerjaan yang ada bila tersedia, selebihnya deskripsi bebas. Aturan
evidence sama dengan scope biasa. Seluruh Added scopes wajib CHECKED sebelum
Visit Outcome DONE/COMPLETED.

## 13. Findings & Mandatory Work Elements

Temuan BEFORE / DURING / AFTER bersifat mandatory untuk semua Service Type.
Condition dan Action selalu required; Diagnosis required saat ada abnormality,
failure, atau troubleshooting; Recommendation required saat ada tindak lanjut
yang perlu disarankan (jangan fabricate bila tidak ada).
Checklist dan Test/Run mandatory untuk semua Service Type; bila tidak dapat
dilakukan: `N/A + Reason` dengan validasi reviewer (aturan N/A eksak dan isi
checklist mengikutitickets keputusan lanjutan; tidak dikarang di sini).

## 14. Hour Meter

Minimum satu HM harus tersedia (initial/start atau final/end). HM dicatat
satu kali per Visit (bukan pasangan awal+akhir yang diwajibkan); titik
capture mengikuti workflow/template. Jika relevan dan tersedia → wajib diisi;
jika tidak tersedia/tidak relevan → `N/A` + reason (open reason, validasi
reviewer; bukan jalan pintas bebas). HM dan konteks pengambilannya disimpan
pada Visit record + audit trail. HM bukan Emergency critical gate.
Aturan HM N/A eksak tetap mengikuti keputusan lanjutan.

## 15. Component Replacement

Bila terjadi replacement, wajib: old component, new component, replacement
date, reason, replacement relationship. Tidak mengubah arsitektur component
(ENGINE, GENERATOR, BOX_CHASIS; lainnya registry/future).

## 16. Service Types

Service types: PM; Inspection/Troubleshoot; Emergency Service; Minor
Service; Major Service; Commissioning/Testing. Installation dan Corrective
Repair bukan Service Type terpisah (pekerjaan repair tercakup Minor/Major).
Batasan konseptual: PM = planned/preventive; Inspection/Troubleshoot =
investigasi/diagnosis (dapat melakukan repair minor bila part tersedia, tipe
WO tetap); Minor/Major = repair kecil/besar; Emergency = situasi
emergency/urgent (tipe, bukan flag); Commissioning/Testing = pekerjaan
commissioning/testing. Tidak ada threshold durasi/jam yang dikunci;
definisi detail menyusul.

## 17. Evidence

Evidence ditentukan oleh event/kondisi pekerjaan aktual (nameplate, hour
meter, before, after sebagai mandatory; during, replaced component, damage,
test result sebagai conditional), bukan pilihan bebas. Evidence TIDAK
globally mandatory Phase 1: saat scope CHECKED, field evidence muncul tetapi
upload optional; tersedia `No Evidence / Opt Out` dengan reason WAJIB bila
dipilih; note optional bila evidence tersedia. Requirement evidence
configurable (tipe/field/workflow) via Dynamic Configuration Panel.
Kontrol publikasi: `photo_type + approval_state + policy_version`;
Technician tidak memilih visibility. Evidence yang tidak eligible tetap
tersimpan dan terlihat internal sesuai permission, tidak tampil pada
Customer Report. Satu aturan retention untuk seluruh evidence (tanpa lifecycle
retention Before/During/After yang terpisah); `photo_type` hanya klasifikasi
kontekstual.

## 18. Report

```text
1 WO → 1 Report → N Visits
```

Report adalah Hybrid Summary + Visit History dan tidak boleh menuntut
technician menduplikasi data Visit secara manual. Summary: informasi WO,
Company/Customer, Unit, tipe/template WO, Work Scope Summary,
Findings/condition, Work Result, Parts/Materials, eligible Evidence, Final
Conclusion. Visit History: nomor Visit, tanggal, attendance, check-in/out,
outcome, ringkasan visit. Visit = sumber operasional; Report = hasil
konsolidasi.

### Report Finalization

Status konseptual `NON-FINAL → (WO CLOSED) → FINAL`. Visit COMPLETED,
Outcome DONE, WAITING APPROVAL, dan CORRECTION_REQUIRED tidak memfinalkan
Report. Tidak ada aksi FINALIZE REPORT Phase 1; tidak ada revisi/versi Report
otomatis per koreksi Phase 1. Bila Visit dikoreksi, Report memakai data Visit
terkini; selama CORRECTION_REQUIRED dan resubmission Report tetap non-final.
Hanya `WO CLOSED → Report FINAL`.

### Final Conclusion

Technician mengisi Draft Final Conclusion; Approver dapat menerima atau
mengoreksi/menetapkan kesimpulan final; yang disahkan saat approval menjadi
official conclusion. History menyimpan draft, modification, final, actor, dan
timestamp. Technician tidak dapat menetapkan Final Conclusion unilateral.

## 19. Review & Customer Acknowledgement

Review Manager/Admin mandatory sebelum CLOSED (mencakup checklist, photos,
material, test, HM, Unit, findings); reviewer dapat mengembalikan untuk
correction. Customer acknowledgement OPTIONAL dan bukan prerequisite CLOSED;
bila tidak tersedia/ditolak, catat reason dan sediakan bukti alternatif
serah terima/kehadiran yang sesuai (tanpa tipe bukti mandatory yang dikunci).

## 20. Service History & Views

Service History mencakup date, WO, Unit, technician, findings, action,
material, component replacement, HM, photos, test result, recommendation.
Prinsip: ONE OPERATIONAL HISTORY, MULTIPLE CONTEXTUAL VIEWS (Unit View
unit-scoped; Customer View agregat WO customer yang masing-masing tied to its
own Unit; QR View unit-scoped). INTERIM/CONTINUATION/FINAL hanya klasifikasi
report/work-stage (dengan BEFORE/DURING/AFTER), bukan lifecycle paralel dan
bukan Visit Type. Outstanding adalah konsep monitoring/attention (bukan
overdue/SLA/eskalasi/blocking); overdue timer nonaktif Phase 1.

## 21. Customer-Safe Visibility & Publication

Customer-safe: date, technician, summary/work performed, approved photos,
replaced component, material quantity bila disepakati, recommendation. Tidak
mengekspos internal notes, correction/cancellation/administrative reasons,
acquisition price, vendor intelligence, dan informasi internal/komersial
lainnya. Informasi customer-facing dikurasi reviewer (Manager/Admin); quantity
material hanya bila appropriate/agreed. Tidak ada mekanisme publikasi teknis
atau permission model yang dikunci di sini (mengikuti HD-01).

## 22. QR

QR permanent + unit-scoped, menampilkan customer-safe history Unit tersebut
saja. Akses mengikuti CONTROLLED ACCESS: SCAN QR → SIGN UP/SIGN IN
(Google-only) → CHECK ACCESS → UNIT DATA; tanpa akses anonim. QR pada
Unit/Invoice/Surat Jalan adalah QR yang sama menuju Unit yang sama.

## 23. Reminder

Manual reminder oleh Admin, Manager, Sales. Automatic reminder generation dan
interval tidak dikunci (disabled Phase 1 mengikuti B2).

## 24. Emergency vs Emergency Purchasing

Emergency Service (tipe service) tidak dicampur dengan Emergency Purchasing
CD-09. Request boleh dilewati; assignment dapat langsung; work dapat terjadi
sebelum WO formal (technician-created direct IN_PROGRESS); WO tetap harus
diformalkan/review sebelum CLOSED. Retroactive timestamp convention dan
retroactive completion deadline menyusul (tidak ada SLA numerik yang dikunci).

## 25. Workspace

WO workspace-owned. Unit CRM-owned/shared. Material usage mengikuti workspace
WO. Service history mengikuti workspace WO. Tidak ada cross-workspace
transaction.

## 26. Material Usage

Material usage adalah operational record (Item + Quantity + Harga Perolehan
per Unit; tanpa total/valuasi/accounting). Alur take → stock-out → WO record
tidak harus atomic. Material non-stock / customer-owned / direct-purchase
dapat dicatat pada WO tanpa stock-out inventory. CD-10 tetap inventory
authority.

## 27. Accounting Boundary

CD-11 tidak mengunci service costing, labor/material costing, HPP, COGS,
invoice accounting, journal, GL, tax, revenue recognition. Material usage
operational only; acquisition price operational reference only.

## 28. Correction / Cancellation / Reopen / Re-create Records

Setiap aksi koreksi/pembatalan/pembukaan-ulang/pembuatan-ulang mencatat actor,
timestamp (server), action, object, reason, dan before/after bila relevan.
Correction history adalah controlling data (bukan sekadar audit) dengan
penomoran siklus; CANCELLED terminal dan tidak dapat REOPEN; REOPEN hanya
untuk CLOSED (kembali IN_PROGRESS, nomor/Report sama, assignment dipulihkan,
target baru editable, histori SLA lama lestari, multi-cycle diizinkan
Phase 1); RE-CREATE menghasilkan WO/nomor/Report/history baru dengan lineage
`CREATED_FROM` (tanpa carry assignment otomatis; Company tetap; Unit boleh
berubah/baru).

## 29. Documentation Requirement

Setiap business rule penting yang LOCKED harus dapat direpresentasikan dalam
aplikasi sebagai (A) Manual Book/in-app documentation (konsep, rule,
workflow, makna status, authority, restrictions, contoh) dan (B) contextual
help/field note (makna field, kapan required, makna values, restrictions,
akibat setelah submit). Kedua lapisan konsisten dengan Source of Truth ini.
Documentation implementation bukan bagian implementasi CD-11 finalization.

## 30. Supersession & Purge Log

Aturan/terminologi berikut dinyatakan SUPERSEDED dan tidak boleh dipakai
sebagai active business rule tanpa keputusan BA baru: lifecycle lama
`DRAFT→ASSIGNED→IN_PROGRESS→COMPLETED→CLOSED` (diganti §2); state
`COMPLETED` dan `ASSIGNED`; `ON PROCESS` sebagai WO status; `FINAL` sebagai
Visit Type; `SKIP_TEMPORARY`; `CLOSE_WO`; `CANCEL_PENDING_APPROVAL` /
`CANCEL_*`; pembatasan CANCELLED pre-COMPLETED; frasa `Customer tidak
meminta`; outcome DONE/CONTINUE/WAITING versi lama; Visit Type
INITIAL/FOLLOW_UP/SYSTEM-DETERMINED versi lama; broad Emergency gate
(summary/HM/outcome sebagai blocker); numeric SLA/H-1/overdue/escalation
sebagai active rule (nilai lama menjadi future reference); universal
mandatory evidence; technician approval; unassigned `IN_PROGRESS`.

## 31. Decision Register CD11-001…CD11-029

CD11-001 canonical lifecycle §2; CD11-002 DRAFT rules; CD11-003 assignment /
take-over §7; CD11-004 emergency lane + minimum validation §6;
CD11-005 dashboard visibility §2; CD11-006 WAITING APPROVAL + auto-close §2;
CD11-007 minor/substantive correction §14; CD11-008 correction loop +
unlimited numbered cycles; CD11-009 approval default + role-based
self-approval rule §2 + §19 (cross-reference corrected 2026-09-25; previously
read "§13", which is Findings & Mandatory Work Elements); CD11-010 cancellation model §9; CD11-011 numeric SLA
disabled P1; CD11-012 audit events/fields §28; CD11-013 outcomes +
recommendation rule §11; CD11-014 evidence rule + emergency exception §17;
CD11-015 HM rule §14; CD11-016 single retention §17; CD11-017 visit types §10;
CD11-018 Final Conclusion §18; CD11-019 template-scoped visit structure §10;
CD11-020 report model §18; CD11-021 customer boundary + no-download +
honest deterrence §§21–22; CD11-022 dynamic configuration domains;
CD11-023 P1 exclusions + purge list §30; CD11-024 reason model §11;
CD11-025 visit terms §10; CD11-026 ON HOLD surfacing §11; CD11-027 approval
defaults §2 + §19 (cross-reference corrected 2026-09-25; previously read "§13");
CD11-028 narrow emergency gate §6; CD11-029 O5
subtype-applicability (system-determined N/A; applicable-unknown dilarang N/A).
Seluruhnya **[LOCKED]** via BA SIGN-OFF.

## 32. Document Status

```text
Decision ID: CD-11
Title: Service / Work Order Operational Boundary
Mode: Business Architecture
Status: SIGNED-OFF / LOCKED / CLOSED
Business Authority Sign-off: YES
Implementation Authorization: NO
```

Perubahan status dari HUMAN-ACCEPTED menjadi SIGNED-OFF / LOCKED / CLOSED
berdasarkan BA SIGN-OFF resmi. File governance (ARCHITECTURE_LOCK,
DECISION_REGISTER, AI_CONTEXT_INDEX) yang masih menyebut HUMAN-ACCEPTED
wajib dibaca sesuai status baru ini hingga pembaruan administratifnya
menyusul pada tahap yang sama.
