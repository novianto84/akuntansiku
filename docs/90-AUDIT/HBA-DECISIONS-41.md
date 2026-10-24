# PERBAIKAN — foto profil pekerja tidak terlihat berubah

```text
Record ID:      HBA-DECISIONS-41
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Laporan HBA:    "Foto profil pekerja tidak berubah yah, setelah saya upload
                 gambar saya. Tetap tidak berubah"
Status:         FIXED — terpasang, teruji di peramban, sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Apa yang sebenarnya terjadi (bukti, bukan dugaan)

Unggahannya BERHASIL dan fotonya TERSIMPAN. Jejaknya ada di log server nyata:

```
21:04:12  POST /api/staff/12/photo            200
21:04:12  GET  /api/staff/12                  200
21:04:15  GET  /api/staff/12/photo?v=...      200
```

Berkasnya juga ada di penyimpanan: `data/staff_files/132df23946c89f989fce23c01247a1ee.jpg`,
122.833 byte, `image/jpeg`, tercatat pada `staff_profiles` akun
`noviantodj@gmail.com` (Novianto) dengan `photo_url = /api/staff/12/photo`.

Jadi bukan unggahannya yang gagal, melainkan TEMPAT MELIHATNYA yang tidak ada:
foto profil hanya pernah dirender di dalam jendela detail pekerja. Daftar
Pekerja tidak punya kolom foto sama sekali, dan avatar kanan atas selalu
menampilkan INISIAL. Karena foto akun sendiri diunggah, yang wajar dilihat
adalah avatar kanan atas — dan itu memang tidak berubah, karena tidak pernah
membaca foto.

## Yang diperbaiki

Foto profil kini tampil di dua tempat yang selama ini kosong, dan keduanya
membaca endpoint foto yang sama dengan penanda versi sehingga tidak pernah
menampilkan gambar basi:

- **Baris daftar Pekerja**: avatar kecil di samping nama. Tanpa foto: inisial
  (bukan gambar karangan). Daftar hanya membawa PENANDA (`photo_url` + versi),
  bukan byte gambarnya.
- **Avatar kanan atas**: memakai foto akun yang sedang masuk bila ada. Setelah
  menyimpan foto, layar membaca ulang profil sendiri sehingga avatar langsung
  berganti tanpa memuat ulang halaman.

Tidak ada perubahan hak akses: endpoint foto tetap Manager/Admin, dan tidak ada
kredensial maupun byte gambar yang ikut di payload daftar/profil.

## Bukti

- 15/15 cek peramban nyata (`crm/ui/verify_worker_photo.mjs`), termasuk: foto
  muncul di jendela detail setelah unggah 56 KB JPEG; berkas yang dilayani
  endpoint = berkas yang diunggah; mengganti berkas benar-benar mengganti
  gambarnya; foto tampil juga di baris daftar Pekerja; dan unggahan pada AKUN
  SENDIRI mengubah avatar kanan atas menjadi foto (bukan inisial).
- 48 tes otomatis pekerja & profil pekerja lulus.
- `npm run typecheck` bersih; `npm run build` sukses; backend dan UI dijalankan
  ulang; UI 8092 dan API 8010 menjawab 200.
- Pemeriksaan pada basis data NYATA: akun Novianto kini membawa
  `photo_url=/api/staff/12/photo` versi `2026-10-24 14:04:12`, sehingga foto yang
  sudah ia unggah akan langsung tampil.

## Kebersihan

Uji coba saya menulis tiga berkas gambar uji 68–70 byte ke penyimpanan staf yang
sama (lokasinya memang satu direktori tetap). Ketiganya tidak dirujuk baris mana
pun dan sudah saya hapus; foto asli HBA (122 KB) tidak tersentuh.

Commit `8320caa` pada branch `feat/wo-discussion-20261024`
(`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main`.

*End of record.*
