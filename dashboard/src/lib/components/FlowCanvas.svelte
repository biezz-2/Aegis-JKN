<script lang="ts">
  import { SvelteFlow, Background, Controls, MiniMap, type Node, type Edge } from '@xyflow/svelte';
  import CustomNode from './CustomNode.svelte';

  let nodes: Node[] = [
    {
      id: '1',
      type: 'custom',
      position: { x: 50, y: 50 },
      data: { label: 'Input KLAIM', color: '#3b82f6' }
    },
    {
      id: '2',
      type: 'custom',
      position: { x: 250, y: 50 },
      data: { label: 'Validasi JKN', color: '#22c55e' }
    },
    {
      id: '3',
      type: 'custom',
      position: { x: 450, y: 50 },
      data: { label: 'AI Approval', color: '#eab308' }
    },
    {
      id: '4',
      type: 'custom',
      position: { x: 650, y: 50 },
      data: { label: 'Payment Gateway', color: '#a855f7' }
    },
    {
      id: '5',
      type: 'custom',
      position: { x: 850, y: 50 },
      data: { label: 'Selesai', color: '#ec4899' }
    }
  ];

  let edges: Edge[] = [
    { id: 'e1-2', source: '1', target: '2', animated: true, style: 'stroke: #3b82f6' },
    { id: 'e2-3', source: '2', target: '3', animated: true, style: 'stroke: #22c55e' },
    { id: 'e3-4', source: '3', target: '4', animated: true, style: 'stroke: #eab308' },
    { id: 'e4-5', source: '4', target: '5', animated: true, style: 'stroke: #a855f7' }
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