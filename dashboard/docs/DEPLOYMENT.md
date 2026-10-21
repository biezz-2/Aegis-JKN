# Deployment

## Scope boundary

Deploy this project as a **separate internal-tool deployment**, not as a route inside `aegisjkn.vercel.app` public showcase. The code is an environment-free client-side app, but public hosting alone does not provide internal access control.

## Internal host (PM2)

The app is built with `@sveltejs/adapter-node` and runs as a Node process.

```bash
cd dashboard
npm ci
npm run build          # emits dashboard/build/index.js
cd ..
pm2 start ecosystem.config.cjs
pm2 logs aegis-dashboard
pm2 save
```

`ecosystem.config.cjs` pins:

- `PORT=5175`, `HOST=0.0.0.0`
- `NODE_ENV=production`
- `max_memory_restart: 500M`, `autorestart: true`, `watch: false`

`HOST=0.0.0.0` only makes the server reachable; it is not authentication or access control. Restrict TCP/5175 to trusted LAN or tailnet peers with the host firewall.

## Vercel settings (optional)

1. Import the repository/project directory containing `dashboard/`.
2. Set **Root Directory** to `dashboard`.
3. Use framework preset **SvelteKit**.
4. Build command: `npm run build`.
5. Install command: `npm ci` when `package-lock.json` is committed.
6. No environment variables are required for the current implementation.

## Required controls before any non-demo deployment

- Protect the deployment with organization SSO or an authenticated reverse proxy.
- Replace device-local `localStorage` audit logging with authenticated, encrypted, append-only server storage.
- Implement role-based authorization, retention/deletion policy, incident logging, audit export, and Safe-Mode Fallback telemetry.
- Perform privacy impact assessment and security review for UU PDP/health-data obligations.
- Use approved pseudonymization/tokenization and do not ship real patient data in static assets.
- Validate SATUSEHAT/FHIR and V-Claim contracts through formal partner authorization; they are absent from this prototype.

## Cache and data warning

The synthetic JSON is bundled into the client output. Never replace it with real data: static assets can be cached and copied. Production data must be fetched after authenticated authorization, under data minimization and institutional retention controls.

## Verification

Before deployment, run:

```bash
npm ci
npm run typecheck
npm test
npm run build
```

Then manually confirm claim selection, filter/sort, conditional syndicate graph, note-required HITL modals, audit entries, and the permanent HITL disclaimer.
