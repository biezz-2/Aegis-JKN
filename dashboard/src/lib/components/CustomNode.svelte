<script lang="ts">
  import { Handle, Position, type NodeProps } from '@xyflow/svelte';

  let { data }: NodeProps & { data: any } = $props();
</script>

<div
  style="background-color: {data.color}; color: white; padding: 12px 20px; border-radius: 12px; font-weight: 600; box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.2);"
>
  {data.label}
</div>

<Handle type="target" position={Position.Left} />
<Handle type="source" position={Position.Right} />