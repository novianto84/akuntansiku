# HBA DECISION RECORD — jawaban empat pertanyaan terbuka diskusi/tag/penanda portal/kolom referensi (2026-10-24)

```text
Record ID:      HBA-DECISIONS-34
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Decisions:      menjawab HBA-DECISIONS-30 bagian "Masih terbuka" (a, b, c, d)
Status:         RECORDED — putusan HBA via chat 2026-10-24, 17:03 WIB
Classification: Audit record. NOT a canonical specification document.
Implementation: NONE — belum ada kata otorisasi eksekusi. Tidak ada kode, skema,
                migrasi, basis data, atau dokumen kanonik yang ditulis/diubah.
```

> Rekaman putusan HBA verbatim + hasil pemeriksaan sistem nyata.
> Putusan bisnis ada di tangan HBA; rekaman ini hanya jejak, bukan spesifikasi.

## Putusan HBA (verbatim)

> "yang boleh membaca diskusi, semua pihak internal.
>  tag cukup di aplikasi. manager dan admin yang berhak menandai berkas tampilan di portal pelanggan
>  satu kolom saja untuk spk / invoice / kontrak"

## Pemeriksaan sistem nyata (17:03 WIB, basis data hidup + kode)

**a. Diskusi dibaca semua pihak internal — SUDAH sesuai, tidak ada perubahan.**
`app/wo/discussion.py` membuka baca/tulis lewat gerbang WO yang sama
(`wo_mod.get(conn, user_id, wo_id)`): setiap pengguna internal aktif yang boleh
membaca WO itu, di dalam workspace aktifnya, boleh membaca dan menulis diskusinya.
Rute hanya dipasang di handler internal; pintu publik menjawab 404 (ada tes
regresinya di `tests/test_doors.py`). Isi tabel hari ini: 0 baris `wo_discussions`.

**b. Tag cukup di aplikasi — BELUM ADA sama sekali.**
`app/wo/discussion.py` menyatakan batasnya sendiri: "Deliberately absent:
notifications, emails, mentions, attachments, edit/delete". Jadi belum ada sebutan
(tag), belum ada penyelesaian nama → pengguna, dan belum ada pemberitahuan. Yang
sudah ada hanya penghitung belum-dibaca per pengguna (badge + kotak masuk).

**c. Manager/Admin menandai berkas yang tampil di portal — BELUM ADA.**
`unit_photos` dan `unit_documents` (migrasi v31) tidak punya kolom penanda terbitan
sama sekali; kolomnya: id, unit_id, mime/filename, caption, uploaded_by_user_id,
created_at, workspace_id. Galeri/dokumen unit juga belum disajikan ke portal
pelanggan. Yang sudah punya pola "peninjau yang menerbitkan" adalah foto WO:
`wo_photos.approval_state`, dan `app/customer/serving.py` hanya menampilkan set
APPROVED. Jadi polanya sudah ada di sistem untuk WO, belum dipindahkan ke berkas unit.

**d. Satu kolom untuk SPK / Invoice / Kontrak — SUDAH ADA, tidak ada pekerjaan.**
Migrasi v38 `units.doc_ref`, satu kolom bebas, tampil di sesi Genset sebagai
"No. SPK / Invoice / Kontrak", disimpan apa adanya. Putusan ini sekaligus menutup
usulan tiga kolom terpisah yang saya ajukan di HBA-DECISIONS-30.

## Catatan audit AI Manager (jujur, tanpa mengubah putusan)

Satu. **Peran "Admin" hari ini tidak berpenghuni.** Kode memakai daftar
`MANAGE_ROLES = ("Manager", "Admin")` di `app/unit/media.py`, tetapi basis data hidup
hanya memuat peran Manager (1), Sales (1), Technician (1), Coordinator (1), dan
Pelanggan_umum (4). Tidak ada satu akun pun berperan Admin. Artinya "Manager dan Admin
yang berhak menandai" secara praktis baru Manager. Bila Admin memang akan ada, saya
butuh satu kalimat: siapa yang diangkat, atau Admin cukup sebagai peran yang siap
dipakai nanti.

