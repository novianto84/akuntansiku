# IMPLEMENTATION RECORD — halaman Galeri Logo & Perlengkapan

```text
Record ID:      HBA-DECISIONS-38
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruction:    pesan HBA 2026-10-24
Status:         IMPLEMENTED — terpasang, teruji di peramban, sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Kata HBA yang dikerjakan

> "Untuk melampirkan gambar logo, saya rasa tidak nyaman harus ketik dulu.
> Mengapa tidak dibuatkan page khusus untuk galeri berdasarkan logo masing2. Dan
> perlengkapan."

## Yang diubah

Unggahan gambar aset tidak lagi berupa formulir di dalam halaman Pengaturan.
Sekarang ada halaman tersendiri, **Galeri Logo & Perlengkapan**, pada menu Master
Data, dan di dalamnya TIDAK ADA satu pun isian teks atau pilihan yang harus diisi
sebelum mengunggah:

- Kotak **logo merek** lahir dari merek yang sudah tercatat pada unit-unit di
  workspace ini ("Merk mesin" → Mesin, "Merk generator" → Generator, "Merk module
  controller" → Panel, sesi Genset → Genset). Pemetaannya memakai fungsi yang sama
  dengan kartu Unit (`brandForUnit`), jadi kotak di galeri tidak mungkin berbeda
  dari yang dicari kartu Unit.
- Kotak **perlengkapan** memakai daftar tertutup yang sama dengan centang pada unit
  (delapan butir, semuanya selalu tampil).
- Tiap kotak: satu tombol memilih berkas ("Unggah gambar" / "Ganti gambar") dan satu
  tombol "Hapus" bila gambarnya sudah ada. Jumlah unit yang memakai sebuah merek
  ikut ditulis kecil di bawah nama merek.

Halaman Pengaturan tidak lagi memuat formulir unggah itu — di sana hanya ada satu
keterangan yang menunjuk ke halaman galeri, supaya tidak ada dua permukaan unggah
yang bisa berbeda diam-diam (komponen lama `UnitAssetsSettings.tsx` dihapus).

## Satu temuan yang diperbaiki di tengah jalan

Percobaan pertama memperlihatkan gambar tersimpan tetapi kotaknya tetap kosong.
Penyebabnya nyata: daftar gambar aset sengaja dikirim **tanpa** isi gambarnya
(metadata saja), sehingga halaman pengelolaan tidak mungkin menampilkan apa yang
tersimpan. Diperbaiki dengan menambah opsi pada rute yang SUDAH ada —
`GET /api/unit-assets?with_data=1` — yang menyertakan gambar hanya bila diminta.
Pemanggil lama tetap menerima daftar metadata seperti sebelumnya, jadi muatan
mereka tidak ikut membengkak. Selain itu baris balikan unggahan langsung dipakai
layar, sehingga kotaknya berubah seketika tanpa menunggu daftar dibaca ulang.

Wewenang tidak berubah: Manager/Admin, dijaga di backend seperti sebelumnya. Peran
lain hanya melihat keterangan.

## Bukti

- 14/14 cek peramban nyata (`crm/ui/verify_gallery.mjs`): menu galeri ada; halaman
  terbuka; **nol** isian teks dan **nol** pilihan di halaman; dua belas pemilih
  berkas (tiga kotak merek + satu kotak genset + delapan butir perlengkapan); kotak
  merek lahir dari merek pada unit (CUMMINS, STAMFORD, DEEP SEA); delapan kotak
  perlengkapan tampil; memilih berkas langsung pada kotak menyimpan gambarnya
  (tombol berubah menjadi "Ganti gambar"/"Hapus"); dan gambar itu langsung tampil di
  bingkai merek pada Profil Unit tanpa tulisan apa pun di dalam bingkai.
- 14/14 cek peramban permukaan Profil Unit tetap lulus (regresi record sebelumnya).
- 46 tes otomatis gambar aset & perlengkapan lulus (rute lama tetap kompatibel).
- `npm run typecheck` bersih; `npm run build` sukses; backend dan UI dijalankan
  ulang; rute galeri menjawab 401 tanpa sesi (bukan terbuka).

## Batas yang perlu HBA ketahui

- Kotak logo muncul dari merek yang **sudah tercatat pada unit**. Merek yang belum
  pernah dicatat tidak punya kotak — begitu mereknya diisi pada sebuah unit, kotaknya
  muncul sendiri. Ini disengaja supaya tidak ada daftar merek tandingan yang harus
  dipelihara terpisah.
- Commit `af3cfbe` pada branch `feat/wo-discussion-20261024`
  (`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main` — menunggu HBA.

*End of implementation record.*
