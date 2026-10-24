# HBA DECISION RECORD — Kunci IS-09 + rate-limit login & QR (2026-10-13)

```text
Record ID:      HBA-DECISIONS-21
Date:           2026-10-13
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-13
Classification: Audit record. NOT a canonical specification document.
Implementation: No code/schema/migration/DB written by this record.
```

> Rekaman tangkap perintah HBA verbatim. Tak tulis kode.

## Putusan HBA (inti)

- IS-09 dikunci jadi aturan tetap.
- Batas login: 5x gagal kunci 2 jam.
- Batas scan QR kode invalid sama: 5x gagal kunci 2 jam per alamat.

## Bacaan kunci

- IS-09 kini LOCKED/CANONICAL v1.0; bukan lagi PROPOSED.
- Angka 5x/2jam login + QR invalid adalah angka HBA, bukan desain implementasi.
- "Per alamat" = per alamat peminta (mis. alamat/IP asal); definisi teknis alamat ikut implementasi, ambang 5x/2jam tetap.
- QR di sini hanya soal batas tebak kode invalid; mekanisme QR lain tetap ikut HBA-DECISIONS-17.

## Supersede

- HBA-19 (tutup tanpa rate-limit, hanya di ledger, belum ada file — dicatat HBA-DECISIONS-20 sebagai utang arsip) SUPERSEDED oleh putusan ini untuk soal rate-limit.
- IS-09 §8 wording lama ("scope/thresholds are implementation design") retained sebagai riwayat; angka HBA di atas override untuk login + QR invalid.
- Nol aturan bisnis baru selain angka HBA di atas.

## Batas

- Record tak tulis kode rate-limit, tabel, endpoint. Itu paket eksekusi via governed path perlu otorisasi tulis terpisah.
- Fakta `qr.py` tulis rate-limit NOT implemented dan login lockout belum ada angka: tetap fakta kode, bukan penolakan putusan.

## Langkah berikut termurah

Eksekusi rate-limit 5x/2jam via governed path berotorisasi, lalu uji hidup login + QR.

*End of decision record.*