Dua. **Tag: yang disapa siapa, dan dikenali bagaimana?** Karena diskusi sudah boleh
dibaca semua pihak internal, tag tidak mengubah siapa yang boleh membaca — tag hanya
memanggil perhatian orang tertentu. Yang belum saya ketahui: apakah semua pengguna
internal boleh disapa, atau hanya pekerja lapangan (registry pekerja); dan saat menulis,
pekerja dikenali lewat nama tampilan, atau lewat pilihan dari daftar.

Tiga. **Granularitas penanda portal.** HBA menyebut sertifikat, manual book, dan
gambar unit boleh dilihat portal. Bila penandanya per berkas, Manager/Admin menandai
satu per satu. Bila penandanya per jenis, sekali set berlaku untuk semua berkas jenis
itu. Keduanya masuk akal; yang dipilih menentukan bentuk tabel dan layar.

Empat. **Berkas WO/SR dan berkas unit punya dua jalur berbeda.** Berkas unit punya
rumah di skema sejak v31 (kosong: 0 dokumen, 3 foto). Lampiran tingkat induk baru
tersedia untuk WO (`wo_photos`, 1 baris), belum untuk SR. Penanda portal ini karena
itu menyentuh dua jalur, dan sebaiknya diputuskan sekali untuk keduanya.

## Masih terbuka (butuh satu kalimat HBA masing-masing)

a. Apakah peran Admin akan diisi akun, atau cukup disiapkan sebagai peran?
b. Siapa yang boleh di-tag, dan pekerja dipilih dari daftar atau ditulis sebagai nama?
c. Penanda "tampil di portal pelanggan": per berkas, atau per jenis berkas?
d. Apakah penanda yang sama nanti berlaku untuk lampiran WO dan SR, atau khusus berkas unit dulu?

## Langkah berikut termurah

Revisi tampilan arah D (Profil Unit, Riwayat, Ruang Diskusi, Galery & berkas dua kolom)
kini tidak lagi tertahan: keempat pertanyaan HBA-DECISIONS-30 sudah terjawab. Itu murni
susunan layar, tanpa skema, sehingga bisa dikerjakan lebih dulu sebagai langkah termurah
begitu HBA memberi kata otorisasi eksekusi. Pekerjaan tag pekerja dan penanda portal
sebaliknya menambah kolom/tabel baru (usulan: satu migrasi v40 untuk keduanya) dan
menunggu jawaban a–d di atas.

## Addendum — jawaban lanjutan + otorisasi eksekusi (2026-10-24, 17:2x WIB)

**Putusan HBA lanjutan (verbatim):**

> "admin akan diisi akun. kaitkan dengan noviantodj@gmail.com
>  semua internal berhak memanggil.
>  segera kanonin kan. dan eksekusikan"

Yang diputuskan: peran **Admin diisi akun** dan akun itu dikaitkan dengan
`noviantodj@gmail.com`; **setiap pengguna internal berhak memanggil** (tag) — jadi
pertanyaan (b) saya terjawab tanpa pembatasan pada pekerja lapangan saja; dan
**otorisasi eksplisit**: kanon direvisi lalu pekerjaan dieksekusi.

Pertanyaan (c) — granularitas penanda portal, per berkas atau per jenis berkas —
**tidak dijawab**. Karena itu penanda dikerjakan sebagai **per artefak** (satu
penanda untuk satu berkas/gambar), yaitu bentuk teknis yang sudah ada di sistem
untuk foto WO (`wo_photos.approval_state`), dan itu saya sebut sebagai pilihan
teknis saya, bukan aturan bisnis baru. Bila HBA menghendaki per jenis berkas,
penanda per artefak tinggal diabaikan tanpa membatalkan kanon.

Pertanyaan (d) — apakah penanda berlaku juga untuk lampiran WO/SR — juga belum
dijawab; lingkup pekerjaan ini dibatasi pada **berkas tingkat Unit** (sertifikat,
manual book, gambar unit) sesuai kata HBA, tanpa menyentuh jalur foto WO/SR yang
sudah berjalan.

**Otorisasi yang terekam:** "segera kanonin kan. dan eksekusikan" (HBA, chat
2026-10-24). Sejak titik ini pekerjaan **bukan lagi NONE**: kanon direvisi dan
implementasi dijalankan atas perintah itu. Catatan status implementasi ada di
HBA-DECISIONS-35 setelah pekerjaan selesai diverifikasi.

*End of decision record (bagian awal). Record ini ditutup setelah eksekusi selesai.*
