---
title: Verifier Dashboard
type: concept
tags: [sveltekit, svelte, vite, hitl, dashboard]
related:
  - "[[Aegis-JKN Overview]]"
  - "[[Dataset Contract]]"
  - "[[Academic Paper]]"
  - "[[Dashboard Development]]"
sources:
  - dashboard/src/
  - dashboard/docs/ARCHITECTURE.md
---

# Verifier Dashboard

The SvelteKit dashboard provides a claims queue with filter/search, an EMR evidence pane, a synthetic AI-evidence pane, conditional syndicate grouping, and note-required human decisions.

## Routes

| Route | Purpose |
|---|---|
| `/` | Public landing page (Aegis JKN Flow). CTAs link to `/demo`. |
| `/demo` | **Dashboard Verifikator Aegis-JKN** — the verifier workspace. |

## Data flow

`RawClaim` preserves the actual source fields. `lib/claims.ts` normalizes only in memory, filters/sorts locally, and exposes a selected claim to UI panels. The `auditLog` store (`store/auditLog.ts`, a Svelte `writable`) appends human actions to device-local `localStorage` scoped by source hash.

## Boundaries

The dashboard never trains or executes a model, never calls SATUSEHAT/V-Claim, and never auto-approves a claim. The syndicate graph is a transparent grouping derived from the existing `Sindikat` label, not discovered graph intelligence. Audit entries are device-local demonstration data, not a production audit trail.

## Local development

Run `cd dashboard && npm i && npm run dev` and open `http://localhost:5175`. See `dashboard/docs/README.md` and `dashboard/docs/DEPLOYMENT.md` for safeguards.
