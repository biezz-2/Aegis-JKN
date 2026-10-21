<script lang="ts">
  import { SvelteFlow, Background, Controls, MiniMap, type Node, type Edge } from '@xyflow/svelte';
  import CustomNode from './CustomNode.svelte';

  /* Alur triase tiga tingkat Aegis-JKN, bukan alur persetujuan otomatis:
     tahap akhir tetap adalah penskalaan antrean, keputusan tetap pada manusia.

     Tahap diurutkan vertikal karena kanvas hero bersifat potret (580px).
     Rantai horizontal lima tahap memaksa zoom 0,54 sehingga label 16px
     ter-render 8,6px — terlalu kecil untuk dibaca.

     Warna memakai ramp ordinal satu hue (biru terang→gelap), bukan trio
     kategorikal: tahap berurutan, bukan identitas. Ramp ini lolos uji
     `validate_palette.js --ordinal` pada permukaan gelap #020617. */
  const STAGES = [
    { id: '1', label: 'Klaim masuk', color: '#9ec5f4', ink: '#020617' },
    { id: '2', label: 'Tier-1 Aturan', color: '#6da7ec', ink: '#020617' },
    { id: '3', label: 'Tier-2 XGBoost', color: '#3987e5', ink: '#ffffff' },
    { id: '4', label: 'Tier-3 GCN', color: '#256abf', ink: '#ffffff' },
    { id: '5', label: 'Antrean verifikator', color: '#184f95', ink: '#ffffff' }
  ];

  const STEP_Y = 96;

  /* Node disejajarkan pada sumbu x yang sama. Lebar node berbeda-beda
     ("Antrean verifikator" lebih lebar dari "Tier-3 GCN"), jadi posisi x
     adalah sudut kiri-atas: tanpa penyamaan ini tepi mengayun diagonal.
     Lebar maksimum node adalah 138px (label terpanjang + padding). */
  const NODE_W = 190;
  const CANVAS_W = 580;
  const X = Math.round((CANVAS_W - NODE_W) / 2);

  let nodes: Node[] = STAGES.map((stage, i) => ({
    id: stage.id,
    type: 'custom',
    position: { x: X, y: 40 + i * STEP_Y },
    data: { label: stage.label, color: stage.color, ink: stage.ink, width: NODE_W }
  }));

  let edges: Edge[] = STAGES.slice(0, -1).map((stage, i) => ({
    id: `e${stage.id}-${STAGES[i + 1].id}`,
    source: stage.id,
    target: STAGES[i + 1].id,
    animated: true,
    style: 'stroke: #64748b'
  }));

  const nodeTypes = { custom: CustomNode };

  /* Diagram statis: interaksi pan/zoom tetap, tapi node tidak bisa diseret
     dan edge tidak bisa dibuat — alur ini bukan editor. */
  const onconnect = (params: unknown) => {
    console.log('Edge connected:', params);
  };
</script>

<div class="w-full h-[600px] bg-slate-950 rounded-3xl overflow-hidden border border-white/10 relative">
  <SvelteFlow
    {nodes}
    {edges}
    {nodeTypes}
    {onconnect}
    fitView
    fitViewOptions={{ padding: 0.2, minZoom: 0.75, maxZoom: 1 }}
    nodesDraggable={false}
    nodesConnectable={false}
    elementsSelectable={false}
    colorMode="dark"
  >
    <Background patternColor="#334155" />
    <Controls showLock={false} />
    <!-- Minimap setinggi 190px: kotak default 200x150 memotong node
         terakhir pada rantai vertikal. -->
    <MiniMap
      zoomable
      pannable
      width={160}
      height={190}
      bgColor="#0b1220"
      nodeColor="#6da7ec"
      nodeStrokeColor="#020617"
      nodeBorderRadius={2}
      maskColor="rgba(57, 135, 229, 0.12)"
      maskStrokeColor="#3987e5"
    />
  </SvelteFlow>
</div>
