<script lang="ts">
  import FlowCanvas from '$lib/components/FlowCanvas.svelte';
  import Button from '$lib/components/ui/button.svelte';
  import Card from '$lib/components/ui/card.svelte';
  import CardContent from '$lib/components/ui/card-content.svelte';
  import CardDescription from '$lib/components/ui/card-description.svelte';
  import CardHeader from '$lib/components/ui/card-header.svelte';
  import CardTitle from '$lib/components/ui/card-title.svelte';
  import { ArrowRight, Zap, Shield, Database } from 'lucide-svelte';
</script>

<div class="min-h-screen bg-background">
  <!-- Premium Hero -->
  <div class="relative bg-gradient-to-b from-slate-950 to-slate-900 text-white overflow-hidden">
    <div class="absolute inset-0 bg-[radial-gradient(at_top_right,#3b82f610_0%,transparent_50%)] pointer-events-none"></div>

    <div class="container mx-auto px-4 py-24 relative z-10">
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <div class="space-y-8">
          <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md px-4 py-2 rounded-full border border-white/20">
            <div class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
            <span class="text-sm font-medium tracking-wider">PREMIUM DASHBOARD</span>
          </div>

          <h1 class="text-7xl lg:text-8xl font-bold tracking-tighter leading-none">
            Aegis<br>JKN
            <span class="bg-gradient-to-r from-blue-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent">Flow</span>
          </h1>

          <p class="text-xl text-slate-400 max-w-lg">
            Platform pengelolaan klaim JKN terdepan.
            <span class="text-white font-semibold">SvelteFlow powered</span> dengan desain premium berbasis AI.
          </p>

          <div class="flex items-center gap-4">
            <Button href="/demo" size="lg" class="bg-white text-slate-900 hover:bg-white/90 text-lg px-8 rounded-xl shadow-2xl shadow-blue-500/30">
              Mulai Trial Gratis
              <ArrowRight class="ml-2 h-5 w-5" />
            </Button>

            <Button href="/demo" size="lg" variant="outline" class="border-white/30 text-white hover:bg-white/10 rounded-xl">
              Lihat Demo
            </Button>
          </div>

          <div class="flex items-center gap-8 text-sm">
            <div class="flex items-center gap-2">
              <div class="flex -space-x-2">
                <div class="w-6 h-6 rounded-full border-2 border-slate-900 overflow-hidden">
                  <img src="https://i.pravatar.cc/64?img=32" alt="" class="w-full h-full object-cover" />
                </div>
                <div class="w-6 h-6 rounded-full border-2 border-slate-900 overflow-hidden">
                  <img src="https://i.pravatar.cc/64?img=33" alt="" class="w-full h-full object-cover" />
                </div>
              </div>
              <div>
                <div class="font-medium">+2.4K dokter</div>
                <div class="text-slate-400">aktif hari ini</div>
              </div>
            </div>

            <div class="h-8 w-px bg-white/20"></div>

            <div>
              <div class="font-medium">99.7% uptime</div>
              <div class="text-emerald-400">SLA terjamin</div>
            </div>
          </div>
        </div>

        <div class="relative">
          <div class="absolute -inset-10 bg-gradient-to-br from-blue-500/20 via-cyan-500/20 to-emerald-500/20 rounded-[4rem] -rotate-6"></div>

          <div class="relative bg-slate-900/70 backdrop-blur-xl border border-white/10 rounded-3xl p-2 shadow-2xl shadow-black/50">
            <FlowCanvas />
          </div>

          <div class="absolute -bottom-4 -right-4 bg-slate-900 border border-white/10 rounded-2xl p-4 max-w-[240px]">
            <div class="flex items-center gap-3">
              <div class="text-emerald-400">
                <Shield class="h-8 w-8" />
              </div>
              <div>
                <div class="font-semibold text-sm">End-to-End Encryption</div>
                <div class="text-xs text-slate-400">AES-256-GCM + Zero-Knowledge</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Premium Features -->
  <div class="container mx-auto px-4 py-24">
    <div class="text-center mb-16">
      <div class="uppercase text-blue-400 text-sm tracking-[3px] font-mono mb-3">FITUR UNGGULAN</div>
      <h2 class="text-5xl font-bold tracking-tight">Desain premium untuk klinik modern</h2>
      <p class="text-slate-400 mt-4 max-w-md mx-auto">SvelteFlow engine yang dioptimalkan untuk performa tinggi dan UI yang premium.</p>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      <Card class="group hover:border-blue-500/30 transition-all duration-300 bg-slate-900/50 border-slate-800">
        <CardHeader>
          <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Zap class="h-7 w-7 text-white" />
          </div>
          <CardTitle>Real-time Flow</CardTitle>
          <CardDescription class="text-slate-400">SvelteFlow dengan drag & drop yang mulus, support edge animation dan custom node.</CardDescription>
        </CardHeader>
        <CardContent>
          <ul class="space-y-3 text-sm">
            <li class="flex items-center gap-2 text-emerald-400">✓ <span>Auto-layout intelligent</span></li>
            <li class="flex items-center gap-2 text-emerald-400">✓ <span>Edge animation premium</span></li>
            <li class="flex items-center gap-2 text-emerald-400">✓ <span>Custom node builder</span></li>
          </ul>
        </CardContent>
      </Card>

      <Card class="group hover:border-blue-500/30 transition-all duration-300 bg-slate-900/50 border-slate-800">
        <CardHeader>
          <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-emerald-500 to-cyan-500 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Shield class="h-7 w-7 text-white" />
          </div>
          <CardTitle>Keamanan Level Enterprise</CardTitle>
          <CardDescription class="text-slate-400">RBAC, audit trail, dan zero-knowledge untuk data JKN yang sensitif.</CardDescription>
        </CardHeader>
        <CardContent>
          <ul class="space-y-3 text-sm">
            <li class="flex items-center gap-2 text-emerald-400">✓ <span>End-to-end encryption</span></li>
            <li class="flex items-center gap-2 text-emerald-400">✓ <span>Single-use blind token</span></li>
            <li class="flex items-center gap-2 text-emerald-400">✓ <span>Immutable audit log</span></li>
          </ul>
        </CardContent>
      </Card>

      <Card class="group hover:border-blue-500/30 transition-all duration-300 bg-slate-900/50 border-slate-800">
        <CardHeader>
          <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Database class="h-7 w-7 text-white" />
          </div>
          <CardTitle>Integrasi AI</CardTitle>
          <CardDescription class="text-slate-400">GraphRAG + LLM gateway untuk analisis klaim otomatis.</CardDescription>
        </CardHeader>
        <CardContent>
          <ul class="space-y-3 text-sm">
            <li class="flex items-center gap-2 text-emerald-400">✓ <span>ReAct multi-turn</span></li>
            <li class="flex items-center gap-2 text-emerald-400">✓ <span>Ontology extraction</span></li>
            <li class="flex items-center gap-2 text-emerald-400">✓ <span>Real-time insight</span></li>
          </ul>
        </CardContent>
      </Card>
    </div>
  </div>

  <!-- CTA -->
  <div class="bg-gradient-to-r from-blue-600 via-cyan-600 to-emerald-600 py-16">
    <div class="container mx-auto px-4 text-center">
      <h3 class="text-4xl font-bold mb-4">Siap melangkah ke era digital klinik?</h3>
      <p class="text-lg text-white/80 mb-8 max-w-md mx-auto">Integrasikan SvelteFlow ke sistem JKN Anda dalam hitungan menit.</p>

      <Button href="/demo" size="lg" class="bg-white text-slate-900 text-lg px-10 rounded-2xl hover:scale-105 transition-transform shadow-2xl">
        Mulai Integrasi Sekarang
        <ArrowRight class="ml-3" />
      </Button>
    </div>
  </div>
</div>