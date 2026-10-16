# Sentinel's Security Journal

## 2025-05-18 - HTTP Security Headers Defense in Depth
**Vulnerability:** Missing HTTP security headers in application response headers allowed potential risks such as clickjacking (framing), MIME-type sniffing, referrer leakage, and XSS.
**Learning:** Next.js application lacked explicitly configured HTTP security headers in `next.config.ts`.
**Prevention:** Always enforce HTTP security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `X-XSS-Protection`, `Permissions-Policy`) at the Next.js framework configuration level.
