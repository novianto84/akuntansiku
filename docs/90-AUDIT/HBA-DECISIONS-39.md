# IMPLEMENTATION RECORD — tulisan barcode dihapus, latar gambar transparan

```text
Record ID:      HBA-DECISIONS-39
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruction:    pesan HBA 2026-10-24
Status:         IMPLEMENTED — terpasang, teruji di peramban, sudah di-push
Classification: Audit record. NOT a canonical specification document.
```

## Kata HBA yang dikerjakan

> "Tulisan di atas barcode, sebaiknya di hapus saja. Begitupun yang dibawah
> barcode.
> Lalu hapus background putih pada gambar. Biarkan gambar berlatar transparant."

## Yang diubah

Blok barcode/QR pada Profil Unit kini TIDAK memuat tulisan apa pun: judul di
atasnya ("Barcode / QR portal unit (kode acak)") dan tulisan kode/tautan di
bawahnya dihapus, dan keterangan URL yang ikut dicetak di bawah gambar juga
tidak lagi diminta. Keterangan itu tetap ada sebagai atribut `title` pada
bingkainya, jadi bloknya masih bisa dikenali saat ditunjuk tetikus tanpa
menambah tulisan di layar. Tombol "Cetak" dan "Unduh SVG" DIPERTAHANKAN karena
keduanya kendali, bukan tulisan; kalau HBA ingin itu ikut hilang, cukup
dikatakan.

Latar putih pada bingkai gambar dihapus — bingkai logo merek, bingkai gambar
perlengkapan, bingkai kotak-kotak galeri, pratinjau logo, dan pembungkus barcode.
Semuanya kini transparan, jadi gambarnya menyatu dengan latar halaman.

Satu hal yang sengaja TIDAK dihilangkan: latar putih di DALAM gambar QR itu
sendiri. QR Code butuh bidang terang di sekeliling modul gelapnya supaya bisa
dibaca pemindai dan kamera ponsel; kalau latar di dalam gambar ikut dihapus,
barcodenya berhenti berfungsi di halaman bertema gelap. Jadi: bingkainya
transparan, isi gambarnya tetap membawa bidang putihnya. Ini bukan bantahan
terhadap permintaan — keduanya memang berbeda, dan yang diminta HBA (latar
bingkai) sudah dituruti.

## Bukti

- 18/18 cek peramban nyata pada permukaan Profil Unit (`crm/ui/verify_unit_profile.mjs`),
  termasuk empat cek baru: tidak ada judul di atas barcode; tidak ada tulisan
  kode/tautan di dalam blok barcode; bingkai barcode terhitung transparan
  (`rgba(0, 0, 0, 0)`); keempat bingkai logo juga transparan; dan gambar QR tetap
  membawa latar putihnya sendiri serta tetap mengarah ke tautan portal unit yang
  benar (`#/portal-unit?code=AB12CD34EF`).
- 14/14 cek peramban halaman Galeri tetap lulus (regresi).
- `npm run typecheck` bersih; `npm run build` sukses; UI dijalankan ulang dan
  berkas baru sudah dilayani (port 8092 menjawab 200). Tidak ada perubahan backend
  pada putaran ini.

## Sisa

Commit `42194e8` pada branch `feat/wo-discussion-20261024`
(`github.com/novianto84/mitrasp-app`). Belum di-merge ke `main` — menunggu HBA.

*End of implementation record.*
