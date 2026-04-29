"use client";

import { Plus, Bell, Moon, Sun } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function Topbar() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  return (
    <header className="h-16 bg-[hsl(var(--card))] border-b border-[hsl(var(--border))] flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <h2 className="text-sm font-medium text-[hsl(var(--muted-foreground))]">
          Sosyal Medya Kontrol Odası
        </h2>
      </div>

      <div className="flex items-center gap-3">
        <Link
          href="/content"
          className="flex items-center gap-2 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] px-4 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity"
        >
          <Plus className="w-4 h-4" />
          Yeni İçerik
        </Link>

        <button className="relative p-2 rounded-lg hover:bg-[hsl(var(--accent))] transition-colors">
          <Bell className="w-5 h-5 text-[hsl(var(--muted-foreground))]" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>

        <button
          onClick={() => setDark(!dark)}
          className="p-2 rounded-lg hover:bg-[hsl(var(--accent))] transition-colors"
        >
          {dark ? (
            <Sun className="w-5 h-5 text-[hsl(var(--muted-foreground))]" />
          ) : (
            <Moon className="w-5 h-5 text-[hsl(var(--muted-foreground))]" />
          )}
        </button>
      </div>
    </header>
  );
}
