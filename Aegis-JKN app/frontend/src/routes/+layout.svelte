<script lang="ts">
  import "../app.css";
  import { onMount } from "svelte";
  import { theme } from "$lib/stores/theme.svelte";
  import { dashboard } from "$lib/stores/dashboard.svelte";
  import { shortcutsModal } from "$lib/stores/shortcuts.svelte";
  import ShortcutsHint from "$lib/components/ShortcutsHint.svelte";
  import type { Claim } from "$lib/types";

  let { children } = $props();

  onMount(() => {
    theme.init();
    if (import.meta.env.DEV) {
      void import("../reticle-dev");
    }
    function handleKeydown(e: KeyboardEvent) {
      // Don't intercept when user is typing in inputs or textareas
      const target = e.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === "INPUT" ||
          target.tagName === "TEXTAREA" ||
          target.isContentEditable)
      ) {
        return;
      }

      // Don't interfere with Ctrl / Meta combinations
      if (e.ctrlKey || e.metaKey) return;

      // Global Help Dialog (? or Shift+/)
      if (e.key === "?" || (e.key === "/" && e.shiftKey)) {
        e.preventDefault();
        shortcutsModal.toggleHelp();
        return;
      }

      // Close Help Dialog on Escape
      if (e.key === "Escape") {
        if (shortcutsModal.helpOpen) {
          e.preventDefault();
          shortcutsModal.closeHelp();
          return;
        }
      }

      // Switch Tabs: 1 = EMR, 2 = AI, 3 = Flow, 4 = Knowledge Graph
      if (e.key === "1") {
        e.preventDefault();
        dashboard.setDetailTab("emr");
        return;
      }
      if (e.key === "2") {
        e.preventDefault();
        dashboard.setDetailTab("ai");
        return;
      }
      if (e.key === "3") {
        e.preventDefault();
        dashboard.setDetailTab("flow");
        return;
      }
      if (e.key === "4") {
        e.preventDefault();
        dashboard.setDetailTab("graphiti");
        return;
      }

      // Claim Queue Navigation: j / ArrowDown (Next), k / ArrowUp (Previous)
      if (e.key === "j" || e.key === "ArrowDown") {
        const list = dashboard.filteredClaims;
        if (list.length > 0) {
          const idx = list.findIndex((c: Claim) => c.id === dashboard.selectedClaimId);
          if (idx < list.length - 1) {
            e.preventDefault();
            dashboard.selectClaim(list[idx + 1].id);
          }
        }
        return;
      }
      if (e.key === "k" || e.key === "ArrowUp") {
        const list = dashboard.filteredClaims;
        if (list.length > 0) {
          const idx = list.findIndex((c: Claim) => c.id === dashboard.selectedClaimId);
          if (idx > 0) {
            e.preventDefault();
            dashboard.selectClaim(list[idx - 1].id);
          }
        }
        return;
      }

      // Theme toggle: T
      if (e.key.toLowerCase() === "t" && !e.altKey) {
        e.preventDefault();
        theme.toggle();
        return;
      }
    }

    window.addEventListener("keydown", handleKeydown);
    return () => {
      window.removeEventListener("keydown", handleKeydown);
    };
  });
</script>

<svelte:head>
  <title>Aegis-JKN · Meja Kerja Verifikator BPJS Kesehatan</title>
  <meta
    name="description"
    content="Clinical Decision Support System (CDSS) Verifikator Klaim JKN dengan MHGSL, Svelte Flow, dan Graphiti Knowledge Graph"
  />
  <meta name="theme-color" content="#0d9488" />
</svelte:head>

<div class="min-h-screen w-full bg-background text-foreground antialiased selection:bg-primary/30 selection:text-foreground relative">
  {@render children()}
  <ShortcutsHint />
</div>
