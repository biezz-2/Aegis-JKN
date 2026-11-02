import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,
  // Security enhancement: Enforce defensive HTTP headers across all routes
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "X-Frame-Options", value: "DENY" }, // Mitigates clickjacking attacks
          { key: "X-Content-Type-Options", value: "nosniff" }, // Prevents MIME-type sniffing
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" }, // Prevents sensitive URL leakage
          { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" }, // Restricts unneeded device APIs
          { key: "X-XSS-Protection", value: "1; mode=block" }, // Legacy XSS protection filter
        ],
      },
    ];
  },
};

export default nextConfig;
