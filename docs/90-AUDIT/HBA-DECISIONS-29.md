# HBA DECISION RECORD — revisi tampilan detail arah D + tiga perubahan kanonik (2026-10-24)

```text
Record ID:      HBA-DECISIONS-29
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — permintaan HBA via chat 2026-10-24; audit AI Manager dilampirkan;
                sebagian item menunggu jawaban HBA (bagian "Pertanyaan terbuka")
Classification: Audit record. NOT a canonical specification document.
Implementation: No code, schema, migration or DB written by this record.
                Tidak ada dokumen kanonik yang diubah.
```

> Rekaman ini menangkap permintaan HBA verbatim beserta audit AI Manager.
> Permintaan HBA = otorisasi bisnis. Perubahan dokumen kanonik (IS-01/IS-05/IS-07)
> belum dilakukan karena menunggu jawaban atas pertanyaan terbuka di bawah.

## Permintaan HBA (verbatim)

> "Sepertinya saya tertarik versi D. namun dengan beberapa revisi.
> 1. profil utama pada sub menu menjadi "Profil Unit" berisikan marge dari (tentang, nameplate, dan perlengkapan).
> 2. sub menu kedua "Riwayat" berisikan histori setiap aktifitas. berurutan berdasarkan tanggal dokumen utamanya. dan di setiap dokument tersebut, detail berkas dan pekerjaan terekam disana.
> 3. sub menu ke 3. "Ruang Diskusi" Berisikan percakapan dari setiap pekerja. dalam bentuk desain seperti forum
> 4. sub menu ke 4. "Galery & berkas" berisikan kumpulan gambar2 dari pekerjaan tersebut. dipisahkan per aktifitas. serta di berikan tambahan 1 kolom di sisi kiri. berisikan dokumen yang di upload.
> 5. Saya jelaskan sedikit, ada 2 type dokumen. yang pertama yang ikut dilampirkan di setiap induk dokumen, misal di lampirkan di WO / SR. dan ada yang di lampirkan langsung ke unitnya. untuk yang dilampirkan ke unitnya, tersedia di kolom sisi kiri. rencananya ini nanti berupa dokumen mesin seperti certificate, manual book, dan gambar2 unit. sementara yang dilampirkan di setiap induk dokumen, ada di kolom utama. di bingkai dengan setiap nomor induk Pekerjaan."
>
> "ini pasti mengubah kanonik. saya yang meminta. jadi sama saja dengan saya mengijinkan.
> namun kamu perlu memberikan saya opini jujurnya. dan anda perlu mengaudit setiap
> permintaan saya ini yang merubah kanonik, untuk memberikan saya penjelasan, pro dan
> cons nya. serta apakah memungkin atau tidaknya."

## Audit per permintaan

### 1. "Profil Unit" = gabungan Tentang + Namaplate + Perlengkapan

**BISA, bukan perubahan kanonik.** Susunan layar tidak diatur kanon; yang diatur
adalah isinya (namaplate 20 isian + 8 perlengkapan, sudah dikunci HBA). Konsekuensi:
satu halaman menjadi panjang. Saran: pengelompokan berjudul (Mesin / Generator /
Panel / Genset / Perlengkapan), bukan penggabungan rata. Field kosong tetap
ditampilkan kosong, bukan dikarang.

### 2. "Riwayat" = histori per aktivitas, urut tanggal dokumen induk

