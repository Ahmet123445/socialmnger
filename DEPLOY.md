# Sunucuya Kurulum

Bu doküman MedyaPanel uygulamasını kendi sunucuna kurmak içindir.

## Güvenlik

Sohbete yazılan SSH şifresi ve GitHub token artık gizli kabul edilmemeli.

1. GitHub token'ını GitHub ayarlarından revoke et.
2. Sunucu root şifresini değiştir.
3. Mümkünse root ile değil ayrı bir `deploy` kullanıcısı ve SSH key ile giriş yap.

## Sunucuda Docker Kurulumu

Ubuntu/Debian sunucuda:

```bash
curl -fsSL https://raw.githubusercontent.com/KULLANICI_ADIN/socialmnger/main/scripts/server-install.sh | bash
```

Firewall:

```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

## GitHub Repo Oluşturma

Token'ı komuta doğrudan yazma. Yeni token oluşturduktan sonra kendi terminalinde geçici environment variable olarak kullan:

```bash
export GH_TOKEN="YENI_GITHUB_TOKEN"
gh repo create socialmnger --private --source=. --remote=origin --push
```

Alternatif olarak GitHub web arayüzünden `socialmnger` reposunu oluşturup:

```bash
git remote add origin https://github.com/KULLANICI_ADIN/socialmnger.git
git push -u origin main
```

## Sunucuda Uygulamayı Çalıştırma

Sunucuya SSH ile bağlan:

```bash
ssh root@167.86.99.131
```

Projeyi tek komutla deploy et:

```bash
REPO_URL=https://github.com/KULLANICI_ADIN/socialmnger.git bash scripts/deploy-prod.sh
```

İlk çalıştırmada `.env` oluşturulur ve senden değerleri güncellemen beklenir.

Manuel kurulum istersen:

```bash
git clone https://github.com/KULLANICI_ADIN/socialmnger.git /opt/socialmnger
cd /opt/socialmnger
cp .env.production.example .env
nano .env
docker compose -f docker-compose.prod.yml up -d --build
```

Production env dosyasını oluştur:

```bash
cp .env.production.example .env
nano .env
```

Şu değerleri mutlaka değiştir:

```env
POSTGRES_PASSWORD=uzun-guclu-sifre
MINIO_ROOT_PASSWORD=uzun-guclu-sifre
JWT_SECRET_KEY=uzun-random-secret
```

Uygulamayı başlat:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Logları kontrol et:

```bash
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f frontend
```

Tarayıcıdan aç:

```text
http://167.86.99.131
```

IP ile kurulumda `.env` içindeki `APP_DOMAIN=:80` kalabilir. Domain bağladığında bunu domain adına çevir.

Demo giriş:

```text
E-posta: demo@sosyalmedya.local
Şifre: demo123
```

## Güncelleme

Yeni kodu sunucuda çekip yeniden build almak için:

```bash
cd /opt/socialmnger
git pull
docker compose -f docker-compose.prod.yml up -d --build
```

## Faydalı Komutlar

```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f
docker compose -f docker-compose.prod.yml restart backend
docker compose -f docker-compose.prod.yml down
```

## Domain Bağlama

Bir domain kullanacaksan A kaydını sunucu IP'sine yönlendir:

```text
A  @  167.86.99.131
```

Sonra `.env` içinde:

```env
APP_DOMAIN=panel.senin-domainin.com
CORS_ORIGINS=https://panel.senin-domainin.com
NEXT_PUBLIC_APP_URL=https://panel.senin-domainin.com
```

Caddy otomatik HTTPS sertifikası alır.
