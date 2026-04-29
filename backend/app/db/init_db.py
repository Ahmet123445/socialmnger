import asyncio
from app.db.session import engine
from app.db.base import Base
from app.models import user, platform_account, content_item, media_asset, platform_post, publish_job, analytics, ai_setting, ai_recommendation, system_setting


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Veritabanı tabloları oluşturuldu.")


if __name__ == "__main__":
    asyncio.run(init_db())
