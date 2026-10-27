# HBA-DECISIONS-65 — Detail WO memuat data genset

Perintah HBA lewat chat 27 Okt 2026: halaman detail Work Order wajib
mencantumkan merk mesin, SN mesin, type mesin, merek generator, SN generator,
dan type generator.

## Yang dikerjakan

Enam baris ditambahkan di kartu identitas WO, tepat di bawah baris Unit,
diambil dari data unit yang tertaut (merk = `engine_brand`/`generator_brand`,
type = `engine_model`/`generator_model`, SN = `engine_serial`/
`generator_serial`). Bila unitnya punya tapi kolomnya kosong tertulis belum
tercatat, bila WO belum punya unit tertulis menyusul setelah Unit dipilih —
tidak ada angka atau nama yang dikarang. Tidak ada perubahan skema, endpoint,
atau aturan bisnis: murni penyajian ulang data yang sudah ada.

## Bukti

- `npm run typecheck` bersih, `npm run build` jadi satu bundle baru.
- Label baru ada di bundle, dan halaman yang disajikan server sama dengan hasil
  build (cek hash HTML cocok).
- Layanan `crm.service` dan `crm-ui.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `feat/wo-detail-genset-20261027`, commit `19ea00d`, sudah
  push, belum merge. Yang berubah hanya `ui/src/screens/WoDetailScreen.tsx`.
