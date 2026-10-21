<script lang="ts">
  import { SvelteFlow, Background, Controls, type Node, type Edge } from '@xyflow/svelte';
  import { relatedSyndicateClaims } from '@/lib/claims';
  import type { Claim } from '@/types/claims';
  import SyndicateNode from './SyndicateNode.svelte';

  let { claim }: { claim: Claim } = $props();

  const nodeTypes = { syndicate: SyndicateNode };

  const group = $derived(relatedSyndicateClaims(claim));

  /**
   * The dataset has no edge list. This graph is a transparent grouping derived from
   * the existing `Sindikat` label: one facility node, doctor nodes, and patient nodes
   * for every claim sharing that label. It is an illustration, not discovered graph
   * intelligence.
   */
  const graph = $derived.by(() => {
    if (!claim.syndromeId) return { nodes: [] as Node[], edges: [] as Edge[] };

    const nodes: Node[] = [];
    const edges: Edge[] = [];
    const facilities = new Set(group.map((item) => item.hospital));
    const doctors = new Map<string, string>();
    const patients = new Map<string, string>();

    let y = 0;
    for (const facility of facilities) {
      nodes.push({
        id: `faskes:${facility}`,
        type: 'syndicate',
        position: { x: 0, y },
        data: { label: facility, kind: 'Faskes' }
      });
      y += 90;
    }

    for (const item of group) {
      const doctorId = item.doctor.pseudonymId ?? item.doctor.display;
      if (!doctors.has(doctorId)) {
        doctors.set(doctorId, item.doctor.display);
        nodes.push({
          id: `dokter:${doctorId}`,
          type: 'syndicate',
          position: { x: 240, y: doctors.size * 90 - 90 },
          data: { label: doctorId, kind: 'Dokter' }
        });
        edges.push({
          id: `faskes:${item.hospital}-dokter:${doctorId}`,
          source: `faskes:${item.hospital}`,
          target: `dokter:${doctorId}`
        });
      }

      const patientId = item.patient.pseudonymId ?? item.patient.display;
      if (!patients.has(patientId)) {
        patients.set(patientId, item.patient.display);
        nodes.push({
          id: `pasien:${patientId}`,
          type: 'syndicate',
          position: { x: 480, y: patients.size * 90 - 90 },
          data: { label: patientId, kind: 'Pasien' }
        });
        edges.push({
          id: `dokter:${doctorId}-pasien:${patientId}`,
          source: `dokter:${doctorId}`,
          target: `pasien:${patientId}`
        });
      }
    }

    return { nodes, edges };
  });
</script>

{#if claim.syndromeId}
  <div class="space-y-3">
    <div>
      <h3 class="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Graf sindikat</h3>
      <p class="mt-1 text-xs text-slate-500">
        Kelompok sintetis dari label <span class="font-mono text-slate-400">{claim.syndromeId}</span> — bukan
        graph produksi.
      </p>
    </div>

    <div class="h-[280px] overflow-hidden rounded-xl border border-slate-800 bg-slate-950">
      <SvelteFlow nodes={graph.nodes} edges={graph.edges} {nodeTypes} fitView colorMode="dark">
        <Background patternColor="#334155" />
        <Controls />
      </SvelteFlow>
    </div>

    <p class="text-xs text-slate-500">
      {group.length} klaim berbagi label ini: {group.map((item) => item.id).join(', ')}
    </p>
  </div>
{:else}
  <div class="space-y-2">
    <h3 class="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Graf sindikat</h3>
    <p class="rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm text-slate-500">
      Klaim ini tidak memiliki label sindikat, sehingga tidak ada graf yang ditampilkan.
    </p>
  </div>
{/if}
