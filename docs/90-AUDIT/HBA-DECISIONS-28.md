# HBA DECISION RECORD — Pemilik Unit: Perusahaan ATAU Perorangan (2026-10-22)

```text
Record ID:      HBA-DECISIONS-28
Date:           2026-10-22 (WIB)
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-22; implementation NOT authorized
Classification: Audit record. NOT a canonical specification document.
Implementation: No code/schema/migration/DB written by this record.
```

> Rekaman tangkap putusan HBA di ruang "etc". Tak tulis kode.

## Putusan HBA (pernyataan HBA)

> "C. Unit harus bisa ikut ke perusahaan ataupun per orangan. dalam case tertentu,
> misal perumahan juga mempunyain genset sendiri untuk backup rumahnya. ini tidak
> bisa dimasukan ke perusahaan."

HBA memilih opsi **C** dari tiga opsi yang Manager sajikan (A tetap seperti sekarang /
B penanggung jawab teks tanpa relasi / C relasi sungguhan unit–orang).

## Bacaan kunci

- Pemilik unit boleh **perusahaan ATAU perorangan**; keduanya sah. Unit tidak wajib
  menempel pada perusahaan.
- Harus ada cara mencatat unit milik perorangan **tanpa mengarang perusahaan palsu**.
- Contoh nyata dari HBA: **perumahan** yang punya genset sendiri untuk backup tidak
  dapat dimasukkan sebagai perusahaan.
- Ini keputusan bisnis (bentuk data & cara pelanggan dikenali), bukan keputusan teknis.

## Fakta sistem saat ini (diverifikasi 2026-10-22, bukan opini)

- `units.company_id` **sudah nullable**; pembuatan unit tanpa perusahaan sudah diizinkan
  kode (`app/unit/unit.py`, disertai komentar "never fabricate a Company").
  Data hidup: 3 unit, semuanya berperusahaan — jadi kemampuan ini belum pernah dipakai.
- `contacts.company_id` **NOT NULL** — kontak tanpa perusahaan tidak dapat eksis.
- **Tidak ada** tabel/relasi apa pun yang menautkan unit ke kontak/PIC. Relasi yang ada:
  companies→contacts (1-N) dan companies→units.
- Canon: BD-G01-G02 (LOCKED — V1) menetapkan perusahaan sebagai akar identitas tunggal
  dan menyatakan "No individual-customer identity model exists anywhere"; IS-01 E-08 /
  R-02 Company→Contact 1-N; SR-requester §12 — perorangan hanya sah sebagai *requester*
  dengan company NULL, tanpa entitas baru.

## Konsekuensi governance

- Putusan ini menyentuh keputusan **LOCKED** (BD-G01-G02) → wajib lewat revisi/supersede
  tercatat, bukan implementasi langsung di belakang kanon.
- Implementasi **belum diotorisasi**. Record ini tidak menulis kode, schema, atau migrasi.
- Canon resmi tidak diubah oleh record ini; revisi dokumen kanonik menunggu instruksi HBA.

## Belum diputuskan (open item, butuh putusan HBA lanjutan)

- **OQ-A — cara mewakili perorangan.** (a) kontak boleh tanpa perusahaan
  (`contacts.company_id` menjadi nullable; arti "kontak" tidak lagi selalu orang-pada-
  perusahaan), atau (b) entitas baru khusus pemilik perorangan. Canon saat ini menolak
  (b) secara eksplisit → (a) paling dekat, namun tetap revisi keputusan LOCKED.
- **OQ-B — kardinalitas pemilik.** Satu unit tepat satu pemilik (perusahaan X **atau**
  orang), atau boleh keduanya (unit milik perusahaan dengan penanggung jawab orang)?
  HBA menyebut "atau".
- **OQ-C — akses portal.** Apakah pemilik perorangan memperoleh akses portal eksternal
  di V1? Canon menunda akses eksternal perorangan ke V2 → rekomendasi tetap ditunda.
- **OQ-D — bentuk "perumahan".** Dicatat sebagai pemilik perorangan berupa *orang*
  (pengelola/ketua) atau sebagai *nama pemilik non-perusahaan* berbasis teks tanpa orang?
  HBA belum menyebut.

## Jawaban HBA atas open item (2026-10-22, lanjutan)

- **OQ-A → (a).** HBA: "kontak yang boleh ada tanpa perusahaan" — kontak tidak lagi wajib
  menempel pada perusahaan. Konsekuensinya `contacts.company_id` harus menjadi nullable
  dan makna "kontak" meluas menjadi orang yang boleh berdiri sendiri. Ini revisi
  keputusan LOCKED (BD-G01-G02 / CD-03), belum dibangun.
- **OQ-D → nama pemilik non-perusahaan.** Pemilik unit di luar perusahaan dicatat sebagai
  **nama berbasis teks** (mis. "Perumahan …"), bukan sebagai orang/entitas baru.
- **OQ-B / OQ-C belum dijawab eksplisit** — tetap OPEN (kardinalitas pemilik tunggal atau
  ganda; akses portal bagi pemilik perorangan).

## Perintah HBA 2026-10-22 (enam butir) + status

1. Kontak boleh ada tanpa perusahaan — **SELESAI & terverifikasi** (migrasi v27: kolom
   `contacts.company_id` menjadi NULL-able; kontak tanpa perusahaan Sah berdiri sendiri).
2. Nama pemilik non-perusahaan — **SELESAI & terverifikasi** (migrasi v27: kolom
   `units.owner_name`; unit boleh menempel ke perusahaan ATAU ke nama pemilik non-perusahaan).
3. Tabel PIC/kontak: tanpa kolom aksi berlebih, cukup tombol Edit + WhatsApp + Email;
   kolom Primary dihapus dari tabel — **SELESAI & terverifikasi**. Status kontak utama
   tetap ada di data dan diatur lewat formulir (backend tetap menegakkan satu per
   perusahaan); yang dihapus hanya tampilannya di tabel.
4. Kode unit otomatis dari singkatan nama perusahaan dengan nomor bertingkat —
   **SELESAI & terverifikasi**. Aturan HBA: 4 huruf (boleh 3 bila inisialnya memang 3) +
   2 angka mulai `01`, huruf dari singkatan nama, jenis usaha (PT/CV/UD/TOKO/KEMENTRIAN)
   TIDAK dipakai, nomor bertingkat per pemilik, kode **editable**. Contoh HBA terpenuhi:
   "Mensa Bina Sukses" → **MEBS-01**.
5. Foto pada daftar kontak — **SELESAI & terverifikasi** (migrasi v25 `contacts.photo`,
   pola sama dengan logo perusahaan; unggah dari pop-up form).
6. Form tambah pelanggan dan PIC sebagai pop-up window, bukan panel di alur halaman —
   **SELESAI & terverifikasi**.
7. (susulan, 22 Okt 2026) "tambah field website dan nomor telp di db pelanggan" —
   **SELESAI & terverifikasi**: migrasi v26 `crm_company_phone_website` menambah kolom
   `phone` dan `website` pada master perusahaan (boleh kosong, tidak dikarang), terbawa di
   create, update, form pop-up "Perusahaan baru", form "Edit perusahaan", dan ringkasan
   detail pelanggan. Field ini milik master pelanggan, terpisah dari profil perusahaan
   sendiri (`company_profile`) yang sudah punya phone/email.

8. (susulan, 22 Okt 2026) "list jenis usaha minta autofill, bukan dropdown" —
   **SELESAI & terverifikasi**: "Jenis usaha" kini input bebas dengan saran autofill
   (datalist PT/CV/TOKO/UD/KEMENTRIAN), bukan pilihan tetap, di pop-up "Perusahaan baru"
   dan di form "Edit perusahaan".

## Pelaksanaan paket poin 1, 2, 4 (2026-10-22)

- **Kode unit tersaran otomatis** dari nama perusahaan atau nama pemilik non-perusahaan,
  diisi lebih dahulu di form dan tetap bisa diedit; begitu diedit manual, saran berhenti
  menimpa. Nomor bertingkat per pemilik: unit pertama sebuah perusahaan mendapat `-01`,
  berikutnya `-02`, dan seterusnya melewati nomor yang sudah terpakai.
- **Kontak tanpa perusahaan** dapat dibuat dari pop-up "Kontak baru" (pilihan perusahaan
  boleh dikosongkan). Konsekuensi teknis yang saya terapkan: kontak tanpa perusahaan tidak
  dapat dijadikan kontak utama, karena status "utama" didefinisikan per perusahaan; dan
  kontak tersebut tidak memperoleh akses portal, karena rantai akses tetap menuntut
  perusahaan + PIC terverifikasi. Bila pembacaan ini berbeda dari maksud HBA, mohon koreksi.
- **Daftar kontak** kini dibaca satu kali per workspace (endpoint baru `GET /api/contacts`)
  supaya kontak tanpa perusahaan ikut tampil; filter "Tanpa perusahaan" ditambahkan.
- **Kode unit lama** `U-GS-001…003` dibiarkan apa adanya (belum ada instruksi HBA untuk
  mengganti); QR dan kode acak unit tidak tersentuh.

## Bukti (2026-10-22)

- Migrasi **v25 `crm_contact_photo`** terdaftar di `app/migrations/migrate.py`; kolom
  `contacts.photo` terbukti ada di `crm/data/crm.db`; `app/company/contact.py` (create +
  update) dan `app/server.py` (POST/PATCH kontak) membawa `photo`.
- `app/company/contact.py` & `app/server.py`: foto masuk lewat jalur yang sudah ada, tanpa
  endpoint baru dan tanpa perubahan allowlist.
- UI: `Modal` baru di `components/ui.tsx` (+ CSS `.modal-backdrop`, `position: fixed`),
  `PicScreen.tsx` ditulis ulang, `CompanyScreen.tsx` memakai pop-up.
