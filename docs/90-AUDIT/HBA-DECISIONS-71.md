# HBA-DECISIONS-71 — Admin boleh menerbitkan QR unit

Pertanyaan HBA lewat chat 27 Okt 2026: kenapa kode QR profil unit belum
diterbitkan. Jawabannya: dua unit (DELO-01, MEBS-04) belum punya kode dan
penerbitan hanya boleh oleh Manager/Koordinator, jadi akun Admin ditolak.
Putusan HBA: beri Admin wewenang menerbitkan QR.

## Yang dikerjakan

`app/unit/qr.py` mendapat daftar wewenang sendiri `ISSUE_ROLES` berisi
Manager, Koordinator, dan Admin. Sengaja tidak menumpang
`unit.VALIDATE_ROLES` yang tetap Manager dan Koordinator saja, supaya
wewenang validasi unit tidak ikut melebar. Pesan penolakan, komentar kanon
di berkas, dan tulisan di layar disesuaikan. Dua kode yang kurang
(DELO-01, MEBS-04) diterbitkan langsung memakai akun Admin sebagai bukti
wewenang baru jalan — sekarang sepuluh unit semuanya berkode.

## Bukti

- `tests.test_unit_qr` 20 uji lolos, termasuk uji baru bahwa Admin bisa
  menerbitkan dan teknisi tetap ditolak.
- Satu uji rute yang tadinya merah (`..._denied_on_public_door`) terbukti
  merah juga di pohon bersih tanpa perubahan saya: ekspektasi 404-nya basi
  sejak `/api/unit/` menjadi prefix publik. Uji itu saya perbarui mengikuti
  aturan baku (anonim tetap 401, login dilayani) dan diganti nama.
- Penerbitan langsung di database live oleh Admin berhasil untuk kedua unit.
- `npm run typecheck` bersih, bundle baru tersaji sama dengan hasil build.
- Layanan `crm.service` dan `crm-ui.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `feat/unit-qr-admin-20261027`, commit `eef1cfb`, sudah
  push, belum merge. Yang berubah: `app/unit/qr.py`,
  `tests/test_unit_qr.py`, `ui/src/screens/UnitScreen.tsx`.
