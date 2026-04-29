import asyncio
from datetime import datetime, timedelta
import random
import uuid

from app.db.session import engine, async_session_factory
from app.db.base import Base
from app.models import *  # noqa
from app.core.security import hash_password
from sqlalchemy import select


DEMO_CONTENT = [
    {
        "title": "TikTok Trend Challenge #2024",
        "description": "En yeni trend challenge videosu. Arkadaşlarımla birlikte çektik!",
        "platforms": ["tiktok", "instagram"],
        "general_caption": "Bu trendi kaçırmayın! 🔥",
        "general_hashtags": "#trend #challenge #2024 #viral",
        "status": "published",
        "platform_captions": {
            "tiktok": "🔥 Trend challenge! Siz de deneyin! #fyp #viral",
            "instagram": "✨ En yeni trend challenge!\n.\n.\n.#trend #challenge #reels",
        },
    },
    {
        "title": "YouTube Tutorial: Python ile Web Scraping",
        "description": "Bu videoda Python kullanarak web scraping yapmayı öğretiyorum.",
        "platforms": ["youtube"],
        "general_caption": "Python Web Scraping Rehberi",
        "general_hashtags": "#python #web scraping #tutorial #programlama",
        "status": "published",
        "platform_captions": {
            "youtube": "📺 Python ile Web Scraping öğrenmek ister misiniz?\n\nBu videoda adım adım anlatıyorum!\n\nAbone olmayı unutmayın! 🔔",
        },
    },
    {
        "title": "Instagram Reels: Günün Motivasyonu",
        "description": "Güne motivasyonla başlayın!",
        "platforms": ["instagram", "tiktok"],
        "general_caption": "Günün motivasyonu 💪",
        "general_hashtags": "#motivasyon #inspiration #gününözü",
        "status": "scheduled",
        "scheduled_at": datetime.utcnow() + timedelta(days=2),
    },
    {
        "title": "X/Twitter Thread: Yapay Zeka Trendleri",
        "description": "2024'ün en önemli yapay zeka trendleri hakkında thread.",
        "platforms": ["twitter"],
        "general_caption": "2024'te yapay zeka nereye gidiyor? 🧵 Thread👇",
        "general_hashtags": "#yapayzeka #AI #teknoloji #2024",
        "status": "draft",
    },
    {
        "title": "YouTube Shorts: Komik Hayvanlar",
        "description": "En komik hayvan videoları derlemesi.",
        "platforms": ["youtube", "tiktok", "instagram"],
        "general_caption": "Bu videolar sizi güldürecek 😂",
        "general_hashtags": "#komik #hayvanlar #funny #shorts",
        "status": "published",
    },
    {
        "title": "Instagram Carousel: Seyahat Fotoğrafları",
        "description": "İstanbul'dan en güzel kareler.",
        "platforms": ["instagram"],
        "general_caption": "İstanbul'dan büyüleyici kareler 📸",
        "general_hashtags": "#istanbul #seyahat #travel #photography",
        "status": "published",
    },
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as db:
        existing = await db.execute(select(User).where(User.email == "demo@sosyalmedya.local"))
        if existing.scalar_one_or_none():
            print("Demo veriler zaten mevcut, seed atlandı.")
            return

        # Create demo user
        demo_user = User(
            email="demo@sosyalmedya.local",
            username="demo",
            hashed_password=hash_password("demo123"),
            full_name="Demo Kullanıcı",
            is_active=True,
        )
        db.add(demo_user)
        await db.flush()

        # Create platform accounts (mock)
        platform_accounts = {}
        for platform in ["youtube", "tiktok", "instagram", "twitter"]:
            account = PlatformAccount(
                user_id=demo_user.id,
                platform=platform,
                platform_username=f"demo_{platform}",
                status="mock",
            )
            db.add(account)
            platform_accounts[platform] = account
        await db.flush()

        # Create AI setting
        ai_setting = AISetting(
            user_id=demo_user.id,
            provider="openai",
            base_url="https://api.openai.com/v1",
            model_name="gpt-4o-mini",
            temperature=0.7,
        )
        db.add(ai_setting)

        # Create content items
        for i, content_data in enumerate(DEMO_CONTENT):
            content = ContentItem(
                user_id=demo_user.id,
                title=content_data["title"],
                description=content_data["description"],
                platforms=content_data["platforms"],
                general_caption=content_data["general_caption"],
                general_hashtags=content_data["general_hashtags"],
                platform_captions=content_data.get("platform_captions"),
                status=content_data["status"],
                scheduled_at=content_data.get("scheduled_at"),
                published_at=datetime.utcnow() - timedelta(days=random.randint(1, 14)) if content_data["status"] == "published" else None,
            )
            db.add(content)
            await db.flush()

            # Create platform posts and analytics for published content
            if content_data["status"] == "published":
                for platform in content_data["platforms"]:
                    post = PlatformPost(
                        content_item_id=content.id,
                        platform_account_id=platform_accounts[platform].id,
                        platform=platform,
                        platform_post_id=f"mock_{uuid.uuid4().hex[:12]}",
                        caption=content_data.get("platform_captions", {}).get(platform, content_data["general_caption"]),
                        status="published",
                        post_url=f"https://mock.{platform}.com/watch/demo",
                        published_at=content.published_at,
                    )
                    db.add(post)
                    await db.flush()

                    # Create multiple analytics snapshots
                    for day_offset in range(7):
                        snapshot = AnalyticsSnapshot(
                            platform_post_id=post.id,
                            content_item_id=content.id,
                            platform=platform,
                            views=random.randint(100, 100000),
                            likes=random.randint(10, 10000),
                            comments=random.randint(0, 1000),
                            shares=random.randint(0, 2000),
                            saves=random.randint(0, 500),
                            follower_count=random.randint(100, 50000),
                            engagement_rate=round(random.uniform(1.0, 20.0), 2),
                            performance_score=round(random.uniform(30.0, 95.0), 1),
                            snapshot_date=datetime.utcnow() - timedelta(days=day_offset),
                        )
                        db.add(snapshot)

        # Create AI recommendations
        recommendations = [
            {
                "type": "timing",
                "title": "En İyi Yayın Saati",
                "recommendation": "Verilerinize göre hafta içi 18:00-21:00 arası yayınladığınız içerikler %40 daha fazla etkileşim alıyor.",
                "confidence": 0.85,
                "platform": None,
            },
            {
                "type": "platform",
                "title": "En İyi Performans Gösteren Platform",
                "recommendation": "TikTok'taki içerikleriniz diğer platformlara göre ortalama 3 kat daha fazla görüntülenme alıyor. Bu platforma ağırlık vermenizi öneririz.",
                "confidence": 0.78,
                "platform": "tiktok",
            },
            {
                "type": "content_style",
                "title": "İçerik Stili Önerisi",
                "recommendation": "Kısa ve enerjik giriş yapan videolarınız daha iyi performans gösteriyor. İlk 3 saniyede dikkat çekici bir giriş yapın.",
                "confidence": 0.72,
                "platform": None,
            },
            {
                "type": "hashtag",
                "title": "Hashtag Stratejisi",
                "recommendation": "5-8 arası hashtag kullanmak optimal. Trend hashtag'lerin yanı sıra niş hashtag'ler de ekleyin.",
                "confidence": 0.65,
                "platform": "instagram",
            },
            {
                "type": "caption",
                "title": "Caption Uzunluğu",
                "recommendation": "TikTok'ta kısa caption'lar (%15 daha iyi), Instagram'da orta uzunlukta caption'lar daha etkili.",
                "confidence": 0.6,
                "platform": "tiktok",
            },
        ]

        for rec in recommendations:
            recommendation = AIRecommendation(
                user_id=demo_user.id,
                recommendation_type=rec["type"],
                platform=rec.get("platform"),
                title=rec["title"],
                recommendation=rec["recommendation"],
                confidence_score=rec["confidence"],
            )
            db.add(recommendation)

        # System settings
        settings = [
            SystemSetting(key="publish_mode", value="mock", description="Yayın modu: mock, official_api, automation_fallback"),
            SystemSetting(key="app_name", value="MedyaPanel", description="Uygulama adı"),
            SystemSetting(key="default_language", value="tr", description="Varsayılan dil"),
        ]
        for s in settings:
            db.add(s)

        await db.commit()
        print("✅ Demo veriler başarıyla oluşturuldu!")
        print(f"   Kullanıcı: demo@sosyalmedya.local / demo123")
        print(f"   {len(DEMO_CONTENT)} içerik, {len(recommendations)} AI önerisi")


if __name__ == "__main__":
    asyncio.run(seed())
