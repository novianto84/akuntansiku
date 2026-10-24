# HBA DECISION RECORD — Deploy production, hybrid publication/serving, unit portal belum diputus (2026-10-08)

```text
Record ID:      HBA-DECISIONS-11
Date:           2026-10-08
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decisions as stated by HBA in group chat 2026-10-08
Classification: Audit record. NOT a canonical specification document.
Implementation: No code written by this record. Execution is a separate governed step.
```

> This record captures the HBA statements in session 2026-10-08. It does not itself
> edit any canonical specification document, open any port, or change any deployment.

---

## Decisions (verbatim intent)

1. **Deploy CRM ke production — AUTHORIZED dengan batas lokal + Tailscale-only.**
HBA states: "ya nyalakan crm.benshi.my.id dengan lokal dan tailscale-only".
Reading: subdomain crm.benshi.my.id dinyalakan; backend tetap lokal/Tailscale-only,
hanya app yang terekspos sesuai split keamanan V1 (target NUC).
Eksekusi (baseline bersih, uji, naik) adalah langkah governed terpisah.

2. **Mekanisme publication & serving — HYBRID, LOCK, eksekusi diotorisasi.**
HBA states: "hybrid! lock dan eksekusi."
Reading: O-01/O-02 IS-06 dikunci ke arah hybrid sesuai TADR-12
(live query untuk internal/operasional; snapshot materialized yang dikunci reviewer
untuk Customer dan QR agar yang dilihat pelanggan tetap).
Eksekusi mekanisme snapshot/refresh/cache/drift monitoring lewat governed path.

3. **Amendment Unit Portal — BELUM DIPUTUS.**
HBA states: "amandemen unit portal masih tidak paham saya."
Status tetap OPEN, tidak ada tier baru yang disetujui, tidak ada pencatatan ke kanonik.
Model dua tingkat yang LOCKED (UNIT_SCOPE / COMPANY_SCOPE) tetap berlaku.

## Boundary

- This record modifies no canonical document, changes no document status,
  creates no business rule beyond the HBA statements above.
- Deploy execution, hybrid mechanism implementation, and any Unit Portal tier
  remain separate explicitly-scoped steps.
- IS-06 L-28 (no third external scope) unchanged until HBA decides otherwise.

## Cheapest next step

Siapkan baseline bersih CRM + readiness deploy embedded, lalu naikkan
crm.benshi.my.id dengan batas lokal/Tailscale-only; jalankan paket mekanisme
hybrid lewat governed path; jelaskan ulang Unit Portal sampai HBA bisa pilih.

*End of decision record.*
