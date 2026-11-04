## 2026-11-04 - Enforce HTTP Security Headers and Suppress Server Fingerprinting

**Vulnerability:**
The Next.js deployment configuration lacked standard HTTP defense-in-depth security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Strict-Transport-Security`, `Permissions-Policy`, and `X-DNS-Prefetch-Control`) and did not disable the `X-Powered-By` header, leaving the application vulnerable to clickjacking, MIME-type sniffing, insecure cross-origin referrer leaks, unauthorized browser API access, and technology stack fingerprinting.

**Learning:**
While documentation in `docs/deployment/vercel.md` documented the recommended security headers configuration, the actual `next.config.ts` had not implemented the `async headers()` configuration block or `poweredByHeader: false`. Discrepancies between architectural/deployment documentation and live configuration files should always be verified programmatically in Next.js applications.

**Prevention:**
Always verify that `next.config.ts` declares comprehensive security headers matching or exceeding the documented deployment guidelines, test with `curl -I` on the built application output, and ensure automated linting can validate configurations without syntax/linter regressions.
