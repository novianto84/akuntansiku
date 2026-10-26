# IMPLEMENTASI — unit pelanggan bisa diklik, lingkup pekerjaan bernomor, penugasan teknisi satu kotak

```text
Record ID:      HBA-DECISIONS-49
Date:           2026-10-26
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruksi HBA:  "1. pada menu pelanggan, unit tidak dapat di klik. seharusnya yang
                 saya mau, pihak internal, ataupun customer yang punya kewenangan
                 bsia mengklik unitnya. dan masuk ke halaman unitnya.
                 2. Scope job itu saya minta dibuatkan frame fielndnya lebih besar.
                 jangan hanya 1 baris. ... buat langsung 4-5 baris. seperti table.
                 dengan nomor di sebelah kirinya. kasih keterangan, 'lingkup
                 pekerjaan yang perlu dilakukan teknisi'
                 3. Begitupun pada table penugasan teknisi, langsung saja disatukan,
                 untuk apa ada 2 field ...
                 4. dan langsung dibuatkan juga Teknisi utama. (field untuk search dan
                 pilih langsung). kemudian dibawahnya teknisi support ... baru
                 kemudian baris ke 3, 'tambah teknisi'" 
Status:         IMPLEMENTED — terpasang di layar yang dipakai (127.0.0.1:8092),
                28 cek peramban nyata LULUS, sudah di-push ke cabang
Classification: Audit record. NOT a canonical specification document.
```

## Bentuk yang dipasang

**Pelanggan → unit bisa dibuka.** Di halaman detail pelanggan, kode unit dan nama
unit sekarang bertautan, dan tiap baris punya tombol **"Buka unit"**. Klik salah
satunya membuka halaman unit itu (`#/unit/<id>`) — halaman yang sama dengan menu
Unit, bukan layar baru. Tautan hanya memindahkan layar; kewenangan tetap diperiksa
backend saat halaman unit memuat datanya, jadi tidak ada izin baru yang lahir dari
perubahan ini.

**Lingkup pekerjaan.** Kotak satu baris diganti kotak **lima baris bernomor**
(nomor di kiri, seperti tabel), berlabel *"Lingkup pekerjaan yang perlu dilakukan
teknisi"*, dan bisa ditambah baris dengan tombol **"+ Tambah baris"**. Dipasang di
dua tempat yang menulis SCOPE: form **Work Order baru** dan form **Tambah JOB** di
detail WO. Bentuk simpannya **tidak berubah** — tetap satu teks (baris digabung
newline), tanpa migrasi. Di tabel JOB, SCOPE kini ditampilkan **bernomor** juga,
supaya yang dibaca teknisi sama dengan yang diketik penugasan.

**Penugasan teknisi, satu kotak.** Bidang "Cari teknisi" + dropdown "Teknisi"
digabung jadi **satu kotak**: ketik sebagian nama → daftar teknisi aktif menyempit
→ klik nama → jadi chip nama dengan tombol "Ganti". Susunannya: baris 1 **Teknisi
utama**, baris 2 **Teknisi support**, lalu tombol **"+ Tambah teknisi"** yang
memunculkan teknisi ke-3, ke-4, dan seterusnya (tiap baris tambahan bisa dihapus).
Teknisi yang sudah dipilih tidak ditawarkan lagi di baris lain, sehingga satu orang
tidak bisa masuk dua kali.

**Yang tidak dilonggarkan.** Alasan penugasan tetap **wajib** (E-20: setiap
perubahan penugasan butuh alasan + jejak audit), satu WO tetap hanya punya **satu
PRIMARY**, dan setiap penugasan tetap dikirim sebagai **panggilan terpisah** karena
kanon mencatatnya per baris. Satu alasan berlaku untuk semua teknisi yang dipilih
pada satu tindakan. Bila salah satu ditolak backend, yang sudah tercatat tidak
dibatalkan — galat ditampilkan apa adanya lalu daftar dimuat ulang.

## Berkas

- `crm/ui/src/components/ScopeLines.tsx` (baru) — kotak SCOPE bernomor.
- `crm/ui/src/components/TechnicianPicker.tsx` (baru) — pencarian + pemilihan teknisi satu kotak.
- `crm/ui/src/screens/WoScreen.tsx` — SCOPE form WO baru.
- `crm/ui/src/screens/WoDetailScreen.tsx` — SCOPE form Tambah JOB, tampilan SCOPE
  bernomor di tabel JOB, dan bentuk baru panel Penugasan (+ `assignMany`).
- `crm/ui/src/screens/CompanyDetailScreen.tsx` — unit jadi tautan + tombol "Buka unit".
- `crm/ui/src/styles.css` — gaya kotak bernomor dan tautan unit.
- `crm/ui/verify_scope_assign_20261026.cjs` (baru) — pemeriksa peramban.

Tanpa migrasi, tanpa endpoint baru, tanpa aturan bisnis baru, tanpa perubahan
skema. Kewenangan (ASSIGN_WO = Manager/Coordinator) tetap di backend.

## Bukti

- `npm run typecheck` bersih; `npm run build` sukses.
- `node verify_scope_assign_20261026.cjs` terhadap **deployment nyata**
  (`http://127.0.0.1:8092`, pintu yang dipakai manusia): **28 cek, SEMUA LULUS**.
  Yang dibuktikan, antara lain: 4 tautan unit muncul dan mengarah ke `#/unit/1`;
  klik "Buka unit" berpindah ke `#/unit/1` dan unit U-GS-001 tampil; kotak lingkup
  setinggi 309px untuk 5 baris bernomor 1–5 (satu baris 36px); SCOPE tiga baris
  tersimpan utuh dan tampil bernomor di detail WO; tidak ada lagi field "Cari
  teknisi" maupun dropdown teknisi; "Tambah teknisi" memunculkan "Teknisi ke-3";
  tiga teknisi berbeda terpilih dan terkirim sebagai **3 panggilan** `/assign`
  dengan peran `PRIMARY,SUPPORTING,SUPPORTING`.
- Baris uji dibersihkan: WO uji dibuat lalu dihapus, hitungan DB sebelum/sesudah
  identik (`wo 9, jobs 10, assign 7`).
- `crm-ui.service` di-restart sehingga `ui/dist` yang disajikan adalah bundle hasil
  build ini (`index-ReDkHlKj.js`).

## Yang masih terbuka

- **Sisi pelanggan (portal).** Permintaan menyebut "ataupun customer yang punya
  kewenangan bisa mengklik unitnya". Yang dipasang sekarang adalah sisi internal
  (menu Pelanggan). Di portal, PIC sudah punya halaman riwayat perusahaan, tetapi
  halaman itu **tidak memuat daftar unit** — menampilkannya berarti memberi
  pelanggan daftar unit beserta jalan masuk per unit, yaitu keputusan **hak
  visibilitas pelanggan**, bukan pekerjaan tampilan. Karena itu tidak dikerjakan
  tanpa keputusan HBA. Pilihan yang tersedia: (a) tetap seperti sekarang — PIC
  masuk lewat QR unit; (b) daftar unit ringkas di portal perusahaan (kode + nama +
  status, tanpa harga), tiap baris menuju portal unit; (c) hanya unit yang punya
  riwayat layanan.
- Cabang `feat/wo-scope-assign-20261026` sudah di-push, **belum di-merge** ke `main`
  — merge tetap gerbang HBA. Bundle yang sedang disajikan dibangun di atas cabang
  `feat/galeri-profil-unit-20261026` yang juga belum di-merge.
