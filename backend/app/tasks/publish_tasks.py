import asyncio
from datetime import datetime
from app.tasks.celery_app import celery_app


def run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def publish_to_platform(self, job_id: str):
    from app.db.session import async_session_factory
    from app.models.publish_job import PublishJob
    from app.models.content_item import ContentItem
    from app.models.platform_post import PlatformPost
    from app.models.platform_account import PlatformAccount
    from app.adapters.registry import get_adapter
    from sqlalchemy import select

    async def _publish():
        async with async_session_factory() as db:
            try:
                result = await db.execute(select(PublishJob).where(PublishJob.id == job_id))
                job = result.scalar_one_or_none()
                if not job:
                    return {"error": "Job bulunamadı"}

                job.status = "processing"
                job.started_at = datetime.utcnow()
                job.attempts += 1
                await db.flush()

                content_result = await db.execute(select(ContentItem).where(ContentItem.id == job.content_item_id))
                content = content_result.scalar_one_or_none()
                if not content:
                    job.status = "failed"
                    job.error_message = "İçerik bulunamadı"
                    await db.flush()
                    return {"error": "İçerik bulunamadı"}

                adapter = get_adapter(job.platform, mode="mock")

                caption = (content.platform_captions or {}).get(job.platform, content.general_caption or content.title)
                hashtags = (content.platform_hashtags or {}).get(job.platform, content.general_hashtags or "")

                publish_result = await adapter.publish_video(
                    access_token="mock_token",
                    video_path="",
                    caption=caption,
                    hashtags=hashtags,
                    title=content.title,
                    description=content.description,
                )

                if publish_result.success:
                    account_result = await db.execute(
                        select(PlatformAccount).where(
                            PlatformAccount.user_id == content.user_id,
                            PlatformAccount.platform == job.platform,
                        )
                    )
                    platform_account = account_result.scalar_one_or_none()
                    if not platform_account:
                        platform_account = PlatformAccount(
                            user_id=content.user_id,
                            platform=job.platform,
                            platform_username=f"mock_{job.platform}",
                            status="mock",
                        )
                        db.add(platform_account)
                        await db.flush()

                    job.status = "completed"
                    job.completed_at = datetime.utcnow()
                    job.result = {
                        "platform_post_id": publish_result.platform_post_id,
                        "post_url": publish_result.post_url,
                        "metadata": publish_result.metadata,
                    }

                    platform_post = PlatformPost(
                        content_item_id=content.id,
                        platform_account_id=platform_account.id,
                        platform=job.platform,
                        platform_post_id=publish_result.platform_post_id,
                        caption=caption,
                        hashtags=hashtags,
                        status="published",
                        post_url=publish_result.post_url,
                        published_at=datetime.utcnow(),
                        platform_metadata=publish_result.metadata,
                    )
                    db.add(platform_post)

                    all_jobs_result = await db.execute(
                        select(PublishJob).where(PublishJob.content_item_id == content.id)
                    )
                    all_jobs = all_jobs_result.scalars().all()
                    if all(j.status == "completed" for j in all_jobs):
                        content.status = "published"
                        content.published_at = datetime.utcnow()
                    elif any(j.status == "failed" for j in all_jobs):
                        content.status = "failed"
                else:
                    if job.attempts < job.max_attempts:
                        job.status = "retrying"
                        raise self.retry(exc=Exception(publish_result.error_message))
                    else:
                        job.status = "failed"
                        job.error_message = publish_result.error_message

                await db.flush()
                return {"status": job.status, "platform": job.platform}

            except Exception as e:
                await db.rollback()
                raise

    return run_async(_publish())


@celery_app.task
def fetch_analytics_for_post(platform_post_id: str):
    from app.db.session import async_session_factory
    from app.models.platform_post import PlatformPost
    from app.models.analytics import AnalyticsSnapshot
    from app.adapters.registry import get_adapter
    from sqlalchemy import select

    async def _fetch():
        async with async_session_factory() as db:
            result = await db.execute(select(PlatformPost).where(PlatformPost.id == platform_post_id))
            post = result.scalar_one_or_none()
            if not post:
                return {"error": "Post bulunamadı"}

            adapter = get_adapter(post.platform, mode="mock")
            analytics = await adapter.fetch_analytics(
                access_token="mock_token",
                platform_post_id=post.platform_post_id or "",
            )

            snapshot = AnalyticsSnapshot(
                platform_post_id=post.id,
                content_item_id=post.content_item_id,
                platform=post.platform,
                views=analytics.views,
                likes=analytics.likes,
                comments=analytics.comments,
                shares=analytics.shares,
                saves=analytics.saves,
                follower_count=analytics.follower_count,
                engagement_rate=analytics.engagement_rate,
                performance_score=min(100, (analytics.engagement_rate or 0) * 7),
            )
            db.add(snapshot)
            await db.flush()
            return {"status": "ok", "platform": post.platform}

    return run_async(_fetch())


@celery_app.task
def fetch_all_pending_analytics():
    from app.db.session import async_session_factory
    from app.models.platform_post import PlatformPost
    from sqlalchemy import select

    async def _fetch_all():
        async with async_session_factory() as db:
            result = await db.execute(
                select(PlatformPost).where(PlatformPost.status == "published")
            )
            posts = result.scalars().all()
            for post in posts:
                fetch_analytics_for_post.delay(str(post.id))

    run_async(_fetch_all())
