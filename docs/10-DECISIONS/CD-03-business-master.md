# CD-03 — Single Company Master / Business Roles / Contact

Status: **LOCKED** (HUMAN CONFIRMED).

Sumber: keputusan HUMAN (revisi CD-03 eksplisit + otorisasi materialisasi Build Mode).
Sifat dokumen: transkripsi keputusan HUMAN. Tidak ada reinterpretasi substantif.
Kode, commit historis, schema SQLite, reverse-engineering Accurate 5, dan analisis
terdahulu tetap **reference/evidence**, bukan sumber keputusan.

## Company Master

`Company` adalah **satu identitas perusahaan kanonis**.

Company adalah identity/master, bukan giant table yang mencampur seluruh proses bisnis.

> Tidak membuat satu giant table yang mencampur seluruh data Customer + Vendor +
> Prospect + Contact + transaksi + pricing + accounting.

Identity disatukan, tetapi domain/business data tetap dapat dipisahkan.

## Business Roles

Company dapat mempunyai role:

* Prospect
* Customer
* Vendor

Prospect/Customer/Vendor adalah **business role/relationship**, bukan tiga master
identity perusahaan yang terpisah.

```text
COMPANY
   │
   ├── PROSPECT ROLE
   │
   ├── CUSTOMER ROLE
   │
   └── VENDOR ROLE
```

Satu Company dapat mempunyai role CUSTOMER dan VENDOR secara bersamaan.
Contoh:

```text
ABC
├── Customer Role
└── Vendor Role
```

Tidak boleh ada dua identity perusahaan independen (`Customer ABC` dan
`Vendor ABC`) sebagai pengganti satu Company identity.

## Contact / PIC

Contact/PIC adalah entitas terpisah dengan hubungan:

```text
Company
  └── Contact/PIC 1-N
```

Model mendukung, sesuai yang disepakati:

* multiple contacts
* PIC role/position
* primary/main contact
* communication history
* future customer access
* future vendor usage

Contact/PIC tidak digabungkan menjadi field-field Company.
RBAC detail tetap OPEN/FUTURE.

## Supersede

Keputusan sebelumnya — Customer dan Vendor sebagai dua master identity/list
terpisah — dinyatakan **SUPERSEDED** oleh satu Company Master kanonis dengan
Prospect/Customer/Vendor sebagai business roles.

Kedua arsitektur tidak dipertahankan bersamaan.

## Consequences

* Duplicate company identity dihindari; profil company konsisten.
* Role Customer/Vendor tetap domain-separated.
* Company yang sama dapat mempunyai beberapa business role.
* Contact/PIC tetap berada di level identitas Company dan dapat dipakai lintas role.
* Sales/Purchasing/ERP di masa depan dapat mereferensikan Company identity yang sama.

## Deferred / Open

* role-specific field detail
* Company numbering
* role codes
* Prospect → Customer transition rules
* migrasi/merge data existing
* detailed RBAC
* price/offer history
* PPN/tax treatment
* accounting integration

## Batas CD-03 (bukan bagian keputusan ini)

* vendor offer/acquisition price history
* price intelligence
* latest-5 vendor offers
* pricing visibility policy
* PPN/tax logic
* selling-price recommendation
* accounting logic

Item-item tersebut ditangani pada gate/workstream yang sesuai, khususnya CD-06
untuk price/offer history.

## Governance

> **A LOCKED decision may not be changed, weakened, expanded, or reinterpreted
> by AI Manager, AI Programmer, or AI Auditor without explicit HUMAN authorization.**

Jika ada konflik antara implementation evidence dan CD-03 LOCKED:

> **STOP → REPORT → HUMAN**
