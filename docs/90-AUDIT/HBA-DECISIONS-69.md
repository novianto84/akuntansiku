# HBA-DECISIONS-69 — Kartu identitas detail WO dua kolom

Perintah HBA lewat chat 27 Okt 2026: tabel WO pada detail work order dibagi
menjadi dua kolom.

## Yang dikerjakan

Komponen `Dl` mendapat pilihan `twoCol` dan CSS `dl--2col` yang memasang dua
pasang label-nilai berdampingan di layar lebar dan kembali satu kolom di
layar sempit. Yang memakai hanya kartu identitas di detail WO; panel Laporan
dan semua layar lain tetap satu kolom. Tidak ada perubahan data, endpoint,
atau aturan.

## Bukti

- `npm run typecheck` bersih, `npm run build` jadi bundle baru yang memuat
  kelas dan properti baru.
- Halaman tersaji sama dengan hasil build (cek hash HTML cocok).
- Layanan `crm-ui.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `feat/wo-detail-dua-kolom-20261027`, commit `5834cd3`,
  sudah push, belum merge. Yang berubah: `ui/src/components/ui.tsx`,
  `ui/src/styles.css`, `ui/src/screens/WoDetailScreen.tsx`.
