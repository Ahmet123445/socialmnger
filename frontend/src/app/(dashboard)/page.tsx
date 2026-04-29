"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { DashboardSummary } from "@/types";
import {
  FileVideo,
  Calendar,
  CheckCircle,
  XCircle,
  Eye,
  Heart,
  TrendingUp,
  AlertTriangle,
  ArrowRight,
} from "lucide-react";
import Link from "next/link";
import { formatNumber, timeAgo, platformNames, statusLabels, statusColors } from "@/lib/utils";

function StatCard({ label, value, icon: Icon, color }: { label: string; value: string | number; icon: any; color: string }) {
  return (
    <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5 flex items-center gap-4">
      <div className={`p-3 rounded-lg ${color}`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
      <div>
        <p className="text-2xl font-bold">{value}</p>
        <p className="text-sm text-[hsl(var(--muted-foreground))]">{label}</p>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const { data, isLoading, error } = useQuery<DashboardSummary>({
    queryKey: ["dashboard"],
    queryFn: async () => {
      const res = await api.get("/dashboard/summary");
      return res.data;
    },
  });

  if (isLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5 animate-pulse">
              <div className="h-20 bg-[hsl(var(--muted))] rounded" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-lg font-semibold mb-2">Bağlantı Hatası</h2>
          <p className="text-[hsl(var(--muted-foreground))]">Backend servisine bağlanılamıyor. Docker servislerinin çalıştığından emin olun.</p>
        </div>
      </div>
    );
  }

  const summary = data || {
    today_content_count: 0,
    week_content_count: 0,
    scheduled_count: 0,
    published_count: 0,
    failed_count: 0,
    total_views: 0,
    total_likes: 0,
    total_engagement_rate: 0,
    recent_content: [],
    alerts: [],
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-sm text-[hsl(var(--muted-foreground))]">
          Hoş geldiniz! İşte bugünün özeti.
        </p>
      </div>

      {summary.alerts && summary.alerts.length > 0 && (
        <div className="space-y-2">
          {summary.alerts.map((alert, i) => (
            <div
              key={i}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm ${
                alert.type === "error"
                  ? "bg-red-50 text-red-700 border border-red-200"
                  : "bg-blue-50 text-blue-700 border border-blue-200"
              }`}
            >
              <AlertTriangle className="w-4 h-4 flex-shrink-0" />
              {alert.message}
            </div>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Bugünkü İçerik" value={summary.today_content_count} icon={FileVideo} color="bg-blue-500" />
        <StatCard label="Zamanlanmış" value={summary.scheduled_count} icon={Calendar} color="bg-purple-500" />
        <StatCard label="Yayınlanan" value={summary.published_count} icon={CheckCircle} color="bg-green-500" />
        <StatCard label="Başarısız" value={summary.failed_count} icon={XCircle} color="bg-red-500" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
          <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] mb-2">
            <Eye className="w-4 h-4" />
            <span className="text-sm">Toplam Görüntülenme</span>
          </div>
          <p className="text-3xl font-bold">{formatNumber(summary.total_views)}</p>
          <p className="text-xs text-[hsl(var(--muted-foreground))] mt-1">Son 7 gün</p>
        </div>
        <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
          <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] mb-2">
            <Heart className="w-4 h-4" />
            <span className="text-sm">Toplam Beğeni</span>
          </div>
          <p className="text-3xl font-bold">{formatNumber(summary.total_likes)}</p>
          <p className="text-xs text-[hsl(var(--muted-foreground))] mt-1">Son 7 gün</p>
        </div>
        <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
          <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] mb-2">
            <TrendingUp className="w-4 h-4" />
            <span className="text-sm">Ortalama Etkileşim</span>
          </div>
          <p className="text-3xl font-bold">%{summary.total_engagement_rate}</p>
          <p className="text-xs text-[hsl(var(--muted-foreground))] mt-1">Son 7 gün</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold">Son İçerikler</h3>
            <Link href="/content" className="text-sm text-[hsl(var(--primary))] hover:underline flex items-center gap-1">
              Tümünü Gör <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
          {summary.recent_content && summary.recent_content.length > 0 ? (
            <div className="space-y-3">
              {summary.recent_content.map((item) => (
                <div key={item.id} className="flex items-center justify-between p-3 rounded-lg bg-[hsl(var(--muted))]/50">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{item.title}</p>
                    <div className="flex items-center gap-2 mt-1">
                      {item.platforms?.map((p) => (
                        <span key={p} className="text-xs px-2 py-0.5 rounded-full bg-[hsl(var(--muted))]">
                          {platformNames[p] || p}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`text-xs px-2 py-1 rounded-full ${statusColors[item.status] || "bg-gray-100 text-gray-700"}`}>
                      {statusLabels[item.status] || item.status}
                    </span>
                    <span className="text-xs text-[hsl(var(--muted-foreground))]">{timeAgo(item.created_at)}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-[hsl(var(--muted-foreground))]">
              <FileVideo className="w-10 h-10 mx-auto mb-2 opacity-50" />
              <p className="text-sm">Henüz içerik yok</p>
              <Link href="/content" className="text-sm text-[hsl(var(--primary))] hover:underline mt-1 inline-block">
                İlk içeriğini oluştur →
              </Link>
            </div>
          )}
        </div>

        <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5">
          <h3 className="font-semibold mb-4">Haftalık Özet</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-[hsl(var(--muted-foreground))]">Bu hafta oluşturulan</span>
              <span className="font-semibold">{summary.week_content_count} içerik</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-[hsl(var(--muted-foreground))]">Yayınlanan</span>
              <span className="font-semibold text-green-600">{summary.published_count}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-[hsl(var(--muted-foreground))]">Zamanlanmış</span>
              <span className="font-semibold text-blue-600">{summary.scheduled_count}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-[hsl(var(--muted-foreground))]">Başarısız</span>
              <span className="font-semibold text-red-600">{summary.failed_count}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