- Verifikasi browser nyata `crm/ui/verify_pic_modal.cjs`: **22/22 PASS** (kolom tabel tanpa
  Primary, kolom Foto & Aksi, Edit + tautan `wa.me` + `mailto:`, pop-up fixed, pratinjau
  dan penyimpanan foto, edit label tersimpan, Escape menutup, nol error halaman).
- Verifikasi browser nyata `crm/ui/verify_v27.cjs`: **13/13 PASS** — saran kode dari nama
  perusahaan (`MEBS-01`), nomor bertingkat (`MEBS-01` → `MEBS-02`), kode tetap editable,
  saran dari nama pemilik non-perusahaan (`Perumahan Griya Asri` → `PEGA-01`), unit dengan
  pemilik non-perusahaan tersimpan dan tampil, kontak tanpa perusahaan dibuat & tampil,
  catatan "tidak bisa jadi kontak utama" muncul, serta "Jenis usaha" benar-benar input
  dengan 5 saran autofill dan nol dropdown.
- Verifikasi browser nyata `crm/ui/verify_company_phone.cjs`: **10/10 PASS** (kedua field ada
  di form pop-up dan form edit, nilai tersimpan ke database, ringkasan menampilkan nilainya,
  dan nilai bisa dikosongkan kembali). Data nyata dikembalikan seperti semula setelah uji.
- **Perbaikan semantik PATCH (temuan saat uji):** sebelumnya field opsional perusahaan tidak
  bisa dikosongkan — mengirim nilai kosong dianggap "jangan diubah", sehingga telepon salah
  ketik mustahil dihapus. Sekarang string kosong berarti "kosongkan" (disimpan NULL) dan
  `null` berarti "jangan diubah"; berlaku untuk alamat, kota, NPWP, jenis usaha, logo, serta
  telepon dan website.
- `npm run build` lulus; `crm.service` (menerapkan migrasi 27 saat start), `crm-ui.service`,
  `crm-ui-admin.service` direstart dan aktif. Data uji dihapus seluruhnya: kembali 3 unit
  (U-GS-001…003), 14 kontak, 3 kode QR unit, dan perusahaan 1 tanpa nilai telepon/website.
- Regresi dijalankan ulang setelah perubahan: `verify_pic_modal.cjs` dan
  `verify_company_phone.cjs` tetap lulus seluruhnya.

## Open item baru

- **OQ-E — aturan kode unit otomatis** (butuh putusan HBA): singkatan diambil dari kata apa
  dan berapa huruf, apakah jenis usaha (PT/CV/UD) ikut dipakai; "bertingkat" itu per
  perusahaan, per tipe unit, atau lintas semua; format nomor (001/01) dan urutannya; kode
  untuk unit tanpa perusahaan (perorangan/perumahan); serta nasib tiga kode lama
  `U-GS-001…003` — diganti atau dibiarkan, dan jaminan QR/kode acak tetap resolve.

## Langkah berikut termurah

HBA menjawab **OQ-E** dan menegaskan OQ-B/OQ-C. Setelah itu Manager membangun satu paket
sekaligus — pemilik unit (perusahaan ATAU nama non-perusahaan), kontak tanpa perusahaan,
dan kode unit otomatis — karena ketiganya menyentuh form unit/kontak yang sama, sehingga
satu kali build saja.

## 28 Okt 2026 — poin 7: pintasan WhatsApp / Telepon / Email jadi ikon

**Perintah HBA (chat):** "sebaiknya email, wa, dan call pakai icon saja. lebih enak dipandang."

**Status:** DIBANGUN dan DIVERIFIKASI (perubahan presentasi UI saja).

**Yang dibangun**
- Tiga ikon SVG inline di `crm/ui/src/components/icons.tsx` (WhatsApp, gagang telepon, amplop) —
  tanpa paket/dependensi baru, ukuran 15 px, warna mengikuti `currentColor`.
- Kolom Aksi daftar Kontak (`PicScreen.tsx`): pintasan WhatsApp dan Email berubah dari teks
  menjadi ikon. **Telepon (`tel:`) adalah pintasan BARU** — sebelumnya tidak ada; memakai kolom
  `contacts.phone` yang sudah ada, tanpa kolom/endpoint baru.
- Tiap tautan tetap membawa `title` + `aria-label` (mis. "WhatsApp 0812…") supaya makna ikon
  tetap terbaca saat hover dan oleh pembaca layar; tombol **Edit tetap berupa teks** karena
  instruksi HBA hanya menyebut email/WA/call.
- Gaya: `btn--icon` di `styles.css`, memakai token tema v9 — WhatsApp `--ok` (hijau), Telepon
  `--warn` (amber), Email `--accent` (merah). Ikon mati bila kontaknya tidak punya data terkait
  (tanpa telepon → WA & Telepon tidak dirender; tanpa email → Email tidak dirender).

**Bukti**
- `npm run build` lulus (bundle `index-D1Oe2egj.js`); `crm-ui.service` + `crm-ui-admin.service`
  direstart dan aktif; `crm.service` tetap aktif.
- Bundle yang benar-benar disajikan sudah memuat fitur ini: `crm.benshi.my.id` menyajikan
  `index-D1Oe2egj.js` dan berkas itu memuat `btn--icon-call`.
- Verifikasi browser nyata `crm/ui/verify_pic_icons.cjs`: **15/15 lulus** — 15 baris kontak aktif
  semuanya punya pintasan; WA 15 tautan, Telepon 15, Email 3 (hanya 3 kontak yang punya email);
  tak ada lagi teks "WhatsApp"/"Email" di kolom Aksi; semua tautan ikon-saja 15 px dengan
  title + aria-label; warna terhitung `rgb(34,197,94)` / `rgb(245,158,11)` / `rgb(239,43,43)`
  (persis token); hover sungguhan memakai `--ok-soft`; nol error halaman. Skrip ini hanya
  membaca — tidak ada data uji yang ditulis atau dihapus.

**Yang TIDAK disentuh:** tidak ada perubahan schema, migrasi, endpoint, allowlist, atau aturan
bisnis. Nomor telepon ditampilkan/dial apa adanya (`tel:`), tanpa normalisasi baru selain
membuang karakter non-digit seperti yang sudah ada pada pintasan WhatsApp.

**Open item (tidak berubah):** OQ-E (rincian kode unit lama `U-GS-001…003`) dan OQ-B/OQ-C
(akses portal pemilik perorangan) masih menunggu putusan HBA. Catatan repo: seluruh perubahan
yang sudah live ini (termasuk yang lebih awal) masih **belum di-commit** di working tree.

## 28 Okt 2026 (lanjutan) — poin 8: pop-up Unit/WO/SR, urutan menu, Email 2 & HP 2

**Perintah HBA (pesan di ruang kerja, 28 Okt 2026)**

1. «pelanggan dan kontak PIC sudah ok. sudah muncul pop up window. tapi unit, dan WO, dan SR masih
   belum. sekalian dirubah yah menjadi pop up window»
2. «kemudian urutan di menu sebelah kiri layar itu, SR diatas. baru WO.»
3. «kemudian tambahkan juga di db PIC untuk email ke 2. dan nomor HP ke 2. namun di tabel tidak
   usah ditampilkan, terkecuali dibuka secara detail.»

**Yang dibangun (semua sudah live)**

- **Pop-up untuk tiga form.** Form "Unit baru" (`UnitScreen.tsx`), "Work Order baru" (`WoScreen.tsx`),
  dan "Service Request baru" (`SrScreen.tsx`) sekarang memakai komponen `Modal` yang sama dengan
  pop-up Pelanggan/Kontak: latar `position: fixed`, judul di kepala jendela, tombol ✕, klik latar
  atau tombol **Escape** menutup. Tidak ada lagi form yang mendorong isi halaman ke bawah. Isi form,
  urutan field, dan aturan validasinya **tidak diubah sama sekali** — hanya bungkusnya.
- **Urutan menu kiri.** Service Request sekarang di ATAS Work Order
  (`Dashboard > Service Request > Work Order > Unit > Pelanggan > Kontak / PIC > …`).
- **Email 2 dan HP 2 pada data kontak/PIC.** Migrasi **v28** (`crm_contact_secondary_contact`)
  menambah kolom `contacts.email2` dan `contacts.phone2` — keduanya boleh kosong (NULL). Keduanya
  muncul di jendela detail/edit kontak saja; **tidak pernah menjadi kolom tabel** Kontak / PIC.
  Domain `app/company/contact.py` meneruskan kedua field pada create dan PATCH, dan sejak paket ini
  field opsional kontak (jabatan, telepon, email, email2, HP 2, label, foto) mengikuti aturan yang
  sama dengan master Pelanggan: **kosong berarti benar-benar dikosongkan**, tidak dikirim berarti
  dibiarkan apa adanya. Tanpa itu, nomor yang salah ketik mustahil dihapus.

**Bukti (dijalankan, bukan klaim)**

- **Migrasi live.** `journalctl --user -u crm.service` mencatat
  `[crm] applied migrations on startup: [28]`; head DB berjalan = 28, kolom
  `email2`/`phone2` ada di `PRAGMA table_info(contacts)`.
- **Uji backend.** `tests/test_contact_secondary.py` (baru, 9 uji) + `tests/test_contact.py` +
  `tests/test_company_logo.py` → **32 uji OK**. Regresi lebih luas
  (`test_company`, `test_company_server`, `test_doors`, `test_customer_wp08`, `test_contact_intake`)
  → **100 uji, 98 lulus**; 2 gagal **bukan** karena paket ini (lihat temuan di bawah).
