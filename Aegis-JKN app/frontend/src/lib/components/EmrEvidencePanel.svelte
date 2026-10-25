<script lang="ts">
  import { dashboard } from "$lib/stores/dashboard.svelte";
  import Icon from "./Icon.svelte";

  function formatRupiah(val: number): string {
    return `Rp ${val.toLocaleString("id-ID")}`;
  }

  const claim = $derived(dashboard.selectedClaim);

  // FORNAS Formularium Nasional reference dictionary
  interface FornasDrug {
    code: string;
    name: string;
    indication: string;
    tier: string;
    riskCategory: "safe" | "high-volume" | "mismatch" | "narcotic";
  }

  const FORNAS_DICT: Record<string, FornasDrug> = {
    M01: { code: "M01", name: "Metformin 500mg", indication: "Antidiabetes Oral (DM Tipe 2)", tier: "Faskes 1/2/3", riskCategory: "safe" },
    M02: { code: "M02", name: "Glimepirid 2mg", indication: "Sulfonilurea Hipoglikemik Oral", tier: "Faskes 1/2/3", riskCategory: "safe" },
    M03: { code: "M03", name: "Ceftriaxone Inj 1g", indication: "Antibiotik Sefalosporin Generasi III", tier: "Faskes 2/3 (Restriksi)", riskCategory: "high-volume" },
    M04: { code: "M04", name: "Omeprazole Inj 40mg", indication: "Proton Pump Inhibitor (PPI GI)", tier: "Faskes 2/3 (Rawat Inap)", riskCategory: "safe" },
    M05: { code: "M05", name: "Salbutamol 2.5mg Respules", indication: "Bronkodilator Agonis Beta-2 Inhalasi", tier: "Faskes 1/2/3", riskCategory: "safe" },
    M08: { code: "M08", name: "Ketorolac Inj 30mg", indication: "Analgetik NSAID Post-Operatif", tier: "Faskes 2/3 (Maks 2 hari)", riskCategory: "safe" },
    M09: { code: "M09", name: "Insulin Glargine 100 IU/ml Pen", indication: "Insulin Basal Long-Acting Analog", tier: "Faskes 2/3 (Maks 1-2 pen/bln)", riskCategory: "high-volume" },
    M10: { code: "M10", name: "Clopidogrel 75mg / Ticagrelor", indication: "Antiplatelet Ganda Pasca-PCI Stent", tier: "Faskes 2/3 (Wajib PCI)", riskCategory: "mismatch" },
  };

  interface ParsedDrug {
    raw: string;
    code: string;
    quantityText: string;
    quantityNum: number;
    meta?: FornasDrug;
    isAnomaly: boolean;
  }

  let activeDrugTooltip = $state<string | null>(null);

  const parsedDrugs = $derived.by<ParsedDrug[]>(() => {
    if (!claim?.drugs || claim.drugs === "—" || claim.drugs.trim() === "") return [];
    const parts = claim.drugs.split(";").map((s) => s.trim()).filter(Boolean);

    return parts.map((part) => {
      const match = part.match(/(M\d{2})\s*(?:x\s*(\d+))?/i);
      const code = match ? match[1].toUpperCase() : part;
      const quantityNum = match && match[2] ? parseInt(match[2], 10) : 1;
      const meta = FORNAS_DICT[code];

      // Anomaly detection: excessive quantities (e.g. insulin M09 > 4 pens, M03 > 10 vials)
      const isAnomaly = (code === "M09" && quantityNum >= 20) || (code === "M03" && quantityNum >= 15);

      return {
        raw: part,
        code,
        quantityText: match && match[2] ? `${match[2]} unit` : part,
        quantityNum,
        meta,
        isAnomaly,
      };
    });
  });

  // INA-CBG Standard Length of Stay benchmarks
  interface InacbgBenchmark {
    group: string;
    cbgCode: string;
    avgLosDays: number;
    minExpectedDays: number;
    maxExpectedDays: number;
  }

  function getInacbgBenchmark(diagnosis: string, procedure: string): InacbgBenchmark {
    const d = diagnosis.toLowerCase();
    const p = procedure.toLowerCase();

    if (p.includes("00.66") || p.includes("pci") || p.includes("angioplasti")) {
      return { group: "Intervensi Kardiovaskular Perkutan", cbgCode: "I-4-10-I", avgLosDays: 3, minExpectedDays: 2, maxExpectedDays: 5 };
    }
    if (p.includes("81.52") || p.includes("hemiarthroplasty")) {
      return { group: "Rekonstruksi Sendi Panggul Mayor", cbgCode: "M-1-04-II", avgLosDays: 6, minExpectedDays: 4, maxExpectedDays: 9 };
    }
    if (p.includes("51.23") || p.includes("kolesistektomi")) {
      return { group: "Kolesistektomi Laparoskopik", cbgCode: "B-4-13-I", avgLosDays: 3, minExpectedDays: 2, maxExpectedDays: 5 };
    }
    if (p.includes("96.04") || p.includes("intubasi")) {
      return { group: "Prosedur Jalan Napas Non-Bedah Terbuka", cbgCode: "E-4-15-I", avgLosDays: 1, minExpectedDays: 0, maxExpectedDays: 2 };
    }
    if (p.includes("47.09") || p.includes("apendektomi")) {
      return { group: "Prosedur Apendektomi Tanpa Komplikasi", cbgCode: "K-1-10-I", avgLosDays: 3, minExpectedDays: 2, maxExpectedDays: 4 };
    }
    if (p.includes("74.1") || p.includes("seksio")) {
      return { group: "Seksio Sesarea Tanpa Komplikasi Berat", cbgCode: "O-6-10-I", avgLosDays: 3, minExpectedDays: 2, maxExpectedDays: 4 };
    }
    if (p.includes("53.1") || p.includes("hernia")) {
      return { group: "Perbaikan Hernia Inguinalis", cbgCode: "K-1-12-I", avgLosDays: 2, minExpectedDays: 1, maxExpectedDays: 3 };
    }
    if (d.includes("k29") || d.includes("gastritis")) {
      return { group: "Penyakit Saluran Cerna Ringan", cbgCode: "K-4-17-I", avgLosDays: 2, minExpectedDays: 1, maxExpectedDays: 3 };
    }
    if (d.includes("j18") || d.includes("pneumonia")) {
      return { group: "Infeksi Paru / Pneumonia Sederhana", cbgCode: "J-4-16-I", avgLosDays: 5, minExpectedDays: 3, maxExpectedDays: 7 };
    }
    if (d.includes("e11") || d.includes("diabetes")) {
      return { group: "Diabetes Melitus Tanpa Komplikasi Mayor", cbgCode: "E-4-10-I", avgLosDays: 0, minExpectedDays: 0, maxExpectedDays: 2 };
    }
    return { group: "Kasus Medis Umum INA-CBG", cbgCode: "Z-9-99-I", avgLosDays: 3, minExpectedDays: 1, maxExpectedDays: 5 };
  }

  const losBenchmark = $derived.by<InacbgBenchmark>(() => {
    if (!claim) return { group: "Umum", cbgCode: "Z-0-00", avgLosDays: 3, minExpectedDays: 1, maxExpectedDays: 5 };
    return getInacbgBenchmark(claim.diagnosisIcd10 || "", claim.procedureIcd9 || "");
  });

  // Clinical Mismatch Evaluator
  interface MismatchEvaluation {
    hasMismatch: boolean;
    severity: "danger" | "warning" | "neutral";
    reason: string;
    icd10Type: "ringan" | "kronis" | "akut_bedah" | "kebidanan";
    procedureType: "bedah_mayor" | "invasif_jantung" | "unbundled" | "konservatif" | "bedah_standar";
    missingDrugs?: string;
  }

  function evaluateClinicalMismatch(dx: string, proc: string, drugsStr: string): MismatchEvaluation {
    const d = dx.toLowerCase();
    const p = proc.toLowerCase();

    // Severe: Gastritis / DM / Persalinan normal claimed for PCI (Coronary Stent)
    if (p.includes("00.66") || p.includes("angioplasti")) {
      if (d.includes("k29") || d.includes("gastritis")) {
        return {
          hasMismatch: true,
          severity: "danger",
          reason: "UPCODING KRITIS: Diagnosis primer hanya gastritis ringan (K29.7) tetapi ditagih tindakan bedah invasif kateterisasi jantung & stent PCI (00.66). Pasien tanpa riwayat penyakit jantung iskemik.",
          icd10Type: "ringan",
          procedureType: "invasif_jantung",
          missingDrugs: "Tidak ditemukan obat antiplatelet (M10 Clopidogrel/Aspirin) maupun statin pasca-PCI.",
        };
      }
      if (d.includes("e11") || d.includes("diabetes")) {
        return {
          hasMismatch: true,
          severity: "danger",
          reason: "UPCODING KRITIS: Kontrol diabetes rutin tanpa komplikasi kardiologis ditagih prosedur pemasangan stent koroner (00.66).",
          icd10Type: "kronis",
          procedureType: "invasif_jantung",
          missingDrugs: "Tanpa protokol pengencer darah kardiovaskular pasca-implan stent.",
        };
      }
    }

    // Severe: Normal spontaneous vaginal delivery claimed as Caesarean Section
    if (d.includes("o80") && (p.includes("74.1") || p.includes("seksio"))) {
      return {
        hasMismatch: true,
        severity: "danger",
        reason: "UPCODING MATERNITAS: Diagnosis O80 (persalinan spontan pervaginam) diklaimkan tindakan seksio sesarea (74.1) tanpa indikasi komplikasi obstetrik.",
        icd10Type: "kebidanan",
        procedureType: "bedah_mayor",
      };
    }

    // Unbundling warning: intubasi ditagih terpisah dari laparoskopi
    if (p.includes("96.04") || p.includes("intubasi")) {
      return {
        hasMismatch: true,
        severity: "warning",
        reason: "UNBUNDLING: Prosedur intubasi endotrakeal (96.04) ditagihkan mandiri pada episode yang bersamaan dengan paket bedah anestesi umum.",
        icd10Type: "ringan",
        procedureType: "unbundled",
      };
    }

    // Hip hemiarthroplasty with 1 day LOS or no drugs
    if ((p.includes("81.52") || p.includes("hemiarthroplasty")) && (!drugsStr || drugsStr === "—")) {
      return {
        hasMismatch: true,
        severity: "danger",
        reason: "PHANTOM PROCEDURE: Hemiarthroplasty panggul (bedah ortopedi mayor) diklaimkan tanpa dispensing analgetik post-op atau antibiotik profilaksis.",
        icd10Type: "akut_bedah",
        procedureType: "bedah_mayor",
        missingDrugs: "Wajib ada antibiotik profilaksis dan analgetik parenteral.",
      };
    }

    return {
      hasMismatch: false,
      severity: "neutral",
      reason: "Diagnosis ICD-10 dan Prosedur ICD-9-CM selaras dengan protokol penjaminan INA-CBG.",
      icd10Type: "akut_bedah",
      procedureType: p.includes("—") ? "konservatif" : "bedah_standar",
    };
  }

  const mismatchEval = $derived.by<MismatchEvaluation>(() => {
    if (!claim) {
      return {
        hasMismatch: false,
        severity: "neutral",
        reason: "",
        icd10Type: "ringan",
        procedureType: "konservatif",
      };
    }
    return evaluateClinicalMismatch(claim.diagnosisIcd10 || "", claim.procedureIcd9 || "", claim.drugs || "");
  });

  // LOS Deviation calculations
  const losDiff = $derived.by<number>(() => {
    if (!claim) return 0;
    return claim.losDays - losBenchmark.avgLosDays;
  });

  const losStatus = $derived.by<"normal" | "prolonged" | "understay">(() => {
    if (!claim) return "normal";
    if (claim.losDays > losBenchmark.maxExpectedDays) return "prolonged";
    if (claim.losDays < losBenchmark.minExpectedDays && (claim.procedureIcd9?.includes("81.52") || claim.procedureIcd9?.includes("51.23"))) return "understay";
    return "normal";
  });
