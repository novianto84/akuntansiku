# BD-WORKMODEL-001 — Work Model Definitions (SERVICE / INSPEKSI / EMERGENCY TROUBLESHOOT)

```text
Decision ID: BD-WORKMODEL-001
Title: Work Model Definitions + JOB Minimum + Continuation/ON HOLD/Minor Boundaries
Mode: Business Decision
Status: APPROVED / CANONICAL — BUSINESS AUTHORITY DECISION (2026-09-23)
Business Authority Approval: YES (final BA decisions per Work Model clarification prompt, 2026-09-23)
Implementation Authorization: NO
```

> This decision captures the Business Authority's final Work Model clarification as
> canonical business vocabulary. It does not rewrite any historical document. Operative
> effects on CD-11 live only in `CD-11-Appendix-B-work-model-continuation.md`.
> Where this decision and a LOCKED baseline conflict, the conflict is stated explicitly
> below (§8) and resolved only by this BA decision — historical texts are left untouched.

---

## 1. Work Models (APPROVED)

Exactly three Work Models. No other Work Model exists. No `TROUBLESHOOT` model
separate from `EMERGENCY TROUBLESHOOT` (§15-prohibition of the clarification prompt
is adopted: timer/SLA/24h/auto-close/auto-switch/auto-JOB/score/threshold/auto-routing
are NOT created by this decision).

### 1.1 SERVICE

- WO memiliki JOB yang telah direncanakan sebelum teknisi mulai bekerja; tujuan utama
  adalah melaksanakan JOB tersebut (cf. CD-11 §12 Scope Checklist; BD-WORKTYPE-001
  SCOPE/JOB vocabulary).
- Pekerjaan tambahan dapat muncul saat pelaksanaan dan dapat dikerjakan apabila
  bersifat minor serta masih dalam kapasitas pelaksanaan yang wajar (see §6 Minor Job).
- SERVICE dapat berlangsung melalui beberapa Visit (cf. CD-11 §10 1WO→1R→NV).
- Pekerjaan yang sama belum selesai karena waktu Visit tidak mencukupi dilanjutkan
  pada Visit berikutnya dalam WO yang sama — continuation operasional, bukan ON HOLD
  (see §4, §5).

### 1.2 INSPEKSI

- Kunjungan pemeriksaan/pencatatan kondisi unit, terutama periodik atau berdasarkan
  kebutuhan. Tujuan awal: mencatat kondisi aktual unit; memeriksa kondisi komponen;
  melakukan pengujian yang relevan; merekam hasil pemeriksaan.
- INSPEKSI tidak menjadikan service/repair sebagai tujuan awal WO.
- Masalah minor yang aman dilakukan teknisi pada kunjungan tersebut boleh dilakukan
  dan tetap dalam WO INSPEKSI (Work Model tidak berubah).
- Pekerjaan yang membutuhkan Service baru → WO baru sesuai proses bisnis
  (cf. CD-11 §3 substantial-work path; BD-WORKTYPE-001 §4 Rules 5–6).

### 1.3 EMERGENCY TROUBLESHOOT

- Respons awal terhadap gangguan yang membutuhkan penanganan segera.
- JOB awal Emergency menggunakan vocabulary: `Troubleshoot`. Diagnosis adalah
  hasil/proses analisis, bukan nama JOB (cf. BD-WORKTYPE-001 §2: DIAGNOSIS ≠ JOB).
- Dalam rangkaian respons Emergency yang sama, teknisi dapat melakukan diagnosis dan
  tindakan/perbaikan yang diperlukan apabila memungkinkan. Ini adalah bagian dari
  rangkaian respons Emergency, bukan "exception" terhadap rule Service/Add Job —
  dengan batas §1.3a.
- §1.3a — Batas: bila tindak lanjut menjadi pekerjaan bisnis baru (quotation,
  approval, spare part, pekerjaan besar, atau kunjungan baru sebagai pekerjaan baru),
  maka dibuat WO baru, umumnya dengan Work Model SERVICE.
- Tidak ada Work Model normal terpisah bernama TROUBLESHOOT.

## 2. Work Model follows initial purpose (APPROVED)

Work Model mengikuti tujuan awal WO dan tidak berubah otomatis hanya karena aktivitas
teknisi berkembang. Minor action/diagnosis dalam model lain tidak memindahkan WO ke
model lain (§§1.1–1.3; cf. CD-11 §16 Inspection/Troubleshoot minor-repair note for the
same non-switching principle).

