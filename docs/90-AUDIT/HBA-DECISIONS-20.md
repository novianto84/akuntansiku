# HBA DECISION RECORD — Audit+selaraskan semua kanonik: IS-03 v1.4 + IS-06 v1.3 LOCKED (2026-10-12)

```text
Record ID:      HBA-DECISIONS-20
Date:           2026-10-12
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — order "audit saja, buang yang basi, selaraskan dengan terbaru" + "kunci IS-06"
Classification: Audit record. NOT a canonical specification document.
Implementation: No code/schema/migration/DB written by this record.
```

> Rekaman tangkap perintah HBA di chat 2026-10-12. Tak edit kanonik selain yang diotorisasi.

## Temuan audit (terverifikasi)

- IS-03 V-4 tulis elevasi otomatis sebagai kondisi kini, padahal HBA-16/18 kunci link manual. Basi.
- IS-06 §6/L-28/amendment tulis elevasi otomatis + acuan IS-03 v1.2. Basi.
- IS-06 status/footer DRAFT v1.2 campur perintah kunci. Basi.
- IS-04/05/07/11: tak ada elevasi otomatis, tak ada acuan versi basi. Bersih.
- HBA-DECISIONS-19 (tutup tanpa rate-limit) hanya di ledger, belum ada file. Dicatat sebagai utang arsip.

## Perbaikan

- IS-03 v1.4 LOCKED: V-4 kondisi kini = manual intake, elevasi otomatis + two-tier jadi riwayat superseded retained. SHA `ed2c8e62433ab32ea7d9c2dc0b468633e1520d58e9245a21e9135dac404469f8`.
- IS-06 v1.3 LOCKED: §6/§9/L-28/amendment/konsistensi selaras HBA-13/16/17/18, acuan IS-03 v1.4, status+footer LOCKED. L 28 baris cocok register. SHA `e92a9f62a4651338cc035152725432ec0f32c9f471a0cef3fbfb57239d8939e4`.
- Nol aturan bisnis baru. Wording lama retained sebagai riwayat, tak dihapus.

## Batas

- IS-09/IS-10 masih PROPOSED, IS-FINAL masih konsolidasi — di luar perintah kunci ini.
- HBA-19 belum ada file arsip.

## Langkah berikut termurah

Arsipkan HBA-19 ke file, lalu uji hidup Google + QR, cabut lokal, commit tree kotor.

*End of decision record.*
