"use client";

import * as React from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  Printer,
  Download,
  Search,
  Activity,
  Layers,
  ArrowLeft,
  Filter,
  Info,
  Check,
  ChevronRight,
  ExternalLink,
  Bot,
  Heart,
  MessageSquare,
  FileSpreadsheet,
  X,
  Sparkles,
  BarChart3,
} from "lucide-react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";
import { OASIS_DATA, type ClaimQueueItem, type SocialFeedItem } from "@/data/oasis-data";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { ThemeToggle } from "@/components/mhgsl/theme-toggle";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

// Palette colors consistent with MHGSL & dashboard-aegis-jkn.html
const SENT_COLORS = {
  Positif: "#10b981",
  Netral: "#94a3b8",
  Negatif: "#f43f5e",
};

const RISK_COLORS: Record<string, string> = {
  fraud: "#f43f5e",
  high: "#f97316",
  medium: "#f59e0b",
  low: "#94a3b8",
};

export function OasisDashboard() {
  const [activeTab, setActiveTab] = React.useState<"overview" | "queue" | "feeds" | "raw">("overview");
  const [queueFilter, setQueueFilter] = React.useState<"all" | "kontra" | "synd" | "nonsynd">("all");
  const [queueSearch, setQueueSearch] = React.useState("");
  const [selectedClaim, setSelectedClaim] = React.useState<ClaimQueueItem | null>(null);

  const [feedPlatform, setFeedPlatform] = React.useState<"all" | "twitter" | "reddit">("all");
  const [feedSentimentFilter, setFeedSentimentFilter] = React.useState<string>("all");
  const [feedFraudOnly, setFeedFraudOnly] = React.useState(false);
  const [feedSearch, setFeedSearch] = React.useState("");

  const d = OASIS_DATA;

  // Pie chart data for Twitter & Reddit
  const twChartData = [
    { name: "Positif", value: d.twSent[0], color: SENT_COLORS.Positif },
    { name: "Netral", value: d.twSent[1], color: SENT_COLORS.Netral },
    { name: "Negatif", value: d.twSent[2], color: SENT_COLORS.Negatif },
  ];

  const rdChartData = [
    { name: "Positif", value: d.rdSent[0], color: SENT_COLORS.Positif },
    { name: "Netral", value: d.rdSent[1], color: SENT_COLORS.Netral },
    { name: "Negatif", value: d.rdSent[2], color: SENT_COLORS.Negatif },
  ];

  // Risk distribution data
  const riskChartData = [
    { name: "Low (<0.35)", count: d.riskDist[0], fill: "#94a3b8" },
    { name: "Medium (0.35-0.6)", count: d.riskDist[1], fill: "#f59e0b" },
    { name: "High (0.6-0.8)", count: d.riskDist[2], fill: "#fb923c" },
    { name: "Fraud (>0.8)", count: d.riskDist[3], fill: "#f43f5e" },
  ];

  // Syndicate hit data
  const syndChartData = Object.entries(d.syndHit).map(([key, val]) => ({
    name: `${key}`,
    modus: val.modus,
    fullName: `${key} · ${val.modus}`,
    hit: val.hit,
    total: val.total,
    rate: val.rate,
  }));

  // Top queue chart data
  const queueChartData = d.queue.slice(0, 10).map((q) => ({
    id: q.id,
    p: q.p,
    modus: q.modus,
    risk: q.risk,
    fill: RISK_COLORS[q.risk] || "#6366f1",
  }));

  // Filtered queue items
  const filteredQueue = React.useMemo(() => {
    return d.queue.filter((item) => {
      if (queueFilter === "kontra" && !item.kontra) return false;
      if (queueFilter === "synd" && item.sindikat === "-") return false;
      if (queueFilter === "nonsynd" && item.sindikat !== "-") return false;
      if (queueSearch.trim()) {
        const query = queueSearch.toLowerCase();
        return (
          item.id.toLowerCase().includes(query) ||
          item.modus.toLowerCase().includes(query) ||
          item.sindikat.toLowerCase().includes(query)
        );
      }
      return true;
    });
  }, [d.queue, queueFilter, queueSearch]);

  // Combined social feeds
  const combinedFeeds = React.useMemo(() => {
    const list: (SocialFeedItem & { platform: "twitter" | "reddit" })[] = [];
    if (feedPlatform === "all" || feedPlatform === "twitter") {
      d.twFeed.forEach((item) => list.push({ ...item, platform: "twitter" }));
    }
    if (feedPlatform === "all" || feedPlatform === "reddit") {
      d.rdFeed.forEach((item) => list.push({ ...item, platform: "reddit" }));
    }

    return list.filter((item) => {
      if (feedSentimentFilter !== "all" && item.sentiment !== feedSentimentFilter) return false;
      if (feedFraudOnly && !item.f_text) return false;
      if (feedSearch.trim()) {
        const q = feedSearch.toLowerCase();
        return item.claim.toLowerCase().includes(q) || item.text.toLowerCase().includes(q);
      }
      return true;
    });
  }, [d.twFeed, d.rdFeed, feedPlatform, feedSentimentFilter, feedFraudOnly, feedSearch]);

  const handlePrint = () => {
    if (typeof window !== "undefined") {
      window.print();
    }
  };

  const handleDownloadJSON = () => {
    const blob = new Blob([JSON.stringify(d, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "payload-aegis-jkn-v2.1.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success("Payload JSON simulasi berhasil diunduh.");
  };

  return (
    <div className="min-h-screen bg-background text-foreground pb-20">
      {/* ── Top Bar / Header ── */}
      <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur-md">
        <div className="container mx-auto max-w-7xl px-4 py-3 sm:px-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <Link
                href="/"
                className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-muted/60 px-2.5 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-muted"
                title="Kembali ke Beranda Aegis-JKN"
              >
                <ArrowLeft className="h-3.5 w-3.5" />
                <span>Beranda</span>
              </Link>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-base sm:text-lg font-bold tracking-tight text-foreground flex items-center gap-2">
                    🛡️ Dashboard Hasil Simulasi Oasis Aegis-JKN
                  </h1>
                  <Badge variant="outline" className="border-emerald-500/30 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-semibold text-[11px]">
                    Protokol v2.1 SESUAI
                  </Badge>
                </div>
                <p className="text-[11px] text-muted-foreground hidden sm:block">
                  Healthkathon BPJS Kesehatan 2026 · 300 Langkah Simulasi Agen Teks (Twitter & Reddit) × MHGSL Late Fusion
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 flex-wrap">
              <Button
                variant="outline"
                size="sm"
                onClick={handlePrint}
                className="no-print h-8 text-xs gap-1.5"
                title="Cetak atau simpan laporan dashboard ke format PDF (Ctrl+P)"
              >
                <Printer className="h-3.5 w-3.5" />
                <span className="hidden md:inline">Cetak / Simpan PDF</span>
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownloadJSON}
                className="no-print h-8 text-xs gap-1.5"
                title="Unduh payload JSON mentah untuk keperluan integrasi"
              >
                <Download className="h-3.5 w-3.5" />
                <span className="hidden md:inline">Unduh JSON</span>
              </Button>
              <a
                href="/dashboard-aegis-jkn.html"
                target="_blank"
                rel="noopener noreferrer"
                className="no-print inline-flex h-8 items-center gap-1 rounded-md border border-border bg-muted/50 px-2.5 text-xs font-medium text-foreground hover:bg-muted"
                title="Buka format standalone HTML Colab murni di tab baru"
              >
                <ExternalLink className="h-3.5 w-3.5" />
                <span className="hidden md:inline">HTML Colab</span>
              </a>
              <ThemeToggle />
            </div>
          </div>
        </div>
      </header>

      {/* ── Main Container ── */}
      <main className="container mx-auto max-w-7xl px-4 pt-6 sm:px-6 space-y-6">
        {/* ── Honesty Alert & Meta Bar ── */}
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 text-xs text-amber-900 dark:text-amber-200">
          <div className="flex items-start gap-2.5">
            <AlertTriangle className="h-4 w-4 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <p className="font-semibold text-amber-800 dark:text-amber-300">
                ⚠️ Kejujuran Label & Protokol Ilmiah:
              </p>
              <p className="leading-relaxed">
                {d.meta.honesty}. Sentimen negatif ≠ bukti fraud — keluhan layanan murni (antrean, kebersihan)
                berfungsi sebagai <em>negative control</em>; sinyal tekstual dikonfirmasi silang dengan skor graf MHGSL
                melalui <em>late fusion</em>.
              </p>
              <div className="flex flex-wrap items-center gap-2 pt-1 font-mono text-[11px] text-amber-700 dark:text-amber-300/80">
                <span>seed: {d.meta.seed}</span>
                <span>•</span>
                <span>versi: {d.meta.version}</span>
                <span>•</span>
                <span>θ_feat: {d.meta.theta_feat}</span>
                <span>•</span>
                <span>γ_text: {d.meta.gamma_text}</span>
                <span>•</span>
                <span>langkah: {d.meta.steps}</span>
                <span>•</span>
                <span>model: {d.meta.model}</span>
              </div>
            </div>
          </div>
        </div>

        {/* ── KPI Summary Cards (6 Metrik Utama) ── */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3.5">
          <Card className="border-border/80 shadow-xs">
            <CardContent className="p-3.5">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                Klaim Sintetis
              </span>
              <div className="text-2xl font-bold text-foreground mt-1">{d.kpi.total_claims}</div>
              <p className="text-[10px] text-muted-foreground mt-0.5">20 pasien · 12 dokter · 6 FKRTL</p>
            </CardContent>
          </Card>

          <Card className="border-border/80 shadow-xs border-l-4 border-l-rose-500">
            <CardContent className="p-3.5">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                Fraud Terdeteksi
              </span>
              <div className="text-2xl font-bold text-rose-600 dark:text-rose-400 mt-1">
                {d.kpi.fraud_detected}/{d.kpi.fraud_total}
              </div>
              <p className="text-[10px] text-muted-foreground mt-0.5">
                {d.kpi.det_rate}% pada antrean ≤{d.kpi.queue_rate}%
              </p>
            </CardContent>
          </Card>

          <Card className="border-border/80 shadow-xs border-l-4 border-l-indigo-500">
            <CardContent className="p-3.5">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                Antrean Investigasi
              </span>
              <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">
                {d.kpi.queue_size}
              </div>
              <p className="text-[10px] text-muted-foreground mt-0.5">
                {d.kpi.queue_rate}% klaim · kontradiksi {d.kpi.kontra_ok}/{d.kpi.kontra_total}
              </p>
            </CardContent>
          </Card>

          <Card className="border-border/80 shadow-xs">
            <CardContent className="p-3.5">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                Sentimen GT (Target)
              </span>
              <div className="text-sm font-bold text-foreground mt-2">
                {d.gtSent[0]}P · {d.gtSent[1]}N · {d.gtSent[2]}Neg
              </div>
              <p className="text-[10px] text-muted-foreground mt-1">62 positif · 14 netral · 24 negatif</p>
            </CardContent>
          </Card>

          <Card className="border-border/80 shadow-xs border-l-4 border-l-emerald-500">
            <CardContent className="p-3.5">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                Akurasi Sentimen
              </span>
              <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">
                {d.kpi.accuracy}%
              </div>
              <p className="text-[10px] text-muted-foreground mt-0.5">leksikon vs GT (200 sampel)</p>
            </CardContent>
          </Card>

          <Card className="border-border/80 shadow-xs border-l-4 border-l-sky-500">
            <CardContent className="p-3.5">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                Efisiensi HITL (ROI)
              </span>
              <div className="text-2xl font-bold text-sky-600 dark:text-sky-400 mt-1">
                ±{d.kpi.capacity.toLocaleString("id-ID")}
              </div>
              <p className="text-[10px] text-muted-foreground mt-0.5">telaah 20→3 mnt/berkas</p>
            </CardContent>
          </Card>
        </div>

        {/* ── Navigation Tabs ── */}
        <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as any)} className="space-y-6">
          <div className="flex items-center justify-between border-b border-border pb-2 flex-wrap gap-2">
            <TabsList className="bg-muted/70">
              <TabsTrigger value="overview" className="text-xs gap-1.5">
                <BarChart3 className="h-3.5 w-3.5" />
                <span>Ringkasan & Visualisasi</span>
              </TabsTrigger>
              <TabsTrigger value="queue" className="text-xs gap-1.5">
                <Layers className="h-3.5 w-3.5" />
                <span>Antrean Late Fusion ({d.queue.length})</span>
              </TabsTrigger>
              <TabsTrigger value="feeds" className="text-xs gap-1.5">
                <MessageSquare className="h-3.5 w-3.5" />
                <span>Log Interaksi Agen ({d.twFeed.length + d.rdFeed.length})</span>
              </TabsTrigger>
              <TabsTrigger value="raw" className="text-xs gap-1.5">
                <ExternalLink className="h-3.5 w-3.5" />
                <span>Format Standalone Colab</span>
              </TabsTrigger>
            </TabsList>
            <div className="text-xs text-muted-foreground flex items-center gap-1.5">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
              <span>4.563 Saluran Fitur Kosinus Dikonfirmasi</span>
            </div>
          </div>

          {/* ═════════════════════════════════════════════════════════════════
              TAB 1: OVERVIEW & CHARTS
          ═════════════════════════════════════════════════════════════════ */}
          <TabsContent value="overview" className="space-y-6 m-0">
            {/* 4 Interactive Charts Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {/* Chart 1: Twitter Sentiment */}
              <Card className="border-border/80">
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                      <span className="text-sky-500 font-normal">🐦</span> Sentimen Simulasi Twitter (24 Log)
                    </CardTitle>
                    <Badge variant="outline" className="text-[10px] text-muted-foreground">
                      Umpan Balik Pasien
                    </Badge>
                  </div>
                  <CardDescription className="text-xs">
                    Distribusi respon pasien terhadap tagihan klaim (Donut Chart)
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-2">
                  <div className="h-56 w-full flex items-center justify-center">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={twChartData}
                          dataKey="value"
                          nameKey="name"
                          cx="50%"
                          cy="50%"
                          innerRadius={50}
                          outerRadius={75}
                          paddingAngle={3}
                        >
                          {twChartData.map((entry, index) => (
                            <Cell key={`tw-cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip
                          formatter={(value: any, name: any) => [`${value} post (${Math.round((Number(value) / 100) * 100)}%)`, name]}
                          contentStyle={{ backgroundColor: "var(--card)", borderColor: "var(--border)", borderRadius: "8px", fontSize: "12px" }}
                        />
                        <Legend
                          verticalAlign="bottom"
                          height={36}
                          formatter={(value) => <span className="text-xs font-medium text-foreground">{value}</span>}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="grid grid-cols-3 gap-2 pt-2 border-t border-border text-center text-xs">
                    <div>
                      <span className="text-emerald-500 font-bold">{d.twSent[0]}</span>
                      <p className="text-[10px] text-muted-foreground">Positif</p>
                    </div>
                    <div>
                      <span className="text-slate-500 font-bold">{d.twSent[1]}</span>
                      <p className="text-[10px] text-muted-foreground">Netral</p>
                    </div>
                    <div>
                      <span className="text-rose-500 font-bold">{d.twSent[2]}</span>
                      <p className="text-[10px] text-muted-foreground">Negatif</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Chart 2: Reddit Sentiment */}
              <Card className="border-border/80">
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                      <span className="text-orange-500 font-normal">💬</span> Sentimen Simulasi Reddit (24 Log)
                    </CardTitle>
                    <Badge variant="outline" className="text-[10px] text-muted-foreground">
                      Diskusi Komunitas & Bot
                    </Badge>
                  </div>
                  <CardDescription className="text-xs">
                    Thread diskusi rumah sakit & komentar otonom verifikator
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-2">
                  <div className="h-56 w-full flex items-center justify-center">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={rdChartData}
                          dataKey="value"
                          nameKey="name"
                          cx="50%"
                          cy="50%"
                          outerRadius={75}
                        >
                          {rdChartData.map((entry, index) => (
                            <Cell key={`rd-cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip
                          formatter={(value: any, name: any) => [`${value} post (${Math.round((Number(value) / 100) * 100)}%)`, name]}
                          contentStyle={{ backgroundColor: "var(--card)", borderColor: "var(--border)", borderRadius: "8px", fontSize: "12px" }}
                        />
                        <Legend
                          verticalAlign="bottom"
                          height={36}
                          formatter={(value) => <span className="text-xs font-medium text-foreground">{value}</span>}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="grid grid-cols-3 gap-2 pt-2 border-t border-border text-center text-xs">
                    <div>
                      <span className="text-emerald-500 font-bold">{d.rdSent[0]}</span>
                      <p className="text-[10px] text-muted-foreground">Positif</p>
                    </div>
                    <div>
                      <span className="text-slate-500 font-bold">{d.rdSent[1]}</span>
                      <p className="text-[10px] text-muted-foreground">Netral</p>
                    </div>
                    <div>
                      <span className="text-rose-500 font-bold">{d.rdSent[2]}</span>
                      <p className="text-[10px] text-muted-foreground">Negatif</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Chart 3: Risk Distribution */}
              <Card className="border-border/80">
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                      <ShieldAlert className="h-4 w-4 text-rose-500" />
                      Distribusi Risiko Ground Truth (100 Klaim)
                    </CardTitle>
                    <Badge variant="outline" className="text-[10px] text-muted-foreground">
                      Target Audit
                    </Badge>
                  </div>
                  <CardDescription className="text-xs">
                    Low (&lt;0.35) · Medium (0.35–0.6) · High (0.6–0.8) · Fraud (&gt;0.8)
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-2">
                  <div className="h-56 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={riskChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" opacity={0.2} vertical={false} />
                        <XAxis dataKey="name" tick={{ fontSize: 10, fill: "var(--muted-foreground)" }} />
                        <YAxis tick={{ fontSize: 10, fill: "var(--muted-foreground)" }} allowDecimals={false} />
                        <Tooltip
                          contentStyle={{ backgroundColor: "var(--card)", borderColor: "var(--border)", borderRadius: "8px", fontSize: "12px" }}
                          formatter={(value) => [`${value} berkas`, "Total"]}
                        />
                        <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                          {riskChartData.map((entry, index) => (
                            <Cell key={`risk-bar-${index}`} fill={entry.fill} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="flex justify-between items-center pt-2 border-t border-border text-[11px] text-muted-foreground">
                    <span>Normal: 76 berkas</span>
                    <span>Anomali Sedang-Tinggi: 10 berkas</span>
                    <span className="font-bold text-rose-500">Kecurangan: 14 berkas (100% terjaring)</span>
                  </div>
                </CardContent>
              </Card>

              {/* Chart 4: Syndicate Hit-Rate */}
              <Card className="border-border/80">
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                      <Sparkles className="h-4 w-4 text-indigo-500" />
                      Hit-Rate per Sindikat pada Antrean Investigasi (%)
                    </CardTitle>
                    <Badge variant="outline" className="text-[10px] text-emerald-600 border-emerald-500/30">
                      100% Sempurna
                    </Badge>
                  </div>
                  <CardDescription className="text-xs">
                    Tingkat isolasi 5 sindikat dengan ragam modus kecurangan JKN
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-2">
                  <div className="h-56 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={syndChartData}
                        layout="vertical"
                        margin={{ top: 5, right: 20, left: 15, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" opacity={0.2} horizontal={false} />
                        <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 10, fill: "var(--muted-foreground)" }} unit="%" />
                        <YAxis dataKey="fullName" type="category" tick={{ fontSize: 10, fill: "var(--foreground)" }} width={120} />
                        <Tooltip
                          contentStyle={{ backgroundColor: "var(--card)", borderColor: "var(--border)", borderRadius: "8px", fontSize: "12px" }}
                          formatter={(value: any, _: any, item: any) => [
                            `${value}% (${item.payload.hit}/${item.payload.total} klaim)`,
                            item.payload.modus,
                          ]}
                        />
                        <Bar dataKey="rate" fill="#6366f1" radius={[0, 4, 4, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="flex justify-between items-center pt-2 border-t border-border text-[11px] text-muted-foreground">
                    <span>Semua 5 sindikat (16 klaim) terdeteksi di 20 berkas teratas</span>
                    <span className="font-bold text-indigo-500">Hit Rate: 16/16 (100%)</span>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Top-10 Fusion Scores Preview */}
            <Card className="border-border/80">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <div>
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                      🎯 Top-10 Skor Late Fusion pada Antrean Investigasi
                    </CardTitle>
                    <CardDescription className="text-xs mt-0.5">
                      Formula: p_fused = p_graph + 0.10 · f_text · (1 − p_graph) · θ_feat = 0.85
                    </CardDescription>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setActiveTab("queue")}
                    className="text-xs gap-1 text-primary hover:text-primary"
                  >
                    <span>Lihat Seluruh 20 Antrean</span>
                    <ChevronRight className="h-3.5 w-3.5" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={queueChartData}
                      layout="vertical"
                      margin={{ top: 5, right: 30, left: 10, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" opacity={0.2} horizontal={false} />
                      <XAxis type="number" domain={[0, 1]} tick={{ fontSize: 10, fill: "var(--muted-foreground)" }} />
                      <YAxis dataKey="id" type="category" tick={{ fontSize: 11, fontWeight: "bold", fill: "var(--foreground)" }} width={70} />
                      <Tooltip
                        contentStyle={{ backgroundColor: "var(--card)", borderColor: "var(--border)", borderRadius: "8px", fontSize: "12px" }}
                        formatter={(val: any, _: any, item: any) => [
                          `p_fused = ${Number(val).toFixed(3)} (${item.payload.modus})`,
                          `Tingkat Risiko: ${item.payload.risk.toUpperCase()}`,
                        ]}
                      />
                      <Bar dataKey="p" radius={[0, 4, 4, 0]}>
                        {queueChartData.map((entry, index) => (
                          <Cell key={`queue-bar-${index}`} fill={entry.fill} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-2 p-3 rounded-lg bg-muted/40 border border-border flex items-center justify-between flex-wrap gap-2 text-xs">
                  <div className="flex items-center gap-4 text-muted-foreground">
                    <span className="flex items-center gap-1.5">
                      <span className="h-2.5 w-2.5 rounded-full bg-rose-500" /> Fraud (14 klaim)
                    </span>
                    <span className="flex items-center gap-1.5">
                      <span className="h-2.5 w-2.5 rounded-full bg-orange-500" /> High Anomali (6 klaim)
                    </span>
                    <span className="flex items-center gap-1.5">
                      <span className="h-2.5 w-2.5 rounded-full bg-amber-500" /> Kontradiksi Teks (8 klaim)
                    </span>
                  </div>
                  <div className="text-muted-foreground">
                    Seluruh 14/14 fraud masuk di antrean prioritas <strong>100% recall</strong>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Validation Protocol Compliance Table */}
            <Card className="border-border/80">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-bold flex items-center gap-2">
                  📋 Matriks Kepatuhan Protokol Validasi v2.1
                </CardTitle>
                <CardDescription className="text-xs">
                  Verifikasi ketat terhadap standar audit kecurangan klaim BPJS Kesehatan
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div className="p-3 rounded-lg border border-border bg-card space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-foreground">1. Kriteria Integritas Graf</span>
                      <Badge className="bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-none">
                        TERPENUHI
                      </Badge>
                    </div>
                    <p className="text-muted-foreground leading-relaxed">
                      Saluran fitur menghubungkan 4.563 edge dengan ambang batas kosinus ≥ 0.85. Deteksi cloning rekam medis KLM016–KLM017 berhasil tertangkap dengan cosine = 1.000.
                    </p>
                  </div>

                  <div className="p-3 rounded-lg border border-border bg-card space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-foreground">2. Kriteria Deteksi & Recall</span>
                      <Badge className="bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-none">
                        TERPENUHI
                      </Badge>
                    </div>
                    <p className="text-muted-foreground leading-relaxed">
                      14 dari 14 berkas fraud (100%) terjaring pada kuota antrean investigasi 20% (target minimal ≥ 90%). Beban verifikator terpangkas hingga 80%.
                    </p>
                  </div>

                  <div className="p-3 rounded-lg border border-border bg-card space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-foreground">3. Kriteria Isolasi Sindikat</span>
                      <Badge className="bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-none">
                        TERPENUHI
                      </Badge>
                    </div>
                    <p className="text-muted-foreground leading-relaxed">
                      Hit-rate 100% pada seluruh 5 sindikat: SYND-01 (Upcoding 3/3), SYND-02 (Phantom Billing 3/3), SYND-03 (Unbundling 6/6), SYND-04 (Drug Diversion 2/2), SYND-05 (Cloning 2/2).
                    </p>
                  </div>

                  <div className="p-3 rounded-lg border border-border bg-card space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-foreground">4. Kriteria Sinyal Kontradiksi</span>
                      <Badge className="bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-none">
                        TERPENUHI
                      </Badge>
                    </div>
                    <p className="text-muted-foreground leading-relaxed">
                      8 dari 8 klaim dengan sinyal kontradiksi tajam (keluhan pasien bertolak belakang dengan tagihan RS) langsung diangkat ke prioritas puncak antrean investigasi.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* ═════════════════════════════════════════════════════════════════
              TAB 2: INVESTIGATION QUEUE
          ═════════════════════════════════════════════════════════════════ */}
          <TabsContent value="queue" className="space-y-4 m-0">
            <Card className="border-border/80">
              <CardHeader className="pb-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                      🎯 Antrean Investigasi Lengkap ({filteredQueue.length} dari {d.queue.length} Berkas)
                    </CardTitle>
                    <CardDescription className="text-xs">
                      Daftar klaim yang diprioritaskan untuk verifikator manusia (HITL) dengan dekomposisi 3 saluran MHGSL
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <div className="relative w-44 sm:w-56">
                      <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-muted-foreground" />
                      <Input
                        placeholder="Cari ID, modus, sindikat..."
                        value={queueSearch}
                        onChange={(e) => setQueueSearch(e.target.value)}
                        className="h-8 pl-8 text-xs"
                      />
                    </div>
                  </div>
                </div>

                {/* Filter Pills */}
                <div className="flex items-center gap-1.5 pt-2 flex-wrap text-xs">
                  <span className="text-muted-foreground text-[11px] mr-1 flex items-center gap-1">
                    <Filter className="h-3 w-3" /> Filter:
                  </span>
                  <Button
                    variant={queueFilter === "all" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setQueueFilter("all")}
                    className="h-7 text-xs px-2.5"
                  >
                    Semua ({d.queue.length})
                  </Button>
                  <Button
                    variant={queueFilter === "kontra" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setQueueFilter("kontra")}
                    className="h-7 text-xs px-2.5 gap-1"
                  >
                    <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
                    Kontradiksi ({d.queue.filter((q) => q.kontra).length})
                  </Button>
                  <Button
                    variant={queueFilter === "synd" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setQueueFilter("synd")}
                    className="h-7 text-xs px-2.5"
                  >
                    Sindikat (16)
                  </Button>
                  <Button
                    variant={queueFilter === "nonsynd" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setQueueFilter("nonsynd")}
                    className="h-7 text-xs px-2.5"
                  >
                    Non-Sindikat (4)
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
                  {filteredQueue.map((item, idx) => {
                    const isFraud = item.risk === "fraud";
                    const hasKontra = item.kontra;
                    return (
                      <div
                        key={item.id}
                        onClick={() => setSelectedClaim(item)}
                        className={cn(
                          "p-3 rounded-lg border transition-all cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs hover:border-primary/60 hover:shadow-xs",
                          selectedClaim?.id === item.id
                            ? "border-primary bg-primary/5"
                            : "border-border bg-card"
                        )}
                      >
                        <div className="flex items-start sm:items-center gap-3">
                          <div className="flex items-center justify-center h-7 w-7 rounded-md bg-muted font-mono font-bold text-xs shrink-0">
                            #{idx + 1}
                          </div>
                          <div className="space-y-1">
                            <div className="flex items-center gap-2 flex-wrap">
                              <span className="font-bold font-mono text-sm text-foreground">
                                {item.id}
                              </span>
                              <span className="font-medium text-foreground">
                                {item.modus}
                              </span>
                              <Badge
                                variant="outline"
                                className={cn(
                                  "text-[10px] py-0 px-1.5 font-semibold",
                                  item.sindikat === "-"
                                    ? "bg-slate-500/10 text-slate-600 dark:text-slate-400 border-slate-500/30"
                                    : "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/30"
                                )}
                              >
                                {item.sindikat === "-" ? "Non-Sindikat" : item.sindikat}
                              </Badge>
                              {hasKontra && (
                                <Badge className="bg-amber-500/15 text-amber-700 dark:text-amber-300 border-amber-500/30 text-[10px] py-0 px-1.5 font-bold">
                                  KONTRADIKSI
                                </Badge>
                              )}
                              <Badge
                                className={cn(
                                  "text-[10px] py-0 px-1.5 font-bold uppercase",
                                  isFraud
                                    ? "bg-rose-500/15 text-rose-600 dark:text-rose-400 border-rose-500/30"
                                    : "bg-orange-500/15 text-orange-600 dark:text-orange-400 border-orange-500/30"
                                )}
                              >
                                {item.risk}
                              </Badge>
                            </div>
                            {/* Decomposed Channels */}
                            <div className="flex items-center gap-3 text-[11px] text-muted-foreground">
                              <span>Dekomposisi Saluran:</span>
                              <span className="font-mono">Fitur: {item.chan.fitur}</span>
                              <span>•</span>
                              <span className="font-mono">Topologi: {item.chan.topologi}</span>
                              <span>•</span>
                              <span className="font-mono">Semantik: {item.chan.semantik}</span>
                            </div>
                          </div>
                        </div>

                        <div className="flex sm:flex-col items-end justify-between sm:justify-center border-t sm:border-t-0 pt-2 sm:pt-0 border-border">
                          <span className="text-[10px] text-muted-foreground">Skor Fusi (p_fused)</span>
                          <span
                            className={cn(
                              "font-mono font-bold text-base",
                              isFraud ? "text-rose-600 dark:text-rose-400" : "text-orange-600 dark:text-orange-400"
                            )}
                          >
                            {item.p.toFixed(3)}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>

            {/* Drilldown Modal / Details of Selected Claim */}
            <AnimatePresence>
              {selectedClaim && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  className="rounded-xl border border-primary/40 bg-card p-5 shadow-md relative space-y-4"
                >
                  <button
                    onClick={() => setSelectedClaim(null)}
                    className="absolute right-4 top-4 text-muted-foreground hover:text-foreground"
                  >
                    <X className="h-4 w-4" />
                  </button>
                  <div className="flex items-center gap-2">
                    <h3 className="text-sm font-bold text-foreground">
                      🔍 Rincian Investigasi Mendalam: Klaim {selectedClaim.id}
                    </h3>
                    <Badge variant="outline" className="text-xs font-semibold">
                      {selectedClaim.modus}
                    </Badge>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                    <div className="p-3 rounded-lg bg-muted/40 border border-border space-y-1">
                      <span className="text-muted-foreground text-[10px] font-semibold uppercase">1. Saluran Fitur Kosinus</span>
                      <div className="text-base font-bold font-mono text-foreground">{selectedClaim.chan.fitur}</div>
                      <p className="text-muted-foreground text-[11px]">
                        Kesamaan vektor atribut ICD, LOS, biaya klaim vs kelompok kontrol faskes selevel.
                      </p>
                    </div>

                    <div className="p-3 rounded-lg bg-muted/40 border border-border space-y-1">
                      <span className="text-muted-foreground text-[10px] font-semibold uppercase">2. Saluran Topologi Graf</span>
                      <div className="text-base font-bold font-mono text-foreground">{selectedClaim.chan.topologi}</div>
                      <p className="text-muted-foreground text-[11px]">
                        Kepadatan subgraph bipartit dokter–pasien & keterikatan sindikat {selectedClaim.sindikat}.
                      </p>
                    </div>

                    <div className="p-3 rounded-lg bg-muted/40 border border-border space-y-1">
                      <span className="text-muted-foreground text-[10px] font-semibold uppercase">3. Saluran Semantik Teks</span>
                      <div className="text-base font-bold font-mono text-foreground">{selectedClaim.chan.semantik}</div>
                      <p className="text-muted-foreground text-[11px]">
                        Ekstraksi leksikal & bukti aduan pasien media sosial (Oasis Agent Twitter/Reddit).
                      </p>
                    </div>
                  </div>

                  {selectedClaim.kontra && (
                    <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 text-xs text-amber-900 dark:text-amber-200">
                      <strong>⚠️ Kontradiksi Prioritas Terdeteksi:</strong> Keluhan pasien di media sosial
                      menunjukkan bahwa prosedur <em>{selectedClaim.modus}</em> tidak pernah dilakukan atau
                      tidak sesuai diagnosis dasar, mengangkat p_fused secara deterministik melalui late fusion.
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </TabsContent>

          {/* ═════════════════════════════════════════════════════════════════
              TAB 3: SOCIAL MEDIA FEEDS (TWITTER & REDDIT AGENTS)
          ═════════════════════════════════════════════════════════════════ */}
          <TabsContent value="feeds" className="space-y-4 m-0">
            <Card className="border-border/80">
              <CardHeader className="pb-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                      💬 Log Interaksi Agen Simulasi Oasis ({combinedFeeds.length} Postingan)
                    </CardTitle>
                    <CardDescription className="text-xs">
                      Postingan umpan balik pasien dan respon bot otonom pada platform Twitter dan Reddit
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <div className="relative w-44 sm:w-56">
                      <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-muted-foreground" />
                      <Input
                        placeholder="Cari klaim atau teks aduan..."
                        value={feedSearch}
                        onChange={(e) => setFeedSearch(e.target.value)}
                        className="h-8 pl-8 text-xs"
                      />
                    </div>
                  </div>
                </div>

                {/* Filters */}
                <div className="flex items-center gap-1.5 pt-2 flex-wrap text-xs">
                  <div className="flex items-center gap-1 border-r border-border pr-2 mr-1">
                    <Button
                      variant={feedPlatform === "all" ? "default" : "outline"}
                      size="sm"
                      onClick={() => setFeedPlatform("all")}
                      className="h-7 text-xs px-2"
                    >
                      Semua Platform
                    </Button>
                    <Button
                      variant={feedPlatform === "twitter" ? "default" : "outline"}
                      size="sm"
                      onClick={() => setFeedPlatform("twitter")}
                      className="h-7 text-xs px-2 gap-1 text-sky-600 dark:text-sky-400"
                    >
                      <span>🐦</span> Twitter ({d.twFeed.length})
                    </Button>
                    <Button
                      variant={feedPlatform === "reddit" ? "default" : "outline"}
                      size="sm"
                      onClick={() => setFeedPlatform("reddit")}
                      className="h-7 text-xs px-2 gap-1 text-orange-600 dark:text-orange-400"
                    >
                      <span>💬</span> Reddit ({d.rdFeed.length})
                    </Button>
                  </div>

                  <Button
                    variant={feedSentimentFilter === "all" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setFeedSentimentFilter("all")}
                    className="h-7 text-xs px-2"
                  >
                    Semua Sentimen
                  </Button>
                  <Button
                    variant={feedSentimentFilter === "Negatif" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setFeedSentimentFilter("Negatif")}
                    className="h-7 text-xs px-2 text-rose-500"
                  >
                    Negatif
                  </Button>
                  <Button
                    variant={feedSentimentFilter === "Netral" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setFeedSentimentFilter("Netral")}
                    className="h-7 text-xs px-2 text-slate-500"
                  >
                    Netral
                  </Button>
                  <Button
                    variant={feedSentimentFilter === "Positif" ? "default" : "outline"}
                    size="sm"
                    onClick={() => setFeedSentimentFilter("Positif")}
                    className="h-7 text-xs px-2 text-emerald-500"
                  >
                    Positif
                  </Button>

                  <Button
                    variant={feedFraudOnly ? "default" : "outline"}
                    size="sm"
                    onClick={() => setFeedFraudOnly(!feedFraudOnly)}
                    className="h-7 text-xs px-2 gap-1 border-amber-500/40 text-amber-600 dark:text-amber-400 ml-auto"
                  >
                    <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
                    Sinyal Fraud Saja (f_text = 1)
                  </Button>
                </div>
              </CardHeader>

              <CardContent>
                <div className="space-y-3 max-h-[650px] overflow-y-auto pr-1">
                  {combinedFeeds.map((item, idx) => {
                    const matchGT = item.sentiment === item.sentiment_gt;
                    const isTwitter = item.platform === "twitter";
                    return (
                      <div
                        key={`${item.platform}-${item.claim}-${idx}`}
                        className="p-4 rounded-xl border border-border bg-card shadow-xs text-xs space-y-2 hover:border-border/80 transition-shadow"
                      >
                        <div className="flex items-center justify-between flex-wrap gap-2">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span
                              className={cn(
                                "flex items-center gap-1 font-bold px-2 py-0.5 rounded text-[11px]",
                                isTwitter
                                  ? "bg-sky-500/10 text-sky-600 dark:text-sky-400"
                                  : "bg-orange-500/10 text-orange-600 dark:text-orange-400"
                              )}
                            >
                              {isTwitter ? "🐦 Twitter" : "💬 Reddit"}
                            </span>
                            <span className="font-mono font-bold text-foreground">
                              📌 {item.claim}
                            </span>
                            <Badge
                              className={cn(
                                "text-[10px] py-0 px-1.5 font-bold uppercase",
                                item.sentiment === "Positif" && "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/30",
                                item.sentiment === "Negatif" && "bg-rose-500/15 text-rose-600 dark:text-rose-400 border-rose-500/30",
                                item.sentiment === "Netral" && "bg-slate-500/15 text-slate-600 dark:text-slate-400 border-slate-500/30"
                              )}
                            >
                              {item.sentiment}
                            </Badge>
                            {Boolean(item.f_text) && (
                              <Badge className="bg-amber-500/15 text-amber-700 dark:text-amber-300 border-amber-500/30 text-[10px] py-0 px-1.5 font-bold">
                                Sinyal Fraud (f_text=1)
                              </Badge>
                            )}
                            <Badge variant="outline" className="text-[10px] text-muted-foreground">
                              {item.source === "ollama" ? "🤖 Mistral Oasis" : "🧮 Heuristik Lokal"}
                            </Badge>
                          </div>

                          <div className="flex items-center gap-2 text-[11px]">
                            <span
                              className={cn(
                                "font-semibold flex items-center gap-1",
                                matchGT ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"
                              )}
                            >
                              {matchGT ? "✓ Sesuai Ground Truth" : `✗ Beda GT (${item.sentiment_gt})`}
                            </span>
                          </div>
                        </div>

                        {/* Post Body */}
                        <div className="pl-3 border-l-2 border-border/80 text-foreground text-[13px] leading-relaxed whitespace-pre-line py-1 bg-muted/20 rounded-r-md">
                          {item.text}
                        </div>

                        {/* Post Footer */}
                        <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-1">
                          <span>{item.step ? `Langkah simulasi #${item.step}` : "Log kompilasi"}</span>
                          <span className="flex items-center gap-1 text-rose-500">
                            <Heart className="h-3 w-3 fill-rose-500/30" /> {item.likes} reaksi
                          </span>
                        </div>
                      </div>
                    );
                  })}
                  {combinedFeeds.length === 0 && (
                    <div className="text-center py-12 text-muted-foreground">
                      Tidak ada postingan yang sesuai dengan filter pencarian.
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* ═════════════════════════════════════════════════════════════════
              TAB 4: RAW STANDALONE COLAB VIEW
          ═════════════════════════════════════════════════════════════════ */}
          <TabsContent value="raw" className="space-y-4 m-0">
            <Card className="border-border/80">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <div>
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                      🌐 Format Asli Colab Output HTML
                    </CardTitle>
                    <CardDescription className="text-xs">
                      Pratinjau langsung file standalone <code>dashboard-aegis-jkn.html</code> yang diekspor dari notebook Colab
                    </CardDescription>
                  </div>
                  <a
                    href="/dashboard-aegis-jkn.html"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-primary font-medium hover:underline"
                  >
                    Buka Halaman Penuh <ExternalLink className="h-3 w-3" />
                  </a>
                </div>
              </CardHeader>
              <CardContent>
                <div className="w-full h-[750px] rounded-lg border border-border overflow-hidden bg-white">
                  <iframe
                    src="/dashboard-aegis-jkn.html"
                    title="Dashboard Aegis JKN Colab Standalone"
                    className="w-full h-full border-0"
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
