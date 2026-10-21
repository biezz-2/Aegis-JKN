<script lang="ts">
  let { class: className = '' }: { class?: string } = $props();
</script>

<div class="font-semibold {className}">
  <slot />
</div>