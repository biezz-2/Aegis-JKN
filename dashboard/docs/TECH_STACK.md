# Aegis-JKN Verifier Dashboard — Tech Stack

Versi di bawah berasal dari `package.json` setelah bootstrap, bukan versi yang diasumsikan dari proposal lama.

| Layer | Dependensi / versi | Alasan |
|---|---|---|
| Build | Vite `5.4.x` | Dev server dan bundler untuk SvelteKit. |
| Framework | SvelteKit `2.x` | Routing file-based, adapter-node untuk deployment PM2. |
| UI runtime | Svelte `5.57` (runes) | State pemilihan klaim dan audit lokal pada satu workspace. |
| Bahasa | TypeScript `~5.6` | Kontrak ketat antara 28 field source JSON dan view model `Claim`. |
| CSS | Tailwind CSS `4.3.3`, `@tailwindcss/vite` `4.3.3` | Styling utility-first tanpa runtime styling. |
| Component primitives | Shadcn-style lokal (`src/lib/components/ui/`) | Primitive Button, Card, Alert, Skeleton bespoke; token warna di `src/index.css`. |
| Graph | `@xyflow/svelte` `1.7.0` | Kanvas graph untuk relasi yang diturunkan dari label sindikat sintetis. |
| Icons | `lucide-svelte` `0.460` | Ikon status dan aksi dengan SVG accessible. |
| Notifikasi | `svelte-sonner` `1.2.1` | Toast global. |
| Testing | Vitest `3.2` | Unit test parser, filter, sort, serta batasan audit log. |
| Type check | `svelte-check` `4.x` | Pemeriksaan tipe Svelte + TypeScript. |
| Deployment | `@sveltejs/adapter-node` `5.5.7` | Output `build/index.js`, dijalankan oleh PM2 pada port `5175`. |

## Deliberate exclusions

Tidak ada backend, database, authentication, API client, FHIR/V-Claim connector, model inference runtime, graph database, atau telemetry. Browser hanya membaca JSON lokal yang dibundel dan menyimpan audit demonstrasi di `localStorage`.

## Dependency note

`radix-svelte`, `sveltekit-superforms`, `zod`, `class-variance-authority`, dan `cn` pernah tercatat di `package.json` tetapi tidak dipakai oleh kode mana pun, dan `radix-svelte@0.9.0` mensyaratkan Svelte 4 sehingga menggagalkan instalasi. Semuanya dihapus.

## Security and privacy posture

`localStorage` bukan audit trail produksi. Production deployment memerlukan authenticated users, authorization, encrypted append-only server storage, retention policy, monitoring Safe-Mode Fallback, dan security assessment sebelum mengolah data pribadi spesifik.
