<script lang="ts">
  let {
    variant = 'default',
    size = 'md',
    href = undefined,
    class: className = ''
  }: {
    variant?: 'default' | 'outline';
    size?: 'sm' | 'md' | 'lg';
    href?: string;
    class?: string;
  } = $props();

  const classes = $derived(
    `rounded-2xl font-medium transition-all active:scale-95 flex items-center justify-center gap-2 ${
      variant === 'outline'
        ? 'border border-white/20 hover:bg-white/10'
        : 'bg-white text-slate-900 hover:bg-slate-200'
    } ${size === 'lg' ? 'px-8 py-4 text-base' : size === 'sm' ? 'px-4 py-2 text-sm' : 'px-6 py-3 text-base'} ${className}`
  );
</script>

{#if href}
  <a {href} class={classes}>
    <slot />
  </a>
{:else}
  <button class={classes}>
    <slot />
  </button>
{/if}
