<script lang="ts">
  import type { Claim } from '@/types/claims';

  let { claim }: { claim: Claim } = $props();

  const CHANNELS = [
    { key: 'topology', label: 'Topologi', color: '#3b82f6' },
    { key: 'feature', label: 'Fitur', color: '#22c55e' },
    { key: 'semantic', label: 'Semantik', color: '#eab308' }
  ] as const;

  const bars = $derived(
    claim.channelContribution
      ? CHANNELS.map((channel) => ({
          ...channel,
          value: claim.channelContribution![channel.key]
        }))
      : []
  );
</script>

<div class="space-y-4">
  <div>
    <h3 class="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Kontribusi saluran</h3>
    <p class="mt-1 text-xs text-slate-500">
      Nilai sintetis dari dataset. Tidak selalu berjumlah 1 dan bukan probabilitas.
    </p>
  </div>

  {#if bars.length > 0}
    <div class="space-y-3">
      {#each bars as bar (bar.key)}
        <div>
          <div class="flex items-baseline justify-between text-sm">
            <span class="text-slate-300">{bar.label}</span>
            <span class="font-mono text-slate-400">{bar.value.toFixed(2)}</span>
          </div>
          <div class="mt-1 h-2 overflow-hidden rounded-full bg-slate-800">
            <div
              class="h-full rounded-full transition-[width] duration-500"
              style="width: {Math.min(Math.max(bar.value, 0), 1) * 100}%; background-color: {bar.color};"
            ></div>
          </div>
        </div>
      {/each}
    </div>

    <table class="w-full text-left text-xs">
      <caption class="sr-only">Kontribusi tiga saluran</caption>
      <thead class="text-slate-500">
        <tr>
          <th scope="col" class="py-1 font-medium">Saluran</th>
          <th scope="col" class="py-1 text-right font-medium">Nilai</th>
        </tr>
      </thead>
      <tbody class="text-slate-300">
        {#each bars as bar (bar.key)}
          <tr class="border-t border-slate-800">
            <td class="py-1">{bar.label}</td>
            <td class="py-1 text-right font-mono">{bar.value.toFixed(2)}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {:else}
    <p class="rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm text-slate-500">
      Kontribusi saluran tidak tersedia pada klaim ini.
    </p>
  {/if}

  <div>
    <h3 class="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Sinyal SHAP</h3>
    {#if claim.shapEvidence.hasDominantSignal}
      <ul class="mt-2 space-y-1.5">
        {#each claim.shapEvidence.clauses as clause (clause)}
          <li class="flex gap-2 text-sm text-slate-300">
            <span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-slate-600"></span>
            <span>{clause}</span>
          </li>
        {/each}
      </ul>
      <p class="mt-2 text-xs text-slate-500">
        Sinyal SHAP disajikan sebagai prosa. Dashboard tidak mengarang batang SHAP per fitur.
      </p>
    {:else}
      <p class="mt-2 text-sm text-slate-500">Tidak ada sinyal dominan pada klaim ini.</p>
    {/if}
  </div>
</div>
