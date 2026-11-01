<script lang="ts">
  import { dashboard } from "$lib/stores/dashboard.svelte";
  import {
    SvelteFlow,
    Background,
    BackgroundVariant,
    type Node,
    type Edge,
    type NodeTypes,
    Position
  } from "@xyflow/svelte";
  import "@xyflow/svelte/dist/style.css";
  import Icon from "./Icon.svelte";
  import FlowCustomNode from "./FlowCustomNode.svelte";
  import FlowActionToolbar from "./FlowActionToolbar.svelte";

  const claim = $derived(dashboard.selectedClaim);

  const nodeTypes: NodeTypes = {
    custom: FlowCustomNode,
  };

  const isVerified = $derived(!!claim?.verifiedStatus);
  const statusBadge = $derived(isVerified ? "VERIFIED" : "ACTIVE");

  const nodes = $derived<Node[]>([
    {
      id: "node-ingest",
      type: "custom",
      position: { x: 30, y: 160 },
      data: {
        step: "Tahap 1",
        title: "SATUSEHAT & V-Claim",
        subLabel: `ID: ${claim?.id || "KLM001"} · ${claim?.serviceType === "rawat inap" ? "Rawat Inap" : "Rawat Jalan"}`,
        detail: `Biaya: Rp ${claim?.costRp.toLocaleString("id-ID") || "0"}`,
        channelIcon: "Database",
        badgeStatus: statusBadge,
        accentColor: "#0d9488",
        borderColor: "#0d9488",
        hasTarget: false,
        sourcePosition: Position.Right
      },
      style: "width: 195px;"
    },
    {
      id: "node-preprocess",
      type: "custom",
      position: { x: 265, y: 160 },
      data: {
        step: "Tahap 2",
        title: "Pre-Filter & UU PDP",
        subLabel: `Anonimitas ${claim?.patient || "PST-***"}`,
        detail: `LOS: ${claim?.losDays || 0} hari · Prosedur ${claim?.procedureIcd9 || "-"}`,
        channelIcon: "ShieldCheck",
        badgeStatus: "VERIFIED",
        accentColor: "#0d9488",
        borderColor: "#0d9488",
        targetPosition: Position.Left,
        sourcePosition: Position.Right
      },
      style: "width: 195px;"
    },
    {
      id: "node-split",
      type: "custom",
      position: { x: 500, y: 160 },
      data: {
        step: "Tahap 3",
        title: "Splitter 3 Saluran",
        subLabel: "Dekomposisi Tri-Kanal MHGSL",
        detail: "Topologi · Fitur Atribut · Semantik ICD",
        channelIcon: "GitBranch",
        badgeStatus: "ACTIVE",
        accentColor: "#6366f1",
        borderColor: "#6366f1",
        targetPosition: Position.Left,
        sourcePosition: Position.Right
      },
      style: "width: 200px;"
    },
    {
      id: "node-topo",
      type: "custom",
      position: { x: 745, y: 40 },
      data: {
        step: "Kanal A⁽ᵗᵒᵖ⁾",
        title: "Topologi (Graf Rujukan)",
        subLabel: `Bobot Relatif: ${(claim?.channelContribution.topology ?? 0.33).toFixed(2)}`,
        detail: claim?.channelContribution.topology && claim.channelContribution.topology < 0
          ? "⚠️ Bobot Negatif (Indikasi Kamuflase)"
          : "Jalur Graf Rujukan Terverifikasi",
        channel: "topology",
        channelIcon: "Layers",
        badgeStatus: claim?.channelContribution.topology && claim.channelContribution.topology < 0 ? "ALERT" : "ACTIVE",
        accentColor: "#e11d48",
        borderColor: "#e11d48",
        targetPosition: Position.Left,
        sourcePosition: Position.Right
      },
      style: "width: 215px;"
    },
    {
      id: "node-feat",
      type: "custom",
      position: { x: 745, y: 160 },
      data: {
        step: "Kanal A⁽ᶠᵉᵃᵗ⁾",
        title: "Fitur Klinis (Kosinus)",
        subLabel: `Bobot Relatif: ${(claim?.channelContribution.feature ?? 0.33).toFixed(2)}`,
        detail: `Kemiripan Atribut θ: ${(claim?.fraudScore ?? 0.5) >= 0.7 ? "≥ 0.85 (Anomali)" : "< 0.70 (Normal)"}`,
        channel: "feature",
        channelIcon: "BarChart3",
        badgeStatus: (claim?.fraudScore ?? 0) >= 0.7 ? "ALERT" : "ACTIVE",
        accentColor: "#d97706",
        borderColor: "#d97706",
        targetPosition: Position.Left,
        sourcePosition: Position.Right
      },
      style: "width: 215px;"
    },
    {
      id: "node-sem",
      type: "custom",
      position: { x: 745, y: 280 },
      data: {
        step: "Kanal A⁽ˢᵉᵐ⁾",
        title: "Semantik (Metapath ICD)",
        subLabel: `Bobot Relatif: ${(claim?.channelContribution.semantic ?? 0.34).toFixed(2)}`,
        detail: `BioBERT · ${claim?.diagnosisIcd10 || "ICD-10"}`,
        channel: "semantic",
        channelIcon: "Sparkles",
        badgeStatus: "ACTIVE",
        accentColor: "#0d9488",
        borderColor: "#0d9488",
        targetPosition: Position.Left,
        sourcePosition: Position.Right
      },
      style: "width: 215px;"
    },
    {
      id: "node-shared",
      type: "custom",
      position: { x: 1000, y: 160 },
      data: {
        step: "Tahap 4",
        title: "Shared-Param GCN",
        subLabel: "Ekstraksi Invarian W_shared",
        detail: "Mereduksi Overfitting Tri-Kanal",
        channelIcon: "Activity",
        badgeStatus: "ACTIVE",
        accentColor: "#8b5cf6",
        borderColor: "#8b5cf6",
        targetPosition: Position.Left,
        sourcePosition: Position.Right
      },
      style: "width: 200px;"
    },
    {
      id: "node-fusion",
      type: "custom",
      position: { x: 1240, y: 160 },
      data: {
        step: "Tahap 5",
        title: "Attention Late Fusion",
        subLabel: "Fusi Adaptif Tri-Kanal",
        detail: "Integrasi Teks Aduan & Audit Multi-Sinyal",
        channelIcon: "GitBranch",
        badgeStatus: "ACTIVE",
        accentColor: "#0ea5e9",
        borderColor: "#0ea5e9",
        targetPosition: Position.Left,
        sourcePosition: Position.Right
      },
      style: "width: 200px;"
    },
    {
      id: "node-shap",
      type: "custom",
      position: { x: 1480, y: 160 },
      data: {
        step: "Tahap 6",
        title: "Prediksi & XAI SHAP",
        subLabel: `Skor Fraud: ${claim ? (claim.fraudScore * 100).toFixed(0) : 0}% (${claim?.risk.toUpperCase() || "LOW"})`,
        detail: `Sinyal: ${claim?.shapSignal || "Atribut Klaim"}`,
        channelIcon: "ShieldAlert",
        badgeStatus: (claim?.fraudScore ?? 0) >= 0.75 ? "ALERT" : "ACTIVE",
        accentColor: (claim?.fraudScore ?? 0) >= 0.75 ? "#e11d48" : "#d97706",
        borderColor: (claim?.fraudScore ?? 0) >= 0.75 ? "#e11d48" : "#d97706",
        targetPosition: Position.Left,
        sourcePosition: Position.Right
      },
      style: "width: 215px;"
    },
    {
      id: "node-hitl",
      type: "custom",
      position: { x: 1735, y: 160 },
      data: {
        step: "Tahap 7",
        title: "Gerbang Verifikator HITL",
        subLabel: `Status: ${claim?.verifiedStatus || "MENUNGGU TINJAUAN"}`,
        detail: claim?.verifiedStatus ? "Keputusan Verifikator Terkunci" : "Prerogatif Verifikator Medis",
        channelIcon: "CheckCircle2",
        badgeStatus: isVerified ? "VERIFIED" : "ACTIVE",
        accentColor: isVerified ? "#0d9488" : "#d97706",
        borderColor: isVerified ? "#0d9488" : "#d97706",
        hasSource: false,
        targetPosition: Position.Left
      },
      style: "width: 220px;"
    },
  ]);

  const edges = $derived<Edge[]>([
    {
      id: "e1",
      source: "node-ingest",
      target: "node-preprocess",
      animated: true,
      style: "stroke: #0d9488; stroke-width: 2px;"
    },
    {
      id: "e2",
      source: "node-preprocess",
      target: "node-split",
      animated: true,
      style: "stroke: #0d9488; stroke-width: 2px;"
    },
    // Merah untuk Topologi
    {
      id: "e-top",
      source: "node-split",
      target: "node-topo",
      animated: true,
      style: "stroke: #e11d48; stroke-width: 2.5px; filter: drop-shadow(0 0 3px rgba(225, 29, 72, 0.4));"
    },
    // Amber untuk Fitur
    {
      id: "e-feat",
      source: "node-split",
      target: "node-feat",
      animated: true,
      style: "stroke: #d97706; stroke-width: 2.5px; filter: drop-shadow(0 0 3px rgba(217, 119, 6, 0.4));"
    },
    // Teal untuk Semantik
    {
      id: "e-sem",
      source: "node-split",
      target: "node-sem",
      animated: true,
      style: "stroke: #0d9488; stroke-width: 2.5px; filter: drop-shadow(0 0 3px rgba(13, 148, 136, 0.4));"
    },
    // Penggabungan kembali ke W_shared
    {
      id: "e-shared-1",
      source: "node-topo",
      target: "node-shared",
      animated: true,
      style: "stroke: #e11d48; stroke-width: 2.5px; stroke-dasharray: 5,5;"
    },
    {
      id: "e-shared-2",
      source: "node-feat",
      target: "node-shared",
      animated: true,
      style: "stroke: #d97706; stroke-width: 2.5px; stroke-dasharray: 5,5;"
    },
    {
      id: "e-shared-3",
      source: "node-sem",
      target: "node-shared",
      animated: true,
      style: "stroke: #0d9488; stroke-width: 2.5px; stroke-dasharray: 5,5;"
    },
    {
      id: "e-fusion",
      source: "node-shared",
      target: "node-fusion",
      animated: true,
      style: "stroke: #8b5cf6; stroke-width: 2px;"
    },
    {
      id: "e-shap",
      source: "node-fusion",
      target: "node-shap",
      animated: true,
      style: "stroke: #0ea5e9; stroke-width: 2px;"
    },
    {
      id: "e-hitl",
      source: "node-shap",
      target: "node-hitl",
      animated: true,
      style: "stroke: #0d9488; stroke-width: 2px;"
    },
  ]);
