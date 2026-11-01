import test, { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  parseChannelContribution,
  normalizeClaim,
  filterClaims,
  INITIAL_CLAIMS,
} from "./claims";
import type { RawClaim, Claim, FilterOptions } from "./types";

// Helper to create minimal valid Mock RawClaim
function createMockRawClaim(overrides: Partial<RawClaim> = {}): RawClaim {
  return {
    Name: "KLM-TEST-001",
    Tanggal: "2024-05-15",
    Status: "review",
    Risiko: "medium",
    "Skor Fraud": 0.55,
    Modus: "Upcoding",
    Sindikat: "SYND-01",
    Faskes: "RS Sehat Sentosa",
    Layanan: "Rawat Inap Kelas 1",
    Pasien: "Budi Santoso",
    Dokter: "Dr. Bambang Sutrisno",
    "Diagnosis ICD-10": "I20.0 - Angina Pectoris Instabil",
    "Prosedur ICD-9-CM": "88.56 - Koroner Angiografi",
    "Biaya Rp": 12500000,
    "LOS hari": 4,
    Obat: "Clopidogrel 75mg, Atorvastatin 20mg",
    Rujukan: "Puskesmas Gambir",
    "Alasan Berobat": "Nyeri dada retrosternal menjalar ke lengan kiri",
    "Narasi Rekam Medis": "Pasien mengeluh nyeri dada mendadak sejak 3 jam SMRS.",
    "Kontradiksi Narasi": false,
    "Umpan Balik Pasien": "Pelayanan baik, tidak ada pungutan liar.",
    Sentimen: "positif",
    "Skor Sentimen": 0.85,
    "Sinyal SHAP": "LOS > 3 (+0.25), Biaya > Rp10M (+0.30)",
    "Kontribusi Saluran": "T 0.45 · F 0.35 · S 0.20",
    Alasan: "Pola rujukan dan kesamaan billing dokter dengan kasus serupa",
    Catatan: "Verifikasi audit berkala",
    "Notion ID": "notion-uuid-001",
    ...overrides,
  };
}

// Helper to create minimal valid FilterOptions
function createFilterOptions(overrides: Partial<FilterOptions> = {}): FilterOptions {
  return {
    search: "",
    risk: "all",
    status: "all",
    modus: "all",
    syndicate: "all",
    serviceType: "all",
    contradictionOnly: false,
    sortBy: "date-desc",
    ...overrides,
  };
}

