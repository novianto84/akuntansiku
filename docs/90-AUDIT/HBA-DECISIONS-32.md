# HBA DECISION RECORD — SPK/invoice/kontrak di sesi genset: cukup 1 field (2026-10-17)

```text
Record ID:      HBA-DECISIONS-32
Date:           2026-10-17
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-17 via chat
Classification: Audit record. NOT a canonical specification document.
Implementation: NONE — belum ada otorisasi eksekusi.
```

> Rekaman putusan HBA verbatim. Dokumen jejak, bukan spesifikasi.

## Putusan HBA

Menjawab pertanyaan apakah nomor SPK / invoice / kontrak disatukan atau dibuat 3 field: cukup tambahkan 1 field saja di sesi genset.

Verbatim: "satu kolom saja itu maksudnya untuk menjawab tentang pertanyaan kamu nomor spk / invoice / kontrak disatukan saja atau dibuat 3 field. jadi maksudnya cukup tambahkan 1 field di sesi genset."

## Kondisi nyata terverifikasi

- Migrasi v30 `crm_unit_genset_spec` (HBA 2026-10-23) menambah kolom nameplate genset di `units` (merk, model, kVA, serial generator, jenis enclosure, serial genset, dll). Belum ada kolom SPK/invoice/kontrak.
- "Sesi genset" = bagian nameplate genset pada Unit card (migrasi v30).

## Batas

Tanpa otorisasi eksekusi eksplisit, tidak ada kolom/field yang ditambah.

## Langkah berikut termurah

Tentukan nama + tipe 1 field itu (mis. `genset_doc_ref` TEXT), ajukan sebagai migrasi v31 + field di sesi genset untuk otorisasi.

*End of decision record.*
