# IMPLEMENTASI — kompres gambar ke bawah 1 MB per gambar

```text
Record ID:      HBA-DECISIONS-42
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Putusan HBA:    "1MB per image. Bukan total."
Status:         IMPLEMENTED — terpasang, teruji di peramban, sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Aturan yang dijalankan

Batas **1 MB per gambar**, bukan kuota gabungan. Lima gambar 900 KB tetap lima
unggahan yang sah; tidak ada penghitung total di mana pun.

Kompresinya dilakukan di peramban SEBELUM berkas dikirim, karena backend CRM
sengaja tanpa dependensi pihak ketiga (tidak ada Pillow/ImageMagick). Berkas yang
sampai ke server sudah kecil, jadi tidak ada beban pemrosesan gambar di server.

## Perilaku yang dipegang

- Sisi terpanjang dibatasi 1600 piksel; mutu diturunkan bertahap sampai muat.
  Gambar TIDAK pernah diperbesar, dan tidak pernah dikompres ulang bila berkasnya
  sudah ≤ 1 MB — tidak ada penurunan mutu tanpa alasan.
- Transparansi dijaga: gambar beralpha dikodekan ke **WebP**, bukan JPEG, karena
  JPEG memaksa latar putih dan itu bertentangan dengan permintaan HBA sebelumnya
  ("biarkan gambar berlatar transparant").
- SVG dan GIF tidak pernah dikodekan ulang (SVG vektor bisa rusak bila
  dirasterisasi; GIF bisa beranimasi).
- Rotasi EXIF dihormati saat dekode, jadi foto ponsel tidak tersimpan miring.
- Bila dekode/encode gagal, berkas ASLI dikembalikan apa adanya dan pemanggil
  menolak unggahan dengan pesan yang jelas — tidak ada gambar karangan.

## Cakupan

Berlaku pada semua unggahan GAMBAR: foto profil pekerja, galeri foto unit, logo
merek & gambar perlengkapan, foto bukti WO, logo pelanggan, dan foto kontak PIC.
Dokumen (PDF dan sejenisnya) tidak disentuh karena bukan gambar. Foto PIC tetap
memakai batas lamanya yang lebih ketat (±150 KB), tetapi kini berkas besar
DIKECILKAN dulu, bukan langsung ditolak.

## Bukti (angka nyata, bukan perkiraan)

10/10 cek peramban sungguhan (`crm/ui/verify_image_limit.mjs`):

- JPEG 3000×2000 sebesar **6.104.468 byte** diunggah sebagai foto pekerja →
  tersimpan **856.311 byte** (1600×1067), masih ter-decode sebagai gambar sah.
- PNG transparan 2200×2200 sebesar **5.425.779 byte** diunggah sebagai logo
  merek → tersimpan **170.274 byte** dengan mime **image/webp** (transparansi
  terjaga, bukan JPEG).
- Gambar kecil 3.242 byte → tersimpan 3.243 byte, yaitu berkas yang SAMA
  (selisih hanya pembulatan taksiran base64): tidak dikompres ulang.
- Dua gambar berbeda pada satu unit sama-sama ≤ 1 MB secara terpisah
  (170.274 dan 3.243 byte) — membuktikan batasnya per gambar, bukan total.

`npm run typecheck` bersih; `npm run build` sukses; UI dijalankan ulang dan
berkas baru sudah dilayani (port 8092 menjawab 200). Tidak ada perubahan backend
pada putaran ini.

## Catatan yang perlu HBA ketahui

- Foto bukti WO ikut aturan 1 MB ini — sesuai kata "per image" tanpa pengecualian.
  Kalau bukti WO ingin tetap resolusi asli, cukup dikatakan; satu baris perubahan.
- Batas di sisi server TIDAK saya turunkan (foto pekerja 2 MB, foto unit 4 MB).
  Fungsinya kini menjadi jaring pengaman luar: aplikasi selalu mengirim ≤ 1 MB,
  sedangkan pemanggil API langsung yang mengirim lebih besar masih diterima
  sampai batas lama. Kalau HBA ingin server ikut menolak di atas 1 MB, itu juga
  satu baris perubahan — tapi konsekuensinya unggahan lewat API tanpa kompresi
  akan gagal.
- Uji coba saya sempat menulis beberapa berkas uji ke penyimpanan staf NYATA
  (direktorinya memang tetap, tidak mengikuti basis data). Semuanya tidak
  dirujuk baris mana pun dan sudah dihapus; foto asli HBA (122.833 byte)
  tidak tersentuh. Skrip uji sekarang diarahkan ke penyimpanan sementara.

Commit `ea60e33` pada branch `feat/wo-discussion-20261024`
(`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main`.

*End of record.*
