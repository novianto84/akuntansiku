# IMPLEMENTASI — tanggal penugasan pada WO baru + pembersihan data dummy

```text
Record ID:      HBA-DECISIONS-54
Date:           2026-10-26
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruksi HBA:  "1. Tambahkan pada buat WO baru, tanggal penugasan. bisa
                 dikosongkan, bisa juga di tetapkan.
                 2. hilangkan data dummy yang dibuat di awal oleh kamu."
Status:         IMPLEMENTED — terpasang, 13 cek peramban LULUS, data dummy bersih
Classification: Audit record. NOT a canonical specification document.
```

## Butir 1 — tanggal penugasan pada Work Order baru

Form **Work Order baru** sekarang punya isian **"Tanggal penugasan"** berupa
pemilih tanggal. Boleh **dikosongkan** (boleh juga ditetapkan). Nilainya disimpan
pada kolom baru `work_orders.assignment_date` (migrasi **v44**, aditif dan
reversibel; WO lama tetap `NULL` = "belum ditetapkan").

Batasannya jelas dan disengaja: kolom ini mencatat **tanggal yang Anda nyatakan**
saat WO dibuat. Ia **bukan** pengganti jejak penugasan yang sebenarnya — saat
teknisi benar-benar ditugaskan, `work_order_assignments.created_at` tetap diisi
server. Tidak ada tanggal karangan: kosong berarti `NULL`, dan nilai yang tidak
berbentuk tanggal sah ditolak dengan pesan yang bisa dibaca.

Detail WO menampilkan baris **"Tanggal penugasan"**; bila kosong tertulis
*belum ditetapkan*, bukan tanggal tebakan.

## Butir 2 — data dummy dihapus

Yang dihapus persis apa yang dicetak `dev_seed.py` saat pertama dijalankan
2 Oktober 2026:

| Jenis | Yang dibuang |
|---|---|
| Work Order | WO-2026-001 … WO-2026-007 (7 WO) beserta JOB, penugasan, visit, kehadiran visit, material, laporan + revisinya, peristiwa persetujuan, snapshot pelanggan, pengingat |
| Service Request | SR-2026-001 … SR-2026-003 dan follow-up-nya |
| Kontak | Budi Santoso, Sari Dewi, Rudi Hartono |
| Unit | U-GS-001, U-GS-002, U-GS-003 beserta kode QR, foto, dokumen, komponen, lokasi, perlengkapan |
| Pelanggan | C-PLN (PT PLN Nusantara Power) dan C-TAMB (PT Tambang Sejahtera) beserta peran perusahaannya |
| Akun dev | `sales` dan `tech` (kata sandi dev `devpass123`) beserta sesi, keanggotaan workspace, profil, dan jejak auditnya |

Total **108 baris** dibuang. **Backup dibuat lebih dulu**:
`crm/data/backups/crm-before-seed-purge-20261026-184100.db` (11,4 MB) — seluruh
pembersihan ini bisa dikembalikan dari berkas itu.

**Yang sengaja TIDAK dihapus, dan alasannya:**

- Akun **`mgr`** — itulah akun yang tertaut ke identitas Google Anda
  (khd.anto@gmail.com). Menghapusnya akan mengunci Anda dari peran Manager.
- Seluruh **data asli**: pelanggan C-001 … C-009, unit MADI/MEBS/SOTA/PREA, WO
  PAG/SPK/…, kontak, spesifikasi, galeri, dan dokumen.
- **WO-2026-008** (dibuat 22 Oktober oleh akun mgr, bukan bagian seed) dan
  **company E-CVDM "Daya Mandiri"** — keduanya tidak dibuat `dev_seed.py`, jadi
  tidak saya sentuh. Kalau salah satunya juga dianggap sampah, cukup satu baris
  perintah.

Keadaan sekarang: **9 pelanggan, 8 unit, 7 WO** (WO-2026-008 + enam WO PAG/SPK),
0 SR, 0 visit, 2 penugasan (keduanya pada WO PAG/SPK/2025/77). Pemeriksaan
referensi menggantung: **nol** — tidak ada baris tersisa yang menunjuk data yang
sudah dihapus.

Alatnya tetap ada dan aman dijalankan ulang: `python3 purge_dev_seed.py` adalah
**dry run** (hanya melapor), `--apply` yang benar-benar menghapus dan selalu
membuat backup lebih dulu.

## Bukti

- `tests.test_migrations` 6 uji OK (migrasi v44 naik-turun bersih).
- `verify_wo_assignment_date_20261026.cjs` di deployment nyata (8092):
  **13 cek LULUS** — isian ada dan bertipe `date`; tanggal 2026-11-05 tersimpan
  apa adanya; dikosongkan tersimpan `NULL`; detail WO menampilkan tanggal dan
  "belum ditetapkan"; dua WO uji dihapus sehingga hitungan DB kembali sama.
- Setelah pembersihan, penjelajahan layar nyata: Dashboard (7 WO aktif),
  Work Order (7 baris), Pelanggan (9 perusahaan), Unit (8 unit), SR (kosong),
  Monitoring (7 WO perlu perhatian) — semuanya tampil normal, **0 galat
  JavaScript**.
- `crm.service` dan `crm-ui.service` aktif, `/healthz` 200, layar 200
  (bundle `index-BBR1afqn.js`).

## Berkas

`crm/app/migrations/migrate.py` (v44), `crm/app/wo/wo.py`, `crm/app/server.py`,
`crm/ui/src/types.ts`, `crm/ui/src/screens/WoScreen.tsx`,
`crm/ui/src/screens/WoDetailScreen.tsx`, `crm/purge_dev_seed.py` (baru),
`crm/ui/verify_wo_assignment_date_20261026.cjs` (baru).

Satu migrasi aditif; tanpa endpoint baru; tanpa aturan bisnis baru.
