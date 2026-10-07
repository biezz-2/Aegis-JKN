import type { Metadata } from "next";
import { OasisDashboard } from "@/components/oasis/oasis-dashboard";

export const metadata: Metadata = {
  title: "Dashboard Hasil Simulasi Oasis · Aegis-JKN",
  description:
    "Hasil simulasi 300 langkah interaksi agen teks Twitter & Reddit menggunakan model mistral-oasis:24b dan MHGSL Late Fusion untuk deteksi sindikat kecurangan klaim JKN BPJS Kesehatan.",
  keywords: [
    "Oasis Simulation",
    "Aegis-JKN",
    "Late Fusion",
    "BPJS Kesehatan",
    "Healthkathon 2026",
    "Twitter Reddit Agent Simulation",
    "Fraud Syndicate Detection",
  ],
};

export default function SimulasiPage() {
  return <OasisDashboard />;
}
