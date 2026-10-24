# HBA DECISION RECORD — Panel antre intake dashboard (2026-10-11)

```text
Record ID:      HBA-DECISIONS-18
Date:           2026-10-11
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decision as stated by HBA in chat 2026-10-11
Classification: Audit record. NOT a canonical specification document.
Implementation: Executed (v15 + IntakePanel). See evidence below.
```

> Rekaman tangkap pernyataan HBA verbatim. Tak edit kanonik selain yang diotorisasi.

## Putusan HBA (inti)

- Pengaitan dilakukan sendiri oleh yang berwenang (manual, tak ada auto-approve).
- Customer hanya isi field kosong manual. Tanpa autofill, tanpa dropdown — supaya tak bisa menerka-nerka.
- Satu panel di dashboard berisi antre intake dengan tiga aksi: approve/kait, reply (balas meminta bukti tambahan bila kurang meyakinkan), ignore.
- Balasan dicatat di CRM saja (diputus via clarify 2026-10-11), tanpa email beneran. Customer baca saat login berikut.
- Otoritas kait tak di-hardcode: default Manager, HBA pertimbangkan lebih lanjut (nilainya di `app_settings.link_authority`, tampil di panel).

## Eksekusi (bukti)

- Migrasi v13 `contact_intakes` + `app_settings` (default Manager); v14 `unit_qr_codes` didaftarkan ke registry; v15 `intake_replies` (balasan in-CRM).
- `app/customer/intake.py`: submit PENDING, list/get gated, link manual buka PENDING link, reject retain, reply/list_replies/my_replies.
- `app/server.py`: `POST /api/intake/submit` publik; antre/link/reply/reject/otoritas admin-only; detail sertakan replies.
- UI: `IntakePanel.tsx` di DashboardScreen (Manager/Admin saja). Tombol: Setujui & kaitkan, Balas, Abaikan. Klaim tampil apa adanya.
- Verifikasi: 9 tes intake OK, 32 tes intake+doors OK, typecheck + build UI lolos, 11 cek browser nyata (login, antre, balas, kait) SEMUA LOLOS.

## Batas

- Tanpa Google OAuth nyata (stub), tanpa mekanisme QR hidup (FAIL-CLOSED), tanpa pengirim email.
- Panel tampil hanya untuk Manager/Admin; backend tetap menegakkan otoritas terkonfigurasi.

*End of decision record.*
