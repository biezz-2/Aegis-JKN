import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import { ThemeProvider } from "@/components/theme-provider";
import { LangProvider } from "@/components/mhgsl/i18n";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Aegis-JKN · Visualisasi MHGSL & GNN untuk Deteksi Fraud Ekosistem JKN",
  description:
    "Visualisasi interaktif Multi-channel Heterogeneous Graph Structure Learning (MHGSL) dan Graph Neural Networks untuk deteksi sindikat kecurangan klaim asuransi kesehatan JKN. Untuk Healthkathon BPJS Kesehatan 2026 — Detect Smarter, Protect JKN.",
  keywords: [
    "MHGSL",
    "GNN",
    "Graph Neural Network",
    "Fraud Detection",
    "JKN",
    "BPJS Kesehatan",
    "Healthkathon 2026",
    "SATUSEHAT",
    "FHIR",
    "XGBoost",
    "SHAP",
  ],
  authors: [{ name: "Aegis-JKN Team" }],
  icons: {
    icon: "https://z-cdn.chatglm.cn/z-ai/static/logo.svg",
  },
  openGraph: {
    title: "Aegis-JKN · MHGSL Fraud Intelligence",
    description:
      "Visualisasi 3 saluran graf heterogen untuk deteksi upcoding & phantom billing pada ekosistem JKN.",
    url: "https://chat.z.ai",
    siteName: "Aegis-JKN",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Aegis-JKN · MHGSL Fraud Intelligence",
    description:
      "Visualisasi interaktif MHGSL & GNN untuk deteksi fraud ekosistem JKN.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="light"
          enableSystem={false}
          disableTransitionOnChange
        >
          <LangProvider>
            {children}
            <Toaster />
          </LangProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
