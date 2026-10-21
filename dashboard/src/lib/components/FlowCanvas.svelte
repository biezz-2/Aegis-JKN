<script lang="ts">
  import { SvelteFlow, Background, Controls, MiniMap, type Node, type Edge } from '@xyflow/svelte';
  import CustomNode from './CustomNode.svelte';

  /* Alur triase tiga tingkat Aegis-JKN, bukan alur persetujuan otomatis:
     tahap akhir tetap adalah penskalaan antrean, keputusan tetap pada manusia. */
  let nodes: Node[] = [
    {
      id: '1',
      type: 'custom',
      position: { x: 50, y: 50 },
      data: { label: 'Klaim masuk', color: '#3987e5' }
    },
    {
      id: '2',
      type: 'custom',
      position: { x: 250, y: 50 },
      data: { label: 'Tier-1 Aturan', color: '#199e70' }
    },
    {
      id: '3',
      type: 'custom',
      position: { x: 450, y: 50 },
      data: { label: 'Tier-2 XGBoost', color: '#d95926' }
    },
    {
      id: '4',
      type: 'custom',
      position: { x: 650, y: 50 },
      data: { label: 'Tier-3 GCN', color: '#3987e5' }
    },
    {
      id: '5',
      type: 'custom',
      position: { x: 850, y: 50 },
      data: { label: 'Antrean verifikator', color: '#199e70' }
    }
  ];

  let edges: Edge[] = [
    { id: 'e1-2', source: '1', target: '2', animated: true, style: 'stroke: #3987e5' },
    { id: 'e2-3', source: '2', target: '3', animated: true, style: 'stroke: #199e70' },
    { id: 'e3-4', source: '3', target: '4', animated: true, style: 'stroke: #d95926' },
    { id: 'e4-5', source: '4', target: '5', animated: true, style: 'stroke: #3987e5' }
  ];

  const nodeTypes = { custom: CustomNode };

  const onconnect = (params: unknown) => {
    console.log('Edge connected:', params);
  };
</script>

<div class="w-full h-[600px] bg-slate-950 rounded-3xl overflow-hidden border border-white/10 relative">
  <SvelteFlow {nodes} {edges} {nodeTypes} {onconnect} fitView colorMode="dark">
    <Background patternColor="#334155" />
    <Controls />
    <MiniMap zoomable pannable />
  </SvelteFlow>
</div>