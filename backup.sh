#!/bin/sh
# Backup harian database container -> ./backup + retensi 14 hari
# Cara pakai di NUC: sh backup.sh   (jadwalkan via cron: 0 2 * * * cd /opt/akuntansiku && sh backup.sh)
set -e
STAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p backup data
if [ -f data/database.db ]; then
  cp data/database.db "backup/database-$STAMP.db"
  echo "Backup OK: backup/database-$STAMP.db"
else
  echo "DB belum ada di data/database.db - jalankan compose dulu (volume akan di-seed otomatis)."
fi
# retensi 14 hari
find backup -name 'database-*.db' -mtime +14 -delete 2>/dev/null || true
ls -lh backup | tail -5
