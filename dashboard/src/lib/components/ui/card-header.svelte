<script lang="ts">
  let { class: className = '' }: { class?: string } = $props();
</script>

<div class="space-y-2 {className}">
  <slot />
</div>