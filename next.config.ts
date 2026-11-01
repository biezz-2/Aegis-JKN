import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,
  // Security Enhancement: Enforce HTTP security headers across all routes
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          // Prevent MIME-sniffing
          { key: "X-Content-Type-Options", value: "nosniff" },
          // Prevent clickjacking via iframes
          { key: "X-Frame-Options", value: "DENY" },
          // Restrict cross-site referrer leakage
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          // Legacy XSS filter for older browsers
          { key: "X-XSS-Protection", value: "1; mode=block" },
          // Restrict browser features and APIs
          { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
        ],
      },
    ];
  },
};

export default nextConfig;
