# IMPLEMENTATION RECORD — empat permukaan Unit, panggilan internal, penanda terbitan, akun Admin (HBA-DECISIONS-29/30/31/34)

```text
Record ID:      HBA-DECISIONS-35
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Decisions:      HBA-DECISIONS-29 (arah D), -30 (empat permukaan, galeri, penyerahan unit),
                -31 (diskusi internal + kotak masuk), -34 (jawaban lanjutan + otorisasi eksekusi)
Authorization:  "segera kanonin kan. dan eksekusikan" (HBA, chat 2026-10-24)
Status:         IMPLEMENTED & VERIFIED — migrasi v40 terpasang di basis data hidup, diuji, diuji peramban
Classification: Audit record. NOT a canonical specification document.
```

## Yang dibangun

**Kanon (kanoninkan).** Enam dokumen spesifikasi direvisi aditif dengan addendum yang menyebut
putusan HBA apa adanya, plus satu catatan aditif di `DECISION_REGISTER.md`:
`IS-01` (diskusi internal per WO, satu kolom rujukan dokumen, penyerahan unit, penanda terbitan),
`IS-03` v1.5 (hak baca internal, panggilan semua pihak internal, penanda terbitan Manager/Admin,
pengisian peran Admin), `IS-05` v1.2 (penanda terbitan artefak tingkat Unit; bingkai WO setara
Visit), `IS-06` v1.4 (berkas unit yang boleh tampil; tiga hal penyerahan yang tidak dicantumkan),
`IS-07` v1.2 (diskusi bukan peristiwa audit; transisi penanda diobservasi audit), `IS-08` v1.2
(empat permukaan detail Unit + permukaan Kotak Masuk). Tidak ada lantai yang sudah terkunci yang
diubah diam-diam: semua tambahan menyebut rekaman HBA sebagai sumbernya.

**Skema.** Migrasi v40 `crm_unit_publication_and_mentions`: tabel `wo_discussion_mentions`
(panggilan pekerja + indeks per pengguna), kolom `published_at`/`published_by_user_id`/`is_delivery`
pada `unit_photos` dan `unit_documents`, dan kolom `units.delivery_date`. Idempoten dan reversibel.

**Diskusi WO — panggilan pekerja.** `app/wo/discussion.py` menerima daftar `mentions`; setiap id
divalidasi sebagai pengguna internal aktif (id asing/non-aktif ditolak dengan pesan Indonesia).
Panggilan adalah pemberitahuan di dalam aplikasi saja, tidak menambah jalur buku-baca kedua
(belum-dibaca tetap dihitung dari ketiadaan baris `wo_discussion_reads`). Rute baru
`GET /api/wo/discussions/mentions` dan `mentioned` pada pesan/kotak masuk.

**Penanda terbitan berkas tingkat Unit.** `app/unit/media.py`: `set_photo_published` /
`set_document_published` hanya untuk Manager/Admin; pengunggah dan teknisi ditolak. Portal
pelanggan (`app/customer/serving.py`) menyajikan HANYA berkas bertanda terbit dan TIDAK PERNAH
lampiran penyerahan — tanpa harga dan tanpa kolom kurasi internal.

**Penyerahan unit.** `units.delivery_date` (disimpan apa adanya) plus centang `is_delivery` untuk
lampiran penyerahan; keduanya internal dan tidak pernah masuk portal pelanggan.

**UI (arah D).** Detail Unit menjadi empat permukaan berurutan — Profil Unit (gabungan Tentang +
Mesin + Generator + Panel + Genset + Perlengkapan), Riwayat, Ruang Diskusi (per WO, bukan ruang
bebas unit), Galery & berkas (dua kolom: berkas tingkat Unit di kiri dengan kendali penanda
terbitan untuk Manager/Admin; berkas WO di kolom utama dibingkai nomor WO). Kotak Masuk mendapat
bagian "Panggilan untuk Anda"; panel diskusi mendapat pemilih rekan internal dan menyorot nama
yang dipanggil. Jenis berkas (sertifikat/manual book/gambar) sengaja TIDAK dijadikan kolom
kategori, karena taksonomi di luar lantai terkunci masih OPEN (OQ-05) — penanda terbitan
diterapkan per artefak, dan itu pilihan teknis, bukan aturan bisnis baru.

**Akun Admin.** Dibuat lewat `provision_admin.py` (skrip sekali jalan, idempoten) karena
`app/access/staff.create_staff` sengaja melarang Manager mengangkat Admin — sehingga Admin
PERTAMA tidak punya jalan lain. Akun: `noviantodj@gmail.com`, peran Admin, aktif, workspace
MitraSP Utama, `created_by` manajer (id 12). Masuknya lewat jalur klaim email Google
terverifikasi yang sudah ada: saat orang itu sign in dengan akun Google tersebut, sistem
mengenali dan mengaitkannya sendiri, tanpa kata sandi.

## Cacat yang ditemukan saat verifikasi — dan diperbaiki

**Fitur diskusi MATI di pintu yang dipakai staf.** `is_public_path()` menolak setiap path yang
memuat segmen `discussions`, sehingga rute diskusi tidak pernah sampai ke handler di pintu publik
(8010) — padahal UI yang dipakai staf internal, `crm.benshi.my.id`, justru dilayani dari pintu
publik itu (`ui_server.py` mem-proxy ke 8010). Akibatnya badge, kotak masuk, dan panel diskusi
menjawab 404 di UI nyata. Ini kemungkinan besar yang membuat HBA melihat "UI belum berubah"
pada increment sebelumnya: fiturnya ada di kode, tetapi tidak terjangkau dari layar yang dia pakai.

