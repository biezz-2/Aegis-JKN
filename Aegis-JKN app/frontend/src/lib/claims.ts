import rawDataset from "./data/klaim-dataset.json";
import rawBpjsRealDataset from "./data/bpjs-real-claims.json";
import type { RawClaim, Claim, ThreeChannelScore, FilterOptions } from "./types";

export function parseChannelContribution(raw: string): ThreeChannelScore {
  let topology = 0.33;
  let feature = 0.33;
  let semantic = 0.34;

  if (raw) {
    const tMatch = raw.match(/T[:=\s]*([0-9.]+)/i);
    const fMatch = raw.match(/F[:=\s]*([0-9.]+)/i);
    const sMatch = raw.match(/S[:=\s]*([0-9.]+)/i);

    if (tMatch) topology = parseFloat(tMatch[1]);
    if (fMatch) feature = parseFloat(fMatch[1]);
    if (sMatch) semantic = parseFloat(sMatch[1]);
  }

  return {
    topology,
    feature,
    semantic,
    rawString: raw || "T 0.33 · F 0.33 · S 0.34",
  };
}

export function normalizeClaim(raw: RawClaim): Claim {
  const channelContribution = parseChannelContribution(raw["Kontribusi Saluran"]);
  const rawStatus = (raw.Status || "").toLowerCase();
  const status =
    rawStatus === "escalate" || rawStatus === "flagged_audit"
      ? "escalate"
      : rawStatus === "auto_clear"
        ? "auto_clear"
        : "review";

  const rawRisk = (raw.Risiko || "").toLowerCase();
  const risk =
    rawRisk === "fraud"
      ? "fraud"
      : rawRisk === "high"
        ? "high"
        : rawRisk === "medium"
          ? "medium"
          : "low";

  const rawLayanan = (raw.Layanan || "").toLowerCase();
  const serviceType = rawLayanan.includes("inap") ? "rawat inap" : "rawat jalan";

  return {
    id: raw.Name,
    date: raw.Tanggal,
    status,
    risk,
    fraudScore: typeof raw["Skor Fraud"] === "number" ? raw["Skor Fraud"] : Number(raw["Skor Fraud"]) || 0,
    modus: raw.Modus,
    syndicate: raw.Sindikat,
    hospital: raw.Faskes,
    serviceType,
    patient: raw.Pasien,
    doctor: raw.Dokter,
    diagnosisIcd10: raw["Diagnosis ICD-10"],
    procedureIcd9: raw["Prosedur ICD-9-CM"],
    costRp: typeof raw["Biaya Rp"] === "number" ? raw["Biaya Rp"] : Number(raw["Biaya Rp"]) || 0,
    losDays: typeof raw["LOS hari"] === "number" ? raw["LOS hari"] : Number(raw["LOS hari"]) || 0,
    drugs: raw.Obat,
    referral: raw.Rujukan,
    chiefComplaint: raw["Alasan Berobat"],
    clinicalNarrative: raw["Narasi Rekam Medis"],
    hasContradiction: Boolean(raw["Kontradiksi Narasi"]),
    patientFeedback: raw["Umpan Balik Pasien"],
    sentiment: raw.Sentimen,
    sentimentScore: typeof raw["Skor Sentimen"] === "number" ? raw["Skor Sentimen"] : Number(raw["Skor Sentimen"]) || 0,
    shapSignal: raw["Sinyal SHAP"],
    channelContribution,
    aiReasoning: raw.Alasan,
    notes: raw.Catatan,
    notionId: raw["Notion ID"],
  };
}

export const INITIAL_CLAIMS: Claim[] = (rawDataset as RawClaim[]).map(normalizeClaim);
export const BPJS_REAL_CLAIMS: Claim[] = Array.isArray(rawBpjsRealDataset)
  ? (rawBpjsRealDataset as RawClaim[]).map(normalizeClaim)
  : [];


export function filterClaims(claims: Claim[], options: FilterOptions): Claim[] {
  return claims
    .filter((c) => {
      // Search filter
      if (options.search) {
        const query = options.search.toLowerCase();
        const matchesSearch =
          c.id.toLowerCase().includes(query) ||
          c.patient.toLowerCase().includes(query) ||
          c.doctor.toLowerCase().includes(query) ||
          c.hospital.toLowerCase().includes(query) ||
          c.diagnosisIcd10.toLowerCase().includes(query) ||
          c.procedureIcd9.toLowerCase().includes(query) ||
          (c.modus && c.modus.toLowerCase().includes(query)) ||
          (c.syndicate && c.syndicate.toLowerCase().includes(query));

        if (!matchesSearch) return false;
      }

      // Risk filter
      if (options.risk !== "all" && c.risk !== options.risk) {
        return false;
      }

      // Status filter
      if (options.status !== "all" && c.status !== options.status) {
        return false;
      }

      // Modus filter
      if (options.modus !== "all" && c.modus !== options.modus) {
        return false;
      }

      // Syndicate filter
      if (options.syndicate !== "all" && c.syndicate !== options.syndicate) {
        return false;
      }

      // Service type filter
      if (options.serviceType !== "all" && c.serviceType !== options.serviceType) {
        return false;
      }

      // Contradiction only
      if (options.contradictionOnly && !c.hasContradiction) {
        return false;
      }

      return true;
    })
    .sort((a, b) => {
      switch (options.sortBy) {
        case "score-desc":
          return b.fraudScore - a.fraudScore;
        case "score-asc":
          return a.fraudScore - b.fraudScore;
        case "cost-desc":
          return b.costRp - a.costRp;
        case "cost-asc":
          return a.costRp - b.costRp;
        case "date-desc":
        default:
          return b.date.localeCompare(a.date);
      }
    });
}