describe("parseChannelContribution", () => {
  it("parses standard inter-dot formatted channel string", () => {
    const result = parseChannelContribution("T 0.33 · F 0.33 · S 0.34");
    assert.strictEqual(result.topology, 0.33);
    assert.strictEqual(result.feature, 0.33);
    assert.strictEqual(result.semantic, 0.34);
    assert.strictEqual(result.rawString, "T 0.33 · F 0.33 · S 0.34");
  });

  it("parses custom weight values accurately", () => {
    const result = parseChannelContribution("T 0.65 · F 0.20 · S 0.15");
    assert.strictEqual(result.topology, 0.65);
    assert.strictEqual(result.feature, 0.20);
    assert.strictEqual(result.semantic, 0.15);
  });

  it("handles different separators: colons and commas", () => {
    const result = parseChannelContribution("T: 0.50, F: 0.30, S: 0.20");
    assert.strictEqual(result.topology, 0.50);
    assert.strictEqual(result.feature, 0.30);
    assert.strictEqual(result.semantic, 0.20);
  });

  it("handles no whitespace between channel letter and score", () => {
    const result = parseChannelContribution("T0.40/F0.35/S0.25");
    assert.strictEqual(result.topology, 0.40);
    assert.strictEqual(result.feature, 0.35);
    assert.strictEqual(result.semantic, 0.25);
  });

  it("handles pipe separated tokens", () => {
    const result = parseChannelContribution("T 0.8 | F 0.1 | S 0.1");
    assert.strictEqual(result.topology, 0.8);
    assert.strictEqual(result.feature, 0.1);
    assert.strictEqual(result.semantic, 0.1);
  });

  it("is case-insensitive for channel labels (lowercase t, f, s)", () => {
    const result = parseChannelContribution("t 0.12 · f 0.48 · s 0.40");
    assert.strictEqual(result.topology, 0.12);
    assert.strictEqual(result.feature, 0.48);
    assert.strictEqual(result.semantic, 0.40);
  });

  it("handles channels specified in non-standard order (S, T, F)", () => {
    const result = parseChannelContribution("S 0.70 · T 0.15 · F 0.15");
    assert.strictEqual(result.topology, 0.15);
    assert.strictEqual(result.feature, 0.15);
    assert.strictEqual(result.semantic, 0.70);
  });

  it("uses default values for missing channels", () => {
    // Only T provided -> F (0.33) and S (0.34) should retain defaults
    const onlyT = parseChannelContribution("T 0.85");
    assert.strictEqual(onlyT.topology, 0.85);
    assert.strictEqual(onlyT.feature, 0.33);
    assert.strictEqual(onlyT.semantic, 0.34);

    // Only F provided
    const onlyF = parseChannelContribution("F 0.60");
    assert.strictEqual(onlyF.topology, 0.33);
    assert.strictEqual(onlyF.feature, 0.60);
    assert.strictEqual(onlyF.semantic, 0.34);

    // Only S provided
    const onlyS = parseChannelContribution("S 0.95");
    assert.strictEqual(onlyS.topology, 0.33);
    assert.strictEqual(onlyS.feature, 0.33);
    assert.strictEqual(onlyS.semantic, 0.95);
  });

  it("handles boundary zero and integer values", () => {
    const zeros = parseChannelContribution("T 0.00 · F 0.00 · S 1.00");
    assert.strictEqual(zeros.topology, 0.0);
    assert.strictEqual(zeros.feature, 0.0);
    assert.strictEqual(zeros.semantic, 1.0);

    const integers = parseChannelContribution("T 1 · F 0 · S 0");
    assert.strictEqual(integers.topology, 1);
    assert.strictEqual(integers.feature, 0);
    assert.strictEqual(integers.semantic, 0);
  });

  it("handles empty string gracefully with defaults and fallback rawString", () => {
    const result = parseChannelContribution("");
    assert.strictEqual(result.topology, 0.33);
    assert.strictEqual(result.feature, 0.33);
    assert.strictEqual(result.semantic, 0.34);
    assert.strictEqual(result.rawString, "T 0.33 · F 0.33 · S 0.34");
  });

  it("handles null or undefined input gracefully", () => {
    const fromNull = parseChannelContribution(null as unknown as string);
    assert.strictEqual(fromNull.topology, 0.33);
    assert.strictEqual(fromNull.feature, 0.33);
    assert.strictEqual(fromNull.semantic, 0.34);
    assert.strictEqual(fromNull.rawString, "T 0.33 · F 0.33 · S 0.34");

    const fromUndef = parseChannelContribution(undefined as unknown as string);
    assert.strictEqual(fromUndef.topology, 0.33);
    assert.strictEqual(fromUndef.feature, 0.33);
    assert.strictEqual(fromUndef.semantic, 0.34);
    assert.strictEqual(fromUndef.rawString, "T 0.33 · F 0.33 · S 0.34");
  });

  it("preserves non-matching arbitrary string in rawString while using default values", () => {
    const arbitrary = "No channel weights specified";
    const result = parseChannelContribution(arbitrary);
    assert.strictEqual(result.topology, 0.33);
    assert.strictEqual(result.feature, 0.33);
    assert.strictEqual(result.semantic, 0.34);
    assert.strictEqual(result.rawString, arbitrary);
  });
});

