# Audit Register — CD-03 Materialization (Single Company Master)

Status dokumen: register materialisasi (fakta pencatatan, bukan keputusan baru).
`docs/90-AUDIT/10-CONSISTENCY-REGISTER.md` tidak diubah.

## Pencatatan

1. HUMAN confirmation: CD-03 direvisi eksplisit dan dinyatakan LOCKED; otorisasi
   materialisasi diberikan pada Build Mode.
2. Materialisasi: `docs/10-DECISIONS/CD-03-business-master.md`, status LOCKED.
3. Company Master sebagai canonical identity (satu identitas, bukan giant table).
4. Prospect/Customer/Vendor sebagai business roles (bukan tiga master terpisah).
5. Contact/PIC sebagai entity 1-N terhadap Company (multiple, peran, utama,
   histori, akses future); RBAC detail OPEN/FUTURE.
6. Supersede: model dua identity/list Customer–Vendor digantikan satu Company
   identity + role; kedua model tidak dipertahankan bersamaan.
7. CD-04 (HPP / Operational Costing) unchanged — tidak didefinisikan ulang
   menjadi price history; tidak ada aturan PPN yang ditambahkan.
8. CD-05 (Sales / Quotation / Order) unchanged — tidak diganti atau dinomori ulang.
9. CD-06 (Acquisition Price / Vendor Offer / Price Reference) masih
   PREVIEW / NOT LOCKED.
10. Code change: NO.
11. Database change: NO.
12. Schema change: NO.
13. Migration: NO.
14. TASK implementation: NO.
15. Governance STOP → REPORT → HUMAN tetap berlaku bila ditemukan konflik
    dengan keputusan LOCKED.

## CD-06 Preview — kebutuhan tercatat (bukan keputusan)

* Price treatment 3-state (koreksi HUMAN): `+ PPN`, `Termasuk PPN`,
  `NET / Tanpa PPN`. `NET / Tanpa PPN` ≠ `EXCL_PPN` — perlakuan harga berbeda.
* Contoh kebutuhan quotation: `Rp10.000 + Rp1.100 = Rp11.100` (detailed:
  base + PPN = final) dan input harga final langsung — tanpa mengunci 1-field
  vs 3-field; keputusan UI milik HUMAN. `price_treatment` dievaluasi sebagai
  single-select mutually-exclusive (PROPOSED, bukan locked).
* Vendor Offer (quotation/penawaran/price list/komunikasi vendor) dibedakan dari
  Actual Acquisition (yang benar-benar dibeli); keduanya membawa tanggal,
  vendor, item, harga, treatment (currency/unit/quantity bila relevan) —
  konseptual, tanpa schema/database.
* Konteks: `Company Master → Vendor Role → Offer/Acquisition History`;
  `Item → Price History`; equipment/service sebagai konteks material —
  konseptual, tanpa schema.
* Issuing Company / dua perusahaan (PKP + Non-PKP): architectural consideration
  OPEN/PROPOSED — tidak diasumsikan identik dengan Customer/Vendor Company;
  bukan tax-engine requirement.
* Latest-5 vendor offers: PROPOSED / HUMAN CONFIRMATION REQUIRED.
  Visibility per role (Admin/Manager/Sales/Purchasing/Technician/Customer-PIC):
  OPEN / PROPOSED — RBAC tidak dikunci.
* Batasan: tanpa tax engine, tanpa tax ledger/reporting, tanpa hardcoded tarif
  PPN, tanpa konversi otomatis antar treatment, tanpa jurnal PPN, tanpa
  FIFO/Average/valuasi/COGS, tanpa rekomendasi harga otomatis. Harga asli +
  basisnya harus tetap diketahui agar perbandingan tidak misleading; formula
  perbandingan tidak didesain kini.
* Inventory boundary: Inventory tetap INSIDE CD-01; CRM Phase 1 hanya
  operational reference; Accurate 5 tetap existing-system authority
  where applicable, bukan dependensi permanen.
