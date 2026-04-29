"use client";

import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { AISetting, PlatformAccount, SystemSetting } from "@/types";
import { platformNames, platformColors } from "@/lib/utils";
import {
  Settings,
  Key,
  Brain,
  Database,
  Server,
  Save,
  Plus,
  Trash2,
  CheckCircle,
  XCircle,
  Loader2,
  Wand2,
  HardDrive,
} from "lucide-react";
import toast from "react-hot-toast";

function Section({ title, icon: Icon, children }: { title: string; icon: any; children: React.ReactNode }) {
  return (
    <div className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-6">
      <div className="flex items-center gap-2 mb-4">
        <Icon className="w-5 h-5 text-[hsl(var(--primary))]" />
        <h3 className="font-semibold">{title}</h3>
      </div>
      {children}
    </div>
  );
}

export default function SettingsPage() {
  const queryClient = useQueryClient();

  // AI Settings
  const [aiProvider, setAiProvider] = useState("openai");
  const [aiBaseUrl, setAiBaseUrl] = useState("https://api.openai.com/v1");
  const [aiApiKey, setAiApiKey] = useState("");
  const [aiModel, setAiModel] = useState("gpt-4o-mini");
  const [aiTemperature, setAiTemperature] = useState(0.7);

  // Platform accounts
  const [newPlatform, setNewPlatform] = useState("youtube");
  const [newUsername, setNewUsername] = useState("");
  const [newToken, setNewToken] = useState("");

  // System health
  const [health, setHealth] = useState<any>(null);

  const { data: aiSettings = [] } = useQuery<AISetting[]>({
    queryKey: ["ai-settings"],
    queryFn: async () => {
      const res = await api.get("/ai/settings");
      return res.data;
    },
  });

  const { data: platforms = [] } = useQuery<PlatformAccount[]>({
    queryKey: ["platforms"],
    queryFn: async () => {
      const res = await api.get("/settings/platforms");
      return res.data;
    },
  });

  useEffect(() => {
    if (aiSettings.length > 0) {
      const s = aiSettings[0];
      setAiProvider(s.provider);
      setAiBaseUrl(s.base_url);
      setAiModel(s.model_name);
      setAiTemperature(s.temperature);
    }
  }, [aiSettings]);

  useEffect(() => {
    api.get("/settings/health").then((r) => setHealth(r.data)).catch(() => {});
  }, []);

  const saveAISettings = async () => {
    try {
      await api.post("/ai/settings", {
        provider: aiProvider,
        base_url: aiBaseUrl,
        api_key: aiApiKey || undefined,
        model_name: aiModel,
        temperature: aiTemperature,
      });
      toast.success("AI ayarları kaydedildi!");
      queryClient.invalidateQueries({ queryKey: ["ai-settings"] });
    } catch {
      toast.error("Kaydetme başarısız");
    }
  };

  const addPlatform = async () => {
    try {
      await api.post("/settings/platforms", {
        platform: newPlatform,
        platform_username: newUsername || undefined,
        access_token: newToken || undefined,
      });
      toast.success(`${platformNames[newPlatform]} hesabı eklendi!`);
      setNewUsername("");
      setNewToken("");
      queryClient.invalidateQueries({ queryKey: ["platforms"] });
    } catch {
      toast.error("Hesap eklenemedi");
    }
  };

  const removePlatform = async (id: string) => {
    try {
      await api.delete(`/settings/platforms/${id}`);
      toast.success("Hesap silindi!");
      queryClient.invalidateQueries({ queryKey: ["platforms"] });
    } catch {
      toast.error("Silme başarısız");
    }
  };

  const providers = [
    { value: "openai", label: "OpenAI" },
    { value: "anthropic", label: "Anthropic (Claude)" },
    { value: "ollama", label: "Ollama (Yerel)" },
    { value: "custom", label: "Özel (OpenAI Uyumlu)" },
  ];

  const allPlatforms = ["youtube", "tiktok", "instagram", "twitter"];

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold">Ayarlar</h1>
        <p className="text-sm text-[hsl(var(--muted-foreground))] mt-1">
          Platform hesaplarınızı, AI ayarlarınızı ve sistem yapılandırmanızı yönetin.
        </p>
      </div>

      <Section title="Yapay Zeka Ayarları" icon={Brain}>
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1.5">Sağlayıcı</label>
              <select
                value={aiProvider}
                onChange={(e) => setAiProvider(e.target.value)}
                className="w-full px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
              >
                {providers.map((p) => (
                  <option key={p.value} value={p.value}>{p.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">Model Adı</label>
              <input
                type="text"
                value={aiModel}
                onChange={(e) => setAiModel(e.target.value)}
                placeholder="gpt-4o-mini"
                className="w-full px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1.5">Base URL</label>
            <input
              type="text"
              value={aiBaseUrl}
              onChange={(e) => setAiBaseUrl(e.target.value)}
              placeholder="https://api.openai.com/v1"
              className="w-full px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1.5">API Key</label>
            <input
              type="password"
              value={aiApiKey}
              onChange={(e) => setAiApiKey(e.target.value)}
              placeholder="sk-..."
              className="w-full px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
            />
            <p className="text-xs text-[hsl(var(--muted-foreground))] mt-1">
              API key girilmezse mock/AI olmadan çalışır.
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1.5">Temperature: {aiTemperature}</label>
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={aiTemperature}
              onChange={(e) => setAiTemperature(parseFloat(e.target.value))}
              className="w-full"
            />
          </div>

          <button
            onClick={saveAISettings}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] text-sm font-medium hover:opacity-90"
          >
            <Save className="w-4 h-4" />
            AI Ayarlarını Kaydet
          </button>
        </div>
      </Section>

      <Section title="Platform Hesapları" icon={Key}>
        <div className="space-y-4">
          {platforms.length > 0 ? (
            <div className="space-y-3">
              {platforms.map((acc) => (
                <div key={acc.id} className="flex items-center justify-between p-3 rounded-lg bg-[hsl(var(--muted))]/50 border border-[hsl(var(--border))]">
                  <div className="flex items-center gap-3">
                    <span className={`w-3 h-3 rounded-full ${platformColors[acc.platform]}`} />
                    <div>
                      <p className="text-sm font-medium">{platformNames[acc.platform]}</p>
                      {acc.platform_username && (
                        <p className="text-xs text-[hsl(var(--muted-foreground))]">@{acc.platform_username}</p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`text-xs px-2 py-1 rounded-full ${acc.status === "active" ? "bg-green-100 text-green-700" : acc.status === "mock" ? "bg-yellow-100 text-yellow-700" : "bg-red-100 text-red-700"}`}>
                      {acc.status === "active" ? "Aktif" : acc.status === "mock" ? "Mock" : "Hata"}
                    </span>
                    <button onClick={() => removePlatform(acc.id)} className="p-1.5 rounded-lg hover:bg-red-100 text-red-500">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-[hsl(var(--muted-foreground))] py-4 text-center">
              Henüz platform hesabı eklenmedi. Aşağıdan ekleyebilirsiniz.
            </p>
          )}

          <div className="border-t border-[hsl(var(--border))] pt-4">
            <h4 className="text-sm font-medium mb-3">Yeni Hesap Ekle</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <select
                value={newPlatform}
                onChange={(e) => setNewPlatform(e.target.value)}
                className="px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
              >
                {allPlatforms.map((p) => (
                  <option key={p} value={p}>{platformNames[p]}</option>
                ))}
              </select>
              <input
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                placeholder="Kullanıcı adı (opsiyonel)"
                className="px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
              />
              <input
                type="text"
                value={newToken}
                onChange={(e) => setNewToken(e.target.value)}
                placeholder="Access token (opsiyonel)"
                className="px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
              />
            </div>
            <button
              onClick={addPlatform}
              className="flex items-center gap-2 mt-3 px-4 py-2.5 rounded-lg bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] text-sm font-medium hover:opacity-90"
            >
              <Plus className="w-4 h-4" />
              Hesap Ekle
            </button>
            <p className="text-xs text-[hsl(var(--muted-foreground))] mt-2">
              Token girilmezse mock modda çalışır. Gerçek API entegrasyonu için geçerli credential girin.
            </p>
          </div>
        </div>
      </Section>

      <Section title="Sistem Durumu" icon={Server}>
        {health ? (
          <div className="space-y-3">
            {Object.entries(health.services || {}).map(([service, status]) => (
              <div key={service} className="flex items-center justify-between p-3 rounded-lg bg-[hsl(var(--muted))]/50">
                <span className="text-sm font-medium capitalize">{service}</span>
                <div className="flex items-center gap-2">
                  {status === "running" || status === "connected" || status === "available" ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : (
                    <XCircle className="w-4 h-4 text-red-500" />
                  )}
                  <span className="text-sm">{String(status)}</span>
                </div>
              </div>
            ))}
            <div className="mt-4">
              <h4 className="text-sm font-medium mb-2">Yayın Modları</h4>
              {Object.entries(health.publish_modes || {}).map(([platform, mode]) => (
                <div key={platform} className="flex items-center justify-between p-2 text-sm">
                  <span>{platformNames[platform] || platform}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${mode === "mock" ? "bg-yellow-100 text-yellow-700" : "bg-green-100 text-green-700"}`}>
                    {String(mode)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-sm text-[hsl(var(--muted-foreground))]">Sistem durumu yükleniyor...</p>
        )}
      </Section>

      <Section title="Depolama" icon={HardDrive}>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-lg bg-[hsl(var(--muted))]/50">
            <span className="text-sm">Depolama Tipi</span>
            <span className="text-sm font-medium">MinIO (S3 Uyumlu)</span>
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg bg-[hsl(var(--muted))]/50">
            <span className="text-sm">Bucket</span>
            <span className="text-sm font-medium">sosyalmedya-media</span>
          </div>
          <p className="text-xs text-[hsl(var(--muted-foreground))]">
            MinIO konsolu: http://localhost:9001 (minioadmin / minioadmin123)
          </p>
        </div>
      </Section>
    </div>
  );
}
