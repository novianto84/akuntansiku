# Audit Register — CD-09 Materialization (Purchasing Transaction Boundary)

Status dokumen: register materialisasi (fakta pencatatan, bukan keputusan baru).
Register audit sebelumnya tidak diubah.

## Pencatatan

1. HUMAN confirmation: ACCEPT atas PROPOSED CD-09 (Q1–Q18 discovery);
   batasan: Inventory Handoff hanya prinsip (receiving sah → input stok
   operasional); detail warehouse/location/movement/adjustment/reservation/
   transfer/lifecycle tidak dikunci.
2. Materialisasi: `docs/10-DECISIONS/CD-09-purchasing-transaction-boundary.md`,
   status LOCKED (`Decision ID: CD-09 / Status: LOCKED / Authority: HUMAN /
   Mode: DESIGN ONLY`).
3. Isi terkunci: PR opsional + inisiator + darurat; PO wajib + bebas offer +
   lifecycle; receiving tersendiri + parsial + outstanding + terima-tolak;
   acquisition saat receive+harga (PO dulu, koreksi aktual berversi);
   cancel per dokumen; koreksi berversi; ownership workspace; handoff prinsip;
   boundary akuntansi; non-goals; deferred.
4. Code: 0. Schema: 0. Migration: 0. Task: 0.
5. Konsistensi: CD-01/03/04/05/06/07/08 CONSISTENT (tidak ada yang diubah).
6. Governance STOP → REPORT → HUMAN tetap berlaku.
