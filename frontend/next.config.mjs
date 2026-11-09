import { fileURLToPath } from 'url';

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Allow an isolated build dir (e.g. for a spare dev server on another port)
  // so it never collides with the primary dev server's `.next`.
  ...(process.env.NEXT_DIST_DIR ? { distDir: process.env.NEXT_DIST_DIR } : {}),
  // The browser talks directly to the local backend using the runtime URLs
  // exposed by lib/runtime-config.ts and app/layout.tsx.
  webpack: (config) => {
    // digitaljs' root export routes browsers to its full view bundle (jointjs
    // SVG rendering, jquery). The interactive web-sim only needs the headless
    // engine, and the package's exports map doesn't expose it as a subpath —
    // alias the bare specifier to the headless entry (same alias in
    // vitest.config.mts).
    config.resolve.alias = {
      ...config.resolve.alias,
      digitaljs$: fileURLToPath(new URL('./node_modules/digitaljs/lib/circuit.js', import.meta.url)),
    };
    return config;
  },
};

export default nextConfig;
