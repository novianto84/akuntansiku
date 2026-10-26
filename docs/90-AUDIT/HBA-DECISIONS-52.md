# PERBAIKAN — "Gagal menyimpan profil perusahaan (http_501)"

```text
Record ID:      HBA-DECISIONS-52
Date:           2026-10-26
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Laporan HBA:    "Mengapa saya dapat error ini? Gagal menyimpan profil perusahaan
                 Permintaan ditolak (http_501)"
Keputusan HBA:  "Buka /api/company-profile dan /api/settings di pintu publik —
                 penjaga Admin tetap di dalam server (seperti yang Anda putuskan
                 untuk menu Pekerja 23 Okt)"
Status:         FIXED — terpasang, uji backend hijau, jalur proxy terbukti 200
Classification: Audit record. NOT a canonical specification document.
```

## Penyebabnya: dua cacat yang bertumpuk

Pertama, **proxy UI tidak mengenal PUT.** `ui_server.py` (pintu 8092, yang
menyajikan UI di `crm.benshi.my.id`) dan `ui_server_admin.py` (8093) hanya
menangani GET, POST, PATCH, dan DELETE. Karena itu setiap permintaan PUT dijawab
`501 Unsupported method` oleh pustaka HTTP Python **sebelum** menyentuh backend —
persis pesan yang muncul di layar. Layar Profil Perusahaan dan Pengaturan
memang memakai PUT untuk menyimpan.

Kedua, **setelah 501 itu dibuka, rutenya tetap tidak ada di pintu publik.**
`/api/company-profile` dan `/api/settings` sengaja hanya dirutekan di pintu admin.
Masalahnya pintu admin tidak pernah bisa dipakai login: alamat kembali Google
dipaku ke host publik, jadi sesi selalu lahir di `crm.benshi.my.id`. Artinya
kedua layar itu **mustahil dipakai siapa pun**, bukan hanya gagal menyimpan —
membacanya pun 404.

## Yang diperbaiki

`do_PUT` ditambahkan pada kedua proxy UI (meneruskan body dan header seperti
POST/PATCH). Tidak ada kewenangan baru di lapisan itu; backend tetap memeriksa
sesi dan peran pada setiap rute.

Atas keputusan HBA di atas, `/api/company-profile` dan `/api/settings`
**dirutekan** di pintu publik dengan gerbang **Admin tetap di dalam**
`company_profile_mod.update` dan `settings_mod`. Ini alasan yang sama dengan
keputusan 2026-10-23 untuk registry pekerja: yang menyembunyikan rute bukan
pengaman, karena pintu admin tak pernah memegang sesi. `/api/link-authority`
(wewenang tautan pelanggan) **tetap** ADMIN-only dan tetap 404 di pintu publik.

## Uji yang diselaraskan (tanpa menghapus bagian penolakan)

- `tests/test_company_profile.py`: `test_public_door_denies_company_profile` →
  `test_public_door_routes_company_profile_but_keeps_admin_gate` (tanpa sesi 401,
  Manager 403, Admin 200 untuk GET dan PUT di pintu publik).
- `tests/test_settings.py`: sama untuk `/api/settings`.
- `tests/test_doors.py`: daftar rute yang "tidak public" kini memakai
  `/api/link-authority`; ditambah
  `test_public_door_routes_config_but_denies_non_admin`. Catatan penting: POST ke
  kedua rute config itu tetap 404 karena **verb tulisnya PUT**, bukan POST —
  perilaku lama tidak berubah, hanya alasannya yang sekarang tertulis.
- `tests/test_staff.py`: dua rute config itu kini dinyatakan routed, sementara
  `/api/link-authority` tetap tidak.

## Bukti

- `tests.test_company_profile` 10 uji OK; `tests.test_settings` 10 uji OK;
  `tests.test_doors` 31 uji OK; `tests.test_staff` 16 uji OK.
- Lewat proxy 8092 (pintu yang dipakai browser): tanpa sesi **401**, sesi Manager
  **403** ("company profile requires Admin role"), sesi Admin **200** untuk
  `GET /api/company-profile`, `GET /api/settings`, dan `PUT /api/company-profile`
  (403/400 dari backend membuktikan PUT kini benar-benar sampai ke backend, bukan
  lagi 501 di proxy).
- Sesi uji Admin dibuat langsung lewat modul sesi, dipakai, lalu **dicabut**
  (`revoked_at` terisi; jumlah sesi aktif kembali seperti sebelumnya). Nomor
  telepon yang ditulis saat uji dikembalikan ke `null`, jadi `company_profile`
  kembali berisi nilai semula (kolom `updated_at` ikut berubah — konsekuensi
  wajar dari satu kali tulis-sunting).
- `crm.service`, `crm-ui.service`, `crm-ui-admin.service` di-restart; `/healthz`
  200 dan layar 200.

## Berkas

`crm/ui_server.py`, `crm/ui_server_admin.py`, `crm/app/server.py` (komentar
routing + dua entri `PUBLIC_EXACT_PATHS`), dan empat berkas uji di atas.
Tanpa migrasi, tanpa endpoint baru, tanpa aturan bisnis baru.

## Yang masih perlu HBA ketahui

Layar **Pengaturan** (`/api/settings`) ikut terbuka dengan keputusan yang sama
karena mekanismenya persis sama; kalau HBA ingin Pengaturan tetap tertutup
sementara, itu satu baris perubahan — kembalikan `/api/settings` ke daftar admin
saja.
