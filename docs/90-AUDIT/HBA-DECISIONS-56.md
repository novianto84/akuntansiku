# IMPLEMENTASI — detail Work Order menyebut pelanggan, PIC, dan nomor yang bisa dihubungi

```text
Record ID:      HBA-DECISIONS-56
Date:           2026-10-26
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruksi HBA:  "pada menu detail work order, tabel pertama work order itu mencakup
                 informasi nama perusahaannya, PIC, atau nama perorangannya. nomor
                 telp yg bisa di hubungi."
Status:         IMPLEMENTED — terpasang, 13 cek peramban LULUS
Classification: Audit record. NOT a canonical specification document.
```

## Bentuk yang dipasang

Tabel pertama pada detail Work Order sekarang **dibuka** dengan tiga baris
informasi pelanggan, di atas baris Unit:

| Baris | Isi | Sumber |
|---|---|---|
| **Pelanggan** | nama perusahaan pemilik Unit beserta kodenya | `companies` lewat `units.company_id` |
| **PIC** | nama kontak utama perusahaan + jabatannya | `contacts` (`is_primary`), cadangan kontak pertama perusahaan |
| **Nomor telepon** | nomor PIC (dan nomor kedua bila ada) sebagai **tautan WhatsApp** | `contacts.phone` / `phone2` |

Nomornya bisa langsung ditekan: tautan menormalkan angka `0…` menjadi `62…`
(`+62 888-1733-966` → `wa.me/628881733966`), sama seperti pintasan di menu Kontak.

**Bila Unitnya milik perorangan** (tanpa perusahaan), baris Pelanggan menampilkan
nama pemilik dengan penanda *non-perusahaan*, dan baris PIC memakai nama pemilik
itu dengan catatan "belum ada kontak tercatat" bila memang belum ada. Kontak
berdiri sendiri (tanpa perusahaan) hanya dipakai bila namanya **sama persis**
dengan nama pemilik Unit — tidak ada pencocokan yang dikarang.

**Bila Unitnya belum ditentukan**, baris Pelanggan menulis apa adanya "belum dapat
ditentukan — Unit belum dipilih", bukan nama pelanggan dari WO lain.

## Bukti

`verify_wo_pelanggan_20261026.cjs` di deployment nyata (8092): **13 cek LULUS**.

- Pada WO nyata **PAG/SPK/2025/77** (Unit MEBS-01 milik **Mensa Bina Sukses**):
  baris Pelanggan, PIC, dan Nomor telepon muncul; nama perusahaan benar; PIC
  **Agung**; nomor `+62 888-1733-966` menjadi tautan `https://wa.me/628881733966`.
- Urutan baris diukur dari teks panel: **Pelanggan → PIC → Nomor telepon → Unit**.
- Pada **WO-2026-008** yang Unitnya belum dipilih: tertulis "belum dapat
  ditentukan", dan tidak ada nama pelanggan yang menempel dari WO lain.
- 0 galat JavaScript; `npm run typecheck` bersih; bundle `index-BAJ0Jq7F.js`
  disajikan `crm-ui.service`.

## Berkas

`crm/ui/src/screens/WoDetailScreen.tsx` (membaca `companies` + `contacts` dan
menambah tiga baris Dl), `crm/ui/verify_wo_pelanggan_20261026.cjs` (baru).

Tanpa migrasi, tanpa endpoint baru, tanpa aturan bisnis baru — hanya menampilkan
data yang memang sudah tercatat.

## Catatan

Nama teknisi pada baris "Penanggung jawab" masih tampil sebagai `Pengguna #<id>`
karena detail WO tidak membawa direktori pekerja. Bila HBA ingin nama teknisi
tertulis di situ (bukan nomor id), itu satu langkah kecil berikutnya — sebutkan
saja.