## 3. JOB minimum (APPROVED — partial supersession, see §8)

- WO resmi wajib memiliki minimal 1 JOB. Cardinality canonical untuk WO resmi:
  `1..N JOB per WO`.
- DRAFT bukan WO: DRAFT adalah penyimpanan sementara milik user pembuat; belum menjadi
  WO; boleh tanpa JOB; akses/visibilitas DRAFT mengikuti otoritas
  permission/visibility yang berlaku (BD-SR-005 §4), sedangkan hak
  melanjutkan/Submit Draft tetap eksklusif milik creator (CD-11 §2); tidak menjadi
  bagian lifecycle WO sampai dibuat/diterbitkan sebagai WO resmi (cf. CD-11 §2 DRAFT
  rules — consistent, now with explicit JOB-minimum exemption pre-submission).
  Penyempurnaan redaksi 2026-09-25: frasa lama "hanya dapat diakses user yang
  membuatnya" dibaca sebagai creator-only continuation, bukan pembatas visibilitas;
  tidak ada perubahan makna bisnis (lihat
  docs/90-AUDIT/UI-BASELINE-APPROVAL-AND-RECONCILIATION-RECORD.md).
- Aturan minimum 1 JOB berlaku ketika DRAFT menjadi WO resmi (pada Submit/OPEN).
  Tidak ada asumsi tambahan tentang DRAFT selain yang di atas.

## 4. Visit & CONTINUATION (APPROVED)

- Canonical Visit Type tetap: `INITIAL` / `ON PROCESS` (CD-11 §10; CD11-017/025).
  Tidak ada Visit Type baru.
- `CONTINUATION` bukan Visit Type, bukan status, bukan outcome, bukan field baru.
  Ia hanya istilah operasional/naratif: pekerjaan yang sama dilanjutkan pada Visit
  berikutnya dalam WO yang sama (waktu Visit habis; tanpa kondisi blocking).
  Visit berikutnya memakai canonical Visit Type sesuai mekanisme sistem
  (yakni `ON PROCESS` untuk Visit kedua dan seterusnya).
- Contoh terkunci: pekerjaan belum selesai karena waktu Visit habis → bukan ON HOLD;
  tetap WO sama; Visit berikutnya; disebut continuation secara operasional.

## 5. ON HOLD (APPROVED — operative definition)

- ON HOLD bukan sekadar pekerjaan yang belum selesai. ON HOLD dipakai ketika pekerjaan
  tertahan karena membutuhkan tindakan/keputusan/persetujuan/kondisi dari pihak
  lain/eksternal sebelum pekerjaan dapat dilanjutkan. Contoh: menunggu approval
  customer; menunggu approval Manager; menunggu spare part; menunggu kondisi/pihak
  lain yang diperlukan (cf. CD-11 §11 ON HOLD defaults: spare part belum tersedia,
  menunggu customer, kondisi lapangan, masalah teknis — consistent).
- Waktu Visit habis / butuh Visit berikutnya / teknisi belum selesai mengerjakan
  pekerjaan yang sama → TIDAK otomatis ON HOLD. Pekerjaan dilanjutkan Visit
  berikutnya selama tidak ada kondisi blocking seperti di atas.
- Mekanisme ON HOLD yang berlaku tetap CD-11 §11 (reason mandatory; WO tetap
  IN_PROGRESS + indikator; bukan WO state; tanpa HOLD workflow). Definisi ini
  menyempitkan *kapan* ON HOLD dipakai, tidak mengubah mekanismenya.

## 6. Minor Job guidance (APPROVED)

> Minor Job adalah pekerjaan yang membutuhkan waktu relatif sedikit, tidak membutuhkan
> peralatan khusus, minim risiko, dan dapat dilakukan dalam kapasitas
> kunjungan/teknisi yang sedang bertugas.

- Tidak ada angka jam, hard duration threshold, scoring, bobot otomatis, SLA/LSA,
  atau rule otomatis berbasis durasi.
- Bila pekerjaan minor terakumulasi hingga praktis menjadi pekerjaan besar,
  Sales/Manager dapat memutuskan membuat WO baru (human decision, bukan system rule).

## 7. Junior / Senior (APPROVED scope boundary)

- Senioritas teknisi (junior/senior, capability, pengalaman) BELUM menjadi system
  rule Phase 1. Dilarang menurunkan dari keputusan ini: permission matrix berbasis
  seniority; automatic routing; automatic skill scoring; technician score; automatic
  assignment berbasis bobot pekerjaan (cf. CD-11 §§7–8: Primary/Supporting hak
  operasional setara — consistent).
