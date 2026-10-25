# IMPLEMENTASI — field "Merk genset": kolomnya sendiri, dan jadi sumber logo genset

```text
Record ID:      HBA-DECISIONS-44
Date:           2026-10-25
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruksi HBA:  "merk genset belum ada di field. dan merek tersebut nantinya yang
                 akan menjadi logo pada genset"
Status:         IMPLEMENTED — terpasang, teruji (86 tes + 33 cek peramban), sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Keadaan sebelum perubahan (bukti, bukan dugaan)

Mandat ini benar, dan kodenya sendiri sudah mencatat kekurangannya: `units` tidak
punya kolom merek tingkat genset. Yang ada hanya `genset_serial` — nomor seri,
bukan merek. Akibatnya bingkai logo "GENSET" di baris namaplate terpaksa
meminjam merek mesin/generator/controller, dan pada unit yang merek mesinnya
belum punya gambar GENSET, bingkainya selalu kosong. Di basis data nyata: enam
unit, tidak satu pun punya kolom merek genset.

## Yang diubah

Satu perubahan skema, **migrasi v42 `crm_unit_genset_brand`**: `units` mendapat
kolom `genset_brand` (teks, NULL bila belum diisi; tidak ada nilai yang diisi
dari unit lain atau dari daftar merek mana pun). Migrasi bersifat aditif,
idempoten (dijalankan dua kali tidak menggandakan apa pun) dan punya jalur turun.

Di sekitarnya:

- `app/unit/unit.py` — `genset_brand` masuk daftar field namaplate `units`, jadi
  ia tersimpan, tersaring, dan tersimpan-kapital dengan aturan yang SAMA seperti
  merek mesin/generator/controller ("isian dari setiap field auto capital").
- `app/unit/assets.py` — pencocokan gambar merek GENSET berhenti meminjam:
  `GENSET -> genset_brand`, bukan lagi ke seluruh merek namaplate. Merek yang
  tidak tercatat berarti bingkainya kosong.
- `app/unit/spec_options.py` — saran isian untuk field ini MURNI dari lookup
  (merek genset yang sudah pernah dicatat di workspace itu). HBA tidak menyebut
  satu pun merek genset, jadi tidak ada daftar yang dikarang — sama persis
  perlakuan untuk "Type generator" yang juga tanpa daftar dari HBA.
- `ui/...` — field "Merk genset" tampil paling atas di grup **Genset** pada
  jendela spesifikasi dan pada kartu unit, dan bingkai logo GENSET membaca kolom
  ini (`brandForUnit`).

## Yang mengikuti dengan sendirinya (tidak ada kode tambahan)

Halaman **Galeri Logo & Perlengkapan** membangun slotnya dari merek yang tercatat
pada unit. Begitu sebuah unit mencatat "Merk genset", slot logo untuk merek itu
muncul sendiri di sana, dan mengunggahnya langsung mengisi bingkai GENSET pada
unit tersebut. Karena itu **hari ini bagian Genset di Galeri masih kosong**: belum
ada satu unit pun yang mencatat merek gensetnya — bukan cacat, melainkan
konsekuensi dari data yang belum ada.

## Bukti

- **86 tes otomatis lulus** pada empat modul yang tersentuh (`test_unit_spec` 40,
  `test_unit_assets` 20, `test_unit_spec_options` 20, `test_migrations` 6).
  Yang baru, khusus putaran ini: migrasi v42 naik–turun–idempoten; fieldnya
  tersimpan kapital dan bisa dikosongkan; mengubah merek mesin **tidak**
  menyentuh merek genset; dan satu uji pencocokan yang sengaja dibuat berbeda —
  unit dengan `engine_brand=Yanmar` dan `genset_brand=Perkins` plus gambar untuk
  KEDUA merek itu: bingkai GENSET yang dipakai adalah **PERKINS**, membuktikan
  peminjaman merek mesin sudah berakhir.
- **33/33 cek peramban nyata** pada UI yang benar-benar dilayani pengguna
  (`:8092`, `crm/ui/verify_unit_profile.mjs`): kartu unit menampilkan baris
  "Merk genset" di grup Genset (terisi "—" karena memang belum diisi), jendela
  spesifikasi menyediakan isian teks bebas untuk field itu, dan seluruh cek
  putaran sebelumnya (baris namaplate gambar-dulu, bingkai transparan, QR, baris
  perlengkapan) tetap lulus. Jendela spesifikasi **tidak** disimpan oleh skrip
  uji — tidak ada data HBA yang ditulis.
- Migrasi diterapkan ke basis data nyata lewat mulai-ulang layanan: catatan
  layanan menulis `[crm] applied migrations on startup: [42]`, versi skema kini
  **42**, kolom `genset_brand` ada, dan **0 dari 6 unit** terisi — tidak ada nilai
  yang dikarang.
- `npm run typecheck` bersih; `npm run build` sukses; UI di 8092 menyajikan
  bundel baru.

## Yang masih menunggu HBA

Fieldnya kini ADA dan kosong. Agar logo genset benar-benar tampil pada sebuah
unit, dua hal milik HBA: mengisi "Merk genset" pada unitnya (satu baris di jendela
spesifikasi), lalu mengunggah logo merek itu di halaman Galeri (slotnya muncul
sendiri setelah langkah pertama). Saya tidak mengisinya sendiri karena merek
genset adalah data bisnis, bukan sesuatu yang boleh saya karang.

HBA juga hanya menyebut **merek**. Bila nanti ingin "Type genset" seperti mesin
dan generator punya "Type", itu field kedua dengan pola yang sama — cukup
dikatakan.

Commit `2126ca4` pada branch `feat/wo-discussion-20261024`
(`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main` — menunggu HBA.

*End of implementation record.*
