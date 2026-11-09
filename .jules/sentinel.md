# Sentinel Journal

## 2026-11-09 - Missing Content-Security-Policy Header in Next.js Server Configuration
**Vulnerability:** The application configured basic HTTP security headers (HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy) in `next.config.ts`, but lacked a `Content-Security-Policy` (CSP) header, leaving client-side execution vulnerable to unrestricted script loading and injection attacks.
**Learning:** Next.js projects relying on custom script executions, styled charts with dynamic styles (e.g. Recharts/CSS variables), and internal iframe previews (e.g. standalone Colab HTML preview in `/public`) require a tailored CSP configuration that permits essential self-hosted resources and frames without opening doors to arbitrary untrusted third-party origins.
**Prevention:** Always define explicit `Content-Security-Policy` directives across all application routes in `next.config.ts` while enforcing `default-src 'self'`, restricting `object-src 'none'`, and bounding frame/script sources.
