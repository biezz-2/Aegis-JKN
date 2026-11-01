<script lang="ts">
  import { useSvelteFlow, Panel } from "@xyflow/svelte";
  import Icon from "./Icon.svelte";

  let {
    onReset,
    onFit
  }: {
    onReset?: () => void;
    onFit?: () => void;
  } = $props();

  const { fitView, setViewport, zoomIn, zoomOut } = useSvelteFlow();

  async function handleFitView() {
    if (onFit) {
      onFit();
    } else {
      await fitView({ padding: 0.15, duration: 400 });
    }
  }

  async function handleResetView() {
    if (onReset) {
      onReset();
    } else {
      await setViewport({ x: 20, y: 40, zoom: 0.85 }, { duration: 400 });
    }
  }

  async function handleZoomIn() {
    await zoomIn({ duration: 200 });
  }

  async function handleZoomOut() {
    await zoomOut({ duration: 200 });
  }
</script>

<Panel position="bottom-right" class="m-3">
  <div class="flex items-center gap-1.5 p-1 rounded-xl border border-border bg-card/95 backdrop-blur-md shadow-lg">
    <button
      type="button"
      onclick={handleZoomIn}
      class="flex items-center justify-center w-8 h-8 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted/80 active:scale-95 transition-all"
      title="Perbesar Canvas (Zoom In)"
      aria-label="Perbesar Canvas"
    >
      <span class="text-sm font-bold font-mono">+</span>
    </button>

    <button
      type="button"
      onclick={handleZoomOut}
      class="flex items-center justify-center w-8 h-8 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted/80 active:scale-95 transition-all"
      title="Perkecil Canvas (Zoom Out)"
      aria-label="Perkecil Canvas"
    >
      <span class="text-sm font-bold font-mono">-</span>
    </button>

    <div class="h-4 w-px bg-border my-auto"></div>

    <button
      type="button"
      onclick={handleFitView}
      class="flex items-center gap-1.5 px-2.5 h-8 rounded-lg text-xs font-semibold text-muted-foreground hover:text-foreground hover:bg-muted/80 active:scale-95 transition-all"
      title="Pusatkan dan sesuaikan seluruh diagram dengan layar (Fit View)"
    >
      <Icon name="Activity" size={13} class="text-primary" />
      <span>Fit View</span>
    </button>

    <button
      type="button"
      onclick={handleResetView}
      class="flex items-center gap-1.5 px-2.5 h-8 rounded-lg text-xs font-semibold text-muted-foreground hover:text-foreground hover:bg-muted/80 active:scale-95 transition-all"
      title="Kembalikan orientasi dan posisi viewport ke awal (Reset View)"
    >
      <Icon name="RotateCcw" size={13} class="text-amber-500" />
      <span>Reset View</span>
    </button>
  </div>
</Panel>
