## 2026-10-26 - Added HTTP Security Headers
**Vulnerability:** Missing security headers on application routes leading to potential clickjacking, MIME sniffing, and cross-site information leakage.
**Learning:** Next.js applications configured without explicit HTTP headers in `next.config.ts` do not include security headers by default.
**Prevention:** Always configure `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy` headers in `next.config.ts`.
