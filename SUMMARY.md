# ERP-MSP — Ringkasan Proyek

## Identitas Aplikasi
- **Nama**: ERP-MSP (Enterprise Resource Planning - Micro Small Business)
- **Referensi**: Accurate Online
- **Stack**: Python 3.13 + SQLite + Vanilla JS SPA
- **Akses**: `http://192.168.30.12:8000` (lokal) / `http://100.72.199.61:8000` (Tailscale)
- **GitHub**: `novianto84/akuntansiku`
- **Container**: `erp-msp` di NUC anto

---

## Arsitektur

```
┌─────────────────────────────────────────────────┐
│                    BROWSER                      │
│  public/index.html + public/app.js + styles.css │
│              (Single Page Application)           │
└──────────────────────┬──────────────────────────┘
                       │ HTTP API
┌──────────────────────▼──────────────────────────┐
│              app.py (Python stdlib)              │
│  - HTTP Server (port 8000)                      │
│  - REST API endpoints                           │
│  - SQLite with WAL mode                         │
│  - Auto-backup (daily 02:00)                    │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│         database.db (SQLite, ~50+ tables)        │
│  - Master data (accounts, customers, vendors)   │
│  - Transactions (invoices, orders, payments)    │
│  - Inventory, Assets, HRD                       │
│  - Document sequences, approvals, reconciliations│
└─────────────────────────────────────────────────┘
```

---

## Fitur yang Sudah Dibangun

### 1. Modul Master

| Master | Deskripsi |
|--------|-----------|
| **Akun Perkiraan** | COA lengkap, 5 level, saldo otomatis |
| **Customer** | Kode, nama, limit kredit, terms pembayaran |
| **Vendor** | Kode, nama, email, akun payable |
| **Item/Barang** | SKU, satuan, harga, stok minimum |
| **Gudang** | Multi-gudang, stok per gudang |
| **Karyawan** | Nama, jabatan, gaji pokok, toleransi keterlambatan |
| **Akun Pajak** | PPN11, PPN0, NONPPN dengan rate |

### 2. Modul Penjualan

| Fitur | Deskripsi |
|-------|-----------|
| **Penawaran (Quotation)** | Buat & close penawaran |
| **Sales Order (SO)** | Pesanan penjualan, link ke quotation |
| **Delivery Order (DO)** | Pengiriman barang |
| **Faktur Penjualan** | Invoice otomatis, komisi salesman |
| **Credit Note (CN)** | Nota kredit terpisah dari retur |
| **Pembayaran Piutang** | Kas masuk, allocation per invoice |
| **Retur Penjualan** | Retur barang |

### 3. Modul Pembelian

| Fitur | Deskripsi |
|-------|-----------|
| **Purchase Requisition** | Permintaan pembelian |
| **Purchase Order (PO)** | Pesanan pembelian |
| **Receive (Penerimaan)** | Penerimaan barang |
| **Faktur Pembelian** | Invoice vendor |
| **Debit Note (DN)** | Nota debet terpisah dari retur |
| **Pembayaran Hutang** | Kas keluar, allocation per invoice |
| **Retur Pembelian** | Retur ke vendor |

### 4. Modul Keuangan

| Fitur | Deskripsi |
|-------|-----------|
| **Kas & Bank** | Multi akun kas, saldo otomatis |
| **Jurnal Umum** | Multi-line journal entries |
| **Jurnal Otomatis** | Auto-generated dari transaksi |
| **Pencocokan Bank (Reconciliation)** | Match transaksi kas dengan bank |

### 5. Modul Persediaan

| Fitur | Deskripsi |
|-------|-----------|
| **Stok Opname** | Opname fisik + approval |
| **Transfer Gudang** | Transfer antar gudang |
| **Stok Real-time** | Hitung otomatis dari transaksi |

### 6. Modul Aset Tetap

| Fitur | Deskripsi |
|-------|-----------|
| **Register Aset** | Daftar aset tetap |
| **Depresiasi** | Perhitungan otomatis |

### 7. Modul HRD

| Fitur | Deskripsi |
|-------|-----------|
| **Data Karyawan** | Profil, jabatan, gaji |
| **Absensi** | Check-in/out, keterlambatan |
| **Cuti** | Pengajuan & approval cuti |
| **Gaji** | Perhitungan gaji otomatis |

### 8. Modul Laporan

| Laporan | Deskripsi |
|---------|-----------|
| **Laba Rugi** | Omzet - HPP = Laba Bersih |
| **Neraca** | Asset = Liabilitas + Modal |
| **Aging Piutang** | Umur piutang (1-30, 31-60, 61-90, >90 hari) |
| **Aging Hutang** | Umur hutang |
| **Buku Besar** | Mutasi per akun |
| **Penjualan per Periode** | Filter bulan/tahun |
| **Pembelian per Periode** | Filter bulan/tahun |

### 9. Modul Sistem

