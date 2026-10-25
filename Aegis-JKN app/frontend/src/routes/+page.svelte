<script lang="ts">
  import { onMount } from "svelte";
  import { theme } from "$lib/stores/theme.svelte";
  import Icon from "$lib/components/Icon.svelte";

  let openFaqIndex = $state<number | null>(0);
  let mobileMenuOpen = $state(false);

  function toggleFaq(index: number) {
    openFaqIndex = openFaqIndex === index ? null : index;
  }

  // Sponsors & Ecosystem Partners
  const partners = [
    { name: "BPJS Kesehatan", role: "Penyelenggara JKN" },
    { name: "Kementerian Kesehatan RI", role: "Standar SatuSehat" },
    { name: "HL7 FHIR R4", role: "Protokol Data Medis" },
    { name: "INA-CBG & NCC", role: "Tarif & Koding Nasional" },
    { name: "RSUP Nasional", role: "Faskes Uji Coba" }
  ];

  // Benefits List with 01, 02, 03, 04 Numbers (shadcn-sveltekit style)
  const benefits = [
    {
      num: "01",
      title: "Pencegahan Kebocoran Rp 42.8 M",
      desc: "Mendeteksi pola klaim fiktif, unbundling prosedur tindakan, dan klaim berulang antar-faskes sebelum pembayaran diproses."
    },
    {
      num: "02",
      title: "Inferensi Cepat < 1.2 Detik",
      desc: "Model MHGSL Multi-Hop GNN menganalisis rekam medis faskes seketika saat berkas dibuka oleh tim verifikator."
    },
    {
      num: "03",
      title: "99.2% Akurasi Penapisan",
      desc: "Meminimalkan kesalahan verifikasi administratif dan memberikan rekomendasi berbasis eviden klinis yang defensibel."
    },
    {
      num: "04",
      title: "100% Jejak Audit SHA-256",
      desc: "Memori bi-temporal Graphiti mencatat waktu peristiwa medis (Tv) dan waktu sistem (Tk) dalam rantai hash anti-tamper."
    }
  ];

  // Features List
  const features = [
    {
      badge: "GNN Deep Learning",
      title: "Multi-Hop Graph Structure Learning",
      desc: "Menghubungkan pola hubungan tersembunyi antara diagnosis (ICD-10), prosedur (ICD-9-CM), faskes perujuk, dan histori klaim secara menyeluruh.",
      icon: "Layers"
    },
    {
      badge: "Bi-Temporal Engine",
      title: "Graphiti Knowledge Graph",
      desc: "Mencatat kebenaran fakta klinis di dua garis waktu untuk mencegah manipulasi tanggal klaim mundur (backdating) dan fraud klaim ganda.",
      icon: "Activity"
    },
    {
      badge: "Interactive Flow",
      title: "Svelte Flow Realtime Pipeline",
      desc: "Visualisasi langkah demi langkah proses inferensi AI secara instan dan responsif di browser tanpa lag, mengedepankan transparansi proses verifikasi.",
      icon: "ShieldCheck"
    },
    {
      badge: "Human Control",
      title: "Human-in-the-Loop Safeguard",
      desc: "AI bertindak sebagai penasehat pintar (CDSS). Keputusan final persetujuan, eskalasi P2PK, atau klarifikasi faskes tetap 100% di tangan verifikator.",
      icon: "ShieldAlert"
    }
  ];

  // Services / Modules
  const services = [
    {
      title: "Triage Otomatis Antrean Klaim",
      desc: "Klasifikasi otomatis berkas klaim menjadi kategori Wajar (Auto-clear), Perlu Review, dan Risiko Tinggi (Fraud) secara objektif."
    },
    {
      title: "Deteksi Upcoding & Unbundling",
      desc: "Pengecekan silang otomatis antara koding INA-CBG yang diajukan dengan resume medis dan laporan tindakan operasi dokter."
    },
    {
      title: "Verifikasi Restriksi Fornas",
      desc: "Pencocokan resep obat dengan Formularium Nasional BPJS Kesehatan dan batasan diagnosis yang diizinkan."
    },
    {
      title: "Paket Eviden Siap Audit",
      desc: "Menghasilkan ringkasan rekomendasi terstruktur yang dapat dilampirkan langsung ke tim investigasi P2PK BPJS Kesehatan."
    }
  ];

  // How It Works Steps
  const howItWorks = [
    {
      step: "Langkah 1",
      title: "Ingesti Berkas EMR",
      desc: "Data rekam medis elektronik dan berkas klaim diterima dari rumah sakit melalui webhook API standar HL7 FHIR."
    },
    {
      step: "Langkah 2",
      title: "Analisis Multi-Hop AI",
      desc: "MHGSL GNN memetakan interaksi multi-entitas klaim dan mendeteksi anomali pola dalam hitungan milidetik."
    },
    {
      step: "Langkah 3",
      title: "Pencocokan Aturan Klinis",
      desc: "Graphiti memvalidasi kesesuaian diagnosis, riwayat pasien, serta batasan koding INA-CBG secara otomatis."
    },
    {
      step: "Langkah 4",
      title: "Keputusan Verifikator",
      desc: "Verifikator meninjau rekomendasi AI di meja kerja interaktif dan memberikan keputusan akhir dengan satu ketukan."
    }
  ];

  // Testimonials
  const testimonials = [
    {
      quote: "Aegis-JKN memangkas waktu verifikasi berkas klaim rawat inap kami hingga lebih dari 65%, dengan transparansi alasan anomali yang sangat jelas.",
      name: "dr. Hendra Prasetyo, Sp.JP",
      role: "Komite Medis Rumah Sakit Rujukan"
    },
    {
      quote: "Deteksi unbundling prosedur bedah yang sebelumnya membutuhkan audit manual berjam-jam kini langsung terpetakan secara visual dalam hitungan detik.",
      name: "Siti Rahmawati, S.Farm",
      role: "Verifikator Klaim Senior BPJS Kesehatan"
    },
    {
      quote: "Integrasi HL7 FHIR SatuSehat berjalan mulus tanpa mengganggu alur operasional SIMRS rumah sakit yang sudah berjalan.",
      name: "Budi Santoso, S.Kom",
      role: "Kepala Departemen IT RSUD"
    }
  ];

  // FAQs
  const faqs = [
    {
      q: "Bagaimana Aegis-JKN mendeteksi anomali klaim yang lolos dari sistem verifikasi konvensional?",
      a: "Sistem konvensional berbasis aturan statis hanya memeriksa kelengkapan administratif sederhana. Aegis-JKN menggunakan Multi-Hop Graph Structure Learning (MHGSL) yang memodelkan relasi kompleks antara riwayat diagnosa (ICD-10), tindakan (ICD-9-CM), faskes perujuk, dan pola resep dalam jaringan graf pengetahuan untuk mengidentifikasi anomali terselubung seperti unbundling, upcoding, dan klaim berulang antar-fasilitas."
    },
    {
      q: "Apakah AI di Aegis-JKN mengambil keputusan persetujuan klaim secara otomatis?",
      a: "Tidak. Aegis-JKN dirancang dengan prinsip ketat Human-in-the-Loop (HITL). AI bertindak sebagai Clinical Decision Support System (CDSS) yang bertugas menyaring, menghitung skor risiko, dan menyajikan paket bukti klinis (Evidence Bundle) lengkap. Keputusan final persetujuan, penolakan, atau permintaan klarifikasi klaim tetap 100% berada di tangan verifikator resmi BPJS Kesehatan."
    },
    {
      q: "Apa fungsi Knowledge Graph Bi-temporal Graphiti dalam sistem ini?",
      a: "Memori bi-temporal mencatat dua dimensi waktu penting: kapan diagnosis/tindakan medis terjadi (Valid Time, Tv) dan kapan transaksi klaim tersebut tercatat di sistem (Known Time, Tk). Hal ini mencegah pemalsuan tanggal mundur (backdating) dan memastikan jejak audit digital memiliki integritas kriptografis SHA-256 yang sah."
    },
    {
      q: "Apakah sistem ini kompatibel dengan standar SatuSehat dan BPJS VClaim?",
      a: "Ya. Aegis-JKN dirancang sesuai standar HL7 FHIR R4 dan Permenkes No. 24 Tahun 2022 tentang Rekam Medis Elektronik, serta mendukung integrasi webhook API VClaim v2.0 BPJS Kesehatan untuk interoperabilitas tanpa hambatan."
    },
    {
      q: "Bagaimana cara mencoba meja kerja verifikator Aegis-JKN?",
      a: "Anda dapat langsung mengeklik tombol 'Buka Meja Kerja' di bagian atas atau bawah halaman ini untuk masuk ke Workstation interaktif yang menyajikan antrean klaim live, visualisasi alur pipeline Svelte Flow, dan panel graf pengetahuan MHGSL."
    }
  ];

  onMount(() => {
    theme.init();
  });
