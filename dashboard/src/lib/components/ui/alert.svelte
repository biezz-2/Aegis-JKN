<script lang="ts">
  let {
    variant = 'default',
    class: className = ''
  }: { variant?: 'default' | 'destructive'; class?: string } = $props();
</script>

<div class="rounded-2xl border {variant === 'destructive' ? 'border-red-500/30 bg-red-950/50' : 'border-slate-800 bg-slate-900/80'} p-4 {className}">
  <slot />
</div>
