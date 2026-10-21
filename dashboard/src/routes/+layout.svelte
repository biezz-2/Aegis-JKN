<script lang="ts">
  import { Toaster } from 'svelte-sonner';
  import '@xyflow/svelte/dist/style.css';
  import '../index.css';
</script>

<slot />

<Toaster position="top-right" richColors />