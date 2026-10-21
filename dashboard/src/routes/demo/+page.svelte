<script lang="ts">
  import { ArrowLeft, ShieldCheck } from 'lucide-svelte';
  import { claims } from '@/lib/claims';
  import type { Claim } from '@/types/claims';
  import ClaimQueue from '$lib/components/demo/ClaimQueue.svelte';
  import EmrPanel from '$lib/components/demo/EmrPanel.svelte';
  import AiPanel from '$lib/components/demo/AiPanel.svelte';
  import HitlActionBar from '$lib/components/demo/HitlActionBar.svelte';
  import AuditLogPanel from '$lib/components/demo/AuditLogPanel.svelte';

  let selected = $state<Claim | null>(claims[0] ?? null);
</script>

<svelte:head>
  <title>Dashboard Verifikator Aegis-JKN — Demo</title>
  <meta
    name="description"
    content="Demo internal Dashboard Verifikator Aegis-JKN untuk menelaah dataset klaim JKN sintetis."
  />
</svelte:head>

<div class="min-h-screen bg-background">
  <header class="border-b border-slate-800 bg-slate-950">
    <div class="mx-auto flex max-w-[1600px] items-center justify-between gap-4 px-4 py-4">
      <div class="flex items-center gap-3">
        <a
          href="/"
          class="inline-flex items-center gap-1.5 rounded-lg border border-slate-800 px-3 py-1.5 text-sm text-slate-400 transition-colors hover:bg-slate-900 hover:text-slate-200"
        >
          <ArrowLeft class="h-4 w-4" />
          Beranda
        </a>
        <div>
          <h1 class="text-lg font-bold text-slate-100">Dashboard Verifikator Aegis-JKN</h1>
          <p class="text-xs text-slate-500">Demo dataset klaim sintetis · 300 klaim</p>
        </div>
      </div>
      <div class="hidden items-center gap-2 text-xs text-slate-500 sm:flex">
        <ShieldCheck class="h-4 w-4 text-emerald-400" />
        AI memberi rekomendasi, keputusan akhir ada pada verifikator
      </div>
    </div>
  </header>

  <main class="mx-auto grid max-w-[1600px] gap-4 p-4 lg:grid-cols-[minmax(320px,380px)_1fr]">
    <!-- Antrean klaim -->
    <section
      class="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 lg:h-[calc(100vh-7rem)]"
      aria-label="Antrean klaim"
    >
      <h2 class="mb-3 text-sm font-semibold text-slate-200">Antrean klaim</h2>
      <div class="h-[calc(100%-2rem)]">
        <ClaimQueue {claims} selectedId={selected?.id ?? null} onselect={(claim) => (selected = claim)} />
      </div>
    </section>

    <!-- Workspace -->
    <div class="space-y-4">
      {#if selected}
        <section class="rounded-2xl border border-slate-800 bg-slate-900/60 p-4" aria-label="Rekam medis">
          <div class="mb-4 flex flex-wrap items-baseline justify-between gap-2">
            <h2 class="text-sm font-semibold text-slate-200">Rekam medis & bukti</h2>
            <span class="font-mono text-xs text-slate-500">{selected.id}</span>
          </div>
          <div class="grid gap-6 xl:grid-cols-2">
            <EmrPanel claim={selected} />
            <AiPanel claim={selected} />
          </div>
        </section>

        <div class="grid gap-4 xl:grid-cols-[1fr_320px]">
          <section class="rounded-2xl border border-slate-800 bg-slate-900/60 p-4" aria-label="Tindakan">
            <HitlActionBar claim={selected} />
          </section>
          <section class="rounded-2xl border border-slate-800 bg-slate-900/60 p-4" aria-label="Audit lokal">
            <AuditLogPanel />
          </section>
        </div>
      {:else}
        <p class="rounded-2xl border border-slate-800 bg-slate-900/60 p-8 text-center text-slate-500">
          Pilih satu klaim dari antrean untuk mulai menelaah bukti.
        </p>
      {/if}
    </div>
  </main>
</div>
