<script lang="ts">
  import { onMount } from "svelte";
  import { theme } from "$lib/stores/theme.svelte";
  import Icon from "$lib/components/Icon.svelte";

  // State for IT Dashboard Environment and Interactive Filters
  let activeEnv = $state<"DEV" | "STG" | "PROD">("DEV");
  let isRefreshing = $state(false);
  let lastRefreshTime = $state(new Date().toLocaleTimeString("id-ID"));
  let activeTab = $state<"overview" | "satusehat" | "observability" | "cluster">("overview");

  // Interactive SmarTerm Terminology Query Simulation
  let terminologyQuery = $state("kateterisasi jantung");
  let isQueryingTerm = $state(false);
  let terminologyResult = $state<{
    code: string;
    system: string;
    display: string;
    valid: boolean;
    latencyMs: number;
  } | null>({
    code: "36.06",
    system: "ICD-9-CM / KPTL",
    display: "Insertion of non-drug-eluting coronary artery stent(s)",
    valid: true,
    latencyMs: 38
  });

  function handleRefreshMetrics() {
    isRefreshing = true;
    setTimeout(() => {
      lastRefreshTime = new Date().toLocaleTimeString("id-ID");
      isRefreshing = false;
    }, 700);
  }

  function handleQueryTerminology() {
    isQueryingTerm = true;
    setTimeout(() => {
      const q = terminologyQuery.toLowerCase();
      if (q.includes("stent") || q.includes("kateter") || q.includes("pci")) {
        terminologyResult = {
          code: "36.06",
          system: "ICD-9-CM / KPTL",
          display: "Insertion of non-drug-eluting coronary artery stent(s)",
          valid: true,
          latencyMs: 34
        };
      } else if (q.includes("jantung") || q.includes("infark") || q.includes("i21")) {
        terminologyResult = {
          code: "I21.0",
          system: "ICD-10 (WHO / Kemenkes)",
          display: "Acute transmural myocardial infarction of anterior wall",
          valid: true,
          latencyMs: 29
        };
      } else {
        terminologyResult = {
          code: "Z03.8",
          system: "ICD-10 / SatuSehat",
          display: `Observasi klinis terpetakan untuk '${terminologyQuery}'`,
          valid: true,
          latencyMs: 41
        };
      }
      isQueryingTerm = false;
    }, 350);
  }

  // FHIR R4 Resource Synchronization Counters
  const fhirResources = [
    { name: "Patient", count: 1240, status: "Synced", rate: "100%", icon: "User" },
    { name: "Encounter", count: 890, status: "Active", rate: "100%", icon: "Activity" },
    { name: "Condition (ICD-10)", count: 2410, status: "Mapped", rate: "99.8%", icon: "ClipboardList" },
    { name: "Procedure (ICD-9)", count: 1815, status: "Mapped", rate: "99.4%", icon: "Layers" },
    { name: "Observation", count: 3120, status: "Streaming", rate: "100%", icon: "Activity" },
    { name: "MedicationRequest", count: 1450, status: "Checked", rate: "99.1%", icon: "Syringe" },
    { name: "Claim (FHIR Bundle)", count: 300, status: "Audited", rate: "100%", icon: "ShieldCheck" }
  ];

  // Observability RED Metrics
  const redMetrics = [
    {
      label: "Traffic Rate (RPS)",
      value: "142.5 req/s",
      sub: "Peak 380 req/s • Kong Gateway",
      trend: "+12% vs last hr",
      status: "healthy"
    },
    {
      label: "Error Budget Burn",
      value: "0.012%",
      sub: "SLO Limit: < 0.05% per 30d",
      trend: "4.1x headroom safe",
      status: "healthy"
    },
    {
      label: "Latency p99 (Scoring)",
      value: "415 ms",
      sub: "SLO Mandate: < 500 ms",
      trend: "-42ms vs baseline",
      status: "healthy"
    },
    {
      label: "Availability (Uptime)",
      value: "99.98%",
      sub: "Target Kemenkes: 99.95%",
      trend: "0 downtime incidents",
      status: "healthy"
    }
  ];

  // Data Tier & Infrastructure Cluster Nodes
  const clusterNodes = [
    {
      name: "PostgreSQL Aurora DB",
      tier: "Relational Master + 2 Replicas",
      metric: "Replica Lag: 8 ms",
      health: "99.99%",
      connections: "42 / 200 pool",
      status: "Healthy"
    },
    {
      name: "Graphiti Knowledge Graph (FalkorDB)",
      tier: "L2 Bi-Temporal Graph Engine",
      metric: "55.2K Nodes • 184.3K Edges",
      health: "18 ms avg query",
      connections: "Multi-Hop Traversal Active",
      status: "Healthy"
    },
    {
      name: "Qdrant Vector DB",
      tier: "HNSW Dense Semantic Store",
      metric: "300 Clinical Dossier Vectors",
      health: "Cosine Recall 0.998",
      connections: "Index Memory: 128 MB",
      status: "Healthy"
    },
    {
      name: "Redis & NATS JetStream",
      tier: "Asynchronous Message Broker",
      metric: "0 Dead-Letter Queue (DLQ)",
      health: "Sync Latency: 1.8 ms",
      connections: "100% Message Delivery",
      status: "Healthy"
    }
  ];

  onMount(() => {
    theme.init();
  });
