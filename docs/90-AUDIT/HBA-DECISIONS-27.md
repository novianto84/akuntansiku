# HBA DECISION RECORD — implementasi UI v9 "hitam-merah filled" ke crm/ui (2026-10-20)

```text
Record ID:      HBA-DECISIONS-27
Date:           2026-10-20
Author:         Hermes (AI Manager / Lead Architect) — record author only
Authority:      Human Business Authority (anto) — decision owner
Status:         RECORDED — putusan HBA 2026-10-20 via chat
Classification: Audit record. NOT a canonical specification document.
Implementation: UI-only visual change under this authorization (no migration, no DB, no server.py logic).
```

> Rekaman putusan HBA verbatim. Dokumen jejak, bukan spesifikasi.

## Putusan HBA

Setujui proposal desain `docs/90-AUDIT/UI-V9-DESIGN-PROPOSAL-20261020.md` (Opsi A) dan otorisasi eksekusi penuh ke `crm/ui/`. Model desain terkunci: `/home/anto/ui-samples-v9-blackred-filled-LOCKED-20261020.html` (read-only, sha `f7d75ca…`).

Verbatim: "di approve, dan di eksekusi segera. nanti akan ditambahkan lagi field fieldnya pada saat sudah mulai berjalan." — lalu "lanjutkan eksekusi."

## Eksekusi

Run governed: ops-ui-v9-20261020 (worker t_ui_v9_01). Perubahan UI-only, struktur layar & semantik TIDAK berubah:

- `src/styles.css` — rewrite penuh ke token v9: bg `#26262e`, surface `#303039`, border `#4a4a55`, brand/accent `#ef2b2b`, grad `#7f0d0d→#ef2b2b`, radius 14px. Semua komponen (sidebar, topbar, panel, stat, badge, button, form, table, dl, callout, timeline, lifecycle, login, toast) diadaptasi ke tema gelap. Semua nama class dipertahankan.
- Tile glow (permintaan eksplisit HBA: tile yang di-hover neon kuning): `.stat` & `.panel` dapat animasi `tileBorderPulse` (glow merah denyut) + hover → border `#fde047` + glow kuning, animasi pause.
- Ikon filled (identitas v9): tambah dep `@fortawesome/fontawesome-free` (satu-satunya dep baru; model pakai Font Awesome filled). Ikon di nav (gauge, clipboard-list, headset, boxes-stacked, users, chart-line, building, gear, clock-rotate-left, qrcode, building-flag), stat dashboard (clipboard-list, wrench, hourglass-half, rotate-left), stat monitoring (triangle-exclamation, headset, bell, clipboard-list), brand mark "M" gradien di sidebar + login.
- `src/components/ui.tsx` — `Stat` dapat prop opsional `icon` (backward-compatible).
- `src/main.tsx` — import CSS Font Awesome.

## Bukti

- `tsc -b` OK, `npm run build` OK (dist: index-Cs8uwXIY.css 100KB, index-DuCf7E0F.js 342KB, FA woff2 ter-bundle).
- Verifikasi browser nyata (headless chromium + CDP, login mgr/devpass123):
  - login: bg `rgb(38,38,46)` = `#26262e`, card `rgb(48,48,57)` = `#303039`, brand mark merah.
  - dashboard: bodyBg `#26262e`, stat border `rgb(74,22,22)` (merah), animasi `tileBorderPulse`, 4 tile, ikon FA ter-render (`fa-solid fa-gauge`, `fa-solid fa-clipboard-list`, font-family "Font Awesome 7 Free").
  - hover tile: border `rgb(253,224,71)` = `#fde047` (neon kuning) + glow kuning, animasi pause.
- Layanan crm-ui aktif, lokal 8092 = 200, serve bundel baru.

## Batas

Tanpa perubahan struktur layar/semantik. Tanpa backend/schema/migrasi/serving/auth. Tanpa perubahan data. Field baru (yang disebut HBA "akan ditambahkan lagi") TIDAK termasuk — butuh otorisasi terpisah.

## Langkah berikut termurah

Login di crm.benshi.my.id, cek tema gelap + tile glow (hover tile → neon kuning) + ikon. Bila ada field baru yang mau ditambahkan, ajukan sebagai task terpisah dengan otorisasi.

*End of decision record.*
