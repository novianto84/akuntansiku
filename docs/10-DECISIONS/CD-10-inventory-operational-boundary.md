# CD-10 — Inventory Operational Boundary

```text
Decision ID: CD-10
Status: LOCKED
Authority: HUMAN
Mode: DESIGN ONLY
```

Sumber: keputusan HUMAN Q1–Q21 discovery CD-10, klarifikasi boundary Accurate,
dan konfirmasi ACCEPT.
Sifat dokumen: transkripsi keputusan HUMAN. Tanpa business rule baru, tanpa
perubahan makna.
Kode, schema, database, dan analisis terdahulu tetap **reference/evidence**.

## Boundary statement (LOCKED)

> Inventory pada platform ini adalah **operational inventory qty-only**.
> Detail costing, valuation, dan accounting tetap di luar CD-10.
> Accurate tetap menjadi existing/current authority selama masa transisi,
> tetapi CD-10 **tidak mengunci Accurate sebagai runtime dependency permanen**
> untuk platform baru.

## Stock definition & movement (Q1–Q6, Q21)

* Q1: stok = barang fisik dalam custody perusahaan.
* Q2: receiving sah menambah stok saat itu juga (+N kini).
* Q3: sumber stock-in: receiving, adjustment, retur customer, retur teknisi
  (transfer konseptual; antar-gudang belum perlu; tanpa mekanisme opening
  formal).
* Q4: stok berkurang langsung saat material dikeluarkan.
* Q5: pemakaian WO mengurangi stok saat pengambilan.
* Q6: sisa material teknisi kembali ke stok tercatat.
* Q21: pengeluaran darurat tanpa PR boleh, tercatat + alasan.

## Control rules (Q7–Q8, Q12–Q14, Q18)

* Q7: adjustment terkendali (pengaju + approval + alasan wajib + histori).
* Q18: koreksi salah-input dibedakan dari adjustment selisih-fisik.
* Q8: opname bila perlu → banding → adjustment.
* Q12: negative stock hanya dengan approval.
* Q13: status AVAILABLE vs DAMAGED/QUARANTINE.
* Q14: retur vendor tercatat, stok berkurang.

## Structure & ownership (Q9–Q11, Q15–Q17, Q20)

* Q9: satu gudang; bin/detail ditunda.
* Q10: transfer antar-gudang belum perlu.
* Q11: tanpa reservasi; stok aktual saja.
* Q15: stok/gudang/movement milik workspace; tanpa cross-workspace.
* Q16: Item Master global; saldo+movement per workspace.
* Q17: tanpa mekanisme opening stock formal.
* Q20: lifecycle AKTIF-NONAKTIF-ARSIP untuk item/lokasi/gudang; histori tetap.

## Traceability (Q19)

Histori lengkap per movement: item, qty, arah, sumber, waktu, workspace,
dokumen referensi, pelaku, alasan (bila adjustment).

## Accounting boundary

Tanpa FIFO/Average/HPP/COGS/valuasi/journal/GL/tax/landed-cost.
Harga perolehan = operational reference (CD-04); bukan valuation basis.

## Deferred (tidak dikunci / tidak diasumsikan)

Detail warehouse/location/bin; transfer; reservation; opening balance formal;
approval matrix teknis; arsitektur inventory pasca-transisi; formula/presisi;
template; audit teknis.

## Cross-Decision Consistency (saat lock)

```text
CD-01: CONSISTENT | CD-03: CONSISTENT | CD-04: CONSISTENT | CD-05: CONSISTENT
CD-06: CONSISTENT | CD-07: CONSISTENT | CD-08: CONSISTENT | CD-09: CONSISTENT
```

Fulfillment sales (non-mutasi, CD-05) dibedakan dari movement gudang
operasional (CD-10). Tidak ada keputusan CD lain yang dibuka kembali.

## Governance

> **A LOCKED decision may not be changed, weakened, expanded, or reinterpreted
> by AI Manager, AI Programmer, or AI Auditor without explicit HUMAN authorization.**

Konflik dengan keputusan LOCKED:

> **STOP → REPORT → HUMAN**
