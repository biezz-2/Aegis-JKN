<script lang="ts">
  let { class: className = '' }: { class?: string } = $props();
</script>

<div class="text-slate-400 text-sm {className}">
  <slot />
</div>