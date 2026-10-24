# Audit Register — CD-04 Materialization (Operational Acquisition Price & Material Usage Boundary)

Status dokumen: register materialisasi (fakta pencatatan, bukan keputusan baru).
Register audit sebelumnya tidak diubah.

## Pencatatan

1. HUMAN confirmation: proposal final CD-04 dinyatakan ACCEPT; APPROVED FOR LOCKING.
2. Materialisasi: `docs/10-DECISIONS/CD-04-operational-acquisition-price.md`,
   status LOCKED (`Decision ID: CD-04 / Status: LOCKED / Authority: HUMAN /
   Mode: DESIGN ONLY`).
3. Isi terkunci: R1 harga perolehan aktual per item (≠ book value/valuation);
   R2 WO Item+Qty+Harga/Unit tanpa Qty×Unit; R3 agregat DEFERRED
   (bukan larangan permanen); R4 costing deferred/neutral; R5 tanpa
   journal/GL/COGS/tax/closing/valuation; offer≠acquisition; provenance
   CD-06/CD-08; terminologi aman; non-goals.
4. Code: 0. Schema: 0. Migration: 0. Task: 0.
5. Konsistensi: CD-01/03/05/06/07/08 CONSISTENT (tidak ada yang diubah).
6. Governance STOP → REPORT → HUMAN tetap berlaku.
