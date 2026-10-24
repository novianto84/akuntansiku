# Audit Register — CD-06 Materialization (Vendor Offer & Acquisition Price Reference)

Status dokumen: register materialisasi (fakta pencatatan, bukan keputusan baru).
Register audit sebelumnya tidak diubah.

## Pencatatan

1. HUMAN confirmation: discovery Q1–Q10 + Q-A–Q-D, finalisasi Q8 (Dynamic
   Role-Based Visibility), dan konfirmasi LOCK CD-06.
2. Materialisasi: `docs/10-DECISIONS/CD-06-vendor-offer-price.md`,
   status LOCKED (`Decision ID: CD-06 / Status: LOCKED / Authority: HUMAN /
   Mode: DESIGN ONLY`).
3. Isi terkunci: model satu-offer-tiga-representasi; basis EXCLUDE/INCLUDE/NET
   (NET ≠ EXCLUDE); single input + derived; rumus generik tanpa locked rate;
   offer vs acquisition terpisah; immutable berversi; lifecycle 3 status;
   provenance + atribut lengkap; perbandingan Final tanpa otomasi; referensi
   quotation tanpa penetapan harga otomatis; Q8 visibility dinamis per role
   via Admin (bukan field-hiding, bukan selector workspace, bukan batasan
   Vendor Master global).
4. Boundary: tanpa tax/accounting/costing engine; tanpa hardcoded tarif;
   tanpa konversi otomatis; tanpa FIFO/Average/valuasi/COGS/HPP; tanpa
   rekomendasi harga; tanpa schema.
5. Code: 0. Schema: 0. Migration: 0. Task: 0.
6. Konsistensi: CD-01–CD-08 CONSISTENT (tidak ada yang diubah; Q1–Q7, Q-A–Q-D,
   CD-01–CD-05, CD-07–CD-08 tidak dibuka kembali).
7. Governance STOP → REPORT → HUMAN tetap berlaku.
