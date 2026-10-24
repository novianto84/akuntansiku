# HBA DECISION RECORD — Aturan draft-WO dikunci: satu draft aktif per user per WO, cap 10, rekam setelah approve (2026-10-09)

```text
Record ID:      HBA-DECISIONS-14
Date:           2026-10-09
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decision as stated by HBA in group chat 2026-10-09
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record. Execution is a separate governed step, AUTHORIZED below.
```

> This record captures the HBA statements in session 2026-10-09. It does not itself
> edit any canonical specification document or write any code.

---

## Decisions (verbatim intent)

**HBA states: "kunci, dan eksekusi"** — atas penjelasan draft vs WO yang HBA sampaikan
di sesi yang sama.

**HBA explanation (basis kunci, diringkas tanpa mengubah maksud):**
satu WO cukup satu draft di user; untuk apa user membuat draft berbeda-beda untuk
satu WO. Sangat jarang dua orang submit bersamaan; biasanya hanya satu orang yang
ditugaskan mengisi. Limit 10 adalah bagian monitoring — tanpa limit draft jadi tempat
sampah yang tidak ditengok. Atas dasar operasional yang baik, WO dibuat dan harus
tertutup secepatnya, bukan digantung. Merekam masing-masing draft akan kacau;
lebih baik merekam setelah di-approve.

## Reading (LOCKED)

- Satu WO = satu draft aktif per user. User tidak membuat beberapa draft berbeda
  untuk satu WO yang sama.
- Penugasan normal = satu orang pengisi per WO; kasus dua orang submit bersamaan
  adalah perkecualian langka, bukan pola yang didesain.
- Cap 10 draft per user DIPERTAHANKAN sebagai alat monitoring kebersihan, bukan
  kuota kerja — supaya draft tidak jadi tempat sampah yang tidak ditengok.
- WO harus tertutup secepatnya, bukan digantung sebagai draft menumpuk.
- Yang direkam resmi = versi yang sudah di-approve; setiap coretan draft per
  user tidak direkam satu per satu.

Supersession note: bacaan ini memurnikan F-20. Aturan lama "competing DRAFTs coexist"
(HBA-DECISIONS-05 §1, paket §11A) untuk satu user satu WO diganti satu-aktif;
cap 10 personal, tanpa expiry, dan draft pesaing antar user tidak saling membatalkan
tetap berlaku kecuali diatur ulang. R-26 satu-pending/WO yang dulu berkonflik
dengan banyak-draft kini selaras dengan satu-aktif ini.

## Boundary

- This record modifies no canonical document, changes no document status,
  creates no business rule beyond the HBA statements above.
- Canonical materialization (paket F-20 decision-sheet + spek korektif atas teks
  stale yang dioverride) and any code/schema/migration are separate
  explicitly-scoped steps.
- Execution authorized below proceeds only through the governed path
  (`.opencode/bin/opencode-governed run --agent mitrasp-manager`) with its own evidence.

## Cheapest next step

Perbarui decision-sheet paket F-20 dari §Reading di atas, lalu corrective spec pass
atas teks stale-nya — tanpa build baru sampai itu selesai.

*End of decision record.*