describe("normalizeClaim", () => {
  it("maps all fields correctly from a valid RawClaim", () => {
    const raw = createMockRawClaim({
      Name: "KLM-100",
      Tanggal: "2024-04-10",
      Status: "escalate",
      Risiko: "fraud",
      "Skor Fraud": 0.94,
      Modus: "Phantom Billing",
      Sindikat: "RING-MEDIKA",
      Faskes: "RSUP Kariadi",
      Layanan: "Rawat Inap Bedah",
      Pasien: "Siti Rahma",
      Dokter: "Dr. Firman Sp.B",
      "Diagnosis ICD-10": "K35.8 - Acute Appendicitis",
      "Prosedur ICD-9-CM": "47.09 - Other Appendectomy",
      "Biaya Rp": 18200000,
      "LOS hari": 5,
      Obat: "Ceftriaxone, Ketorolac",
      Rujukan: "Faskes 1 Kota Semarang",
      "Alasan Berobat": "Nyeri perut kanan bawah",
      "Narasi Rekam Medis": "Pasien datang dengan tanda peritonitis lokal.",
      "Kontradiksi Narasi": true,
      "Umpan Balik Pasien": "Tidak pernah dioperasi appendectomy.",
      Sentimen: "negatif",
      "Skor Sentimen": -0.75,
      "Sinyal SHAP": "Phantom procedure detected (+0.42)",
      "Kontribusi Saluran": "T 0.70 · F 0.20 · S 0.10",
      Alasan: "Klaim ganda dan tagihan fiktif",
      Catatan: "Eskalasi ke tim investigasi lapangan",
      "Notion ID": "notion-klm-100",
    });

    const normalized = normalizeClaim(raw);

    assert.strictEqual(normalized.id, "KLM-100");
    assert.strictEqual(normalized.date, "2024-04-10");
    assert.strictEqual(normalized.status, "escalate");
    assert.strictEqual(normalized.risk, "fraud");
    assert.strictEqual(normalized.fraudScore, 0.94);
    assert.strictEqual(normalized.modus, "Phantom Billing");
    assert.strictEqual(normalized.syndicate, "RING-MEDIKA");
    assert.strictEqual(normalized.hospital, "RSUP Kariadi");
    assert.strictEqual(normalized.serviceType, "rawat inap");
    assert.strictEqual(normalized.patient, "Siti Rahma");
    assert.strictEqual(normalized.doctor, "Dr. Firman Sp.B");
    assert.strictEqual(normalized.diagnosisIcd10, "K35.8 - Acute Appendicitis");
    assert.strictEqual(normalized.procedureIcd9, "47.09 - Other Appendectomy");
    assert.strictEqual(normalized.costRp, 18200000);
    assert.strictEqual(normalized.losDays, 5);
    assert.strictEqual(normalized.drugs, "Ceftriaxone, Ketorolac");
    assert.strictEqual(normalized.referral, "Faskes 1 Kota Semarang");
    assert.strictEqual(normalized.chiefComplaint, "Nyeri perut kanan bawah");
    assert.strictEqual(normalized.clinicalNarrative, "Pasien datang dengan tanda peritonitis lokal.");
    assert.strictEqual(normalized.hasContradiction, true);
    assert.strictEqual(normalized.patientFeedback, "Tidak pernah dioperasi appendectomy.");
    assert.strictEqual(normalized.sentiment, "negatif");
    assert.strictEqual(normalized.sentimentScore, -0.75);
    assert.strictEqual(normalized.shapSignal, "Phantom procedure detected (+0.42)");
    assert.strictEqual(normalized.channelContribution.topology, 0.70);
    assert.strictEqual(normalized.channelContribution.feature, 0.20);
    assert.strictEqual(normalized.channelContribution.semantic, 0.10);
    assert.strictEqual(normalized.aiReasoning, "Klaim ganda dan tagihan fiktif");
    assert.strictEqual(normalized.notes, "Eskalasi ke tim investigasi lapangan");
    assert.strictEqual(normalized.notionId, "notion-klm-100");
  });

  it("normalizes status: escalate, flagged_audit, auto_clear, and review fallback", () => {
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: "escalate" })).status, "escalate");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: "ESCALATE" })).status, "escalate");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: "flagged_audit" })).status, "escalate");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: "FLAGGED_AUDIT" })).status, "escalate");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: "auto_clear" })).status, "auto_clear");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: "AUTO_CLEAR" })).status, "auto_clear");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: "review" })).status, "review");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: "unknown_status" })).status, "review");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: "" })).status, "review");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Status: null as unknown as string })).status, "review");
  });

  it("normalizes risk levels: fraud, high, medium, low fallback", () => {
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Risiko: "fraud" })).risk, "fraud");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Risiko: "FRAUD" })).risk, "fraud");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Risiko: "high" })).risk, "high");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Risiko: "HIGH" })).risk, "high");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Risiko: "medium" })).risk, "medium");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Risiko: "low" })).risk, "low");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Risiko: "unspecified" })).risk, "low");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Risiko: "" })).risk, "low");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Risiko: null as unknown as string })).risk, "low");
  });

  it("normalizes serviceType based on 'inap' keyword presence", () => {
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Layanan: "Rawat Inap" })).serviceType, "rawat inap");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Layanan: "RAWAT INAP TINGKAT 1" })).serviceType, "rawat inap");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Layanan: "ICU / Inap" })).serviceType, "rawat inap");

    assert.strictEqual(normalizeClaim(createMockRawClaim({ Layanan: "Rawat Jalan" })).serviceType, "rawat jalan");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Layanan: "Poli Bedah" })).serviceType, "rawat jalan");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Layanan: "" })).serviceType, "rawat jalan");
    assert.strictEqual(normalizeClaim(createMockRawClaim({ Layanan: null as unknown as string })).serviceType, "rawat jalan");
  });

  it("converts string-encoded numeric values and falls back safely on invalid values", () => {
    // Valid numeric strings
    const strRaw = createMockRawClaim({
      "Skor Fraud": "0.88" as unknown as number,
      "Biaya Rp": "15000000" as unknown as number,
      "LOS hari": "7" as unknown as number,
      "Skor Sentimen": "-0.45" as unknown as number,
    });
    const normalizedStr = normalizeClaim(strRaw);
    assert.strictEqual(normalizedStr.fraudScore, 0.88);
    assert.strictEqual(normalizedStr.costRp, 15000000);
    assert.strictEqual(normalizedStr.losDays, 7);
    assert.strictEqual(normalizedStr.sentimentScore, -0.45);

    // Invalid non-numeric strings fallback to 0
    const invalidRaw = createMockRawClaim({
      "Skor Fraud": "invalid" as unknown as number,
      "Biaya Rp": "not-a-number" as unknown as number,
      "LOS hari": "NaN" as unknown as number,
      "Skor Sentimen": "null" as unknown as number,
    });
    const normalizedInvalid = normalizeClaim(invalidRaw);
    assert.strictEqual(normalizedInvalid.fraudScore, 0);
    assert.strictEqual(normalizedInvalid.costRp, 0);
    assert.strictEqual(normalizedInvalid.losDays, 0);
    assert.strictEqual(normalizedInvalid.sentimentScore, 0);
  });

  it("coerces boolean contradiction flag from truthy/falsy values", () => {
    assert.strictEqual(normalizeClaim(createMockRawClaim({ "Kontradiksi Narasi": true })).hasContradiction, true);
    assert.strictEqual(normalizeClaim(createMockRawClaim({ "Kontradiksi Narasi": false })).hasContradiction, false);
    assert.strictEqual(normalizeClaim(createMockRawClaim({ "Kontradiksi Narasi": 1 as unknown as boolean })).hasContradiction, true);
    assert.strictEqual(normalizeClaim(createMockRawClaim({ "Kontradiksi Narasi": 0 as unknown as boolean })).hasContradiction, false);
    assert.strictEqual(normalizeClaim(createMockRawClaim({ "Kontradiksi Narasi": null as unknown as boolean })).hasContradiction, false);
  });

  it("handles null modus and syndicate without errors", () => {
    const raw = createMockRawClaim({
      Modus: null,
      Sindikat: null,
    });
    const normalized = normalizeClaim(raw);
    assert.strictEqual(normalized.modus, null);
    assert.strictEqual(normalized.syndicate, null);
  });
});

