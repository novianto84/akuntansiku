# HBA DECISION RECORD — Setuju IS-06 v1.2 + IS-03 v1.2, tutup U1, monitor gagal diakui (2026-10-11)

```text
Record ID:      HBA-DECISIONS-15
Date:           2026-10-11
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decision as stated by HBA in chat 2026-10-11
Classification: Audit record. NOT a canonical specification document.
Implementation: No code/schema/migration/DB written by this record.
```

> Rekaman ini menangkap pernyataan HBA di chat 2026-10-11. Tidak mengedit dokumen kanonik, tidak menulis kode.

---

## Keputusan HBA (inti)

HBA states: "Ya catat. Lalu saya setuju IS-06 dan IS-03. Run U1."

Bacaan:

- HBA setuju IS-06 v1.2 dan IS-03 v1.2 sebagai selaras HBA-DECISIONS-13.
- U1 `ops-unitportal-tier-20261010` ditutup sebagai selesai via audit manager (isi sudah benar, gerbang worker gagal template envelope).
- Kegagalan monitor diakui dan wajib diperbaiki.

## Kondisi terverifikasi (sistem nyata)

- IS-06 `docs/40-SPECIFICATION/IS-06-customer-projection-portal.md` v1.2, SHA kini `82622656fba3cdb764ac14da25929fc0f646e47a65245d200db6c534bd40ba90` (sebelum `87245a66c07fd8ef2d846f8d2d58ed3c0dbeb69550e4ad2b6774bf77a4ef807a`). Tiga tier eksplisit §6 + L-28 baru, wording lama retained sebagai SUPERSEDED.
- IS-03 `docs/40-SPECIFICATION/IS-03-access-identity-permission.md` v1.2, SHA kini `5cebf8d73296fbc41cde67752db6064a0b1f7c7ec52947ecf7581f6ea8e8fd14` (sebelum `069eac9820d28f5a3e8595db1e0c5ef49eaaf4b76ea29db2373e50c12d002448`). V-4 tiga tier, wording lama retained sebagai superseded.
- HBA-DECISIONS-13 SHA `b199493d92839cfebfde3ade141421a610172f9dd05c5cd4366356406702483f`.
- Ledger terakhir fase ini: `ORCH_INVOCATION_BEGIN f1d0e333956f-U1-R1 2026-10-10T20:31:55Z`, tanpa `ORCH_RESULT_GATE` susulan. `invocations.jsonl` hanya `da608258d140-U1-1 REJECTED_ENVELOPE`. Nol worker hidup.
- Nol aturan bisnis baru. Nol kode/skema/migrasi/DB. Hanya dua file otorisasi berubah.

## Kegagalan monitor (diakui)

Monitor per jam `f8818f2d7983` ada tapi buta: nilai dari `git diff --stat` kosong karena `docs/` untracked, simpulkan "IS-06 + IS-03 untouched" padahal SHA berubah dan isi tiga tier ada. Lakukan relaunch buta plan sama, timeout 420 detik, tanpa hasil. Hermes baru cek setelah HBA minta. Salah Hermes, bukan salah substrate.

Perbaikan pasang 2026-10-11:

- Prompt monitor tulis ulang: nilai dari sha256 vs `sha_before.txt` + grep tiga tier + SUPERSEDED, larang relaunch buta bila file sudah benar, lapor siap-HBA-approval + SHA baru.
- Aturan baru: `NO_RESULT` / `REJECTED_ENVELOPE` dua kali beruntun = audit manager, bukan retry buta ketiga.
- Tick berikut 04:34 WIB.

## Penutup U1

U1 dinyatakan COMPLETED-BY-MANAGER-AUDIT atas persetujuan HBA ini. Bukti sah = SHA + grep isi + record ini. Retry worker untuk materi sama tidak perlu. Sisa gerbang (`NO_RESULT`, envelope template audit-vs-write) dicatat sebagai utang template, bukan blokir materi.

## Batas

- Record ini tidak mengunci IS-06 (IS-06 tetap DRAFT perlu independent review). IS-03 tetap LOCKED dengan OPEN items.
- Kaki dua HBA-DECISIONS-13 (form kontak + naik-kelas PIC) belum jalan, perlu otorisasi eksekusi eksplisit terpisah.
- Tanpa coding/schema/migration tanpa perintah eksekusi eksplisit.

## Langkah berikut termurah

Otorisasi kaki kontak via governed path, atau stop dan biarkan portal materi DRAFT.

*End of decision record.*
