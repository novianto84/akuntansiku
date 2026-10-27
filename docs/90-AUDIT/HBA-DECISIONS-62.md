# HBA-DECISIONS-62 — Deutz dan Stamford dikembalikan ke semula

HBA lewat chat 27 Okt 2026 menilai hasil transparan Deutz dan Stamford tidak
bersih dan meminta keduanya dikembalikan seperti semula.

## Yang dikerjakan

Dua baris `unit_brand_images` dikembalikan byte-per-byte dari cadangan yang
dibuat sebelum pengubahan: id 10 STAMFORD dan id 18 DEUTZ. Hasil cek hash
menyatakan identik dengan aslinya. AGG dan POWERLINK tetap versi transparan
karena tidak diminta dikembalikan. Perkins dan Yanmar memang tidak pernah
diubah.

## Bukti

- Panjang data kembali 28852 (STAMFORD) dan 14960 (DEUTZ), sama seperti awal.
- Hash isi sama persis dengan cadangan.

## Masih terbuka

- Kalau mau logo Deutz dan Stamford versi transparan yang rapi, langkah
  termurah adalah minta file PNG resmi berlatar transparan dari pemilik merek
  lalu saya pasang langsung tanpa olah gambar.