describe("filterClaims", () => {
  const sampleClaims: Claim[] = [
    {
      id: "KLM001",
      date: "2024-03-01",
      status: "escalate",
      risk: "fraud",
      fraudScore: 0.95,
      modus: "Upcoding",
      syndicate: "SYND-01",
      hospital: "RS Medika Utama",
      serviceType: "rawat inap",
      patient: "Agus Raharjo",
      doctor: "Dr. Rudi Hartono",
      diagnosisIcd10: "K29.7 - Gastritis",
      procedureIcd9: "45.13 - EGD Biopsy",
      costRp: 15000000,
      losDays: 4,
      drugs: "Omeprazole",
      referral: "Faskes A",
      chiefComplaint: "Sakit ulu hati",
      clinicalNarrative: "Pemeriksaan EGD menunjukkan lesi erosi.",
      hasContradiction: true,
      patientFeedback: "Tidak pernah dilakukan endoskopi",
      sentiment: "negatif",
      sentimentScore: -0.8,
      shapSignal: "Procedure mismatch (+0.35)",
      channelContribution: { topology: 0.5, feature: 0.3, semantic: 0.2, rawString: "T 0.5 · F 0.3 · S 0.2" },
      aiReasoning: "Indikasi upcoding sistematis",
      notes: "Prioritas audit investigatif",
      notionId: "notion-1",
    },
    {
      id: "KLM002",
      date: "2024-03-05",
      status: "escalate",
      risk: "high",
      fraudScore: 0.82,
      modus: "Phantom Billing",
      syndicate: "SYND-02",
      hospital: "RS Pelita Harapan",
      serviceType: "rawat jalan",
      patient: "Bunga Lestari",
      doctor: "Dr. Siti Aminah",
      diagnosisIcd10: "I10 - Essential Hypertension",
      procedureIcd9: "89.52 - ECG",
      costRp: 3500000,
      losDays: 0,
      drugs: "Amlodipine 10mg",
      referral: "Faskes B",
      chiefComplaint: "Pusing tengkuk",
      clinicalNarrative: "Tekanan darah 160/100.",
      hasContradiction: false,
      patientFeedback: "Pelayanan cepat dan ramah",
      sentiment: "positif",
      sentimentScore: 0.7,
      shapSignal: "Cost high for outpatient (+0.20)",
      channelContribution: { topology: 0.3, feature: 0.4, semantic: 0.3, rawString: "T 0.3 · F 0.4 · S 0.3" },
      aiReasoning: "Biaya lab melebihi batas tarif",
      notes: "Klarifikasi rincian biaya lab",
      notionId: "notion-2",
    },
    {
      id: "KLM003",
      date: "2024-03-10",
      status: "review",
      risk: "medium",
      fraudScore: 0.58,
      modus: "Upcoding",
      syndicate: null,
      hospital: "RS Graha Medika",
      serviceType: "rawat inap",
      patient: "Candra Wijaya",
      doctor: "Dr. Bambang Sutrisno",
      diagnosisIcd10: "J18.9 - Pneumonia",
      procedureIcd9: "96.71 - Continuous mechanical ventilation",
      costRp: 25000000,
      losDays: 6,
      drugs: "Levofloxacin, Ceftriaxone",
      referral: "Faskes C",
      chiefComplaint: "Sesak napas dan demam tinggi",
      clinicalNarrative: "Infiltrat paru bilateral pada rontgen toraks.",
      hasContradiction: true,
      patientFeedback: "Dirawat di ruang biasa tanpa ventilator",
      sentiment: "negatif",
      sentimentScore: -0.6,
      shapSignal: "Ventilator claim without ICU record (+0.30)",
      channelContribution: { topology: 0.2, feature: 0.5, semantic: 0.3, rawString: "T 0.2 · F 0.5 · S 0.3" },
      aiReasoning: "Klaim ventilator pada bangsal non-ICU",
      notes: "Perlu konfirmasi rekam medis fisik",
      notionId: "notion-3",
    },
    {
      id: "KLM004",
      date: "2024-02-20",
      status: "auto_clear",
      risk: "low",
      fraudScore: 0.12,
      modus: null,
      syndicate: null,
      hospital: "RSUD Cengkareng",
      serviceType: "rawat jalan",
      patient: "Dewi Kartika",
      doctor: "Dr. Hendra Wijaya",
      diagnosisIcd10: "Z00.0 - General medical examination",
      procedureIcd9: "89.07 - Consultation",
      costRp: 450000,
      losDays: 0,
      drugs: "Multivitamin",
      referral: "Faskes D",
      chiefComplaint: "Medical check-up rutin",
      clinicalNarrative: "Kondisi fisik normal, tensi 120/80.",
      hasContradiction: false,
      patientFeedback: "Sangat puas",
      sentiment: "positif",
      sentimentScore: 0.9,
      shapSignal: "Normal claim pattern (-0.45)",
      channelContribution: { topology: 0.33, feature: 0.33, semantic: 0.34, rawString: "T 0.33 · F 0.33 · S 0.34" },
      aiReasoning: "Klaim sesuai pedoman klinis standar",
      notes: "Auto-clear verifikasi otomatis",
      notionId: "notion-4",
    },
  ];

  it("returns all claims when default 'all' options are applied", () => {
    const result = filterClaims(sampleClaims, createFilterOptions());
    assert.strictEqual(result.length, 4);
  });

  describe("search filter", () => {
    it("filters by claim ID (case-insensitive)", () => {
      const resUpper = filterClaims(sampleClaims, createFilterOptions({ search: "KLM001" }));
      assert.strictEqual(resUpper.length, 1);
      assert.strictEqual(resUpper[0].id, "KLM001");

      const resLower = filterClaims(sampleClaims, createFilterOptions({ search: "klm002" }));
      assert.strictEqual(resLower.length, 1);
      assert.strictEqual(resLower[0].id, "KLM002");
    });

    it("filters by patient name", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ search: "agus" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].patient, "Agus Raharjo");
    });

    it("filters by doctor name", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ search: "aminah" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].doctor, "Dr. Siti Aminah");
    });

    it("filters by hospital name", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ search: "pelita" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].hospital, "RS Pelita Harapan");
    });

    it("filters by ICD-10 diagnosis code or text", () => {
      const byCode = filterClaims(sampleClaims, createFilterOptions({ search: "k29.7" }));
      assert.strictEqual(byCode.length, 1);
      assert.strictEqual(byCode[0].id, "KLM001");

      const byText = filterClaims(sampleClaims, createFilterOptions({ search: "pneumonia" }));
      assert.strictEqual(byText.length, 1);
      assert.strictEqual(byText[0].id, "KLM003");
    });

    it("filters by ICD-9-CM procedure code or text", () => {
      const byCode = filterClaims(sampleClaims, createFilterOptions({ search: "89.52" }));
      assert.strictEqual(byCode.length, 1);
      assert.strictEqual(byCode[0].id, "KLM002");

      const byText = filterClaims(sampleClaims, createFilterOptions({ search: "ventilation" }));
      assert.strictEqual(byText.length, 1);
      assert.strictEqual(byText[0].id, "KLM003");
    });

    it("filters by modus keyword", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ search: "phantom" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].modus, "Phantom Billing");
    });

    it("filters by syndicate ID", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ search: "SYND-01" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].syndicate, "SYND-01");
    });

    it("handles claims with null modus and syndicate safely during search", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ search: "nonexistent query xyz" }));
      assert.strictEqual(result.length, 0);
    });
  });

  describe("risk filter", () => {
    it("filters fraud risk claims", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ risk: "fraud" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].id, "KLM001");
    });

    it("filters high risk claims", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ risk: "high" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].id, "KLM002");
    });

    it("filters medium risk claims", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ risk: "medium" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].id, "KLM003");
    });

    it("filters low risk claims", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ risk: "low" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].id, "KLM004");
    });
  });

  describe("status filter", () => {
    it("filters escalate status claims", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ status: "escalate" }));
      assert.strictEqual(result.length, 2);
      assert.ok(result.every((c) => c.status === "escalate"));
    });

    it("filters review status claims", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ status: "review" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].id, "KLM003");
    });

    it("filters auto_clear status claims", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ status: "auto_clear" }));
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].id, "KLM004");
    });
  });

  describe("modus filter", () => {
    it("filters specific modus and excludes non-matching or null modus", () => {
      const upcodingClaims = filterClaims(sampleClaims, createFilterOptions({ modus: "Upcoding" }));
      assert.strictEqual(upcodingClaims.length, 2);
      assert.ok(upcodingClaims.every((c) => c.modus === "Upcoding"));

      const phantomClaims = filterClaims(sampleClaims, createFilterOptions({ modus: "Phantom Billing" }));
      assert.strictEqual(phantomClaims.length, 1);
      assert.strictEqual(phantomClaims[0].id, "KLM002");
    });
  });

  describe("syndicate filter", () => {
    it("filters specific syndicate and excludes null or other syndicates", () => {
      const synd1 = filterClaims(sampleClaims, createFilterOptions({ syndicate: "SYND-01" }));
      assert.strictEqual(synd1.length, 1);
      assert.strictEqual(synd1[0].id, "KLM001");

      const synd2 = filterClaims(sampleClaims, createFilterOptions({ syndicate: "SYND-02" }));
      assert.strictEqual(synd2.length, 1);
      assert.strictEqual(synd2[0].id, "KLM002");

      const emptySynd = filterClaims(sampleClaims, createFilterOptions({ syndicate: "SYND-UNKNOWN" }));
      assert.strictEqual(emptySynd.length, 0);
    });
  });

  describe("serviceType filter", () => {
    it("filters inpatient (rawat inap) claims", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ serviceType: "rawat inap" }));
      assert.strictEqual(result.length, 2);
      assert.ok(result.every((c) => c.serviceType === "rawat inap"));
    });

    it("filters outpatient (rawat jalan) claims", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ serviceType: "rawat jalan" }));
      assert.strictEqual(result.length, 2);
      assert.ok(result.every((c) => c.serviceType === "rawat jalan"));
    });
  });

  describe("contradictionOnly filter", () => {
    it("returns only claims with narrative contradictions when enabled", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ contradictionOnly: true }));
      assert.strictEqual(result.length, 2);
      assert.ok(result.every((c) => c.hasContradiction === true));
      assert.deepStrictEqual(result.map((c) => c.id).sort(), ["KLM001", "KLM003"]);
    });

    it("returns both contradicted and clean claims when disabled", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ contradictionOnly: false }));
      assert.strictEqual(result.length, 4);
    });
  });

  describe("sorting functionality", () => {
    it("sorts by score-desc (highest fraud score first)", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ sortBy: "score-desc" }));
      const scores = result.map((c) => c.fraudScore);
      assert.deepStrictEqual(scores, [0.95, 0.82, 0.58, 0.12]);
      assert.strictEqual(result[0].id, "KLM001");
    });

    it("sorts by score-asc (lowest fraud score first)", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ sortBy: "score-asc" }));
      const scores = result.map((c) => c.fraudScore);
      assert.deepStrictEqual(scores, [0.12, 0.58, 0.82, 0.95]);
      assert.strictEqual(result[0].id, "KLM004");
    });

    it("sorts by cost-desc (highest cost first)", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ sortBy: "cost-desc" }));
      const costs = result.map((c) => c.costRp);
      assert.deepStrictEqual(costs, [25000000, 15000000, 3500000, 450000]);
      assert.strictEqual(result[0].id, "KLM003");
    });

    it("sorts by cost-asc (lowest cost first)", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ sortBy: "cost-asc" }));
      const costs = result.map((c) => c.costRp);
      assert.deepStrictEqual(costs, [450000, 3500000, 15000000, 25000000]);
      assert.strictEqual(result[0].id, "KLM004");
    });

    it("sorts by date-desc (newest claim first)", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ sortBy: "date-desc" }));
      const dates = result.map((c) => c.date);
      assert.deepStrictEqual(dates, ["2024-03-10", "2024-03-05", "2024-03-01", "2024-02-20"]);
      assert.strictEqual(result[0].id, "KLM003");
    });

    it("defaults to date-desc when unknown sort specified", () => {
      const result = filterClaims(sampleClaims, createFilterOptions({ sortBy: "unknown-sort" as unknown as FilterOptions["sortBy"] }));
      const dates = result.map((c) => c.date);
      assert.deepStrictEqual(dates, ["2024-03-10", "2024-03-05", "2024-03-01", "2024-02-20"]);
    });
  });

  describe("combined filter scenarios", () => {
    it("combines search, risk, serviceType, contradictionOnly, and sorting", () => {
      const result = filterClaims(
        sampleClaims,
        createFilterOptions({
          search: "upcoding",
          risk: "fraud",
          serviceType: "rawat inap",
          contradictionOnly: true,
          sortBy: "score-desc",
        })
      );
      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].id, "KLM001");
      assert.strictEqual(result[0].hasContradiction, true);
      assert.strictEqual(result[0].risk, "fraud");
    });

    it("handles empty claims array gracefully", () => {
      const result = filterClaims([], createFilterOptions({ search: "test", sortBy: "score-desc" }));
      assert.deepStrictEqual(result, []);
    });
  });
});

