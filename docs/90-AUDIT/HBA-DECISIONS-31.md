# HBA DECISION RECORD — Diskusi WO: internal-only, kotak masuk/dashboard (2026-10-17)

```text
Record ID:      HBA-DECISIONS-31
Date:           2026-10-17
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-17 via chat (lengkap setelah klarifikasi)
Classification: Audit record. NOT a canonical specification document.
Implementation: NONE — belum ada otorisasi eksekusi. Modul diskusi WO belum ada di kanon.
```

> Rekaman putusan HBA verbatim. Dokumen jejak, bukan spesifikasi.

## Putusan HBA (lengkap)

- Diskusi WO boleh dibaca semua pihak internal. Tidak bisa oleh external.
- Tempat: cukup kotak masuk saja, atau di dashboard pekerja.
- Penanda: badge angka di menu/kotak masuk (jumlah diskusi belum dibaca). [klarifikasi 2026-10-17]
- "Satu kolom saja" TIDAK untuk diskusi WO — itu menjawab pertanyaan SPK/invoice/kontrak di sesi genset (lihat HBA-DECISIONS-32).

## Kondisi nyata terverifikasi

- Tidak ada tabel diskusi/komentar/thread di `migrate.py` (hanya `intake_replies` v15 untuk panel intake, bukan diskusi WO).
- Tidak ada kotak masuk / notifikasi di `app/` maupun `ui/src/`.
- Modul diskusi WO = modul baru, belum ada di kanon.

## Batas

Tanpa jawaban atas bagian ambigu + otorisasi eksekusi eksplisit, tidak ada skema/tabel/UI yang dibuat.

## Langkah berikut termurah

Jawab dua bagian ambigu (penanda apa, satu kolom apa), lalu catat putusan lengkap dan susun proposal skema + UI untuk otorisasi.

*End of decision record.*
