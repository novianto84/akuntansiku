# PANDUAN OPERASIONAL — ERP-MSP (ala Accurate Online)

## 1. Menjalankan aplikasi
- Buka folder ini, jalankan: `python app.py`
- Buka browser: `http://localhost:8000` (jangan double-klik index.html)
- Menutup: tekan `Ctrl+C` di jendela terminal.

## 2. Akun bawaan (wajib ganti password saat login pertama!)
| Username | Password | Peran | Akses |
|---|---|---|---|
| admin | admin123 | ADMIN | Semua + kelola user + backup/restore |
| manager | manager123 | MANAGER | Semua kecuali kelola user |
| kasir | kasir123 | KASIR | Dashboard, Penjualan, Pembelian, Kas & Bank, Persediaan |
| finance* | — | FINANCE | Seperti manager (keuangan, tanpa kelola user) |
| gudang* | — | GUDANG | Dashboard, Persediaan, Pembelian |
| hrd* | — | HRD | Dashboard, Master (karyawan/cuti) |
\*dibuat admin via Master → User & Peran.
- Login dengan password default → aplikasi **wajibkan ganti password** (peringatan otomatis).
- Ganti password: tombol **Ganti password** di panel kiri.
- Tambah user: Master → User & Peran (khusus admin).
- Lupa password admin: hentikan aplikasi, jalankan perintah ini di folder aplikasi:
  `python -c "import sqlite3,hashlib,secrets; c=sqlite3.connect('database.db'); s=secrets.token_hex(8); c.execute(\"UPDATE users SET password_hash=?,salt=? WHERE username='admin'\",(hashlib.pbkdf2_hmac('sha256',b'admin123',s.encode(),100000).hex(),s)); c.commit()"`
  lalu login admin/admin123.

## 3. Alur kerja harian
1. **Penjualan**: buat faktur (customer bisa `+ Baru` langsung, PPN dari master pajak, diskon %, satuan, salesman, tukar tambah) → otomatis menjurnal + kurangi stok + hitung HPP.
2. **Pembelian**: buat tagihan (vendor bisa `+ Baru`, PPN master) → stok bertambah + utang tercatat.
3. **Kas & Bank**: catat pelunasan per invoice (bisa parsial), transfer antar kas/bank, input mutasi koran → Auto-Match (toleransi tgl ±3 hari, nominal Rp pas).
4. **Persediaan**: cek saran order cerdas; opname bila perlu; mutasi antar gudang.
5. **HRIS**: absensi di Dashboard; cuti diajukan lalu disetujui manager; gaji pakai hitung PPh21 TER otomatis.
6. **Void besar**: kasir/gudang ajukan → muncul di Master → Persetujuan Void → manager setujui/tolak.

## 4. Rutinitas akhir bulan
1. Aset Tetap → **Susutkan** tiap aset.
2. HRIS → posting **Gaji + PPh21**.
3. Kas & Bank → lengkapi **rekonsiliasi** (target: tidak ada selisih).
4. Laporan → cek **Trial Balance** (harus seimbang), **Laba/Rugi**, **Neraca**, **Arus Kas**, **PPN** (kurang/lebih bayar).
5. **Tutup periode bulanan** (Buku Besar → Period End kirim `period: YYYY-MM`) atau tahunan (`year: YYYY`). Periode terkunci tolak posting mundur.
6. **Backup** (Master → Unduh Backup), simpan di luar komputer ini. Restore otomatis bikin `database.auto-backup-*.db` dulu.

## 5. Aturan penting (jangan dilanggar)
- **Rupiah bulat:** semua nominal dibulatkan ke Rp 1, tanpa sen/desimal.
- Nomor dokumen otomatis anti-duplikat (aman dipakai 2 kasir bersamaan).
- Jurnal yang sudah POSTED tidak bisa diedit — salah input? Buat **Void** (penjualan/pembelian) atau **Jurnal pembalik** manual.
- Stok tidak boleh minus; void pembelian ditolak bila barang sudah terjual.
- Pembayaran/retur tidak boleh melebihi sisa tagihan.
- Pembelian melewati **limit utang vendor** akan ditolak.
- Metode HPP (Average/FIFO) per barang hanya diubah oleh manager/admin.

## 6. File-file
- `app.py` — program utama. `database.db` — seluruh data (ini yang di-backup).
- `public/` — tampilan. Jangan hapus `database.db` kecuali ingin mengulang dari nol
  (data awal + akun bawaan dibuat otomatis saat file tidak ada).

## 7. Masalah umum
- Halaman "Memuat" terus: pastikan dibuka via http://localhost:8000 + refresh Ctrl+F5.
- Port 8000 dipakai: hentikan proses python lain yang menjalankan app.py.
- Sesi habis: login ulang (sesi 12 jam).
