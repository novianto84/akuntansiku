# CD-06 — Vendor Offer & Acquisition Price Reference

```text
Decision ID: CD-06
Status: LOCKED
Authority: HUMAN
Mode: DESIGN ONLY
```

Sumber: keputusan HUMAN Q1–Q10 (decision gate), Q-A–Q-D (discovery), dan
finalisasi Q8 (Dynamic Role-Based Visibility) + konfirmasi LOCK CD-06.
Sifat dokumen: transkripsi keputusan HUMAN. Tidak ada reinterpretasi.
Kode, schema, database, dan analisis terdahulu tetap **reference/evidence**.

## Model konseptual

```text
COMPANY → Vendor Role → Vendor Offer
  ├── Original Input + Price Basis → Derived (Exclude/Include) → Final
  ├── Provenance + Validity + Version/Correction History → Price History
  └── (terpisah) Acquisition Price → Shared Operational Reference
```

Satu offer = satu harga asli + satu basis → tiga representasi (Exclude PPN,
Include PPN, Final). Ketiganya bukan tiga harga independen.

## Price basis

Bases: EXCLUDE_PPN / INCLUDE_PPN / NET_FINAL. NET_FINAL ≠ EXCLUDE_PPN.
Satu nilai menjadi input berdasarkan basis; representasi lain dihitung/
diturunkan. Untuk NET/FINAL, hanya Final yang terisi; Exclude/Include kosong.
Basis asli tersimpan bersama harga; tidak dinormalisasi diam-diam.

Rumus generik (`Include = Exclude × (1 + Rate)`, sebaliknya). Tarif PPN
tidak dikunci; contoh 11% hanya matematika. Sumber tarif = domain
Tax/Accounting future.

## Offer vs acquisition

Vendor Offer (penawaran vendor) dibedakan dari Acquisition Price (referensi
peristiwa perolehan aktual). Tidak identik otomatis. Acquisition jamak per
item/vendor, immutable, shared, bukan valuasi/HPP/FIFO/Average/COGS.
Konteks transaksi pembentuknya = desain mendatang.

## Immutability & lifecycle

Koreksi = record/versi baru (v1 lestari; pemakaian tertaut ke versi yang
dipakai). Lifecycle: ACTIVE → INACTIVE → ARCHIVED (sekuensialitas pola;
syarat kunci: tanpa hapus destruktif, referensi valid, arsip terlacak).
Ubah terkendali via suggest + approval admin (CD-08); matriks otoritas
detail OPEN.

## Provenance & atribut

Lestari: vendor, item, harga asli, basis, derived/final, currency, unit,
effective date, validity, source, relasi versi. Currency asli dipertahankan;
konversi operasional DEFERRED. MOQ/quantity-break/pack OPEN/DEFERRED.

## Perbandingan & penggunaan Sales

Perbandingan faktual memakai Final + konteks asli tampil; tanpa ranking,
rekomendasi, seleksi, atau "best vendor". Offer = referensi quotation;
tidak otomatis menjadi harga jual; tanpa pricing engine. Latest offers:
perlu (jumlah OPEN).

## Q8 — Dynamic Role-Based Visibility (FINAL)

Vendor Offer tetap **shared intelligence** lintas workspace, tetapi visibility
dikendalikan dinamis per role via konfigurasi Admin
(`Access / Visibility Policy → Vendor Offer`).

* Admin mengaktifkan/menonaktifkan visibility per role tanpa mengubah
  ownership, sharing, record, history, acquisition, atau provenance.
* Role tanpa visibility tidak dapat melihat/menggunakan offer maupun
  turunannya yang mengungkap price intelligence (offer, harga, identitas
  vendor terkait, input asli, basis, derived, final/reference, history,
  provenance, source, relasi offer→vendor, pemakaian sebagai referensi).
  Bukan sekadar field-level hiding; bukan selector per workspace.
* Batas: `Vendor Master ≠ Vendor Offer Visibility ≠ Global Vendor Master
  Visibility`. Q8 tidak membatasi akses Sales atas info vendor dari konteks
  bisnis lain yang diizinkan RBAC/workflow lain.
* Detail UI, nama menu, permission key, implementasi otorisasi, matriks
  lengkap: OPEN/DEFERRED technical design (tidak dikarang di sini).

## Boundary

CD-06 bukan accounting engine dan bukan inventory costing engine. Tanpa:
journal, GL, COA, COGS, FIFO, Average Cost, stock valuation, HPP, tax
accounting/ledger/filing/reconciliation, hardcoded tarif, konversi otomatis,
rekomendasi harga otomatis. Tanpa schema/tabel/kolom.

## Cross-decision consistency (saat lock)

```text
CD-01: CONSISTENT | CD-02: CONSISTENT | CD-03: CONSISTENT | CD-04: CONSISTENT
CD-05: CONSISTENT | CD-07: CONSISTENT | CD-08: CONSISTENT
```

## Governance

> **A LOCKED decision may not be changed, weakened, expanded, or reinterpreted
> by AI Manager, AI Programmer, or AI Auditor without explicit HUMAN authorization.**

Konflik dengan keputusan LOCKED:

> **STOP → REPORT → HUMAN**
