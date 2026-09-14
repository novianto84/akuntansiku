# RANCANGAN GABUNGAN ERP-MSP + AUDIT PEKERJAAN SAAT INI

Tanggal: 14 Sep 2026. Disusun dari 2 sumber riset yang berhasil dibaca penuh.

## A. Sumber yang dipelajari

1. **riset-spesifikasi-crm-erp-msp.md** (12 bab, ~35KB) — brief teknis CRM→ERP aset, pola Accurate Online + Deluxe, skema PostgreSQL §7, roadmap Fase 0–3. Rekomendasi: jangan bangun ulang akuntansi, sync ke Accurate Online via Open API.
2. **Riset dan rancangan ERP berbasis Accurate.pdf** (749 baris) — rancangan enterprise paling detail: 3 lapisan (CRM pelanggan, field service/asset maintenance, ERP-keuangan), relasi Customer→Site→Asset→WO→Invoice→Payment, 6 fase pembangunan, API list, costing 3-nilai (cost/billable/revenue), approval engine, multi-tenant organization_id.
3. **Arsitektur & Spesifikasi Aplikasi Akuntansi Serupa Accurate Online.pdf** — GAGAL dibaca (butuh OCR, hal. 3–5). Tidak dimasukkan ke rancangan; perlu di-OCR terpisah bila isinya penting.

Kedua riset yang terbaca **sepakat 90%**: relational DB, document-flow pull/convert (Penawaran→Pesanan→Kirim→Faktur→Bayar), audit trail, auto-numbering, RBAC, modular monolith dulu, dan diferensiasi utama = **aset milik pelanggan** (bukan aset tetap milik sendiri seperti di Accurate).

## B. RANCANGAN GABUNGAN (satu acuan final)

### B.1 Visi & prinsip (tidak bisa ditawar)

- Sistem **service-centric**, bukan dagang-centric: rantai wajib `Customer → Site/Lokasi → Customer Asset → Work Order → Material/Jasa → Invoice → Payment`. Setiap WO **wajib terikat 1 aset**.
- Histori aset = read-model dari tabel transaksi (WO + lines + meter + foto), **bukan satu kolom JSON besar**.
- Transaksi posted immutable — koreksi via void/reversal, bukan edit. Master pakai soft-delete. Semua dokumen punya status eksplisit + `created_by/updated_by` + audit log.
- Costing 3 nilai per baris WO: `cost_amount` (HPP/biaya riil), `billable_amount` (yang ditagih), `revenue_amount` — untuk margin per WO/aset/pelanggan/teknisi/kontrak.
- Multi-tenant `organization_id` sejak awal (satu DB, satu schema + enforcement di app layer; RLS bila pindah ke PostgreSQL). Menjawab kebutuhan multi-entitas MSP/PT-PAG.
- Akuntansi: **pertahankan engine double-entry yang sudah ada** (jangan buang), jadikan ia lapisan ledger; modul service menulis jurnal otomatis ke sana. Sync dua arah ke Accurate Online = Fase akhir (opsional), bukan prasyarat.

### B.2 Modul final (menu)

