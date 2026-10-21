<script lang="ts">
  let { class: className = '' }: { class?: string } = $props();
</script>

<div class="bg-slate-900 border border-slate-800 rounded-3xl shadow-xl {className}">
  <slot />
</div>