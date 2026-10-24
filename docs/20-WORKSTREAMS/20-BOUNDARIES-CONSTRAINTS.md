# Boundaries & Constraints (Materialisasi Ini)

Status dokumen: PROPOSED (dokumentasi saja, bukan LOCKED, bukan keputusan bisnis).

## 1. Batasan yang mengikat

1. Dokumentasi saja. Hanya 5 file kanonis.
2. Lokasi hanya di `docs/20-WORKSTREAMS/` (3 file) dan `docs/90-AUDIT/` (2 file).
3. Jangan ubah code (termasuk `app.py`, `public/`, skrip, config runtime).
4. Jangan ubah DB/schema (termasuk SQLite, `data/`, file `.GDB`/`.GBK`).
5. Jangan buat migration.
6. Jangan buat TASK-001 (tidak ada file task, tidak ada penomoran task tersembunyi).
7. Jangan mengubah LOCKED (tidak menambah, mengurangi, atau menafsir ulang).
8. Jangan mempromosikan PROPOSED menjadi LOCKED.
9. Jangan membuat business decision baru (tidak menetapkan prioritas, skop, HPP, COA, pajak, currency, cabang, rantai dokumen, atau urutan kerja).

## 2. Aturan STOP → REPORT → HUMAN

Jika saat penulisan ditemukan kontradiksi dengan keputusan yang sudah disetujui:

1. STOP (hentikan penulisan bagian yang berkontradiksi).
2. REPORT (catat di `docs/90-AUDIT/10-CONSISTENCY-REGISTER.md` sebagai discrepancy).
3. HUMAN (minta keputusan manusia; dilarang menyelesaikan dengan asumsi sendiri).

## 3. Larangan implementasi lanjutan

- Setelah materialisasi selesai, jangan memulai implementasi.
- Katalog observasi bukan backlog eksekusi.
- Tidak ada kode, tidak ada DDL, tidak ada seed, tidak ada perubahan `.xlsx`/spec sumber.

## 4. Kriteria selesai tahap ini

- 5 file ada di lokasi yang benar.
- Consistency check dilaporkan dengan 7 poin (files created, directories created, files changed, code/database/schema status, LOCKED change status, PROPOSED→LOCKED status, discrepancy).
