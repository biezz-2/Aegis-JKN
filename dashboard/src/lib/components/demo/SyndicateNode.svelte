<script lang="ts">
  import { Handle, Position, type NodeProps } from '@xyflow/svelte';

  let { data }: NodeProps & { data: { label: string; kind: string } } = $props();

  /* Slot kategorikal tervalidasi (lihat landing/assets/landing.css).
     Warna lama #22c55e/#eab308 gagal uji pemisahan CVD. */
  const COLORS: Record<string, string> = {
    Faskes: '#3987e5',
    Dokter: '#d95926',
    Pasien: '#199e70'
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
