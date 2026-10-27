# HBA-DECISIONS-67 — Ubah WO gagal Row is not JSON Serializable

Laporan HBA lewat chat 27 Okt 2026: ubah WO gagal dengan pesan Object of
type Row is not JSON Serializable.

## Temuan

Ujung `POST /api/wo/{id}/edit` di `app/server.py` meneruskan hasil
`wo_mod.update` apa adanya ke pengirim JSON, padahal itu baris database
mentah yang tidak bisa diserialkan. Ujung lain yang serupa sudah dibungkus
`dict`, ujung ini terlewat.

## Yang dikerjakan

Satu baris: jawaban edit dibungkus `dict` seperti ujung-ujung tetangganya.
Tidak ada perubahan perilaku, skema, atau aturan.

## Bukti

- `tests.test_batch3_wo_edit_timestamp` 7 uji lolos.
- Skrip bukti langsung: update lalu `json.dumps` seperti pengirim server,
  keluar JSON valid.
- Layanan `crm.service` aktif setelah deploy.

## Berkas dan status git

- Repo CRM, branch `fix/wo-edit-row-json-20261027`, commit `87408e4`, sudah
  push, belum merge. Yang berubah hanya `app/server.py` satu baris.
