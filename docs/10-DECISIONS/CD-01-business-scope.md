# CD-01 — Business Scope & System Boundary

Status: **FINAL / LOCKED** (HUMAN CONFIRMED).

Sumber: keputusan HUMAN (konfirmasi final CD-01) dan rekonsiliasi CD-01 Phase 1B.
Sifat dokumen: transkripsi keputusan HUMAN. Tidak ada reinterpretasi substantif.
Repository current state, commit historis `137c6d5`, `docs/accurate5-spec.md`,
`docs/accurate5-gap-akuntansiku.md`, `docs/accurate5-inventory.xlsx`, implementasi
`app.py`, dan schema/database saat ini tetap **evidence/reference**, bukan sumber
keputusan CD-01.

## S1 — Long-Term System Purpose

* ERP adalah tujuan jangka panjang (destination arsitektur).
* CRM adalah **first major workstream untuk fase awal**.
* Accurate 5 adalah reference, knowledge source, dan existing business reference.
* Accurate 5 bukan requirement otomatis dan bukan target parity.

## S2 — Initial Business Scope (INSIDE fase awal)

1. CRM / Customer Management
2. Sales
3. Purchasing
4. Inventory

CRM adalah domain tersendiri, bukan sekadar customer master. Scope CRM fase awal
mencakup secara konseptual:

* Company / Customer
* Contact / PIC
* Customer relationship
* Customer activity/history
* Unit / Asset customer
* Service / Work Order / SPK
* Technician workflow
* Service history
* Material / spare-part usage
* Customer-facing unit history
* Reminder / follow-up customer
* CRM-related communication/activity

Daftar di atas adalah scope konseptual, bukan schema atau implementasi.

## Finance / Accounting / Tax — DEFERRED / FUTURE SCOPE

Status: **DEFERRED / FUTURE SCOPE**. Bukan OUTSIDE PERMANENTLY.

Yang termasuk deferred:

* Full Finance / Accounting
* Full General Ledger
* Full Tax
* Full Fixed Asset Accounting
* Full Project Accounting
* Advanced accounting dimensions
* Advanced multi-currency accounting

> DEFERRED ≠ OUTSIDE PERMANENTLY.

Arsitektur jangka panjang tidak boleh sengaja menutup kemungkinan domain-domain
tersebut. Tahap awal tidak boleh mengimplementasikan full scope tersebut hanya
karena alasan "ERP".

## S3 — Role Structure

Role aplikasi yang dipertahankan:

* ADMIN
* MANAGER
* FINANCE
* KASIR

> Role structure ≠ business module scope.

Keberadaan role FINANCE/KASIR tidak berarti Finance/Accounting harus menjadi
scope implementasi fase awal. Detail permission/RBAC adalah pekerjaan desain
tersendiri dan tidak didesain di sini.

## S4 — Accurate 5 Position

> Accurate 5 = REFERENCE / KNOWLEDGE / EXISTING BUSINESS REFERENCE.

Accurate 5:

* bukan runtime dependency yang sudah diputuskan,
* bukan automatic source of requirement,
* bukan target parity,
* bukan alasan otomatis untuk menambahkan fitur.

Status migration/integration/runtime: **OPEN DECISION**. Tidak ditentukan di sini.
Tidak ada desain integrasi dan tidak ada migration plan.

## S5 — Initial System Boundary (fase awal)

### CRM

* Customer/company
* Contact/PIC
* Customer relationship/activity
* Unit/customer asset registry
* Service/WO/SPK
* Technician workflow
* Service history
* Material usage
* Reminder/follow-up
* Customer-facing access bila diperlukan

### Sales

* Customer-related sales process
* Quotation
* Sales Order bila diperlukan
* Delivery/fulfillment bila diperlukan
* Sales invoice bila diperlukan
* Sales status/history

### Purchasing

* Vendor
* Purchase Request bila diperlukan
* Purchase Order
* Receiving
* Purchasing history

### Inventory

* Item/spare part
* Item master
* Stock
* Stock movement
* Warehouse/location bila diperlukan
* Reservation/usage bila diperlukan
* Material usage untuk service
* Inventory history

### Supporting capabilities

Dapat diperlukan untuk menopang scope di atas, antara lain:

* Authentication
* Authorization/RBAC
* Audit log
* File/photo/document management
* Notification
* Customer access
* Technician access
* Approval workflow
* QR code/public unit access
* Search/filter
* Operational reporting

Item dengan kata "bila diperlukan" atau "supporting" bukan keputusan detail
final. Detailnya ditentukan pada desain masing-masing workstream.

## S6 — Initial Data Ownership (PROPOSED, bukan LOCKED)

| Data | Initial SoR |
|---|---|
| Customer / Company | CRM |
| Contact / PIC | CRM |
| Vendor | Purchasing |
| Item / Spare Part | Inventory |
| Inventory / Stock | Inventory |
| Sales Transaction | Sales |
| Purchasing Transaction | Purchasing |
| Service / Work Order | CRM / Service |
| Customer Unit / Asset | CRM / Asset Registry |
| Accounting | Accurate 5 / existing accounting system untuk saat ini |
| Tax | Accurate 5 / existing accounting system untuk saat ini |

* S6 ownership belum seluruhnya LOCKED.
* Kategori yang belum jelas tetap UNKNOWN/OPEN.
* Future synchronization/integration dengan Accurate 5 belum didesain.
* PROPOSED tidak diubah menjadi LOCKED.

## Status register

### LOCKED

**CD-01 — Business Scope & System Boundary: FINAL / LOCKED.**

### PROPOSED (sengaja tetap, tidak diubah)

* S1 detail turunan bila ada
* S2 detail sub-process yang masih "bila diperlukan"
* S3 role structure
* S5 detail supporting capability
* S6 initial ownership

### DEFERRED

* Full Finance/Accounting
* Full GL
* Full Tax
* Fixed Asset Accounting
* Project Accounting
* Advanced accounting dimensions
* Advanced multi-currency accounting
* Full RMA

### OPEN

* Accurate 5 migration/integration/runtime role
* Detailed RBAC permissions
* Supporting capability detail
* Optional document-flow components
* Future integration design

### UNKNOWN

Data ownership/category yang memang belum ditentukan.

## Governance

> **A LOCKED decision may not be changed, weakened, expanded, or reinterpreted by AI Manager, AI Programmer, or AI Auditor without explicit HUMAN authorization.**

Jika ada konflik antara implementation evidence dan CD-01 LOCKED:

> **STOP → REPORT → HUMAN**

Konflik tidak diselesaikan melalui asumsi AI.
