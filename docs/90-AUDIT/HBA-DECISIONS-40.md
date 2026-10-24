# IMPLEMENTATION RECORD — tombol Cetak & Unduh SVG dihapus dari blok barcode

```text
Record ID:      HBA-DECISIONS-40
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruction:    "Hilangkan saja cetak dan svg nya" (HBA, chat 2026-10-24)
Status:         IMPLEMENTED — terpasang, teruji di peramban, sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Yang diubah

Blok barcode/QR pada Profil Unit kini hanya berisi GAMBARNYA. Setelah sebelumnya
judul di atas dan kode/tautan di bawah dihapus, dua tombol yang tersisa —
"Cetak" dan "Unduh SVG" — juga dihilangkan. Komponen `QrImage` sudah punya
sakelar untuk itu (`actions={false}`), jadi tidak ada komponen baru maupun
perubahan perilaku di tempat lain: pemanggil lain tetap memakai bawaannya.

Dengan begitu blok barcode tidak lagi memuat tulisan maupun kendali apa pun;
keterangannya hanya tersisa sebagai atribut `title` pada bingkainya, yang tidak
terlihat di layar.

## Bukti

- 19/19 cek peramban nyata pada permukaan Profil Unit
  (`crm/ui/verify_unit_profile.mjs`), termasuk cek baru: teks di dalam blok
  barcode benar-benar kosong dan jumlah tombol di dalamnya nol, sementara gambar
  QR-nya tetap ada dan tetap mengarah ke tautan portal unit yang benar.
- `npm run typecheck` bersih; `npm run build` sukses; UI dijalankan ulang dan
  berkas baru sudah dilayani (port 8092 menjawab 200). Tidak ada perubahan
  backend pada putaran ini.

## Catatan

Dua layar lain (detail Pelanggan) memakai komponen QR yang sama dan MASIH
menampilkan tombol Cetak/Unduh SVG. Putaran ini hanya menyentuh blok barcode
Profil Unit yang sedang dibahas. Kalau HBA ingin tombol itu hilang di sana juga,
cukup dikatakan — satu baris perubahan per pemanggil.

Commit `31a1f1f` pada branch `feat/wo-discussion-20261024`
(`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main`.

*End of implementation record.*
