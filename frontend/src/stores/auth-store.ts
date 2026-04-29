import { create } from "zustand";

interface AuthState {
  token: string | null;
  user: any | null;
  setAuth: (token: string, user: any) => void;
  logout: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: typeof window !== "undefined" ? localStorage.getItem("access_token") : null,
  user: null,
  setAuth: (token, user) => {
    localStorage.setItem("access_token", token);
    set({ token, user });
  },
  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    set({ token: null, user: null });
  },
  isAuthenticated: () => !!get().token,
}));
