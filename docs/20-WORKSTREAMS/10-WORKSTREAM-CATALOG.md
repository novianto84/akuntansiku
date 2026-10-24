# Workstream Catalog (Observasi, PROPOSED)

Status dokumen: PROPOSED (dokumentasi saja, bukan LOCKED, bukan keputusan bisnis).
Sumber: observasi route `/api/*` di `app.py` + kutipan `docs/accurate5-gap-akuntansiku.md`.
Catatan: daftar ini mencatat keberadaan, bukan menyetujui skop, prioritas, atau desain.

## 1. Metode pencatatan

- Setiap baris di bawah hanya menyatakan "teramati di repo" atau "tercatat di gap doc".
- Kolom Status selalu PROPOSED pada tahap ini.
- Tidak ada TASK-001 yang dibuat dari katalog ini.

## 2. Katalog turunan observasi

| ID observasi | Area (label deskriptif saja) | Bukti di repo | Status |
|---|---|---|---|
| WS-OBS-01 | Master: COA / akun | `GET /api/coa` teramati di `app.py`; gap doc mencatat selisih hierarki GLACCNT vs flat | PROPOSED |
| WS-OBS-02 | Master: gudang, item, kategori/grup, satuan | `GET /api/warehouses`, `/api/items`, `/api/categories`, `/api/groups` teramati; spec ITEM/WAREHS sebagai acuan | PROPOSED |
| WS-OBS-03 | Master: customer, vendor, kontak | `GET /api/customers`, `/api/vendors` teramati; spec PERSONDATA/CONTACT sebagai acuan | PROPOSED |
| WS-OBS-04 | Penjualan: quotation, sales order, delivery, invoice/retur | `GET /api/quotations`, `/api/sales-orders`, `/api/deliveries`, `/api/sales`, `/api/returns` teramati; spec QUOTATION/SO/ARINV sebagai acuan | PROPOSED |
| WS-OBS-05 | Pembelian: requisition, PO, receive, invoice/retur | `GET /api/requisitions`, `/api/purchase-orders`, `/api/receives`, `/api/purchases` teramati; spec REQUISITION/PO/APINV sebagai acuan | PROPOSED |
| WS-OBS-06 | Kas/Bank: payment, giro, DP, rekonsiliasi, buku bank | `GET /api/payments`, `/api/giros`, `/api/sales-dp`, `/api/purchase-dp`, `/api/reconcile`, `/api/bank-book` teramati | PROPOSED |
| WS-OBS-07 | Buku besar: jurnal, ledger, laporan keuangan | `GET /api/journals`, `/api/ledger`, `/api/reports/trial-balance`, `/api/reports/profit-loss`, `/api/reports/balance-sheet`, `/api/reports/cash-flow` teramati | PROPOSED |
| WS-OBS-08 | Persediaan: stok, opname, transfer, adjustment, kartu stok | `GET /api/stock`, `/api/stock-card`, `/api/stock-adjustments` teramati; spec ITEMADJ/STOCKOPNAME sebagai acuan | PROPOSED |
| WS-OBS-09 | Proyek, RMA, aset tetap, approval | `GET /api/projects`, `/api/rmas`, `/api/assets`, `/api/approvals` teramati; gap doc P1 mencatat kesenjangan | PROPOSED |
| WS-OBS-10 | Pendukung: pajak, cabang, salesman, karyawan/absensi, settings, audit log | `GET /api/taxes`, `/api/branches`, `/api/salespersons`, `/api/employees`, `/api/attendance`, `/api/settings`, `/api/activity` teramati | PROPOSED |

## 3. Kutipan gap doc (tanpa promosi status)

- Gap doc memakai label P0/P1/P2. Label tersebut dikutip apa adanya sebagai isi gap doc, bukan sebagai keputusan prioritas yang di-LOCKED oleh materialisasi ini.
- Selisih field yang dicatat gap doc (contoh: FREIGHT, TAXINCLUSIVE, multi-tax, SHIPVIA, DP-account, overpay, nomor faktur pajak) tetap PROPOSED.

## 4. Fakta historis yang dikutip (tanpa perubahan)

- Commit `137c6d5`: "Metode HPP jadi setting global perusahaan, berlaku semua item, terkunci setelah transaksi". Dikutip sebagai fakta historis. Materialisasi ini tidak mengubah, menafsir ulang, atau mengunci ulang fakta tersebut.

## 5. Yang TIDAK ada di dokumen ini

- Tidak ada penomoran TASK (termasuk TASK-001).
- Tidak ada urutan eksekusi.
- Tidak ada keputusan skop in/out, tidak ada keputusan desain, tidak ada estimasi.
