## 2025-05-18 - Missing Security HTTP Headers in Next.js Application
**Vulnerability:** The application was missing standard security HTTP headers (such as `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `Strict-Transport-Security`, and `Content-Security-Policy`), leaving the web application vulnerable to clickjacking, MIME sniffing, and cross-site embedding risks.
**Learning:** Next.js applications require explicit `headers()` configuration in `next.config.ts` to ensure all server responses enforce security policy headers across static and dynamic routes.
**Prevention:** Always configure `headers()` in `next.config.ts` with OWASP-recommended security headers for production web apps.