1. Dashboard (pipeline, WO terbuka/terlambat, jadwal maintenance hari ini, piutang jatuh tempo, stok kritis, utilisasi teknisi) + filter cabang/periode/teknisi/jenis aset.
2. CRM: Pelanggan, Kontak PIC, Site/Lokasi, Leads→Opportunity, Aktivitas (call/visit/WA/email), Penawaran.
3. Aset Pelanggan: master + komponen (parent_asset_id) + atribut fleksibel (EAV: asset_attribute_values) + meter reading + garansi + dokumen/foto + timeline + transfer lokasi.
4. Service: Service Request (New→Triage→Scheduled→Converted→Closed) → Work Order (Draft→Scheduled→Dispatched→OnSite→WaitingPart→Completed→Signoff→Invoiced→Closed) + assignment teknisi + checklist/inspeksi + timesheet + foto before/after + tanda tangan.
5. Kontrak & SLA: maintenance_contracts, contract_assets, maintenance_plans (interval hari/jam/meter, auto-create WO, cegah duplikat via unique rule asset+due_date), approval engine configurable (nominal > X, diskon > Y, warranty claim).
6. Penjualan & Pembelian: Quotation→SO→DO→Invoice→Receipt (+DP/giro/retur); PR→PO→GR→PI→Payment. Pola "Ambil/pull" antar dokumen via `source_type/source_id`.
7. Persediaan: multi-gudang/bin, serial/batch, FIFO/Average per item, stock reservation untuk WO, kartu stok, opname.
8. Keuangan: COA, jurnal otomatis dari WO/penjualan/pembelian, AR/AP, kas-bank + rekonsiliasi + auto-match, pajak PPN/PPh21 TER, period lock, laporan (trial balance, L/R, neraca, arus kas, L/R per pelanggan/proyek/aset/WO).
9. Laporan service: response/resolution time, first-time-fix, repeat failure, downtime/aset, PM compliance, biaya per jam operasi, TCO.
10. Pengaturan + Integrasi: user/role/permission matrix, penomoran dokumen, webhook + API key per integrasi (scope, signature, retry, idempotency), import/export CSV.

### B.3 Skema DB target (PostgreSQL, UUID; bila tetap SQLite sementara, kolom yang DITANDAI * adalah tabel BARU yang belum ada di app.py)

Master & tenant: organizations*, branches (ada), users (ada), roles/permissions*, teams*, approval_requests/steps/actions*.
CRM: customers (ada, perlu +type/NPWP/termin/kredit), customer_contacts*, customer_sites*, leads*, lead_activities*, sales_pic (ada salespersons).
Aset*: asset_types*, asset_categories*, customer_assets*, asset_attribute_defs/values*, asset_components (parent_asset_id)*, asset_meter_readings*, asset_transfers*, asset_warranties*, asset_documents*.
Service*: service_requests*, work_orders*, work_order_lines (material/labor/expense/travel)*, work_order_checklist_results*, technician_assignments/timesheets*, customer_signoffs*.
Kontrak*: maintenance_contracts*, contract_assets*, maintenance_plans/plan_tasks*.
Komersial (SUDAH ADA di app.py — pertahankan): sales_quotations(+lines), sales_orders(+lines), delivery_orders(+lines), sales_invoices(+lines), payments+allocations, sales/purchase_DP(+allocations), giros, purchase_requisitions/orders/receives/invoices/returns.
Inventory & accounting (SUDAH ADA — pertahankan): items, item_units, warehouses, inventory_transactions/layers, chart_of_accounts, journal_entries(+lines), taxes, fixed_assets (aset milik sendiri — JANGAN dicampur dengan customer_assets), bank_statements, payroll/employees/attendance/leaves.
Cross-cutting: activity_logs (ada, perlu +entity_type/entity_id/detail JSON), attachments*, comments*, notifications*.

### B.4 API minimal (REST, OpenAPI)

- CRM: `GET/POST /api/customers`, `GET/PATCH /api/customers/{id}`, `GET /api/customers/{id}/360`, `/api/sites`, `/api/leads`, `/api/quotations`.
- Aset: `GET/POST /api/assets`, `GET /api/assets/{id}`, `GET /api/assets/{id}/timeline`, `GET /api/assets/{id}/service-history`, `POST /api/assets/{id}/meter-readings`.
- Service: `POST/GET /api/service-requests`, `POST/GET /api/work-orders`, `PATCH /api/work-orders/{id}/status`, `POST .../assignments|materials|checklist|signoff|invoice`.
- Integrasi: `POST /api/webhooks/accounting/invoice|payment/received|iot/meter-reading`, `POST /api/import/{customers,items}`, `GET /api/export/work-orders`.

### B.5 UI standar

