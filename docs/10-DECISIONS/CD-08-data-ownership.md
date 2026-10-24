# CD-08 — Data Ownership, Sharing & Lifecycle

Status: **LOCKED** (HUMAN CONFIRMED — "HUMAN CONFIRM — LOCK CD-08").

Sumber: 18 keputusan HUMAN pada CD-08 Decision Gate (Q1–Q18).
Sifat dokumen: transkripsi keputusan HUMAN. Tidak ada reinterpretasi substantif.
Kode, schema, database, dan analisis terdahulu tetap **reference/evidence**.
CD-07 tetap berlaku; dokumen ini mengisi governance ownership yang ditunda.

## Ownership model

### GLOBAL / SHARED

Dapat digunakan lintas Workspace:

* Customer / Company Master (+ relasi workspace, Q4)
* Contact / PIC (shared; konteks workspace-specific menyusul, Q5)
* Vendor Master (Q5 CD-07)
* Inventory Item / Product Master (stok milik workspace, Q6 CD-07)
* Vendor Offer (Q7 CD-07)
* Acquisition Price Reference (Q8 CD-07)
* Price History: intelligence umum maupun riwayat pemakaian (Q9 CD-07)
* Provenance tiap info harga: vendor, item, harga, basis, tanggal, sumber (Q10)

### WORKSPACE-OWNED

Hanya milik Workspace tertentu:

* Sales Pipeline (Q15 CD-07)
* Quotation, Sales Order, Purchasing/Service transaction, dokumen (Q10 CD-07)
* Numbering per workspace (Q11 CD-07)
* Template per workspace (Q12 CD-07)
* Approval, reporting operasional (Q2/Q16 CD-07)
* Stock / inventory transaction (Q6 CD-07)
* Pemakaian harga di transaksi milik workspace (Q16):
  intelligence shared ("XYZ pernah menawar 10jt") terpisah dari aktivitas
  workspace ("A memakai 10jt di A-001").

### WORKSPACE RELATIONSHIP

* Q4: relasi Customer ↔ Workspace adalah **penanda** pemakaian
  ("customer ini dipakai workspace ini"). Bentuk pencatatan menyusul (desain).

### HISTORICAL / IMMUTABLE

* Q8: price history **immutable** — record lama (mis. Jan Rp10rb) dan baru
  (Mar Rp11rb) keduanya tersimpan; tidak boleh diedit setelah tercatat.

## Governance aturan

* Q1 (creation): user tiap workspace boleh membuat master baru (Customer,
  Vendor, Item); langsung menjadi shared.
* Q2 (modification): perubahan master via **suggest**; **approval admin**.
* Q3 (global effect): perubahan yang disetujui **berlaku global**;
  tidak ada info workspace-specific yang teridentifikasi kini.
* Q6–Q7 (offer): offer yang dibuat langsung terlihat dan dipakai lintas
  workspace; lihat/pakai bebas, ubah sumber terkendali (Q2).
* Q11–Q13 (lifecycle): master yang sudah dipakai **nonaktif/arsip**,
  bukan hard-delete — berlaku untuk vendor, item, dan customer.
* Q14 (duplicate): satu identitas master dijaga via **proses bisnis**;
  tanpa matching otomatis.
* Q15 (merge): proses merge master diperlukan bila duplikat terbukti sama
  entity; cara teknis menyusul.
* Q17 (private notes): **tidak ada catatan privat** — informasi vendor shared.

## Open (bukan bagian lock)

* Bentuk relasi customer-workspace dan konteks kontak workspace-specific.
* Matriks suggest/approval detail.
* Teknis merge dan teknis nonaktif/arsip.

## Governance

> **A LOCKED decision may not be changed, weakened, expanded, or reinterpreted
> by AI Manager, AI Programmer, or AI Auditor without explicit HUMAN authorization.**

Konflik dengan keputusan LOCKED:

> **STOP → REPORT → HUMAN**
