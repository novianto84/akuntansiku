# HBA-DECISIONS-73 — Semua isian tanggal DD/MM/YYYY

Keluhan HBA lewat chat 27 Okt 2026: isian tanggal masih MM/DD/YYYY,
terlihat di tanggal lahir data pekerja dan beberapa tempat lain.

## Temuan

Tampilan tanggal memang sudah DD/MM/YYYY sejak HBA-DECISIONS-66, tetapi
isian memakai `input type="date"` bawaan browser yang mengikuti bahasa
browser sehingga tetap tampil MM/DD/YYYY. Ditemukan tujuh titik: tanggal
lahir di data pekerja dan form pekerja, tanggal penugasan di form dan
jendela ubah WO, tanggal penyerahan unit, serta dua tanggal material di
detail WO.

## Yang dikerjakan

Komponen `DateField` baru di `ui/src/components/ui.tsx`: selalu tampil dan
menerima DD/MM/YYYY (ketikan bebas, tanggal tidak sah ditolak dan
dikembalikan saat fokus pindah, kosong = belum ditetapkan), sedangkan nilai
yang disimpan tetap ISO seperti sebelumnya sehingga backend tidak berubah
sama sekali. Ketujuh titik diganti ke komponen ini. Tidak ada perubahan
skema, endpoint, atau aturan.

## Bukti

- `npm run typecheck` bersih, bundle memuat format baru, halaman tersaji
  sama dengan hasil build.
- Layanan `crm-ui.service` aktif setelah deploy. Tidak ada lagi
  `type="date"` di kode layar.

## Berkas dan status git

- Repo CRM, branch `feat/isian-tanggal-ddmmyyyy-20261027`, commit `5c5318d`,
  sudah push, belum merge. Yang berubah: `ui/src/components/ui.tsx` dan
  enam layar/komponen pemakainya.
