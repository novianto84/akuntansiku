# IMPLEMENTATION RECORD — bingkai logo, perlengkapan memanjang, sel QR menyatu

```text
Record ID:      HBA-DECISIONS-37
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruction:    pesan HBA 2026-10-24 (dua bagian, apa adanya di bawah)
Status:         IMPLEMENTED — terpasang, teruji di peramban, sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Kata HBA yang dikerjakan

Bagian pertama — logo merek dan tabel perlengkapan:

> "tidak usah cantumkan Logo merk genset / mesin / generator. cukup buatkan frame
> saja disana untuk logo masing2nya itu.
> dan untuk tabel perlengkapan, dibuat memanjang saja jangan menurun. tidak perlu
> ada keterangan namanya. cukup nanti gambar saja langsung yang mewakili. atau
> jika mau dibuatkan nama juga boleh, dibawah gambarnya."

Bagian kedua — sel barcode/QR pada Profil Unit:

> "barcode sudah ok di sebelah kanan. tapi saya lihat 1 baris itu dengan kode unit.
> sebaiknya logo itu tingginya terdiri dari beberapa baris yang di merger. sesuai
> tabel kode unit sampai dengan sirklus hidup."

## Yang diubah

Sel logo merek pada kartu Unit tidak lagi menulis judul di atas bingkai maupun
kata pengganti di dalamnya ("—" / "Logo belum diunggah"); yang tampil hanya
bingkainya, dan gambarnya muncul begitu diunggah dari halaman Pengaturan. Bingkai
kosong tetap punya atribut `title` supaya masih bisa dikenali saat ditunjuk
tetikus, tanpa menambah tulisan di layar.

Tabel perlengkapan dua kolom yang menurun diganti SATU BARIS MEMANJANG berisi
bingkai gambar per perlengkapan yang dicentang pada unit itu, dengan namanya kecil
di bawah gambar (HBA membolehkan: "jika mau dibuatkan nama juga boleh, dibawah
gambarnya"). Nama dipakai karena bingkai yang belum berisi gambar tetap perlu bisa
dikenali; kalau HBA ingin namanya dihapus, itu satu baris perubahan.

Blok baris pada Profil Unit disatukan menjadi satu daftar — Kode unit, Nama unit,
Tipe, Pelanggan/pemilik, Siklus hidup — dan sel barcode/QR di sebelah kanannya
kini MERENTANG setinggi seluruh blok itu (bukan hanya setinggi satu baris), dengan
bingkai berlatar supaya penyatuannya terlihat. Di layar sempit (≤820 px) blok QR
turun ke bawah, karena tidak lagi muat berdampingan.

Satu cacat tata letak ikut diperbaiki: elemen daftar membawa margin bawaan
peramban sehingga kolom kiri bergeser 14 px dari bingkai QR; margin itu dinolkan di
dalam blok ini saja.

## Bukti

- 14/14 cek peramban nyata (chromium, ukuran jendela desktop) pada permukaan Profil
  Unit: tidak ada judul di atas bingkai, empat bingkai logo ada dan yang kosong
  benar-benar tanpa tulisan, bingkai merek yang punya gambar menampilkan gambarnya,
  blok baris memuat kelima baris yang diminta, tinggi sel QR sama dengan tinggi blok
  (325 px : 325 px) dan sejajar dari baris pertama, QR memang diterbitkan, strip
  perlengkapan ada tanpa tabel, tiga perlengkapan tampil dalam SATU baris, satu tile
  menampilkan gambar, dan tiap tile punya nama kecil di bawah bingkai.
- `npm run typecheck` bersih; `npm run build` sukses; UI yang dilayani (port 8092)
  sudah memakai bundel baru dan berkas CSS-nya menjawab 200.
- Skrip pemeriksanya disimpan: `crm/ui/verify_unit_profile.mjs`.

## Catatan yang perlu HBA ketahui

- Halaman **Pengaturan** (unggah gambar merek/perlengkapan) TIDAK diubah: di sana
  nama tetap ditampilkan karena itu yang memberi tahu gambar sedang diunggah untuk
  butir yang mana. Kalau maksud HBA termasuk halaman itu, cukup dikatakan.
- Push kali ini juga membawa tiga commit lokal yang sebelumnya belum pernah naik ke
  GitHub (permukaan detail Unit arah D + berkas unit + penyerahan unit v40, akun
  Admin lewat klaim Google, penanda tanggal dokumen riwayat, dan kartu Unit dengan
  gambar aset v41). Commit-commit itu sudah ada di riwayat lokal dengan jejak
  "create by Hermes"; sekarang ikut ter-push bersama perubahan ini.
- Commit: `8d71ee8` pada branch `feat/wo-discussion-20261024`
  (`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main` — menunggu HBA.

*End of implementation record.*
