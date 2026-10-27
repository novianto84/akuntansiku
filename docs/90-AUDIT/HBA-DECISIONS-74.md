# HBA-DECISIONS-74 — Panel penugasan ringkas

Perintah HBA lewat chat 27 Okt 2026: saat belum ada teknisi cukup satu kolom
cari nama yang otomatis menjadi utama; setelah tersimpan tampil foto dan
namanya tanpa label peran; tombol tambah teknisi baru muncul di bawahnya;
tanpa tabel support, tanpa keterangan panjang; alasan terisi otomatis
"penugasan umum" dan bisa diganti.

## Yang dikerjakan

Panel Penugasan ditulis ulang. Belum ada teknisi: satu kolom cari nama,
tombol Tugaskan, teknisi pertama otomatis PRIMARY. Sudah ada: tiap baris
hanya foto profil (inisial bila belum punya foto) dan nama. Tombol
"+ Add teknisi" hanya muncul setelah teknisi pertama tersimpan; teknisi
berikutnya tercatat SUPPORTING di backend tanpa label di layar. Alasan
terisi "penugasan umum" dan tetap bisa diubah; kewajiban alasan tercatat
tetap dijaga backend seperti sebelumnya. Tabel peran, daftar alasan, dan
semua keterangan (satu utama, hak support, alasan wajib, otoritas) dibuang.
Backend `list_assignments` kini mengikutkan penanda foto teknisi (tanpa
byte gambar), supaya avatar tampil untuk semua peran lewat jalur yang sama
dengan daftar penugasan.

## Bukti

- `tests.test_assignment` 16 uji lolos.
- Skrip bukti: daftar penugasan memuat kolom foto (null = inisial, jujur).
- `npm run typecheck` bersih, bundle memuat teks baru, halaman tersaji sama
  dengan hasil build.
- Layanan `crm.service` dan `crm-ui.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `feat/penugasan-ringkas-20261027`, commit `c837425`,
  sudah push, belum merge. Yang berubah: `app/wo/assignment.py`,
  `ui/src/types.ts`, `ui/src/screens/WoDetailScreen.tsx`.
