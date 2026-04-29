"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { ContentItem, AIGenerateResponse } from "@/types";
import {
  Plus,
  Upload,
  Wand2,
  Send,
  Calendar,
  Trash2,
  Edit3,
  X,
  Check,
  Loader2,
  FileVideo,
  Clock,
} from "lucide-react";
import { platformNames, platformColors, statusLabels, statusColors, timeAgo, formatNumber } from "@/lib/utils";
import toast from "react-hot-toast";

function ContentEditor({ item, onClose, onSave }: { item?: ContentItem; onClose: () => void; onSave: () => void }) {
  const [title, setTitle] = useState(item?.title || "");
  const [description, setDescription] = useState(item?.description || "");
  const [platforms, setPlatforms] = useState<string[]>(item?.platforms || []);
  const [generalCaption, setGeneralCaption] = useState(item?.general_caption || "");
  const [generalHashtags, setGeneralHashtags] = useState(item?.general_hashtags || "");
  const [platformCaptions, setPlatformCaptions] = useState<Record<string, string>>(item?.platform_captions || {});
  const [platformHashtags, setPlatformHashtags] = useState<Record<string, string>>(item?.platform_hashtags || {});
  const [scheduledAt, setScheduledAt] = useState(item?.scheduled_at || "");
  const [aiLoading, setAiLoading] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [mediaId, setMediaId] = useState(item?.media_asset_id || "");

  const allPlatforms = ["youtube", "tiktok", "instagram", "twitter"];

  const togglePlatform = (p: string) => {
    setPlatforms((prev) => (prev.includes(p) ? prev.filter((x) => x !== p) : [...prev, p]));
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await api.post("/media/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMediaId(res.data.id);
      toast.success("Video yüklendi!");
    } catch {
      toast.error("Yükleme başarısız");
    } finally {
      setUploading(false);
    }
  };

  const generateAI = async (platform: string, type: string = "caption") => {
    setAiLoading(`${platform}-${type}`);
    try {
      const res = await api.post<AIGenerateResponse>("/ai/generate", {
        platform,
        title,
        description,
        existing_caption: generalCaption,
        generate_type: type,
      });
      if (type === "caption" || type === "all") {
        setPlatformCaptions((prev) => ({ ...prev, [platform]: res.data.caption || "" }));
      }
      if (type === "hashtags" || type === "all") {
        setPlatformHashtags((prev) => ({ ...prev, [platform]: res.data.hashtags || "" }));
      }
      toast.success(`${platformNames[platform]} için AI içerik üretildi!`);
    } catch {
      toast.error("AI içerik üretilemedi");
    } finally {
      setAiLoading(null);
    }
  };

  const generateAllAI = async () => {
    setAiLoading("all");
    try {
      for (const p of platforms) {
        const res = await api.post<AIGenerateResponse>("/ai/generate", {
          platform: p,
          title,
          description,
          existing_caption: generalCaption,
          generate_type: "all",
        });
        setPlatformCaptions((prev) => ({ ...prev, [p]: res.data.caption || "" }));
        setPlatformHashtags((prev) => ({ ...prev, [p]: res.data.hashtags || "" }));
      }
      toast.success("Tüm platformlar için AI içerik üretildi!");
    } catch {
      toast.error("AI içerik üretimi başarısız");
    } finally {
      setAiLoading(null);
    }
  };

  const handleSave = async () => {
    const payload = {
      title,
      description,
      platforms,
      general_caption: generalCaption,
      general_hashtags: generalHashtags,
      platform_captions: platformCaptions,
      platform_hashtags: platformHashtags,
      scheduled_at: scheduledAt || null,
      media_asset_id: mediaId || null,
    };
    try {
      if (item?.id) {
        await api.put(`/content/${item.id}`, payload);
      } else {
        await api.post("/content/", payload);
      }
      toast.success(item?.id ? "İçerik güncellendi!" : "İçerik oluşturuldu!");
      onSave();
    } catch {
      toast.error("Kaydetme başarısız");
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-[hsl(var(--card))] rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto border border-[hsl(var(--border))]">
        <div className="flex items-center justify-between p-6 border-b border-[hsl(var(--border))]">
          <h2 className="text-xl font-bold">{item?.id ? "İçeriği Düzenle" : "Yeni İçerik Oluştur"}</h2>
          <button onClick={onClose} className="p-2 hover:bg-[hsl(var(--accent))] rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">Video Yükle</label>
            <div className="border-2 border-dashed border-[hsl(var(--border))] rounded-xl p-8 text-center hover:border-[hsl(var(--primary))] transition-colors">
              <input type="file" accept="video/*" onChange={handleFileUpload} className="hidden" id="video-upload" />
              <label htmlFor="video-upload" className="cursor-pointer">
                {uploading ? (
                  <Loader2 className="w-10 h-10 mx-auto mb-2 text-[hsl(var(--primary))] animate-spin" />
                ) : (
                  <Upload className="w-10 h-10 mx-auto mb-2 text-[hsl(var(--muted-foreground))]" />
                )}
                <p className="text-sm text-[hsl(var(--muted-foreground))]">
                  {uploading ? "Yükleniyor..." : "Video dosyası seçin veya sürükleyin"}
                </p>
              </label>
              {mediaId && <p className="text-sm text-green-600 mt-2">✓ Video yüklendi</p>}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Başlık</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="İçerik başlığı..."
              className="w-full px-4 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Açıklama</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="İçerik açıklaması..."
              rows={3}
              className="w-full px-4 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] resize-none"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="text-sm font-medium">Platform Seçimi</label>
              {platforms.length > 0 && (
                <button
                  onClick={generateAllAI}
                  disabled={!!aiLoading}
                  className="flex items-center gap-2 text-sm px-3 py-1.5 rounded-lg bg-purple-100 text-purple-700 hover:bg-purple-200 transition-colors disabled:opacity-50"
                >
                  {aiLoading === "all" ? <Loader2 className="w-4 h-4 animate-spin" /> : <Wand2 className="w-4 h-4" />}
                  Tüm Platformlar için AI ile Optimize Et
                </button>
              )}
            </div>
            <div className="flex gap-3">
              {allPlatforms.map((p) => (
                <button
                  key={p}
                  onClick={() => togglePlatform(p)}
                  className={`flex items-center gap-2 px-4 py-2.5 rounded-lg border text-sm font-medium transition-all ${
                    platforms.includes(p)
                      ? "border-[hsl(var(--primary))] bg-[hsl(var(--primary))]/10 text-[hsl(var(--primary))]"
                      : "border-[hsl(var(--border))] hover:border-[hsl(var(--primary))]/50"
                  }`}
                >
                  <span className={`w-3 h-3 rounded-full ${platformColors[p]}`} />
                  {platformNames[p]}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Genel Caption</label>
              <textarea
                value={generalCaption}
                onChange={(e) => setGeneralCaption(e.target.value)}
                placeholder="Tüm platformlar için genel caption..."
                rows={3}
                className="w-full px-4 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] resize-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Genel Hashtag'ler</label>
              <textarea
                value={generalHashtags}
                onChange={(e) => setGeneralHashtags(e.target.value)}
                placeholder="#hashtag1 #hashtag2..."
                rows={3}
                className="w-full px-4 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] resize-none"
              />
            </div>
          </div>

          {platforms.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold mb-3">Platforma Özel İçerik</h3>
              <div className="space-y-4">
                {platforms.map((p) => (
                  <div key={p} className="border border-[hsl(var(--border))] rounded-xl p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <span className={`w-3 h-3 rounded-full ${platformColors[p]}`} />
                        <span className="font-medium text-sm">{platformNames[p]}</span>
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => generateAI(p, "caption")}
                          disabled={!!aiLoading}
                          className="flex items-center gap-1 text-xs px-2.5 py-1.5 rounded-lg bg-purple-100 text-purple-700 hover:bg-purple-200 disabled:opacity-50"
                        >
                          {aiLoading === `${p}-caption` ? <Loader2 className="w-3 h-3 animate-spin" /> : <Wand2 className="w-3 h-3" />}
                          Caption Üret
                        </button>
                        <button
                          onClick={() => generateAI(p, "hashtags")}
                          disabled={!!aiLoading}
                          className="flex items-center gap-1 text-xs px-2.5 py-1.5 rounded-lg bg-blue-100 text-blue-700 hover:bg-blue-200 disabled:opacity-50"
                        >
                          {aiLoading === `${p}-hashtags` ? <Loader2 className="w-3 h-3 animate-spin" /> : <Wand2 className="w-3 h-3" />}
                          Hashtag Üret
                        </button>
                      </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <input
                        type="text"
                        value={platformCaptions[p] || ""}
                        onChange={(e) => setPlatformCaptions((prev) => ({ ...prev, [p]: e.target.value }))}
                        placeholder={`${platformNames[p]} caption...`}
                        className="px-3 py-2 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] text-sm focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
                      />
                      <input
                        type="text"
                        value={platformHashtags[p] || ""}
                        onChange={(e) => setPlatformHashtags((prev) => ({ ...prev, [p]: e.target.value }))}
                        placeholder={`${platformNames[p]} hashtag'ler...`}
                        className="px-3 py-2 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] text-sm focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium mb-2">Zamanlanmış Yayın (Opsiyonel)</label>
            <input
              type="datetime-local"
              value={scheduledAt}
              onChange={(e) => setScheduledAt(e.target.value)}
              className="px-4 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
            />
          </div>
        </div>

        <div className="flex items-center justify-end gap-3 p-6 border-t border-[hsl(var(--border))]">
          <button onClick={onClose} className="px-4 py-2.5 rounded-lg border border-[hsl(var(--border))] text-sm font-medium hover:bg-[hsl(var(--accent))]">
            İptal
          </button>
          <button
            onClick={handleSave}
            disabled={!title.trim()}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] text-sm font-medium hover:opacity-90 disabled:opacity-50"
          >
            <Check className="w-4 h-4" />
            {item?.id ? "Güncelle" : "Kaydet"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function ContentPage() {
  const queryClient = useQueryClient();
  const [showEditor, setShowEditor] = useState(false);
  const [editingItem, setEditingItem] = useState<ContentItem | undefined>();
  const [statusFilter, setStatusFilter] = useState<string>("");

  const { data: items = [], isLoading } = useQuery<ContentItem[]>({
    queryKey: ["content", statusFilter],
    queryFn: async () => {
      const params = statusFilter ? `?status=${statusFilter}` : "";
      const res = await api.get(`/content/${params}`);
      return res.data;
    },
  });

  const publishMutation = useMutation({
    mutationFn: async (contentItemId: string) => {
      const res = await api.post("/content/publish", { content_item_id: contentItemId });
      return res.data;
    },
    onSuccess: () => {
      toast.success("Yayınlatma başlatıldı!");
      queryClient.invalidateQueries({ queryKey: ["content"] });
    },
    onError: () => toast.error("Yayınlatma başarısız"),
  });

  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/content/${id}`);
    },
    onSuccess: () => {
      toast.success("İçerik silindi!");
      queryClient.invalidateQueries({ queryKey: ["content"] });
    },
  });

  const filters = [
    { value: "", label: "Tümü" },
    { value: "draft", label: "Taslak" },
    { value: "scheduled", label: "Zamanlanmış" },
    { value: "publishing", label: "Yayınlanıyor" },
    { value: "published", label: "Yayınlandı" },
    { value: "failed", label: "Başarısız" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">İçerik Stüdyosu</h1>
          <p className="text-sm text-[hsl(var(--muted-foreground))] mt-1">
            Videolarınızı yönetin, AI ile optimize edin ve yayınlayın.
          </p>
        </div>
        <button
          onClick={() => { setEditingItem(undefined); setShowEditor(true); }}
          className="flex items-center gap-2 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] px-4 py-2.5 rounded-lg text-sm font-medium hover:opacity-90"
        >
          <Plus className="w-4 h-4" />
          Yeni İçerik
        </button>
      </div>

      <div className="flex gap-2">
        {filters.map((f) => (
          <button
            key={f.value}
            onClick={() => setStatusFilter(f.value)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              statusFilter === f.value
                ? "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]"
                : "bg-[hsl(var(--card))] border border-[hsl(var(--border))] hover:bg-[hsl(var(--accent))]"
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5 animate-pulse">
              <div className="h-32 bg-[hsl(var(--muted))] rounded" />
            </div>
          ))}
        </div>
      ) : items.length === 0 ? (
        <div className="text-center py-16">
          <FileVideo className="w-16 h-16 mx-auto mb-4 text-[hsl(var(--muted-foreground))] opacity-50" />
          <h3 className="text-lg font-semibold mb-2">Henüz içerik yok</h3>
          <p className="text-[hsl(var(--muted-foreground))] mb-4">İlk içeriğinizi oluşturarak başlayın.</p>
          <button
            onClick={() => { setEditingItem(undefined); setShowEditor(true); }}
            className="inline-flex items-center gap-2 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] px-4 py-2.5 rounded-lg text-sm font-medium hover:opacity-90"
          >
            <Plus className="w-4 h-4" />
            Yeni İçerik Oluştur
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((item) => (
            <div key={item.id} className="bg-[hsl(var(--card))] rounded-xl border border-[hsl(var(--border))] p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold text-sm line-clamp-2 flex-1">{item.title}</h3>
                <span className={`text-xs px-2 py-1 rounded-full ml-2 flex-shrink-0 ${statusColors[item.status]}`}>
                  {statusLabels[item.status]}
                </span>
              </div>

              {item.description && (
                <p className="text-xs text-[hsl(var(--muted-foreground))] line-clamp-2 mb-3">{item.description}</p>
              )}

              <div className="flex flex-wrap gap-1.5 mb-4">
                {item.platforms?.map((p) => (
                  <span key={p} className="flex items-center gap-1.5 text-xs px-2 py-1 rounded-full bg-[hsl(var(--muted))]">
                    <span className={`w-2 h-2 rounded-full ${platformColors[p]}`} />
                    {platformNames[p]}
                  </span>
                ))}
              </div>

              <div className="flex items-center gap-1.5 text-xs text-[hsl(var(--muted-foreground))] mb-4">
                <Clock className="w-3.5 h-3.5" />
                {timeAgo(item.created_at)}
              </div>

              <div className="flex items-center gap-2">
                {(item.status === "draft" || item.status === "scheduled") && (
                  <button
                    onClick={() => publishMutation.mutate(item.id)}
                    className="flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg bg-green-100 text-green-700 hover:bg-green-200"
                  >
                    <Send className="w-3 h-3" />
                    Yayınla
                  </button>
                )}
                <button
                  onClick={() => { setEditingItem(item); setShowEditor(true); }}
                  className="flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg bg-[hsl(var(--muted))] hover:bg-[hsl(var(--accent))]"
                >
                  <Edit3 className="w-3 h-3" />
                  Düzenle
                </button>
                <button
                  onClick={() => deleteMutation.mutate(item.id)}
                  className="flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 ml-auto"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {showEditor && (
        <ContentEditor
          item={editingItem}
          onClose={() => setShowEditor(false)}
          onSave={() => {
            setShowEditor(false);
            queryClient.invalidateQueries({ queryKey: ["content"] });
          }}
        />
      )}
    </div>
  );
}
