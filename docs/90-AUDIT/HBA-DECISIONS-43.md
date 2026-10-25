# IMPLEMENTASI — baris namaplate Profil Unit: gambar dulu, baru data teknis

```text
Record ID:      HBA-DECISIONS-43
Date:           2026-10-25
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruksi HBA:  "saya mau rubah posisi tabel, jadi gambar dulu, baru data teknis
                 mesin, gambar logo, data teknis generator. begitupun juga baris
                 data genset dan data panel"
Status:         IMPLEMENTED — terpasang, teruji di peramban, sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Kata HBA yang dikerjakan

Tata letak baris namaplate di permukaan **Profil Unit** dibalik: dulu tiap pasangan
menulis DATA TEKNIS lebih dulu lalu bingkai logonya di kanan; sekarang **bingkai
gambar berdiri lebih dulu di kiri**, baru data teknisnya. Tidak ada isi, field,
urutan field, maupun aturan bisnis yang berubah — hanya posisi sel di layar.

## Bentuk yang dipasang

| | Kiri ke kanan | |
|---|---|---|
| Baris 1 | `[bingkai logo merek mesin]` | `MESIN` + data teknisnya |
| | `[bingkai logo merek generator]` | `GENERATOR` + data teknisnya |
| Baris 2 | `[bingkai logo merek controller]` | `PANEL` + data teknisnya |
| | `[bingkai logo merek genset]` | `GENSET` + data teknisnya (termasuk Battery/Accu, No. SPK/Invoice/Kontrak, Tanggal penyerahan unit) |

Judul grup dan urutan data teknis di dalamnya **tidak diubah**: Mesin lalu
Generator, Panel lalu Genset. Perlengkapan tetap satu baris memanjang di bawah.

## Yang diubah (tiga berkas, tanpa perubahan backend)

- `ui/src/components/UnitSpecCard.tsx` — sel bingkai logo dirender sebelum grup
  data teknisnya; komentar berkas disesuaikan dengan permintaan ini.
- `ui/src/styles.css` — kolom grid baris namaplate dibalik: `128px` di kiri
  (bingkai), lalu kolom data. Pada layar ≤1180px susunan dua kolomnya juga
  dibalik, jadi bingkai tetap di kiri datanya; layar sempit (≤820px) tetap satu
  kolom (bingkai di atas datanya).
- `ui/verify_unit_profile.mjs` — tambahan pemeriksaan untuk urutan baru (lihat
  catatan "Bukti" soal dua perbaikan skrip di bawah).

## Bukti (angka nyata, bukan perkiraan)

**29/29 cek peramban sungguhan** (`crm/ui/verify_unit_profile.mjs`, Chromium
headless, login nyata ke backend admin, unit MADI-03 yang memang membawa data
nyata: merek CUMMINS/STAMFORD/DEEPSEA, tiga perlengkapan, dan tiga logo merek
terunggah). Enam cek di antaranya baru, khusus untuk putaran ini:

- susunan DOM tiap baris: `gambar > data > gambar > data` — untuk KEDUA baris;
- urutan data teknis tetap `Mesin, Generator` dan `Panel, Genset`;
- posisi mendatar nyata (piksel): `271 < 413 < 851 < 993` di kedua baris —
  bingkai benar-benar di kiri datanya, bukan hanya di DOM;
- bingkai dan datanya **sebaris** (`top` identik: 505 dan 672) — tidak turun ke
  bawah;
- lebar kolom bingkai `128px` untuk keempatnya.

Cek lama yang tetap lulus memastikan tidak ada regresi: empat bingkai hanya
bingkai (tanpa tulisan pengganti), bingkai transparan, blok QR tanpa tulisan dan
tanpa tombol, QR tetap mengarah ke tautan portal unit yang benar, dan
perlengkapan tetap satu baris memanjang.

Bukti visual: potret baris namaplate dari peramban nyata pada unit tersebut
(Lampiran `unit-nameplate.png`) — terlihat bingkai CUMMINS di kiri `MESIN`,
STAMFORD di kiri `GENERATOR`, DEEPSEA di kiri `PANEL`, dan bingkai kosong di kiri
`GENSET`.

`npm run typecheck` bersih; `npm run build` sukses (bundel baru
`index-Dy6iCdLo.js` / `index-BLRsQnFQ.css`); UI statis di 8092 sudah melayani
bundel baru (hash pada index.html = bundel di disk). **Tidak ada perubahan
backend** pada putaran ini.

## Dua catatan yang perlu HBA ketahui (bukan bagian permintaan)

- **Baris kedua tetap Panel lalu Genset.** HBA menyebut "baris data genset dan
  data panel" tanpa menyatakan urutannya, dan yang diminta adalah "begitupun
  juga" — yaitu gambar-dulu — maka urutan datanya saya biarkan seperti sekarang.
  Kalau yang dimaksud juga menukar posisi Genset ke kiri Panel, itu satu baris
  perubahan; cukup dikatakan.
- **Skrip pemeriksa lama ternyata menunjuk data yang sudah tidak ada.** Skrip itu
  membuka unit id 1 dan membandingkan QR-nya dengan kode tetap `AB12CD34EF`.
  Unit 1 sekarang tidak punya satu pun field spesifikasi, logo, maupun
  perlengkapan, dan kode `AB12CD34EF` tidak ada di basis data mana pun — jadi
  delapan cek lama gagal bukan karena perubahan ini. Skrip saya arahkan ke unit
  yang memang membawa data (id 35, bisa ditimpa lewat `UNIT_ID=...`) dan cek QR
  kini membandingkan dengan **kode yang benar-benar diterbitkan server** untuk
  unit itu (`A4KZV7MAJG`), bukan angka tetap. Satu cek lama yang menuntut "tepat
  satu" perlengkapan bergambar juga dilonggarkan menjadi "sekurangnya satu",
  karena datanya sekarang dua gambar — jumlah gambar adalah isi data, bukan
  perilaku yang sedang diuji. Tidak ada cek yang dihapus.

## Kebersihan

Tidak ada data HBA yang disentuh: tidak ada baris basis data, tidak ada unggahan,
tidak ada berkas gambar yang ditulis pada putaran ini. Potret bukti dan skrip
potretnya ada di luar repo (direktori sementara), sehingga tidak ada berkas uji
yang tertinggal di repositori.

Commit `9b2c063` pada branch `feat/wo-discussion-20261024`
(`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main` — menunggu HBA.

*End of implementation record.*