- **Verifikasi browser nyata** (`crm/ui/verify_modal_v28.cjs`, Chromium headless):
  **30/30 lulus** — menu `Service Request (1) di atas Work Order (2)`; ketiga form membuka
  `.modal-backdrop` dengan `position: fixed`, form berada DI DALAM jendela, dan **nol form inline**
  di panel halaman; Escape/klik latar menutup; tabel kontak tetap `FOTO | NAMA | PERUSAHAAN |
  JABATAN | TELEPON | EMAIL | LABEL / CATATAN | AKSI` (tidak ada kolom HP 2 / Email 2); jendela
  detail memuat field HP 2 dan Email 2; satu penulisan NYATA dilakukan (Email 2 dan HP 2 tersimpan
  lalu dibaca ulang) dan **dikosongkan kembali** sehingga nol baris uji tertinggal; nilai kedua
  field tidak bocor ke tabel; nol error halaman.
- **Bukti form benar-benar mengirim permintaan** (`crm/ui/verify_modal_submit_v28.cjs`):
  **11/11 lulus** — ketiga pop-up mengirim POST ke `/api/unit`, `/api/wo`, `/api/sr` (terlihat di
  jaringan), penolakan duplikat tampil sebagai toast error, jendela tetap terbuka saat gagal, dan
  jumlah baris tidak berubah (3→3 unit, 7→7 WO, 3→3 SR) — jadi bukti ini tidak meninggalkan data.
- **Regresi fitur sebelumnya** (`crm/ui/verify_pic_icons.cjs`): **15/15 lulus** (pintasan
  WA/Telepon/Email tetap ikon + title/aria-label, warna token tidak berubah).
- **Live di domain.** `crm.benshi.my.id` menyajikan bundle `index-CWBPwNqY.js`
  (sha256 `48f4e9e87ba2b4bc8cbf7f88e29b776dba722cc975f5c45ec4215f6254989ad0`),
  berkas yang sama ada di `ui/dist/assets/`, dan memuat label `Email 2` serta `HP 2`.
  `crm.service`, `crm-ui.service`, `crm-ui-admin.service` direstart dan aktif; `/healthz` publik 200.

**Temuan (bukan bagian perintah HBA, saya laporkan apa adanya)**

- Dua uji di `tests/test_doors.py` gagal: `test_internal_routes_are_not_public` dan
  `test_public_door_denies_role_delete` masih menuntut `/api/company/1/roles` **ditolak** di pintu
  publik. Perilaku yang berlaku sejak keputusan Anda 21 Okt 2026 (Manager boleh menempelkan role,
  gerbangnya di dalam `company_mod`) memang membuat path itu publik-tapi-tergerbang. **Bukan akibat
  paket ini**: `git show HEAD:app/server.py` sudah memuat bentuk itu, dan diff `server.py` dalam
  paket ini tidak menyentuh satu baris pun yang memuat kata `roles`. Uji itu perlu diselaraskan ke
  keputusan 21 Okt — **saya tidak mengubahnya tanpa persetujuan Anda**.

**Yang tidak diputuskan sendiri**

- "Dibuka secara detail" saya tafsirkan sebagai **jendela Edit/detail kontak** yang sudah ada — untuk
  kontak belum ada halaman detail tersendiri. Kalau yang Anda maksud halaman detail tersendiri
  (read-only), sebut saja; itu perubahan tampilan kecil, bukan data.
- Kode unit lama `U-GS-001…003` dan akses portal pemilik perorangan **masih menunggu putusan Anda**
  (open item lama, tidak berubah).
- Seluruh perubahan yang sudah live ini **masih belum di-commit** di working tree.

---

## Paket: sesi cookie httpOnly — "kenapa tiap refresh harus login ulang?" (22 Okt 2026)

**Pertanyaan HBA (grup "etc"):** "mengapa setiap saya refresh, saya harus login ulang yah?"
**Pilihan HBA:** "cookie httpOnly yang saya pilih".

**Diagnosis (fakta, bukan dugaan).** Sesinya sendiri sehat: `sessions.expires_at`
berlaku 8 jam dan tidak ada yang dicabut. Yang terjadi adalah token sesi hanya
hidup di memori SPA (`ui/src/api.ts` menyatakannya sebagai trade-off V1), jadi
setiap muat ulang dokumen mengosongkan token dan jatuh kembali ke layar masuk.
Buktinya di DB saat itu: 66 sesi aktif dengan jejak login berjarak 30–60 detik —
pola khas "refresh lalu masuk lagi", bukan pola sesi kedaluwarsa.

**Yang dibangun (IS-04, increment yang dulu ditunda).**

- `app/server.py` — login dan callback Google kini juga mengirim sesi sebagai
  cookie `crm_session` (`HttpOnly`, `SameSite=Lax`, `Max-Age=28800`, `Path=/`,
  plus `Secure` bila permintaan memang datang lewat TLS menurut
  `X-Forwarded-Proto`). Logout mencabut sesi **dan** menghapus cookie.
  `Authorization: Bearer` tetap diterima dan tetap menang bila keduanya ada —
  jadi klien API dan seluruh uji lama tidak berubah. TTL, pencabutan, dan
  pemeriksaan peran tidak disentuh sama sekali.
- `ui_server.py` + `ui_server_admin.py` — meneruskan header `Cookie` ke backend
  dan meneruskan `X-Forwarded-Proto` (sebelumnya keduanya disaring; tanpa ini
  cookie akan hilang di perantara).
- `ui/src/App.tsx` — saat boot, bila tidak ada token di fragment, SPA menanyakan
  `/api/auth/me` sekali; sesi pulih dari cookie. 401 tetap berarti layar masuk.
- `ui/src/api.ts` — komentar postur diperbarui (bukan lagi "reload = login ulang").

**Tanpa schema.** Tidak ada migrasi baru; head DB tetap **28**. Tidak ada
endpoint, aturan bisnis, atau hak akses yang berubah.

**Bukti nyata.**

- `crm/ui/verify_session_cookie.cjs` (Chromium headless) → **20/20 lulus**:
  pintu publik `https://crm.benshi.my.id` memasang cookie `HttpOnly` +
  `SameSite=Lax` + `Secure` (Path=/), `document.cookie` **tidak** memuat
  `crm_session`, **refresh tetap masuk**, tab baru langsung masuk, 3× refresh
  berturut tetap masuk, `/api/auth/me` dengan cookie saja = 200 (`mgr`);
  logout → cookie terhapus, reload kembali ke form masuk. Pintu admin
  `http://100.72.199.61:8093` (http polos) juga tetap hidup setelah refresh,
  cookie tanpa `Secure` (kalau `Secure` dipasang di http, browser membuangnya).
  Nol error halaman.
- Uji `curl` langsung: `Set-Cookie` muncul di backend 8010, di proxy 8092, dan
  di domain publik (di sana dengan atribut `Secure` — cloudflared memang
  meneruskan `X-Forwarded-Proto: https`). Tanpa cookie dan tanpa token → 401;
  data operasional (`/api/company`, `/api/sr`, `/api/wo`) dengan cookie saja → 200.
- Uji backend tersasar: `test_session`, `test_auth_server`, `test_google_oauth`,
  `test_lockout`, `test_server`, `test_authz`, `test_doors`,
  `test_customer_auto_register`, `test_identity` → **135 uji, 131 lulus**.
- Live: `crm.benshi.my.id` menyajikan `assets/index-C-oJt2iX.js`
  (sha256 `fc558e30813065fcc5dc6c5679421ed03b62d5413335a943042c9c90c50b9915`,
  identik dengan `ui/dist/assets/`); ketiga unit direstart dan aktif.
- Kebersihan data: 5 sesi uji (curl + browser) dicabut kembali; sesi aktif
  kembali **66**, sama seperti sebelum paket ini. Nol data domain tersentuh.

**Temuan yang saya laporkan apa adanya (bukan akibat paket ini).**

- `tests/test_doors.py`: dua uji gagal (`test_internal_routes_are_not_public`,
  `test_public_door_denies_role_delete`) — keduanya masih menuntut
  `/api/company/1/roles` ditolak di pintu publik, padahal keputusan Anda 21 Okt
  2026 (Manager boleh menempel role) berlaku. Sama seperti yang sudah dilaporkan
  di paket sebelumnya; belum saya ubah tanpa persetujuan Anda.
- `tests/test_customer_auto_register.py`: dua uji gagal karena masih menuntut
  head migrasi = **20**, sedangkan working tree sudah **28**. Kedua uji ini tidak
  menyentuh HTTP maupun sesi (hanya `migrate`/`db`), jadi tidak mungkin
  dipengaruhi paket ini; keduanya perlu diselaraskan ke head migrasi terkini —
  juga tidak saya ubah tanpa persetujuan Anda.

**Yang tidak dipecahkan sendiri / masih menunggu HBA.**

- Empat uji usang di atas: mau saya selaraskan ke keputusan yang berlaku?
- Open item lama tetap: nasib tiga kode unit `U-GS-001…003` dan apakah pemilik
  perorangan perlu akses portal.
- Seluruh perubahan live ini **masih belum di-commit** di working tree.

**Tindak lanjut (HBA: "selaraskan saja. kemudian commit" — 22 Okt 2026).**

- Empat uji usang diselaraskan ke keputusan yang berlaku, tanpa menyentuh
  perilaku aplikasi:
  `tests/test_doors.py` (`test_internal_routes_are_not_public` tidak lagi
  memuat path roles; `test_public_door_denies_role_delete` →
  `test_public_door_routes_role_delete_to_staff_gate`, menuntut 401 tanpa sesi
  alih-alih 404) dan `tests/test_customer_auto_register.py` (uji v20 memakai
  helper `_head()` dari registry migrasi, tidak lagi mematok 20).
  Bukti: `tests.test_doors` + `tests.test_customer_auto_register` →
  **45 uji OK**, sebelumnya 2 gagal.