describe("INITIAL_CLAIMS integration integrity", () => {
  it("loads INITIAL_CLAIMS dataset properly", () => {
    assert.ok(Array.isArray(INITIAL_CLAIMS));
    assert.ok(INITIAL_CLAIMS.length > 0, "INITIAL_CLAIMS should contain claims");
  });

  it("ensures every initialized claim satisfies typed Claim contract", () => {
    for (const claim of INITIAL_CLAIMS) {
      assert.ok(typeof claim.id === "string" && claim.id.length > 0, "Claim ID must be valid string");
      assert.ok(["escalate", "review", "auto_clear"].includes(claim.status), `Invalid status ${claim.status} in ${claim.id}`);
      assert.ok(["fraud", "high", "medium", "low"].includes(claim.risk), `Invalid risk ${claim.risk} in ${claim.id}`);
      assert.ok(["rawat inap", "rawat jalan"].includes(claim.serviceType), `Invalid serviceType ${claim.serviceType}`);
      assert.ok(typeof claim.fraudScore === "number" && !isNaN(claim.fraudScore), `Invalid fraudScore in ${claim.id}`);
      assert.ok(typeof claim.costRp === "number" && !isNaN(claim.costRp), `Invalid costRp in ${claim.id}`);
      assert.ok(typeof claim.hasContradiction === "boolean", `Invalid hasContradiction in ${claim.id}`);
      assert.ok(typeof claim.channelContribution === "object" && claim.channelContribution !== null, `Channel contribution missing in ${claim.id}`);
      assert.ok(typeof claim.channelContribution.topology === "number", `Topology score not a number in ${claim.id}`);
      assert.ok(typeof claim.channelContribution.feature === "number", `Feature score not a number in ${claim.id}`);
      assert.ok(typeof claim.channelContribution.semantic === "number", `Semantic score not a number in ${claim.id}`);
    }
  });
});
