<script lang="ts">
  import { formatCurrency } from '@/lib/claims';
  import type { Claim } from '@/types/claims';

  let { claim }: { claim: Claim } = $props();

  const rows = $derived([
    { label: 'Tanggal klaim', value: claim.date },
    { label: 'Faskes', value: claim.hospital },
    { label: 'Layanan', value: claim.service },
    { label: 'Dokter', value: claim.doctor.display },
    { label: 'Diagnosis ICD-10', value: claim.icd10Diagnosis.raw },
    { label: 'Prosedur ICD-9-CM', value: claim.icd9cmProcedure?.raw ?? '—' },
    { label: 'Obat', value: claim.medication },
    { label: 'Rujukan', value: claim.referral },
    { label: 'Alasan berobat', value: claim.visitReason },
    { label: 'LOS', value: `${claim.lengthOfStayDays} hari` },
    { label: 'Biaya klaim', value: formatCurrency(claim.claimedAmount) }
  ]);
</script>

<div class="space-y-5">
  <div>
    <h3 class="text-xs font-semibold tracking-[0.2em] text-slate-500 uppercase">Narasi rekam medis</h3>
    <p class="mt-2 text-sm leading-relaxed text-slate-300">{claim.clinicalNarrative}</p>
  </div>

  {#if claim.narrativeContradiction}
    <div class="rounded-xl border border-red-500/30 bg-red-950/40 p-3">
      <p class="text-xs font-semibold text-red-300">Kontradiksi narasi terdeteksi</p>
      <p class="mt-1 text-sm text-red-200/80">{claim.patientFeedback}</p>
    </div>
  {/if}

  <dl class="grid gap-x-4 gap-y-3 sm:grid-cols-2">
    {#each rows as row (row.label)}
      <div>
        <dt class="text-xs text-slate-500">{row.label}</dt>
        <dd class="mt-0.5 text-sm break-words text-slate-200">{row.value}</dd>
      </div>
    {/each}
  </dl>

  <div class="rounded-xl border border-slate-800 bg-slate-950 p-3">
    <p class="text-xs text-slate-500">Sentimen pasien</p>
    <p class="mt-1 text-sm text-slate-200 capitalize">
      {claim.sentiment} <span class="font-mono text-slate-500">({claim.sentimentScore})</span>
    </p>
  </div>
</div>
