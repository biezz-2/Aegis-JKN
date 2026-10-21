<script lang="ts">
  import { auditLog } from '@/store/auditLog';
  import type { AuditAction } from '@/types/claims';

  const LABELS: Record<AuditAction, string> = {
    approve: 'Setujui',
    request_confirmation: 'Konfirmasi RS',
    reject: 'Tolak'
  };

  const COLORS: Record<AuditAction, string> = {
    approve: 'text-emerald-300',
    request_confirmation: 'text-amber-300',
    reject: 'text-red-300'
  };
</script>

<div>
  <h3 class="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Audit lokal</h3>
  {#if $auditLog.length === 0}
    <p class="mt-2 rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm text-slate-500">
      Belum ada keputusan tercatat di perangkat ini.
    </p>
  {:else}
    <ul class="mt-2 max-h-64 space-y-2 overflow-y-auto pr-1">
      {#each [...$auditLog].reverse() as entry (entry.id)}
        <li class="rounded-lg border border-slate-800 bg-slate-950 p-2.5">
          <div class="flex items-center justify-between gap-2">
            <span class="font-mono text-xs text-slate-300">{entry.claimId}</span>
            <span class="text-xs font-semibold {COLORS[entry.action]}">{LABELS[entry.action]}</span>
          </div>
          <p class="mt-1 text-xs text-slate-400">{entry.note}</p>
          <p class="mt-1 text-[10px] text-slate-600">
            {new Date(entry.timestamp).toLocaleString('id-ID')} · skor AI {entry.aiScore}
          </p>
        </li>
      {/each}
    </ul>
  {/if}
  <p class="mt-2 text-xs text-slate-600">
    Audit disimpan di localStorage browser. Ini demonstrasi perangkat-lokal, bukan rekam audit produksi.
  </p>
</div>
