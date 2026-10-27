# HBA-DECISIONS-64 — Admin diberi wewenang menugaskan teknisi

Putusan HBA lewat chat 27 Okt 2026 menjawab pertanyaan di HBA-DECISIONS-63:
Admin boleh menugaskan seperti Manager.

## Yang dikerjakan

`ASSIGN_WO_ROLES` di `app/wo/assignment.py` menjadi Manager, Coordinator, dan
Admin. Berlaku untuk menugaskan dan melepas teknisi, dengan alasan dan audit
tetap wajib seperti sebelumnya. Pesan penolakan dan komentar kanon di berkas
disesuaikan. Pengambilalihan sepihak (take over) tetap khusus Manager karena
itu tindakan mengambil alih menjadi diri sendiri, bukan menugaskan orang lain.
Layar penugasan memang tidak pernah menyembunyikan panel dari Admin, jadi
tidak ada perubahan layar — yang menghalangi kemarin murni penolakan backend.

## Bukti

- `tests.test_assignment` 12 uji lolos, termasuk uji baru bahwa Admin bisa
  menugaskan dan Sales tetap ditolak.
- `tests.test_authz` dan `tests.test_batch5_admin_full_access` 15 uji lolos.
- `tests.test_exec_server` 4 uji lolos.
- Layanan `crm.service` aktif setelah deploy, WO 27 tetap ber-teknisi utama
  Adi Setiawan.

## Berkas dan status git

- Repo CRM, branch `feat/wo-assign-admin-20261027`, commit `e9aef68`, sudah
  push, belum merge. Yang berubah: `app/wo/assignment.py` dan
  `tests/test_assignment.py`.