</script>

{#if claim}
  <div class="h-full overflow-y-auto p-4 sm:p-6 space-y-6 scrollbar-thin text-foreground">
    <!-- Top Meta Banner -->
    <div class="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-border">
      <div>
        <div class="flex items-center gap-2">
          <span class="font-mono font-black text-xl text-primary">{claim.id}</span>
          <span class="rounded-full px-2.5 py-0.5 text-xs font-bold font-mono uppercase {claim.risk === 'fraud' ? 'bg-rose-500/15 text-rose-800 dark:text-rose-300 border border-rose-500/30' : claim.risk === 'high' ? 'bg-amber-500/15 text-amber-800 dark:text-amber-300 border border-amber-500/30' : 'bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 border border-emerald-500/30'}">
            Risiko: {claim.risk}
          </span>
          {#if claim.syndicate}
            <span class="rounded bg-primary/15 text-primary text-xs font-bold px-2 py-0.5">
              Klaster {claim.syndicate}
            </span>
          {/if}
        </div>
        <div class="text-xs text-muted-foreground mt-1">
          Episode Pelayanan: <strong class="text-foreground">{claim.date}</strong> · {claim.hospital} ({claim.serviceType})
        </div>
      </div>

      <div class="text-right">
        <div class="text-[11px] text-muted-foreground">Biaya Diajukan Faskes:</div>
        <div class="text-xl sm:text-2xl font-black font-mono tabular-nums text-foreground">
          {formatRupiah(claim.costRp)}
        </div>
      </div>
    </div>

    <!-- Administrative & SEP Profile Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
      <div class="rounded-xl border border-border bg-card p-3 shadow-2xs">
        <span class="text-[11px] text-muted-foreground block font-medium">Pasien Terdaftar:</span>
        <span class="font-bold text-foreground text-sm mt-0.5 block truncate" title={claim.patient}>{claim.patient}</span>
      </div>

      <div class="rounded-xl border border-border bg-card p-3 shadow-2xs">
        <span class="text-[11px] text-muted-foreground block font-medium">Dokter DPJP:</span>
        <span class="font-bold text-foreground text-sm mt-0.5 block truncate" title={claim.doctor}>{claim.doctor}</span>
      </div>

      <div class="rounded-xl border border-border bg-card p-3 shadow-2xs">
        <span class="text-[11px] text-muted-foreground block font-medium">Fasilitas Kesehatan:</span>
        <span class="font-bold text-foreground text-sm mt-0.5 block truncate" title={claim.hospital}>{claim.hospital}</span>
      </div>

      <!-- Enhanced LOS card with INA-CBG benchmark deviation -->
      <div class="rounded-xl border border-border bg-card p-3 shadow-2xs relative overflow-hidden">
        <div class="flex items-center justify-between">
          <span class="text-[11px] text-muted-foreground font-medium">Lama Rawat (LOS):</span>
          {#if losStatus === 'prolonged'}
            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/30">
              +{losDiff} Hari (Overstay)
            </span>
          {:else if losStatus === 'understay'}
            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30">
              Bedah Mayor {claim.losDays}H
            </span>
          {:else}
            <span class="text-[10px] font-medium text-emerald-600 dark:text-emerald-400">
              Wajar INA-CBG
            </span>
          {/if}
        </div>
        <div class="flex items-baseline gap-2 mt-1">
          <span class="font-mono font-black text-foreground text-lg tabular-nums">{claim.losDays} Hari</span>
          <span class="text-[11px] text-muted-foreground font-mono">
            (Wajar: {losBenchmark.avgLosDays} hari)
          </span>
        </div>
      </div>
    </div>

    <!-- Referral Info -->
    <div class="rounded-xl border border-border/80 bg-muted/20 p-3 text-xs flex items-center gap-2">
      <Icon name="Hospital" size={16} class="text-primary shrink-0" />
      <div class="truncate">
        <span class="text-muted-foreground">Surat Rujukan: </span>
        <strong class="text-foreground">{claim.referral}</strong>
      </div>
    </div>

    <!-- Diagnosis vs Procedure Match Card with ICD-10 vs ICD-9 Mismatch Diff -->
    <div class="rounded-2xl border {mismatchEval.hasMismatch ? 'border-rose-500/40 bg-card' : 'border-border bg-card'} p-5 shadow-xs space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <Icon name="ClipboardList" size={16} class="text-primary" />
          <h3 class="font-bold text-sm text-foreground">Evaluasi Koding INA-CBG (ICD-10 vs ICD-9-CM)</h3>
        </div>
        
        <div class="flex items-center gap-1.5">
          {#if mismatchEval.hasMismatch}
            <span class="rounded-full bg-rose-500/15 text-rose-800 dark:text-rose-300 font-bold px-2.5 py-0.5 text-[10px] flex items-center gap-1 border border-rose-500/40 animate-pulse">
              <Icon name="AlertTriangle" size={11} />
              <span>DISKREPANSI KLINIS TINGGI</span>
            </span>
          {:else}
            <span class="rounded-full bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 font-semibold px-2.5 py-0.5 text-[10px] flex items-center gap-1 border border-emerald-500/30">
              <Icon name="CheckCircle2" size={11} />
              <span>Koding Sinkron</span>
            </span>
          {/if}
        </div>
      </div>

      <!-- Visual Diff Comparison Panel -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
        <!-- Left: Diagnosis ICD-10 -->
        <div class="rounded-xl border {mismatchEval.hasMismatch ? 'border-amber-500/40 bg-amber-500/5' : 'border-border bg-muted/30'} p-3.5 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-[10px] uppercase font-bold text-muted-foreground tracking-wider block">
              Diagnosis Primer (ICD-10)
            </span>
            <span class="text-[10px] font-mono px-1.5 py-0.2 rounded {mismatchEval.icd10Type === 'ringan' ? 'bg-amber-500/20 text-amber-800 dark:text-amber-300' : 'bg-muted text-muted-foreground'}">
              Tingkat: {mismatchEval.icd10Type.toUpperCase()}
            </span>
          </div>
          <div class="font-mono font-bold text-sm text-foreground">
            {claim.diagnosisIcd10}
          </div>
          <p class="text-[11px] text-muted-foreground leading-relaxed">
            Kondisi medis utama penjaminan saat admisi awal faskes.
          </p>
        </div>

        <!-- Right: Procedure ICD-9-CM with Mismatch Highlighting -->
        <div class="rounded-xl border {mismatchEval.hasMismatch ? 'border-rose-500/40 bg-rose-500/10' : 'border-border bg-muted/30'} p-3.5 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-[10px] uppercase font-bold text-muted-foreground tracking-wider block">
              Prosedur / Tindakan (ICD-9-CM)
            </span>
            {#if mismatchEval.hasMismatch}
              <span class="text-[10px] font-bold font-mono px-1.5 py-0.2 rounded bg-rose-600 text-white dark:bg-rose-500">
                MISMATCH TINGKAT BEDAH
              </span>
            {/if}
          </div>
          <div class="font-mono font-bold text-sm {mismatchEval.hasMismatch ? 'text-rose-600 dark:text-rose-400' : 'text-foreground'}">
            {claim.procedureIcd9 || "— (Perawatan Konservatif Non-Bedah)"}
          </div>
          <p class="text-[11px] text-muted-foreground leading-relaxed">
            Tindakan yang diklaimkan untuk penentuan tarif paket INA-CBG.
          </p>
        </div>
      </div>

      <!-- High-Contrast Mismatch Alert Banner if discrepancy exists -->
      {#if mismatchEval.hasMismatch}
        <div class="p-3.5 rounded-xl border border-rose-500/40 bg-rose-500/10 text-xs text-rose-900 dark:text-rose-200 space-y-1.5">
          <div class="flex items-center gap-2 font-bold">
            <Icon name="ShieldAlert" size={15} class="text-rose-600 dark:text-rose-400 shrink-0" />
            <span class="font-mono tracking-tight uppercase">Audit Koding Klinis Terpental (Kaidah Kemenkes / INA-CBG):</span>
          </div>
          <p class="leading-relaxed pl-5 font-medium">
            {mismatchEval.reason}
          </p>
          {#if mismatchEval.missingDrugs}
            <div class="pl-5 text-[11px] text-rose-700 dark:text-rose-300 font-mono flex items-center gap-1.5">
              <Icon name="AlertTriangle" size={12} class="shrink-0" />
              <span>Gap Terapi Farmasi: {mismatchEval.missingDrugs}</span>
            </div>
          {/if}
        </div>
      {/if}

      <!-- LOS Deviation Analysis Progress Gauge -->
      <div class="pt-3 border-t border-border/70 space-y-2">
        <div class="flex items-center justify-between text-xs">
          <div class="flex items-center gap-1.5">
            <Icon name="Activity" size={14} class="text-primary" />
            <span class="font-semibold text-foreground">Analisis Deviasi LOS (Lama Hari Rawat vs Rata-Rata INA-CBG):</span>
          </div>
          <span class="font-mono text-[11px] text-muted-foreground">
            Tarif Paket: <strong>{losBenchmark.cbgCode}</strong> ({losBenchmark.group})
          </span>
        </div>

        <!-- Visual Range Bar -->
        <div class="rounded-xl bg-muted/40 p-3 border border-border/80 text-xs space-y-2">
          <div class="flex items-center justify-between text-[11px]">
            <span class="text-muted-foreground">Rentang Normal INA-CBG: <strong class="text-foreground">{losBenchmark.minExpectedDays} - {losBenchmark.maxExpectedDays} hari</strong></span>
            <span class="font-mono font-bold {losStatus === 'prolonged' ? 'text-rose-600 dark:text-rose-400' : losStatus === 'understay' ? 'text-amber-600 dark:text-amber-400' : 'text-emerald-600 dark:text-emerald-400'}">
              {#if losStatus === 'prolonged'}
                Deviasi: +{losDiff} Hari di atas median
              {:else if losStatus === 'understay'}
                Deviasi: {claim.losDays} Hari (Pulang tergesa-gesa pasca bedah)
              {:else}
                Deviasi: Sesuai Panduan Klinis (±0)
              {/if}
            </span>
          </div>

          <!-- Comparative meter bar -->
          <div class="h-2.5 w-full bg-muted rounded-full overflow-hidden flex border border-border/50">
            <div
              class="h-full {losStatus === 'prolonged' ? 'bg-rose-500' : losStatus === 'understay' ? 'bg-amber-500' : 'bg-emerald-500'} transition-all duration-300"
              style="width: {Math.min(100, Math.max(8, (claim.losDays / Math.max(10, losBenchmark.maxExpectedDays + 3)) * 100))}%"
            ></div>
          </div>
          <div class="flex justify-between text-[10px] text-muted-foreground font-mono">
            <span>0 hari</span>
            <span>Median: {losBenchmark.avgLosDays} hari</span>
            <span>Max Wajar: {losBenchmark.maxExpectedDays} hari</span>
            <span>Aktual: {claim.losDays} hari</span>
          </div>
        </div>
      </div>

      <!-- FORNAS Interactive Chip Badges -->
      <div class="pt-3 border-t border-border/70 space-y-2">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-1.5">
            <Icon name="Syringe" size={14} class="text-primary" />
            <span class="text-xs font-semibold text-foreground">
              Daftar Obat & Terapi Farmasi Terdispensasi (FORNAS):
            </span>
          </div>
          <span class="text-[10px] text-muted-foreground">
            Klik badge untuk rincian restriksi FORNAS
          </span>
        </div>

        {#if parsedDrugs.length > 0}
          <div class="flex flex-wrap gap-2 pt-1">
            {#each parsedDrugs as drug}
              <button
                type="button"
                onclick={() => activeDrugTooltip = activeDrugTooltip === drug.code ? null : drug.code}
                class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-mono font-medium border transition-colors cursor-pointer text-left {drug.isAnomaly ? 'bg-rose-500/15 text-rose-800 dark:text-rose-200 border-rose-500/40 hover:bg-rose-500/25' : drug.meta?.riskCategory === 'high-volume' ? 'bg-amber-500/15 text-amber-800 dark:text-amber-200 border-amber-500/40 hover:bg-amber-500/25' : 'bg-secondary text-secondary-foreground border-border hover:bg-accent'}"
                title="Klik untuk melihat indikasi FORNAS"
              >
                <span class="font-bold">{drug.code}</span>
                {#if drug.meta}
                  <span class="text-[11px] opacity-80 truncate max-w-[140px]">{drug.meta.name.split(" ")[0]}</span>
                {/if}
                <span class="text-[10px] opacity-70 px-1 rounded bg-black/10 dark:bg-white/10 tabular-nums">
                  {drug.quantityText}
                </span>
                {#if drug.isAnomaly}
                  <Icon name="AlertTriangle" size={11} class="text-rose-600 dark:text-rose-400" />
                {/if}
              </button>
            {/each}
          </div>

          <!-- Expanded Interactive Drug Detail Sheet -->
          {#if activeDrugTooltip}
            {@const active = parsedDrugs.find(d => d.code === activeDrugTooltip)}
            {#if active}
              <div class="mt-2 p-3 rounded-xl bg-card border border-primary/30 shadow-sm text-xs space-y-1.5 animate-fadeIn">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="font-mono font-black text-primary text-sm">{active.code}</span>
                    <span class="font-bold text-foreground">{active.meta ? active.meta.name : active.raw}</span>
                  </div>
                  <button
                    type="button"
                    onclick={() => activeDrugTooltip = null}
                    class="text-muted-foreground hover:text-foreground text-xs p-1"
                    aria-label="Tutup rincian obat"
                  >
                    <Icon name="X" size={14} />
                  </button>
                </div>
                {#if active.meta}
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 text-[11px]">
                    <div>
                      <span class="text-muted-foreground block">Indikasi Medis:</span>
                      <span class="text-foreground font-medium">{active.meta.indication}</span>
                    </div>
                    <div>
                      <span class="text-muted-foreground block">Restriksi / Faskes FORNAS:</span>
                      <span class="text-foreground font-medium">{active.meta.tier}</span>
                    </div>
                  </div>
                {/if}
                {#if active.isAnomaly}
                  <div class="mt-1 text-[11px] text-rose-700 dark:text-rose-300 font-medium flex items-center gap-1">
                    <Icon name="AlertTriangle" size={12} class="shrink-0" />
                    <span>Volume peresepan melampaui batas wajar episode tunggal ({active.quantityText}). Indikasi drug diversion.</span>
                  </div>
                {/if}
              </div>
            {/if}
          {/if}
        {:else}
          <div class="p-2.5 rounded-lg bg-background border border-border font-mono text-xs text-muted-foreground">
            Tidak ada rincian obat tercatat pada berkas klaim ini.
          </div>
        {/if}
      </div>
    </div>

    <!-- Clinical Narrative vs Patient Feedback (The Ground Truth Contrast) -->
    <div class="rounded-2xl border border-border bg-card p-5 shadow-xs space-y-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <Icon name="FileText" size={16} class="text-primary" />
          <h3 class="font-bold text-sm text-foreground">Verifikasi Narasi Medis vs Pengakuan Pasien</h3>
        </div>
        <span class="text-[11px] text-muted-foreground font-mono">
          Sentimen: <strong class="{claim.sentiment === 'negatif' ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'}">{claim.sentiment} ({claim.sentimentScore})</strong>
        </span>
      </div>

      <div class="space-y-3">
        <!-- Chief complaint -->
        <div class="p-3 rounded-xl bg-muted/20 border border-border/70 text-xs">
          <span class="text-[10px] font-bold uppercase text-muted-foreground block mb-0.5">Keluhan Utama Saat Berobat:</span>
          <p class="text-foreground font-medium">"{claim.chiefComplaint}"</p>
        </div>

        <!-- EMR Narrative -->
        <div class="p-3 rounded-xl bg-muted/20 border border-border/70 text-xs">
          <span class="text-[10px] font-bold uppercase text-muted-foreground block mb-0.5">Narasi Resume Medis Elektronik (DPJP):</span>
          <p class="text-foreground leading-relaxed italic">"{claim.clinicalNarrative}"</p>
        </div>

        <!-- Patient Survey Feedback -->
        <div class="p-3 rounded-xl bg-primary/5 border border-primary/20 text-xs">
          <span class="text-[10px] font-bold uppercase text-primary block mb-0.5">Pengakuan / Umpan Balik Pasien (Survei Oasis):</span>
          <p class="text-foreground leading-relaxed italic font-semibold">"{claim.patientFeedback}"</p>
        </div>

        <!-- Contradiction Warning Alert -->
        {#if claim.hasContradiction}
          <div class="p-4 rounded-xl border border-rose-500/40 bg-rose-500/10 text-xs text-rose-800 dark:text-rose-300 space-y-1">
            <div class="flex items-center gap-2 font-bold">
              <Icon name="AlertTriangle" size={16} />
              <span>PERINGATAN KONTRADIKSI KLINIS:</span>
            </div>
            <p class="leading-relaxed pl-6">
              Pengakuan pasien secara faktual bertentangan dengan tindakan bernilai tinggi yang diklaimkan oleh faskes. Berkas ini berpotensi kuat sebagai <strong>Phantom Billing</strong> atau <strong>Upcoding terencana</strong>.
            </p>
          </div>
        {/if}
      </div>
    </div>
  </div>
{:else}
  <div class="flex h-full items-center justify-center p-8 text-center text-xs text-muted-foreground">
    Pilih berkas klaim dari antrean sebelah kiri untuk melihat bukti rekam medis.
  </div>
{/if}

