# Proposal Desain UI MitraSP CRM — Basis Model v9 LOCKED (Hitam-Merah filled)

```text
Status          : PROPOSED — siap untuk keputusan HBA. Bukan keputusan, bukan approval.
                  Dokumen ini tidak menyetujui dirinya sendiri.
Dibuat oleh     : Hermes (AI Manager / Lead Architect) — author proposal
Tanggal         : 2026-10-20 (WIB)
Referensi model : /home/anto/ui-samples-v9-blackred-filled-LOCKED-20261020.html
                  sha256 f7d75ca189c5fe8b6ad1938b4af2a01f3576df7472cb50dd2da269a7e4932d55
                  mtime 2026-10-20 15:25:41 WIB — read-only (-r--r--r--), 37035 byte
Model kerja     : ui-samples-v9-blackred-filled.html (sha identik dengan LOCKED)
Logo           : logo_msp.png (direferensikan relatif di dalam model)
Canonical       : BUKAN CANONICAL / BUKAN LOCKED
Implementation  : BELUM DIIMPLEMENTASI — proposal ini bukan otorisasi build
Gate            : NO CODING / NO SCHEMA / NO MIGRATION / NO PRODUCTION UI tanpa
                  otorisasi implementasi HBA terpisah
```

## 1. Apa yang diusulkan

Mengadopsi model UI **v9 Hitam-Merah filled (LOCKED)** sebagai dasar desain visual
UI MitraSP CRM. Jika HBA menyetujui, langkah berikutnya adalah otorisasi
implementasi untuk menerapkan desain ini ke UI CRM (`crm/ui/`, React+TS+Vite,
CSS + design tokens).

Proposal ini **hanya** mengikat sisi visual/presentasi. Tidak ada perubahan
semantik bisnis, lifecycle, authority, atau perilaku aplikasi.

## 2. Fakta desain terverifikasi dari file LOCKED

Verifikasi nyata atas file (bukan klaim pihak lain):

| Aspek | Nilai terverifikasi |
|---|---|
| Background | `--bg:#26262e` (abu charcoal), `--card:#303039` |
| Brand | `--brand:#ef2b2b` (merah), gradient `linear-gradient(135deg,#7f0d0d,#ef2b2b)` |
| Status | `--ok:#22c55e`, `--warn:#f59e0b`, `--bad:#ef2b2b` |
| Efek tile | glow border denyut `tileBorderPulse` (box-shadow merah rgba(239,43,43,…)); komentar eksplisit "v9 tile glow only - no icon glow" |
| Ikon | Font Awesome **filled** (`fa-solid`), 22 referensi: fa-users, fa-boxes-stacked, fa-clipboard-list, fa-file-invoice-dollar, fa-screwdriver-wrench, dll. |
| Tata letak | 3 view: profil (`v-profile`), dashboard (`v-dash`), portal (`v-portal`); grid g2/g3/g4 responsif |
| Tombol | `.btn` (light) + `.btn.primary` (merah filled) |
| Cover | gradient merah, frame logo `logo_msp.png`, badge, aksi |
| Font | system-ui stack; tanpa dependency font eksternal |

## 3. Delta vs UI CRM saat ini

| Item | Sekarang (`crm/ui/src/styles.css`) | Model v9 LOCKED |
|---|---|---|
| Background | `--bg:#f4f6f8` (terang) | `--bg:#26262e` (charcoal gelap) |
| Tema | light | dark |
| Ikon | Tabler (outline) | Font Awesome filled |
| Efek tile | none | glow denyut pada border tile saja |

Aplikasi model ini ke `crm/ui/` = penggantian design tokens + elemen visual,
tanpa mengubah struktur layar atau semantik.

## 4. Opsi untuk HBA

- **Opsi A — Setujui sebagai basis desain, otorisasi implementasi ke `crm/ui/`**
  dengan scope penerapan penuh (seluruh layar mengikuti model v9).
  Konsekuensi: perubahan visual menyeluruh; perlu build + verifikasi browser.
- **Opsi B — Setujui sebagai basis desain, implementasi bertahap**
  (mis. hanya layar dashboard dulu, sisanya menyusul). Konsekuensi: transisi
  tidak seragam antar layar sementara.
- **Opsi C — Simpan sebagai arsip desain, belum diimplementasikan**
  (model tetap direferensikan; UI produksi tidak berubah). Konsekuensi: tanpa
  biaya, tanpa risiko; desain siap dipakai kapan pun.

## 5. Yang AI tidak putuskan sendiri

- Persetujuan desain (HBA yang menyetujui, bukan AI).
- Scope penerapan (A/B/C di atas).
- Otorisasi implementasi ke kode UI — keputusan terpisah setelah persetujuan
  desain (§ IS-00: persetujuan spec ≠ otorisasi build).

## 6. Status & jejak

- Model terkunci (read-only, sha tercatat). File kerja & LOCKED sha identik —
  tidak ada drift.
- Proposal ini ditulis tanpa mengubah kode, schema, atau status dokumen kanonik.
- Setelah keputusan HBA, catat di DECISION_REGISTER / HBA-DECISIONS dan, bila
  A/B, ajukan otorisasi implementasi terpisah.
