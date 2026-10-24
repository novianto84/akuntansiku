# CD-07 — Sales Tools Multi-Workspace & Shared Intelligence

Status: **LOCKED** (HUMAN CONFIRMED — "HUMAN CONFIRM — LOCK CD-07").

Sumber: 18 keputusan HUMAN pada CD-07 Decision Gate (Q1–Q18).
Sifat dokumen: transkripsi keputusan HUMAN. Tidak ada reinterpretasi substantif.
Kode, schema, database, dan analisis terdahulu tetap **reference/evidence**.

## Platform & Workspace

* Q1: Aplikasi adalah **satu Sales Tools / CRM Platform** multi-workspace,
  bukan satu aplikasi per perusahaan.
* Q2: Setiap perusahaan mempunyai **Workspace / Business Context sendiri**:
  transaksi, dokumen, numbering, template, approval, reporting masing-masing,
  dalam satu platform.
* Q3: PKP dan Non-PKP adalah **dua workspace berbeda**; transaksi, quotation,
  numbering, template, dan reporting tidak bercampur. Bukan dua sistem terpisah.
* Q13: **Satu database**; user memilih workspace via login (sebelum transaksi).
  Pendekatan DB-terpisah dan port-terpisah tidak dipilih.
* Q17 (HARD CONSTRAINT): **tidak boleh ada transaksi yang otomatis berpindah
  atau tercampur antar-workspace.**
* Q18: Sales Tools **tanpa journal/GL/financial ledger**; Accounting dibangun
  sebagai sistem/workstream terpisah di masa depan.

## Shared Master (Q4–Q6)

* Q4: Customer/Company Master **shared** lintas workspace tanpa identitas ganda;
  relasi customer ↔ workspace dicatat.
* Q5: Vendor Master **shared** lintas workspace tanpa identitas kedua.
* Q6: Inventory Item/Product Master **shared** (satu identitas);
  stock quantity/transaction tetap milik workspace.

## Shared Intelligence (Q7–Q9)

* Q7: Vendor Offer adalah **Shared Sales Intelligence** lintas workspace.
* Q8: Acquisition Price Reference **shared** sebagai referensi operasional
  (bukan valuasi/HPP/COGS/jurnal).
* Q9: **Keduanya shared** — intelligence umum (harga pernah ditawarkan/
  diperoleh) maupun riwayat pemakaian harga di transaksi workspace.

## Workspace-Owned Data (Q10–Q12, Q15–Q16)

* Q10: Quotation **selalu milik workspace** walau master/referensi sama.
* Q11: Numbering **per workspace**; sequence tidak saling mengambil;
  format boleh berbeda.
* Q12: Template dokumen **per workspace** (logo, nama, alamat, layout).
* Q15: Sales Pipeline **milik workspace** (stage/aktivitas per workspace).
* Q16: Reporting operasional **per workspace**; tanpa laporan gabungan
  transaksi (tanpa laporan global).

## Visibility (Q14)

* Data shared **otomatis terlihat** semua workspace. Keputusan ini menutup
  kelonggaran Q7 — bila kelak perlu pembatasan, itu keputusan baru, bukan
  bagian CD-07. (Kebutuhan visibility-by-admin dari CD-06 Q8 tetap OPEN di
  gate-nya sendiri dan tidak diubah oleh dokumen ini.)

## Open (bukan bagian lock)

* Format numbering per workspace.
* Mekanisme pilih workspace (sesudah login / sebelum transaksi / terakhir).
* Bentuk pencatatan relasi customer ↔ workspace.
* Aktivitas/relationship tertentu yang perlu dipisah (Q15 sub-item).

## Governance

> **A LOCKED decision may not be changed, weakened, expanded, or reinterpreted
> by AI Manager, AI Programmer, or AI Auditor without explicit HUMAN authorization.**

Konflik dengan keputusan LOCKED:

> **STOP → REPORT → HUMAN**
