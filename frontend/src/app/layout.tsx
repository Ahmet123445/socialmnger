import type { Metadata } from "next";
import "./globals.css";
import QueryProvider from "@/providers/query-provider";
import { Toaster } from "react-hot-toast";

export const metadata: Metadata = {
  title: "MedyaPanel — Sosyal Medya Kontrol Odası",
  description: "TikTok, X/Twitter, YouTube ve Instagram içerik yönetim ve analiz uygulaması",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr" suppressHydrationWarning>
      <body className="min-h-screen antialiased">
        <QueryProvider>
          {children}
          <Toaster position="top-right" />
        </QueryProvider>
      </body>
    </html>
  );
}
