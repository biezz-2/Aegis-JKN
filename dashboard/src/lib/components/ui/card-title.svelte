<script lang="ts">
  let { class: className = '' }: { class?: string } = $props();
</script>

<div class="text-2xl font-bold {className}">
  <slot />
</div>