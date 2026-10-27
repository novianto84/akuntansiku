# HBA-DECISIONS-63 — Teknisi utama PAG/SPK/2026/018 diganti ke Adi Setiawan

HBA lewat chat 27 Okt 2026: admin tidak bisa mengubah teknisi, dan teknisi
utama WO PAG/SPK/2026/018 diminta diganti ke Adi Setiawan.

## Temuan

WO id 27 (PAG/SPK/2026/018, OPEN) tadinya ber-teknisi utama Andi Kurniawan
(id 17). Adi Setiawan (id 16, xwa@123.com) memang terdaftar sebagai Technician
aktif. Aturan backend `ASSIGN_WO_ROLES` hanya mengizinkan Manager dan
Coordinator menugaskan, jadi akun Admin (Novianto, id 12) ditolak saat
menekan penugasan — itu bukan bug layar, melainkan otoritas yang memang belum
diberikan ke Admin. Layar juga tidak punya tombol lepas-ganti PRIMARY, jadi
pergantian ini dikerjakan lewat fungsi domain resmi.

## Yang dikerjakan

Dua langkah lewat `app.wo.assignment` dengan pelaksana akun Manager (id 1)
dan alasan tercatat atas perintah HBA: lepas Andi Kurniawan (assignment id 14
terhapus), lalu tetapkan Adi Setiawan sebagai PRIMARY (assignment id 19).
Alasan dan pelaku tercatat di baris penugasan. Tidak ada perubahan skema,
tidak ada perubahan kode.

## Bukti

- Baris akhir WO 27: satu PRIMARY yaitu id 16 Adi Setiawan, pelaku 1.
- Tidak ada PRIMARY ganda.

## Masih terbuka

- Apakah Admin perlu wewenang menugaskan teknisi secara umum, atau cukup
  lewat Manager/Coordinator seperti sekarang. Menunggu putusan HBA.
