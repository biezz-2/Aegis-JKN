<script lang="ts">
  import FlowCanvas from '$lib/components/FlowCanvas.svelte';
  import Button from '$lib/components/ui/button.svelte';
  import Card from '$lib/components/ui/card.svelte';
  import CardContent from '$lib/components/ui/card-content.svelte';
  import CardDescription from '$lib/components/ui/card-description.svelte';
  import CardHeader from '$lib/components/ui/card-header.svelte';
  import CardTitle from '$lib/components/ui/card-title.svelte';
  import { ArrowRight, Zap, Shield, Database } from 'lucide-svelte';
  import { claims, SOURCE_DATASET_HASH, SOURCE_RECORD_COUNT, formatCurrency } from '@/lib/claims';

  /* Angka di bawah dihitung dari dataset sintetis yang tertanam di repo —
     bukan angka pemasaran. Lihat claims.ts untuk sumber tunggalnya. */
  const total = claims.length;
  const byStatus = (status: 'auto_clear' | 'review' | 'escalate') =>
    claims.filter((claim) => claim.triageStatus === status);

  const autoClear = byStatus('auto_clear');
  const review = byStatus('review');
  const escalate = byStatus('escalate');

  const totalValue = claims.reduce((sum, claim) => sum + claim.claimedAmount, 0);
  const escalateValue = escalate.reduce((sum, claim) => sum + claim.claimedAmount, 0);
  const syndromes = new Set(claims.map((claim) => claim.syndromeId).filter(Boolean));
  const contradictions = claims.filter((claim) => claim.narrativeContradiction);
  const faskes = new Set(claims.map((claim) => claim.hospital));

  const meanScore = (items: typeof claims) =>
    items.reduce((sum, claim) => sum + claim.fraudScore, 0) / items.length;

  const stats = [
    { label: 'Klaim dalam dataset', value: String(total), sub: 'sintetis, 28 field per klaim' },
    { label: 'Antrean eskalasi', value: String(escalate.length), sub: `${((escalate.length / total) * 100).toFixed(0)}% dari total klaim` },
    { label: 'Sindikat teridentifikasi', value: String(syndromes.size), sub: 'pola berulang lintas faskes' },
    { label: 'Nilai klaim tereskalasi', value: formatCurrency(escalateValue), sub: `dari ${formatCurrency(totalValue)} total` }
  ];

  const features = [
    {
      icon: Zap,
      title: 'Triase tiga tingkat',
      description:
        'Aturan deterministik, model tabular, lalu graph convolution. Klaim berisiko rendah diteruskan otomatis; sumber daya manusia hanya untuk anomali.',
      points: [
        `Tier-1 aturan <50 ms — ${autoClear.length} klaim lolos otomatis`,
        'Tier-2 XGBoost 10 fitur bersih',
        'Tier-3 GCN heterograf'
      ]
    },
    {
      icon: Shield,
      title: 'Keputusan tetap pada manusia',
      description:
        'AI memberi rekomendasi, keputusan akhir ada pada verifikator. Jejak audit append-only dengan rantai hash SHA-256, dan Safe-Mode otomatis bila override melonjak.',
      points: [
        'Tiga aksi verifikator: konfirmasi, override, eskalasi',
        'Alasan wajib pada setiap override',
        'Safe-Mode saat override >30% per 24 jam'
      ]
    },
    {
      icon: Database,
      title: 'Jejak audit yang bisa ditelusuri',
      description:
        'Setiap klaim memuat bukti klinis, kontribusi tiga saluran graph, dan alasan penentuan antrean — sehingga keputusan dapat direproduksi, bukan sekadar percaya.',
      points: [
        'Bukti SHAP disajikan sebagai prosa, bukan angka karangan',
        'Hash dataset tertanam di repositori',
        'Tanpa panggilan LLM eksternal'
      ]
    }
  ];
</script>

