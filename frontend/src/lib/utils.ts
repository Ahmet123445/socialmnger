import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(num: number): string {
  if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + "M";
  if (num >= 1_000) return (num / 1_000).toFixed(1) + "B";
  return num.toString();
}

export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString("tr-TR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export function formatDateTime(date: string | Date): string {
  return new Date(date).toLocaleDateString("tr-TR", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function timeAgo(date: string | Date): string {
  const now = new Date();
  const d = new Date(date);
  const diffMs = now.getTime() - d.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);

  if (diffMin < 1) return "Az önce";
  if (diffMin < 60) return `${diffMin} dakika önce`;
  if (diffHour < 24) return `${diffHour} saat önce`;
  if (diffDay < 7) return `${diffDay} gün önce`;
  return formatDate(date);
}

export const platformColors: Record<string, string> = {
  youtube: "bg-red-500",
  tiktok: "bg-black",
  instagram: "bg-gradient-to-r from-purple-500 to-pink-500",
  twitter: "bg-sky-500",
};

export const platformNames: Record<string, string> = {
  youtube: "YouTube",
  tiktok: "TikTok",
  instagram: "Instagram",
  twitter: "X/Twitter",
};

export const statusLabels: Record<string, string> = {
  draft: "Taslak",
  scheduled: "Zamanlandı",
  publishing: "Yayınlanıyor",
  published: "Yayınlandı",
  failed: "Başarısız",
  queued: "Sırada",
  processing: "İşleniyor",
  completed: "Tamamlandı",
  retrying: "Yeniden Deneniyor",
};

export const statusColors: Record<string, string> = {
  draft: "bg-gray-100 text-gray-700",
  scheduled: "bg-blue-100 text-blue-700",
  publishing: "bg-yellow-100 text-yellow-700",
  published: "bg-green-100 text-green-700",
  failed: "bg-red-100 text-red-700",
  queued: "bg-gray-100 text-gray-700",
  processing: "bg-yellow-100 text-yellow-700",
  completed: "bg-green-100 text-green-700",
  retrying: "bg-orange-100 text-orange-700",
};
