import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Security: disable X-Powered-By header to prevent server fingerprinting
  poweredByHeader: false,

  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,

  // Security: HTTP Response Headers for defense-in-depth against XSS, clickjacking, and MIME-sniffing
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          { key: "X-DNS-Prefetch-Control", value: "on" },
          {
            key: "Strict-Transport-Security",
            value: "max-age=63072000; includeSubDomains; preload",
          },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