<svelte:head>
  <title>Dashboard Verifikator Aegis-JKN</title>
  <meta
    name="description"
    content="Dashboard verifikator internal Aegis-JKN untuk telaah klaim JKN: triase tiga tingkat, bukti XAI, dan jejak audit append-only."
  />
</svelte:head>

<div class="min-h-screen bg-background">
  <!-- Hero -->
  <div class="relative bg-gradient-to-b from-slate-950 to-slate-900 text-white overflow-hidden">
    <div class="absolute inset-0 bg-[radial-gradient(at_top_right,#3b82f610_0%,transparent_50%)] pointer-events-none"></div>

    <div class="container mx-auto px-4 py-24 relative z-10">
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <div class="space-y-8">
          <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full border border-white/20">
            <div class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium tracking-wider">DASHBOARD VERIFIKATOR · TOOL INTERNAL</span>
          </div>

          <h1 class="text-6xl lg:text-7xl font-bold tracking-tighter leading-none">
            Aegis-JKN
            <span class="bg-gradient-to-r from-blue-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent">
              Verifikator
            </span>
          </h1>

          <p class="text-xl text-slate-400 max-w-lg">
            Antarmuka telaah untuk <span class="text-white font-semibold">fraud intelligence dan clinical
            decision support</span> klaim JKN. AI memberi rekomendasi, keputusan akhir ada pada verifikator.
          </p>

          <div class="flex items-center gap-4">
            <Button href="/demo" size="lg" class="bg-white text-slate-900 hover:bg-white/90 text-lg px-8 rounded-xl shadow-2xl shadow-blue-500/30">
              Buka Dashboard
              <ArrowRight class="ml-2 h-5 w-5" />
            </Button>

            <Button href="/demo" size="lg" variant="outline" class="border-white/30 text-white hover:bg-white/10 rounded-xl">
              Lihat Antrean Klaim
            </Button>
          </div>

          <div class="flex flex-wrap items-center gap-8 text-sm">
            <div>
              <div class="font-medium">{SOURCE_RECORD_COUNT} klaim</div>
              <div class="text-slate-400">dataset sintetis, {SOURCE_DATASET_HASH.slice(0, 12)}…</div>
            </div>

            <div class="h-8 w-px bg-white/20"></div>

            <div>
              <div class="font-medium">{faskes.size} faskes · {syndromes.size} sindikat</div>
              <div class="text-emerald-400">{contradictions.length} klaim dengan kontradiksi narasi</div>
            </div>
          </div>
        </div>

        <div class="relative">
          <div class="absolute -inset-10 bg-gradient-to-br from-blue-500/20 via-cyan-500/20 to-emerald-500/20 rounded-[4rem] -rotate-6"></div>

          <div class="relative bg-slate-900/70 backdrop-blur-xl border border-white/10 rounded-3xl p-2 shadow-2xl shadow-black/50">
            <FlowCanvas />
          </div>

          <div class="absolute -top-4 -left-4 bg-slate-900 border border-white/10 rounded-2xl p-4 max-w-[240px]">
            <div class="flex items-center gap-3">
              <div class="text-emerald-400">
                <Shield class="h-8 w-8" />
              </div>
              <div>
                <div class="font-semibold text-sm">Audit Trail Immutable</div>
                <div class="text-xs text-slate-400">Append-only, hash chaining SHA-256</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Angka dari dataset -->
  <div class="container mx-auto px-4 -mt-10 relative z-10">
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {#each stats as stat (stat.label)}
        <div class="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-xl">
          <div class="text-xs uppercase tracking-[0.16em] text-slate-500">{stat.label}</div>
          <div class="mt-2 text-2xl font-bold tracking-tight text-slate-100">{stat.value}</div>
          <div class="mt-1 text-xs text-slate-500">{stat.sub}</div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Fitur -->
  <div class="container mx-auto px-4 py-24">
    <div class="text-center mb-16">
      <div class="uppercase text-blue-400 text-sm tracking-[3px] font-mono mb-3">ALUR KERJA</div>
      <h2 class="text-5xl font-bold tracking-tight">Dari anomali menjadi keputusan yang dapat diaudit</h2>
      <p class="text-slate-400 mt-4 max-w-2xl mx-auto">
        Setiap klaim yang mencapai antrean review membawa bukti: skor fraud, kontribusi tiga kanal graph,
        sinyal SHAP dalam bentuk prosa, dan alasan klinis penentuannya.
      </p>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      {#each features as feature (feature.title)}
        <Card class="group hover:border-blue-500/30 transition-all duration-300 bg-slate-900/50 border-slate-800">
          <CardHeader>
            <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <feature.icon class="h-7 w-7 text-white" />
            </div>
            <CardTitle>{feature.title}</CardTitle>
            <CardDescription class="text-slate-400">{feature.description}</CardDescription>
          </CardHeader>
          <CardContent>
            <ul class="space-y-3 text-sm">
              {#each feature.points as point (point)}
                <li class="flex items-start gap-2 text-slate-300">
                  <span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-400"></span>
                  <span>{point}</span>
                </li>
              {/each}
            </ul>
          </CardContent>
        </Card>
      {/each}
    </div>
  </div>

  <!-- Distribusi antrean -->
  <div class="container mx-auto px-4 pb-24">
    <div class="rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
      <div class="flex flex-wrap items-baseline justify-between gap-3">
        <h2 class="text-2xl font-bold tracking-tight">Distribusi antrean pada dataset</h2>
        <span class="text-xs uppercase tracking-[0.16em] text-slate-500">Rekomendasi sistem, bukan vonis</span>
      </div>
      <p class="mt-3 max-w-3xl text-slate-400 text-sm">
        Antrean Hijau adalah rekomendasi sistem untuk meloloskan klaim lebih cepat; antrean Kuning dan Merah
        menunggu penilaian verifikator. Sebarannya di bawah dihitung langsung dari {SOURCE_RECORD_COUNT} klaim.
      </p>

      <div class="mt-8 space-y-5">
        {#each [{ label: 'Auto-clear', items: autoClear, tone: 'text-emerald-400', bar: 'bg-emerald-400' }, { label: 'Review', items: review, tone: 'text-amber-300', bar: 'bg-amber-300' }, { label: 'Escalate', items: escalate, tone: 'text-red-400', bar: 'bg-red-400' }] as row (row.label)}
          <div>
            <div class="flex items-baseline justify-between text-sm">
              <span class="text-slate-300">{row.label}</span>
              <span class="text-slate-500">
                {row.items.length} klaim
                <span class="font-mono">({meanScore(row.items).toFixed(3)})</span>
                · {formatCurrency(row.items.reduce((sum, claim) => sum + claim.claimedAmount, 0))}
              </span>
            </div>
            <div class="mt-1.5 h-2 overflow-hidden rounded-full bg-slate-800">
              <div class="h-full rounded-full {row.bar}" style="width: {(row.items.length / total) * 100}%"></div>
            </div>
          </div>
        {/each}
      </div>

      <p class="mt-6 text-xs text-slate-500">
        Angka dalam tanda kurung adalah rata-rata skor fraud pada antrean tersebut. Skor 0–1, makin tinggi makin
        perlu ditelaah; bukan probabilitas dan bukan vonis.
      </p>
    </div>
  </div>

  <!-- CTA -->
  <div class="bg-gradient-to-r from-blue-600 via-cyan-600 to-emerald-600 py-16">
    <div class="container mx-auto px-4 text-center">
      <h3 class="text-4xl font-bold mb-4">Masuk ke antrean klaim</h3>
      <p class="text-lg text-white/80 mb-8 max-w-md mx-auto">
        Pilih klaim, telaah bukti klinisnya, lalu catat keputusan Anda pada jejak audit.
      </p>

      <Button href="/demo" size="lg" class="bg-white text-slate-900 text-lg px-10 rounded-2xl hover:scale-105 transition-transform shadow-2xl">
        Buka Dashboard Verifikator
        <ArrowRight class="ml-3" />
      </Button>
    </div>
  </div>
</div>