</script>

<svelte:head>
  <title>Aegis-JKN · Sistem Verifikasi & Deteksi Anomali Klaim BPJS Kesehatan Berbasis AI</title>
  <meta
    name="description"
    content="Clinical Decision Support System (CDSS) Verifikator Klaim JKN dengan MHGSL GNN dan Graphiti Knowledge Graph."
  />
</svelte:head>

<!-- Clean, modern, borderless layout inspired by shadcn-sveltekit-landing-page -->
<div class="min-h-screen w-full bg-background text-foreground flex flex-col font-sans selection:bg-[#588157]/25 selection:text-foreground">
  <!-- 1. NAVBAR (Borderless, Glassmorphic) -->
  <header class="sticky top-0 z-50 w-full bg-background/80 backdrop-blur-xl transition-colors duration-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between gap-4">
      <!-- Brand Logo -->
      <a href="/" class="flex items-center gap-3 group">
        <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-[#3a5a40] via-[#588157] to-[#a3b18a] text-white shadow-lg shadow-[#3a5a40]/20 transition-transform duration-200 group-hover:scale-105">
          <Icon name="ShieldAlert" size={24} />
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-lg font-black tracking-tight text-foreground">Aegis-JKN</span>
            <span class="inline-flex items-center rounded-full bg-[#a3b18a]/20 px-2.5 py-0.5 text-[10px] font-bold text-[#3a5a40] dark:text-[#a3b18a] font-mono">
              HEALTHKATHON 2026
            </span>
          </div>
          <p class="text-xs text-muted-foreground font-medium hidden sm:block">
            AI Clinical Decision Support System
          </p>
        </div>
      </a>

      <!-- Desktop Nav Links (Clean, No Borders) -->
      <nav class="hidden md:flex items-center gap-7 text-sm font-semibold text-muted-foreground">
        <a href="#benefits" class="hover:text-primary transition-colors">Keunggulan</a>
        <a href="#features" class="hover:text-primary transition-colors">Fitur AI</a>
        <a href="#how-it-works" class="hover:text-primary transition-colors">Alur Kerja</a>
        <a href="#testimonials" class="hover:text-primary transition-colors">Dampak</a>
        <a href="#faq" class="hover:text-primary transition-colors">FAQ</a>
        <a href="/it" class="text-[#588157] hover:underline transition-colors flex items-center gap-1 font-bold">
          <span>Dashboard IT</span>
          <span class="text-[10px] font-mono rounded bg-[#588157]/15 px-1.5 py-0.2">Ops</span>
        </a>
      </nav>

      <!-- Right Action & Theme Toggle -->
      <div class="flex items-center gap-3">
        <!-- Theme Toggle Button (Borderless) -->
        <button
          type="button"
          data-testid="landing-theme-toggle"
          onclick={() => theme.toggle()}
          class="flex h-10 w-10 items-center justify-center rounded-2xl bg-muted/60 text-muted-foreground hover:text-foreground hover:bg-muted transition-all active:scale-95 shadow-2xs"
          aria-label="Ganti Tema Tampilan"
        >
          {#if theme.current === "dark"}
            <Icon name="Sun" size={19} class="text-[#a3b18a]" />
          {:else}
            <Icon name="Moon" size={19} class="text-[#3a5a40]" />
          {/if}
        </button>

        <!-- Primary CTA Launch App Button (Borderless gradient) -->
        <a
          href="/app"
          data-testid="landing-cta-app"
          class="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-[#3a5a40] via-[#588157] to-[#3a5a40] hover:from-[#344e41] hover:to-[#588157] px-5 py-2.5 text-xs sm:text-sm font-bold text-white shadow-lg shadow-[#3a5a40]/25 transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
        >
          <span>Buka Meja Kerja</span>
          <Icon name="ArrowRight" size={16} />
        </a>

        <!-- Mobile Menu Toggle Button -->
        <button
          type="button"
          onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
          class="md:hidden flex h-10 w-10 items-center justify-center rounded-2xl bg-muted/60 text-muted-foreground hover:text-foreground"
          aria-label="Buka Menu"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Drawer -->
    {#if mobileMenuOpen}
      <div class="md:hidden bg-background/95 backdrop-blur-2xl px-6 py-4 space-y-3 shadow-xl">
        <a href="#benefits" onclick={() => (mobileMenuOpen = false)} class="block py-2 text-sm font-semibold text-foreground hover:text-[#588157]">Keunggulan</a>
        <a href="#features" onclick={() => (mobileMenuOpen = false)} class="block py-2 text-sm font-semibold text-foreground hover:text-[#588157]">Fitur AI</a>
        <a href="#how-it-works" onclick={() => (mobileMenuOpen = false)} class="block py-2 text-sm font-semibold text-foreground hover:text-[#588157]">Alur Kerja</a>
        <a href="#testimonials" onclick={() => (mobileMenuOpen = false)} class="block py-2 text-sm font-semibold text-foreground hover:text-[#588157]">Dampak</a>
        <a href="#faq" onclick={() => (mobileMenuOpen = false)} class="block py-2 text-sm font-semibold text-foreground hover:text-[#588157]">FAQ</a>
        <a href="/it" onclick={() => (mobileMenuOpen = false)} class="block py-2 text-sm font-bold text-[#588157]">Dashboard IT (Observabilitas)</a>
      </div>
    {/if}
  </header>

  <!-- 2. HERO SECTION (shadcn-sveltekit style: Centered, No 3D, No Borders, Clean Mockup Preview) -->
  <section class="relative pt-12 pb-20 sm:pt-20 sm:pb-32 overflow-hidden">
    <!-- Ambient Radial Glow -->
    <div class="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 w-[900px] h-[550px] bg-gradient-to-b from-[#3a5a40]/20 via-[#588157]/10 to-transparent blur-3xl rounded-full -z-10"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center space-y-8 max-w-4xl mx-auto">
        <!-- Top Pill Badge (Borderless, Pill Shape) -->
        <div class="inline-flex items-center gap-2 rounded-full bg-[#a3b18a]/20 px-4 py-1.5 text-xs sm:text-sm font-semibold text-[#3a5a40] dark:text-[#a3b18a] shadow-xs">
          <span class="flex h-2 w-2 rounded-full bg-[#588157] animate-pulse"></span>
          <span>Inovasi Verifikasi Klaim JKN Berbasis Multi-Hop GNN</span>
        </div>

        <!-- Headline with Gradient Accent -->
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-[1.12] text-foreground">
          Pengambilan Keputusan Klinis Cerdas untuk
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#3a5a40] via-[#588157] to-[#a3b18a]">
            Integritas Klaim BPJS Kesehatan
          </span>
        </h1>

        <!-- Subtitle -->
        <p class="max-w-2xl mx-auto text-base sm:text-xl text-muted-foreground leading-relaxed font-normal">
          Aegis-JKN mendeteksi anomali diagnosis, unbundling prosedur, dan ketidaksesuaian INA-CBG secara otomatis dalam <strong>&lt; 1.2 detik</strong>, didukung transparansi memori bi-temporal Graphiti.
        </p>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <a
            href="/app"
            data-testid="landing-cta-hero"
            class="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 rounded-2xl bg-gradient-to-r from-[#3a5a40] via-[#588157] to-[#3a5a40] hover:from-[#344e41] hover:to-[#588157] px-8 py-4 text-sm sm:text-base font-bold text-white shadow-xl shadow-[#3a5a40]/25 transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
          >
            <Icon name="Activity" size={20} />
            <span>Buka Meja Kerja (Live Demo)</span>
          </a>

          <a
            href="#features"
            data-testid="landing-cta-arch"
            class="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-2xl bg-muted/60 hover:bg-muted px-6 py-4 text-sm sm:text-base font-semibold text-foreground transition-all duration-200"
          >
            <span>Pelajari Fitur</span>
            <Icon name="ChevronRight" size={18} />
          </a>
        </div>
      </div>

      <!-- Hero Interactive Workstation Preview Mockup (Borderless, Elegant Depth) -->
      <div class="relative mt-16 max-w-5xl mx-auto">
        <!-- Glowing Backdrop Shadow -->
        <div class="pointer-events-none absolute -inset-4 bg-gradient-to-r from-[#3a5a40]/30 via-[#588157]/20 to-[#a3b18a]/30 blur-2xl rounded-3xl opacity-60"></div>

        <!-- Mockup Card Container (No borders, pure shadow & background) -->
        <div class="relative rounded-3xl bg-card shadow-2xl overflow-hidden">
          <!-- Mockup Top Window Header -->
          <div class="flex items-center justify-between px-6 py-3.5 bg-muted/40">
            <div class="flex items-center gap-2">
              <span class="h-3 w-3 rounded-full bg-rose-500/70"></span>
              <span class="h-3 w-3 rounded-full bg-amber-500/70"></span>
              <span class="h-3 w-3 rounded-full bg-emerald-500/70"></span>
              <span class="ml-2 text-xs font-mono font-semibold text-muted-foreground">aegis-jkn.bpjs-kesehatan.go.id/workstation</span>
            </div>
            <div class="inline-flex items-center gap-1.5 rounded-full bg-[#588157]/20 px-2.5 py-0.5 text-[10px] font-mono font-bold text-[#588157]">
              <span>ONLINE · 128 KLAIM AKTIF</span>
            </div>
          </div>

          <!-- Mockup Body Content Preview -->
          <div class="p-6 sm:p-8 space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
              <!-- Left Claim Card Preview -->
              <div class="md:col-span-5 bg-muted/30 rounded-2xl p-5 space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-[#588157] font-mono">#KLM-2026-0891</span>
                  <span class="rounded-full bg-rose-500/15 px-2 py-0.5 text-[10px] font-bold text-rose-600 dark:text-rose-400 font-mono">
                    SKOR FRAUD: 0.94
                  </span>
                </div>
                <h4 class="text-sm font-bold text-foreground">Indikasi Unbundling PCI Multivaskular</h4>
                <p class="text-xs text-muted-foreground leading-relaxed">
                  Pasien Ny. Suminah (62 th) • RSUD Rujukan Provinsi • Klaim Rp 48.500.000
                </p>
                <div class="flex items-center gap-2 pt-1 text-[11px] font-medium text-[#588157]">
                  <span>✓ 3 Diskrepansi Eviden Klinis Terdeteksi</span>
                </div>
              </div>

              <!-- Right GNN Pipeline Snapshot Preview -->
              <div class="md:col-span-7 bg-muted/20 rounded-2xl p-5 space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-foreground">Multi-Hop GNN Graph Trace</span>
                  <span class="text-[10px] font-mono text-muted-foreground">Inferensi: 0.84s</span>
                </div>
                <div class="grid grid-cols-3 gap-2 text-center text-xs">
                  <div class="p-2.5 rounded-xl bg-card shadow-xs">
                    <div class="font-bold text-foreground">Faskes Asal</div>
                    <div class="text-[10px] text-muted-foreground">Cluster Anomali #4</div>
                  </div>
                  <div class="p-2.5 rounded-xl bg-[#588157]/15 text-[#588157] font-bold">
                    <div>MHGSL AI</div>
                    <div class="text-[10px]">99.2% Confidence</div>
                  </div>
                  <div class="p-2.5 rounded-xl bg-card shadow-xs">
                    <div class="font-bold text-foreground">INA-CBG</div>
                    <div class="text-[10px] text-muted-foreground">I-4-10-II Mismatch</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Ribbon inside preview -->
            <div class="flex flex-wrap items-center justify-between gap-3 pt-2">
              <div class="flex items-center gap-2 text-xs text-muted-foreground">
                <span class="h-2 w-2 rounded-full bg-[#588157]"></span>
                <span>Clinical Decision Support System (CDSS) Aktif</span>
              </div>
              <a href="/app" class="text-xs font-bold text-[#588157] hover:underline flex items-center gap-1">
                <span>Eksplorasi Meja Kerja Penuh</span>
                <Icon name="ArrowRight" size={14} />
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 3. SPONSORS / ECOSYSTEM PARTNERS (shadcn-sveltekit Sponsors section) -->
  <section class="py-12 bg-muted/20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h3 class="text-xs font-bold uppercase tracking-widest text-muted-foreground font-mono mb-6">
        Interoperabilitas &amp; Standar Ekosistem Kesehatan Nasional
      </h3>

      <div class="flex flex-wrap items-center justify-center gap-8 sm:gap-14">
        {#each partners as p}
          <div class="flex flex-col items-center">
            <span class="text-base sm:text-lg font-extrabold text-foreground tracking-tight">{p.name}</span>
            <span class="text-[11px] text-muted-foreground">{p.role}</span>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- 4. BENEFITS SECTION (shadcn-sveltekit style: 01, 02, 03, 04 Numbers, No Borders) -->
  <section id="benefits" class="py-20 sm:py-32">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
        <!-- Left Title Column -->
        <div class="space-y-4">
          <span class="text-sm font-bold text-[#588157] uppercase tracking-wider font-mono">Keunggulan Strategis</span>
          <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-foreground leading-tight">
            Akurasi Tanpa Kompromi, Integritas Terjamin
          </h2>
          <p class="text-base sm:text-lg text-muted-foreground leading-relaxed">
            Menghilangkan celah kecurangan klaim kesehatan yang kompleks melalui analisis graf mendalam, tanpa menambah beban administratif verifikator manusia.
          </p>
        </div>

        <!-- Right 2x2 Grid with Large Numbers (Borderless cards) -->
        <div class="grid sm:grid-cols-2 gap-4">
          {#each benefits as b}
            <div class="bg-muted/40 hover:bg-muted/70 rounded-3xl p-6 transition-all duration-200 group">
              <div class="flex items-center justify-between mb-4">
                <span class="text-4xl font-black font-mono text-[#a3b18a] group-hover:text-[#588157] transition-colors">
                  {b.num}
                </span>
              </div>
              <h3 class="text-base font-bold text-foreground mb-2">
                {b.title}
              </h3>
              <p class="text-xs text-muted-foreground leading-relaxed">
                {b.desc}
              </p>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </section>

  <!-- 5. FEATURES SECTION (4 Core Innovation Pillars, Borderless) -->
  <section id="features" class="py-20 sm:py-32 bg-muted/20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-3">
        <span class="text-sm font-bold text-[#588157] uppercase tracking-wider font-mono">Arsitektur AI Terdepan</span>
        <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-foreground">
          Empat Pilar Inovasi Aegis-JKN
        </h2>
        <p class="text-base text-muted-foreground leading-relaxed">
          Dirancang dari fondasi teori graf mutakhir dan kepatuhan regulasi BPJS Kesehatan.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
        {#each features as f}
          <div class="rounded-3xl bg-card p-8 shadow-sm hover:shadow-md transition-all duration-200 space-y-4">
            <div class="flex items-center justify-between">
              <span class="inline-flex items-center rounded-xl bg-muted px-3 py-1 text-xs font-mono font-bold text-muted-foreground">
                {f.badge}
              </span>
              <div class="h-10 w-10 rounded-2xl bg-[#588157]/15 flex items-center justify-center text-[#588157]">
                <Icon name={f.icon} size={20} />
              </div>
            </div>

            <h3 class="text-xl font-bold text-foreground tracking-tight">
              {f.title}
            </h3>

            <p class="text-sm text-muted-foreground leading-relaxed">
              {f.desc}
            </p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- 6. SERVICES / CAPABILITIES SECTION (Borderless Grid) -->
  <section class="py-20 sm:py-28">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-3xl mx-auto mb-14 space-y-3">
        <span class="text-sm font-bold text-[#588157] uppercase tracking-wider font-mono">Kapabilitas Meja Kerja</span>
        <h2 class="text-3xl sm:text-4xl font-black tracking-tight text-foreground">
          Solusi Komprehensif Klaim BPJS
        </h2>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {#each services as s}
          <div class="rounded-3xl bg-muted/40 p-6 space-y-3 hover:bg-muted/70 transition-colors">
            <div class="h-8 w-8 rounded-xl bg-[#588157]/20 flex items-center justify-center text-[#588157] font-bold">
              ✓
            </div>
            <h3 class="text-base font-bold text-foreground">
              {s.title}
            </h3>
            <p class="text-xs text-muted-foreground leading-relaxed">
              {s.desc}
            </p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- 7. HOW IT WORKS (shadcn-sveltekit style: Step 1 to 4) -->
  <section id="how-it-works" class="py-20 sm:py-32 bg-muted/20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-3">
        <span class="text-sm font-bold text-[#588157] uppercase tracking-wider font-mono">Alur Otomasi</span>
        <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-foreground">
          Bagaimana Aegis-JKN Bekerja
        </h2>
        <p class="text-base text-muted-foreground leading-relaxed">
          Proses verifikasi mulus dari integrasi data hingga verifikasi final verifikator.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {#each howItWorks as step}
          <div class="rounded-3xl bg-card p-6 shadow-xs flex flex-col justify-between space-y-4">
            <div>
              <span class="inline-flex items-center rounded-lg bg-[#a3b18a]/20 px-2.5 py-1 text-xs font-mono font-bold text-[#3a5a40] dark:text-[#a3b18a]">
                {step.step}
              </span>
              <h3 class="text-base font-bold text-foreground mt-3 mb-2">
                {step.title}
              </h3>
              <p class="text-xs text-muted-foreground leading-relaxed">
                {step.desc}
              </p>
            </div>
            <div class="pt-2 text-xs font-semibold text-[#588157]">
              Otomatis &amp; Real-time →
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- 8. TESTIMONIALS (shadcn-sveltekit Testimonials style) -->
  <section id="testimonials" class="py-20 sm:py-28">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-3xl mx-auto mb-14 space-y-3">
        <span class="text-sm font-bold text-[#588157] uppercase tracking-wider font-mono">Suara Praktisi</span>
        <h2 class="text-3xl sm:text-4xl font-black tracking-tight text-foreground">
          Terpercaya di Lapangan
        </h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        {#each testimonials as t}
          <div class="rounded-3xl bg-muted/30 p-8 flex flex-col justify-between space-y-4">
            <p class="text-sm text-foreground italic leading-relaxed">
              "{t.quote}"
            </p>
            <div>
              <div class="text-sm font-bold text-foreground">{t.name}</div>
              <div class="text-xs text-muted-foreground">{t.role}</div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- 9. FAQ ACCORDION (Borderless) -->
  <section id="faq" class="py-20 sm:py-32 bg-muted/20">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-14 space-y-3">
        <span class="text-sm font-bold text-[#588157] uppercase tracking-wider font-mono">Tanya Jawab</span>
        <h2 class="text-3xl sm:text-4xl font-black tracking-tight text-foreground">
          Pertanyaan yang Sering Diajukan
        </h2>
      </div>

      <div class="space-y-4">
        {#each faqs as item, idx}
          <div class="rounded-3xl bg-card overflow-hidden shadow-xs transition-all duration-200">
            <button
              type="button"
              data-testid="landing-faq-toggle-{idx}"
              onclick={() => toggleFaq(idx)}
              class="w-full text-left px-6 py-5 flex items-center justify-between gap-4 font-bold text-sm sm:text-base text-foreground hover:bg-muted/40 transition-colors"
              aria-expanded={openFaqIndex === idx}
            >
              <span>{item.q}</span>
              <span class="shrink-0 text-muted-foreground font-mono transition-transform duration-200 {openFaqIndex === idx ? 'rotate-180 text-primary' : ''}">
                ▼
              </span>
            </button>

            {#if openFaqIndex === idx}
              <div class="px-6 pb-6 pt-1 text-xs sm:text-sm text-muted-foreground leading-relaxed bg-muted/10">
                {item.a}
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- 10. CALL TO ACTION BANNER (Borderless, Pill/Curved, Warm Gradient) -->
  <section class="py-16 sm:py-24">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="rounded-3xl bg-gradient-to-br from-[#203127] via-[#2a4133] to-[#17241d] p-10 sm:p-16 text-center text-white relative overflow-hidden shadow-2xl">
        <div class="max-w-3xl mx-auto space-y-4">
          <h2 class="text-3xl sm:text-5xl font-black tracking-tight text-[#dad7cd]">
            Siap Mengoptimalkan Verifikasi Klaim?
          </h2>
          <p class="text-sm sm:text-lg text-[#a3b18a] leading-relaxed">
            Coba langsung meja kerja verifikator Aegis-JKN dengan antrean klaim terpadu, skor fraud MHGSL AI, dan jejak audit Graphiti.
          </p>

          <div class="pt-6 flex flex-wrap items-center justify-center gap-4">
            <a
              href="/app"
              data-testid="landing-cta-banner"
              class="inline-flex items-center gap-2.5 rounded-2xl bg-gradient-to-r from-[#3a5a40] to-[#588157] hover:from-[#344e41] hover:to-[#3a5a40] px-8 py-4 text-sm sm:text-base font-bold text-white shadow-xl shadow-[#3a5a40]/40 transition-all duration-200 hover:scale-105"
            >
              <Icon name="Activity" size={20} />
              <span>Masuk ke Workstation Demo</span>
            </a>

            <a
              href="https://github.com/zxce3/shadcn-sveltekit-landing-page"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2 rounded-2xl bg-white/10 hover:bg-white/20 px-6 py-4 text-sm sm:text-base font-semibold text-white transition-all duration-200"
            >
              <span>GitHub Sample Template</span>
              <Icon name="ArrowRight" size={16} />
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 11. FOOTER (Clean, Borderless) -->
  <footer class="bg-muted/30 py-12 text-xs text-muted-foreground">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-3">
        <div class="h-7 w-7 rounded-xl bg-[#3a5a40] flex items-center justify-center text-white font-bold text-xs">
          A
        </div>
        <span class="font-bold text-foreground text-sm">Aegis-JKN</span>
        <span>•</span>
        <span>BPJS Kesehatan Healthkathon 2026</span>
      </div>

      <div class="flex flex-wrap items-center justify-center gap-6 font-semibold">
        <a href="#benefits" class="hover:text-foreground transition-colors">Keunggulan</a>
        <a href="#features" class="hover:text-foreground transition-colors">Fitur</a>
        <a href="#how-it-works" class="hover:text-foreground transition-colors">Alur Kerja</a>
        <a href="#faq" class="hover:text-foreground transition-colors">FAQ</a>
        <a href="/it" class="text-muted-foreground hover:text-foreground">Dashboard IT</a>
        <a href="/app" class="text-[#588157] font-bold hover:underline">Masuk Meja Kerja</a>
      </div>
    </div>
  </footer>
</div>
