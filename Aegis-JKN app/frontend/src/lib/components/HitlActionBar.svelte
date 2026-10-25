<script lang="ts">
  import { onMount } from "svelte";
  import { dashboard } from "$lib/stores/dashboard.svelte";
  import type { HitlAction } from "$lib/types";
  import Icon from "./Icon.svelte";
  import {
    playSubtleClick,
    playSuccessChime,
    playWarningAlert,
    playClarifyChime,
    toggleAudioMute,
    subscribeAudioMute,
    isReducedMotionPreferred,
  } from "$lib/audio";

  interface NoteTemplate {
    label: string;
    action: HitlAction;
    text: string;
  }

  const NOTE_TEMPLATES: NoteTemplate[] = [
    {
      label: "Indikasi Upcoding PCI",
      action: "ESCALATE_P2PK",
      text: "Terindikasi kuat upcoding kateterisasi jantung (PCI) multivasikular tanpa bukti stenosis signifikan pada angiografi. Berkas dieskalasi ke Tim Investigasi P2PK BPJS Kesehatan.",
    },
    {
      label: "Phantom Billing LOS 0",
      action: "ESCALATE_P2PK",
      text: "Indikasi phantom billing rawat inap (LOS 0 hari tapi ditagihkan rawat inap intensif). Surat eligibilitas dan resume medis tidak sinkron.",
    },
    {
      label: "Klaim Wajar",
      action: "APPROVE",
      text: "Klaim diverifikasi valid secara medis. Kesesuaian diagnosa primer, sekunder, dan terapi obat sesuai panduan klinis BPJS Kesehatan.",
    },
    {
      label: "Klarifikasi Koding RS",
      action: "CLARIFY_RS",
      text: "Terdapat diskrepansi koding tindakan vs laporan operasi. Meminta faskes mengirimkan resume medis lengkap, rincian obat, dan bukti penunjang laboratorium.",
    },
    {
      label: "Readmisi <30 Hari Tidak Wajar",
      action: "CLARIFY_RS",
      text: "Terdeteksi pola readmisi berulang interval <30 hari dengan diagnosis identik. Meminta konfirmasi indikasi medis pemulangan sebelumnya.",
    },
  ];

  const claim = $derived(dashboard.selectedClaim);

  let modalOpen = $state(false);
  let pendingAction = $state<HitlAction>("APPROVE");
  let verifierNote = $state("");
  let isSubmitting = $state(false);
  let isMuted = $state(true);
  let reducedMotion = $state(false);
  let toastBanner = $state<{
    type: "success" | "warning" | "danger";
    title: string;
    message: string;
    action: HitlAction;
    claimId: string;
  } | null>(null);
  let toastTimer: ReturnType<typeof setTimeout> | null = null;

  function openActionDialog(action: HitlAction, initialText?: string) {
    if (!claim) return;
    playSubtleClick();
    pendingAction = action;
    if (initialText) {
      verifierNote = initialText;
    } else {
      verifierNote =
        action === "APPROVE"
          ? "Klaim diverifikasi valid secara medis. Kesesuaian diagnosa dan obat wajar."
          : action === "CLARIFY_RS"
            ? "Terdapat diskrepansi koding tindakan. Meminta faskes mengirimkan resume medis lengkap dan bukti penunjang tindakan."
            : "Terindikasi kuat sindikat upcoding dan pemalsuan tagihan. Berkas dieskalasi ke Tim Investigasi Anti-Fraud P2PK BPJS Kesehatan.";
    }
    modalOpen = true;
  }

  function applyTemplate(tpl: NoteTemplate) {
    playSubtleClick();
    pendingAction = tpl.action;
    verifierNote = tpl.text;
  }

  async function handleSubmit() {
    if (!verifierNote.trim() || !claim) return;
    isSubmitting = true;

    const submittedAction = pendingAction;
    const submittedClaimId = claim.id;
    await dashboard.recordHitlDecision(submittedAction, verifierNote);

    isSubmitting = false;
    modalOpen = false;

    // Mainkan umpan balik audio prosedural sesuai putusan
    if (submittedAction === "APPROVE") {
      playSuccessChime();
    } else if (submittedAction === "ESCALATE_P2PK") {
      playWarningAlert();
    } else {
      playClarifyChime();
    }
    // Tampilkan toast konfirmasi instan
    if (toastTimer) clearTimeout(toastTimer);
    const type =
      submittedAction === "APPROVE"
        ? "success"
        : submittedAction === "CLARIFY_RS"
          ? "warning"
          : "danger";
    const actionLabel =
      submittedAction === "APPROVE"
        ? "Disetujui (Approved)"
        : submittedAction === "CLARIFY_RS"
          ? "Dimintakan Klarifikasi RS"
          : "Dieskalasi ke Tim Anti-Fraud P2PK";

    toastBanner = {
      type,
      title: `Putusan Berhasil Dicatat: ${actionLabel}`,
      message: `Berkas ${submittedClaimId} telah ditandatangani dan dicatat ke Audit Trail SHA-256.`,
      action: submittedAction,
      claimId: submittedClaimId,
    };

    toastTimer = setTimeout(() => {
      toastBanner = null;
    }, 4500);
  }

  function dismissToast() {
    if (toastTimer) clearTimeout(toastTimer);
    toastBanner = null;
  }

  onMount(() => {
    reducedMotion = isReducedMotionPreferred();
    const unsubAudio = subscribeAudioMute((muted) => {
      isMuted = muted;
    });

    function handleKeydown(e: KeyboardEvent) {
      const target = e.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === "INPUT" ||
          target.tagName === "TEXTAREA" ||
          target.isContentEditable)
      ) {
        return;
      }

      // Jangan intercept jika ada modifier (Ctrl/Meta/Alt)
      if (e.ctrlKey || e.metaKey || e.altKey) return;

      const key = e.key.toLowerCase();
      if (key === "a") {
        e.preventDefault();
        openActionDialog("APPROVE");
      } else if (key === "c") {
        e.preventDefault();
        openActionDialog("CLARIFY_RS");
      } else if (key === "e") {
        e.preventDefault();
        openActionDialog("ESCALATE_P2PK");
      } else if (key === "m") {
        e.preventDefault();
        isMuted = toggleAudioMute();
      }
    }

    window.addEventListener("keydown", handleKeydown);
    return () => {
      window.removeEventListener("keydown", handleKeydown);
      unsubAudio();
      if (toastTimer) clearTimeout(toastTimer);
    };
  });
