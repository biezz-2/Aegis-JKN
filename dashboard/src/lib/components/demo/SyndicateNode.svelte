<script lang="ts">
  import { Handle, Position, type NodeProps } from '@xyflow/svelte';

  let { data }: NodeProps & { data: { label: string; kind: string } } = $props();

  const COLORS: Record<string, string> = {
    Faskes: '#3b82f6',
    Dokter: '#22c55e',
    Pasien: '#eab308'
  };
</script>

<div
  class="rounded-xl px-3 py-2 text-xs font-semibold text-white shadow-lg"
  style="background-color: {COLORS[data.kind] ?? '#64748b'};"
>
  <div class="text-[10px] font-normal opacity-80">{data.kind}</div>
  {data.label}
</div>

<Handle type="target" position={Position.Left} />
<Handle type="source" position={Position.Right} />
