# Audit Register — CD-05 Materialization (Sales Transaction & Quotation)

Status dokumen: register materialisasi (fakta pencatatan, bukan keputusan baru).
Register audit sebelumnya tidak diubah.

## Pencatatan

1. HUMAN confirmation: "HUMAN CONFIRM — LOCK CD-05" atas rekonsiliasi final
   (Q1–Q5 + Q-AUTO-CLOSE=(a)).
2. Materialisasi: `docs/10-DECISIONS/CD-05-sales-transaction-quotation.md`,
   status LOCKED (`Decision ID: CD-05 / Status: LOCKED / Authority: HUMAN /
   Mode: DESIGN ONLY`).
3. Isi terkunci: konversi parsial 1QT→N SO; fulfillment parsial 1SO→N
   (non-mutasi, non-reservasi, SoR Accurate 5); SO standalone; status
   PARTIALLY_CONVERTED; model CLOSED dua jalur (otomatis COMPLETED saat
   semua item terkonversi — tanpa tunggu fulfillment; manual via
   request+alasan+approval); terminal tanpa REVOKED; revisi bernomor-sama
   immutable; boundary akuntansi/pricing/PPN/numbering/audit/workspace.
4. Reconciliation sebelumnya: `CD-05: READY FOR HUMAN LOCK` (CODE/SCHEMA/
   MIGRATION/TASK = 0).
5. Q-AUTO-CLOSE=(a): auto-close saat semua item terkonversi ke SO.
6. Code: 0. Schema: 0. Migration: 0. Task: 0.
7. Konsistensi: CD-01–CD-08 CONSISTENT (tidak ada yang diubah).
8. Governance STOP → REPORT → HUMAN tetap berlaku.
