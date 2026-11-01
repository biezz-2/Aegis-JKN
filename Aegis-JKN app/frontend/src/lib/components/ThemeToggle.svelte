<script lang="ts">
  import { theme } from "$lib/stores/theme.svelte";
  import { lang } from "$lib/stores/lang.svelte";
  import Icon from "./Icon.svelte";
</script>

<button
  type="button"
  onclick={() => theme.toggle()}
  class="relative inline-flex h-9 w-9 items-center justify-center rounded-lg border border-border/80 bg-background/50 hover:bg-muted text-foreground transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary/40"
  aria-label={theme.current === "dark" ? lang.t.themeLight : lang.t.themeDark}
  title={theme.current === "dark" ? lang.t.themeLight : lang.t.themeDark}
>
  {#if theme.current === "dark"}
    <Icon name="Sun" size={17} class="text-amber-400 animate-count-up" />
  {:else}
    <Icon name="Moon" size={17} class="text-emerald-700 animate-count-up" />
  {/if}
</button>
