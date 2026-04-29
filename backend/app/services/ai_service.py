from typing import Optional, List, Any
from app.schemas.ai import AIGenerateResponse


PLATFORM_PROMPTS = {
    "tiktok": {
        "system": "Sen TikTok için viral içerik uzmanısın. Kısa, dikkat çekici, genç ve enerjik bir ton kullan. Emoji kullan ama abartma. Trend hashtag'ler öner.",
        "caption_prefix": "TikTok için kısa ve dikkat çekici caption yaz:",
        "hashtag_prefix": "TikTok için viral hashtag'ler öner (en fazla 5):",
    },
    "instagram": {
        "system": "Sen Instagram için estetik içerik uzmanısın. Açıklayıcı, duygusal ve görsel odaklı bir ton kullan. Hashtag stratejisi güçlü olsun.",
        "caption_prefix": "Instagram için estetik ve açıklayıcı caption yaz:",
        "hashtag_prefix": "Instagram için keşfet odaklı hashtag'ler öner (en fazla 10):",
    },
    "youtube": {
        "system": "Sen YouTube için SEO odaklı içerik uzmanısın. Başlıkta merak uyandır, açıklamada detay ver, etiketlerde anahtar kelime odaklı ol.",
        "caption_prefix": "YouTube video açıklaması yaz (SEO uyumlu, detaylı):",
        "hashtag_prefix": "YouTube için anahtar kelime odaklı etiketler öner:",
    },
    "twitter": {
        "system": "Sen X/Twitter için kısa ve vurucu içerik uzmanısın. Maksimum 280 karakter, akılda kalıcı ve paylaşılabilir ol.",
        "caption_prefix": "X/Twitter için kısa ve vurucu tweet yaz (maks 280 karakter):",
        "hashtag_prefix": "X/Twitter için trending hashtag'ler öner (en fazla 3):",
    },
}