- Sidebar gelap (abu tua/hitam) + aksen merah (butuh perhatian) / kuning (menunggu); badge status berwarna di tiap dokumen.
- Form transaksi seragam: header 2 kolom (pelanggan/aset/tanggal + nomor auto & status), tombol aksi (Ambil dari…/Simpan/Proses/Cetak/Lampiran), tab (Detail Item-Jasa | Info Lainnya | Riwayat Aktivitas).
- Kartu Aset: foto + identitas + status + next service; tab (Overview | Spesifikasi | Meter | Riwayat Servis timeline | Biaya | Garansi | Kontrak | Dokumen).
- WO 2 kolom (kiri: pelanggan/lokasi/aset/prioritas/jadwal/teknisi/SLA; kanan: masalah/diagnosis/solusi/checklist/material/foto/TTD) + tombol sesuai status.
- Mobile teknisi: daftar kerja hari ini, navigasi, check-in/out, meter, checklist offline-first, foto, TTD; sinkron saat online.

### B.6 Roadmap (gabungan kedua riset, disesuaikan dgn kondisi kode saat ini)

- Fase 1 Fondasi: pindah ke UUID + organization_id + RBAC matriks + audit log generik + penomoran + migrasi SQLite→PostgreSQL (atau tetapkan SQLite sbg mode dev saja).
- Fase 2 CRM+Aset: kontak, site, leads, master aset + komponen + meter + garansi + timeline + kontrak (read-only dulu).
- Fase 3 Service MVP: request→WO→checklist→material→foto→TTD→status workflow + mobile teknisi dasar.
- Fase 4 Komersial-Service link: WO→Invoice (billable vs warranty-covered), stock issue dari WO, DP/giro untuk servis.
- Fase 5 Akuntansi-service costing: jurnal otomatis WO (Dr Biaya/WIP–Cr Persediaan; Dr Piutang–Cr Pendapatan jasa), L/R per aset/WO/pelanggan, period lock tetap.
- Fase 6 Advanced: PM otomatis (cron), SLA engine, approval engine, warranty claim ke supplier, portal pelanggan, IoT meter, prediktif.
- Urutan bangun yang disepakati kedua riset: **Customer 360 → Asset Registry → Work Order → Material+Labor costing → Invoice → Accounting**. Jangan mulai dari seluruh ERP sekaligus.

---

## C. AUDIT PEKERJAAN SAAT INI (terhadap rancangan §B)

### C.1 Opencode "CRM Apps" (app.py + public + Docker) — accounting HEAVY, service NOL

**Yang SUDAH ADA & bagus (pertahankan):** engine double-entry seimbang (Dr=Cr), auto-posting Sales→(Dr Piutang/Cr Penjualan+PPN, Dr HPP/Cr Persediaan), Purchase, Payment+alokasi, DP terima/bayar + alokasi, giro (cair/tolak), retur, delivery/receive, multi-gudang, inventory_layers (FIFO) + average, doc_sequences anti-duplikat, period_locks, void (bukan edit posted), validasi (stok minus ditolak, bayar/retur ≤ sisa, limit utang vendor), rupiah integer, COA 5-digit + seed, pajak master, PPh21 TER, HRIS (karyawan/absensi/cuti/gaji), cabang, salesman+komisi, tukar tambah, kas-bank + rekonsiliasi auto-match ±3 hari, laporan (TB/LR/neraca/arus kas/PPN/cabang/aging/forecast/reorder), user+role (admin/manager/kasir/finance/gudang/hrd) + ganti password wajib + sesi 12 jam, activity log, webhook+log, backup/restore + backup.sh + Docker + DEPLOY-NUC (Tailscale) + PANDUAN operasional. Total ~55 tabel, 2273 baris, stdlib-only (tanpa dependensi) — kekuatan untuk NUC.

**GAP KRITIS (semua inti rancangan §B belum ada — grep keyword lead/work_order/service_request/contract/meter/site/customer_contact/technician = NOL di app.py):**