- Commit di repo `crm/` (working tree kini bersih):
  `17cb835` — penyelarasan uji; `cef7aca` — paket data & UI v25–v28 + sesi
  cookie httpOnly. **Belum di-push** ke `origin` (branch
  `feat/company-logo-20261017` kini 5 commit di depan) karena push bukan
  pekerjaan yang Anda minta; sebut saja kalau mau saya dorong.

- Sapuan **seluruh** paket uji (`python3 -m unittest discover -s tests`) dijalankan
  sebagai penutup: **633 uji, 12 gagal (5 failures + 7 errors)**. Kedua belasnya
  **bukan akibat paket ini** dan sudah ada sebelum commit cookie: saya jalankan
  ulang berkas-berkas uji yang gagal di salinan repo pada commit `17cb835`
  (sebelum pekerjaan cookie) dan daftarnya **identik** — 12 yang sama, nama yang
  sama. Rinciannya:
  - **4 dari satu cacat nyata** di `app/material/seam.py` (berkas terakhir diubah
    di commit `bb5e100`, 16 Okt — tidak tersentuh paket v25–v28 maupun paket
    cookie): `_require_seam_scope` memakai nama `material_usage_id` yang tidak ada
    di lingkupnya, sehingga fungsi gagal **sebelum** memeriksa kepemilikan. Di
    lapisan HTTP hasilnya 403 "denied", jadi **tertutup, bukan bocor** — tapi
    fitur tautan material–inventory praktis tidak bisa dipakai
    (`tests.test_material_server` 403 pada alur yang sah, 3 error di
    `tests.test_material_seam`).
  - **5 pemeriksaan kepemilikan tidak menyala**: `test_visit`, `test_material_usage`,
    dan 3 error `tests.test_wo` (WO dari SR ditolak sebagai "lintas workspace"
    padahal sah), plus `tests.test_location` (label lokasi kembali kosong).
  - **2 uji usang** karena keputusan yang sudah berlaku: `tests.test_unit_qr`
    menuntut rute unit ditolak di pintu publik, padahal keputusan operasional
    publik sudah berlaku; `tests.test_internal_identity_link` masih menuntut akun
    Google tak dikenal ditolak, padahal pendaftaran Google otomatis sudah berlaku.

## 28 Okt 2026 (lanjutan) — poin 9: form Work Order (nomor otomatis, status, unit lookup, lingkup tipe pekerjaan)

**Perintah HBA (pesan di ruang kerja, 28 Okt 2026)**

```text
nomor WO dibuat otomatis saja incresement.
untuk apa ada status awal draft dan open. saya rasa ini tidak perlu. cukup pilihan
nantinya buat WO order, artinya open WO, save = draft, dan batal = cancel.
Unit Posture sebaiknya diganti formatnya. misal secara default berarti belum
ditentukan, jika unit sudah ada, bisa di isi langsung kodenya atau di lookup. misal
berdasarkan company nya. atau pic nya. dan untuk unit yang belum ada, berarti diganti
jadi tombol unit baru. dan memunculkan page unit baru.
field "unit" ini lah yang saya maksud tadi dengan lookup. tapi akan lebih baiknya
menjadi kolom search berdasarkan company atau kodenya langsung. atau bisa juga ambil
dari SR.
kode job ini apa saya bingung.
Tipe pekerjaan itu tolong dijabarkan lingkupnya misal "Service - Perawatan berkala,
perbaikan terjadwal, penggantian suku cadang"
mungkin ada baiknya ditambahkan field. "Info yang diterima", " merk mesin", "merk
generator" ,"kapasitas","mode operasi (single operation / synchrone operation)",
"module controller", "typical load( standby / baseload / primeload)"
```

**Status:** DIBANGUN dan DIVERIFIKASI untuk empat hal yang tidak menyentuh schema.
Dua hal dijawab sebagai penjelasan (bukan perubahan), satu hal DITUNDA karena menuntut
keputusan HBA (field baru = schema + tempatnya belum jelas).

**Yang dibangun**

- **Nomor WO otomatis (increment).** `app/wo/wo.py` menambah `next_wo_number()` yang
  melanjutkan pola yang sudah dipakai produksi (`WO-<tahun>-<3 angka>` — data lama
  WO-2026-001…008). Form boleh dikosongkan; keunikan tetap diperiksa
  `_check_unique_wo_number`, jadi nomor kembar tetap ditolak (tidak pernah senyap).
  Isian manual tetap dihormati.
- **Pilihan "Status awal" dihapus.** Yang menentukan sekarang tombolnya: **Buat WO
  (OPEN)** menerbitkan WO resmi, **Simpan sebagai draf** menyimpan DRAFT, **Batal**
  membuang form. Ini sejalan dengan kanon, bukan melonggarkannya: BD-WORKMODEL-001 §3
  menyatakan DRAFT **bukan** WO (penyimpanan sementara milik pembuat, boleh tanpa JOB,
  tidak masuk lifecycle). Tidak ada state baru, tidak ada transisi baru.
- **Field unit menjadi pencarian + tombol "Unit baru".** Dropdown "Unit posture"
  dihapus dari form. Sekarang: kotak pencarian yang menyaring unit berdasarkan **kode
  unit, nama unit, nama perusahaan, atau nama pemilik**; memilih unit menampilkan chip
  kode unit + tombol "Ganti unit"; tombol **Unit baru** membuka form unit baru di atas
  form WO (jendela bersarang) dan unit yang baru dibuat langsung tersedia untuk dipilih.
  Bila WO dibuat dari SR milik sebuah perusahaan, daftar unit dipersempit ke perusahaan
  itu lebih dahulu ("ambil dari SR"); kata kunci melebarkannya kembali ke seluruh unit.
- **Form unit baru kini satu komponen bersama** (`ui/src/components/UnitFormModal.tsx`)
  yang dipakai layar Unit dan form WO — supaya tidak ada dua versi isian unit yang bisa
  berbeda diam-diam. Isi form, saran kode, dan panggilan `POST /api/unit` tidak berubah.
- **Escape pada jendela bersarang diperbaiki.** Sebelumnya satu tekanan Escape menutup
  **kedua** jendela sekaligus (setiap jendela punya pendengar sendiri); sekarang hanya
  jendela paling atas yang ditutup.
- **Lingkup tipe pekerjaan ditampilkan.** Pilihan tipe pekerjaan memakai kalimat lingkup
  yang diturunkan dari BD-WORKMODEL-001 §§1.1–1.3: Service (PM) — perawatan berkala
  terjadwal & penggantian suku cadang; Inspeksi — kunjungan pemeriksaan/pencatatan
  kondisi unit (bukan kunjungan service); Emergency Troubleshoot — respons awal gangguan
  yang perlu segera. Kalimat lengkapnya muncul di bawah dropdown saat tipe dipilih.
  Tidak ada Work Model baru, service type baru, atau aturan baru.
- **Kode JOB diberi penjelasan di form** (jawaban atas pertanyaan HBA): kode JOB adalah
  penanda baris pekerjaan **di dalam** WO itu (J1, J2, …), bukan nomor global; satu WO
  boleh punya beberapa JOB dengan kode, tipe pekerjaan, dan SCOPE masing-masing.

**Yang TIDAK dibangun (menunggu keputusan HBA) — bukan karena teknis, tapi karena bisnis**

- **Field baru**: "Info yang diterima", "merk mesin", "merk generator", "kapasitas",
  "mode operasi (single/synchrone)", "module controller", "typical load
  (standby/baseload/primeload)". Ini menuntut migrasi baru, dan tempatnya belum
  ditentukan: merk mesin/generator/kapasitas/mode operasi/module controller/typical load
  sifatnya **atribut unit** (melekat pada genset, dipakai berulang lintas WO), sedangkan
  "Info yang diterima" sifatnya **milik WO/SR** (terikat intake). Menaruhnya di tempat
  yang salah berarti mengetik ulang data yang sama setiap WO. Tidak ada satu pun field
  ini yang diturunkan dari kanon — semuanya usulan baru, jadi harus diputuskan dulu.
- **Unit Posture "belum ditentukan" sebagai keadaan default.** Secara tampilan sudah
  demikian (unit kosong = belum ditentukan). Yang **tidak** dilonggarkan: posture itu
  menurut CD-11 §5 menuntut **alasan** dan otoritas **Manager/Coordinator**. Form
  sekarang menolak menyimpan bila unit belum dipilih dan alasannya kosong. Bila HBA
  memang ingin syarat itu dihapus, itu keputusan bisnis yang mengubah CD-11 §5 — bukan
  keputusan teknis AI.
- **Ambil unit dari PIC**: unit menempel ke perusahaan atau ke nama pemilik
  non-perusahaan; tidak ada relasi unit→PIC, sehingga "berdasarkan pic nya" belum bisa
  ditepati apa adanya (yang tersedia: pencarian lewat nama perusahaan/pemilik).

**Bukti**

