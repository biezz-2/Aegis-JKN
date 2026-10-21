<script lang="ts">
  import { Check, MessageSquareWarning, X } from 'lucide-svelte';
  import { recordAudit } from '@/store/auditLog';
  import type { AuditAction, Claim } from '@/types/claims';

  let { claim }: { claim: Claim } = $props();

  const ACTIONS: { action: AuditAction; label: string; icon: typeof Check; className: string }[] = [
    {
      action: 'approve',
      label: 'Setujui Klaim',
      icon: Check,
      className: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30 hover:bg-emerald-500/25'
    },
    {
      action: 'request_confirmation',
      label: 'Minta Konfirmasi RS',
      icon: MessageSquareWarning,
      className: 'bg-amber-500/15 text-amber-300 border-amber-500/30 hover:bg-amber-500/25'
    },
    {
      action: 'reject',
      label: 'Tolak',
      icon: X,
      className: 'bg-red-500/15 text-red-300 border-red-500/30 hover:bg-red-500/25'
    }
  ];

  let pending = $state<AuditAction | null>(null);
  let note = $state('');
  let error = $state('');

  function open(action: AuditAction) {
    pending = action;
    note = '';
    error = '';
  }

  function close() {
    pending = null;
    note = '';
    error = '';
  }

  function submit() {
    if (!pending) return;
    if (!note.trim()) {
      error = 'Catatan verifikator wajib diisi.';
      return;
    }
    recordAudit(claim.id, pending, note, claim.fraudScore);
    close();
  }
</script>

<div>
  <h3 class="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Tindakan verifikator</h3>
  <div class="mt-3 flex flex-wrap gap-2">
    {#each ACTIONS as item (item.action)}
      <button
        type="button"
        onclick={() => open(item.action)}
        class="inline-flex items-center gap-2 rounded-xl border px-3.5 py-2 text-sm font-medium transition-colors {item.className}"
      >
        <item.icon class="h-4 w-4" />
        {item.label}
      </button>
    {/each}
  </div>

  {#if pending}
    <div class="mt-4 rounded-xl border border-slate-700 bg-slate-950 p-4">
      <label for="verifier-note" class="text-sm text-slate-300">
        Catatan verifikator <span class="text-red-400">*</span>
      </label>
      <textarea
        id="verifier-note"
        bind:value={note}
        rows="3"
        placeholder="Alasan keputusan Anda…"
        class="mt-2 w-full rounded-lg border border-slate-800 bg-slate-900 p-3 text-sm text-slate-200 placeholder:text-slate-600 focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
      ></textarea>
      {#if error}
        <p class="mt-1.5 text-xs text-red-400">{error}</p>
      {/if}
      <div class="mt-3 flex gap-2">
        <button
          type="button"
          onclick={submit}
          class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-500"
        >
          Simpan keputusan
        </button>
        <button
          type="button"
          onclick={close}
          class="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-800"
        >
          Batal
        </button>
      </div>
    </div>
  {/if}
</div>
