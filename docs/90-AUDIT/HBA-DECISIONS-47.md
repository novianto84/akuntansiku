# PERBAIKAN KEAMANAN — tautan unit bernomor bisa ditebak + profil unit untuk pelanggan

```text
Record ID:      HBA-DECISIONS-47
Date:           2026-10-26
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Laporan HBA:    "link unit masih berurutan. bukankah ini berarti siapa saja
                 tinggal mengganti link dan menaikan satu satu angka? bukankah
                 lebih baik di shuffle link dengan kode di barcode. yang kemarin
                 sekitar 10 / 15 karakter?"
Status:         FIXED — celah ditutup, teruji (4 tes baru + pemeriksaan langsung)
Classification: Audit record. NOT a canonical specification document.
```

## Kecurigaan HBA benar, dan lebih serius daripada yang terlihat

Yang bisa ditebak bukan hanya alamat halaman, melainkan **rute datanya**. Sebelum
perbaikan, akun pelanggan biasa (`Pelanggan_umum`, akun yang lahir dari login
Google tanpa ditautkan ke perusahaan mana pun) bisa membaca unit **milik
perusahaan lain** hanya dengan menaikkan angka. Bukti langsung dari sistem yang
berjalan, dengan sesi pelanggan nyata:

```text
GET /api/customer/unit/35  -> 200  {"unit_code": "MADI-03",  ... perusahaan 6}
GET /api/customer/unit/48  -> 200  {"unit_code": "MEBS-01",  ... perusahaan 8}
```

Dua permintaan itu datang dari akun pelanggan yang sama, dan dua unit itu milik
dua perusahaan berbeda. Penyebabnya: rute numerik itu memakai **UNIT_SCOPE**,
yang artinya hanya "satu workspace" — bukan "perusahaan Anda". Jadi pagarnya
hanya selebar workspace, padahal workspace-nya satu untuk semua pelanggan.

Halaman internal `#/unit/<angka>` sendiri TIDAK bocor: rute itu menolak peran
pelanggan (`403 "peran pelanggan tidak berwenang pada permukaan operasional"`),
jadi menaikkan angka di alamat halaman internal hanya berarti bagi staf — dan
staf memang berhak melihat seluruh unit di workspace-nya.

Perlu dicatat dengan jujur: pada putaran yang sama saya baru menambahkan **profil
unit** (namaplate) ke proyeksi pelanggan. Artinya selama beberapa menit sebelum
perbaikan ini, rute numerik itu juga membuka namaplate — termasuk nomor seri —
lintas perusahaan. Jendela itu hanya berisi akun uji yang sedang saya pakai
(`cust_dev`), tidak ada bukti dipakai pihak lain, dan sejak commit
`a5fb109` rute itu menolak.

## Yang diperbaiki

`/api/customer/unit/<id>` sekarang menuntut **COMPANY_SCOPE terverifikasi** untuk
perusahaan PEMILIK unit itu — yaitu identitas pelanggan yang sudah ditautkan
staf. Akun QR-only ditolak di rute itu. Jalan masuk untuk mereka tetap satu:
**kode QR unit**, yang memang sudah acak dan bukan angka — 10 karakter dari
abjad tanpa huruf/angka kembar (`A4KZV7MAJG`, `Q864P8452E`), sesuai yang HBA
ingat "sekitar 10/15 karakter". Jadi saran HBA ("shuffle link dengan kode di
barcode") memang sudah menjadi bentuk tautan pelanggan sejak awal
(`#/portal-unit?code=…`); yang salah adalah rute API numerik di belakangnya, dan
itu yang ditutup.

Pemisahan fungsinya sekarang jelas: **kode QR memilih unit** (acak, per unit,
tanpa kedaluwarsa, dan setiap tebakan kode yang salah dihitung per alamat IP),
sedangkan **tautan identitas pelanggan** hanya berlaku untuk unit perusahaannya
sendiri.

## Profil unit untuk pelanggan (putusan HBA 2026-10-26)

HBA menjawab pertanyaan "data profil mana yang boleh dilihat pelanggan" dengan:
*"semua tampilan pada page https://crm.benshi.my.id/#/unit/48. yaitu menu
riwayat, dan profil unit."* Karena itu proyeksi pelanggan kini memuat profil unit:
identitas (kode, nama, tipe, pelanggan/pemilik, siklus hidup) + seluruh field
namaplate + perlengkapan (berlabel, bukan kode mentah), di samping riwayat
layanan customer-safe yang sudah ada.

Dua pengecualian SENGAJA dipertahankan, karena HBA sendiri yang menyatakannya
internal lebih dulu: **nomor dokumen** (No. SPK / Invoice / Kontrak,
HBA-DECISIONS-32) dan **tanggal penyerahan unit** beserta lampirannya
(HBA-DECISIONS-30/34, adendum IS-06). Allowlist-nya disusun sebagai "semua field
namaplate DIKURANGI dua itu", jadi field baru di masa depan tidak otomatis
terkirim ke pelanggan tanpa keputusan. Kalau HBA ingin kedua hal itu ikut
tampil, cukup dikatakan — satu baris.

## Bukti

- **4 tes baru** (`tests/test_customer_wp08.py::TestUnitByNumericIdIsNotEnumerable`):
  akun QR-only ditolak di rute numerik untuk dua unit berbeda; akun terverifikasi
  hanya bisa membaca unit perusahaannya sendiri dan ditolak untuk perusahaan
  lain; kode QR tetap membuka unitnya; dan profil pelanggan memuat namaplate
  TETAPI tidak memuat `doc_ref` maupun `delivery_date`. Seluruh modul itu
  dijalankan ulang (hasil di laporan chat).
- **Pemeriksaan pada sistem yang berjalan** sesudah perbaikan:
  `GET /api/customer/unit/35` dan `/48` -> **403** untuk sesi pelanggan QR-only,
  sementara `GET /api/customer/qr/A4KZV7MAJG` -> **200** dengan profil lengkap
  (20 field namaplate, tanpa dua field internal, perlengkapan berlabel).
- Pemeriksaan peramban untuk sisi tampilan portal ada di rekaman berikutnya
  (HBA-DECISIONS-48): profil unit, slide gambar, dan riwayat tampil, sedangkan
  nomor dokumen dan tanggal penyerahan tidak pernah muncul di halaman pelanggan.

## Sisa yang perlu HBA ketahui

Kalau nanti ada tautan unit yang dibagikan ke pelanggan **terverifikasi**
(mis. "unit saya"), bentuknya tetap numerik dan itu wajar: batasnya kini
perusahaan, bukan angka. Untuk pemakaian sehari-hari, tautan yang dibagikan
tetap yang berisi kode QR — angka tidak pernah menjadi kunci akses pelanggan.

Commit `a5fb109` pada branch `feat/galeri-profil-unit-20261026`
(`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main` — menunggu HBA.

*End of record.*
