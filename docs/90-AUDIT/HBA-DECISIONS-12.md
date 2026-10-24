# HBA DECISION RECORD — Unit Portal login & kontak (2026-10-08)

```text
Record ID:      HBA-DECISIONS-12
Date:           2026-10-08
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decision as stated by HBA in group chat 2026-10-08
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record. Execution/materialization is a separate governed step.
```

> This record captures the HBA statement in session 2026-10-08. It does not itself
> edit any canonical specification document or authorize implementation.

---

## Decision (verbatim intent)

**Unit Portal: login hanya via Google; minta input nama, perusahaan, nomor telepon;
email otomatis dari Google sign-up.**

HBA states: "unit portal itu saya mau login hanya via google, dan diminta input
nama, perusahaan, dan nomor teleponnya, serta email (otomatis dari sign up googlenya kan)"

Reading:
- Login Unit Portal = Google-only (konsisten dengan portal decisions HBA-DECISIONS-08/09).
- Setelah login Google, pengguna diminta melengkapi: nama, perusahaan, nomor telepon.
- Email = otomatis dari akun Google (tidak diketik manual).
- Field "perusahaan" adalah tambahan eksplisit HBA dibanding draft amendment
  (yang hanya menyebut nama + telepon).

## Boundary

- This record modifies no canonical document, changes no document status,
  creates no business rule beyond the HBA statement above.
- Canonical materialization (mencatat tier Unit Portal + kontak ke IS-06/kanonik,
  menyelaraskan IS-06 L-28) is a separate explicitly-scoped step — NOT done by this record.
- Implementation (form, penyimpanan kontak, validasi) requires separate authorization.

## Cheapest next step

Minta otorisasi materialisasi aditif Unit Portal + kontak ke kanonik,
lalu otorisasi implementasi form-nya.

*End of decision record.*
