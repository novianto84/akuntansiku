# CD-04 — Operational Acquisition Price & Material Usage Boundary

```text
Decision ID: CD-04
Status: LOCKED
Authority: HUMAN
Mode: DESIGN ONLY
```

Sumber: proposal final CD-04 (D-04A/C/E + H-CD04-1/2 + H-CLAR/H-AGG) yang
dinyatakan ACCEPT oleh HUMAN.
Sifat dokumen: transkripsi keputusan HUMAN. Tanpa business rule baru, tanpa
perubahan makna.
Kode, schema, database, dan analisis terdahulu tetap **reference/evidence**.

## R1 — Acquisition Price (LOCKED)

CRM mencatat **Harga Perolehan Aktual** per item sebagai operational reference.

Harga perolehan ≠ book value ≠ valuation.

Mencakup: Item; harga perolehan; quantity yang relevan; vendor/provenance
sesuai kebutuhan (mengikuti aturan CD-06/CD-08); hubungan dengan acquisition.

## R2 — WO Material (LOCKED)

Material pada WO dicatat sebagai:

> **Item + Quantity + Harga Perolehan per Unit**

Contoh:

```text
Bearing SKF 6312
Qty: 2 pcs
Harga Perolehan: Rp900.000/pcs
```

Tidak ada requirement untuk menghitung `Quantity × Unit Price`.
Tidak ada requirement total material cost. Bukan jurnal accounting.

## R3 — Aggregate (LOCKED)

Tidak ada aggregate/summed stock value pada fase ini.

Status: **DEFERRED, bukan permanent prohibition** terhadap sistem
Accounting/Inventory masa depan.

## R4 — Costing (LOCKED)

Costing method: **DEFERRED / NEUTRAL**.

Tidak ada requirement: FIFO; Average Cost; HPP; COGS; valuation;
costing engine.

## R5 — Accounting Boundary (LOCKED)

Tidak ada: Journal; GL; COGS posting; Tax engine; Financial closing;
Accounting valuation.

## Vendor Offer Boundary

Vendor Offer (Harga Penawaran) ≠ Acquisition (Harga Perolehan Aktual).
Keduanya tidak otomatis identik. Konsisten dengan CD-06.

## Provenance

Prinsip provenance CD-06/CD-08 dipertahankan (vendor, item, harga, basis,
tanggal, sumber, versi; immutable; shared sesuai policy). Tanpa business
rule provenance baru.

## Terminologi

Gunakan: Harga Penawaran Vendor; Harga Perolehan; Harga Perolehan per Unit.
Hindari "Acquisition Cost" dan "Material Cost" sebagai istilah utama bila
berpotensi dibaca sebagai accounting costing.

## Non-Goals (bukan bagian CD-04)

Landed cost; weighted average; valuation layer; cost allocation; material
costing engine; automatic acquisition calculation; automatic COGS;
accounting cost; book value.

## Cross-Decision Consistency (saat lock)

```text
CD-01: CONSISTENT | CD-03: CONSISTENT | CD-05: CONSISTENT
CD-06: CONSISTENT | CD-07: CONSISTENT | CD-08: CONSISTENT
```

## Governance

> **A LOCKED decision may not be changed, weakened, expanded, or reinterpreted
> by AI Manager, AI Programmer, or AI Auditor without explicit HUMAN authorization.**

Konflik dengan keputusan LOCKED:

> **STOP → REPORT → HUMAN**
