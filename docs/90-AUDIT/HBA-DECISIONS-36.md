# HBA DECISION RECORD — tata letak kartu Unit + registri gambar merek/perlengkapan (2026-10-24)

```text
Record ID:      HBA-DECISIONS-36
Date:           2026-10-24
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — permintaan HBA via chat 2026-10-24; eksekusi berjalan
Classification: Audit record. NOT a canonical specification document.
Implementation: BERJALAN — migrasi v41 + halaman konfigurasi gambar + tata letak kartu Unit.
                Rekaman hasil ada di HBA-DECISIONS-37 setelah diverifikasi.
```

> Rekaman putusan HBA verbatim. Dokumen jejak, bukan spesifikasi.

## Permintaan HBA (verbatim)

> "tanggal dokumen dari tanggal di undah.
>
> Perubahan tampilan UI Unit,
> 1, Barcode di letakan di sebelah kanan tabel "kode unit"
> 2. tabel mesin sudah ok. tapi di buat tambahan ke kanan untuk logo mesin. sesuai dengan merk mesinnya. kemudian tabel generator di sebelahnya lagi, dan kemudian tabel logo generator sesuai dengan merek generatornya.
> 3. Tabel Panel dibuat sama seperti nomor 2. dengan logo dari merk controllernya. serta disampingnya label genset. dan logo dari merk gensetnya.
> 4. Terakhir Perlengkapan dibuat dibawah berupa 1 tabel dengan gambar mewakili perlengkapan yang ada. misal untuk Trailer, maka ada gambar trailer. lalu APAR, dan Fuel separator.
> 5. maka untuk menunjang no 4. buatkan satu halaman page lagi di konfigurasi untuk memasukan gambar yang mewakili perlengkapan tersebut."

## Yang diputuskan

**Tanggal dokumen pada Riwayat** = tanggal unggah berkasnya ("tanggal di undah"). Sudah terpasang:
`_enrich_history` mengisi `document_date` dari waktu unggah berkas WO; WO tanpa berkas tampil tanpa
penanda. Menutup pertanyaan terbuka yang saya angkat di HBA-DECISIONS-35.

**Kartu Unit (Profil Unit)** disusun ulang: barcode/QR portal pindah ke sebelah kanan baris kode
unit; logo merek mesin di sebelah kanan tabel Mesin, lalu tabel Generator, lalu logo merek
generator; pola yang sama untuk Panel (logo merek controller) dan Genset (logo merek genset);
Perlengkapan menjadi satu tabel berisi gambar tiap perlengkapan yang dicentang.

**Registri gambar** — halaman konfigurasi baru untuk mengunggah gambar yang mewakili merek dan
perlengkapan. Satu gambar per jenis+merek dan satu gambar per butir perlengkapan, per workspace;
unggahan berikutnya menggantikan yang lama, bukan menumpuk. Manager/Admin yang berwenang; peran
lapangan hanya membaca.

## Catatan audit (jujur, tanpa mengubah putusan)

Satu. **Sumber logo merek.** Permintaan nomor 5 menyebut halaman konfigurasi untuk gambar
PERLENGKAPAN. Logo merek (mesin/generator/controller/genset) tidak disebut sumbernya. Saya
menyatukan keduanya di halaman konfigurasi yang sama — satu tempat untuk semua gambar yang
melengkapi kartu Unit — dan sudah menanyakan penegasannya ke HBA lewat Telegram. Bila HBA
menghendaki logo merek diurus di tempat lain, yang berubah hanya halaman unggahnya, bukan skema.

Dua. **"Merk genset".** Tidak ada field merek genset di data unit hari ini (yang ada: merek mesin,
merek generator, merek module controller). Pembacaan sementara: logo GENSET dicocokkan dengan
merek MESIN, karena satu gabungan genset membawa merek mesinnya. Pemetaan ini sengaja diletakkan
di SATU fungsi supaya satu perubahan kecil cukup bila HBA memutuskan lain.

Tiga. **Label genset.** HBA menyebut "label genset" di samping tabel Panel; yang tersedia adalah
grup Genset (jenis enclosure, serial genset, speed, frequency, tegangan, baterai). Saya
menampilkan grup itu apa adanya — bukan label baru yang dikarang.

Empat. **Gambar yang belum ada tidak dikarang.** Sel logo/gambar tetap kosong sampai Manager/Admin
mengunggahnya; tidak ada gambar contoh, tidak ada placeholder palsu.

## Langkah berikut

Kerjakan migrasi v41 + modul registri gambar + rute internal, lalu tata letak kartu Unit dan
halaman konfigurasi. Setelah diverifikasi di peramban nyata, hasilnya dicatat di HBA-DECISIONS-37
dan dilaporkan ke HBA lewat Telegram (HBA sedang mematikan PC-nya).

*End of decision record.*
