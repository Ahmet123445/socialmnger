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

  public_host=${PUBLIC_HOST:-$(curl -fsS https://api.ipify.org || hostname -I | awk '{print $1}')}
  postgres_password=$(openssl rand -hex 24)
  minio_password=$(openssl rand -hex 24)
  jwt_secret=$(openssl rand -hex 48)

  sed -i "s|POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=${postgres_password}|" .env
  sed -i "s|MINIO_ROOT_PASSWORD=.*|MINIO_ROOT_PASSWORD=${minio_password}|" .env
  sed -i "s|JWT_SECRET_KEY=.*|JWT_SECRET_KEY=${jwt_secret}|" .env
  sed -i "s|CORS_ORIGINS=.*|CORS_ORIGINS=http://${public_host}|" .env
  sed -i "s|NEXT_PUBLIC_APP_URL=.*|NEXT_PUBLIC_APP_URL=http://${public_host}|" .env
  echo ".env otomatik oluşturuldu. Değerler sadece sunucuda tutuluyor: $APP_DIR/.env"
fi

docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps

echo "Deploy tamamlandı."
