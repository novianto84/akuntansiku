# HBA-DECISIONS-72 — Rombak detail WO: Work Progress, mulai otomatis, panggil via @

Tiga perintah HBA lewat chat 27 Okt 2026 untuk halaman detail WO: hapus tabel
Aksi dan pindahkan tombolnya, status mulai otomatis IN_PROGRESS saat teknisi
ditugaskan, tombol batal gabung ke tabel peninjauan yang diganti nama menjadi
Work Progress, dan tabel panggil internal di diskusi dihapus diganti panggilan
langsung "@".

## Yang dikerjakan

Panel Aksi dihapus. Semua tombol WO pindah ke panel Work Progress (nama baru
dari Cakupan peninjauan, isinya tetap): Buka WO saat DRAFT, Ajukan
persetujuan dan Ajukan ulang saat IN_PROGRESS atau koreksi, Setujui dan Minta
koreksi saat WAITING APPROVAL, Buka kembali saat CLOSED, dan Batalkan WO saat
OPEN atau IN_PROGRESS dengan pop up alasan seperti sebelumnya. Tombol Mulai
pekerjaan tidak ada lagi karena tidak dibutuhkan: penugasan PRIMARY kini
memindahkan OPEN ke IN_PROGRESS otomatis di backend, persis seperti yang
ditulis CD-11 §4 (bukan aturan baru). Jalur `start` di backend tetap ada
untuk kompatibilitas.

Di diskusi WO, blok Panggil rekan internal (kolom cari, dropdown, tombol
tambah) dibuang. Panggilan cukup ketik "@nama" di kotak pesan seperti
sebelumnya; nama yang terpanggil tetap terlihat sebagai chip yang bisa
dibatalkan sebelum dikirim.

Dua WO lama yang terjebak OPEN padahal sudah ber-PRIMARY (PAG/SPK/2025/017
dan PAG/SPK/2025/059, keadaan yang tidak bisa terjadi lagi) diselaraskan ke
IN_PROGRESS lewat jalur domain yang sah supaya tidak ada yang yatim tanpa
tombol mulai.

## Bukti

- `tests.test_assignment` 16 uji lolos, termasuk 4 uji baru perilaku otomatis
  (PRIMARY di OPEN jadi IN_PROGRESS, SUPPORTING tidak memicu, DRAFT tidak
  ikut, take-over memicu).
- `tests.test_wo.WOLifecycleTest` 7 uji lolos; alur uji yang masih menekan
  mulai manual disesuaikan ke otomatis.
- `tests.test_exec_server` 4 uji lolos; `tests.test_batch4` 5 uji lolos.
- Tiga uji lineage di `tests.test_wo` merah juga di pohon bersih tanpa
  perubahan ini (galat scope SR di setup uji, pra-ada) — bukan bawaan kerjaan
  ini.
- `npm run typecheck` bersih, bundle memuat Work Progress dan tidak lagi
  memuat tombol mulai atau tabel panggil, halaman tersaji sama dengan hasil
  build.
- Layanan `crm.service` dan `crm-ui.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `feat/wo-detail-rombak-20261027`, commit `a4bab59`,
  sudah push, belum merge. Yang berubah: `app/wo/assignment.py`,
  `tests/test_assignment.py`, `tests/test_wo.py`,
  `tests/test_exec_server.py`, `ui/src/screens/WoDetailScreen.tsx`,
  `ui/src/components/DiscussionPanel.tsx`.
