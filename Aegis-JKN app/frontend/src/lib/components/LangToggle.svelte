<script lang="ts">
  import { lang } from "$lib/stores/lang.svelte";
</script>

<div class="inline-flex items-center rounded-lg border border-border/80 bg-background/50 p-0.5 text-xs font-semibold shadow-xs">
  <button
    type="button"
    onclick={() => lang.setLang("id")}
    class="rounded-md px-2 py-1 transition-all duration-150 {lang.current === 'id' ? 'bg-primary text-primary-foreground shadow-xs' : 'text-muted-foreground hover:text-foreground'}"
    aria-label="Bahasa Indonesia"
  >
    ID
  </button>
  <button
    type="button"
    onclick={() => lang.setLang("en")}
    class="rounded-md px-2 py-1 transition-all duration-150 {lang.current === 'en' ? 'bg-primary text-primary-foreground shadow-xs' : 'text-muted-foreground hover:text-foreground'}"
    aria-label="English Language"
  >
    EN
  </button>
</div>