</script>

<!-- Toast Banner Konfirmasi Instan -->
{#if toastBanner}
  <div
    role="status"
    aria-live="polite"
    class="border-t border-border px-4 py-2.5 shadow-sm transition-all animate-count-up {toastBanner.type === 'success' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-900 dark:text-emerald-200' : toastBanner.type === 'warning' ? 'bg-yellow-500/10 border-yellow-500/30 text-yellow-900 dark:text-yellow-200' : 'bg-rose-500/10 border-rose-500/30 text-rose-900 dark:text-rose-200'}"
  >
    <div class="flex items-center justify-between gap-3 text-xs">
      <div class="flex items-center gap-2 min-w-0">
        <div class="shrink-0">
          {#if toastBanner.type === 'success'}
            <Icon name="CheckCircle2" size={16} class="text-emerald-600 dark:text-emerald-400" />
          {:else if toastBanner.type === 'warning'}
            <Icon name="AlertTriangle" size={16} class="text-yellow-600 dark:text-yellow-400" />
          {:else}
            <Icon name="ShieldAlert" size={16} class="text-rose-600 dark:text-rose-400" />
          {/if}
        </div>
        <div class="truncate">
          <span class="font-bold">{toastBanner.title}</span>
          <span class="opacity-80 ml-1.5 hidden sm:inline">{toastBanner.message}</span>
        </div>
      </div>
      <button
        type="button"
        onclick={dismissToast}
        class="shrink-0 rounded-md p-1 hover:bg-black/5 dark:hover:bg-white/5 opacity-70 hover:opacity-100 transition-opacity"
        aria-label="Tutup notifikasi"
      >
        <Icon name="X" size={14} />
      </button>
    </div>
  </div>
{/if}

<div class="border-t border-slate-200/70 dark:border-[#a3b18a]/15 bg-card p-3.5 shadow-sm">
  <div class="flex flex-wrap items-center justify-between gap-3">
    <!-- Left: Status of active claim -->
    <div class="flex items-center gap-2">
      <span class="text-xs text-muted-foreground font-medium">Status Berkas:</span>
      {#if claim?.verifiedStatus}
        <span class="rounded-lg px-2.5 py-1 text-xs font-bold font-mono uppercase {claim.verifiedStatus === 'APPROVE' ? 'bg-emerald-500/20 text-emerald-800 dark:text-emerald-300 border border-emerald-500/40' : claim.verifiedStatus === 'CLARIFY_RS' ? 'bg-yellow-500/20 text-yellow-800 dark:text-yellow-300 border border-yellow-500/40' : 'bg-rose-500/20 text-rose-800 dark:text-rose-300 border border-rose-500/40'}">
          ✓ {claim.verifiedStatus === 'APPROVE' ? 'DISETUJUI' : claim.verifiedStatus === 'CLARIFY_RS' ? 'MENUNGGU KLARIFIKASI RS' : 'DITOLAK / ESKALASI P2PK'}
        </span>
      {:else}
        <span class="rounded-lg bg-muted px-2.5 py-1 text-xs font-medium text-muted-foreground">
          Menunggu Keputusan Verifikator
        </span>
      {/if}
    </div>

    <!-- Right: The 3 HITL Action Buttons with Keyboard Shortcuts Badges -->
    <div class="flex items-center gap-2">
      <!-- 1. Setujui Klaim (Shortcut: A) -->
      <button
        type="button"
        data-testid="hitl-action-approve"
        onclick={() => openActionDialog("APPROVE")}
        title="Setujui Klaim (Tekan shortcut 'A')"
        class="inline-flex items-center gap-1.5 rounded-xl border border-emerald-500/40 bg-emerald-500/10 px-3.5 py-2 text-xs font-bold text-emerald-800 dark:text-emerald-300 hover:bg-emerald-500/20 active:scale-98 transition-all min-h-[36px]"
      >
        <Icon name="CheckCircle2" size={15} />
        <span>Setujui Klaim</span>
        <kbd class="ml-1 rounded border border-emerald-500/30 bg-emerald-500/15 px-1.5 py-0.2 text-[10px] font-mono font-medium">A</kbd>
      </button>

      <!-- 2. Minta Konfirmasi RS (Shortcut: C) -->
      <button
        type="button"
        data-testid="hitl-action-clarify"
        onclick={() => openActionDialog("CLARIFY_RS")}
        title="Minta Konfirmasi RS (Tekan shortcut 'C')"
        class="inline-flex items-center gap-1.5 rounded-xl border border-yellow-500/40 bg-yellow-500/10 px-3.5 py-2 text-xs font-bold text-yellow-800 dark:text-yellow-300 hover:bg-yellow-500/20 active:scale-98 transition-all min-h-[36px]"
      >
        <Icon name="AlertTriangle" size={15} />
        <span>Minta Konfirmasi RS</span>
        <kbd class="ml-1 rounded border border-yellow-500/30 bg-yellow-500/15 px-1.5 py-0.2 text-[10px] font-mono font-medium">C</kbd>
      </button>
      <!-- 3. Tolak / Eskalasi P2PK (Shortcut: E) -->
      <button
        type="button"
        data-testid="hitl-action-escalate"
        onclick={() => openActionDialog("ESCALATE_P2PK")}
        title="Tolak / Eskalasi ke Tim P2PK (Tekan shortcut 'E')"
        class="inline-flex items-center gap-1.5 rounded-xl bg-rose-600 hover:bg-rose-700 px-3.5 py-2 text-xs font-bold text-white shadow-xs hover:shadow-md active:scale-98 transition-all min-h-[36px]"
      >
        <Icon name="ShieldAlert" size={15} />
        <span>Tolak / Eskalasi P2PK</span>
        <kbd class="ml-1 rounded border border-white/30 bg-white/15 px-1.5 py-0.2 text-[10px] font-mono font-medium text-white">E</kbd>
      </button>
      <!-- 4. Bisukan / Aktifkan Suara Audio Feedback (Shortcut: M) -->
      <button
        type="button"
        onclick={() => {
          isMuted = toggleAudioMute();
        }}
        title={isMuted
          ? (reducedMotion ? "Suara dinonaktifkan (Preferensi Reduced-Motion aktif). Klik atau tekan 'M' untuk mengaktifkan." : "Suara dibisukan. Klik atau tekan 'M' untuk mengaktifkan.")
          : "Suara aktif (klik/lonceng prosedural). Klik atau tekan 'M' untuk membisukan."}
        aria-label={isMuted ? "Aktifkan feedback suara" : "Bisukan feedback suara"}
        aria-pressed={!isMuted}
        class="inline-flex items-center justify-center gap-1.5 rounded-xl border border-slate-200 dark:border-[#a3b18a]/20 px-2.5 py-2 text-xs font-medium transition-all min-h-[36px] min-w-[36px] active:scale-95 {isMuted ? 'text-muted-foreground bg-muted/40 hover:bg-muted hover:text-foreground' : 'text-primary bg-primary/10 border-primary/30 hover:bg-primary/20'}"
      >
        <Icon name={isMuted ? "VolumeX" : "Volume2"} size={15} />
        <kbd class="rounded border border-slate-200/70 dark:border-[#a3b18a]/20 bg-muted/80 px-1.5 py-0.2 text-[10px] font-mono text-muted-foreground font-medium">M</kbd>
      </button>
    </div>
  </div>
</div>

<!-- Modal Dialog: Verifier Mandatory Review Note -->
{#if modalOpen && claim}
  <div
    role="dialog"
    aria-modal="true"
    tabindex="-1"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4 overflow-y-auto"
    onclick={(e) => { if (e.target === e.currentTarget) modalOpen = false; }}
    onkeydown={(e) => { if (e.key === 'Escape') modalOpen = false; }}
  >
    <div class="relative w-full max-w-lg rounded-3xl border border-slate-200 dark:border-[#a3b18a]/25 bg-card p-6 shadow-2xl text-card-foreground my-8 space-y-4">
      <div class="flex items-center justify-between pb-3 border-b border-slate-200/70 dark:border-[#a3b18a]/20">
        <div class="flex items-center gap-2">
          <Icon name="ShieldCheck" size={18} class="text-primary" />
          <h3 class="font-bold text-base">Konfirmasi Putusan Human-in-the-Loop</h3>
        </div>
        <button
          type="button"
          onclick={() => (modalOpen = false)}
          class="rounded-lg p-1 text-muted-foreground hover:text-foreground"
          aria-label="Tutup"
        >
          <Icon name="X" size={18} />
        </button>
      </div>

      <!-- Claim Summary Info -->
      <div class="p-3 rounded-xl bg-muted/30 border border-border/60 text-xs space-y-1">
        <div class="flex items-center justify-between">
          <span class="font-mono font-bold text-foreground">{claim.id} ({claim.patient})</span>
          <span class="font-mono font-bold text-rose-600">Skor AI: {(claim.fraudScore * 100).toFixed(0)}%</span>
        </div>
        <div class="text-muted-foreground">
          {claim.hospital} · Rp {claim.costRp.toLocaleString("id-ID")} · {claim.diagnosisIcd10.split(" - ")[0]}
        </div>
      </div>

      <!-- Action Selected Pill -->
      <div class="text-xs">
        <span class="text-muted-foreground block mb-1">Tindakan yang Dipilih:</span>
        <div class="p-2.5 rounded-xl font-bold font-mono text-xs {pendingAction === 'APPROVE' ? 'bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 border border-emerald-500/30' : pendingAction === 'CLARIFY_RS' ? 'bg-yellow-500/15 text-yellow-800 dark:text-yellow-300 border border-yellow-500/30' : 'bg-rose-500/15 text-rose-800 dark:text-rose-300 border border-rose-500/30'}">
          {pendingAction === 'APPROVE' ? 'SETUJUI KLAIM (APPROVE)' : pendingAction === 'CLARIFY_RS' ? 'MINTA KONFIRMASI RS (DISPUTE / CLARIFY)' : 'TOLAK / ESKALASI KE TIM P2PK (ESCALATE)'}
        </div>
      </div>

      <!-- Quick Templates / Template Catatan Cepat Standar BPJS -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between text-xs">
          <span class="font-semibold text-foreground flex items-center gap-1.5">
            <Icon name="Sparkles" size={13} class="text-primary" />
            <span>Template Catatan Cepat (Standar BPJS):</span>
          </span>
          <span class="text-[10px] text-muted-foreground">Klik untuk mengisi instan</span>
        </div>
        <div class="flex flex-wrap gap-1.5">
          {#each NOTE_TEMPLATES as tpl}
            <button
              type="button"
              onclick={() => applyTemplate(tpl)}
              class="inline-flex items-center gap-1 rounded-lg border px-2.5 py-1 text-[11px] font-medium transition-all min-h-[30px] {tpl.action === 'APPROVE' ? 'border-emerald-500/30 bg-emerald-500/5 text-emerald-800 dark:text-emerald-300 hover:bg-emerald-500/15' : tpl.action === 'CLARIFY_RS' ? 'border-yellow-500/30 bg-yellow-500/5 text-yellow-800 dark:text-yellow-300 hover:bg-yellow-500/15' : 'border-rose-500/30 bg-rose-500/5 text-rose-800 dark:text-rose-300 hover:bg-rose-500/15'}"
            >
              <span>{tpl.label}</span>
            </button>
          {/each}
        </div>
      </div>

      <!-- Mandatory Note Form -->
      <div class="space-y-1.5 text-xs">
        <label for="verifier-note" class="font-semibold text-foreground block">
          Catatan Telaah Verifikator (Wajib):
        </label>
        <textarea
          id="verifier-note"
          bind:value={verifierNote}
          rows="4"
          placeholder="Tuliskan justifikasi klinis atau dasar penolakan..."
          class="w-full rounded-xl border border-border bg-background p-3 text-xs text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40 leading-relaxed font-sans"
        ></textarea>
        <div class="flex items-center justify-between text-[10px] text-muted-foreground">
          <span>Catatan ditandatangani kriptografis SHA-256 & disimpan ke Audit Trail (UU PDP No. 27/2022).</span>
          <span class="font-mono">{verifierNote.length} karakter</span>
        </div>
      </div>

      <!-- Buttons -->
      <div class="flex items-center justify-end gap-2 pt-3 border-t border-border">
        <button
          type="button"
          onclick={() => { playSubtleClick(); modalOpen = false; }}
          class="rounded-xl border border-border px-4 py-2 text-xs font-semibold hover:bg-muted"
        >
          Batal
        </button>
        <button
          type="button"
          disabled={!verifierNote.trim() || isSubmitting}
          onclick={handleSubmit}
          class="rounded-xl bg-primary px-4 py-2 text-xs font-bold text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-all"
        >
          {isSubmitting ? "Menyimpan & Enkripsi..." : "Simpan Putusan"}
        </button>
      </div>
    </div>
  </div>
{/if}
