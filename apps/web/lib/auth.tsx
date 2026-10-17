"use client";

import React, { createContext, useContext } from "react";
import Link from "next/link";

export const IS_CLERK_ENABLED = Boolean(
  process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY &&
  process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY.trim() !== ""
);

export interface AuthContextType {
  isLoaded: boolean;
  isSignedIn: boolean;
  userId: string | null;
  sessionId: string | null;
  getToken: (options?: { template?: string }) => Promise<string | null>;
  signOut: () => Promise<void>;
}

const defaultAuthContext: AuthContextType = {
  isLoaded: true,
  isSignedIn: true,
  userId: "demo_user",
  sessionId: "demo_session",
  getToken: async () => null,
  signOut: async () => {},
};

const DemoAuthContext = createContext<AuthContextType>(defaultAuthContext);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return (
    <DemoAuthContext.Provider value={defaultAuthContext}>
      {children}
    </DemoAuthContext.Provider>
  );
}

export const ClerkProvider = AuthProvider;

export function useAuth(): AuthContextType {
  return useContext(DemoAuthContext);
}

export function UserButton(_props: { afterSignOutUrl?: string }) {
  return (
    <div className="flex items-center gap-2 px-2.5 py-1 rounded-full border border-orange-500/20 bg-orange-500/5 text-xs font-mono text-orange-300">
      <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
      <span>DEMO MODE</span>
    </div>
  );
}

export function SignIn() {
  return (
    <div className="flex flex-col items-center justify-center p-6 text-center space-y-4">
      <div className="h-10 w-10 rounded-full bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 font-bold font-mono">
        ✓
      </div>
      <div>
        <h2 className="text-lg font-semibold text-white">Demo Mode Active</h2>
        <p className="text-xs text-white/50 mt-1 max-w-xs">
          Clerk authentication is optional and currently disabled. No login required!
        </p>
      </div>
      <Link
        href="/compliance-feed"
        className="w-full py-2.5 px-4 rounded-lg bg-gradient-to-r from-orange-500 to-amber-500 text-black font-semibold text-sm hover:opacity-95 transition"
      >
        Enter Dashboard Directly →
      </Link>
    </div>
  );
}

export function SignUp() {
  return <SignIn />;
}
