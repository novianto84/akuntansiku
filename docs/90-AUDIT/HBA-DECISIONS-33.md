# IMPLEMENTATION RECORD — Diskusi WO + field dokumen genset (HBA-DECISIONS-31/32)

```text
Record ID:      HBA-DECISIONS-33
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Decisions:      HBA-DECISIONS-31 (diskusi WO), HBA-DECISIONS-32 (1 field dokumen)
Authorization:  "setuju. di otorisasi. silahkan eksekusi" (HBA, chat 2026-10-24)
Status:         IMPLEMENTED — migration applied on the live database, tested
Classification: Audit record. NOT a canonical specification document.
```

## Yang dibangun

**Diskusi WO (HBA-DECISIONS-31)** — internal-only, kotak masuk, badge angka:
migrasi v39 (`wo_discussions`, `wo_discussion_reads`); modul `app/wo/discussion.py`;
rute `GET/POST /api/wo/{id}/discussions`, `POST /api/wo/{id}/discussions/read`,
`GET /api/wo/discussions` (kotak masuk), `GET /api/wo/discussions/unread` (angka badge);
UI: panel `DiscussionPanel` pada detail WO, `DiscussionInbox` pada menu **Kotak Masuk**
sekaligus ringkas di dashboard, dan badge angka pada item menu.

Unread TIDAK disimpan sebagai penghitung: sebuah pesan disebut belum dibaca bila TIDAK
ada baris baca milik pengguna itu. Karena itu angka badge tidak bisa melenceng dari
jumlah barisnya, dan tidak ada nilai per-pengguna yang bisa basi.

**Field dokumen genset (HBA-DECISIONS-32)** — satu field, bukan tiga: migrasi v38
(`units.doc_ref`), ikut jalur spec unit yang sudah ada (create/update/PATCH), tampil di
sesi Genset sebagai "No. SPK / Invoice / Kontrak". Nilainya disimpan **apa adanya**
(tidak diubah kapitalnya): aturan auto-capital HBA ditujukan pada field kernel namaplate,
dan mengubah kapital sebuah nomor referensi bisa membuatnya tidak lagi cocok dengan berkas
aslinya. Kolom `spk_number`/`invoice_number`/`contract_number` sengaja tidak dibuat.

## Temuan yang diperbaiki saat verifikasi

Rute diskusi awalnya IKUT terbuka di pintu publik, karena `/api/wo/` sudah termasuk
daftar prefix publik. Itu melanggar kata HBA "tidak bisa oleh external" — sesi pelanggan
punya jalan ke catatan internal. Diperbaiki di gerbang fail-closed pintu publik:
sebuah path yang memuat segmen `discussions` kini tidak pernah dianggap publik, sehingga
rutenya tidak pernah dikirim ke handler di pintu publik (menjawab 404, bukan 403 —
tidak mengonfirmasi keberadaan rute internal). Ada tes regresinya.

## Bukti

- 18/18 cek HTTP hidup lewat dua pintu: kirim pesan, belum-dibaca per pengguna, kotak
  masuk, tandai terbaca, perpindahan badge antar pengguna, badan kosong ditolak (400),
  WO milik workspace lain ditolak (403), **pintu publik menjawab 404 untuk rute diskusi**,
  dan `doc_ref` tersimpan verbatim.
- 47 tes unittest lulus (`tests/test_wo_discussion.py` 17 tes baru + `tests/test_doors.py`
  dengan 1 tes gerbang baru).
- `npm run typecheck` bersih; `npm run build` sukses.
- 12/12 cek peramban nyata (chromium, layar sungguhan): menu Kotak Masuk beserta angka
  badge, kotak masuk berisi baris WO, panel Diskusi WO menampilkan pesan lama sebagai
  belum dibaca, tombol tandai terbaca menghapus penanda, kirim pesan dari UI tersimpan,
  dan field "No. SPK / Invoice / Kontrak" menampilkan nilai apa adanya.
- Migrasi terpasang di basis data hidup: `schema_migrations` memuat v38 `crm_unit_doc_ref`
  dan v39 `crm_wo_discussion`; `crm.service` dijalankan ulang (restart disetujui HBA).

## Batas yang dipatuhi

Tidak ada modul, peran, izin, atau aturan bisnis baru di luar kedua putusan. Tidak ada
notifikasi/email (HBA hanya meminta diskusi internal). Angka badge, siapa yang boleh baca,
dan bentuk field dokumen semuanya berasal dari kata HBA, bukan karangan teknis.

## Sisa pekerjaan

- Pekerjaan ini masih **belum di-commit**: `crm/` dan `docs/` belum pernah masuk git.
  Klaim "branch ter-push" pada fase-fase otomatis sebelumnya juga belum pernah benar.
  Perlu keputusan HBA apakah mau commit resmi.

*End of implementation record.*
