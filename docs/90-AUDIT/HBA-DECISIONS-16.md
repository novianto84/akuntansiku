# HBA DECISION RECORD — Kontak Unit Portal manual, link manual, panel dinamis (2026-10-11)

```text
Record ID:      HBA-DECISIONS-16
Date:           2026-10-11
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — decision as stated by HBA in chat 2026-10-11
Classification: Audit record. NOT a canonical specification document.
Implementation: No code/schema/migration/DB written by this record.
```

> Rekaman tangkap pernyataan HBA verbatim. Tak edit kanonik, tak tulis kode.

## Putusan HBA (inti)

HBA states: customer hanya signup dan tulis manual nama perusahaan. Form dikirim ke role manager. Siapkan panel dynamic agar HBA bisa rubah sendiri. Yang berwenang link manual. Selama belum link manual, customer hanya lihat portal unit.

Bacaan kunci:

- Signup Google, isi nama + nama perusahaan manual (teks bebas) + telepon. Email otomatis Google.
- Form masuk antrean manager.
- Link PIC manual oleh berwenang. Tanpa auto-approve, tanpa auto-elevate otomatis sistem.
- Sebelum link manual: scope UNIT_SCOPE saja, satu unit QR.
- Panel dinamis: HBA ubah sendiri tanpa programmer. Isi panel belum rinci (field form / antrean / aturan link). Tetap OPEN sampai HBA rinci.

## Kondisi nyata (terverifikasi)

- `contacts` ada nama/posisi/telepon/email, `company_id NOT NULL`. Tak ada kolom nama-perusahaan-teks-bebas, asal Google, unit QR.
- `identity_links` kunci unik identitas+perusahaan, PENDING VERIFIED REVOKED, tanpa auto-approve.
- Tanpa endpoint publik. Tanpa panel dinamis. Panel konfigurasi (E-56) masih OPEN, belum bangun.
- Spec IS-06 v1.2 / IS-03 v1.2 kunci tiga tier, selaras HBA-13.

## Batas

- Record tak cipta tabel/endpoint/panel. Eksekusi via governed path perlu otorisasi paket tulis terpisah.
- Detail panel dinamis belum putus: objek apa HBA ubah.
- Tanpa coding/skema/migrasi tanpa perintah eksekusi eksplisit.

## Langkah berikut termurah

Rinci panel dinamis (satu kalimat: objek ubah), lalu otorisasi paket eksekusi kontak.

*End of decision record.*
