# CD-09 — Purchasing Transaction Boundary

```text
Decision ID: CD-09
Status: LOCKED
Authority: HUMAN
Mode: DESIGN ONLY
```

Sumber: keputusan HUMAN Q1–Q18 discovery CD-09 dan konfirmasi ACCEPT.
Sifat dokumen: transkripsi keputusan HUMAN. Tanpa business rule baru, tanpa
perubahan makna.
Kode, schema, database, dan analisis terdahulu tetap **reference/evidence**.

## Purchase Request

* PR **opsional** — boleh dilewati; pembelian dapat langsung ke PO.
* Inisiator kebutuhan: Technician, Coordinator, Sales, Manager, Purchasing,
  Admin (ownership kasar; permission final menyusul).
* PR dapat dibatalkan (alasan wajib, histori tetap).
* Emergency purchase boleh melewati PR; tetap PO + receiving + alasan darurat.

## Purchase Order

* PO **wajib** untuk pembelian vendor.
* PO bebas offer: boleh dari Vendor Offer (harga boleh hasil negosiasi/beda)
  atau tanpa offer.
* Lifecycle: Draft → Issued → Received → Completed. Resmi saat Issued;
  immutable setelah terbit; batal/koreksi via revisi.
* Harga SO-vs-quotation tidak relevan di sini; harga PO mengikuti aturan §11.
* SO dapat standalone — cermin sisi-beli: PO dapat tanpa PR.

## Vendor Offer Relationship

PO boleh merujuk offer; offer ≠ acquisition; harga PO boleh beda dari offer.

## Receiving

* Dokumen/record tersendiri per penerimaan; milik satu workspace.
* Partial receiving didukung (6 kini + 4 kemudian).
* Sisa kuantitas tetap outstanding (tanpa auto-complete).
* Terima-tolak terpisah untuk rusak (terima 8 + tolak 2; ganti/retur menyusul).

## Acquisition Event & Price

* Acquisition terjadi saat barang diterima + harga aktual tersedia.
* Harga PO menjadi dasar awal; dikoreksi saat receiving bila beda.
* Harga perolehan mengikuti harga aktual + koreksi tercatat berversi.
* Input saat receiving oleh penerima; record lama immutable.
* Konsisten CD-04 R1 (harga perolehan aktual sebagai operational reference).

## Cancellation & Correction

* PR, PO, receiving masing-masing dapat dibatalkan (alasan wajib, histori).
* Koreksi = revisi/versi baru; histori lestari (konsisten CD-05/06/08).

## Workspace Ownership

PR/PO/receiving milik satu workspace; tanpa cross-workspace.
Vendor/offer/acquisition shared sebagai referensi (konsisten CD-07/08).

## Inventory Handoff (prinsip saja — LOCKED sebatas ini)

Receiving yang sah menjadi input stok operasional (qty; gudang/lokasi dan
movement sebagai data operasional tanpa valuasi).

**Tidak dikunci / tidak diasumsikan dari CD-09:** detail warehouse, location,
movement, adjustment, reservation, transfer, dan inventory lifecycle — menunggu
gate/desain tersendiri.

## Accounting Boundary

Tanpa AP/invoice-akuntansi/payment/journal/GL/tax/HPP/COGS/valuasi.
Vendor invoice = dokumen/referensi operasional.

## Non-Goals

Payment workflow; AP aging; tax/PPN engine; landed cost; stock valuation;
FIFO/Average; multi-currency accounting.

## Deferred

Threshold nominal darurat/kecil; format nomor; daftar approver; teknis rantai
revisi; detail gudang/lokasi; retur-penggantian detail; template dokumen.

## Cross-Decision Consistency (saat lock)

```text
CD-01: CONSISTENT | CD-03: CONSISTENT | CD-04: CONSISTENT | CD-05: CONSISTENT
CD-06: CONSISTENT | CD-07: CONSISTENT | CD-08: CONSISTENT
```

## Governance

> **A LOCKED decision may not be changed, weakened, expanded, or reinterpreted
> by AI Manager, AI Programmer, or AI Auditor without explicit HUMAN authorization.**

Konflik dengan keputusan LOCKED:

> **STOP → REPORT → HUMAN**
