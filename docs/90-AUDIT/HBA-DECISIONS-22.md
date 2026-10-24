# HBA DECISION RECORD — Kanon v16/v17 + kunci IS-10 + snapshot saat approve + panel konfigurasi + Google HBA ke manager (2026-10-13)

```text
Record ID:      HBA-DECISIONS-22
Date:           2026-10-13
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-13
Classification: Audit record. NOT a canonical specification document.
Implementation: No code/schema/migration/DB written by this record.
```

> Rekaman tangkap perintah HBA verbatim. Tak tulis kode. Dokumen saja.

## Perintah HBA verbatim (lima intent)

1. (a) Kanonkan migrasi v16 profil perusahaan sendiri + v17 lokasi visit.
2. (b) Kunci buku syarat pemasangan dan migrasi (IS-10).
3. (c) Salinan pelanggan dibuat saat WO ditutup yaitu saat manager approve.
4. (d) Perluas panel konfigurasi.
5. (e) Kaitkan Google HBA ke manager.

## Bacaan kunci

- v16 (profil perusahaan sendiri) + v17 (lokasi visit) adalah kanon migrasi per perintah (a); detail teknis ikut paket eksekusi, bukan record ini.
- IS-10 kini LOCKED/CANONICAL; bukan lagi PROPOSED. Wording lama PROPOSED retained sebagai riwayat.
- Timing snapshot pelanggan: saat WO ditutup yaitu saat manager approve (`approve_report` / CLOSED). Wording lama yang bertentangan retained sebagai riwayat superseded, tak dihapus.
- Perluasan panel konfigurasi + kaitan Google HBA ke manager dicatat sebagai perintah; rincian ikut addendum/eksekusi terotorisasi, nol aturan bisnis baru di luar perintah.
- Nol aturan bisnis baru selain kelima perintah di atas.

## Supersede

- Header IS-10 §Status wording lama ("PROPOSED — DRAFT FOR REVIEW (to be raised via IS-FINAL acceptance gate)") retained sebagai riwayat; status kini LOCKED/CANONICAL per perintah (b).
- Wording lama soal timing snapshot yang bertentangan dengan "saat manager approve / CLOSED" retained sebagai riwayat superseded di IS-01/IS-06; timing kanon kini ikut perintah (c).
- Nol penghapusan wording lama.

## Batas

- Record tak tulis kode/skema/migrasi/DB/endpoint. v16/v17 belum diverifikasi ada di tree (hanya `migrate.py` + `v10_customer_snapshots.py` terlihat); kanonisasi di sini adalah kanonisasi perintah, bukan bukti file migrasi.
- Eksekusi (migrasi, panel, Google-link) via governed path perlu otorisasi tulis terpisah.

## Langkah berikut termurah

Patch header IS-10 ke LOCKED/CANONICAL + adendum IS-01/IS-06 untuk v16/v17 + timing snapshot, lalu baca ulang header sebagai verifikasi.

*End of decision record.*
