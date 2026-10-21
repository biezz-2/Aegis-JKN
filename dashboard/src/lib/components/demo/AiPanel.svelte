<script lang="ts">
  import { BrainCircuit } from 'lucide-svelte';
  import { labelTriage } from '@/lib/claims';
  import type { Claim } from '@/types/claims';
  import RiskBadge from './RiskBadge.svelte';
  import ShapChart from './ShapChart.svelte';
  import SyndicateGraph from './SyndicateGraph.svelte';

  let { claim }: { claim: Claim } = $props();
</script>

<div class="space-y-6">
  <div class="flex items-start justify-between gap-4">
    <div>
      <div class="flex items-center gap-2 text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">
        <BrainCircuit class="h-3.5 w-3.5" />
        Bukti AI sintetis
      </div>
      <div class="mt-2 flex items-baseline gap-3">
        <span class="text-4xl font-bold text-slate-100">{claim.fraudScore.toFixed(2)}</span>
        <span class="text-sm text-slate-500">skor fraud</span>
      </div>
      <p class="mt-1 text-xs text-slate-500">{labelTriage(claim.triageStatus)}</p>
    </div>
    <RiskBadge label={claim.syndromeId ? 'Syndicate' : claim.triageStatus === 'escalate' ? 'Escalate' : claim.triageStatus === 'review' ? 'Review' : 'Safe'} />
  </div>

  <ShapChart {claim} />
  <SyndicateGraph {claim} />

  <div>
    <h3 class="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Alasan sistem</h3>
    <p class="mt-2 text-sm leading-relaxed text-slate-300">{claim.reason}</p>
  </div>

  {#if claim.notes}
    <div>
      <h3 class="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Catatan dataset</h3>
      <p class="mt-2 text-sm text-slate-400">{claim.notes}</p>
    </div>
  {/if}

  <p class="rounded-xl border border-slate-800 bg-slate-950 p-3 text-xs text-slate-500">
    Nilai di atas adalah bukti sintetis yang sudah dihitung di dataset. Dashboard tidak menjalankan
    inferensi model maupun memanggil layanan eksternal.
  </p>
</div>
