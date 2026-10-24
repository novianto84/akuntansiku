# HBA DECISION RECORD — akui portal existing wajib login + rebuild/uji bukti (2026-10-16)

```text
Record ID:      HBA-DECISIONS-24
Date:           2026-10-16
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-16 via chat
Classification: Audit record. NOT a canonical specification document.
Implementation: No code/schema/migration/DB written by this record.
```

> Rekaman putusan HBA verbatim. Tak tulis kode. Dokumen saja.

## Putusan HBA

Tetap wajib login, akui kode portal unit + perusahaan yang sudah ada sebagai hasil akhir (opsi pertama), lalu rebuild UI dan jalankan tes bukti agar barcode terbuka setelah login.

Putusan chat verbatim: "saya pilih opsi pertama. ayo lakukan" (menjawab briefing opsi akui-existing vs re-scope baru).

## Kondisi yang diverifikasi sebelum/sesudah putusan

Run ops-portal-dual-20261014 berstatus NOT_SUCCESS, Q1 INVALID_OUTPUT hanya karena format evidence bukan array; worker STOP tanpa dispatch karena menilai enam item sudah ada. Cek independen membenarkan: server.py baris 1632 (company) dan 1656 (unit) sudah pakai parts[4] yang benar, layar PortalUnit/PortalCompany sudah ada dan wiring portal-unit + portal-company di App.tsx sudah nyambung, API customerQr/history + tipe narrow sudah ada tanpa harga, tes route wiring sudah ada.

Bukti eksekusi opsi pertama hari ini: UI typecheck OK (tsc -b), build OK (dist/assets index-CfvEVJFP.js 328KB + index-_n-lniCF.css), backend 65 tes OK (tests.test_doors + tests.test_customer_wp08 — mencakup 401 anonim, 200/403 by scope, 400 non-numeric), service crm + crm-ui aktif, lokal :8092 = 200, publik crm.benshi.my.id = 200.

## Batas

Record ini tak mengubah kunci tanpa-anonim IS-06, tak membuka rute anonim, tak tambah harga/lintas skop, tak perluas allowlist. Perluasan allowlist publik tetap butuh otorisasi terpisah (HBA-DECISIONS-23).

## Langkah berikut termurah

Verifikasi manual sekali: login di crm.benshi.my.id lalu buka portal unit + perusahaan via scan/pilih unit; bila ada tampilan tak sesuai, re-scope baru yang presisi.

*End of decision record.*
