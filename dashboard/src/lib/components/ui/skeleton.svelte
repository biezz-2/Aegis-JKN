<script lang="ts">
  let { class: className = '' }: { class?: string } = $props();
</script>

<div class="animate-pulse bg-slate-800 rounded-xl {className}"></div>