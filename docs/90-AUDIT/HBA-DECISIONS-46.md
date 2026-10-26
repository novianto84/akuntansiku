# MERGE KE main + daftar merek genset dari HBA

```text
Record ID:      HBA-DECISIONS-46
Date:           2026-10-25
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Putusan HBA:    "branch di commit dan di merge."
                "merk genset = FG Wilson, AKSA, POWERLINK, HARTECH, BAIFA."
                "urutan name plate tidak masalah panel dulu baru genset."
                "type genset tidak perlu ada."
Status:         DONE — main sudah memuat seluruh rangkaian, terverifikasi pasca-merge
Classification: Audit record. NOT a canonical specification document.
```

## Satu: branch di-merge ke main

Seluruh pekerjaan branch `feat/wo-discussion-20261024` di-merge ke `main` sebagai
satu merge commit `c23bb60` (bukan fast-forward, supaya batas rangkaiannya
kelihatan di riwayat), lalu di-push. Keadaan sebelum merge ditandai
`archive/main-pre-merge-20261025` sehingga bisa dibandingkan atau dikembalikan.
Sesudah merge: `main` memuat semua commit branch, dan branch tidak menyimpan
satu pun commit yang belum masuk `main`.

Dua commit dokumen yang sudah ada di `main` sebelum merge (charter organisasi AI
dan kebijakan operasi GitHub) ikut terbawa dan tidak bertabrakan — keduanya
menyentuh berkas yang berbeda.

**Catatan tata kelola yang saya sampaikan terbuka:** kebijakan LOCKED di repo
(`docs/GITHUB-OPERATIONS-AND-CHANGE-AUTHORITY.md` §8) menyebut merge gate
termasuk "independent audit ... where required". Saya yang menulis perbaikan ini,
jadi saya BUKAN auditor independen untuknya: yang saya lakukan adalah verifikasi
sendiri (tes otomatis + peramban nyata) sebelum dan sesudah merge, bukan audit
pihak ketiga. HBA memberi otorisasi merge secara eksplisit, dan itu yang saya
jalankan. Bila HBA ingin pintu audit independen tetap tertutup rapi, langkah
termurah: satu putaran audit baca-saja oleh auditor terpisah (mis. Manus) atas
`main` pasca-merge — tidak menghalangi pemakaian aplikasi sekarang.

## Dua: daftar merek genset

Lima merek yang HBA sebutkan dipasang sebagai daftar saran isian untuk field
"Merk genset", **apa adanya dan dalam urutannya**: `FG Wilson`, `AKSA`,
`POWERLINK`, `HARTECH`, `BAIFA`. Saran isian tetap ADVISORY — field-nya tetap
teks bebas dan backend tetap menerima nilai apa pun; kapitalisasi "FG Wilson"
sengaja tidak diubah karena itu kosakata HBA, sedangkan nilai yang TERSIMPAN
tetap kapital seperti field namaplate lain ("FG WILSON").

Nilai yang sudah tercatat pada unit otomatis ikut menjadi saran, dan tidak
menggandakan entri daftar HBA yang sama (penggabungannya tidak membedakan huruf
besar/kecil, dan ejaan HBA yang menang).

## Tiga: dua hal yang TIDAK dikerjakan (karena HBA menyatakan tidak perlu)

- Urutan baris kedua namaplate tetap **Panel lalu Genset** — HBA: "urutan name
  plate tidak masalah panel dulu baru genset."
- **Tidak ada** field "Type genset" — HBA: "type genset tidak perlu ada."

## Bukti pasca-merge (pada sistem yang berjalan, bukan pada kode saja)

- `main` = `c23bb60`; `git rev-list --left-right --count origin/main...feat/...`
  = `3 0` (tidak ada commit branch yang tertinggal).
- UI dibangun ulang dari `main` (bundel `index-B-An3M54.js`) dan backend
  dijalankan ulang; ketiga layanan aktif dan `/readyz` menjawab `ready`.
- Permintaan nyata ke backend yang berjalan:
  `GET /api/unit/spec-options?kind=genset_brand` →
  `["FG Wilson", "AKSA", "POWERLINK", "HARTECH", "BAIFA"]`, urutannya sama dengan
  yang HBA tulis.
- Skema basis data tetap **42** (tidak ada migrasi baru pada putaran ini) dan
  `genset_brand` pada unit yang ada masih kosong — tidak ada nilai yang dikarang.
- 86 tes otomatis pada empat modul terkait dijalankan ULANG pada `main`
  pasca-merge (hasilnya dicatat di laporan chat; 8 tes katalog saran isian
  termasuk dua tes baru untuk daftar merek genset).

## Yang masih menunggu HBA

Lima merek sudah tersedia sebagai saran, tetapi **pemetaan merek ke unit** masih
milik HBA: di basis data ada enam unit (U-GS-001/002/003 dan MADI-01/02/03),
sedangkan merek yang disebut lima. Saya tidak menebak mana unit memakai merek
mana. Bila HBA menyebut pasangannya (mis. "MADI-01 = FG Wilson, MADI-02 = AKSA,
…"), saya isikan, lalu slot logo untuk merek itu muncul di halaman Galeri untuk
diunggah gambarnya.

Commit `c23bb60` pada `main` (`github.com/novianto84/mitrasp-app`).

*End of record.*
