# IMPLEMENTASI — dokumen menurun, lampiran penyerahan kelihatan, galeri memutar, dashboard "WO on progress", alamat Google di daftar Pekerja

```text
Record ID:      HBA-DECISIONS-51
Date:           2026-10-26
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruksi HBA:  "1. Untuk dokumen yang terlampir pada menu unit. sepertinya lebih
                 baik dibuat menurun kebawah. per setiap dokumen.
                 2. Lampiran pada spesifikasi unit. pada field 'lampiran
                 penyerahan', dimana saya bisa lihat?
                 3. Galeri Gambar, sudah cukup bagus. namun saya rasa lebih baik
                 frame dikecilkan lagi. dan dibuat dalam satu slide itu ada
                 beberapa gambar yang berjalan pelan. menggunakan effect slow
                 moving ke beberapa gambar. looping
                 4. Pada menu dashboard, sebelah kanan ada list outstanding WO.
                 tolong dirubah warna nya jangan merah. tetap putih saja. judulnya
                 diganti menjadi 'WO on progress' dan hilangkan text 'Penghitung
                 overdue (timer) tidak aktif pada Fase 1 — overdue_timer_enabled:
                 false.'
                 5. rubah sebagai berikut, khd.anto@gmail.com di link sebagai mgr.
                 dan noviantodj@gmail.com sebagai admin.
                 6. saya masih agak ragu dengan penjelasan kalian tentang apa yang
                 dilihat pelanggan. nanti kita buat konfirmasi ulang di sesi
                 selanjutnya. agar tidak ambigu."
Status:         IMPLEMENTED 1–5 — terpasang, 30 cek peramban nyata LULUS.
                Butir 6 SENGAJA BELUM dikerjakan (HBA menunda ke sesi berikutnya).
Classification: Audit record. NOT a canonical specification document.
```

## Butir 1 — dokumen unit menurun

Daftar dokumen pada **Profil Unit** kini menurun: satu dokumen satu baris, selebar
kolomnya, nama berkas tidak lagi saling menekan. Sebelumnya memanjang mendatar
dengan gulir samping. Hanya tata letak yang berubah — daftar, tombol buka, penanda
portal, dan hapus tetap sama.

## Butir 2 — "lampiran penyerahan" akhirnya kelihatan

Jawaban jujur atas pertanyaan "dimana saya bisa lihat": **sebelum perubahan ini, di
mana pun tidak.** Berkasnya memang tersimpan (berkas unit bertanda `is_delivery`
pada tabel `unit_documents`), tetapi tidak ada satu pun layar yang menampilkannya
setelah diunggah — jadi dari sisi pemakai unggahannya seolah hilang.

Sekarang ada blok **"Lampiran penyerahan (internal)"** pada kartu Profil Unit:
daftar berkas (nama + keterangan) dengan tombol buka per berkas, dan daftar yang
sama muncul di jendela **Ubah spesifikasi** tepat di bawah field unggahnya. Sesudah
mengunggah, daftar langsung dibaca ulang sehingga berkas baru muncul tanpa memuat
ulang halaman. Berkas tetap internal — tidak pernah masuk portal pelanggan (aturan
itu tidak disentuh).

## Butir 3 — galeri: bingkai kecil, banyak gambar, geser pelan, memutar

Bingkai galeri diperkecil dari 300 px menjadi **118 px** dan sekarang berisi
**beberapa gambar sekaligus** (bukan satu gambar besar). Barisan gambar bergeser
mendatar sangat pelan (± 5 detik per gambar, jadi makin banyak gambar makin lama
satu putaran), **berputar terus (looping)** tanpa lompatan karena barisan
digandakan, dan **berhenti saat ditunjuk** atau difokuskan supaya tidak kabur saat
dilihat. Klik gambar mana pun membuka pop up besar seperti sebelumnya (ESC
menutup, panah kiri/kanan berpindah). Unggah/hapus/penanda portal tetap hanya untuk
Manager/Admin dan berlaku pada gambar yang sedang dipilih.

## Butir 4 — dashboard

Panel kanan dashboard berjudul **"WO on progress"**, nomor WO berwarna **putih
biasa** (bukan merah), dan keterangan "Penghitung overdue (timer) tidak aktif pada
Fase 1 — `overdue_timer_enabled: false`" **dihapus**. Isi daftarnya tetap daftar
Outstanding dari server — tidak ada filter atau aturan baru yang dibuat di UI.

## Butir 5 — tautan Google: keadaan nyata + yang diperbaiki

Diperiksa lebih dahulu ke database, bukan dikira-kira. **Kedua tautan yang diminta
SUDAH ADA sebelum sesi ini:**

