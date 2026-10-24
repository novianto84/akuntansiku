# CD-05 — Sales Transaction & Quotation

```text
Decision ID: CD-05
Status: LOCKED
Authority: HUMAN
Mode: DESIGN ONLY
```

Sumber: keputusan HUMAN Q1–Q5, Q-AUTO-CLOSE=(a), dan konfirmasi
"HUMAN CONFIRM — LOCK CD-05".
Sifat dokumen: transkripsi keputusan HUMAN. Tidak ada reinterpretasi,
peningkatan, perluasan, atau perubahan.
Kode, schema, database, dan analisis terdahulu tetap **reference/evidence**.

## Scope

CD-05 mencakup: Quotation; Sales Order; konversi quotation → SO; konversi
parsial; SO standalone; fulfillment; partial fulfillment/backorder; invoice
sebagai accounting reference; pricing; discount boundary; PPN informational
boundary; numbering boundary; cancellation/closure; audit/history; workspace
ownership.

## Q1 — Partial Quotation → Sales Order (LOCKED)

```text
1 Quotation → N Sales Orders
```

* partial conversion diperbolehkan;
* hanya item quotation terpilih yang dikonversi;
* sisa item tetap outstanding;
* konversi lanjutan atas sisa item tetap dimungkinkan;
* riwayat konversi harus dapat ditelusuri.

## Q2 — Partial Sales Order Fulfillment (LOCKED)

```text
1 Sales Order → N Fulfillments
```

* multiple fulfillment records diperbolehkan;
* partial fulfillment diperbolehkan;
* sisa kuantitas tetap outstanding/backorder;
* riwayat fulfillment harus dapat ditelusuri;
* fulfillment tidak memutasi inventory;
* tidak ada inventory reservation;
* Accurate 5 tetap stock authority saat ini;
* tidak ada FIFO/average-cost/COGS/stock valuation dari CD-05.

## Q3 — Standalone Sales Order (LOCKED)

Sales Order dapat dibuat tanpa quotation.

* quotation bersifat opsional;
* SO dapat benar-benar standalone;
* tidak ada pipeline/activity/reference pendahulu yang diwajibkan;
* informasi wajib SO sendiri harus mencukupi;
* bila quotation ada, SO boleh mereferensikannya.

## Q4 — Quotation Status After Partial Conversion (LOCKED)

```text
PARTIALLY_CONVERTED
```

* bila hanya sebagian item terkonversi ke SO, quotation menjadi
  `PARTIALLY_CONVERTED`;
* sisa item tetap outstanding;
* quotation tetap aktif;
* konversi lanjutan tetap dimungkinkan;
* konversi parsial tidak menjadikan quotation terminal.

## Q5 — CLOSED Model (LOCKED)

Tidak ada status `REVOKED` yang terpisah. Seluruh penutupan terminal
quotation memakai:

```text
CLOSED
```

### Automatic closure

Bila seluruh item quotation telah terkonversi ke SO:

```text
CLOSED
closure_reason = COMPLETED
```

Terjadi otomatis. Tanpa approval Manager/Admin.

PENTING: automatic closure terjadi saat seluruh item **terkonversi ke SO**.
Tidak menunggu: pemenuhan SO, penyelesaian delivery/service, invoice,
maupun posting accounting.

### Manual closure

Bila quotation belum lengkap tetapi tidak dilanjutkan (customer tidak
melanjutkan sisa item; sisa tidak diperlukan; tidak relevan komersial;
alasan bisnis sah lainnya):

1. Sales mengajukan close request;
2. alasan wajib;
3. approval Manager/Admin wajib;
4. setelah disetujui menjadi `CLOSED`;
5. alasan dan riwayat approval dipertahankan.

### Terminal behavior

Setelah `CLOSED`: tidak kembali ke `OPEN` atau `PARTIALLY_CONVERTED`;
tidak ada konversi lanjutan; histori tetap; nomor tidak dipakai ulang.
Tidak ada status `REVOKED`.

## Quotation Revision

