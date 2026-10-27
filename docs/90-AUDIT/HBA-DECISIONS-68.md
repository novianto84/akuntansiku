# HBA-DECISIONS-68 — Tanggal penugasan bisa diubah dari detail WO

Keluhan HBA lewat chat 27 Okt 2026: tanggal penugasan belum bisa diubah di
halaman detail WO.

## Temuan

Kolomnya sudah ada di database dan form pembuat WO bisa mengisinya, tetapi
jendela Ubah WO tidak punya field tanggal dan backend `wo_mod.update` tidak
menerima tanggal — jadi tidak ada jalur ubah sama sekali. Ini permukaan yang
hilang, bukan aturan baru: makna kosong = NULL sudah diputuskan 26 Okt 2026
dan tetap dipakai.

## Yang dikerjakan

Jendela Ubah WO mendapat isian tanggal penugasan (boleh dikosongkan;
dikosongkan tersimpan sebagai belum ditetapkan). Backend meneruskan tanggal
hanya bila kuncinya dikirim, memakai validasi yang sama dengan saat
pembuatan: format salah ditolak dengan pesan terbaca. Pengiriman ubah yang
tidak membawa kunci tanggal tidak mengubah nilai lama. Tidak ada perubahan
skema atau aturan bisnis.

## Bukti

- Skrip bukti: tanpa kirim tanggal nilai dipertahankan, kirim tanggal
  tersimpan, kirim kosong dibersihkan, format salah ditolak — lolos.
- `tests.test_batch3_wo_edit_timestamp` 7 uji lolos.
- `npm run typecheck` bersih, `npm run build` jadi bundle baru yang memuat
  field tanggal, halaman tersaji sama dengan hasil build.
- Layanan `crm.service` dan `crm-ui.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `feat/wo-edit-assign-date-20261027`, commit `ecb199a`,
  sudah push, belum merge. Yang berubah: `app/wo/wo.py`, `app/server.py`,
  `ui/src/components/WoEditModal.tsx`.
