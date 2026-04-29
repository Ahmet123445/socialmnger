"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { useAuthStore } from "@/stores/auth-store";
import { Zap, Loader2 } from "lucide-react";
import toast from "react-hot-toast";

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((s) => s.setAuth);
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("demo@sosyalmedya.local");
  const [username, setUsername] = useState("demo");
  const [password, setPassword] = useState("demo123");
  const [fullName, setFullName] = useState("Demo Kullanıcı");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const endpoint = isRegister ? "/auth/register" : "/auth/login";
      const payload = isRegister
        ? { email, username, password, full_name: fullName }
        : { email, password };
      const res = await api.post(endpoint, payload);
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);
      setAuth(res.data.access_token, { email, username });
      toast.success(isRegister ? "Hesap oluşturuldu!" : "Giriş başarılı!");
      router.push("/");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "İşlem başarısız");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[hsl(var(--muted))]/50">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Zap className="w-10 h-10 text-[hsl(var(--primary))]" />
          </div>
          <h1 className="text-2xl font-bold">MedyaPanel</h1>
          <p className="text-sm text-[hsl(var(--muted-foreground))] mt-1">
            Sosyal Medya Kontrol Odası
          </p>
        </div>

        <div className="bg-[hsl(var(--card))] rounded-2xl border border-[hsl(var(--border))] p-6">
          <h2 className="text-lg font-semibold mb-4">{isRegister ? "Hesap Oluştur" : "Giriş Yap"}</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1.5">E-posta</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
              />
            </div>

            {isRegister && (
              <>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Kullanıcı Adı</label>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    className="w-full px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5">Ad Soyad</label>
                  <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="w-full px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
                  />
                </div>
              </>
            )}

            <div>
              <label className="block text-sm font-medium mb-1.5">Şifre</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-3 py-2.5 rounded-lg border border-[hsl(var(--border))] bg-[hsl(var(--background))] focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))]"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] font-medium hover:opacity-90 disabled:opacity-50"
            >
              {loading && <Loader2 className="w-4 h-4 animate-spin" />}
              {isRegister ? "Kayıt Ol" : "Giriş Yap"}
            </button>
          </form>

          <div className="mt-4 text-center">
            <button
              onClick={() => setIsRegister(!isRegister)}
              className="text-sm text-[hsl(var(--primary))] hover:underline"
            >
              {isRegister ? "Zaten hesabınız var mı? Giriş yapın" : "Hesabınız yok mu? Kayıt olun"}
            </button>
          </div>

          {!isRegister && (
            <div className="mt-4 p-3 rounded-lg bg-blue-50 border border-blue-200 text-xs text-blue-700">
              <p className="font-medium mb-1">Demo Hesap:</p>
              <p>E-posta: demo@sosyalmedya.local</p>
              <p>Şifre: demo123</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
