# IMPLEMENTASI — galeri dipindah ke Profil Unit & Riwayat

```text
Record ID:      HBA-DECISIONS-48
Date:           2026-10-26
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruksi HBA:  "saya juga ingin rubah tampilan galery. bagaimana jika di merger
                 saja di halaman profil unit? ... Galery sebelah kiri di menu
                 galery, di pisahkan yang berupa format image, di buat kan jadi
                 slide pada diantara tabel 'tentang' dengan tabel spesifikasi
                 genset'. Galerinya berjalan perlahan. horizontal. dan bisa di
                 klik untuk diperbesar muncul pop up windowsnya. Sementara yang
                 berupa dokumen, dibuatkan dalam bentuk link, dibuat memanjang
                 horizontal. jika di klik baru terbuka pada tab baru. Dan untuk
                 galeri yang sebelah kanan menu galery, nantinya bisa masuk di
                 riwayat. per WO."
Keputusan HBA:  tab "Galery & berkas" DIHAPUS; unggah/kelola lewat tombol di
                 slide dan di baris dokumen (hanya Manager/Admin yang melihat).
Status:         IMPLEMENTED — terpasang, 18 cek peramban nyata, sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Bentuk yang dipasang

Halaman **Profil Unit** sekarang berisi, berurutan: tabel **Tentang** (identitas +
QR portal) → **slide gambar** → **baris tautan dokumen** → **Spesifikasi genset**
(Mesin / Generator / Panel / Genset) → **Perlengkapan**.

Slide gambar berjalan sendiri dengan lambat — satu gambar tiap **6 detik**, dengan
gerak masuk mendatar yang halus — berhenti selama penunjuk berada di atasnya atau
kendalinya difokuskan, punya panah dan titik navigasi bila gambarnya lebih dari
satu, dan **klik gambarnya membuka pop up** berisi gambar besar (ESC atau klik
latar menutup; panah kiri/kanan berpindah gambar di dalam pop up).

Dokumen menjadi **baris tautan memanjang** (bisa digeser mendatar): nama berkas,
jenisnya lewat ikon, ukurannya, dan penanda kecil bahwa tautan membuka tab baru.
Klik tautan → berkas terbuka di **tab baru**; halaman unit tidak ditinggalkan.

Foto bukti **per Work Order** tidak lagi berdiri di kolom kanan halaman berkas,
melainkan menempel pada WO-nya di tab **Riwayat**: thumbnail kecil di bawah tabel
visit WO itu, dengan status persetujuan (menunggu / disetujui / ditolak) karena
halaman ini internal. Klik thumbnail juga memperbesar.

Tab **"Galery & berkas" dihapus**. Unggah gambar, unggah dokumen, hapus, dan
penanda "tampil di portal pelanggan" tetap tersedia — tetapi hanya untuk Manager
dan Admin, di slide dan di baris dokumen. Peran lapangan tidak melihat satu pun
kendali itu (penjaganya tetap di server, bukan hanya disembunyikan).

Di **portal pelanggan** (hasil scan QR) blok profil unit kini tampil lengkap
dengan susunan yang sama: Tentang → slide gambar → tautan dokumen → namaplate →
perlengkapan → riwayat layanan. Yang dikirim ke pelanggan hanya **gambar dan
dokumen yang sudah ditandai terbit** oleh Manager/Admin, dan namaplate tanpa
nomor dokumen serta tanpa tanggal penyerahan (lihat HBA-DECISIONS-47).

## Bukti — 18 cek peramban nyata (`crm/ui/verify_unit_gallery.mjs`, UI :8092)

- tab lama benar-benar hilang: sisa tiga tab (`Profil Unit`, `Riwayat`,
  `Ruang Diskusi`);
- posisi slide terukur: Tentang `top=240` → slide `top=501` → namaplate
  `top=989`, jadi slide memang berada DI ANTARA keduanya;
- slide bergerak sendiri: penghitung berubah `1/3` → `3/3` dalam ~7 detik;
- klik gambar membuka pop up (`.lightbox` berisi gambar) dan ESC menutupnya;
- dokumen tampil sebagai tautan, dan **klik sungguhan** (gerakan tetikus lewat
  protokol, bukan `.click()` dari skrip) membuka **tab baru** berisi berkasnya
  (`tab 1 → 2`, alamat `blob:…`) — diuji dengan satu dokumen sementara pada unit
  MEBS-01, lalu **dihapus kembali** (sisa dokumen di unit itu: 0);
- foto bukti WO muncul di dalam grup WO pada Riwayat (WO-2026-001 dan
  WO-2026-007 masing-masing menampilkan thumbnail);
- portal pelanggan: blok profil tampil, namaplate terlihat, **tidak** memuat
  nomor SPK/Invoice/Kontrak, **tidak** memuat tanggal penyerahan, riwayat tetap
  ada, dan slide hanya memuat **1 gambar** dari 3 yang dimiliki unit itu —
  bukti bahwa penanda terbitan benar-benar menyaring.

`npm run typecheck` bersih; `npm run build` sukses; UI di :8092 menyajikan bundel
baru. Perubahan backend pada putaran ini hanya proyeksi profil pelanggan dan
penutupan rute numerik (HBA-DECISIONS-47).

## Catatan yang perlu HBA ketahui

- Hari ini belum ada **dokumen** yang terunggah di unit mana pun (0 baris), jadi
  baris tautan dokumen tampil kosong dengan keterangan jujur. Tautannya sudah
  diuji memakai dokumen sementara yang lalu dihapus.
- Slide di portal hanya akan berisi gambar yang HBA tandai "tampil di portal
  pelanggan". Saat ini unit MADI-01 punya 3 gambar dan baru 1 yang ditandai, jadi
  pelanggan melihat 1. Untuk menambah, cukup tekan "Tampilkan di portal" pada
  slide yang bersangkutan (Manager/Admin).
- Satu gambar berpindah tiap 6 detik. Kalau terasa terlalu cepat/lambat, itu satu
  konstanta di komponen slide — cukup dikatakan.

Commit `a729547` pada branch `feat/galeri-profil-unit-20261026`
(`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main` — menunggu HBA.

*End of implementation record.*
