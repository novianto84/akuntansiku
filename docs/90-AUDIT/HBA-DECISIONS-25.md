# HBA DECISION RECORD — operasional publik login-wajib, setting lokal (2026-10-16)

```text
Record ID:      HBA-DECISIONS-25
Date:           2026-10-16
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-16 via chat
Classification: Audit record. NOT a canonical specification document.
Implementation: Change implemented under this authorization (server allowlist + tests).
```

> Rekaman putusan HBA verbatim. Dokumen jejak, bukan spesifikasi.

## Putusan HBA

Verbatim: "saya otoritaskan bahwa operasional dibuka di publik dengan login wajib kecuali alamat setting atau konfigurasi tetap lokal".

## Eksekusi

File: crm/app/server.py — PUBLIC_PATH_PREFIXES tambah operasional (company/contacts/unit/components/sr/wo/reporting/history/material/visits/intakes/outstanding/reminders) + collection root exact. Guard: roles + pic-link tetap ADMIN-only. Setting fondasi tetap ADMIN-only: /api/settings, /api/company-profile, /api/link-authority.

Handler tetap _require_auth FIRST — allowlist putuskan routing (404 vs dispatch), bukan auth. Tanpa token operasional = 401, bukan data.

Tes: crm/tests/test_doors.py selaras HBA-25. 69 tes OK (test_doors + test_customer_wp08).

Live pasca-restart: publik 8010 operasional 401 (company/unit/wo/outstanding/unit-QR), setting 404 (settings/company-profile/link-authority). UI 8092 root 200, /api/company 401, /api/settings 404. Publik crm.benshi.my.id 200.

## Batas

Tanpa anonim baru. Tanpa harga di portal. Tanpa ekspor DB / kelola peran di publik. Role attach/detach + pic-link tetap admin.

## Langkah berikut termurah

Login di crm.benshi.my.id, buka Portal Unit (ketik kode QR), verifikasi kolom QR di Pelanggan & PIC kini terisi lewat publik.

*End of decision record.*
