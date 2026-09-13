# DEPLOY NUC (Docker, Supervised 8GB+) + Akses Internet Aman via Tailscale
Prioritas yang dipilih: Docker dulu (persisten + backup), baru akses aman. Jangan expose port ke Mikrotik langsung.

## 1. Siapkan folder di NUC
```
mkdir -p /opt/akuntansiku/data /opt/akuntansiku/backup
cp app.py Dockerfile docker-compose.yml backup.sh /opt/akuntansiku/
cp -r public /opt/akuntansiku/
cd /opt/akuntansiku
```

## 2. Jalankan (seed otomatis bila DB kosong)
```
docker compose up -d --build
docker compose logs -f
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/
```
Buka lokal dulu: `http://<IP-NUC>:8000` → login admin/admin123 → langsung ganti password.

## 3. Akses internet aman — Tailscale (dipilih karena paling mudah, tanpa buka port)
```
# di NUC + tiap HP/laptop kasir: install Tailscale, login akun yang sama
tailscale up
tailscale status
```
Lalu buka `http://<IP-TAILSCALE-NUC>:8000`. Jangan publish via port-forward Mikrotik.
Alternatif bila perlu link publik: Cloudflare Tunnel (HTTPS + Access policy).

## 4. Backup
- Otomatis container: unduh via Master → Unduh Backup.
- Harian host: `sh backup.sh` + cron `0 2 * * *`.
- `database.db` TIDAK ikut git/compose (ada di volume `./data`). Yang di-backup: `./data/database.db` + `./backup/`.

## 5. Update aman
```
cd /opt/akuntansiku && docker compose up -d --build
sh backup.sh   # sebelum & sesudah update
```
Rollback: `cp backup/database-<STAMP>.db data/database.db && docker compose restart`.
