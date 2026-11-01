import type { Claim } from "$lib/types";

const ROUTER_BASE_URL =
  (typeof import.meta !== "undefined" && import.meta.env?.PUBLIC_ROUTER_BASE_URL) ||
  "https://9router.biezz.my.id/v1";
const ROUTER_URL = `${ROUTER_BASE_URL.replace(/\/+$/, "")}/chat/completions`;
const API_KEY =
  (typeof import.meta !== "undefined" && import.meta.env?.PUBLIC_ROUTER_API_KEY) ||
  "";
const MODEL_NAME =
  (typeof import.meta !== "undefined" && import.meta.env?.PUBLIC_REPORTING_MODEL) ||
  "aegis-jkn";

export async function requestClinicalReport(claim: Claim, maxTokens: number = 2500): Promise<string> {

  // Priority 2: Attempt standard backend report endpoint
  try {
    const backendRes = await fetch("/api/report/generate-claim-explanation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        claim_id: claim.id,
        hospital: claim.hospital,
        doctor: claim.doctor,
        diagnosis_icd10: claim.diagnosisIcd10,
        procedure_icd9: claim.procedureIcd9,
        cost_rp: claim.costRp,
        los_days: claim.losDays,
        clinical_narrative: claim.clinicalNarrative,
        patient_feedback: claim.patientFeedback,
        has_contradiction: claim.hasContradiction,
        fraud_score: claim.fraudScore,
        topology_score: claim.channelContribution.topology,
        feature_score: claim.channelContribution.feature,
        semantic_score: claim.channelContribution.semantic,
      }),
    });

    if (backendRes.ok) {
      const data = await backendRes.json();
      if (data.success && data.data?.report) {
        return data.data.report;
      }
    }
  } catch (backendErr) {
    // Fall through to direct AI synthesis
  }

  // Strategy 2: Direct call to 9router with aegis-jkn model
  const systemPrompt =
    "Kamu adalah Spesialis Auditor Medis & Pencegahan Kecurangan (Anti-Fraud P2PK) BPJS Kesehatan tingkat ahli.\n" +
    "ATURAN MUTLAK:\n" +
    "1. Gunakan 100% BAHASA INDONESIA formal medis standar BPJS Kesehatan.\n" +
    "2. DILARANG KERAS memunculkan proses berpikir internal (thinking/chain-of-thought/preamble) dalam bahasa Inggris.\n" +
    "3. DILARANG menulis kalimat pengantar seperti 'The user wants...' atau 'Let me analyze...'.\n" +
    "4. LANGSUNG mulai respons dengan judul laporan:\n" +
    "# LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN";

  const userPrompt = `
Berkas Klaim BPJS Kesehatan:
- ID Klaim: ${claim.id}
- Faskes: ${claim.hospital}
- Dokter DPJP: ${claim.doctor}
- Diagnosis Primer (ICD-10): ${claim.diagnosisIcd10}
- Prosedur Ditagih (ICD-9-CM): ${claim.procedureIcd9 || "-"}
- Biaya Klaim: Rp ${claim.costRp.toLocaleString("id-ID")} | Lama Rawat (LOS): ${claim.losDays} hari
- Narasi Rekam Medis DPJP: "${claim.clinicalNarrative}"
- Umpan Balik Pasien: "${claim.patientFeedback}"
- Flag Kontradiksi Narasi: ${claim.hasContradiction ? "YA (TERDETEKSI KONTRADIKSI KLINIS)" : "TIDAK"}

Hasil Inferensi Model Graf MHGSL:
- Probabilitas Fraud: ${(claim.fraudScore * 100).toFixed(1)}%
- Kontribusi Kanal: Topologi T=${claim.channelContribution.topology.toFixed(2)}, Fitur F=${claim.channelContribution.feature.toFixed(2)}, Semantik S=${claim.channelContribution.semantic.toFixed(2)}

Susun laporan audit dalam format markdown berikut:
# LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN
**ID Klaim:** ${claim.id} | **Faskes:** ${claim.hospital} | **Status Risiko:** ${(claim.fraudScore * 100).toFixed(0)}%

## 1. [ANALISIS KLINIS & KODING INA-CBG]
Evaluasi kesesuaian diagnosis dan tindakan medis yang ditagihkan.

## 2. [EVALUASI KONTRADIKSI NARASI]
Analisis diskrepansi antara rekam medis dokter dan pengakuan pasien.

## 3. [INTERPRETASI GRAF MHGSL & ANTI-KAMUFLASE]
Uraikan arti bobot 3 kanal dan indikasi sindikat kolusi.

## 4. [REKOMENDASI PUTUSAN VERIFIKATOR]
Putusan definitif (SETUJUI / KLARIFIKASI RS / ESKALASI P2PK) beserta dasar regulasi penjaminan.
`;

  const payload = {
    model: MODEL_NAME,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
    max_tokens: 2500,
    temperature: 0.1,
  };

  const directRes = await fetch(ROUTER_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!directRes.ok) {
    const errText = await directRes.text();
    throw new Error(`Gagal memanggil model ${MODEL_NAME}: HTTP ${directRes.status} - ${errText}`);
  }

  const parsed = await directRes.json();
  const rawContent = parsed.choices?.[0]?.message?.content || "";
  const finalContent = sanitizeAiReport(rawContent);
  const regulatoryAppendix =
    "\n\n---\n" +
    "### DASAR REGULASI & KEPATUHAN PENJAMINAN:\n" +
    "- **Permenkes No. 24/2022**: Kewajiban Rekam Medis Elektronik & kebenaran resume medis.\n" +
    "- **UU No. 27/2022 (UU PDP)**: Perlindungan data pribadi kesehatan & integritas audit trail.\n" +
    "- **Permenkes No. 16/2019**: Pencegahan dan Penanganan Kecurangan (Fraud) pada Program JKN.\n" +
    "- **Status Kriptografis**: Rekaman audit ini disegel menggunakan tanda tangan Ed25519 & hash SHA-256.";

  return finalContent.includes("DASAR REGULASI") ? finalContent : `${finalContent}${regulatoryAppendix}`;
}

export function sanitizeAiReport(content: string): string {
  if (!content) return "";
  // 1. Remove <think> and <thought> tags
  let cleaned = content.replace(/<think>[\s\S]*?<\/think>/gi, "");
  cleaned = cleaned.replace(/<thought>[\s\S]*?<\/thought>/gi, "");

  // 2. Strip English thinking preambles before the first Indonesian report header
  const headerRegexes = [
    /(#+\s*LAPORAN\s+AUDIT[\s\S]*)/i,
    /(\*\*ID Klaim:\*\*[\s\S]*)/i,
    /(#+\s*1\.\s*RINGKASAN[\s\S]*)/i,
    /(\*?\*?1\.\s*\[ANALISIS[\s\S]*)/i,
    /(\*?\*?1\.\s*\*\*\[ANALISIS[\s\S]*)/i,
  ];

  for (const regex of headerRegexes) {
    const match = cleaned.match(regex);
    if (match && match[1]) {
      cleaned = match[1];
      break;
    }
  }

  return cleaned.trim();
}
