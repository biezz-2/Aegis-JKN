<script lang="ts">
  import { Search, SlidersHorizontal } from 'lucide-svelte';
  import { deriveRiskBadge, filterClaims, sortByPriority, type ClaimFilters } from '@/lib/claims';
  import type { Claim } from '@/types/claims';
  import RiskBadge from './RiskBadge.svelte';

  let {
    claims,
    selectedId,
    onselect
  }: {
    claims: Claim[];
    selectedId: string | null;
    onselect: (claim: Claim) => void;
  } = $props();

  let query = $state('');
  let risk = $state<ClaimFilters['risk']>('all');
  let contradiction = $state<ClaimFilters['contradiction']>('all');
  let syndrome = $state<ClaimFilters['syndrome']>('all');

  const visible = $derived(
    sortByPriority(filterClaims(claims, { query, risk, contradiction, syndrome }))
  );
</script>

<div class="flex h-full flex-col gap-4">
  <div class="flex items-center gap-2">
    <div class="relative flex-1">
      <Search class="pointer-events-none absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-slate-500" />
      <input
        type="search"
        bind:value={query}
        placeholder="Cari klaim, pasien, dokter, faskes…"
        class="w-full rounded-xl border border-slate-800 bg-slate-950 py-2.5 pr-3 pl-9 text-sm text-slate-200 placeholder:text-slate-500 focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
      />
    </div>
    <span class="inline-flex items-center gap-1.5 rounded-xl border border-slate-800 bg-slate-950 px-3 py-2.5 text-xs text-slate-400">
      <SlidersHorizontal class="h-3.5 w-3.5" />
      {visible.length}/{claims.length}
    </span>
  </div>

  <div class="flex flex-wrap gap-2">
    <select
      bind:value={risk}
      class="rounded-lg border border-slate-800 bg-slate-950 px-2.5 py-1.5 text-xs text-slate-300 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
    >
      <option value="all">Semua risiko</option>
      <option value="fraud">Fraud</option>
      <option value="high">Tinggi</option>
      <option value="medium">Sedang</option>
      <option value="low">Rendah</option>
    </select>
    <select
      bind:value={contradiction}
      class="rounded-lg border border-slate-800 bg-slate-950 px-2.5 py-1.5 text-xs text-slate-300 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
    >
      <option value="all">Kontradiksi: semua</option>
      <option value="yes">Kontradiksi ada</option>
      <option value="no">Tanpa kontradiksi</option>
    </select>
    <select
      bind:value={syndrome}
      class="rounded-lg border border-slate-800 bg-slate-950 px-2.5 py-1.5 text-xs text-slate-300 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
    >
      <option value="all">Sindikat: semua</option>
      <option value="yes">Hanya bersindikat</option>
    </select>
  </div>

  <div class="-mr-2 min-h-0 flex-1 overflow-y-auto pr-2">
    <table class="w-full border-collapse text-left text-sm">
      <thead class="sticky top-0 z-10 bg-slate-950 text-xs tracking-wide text-slate-500 uppercase">
        <tr>
          <th class="w-28 py-2 pr-2 font-medium">Klaim</th>
          <th class="py-2 pr-2 font-medium">Pasien</th>
          <th class="w-12 py-2 pr-2 font-medium">Skor</th>
          <th class="w-24 py-2 font-medium">Status</th>
        </tr>
      </thead>
      <tbody>
        {#each visible as claim (claim.id)}
          <tr
            onclick={() => onselect(claim)}
            onkeydown={(event) => {
              if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                onselect(claim);
              }
            }}
            role="button"
            tabindex="0"
            aria-pressed={claim.id === selectedId}
            class="cursor-pointer border-t border-slate-900 transition-colors hover:bg-slate-900/60 {claim.id === selectedId
              ? 'bg-blue-500/10'
              : ''}"
          >
            <td class="py-2.5 pr-2">
              <div class="font-mono text-slate-200">{claim.id}</div>
              <div class="text-xs whitespace-nowrap text-slate-500">{claim.hospital}</div>
            </td>
            <td class="py-2.5 pr-2">
              <div class="truncate text-slate-300">{claim.patient.display}</div>
              <div class="truncate text-xs text-slate-500">{claim.mode ?? '—'}</div>
            </td>
            <td class="py-2.5 pr-2 font-mono text-slate-300">{claim.fraudScore.toFixed(2)}</td>
            <td class="py-2.5">
              <RiskBadge label={deriveRiskBadge(claim)} />
            </td>
          </tr>
        {:else}
          <tr>
            <td colspan="4" class="py-8 text-center text-sm text-slate-500">
              Tidak ada klaim yang cocok dengan filter.
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>
