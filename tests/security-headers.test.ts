import { describe, it, expect } from "vitest";
import nextConfig from "../next.config";

describe("Security Headers Configuration", () => {
  it("should configure headers function", async () => {
    expect(typeof nextConfig.headers).toBe("function");
    if (!nextConfig.headers) return;

    const headersConfig = await nextConfig.headers();
    expect(headersConfig).toHaveLength(1);
    expect(headersConfig[0].source).toBe("/:path*");

    const headers = headersConfig[0].headers;
    const headerMap = new Map(headers.map((h) => [h.key, h.value]));

    expect(headerMap.get("X-Frame-Options")).toBe("DENY");
    expect(headerMap.get("X-Content-Type-Options")).toBe("nosniff");
    expect(headerMap.get("Referrer-Policy")).toBe("origin-when-cross-origin");
    expect(headerMap.get("Strict-Transport-Security")).toContain("max-age=");
    expect(headerMap.get("Permissions-Policy")).toContain("camera=()");
    expect(headerMap.get("Content-Security-Policy")).toContain("default-src 'self'");
  });
});
