import type { Metadata } from "next";
import { DatasetExplorer } from "@/components/dataset/dataset-explorer";

export const metadata: Metadata = {
  title: "Katalog Dataset Notion · Aegis-JKN",
  description:
    "Eksplorasi katalog dataset Notion Aegis-JKN: 300 data klaim JKN sintetis bernilai Rp 3,53 Miliar, 33 pilar riset literatur MHGSL & XAI, serta dokumentasi interoperabilitas SATUSEHAT dan V-Claim BPJS Kesehatan.",
  keywords: [
    "Dataset Notion",
    "Aegis-JKN",
    "Klaim BPJS Kesehatan",
    "MHGSL",
    "Explainable AI",
    "SHAP",
    "Healthkathon 2026",
    "Fraud Syndicate Detection",
    "SATUSEHAT",
    "FHIR R4",
  ],
  openGraph: {
    title: "Katalog Dataset Notion · Aegis-JKN",
    description:
      "Eksplorasi interaktif 300 berkas klaim JKN sintetis (Rp 3,53 Miliar) dan 33 basis riset MHGSL multi-channel graph intelligence.",
    siteName: "Aegis-JKN",
    type: "website",
  },
};

export default function DatasetPage() {
  return <DatasetExplorer />;
}
