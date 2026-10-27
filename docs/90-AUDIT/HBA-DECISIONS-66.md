# HBA-DECISIONS-66 — Tanggal tampil DD/MM/YYYY

Perintah HBA lewat chat 27 Okt 2026: format penanggalan di website menjadi
DD/MM/YYYY.

## Yang dikerjakan

Dua fungsi pusat di `ui/src/lib/format.ts` yang dipakai semua layar diubah:
`fmtDate` menjadi DD/MM/YYYY dan `fmtDateTime` menjadi DD/MM/YYYY HH:MM.
Kolom isian tanggal di form tidak diubah karena browser memang memakai format
baku di balik layar. Tidak ada perubahan skema, endpoint, atau aturan bisnis.

## Bukti

- `npm run typecheck` bersih, `npm run build` jadi satu bundle baru.
- Halaman yang disajikan server sama dengan hasil build (cek hash HTML cocok).
- Layanan `crm-ui.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `feat/tanggal-ddmmyyyy-20261027`, commit `5511100`, sudah
  push, belum merge. Yang berubah hanya `ui/src/lib/format.ts`.
