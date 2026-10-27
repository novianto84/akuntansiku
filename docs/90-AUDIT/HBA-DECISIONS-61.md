# HBA-DECISIONS-61 — WO diurutkan dan disaring, logo merek dibuat transparan

Keputusan HBA lewat chat 27 Okt 2026: halaman Work Order diurutkan OPEN paling
atas lalu IN_PROGRESS sementara CLOSED dan CANCELLED di bawah, ada kolom Nama
Perusahaan, ada saringan status dan perusahaan, dan logo AGG, Powerlink, Deutz,
Stamford, Perkins, Yanmar dibuat transparan.

## Yang dikerjakan

Halaman WO sekarang mengurutkan OPEN paling atas lalu IN_PROGRESS, DRAFT,
WAITING APPROVAL, CORRECTION REQUIRED, CLOSED, dan CANCELLED paling bawah.
Urutan ini murni tampilan, bukan aturan bisnis. Kolom Perusahaan diisi dari
perusahaan pemilik unit, kalau WO belum punya unit diambil dari perusahaan SR
asalnya, kalau dua-duanya kosong ditulis strip. Saringan ada dua: pilihan status
dan ketikan nama perusahaan, plus tombol pembersih. Kolom Asal SR dan Posture
tetap tampil supaya lineage tidak hilang.

Untuk logo: yang di database ada 11 baris merek. Yang diminta HBA enam nama:
AGG, POWERLINK, DEUTZ, STAMFORD, PERKINS, YANMAR. Hasil cek: Perkins dan
Yanmar memang sudah transparan sejak awal jadi tidak diubah. Empat sisanya
(AGG, POWERLINK, DEUTZ, STAMFORD) background putihnya dihapus dengan cara
membuang putih yang menempel ke tepi gambar, jadi putih di dalam logo seperti
kotak STAMFORD tidak ikut hilang. POWERLINK ENGINE dan GENSET memakai gambar
yang sama jadi dua-duanya diperbarui. Format diseragamkan ke PNG dan bingkai
galeri memang sudah transparan jadi logo langsung menyatu.

## Bukti

- `npm run typecheck` bersih, `npm run build` jadi satu bundle baru.
- Bundle yang disajikan server sama dengan hasil build (cek hash HTML cocok).
- Pojok tiap gambar hasil sudah alpha nol (tembus pandang) dan jenisnya PNG.
- Layanan `crm.service` dan `crm-ui.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM (`github.com/novianto84/mitrasp-app`), branch
  `feat/wo-scope-assign-20261026`, commit `fb40bc8`, sudah push, belum merge.
  Yang berubah hanya `ui/src/screens/WoScreen.tsx`.
- Isi database `unit_brand_images` id 10, 12, 18, 19, 20 diperbarui langsung di
  `data/crm.db` (bukan lewat git, file DB memang tidak di-commit).
- Catatan: Perkins masih membawa watermark tulisan situs unduhan di gambarnya;
  kalau mau bersih perlu ganti file dari sumber resmi.

## Masih terbuka

- Logo CUMMINS, DEEPSEA, MITSUBISHI, LEROY SOMER, TIDE POWER tidak diminta
  jadi tidak disentuh.
- Uji browser klik-langsung halaman WO belum dijalankan ulang; verifikasi yang
  dipakai baru build, hash bundle, dan layanan aktif.