Perbaikan: rute diskusi kini didispatch di pintu publik seperti rute operasional lain (mis.
`/api/staff`), dan penegakan aturan HBA "tidak bisa oleh external" tetap berjalan di dalam
handler — gerbang sesi `_require_auth` menolak kedua peran pelanggan dengan 403 ("butuh staf"),
dan modul diskusi tetap scope-gated per workspace. Rute tidak lagi disembunyikan; ditolak dengan
alasan yang jujur. Bukti: tes HTTP pintu publik baru (staf 200, pelanggan 403) dan verifikasi
peramban nyata.

## Bukti

- **Tes unit**: seluruh rangkaian lulus (`python3 -m unittest discover -s tests -t . -q`), dengan
  satu-satunya sisa kegagalan adalah empat error yang SUDAH ADA sebelum perubahan ini
  (`tests.test_location`, tiga di `tests.test_material_seam`) — dibuktikan dengan menjalankan
  rangkaian yang sama pada worktree bersih di HEAD tanpa perubahan ini.
- **HTTP pintu publik** (`tests/test_unit_publication.py::PublicDoorDiscussionTest`): staf 200 pada
  kotak masuk dan umpan panggilan; pelanggan 403 pada seluruh rute diskusi; tanpa sesi 401.
- **Peramban nyata** (`ui/verify_arahd.mjs`, chromium headless melawan layanan hidup 8092 → 8010 →
  basis data nyata): 31/31 pemeriksaan lulus, dua sesi. Manager: empat permukaan dengan urutan
  benar, nilai nameplate apa adanya, `No. SPK / Invoice / Kontrak`, `Tanggal penyerahan unit`,
  kendali penanda terbitan (3 centang), terbit → `published=true` di backend, batal → bersih,
  panel diskusi + pemilih panggilan, catatan terkirim dengan nama yang dipanggil tersorot.
  Teknisi: "Panggilan untuk Anda" berisi nomor WO dan isi catatan, umpan panggilan `unread:1`,
  NOL kendali penerbitan, dan 403 saat memaksa menerbitkan.
- **Basis data hidup**: `schema_migrations` memuat v40; kolom dan tabel baru sesuai bentuk yang
  diminta. Data uji dari verifikasi peramban dihapus kembali; tidak ada foto dalam keadaan terbit.
- `crm.service` dijalankan ulang; pintu publik 8010, pintu admin 8011, UI 8092 dan 8093 melayani
  bundel baru.

## Penyimpangan yang dicatat jujur

Satu. **Migrasi v40 terpasang di basis data hidup lebih awal dari rencana.** Yang menerapkannya
adalah layanan itu sendiri: `crm.service` menerapkan migrasi tertunda saat start, dan pada
18:52:25 layanan sempat dijalankan ulang saat berkas migrasi baru saja ditulis. Saya memeriksa
bentuk skema sesudahnya (kolom/tabel sesuai), menjalankan `upgrade` sekali lagi (idempoten, tidak
mengubah apa pun), dan memastikan tidak ada baris data yang ikut ditulis. Tidak ada kerusakan;
yang perlu dicatat adalah urutannya, bukan hasilnya.

Dua. **Empat error tes yang tersisa bukan dari pekerjaan ini** — diverifikasi dengan baseline di
worktree bersih.

Tiga. **Dua skrip verifikasi lama kini usang** terhadap tata letak baru: `ui/verify_unit_spec_v30.cjs`
dan `ui/verify_disc.mjs` masih mencari susunan layar lama. Keduanya tidak dijalankan ulang dalam
increment ini; penggantinya `ui/verify_arahd.mjs`.

## Batas yang dipatuhi

Tidak ada modul, peran, izin, atau aturan bisnis baru di luar rekaman HBA. Taksonomi jenis berkas
unit tidak dikarang (OQ-05 tetap OPEN). Pemberitahuan hanya di dalam aplikasi — tidak ada kanal
WhatsApp/email. Lampiran WO/SR tidak disentuh (HBA belum memutuskan apakah penanda berlaku di
sana). Tidak ada harga atau valuasi di jalur portal.

## Sisa pekerjaan

- Belum di-commit saat record ini ditulis; commit dan push per-branch menyusul di repo CRM dan
  repo kanon/dokumen. **Belum di-merge ke `main`** — merge menunggu HBA.
- Granularitas penanda (per berkas atau per jenis berkas) belum diputuskan HBA; implementasi
  memakai per artefak dan mudah disesuaikan bila HBA memilih lain.
- **Penanda tanggal dokumen pada Riwayat: TERJAWAB dan terpasang.** HBA-DECISIONS-30 menetapkan
  tanggal dokumen menjadi penanda di Riwayat; saat implementasi ternyata sistem tidak menyimpan
  tanggal dokumen di mana pun, dan pertanyaan saya dijawab HBA 2026-10-24: "tanggal dokumen dari
  tanggal di undah" — penandanya adalah **waktu unggah berkasnya**. Terpasang di
  `app/reporting/history.py` (`_enrich_history` mengisi `document_date` dari waktu unggah berkas
  WO; kosong bila WO belum punya berkas, tidak dipinjam dari tanggal peristiwa), dan UI Riwayat
  menampilkannya sebagai lencana "Dokumen &lt;tanggal&gt;". Bukti: `tests/test_reporting_history.py`
  (`test_document_date_is_the_upload_time_of_the_wo_files`).
- Apakah penanda yang sama berlaku untuk lampiran WO/SR: menunggu satu kalimat HBA.
- Peran Admin kini berpenghuni; akun lain (mis. Finance/Kasir) belum diminta.

*End of implementation record.*
