<script lang="ts">
  import Icon from "./Icon.svelte";
  import { shortcutsModal } from "$lib/stores/shortcuts.svelte";

  const sections = [
    {
      title: "Navigasi Tab Detail",
      items: [
        { key: "1", label: "Tab Bukti EMR (Rekam Medis)" },
        { key: "2", label: "Tab Pembuktian AI & SHAP" },
        { key: "3", label: "Tab Pipeline Flow (Svelte Flow)" },
        { key: "4", label: "Tab Knowledge Graph (Graphiti)" },
      ],
    },
    {
      title: "Triase Antrean Klaim",
      items: [
        { key: "J / ↓", label: "Pilih Klaim Berikutnya" },
        { key: "K / ↑", label: "Pilih Klaim Sebelumnya" },
        { key: "Tab", label: "Pindah Fokus Elemen Berikutnya" },
        { key: "Shift + Tab", label: "Pindah Fokus Elemen Sebelumnya" },
      ],
    },
    {
      title: "Aksi Human-In-The-Loop (HITL)",
      items: [
        { key: "A", label: "Setujui Klaim (Approve)" },
        { key: "C", label: "Klarifikasi RS (Clarify)" },
        { key: "E", label: "Eskalasi ke Anti-Fraud P2PK" },
      ],
    },
    {
      title: "Sistem & Tampilan",
      items: [
        { key: "T", label: "Toggle Tema (Gelap / Terang)" },
        { key: "M", label: "Bisukan / Aktifkan Audio Feedback" },
        { key: "?", label: "Buka / Tutup Bantuan Pintasan" },
        { key: "Esc", label: "Tutup Dialog / Modal Terbuka" },
      ],
    },
  ];
</script>

<!-- Floating trigger button in bottom right -->
<div class="fixed bottom-4 right-4 z-40">
  <button
    type="button"
    onclick={() => shortcutsModal.toggleHelp()}
    class="inline-flex h-9 items-center gap-1.5 rounded-lg border border-border/80 bg-card/90 px-3 py-1.5 text-xs font-semibold text-muted-foreground shadow-md backdrop-blur-sm transition-all duration-200 hover:bg-muted hover:text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
    aria-label="Pintasan Keyboard (Tekan ?)"
    title="Pintasan Keyboard (Tekan ?)"
  >
    <Icon name="Keyboard" size={15} class="text-primary" />
    <span class="hidden sm:inline">Pintasan</span>
    <kbd class="rounded border border-border bg-muted/80 px-1.5 py-0.2 font-mono text-[10px] font-bold text-foreground">?</kbd>
  </button>
</div>

{#if shortcutsModal.helpOpen}
  <div
    role="dialog"
    aria-modal="true"
    tabindex="-1"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4"
    onclick={(e) => {
      if (e.target === e.currentTarget) shortcutsModal.closeHelp();
    }}
    onkeydown={(e) => {
      if (e.key === "Escape") shortcutsModal.closeHelp();
    }}
  >
    <div class="relative w-full max-w-md rounded-2xl border border-border bg-card p-6 shadow-2xl text-card-foreground animate-count-up max-h-[90vh] overflow-y-auto scrollbar-thin">
      <!-- Header -->
      <div class="flex items-center justify-between pb-3.5 border-b border-border">
        <div class="flex items-center gap-2.5">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 text-primary">
            <Icon name="Keyboard" size={18} />
          </div>
          <div>
            <h3 class="font-bold text-sm tracking-tight text-foreground">Pintasan Keyboard Verifikator</h3>
            <p class="text-[11px] text-muted-foreground">Kendali penuh workstation tanpa mouse</p>
          </div>
        </div>
        <button
          type="button"
          onclick={() => shortcutsModal.closeHelp()}
          class="rounded-lg p-1.5 hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
          aria-label="Tutup dialog pintasan"
        >
          <Icon name="X" size={16} />
        </button>
      </div>

      <!-- Shortcut Sections -->
      <div class="mt-4 space-y-4">
        {#each sections as sec}
          <div class="space-y-2">
            <h4 class="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
              {sec.title}
            </h4>
            <div class="rounded-xl border border-border/70 bg-muted/20 p-2.5 space-y-2">
              {#each sec.items as item}
                <div class="flex items-center justify-between text-xs">
                  <span class="text-foreground/90 font-medium">{item.label}</span>
                  <kbd class="inline-flex items-center justify-center rounded-md border border-border bg-card px-2 py-0.5 font-mono text-[11px] font-bold text-foreground shadow-2xs">
                    {item.key}
                  </kbd>
                </div>
              {/each}
            </div>
          </div>
        {/each}
      </div>

      <!-- Footer hint -->
      <div class="mt-5 pt-3.5 border-t border-border flex items-center justify-between text-[11px] text-muted-foreground">
        <span>Tekan <kbd class="px-1.5 py-0.5 rounded border border-border bg-muted font-mono font-bold text-foreground">Esc</kbd> untuk menutup</span>
        <span class="text-primary font-medium">Aegis-JKN Workstation</span>
      </div>
    </div>
  </div>
{/if}