| Kebutuhan riset | Status di app.py | Dampak |
|---|---|---|
| Leads/Opportunity/pipeline + aktivitas | TIDAK ADA (hanya sales_quotations dagang) | CRM §B.2-#2 gagal — tidak ada funnel |
| customer_contacts & customer_sites | TIDAK ADA (customers hanya code/name/email + receivable account) | Relasi Customer→Site→Asset putus di hulu |
| customer_assets + kategori + komponen + atribut fleksibel + transfer + garansi + dokumen | TIDAK ADA (`/api/assets` yang ada = fixed_assets milik sendiri + depreciate/dispose) | Diferensiasi utama ERP-MSP = 0% |
| service_requests + work_orders + lines/checklist/timesheet/signoff | TIDAK ADA | Rantai WO wajib-ke-aset tidak bisa jalan |
| meter readings (hour/km) | TIDAK ADA | PM berbasis jam operasi mustahil |
| maintenance_contracts + plans + SLA | TIDAK ADA | Tidak ada kontrak berlangganan / PM otomatis |
| approval engine configurable | Parsial (tabel approvals + decide, hanya untuk void) | Aturan nominal/diskon/warranty belum ada |
| multi-tenant organization_id | TIDAK ADA (single-tenant; SQLite satu file) | Multi-entitas MSP/PAG butuh retrofit |
| UUID PK | TIDAK (INTEGER AUTOINCREMENT) | Migrasi ke skema §B.3 = rewrite migrasi |
| costing 3-nilai per WO | TIDAK ADA (hanya HPP barang dagang) | Margin jasa/teknisi/kontrak tak terhitung |
| mobile teknisi / offline / foto / TTD | TIDAK ADA (frontend 927-line app.js, bukan PWA) | Eksekusi lapangan tidak terlayani |

**Risiko teknis:** satu file 2273 baris (susah direview/dipecah ke modular monolith); SQLite WAL+busy_timeout oke untuk 1–2 kasir tapi tanpa test otomatis, tanpa OpenAPI, auth session-token sederhana (bukan JWT/OAuth), PANDUAN masih kredensial default admin/admin123 di dokumen.

### C.2 Jules Laravel (CRM_asset_management_jules) — SKELETON 0%

Hanya Laravel fresh: 3 migrasi bawaan (users/cache/jobs), 1 model User, 1 controller kosong, routes web.php default. **Nol tabel bisnis, nol modul §B.** Nilai saat ini = titik awal bersih untuk bangun modular monolith Laravel + PostgreSQL + UUID sesuai §B (bukan untuk diadu dengan app.py yang sudah jadi).

### C.3 Putusan audit

- Pekerjaan saat ini **adalah "Accurate versi online" (lapisan 3: ERP-keuangan dagang) — justru yang riset #1 menyarankan JANGAN dibangun ulang** — sementara **lapisan 1 (CRM) dan 2 (asset/service) yang menjadi diferensiasi MSP belum dikerjakan sama sekali**.
- Jalur termurah: **JANGAN buang app.py** (ledger-nya matang) — bangun modul §B.3-BERTANDA-* sebagai lapisan service di atasnya (atau sebagai service Laravel terpisah yang menulis jurnal ke API app.py), lalu migrasi DB ke PostgreSQL di Fase 1. Alternatif buang-salah-satu = buang Jules (masih kosong, murah) ATAU jadikan Jules sebagai backend service-modul, bukan rewrite accounting.
- Sebelum koding: butuhkan ERD + state machine WO/request + permission matrix + OpenAPI (sesuai perintah riset #2 §13) — keempatnya belum ada di repo.

## D. Rekomendasi next step konkret

1. OCR PDF #3 bila dianggap sumber wajib; bila tidak, bekukan acuan = dokumen ini.
2. Pilih arsitektur: (a) tambah modul service ke app.py (cepat, cocok NUC 8GB, tetap SQLite→PG nanti) atau (b) Laravel Jules untuk modul service + app.py jadi ledger-service. Rekomendasi saya: (a) untuk 1–2 bulan ke depan.
3. Kerjakan berurutan: customer_contacts+sites → customer_assets+meter → service_requests+work_orders+lines → WO→invoice link + warranty flag → kontrak+PM cron. Setiap modul: migrasi + API + UI tab + seed (2 pelanggan, 3 lokasi, 5 genset, 2 kendaraan, 10 part, 5 jasa, 3 teknisi, 3 WO, 2 kontrak, 2 invoice — sesuai seed riset #2).
4. Definisi selesai per modul (acceptance): WO wajib 1 aset; histori aset terisi otomatis dari WO closed; margin WO = revenue−(material+labor+expense); PM auto-create tanpa duplikat; posted transaction tak bisa diedit.