* Revisi negosiasi menghasilkan dokumen revisi/quotation baru, bukan mutasi
  in-place atas revisi yang sudah final.
* Revisi memakai nomor dasar yang sama + suffix/version.
* Revisi sebelumnya tetap immutable; relasi/riwayat revisi terlacak.
* Hubungan teknis SO dengan revisi quotation tertentu adalah detail
  deferred/non-material — tidak ditentukan di sini.

## Sales Order

* SO dapat berasal dari quotation atau standalone.
* Harga SO boleh berbeda dari harga quotation.
* SO tidak memerlukan approval.
* SO milik workspace aktif.

## Fulfillment

* Multiple fulfillment records per SO; partial fulfillment; outstanding/backorder.
* Riwayat fulfillment terlacak.
* Tanpa mutasi inventory; tanpa reservasi; Accurate 5 stock authority.

## Accounting Boundary

CD-05 tidak memperkenalkan: journal; General Ledger; dependensi COA; COGS;
FIFO; Average Cost; stock valuation; tax accounting; accounting posting.
Invoice hanya accounting/reference boundary.

## Pricing / Vendor Offer Boundary

* Harga quotation adalah data sales operasional; harga SO boleh berbeda;
  harga boleh di-override menurut aturan bisnis.
* Vendor Offer adalah reference/intelligence; tidak otomatis menjadi harga jual.
* Tanpa ranking/rekomendasi vendor otomatis; tanpa pricing engine otomatis.

## PPN / Tax Boundary

* PPN informatif/referensi saja di CD-05.
* Tanpa tax engine, tax journal, tax filing; tanpa locked tax rate kecuali
  diputuskan pada desain Tax/Accounting mendatang.

## Numbering

* Numbering milik workspace; sequence terpisah per workspace; reset tahunan.
* Nomor immutable; tidak dipakai ulang.
* Sintaks final eksak: OPEN / DEFERRED DESIGN DETAIL — tidak ditentukan.

## Audit / History

Ketertelusuran wajib: kreasi; perubahan status; revisi quotation; konversi
parsial; relasi quotation → SO; sisa/outstanding; fulfillment; close request
manual; approval penutupan; closure reason; referensi harga/offer; timestamp;
user penanggung jawab. Tanpa penghapusan destruktif dokumen komersial.

## Workspace Boundary (konsisten CD-07)

Quotation, SO, fulfillment milik workspace; numbering dan reporting
workspace-specific; cross-workspace transaction dilarang; master
customer/vendor/item shared dan intelligence shared boleh direferensikan;
ownership transaksi tetap workspace-specific.

## Cross-Decision Consistency (saat materialisasi)

```text
CD-01: CONSISTENT
CD-02: CONSISTENT
CD-03: CONSISTENT
CD-04: CONSISTENT
CD-06: CONSISTENT
CD-07: CONSISTENT
CD-08: CONSISTENT
```

Keputusan-keputusan tersebut tidak diubah.

## Status Model

```text
DRAFT
  ↓
OPEN
  ↓
PARTIALLY_CONVERTED
  ↓
CLOSED
```

Quotation dapat pula `OPEN → CLOSED` melalui manual closure yang disetujui.

Automatic closure:

```text
OPEN / PARTIALLY_CONVERTED
        ↓
ALL ITEMS CONVERTED TO SO
        ↓
CLOSED
closure_reason = COMPLETED
```

Manual closure:

```text
OPEN / PARTIALLY_CONVERTED
        ↓
SALES CLOSE REQUEST
        ↓
REASON REQUIRED
        ↓
MANAGER / ADMIN APPROVAL
        ↓
CLOSED
```

Tidak ada status terminal tambahan seperti `REVOKED`.

## Governance

> **A LOCKED decision may not be changed, weakened, expanded, or reinterpreted
> by AI Manager, AI Programmer, or AI Auditor without explicit HUMAN authorization.**

Konflik dengan keputusan LOCKED:

> **STOP → REPORT → HUMAN**
