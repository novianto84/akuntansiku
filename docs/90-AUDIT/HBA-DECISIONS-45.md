# PERBAIKAN — hasil scan QR unit hilang setelah login Google

```text
Record ID:      HBA-DECISIONS-45
Date:           2026-10-25
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Laporan HBA:    "hasil scan barcode unit, masih belum bisa diakses oleh pengguna
                 umum. saya coba login menggunakan google akun yang belum
                 terdaftar, dan tidak menampilkan unit"
Status:         FIXED — terpasang, teruji di peramban nyata, sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Apa yang sebenarnya terjadi (dibuktikan pada sistem nyata, bukan dugaan)

Saya menirukan alurnya di peramban sungguhan dengan sesi pelanggan nyata
(`Pelanggan_umum`), lalu memeriksa jejaknya. Rantainya begini: QR unit memuat
tautan `#/portal-unit?code=<kode>`. Fragmen URL **tidak pernah dikirim ke
server**, sedangkan login Google adalah perpindahan halaman penuh — backend
mengembalikan peramban ke `/#crm-token=...` untuk menyerahkan sesi. Akibatnya
rute hasil pindai DIGANTI oleh fragmen token, dan pelanggan mendarat di halaman
portal dengan **kotak kode kosong**:

```text
sebelum perbaikan (peramban nyata, sesi Pelanggan_umum):
  hash sesudah mendarat : ''            -> rute '#/portal-unit?code=A4KZV7MAJG' hilang
  kotak kode            : ['']          -> kosong
  panel unit            : tidak ada     -> "tidak menampilkan unit", persis laporan HBA
```

Dua sebab, keduanya di sisi tampilan:

1. rute hasil pindai hilang saat peramban pergi ke dan kembali dari Google;
2. tautan dalam (deep link) hanya MENGISI kotak kode — profil unit baru dimuat
   setelah pelanggan menekan tombol "Lihat", sehingga layar hasil pindai tampak
   kosong.

Bukan soal izin: pelanggan yang sama, setelah kode dimuat, memang berhak melihat
unit itu. Yang gagal hanyalah membawa orang kembali ke halaman yang ia pindai.

## Yang diperbaiki (hanya tampilan; tidak ada perubahan backend)

- Rute yang sedang dibuka **diingat sebentar** (`sessionStorage`) tepat sebelum
  peramban pergi ke Google, lalu dipulihkan SEKALI setelah sesi benar-benar ada.
  Batasnya dijaga: hanya rute aplikasi `#/...` yang diingat, umurnya 30 menit,
  sekali pakai langsung dilupakan, dan kegagalan penyimpanan diabaikan supaya
  login tidak pernah gagal karena urusan ingatan rute. Kalau pelanggan sudah
  membuka halaman lain sendiri, rutenya tidak diganggu.
- Kode yang datang dari tautan/QR **langsung dimuat** tanpa menekan "Lihat";
  kotak kode dan tombolnya tetap ada untuk pengisian manual.

Yang TIDAK berubah, dan itu disengaja: portal tetap wajib login (tanpa sesi
jawabannya tetap 401 — dibuktikan), cakupannya tetap satu unit saja
(UNIT_SCOPE), dan isinya tetap allowlist IS-06 §10: identitas unit + riwayat
layanan customer-safe, tanpa harga. Tidak ada izin, peran, atau aturan bisnis
baru — perbaikan ini hanya mengembalikan orang ke halaman yang tadi ia pindai.

## Bukti (peramban sungguhan, UI yang dilayani pengguna di :8092)

**11/11 cek** pada `crm/ui/verify_portal_qr.mjs` (Chromium headless, akun
pelanggan nyata, alur penuh):

- tanpa sesi: layar masuk tampil dan rute QR **tetap** di alamat;
- tanpa sesi: permintaan unit tetap ditolak **401** (batas sesi utuh);
- menekan tombol "Masuk / Daftar dengan Google" benar-benar membawa peramban ke
  `accounts.google.com`, dan rute hasil pindai sudah tersimpan sebelum pergi;
- pendaratan OAuth memulihkan rute `#/portal-unit?code=A4KZV7MAJG`, kode terisi di
  kotak kode, sesi pelanggan aktif, dan **unitnya termuat sendiri**:
  `CUMMINS 1000 KVA TRAILER III — Unit MADI-03 · riwayat layanan customer-safe (0)`;
- rute yang diingat sekali pakai langsung dilupakan (tidak menyeret orang ke
  halaman lama).

Regresi: **33/33 cek** permukaan Profil Unit tetap lulus (baris namaplate,
bingkai logo, QR, perlengkapan) dengan bundel baru. `npm run typecheck` bersih,
`npm run build` sukses. **Tidak ada perubahan backend** pada putaran ini.

## Dua hal yang perlu HBA ketahui

- Uji ini memakai akun pelanggan uji yang sudah ada (`cust_dev`), bukan akun
  Google HBA — mekanisme yang diuji adalah bagian yang sama persis (pendaratan
  `#crm-token=...` sesudah Google mengembalikan peramban). Kalau HBA ingin saya
  ikut menguji dengan akun Google miliknya, akun itu harus dipakai dari
  peramban HBA sendiri; saya tidak pernah menyentuh kredensial siapa pun.
- Untuk unit MADI-03 riwayat layanannya masih **0**. Itu bukan cacat: riwayat
  pelanggan hanya berisi Work Order yang sudah **CLOSED** dan laporannya FINAL,
  dan di basis data nyata snapshot pelanggan baru ada untuk unit 1
  (WO-2026-001 dan WO-2026-007). Jadi unit akan menampilkan riwayat begitu ada WO
  yang ditutup untuknya — tidak ada riwayat yang dikarang untuk mengisi layar.

Commit `927af31` (perbaikan) dan `3b5d117` (skrip bukti) pada branch
`feat/wo-discussion-20261024` (`github.com/novianto84/mitrasp-app`). Belum
di-merge ke `main` — menunggu HBA.

*End of record.*
