# HBA DECISION RECORD — ruang diskusi, galeri SR/WO, urutan riwayat, data penyerahan unit (2026-10-24)

```text
Record ID:      HBA-DECISIONS-30
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA via chat 2026-10-24, menjawab lima pertanyaan
                terbuka di HBA-DECISIONS-29. Sisa pertanyaan kecil: bagian "Masih terbuka".
Classification: Audit record. NOT a canonical specification document.
Implementation: No code, schema, migration or DB written by this record.
                Tidak ada dokumen kanonik yang diubah.
```

## Putusan HBA (verbatim)

> "Ruang diskusi memang terbatas hanya di setiap WO saja. atau di setiap unit. mana yang
> memungkinkan? agar setiap WO, jelas percakapannya. bisa memanggil pekerja dengan men tag
> si pekerja. maka perlu semacam inbox atau bentuk notifikasi di pekerja masing masing.
>
> Mengenai Galery / Dokumen. saya rasa di adakan saja. di SR maupun di WO. jika perlu
> dibuatkan tabel sendiri lagi, dan di relasikan ke unit. nantinya bisa di pasang juga
> galery tersebut di portal pelanggan.
>
> Mengenai bukti itu melekast di WO atau Visit, Visit adalah bagian dari WO. jadi menurut
> saya sama saja. tidak ada pekerjaan visit yang tanpa WO.
>
> saya setuju dengan peristiwa jadi urutan dasar, tanggal dokumen jadi penanda.
> Dokumen yang di upload belakangan akan ada di grup WO. namun di urutan terakhir,
>
> Ruang diskusi hanya bisa dilihat oleh internal. tidak boleh keluar. dan hanya berupa catatan.
>
> Sertifikat dan manual book, galery image. boleh dilihat portal pelanggan.
>
> Induk pekerjaan itu berupa WO, atau SR, atau mungkin nanti akan ada lagi.
>
> lalu buat juga tambahan di data genset.
> Referensi nomor Invoice / Project / SPK
> Tanggal Penyerahan unit dan diberikan field lampiran dokume / image.
> tiga hal ini tidak dicantumkan di portal pelanggan"

## Putusan yang terekam

**Ruang Diskusi.** Terbatas pada Work Order (bukan ruang bebas tingkat unit); hanya
internal, tidak boleh keluar ke pelanggan; isinya **catatan**, bukan perintah kerja dan
bukan persetujuan; pekerja dapat dipanggil dengan sebutan nama (tag); tag menimbulkan
pemberitahuan pada pekerja yang disebut, sehingga dibutuhkan kotak masuk per pekerja.

**Galeri / Dokumen.** Diadakan di SR maupun WO. Boleh berupa tabel tersendiri yang
direlasikan ke unit. Galeri boleh dipasang juga di portal pelanggan.

**Bingkai bukti.** HBA menyatakan Visit adalah bagian dari WO sehingga bingkai WO
dianggap setara. AI: disarankan tetap mencatat Visit di titik pengambilan bukti agar
tidak ada informasi yang hilang (lihat Catatan audit).

**Urutan Riwayat.** Peristiwa menjadi urutan dasar, tanggal dokumen menjadi penanda.
Dokumen yang diunggah belakangan masuk ke grup WO-nya dan berdiri di urutan terakhir.

**Visibilitas dokumen unit.** Sertifikat, manual book, dan gambar unit boleh dilihat
portal pelanggan.

**Induk dokumen lampiran.** WO, SR, dan kemungkinan jenis induk baru di masa depan.

**Tambahan data unit (genset), tidak dicantumkan di portal pelanggan:**
referensi nomor Invoice / Project / SPK; tanggal penyerahan unit; dan lampiran
dokumen atau gambar penyerahan.

## Catatan audit AI Manager (jujur, tanpa mengubah putusan)

Satu. **Menyimpan Visit di titik pengambilan bukti tidak bertentangan dengan putusan HBA.**
Bingkai tampilan boleh WO, tetapi bila foto tidak menyimpan Visit asalnya, pertanyaan
"foto ini dari kunjungan yang mana" tidak bisa dijawab. Kanon IS-05 §4 memang menetapkan
satu artefak melekat pada tepat satu Visit. Menambahkan penanda Visit di titik unggah
justru menyelaraskan kode dengan kanon, tanpa mengubah tampilan yang HBA pilih.

Tiga. **Diskusi internal berarti semua peran internal atau sebagian?** Sales dan
Coordinator tidak berhak melihat data pribadi pekerja (KTP, NPWP). Bila semua peran
internal boleh membaca diskusi, satu pesan bisa memindahkan data terlindungi ke ruang
yang lebih terbuka. Perlu satu kalimat HBA.

Empat. **Berkas yang tampil di portal pelanggan butuh penentu.** Kanon IS-05 §7
menyatakan teknisi tidak pernah memilih visibilitas; kurasi dilakukan peninjau
(Manager/Admin). Jadi sertifikat/manual/gambar sebaiknya punya penanda terbitan yang
diubah Manager/Admin, bukan otomatis tampil begitu diunggah. Bila HBA ingin pengunggah
boleh langsung menerbitkan, itu perubahan aturan dan harus disebut eksplisit.

Lima. **Tiga hal penyerahan unit memakai kolom apa?** "Referensi nomor Invoice / Project
/ SPK" bisa berarti tiga kolom terpisah atau satu kolom bebas. Usulan AI: tiga kolom
terpisah, karena ketiganya dipakai berbeda saat penelusuran.

Enam. **Batas teknis pemberitahuan.** Kotak masuk di dalam aplikasi bisa dikerjakan
tanpa layanan luar. Bila pemberitahuan perlu sampai ke WhatsApp pekerja, itu
menyentuh layanan di luar CRM dan butuh keputusan tersendiri.

## Masih terbuka (butuh satu kalimat HBA)

a. Diskusi WO: boleh dibaca semua peran internal, atau hanya pekerja yang terlibat WO itu?
b. Pemberitahuan tag: cukup kotak masuk di aplikasi, atau harus sampai WhatsApp pekerja?
c. Penanda "tampil di portal pelanggan": hanya Manager/Admin yang mengubah, atau
   pengunggah boleh menandai sendiri?
d. Referensi Invoice / Project / SPK: tiga kolom terpisah (usulan AI) atau satu kolom bebas?

## Langkah berikut termurah

Kerjakan revisi tampilan arah D memakai putusan di atas (murni tampilan, tanpa skema).
Skema dan kanon tetap belum disentuh sampai HBA memberi otorisasi implementasi tersendiri.

*End of decision record.*
