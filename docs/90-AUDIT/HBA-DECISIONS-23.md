# HBA DECISION RECORD — operasional penuh di publik, konfigurasi tetap Tailscale (2026-10-14)

```text
Record ID:      HBA-DECISIONS-23
Date:           2026-10-14
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-14 via chat
Classification: Audit record. NOT a canonical specification document.
Implementation: No code/schema/migration/DB written by this record.
```

> Rekaman putusan HBA verbatim. Tak tulis kode. Dokumen saja.

## Putusan HBA

Operasional dibuka penuh di jalur publik agar bisa kerja dari mana saja tanpa Tailscale.
Konfigurasi tetap hanya via Tailscale, untuk sementara tiga item: setting dinamis
(`/api/settings`), ubah profil perusahaan sendiri (`/api/company-profile`), dan ubah
nilai otoritas kait (`/api/link-authority`). Daftar konfigurasi akan bertambah
seiring waktu karena HBA tidak hapal semuanya.

## Prinsip pertumbuhan yang disetujui HBA

Contoh tambahan yang HBA sebut sebagai konfigurasi lokal: export DB, penambahan
role, penambahan pekerja. Artinya setiap kemampuan baru yang bersifat fondasi
(ekspor data mentah, ubah struktur peran, kelola pengguna internal) otomatis
masuk sisi Tailscale, bukan publik, sampai HBA menyatakan lain per item.

## Klarifikasi peran

Sistem hari ini hanya punya peran Admin, Manager, Sales, Coordinator, Technician,
Finance, Kasir — tidak ada peran super-admin tersendiri. Untuk putusan ini,
Admin dianggap sebagai super-admin. Pembuatan peran super-admin baru butuh
keputusan bisnis tersendiri dan tidak diputuskan di sini.

## Kondisi yang diverifikasi sebelum putusan

Pintu publik saat ini hanya melayani status, login/logout/profil sesi, dua alamat
Google, serta alamat pelanggan dan penitipan klaim. Seluruh kerja operasional
(perusahaan, kontak, unit, SR, WO, visit, laporan, approval, material, ringkasan,
riwayat, pengingat, antrean penitipan beserta kait/tolak/balas, QR) masih ditolak
di pintu publik dan hanya dilayani pintu admin. Ketiga alamat konfigurasi di atas
sudah Admin-only (sesi Admin + workspace valid). Buka penuh nanti tetap mewajibkan
login sesi, bukan tanpa login, kecuali penitipan klaim yang memang publik.

## Batas

Record ini tak membuka pintu publik dan tak menulis kode/skema/migrasi. Pembukaan
allowlist publik butuh otorisasi implementasi terpisah. Yang dimaksud HBA dengan
"edit aplikasi" belum dirinci — perlu dijelaskan HBA (ubah apa) sebelum masuk
klasifikasi.

## Langkah berikut termurah

Minta otorisasi implementasi satu kalimat dari HBA untuk perluas allowlist publik
ke operasional, lalu kerjakan sebagai perubahan allowlist tanpa ubah logika domain,
plus verifikasi pintu publik vs admin per verb.

*End of decision record.*
