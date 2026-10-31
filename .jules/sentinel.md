# Sentinel Security Journal

## 2026-10-31 - Global HTTP Security Headers in Next.js
**Vulnerability:** The application was serving responses without essential HTTP security headers (e.g., `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, and `Strict-Transport-Security`). This exposed users to clickjacking attacks via iframe embedding, MIME-confusion attacks, and leakage of sensitive URLs through HTTP referrers.
**Learning:** In Next.js App Router applications, configuring security headers at the framework level in `next.config.ts` via the `headers()` async hook guarantees uniform defense-in-depth across all server-rendered and statically generated routes without relying on edge-proxy specific directives.
**Prevention:** Always define a comprehensive security headers profile (`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Strict-Transport-Security`, `Permissions-Policy`) in `next.config.ts` covering `/:path*` for any web application facing untrusted networks.
