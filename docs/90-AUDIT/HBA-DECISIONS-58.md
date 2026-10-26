# IMPLEMENTASI — tautan unit tidak merah lagi, alamat halaman unit memakai rujukan acak

```text
Record ID:      HBA-DECISIONS-58
Date:           2026-10-26
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruksi HBA:  "1. tulisan (link) unit genset pada profil pelanggan masih merah.
                 tolong dirubah
                 2. page unit tetap belum acak. masih berurutan. saya bingung,
                 kalian yang merekomendasikan dengan acak, tapi kalian juga yang
                 tidak mematuhi. tetap memberikan nomor berurutan."
Status:         IMPLEMENTED — terpasang, 12 cek peramban LULUS
Classification: Audit record. NOT a canonical specification document.
```

## Butir 1 — tautan unit tidak merah lagi

Tautan kode unit dan nama unit pada **profil pelanggan** memakai **warna teks
biasa** (putih), bukan merah. Tanda bahwa itu bisa diklik dibawa oleh garis bawah
putus-putus, bukan warna. Diukur di peramban: `rgb(246, 246, 247)` — warna teks
aplikasi, bukan `rgb(239, 43, 43)`.

## Butir 2 — alamat halaman unit sekarang acak

Sebelumnya alamat unit memakai nomor berurutan (`#/unit/33`), sehingga halaman
berikutnya bisa ditebak. Sekarang setiap unit punya **rujukan acak** yang tetap:

- Kolom baru `units.public_ref` — **migrasi v46**, 12 karakter dari CSPRNG
  (`abcdefghijkmnopqrstuvwxyz23456789`, tanpa `0/1/l/o` supaya tidak salah baca),
  **unik** lewat indeks, diisi untuk **semua unit lama** dan dibuat otomatis untuk
  unit baru.
- Alamat halaman memakai rujukan itu: `#/unit/hae6eavy3qus`, bukan `#/unit/48`.
- Tautan dari profil pelanggan, hash di address bar, dan tautan yang dibagikan
  semuanya memakai rujukan. Tautan **berbasis nomor tetap hidup** — bila dibuka,
  alamatnya dinormalkan ke rujukan, jadi tidak ada tautan yang sudah tersebar
  menjadi mati.

Batasnya jelas dan disengaja: rujukan acak hanya membuat alamat **tidak bisa
ditebak**; ia **bukan** pengganti kewenangan, karena sesi dan peran tetap
diperiksa server pada setiap permintaan. Kode QR portal (`unit_qr_codes`) **tidak**
dipakai untuk alamat internal — ia sengaja dipakai pelanggan dan tidak dicampur.

Contoh rujukan yang sekarang tersimpan: MADI-01 `qo5sbtnchae2`, MADI-02
`jynh3zdv8hjf`, MADI-03 `7echhyypjt9u`, MEBS-01 `hae6eavy3qus`.

## Catatan kejujuran tentang pohon kerja bersama

Sesi lain (batch 3: Ubah WO, timestamp, sebut @) **ikut meng-commit sebagian berkas
batch ini** di commit `78f1ae8` — pohon kerja dipakai bersama, dan `git commit`
mereka menyapu berkas yang sedang saya ubah. Isinya tetap benar dan terverifikasi,
tetapi riwayatnya tidak bersih: sebagian perubahan ini berada di commit sesi lain,
sisanya di commit `c77e899`. Selain itu **nomor migrasi bentrok**: sesi itu memakai
45 (awalnya menulis 44) sementara saya sudah menulis 45; saya pindahkan rujukan
acak unit ke **46** dan mengurutkan registry (43, 44, 45, 46). Migrasi 45 milik
sesi itu sudah terlanjur tercatat di database live, jadi penomoran ulang ke 46
adalah jalan yang benar — bukan menghapus catatannya.

## Bukti

- `tests.test_migrations` 6 OK, `tests.test_unit` 10 OK,
  `tests.test_unit_server` 4 OK, `tests.test_unit_spec` 40 OK.
- `verify_unit_ref_20261026.cjs` di deployment nyata (8092): **12 cek LULUS** —
  semua 8 unit punya rujukan acak yang tidak kembar; tautan profil pelanggan
  berwarna `rgb(246, 246, 247)`; href berbentuk `#/unit/<rujukan>` dan cocok dengan
  database; klik tautan membuka unit yang benar dengan alamat berujukan; deep link
  `#/unit/<rujukan>` benar; tautan lama `#/unit/33` masih membuka unitnya lalu
  alamatnya **dinormalkan** ke `#/unit/qo5sbtnchae2`; 0 galat JavaScript.
- Migrasi live: `schema_migrations` berisi 44, 45, 46; `units.public_ref` ada dan
  **0 unit** yang kosong.
- Bundle `index-pkXYvqmf.js` disajikan ulang setelah `crm-ui.service` restart.

## Berkas

`crm/app/migrations/migrate.py` (v46), `crm/app/unit/unit.py`,
`crm/ui/src/App.tsx`, `crm/ui/src/screens/UnitScreen.tsx`,
`crm/ui/src/screens/CompanyDetailScreen.tsx`, `crm/ui/src/types.ts`,
`crm/ui/src/styles.css`, `crm/ui/verify_unit_ref_20261026.cjs` (baru).

Satu migrasi aditif (kolom + indeks unik, reversibel); tanpa endpoint baru; tanpa
aturan bisnis baru.