- Backend: `tests/test_wo.py` bertambah kelas `WOAutoNumberTest` (5 uji) — nomor
  kosong diterbitkan, bertingkat, melanjutkan urutan yang ada, isian manual tetap
  dihormati, duplikat tetap ditolak, dan penomoran tetap unik lintas workspace: **5/5
  lulus**. Regresi tersasar **96 uji, 3 error** — ketiganya `tests.test_wo.WOSRLineageTest`
  yang sudah tercatat di berkas ini sebagai cacat **pra-ada** ("WO dari SR ditolak
  sebagai lintas workspace padahal sah"), daftar yang sama seperti sebelum paket ini.
  Sapuan pendukung lain: `tests.test_wo_server`, `test_job`, `test_emergency`,
  `test_outstanding`, `test_workspace_isolation_negative` — **40 uji lulus penuh**.
- UI: `npx tsc -p tsconfig.json --noEmit` bersih; `npm run build` lulus
  (`index-BTyGqPTG.js`); `crm.service`, `crm-ui.service`, `crm-ui-admin.service`
  direstart dan aktif; `crm.benshi.my.id` menyajikan bundle yang identik dengan berkas
  di server.
- Verifikasi browser baru `crm/ui/verify_wo_form_v29.cjs`: **44/44 lulus**, termasuk
  satu **penulisan sungguhan** — WO diterbitkan tanpa nomor dan keluar **WO-2026-009**
  (lanjutan dari 008), `state=OPEN`, `unit_posture=EXISTING_UNIT`, baris daftar
  bertambah tepat satu, lalu baris uji itu **dihapus kembali** sehingga jumlah WO
  kembali 8 dan pekerjaan tetap 8 JOB. Skrip juga membuktikan form **tidak mengirim
  apa pun** bila unit dan alasan sama-sama kosong, dan membuktikan Escape hanya menutup
  jendela teratas.
- Regresi skrip verifikasi lama: `verify_modal_v28` 30/30, `verify_modal_submit_v28`
  11/11 (skrip ini disesuaikan ke bentuk form baru), `verify_pic_icons` 15/15,
  `verify_pic_modal` 22/22, `verify_company_phone` 10/10, `verify_session_cookie`
  20/20 (satu kegagalan chip pada percobaan pertama adalah **flaky** — lulus penuh saat
  dijalankan ulang sendirian).
- **Dua skrip verifikasi lama memang sudah usang sebelum paket ini**, dan saya
  membuktikannya dengan membangun ulang commit terakhir (`cef7aca`) di direktori
  terpisah, menyajikannya di port 8192, lalu menjalankannya di sana: `verify_v27.cjs`
  gagal persis sama (menunggu `.panel:has-text("Unit baru")` padahal form unit sudah
  menjadi jendela pop-up sejak paket 28 Okt sebelumnya) dan `verify_photo.cjs` gagal
  persis sama (bagian portal pelanggan menunggu form login, padahal sejak sesi
  cookie httpOnly halaman kedua dalam konteks browser yang sama sudah langsung masuk).
  Keduanya perlu diselaraskan ke bentuk sekarang — menunggu izin Anda karena menyentuh
  skrip verifikasi paket lama.
- **Data uji dibersihkan**: empat foto uji yang terunggah ke WO 7 oleh `verify_photo.cjs`
  saat sapuan regresi saya hapus kembali (tersisa satu foto lama dari 21 Okt). Sesi
  login uji dari puluhan kali masuk otomatis **tidak** saya cabut — tabel `sessions`
  tidak menyimpan penanda peramban, sehingga mencabut berdasarkan waktu berisiko
  mengeluarkan sesi Anda sendiri; sesi-sesi itu kedaluwarsa sendiri dalam 8 jam.

**Yang tidak disentuh:** tidak ada migrasi baru (head database tetap **28**), tidak ada
endpoint baru, tidak ada perubahan otorisasi, tidak ada Work Model/service type/status
baru, dan tidak ada aturan CD-11 §5 yang dilonggarkan.

**Langkah berikut termurah:** HBA memutuskan **tempat** tujuh field baru (atribut unit
vs milik WO/SR) dan menegaskan apakah posture "unit belum ditentukan" tetap menuntut
alasan + otoritas Manager/Coordinator. Setelah itu satu paket migrasi + form bisa
dibangun sekaligus bersama penyelarasan dua skrip verifikasi lama.

## 28 Okt 2026 (lanjutan) — poin 10: lanjutan form WO (asal SR menyatu, contoh alasan) + penjelasan JOB

**Perintah/pertanyaan HBA (ruang kerja)**

```text
saya masih bingung kode job ini. fungsinya apa? dan apa tujuannya? atau dari pembicaraan
apa hingga jadi ada "job" ini ?
alasan unit belum ditentukan, berikan contohnya "belum teridentifikasi" atau
"belum dapat informasi detail dari customer"
"Dibuat dari service request" sebaiknya dihilangkan, dan digabungkan saja langsung di
field search "unit"
abaikan dulu mengenai 7 field itu. saya lupa. itu harusnya masuk ke unit. nanti saya akan
cek dulu kelengkapan di unit.
```

**Status:** dua perubahan DIBANGUN dan DIVERIFIKASI; satu pertanyaan DIJAWAB dari kanon
(tanpa perubahan kode); satu hal DITUNDA atas permintaan HBA sendiri.

**Yang dibangun**

- **"Dibuat dari Service Request" dihapus; asalnya dipilih dari kotak pencarian unit yang
  sama.** Satu kotak sekarang mencari **dua hal**: unit (kode unit, nama unit, nama
  perusahaan, nama pemilik) dan **Service Request** (nomor SR, nama peminta, nama
  perusahaan). Baris SR ditandai badge "SR"; memilihnya menampilkan chip "SR <nomor>" plus
  tombol **Lepas SR**, dan daftar unit langsung dipersempit ke perusahaan SR itu. Backend
  tidak berubah: `source_sr_id` tetap dikirim dan lineage tetap dicatat CREATED_FROM —
  yang hilang hanya dropdown terpisahnya. Aturan kanonik "paling banyak satu WO resmi per
  SR" tetap berlaku dan tetap ditegakkan backend.
- **Contoh alasan "unit belum ditentukan"** dari HBA: kotak isian kini memakai saran
  (datalist) berisi **"Belum teridentifikasi"** dan **"Belum dapat informasi detail dari
  customer"**, dan teks bebas tetap boleh. Syaratnya tidak dilonggarkan: posture ini tetap
  menuntut alasan terisi dan otoritas Manager/Coordinator (CD-11 §5).

**Yang dijawab (tidak ada kode yang berubah)**

Pertanyaan HBA: *kode JOB itu apa, fungsinya apa, dan dari pembicaraan apa ia muncul.*

- **Asalnya**: pada 23 Sep 2026 Business Authority mengeluarkan
  `BD-WORKTYPE-001 Rev.A — JOB / SCOPE Canonicalization`. Keputusannya lahir karena satu
  pekerjaan yang sama punya banyak nama yang saling bertumpuk (Issued Job, Add Job,
  Corrective Job, Current/Planned/Pending Job, Task, Scope Item). Semua nama itu
  dinyatakan **bukan entitas terpisah** dan disatukan menjadi **satu konsep: JOB**.
  Usulan-usulan otomatis yang sempat muncul (aturan sehari, timeout 24 jam, WO baru
  otomatis, ON HOLD otomatis, Add Job otomatis) **ditarik seluruhnya** dan tidak pernah
  menjadi kanon.
- **Fungsinya**: JOB adalah **satuan pekerjaan di dalam satu WO** — hal yang benar-benar
  dikerjakan teknisi, yang bisa ditandai selesai (CHECKED) atau belum (UNCHECKED), dan
  yang menjadi tempat menempelnya ON HOLD bila pekerjaan belum selesai. SCOPE adalah
  **daftar/lingkup pekerjaan** milik WO; JOB tinggal di dalamnya. Satu JOB hanya milik satu
  WO, dan satu WO boleh punya banyak JOB.
- **Tujuannya**: supaya "apa yang dijanjikan dan apa yang dikerjakan" bisa **dihitung,
  dilaporkan, dan diaudit per WO** — bukan catatan bebas yang tidak bisa ditagih.
  Finding, Diagnosis, dan Recommendation **bukan** JOB dan tidak menghasilkan JOB secara
  otomatis; pekerjaan yang muncul saat pelaksanaan hanya menjadi JOB bila benar-benar
  dikerjakan (penanda Added During Execution).
- **Kode JOB** hanya label baris itu di dalam WO bersangkutan (J1, J2, …) supaya bisa
  dirujuk saat menandai selesai, menambah JOB saat pelaksanaan, atau melaporkan. Ia bukan
  nomor identitas seperti kode unit, tidak unik lintas WO, dan tidak punya aturan
  penomoran bisnis — karena itu sampai sekarang diisi J1 lebih dahulu dan boleh diganti.
  Usul menunggu keputusan HBA: dibuat otomatis J1, J2, … di dalam tiap WO, atau dibiarkan
  manual.

**Yang DITUNDA atas permintaan HBA**

Tujuh field tambahan ("Info yang diterima", merk mesin, merk generator, kapasitas, mode
operasi, module controller, typical load) **tidak dibangun** dan tidak akan menyentuh WO:
HBA menyatakan semuanya **milik Unit** dan akan memeriksa dulu kelengkapan field Unit.
Manager mencatatnya sebagai item terbuka, bukan sebagai pekerjaan berjalan.

**Bukti**

- `npx tsc -p tsconfig.json --noEmit` bersih; `npm run build` lulus
  (`index-UfqDEKcG.js`); `crm-ui.service` + `crm-ui-admin.service` direstart dan aktif.
- Verifikasi browser `crm/ui/verify_wo_form_v29.cjs` diperbarui menjadi **55 pemeriksaan,
  55 lulus**, termasuk: kotak yang sama menemukan unit dan SR sekaligus (mengetik
  "Tambang" menemukan U-GS-003 **dan** SR-2026-002), memilih SR memunculkan chip + tombol
  Lepas SR dan mempersempit daftar unit ke perusahaan SR itu (2 unit), Lepas SR
  mengembalikan 3 unit, dua contoh alasan benar-benar tersedia di datalist, dan satu
  penulisan sungguhan tetap dilakukan (WO otomatis `WO-2026-009`) lalu **dihapus kembali**
  sehingga WO kembali 8 dan JOB tetap 8.
- Regresi skrip verifikasi lama: `verify_modal_v28` 30/30, `verify_modal_submit_v28`
  11/11, `verify_pic_icons` 15/15, `verify_pic_modal` 22/22, `verify_company_phone`
  10/10, `verify_session_cookie` 20/20 — total **163 pemeriksaan hijau, nol gagal**.
- Database yang jalan bersih dari sisa uji: 8 WO, 8 JOB, 1 foto (foto lama 21 Okt).

**Yang tidak disentuh:** tidak ada migrasi baru (head tetap **28**), tidak ada endpoint
baru, tidak ada perubahan otorisasi, dan tidak ada aturan CD-11 §5 yang dilonggarkan.

**Langkah berikut termurah:** HBA memutuskan (a) kode JOB otomatis atau tetap manual, dan
(b) kelengkapan field Unit. Setelah itu field unit bisa dibangun sebagai satu paket
migrasi tanpa menyentuh WO.

## 28 Okt 2026 (lanjutan) — catatan lintas-pekerja: dua skrip verifikasi lama kini hijau, belum di-commit

Setelah paket poin 10 selesai, saat memeriksa status repo ditemukan **dua berkas yang
berubah tanpa dikerjakan sesi Manager ini**: `ui/verify_v27.cjs` dan `ui/verify_photo.cjs`.
Isinya tepat penyelarasan yang tadi diusulkan (`.panel` → `.modal` karena form unit sudah
menjadi jendela pop-up; konteks peramban terpisah untuk staf dan pelanggan karena sesi
cookie httpOnly membuat halaman kedua sudah masuk sebagai staf; penghapusan fixture unit/
kontak alih-alih sekadar menonaktifkannya). Jejak lain di mesin ini menunjukkan proses
Hermes lain berjalan pada jam yang sama (`~/.hermes/logs/process-results/` memuat dua
proses yang bukan milik sesi ini, dan beberapa profil Hermes aktif pada 21:55).

Tindakan Manager: **keduanya dijalankan ulang untuk memeriksa hasilnya, tanpa menyunting
dan tanpa meng-commit** — `verify_v27.cjs` **13/13 lulus**, `verify_photo.cjs` **4/4
lulus** (fixture-nya membersihkan sendiri: unit 3, kontak 1 dihapus). Kedua berkas itu
**masih tertinggal sebagai perubahan belum di-commit** di working tree, menunggu keputusan
HBA — bukan hanya soal isi, tetapi soal siapa yang berhak menyentuh skrip verifikasi paket
lama supaya tidak ada dua pekerja menyentuh area yang sama tanpa saling tahu.

Dua catatan data apa adanya: satu foto uji yang diunggah `verify_photo.cjs` pada
pemeriksaan ulang ini sudah dihapus kembali (kini 1 foto lama), dan di tabel `contacts`
ditemukan **empat baris bernama "Uji Foto Hermes 22Okt"** (tiga aktif, satu nonaktif) yang
**bukan** dibuat sesi ini dan **tidak** saya hapus — asalnya dari pekerjaan agen lain dan
saya tidak menyentuh hasil kerja yang bukan milik saya tanpa perintah HBA.

## 22 Okt 2026 (lanjutan) — kode JOB otomatis; dua skrip verifikasi lama di-commit; jejak repo ditrace

**Keputusan HBA** (chat ruang "etc", 22 Okt 2026, dijawab satu per satu):

- **"JOB itu bukannya harusnya otomatis?"** — ya, dan sekarang begitu: kode JOB
  diterbitkan server sebagai lanjutan `J1`, `J2`, … **di dalam** WO bersangkutan.
  Form "Work Order baru" dan form "Tambah JOB" tidak lagi meminta kode. Isi form
  WO yang tadinya 5 kotak kini 4 (nomor, cari unit, alasan unit, SCOPE).
- **"Info yang diterima bisa di SR maupun WO. sama saja."** — field itu dibangun
  di SR **dan** WO; belum dikerjakan, masuk paket migrasi berikutnya (bersama
  enam field mesin/generator).
- **Tiga kode unit lama `U-GS-001…003` = item dummy, diabaikan dulu**, dan HBA
  minta diingatkan untuk menghapus data dummy. Reminder dicatat di sini **dan**
  di kanban (`hba-hapus-data-dummy`). Sisa data uji yang ditemukan apa adanya:
  4 baris kontak `Uji Foto Hermes 22Okt` (tiga aktif, satu nonaktif) — belum
  dihapus, menunggu perintah HBA.
- **Portal pemilik perorangan = portal unit** → tidak ada yang perlu ditambah
  atau diubah.
- **Izin menyelaraskan skrip verifikasi lama diberikan** → `verify_v27.cjs` dan
  `verify_photo.cjs` kini di-commit.

**Batas kanon yang tidak dilonggarkan.** Kanon melarang auto-JOB / auto-derivation
(BD-WORKMODEL-001 §"tidak diadopsi: … auto-JOB"; TA-01 §"JOB establishment …
No auto-derivation"; IS-02 "never auto-JOB"). Yang otomatis hanyalah **label baris**
di dalam satu WO. Aktor tetap menetapkan tipe pekerjaan dan lingkupnya, dan WO
resmi tetap wajib ≥1 JOB. Fungsi penomoran menolak mengarang baris: DRAFT tanpa
JOB tetap tanpa JOB (diuji). Tidak ada migrasi/schema/endpoint baru — head tetap **28**.

**Bukti.** `tests/test_wo.py` 35 uji (6 uji baru `JobCodeAutoTest` semua hijau;
3 error lama `WOSRLineageTest` lintas-workspace tetap sama persis dan terbukti bukan
akibat paket ini), `tests/test_emergency.py` 9/9 lulus. Verifikasi peramban
`verify_wo_form_v29.cjs` **58/58 lulus** dengan dua pemeriksaan baru: form tidak lagi
memuat "Kode JOB", dan satu WO sungguhan terbit sebagai `WO-2026-009` dengan JOB `J1`
dari server lalu dihapus kembali (WO kembali 8, JOB tetap 8). `verify_v27.cjs` **13/13**
dan `verify_photo.cjs` **4/4** lulus setelah penyelarasan; sesi/bundel yang dipakai
verifikasi dicabut dan foto uji dihapus kembali (kini 1 foto lama 21 Okt). Bundle yang
disajikan cocok dengan berkas di server (`index-Dc5_bhVj.js`), layanan `crm`, `crm-ui`,
`crm-ui-admin` aktif kembali.

**Trace repo (permintaan HBA "coba trace siapa itu").** Seluruh **13 commit** repo CRM
diautor dan di-commit oleh `Hermes <hermes@mitrasp.local>`; hari ini **6 commit**
(13:10, 13:10, 19:55, 19:55, 21:18, 21:51). Identitas git repo ini memang Hermes, dan
**tidak ada author lain sepanjang sejarah repo**. **Tidak ada push ke GitHub hari ini**
— branch fitur di remote masih commit 18 Okt. Dua commit yang tampak "baru" di
`origin/main` (`b2ebe48`, `23abbb2`, dokumentasi) berasal dari akun GitHub HBA sendiri
tertanggal **2 Okt** dan baru terlihat hari ini hanya karena repo lokal belum pernah
`fetch` sejak saat itu: bukan pengiriman hari ini.

Temuan yang perlu ditindak dari trace itu: **dua sesi Hermes mengerjakan repo yang sama
secara bersamaan**. Pada 22:40 dua sesi agen (`20261022_211927_571a32` dan
`20261022_212021_ea6299`) menerima prompt ruang "etc" yang sama; satu sesi menyunting
`verify_v27.cjs`/`verify_photo.cjs` pada 21:26–21:30 dan menulis bagian audit di berkas
ini, sesi ini mengerjakan penomoran JOB. Dua penulis pada satu working tree adalah risiko
kehilangan perubahan yang nyata; usul: **satu sesi pemilik repo per paket kerja**, sesi
lain menyerahkan (handoff) alih-alih menyunting langsung.

---

## Lock HBA 2026-10-22 (lanjutan) — pekerja boleh ditambah Manager dan Admin

```text
Record ID:      HBA-DECISIONS-28 (addendum pekerja)
Date:           2026-10-22
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED + IMPLEMENTED (paket "lock dan eksekusi")
Classification: Audit record. Bukan dokumen kanon.
```

**Putusan HBA (verbatim ruang chat).** "yang boleh menambah pekerja manager dan admin."
Sebelumnya HBA juga menanyakan menu data pekerja ("belum ada kah menu untuk data pekerja?
untuk add mereka, kemudian untuk pasang role mereka") dan menjawab pilihan sandi dengan
"lock dan eksekusi".

**Yang dibangun (satu paket).**

- `app/access/staff.py` — registry pekerja: daftar, daftar-ulang, ubah peran, aktif/nonaktif,
  dan picker teknisi. Tidak pernah menerbitkan atau mengembalikan kredensial.
- Migrasi **v29** (aditif, reversibel): `internal_users.full_name`, `internal_users.created_by_user_id`.
- Sel otoritas baru di `app/access/authz.py`: `manage/internal_user` = Manager, Admin (dari lock
  HBA 22 Okt); `view/internal_user` = Manager, Admin, Coordinator (dibutuhkan peran ASSIGN_WO
  untuk memilih teknisi **berdasarkan nama**).
- Rute: `GET/POST /api/staff`, `GET /api/staff/{id}`, `GET /api/staff/technicians`.
  `/api/staff` dan `/api/staff/{id}` **tetap pintu ADMIN** karena menambah pekerja dan mengubah
  struktur peran adalah kapabilitas fondasi (HBA-DECISIONS-23: sisi Tailscale, bukan publik).
  `/api/staff/technicians` **publik** karena membaca daftar teknisi aktif adalah kebutuhan
  operasional penugasan WO (penugasan terjadi di permukaan operasional).
- UI: menu **Pekerja** (daftar, tombol tambah, penyetelan peran, status aktif/nonaktif, status
  "Masuk Google"); field "ID pengguna teknisi" (numerik) di halaman WO diganti pencarian nama.

**Batas keamanan yang dipertahankan (bukan keputusan AI, tapi pengaman teknis).** Manager boleh
mendaftarkan pekerja dan memasang peran lapangan (Sales/Coordinator/Technician) serta
mengaktifkan/menonaktifkannya; Manager **tidak boleh** membuat atau memberi peran Admin/Manager,
tidak boleh mengubah peran sendiri, tidak boleh menonaktifkan akun sendiri atau akun Admin/Manager
lain. Pekerja **tidak pernah dihapus** — hanya dinonaktifkan, supaya riwayat penugasan dan
persetujuan tidak putus. Admin aktif terakhir tidak bisa dinonaktifkan. Akun peran pelanggan
tidak tersentuh modul ini.

**Sandi: tidak ada.** Identitas eksternal produksi adalah Google saja (terkunci IS-03, `authn.py`),
jadi modul ini tidak menerbitkan sandi awal; pekerja masuk dengan akun Google dan status
"belum tertaut" ditampilkan sampai Admin/Manager menautkan akun Google orang itu. Sandi lama
(`LocalProvider`) tetap hanya jalur dev/uji.

**Bukti.** `tests/test_staff.py` 16 uji baru (domain + HTTP + migrasi) lulus; `tests/test_authz.py`
dan `tests/test_doors.py` tetap lulus (57 uji gabungan, OK). UI `npm run build` lulus (tsc + vite).
Bukti live pada **salinan** `data/crm.db` (DB produksi **tidak** disentuh, masih v28):
17/17 pemeriksaan lulus — migrasi v29 naik di data produksi, Manager 201 membuat pekerja,
proyeksi tanpa kredensial, picker tersaring nama, Manager 403 saat memberi peran Admin,
nonaktifkan 200 lalu hilang dari picker, Technician 403 pada registry dan picker,
pintu publik 404 pada registry dan 200 pada picker.

**Belum dikerjakan / menunggu.** (a) Menautkan akun Google pekerja belum punya layarnya sendiri —
mekanisme v19 (`internal_link`) sudah ada, tombolnya belum. (b) Sapuan paket uji penuh dijalankan
terpisah; hasilnya dilaporkan di chat. (c) Restart layanan agar migrasi v29 naik di DB produksi.

*End of addendum.*

## Addendum — 23 Oktober 2026: hapus permanen master belum terpakai + temuan pintu admin

**Keputusan HBA (diruang obrolan, dikutip apa adanya).** "tombol delete hanya bila belum ada data
masuk. saya setujui." dan sebelumnya "role manager dan admin yang bisa delete". Sekaligus izin
menghapus data uji: "hapus data 'uji foto hermes' yang lain biarkan dulu saja. karena masih butuh
data dummy. nanti reminder lagi untuk hapus data dummy."

**Aturan yang dibangun.** Master (Pelanggan, Kontak/PIC, Unit) boleh dihapus **permanen** hanya
selama belum ada satu baris pun yang menunjuknya; begitu ada unit, kontak, SR, tautan, peran, WO,
komponen, lokasi, QR, atau snapshot, backend menolak dengan 409 `in_use` dan pesannya meminta
menonaktifkan saja — CD-08 Q11-Q13 tetap berlaku untuk master yang sudah dipakai. Kewenangan baru
`("delete","master")` hanya Manager dan Admin; selain itu 403 `forbidden`. Titik masuk:
`DELETE /api/contacts/{id}`, `DELETE /api/company/{id}`, `DELETE /api/unit/{id}`.

**Bukti.** `tests/test_purge.py` 14 uji lulus (izin matriks, hapus kosong, tolak terpakai, tolak
peran lain, tolak lintas workspace). Uji live lewat pintu publik crm.benshi.my.id (Manager):
kontak kosong dihapus 200, unit kosong dihapus 200, pelanggan kosong dihapus 200, Technician
403 `forbidden`, pelanggan id 1 ditolak 409 ("units (2), contacts (2), service_requests (2),
company_roles (1)"), unit id 1 ditolak 409 ("work_orders (3), unit_qr_codes (1),
customer_snapshots (2)"). Setelah semua uji, jumlah data kembali seperti semula: 7 pelanggan,
16 kontak, 3 unit, 6 akun internal; tidak ada baris uji tersisa. Commit `b80b103`; bundle UI
`index-DVUXvrM2.js` sudah tersaji di `crm.benshi.my.id`.

**Pembersihan data uji.** Empat baris kontak `Uji Foto Hermes 22Okt` (id 20/21/24/25) dihapus
permanen atas izin HBA, setelah dipastikan tidak dirujuk SR, intake, maupun tautan identitas.
Cadangan DB sebelum hapus: `crm/data/backup/crm.db.bak-20261023-115636-before-ujifoto-purge`.
Data dummy lain (termasuk unit `U-GS-001..003`) sengaja dibiarkan; pengingat di board
`t_d9eb7194` diperbarui.

**Temuan dan keputusan HBA — pintu admin tidak bisa dipakai masuk.** `CRM_GOOGLE_REDIRECT_URL`
dipatok ke `https://crm.benshi.my.id/api/auth/google/callback`, sehingga login dari alamat
Tailscale pun selalu mendarat kembali di crm.benshi.my.id dan sesi cookie-nya menempel di host
publik itu; akibatnya pintu admin (UI 8093 → backend 8011) tidak pernah mendapat sesi. Karena
menu Pekerja sengaja hanya hidup di pintu admin (PUBLIC_PATH_PREFIXES hanya membuka
`/api/staff/technicians`), menu itu **tampil tetapi gagal memuat dan gagal menyimpan** dari
crm.benshi.my.id — terbukti dengan 404 pada GET dan POST `/api/staff` lewat pintu publik.
Dua pilihan disodorkan ke HBA, dan HBA memilih yang kedua (dikutip apa adanya): "buka endpoint
pekerja di crm.benshi.my.id untuk Manager dan Admin saja". **Dilaksanakan**: `/api/staff` dan
`/api/staff/{id}` kini dirutekan di pintu publik, penjaganya tidak pindah (tanpa sesi 401, selain
Manager/Admin 403). `/api/settings`, `/api/company-profile`, dan `/api/link-authority` tetap
tertutup rapat di pintu publik. Bukti live lewat crm.benshi.my.id: Manager membaca registry 200,
menyimpan pekerja baru 201, Manager diberi peran Admin ditolak 403 ("butuh Admin"), menonaktifkan
pekerja 200, Technician 403, Sales 403, tanpa sesi 401, `/api/settings` 404. Akun uji yang dibuat
saat pembuktian sudah dihapus; akun internal kembali enam seperti semula (mgr, sales, tech, tiga
akun pelanggan). Uji `test_staff` disesuaikan: dua uji lama (yang menuntut 404) diganti uji baru
yang menuntut 200 untuk Manager dan 403 untuk peran lain; `test_doors` dan `test_purge` tetap lulus.


## 23 Oktober 2026 (lanjutan) — field genset pada Unit + dua gallery (foto & dokumen)

**Permintaan HBA (dikutip apa adanya).** "Saya minta penambahan field pada unit genset. sebagai
berikut: Merk Mesin; type mesin; Kapasitas mesin ..... kVA; Serial number mesin. Merk Generator;
Type Generator; Kapasitas Generator ... kVA; Serial Number Generator. Jenis Enclosure (open type /
silent type / containerize); Serial Number Genset; Speed .... (RPM); Frequncy .... (Hz);
Tegangan .... (V). Gallery untuk upload foto. Gallery untuk dokumen / pdf."

Ini sekaligus **menjawab item terbuka poin 10**: Manager dulu mencatat merk mesin/merk
generator/kapasitas/mode operasi/module controller/typical load sebagai "menunggu tempatnya".
HBA kini menyebut daftar finalnya sendiri, dan seluruhnya **milik Unit** — persis seperti yang
diusulkan (melekat pada genset, dipakai ulang setiap WO, bukan diulang di tiap WO).

**Yang dibangun.** Dua belas field nameplate + jenis enclosure disimpan pada tabel `units`
(migrasi **v30** `crm_unit_genset_spec`, aditif dan reversibel), dan dua gallery pada dua tabel
baru (migrasi **v31** `crm_unit_media`): `unit_photos` dan `unit_documents`. Head bergerak
**29 → 31**.

- **Kolom bertipe TEXT, bukan REAL/INTEGER.** HBA tidak menetapkan satuan di luar tanda kurung
  pada label, dan nameplate kerap ditulis lebih dari satu angka (mis. tegangan "380/220").
  Kolom karena itu menyimpan **apa yang benar-benar diketik**, dan kosong tetap NULL. Sifat
  angka ditegakkan di modul (`app/unit/unit.py`), bukan oleh tipe kolom: kapasitas (kVA) harus
  angka, speed/frequency harus angka bulat, tegangan boleh berbentuk himpunan angka
  (`^[0-9][0-9 ,./-]*$`), panjang nilai dibatasi 120 karakter. Nilai tak sah **ditolak dengan
  pesan**, bukan disimpan senyap.
- **Kosakata jenis enclosure ditutup** pada tiga jenis yang HBA sebut sendiri — `OPEN`,
  `SILENT`, `CONTAINERIZE` — dengan label yang memakai kata-katanya ("open type", "silent type",
  "containerize"). Jenis lain ditolak (`jenis enclosure tidak dikenal: 'TENDA'`).
- **Kontrak isian.** Field yang tidak dikirim **tidak berubah**; field yang dikirim `null` juga
  tidak berubah; field yang dikirim string kosong **dikosongkan** (disimpan NULL). Tidak ada
  pengisian otomatis dari unit lain, template, atau WO sebelumnya — diuji eksplisit.
- **Dua gallery = catatan aset, bukan bukti WO dan bukan permukaan publikasi.** Karena itu
  tabel gallery **sengaja tidak punya kolom approval/publikasi**: kontrol publikasi ke pelanggan
  tetap di tempat yang kanon tetapkan, yaitu bukti WO (`wo_photos.approval_state`, v22).
  Menambah kolom setujui di sini akan menjadi perubahan bisnis yang belum ada yang memutuskan,
  jadi tidak dibuat.
- **Kewenangan.** Unggah foto/dokumen: peran staf yang bekerja pada unit (Manager, Sales,
  Technician, Admin, Coordinator — himpunan yang sama dengan unggah bukti WO). Hapus: **Manager
  dan Admin saja**, memakai sel wewenang kurasi yang sudah ada (bukan sel matriks baru).
  Scope workspace (IS-11) ditegakkan lewat penjaga `app/unit/unit` untuk kedua gallery.
- **Batas ukuran (dipilih Manager, terbuka untuk dikoreksi HBA).** Foto maksimal **4 MB** dan
  dokumen maksimal **10 MB** (ukuran setelah didekode), dengan daftar jenis berkas yang diterima
  (foto: jpeg/png/webp/gif; dokumen: pdf, txt, csv, jpeg/png, doc/docx, xls/xlsx). Permintaan
  yang tidak sah dijawab **400**, aktor yang tidak berwenang **403** — dipisah supaya layar bisa
  membedakan "berkasnya salah" dari "Anda tidak boleh".
- **Titik masuk:** `GET/POST /api/unit/{id}/photos`, `GET/DELETE /api/unit/{id}/photos/{pid}`,
  `GET/POST /api/unit/{id}/documents`, `GET/DELETE /api/unit/{id}/documents/{did}`. Semuanya
  dirutekan di **pintu publik** (awalan `/api/unit/` sudah publik), tetapi login tetap wajib:
  tanpa sesi 401, dan peran di cek di dalam modul. `spec` ikut pada `POST /api/unit` dan
  `PATCH /api/unit/{id}`.

**Bukti.**

- Uji backend baru `tests/test_unit_spec.py`: **33 uji lulus** — round-trip migrasi v30/v31
  (turun ke 29 melepas kolom+tabel, naik lagi mengembalikan), simpan-baca seluruh field, kosong
  tetap NULL, tolak enclosure asing / kapasitas bukan angka / RPM pecahan / tegangan berisi kata /
  nilai terlalu panjang, tolak lintas workspace, gallery foto & dokumen (unggah, daftar, unduh,
  hapus), Technician boleh unggah tetapi **tidak** boleh menghapus, tolak mime asing, tolak
  berkas terlalu besar, tolak base64 rusak, nama berkas dibersihkan dari jalur direktori
  (`C:\\Users\\anto\\sertifikat.pdf` → `sertifikat.pdf`), foto unit lain tidak dapat dihapus lewat
  id unit yang salah, dan permukaan HTTP-nya (401 tanpa sesi, 201/200/403 sesuai peran, 400 untuk
  berkas terlalu besar).
- Bukti **live lewat pintu publik crm.benshi.my.id** (`/home/anto/.hermes/cache/scratch/verify_unit_spec.sh`):
  unit uji dibuat 201 dengan 13 field terisi apa adanya; `PATCH` mengosongkan satu field
  (`engine_serial` → `null`) dan menaikkan `frequency_hz` ke 60 sementara field lain tidak
  tersentuh; `enclosure_type: "TENDA"` ditolak 403 dengan pesannya; foto 1x1 PNG terunggah 201
  dan terbaca kembali (`max_bytes` 4194304); PDF terunggah 201 dengan `byte_size` benar dan nama
  berkas sudah bersih; daftar dokumen **tanpa** payload, unduhan satu dokumen mengembalikan isi
  yang benar; Technician ditolak 403 saat menghapus foto, Manager 200; kedua gallery kembali nol;
  unit uji dihapus 200; **daftar unit kembali tiga (U-GS-001…003)** dan tabel gallery kembali 0
  baris.
- Verifikasi peramban `ui/verify_unit_spec_v30.cjs`: **34 pemeriksaan lulus, nol gagal** — 12
  field nameplate + jenis enclosure benar-benar ada di form "Unit baru"; unit uji dibuat lewat
  layar dan seluruh nilai terbaca kembali di kartu; kapasitas "seratus" **ditolak dengan pesan**
  dan data lama tidak berubah; field yang dikosongkan ikut kosong di kartu; gallery foto dimulai
  kosong (tanpa placeholder palsu), foto diunggah lewat input berkas sungguhan lalu tampil;
  dokumen tampil dengan nama dan ukuran, tombol **Unduh** menghasilkan berkas bernama asli; peran
  **Technician melihat isi gallery tetapi tidak melihat tombol Hapus**; foto & dokumen dihapus
  lewat tombol; form panjang tetap selesai di layar 900x520; nol galat halaman.
- Regresi skrip lama: `verify_v27.cjs` 13/13, `verify_wo_form_v29.cjs` semua lulus,
  `verify_photo.cjs` 4/4, `verify_modal_v28.cjs` semua lulus.
- `npx tsc -p tsconfig.json --noEmit` bersih; `npm run build` lulus (`index-DJpD8uRH.js` + `index-Ctsf_PKz.css`),
  `crm.service`, `crm-ui.service`, dan `crm-ui-admin.service` direstart dan aktif; bundle baru
  sudah tersaji di crm.benshi.my.id (health dan API mengembalikan field baru).
- Commit: `9c70b81` (backend), `58e9b5f` (layar + skrip verifikasi), dan satu commit lanjutan
  untuk batas tinggi pop-up. Working tree bersih.

**Perbaikan kecil yang perlu ikut tercatat.** Form "Unit baru" kini jauh lebih panjang, dan
sebelum paket ini jendela pop-up tidak punya batas tinggi sama sekali (`.modal` hanya
`overflow: hidden`). Tingginya sekarang dibatasi `calc(100vh - 10vh)`, isi jendela yang bergulir,
sedangkan judul dan tombol tutupnya tetap terlihat. Diuji di layar kecil 900x520: form panjang
tetap dapat diisi sampai tombol Simpan — satu pemeriksaan tambahan di skrip verifikasi peramban.

**Tidak bocor ke portal pelanggan.** Proyeksi customer tetap allowlist eksplisit
(`unit_code`, `unit_name` di `app/customer/serving.py`; snapshot v10 menyusun datanya sendiri di
`app/customer/snapshot.py`), jadi nomor seri mesin/generator/genset dan field nameplate lain —
data internal yang lazimnya sensitif — **tidak** ikut terkirim ke halaman pelanggan. Ini fakta
hasil pemeriksaan, bukan fitur baru; kalau HBA ingin sebagian field tampil ke pemilik unit, itu
keputusan terpisah.

**Temuan yang perlu HBA ketahui (bukan kerusakan, tapi interaksi dua aturan HBA).**
Membuka kartu sebuah unit **menerbitkan QR portalnya** (perilaku HBA-25 yang sudah berlaku), dan
QR itu terhitung sebagai "sudah ada data masuk". Jadi begitu Anda membuka satu unit, tombol Hapus
unit itu **berhenti berlaku** dan menolak dengan alasan "sudah ada unit_qr_codes (1)" — bukan
dihapus diam-diam. Ini terlihat langsung di verifikasi peramban. Bila Anda ingin unit yang baru
salah input tetap bisa dihapus lantas, jalan yang terbuka adalah tidak menerbitkan QR saat kartu
sekadar dibuka (mis. QR dibuat hanya saat diminta). Itu keputusan Anda; belum saya ubah.

**Temuan kecil tentang sisa uji (bukan akibat paket ini, tapi ketahuan saat memeriksa).**
`ui/verify_photo.cjs` mengunggah **dan menyetujui** satu foto ke WO-2026-007 sebagai fixture,
lalu membersihkan unit/kontaknya — tetapi **foto dan barisnya tidak pernah dihapus**. Dua kali
skrip itu dijalankan hari ini untuk regresi meninggalkan dua baris `wo_photos` (id 11 dan 12);
akibatnya galeri portal pelanggan menampilkan satu gambar lebih banyak setiap kali skrip
dijalankan. Kedua baris sisa itu sudah dihapus kembali (cadangan DB lebih dulu:
`data/backup/crm.db.bak-20261023-135634-before-verifyphoto-residue-purge`), sehingga `wo_photos`
kembali satu baris seperti sebelum pengujian. Usul: skrip itu dibuat membersihkan fotonya sendiri
(atau memakai WO khusus uji) supaya pengujian berulang tidak lagi menumpuk bukti palsu di
database kerja. **Belum saya ubah** — berkas itu bukan bagian dari paket ini.

**Masih terbuka.** Tiga field yang disebut di poin 10 tetapi **tidak ada** pada daftar final HBA
kali ini — **mode operasi (single/synchrone), module controller, typical load** — belum punya
tempat: kalau memang masih diinginkan, sebut tempatnya (kartu unit bersama field lain, atau
dianggap gugur) dan saya tambahkan. "Info yang diterima" tetap seperti keputusan sebelumnya: di
SR **dan** WO pada paket migrasi berikutnya. Seluruh commit paket ini **belum didorong ke origin**
(ref `origin/main` di mesin ini masih dari 2 Oktober, 22 commit di belakang HEAD) — menunggu
perintah HBA.

*End of decision record.*
