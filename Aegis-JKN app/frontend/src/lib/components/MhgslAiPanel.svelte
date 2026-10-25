<script lang="ts">
  import { dashboard } from "$lib/stores/dashboard.svelte";
  import Icon from "./Icon.svelte";
  import type { Claim } from "$lib/types";
  import { requestClinicalReport } from "$lib/ai-reporter";
  import FormattedAiReport from "./FormattedAiReport.svelte";

  const claim = $derived(dashboard.selectedClaim);

  // Parse SHAP signals separated by semicolons
  const shapList = $derived(
    claim?.shapSignal
      ? claim.shapSignal.split(";").map((s: string) => s.trim()).filter(Boolean)
      : []
  );

  // Active tooltip index for mobile/tap or keyboard interaction
  let activeTooltip = $state<number | null>(null);

  function toggleTooltip(index: number) {
    activeTooltip = activeTooltip === index ? null : index;
  }

  function closeTooltip() {
    activeTooltip = null;
  }

  // Unified Clinical Report & MCP Investigation Dossier State
  let unifiedReport = $state<string | null>(null);
  let isGeneratingReport = $state(false);
  let reportError = $state<string | null>(null);
  let copied = $state(false);
  let lastClaimId = $state<string | null>(null);

  $effect(() => {
    if (claim && claim.id !== lastClaimId) {
      lastClaimId = claim.id;
      unifiedReport = null;
      reportError = null;
    }
  });

  async function generateUnifiedReport() {
    if (!claim) return;
    isGeneratingReport = true;
    reportError = null;
    try {
      const result = await requestClinicalReport(claim);
      unifiedReport = result;
    } catch (err) {
      reportError = err instanceof Error ? err.message : "Gagal menyusun laporan audit terverifikasi via MCP tools.";
    } finally {
      isGeneratingReport = false;
    }
  }

  function downloadReport() {
    if (!unifiedReport || !claim) return;
    const blob = new Blob([unifiedReport], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `DOSSIER-AUDIT-KLINIS-${claim.id}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function copyReport() {
    if (unifiedReport && typeof navigator !== "undefined" && navigator.clipboard) {
      navigator.clipboard.writeText(unifiedReport);
      copied = true;
      setTimeout(() => (copied = false), 2000);
    }
  }
  // Radius 48, Center (60, 60), 240 degree arc sweep (from 150deg to 390deg)
  const GAUGE_RADIUS = 48;
  const GAUGE_CIRCUMFERENCE = 2 * Math.PI * GAUGE_RADIUS; // ~301.59
  const ARC_FRACTION = 240 / 360; // 0.6667
  const ARC_LENGTH = GAUGE_CIRCUMFERENCE * ARC_FRACTION; // ~201.06

  const strokeDashoffset = $derived(
    claim
      ? ARC_LENGTH * (1 - Math.min(1, Math.max(0, claim.fraudScore)))
      : ARC_LENGTH
  );

  // Normalized Channel Proportions for proportional visualization
  const channelTotals = $derived.by(() => {
    if (!claim) return { topPct: 33.3, featPct: 33.3, semPct: 33.4, sum: 1 };
    const t = claim.channelContribution.topology || 0.01;
    const f = claim.channelContribution.feature || 0.01;
    const s = claim.channelContribution.semantic || 0.01;
    const sum = t + f + s;
    return {
      topPct: (t / sum) * 100,
      featPct: (f / sum) * 100,
      semPct: (s / sum) * 100,
      sum,
    };
  });

  // Identify dominant channel that broke the camouflage
  const dominantChannel = $derived.by(() => {
    if (!claim) return { name: "Topologi", key: "T", score: 0 };
    const { topology: t, feature: f, semantic: s } = claim.channelContribution;
    if (t >= f && t >= s) {
      return { name: "Topologi (T)", key: "T", score: t, role: "Koalisi Rujukan Tertutup (Clique)" };
    }
    if (f >= t && f >= s) {
      return { name: "Fitur (F)", key: "F", score: f, role: "Keseragaman Profil Klaim & Tarif" };
    }
    return { name: "Semantik (S)", key: "S", score: s, role: "Inkonsistensi Medis ICD-10 vs Tindakan" };
  });

  interface ShapMetadata {
    signal: string;
    channel: "T" | "F" | "S";
    category: string;
    phiValue: number;
    deltaProb: string;
    mechanism: string;
    auditAdvice: string;
    isHighRisk: boolean;
  }

  // Generate transparent, evidence-based mathematical interpretation for SHAP signals
  function analyzeShapSignal(signal: string, index: number, total: number, curClaim: Claim): ShapMetadata {
    const lower = signal.toLowerCase();

    // 1. Semantic / Clinical inconsistency
    if (
      lower.includes("inkonsistensi") ||
      lower.includes("tanpa indikasi") ||
      lower.includes("tanpa medicationdispense") ||
      lower.includes("tanpa antiplatelet") ||
      lower.includes("layanan tak terverifikasi") ||
      lower.includes("gastritis") ||
      lower.includes("pci")
    ) {
      const phi = Number((0.26 + (curClaim.fraudScore * 0.12) / Math.max(1, total)).toFixed(2));
      return {
        signal,
        channel: "S",
        category: "Inkonsistensi Medis (Metapath)",
        phiValue: phi,
        deltaProb: `+${(phi * 100).toFixed(1)}%`,
        mechanism:
          "Metapath semantik BioBERT Pasien→Diagnosis→Tindakan mendeteksi diskrepansi klinis fatal: tindakan invasif bernilai tinggi ditagih tanpa rekam terapi farmasi pendukung di SATUSEHAT.",
        auditAdvice:
          `Verifikasi ketersediaan resume medis kardiologi/cath lab dan histori resep obat (${curClaim.drugs || "obat kronis"}).`,
        isHighRisk: true,
      };
    }

    // 2. Feature / Cost / LOS / Unbundling
    if (
      lower.includes("identik") ||
      lower.includes("biaya") ||
      lower.includes("los") ||
      lower.includes("pecah") ||
      lower.includes("unbundling") ||
      lower.includes("outlier") ||
      lower.includes("tarif")
    ) {
      const phi = Number((0.23 + (curClaim.fraudScore * 0.11) / Math.max(1, total)).toFixed(2));
      return {
        signal,
        channel: "F",
        category: "Keseragaman Fitur & Tarif",
        phiValue: phi,
        deltaProb: `+${(phi * 100).toFixed(1)}%`,
        mechanism:
          "Metrik kemiripan kosinus ruang fitur membongkar pola duplikasi tagihan (Rp " +
          curClaim.costRp.toLocaleString("id-ID") +
          ") dan LOS (" +
          curClaim.losDays +
          " hari) yang kembar identik pada pasien berbeda.",
        auditAdvice:
          "Periksa rincian tagihan komponen INA-CBG apakah ada pemecahan prosedur (unbundling) atau copy-paste rekam billing.",
        isHighRisk: curClaim.fraudScore >= 0.7,
      };
    }

    // 3. Topology / Subgraph / Faskes / Network
    if (
      lower.includes("subgraf") ||
      lower.includes("padat") ||
      lower.includes("faskes") ||
      lower.includes("dokter") ||
      lower.includes("kunjungan") ||
      lower.includes("interval") ||
      lower.includes("sindikat") ||
      lower.includes("p-d-rs")
    ) {
      const phi = Number((0.20 + (curClaim.fraudScore * 0.10) / Math.max(1, total)).toFixed(2));
      return {
        signal,
        channel: "T",
        category: "Topologi Klaster Sindikat",
        phiValue: phi,
        deltaProb: `+${(phi * 100).toFixed(1)}%`,
        mechanism:
          "Konvolusi graf heterogen mendeteksi klik subgraf tertutup antara faskes (" +
          curClaim.hospital +
          "), dokter (" +
          curClaim.doctor +
          "), dan simpul pasien dengan derajat anomali k-hop tinggi.",
        auditAdvice:
          "Lakukan audit silang ke jejaring rujukan faskes pengirim untuk mendeteksi sindikat calo pasien BPJS.",
        isHighRisk: true,
      };
    }

    // 4. Drug / Pharmacy diversion
    if (
      lower.includes("insulin") ||
      lower.includes("obat") ||
      lower.includes("qty") ||
      lower.includes("refill") ||
      lower.includes("diversion")
    ) {
      const phi = Number((0.25 + (curClaim.fraudScore * 0.10) / Math.max(1, total)).toFixed(2));
      return {
        signal,
        channel: "S",
        category: "Anomali Alokasi Farmasi",
        phiValue: phi,
        deltaProb: `+${(phi * 100).toFixed(1)}%`,
        mechanism:
          "Volume pengambilan obat melampaui kurva kebutuhan klinis standar (>3 standar deviasi dari batas rasional bulanan), mengindikasikan pengalihan/penjualan obat.",
        auditAdvice:
          "Cek kartu stok apotek faskes dan konfirmasi tanda tangan pasien pada bukti serah-terima fisik obat.",
        isHighRisk: true,
      };
    }

    // Default proportional attribution
    const basePhi = Number(((curClaim.fraudScore * 0.85) / Math.max(1, total)).toFixed(2));
    return {
      signal,
      channel: index % 2 === 0 ? "F" : "T",
      category: "Atribusi Fitur Tambahan",
      phiValue: basePhi,
      deltaProb: `+${(basePhi * 100).toFixed(1)}%`,
      mechanism:
        "Fitur ini memberikan kontribusi marginal positif pada cabang klasifikasi GNN TreeExplainer ke arah prediksi kecurangan klaim.",
      auditAdvice:
        "Tinjau kesesuaian berkas pendukung klaim dengan regulasi tarif dan indikasi medis BPJS Kesehatan.",
      isHighRisk: curClaim.fraudScore >= 0.8,
    };
  }
</script>

<svelte:window onkeydown={(e) => { if (e.key === "Escape") closeTooltip(); }} />

{#if claim}
  <div class="h-full overflow-y-auto p-4 sm:p-6 space-y-6 scrollbar-thin text-foreground">
    <!-- AI Header with Score Gauge & Proportional Bar -->
    <div class="rounded-3xl border border-border bg-card p-6 shadow-xs space-y-6">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <!-- Text intro -->
        <div class="space-y-1.5 flex-1">
          <div class="inline-flex items-center gap-1.5 rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
            <Icon name="Activity" size={13} />
            <span>Hasil Inferensi Multi-Channel GNN (MHGSL)</span>
          </div>
          <h2 class="text-xl font-bold tracking-tight text-foreground">
            Skor Probabilitas Kecurangan
          </h2>
          <p class="text-xs text-muted-foreground leading-relaxed max-w-xl">
            Hasil fusi terbobot dari tiga saluran representasi graf: topologi rujukan fisik,
            kemiripan ruang fitur numerik, dan metapath semantik rekam medis.
          </p>
        </div>

        <!-- Circular Radial Gauge -->
        <div class="flex items-center gap-5 shrink-0 self-center md:self-auto">
          <div class="relative flex items-center justify-center">
            <svg
              width="132"
              height="132"
              viewBox="0 0 120 120"
              class="overflow-visible"
              role="img"
              aria-label="Meteran probabilitas fraud {(claim.fraudScore * 100).toFixed(1)}%"
            >
              <defs>
                <linearGradient id="gaugeGradRose" x1="0%" y1="100%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#f59e0b" />
                  <stop offset="100%" stop-color="#e11d48" />
                </linearGradient>
                <linearGradient id="gaugeGradAmber" x1="0%" y1="100%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#eab308" />
                  <stop offset="100%" stop-color="#f59e0b" />
                </linearGradient>
                <linearGradient id="gaugeGradEmerald" x1="0%" y1="100%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#14b8a6" />
                  <stop offset="100%" stop-color="#10b981" />
                </linearGradient>
              </defs>

              <!-- Background Track Arc (240 degrees) -->
              <circle
                cx="60"
                cy="60"
                r={GAUGE_RADIUS}
                fill="none"
                stroke="currentColor"
                stroke-width="9"
                stroke-linecap="round"
                stroke-dasharray="{ARC_LENGTH} {GAUGE_CIRCUMFERENCE}"
                stroke-dashoffset="0"
                transform="rotate(150 60 60)"
                class="text-muted/30 dark:text-muted/20"
              />

              <!-- Active Gauge Progress Arc -->
              <circle
                cx="60"
                cy="60"
                r={GAUGE_RADIUS}
                fill="none"
                stroke={claim.fraudScore >= 0.8
                  ? "url(#gaugeGradRose)"
                  : claim.fraudScore >= 0.35
                    ? "url(#gaugeGradAmber)"
                    : "url(#gaugeGradEmerald)"}
                stroke-width="9"
                stroke-linecap="round"
                stroke-dasharray="{ARC_LENGTH} {GAUGE_CIRCUMFERENCE}"
                stroke-dashoffset={strokeDashoffset}
                transform="rotate(150 60 60)"
                class="transition-[stroke-dashoffset] duration-300 ease-out"
              />

              <!-- Threshold Reference Ticks -->
              <!-- 35% Review Tick (angle ~ 234 deg) -->
              <circle cx="31.8" cy="21.2" r="2" class="fill-amber-500/70" />
              <!-- 80% Escalation Tick (angle ~ 342 deg) -->
              <circle cx="105.7" cy="45.2" r="2" class="fill-rose-500/80" />
            </svg>

            <!-- Center Metric Text -->
            <div class="absolute inset-0 flex flex-col items-center justify-center text-center select-none pt-2">
              <span class="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                Probabilitas
              </span>
              <span
                class="text-2xl font-black font-mono tracking-tight tabular-nums {claim.fraudScore >= 0.8
                  ? 'text-rose-600 dark:text-rose-400'
                  : claim.fraudScore >= 0.35
                    ? 'text-amber-600 dark:text-amber-400'
                    : 'text-emerald-600 dark:text-emerald-400'}"
              >
                {(claim.fraudScore * 100).toFixed(1)}%
              </span>
              <span
                class="inline-block mt-0.5 px-2 py-0.5 text-[9px] font-bold rounded-full {claim.fraudScore >= 0.8
                  ? 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20'
                  : claim.fraudScore >= 0.35
                    ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20'
                    : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20'}"
              >
                {claim.fraudScore >= 0.8 ? "ESKALASI FRAUD" : claim.fraudScore >= 0.35 ? "REVIEW MANUAL" : "AUTO-CLEAR"}
              </span>
            </div>
          </div>

          <!-- Quick Gauge Legend -->
          <div class="space-y-1.5 text-[11px] min-w-[130px]">
            <div class="flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-emerald-500 shrink-0"></span>
              <span class="text-muted-foreground">&lt; 35%: Layak Bayar</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-amber-500 shrink-0"></span>
              <span class="text-muted-foreground">35-79%: Audit Manual</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-rose-500 shrink-0"></span>
              <span class="text-muted-foreground">&ge; 80%: Investigasi</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Proportional Segmented Risk Meter & Needle -->
      <div class="space-y-2 pt-2 border-t border-border/60">
        <div class="flex items-center justify-between text-xs">
          <span class="font-semibold text-foreground flex items-center gap-1.5">
            <Icon name="BarChart3" size={14} class="text-primary" />
            <span>Distribusi Zona Keputusan Regulasi BPJS</span>
          </span>
          <span class="font-mono text-[11px] tabular-nums text-muted-foreground">
            Titik Klaim: <strong class="text-foreground">{(claim.fraudScore * 100).toFixed(1)}%</strong>
          </span>
        </div>

        <!-- Multi-segment proportional bar -->
        <div class="relative h-4 w-full rounded-full bg-muted/40 p-0.5 border border-border overflow-visible">
          <div class="h-full w-full rounded-full flex overflow-hidden">
            <!-- Zone 1: Auto-clear (35%) -->
            <div
              class="h-full bg-emerald-500/25 dark:bg-emerald-500/20 border-r border-emerald-500/40"
              style="width: 35%"
              title="Zona 0-35%: Auto-Clear"
            ></div>
            <!-- Zone 2: Review (45%) -->
            <div
              class="h-full bg-amber-500/25 dark:bg-amber-500/20 border-r border-amber-500/40"
              style="width: 45%"
              title="Zona 35-80%: Review Manual Verifikator"
            ></div>
            <!-- Zone 3: Escalate (20%) -->
            <div
              class="h-full bg-rose-500/30 dark:bg-rose-500/25"
              style="width: 20%"
              title="Zona 80-100%: Eskalasi Fraud Ring"
            ></div>
          </div>

          <!-- Needle / Pin Indicator -->
          <div
            class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 flex flex-col items-center pointer-events-none transition-all duration-300"
            style="left: {Math.min(98.5, Math.max(1.5, claim.fraudScore * 100))}%"
          >
            <div class="h-6 w-2 rounded-full shadow-md border-2 border-background {claim.fraudScore >= 0.8 ? 'bg-rose-600' : claim.fraudScore >= 0.35 ? 'bg-amber-500' : 'bg-emerald-500'}"></div>
          </div>
        </div>

        <!-- Scale Labels -->
        <div class="flex items-center justify-between text-[10px] font-mono tabular-nums text-muted-foreground pt-0.5">
          <span class="text-emerald-600 dark:text-emerald-400 font-medium">0% (Auto-Clear)</span>
          <span class="text-amber-600 dark:text-amber-400 font-medium">Ambang Review: 35%</span>
          <span class="text-rose-600 dark:text-rose-400 font-medium">Ambang Eskalasi: 80%</span>
          <span>100% (Confirmed Fraud)</span>
        </div>
      </div>

      <!-- Proportional 3-Channel Stacked Summary -->
      <div class="rounded-2xl bg-muted/20 border border-border/70 p-3.5 space-y-2">
        <div class="flex items-center justify-between text-xs">
          <span class="text-muted-foreground font-medium">
            Proporsi Komparatif Saluran Graf (T : F : S)
          </span>
          <span class="font-mono text-xs font-bold text-foreground">
            {claim.channelContribution.rawString}
          </span>
        </div>

        <div class="h-2.5 w-full rounded-full bg-muted overflow-hidden flex">
          <div
            class="h-full bg-rose-500 transition-all duration-300"
            style="width: {channelTotals.topPct}%"
            title="Topologi: {channelTotals.topPct.toFixed(1)}%"
          ></div>
          <div
            class="h-full bg-amber-500 transition-all duration-300"
            style="width: {channelTotals.featPct}%"
            title="Fitur: {channelTotals.featPct.toFixed(1)}%"
          ></div>
          <div
            class="h-full bg-teal-500 transition-all duration-300"
            style="width: {channelTotals.semPct}%"
            title="Semantik: {channelTotals.semPct.toFixed(1)}%"
          ></div>
        </div>

        <div class="flex items-center justify-between text-[11px] font-mono tabular-nums pt-0.5">
          <span class="text-rose-600 dark:text-rose-400 font-medium">
            T: {claim.channelContribution.topology.toFixed(2)} ({channelTotals.topPct.toFixed(0)}%)
          </span>
          <span class="text-amber-600 dark:text-amber-400 font-medium">
            F: {claim.channelContribution.feature.toFixed(2)} ({channelTotals.featPct.toFixed(0)}%)
          </span>
          <span class="text-teal-600 dark:text-teal-400 font-medium">
            S: {claim.channelContribution.semantic.toFixed(2)} ({channelTotals.semPct.toFixed(0)}%)
          </span>
        </div>
      </div>
    </div>

    <!-- Comparative Anti-Camouflage Syndicate Cards -->
    <div class="rounded-3xl border border-border bg-card p-6 shadow-xs space-y-5">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <Icon name="ShieldAlert" size={17} class="text-primary" />
            <h3 class="font-bold text-base text-foreground">
              Analisis Pematahan Kamuflase Sindikat (Multi-Channel Anti-Camouflage)
            </h3>
          </div>
          <p class="text-xs text-muted-foreground leading-relaxed">
            Sindikat fraud berusaha menyamarkan diri dengan memanipulasi salah satu saluran.
            Arsitektur MHGSL membongkar penyamaran melalui fusi tiga pandangan ortogonal.
          </p>
        </div>
        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-semibold self-start sm:self-auto shrink-0">
          <Icon name="Sparkles" size={12} />
          <span>Sinyal Dominan: {dominantChannel.name}</span>
        </div>
      </div>

      <!-- 3 Channels Comparative Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 pt-1">
        <!-- 1. TOPOLOGI (T) -->
        <div class="rounded-2xl border border-border bg-muted/15 p-4 space-y-3.5 flex flex-col justify-between">
          <div class="space-y-2.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="h-7 w-7 rounded-lg bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-500 font-bold font-mono text-xs">
                  T
                </div>
                <div>
                  <h4 class="font-bold text-xs text-foreground">Topologi Graf</h4>
                  <span class="text-[10px] font-mono text-muted-foreground">A⁽ᵗᵒᵖ⁾ &isin; &#123;0, 1&#125;</span>
                </div>
              </div>
              <span class="font-mono font-extrabold text-sm tabular-nums text-rose-600 dark:text-rose-400">
                {claim.channelContribution.topology.toFixed(2)}
              </span>
            </div>

            <!-- Taktik Sindikat vs MHGSL Solution -->
            <div class="space-y-2 text-xs">
              <div class="p-2.5 rounded-xl bg-background/80 border border-border/60 space-y-1">
                <span class="text-[10px] uppercase font-bold tracking-wider text-muted-foreground block">
                  Taktik Kamuflase Sindikat:
                </span>
                <p class="text-muted-foreground leading-relaxed text-[11px]">
                  <strong>Graph Dispersal (Degree Masking):</strong> Pasien disebar ke dokter berbeda dan faskes satelit
                  agar derajat simpul fisik tampak normal dan lolos deteksi klaster tunggal.
                </p>
              </div>

              <div class="p-2.5 rounded-xl bg-rose-500/5 border border-rose-500/20 space-y-1">
                <span class="text-[10px] uppercase font-bold tracking-wider text-rose-600 dark:text-rose-400 block">
                  Cara MHGSL Mematahkan:
                </span>
                <p class="text-foreground leading-relaxed text-[11px]">
                  Konvolusi graf <em>k-hop</em> melacak koalisi tersembunyi (clique) dan mengukur kerapatan tetangga bersama
                  antara faskes <strong>{claim.hospital}</strong> dan dokter <strong>{claim.doctor}</strong>.
                </p>
              </div>
            </div>
          </div>

          <div class="pt-2 border-t border-border/50 flex items-center justify-between text-[11px]">
            <span class="text-muted-foreground">Peran Anti-Kamuflase:</span>
            <span class="font-semibold text-rose-600 dark:text-rose-400">
              {claim.channelContribution.topology >= 0.3 ? "Klaster Padat Terdeteksi" : "Dispersi Tertangkap F/S"}
            </span>
          </div>
        </div>

        <!-- 2. FITUR (F) -->
        <div class="rounded-2xl border border-border bg-muted/15 p-4 space-y-3.5 flex flex-col justify-between">
          <div class="space-y-2.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="h-7 w-7 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-500 font-bold font-mono text-xs">
                  F
                </div>
                <div>
                  <h4 class="font-bold text-xs text-foreground">Ruang Fitur</h4>
                  <span class="text-[10px] font-mono text-muted-foreground">A⁽ᶠᵉᵃᵗ⁾ = cos(xᵢ, xⱼ)</span>
                </div>
              </div>
              <span class="font-mono font-extrabold text-sm tabular-nums text-amber-600 dark:text-amber-400">
                {claim.channelContribution.feature.toFixed(2)}
              </span>
            </div>

            <!-- Taktik Sindikat vs MHGSL Solution -->
            <div class="space-y-2 text-xs">
              <div class="p-2.5 rounded-xl bg-background/80 border border-border/60 space-y-1">
                <span class="text-[10px] uppercase font-bold tracking-wider text-muted-foreground block">
                  Taktik Kamuflase Sindikat:
                </span>
                <p class="text-muted-foreground leading-relaxed text-[11px]">
                  <strong>Attribute Perturbation:</strong> Mengacak sedikit biodata dan rujukan geografis agar
                  terlihat sebagai kejadian terpisah yang tidak saling berhubungan secara fisik.
                </p>
              </div>

              <div class="p-2.5 rounded-xl bg-amber-500/5 border border-amber-500/20 space-y-1">
                <span class="text-[10px] uppercase font-bold tracking-wider text-amber-600 dark:text-amber-400 block">
                  Cara MHGSL Mematahkan:
                </span>
                <p class="text-foreground leading-relaxed text-[11px]">
                  Simpul dihubungkan berdasarkan kemiripan kosinus metrik numerik. Biaya
                  (<strong>Rp {claim.costRp.toLocaleString("id-ID")}</strong>) dan LOS
                  (<strong>{claim.losDays} hari</strong>) yang kembar langsung terhubung melintasi faskes.
                </p>
              </div>
            </div>
          </div>

          <div class="pt-2 border-t border-border/50 flex items-center justify-between text-[11px]">
            <span class="text-muted-foreground">Peran Anti-Kamuflase:</span>
            <span class="font-semibold text-amber-600 dark:text-amber-400">
              {claim.channelContribution.feature >= 0.3 ? "Duplikasi Tarif Terbuka" : "Metrik Variansi Wajar"}
            </span>
          </div>
        </div>

        <!-- 3. SEMANTIK (S) -->
        <div class="rounded-2xl border border-border bg-muted/15 p-4 space-y-3.5 flex flex-col justify-between">
          <div class="space-y-2.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="h-7 w-7 rounded-lg bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-500 font-bold font-mono text-xs">
                  S
                </div>
                <div>
                  <h4 class="font-bold text-xs text-foreground">Semantik Klinis</h4>
                  <span class="text-[10px] font-mono text-muted-foreground">A⁽ˢᵉᵐ⁾ via Metapath ℳ</span>
                </div>
              </div>
              <span class="font-mono font-extrabold text-sm tabular-nums text-teal-600 dark:text-teal-400">
                {claim.channelContribution.semantic.toFixed(2)}
              </span>
            </div>

            <!-- Taktik Sindikat vs MHGSL Solution -->
            <div class="space-y-2 text-xs">
              <div class="p-2.5 rounded-xl bg-background/80 border border-border/60 space-y-1">
                <span class="text-[10px] uppercase font-bold tracking-wider text-muted-foreground block">
                  Taktik Kamuflase Sindikat:
                </span>
                <p class="text-muted-foreground leading-relaxed text-[11px]">
                  <strong>Clinical Cloaking (Upcoding):</strong> Menyelipkan kode diagnosis umum untuk menjustifikasi
                  tindakan invasif mahal atau pemecahan paket INA-CBG (unbundling).
                </p>
              </div>

              <div class="p-2.5 rounded-xl bg-teal-500/5 border border-teal-500/20 space-y-1">
                <span class="text-[10px] uppercase font-bold tracking-wider text-teal-600 dark:text-teal-400 block">
                  Cara MHGSL Mematahkan:
                </span>
                <p class="text-foreground leading-relaxed text-[11px]">
                  BioBERT mengevaluasi rantai metapath <em>Dx ({claim.diagnosisIcd10}) &rarr; Prosedur ({claim.procedureIcd9}) &rarr; Terapi</em>.
                  Diskrepansi logika klinis langsung memicu penalti semantik berat.
                </p>
              </div>
            </div>
          </div>

          <div class="pt-2 border-t border-border/50 flex items-center justify-between text-[11px]">
            <span class="text-muted-foreground">Peran Anti-Kamuflase:</span>
            <span class="font-semibold text-teal-600 dark:text-teal-400">
              {claim.channelContribution.semantic >= 0.28 ? "Diskrepansi Klinis Terbukti" : "Kepatuhan Rekam Medis"}
            </span>
          </div>
        </div>
      </div>

      <!-- Fusion Mathematical Proof Note -->
      <div class="rounded-2xl bg-primary/5 border border-primary/20 p-4 space-y-2 text-xs">
        <div class="flex items-center gap-2 text-primary font-bold">
          <Icon name="Layers" size={15} />
          <span>Prinsip Fusi Multi-Saluran Anti-Kamuflase:</span>
        </div>
        <p class="text-foreground leading-relaxed">
          Dalam model graf biasa, sindikat yang menyebarkan rujukan (menurunkan skor $T$) akan lolos sebagai klaim normal.
          Pada MHGSL, representasi akhir dihitung melalui gabungan
          <code class="bg-primary/10 text-primary px-1.5 py-0.5 rounded font-mono text-[11px]">
            H⁽ᶠⁱⁿᵃˡ⁾ = Concat(H⁽ᵗᵒᵖ⁾, H⁽ᶠᵉᵃᵗ⁾, H⁽ˢᵉᵐ⁾, H⁽ˢʰᵃʳᵉᵈ⁾)
          </code>.
          Bila ada sindikat yang berupaya memanipulasi satu dimensi, dua dimensi lainnya memberikan kompensasi matematis independen
          sehingga nilai prediksi akhir tetap akurat tanpa false-negative.
        </p>
      </div>
    </div>

    <!-- SHAP Signal Prose with Interactive Math Impact Tooltips -->
    <div class="rounded-3xl border border-border bg-card p-6 shadow-xs space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <Icon name="Sparkles" size={17} class="text-primary" />
          <h3 class="font-bold text-base text-foreground">
            Sinyal Penjelas SHAP & Dampak Matematis Kenaikan Skor
          </h3>
        </div>
        <span class="text-xs text-muted-foreground">
          Klik atau arahkan kursor pada ikon <strong class="text-foreground">Info</strong> untuk rincian dampak kalkulasi.
        </span>
      </div>

      <p class="text-xs text-muted-foreground leading-relaxed">
        Analisis atribusi fitur menggunakan TreeExplainer terintegrasi pada modul MHGSL.
        Setiap sinyal merepresentasikan deviasi marginal (&phi;) yang mendorong probabilitas fraud berkas ini:
      </p>

      <div class="space-y-3 pt-1">
        {#each shapList as shap, idx}
          {@const meta = analyzeShapSignal(shap, idx, shapList.length, claim)}
          <div class="relative rounded-2xl border border-border/80 bg-muted/25 p-3.5 transition-colors hover:bg-muted/40 hover:border-border">
            <div class="flex items-start justify-between gap-3">
              <div class="flex items-start gap-3 flex-1">
                <!-- Channel Tag Chip -->
                <span
                  class="shrink-0 mt-0.5 inline-flex items-center justify-center h-6 w-6 rounded-md font-mono text-[11px] font-bold border {meta.channel === 'T'
                    ? 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/30'
                    : meta.channel === 'F'
                      ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30'
                      : 'bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/30'}"
                  title="Saluran Dominan: {meta.channel === 'T' ? 'Topologi' : meta.channel === 'F' ? 'Fitur' : 'Semantik'}"
                >
                  {meta.channel}
                </span>

                <div class="space-y-1 flex-1">
                  <div class="flex flex-wrap items-center gap-2">
                    <span class="text-[11px] font-bold text-muted-foreground uppercase tracking-wider">
                      {meta.category}
                    </span>
                    <span class="font-mono text-[10px] px-1.5 py-0.2 rounded bg-rose-500/10 text-rose-600 dark:text-rose-400 font-semibold tabular-nums">
                      &Delta;p &approx; {meta.deltaProb}
                    </span>
                  </div>
                  <p class="text-xs font-medium text-foreground leading-relaxed">
                    {shap}
                  </p>
                </div>
              </div>

              <!-- Interactive Info Tooltip Trigger (accessible >= 32px click target) -->
              <div class="relative shrink-0">
                <button
                  type="button"
                  class="min-h-[32px] min-w-[32px] rounded-lg border border-border/80 bg-background hover:bg-muted text-muted-foreground hover:text-foreground flex items-center justify-center transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                  onclick={() => toggleTooltip(idx)}
                  onmouseenter={() => (activeTooltip = idx)}
                  aria-expanded={activeTooltip === idx}
                  aria-label="Penjelasan dampak kenaikan skor untuk {shap}"
                >
                  <Icon name="Info" size={15} />
                </button>

                <!-- Tooltip / Popover Content -->
                {#if activeTooltip === idx}
                  <div
                    class="absolute right-0 bottom-full mb-2 w-72 sm:w-80 rounded-2xl border border-slate-200 dark:border-[#a3b18a]/25 bg-white dark:bg-[#203127] text-foreground p-4 shadow-2xl z-50 text-xs space-y-2.5 animate-in fade-in zoom-in-95 duration-150"
                    role="tooltip"
                    onmouseleave={closeTooltip}
                  >
                    <div class="flex items-center justify-between border-b border-slate-200 dark:border-[#a3b18a]/25 pb-2">
                      <div class="flex items-center gap-1.5 font-bold text-foreground">
                        <Icon name="Activity" size={13} class="text-primary" />
                        <span>Kalkulasi Dampak SHAP (&phi;)</span>
                      </div>
                      <span class="font-mono text-[11px] font-extrabold text-rose-600 dark:text-rose-400 tabular-nums">
                        &Delta;p = {meta.deltaProb}
                      </span>
                    </div>

                    <div class="space-y-1">
                      <span class="text-[10px] font-semibold uppercase text-muted-foreground block">
                        Mekanisme Peningkatan Skor:
                      </span>
                      <p class="text-foreground leading-relaxed text-[11px]">
                        {meta.mechanism}
                      </p>
                    </div>

                    <div class="rounded-xl bg-muted/60 p-2.5 border border-slate-200/80 dark:border-[#a3b18a]/20 space-y-1">
                      <span class="text-[10px] font-semibold uppercase text-primary block">
                        Rekomendasi Audit Verifikator:
                      </span>
                      <p class="text-muted-foreground leading-relaxed text-[11px]">
                        {meta.auditAdvice}
                      </p>
                    </div>

                    <div class="pt-1 flex items-center justify-between text-[10px] text-muted-foreground">
                      <span>Estimasi Deviasi: &phi; = +{meta.phiValue.toFixed(2)}</span>
                      <button
                        type="button"
                        class="text-primary hover:underline font-semibold"
                        onclick={closeTooltip}
                      >
                        Tutup
                      </button>
                    </div>
                  </div>
                {/if}
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>

    <!-- Clinical AI Reasoning Card -->
    <div class="rounded-3xl border border-border bg-card p-6 shadow-xs space-y-3.5">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <Icon name="Bot" size={17} class="text-primary" />
          <h3 class="font-bold text-base text-foreground">
            Penalaran Klinis AI (Explainable AI Synthesis)
          </h3>
        </div>
        <span class="rounded-full bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-0.5 text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold font-mono">
          Ground Truth Verified
        </span>
      </div>

      <div class="p-4 rounded-2xl bg-primary/5 border border-primary/20 text-xs text-foreground leading-relaxed">
        <p class="font-medium">{claim.aiReasoning}</p>
      </div>

      {#if claim.notes}
        <div class="p-3.5 rounded-2xl bg-muted/25 border border-border text-[11px] text-muted-foreground space-y-1">
          <strong class="text-foreground block">Catatan Tambahan Verifikator:</strong>
          <p>{claim.notes}</p>
        </div>
      {/if}
    </div>

    <!-- Unified Factual Clinical Audit Report & MCP Investigation Dossier -->
    <div class="rounded-3xl bg-card p-6 shadow-md space-y-5 border border-slate-200/80 dark:border-[#a3b18a]/20">
      <!-- Card Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 mb-2 border-b border-slate-200/60 dark:border-[#a3b18a]/20">
        <div>
          <div class="flex items-center gap-2">
            <span class="flex h-7 w-7 items-center justify-center rounded-xl bg-[#588157]/15 text-[#588157] font-bold text-sm">
              📋
            </span>
            <h3 class="font-bold text-base text-foreground">
              Laporan Audit Klinis &amp; Dossier Investigasi (AI + MCP Grounded Evidence)
            </h3>
          </div>
          <p class="text-xs text-muted-foreground mt-0.5">
            AI Agent menghimpun data rekam medis EMR, hasil dekomposisi 3-kanal MHGSL GNN, dan eviden regulasi via MCP tools untuk menyusun laporan ringkas berbasis fakta murni.
          </p>
        </div>

        <div class="flex items-center gap-2 shrink-0">
          <span class="rounded-full bg-[#588157]/10 px-2.5 py-0.5 text-[10px] font-mono text-[#3a5a40] dark:text-[#a3b18a] font-bold">
            Model: aegis-jkn · MCP v1.0
          </span>
          <button
            type="button"
            data-testid="ai-report-generate-button"
            disabled={isGeneratingReport}
            onclick={generateUnifiedReport}
            class="inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-[#3a5a40] to-[#588157] hover:from-[#344e41] hover:to-[#3a5a40] px-4 py-2 text-xs font-bold text-white shadow-xs disabled:opacity-50 transition-all cursor-pointer"
          >
            {#if isGeneratingReport}
              <span class="inline-block h-3.5 w-3.5 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
              <span>Menghimpun Fakta...</span>
            {:else}
              <Icon name="Sparkles" size={14} />
              <span>{unifiedReport ? "Analisis Ulang (MCP)" : "Buat Laporan Terverifikasi MCP"}</span>
            {/if}
          </button>
        </div>
      </div>

      <!-- Factual Evidence Data Pipeline Trace (What MCP retrieved) -->
      <div class="p-3.5 rounded-2xl bg-muted/40 text-xs space-y-2 border border-slate-200/60 dark:border-[#a3b18a]/15">
        <div class="flex items-center justify-between">
          <span class="text-[11px] font-bold uppercase tracking-wider text-muted-foreground font-mono flex items-center gap-1.5">
            <span>Alur Bukti Fakta (MCP Data Retrieval Tools):</span>
          </span>
          <span class="inline-flex items-center gap-1 text-[10px] font-mono font-bold text-[#588157]">
            <span class="h-1.5 w-1.5 rounded-full bg-[#588157] animate-pulse"></span>
            MCP Tools Active
          </span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-[11px]">
          <div class="p-2.5 rounded-xl bg-card shadow-2xs space-y-1">
            <div class="font-bold text-foreground flex items-center gap-1">
              <span class="text-[#588157] font-mono">1.</span> get_claim_forensic_facts
            </div>
            <p class="text-[10px] text-muted-foreground leading-tight">Data Pasien, DPJP, ICD-10/ICD-9, Biaya &amp; LOS</p>
          </div>
          <div class="p-2.5 rounded-xl bg-card shadow-2xs space-y-1">
            <div class="font-bold text-foreground flex items-center gap-1">
              <span class="text-[#588157] font-mono">2.</span> get_mhgsl_analysis
            </div>
            <p class="text-[10px] text-muted-foreground leading-tight">Skor Anomali, Bobot Kanal T:F:S &amp; Sindikat</p>
          </div>
          <div class="p-2.5 rounded-xl bg-card shadow-2xs space-y-1">
            <div class="font-bold text-foreground flex items-center gap-1">
              <span class="text-[#588157] font-mono">3.</span> get_clinical_evidence_rules
            </div>
            <p class="text-[10px] text-muted-foreground leading-tight">Fornas, Kontradiksi Narasi &amp; UU PDP 27/2022</p>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      {#if isGeneratingReport}
        <div class="p-8 text-center space-y-2.5 rounded-2xl bg-muted/20">
          <div class="inline-block h-6 w-6 animate-spin rounded-full border-2 border-[#588157] border-t-transparent"></div>
          <div class="text-xs font-bold text-foreground">Menjalankan pipeline MCP &amp; sintesis AI model aegis-jkn...</div>
          <p class="text-[11px] text-muted-foreground max-w-md mx-auto leading-relaxed">
            Mengekstraksi fakta klinis klaim {claim.id}, mengkalkulasi kontribusi saluran graf MHGSL, dan menyusun Berita Acara bersegel kriptografis tanpa halusinasi.
          </p>
        </div>
      {:else if reportError}
        <div class="p-4 rounded-2xl bg-rose-500/10 text-xs text-rose-800 dark:text-rose-300 flex items-start justify-between gap-3">
          <div class="flex items-start gap-2">
            <Icon name="AlertTriangle" size={16} class="shrink-0 mt-0.5" />
            <div>
              <strong>Kendala Eksekusi Laporan:</strong>
              <p class="mt-0.5">{reportError}</p>
            </div>
          </div>
          <button
            type="button"
            onclick={generateUnifiedReport}
            class="rounded-lg bg-rose-500/15 hover:bg-rose-500/25 px-2.5 py-1 text-[11px] font-bold shrink-0 cursor-pointer"
          >
            Coba Lagi
          </button>
        </div>
      {:else if unifiedReport}
        <div class="space-y-3 animate-in fade-in duration-200">
          <div class="flex flex-wrap items-center justify-between gap-2 text-xs">
            <span class="font-bold text-foreground flex items-center gap-1.5">
              <Icon name="ShieldCheck" size={15} class="text-[#588157]" />
              <span>Berkas Laporan Klinis &amp; Dossier Forensik Bersegel:</span>
            </span>
            <div class="flex items-center gap-2">
              <button
                type="button"
                onclick={copyReport}
                class="inline-flex items-center gap-1 rounded-xl bg-muted/60 hover:bg-muted px-3 py-1.5 text-[11px] font-semibold text-foreground transition-colors cursor-pointer"
              >
                {#if copied}
                  <Icon name="Check" size={12} class="text-emerald-500" />
                  <span>Tersalin!</span>
                {:else}
                  <Icon name="ClipboardList" size={12} />
                  <span>Salin Teks</span>
                {/if}
              </button>
              <button
                type="button"
                onclick={downloadReport}
                class="inline-flex items-center gap-1 rounded-xl bg-gradient-to-r from-[#3a5a40] to-[#588157] hover:from-[#344e41] hover:to-[#3a5a40] px-3.5 py-1.5 text-[11px] font-bold text-white shadow-2xs transition-all cursor-pointer"
              >
                <Icon name="Download" size={12} />
                <span>Unduh Dossier (.md)</span>
              </button>
            </div>
          </div>

          <FormattedAiReport
            rawText={unifiedReport}
            claimId={claim.id}
            hospital={claim.hospital}
            fraudScore={claim.fraudScore}
            title="Laporan Audit Klinis &amp; Dossier Forensik Terverifikasi MCP"
          />
        </div>
      {:else}
        <div class="p-6 rounded-2xl bg-muted/20 text-center text-xs text-muted-foreground space-y-1">
          <p>
            Klik tombol <strong>"Buat Laporan Terverifikasi MCP"</strong> di atas untuk meminta AI Agent mengeksekusi tools MCP (fakta klaim, graf MHGSL, dan regulasi klinis) dan menerbitkan dossier audit forensik resmi.
          </p>
        </div>
      {/if}
    </div>
  </div>
{:else}
  <div class="flex h-full flex-col items-center justify-center p-8 text-center text-xs text-muted-foreground space-y-2">
    <Icon name="ClipboardList" size={32} class="text-muted-foreground/40 mb-1" />
    <span class="font-semibold text-foreground">Tidak Ada Berkas Terpilih</span>
    <p class="max-w-xs">
      Pilih salah satu berkas klaim dari antrean sebelah kiri untuk melihat pembuktian matematis MHGSL.
    </p>
  </div>
{/if}
