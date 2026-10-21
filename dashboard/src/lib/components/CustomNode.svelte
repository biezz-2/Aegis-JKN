<script lang="ts">
  import { Handle, Position, type NodeProps } from '@xyflow/svelte';

  let { data }: NodeProps & { data: any } = $props();
</script>

<!-- `data.ink` menentukan warna teks: ramp ordinal biru punya langkah
     terang yang kontrasnya tinggi hanya dengan teks gelap, bukan putih. -->
<!-- Lebar tetap: posisi node Svelte Flow adalah sudut kiri-atas, jadi node
     dengan lebar berbeda akan punya pusat yang berbeda dan tepinya mengayun
     diagonal. Lebar seragam membuat rantai tegak lurus. -->
<div
  style="width: {data.width}px; text-align: center; background-color: {data.color}; color: {data.ink ?? '#ffffff'}; padding: 12px 12px; border-radius: 12px; font-weight: 600; font-size: 15px; box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.2);"
>
  {data.label}
</div>

<!-- Rantai tahap berjalan vertikal, jadi handle harus atas/bawah.
     Handle kiri/kanan membuat garis tepi melintang diagonal. -->
<Handle type="target" position={Position.Top} />
<Handle type="source" position={Position.Bottom} />