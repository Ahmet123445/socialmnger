#!/usr/bin/env bash
set -euo pipefail

APP_DIR=${APP_DIR:-/opt/socialmnger}
REPO_URL=${REPO_URL:-}

if [ -z "$REPO_URL" ]; then
  echo "REPO_URL gerekli. Örnek: REPO_URL=https://github.com/kullanici/socialmnger.git ./scripts/deploy-prod.sh"
  exit 1
fi

if [ ! -d "$APP_DIR/.git" ]; then
  mkdir -p "$(dirname "$APP_DIR")"
  git clone "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"
git pull --ff-only

if [ ! -f .env ]; then
  cp .env.production.example .env
  echo ".env oluşturuldu. Lütfen güçlü şifreleri girip scripti tekrar çalıştır: $APP_DIR/.env"
  exit 1
fi

docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps

echo "Deploy tamamlandı."