</script>

<div class="h-full flex flex-col bg-background text-foreground overflow-hidden">
  <!-- Pipeline Header Bar -->
  <div class="p-4 border-b border-border bg-card flex flex-wrap items-center justify-between gap-3 shrink-0">
    <div>
      <div class="flex items-center gap-2">
        <Icon name="GitBranch" size={16} class="text-primary" />
        <h3 class="font-bold text-sm">Visualisasi Alur Pipeline Realtime (Svelte Flow)</h3>
      </div>
      <p class="text-xs text-muted-foreground mt-0.5">
        Diagram alir reaktif merefleksikan proses screening MHGSL pada berkas aktif: <strong class="text-primary font-mono">{claim?.id}</strong>
      </p>
    </div>

    <!-- Kanal Color Legend & Status -->
    <div class="flex flex-wrap items-center gap-3 text-xs">
      <!-- Legend Tri-Kanal -->
      <div class="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-lg border border-border bg-muted/20 text-[11px] font-medium">
        <span class="text-muted-foreground text-[10px] uppercase font-mono tracking-wider mr-1">Kanal:</span>
        <span class="inline-flex items-center gap-1 text-rose-500 font-semibold">
          <span class="w-2 h-2 rounded-full bg-rose-500"></span>
          Topologi
        </span>
        <span class="text-border">·</span>
        <span class="inline-flex items-center gap-1 text-amber-500 font-semibold">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span>
          Fitur
        </span>
        <span class="text-border">·</span>
        <span class="inline-flex items-center gap-1 text-teal-500 font-semibold">
          <span class="w-2 h-2 rounded-full bg-teal-500"></span>
          Semantik
        </span>
      </div>

      <span class="inline-flex items-center gap-1.5 rounded-lg border border-border bg-muted/30 px-2.5 py-1 text-muted-foreground font-mono">
        <span class="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
        Streaming WebSocket Active
      </span>
    </div>
  </div>

  <!-- Svelte Flow Canvas -->
  <div class="flex-1 w-full h-[550px] bg-background relative">
    <SvelteFlow
      {nodes}
      {edges}
      {nodeTypes}
      fitView
      minZoom={0.2}
      maxZoom={2}
    >
      <Background variant={BackgroundVariant.Dots} gap={20} size={1} />
      <FlowActionToolbar />
    </SvelteFlow>
  </div>
</div>
