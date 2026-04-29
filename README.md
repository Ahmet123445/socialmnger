# 🚀 MedyaPanel — Sosyal Medya Kontrol Odası

TikTok, X/Twitter, YouTube ve Instagram hesaplarınızı tek panelden yönetin.

## ✨ Özellikler

- **Dashboard**: Bugünkü/haftalık içerik özeti, platform performansı, AI önerileri
- **İçerik Stüdyosu**: Video yükleme, AI ile caption/hashtag üretimi, tek tıkla çoklu platform yayınlama
- **Analitik**: Platform bazlı performans karşılaştırma, etkileşim analizi
- **AI Önerileri**: Geçmiş performansa dayalı akıllı öneriler
- **Çoklu Platform**: YouTube, TikTok, Instagram, X/Twitter desteği
- **Mock Mod**: API credential olmadan tamamen çalışır

## 🛠 Teknoloji Stack

| Katman | Teknoloji |
|--------|-----------|
| Frontend | Next.js 14 + React + TypeScript + TailwindCSS |
| Backend | FastAPI + SQLAlchemy + asyncpg |
| Veritabanı | PostgreSQL 16 |
| Queue | Redis + Celery |
| Storage | MinIO (S3 uyumlu) |
| AI | OpenAI / Anthropic / Ollama (OpenAI-compatible) |
| Container | Docker Compose |

## 📦 Kurulum

### 1. Docker Compose ile Başlatın

```bash
docker compose up -d
```

Bu komut tüm servisleri başlatır:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Konsol**: http://localhost:9001 (minioadmin / minioadmin123)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 2. Demo Hesapla Giriş Yapın

```
E-posta: demo@sosyalmedya.local
Şifre: demo123
```

Demo veriler otomatik olarak oluşturulur (içerikler, analytics, AI önerileri).

### 3. Manuel Seed (Opsiyonel)

```bash
docker compose exec backend python seed.py
```

## 🔧 Ortam Değişkenleri

`.env.example` dosyasını `.env` olarak kopyalayın:

```bash
cp .env.example .env
```

| Değişken | Açıklama | Varsayılan |
|----------|----------|------------|
| `POSTGRES_USER` | DB kullanıcısı | sosyalmedya |
| `POSTGRES_PASSWORD` | DB şifresi | sosyalmedya123 |
| `MINIO_ROOT_USER` | MinIO kullanıcısı | minioadmin |
| `MINIO_ROOT_PASSWORD` | MinIO şifresi | minioadmin123 |
| `JWT_SECRET_KEY` | JWT gizli anahtarı | (değiştirin!) |
| `NEXT_PUBLIC_API_URL` | Backend API URL | http://localhost:8000/api/v1 |

## 🤖 AI Ayarları

Settings sayfasından veya `.env` dosyasından yapılandırabilirsiniz:

| Sağlayıcı | Base URL | Model Örnekleri |
|-----------|----------|-----------------|
| OpenAI | https://api.openai.com/v1 | gpt-4o-mini, gpt-4o |
| Anthropic | - | claude-3-5-sonnet |
| Ollama | http://localhost:11434/v1 | llama3, mistral |
| Özel | Herhangi bir OpenAI-compatible URL | - |

API key girilmezse **mock mod**da çalışır (AI olmadan örnek içerik üretir).

## 📡 Platform Durumu

| Platform | Durum | Not |
|----------|-------|-----|
| YouTube | 🔶 Interface Hazır | YouTube Data API v3 - credential ekleyince çalışır |
| TikTok | 🔶 Interface Hazır | Content Posting API - credential ekleyince çalışır |
| Instagram | 🔶 Interface Hazır | Graph API - Business/Creator hesap gerekli |
| X/Twitter | 🔶 Interface Hazır | API v2 - credential ekleyince çalışır |
| Tümü | ✅ Mock Mod | Credential olmadan simülasyon |

## 🏗 Mimari

```
┌─────────────┐     ┌──────────────┐     ┌──────────┐
│   Frontend   │────▶│   Backend    │────▶│ PostgreSQL│
│  Next.js 14  │     │   FastAPI    │     └──────────┘
└─────────────┘     │              │     ┌──────────┐
                    │  ┌─────────┐ │────▶│  Redis   │
                    │  │Adapters │ │     └──────────┘
                    │  │- YouTube│ │     ┌──────────┐
                    │  │- TikTok │ │────▶│  MinIO   │
                    │  │- Insta  │ │     └──────────┘
                    │  │- Twitter│ │
                    │  │- Mock   │ │     ┌──────────┐
                    │  └─────────┘ │────▶│ Celery   │
                    └──────────────┘     │ Worker   │
                                         └──────────┘
```

### Adapter Pattern

Her platform için ayrı adapter sınıfı:
- `BasePlatformAdapter` → abstract interface
- `MockAdapter` → simülasyon modu
- `YouTubeAdapter` → YouTube Data API v3
- `TikTokAdapter` → TikTok Content Posting API
- `InstagramAdapter` → Instagram Graph API
- `TwitterAdapter` → Twitter API v2

Yeni platform eklemek için `BasePlatformAdapter`'ı extend edin ve `registry.py`'ye kaydedin.

## 📁 Proje Yapısı

```
sosyalmedya/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── seed.py
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── config.py        # Ayarlar
│   │   ├── db/              # Veritabanı
│   │   ├── models/          # SQLAlchemy modelleri
│   │   ├── schemas/         # Pydantic şemaları
│   │   ├── api/v1/          # API endpoint'leri
│   │   ├── services/        # İş mantığı
│   │   ├── adapters/        # Platform entegrasyonları
│   │   ├── tasks/           # Celery task'ları
│   │   └── storage/         # MinIO client
│   └── alembic/
├── frontend/
│   ├── Dockerfile
│   ├── src/
│   │   ├── app/             # Next.js App Router
│   │   ├── components/      # React bileşenleri
│   │   ├── hooks/           # Custom hook'lar
│   │   ├── lib/             # Yardımcı fonksiyonlar
│   │   ├── types/           # TypeScript tip tanımları
│   │   ├── stores/          # Zustand store'lar
│   │   └── providers/       # Context provider'lar
│   └── public/
└── docker/
```

## 🚀 Sonraki Geliştirme Noktaları

1. **Gerçek API Entegrasyonu**: Her platform için OAuth2 flow'u ekleyin
2. **Video Processing**: FFmpeg ile thumbnail çıkarma, video compress
3. **WebSocket**: Publish job durumları için real-time güncelleme
4. **Takvim Görünümü**: İçerik planlaması için drag-drop takvim
5. **Toplu Yayınlama**: Birden fazla içeriği aynı anda zamanlama
6. **Raporlama**: Haftalık/aylık PDF rapor oluşturma
7. **Webhook**: Platform bildirimleri için webhook endpoint'leri
8. **Çoklu Kullanıcı**: Ekip üyeleri ve rol yönetimi
9. **A/B Testing**: Farklı caption'ları test etme
10. **Otomatik Yeniden Paylaşım**: En iyi performans gösteren içerikleri tekrar yayınlama

## 📝 Komutlar

```bash
# Başlat
docker compose up -d

# Durdur
docker compose down

# Logları gör
docker compose logs -f backend
docker compose logs -f frontend

# Yeniden build
docker compose build --no-cache

# Backend shell
docker compose exec backend bash

# Veritabanı migration
docker compose exec backend alembic upgrade head

# Seed data
docker compose exec backend python seed.py
```

## 📄 Lisans

Bu proje kişisel kullanım içindir. MIT Lisansı.
