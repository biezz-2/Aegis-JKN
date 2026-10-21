<script lang="ts">
  import type { RiskBadge as RiskBadgeType } from '@/types/claims';

  let { label }: { label: RiskBadgeType } = $props();

  const STYLES: Record<RiskBadgeType, string> = {
    Safe: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    Review: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    Escalate: 'bg-orange-500/15 text-orange-300 border-orange-500/30',
    Syndicate: 'bg-red-500/15 text-red-300 border-red-500/30'
  };
</script>

<span
  class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold whitespace-nowrap {STYLES[label]}"
>
  {label}
</span>