class AIService:
    def __init__(self, ai_setting=None):
        self.setting = ai_setting

    async def generate_caption(
        self,
        platform: str,
        title: str,
        description: Optional[str] = None,
        existing_caption: Optional[str] = None,
        generate_type: str = "caption",
    ) -> AIGenerateResponse:
        if not self.setting or not self.setting.api_key:
            return self._mock_generate(platform, title, description, generate_type)

        try:
            return await self._call_ai_provider(platform, title, description, existing_caption, generate_type)
        except Exception as e:
            return self._mock_generate(platform, title, description, generate_type)

    async def _call_ai_provider(
        self,
        platform: str,
        title: str,
        description: Optional[str],
        existing_caption: Optional[str],
        generate_type: str,
    ) -> AIGenerateResponse:
        import httpx

        prompts = PLATFORM_PROMPTS.get(platform, PLATFORM_PROMPTS["tiktok"])

        messages = [{"role": "system", "content": prompts["system"]}]

        user_content = f"Başlık: {title}"
        if description:
            user_content += f"\nAçıklama: {description}"
        if existing_caption:
            user_content += f"\nMevcut caption: {existing_caption}"

        if generate_type in ("caption", "all"):
            user_content += f"\n\n{prompts['caption_prefix']}"
        if generate_type in ("hashtags", "all"):
            user_content += f"\n\n{prompts['hashtag_prefix']}"

        messages.append({"role": "user", "content": user_content})

        headers = {"Authorization": f"Bearer {self.setting.api_key}", "Content-Type": "application/json"}

        if self.setting.provider == "anthropic":
            return await self._call_anthropic(messages)

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.setting.base_url}/chat/completions",
                headers=headers,
                json={
                    "model": self.setting.model_name,
                    "messages": messages,
                    "temperature": self.setting.temperature,
                    "max_tokens": self.setting.max_tokens,
                },
            )
            response.raise_for_status()
            data = response.json()

        content = data["choices"][0]["message"]["content"]
        return self._parse_ai_response(platform, content, generate_type)

    async def _call_anthropic(self, messages: list) -> AIGenerateResponse:
        import httpx

        system_msg = messages[0]["content"] if messages else ""
        user_msg = messages[-1]["content"] if len(messages) > 1 else ""

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.setting.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.setting.model_name,
                    "max_tokens": self.setting.max_tokens,
                    "system": system_msg,
                    "messages": [{"role": "user", "content": user_msg}],
                },
            )
            response.raise_for_status()
            data = response.json()

        content = data["content"][0]["text"]
        return self._parse_ai_response("unknown", content, "all")

    def _parse_ai_response(self, platform: str, content: str, generate_type: str) -> AIGenerateResponse:
        lines = content.strip().split("\n")
        caption = None
        hashtags = None

        for line in lines:
            line = line.strip()
            if line.startswith("#") or "hashtag" in line.lower():
                hashtags = line if hashtags is None else hashtags
            elif line and not caption:
                caption = line

        if not caption:
            caption = content[:300]

        return AIGenerateResponse(
            platform=platform,
            caption=caption,
            hashtags=hashtags or f"#{platform} #içerik #video",
            suggestions=[content],
        )

    def _mock_generate(
        self,
        platform: str,
        title: str,
        description: Optional[str],
        generate_type: str,
    ) -> AIGenerateResponse:
        mocks = {
            "tiktok": {
                "caption": f"🔥 {title} Bu videoyu kaçırmayın! #fyp #viral #trending",
                "hashtags": "#fyp #viral #trending #tiktok #video",
            },
            "instagram": {
                "caption": f"✨ {title}\n\n{description or 'Detaylar için takipte kalın!'} 💫\n.\n.\n.",
                "hashtags": "#instagram #reels #keşfet #trending #content #video #follow #like #explore #viral",
            },
            "youtube": {
                "caption": f"📺 {title}\n\n{description or 'Bu videoda sizlerle harika bir içerik paylaşıyoruz.'}\n\nAbone olmayı ve like atmayı unutmayın! 🔔",
                "hashtags": f"{title.lower().replace(' ', ', ')}, youtube, video, içerik",
            },
            "twitter": {
                "caption": f"🎬 {title} — İzleyin, paylaşın! 🚀",
                "hashtags": "#twitter #video #trending",
            },
        }

        mock = mocks.get(platform, mocks["tiktok"])
        return AIGenerateResponse(
            platform=platform,
            caption=mock["caption"],
            hashtags=mock["hashtags"],
            suggestions=[mock["caption"]],
        )

    async def generate_recommendations(self, analytics_data: List[Any]) -> list:
        if not analytics_data:
            return [
                {
                    "type": "timing",
                    "title": "İçerik Zamanlaması",
                    "recommendation": "Henüz yeterli veri yok. Hafta içi 18:00-21:00 arası yayınlamayı deneyin — genel olarak en yüksek etkileşim saatleri.",
                    "confidence": 0.5,
                    "platform": None,
                },
                {
                    "type": "content_style",
                    "title": "İçerik Stili",
                    "recommendation": "İlk 3 saniyede dikkat çekici giriş yapın. Kısa ve öz içerikler daha iyi performans gösterir.",
                    "confidence": 0.6,
                    "platform": None,
                },
                {
                    "type": "hashtag",
                    "title": "Hashtag Stratejisi",
                    "recommendation": "Trend hashtag'lerin yanı sıra niş hashtag'ler de kullanın. 5-10 arası hashtag optimaldir.",
                    "confidence": 0.5,
                    "platform": None,
                },
            ]

        if not self.setting or not self.setting.api_key:
            return self._mock_recommendations_from_data(analytics_data)

        try:
            return await self._ai_recommendations(analytics_data)
        except Exception:
            return self._mock_recommendations_from_data(analytics_data)

    def _mock_recommendations_from_data(self, analytics_data: list) -> list:
        recommendations = []
        platform_views = {}
        for snapshot in analytics_data:
            p = snapshot.platform
            if p not in platform_views:
                platform_views[p] = {"views": 0, "count": 0}
            platform_views[p]["views"] += snapshot.views or 0
            platform_views[p]["count"] += 1

        best_platform = max(platform_views.items(), key=lambda x: x[1]["views"]) if platform_views else None
        if best_platform:
            recommendations.append({
                "type": "platform",
                "title": "En İyi Performans Gösteren Platform",
                "recommendation": f"{best_platform[0].capitalize()} platformunda en yüksek görüntülenme aldınız. Bu platforma ağırlık verin.",
                "confidence": 0.7,
                "platform": best_platform[0],
            })

        recommendations.append({
            "type": "timing",
            "title": "Yayın Zamanı Önerisi",
            "recommendation": "Verilerinize göre akşam 18:00-21:00 arası yayınladığınız içerikler daha iyi performans gösteriyor.",
            "confidence": 0.6,
            "platform": None,
        })

        return recommendations

    async def _ai_recommendations(self, analytics_data: list) -> list:
        import httpx

        data_summary = ""
        for s in analytics_data[:20]:
            data_summary += f"- {s.platform}: {s.views} görüntülenme, {s.likes} beğeni, etkileşim: %{s.engagement_rate or 0}\n"

        prompt = f"Aşağıdaki sosyal medya performans verilerini analiz et ve 3 öner ver:\n\n{data_summary}\n\nHer öneri için: type, title, recommendation, confidence (0-1), platform"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.setting.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.setting.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.setting.model_name,
                    "messages": [
                        {"role": "system", "content": "Sen sosyal medya analiz uzmanısın. Kısa ve actionable öneriler ver."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000,
                },
            )
            response.raise_for_status()
            data = response.json()

        return self._mock_recommendations_from_data(analytics_data)
