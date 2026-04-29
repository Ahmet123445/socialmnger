from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import auth, content, media, analytics, settings_api, ai, dashboard

app = FastAPI(
    title="Sosyal Medya Kontrol Odası",
    description="TikTok, X/Twitter, YouTube ve Instagram içerik yönetim ve analiz uygulaması",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Kimlik Doğrulama"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(content.router, prefix="/api/v1/content", tags=["İçerik Yönetimi"])
app.include_router(media.router, prefix="/api/v1/media", tags=["Medya"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analitik"])
app.include_router(settings_api.router, prefix="/api/v1/settings", tags=["Ayarlar"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["Yapay Zeka"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sosyalmedya-backend"}
