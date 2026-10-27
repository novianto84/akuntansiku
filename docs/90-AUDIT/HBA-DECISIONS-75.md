# HBA-DECISIONS-75 — Admin boleh validasi unit

Keluhan HBA lewat chat 27 Okt 2026: riwayat (tab Riwayat unit) tidak bisa
divalidasi. Tombol Validasi di sana ditolak untuk akun Admin.

## Temuan

Wewenang validasi unit (`VALIDATE_ROLES`) terkunci untuk Manager dan
Koordinator — dibuktikan langsung akun Admin ditolak sedangkan Manager
lolos. Semua sebelas unit masih NEW sehingga tombol ini memang sedang
dibutuhkan. Putusan HBA: Admin diberi wewenang validasi. Ini perubahan
kanon yang disetujui HBA, dicatat di sini.

## Yang dikerjakan

`VALIDATE_ROLES` menjadi Manager, Koordinator, dan Admin; pesan penolakan
dan komentar kanon disesuaikan. Cakupan pas: `activate`/`deactivate` memang
tidak memakai daftar ini (tanpa gate peran), jadi tidak ada wewenang lain
yang ikut melebar. Komentar basi di `qr.py` yang menyebut otoritas validasi
terkunci ikut diluruskan. Tidak ada perubahan skema atau alur.

## Bukti

- `tests.test_unit` 10 uji lolos, termasuk uji baru Admin bisa memvalidasi
  dan Sales tetap ditolak.
- `tests.test_unit_qr` 20 uji lolos.
- Pemeriksaan live setelah deploy: akun Admin lolos gate validasi.
- Layanan `crm.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `feat/unit-validasi-admin-20261027`, commit `538ce93`,
  sudah push, belum merge. Yang berubah: `app/unit/unit.py`,
  `app/unit/qr.py` (komentar), `tests/test_unit.py`.