| Alamat Google | Akun internal | Peran | Bukti |
|---|---|---|---|
| khd.anto@gmail.com | `mgr` (id 1) | Manager | `internal_identity_links` id 1, sub `116565251415480860165`, dibuat 2026-10-13 |
| noviantodj@gmail.com | `noviantodj@gmail.com` (id 12) | Admin | `internal_identity_links` id 3, sub `115714397678710252380`, dibuat 2026-10-24 |

Login Google memakai jalur tautan internal ini lebih dahulu (`app/server.py`,
`_handle_google_callback`), jadi kedua alamat masuk ke peran yang benar; sesi
2026-10-26 pukul 16:33 WIB tercatat untuk akun Admin (id 12).

Yang **memang belum ada** adalah cara memeriksanya dari layar: daftar **Pekerja**
hanya menulis lencana "tertaut" tanpa menyebut alamat mana. Itu yang diperbaiki —
payload pekerja kini membawa `google_email` (dibaca dari tabel tautan, cadangan dari
alamat login terakhir) dan barisnya menampilkan alamat itu di bawah nama akun, plus
"alamat Google belum terekam" bila tautannya ada tetapi alamatnya kosong. Proyeksi
baca saja: alamat Google bukan kredensial dan tidak memberi kewenangan apa pun.

Keadaan yang perlu HBA ketahui: ada **dua akun Manager** di daftar Pekerja — `mgr`
(tertaut ke khd.anto) dan `artaniz18@gmail.com` atas nama Jan Antonius Djunaedi
(**belum tertaut**) yang dibuat 2026-10-26. Tidak ada yang diubah pada akun itu;
kalau maksudnya salah satu harus dipindahkan atau dinonaktifkan, itu keputusan HBA
dan cukup satu baris instruksi.

## Butir 6 — ditunda atas permintaan HBA

Penjelasan "apa yang dilihat pelanggan" **tidak** dikerjakan ulang di sesi ini dan
tidak ada perubahan hak visibilitas pelanggan yang dibuat. Konfirmasi ulang
dijadwalkan pada sesi berikutnya; sampai itu terjadi, keadaan portal tetap seperti
sekarang (PIC masuk lewat QR unit; portal perusahaan belum memuat daftar unit).

## Berkas

- `crm/ui/src/components/UnitDocumentsStrip.tsx` (tata letak menurun lewat CSS).
- `crm/ui/src/styles.css` — `.doc-strip`/`.doc-chip` menurun, `.carousel__track`/
  `.carousel__thumb` (bingkai 118 px, geser pelan, looping), `.wo-progress` putih.
- `crm/ui/src/components/UnitPhotoCarousel.tsx` — bentuk slide baru.
- `crm/ui/src/components/UnitSpecCard.tsx` — daftar lampiran penyerahan (kartu +
  jendela), muat ulang sesudah unggah, tombol buka.
- `crm/ui/src/screens/DashboardScreen.tsx` — judul, warna, hapus keterangan overdue.
- `crm/app/access/staff.py` — `google_email` pada proyeksi pekerja (baca saja).
- `crm/ui/src/screens/WorkersScreen.tsx` — alamat Google tampil di baris pekerja.
- Pemeriksa: `crm/ui/verify_unit_docs_gallery_dash_20261026.cjs` (25 cek) dan
  `crm/ui/verify_worker_links_20261026.cjs` (5 cek).

Tanpa migrasi, tanpa endpoint baru, tanpa perubahan skema, tanpa aturan bisnis baru.

## Bukti

- `npm run typecheck` bersih; `npm run build` sukses (`index-DTEoqbw-.js`);
  `npm run lint` tidak menambah peringatan baru.
- Pemeriksa galeri/dokumen/dashboard terhadap **deployment nyata** (8092):
  **25 cek LULUS** — dokumen `flex-direction: column` dengan posisi atas berbeda
  (720/757/794/831) dan lebar penuh 970 px; blok "lampiran penyerahan" tampil
  dengan tombol buka; unggahan uji muncul di jendela **dan** di kartu; bingkai
  galeri 118 px dengan 10 bingkai kecil (5 gambar digandakan), animasi
  `carouselPan`, `iteration-count: infinite`, 25 detik per putaran, `paused` saat
  ditunjuk, klik membuka pop up dan ESC menutup; dashboard berjudul "WO on
  progress", nomor WO `rgb(246, 246, 247)`, keterangan overdue hilang.
- Lampiran uji dihapus kembali: `unit_documents` 3 → 3 (nol baris uji tertinggal).
- Pemeriksa tautan Pekerja: **5 cek LULUS** — khd.anto (Manager, tertaut) dan
  noviantodj (Admin, tertaut) terbaca dari layar.
- `crm.service` dan `crm-ui.service` di-restart; `/healthz` 200 dan layar 200.
- Uji backend yang menyentuh proyeksi pekerja: `tests.test_staff` (16 uji, OK),
  `tests.test_staff_profile`, `tests.test_internal_identity_link`.
