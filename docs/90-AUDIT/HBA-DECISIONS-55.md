# IMPLEMENTASI — jarak pada pemilih teknisi, pembatalan lewat pop up, proses visit lengkap

```text
Record ID:      HBA-DECISIONS-55
Date:           2026-10-26
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Instruksi HBA:  "1. pada kolom pilih teknisi utama, email dan nama teknisi nempel.
                 sebaiknya berikan spasi.
                 2. ada tabel aksi. menurut saya, tidak perlu ada tabel ini. untuk
                 pembatalan, bisa dibuatkan tombol batal saja. baru begitu ada yang
                 mengklik pembatalan, muncul layar pop up, untuk memberikan
                 alasannya. serta sebagai konfirmasi jika tidak sengaja terpencet.
                 3. bagaimana saya bisa mengisi proses visit?"
Status:         IMPLEMENTED — terpasang, 25 cek peramban LULUS
Classification: Audit record. NOT a canonical specification document.
```

## Butir 1 — jarak pada pemilih teknisi

Baris pilihan teknisi dan chip teknisi terpilih sekarang berjarak jelas: alamat
Google, pemisah titik, lalu nama. Jaraknya diukur di peramban, bukan dikira-kira —
**7 px** pada daftar pilihan dan **10 px** pada chip yang sudah terpilih. Aturan
yang sama berlaku untuk kotak pencarian unit karena memakai kelas baris yang sama,
jadi tampilannya tetap konsisten.

## Butir 2 — pembatalan jadi satu tombol + pop up

Isian **"Alasan pembatalan"** yang tadinya menempel di panel Aksi **dihapus**. Yang
tersisa hanya satu tombol **"Batalkan WO"**. Menekannya membuka jendela pop up
berisi peringatan bahwa pembatalan bersifat terminal, isian alasan yang **wajib**,
serta dua tombol: **"Ya, batalkan WO"** (nonaktif selama alasan masih kosong) dan
**"Tidak, kembali"**. Jadi jendela itu sekaligus menjadi konfirmasi bila tombolnya
tersenggol — ditutup tanpa menekan konfirmasi, WO tidak berubah sama sekali
(diuji: status tetap IN_PROGRESS).

Tombol siklus hidup lain di panel yang sama — Buka WO, Mulai pekerjaan, Ajukan
persetujuan, Setujui laporan, Minta koreksi, Buka kembali — **tidak berubah**,
karena yang Anda maksud adalah isian pembatalan yang menempel, bukan tombol
sah lainnya.

## Butir 3 — cara mengisi proses visit, dan yang tadinya kurang

Rantainya sekarang lengkap di layar detail WO, berurutan:

| Langkah | Syarat | Yang terjadi |
|---|---|---|
| Tugaskan teknisi utama | WO belum punya PRIMARY | tersimpan di panel Penugasan (wajib beralasan) |
| **Mulai pekerjaan** | WO OPEN dan sudah ada PRIMARY | WO → IN_PROGRESS |
| **Buat Visit** | WO IN_PROGRESS | satu Visit dibuat sistem (tipe ditentukan sistem, bukan dipilih) |
| **Check-in** | Visit masih OPEN | waktu masuk tercatat + pembuat visit ditandai hadir |
| **Check-out** | sudah check-in | waktu keluar tercatat — **tombol ini baru ada sekarang** |
| **Selesaikan** | Visit masih OPEN | pilih hasil (COMPLETED / NOT_PERFORMED / ON_HOLD; dua yang terakhir wajib beralasan) lalu "Simpan hasil" |

Penyelesaian Visit **tidak** menutup WO — penutupan terjadi lewat persetujuan
laporan di panel Aksi.

Yang tadinya kurang: tabel Visit punya kolom **Check-out**, tetapi **tidak ada
tombolnya**, sehingga waktu keluar tidak pernah bisa dicatat. Endpoint-nya
(`POST /api/visits/<id>/check-out`) sudah ada sejak lama; perubahan ini hanya
memunculkan permukaannya, tanpa aturan bisnis baru.

## Temuan yang belum saya ubah (perlu keputusan HBA)

Waktu check-in dan check-out saat ini berasal dari **jam peramban** yang dikirim
layar, bukan dari server. Keputusan 2026-10-03 menetapkan jam teknisi = waktu
server, tanpa input manual. Memperbaikinya berarti domain memberi cap waktu
sendiri ketika tidak diberi nilai — itu perubahan perilaku backend, jadi saya
laporkan dulu, tidak saya kerjakan sendiri. Dampaknya nyata: jam perangkat yang
meleset akan tercatat sebagai waktu kerja.

## Bukti

`verify_visit_batal_picker_20261026.cjs` di deployment nyata (8092): **25 cek
LULUS**.

- Jarak terukur: chip 10 px, daftar pilihan 7 px.
- Panel Aksi tanpa isian alasan; satu tombol; pop up muncul; konfirmasi nonaktif
  saat alasan kosong; "Tidak, kembali" menutup dan WO tidak berubah.
- Rantai visit dijalankan sungguhan pada satu WO uji (unit MEBS-01, JOB nyata):
  Buat Visit → Check-in → Check-out → Selesaikan, dengan hasil di database
  `check_in_at 2026-10-26T12:09:38Z`, `check_out_at 2026-10-26T12:09:40Z`,
  `state COMPLETED`, `outcome COMPLETED`.
- Pembatalan sungguhan lewat pop up: WO uji berubah **CANCELLED** dengan
  `cancelled_reason` dan pelaku tercatat.
- Seluruh baris uji dihapus: hitungan DB kembali sama, nol referensi menggantung
  (7 WO, 3 penugasan nyata, 0 visit).
- 0 galat JavaScript; `npm run typecheck` bersih; bundle `index-DToPCUKu.js`
  disajikan `crm-ui.service`; kedua layanan aktif, `/healthz` 200.

## Berkas

`crm/ui/src/components/TechnicianPicker.tsx`, `crm/ui/src/screens/WoDetailScreen.tsx`,
`crm/ui/src/styles.css`, `crm/ui/verify_visit_batal_picker_20261026.cjs` (baru).

Tanpa migrasi, tanpa endpoint baru, tanpa aturan bisnis baru.