- Untuk Phase 1, senioritas hanya boleh menjadi operational guidance/manual bila
  diperlukan. Scope ini tidak diperluas sekarang (BA instruction: agar CRM selesai).

## 8. Conflicts & supersession (explicit, no silent rewrite)

| # | Conflict | Resolution by this BA decision |
|---|---|---|
| C-01 | BD-WORKTYPE-001 §2 ("zero or more JOBs — no minimum locked") + §4 Rule 1 ("zero or more JOBs") + §7 vs §3 di atas (`1..N` untuk WO resmi) | PARTIALLY SUPERSEDED: frasa minimum-cardinality pada BD-WORKTYPE-001 diganti `1..N` untuk WO resmi; DRAFT dikecualikan (§3). Seluruh sisa BD-WORKTYPE-001 (satu konsep JOB, SCOPE, marker, Finding/Diagnosis/Recommendation/Outcome≠JOB, no-auto rules) tetap berlaku penuh. Teks historis BD-WORKTYPE-001 tidak diedit; supersesi ini yang berlaku operatif. |
| C-02 | BD-WORKTYPE-001 §5 "definitions per approved reconciliation" (tanpa sumber) | SUPERSEDED oleh §§1–2 dokumen ini sebagai definisi Work Model yang disetujui. Klaim lama dibaca sebagai penanda masalah yang kini dijawab, bukan sebagai sumber definisi. |
| C-03 | Clarification-prompt §12 redaksi Visit "INITIAL/CONTINUATION/FINAL" vs CD-11 §10+§30 | REJECTED sebagian: FINAL sebagai Visit Type ditolak (CD-11 menang); CONTINUATION sebagai Visit Type ditolak; yang disahkan hanya §4 di atas (naratif operasional). |
| C-04 | Clarification-prompt §7.5 kata "exception" vs BA final §F | CLARIFIED: rangkaian respons Emergency BUKAN exception terhadap rule Service/Add Job; ia bagian dari respons Emergency dengan batas §1.3a. Aturan Add Job minor-only (CD-11 §12 + Appendix A, actually-performed-only) tetap berlaku untuk pekerjaan di luar rangkaian respons tersebut. |

Non-conflicts recorded (consistent, no amendment needed): template lama
FULL_SERVICE/INSPECTION_ONLY/EMERGENCY tetap tidak dipakai (IS-01 OQ-01 sumbu template
kini CLOSED sebagai REJECTED/unused — see §10); no TROUBLESHOOT model; Service Type
(CD-11 §16) tidak berubah/tidak bertambah; tidak ada status/Visit Type/transisi
otomatis/timer/SLA/24h/auto-close/auto-JOB baru.

## 9. DRAFT retention (APPROVED — conditional)

- DRAFT dipertahankan secara conditional: boleh dipertahankan jika implementasinya
  sederhana dan tidak menambah kompleksitas berarti (cf. CD-11 §2 + Approval Package
  Sec 2: DRAFT = milik creator, pre-Submit, belum official, belum masuk workflow —
  konsepnya sudah ada di baseline sehingga retensi bukan konsep baru).
- Jika discovery/technical assessment menunjukkan effort besar, banyak
  state/permission/audit complexity tambahan, atau tidak sebanding manfaatnya untuk
  Phase 1 → DRAFT boleh dihapus dari Phase 1 (DEFERRED/OPTIONAL).
- DRAFT tidak boleh menjadi blocker penyelesaian CRM.

## 10. Traceability & downstream notes

- Menjawab: IS-01 OQ-01 sumbu work-model (closed oleh §§1–2) dan sumbu template
  (closed sebagai REJECTED — template lama tidak dipakai); IS-01 OQ-04/F-1
  (checklist/N/A/HM eksak) tetap DEFERRED — definisi §§1,5,6 di sini tidak
  mengisi konten deferred tersebut.
- IS-02 mengonsumsi: §§1–7 sebagai guards naratif (tanpa threshold/score/otomasi);
  C-01 sebagai guard WO-creation (≥1 JOB pada OPEN/submit; DRAFT exempt);
  C-03/C-04 sebagai larangan Visit Type/status baru.
- Tidak ada schema/API/UI/permission yang dibentuk oleh dokumen ini.

*End of BD-WORKMODEL-001.*
