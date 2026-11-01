<script lang="ts">
  import { dashboard } from "$lib/stores/dashboard.svelte";
  import type { GraphitiNode, GraphitiEdge, RiskLevel } from "$lib/types";
  import Icon from "./Icon.svelte";

  const claim = $derived(dashboard.selectedClaim);

  // Entities in graph
  const defaultNodes: GraphitiNode[] = [
    { id: "P01", label: "P01 (Agus R)", type: "patient", risk: "fraud", detail: "Pasien peserta PBPU Jakarta · Gastritis tapi ditagih PCI" },
    { id: "P02", label: "P02 (Bunga L)", type: "patient", risk: "fraud", detail: "Pasien peserta PBPU Jakarta · LOS identik 2 hari" },
    { id: "P03", label: "P03 (Candra W)", type: "patient", risk: "fraud", detail: "Pasien peserta PBPU Jakarta · Pola tagihan kloning" },
    { id: "D01", label: "dr. Adnan Prakoso, Sp.BTKV", type: "doctor", risk: "fraud", detail: "DPJP RS_A · Konsentrasi tagihan upcoding 00.66" },
    { id: "D02", label: "dr. Barli Soemarno, Sp.B", type: "doctor", risk: "fraud", detail: "DPJP RS_A · Rekanan kolusi rujukan tertutup SYND-01" },
    { id: "RS_A", label: "RS Aegis Medika A", type: "hospital", risk: "fraud", detail: "FKRTL Swasta Kelas B · Pusat kluster penagihan sindikat" },
    { id: "DX_K29", label: "ICD-10: K29.7", type: "diagnosis", risk: "low", detail: "Gastritis Akut Ringan Tanpa Perdarahan" },
    { id: "PROC_PCI", label: "ICD-9: 00.66", type: "procedure", risk: "fraud", detail: "PCI Kateterisasi Jantung + Stent Koroner (Rp 52,3 Jt)" },
    { id: "RS_B", label: "RS Mitra Sehat B", type: "hospital", risk: "low", detail: "Faskes pembanding kontrol normal" },
    { id: "D03", label: "dr. Fitri H, Sp.A", type: "doctor", risk: "low", detail: "Praktik dokter reguler kontrol non-sindikat" },
  ];

  // Edges connecting entities
  const defaultEdges: GraphitiEdge[] = [
    { source: "P01", target: "D01", label: "Konsultasi / Rujukan", channel: "topology" },
    { source: "P02", target: "D01", label: "Konsultasi / Rujukan", channel: "topology" },
    { source: "P03", target: "D02", label: "Konsultasi / Rujukan", channel: "topology" },
    { source: "D01", target: "RS_A", label: "Penugasan DPJP", channel: "topology" },
    { source: "D02", target: "RS_A", label: "Penugasan DPJP", channel: "topology" },
    { source: "P01", target: "DX_K29", label: "Hasil Diagnosis", channel: "semantic" },
    { source: "P02", target: "DX_K29", label: "Hasil Diagnosis", channel: "semantic" },
    { source: "D01", target: "PROC_PCI", label: "Klaim Tindakan", channel: "semantic" },
    { source: "D02", target: "PROC_PCI", label: "Klaim Tindakan", channel: "semantic" },
    { source: "P01", target: "P02", label: "Cosine Sim θ = 0.94", channel: "feature" },
    { source: "P02", target: "P03", label: "Cosine Sim θ = 0.89", channel: "feature" },
    { source: "D01", target: "D02", label: "Kolusi Kolaboratif", channel: "feature" },
    { source: "D03", target: "RS_B", label: "Praktik Normal", channel: "topology" },
  ];

  // Positions mapped for SVG canvas
  const nodePositions: Record<string, { x: number; y: number }> = {
    P01: { x: 120, y: 100 },
    P02: { x: 120, y: 220 },
    P03: { x: 120, y: 340 },
    D01: { x: 300, y: 140 },
    D02: { x: 300, y: 280 },
    RS_A: { x: 480, y: 200 },
    DX_K29: { x: 280, y: 400 },
    PROC_PCI: { x: 620, y: 200 },
    RS_B: { x: 620, y: 380 },
    D03: { x: 480, y: 380 },
  };

  // Node Type Filter Definition
  type NodeTypeFilter = "all" | "patient" | "doctor" | "hospital" | "medical";
  let activeFilter = $state<NodeTypeFilter>("all");

  const filterOptions: { id: NodeTypeFilter; label: string; icon: string; count: number }[] = [
    { id: "all", label: "Semua Simpul", icon: "Layers", count: defaultNodes.length },
    { id: "patient", label: "Pasien", icon: "User", count: defaultNodes.filter(n => n.type === "patient").length },
    { id: "doctor", label: "Dokter", icon: "Stethoscope", count: defaultNodes.filter(n => n.type === "doctor").length },
    { id: "hospital", label: "Faskes", icon: "Hospital", count: defaultNodes.filter(n => n.type === "hospital").length },
    { id: "medical", label: "Dx / Prosedur", icon: "ClipboardList", count: defaultNodes.filter(n => n.type === "diagnosis" || n.type === "procedure").length },
  ];

  function isNodeMatchingFilter(node: GraphitiNode, filter: NodeTypeFilter): boolean {
    if (filter === "all") return true;
    if (filter === "medical") return node.type === "diagnosis" || node.type === "procedure";
    return node.type === filter;
  }

  // Camera & Zoom Focus State
  let isSyndicateFocused = $state(false);
  let zoomScale = $state(1);
  let panOffset = $state({ x: 0, y: 0 });

  function toggleSyndicateFocus() {
    if (!isSyndicateFocused) {
      isSyndicateFocused = true;
      zoomScale = 1.35;
      panOffset = { x: -25, y: -15 };
      // If current selected node is normal control, focus onto key syndicate doctor
      if (selectedNode && selectedNode.risk !== "fraud") {
        const fraudDoctor = defaultNodes.find((n) => n.id === "D01");
        if (fraudDoctor) selectedNode = fraudDoctor;
      }
    } else {
      resetCamera();
    }
  }

  function resetCamera() {
    isSyndicateFocused = false;
    zoomScale = 1;
    panOffset = { x: 0, y: 0 };
  }

  function zoomIn() {
    zoomScale = Math.min(2.2, +(zoomScale + 0.2).toFixed(2));
  }

  function zoomOut() {
    zoomScale = Math.max(0.7, +(zoomScale - 0.2).toFixed(2));
  }

  let selectedNode = $state<GraphitiNode | null>(defaultNodes[3]); // default to D01 (key doctor)
  let selectedEdge = $state<GraphitiEdge | null>(null);

  const isClaimSyndicate = $derived(Boolean(claim?.syndicate));

  // Graph Degree Centrality & Relational Analysis
  const totalEntities = defaultNodes.length;

  const incidentEdges = $derived.by(() => {
    const curr = selectedNode;
    if (!curr) return [];
    return defaultEdges.filter(
      (e) => e.source === curr.id || e.target === curr.id
    );
  });

  const inEdges = $derived.by(() => {
    const curr = selectedNode;
    if (!curr) return [];
    return defaultEdges.filter((e) => e.target === curr.id);
  });

  const outEdges = $derived.by(() => {
    const curr = selectedNode;
    if (!curr) return [];
    return defaultEdges.filter((e) => e.source === curr.id);
  });

  const degree = $derived(incidentEdges.length);
  // Degree Centrality C_D(v) = degree / (N - 1)
  const degreeCentralityScore = $derived(
    totalEntities > 1 ? degree / (totalEntities - 1) : 0
  );

  interface NeighborItem {
    node: GraphitiNode;
    edge: GraphitiEdge;
    direction: "in" | "out" | "bilateral";
  }

  const neighbors = $derived.by<NeighborItem[]>(() => {
    const curr = selectedNode;
    if (!curr) return [];
    return incidentEdges.map((edge) => {
      const isOut = edge.source === curr.id;
      const neighborId = isOut ? edge.target : edge.source;
      const neighborNode = defaultNodes.find((n) => n.id === neighborId)!;
      const direction = edge.channel === "feature" ? "bilateral" : isOut ? "out" : "in";
      return {
        node: neighborNode,
        edge,
        direction,
      };
    });
  });

  const fraudNeighbors = $derived(
    neighbors.filter((item) => item.node?.risk === "fraud")
  );

  const fraudNeighborRatio = $derived(
    degree > 0 ? (fraudNeighbors.length / degree) * 100 : 0
  );

  function getCentralityBadge(centrality: number): { label: string; class: string } {
    if (centrality >= 0.4) {
      return { label: "Hub Sentral (Tinggi)", class: "bg-rose-500/15 text-rose-800 dark:text-rose-300 border-rose-500/30" };
    }
    if (centrality >= 0.2) {
      return { label: "Intermediat (Sedang)", class: "bg-amber-500/15 text-amber-800 dark:text-amber-300 border-amber-500/30" };
    }
    return { label: "Perifer (Rendah)", class: "bg-muted text-muted-foreground border-border" };
  }

  function getForensicInsight(node: GraphitiNode, deg: number, cent: number, fraudRatio: number): string {
    if (node.id === "D01") {
      return "Hub DPJP Sentral Sindikat: Memiliki derajat keterhubungan tertinggi (Degree 5, C_D: 55.6%) dengan 80% tetangga berisiko Fraud. Mengarahkan rujukan pasien PBPU Agus R & Bunga L ke RS Aegis Medika A serta memicu penagihan PCI ganda melalui kolusi rujukan tertutup.";
    }
    if (node.id === "D02") {
      return "DPJP Rekanan Kolaborator: Berada pada relasi kolusi horizontal bilateral (↔) dengan dr. Adnan (D01), meloloskan penagihan klaim PCI pada pasien P03 dengan pola klaim kloningan.";
    }
    if (node.id === "RS_A") {
      return "Faskes Episentrum Penampung: Menjadi muara penugasan seluruh DPJP sindikat. 100% tetangga terhubung berstatus sindikat tanpa mekanisme verifikasi silang pada klaim rujukan tertutup.";
    }
    if (node.id === "PROC_PCI") {
      return "Objek Upcoding Kateterisasi Jantung: Prosedur berbiaya Rp 52,3 Jt yang diklaim berulang oleh jejaring DPJP sindikat pada pasien berdiagnosis gastritis ringan tanpa riwayat kardiologis.";
    }
    if (node.id === "DX_K29") {
      return "Diagnosis Kedok (Camouflage): Gastritis akut ringan yang dipakai sebagai pintu masuk rawat inap sebelum dilakukan eskalasi ke tindakan kateterisasi PCI berbiaya tinggi.";
    }
    if (node.id === "P01" || node.id === "P02" || node.id === "P03") {
      return `Klaster Pasien Duplikasi: Memiliki kemiripan fitur teks & pola rawat sangat tinggi (Cosine Similarity 0.89 - 0.94) dengan LOS identik 2 hari di RS Aegis Medika A.`;
    }
    if (node.risk === "fraud") {
      return `Simpul Sindikat Aktif: Terkoneksi ${fraudRatio.toFixed(0)}% dengan entitas anomali dalam subgraf kolusi rujukan tertutup.`;
    }
    return `Simpul Kontrol Normal: Menampilkan pola relasi medis wajar (${deg} relasi, C_D: ${(cent * 100).toFixed(1)}%) di luar klaster sindikat rujukan tertutup.`;
  }
