// Backend endpoints and optional sign-in settings shared by server and browser.

export type RuntimeEnv = {
  apiUrl: string;
  wsUrl: string;
  googleClientId: string;
  // WorkOS AuthKit (hosted identity unification). When set, the web sign-in
  // goes through WorkOS (Google upstream) so web + MCP share one user_id. Empty
  // keeps today's Google-direct sign-in (or no auth at all in self-host).
  workosClientId: string;
  workosRedirectUri: string;
  workosUseLocalStorageRefresh: boolean;
};

declare global {
  interface Window {
    __SC_ENV__?: RuntimeEnv;
  }
}

// Global name shared between the server injector and the client reader.
export const SC_ENV_GLOBAL = "__SC_ENV__";

// Local demo defaults: backend on :8000 and no sign-in configuration.
const DEV_DEFAULT: RuntimeEnv = {
  apiUrl: "http://localhost:8000",
  wsUrl: "ws://localhost:8000",
  googleClientId: "",
  workosClientId: "",
  workosRedirectUri: "",
  workosUseLocalStorageRefresh: false,
};

// Derive the ws(s):// origin from an http(s):// origin when WS_URL is unset.
function deriveWsUrl(apiUrl: string): string {
  return apiUrl.replace(/^http/, "ws");
}

function envFlag(name: string, fallbackName?: string): boolean {
  const raw = process.env[name] || (fallbackName ? process.env[fallbackName] : "");
  return ["1", "true", "yes", "on"].includes((raw || "").trim().toLowerCase());
}

// Server-side: read optional backend and sign-in settings for the root layout.
export function readServerEnv(): RuntimeEnv {
  const apiUrl = process.env.API_URL || DEV_DEFAULT.apiUrl;
  const wsUrl = process.env.WS_URL || deriveWsUrl(apiUrl);
  const googleClientId =
    process.env.GOOGLE_CLIENT_ID || process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "";
  const workosClientId =
    process.env.WORKOS_CLIENT_ID || process.env.NEXT_PUBLIC_WORKOS_CLIENT_ID || "";
  const workosRedirectUri =
    process.env.WORKOS_REDIRECT_URI || process.env.NEXT_PUBLIC_WORKOS_REDIRECT_URI || "";
  const workosUseLocalStorageRefresh = envFlag(
    "WORKOS_USE_LOCAL_STORAGE_REFRESH",
    "NEXT_PUBLIC_WORKOS_USE_LOCAL_STORAGE_REFRESH"
  );
  return {
    apiUrl,
    wsUrl,
    googleClientId,
    workosClientId,
    workosRedirectUri,
    workosUseLocalStorageRefresh,
  };
}

// Client-side: read the env injected by the layout. Falls back to the dev
// default (used by `next dev` without injection and by unit tests).
export function getRuntimeEnv(): RuntimeEnv {
  if (typeof window !== "undefined" && window.__SC_ENV__) {
    return window.__SC_ENV__;
  }
  return DEV_DEFAULT;
}

// Coalesce to "" so a partially-populated injected __SC_ENV__ (e.g. an older
// server build that predates the WorkOS fields) never throws on a missing key.
export const getApiBase = (): string => getRuntimeEnv().apiUrl;
export const getWsBase = (): string => getRuntimeEnv().wsUrl;
export const getGoogleClientId = (): string => getRuntimeEnv().googleClientId ?? "";
export const getWorkosClientId = (): string => getRuntimeEnv().workosClientId ?? "";
export const getWorkosRedirectUri = (): string => getRuntimeEnv().workosRedirectUri ?? "";
export const getWorkosUseLocalStorageRefresh = (): boolean =>
  Boolean(getRuntimeEnv().workosUseLocalStorageRefresh);
