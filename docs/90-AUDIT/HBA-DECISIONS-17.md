# HBA DECISION RECORD — Mekanisme QR Unit (2026-10-11)

```text
Record ID:      HBA-DECISIONS-17
Date:           2026-10-11
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         LOCKED / CANONICAL — promoted by HBA 2026-10-11 ("kanon sudah disetujui, lock dan approve")
Classification: Canonical decision record (promoted from audit record by explicit HBA order).
Implementation: No code/schema/migration/DB written by this record.
```

> Rekaman tangkap pernyataan HBA verbatim. Tak edit kanonik, tak tulis kode.

## Putusan HBA (inti)

- Kode QR acak pendek.
- Kalau tersebar tidak apa. Siapa pun boleh cetak ulang.
- QR untuk profil unit.
- Bebas siapa pun boleh buka, dengan signup atau login.
- Permanen murni.
- Cara mulai pakai (rollout) HBA putuskan 2026-10-11: layar saja. Kode jalan di layar/admin dulu, cetak fisik kapan saja menyusul.

## Bacaan kunci

- Token acak pendek simpan di database, satu kode satu unit. Bentuk panjang/karakter detail teknis menyusul di paket eksekusi.
- Tersebar bukan insiden: tak ada rotasi/revokasi karena bocor, tak ada cetak ulang terkendali. Konsekuensi: siapa pun pegang kode lihat profil customer-safe unit itu setelah login.
- CONTROLLED ACCESS tetap: tanpa login tanpa data. Bebas di sini artinya bebas siapa pun asal signup/login, bukan anonim.
- Permanen murni: tanpa kedaluwarsa, tanpa putar kunci berkala.
- Scope profil unit: identitas unit + riwayat customer-safe saja, tanpa harga, tanpa data perusahaan lain, tanpa lompat unit.

## Risiko catat (bukan tolak)

- Acak pendek lebih mudah tebak daripada panjang. TADR-16 minta tak bisa tebak. Mitigasi wajib di paket eksekusi: panjang/alfabet cukup + rate-limit scan. HBA sudah terima risiko sebar.
- Permanen murni tanpa cabut berarti kode bocor luas tak bisa dimatikan tanpa ganti kode + cetak ulang. HBA terima.

## Batas

- Record tak pilih panjang pasti, URL, rate-limit, tabel, endpoint. Itu paket eksekusi via governed path perlu otorisasi tulis terpisah.

## Langkah berikut termurah

HBA pilih cara mulai pakai, lalu otorisasi paket eksekusi QR.

*End of decision record.*
