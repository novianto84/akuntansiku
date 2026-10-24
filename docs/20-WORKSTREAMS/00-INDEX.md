# 20-WORKSTREAMS — Index Kanonis

Status dokumen: PROPOSED (dokumentasi saja, bukan LOCKED, bukan keputusan bisnis).
Tanggal materialisasi: 2026-09-18.
Sifat materialisasi: dokumentasi saja. Tidak ada perubahan code, DB/schema, migration, dan tidak ada TASK-001.

## 1. Tujuan

Mencatat struktur workstream secara kanonis tanpa membuat keputusan bisnis baru.
Dokumen ini hanya merujuk fakta yang sudah ada di repo.

## 2. Sumber acuan (satu-satunya dasar)

1. `docs/accurate5-spec.md` — spec hasil reverse-engineer Accurate 5 (sumber: `test.GBK` / `analisa2.GDB`).
2. `docs/accurate5-gap-akuntansiku.md` — gap mapping Accurate 5 vs `app.py`.
3. `app.py` — route `/api/*` yang teramati di repo (fakta keberadaan route, bukan keputusan).
4. `git log` — fakta historis, antara lain commit `137c6d5` tentang metode HPP.

Tidak ada sumber keputusan tambahan yang dimaterialisasi di sini.

## 3. Isi direktori ini (3 dari 5 file kanonis)

1. `00-INDEX.md` (file ini) — index dan aturan pakai.
2. `10-WORKSTREAM-CATALOG.md` — katalog workstream turunan observasi, semua PROPOSED.
3. `20-BOUNDARIES-CONSTRAINTS.md` — batasan eksplisit materialisasi ini.

2 file kanonis sisanya ada di `docs/90-AUDIT/`:

4. `docs/90-AUDIT/00-INDEX.md`
5. `docs/90-AUDIT/10-CONSISTENCY-REGISTER.md`

Total: 5 file kanonis. Tidak lebih, tidak kurang untuk tahap ini.

## 4. Definisi status (definisi saja, bukan penetapan)

- LOCKED: keputusan yang sudah disetujui pada langkah sebelumnya. Materialisasi ini TIDAK mengubah, menambah, atau mengurangi LOCKED.
- PROPOSED: usulan / observasi yang belum dikunci. Semua isi `20-WORKSTREAMS/` pada tahap ini adalah PROPOSED.
- Dilarang mempromosikan PROPOSED menjadi LOCKED dalam tahap ini.

## 5. Aturan kontradiksi

Jika saat penulisan ditemukan kontradiksi dengan keputusan yang sudah disetujui: STOP → REPORT → HUMAN.
Tidak boleh menyelesaikan kontradiksi dengan asumsi sendiri atau keputusan bisnis baru.

## 6. Non-tujuan eksplisit

- Tidak membuat TASK-001.
- Tidak memulai implementasi setelah materialisasi.
- Tidak mengubah code, DB/schema, migration.
- Tidak membuat keputusan bisnis baru (tidak menetapkan prioritas, skop, HPP, COA, pajak, multi-currency, cabang, atau rantai dokumen).