Kondisi terverifikasi: riwayat operasional hari ini per Work Order —
`app/exec/history.py`, `operational_history(conn, user_id, wo_id)`; uji
`tests/test_history.py` ("one operational history", "contextual views share one
history"). Riwayat tingkat Unit sebagai **gabungan** diperbolehkan kanon
**IS-05 §8** (agregasi lewat rantai WO, tanpa gudang salinan baru) — jadi tidak
perlu tabel baru.

Titik gesek: **IS-07 §4–5 (LOCKED)** menetapkan urutan peristiwa sebagai dasar
kebenaran (append-only, aktor + waktu server). Mengurutkan ulang berdasarkan
tanggal dokumen induk dapat menghasilkan urutan yang berbeda dari urutan peristiwa.
Butuh keputusan HBA: mana yang mengikat, dan apa yang terjadi bila dokumen
bertanggal lama diunggah belakangan.

### 3. "Ruang Diskusi" (forum pekerja)

**Belum ada di kanon maupun di sistem.** DB produksi 44 tabel, tidak ada tabel
pesan/komentar/diskusi. Tidak ada entitasnya di IS-01, tidak ada keluarga peristiwa
audit-nya di IS-07.

Ini modul baru: butuh keputusan soal siapa boleh menulis/melihat, batas terhadap
catatan resmi (diskusi bukan persetujuan dan bukan perintah kerja), perlindungan
data pribadi pekerja (KTP/NPWP tidak boleh tercampur ke ruang umum), retensi, dan
penegasan diskusi bukan bagian audit (IS-07 §2: satu pemilik definisi audit).
Biaya: skema + izin + tampilan + uji. Risiko terbesar: percakapan dianggap perintah
kerja, dan data terlindungi bocor ke ruang umum.

### 4. "Galery & berkas" dua kolom

Kolom kiri **sudah ada** — `unit_documents` (0 baris) dan `unit_photos` (3 baris) di
DB produksi, dengan modul `app/unit/media.py` (upload: Manager/Sales/Technician/
Admin/Coordinator; hapus: Manager/Admin). Galeri unit belum disajikan ke portal
pelanggan (tidak ada di `app/customer/serving.py` maupun `PortalUnitScreen.tsx`) —
hari ini internal saja.

Yang belum ada: lampiran pada Service Request (tidak ada tabelnya) dan pengelompokan
galeri per aktivitas. Foto pekerjaan hari ini tersimpan di tingkat WO (`wo_photos`,
1 baris, punya `photo_type` + `approval_state`).

### 5. Dua jenis dokumen (lampiran induk vs lampiran unit)

Jenis kedua (lampiran unit: certificate, manual book, gambar unit) **sudah punya
rumah** di skema. Yang belum ada: kolom jenis dokumen pada `unit_documents`
(`doc_type` hanya ada di `staff_documents`). Menambah taksonomi jenis dokumen di luar
lantai terkunci **IS-05 §6** — di kanon ditandai OPEN (OQ-05) — adalah keputusan
bisnis HBA, bukan keputusan AI.

Jenis pertama (lampiran pada dokumen induk) sebagian sudah ada untuk WO
(`wo_photos`), **belum ada untuk SR**.

### Temuan lintas item (GAP kanon vs implementasi — belum diselesaikan)

**IS-05 §3–4 (LOCKED)** menetapkan evidence dikumpulkan di **Visit** dan satu artefak
melekat pada tepat satu Visit. Implementasi hari ini menyimpan foto di tingkat **WO**
(`wo_photos.work_order_id`, tidak ada `visit_id`). Permintaan "dibingkai dengan nomor
induk Pekerjaan" karena itu harus memilih: tetap bingkai WO (realitas implementasi)
atau selaraskan ke Visit (bunyi kanon). Perbedaan ini sudah ada sebelum permintaan ini
dan belum diputuskan.

## Pertanyaan terbuka untuk HBA

a. Urutan Riwayat: peristiwa sebagai urutan dasar dengan tanggal dokumen sebagai
   penanda — setuju? Bila dokumen bertanggal lama diunggah belakangan, histori
   melompat ke posisi tanggalnya atau tetap di posisi unggah?
b. Ruang Diskusi: siapa boleh menulis dan melihat (semua peran internal, pelanggan
   dan PIC dikecualikan?), dan apakah diskusi boleh menjadi dasar perintah kerja atau
   murni catatan?
c. Dokumen unit (certificate/manual/gambar): internal saja seperti hari ini, atau
   juga boleh dilihat pelanggan lewat portal?
d. Bingkai lampiran: tingkat WO (seperti sistem sekarang) atau tingkat Visit (seperti
   IS-05)? Dan jenis dokumen unit apa saja yang Anda inginkan?
e. "Induk Pekerjaan" yang Anda maksud = nomor WO saja, atau termasuk SR?

## Langkah berikut termurah

Jawab lima pertanyaan di atas dalam satu pesan; setelah itu revisi mockup arah D dapat
dikerjakan (murni tampilan), sementara perubahan kanon IS-01/IS-05/IS-07 menunggu kata
kunci otorisasi tersendiri karena mengubah lantai yang sudah terkunci.

*End of decision record.*
