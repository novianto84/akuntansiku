# HBA-DECISIONS-70 — Visit WO-018: bukan rusak, WO belum dimulai

Keluhan HBA lewat chat 27 Okt 2026: visit tidak bisa, walau admin.

## Temuan

Diperiksa langsung dengan akun Admin pada WO 27 (PAG/SPK/2026/018, OPEN):
mulai pekerjaan, buat visit, dan check-in semuanya lolos di backend.
Aturannya: visit hanya bisa dibuat saat WO IN_PROGRESS, sedangkan WO ini
masih OPEN — jadi tombol Buat Visit memang belum muncul dan layarnya
menampilkan catatan itu. Bukan bug peran, admin tidak dibatasi di jalur ini.

## Yang dikerjakan

Tidak ada perubahan kode. Baris uji dari pemeriksaan (satu visit + satu
check-in) sudah dihapus dan WO dikembalikan ke OPEN dengan nol visit.
Catatan jujur: cap waktu `updated_at` WO 27 ikut tersentuh pemeriksaan
(menjadi jam pemeriksaan), isi lainnya tidak berubah.

## Langkah termurah

Di detail WO 27 tekan Mulai pekerjaan (sudah bisa karena Adi Setiawan kini
PRIMARY), tombol Buat Visit muncul, lalu check-in seperti biasa.
