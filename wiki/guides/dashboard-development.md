---
title: Dashboard Development
type: guide
tags: [development, verification, deployment]
related:
  - "[[Verifier Dashboard]]"
sources:
  - dashboard/package.json
  - dashboard/vite.config.ts
  - ecosystem.config.cjs
---

# Dashboard Development

```bash
cd dashboard
npm i
npm run typecheck
npm test
npm run build
npm run dev
```

The dev server is pinned to port **5175** (`strictPort`) in `vite.config.ts`.

## Deployment

```bash
cd dashboard && npm run build
cd .. && pm2 start ecosystem.config.cjs
pm2 logs aegis-dashboard
```

`ecosystem.config.cjs` runs `dashboard/build/index.js` (adapter-node) with `PORT=5175`, `HOST=0.0.0.0`.

## Path aliases

`@` maps to `src/` — declared in `svelte.config.js` (SvelteKit alias) and `vite.config.ts` (Vitest alias). Both are required: Vite resolves it for the app and for tests.

## Svelte 5 conventions

- Components use runes (`$props()`, `$state`, `$derived`), not `export let`.
- `class` is a reserved word in Svelte 5, so component styles accept it as a prop via `let { class: className = '' } = $props()`.
- `@xyflow/svelte` v1 requires `nodeTypes` to map to Svelte **components**, and its `colorMode="dark"` prop is needed for dark-theme controls.

## Before changing the synthetic source

Obtain explicit approval. Recalculate its SHA-256, audit the schema, update `docs/DATA_SCHEMA.md`, and refresh the dashboard copy only as a byte-identical transfer.
