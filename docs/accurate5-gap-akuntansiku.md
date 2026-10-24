# Gap Mapping: Accurate 5 Deluxe vs akuntansiku (app.py)

Basis: skema di atas + route app.py (/api/*). DB dummy belum ada transaksi jual/beli sehingga efek jurnal disimpulkan dari FK + Manual Book.

## P0 — Paritas wajib (inti sudah ada, selisih field)
- COA hierarkis (GLACCNT PARENTACCOUNT/INDENTLEVEL/LFT/RGT) vs akuntansiku flat 5-digit → tambah parent/kode bertitik (1000.01).
- Customer+Vendor gabung PERSONDATA(PERSONTYPE) + CONTACT(1-N) vs customers/vendors terpisah → tambah tabel kontak + PERSONTYPE bila ingin impor 1:1.
- Quotation (QUOTATION/QUOTATIONDET: QUOTENO, QUOTEDATE, CASHDISCPC, TAX1/2, FREIGHT, PROCEED/CLOSED, SHIPTO, TEMPLATEID) ≈ /api/quotations — kurang: FREIGHT, TAXINCLUSIVE, multi-tax, TEMPLATEID.
- SO (SONO, ESTSHIPDATE, PONO, FOB, SHIPVIA->SHIPMENT, DP/DPUSED/DPACCOUNT, CHEQUENO/DATE) ≈ /api/sales-orders — kurang: FOB/SHIPVIA/ESTSHIPDATE/DP-account.
- SI/DO gabung (ARINV DELIVERYORDER/GETFROMSO/GETFROMDO + ARINVDET DOID/DOSEQ/SOID/SOSEQ, PPH23AMOUNT, FISCALRATE, TAXFORMNUMBER) ≈ sales_invoices + deliveries — kurang: flag DO-dalam-SI, PPh23, nomor faktur pajak.
- PO (PONO, EXPECTED, FOB, FREIGHTTOCOST, GETFROMREQUEST) ≈ /api/purchase-orders — kurang: FREIGHTTOCOST/FOB/EXPECTED.
- PI merangkap terima (APINV BILL/GETFROMPO, FREIGHTTOVENDOR/SHIPVENDID, INVTAXNO, SSPDATE) ≈ purchase_invoices + receives — kurang: pemisah BILL vs expense lines (APINVDET vs APITMDET).
- Payment: ARPMT (SEQUENCENO, OVERPAY/AROVERPAY, APPLYFROMCREDIT) / APCHEQ (PAYEE, FISCALPMT) ≈ /api/payments — kurang: overpay/kelebihan bayar, alokasi kredit.
- JV (JV/JVDET) ≈ journals — JV dummy ada 364 baris saldo awal; cocok.
- Pajak ganda TAX1/TAX2 + TAXTYPE_IN/OUT + PPN* vs taxes tunggal rate → perlu multi-tax per dokumen.
- Multi-mata uang (CURRENCY, RATE/RATETYPE/FISCALRATE per dokumen) vs akuntansiku IDR-only → P1 bila perlu.
- Cabang/Departemen/Project di semua detail (BRANCHCODEID/DEPTID/PROJECTID) vs branches/departments minim → tambah dimensi.

## P1 — Deluxe (ada sebagian)
- RMA (RMA/RMACOMPONENTUSED/ACTIONACTIVITY) ≈ /api/rmas — cek SN/warranty (SERIALNUMBERS, WARRANTYDATE di ARINVDET).
- Project (PROJECT/PROJECTCOST/ENDING/BUDGET/PAYMENT/SURVEY) ≈ /api/projects — kurang: budget vs actual, survey, price analysis.
- Aset (FIXASSET/FASETTYP/FAFISCAL/FADEPHIS) ≈ /api/assets — kurang: fiskal vs komersial, revaluasi.
- Rekonsiliasi (RECONCILIATION, RECONCILED/RECONCILEID di ARINV/APINV/ARPMT/APCHEQ) ≈ /api/reconcile — cocok, tinggal samakan flag.
- Stock opname/adjust (ITEMADJ/ITADJDET, STOCKOPNAME*) ≈ /api/stock/* — cocok.

## P2 — Skip/tunda (Enterprise/Manufaktur/Pajak lanjut)
- Manufaktur: BOM/WO/WODET/WOEXECUTION/PROD*/MATRLS/MFSHT — akuntansiku tidak punya; tunda.
- SPT/PPh: SPTPPWPB_*, PPN1106/1195, ONLINE_PAJAK — hanya e-Faktur CSV sederhana di akuntansiku.
- Audit: AUDIT/AUDITDET, DELETED_TRANSACTIONS, LOCK_TABLE — akuntansiku punya activity_logs; cukup.
- Serial number: SERIALNUMBERS/SNHISTORY — belum ada; tunda kecuali jual elektronik berseri.
