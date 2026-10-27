# HBA-DECISIONS-76 — Penugasan 2 kolom + WA, material per submit, hapus foto

Tiga perintah HBA lewat chat 27 Okt 2026 untuk halaman detail WO.

## Penugasan dua kolom + hubungi teknisi

Panel Penugasan kini dua kolom: kiri daftar teknisi dan kolom cari, kanan
alasan penugasan. Tiap teknisi tampil foto profilnya yang diperbesar, baris
pertama nama, baris kedua ikon chat WA dan ikon telepon bila nomornya
tercatat (ikon chat membuka wa.me, ikon telepon memakai tel:). Tanpa nomor
tertulis tanpa nomor WA tercatat. Tanpa label peran dan tanpa semua
keterangan panjang. Nomor telepon diambil dari profil staf lewat jalur yang
sama dengan daftar penugasan; batas privasinya sama dengan daftar pekerja
(nama + nomor telpon boleh, KTP/NPWP/alamat tidak ikut).

## Material per submit + kumulatif

Daftar material dikelompokkan per submit (satu tanggal = satu submit),
setiap kelompok punya tombol Ubah yang membuka tanggal + semua barisnya
untuk diedit sekaligus lalu disimpan. Kumulatif pemakaian 1 WO tampil di
bawah daftar dan tetap dijaga. Form catat baru tidak berubah. Tidak ada
perubahan backend: edit memakai ujung ubah per baris yang sudah ada,
dipanggil berurutan.

## Hapus foto bukti

Ujung `DELETE /api/wo/{id}/photos/{pid}` baru beserta fungsi domainnya,
khusus Manager/Admin seperti persetujuan foto di permukaan yang sama,
workspace-scoped, baris dihapus permanen. Di layar tiap foto mendapat tombol
Hapus untuk Manager/Admin dengan konfirmasi dulu. HBA memerintahkan untuk
admin; Manager diikutkan mengikuti pola persetujuan foto yang sama.

## Bukti

- `tests.test_assignment` 16 uji lolos; `tests.test_wo_photo` 8 uji lolos
  termasuk uji hapus baru (teknisi ditolak, Admin menghapus permanen).
- `npm run typecheck` bersih, bundle memuat teks baru, halaman tersaji sama
  dengan hasil build.
- Layanan `crm.service` dan `crm-ui.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `feat/wo-tiga-permintaan-20261027`, commit `2d69527`,
  sudah push, belum merge. Yang berubah: `app/wo/assignment.py`,
  `app/wo/photo.py`, `app/server.py`, `ui/src/api.ts`,
  `ui/src/screens/WoDetailScreen.tsx`, `ui/src/styles.css`,
  `ui/src/types.ts`, `tests/test_wo_photo.py`.