</script>

<svelte:head>
  <title>Aegis-JKN · IT Operations &amp; SATUSEHAT Gateway Hub</title>
  <meta
    name="description"
    content="Dashboard Operasional IT Aegis-JKN: Observabilitas Prometheus/OpenTelemetry, Status Klaster AI MHGSL, dan Interoperabilitas SATUSEHAT FHIR R4."
  />
</svelte:head>

<div class="min-h-screen w-full bg-background text-foreground flex flex-col font-sans select-text selection:bg-[#588157]/25 selection:text-foreground">
  <!-- TOP NAVIGATION BAR (Borderless, Glassmorphic) -->
  <header class="sticky top-0 z-50 w-full bg-background/85 backdrop-blur-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between gap-4">
      <!-- Brand & Hub Identity -->
      <div class="flex items-center gap-3.5">
        <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-[#3a5a40] via-[#588157] to-[#a3b18a] text-white shadow-lg shadow-[#3a5a40]/20">
          <Icon name="Server" size={22} />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-base sm:text-lg font-black tracking-tight text-foreground">Aegis-JKN</span>
            <span class="inline-flex items-center rounded-full bg-[#3a5a40]/15 px-2.5 py-0.5 text-[10px] font-bold text-[#3a5a40] dark:text-[#a3b18a] font-mono">
              IT OPERATIONS &amp; GATEWAY
            </span>
          </div>
          <p class="text-xs text-muted-foreground font-medium hidden sm:block">
            Pusat Observabilitas Sistem &amp; SATUSEHAT FHIR R4
          </p>
        </div>
      </div>

      <!-- Environment Selector & Global Status Pill -->
      <div class="flex items-center gap-2 sm:gap-3">
        <!-- Live System Status Pill -->
        <div class="hidden md:inline-flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-800 dark:text-emerald-300 font-mono shadow-2xs">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span>SEMUA LAYANAN NORMAL (99.98% SLO)</span>
        </div>

        <!-- Environment Switcher (DEV / STG / PROD) -->
        <div class="inline-flex items-center rounded-2xl bg-muted/60 p-1 text-xs font-semibold shadow-2xs">
          <button
            type="button"
            data-testid="it-env-dev"
            onclick={() => (activeEnv = "DEV")}
            class="px-2.5 py-1 rounded-xl transition-all {activeEnv === 'DEV' ? 'bg-[#3a5a40] text-white shadow-xs' : 'text-muted-foreground hover:text-foreground'}"
          >
            DEV
          </button>
          <button
            type="button"
            data-testid="it-env-stg"
            onclick={() => (activeEnv = "STG")}
            class="px-2.5 py-1 rounded-xl transition-all {activeEnv === 'STG' ? 'bg-[#3a5a40] text-white shadow-xs' : 'text-muted-foreground hover:text-foreground'}"
          >
            STG
          </button>
          <button
            type="button"
            data-testid="it-env-prod"
            onclick={() => (activeEnv = "PROD")}
            class="px-2.5 py-1 rounded-xl transition-all {activeEnv === 'PROD' ? 'bg-[#3a5a40] text-white shadow-xs' : 'text-muted-foreground hover:text-foreground'}"
          >
            PROD
          </button>
        </div>

        <!-- Theme Toggle -->
        <button
          type="button"
          data-testid="it-theme-toggle"
          onclick={() => theme.toggle()}
          class="flex h-10 w-10 items-center justify-center rounded-2xl bg-muted/60 text-muted-foreground hover:text-foreground hover:bg-muted transition-all active:scale-95 shadow-2xs"
          aria-label="Ganti Tema Tampilan"
        >
          {#if theme.current === "dark"}
            <Icon name="Sun" size={18} class="text-[#a3b18a]" />
          {:else}
            <Icon name="Moon" size={18} class="text-[#3a5a40]" />
          {/if}
        </button>

        <!-- Navigation Buttons -->
        <a
          href="/"
          class="hidden sm:inline-flex items-center gap-1.5 rounded-2xl bg-muted/60 hover:bg-muted px-3.5 py-2 text-xs font-semibold text-foreground transition-all"
        >
          <span>← Beranda</span>
        </a>

        <a
          href="/app"
          data-testid="it-nav-workstation"
          class="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-[#3a5a40] to-[#588157] hover:from-[#344e41] hover:to-[#3a5a40] px-4 py-2 text-xs sm:text-sm font-bold text-white shadow-md shadow-[#3a5a40]/25 transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
        >
          <Icon name="Activity" size={15} />
          <span>Meja Kerja</span>
        </a>
      </div>
    </div>
  </header>

  <!-- MAIN IT DASHBOARD WORKSPACE -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- SUB-NAV & REFRESH ACTIONS BAR (Borderless, Soft Cards) -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-card rounded-3xl p-5 shadow-xs">
      <div>
        <h1 class="text-xl sm:text-2xl font-black tracking-tight text-foreground">
          Pusat Kendali Sistem &amp; Infrastruktur Terpadu
        </h1>
        <p class="text-xs text-muted-foreground mt-0.5">
          Monitoring telemetri real-time, pipeline FHIR R4 Kemenkes, dan integritas kriptografis klaster Aegis-JKN.
        </p>
      </div>

      <div class="flex items-center gap-3">
        <span class="text-xs text-muted-foreground font-mono">
          Sinkron: <strong class="text-foreground">{lastRefreshTime}</strong>
        </span>
        <button
          type="button"
          data-testid="it-refresh-btn"
          onclick={handleRefreshMetrics}
          disabled={isRefreshing}
          class="inline-flex items-center gap-2 rounded-2xl bg-[#588157]/15 hover:bg-[#588157]/25 text-[#3a5a40] dark:text-[#a3b18a] px-3.5 py-2 text-xs font-bold transition-all disabled:opacity-50 cursor-pointer shadow-2xs"
        >
          <Icon name="RotateCcw" size={14} class={isRefreshing ? "animate-spin" : ""} />
          <span>{isRefreshing ? "Menyegarkan..." : "Segarkan Metrik"}</span>
        </button>
      </div>
    </div>

    <!-- 1. OBSERVABILITY PILLAR: RED METRICS & SLO PERFORMANCE (Section 11.5 Blueprint) -->
    <section class="space-y-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-sm font-black uppercase tracking-wider text-[#588157] font-mono">
            01 · Tiga Pilar Observabilitas (RED Metrics &amp; SLO Target)
          </span>
        </div>
        <span class="text-xs text-muted-foreground font-mono">Prometheus v2.54 • OpenTelemetry Spans</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {#each redMetrics as m}
          <div class="rounded-3xl bg-card p-6 shadow-xs space-y-2 hover:shadow-md transition-shadow">
            <span class="text-xs font-semibold text-muted-foreground">{m.label}</span>
            <div class="text-2xl sm:text-3xl font-black text-foreground font-mono tracking-tight">
              {m.value}
            </div>
            <div class="flex items-center justify-between text-[11px] pt-1">
              <span class="text-muted-foreground">{m.sub}</span>
              <span class="font-bold text-[#588157] font-mono">{m.trend}</span>
            </div>
          </div>
        {/each}
      </div>
    </section>

    <!-- 2. SATUSEHAT INTEGRATION HUB & FHIR R4 PIPELINE (ivanwilliammd/satusehat-integration Engine) -->
    <section class="space-y-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-sm font-black uppercase tracking-wider text-[#588157] font-mono">
            02 · SATUSEHAT Platform Gateway &amp; HL7 FHIR R4 Engine
          </span>
        </div>
        <span class="text-xs text-muted-foreground font-mono">Permenkes No. 24/2022 • DTO Kemenkes RI</span>
      </div>

      <!-- Top Integration Status Banner (Borderless Soft Card) -->
      <div class="rounded-3xl bg-card p-6 shadow-xs space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- OAuth2 Gateway Card -->
          <div class="rounded-2xl bg-muted/30 p-5 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-foreground">OAuth2 Kemenkes DTO</span>
              <span class="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800 dark:text-emerald-300 font-mono">
                TERHUBUNG (200 OK)
              </span>
            </div>
            <div class="space-y-1 font-mono text-xs">
              <div class="text-muted-foreground text-[11px]">Endpoint:</div>
              <div class="text-foreground font-semibold truncate text-[11px]">
                {activeEnv === 'DEV' ? 'api-satusehat-dev.dto.kemkes.go.id' : activeEnv === 'STG' ? 'api-satusehat-stg.dto.kemkes.go.id' : 'api-satusehat.kemkes.go.id'}
              </div>
            </div>
            <div class="flex items-center justify-between text-[11px] pt-1">
              <span class="text-muted-foreground">Token Expire:</span>
              <span class="font-bold text-[#588157] font-mono">48m 12s (Auto-Refresh)</span>
            </div>
          </div>

          <!-- SmarTerm Terminology Client Status -->
          <div class="rounded-2xl bg-muted/30 p-5 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-foreground">SmarTerm Terminology</span>
              <span class="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800 dark:text-emerald-300 font-mono">
                ACTIVE · 38ms
              </span>
            </div>
            <p class="text-xs text-muted-foreground leading-relaxed">
              Kamus terminologi kesehatan nasional terpadu (ICD-10, ICD-9-CM, SNOMED CT, LOINC, dan KFA Obat Kemenkes).
            </p>
            <div class="text-[11px] font-mono text-foreground font-semibold">
              Host: terminology.ivanmd.id
            </div>
          </div>

          <!-- 558 Rule Validation Checker -->
          <div class="rounded-2xl bg-muted/30 p-5 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-foreground">Validasi Aturan FHIR</span>
              <span class="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800 dark:text-emerald-300 font-mono">
                0 PENOLAKAN
              </span>
            </div>
            <p class="text-xs text-muted-foreground leading-relaxed">
              Memetakan 558 aturan validasi SATUSEHAT secara otomatis sebelum pengiriman berkas klaim ke Kemenkes.
            </p>
            <div class="text-[11px] text-muted-foreground">
              Total bundle divalidasi: <strong class="text-foreground font-mono">300/300 lolos</strong>
            </div>
          </div>
        </div>

        <!-- Interactive SmarTerm Query Tester (Direct Sandbox Experience) -->
        <div class="rounded-2xl bg-muted/20 p-5 space-y-3">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="text-xs font-bold text-foreground flex items-center gap-1.5">
              <Icon name="Search" size={14} class="text-[#588157]" />
              <span>Uji Coba Lookup Terminologi Medis Real-time (SmarTerm Client)</span>
            </span>
            <span class="text-[10px] font-mono text-muted-foreground">KFA v2 • ICD-10 • ICD-9-CM</span>
          </div>

          <div class="flex flex-col sm:flex-row items-center gap-2.5">
            <input
              type="text"
              data-testid="it-terminology-input"
              bind:value={terminologyQuery}
              placeholder="Ketik istilah medis (contoh: kateterisasi jantung, infark miokard, dll)..."
              class="w-full flex-1 rounded-xl bg-card px-3.5 py-2.5 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-[#588157]/40 shadow-2xs"
            />
            <button
              type="button"
              data-testid="it-terminology-btn"
              onclick={handleQueryTerminology}
              disabled={isQueryingTerm}
              class="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 rounded-xl bg-[#3a5a40] hover:bg-[#344e41] text-white px-4 py-2.5 text-xs font-bold transition-all disabled:opacity-50 cursor-pointer shadow-xs"
            >
              <span>{isQueryingTerm ? "Mencari..." : "Resolve Kode FHIR"}</span>
            </button>
          </div>

          {#if terminologyResult}
            <div class="p-3 rounded-xl bg-card text-xs flex flex-wrap items-center justify-between gap-3 shadow-2xs">
              <div class="flex items-center gap-2">
                <span class="font-mono font-bold text-lg text-[#588157]">{terminologyResult.code}</span>
                <div>
                  <span class="font-semibold text-foreground">{terminologyResult.display}</span>
                  <span class="text-[10px] text-muted-foreground block font-mono">Standar: {terminologyResult.system}</span>
                </div>
              </div>
              <div class="flex items-center gap-2 text-[10px] font-mono">
                <span class="rounded bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 font-bold px-2 py-0.5">VALID</span>
                <span class="text-muted-foreground">{terminologyResult.latencyMs} ms</span>
              </div>
            </div>
          {/if}
        </div>

        <!-- FHIR Resource Sync Throughput Matrix -->
        <div class="space-y-3">
          <div class="flex items-center justify-between text-xs font-bold text-foreground">
            <span>Matriks Throughput Resource FHIR R4:</span>
            <span class="text-muted-foreground font-mono text-[11px]">Pipeline Ingesti Otomatis</span>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
            {#each fhirResources as res}
              <div class="rounded-2xl bg-muted/30 p-3.5 text-center space-y-1">
                <div class="text-[10px] font-mono font-bold text-muted-foreground truncate">{res.name}</div>
                <div class="text-lg font-black text-foreground font-mono tabular-nums">{res.count}</div>
                <div class="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-1.5 py-0.2 text-[9px] font-bold text-emerald-800 dark:text-emerald-300 font-mono">
                  <span>✓ {res.rate}</span>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </section>

    <!-- 3. DATA TIER & CLUSTER HEALTH (PostgreSQL, Graphiti L2, Qdrant, Redis/NATS) -->
    <section class="space-y-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-sm font-black uppercase tracking-wider text-[#588157] font-mono">
            03 · Klaster Data Forensik &amp; Topologi Infrastruktur
          </span>
        </div>
        <span class="text-xs text-muted-foreground font-mono">High Availability (K8s Istio Mesh)</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {#each clusterNodes as node}
          <div class="rounded-3xl bg-card p-6 shadow-xs space-y-3 flex flex-col justify-between hover:shadow-md transition-shadow">
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-mono font-bold text-[#588157] uppercase tracking-wide">
                  {node.status}
                </span>
                <span class="h-2 w-2 rounded-full bg-emerald-500"></span>
              </div>
              <h3 class="text-base font-bold text-foreground tracking-tight">
                {node.name}
              </h3>
              <p class="text-[11px] text-muted-foreground">
                {node.tier}
              </p>
            </div>

            <div class="pt-2 border-t border-slate-200/60 dark:border-[#a3b18a]/15 text-xs space-y-1 font-mono">
              <div class="text-foreground font-semibold">{node.metric}</div>
              <div class="text-[10px] text-muted-foreground">{node.connections}</div>
            </div>
          </div>
        {/each}
      </div>
    </section>

    <!-- 4. SECURITY, RBAC & CRYPTOGRAPHIC MERKLE AUDIT TRAIL -->
    <section class="rounded-3xl bg-gradient-to-br from-[#203127] via-[#273b30] to-[#17241d] p-6 sm:p-8 text-white shadow-xl space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-[#dad7cd]/20">
        <div>
          <div class="flex items-center gap-2">
            <Icon name="ShieldCheck" size={20} class="text-[#a3b18a]" />
            <h2 class="text-lg font-bold text-[#dad7cd]">
              Keamanan Jaringan &amp; Audit Kriptografis (UU PDP No. 27/2022)
            </h2>
          </div>
          <p class="text-xs text-[#a3b18a] mt-0.5">
            Setiap perubahan data klaim dan keputusan verifikator disegel dengan rantai hash SHA-256 yang immutable.
          </p>
        </div>

        <div class="flex items-center gap-2">
          <span class="rounded-full bg-[#588157]/30 px-3 py-1 text-xs font-mono font-bold text-[#dad7cd]">
            mTLS v1.3 STRICT
          </span>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-mono">
        <div class="p-4 rounded-2xl bg-white/5 space-y-1.5">
          <span class="text-[#a3b18a] text-[11px] font-sans font-semibold">Integritas Rantai Hash:</span>
          <div class="text-sm font-bold text-emerald-400">100% TERVERIFIKASI VALID</div>
          <p class="text-[10px] text-[#dad7cd]/70 leading-relaxed font-sans">
            Seluruh 300 blok audit lolos verifikasi verifier SHA-256 tanpa anomali pemutusan rantai.
          </p>
        </div>

        <div class="p-4 rounded-2xl bg-white/5 space-y-1.5">
          <span class="text-[#a3b18a] text-[11px] font-sans font-semibold">Tanda Tangan Digital:</span>
          <div class="text-sm font-bold text-white truncate">Ed25519-BPJS-2026-KEY</div>
          <p class="text-[10px] text-[#dad7cd]/70 leading-relaxed font-sans">
            Sertifikat digital terdaftar pada root trust authority BPJS Kesehatan dan Kemenkes.
          </p>
        </div>

        <div class="p-4 rounded-2xl bg-white/5 space-y-1.5">
          <span class="text-[#a3b18a] text-[11px] font-sans font-semibold">Kepatuhan UU PDP No. 27/2022:</span>
          <div class="text-sm font-bold text-emerald-400">AUDIT TRAIL IMMUTABLE</div>
          <p class="text-[10px] text-[#dad7cd]/70 leading-relaxed font-sans">
            Rekaman akses data EMR terenkripsi end-to-end dengan retensi log append-only.
          </p>
        </div>
      </div>
    </section>
  </main>

  <!-- FOOTER -->
  <footer class="bg-card py-8 text-xs text-muted-foreground mt-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-2">
        <span class="font-bold text-foreground">Aegis-JKN IT Hub</span>
        <span>•</span>
        <span>Observabilitas &amp; SATUSEHAT FHIR R4 Engine</span>
      </div>

      <div class="flex items-center gap-6 font-semibold">
        <a href="/" class="hover:text-foreground">Beranda</a>
        <a href="/app" class="hover:text-foreground">Meja Kerja</a>
        <a href="/it" class="text-[#588157] font-bold">Dashboard IT</a>
      </div>
    </div>
  </footer>
</div>
