# HBA DECISION RECORD — halaman profil ber-URL + QR link + frame logo (2026-10-16)

```text
Record ID:      HBA-DECISIONS-26
Date:           2026-10-16
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-16 via chat
Classification: Audit record. NOT a canonical specification document.
Implementation: UI-only change under this authorization (no migration, no DB, no server.py logic).
```

> Rekaman putusan HBA verbatim. Dokumen jejak, bukan spesifikasi.

## Putusan HBA

Tiap perusahaan dan tiap unit punya halaman profil sendiri ber-URL; barcode berisi link ke halaman itu; di halaman pelanggan ada frame logo + contoh barcode. Tetap wajib login. Logo pakai URL yang sudah ada atau upload baru.

Verbatim lanjutan: "tetap wajib login untuk halaman itu, dan logo pakai URL yang sudah ada atau upload baru."

## Eksekusi

Run governed: ops-profile-url-20261016 (worker t_profile_url_01; file kerja mendarat di tree; verifikasi + penyelesaian kekurangan oleh Hermes langsung karena result orkestrasi belum masuk).

UI (tanpa dep npm baru):
- crm/ui/src/lib/qr.ts (new) — encoder QR mandiri byte-mode ECC-M -> SVG; absoluteRouteUrl(hash) -> URL absolut shareable.
- crm/ui/src/components/QrImage.tsx (new) — render SVG via data-URL <img> + cetak (jendela baru) + unduh SVG.
- App.tsx — hash-route dua arah: #/company/<id>, #/unit/<id>, #/portal-unit[?code=]; sinkron view<->hash (back browser pindah menu; link bisa dibagikan dalam sesi). Login gate tak berubah: tanpa token selalu layar login.
- CompanyScreen.tsx — panel Profil perusahaan: frame logo 160px (img bila URL tersedia, placeholder bila tidak) + QR link halaman itu + cetak/unduh; tiap baris unit: gambar QR kecil link halaman unit + kode teks portal.
- UnitScreen.tsx — panel Profil unit: QR link halaman unit + cetak/unduh.
- PortalUnitScreen.tsx — prefill kode dari hash (initialCode).

Keputusan skema: master `companies` TIDAK punya kolom logo (verifikasi app/company/company.py) — UI baca opsional + placeholder jujur, tanpa fabrikasi URL. Persistensi logo butuh keputusan skema terpisah (migrasi = otorisasi baru). Logo own-company (company_profile.logo, Admin-only) tak dicampur ke master pelanggan.

Bukti: typecheck OK (tsc -b), build OK (dist index-Bi2OS39p.js 340KB, 34 modul), layanan crm+crm-ui aktif, lokal 8092 = 200, publik = 200, root serve bundel baru.

## Batas

Tanpa anonim. Tanpa harga. Tanpa lintas scope. Tanpa perubahan backend/serving/auth/allowlist. Tanpa migrasi/DB/docs. Tanpa dep npm baru.

## Langkah berikut termurah

Login di crm.benshi.my.id, buka Pelanggan & PIC -> pilih perusahaan (lihat frame logo + QR halaman + QR per unit), buka Unit -> pilih unit (lihat QR halaman), uji back browser + salin link hash. Bila persistensi logo disetujui, ajukan otorisasi skema (kolom logo di companies) sebagai fase terpisah.

*End of decision record.*
