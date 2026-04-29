"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { AnalyticsSummary, AIRecommendation } from "@/types";
import { formatNumber, platformNames, platformColors } from "@/lib/utils";
import {
  BarChart3,
  Eye,
  Heart,
  MessageCircle,
  Share2,
  TrendingUp,
  Lightbulb,
  RefreshCw,
  Loader2,
} from "lucide-react";
import toast from "react-hot-toast";

function MetricCard({ label, value, icon: Icon, change }: { label: string; value: string; icon: any; change?: number }) {
  return (
    <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
      <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] mb-2">
        <Icon className="w-4 h-4" />
        <span className="text-sm">{label}</span>
      </div>
      <p className="text-2xl font-bold">{value}</p>
      {change !== undefined && (
        <p className={`text-xs mt-1 ${change >= 0 ? "text-green-600" : "text-red-600"}`}>
          {change >= 0 ? "+" : ""}{change}% geçen haftaya göre
        </p>
      )}
    </div>
  );
}

export default function AnalyticsPage() {
  const [days, setDays] = useState(30);
  const [selectedPlatform, setSelectedPlatform] = useState<string>("");
  const [recommendations, setRecommendations] = useState<AIRecommendation[]>([]);
  const [recLoading, setRecLoading] = useState(false);

  const { data: summary, isLoading } = useQuery<AnalyticsSummary>({
    queryKey: ["analytics", days, selectedPlatform],
    queryFn: async () => {
      const params = new URLSearchParams({ days: String(days) });
      if (selectedPlatform) params.set("platform", selectedPlatform);
      const res = await api.get(`/analytics/summary?${params}`);
      return res.data;
    },
  });

  const { data: recs = [] } = useQuery<AIRecommendation[]>({
    queryKey: ["recommendations"],
    queryFn: async () => {
      const res = await api.get("/ai/recommendations");
      return res.data;
    },
  });

  const generateRecommendations = async () => {
    setRecLoading(true);
    try {
      await api.post("/ai/recommendations/generate");
      toast.success("Öneriler üretildi!");
      window.location.reload();
    } catch {
      toast.error("Öneri üretimi başarısız");
    } finally {
      setRecLoading(false);
    }
  };

  const platforms = ["", "youtube", "tiktok", "instagram", "twitter"];
  const dayOptions = [7, 14, 30, 90];

  const data = summary || {
    total_views: 0,
    total_likes: 0,
    total_comments: 0,
    total_shares: 0,
    avg_engagement_rate: 0,
    content_count: 0,
    platform_breakdown: {},
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Analitik</h1>
          <p className="text-sm text-[hsl(var(--muted-foreground))] mt-1">
            Platform performansınızı analiz edin.
          </p>
        </div>
        <div className="flex gap-2">
          {dayOptions.map((d) => (
            <button
              key={d}
              onClick={() => setDays(d)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                days === d
                  ? "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]"
                  : "bg-[hsl(var(--card))] border border-[hsl(var(--border))]"
              }`}
            >
              {d} Gün
            </button>
          ))}
        </div>
      </div>

      <div className="flex gap-2">
        {platforms.map((p) => (
          <button
            key={p}
            onClick={() => setSelectedPlatform(p)}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium ${
              selectedPlatform === p
                ? "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]"
                : "bg-[hsl(var(--card))] border border-[hsl(var(--border))]"
            }`}
          >
            {p && <span className={`w-2.5 h-2.5 rounded-full ${platformColors[p]}`} />}
            {p ? platformNames[p] : "Tümü"}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5 animate-pulse">
              <div className="h-16 bg-[hsl(var(--muted))] rounded" />
            </div>
          ))}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard label="Toplam Görüntülenme" value={formatNumber(data.total_views)} icon={Eye} />
            <MetricCard label="Toplam Beğeni" value={formatNumber(data.total_likes)} icon={Heart} />
            <MetricCard label="Toplam Yorum" value={formatNumber(data.total_comments)} icon={MessageCircle} />
            <MetricCard label="Toplam Paylaşım" value={formatNumber(data.total_shares)} icon={Share2} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
              <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] mb-2">
                <TrendingUp className="w-4 h-4" />
                <span className="text-sm">Ortalama Etkileşim Oranı</span>
              </div>
              <p className="text-3xl font-bold">%{data.avg_engagement_rate}</p>
            </div>
            <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
              <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] mb-2">
                <BarChart3 className="w-4 h-4" />
                <span className="text-sm">İçerik Sayısı</span>
              </div>
              <p className="text-3xl font-bold">{data.content_count}</p>
            </div>
            <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
              <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] mb-2">
                <TrendingUp className="w-4 h-4" />
                <span className="text-sm">İçerik Başına Görüntülenme</span>
              </div>
              <p className="text-3xl font-bold">
                {data.content_count > 0 ? formatNumber(Math.round(data.total_views / data.content_count)) : "0"}
              </p>
            </div>
          </div>

          {Object.keys(data.platform_breakdown).length > 0 && (
            <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
              <h3 className="font-semibold mb-4">Platform Bazlı Performans</h3>
              <div className="space-y-4">
                {Object.entries(data.platform_breakdown).map(([platform, stats]) => {
                  const maxViews = Math.max(...Object.values(data.platform_breakdown).map((s: any) => s.views || 1));
                  return (
                    <div key={platform} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className={`w-3 h-3 rounded-full ${platformColors[platform]}`} />
                          <span className="text-sm font-medium">{platformNames[platform]}</span>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-[hsl(var(--muted-foreground))]">
                          <span>{formatNumber((stats as any).views)} görüntülenme</span>
                          <span>{formatNumber((stats as any).likes)} beğeni</span>
                        </div>
                      </div>
                      <div className="w-full bg-[hsl(var(--muted))] rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${platformColors[platform]}`}
                          style={{ width: `${((stats as any).views / maxViews) * 100}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </>
      )}

      <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-yellow-500" />
            <h3 className="font-semibold">AI Önerileri</h3>
          </div>
          <button
            onClick={generateRecommendations}
            disabled={recLoading}
            className="flex items-center gap-2 text-sm px-3 py-1.5 rounded-lg bg-purple-100 text-purple-700 hover:bg-purple-200 disabled:opacity-50"
          >
            {recLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
            Yeni Öneri Üret
          </button>
        </div>

        {recs.length > 0 ? (
          <div className="space-y-3">
            {recs.map((rec) => (
              <div key={rec.id} className="p-4 rounded-lg bg-[hsl(var(--muted))]/50 border border-[hsl(var(--border))]">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-medium text-sm">{rec.title}</p>
                    <p className="text-sm text-[hsl(var(--muted-foreground))] mt-1">{rec.recommendation}</p>
                  </div>
                  {rec.confidence_score && (
                    <span className="text-xs px-2 py-1 rounded-full bg-green-100 text-green-700 flex-shrink-ml-2">
                      %{Math.round(rec.confidence_score * 100)} güven
                    </span>
                  )}
                </div>
                {rec.platform && (
                  <div className="flex items-center gap-1.5 mt-2">
                    <span className={`w-2 h-2 rounded-full ${platformColors[rec.platform]}`} />
                    <span className="text-xs text-[hsl(var(--muted-foreground))]">{platformNames[rec.platform]}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-[hsl(var(--muted-foreground))]">
            <Lightbulb className="w-10 h-10 mx-auto mb-2 opacity-50" />
            <p className="text-sm">Henüz AI önerisi yok.</p>
            <p className="text-xs mt-1">İçerik yayınladıkça öneriler burada görünecek.</p>
          </div>
        )}
      </div>
    </div>
  );
}