</script>

<div class="h-full flex flex-col bg-card text-foreground overflow-hidden">
  <!-- Header Bar -->
  <div class="p-4 border-b border-border bg-card flex flex-wrap items-center justify-between gap-3">
    <div>
      <div class="flex items-center gap-2">
        <Icon name="Activity" size={16} class="text-primary" />
        <h3 class="font-bold text-sm">Graphiti Bi-Temporal Knowledge Graph</h3>
      </div>
      <p class="text-xs text-muted-foreground mt-0.5">
        Graf neuron entitas faktual bi-temporal memetakan interaksi relasional dokter, pasien, dan faskes rujukan.
      </p>
    </div>

    <!-- Action Bar: Syndicate Focus Toggle & Syndicate Alert -->
    <div class="flex items-center gap-2 flex-wrap">
      <button
        type="button"
        onclick={toggleSyndicateFocus}
        class="min-h-[32px] px-3.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 border transition-all duration-200 cursor-pointer {isSyndicateFocused
          ? 'bg-rose-500/20 border-rose-500/50 text-rose-800 dark:text-rose-200 shadow-sm ring-1 ring-rose-500/40'
          : 'bg-muted/60 hover:bg-muted border-border text-foreground hover:border-foreground/20'}"
        title="Fokuskan kamera dan perbesar subgraf sindikat kolusi"
      >
        <Icon name={isSyndicateFocused ? "ShieldAlert" : "Sparkles"} size={14} class={isSyndicateFocused ? "text-rose-600 dark:text-rose-400" : "text-amber-500"} />
        <span>{isSyndicateFocused ? "Subgraf Kolusi Terfokus" : "Sorot Sindikat Kolusi"}</span>
        {#if isSyndicateFocused}
          <span class="ml-1 px-1.5 py-0.2 rounded text-[10px] bg-rose-500 text-white font-mono">1.35x</span>
        {/if}
      </button>

      {#if isClaimSyndicate || isSyndicateFocused}
        <div class="inline-flex items-center gap-1.5 rounded-full border border-rose-500/40 bg-rose-500/15 px-3 py-1 text-xs font-bold text-rose-800 dark:text-rose-300 animate-pulse">
          <Icon name="ShieldAlert" size={14} />
          <span>Sindikat {claim?.syndicate || "SYND-01"} Aktif</span>
        </div>
      {:else}
        <div class="inline-flex items-center gap-1.5 rounded-full border border-border bg-muted/40 px-3 py-1 text-xs text-muted-foreground">
          <span>Struktur Graf Normal</span>
        </div>
      {/if}
    </div>
  </div>

  <!-- Sub-Header: Node Type Filter Toolbar -->
  <div class="px-4 py-2 border-b border-border/70 bg-muted/20 flex flex-wrap items-center justify-between gap-2 text-xs">
    <div class="flex items-center gap-1.5 overflow-x-auto py-0.5">
      <span class="text-[11px] font-semibold text-muted-foreground mr-1 flex items-center gap-1">
        <Icon name="Filter" size={13} class="text-muted-foreground" />
        Filter Simpul:
      </span>
      {#each filterOptions as opt}
        {@const isActive = activeFilter === opt.id}
        <button
          type="button"
          onclick={() => (activeFilter = opt.id)}
          class="min-h-[32px] px-2.5 py-1 rounded-md text-xs font-medium flex items-center gap-1.5 border transition-colors duration-150 cursor-pointer {isActive
            ? 'bg-primary text-primary-foreground border-primary shadow-xs'
            : 'bg-card hover:bg-muted/80 text-muted-foreground hover:text-foreground border-border'}"
        >
          <Icon name={opt.icon} size={13} />
          <span>{opt.label}</span>
          <span class="px-1.5 py-0.2 rounded text-[10px] tabular-nums font-mono {isActive ? 'bg-primary-foreground/20 text-primary-foreground' : 'bg-muted text-muted-foreground'}">
            {opt.count}
          </span>
        </button>
      {/each}
    </div>

    <!-- Active Filter Counter & Quick Reset -->
    <div class="flex items-center gap-2 text-[11px] text-muted-foreground font-mono">
      {#if activeFilter !== "all"}
        <button
          type="button"
          onclick={() => (activeFilter = "all")}
          class="min-h-[32px] px-2 py-0.5 text-xs text-primary hover:underline flex items-center gap-1 cursor-pointer"
        >
          <Icon name="X" size={12} />
          <span>Reset Filter</span>
        </button>
      {/if}
      <span class="tabular-nums">Simpul: {defaultNodes.length}</span>
      <span>•</span>
      <span class="tabular-nums">Relasi: {defaultEdges.length}</span>
    </div>
  </div>

  <!-- Main Canvas & Inspector Area -->
  <div class="flex-1 grid grid-cols-1 lg:grid-cols-12 overflow-hidden">
    <!-- SVG Graph Canvas (8 cols) -->
    <div class="lg:col-span-8 relative bg-background border-r border-border p-4 flex items-center justify-center overflow-hidden">
      <!-- Floating Camera Controls (Zoom In, Zoom Out, Reset) -->
      <div class="absolute top-3 right-3 z-10 flex items-center gap-1 rounded-lg bg-card/90 backdrop-blur-md p-1 border border-border shadow-xs">
        <button
          type="button"
          onclick={zoomIn}
          class="w-8 h-8 rounded flex items-center justify-center text-foreground hover:bg-muted transition-colors cursor-pointer"
          title="Perbesar Kamera (+)"
          aria-label="Perbesar Kamera"
        >
          <span class="text-base font-bold leading-none">+</span>
        </button>
        <button
          type="button"
          onclick={zoomOut}
          class="w-8 h-8 rounded flex items-center justify-center text-foreground hover:bg-muted transition-colors cursor-pointer"
          title="Perkecil Kamera (-)"
          aria-label="Perkecil Kamera"
        >
          <span class="text-base font-bold leading-none">−</span>
        </button>
        <button
          type="button"
          onclick={resetCamera}
          class="w-8 h-8 rounded flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted transition-colors cursor-pointer"
          title="Reset Kamera ke Posisi Semula"
          aria-label="Reset Kamera"
        >
          <Icon name="RotateCcw" size={13} />
        </button>
        <span class="px-1.5 text-[10px] font-mono tabular-nums text-muted-foreground select-none">
          {Math.round(zoomScale * 100)}%
        </span>
      </div>

      <!-- Focused Syndicate Banner Notification -->
      {#if isSyndicateFocused}
        <div class="absolute top-3 left-3 z-10 flex items-center gap-2 rounded-lg bg-rose-500/10 border border-rose-500/30 px-3 py-1.5 text-xs text-rose-800 dark:text-rose-200 backdrop-blur-md shadow-xs animate-in fade-in duration-200">
          <Icon name="ShieldAlert" size={14} class="text-rose-600 dark:text-rose-400 shrink-0" />
          <span class="font-medium">Subgraf Sindikat Kolusi Terfokus (8 Simpul, 11 Sisi)</span>
          <button
            type="button"
            onclick={resetCamera}
            class="min-h-[28px] ml-1 px-2 py-0.5 rounded bg-rose-500/20 hover:bg-rose-500/30 text-rose-800 dark:text-rose-200 text-[11px] font-semibold cursor-pointer transition-colors"
          >
            Reset Kamera
          </button>
        </div>
      {/if}

      <svg viewBox="0 0 740 480" class="w-full h-full select-none">
        <!-- Background Grid -->
        <pattern id="graphiti-grid" width="30" height="30" patternUnits="userSpaceOnUse">
          <path d="M 30 0 L 0 0 0 30" fill="none" stroke="currentColor" stroke-width="0.5" class="text-border/30" />
        </pattern>
        <rect width="740" height="480" fill="url(#graphiti-grid)" />

        <!-- Camera Zoom and Pan Wrapper -->
        <g
          transform="translate({panOffset.x}, {panOffset.y}) scale({zoomScale})"
          style="transform-origin: 370px 240px; transition: transform 300ms cubic-bezier(0.2, 0, 0, 1);"
        >
          <!-- Syndicate Halo Glow when active or focused -->
          {#if isClaimSyndicate || isSyndicateFocused}
            <circle
              cx="330"
              cy="210"
              r="170"
              fill="oklch(0.62 0.22 20 / 0.07)"
              stroke="oklch(0.62 0.22 20 / 0.35)"
              stroke-width="1.5"
              stroke-dasharray="5 5"
              class="animate-pulse"
            />
            <text x="330" y="32" text-anchor="middle" fill="oklch(0.62 0.22 20)" font-size="11" font-weight="bold" font-family="monospace">
              [Klaster Sindikat Kolusi {claim?.syndicate || "SYND-01"} - Rujukan Tertutup]
            </text>
          {/if}

          <!-- Edges -->
          {#each defaultEdges as edge}
            {@const p1 = nodePositions[edge.source]}
            {@const p2 = nodePositions[edge.target]}
            {@const srcNode = defaultNodes.find((n) => n.id === edge.source)}
            {@const tgtNode = defaultNodes.find((n) => n.id === edge.target)}
            {#if p1 && p2 && srcNode && tgtNode}
              {@const isSelected = selectedEdge?.source === edge.source && selectedEdge?.target === edge.target}
              {@const srcMatches = isNodeMatchingFilter(srcNode, activeFilter)}
              {@const tgtMatches = isNodeMatchingFilter(tgtNode, activeFilter)}
              {@const isEdgeSyndicate = srcNode.risk === "fraud" && tgtNode.risk === "fraud"}
              
              <!-- Edge dimming based on filter and syndicate focus -->
              {@const isDimmedByFilter = activeFilter !== "all" && !srcMatches && !tgtMatches}
              {@const isDimmedBySyndicate = isSyndicateFocused && !isEdgeSyndicate}
              {@const edgeOpacity = isSelected ? 1 : isDimmedByFilter || isDimmedBySyndicate ? 0.12 : 0.7}

              <line
                x1={p1.x}
                y1={p1.y}
                x2={p2.x}
                y2={p2.y}
                stroke={edge.channel === "topology" ? "oklch(0.62 0.22 20)" : edge.channel === "feature" ? "oklch(0.7 0.16 70)" : "oklch(0.55 0.14 165)"}
                stroke-width={isSelected ? 3.5 : (isSyndicateFocused && isEdgeSyndicate) ? 3 : 1.5}
                stroke-opacity={edgeOpacity}
                stroke-dasharray={edge.channel === "feature" ? "4 4" : undefined}
                class="cursor-pointer transition-all duration-200 hover:stroke-width-3"
                role="button"
                tabindex="0"
                aria-label={`Sisi ${edge.source} ke ${edge.target}: ${edge.label}`}
                onclick={() => { selectedEdge = edge; }}
                onkeydown={(e) => { if (e.key === 'Enter') selectedEdge = edge; }}
              />
            {/if}
          {/each}

          <!-- Nodes -->
          {#each defaultNodes as node}
            {@const pos = nodePositions[node.id]}
            {#if pos}
              {@const isSelected = selectedNode?.id === node.id}
              {@const isFraud = node.risk === "fraud"}
              {@const matchesFilter = isNodeMatchingFilter(node, activeFilter)}
              {@const isDimmedBySyndicate = isSyndicateFocused && !isFraud}
              {@const isNodeDimmed = !matchesFilter || isDimmedBySyndicate}

              <g
                transform={`translate(${pos.x}, ${pos.y})`}
                role="button"
                tabindex="0"
                aria-label={`Simpul ${node.label}, tipe ${node.type}, risiko ${node.risk}`}
                onclick={() => { selectedNode = node; selectedEdge = null; }}
                onkeydown={(e) => { if (e.key === 'Enter') { selectedNode = node; selectedEdge = null; } }}
                class="cursor-pointer transition-opacity duration-200 {isNodeDimmed ? 'opacity-20 pointer-events-none' : 'opacity-100'}"
              >
                <!-- Fraud Syndicate Warning Halo -->
                {#if isFraud && (isClaimSyndicate || isSyndicateFocused)}
                  <circle
                    r="25"
                    fill="none"
                    stroke="oklch(0.62 0.22 20)"
                    stroke-width="2"
                    stroke-dasharray="3 3"
                    class="animate-pulse"
                  />
                {/if}

                <!-- Active Selection Ring -->
                {#if isSelected}
                  <circle
                    r="23"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2.5"
                    class="text-primary"
                  />
                {/if}

                <!-- Node Body Circle -->
                <circle
                  r={node.type === "hospital" ? 19 : node.type === "doctor" ? 16 : 14}
                  fill={node.type === "hospital" ? "oklch(0.7 0.16 70)" : node.type === "doctor" ? "oklch(0.62 0.13 200)" : node.type === "procedure" ? "oklch(0.62 0.22 20)" : node.type === "diagnosis" ? "oklch(0.5 0.13 280)" : "oklch(0.55 0.14 165)"}
                  class="shadow-md transition-transform duration-150 hover:scale-115"
                />

                <!-- Node Text Label -->
                <text
                  y={node.type === "hospital" ? 31 : 26}
                  text-anchor="middle"
                  fill="currentColor"
                  font-size="10"
                  font-weight="bold"
                  class="text-foreground pointer-events-none drop-shadow-xs"
                >
                  {node.label.split(" (")[0]}
                </text>
              </g>
            {/if}
          {/each}
        </g>
      </svg>

      <!-- Channel Legend -->
      <div class="absolute bottom-3 left-3 flex flex-wrap gap-2 rounded-xl bg-card/90 backdrop-blur-md p-2 border border-border text-[10px] shadow-xs">
        <div class="flex items-center gap-1.5">
          <span class="h-2.5 w-2.5 rounded-full bg-rose-500"></span>
          <span>Topologi (Rujukan)</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="h-2.5 w-2.5 rounded-full bg-amber-500"></span>
          <span>Fitur (Cosine / Kolusi)</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="h-2.5 w-2.5 rounded-full bg-teal-500"></span>
          <span>Semantik (Diagnosis/PCI)</span>
        </div>
      </div>
    </div>

    <!-- Node & Edge Inspector Sidebar (4 cols) -->
    <div class="lg:col-span-4 p-4 space-y-4 overflow-y-auto scrollbar-thin bg-card border-t lg:border-t-0 border-border">
      {#if selectedNode}
        {@const centBadge = getCentralityBadge(degreeCentralityScore)}
        <div class="p-4 rounded-2xl border border-border bg-muted/20 space-y-4">
          <!-- Node Header & Badges -->
          <div class="flex items-start justify-between gap-2 pb-3 border-b border-border/60">
            <div>
              <div class="flex items-center gap-1.5">
                <span class="text-[10px] uppercase font-bold text-muted-foreground font-mono">
                  Simpul: {selectedNode.id}
                </span>
                <span class="px-1.5 py-0.2 rounded text-[10px] font-semibold bg-muted text-foreground border border-border">
                  {selectedNode.type}
                </span>
              </div>
              <h4 class="font-bold text-sm text-foreground mt-1 leading-snug">{selectedNode.label}</h4>
            </div>
            <span class="rounded px-2 py-0.5 font-bold text-[10px] shrink-0 border {selectedNode.risk === 'fraud' ? 'bg-rose-500/15 text-rose-800 dark:text-rose-300 border-rose-500/30' : 'bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 border-emerald-500/30'}">
              {selectedNode.risk === 'fraud' ? 'RISK HIGH' : 'NORMAL'}
            </span>
          </div>

          <!-- Entity Characteristics & Detail -->
          <div class="text-xs text-muted-foreground leading-relaxed">
            <strong class="text-foreground block mb-0.5">Karakteristik Entitas:</strong>
            <p>{selectedNode.detail}</p>
          </div>

          <!-- DEGREE CENTRALITY & METRICS PANEL -->
          <div class="p-3 rounded-xl border border-border/80 bg-background/80 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold text-foreground flex items-center gap-1.5">
                <Icon name="Activity" size={13} class="text-primary" />
                Derajat Keterhubungan
              </span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-semibold border {centBadge.class}">
                {centBadge.label}
              </span>
            </div>

            <!-- Centrality Stat Grid -->
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="p-2 rounded-lg bg-muted/40 border border-border/50">
                <span class="text-[10px] text-muted-foreground block">Degree Centrality (C_D)</span>
                <span class="font-bold font-mono tabular-nums text-sm text-foreground">
                  {(degreeCentralityScore * 100).toFixed(1)}%
                </span>
                <span class="text-[9px] text-muted-foreground block mt-0.5">
                  ({degree} dari {totalEntities - 1} entitas)
                </span>
              </div>

              <div class="p-2 rounded-lg bg-muted/40 border border-border/50">
                <span class="text-[10px] text-muted-foreground block">Koneksi Sindikat</span>
                <span class="font-bold font-mono tabular-nums text-sm {fraudNeighborRatio >= 50 ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'}">
                  {fraudNeighborRatio.toFixed(0)}%
                </span>
                <span class="text-[9px] text-muted-foreground block mt-0.5">
                  ({fraudNeighbors.length} dari {degree} tetangga)
                </span>
              </div>

              <div class="p-2 rounded-lg bg-muted/40 border border-border/50">
                <span class="text-[10px] text-muted-foreground block">Relasi Masuk (In)</span>
                <span class="font-bold font-mono tabular-nums text-foreground">{inEdges.length}</span>
              </div>

              <div class="p-2 rounded-lg bg-muted/40 border border-border/50">
                <span class="text-[10px] text-muted-foreground block">Relasi Keluar (Out)</span>
                <span class="font-bold font-mono tabular-nums text-foreground">{outEdges.length}</span>
              </div>
            </div>
          </div>

          <!-- FORENSIC INVESTIGATION INSIGHT -->
          <div class="p-3 rounded-xl border border-primary/20 bg-primary/5 text-xs space-y-1.5">
            <div class="font-bold text-foreground flex items-center gap-1.5 text-[11px]">
              <Icon name="ShieldAlert" size={13} class="text-primary" />
              <span>Analisis Forensik Grafiti:</span>
            </div>
            <p class="text-muted-foreground leading-relaxed text-[11px]">
              {getForensicInsight(selectedNode, degree, degreeCentralityScore, fraudNeighborRatio)}
            </p>
          </div>

          <!-- NEIGHBORS / RELATIONS BREAKDOWN -->
          <div class="space-y-2">
            <div class="flex items-center justify-between text-xs font-semibold text-foreground">
              <span>Tetangga Terhubung ({neighbors.length})</span>
              <span class="text-[10px] text-muted-foreground font-normal">Klik untuk inspeksi</span>
            </div>

            <div class="space-y-1.5 max-h-48 overflow-y-auto scrollbar-thin pr-0.5">
              {#if neighbors.length === 0}
                <p class="text-xs text-muted-foreground italic">Tidak ada relasi terhubung.</p>
              {:else}
                {#each neighbors as item}
                  <button
                    type="button"
                    onclick={() => {
                      selectedNode = item.node;
                      selectedEdge = item.edge;
                    }}
                    class="w-full min-h-[36px] text-left p-2 rounded-xl border border-border/70 bg-card hover:bg-muted/80 transition-colors duration-150 flex items-center justify-between gap-2 cursor-pointer group"
                  >
                    <div class="flex items-center gap-2 min-w-0">
                      <span class="text-[10px] font-mono px-1.5 py-0.5 rounded font-semibold shrink-0 {item.direction === 'in' ? 'bg-blue-500/10 text-blue-800 dark:text-blue-300' : item.direction === 'out' ? 'bg-amber-500/10 text-amber-800 dark:text-amber-300' : 'bg-purple-500/10 text-purple-800 dark:text-purple-300'}">
                        {item.direction === "in" ? "← Masuk" : item.direction === "out" ? "→ Keluar" : "↔ Kolusi"}
                      </span>
                      <div class="truncate">
                        <div class="font-bold text-xs text-foreground group-hover:text-primary transition-colors truncate">
                          {item.node.label}
                        </div>
                        <div class="text-[10px] text-muted-foreground truncate">
                          {item.edge.label} · <span class="capitalize">{item.edge.channel}</span>
                        </div>
                      </div>
                    </div>

                    <span class="rounded px-1.5 py-0.2 text-[9px] font-bold shrink-0 {item.node.risk === 'fraud' ? 'bg-rose-500/15 text-rose-800 dark:text-rose-300' : 'bg-emerald-500/15 text-emerald-800 dark:text-emerald-300'}">
                      {item.node.risk === 'fraud' ? 'RISK' : 'NORMAL'}
                    </span>
                  </button>
                {/each}
              {/if}
            </div>
          </div>

          <!-- Bi-temporal timestamps -->
          <div class="pt-2 border-t border-border/60 space-y-1 font-mono text-[10px] text-muted-foreground">
            <div>Tv (Valid at): <span class="text-foreground">2026-02-16 08:30:00 WIB</span></div>
            <div>Tk (Recorded at): <span class="text-foreground">2026-02-16 08:35:12 WIB</span></div>
          </div>
        </div>
      {/if}

      <!-- Selected Edge Inspector -->
      {#if selectedEdge}
        <div class="p-4 rounded-2xl border border-border bg-muted/20 space-y-2">
          <div class="text-[10px] uppercase font-bold text-muted-foreground font-mono">
            Inspeksi Relasi Sisi (Edge)
          </div>
          <div class="font-bold text-xs text-foreground">
            {selectedEdge.source} ➔ {selectedEdge.target}
          </div>
          <div class="text-xs text-primary font-semibold">
            {selectedEdge.label}
          </div>
          <div class="text-[11px] text-muted-foreground capitalize">
            Saluran: <strong>{selectedEdge.channel}</strong>
          </div>
        </div>
      {/if}

      <!-- Graph Guidance Note -->
      <div class="p-4 rounded-2xl border border-border/80 bg-background text-xs text-muted-foreground space-y-2">
        <div class="font-bold text-foreground flex items-center gap-1.5">
          <Icon name="Info" size={14} class="text-primary" />
          <span>Petunjuk Investigasi Visual:</span>
        </div>
        <p class="leading-relaxed">
          Gunakan filter tipe untuk mengisolasi kategori entitas, atau klik <strong>"Sorot Sindikat Kolusi"</strong> untuk memperbesar kamera langsung ke jejaring rujukan tertutup. Klik sembarang simpul atau tetangga untuk melihat metrik derajat sentralitas (<span class="font-mono">C_D</span>).
        </p>
      </div>
    </div>
  </div>
</div>
