import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,
  // Security enhancement: disable X-Powered-By header to avoid disclosing backend technology
  poweredByHeader: false,
  // Security enhancement: define defense-in-depth HTTP security headers
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          // Prevent site framing to protect against clickjacking attacks
          { key: "X-Frame-Options", value: "DENY" },
          // Prevent MIME-type sniffing attacks
          { key: "X-Content-Type-Options", value: "nosniff" },
          // Control referrer data leakage across origins
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          // Restrict unnecessary browser permissions and feature access
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
          // Enable legacy cross-site scripting filter in older browsers
          { key: "X-XSS-Protection", value: "1; mode=block" },
        ],
      },
    ];
  },
};

export default nextConfig;
