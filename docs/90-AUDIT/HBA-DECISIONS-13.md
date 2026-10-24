# HBA DECISION RECORD — Tiga tingkat akses LOCK + eksekusi diotorisasi (2026-10-08)

```text
Record ID:      HBA-DECISIONS-13
Date:           2026-10-08
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decision as stated by HBA in group chat 2026-10-08
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record. Execution is a separate governed step, AUTHORIZED below.
```

> This record captures the HBA statement in session 2026-10-08. It does not itself
> edit any canonical specification document.

---

## Decision (verbatim intent)

**Setuju 3 tingkat. LOCK. Eksekusi.**

HBA states: "jadi setuju 3 tingkat. locked. eksekusi"

Reading (building on HBA-DECISIONS-12):
- Tiga tingkat akses DISETUJUI dan DIKUNCI: Internal CRM / Customer Portal / Unit Portal.
- Unit Portal = 1 unit hasil scan QR, read-only, tanpa harga; login Google-only;
  setelah login minta nama + perusahaan + nomor telepon; email otomatis dari Google;
  otomatis naik ke Customer Portal bila email terdaftar sebagai PIC (sesuai draft amendment).
- Kontak + arsitektur menempel di backend CRM (bagian dari paket amendment) ikut dikunci.
- Eksekusi DIOTORISASI: materialisasi aditif ke kanonik (termasuk penyelarasan IS-06 L-28)
  + implementasi form/penyimpanan kontak lewat governed path.

Supersession note: IS-06 L-28 ("no third external scope") disalip oleh keputusan ini
untuk Unit Portal; penyelarasan wording-nya bagian dari eksekusi yang diotorisasi.
Model dua tingkat sebelumnya SUPERSEDED untuk scope ini.

## Boundary

- This record modifies no canonical document and writes no code.
- Materialization + implementation are authorized but executed as separate governed steps
  with their own evidence.

## Cheapest next step

Jalankan paket eksekusi: (1) materialisasi aditif Unit Portal ke kanonik,
(2) implementasi form kontak + aturan naik-kelas PIC, masing-masing via governed path.

*End of decision record.*
