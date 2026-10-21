<script lang="ts">
  let { class: className = '' }: { class?: string } = $props();
</script>

<div class="space-y-4 {className}">
  <slot />
</div>