| Fitur | Deskripsi |
|-------|-----------|
| **Multi User** | admin, finance, gudang, hrd |
| **RBAC** | Role-based access control |
| **Approval (Maker-Checker)** | Transaksi perlu approval |
| **Audit Trail** | Log semua perubahan data |
| **Backup/Restore** | Auto-backup harian, restore manual |
| **Period Lock** | Kunci transaksi per bulan |

### 10. UI/UX

| Fitur | Deskripsi |
|-------|-----------|
| **Glassmorphism Sidebar** | Efek kaca modern |
| **Gradient KPI Cards** | Kartu statistik gradien |
| **Login Modern** | Background gradient ungu |
| **Responsive Design** | Mobile sidebar toggle |
| **Transaction Detail Pages** | Klik invoice → detail lengkap |
| **Form Validation** | Required fields + error messages |
| **Loading States** | Spinner saat proses |
| **Dashboard Charts** | Omzet 6 bulan + piutang/hutang |
| **Export PDF** | Cetak faktur via print dialog |

---

## Database (50+ Tabel)

### Master
`accounts`, `customers`, `vendors`, `items`, `warehouses`, `employees`, `taxes`, `categories`, `brands`, `units`

### Transaksi
`quotations`, `quotation_lines`, `sales_orders`, `sales_order_lines`, `deliveries`, `delivery_lines`, `sales`, `sale_lines`, `sales_returns`, `sales_return_lines`, `credit_notes`, `debit_notes`

### Pembelian
`purchase_requisitions`, `purchase_requisition_lines`, `purchase_orders`, `purchase_order_lines`, `receives`, `receive_lines`, `purchases`, `purchase_lines`, `purchase_returns`, `purchase_return_lines`

### Keuangan
`journals`, `journal_lines`, `payments`, `payment_allocations`, `bank_reconciliations`, `bank_reconciliation_lines`

### Persediaan
`stock_adjustments`, `stock_adjustment_lines`, `stock_transfers`, `stock_transfer_lines`, `inventory_movements`

### Aset
`fixed_assets`, `depreciation_entries`

### HRD
`attendance`, `leave_requests`, `payrolls`, `payroll_lines`

### Sistem
`users`, `approvals`, `reconciliations`, `reconciliation_lines`, `doc_sequences`, `system_settings`, `audit_logs`, `backups`

---

## Infrastruktur

| Komponen | Detail |
|----------|--------|
| **Server** | anto-NUC7i3BNHXF, 8GB RAM |
| **OS** | Ubuntu 26.04 LTS |
| **Docker** | 29.6.2 + Compose 5.3.1 |
| **Container** | `erp-msp` (python:3.13-slim) |
| **Database** | `/opt/akuntansiku/data/database.db` |
| **Tailscale** | `100.72.199.61` (NUC), `100.114.143.66` (laptop) |
| **SSH** | `anto@192.168.30.12` (plink/pscp) |
| **Backup** | Daily 02:00, 14-day retention |

---

## Command Penting

```bash
# Deploy ke NUC
pscp -pw "Pass4life" public\app.js anto@192.168.30.12:/opt/akuntansiku/public/
plink -batch -pw "Pass4life" anto@192.168.30.12 "cd /opt/akuntansiku && docker compose up -d --build"

# SSH ke NUC
plink -batch -pw "Pass4life" anto@192.168.30.12 "docker exec -it erp-msp sh"

# Lihat log
plink -batch -pw "Pass4life" anto@192.168.30.12 "docker logs erp-msp --tail 50"

# Restart container
plink -batch -pw "Pass4life" anto@192.168.30.12 "cd /opt/akuntansiku && docker compose restart"
```

---

## Statistik Kode

| File | Baris | Deskripsi |
|------|-------|-----------|
| `app.py` | ~2270 | Backend Python |
| `public/app.js` | ~1400 | Frontend SPA |
| `public/styles.css` | ~1300 | CSS modern UI |
| `public/index.html` | ~50 | Shell HTML |

---

## Commit History

| Commit | Deskripsi |
|--------|-----------|
| `fb70b7c` | Tahap 1+2 (Critical & Parity) |
| `395e9bd` | UI Redesign (Glassmorphism, Gradients) |
| `311b0f7` | Master sub-menus, detail pages |
| `2d66005` | Transaction detail pages |
| `a6e4167` | Rename: AkuntansiKu → ERP-MSP |
| `2679f5a` | Form validation, mobile responsive |
| `87edfc7` | Credit Note, Debit Note, Export PDF |
| `d0545ea` | Dashboard charts, 6 laporan |

---

## Todo List (Fitur Selanjutnya)

1. ~~Form validation~~ ✅
2. ~~Mobile responsive~~ ✅
3. ~~Credit Note / Debit Note~~ ✅
4. ~~Export PDF~~ ✅
5. ~~Better reporting~~ ✅
6. ~~Dashboard charts~~ ✅
7. Inventory adjustment (opname) —待実装
8. Multi-print batch invoice —待実装
9. Multi-currency support —待実装
10. Multi-company support —待実装
