"use client";

import * as React from "react";
import Link from "next/link";
import {
  Search,
  Download,
  Database,
  BookOpen,
  FileText,
  ShieldAlert,
  AlertTriangle,
  ArrowLeft,
  ExternalLink,
  Eye,
  RefreshCw,
  FileSpreadsheet,
  Grid,
  List,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Stethoscope,
  Building2,
  DollarSign,
  Network,
  X,
  FileCheck,
  AlertCircle,
  Cpu,
  Fingerprint,
} from "lucide-react";

import { NOTION_RESEARCH_DATASET, NOTION_CLAIMS_DATASET } from "@/data/notion-datasets";
import type { ClaimRecord, ResearchRecord, RiskLevel, ClaimStatus } from "@/types/dataset";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ThemeToggle } from "@/components/mhgsl/theme-toggle";
import { cn } from "@/lib/utils";

// Helper: Format Rupiah
function formatRupiah(amount: number = 0): string {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0,
  }).format(amount || 0);
}

// Helpers for badges styling
function getRiskBadge(risk: string) {
  switch (risk.toLowerCase()) {
    case "fraud":
      return {
        label: "Fraud Terkonfirmasi",
        className: "bg-rose-500/15 text-rose-600 dark:text-rose-400 border-rose-500/30",
        badgeVariant: "destructive" as const,
      };
    case "high":
      return {
        label: "Risiko Tinggi",
        className: "bg-orange-500/15 text-orange-600 dark:text-orange-400 border-orange-500/30",
        badgeVariant: "outline" as const,
      };
    case "medium":
      return {
        label: "Risiko Sedang",
        className: "bg-amber-500/15 text-amber-600 dark:text-amber-400 border-amber-500/30",
        badgeVariant: "outline" as const,
      };
    case "low":
    default:
      return {
        label: "Risiko Rendah",
        className: "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/30",
        badgeVariant: "outline" as const,
      };
  }
}

function getStatusBadge(status: string) {
  switch (status.toLowerCase()) {
    case "escalate":
      return {
        label: "Escalate (Penyidikan)",
        className: "bg-rose-500/15 text-rose-600 dark:text-rose-400 border-rose-500/30",
      };
    case "review":
      return {
        label: "Manual Review",
        className: "bg-amber-500/15 text-amber-600 dark:text-amber-400 border-amber-500/30",
      };
    case "auto_clear":
    default:
      return {
        label: "Auto-Clear (Lolos)",
        className: "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/30",
      };
  }
}

function getRelevanceBadge(relevance: string) {
  switch (relevance) {
    case "Kritis":
      return "bg-rose-500/15 text-rose-600 dark:text-rose-400 border-rose-500/30";
    case "Tinggi":
      return "bg-amber-500/15 text-amber-600 dark:text-amber-400 border-amber-500/30";
    case "Pendukung":
    default:
      return "bg-sky-500/15 text-sky-600 dark:text-sky-400 border-sky-500/30";
  }
}

function getVerificationBadge(status: string) {
  switch (status) {
    case "Terverifikasi":
      return "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/30";
    case "Perlu Verifikasi":
      return "bg-amber-500/15 text-amber-600 dark:text-amber-400 border-amber-500/30";
    case "Sebagian Terverifikasi":
    default:
      return "bg-purple-500/15 text-purple-600 dark:text-purple-400 border-purple-500/30";
  }
}

// Format modus label
function formatModusLabel(modus: string | null): string {
  if (!modus) return "Normal / Standar";
  return modus
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

export function DatasetExplorer() {
  const [activeTab, setActiveTab] = React.useState<string>("claims");
  const [viewMode, setViewMode] = React.useState<"table" | "grid">("table");
  const [researchViewMode, setResearchViewMode] = React.useState<"grid" | "table">("grid");

  // Filter States - Claims
  const [claimSearch, setClaimSearch] = React.useState("");
  const [riskFilter, setRiskFilter] = React.useState<string>("all");
  const [statusFilter, setStatusFilter] = React.useState<string>("all");
  const [serviceFilter, setServiceFilter] = React.useState<string>("all");
  const [modusFilter, setModusFilter] = React.useState<string>("all");
  const [syndicateFilter, setSyndicateFilter] = React.useState<string>("all");
  const [contradictionOnly, setContradictionOnly] = React.useState<boolean>(false);
  const [sortBy, setSortBy] = React.useState<string>("fraud-desc");

  // Pagination - Claims
  const [currentPage, setCurrentPage] = React.useState(1);
  const [pageSize, setPageSize] = React.useState(25);

  // Filter States - Research
  const [researchSearch, setResearchSearch] = React.useState("");
  const [categoryFilter, setCategoryFilter] = React.useState<string>("all");
  const [relevanceFilter, setRelevanceFilter] = React.useState<string>("all");
  const [verificationFilter, setVerificationFilter] = React.useState<string>("all");

  // Selection for Sheet Drawers
  const [selectedClaim, setSelectedClaim] = React.useState<ClaimRecord | null>(null);
  const [selectedResearch, setSelectedResearch] = React.useState<ResearchRecord | null>(null);

  // Extract distinct values
  const distinctModi = React.useMemo(() => {
    const set = new Set<string>();
    NOTION_CLAIMS_DATASET.forEach((c) => {
      if (c.modus) set.add(c.modus);
    });
    return Array.from(set).sort();
  }, []);

  const distinctSyndicates = React.useMemo(() => {
    const set = new Set<string>();
    NOTION_CLAIMS_DATASET.forEach((c) => {
      if (c.sindikat) set.add(c.sindikat);
    });
    return Array.from(set).sort();
  }, []);

  const distinctCategories = React.useMemo(() => {
    const set = new Set<string>();
    NOTION_RESEARCH_DATASET.forEach((r) => set.add(r.kategori));
    return Array.from(set).sort();
  }, []);

  // KPI Metrics Calculations
  const metrics = React.useMemo(() => {
    const totalClaims = NOTION_CLAIMS_DATASET.length;
    let highOrFraud = 0;
    let contradictions = 0;
    const syndicates = new Set<string>();
    let totalCost = 0;

    NOTION_CLAIMS_DATASET.forEach((c) => {
      if (c.risiko === "high" || c.risiko === "fraud") highOrFraud++;
      if (c.kontradiksiNarasi) contradictions++;
      if (c.sindikat) syndicates.add(c.sindikat);
      totalCost += c.biayaRp || 0;
    });

    const totalResearch = NOTION_RESEARCH_DATASET.length;
    const verifiedResearch = NOTION_RESEARCH_DATASET.filter(
      (r) => r.statusVerifikasi === "Terverifikasi"
    ).length;

    return {
      totalClaims,
      highOrFraud,
      contradictions,
      syndicatesCount: syndicates.size,
      totalCost,
      totalResearch,
      verifiedResearch,
    };
  }, []);

  // Filtered Claims
  const filteredClaims = React.useMemo(() => {
    return NOTION_CLAIMS_DATASET.filter((c) => {
      // Search
      if (claimSearch.trim()) {
        const q = claimSearch.toLowerCase().trim();
        const matchesSearch =
          c.id.toLowerCase().includes(q) ||
          c.pasien.toLowerCase().includes(q) ||
          c.dokter.toLowerCase().includes(q) ||
          c.faskes.toLowerCase().includes(q) ||
          c.diagnosisIcd10.toLowerCase().includes(q) ||
          c.prosedurIcd9.toLowerCase().includes(q) ||
          c.obat.toLowerCase().includes(q) ||
          (c.sindikat && c.sindikat.toLowerCase().includes(q)) ||
          (c.modus && c.modus.toLowerCase().includes(q)) ||
          c.rujukan.toLowerCase().includes(q) ||
          c.narasiRekamMedis.toLowerCase().includes(q) ||
          c.alasan.toLowerCase().includes(q);

        if (!matchesSearch) return false;
      }

      // Risk
      if (riskFilter !== "all" && c.risiko !== riskFilter) return false;

      // Status
      if (statusFilter !== "all" && c.status !== statusFilter) return false;

      // Layanan
      if (serviceFilter !== "all" && c.layanan !== serviceFilter) return false;

      // Modus
      if (modusFilter !== "all") {
        if (modusFilter === "none" && c.modus !== null) return false;
        if (modusFilter !== "none" && c.modus !== modusFilter) return false;
      }

      // Sindikat
      if (syndicateFilter !== "all") {
        if (syndicateFilter === "syndicate_only" && !c.sindikat) return false;
        if (syndicateFilter === "no_syndicate" && c.sindikat) return false;
        if (
          syndicateFilter !== "syndicate_only" &&
          syndicateFilter !== "no_syndicate" &&
          c.sindikat !== syndicateFilter
        )
          return false;
      }

      // Contradiction toggle
      if (contradictionOnly && !c.kontradiksiNarasi) return false;

      return true;
    }).sort((a, b) => {
      switch (sortBy) {
        case "fraud-desc":
          return b.skorFraud - a.skorFraud;
        case "fraud-asc":
          return a.skorFraud - b.skorFraud;
        case "cost-desc":
          return b.biayaRp - a.biayaRp;
        case "cost-asc":
          return a.biayaRp - b.biayaRp;
        case "date-desc":
          return b.tanggal.localeCompare(a.tanggal);
        case "date-asc":
          return a.tanggal.localeCompare(b.tanggal);
        case "los-desc":
          return b.losHari - a.losHari;
        case "los-asc":
          return a.losHari - b.losHari;
        case "id-asc":
          return a.id.localeCompare(b.id, undefined, { numeric: true });
        case "id-desc":
          return b.id.localeCompare(a.id, undefined, { numeric: true });
        default:
          return 0;
      }
    });
  }, [
    claimSearch,
    riskFilter,
    statusFilter,
    serviceFilter,
    modusFilter,
    syndicateFilter,
    contradictionOnly,
    sortBy,
  ]);

  // Reset pagination when filters change
  React.useEffect(() => {
    setCurrentPage(1);
  }, [
    claimSearch,
    riskFilter,
    statusFilter,
    serviceFilter,
    modusFilter,
    syndicateFilter,
    contradictionOnly,
    sortBy,
    pageSize,
  ]);

  // Paginated Claims
  const totalPages = Math.ceil(filteredClaims.length / pageSize) || 1;
  const paginatedClaims = React.useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredClaims.slice(start, start + pageSize);
  }, [filteredClaims, currentPage, pageSize]);

  // Filtered Research
  const filteredResearch = React.useMemo(() => {
    return NOTION_RESEARCH_DATASET.filter((r) => {
      if (researchSearch.trim()) {
        const q = researchSearch.toLowerCase().trim();
        const matches =
          r.item.toLowerCase().includes(q) ||
          r.deskripsi.toLowerCase().includes(q) ||
          r.pendekatanTeknis.toLowerCase().includes(q) ||
          r.catatanRiset.toLowerCase().includes(q) ||
          r.kategori.toLowerCase().includes(q);
        if (!matches) return false;
      }

      if (categoryFilter !== "all" && r.kategori !== categoryFilter) return false;
      if (relevanceFilter !== "all" && r.relevansi !== relevanceFilter) return false;
      if (verificationFilter !== "all" && r.statusVerifikasi !== verificationFilter) return false;

      return true;
    });
  }, [researchSearch, categoryFilter, relevanceFilter, verificationFilter]);

  // Check if any claim filter is active
  const isClaimFilterActive =
    claimSearch.trim() !== "" ||
    riskFilter !== "all" ||
    statusFilter !== "all" ||
    serviceFilter !== "all" ||
    modusFilter !== "all" ||
    syndicateFilter !== "all" ||
    contradictionOnly;

  const resetClaimFilters = () => {
    setClaimSearch("");
    setRiskFilter("all");
    setStatusFilter("all");
    setServiceFilter("all");
    setModusFilter("all");
    setSyndicateFilter("all");
    setContradictionOnly(false);
    setSortBy("fraud-desc");
  };

  const isResearchFilterActive =
    researchSearch.trim() !== "" ||
    categoryFilter !== "all" ||
    relevanceFilter !== "all" ||
    verificationFilter !== "all";

  const resetResearchFilters = () => {
    setResearchSearch("");
    setCategoryFilter("all");
    setRelevanceFilter("all");
    setVerificationFilter("all");
  };

  // Export functions (CSV & JSON using native Blob)
  const handleExportClaimsCSV = () => {
    const escapeCSV = (val: unknown) => {
      if (val === null || val === undefined) return '""';
      let str = String(val);
      // Prevent formula injection in spreadsheet software
      if (/^[=+\-@\t\r]/.test(str)) {
        str = "'" + str;
      }
      return `"${str.replace(/"/g, '""')}"`;
    };

    const headers = [
      "ID",
      "Tanggal",
      "Layanan",
      "Faskes",
      "Rujukan",
      "Dokter",
      "Pasien",
      "Diagnosis ICD-10",
      "Prosedur ICD-9",
      "Obat",
      "Biaya (Rp)",
      "LOS (Hari)",
      "Alasan Berobat",
      "Narasi Rekam Medis",
      "Kontradiksi Narasi",
      "Skor Fraud",
      "Risiko",
      "Status",
      "Modus",
      "Sindikat",
      "Sinyal SHAP",
      "Kontribusi Saluran",
      "Sentimen",
      "Skor Sentimen",
      "Umpan Balik Pasien",
      "Alasan Audit",
      "Catatan",
    ];

    const rows = filteredClaims.map((c) =>
      [
        escapeCSV(c.id),
        escapeCSV(c.tanggal),
        escapeCSV(c.layanan),
        escapeCSV(c.faskes),
        escapeCSV(c.rujukan),
        escapeCSV(c.dokter),
        escapeCSV(c.pasien),
        escapeCSV(c.diagnosisIcd10),
        escapeCSV(c.prosedurIcd9),
        escapeCSV(c.obat),
        escapeCSV(c.biayaRp),
        escapeCSV(c.losHari),
        escapeCSV(c.alasanBerobat),
        escapeCSV(c.narasiRekamMedis),
        escapeCSV(c.kontradiksiNarasi ? "YA" : "TIDAK"),
        escapeCSV(c.skorFraud),
        escapeCSV(c.risiko),
        escapeCSV(c.status),
        escapeCSV(c.modus || "-"),
        escapeCSV(c.sindikat || "-"),
        escapeCSV(c.sinyalShap),
        escapeCSV(c.kontribusiSaluran),
        escapeCSV(c.sentimen),
        escapeCSV(c.skorSentimen),
        escapeCSV(c.umpanBalikPasien),
        escapeCSV(c.alasan),
        escapeCSV(c.catatan),
      ].join(",")
    );

    const csvContent = "﻿" + [headers.map(escapeCSV).join(","), ...rows].join("\r\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `aegis-jkn-claims-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  const handleExportClaimsJSON = () => {
    const jsonContent = JSON.stringify(filteredClaims, null, 2);
    const blob = new Blob([jsonContent], { type: "application/json;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `aegis-jkn-claims-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  const handleExportResearchCSV = () => {
    const escapeCSV = (val: unknown) => {
      if (val === null || val === undefined) return '""';
      let str = String(val);
      if (/^[=+\-@\t\r]/.test(str)) {
        str = "'" + str;
      }
      return `"${str.replace(/"/g, '""')}"`;
    };

    const headers = [
      "ID",
      "Item",
      "Kategori",
      "Relevansi",
      "Status Verifikasi",
      "Sumber Riset",
      "Deskripsi",
      "Pendekatan Teknis",
      "Catatan Riset",
      "Notion URL",
    ];

    const rows = filteredResearch.map((r) =>
      [
        escapeCSV(r.id),
        escapeCSV(r.item),
        escapeCSV(r.kategori),
        escapeCSV(r.relevansi),
        escapeCSV(r.statusVerifikasi),
        escapeCSV(r.sumberRiset || "-"),
        escapeCSV(r.deskripsi),
        escapeCSV(r.pendekatanTeknis),
        escapeCSV(r.catatanRiset),
        escapeCSV(r.notionUrl),
      ].join(",")
    );

    const csvContent = "﻿" + [headers.map(escapeCSV).join(","), ...rows].join("\r\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `aegis-jkn-research-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  const handleExportResearchJSON = () => {
    const jsonContent = JSON.stringify(filteredResearch, null, 2);
    const blob = new Blob([jsonContent], { type: "application/json;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `aegis-jkn-research-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-primary/20">
      {/* Top Header Bar */}
      <header className="sticky top-0 z-40 border-b border-border/80 bg-background/80 backdrop-blur-md">
        <div className="container mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6">
          <div className="flex items-center gap-3">
            <Link
              href="/"
              className="inline-flex h-8 items-center gap-1.5 rounded-lg border border-border/70 px-2.5 text-xs font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">Kembali</span>
            </Link>
            <div className="flex items-center gap-2">
              <div
                className="flex h-7 w-7 items-center justify-center rounded-lg shadow-xs"
                style={{
                  background: "linear-gradient(135deg, var(--primary), var(--chart-2))",
                }}
              >
                <Database className="h-3.5 w-3.5 text-primary-foreground" />
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <span className="text-xs font-bold leading-none sm:text-sm">
                    Katalog Dataset Notion
                  </span>
                  <Badge variant="outline" className="h-4 px-1 text-[10px] font-semibold text-primary">
                    v2.1
                  </Badge>
                </div>
                <div className="text-[10px] text-muted-foreground leading-none hidden md:block mt-0.5">
                  Aegis-JKN · MHGSL Multi-Channel Graph Intelligence
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Link
              href="/simulasi"
              className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-600 dark:text-emerald-400 transition-colors hover:bg-emerald-500/20"
            >
              <Sparkles className="h-3 w-3 text-emerald-500" />
              <span className="hidden sm:inline">Hasil</span> Simulasi
            </Link>

            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="container mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8 space-y-6">
        {/* Hero Title & Export Banner */}
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-primary/10 px-2.5 py-0.5 text-[11px] font-semibold text-primary">
              <Database className="h-3 w-3" />
              Repository Data & Knowledge Base
            </div>
            <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl lg:text-4xl">
              Dataset Notion Aegis-JKN
            </h1>
            <p className="text-xs text-muted-foreground sm:text-sm max-w-3xl">
              Repositori komprehensif 300 berkas klaim sintetis BPJS Kesehatan (senilai Rp 3,53 Miliar),
              33 pilar riset literatur multi-channel graph, dan spesifikasi interoperabilitas SATUSEHAT.
            </p>
          </div>

          {/* Export Action Buttons */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="flex items-center gap-1 rounded-lg border border-border p-1 bg-muted/30">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleExportClaimsCSV}
                className="h-7 text-xs px-2.5"
                title="Unduh seluruh atau data klaim yang difilter ke format CSV"
              >
                <Download className="h-3 w-3 mr-1 text-emerald-500" />
                Klaim (CSV)
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleExportClaimsJSON}
                className="h-7 text-xs px-2.5"
                title="Unduh data klaim yang difilter ke format JSON"
              >
                <FileText className="h-3 w-3 mr-1 text-cyan-500" />
                Klaim (JSON)
              </Button>
            </div>

            <div className="flex items-center gap-1 rounded-lg border border-border p-1 bg-muted/30">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleExportResearchCSV}
                className="h-7 text-xs px-2.5"
                title="Unduh 33 basis riset ke CSV"
              >
                <Download className="h-3 w-3 mr-1 text-indigo-500" />
                Riset (CSV)
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleExportResearchJSON}
                className="h-7 text-xs px-2.5"
                title="Unduh 33 basis riset ke JSON"
              >
                <FileText className="h-3 w-3 mr-1 text-purple-500" />
                Riset (JSON)
              </Button>
            </div>
          </div>
        </div>

        {/* KPI Metric Stat Cards (6 Cards) */}
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {/* Card 1: Total Klaim */}
          <Card className="p-3.5 gap-2 border-border/80 bg-card/60 hover:border-primary/40 transition-all card-hover">
            <div className="flex items-center justify-between text-muted-foreground">
              <span className="text-[11px] font-semibold uppercase tracking-wider">Total Klaim</span>
              <FileSpreadsheet className="h-4 w-4 text-primary" />
            </div>
            <div className="text-xl font-bold tracking-tight text-foreground sm:text-2xl">
              {metrics.totalClaims}
            </div>
            <div className="text-[10px] text-muted-foreground flex items-center gap-1">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-500" />
              <span>240 Rawat Inap · 60 Jalan</span>
            </div>
          </Card>

          {/* Card 2: High / Fraud */}
          <Card className="p-3.5 gap-2 border-border/80 bg-card/60 hover:border-rose-500/40 transition-all card-hover">
            <div className="flex items-center justify-between text-muted-foreground">
              <span className="text-[11px] font-semibold uppercase tracking-wider">High / Fraud</span>
              <ShieldAlert className="h-4 w-4 text-rose-500" />
            </div>
            <div className="text-xl font-bold tracking-tight text-rose-600 dark:text-rose-400 sm:text-2xl">
              {metrics.highOrFraud}
            </div>
            <div className="text-[10px] text-muted-foreground flex items-center gap-1">
              <span className="text-rose-500 font-semibold">16.7%</span>
              <span>36 Fraud + 14 Tinggi</span>
            </div>
          </Card>

          {/* Card 3: Kontradiksi Narasi */}
          <Card className="p-3.5 gap-2 border-border/80 bg-card/60 hover:border-amber-500/40 transition-all card-hover">
            <div className="flex items-center justify-between text-muted-foreground">
              <span className="text-[11px] font-semibold uppercase tracking-wider">Kontradiksi</span>
              <AlertTriangle className="h-4 w-4 text-amber-500" />
            </div>
            <div className="text-xl font-bold tracking-tight text-amber-600 dark:text-amber-400 sm:text-2xl">
              {metrics.contradictions}
            </div>
            <div className="text-[10px] text-muted-foreground flex items-center gap-1">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-amber-500" />
              <span>Disparitas Narasi Medis</span>
            </div>
          </Card>

          {/* Card 4: Sindikat Kolusi */}
          <Card className="p-3.5 gap-2 border-border/80 bg-card/60 hover:border-violet-500/40 transition-all card-hover">
            <div className="flex items-center justify-between text-muted-foreground">
              <span className="text-[11px] font-semibold uppercase tracking-wider">Sindikat</span>
              <Network className="h-4 w-4 text-violet-500" />
            </div>
            <div className="text-xl font-bold tracking-tight text-violet-600 dark:text-violet-400 sm:text-2xl">
              {metrics.syndicatesCount}
            </div>
            <div className="text-[10px] text-muted-foreground flex items-center gap-1">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-violet-500" />
              <span>SYND-01 s/d SYND-09</span>
            </div>
          </Card>

          {/* Card 5: Total Nilai Klaim */}
          <Card className="p-3.5 gap-2 border-border/80 bg-card/60 hover:border-cyan-500/40 transition-all card-hover">
            <div className="flex items-center justify-between text-muted-foreground">
              <span className="text-[11px] font-semibold uppercase tracking-wider">Nilai Klaim</span>
              <DollarSign className="h-4 w-4 text-cyan-500" />
            </div>
            <div className="text-xl font-bold tracking-tight text-cyan-600 dark:text-cyan-400 sm:text-2xl">
              Rp 3,53 M
            </div>
            <div className="text-[10px] text-muted-foreground flex items-center gap-1">
              <span>{formatRupiah(metrics.totalCost)}</span>
            </div>
          </Card>

          {/* Card 6: Basis Riset */}
          <Card className="p-3.5 gap-2 border-border/80 bg-card/60 hover:border-indigo-500/40 transition-all card-hover">
            <div className="flex items-center justify-between text-muted-foreground">
              <span className="text-[11px] font-semibold uppercase tracking-wider">Knowledge Base</span>
              <BookOpen className="h-4 w-4 text-indigo-500" />
            </div>
            <div className="text-xl font-bold tracking-tight text-indigo-600 dark:text-indigo-400 sm:text-2xl">
              {metrics.totalResearch}
            </div>
            <div className="text-[10px] text-muted-foreground flex items-center gap-1">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-indigo-500" />
              <span>{metrics.verifiedResearch} Terverifikasi Peer-Rev</span>
            </div>
          </Card>
        </div>

        {/* Interactive Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full space-y-6">
          <TabsList className="h-10 w-full sm:w-auto p-1 bg-muted/60 border border-border">
            <TabsTrigger value="claims" className="flex items-center gap-2 text-xs font-semibold sm:text-sm">
              <Database className="h-4 w-4 text-emerald-500" />
              <span>Dataset Klaim JKN</span>
              <Badge variant="secondary" className="h-5 px-1.5 text-[10px]">
                {filteredClaims.length} / 300
              </Badge>
            </TabsTrigger>
            <TabsTrigger value="research" className="flex items-center gap-2 text-xs font-semibold sm:text-sm">
              <BookOpen className="h-4 w-4 text-indigo-500" />
              <span>Knowledge Base & Riset</span>
              <Badge variant="secondary" className="h-5 px-1.5 text-[10px]">
                {filteredResearch.length} / 33
              </Badge>
            </TabsTrigger>
            <TabsTrigger value="notion_summary" className="flex items-center gap-2 text-xs font-semibold sm:text-sm">
              <FileText className="h-4 w-4 text-cyan-500" />
              <span>Dokumentasi Arsitektur Notion</span>
            </TabsTrigger>
          </TabsList>

          {/* ========================================================================= */}
          {/* TAB 1: DATASET KLAIM JKN (300 KLAIM)                                      */}
          {/* ========================================================================= */}
          <TabsContent value="claims" className="space-y-4 focus-visible:outline-none">
            {/* Filter Bar Card */}
            <Card className="p-4 gap-4 border-border/80 bg-card/60">
              {/* Row 1: Search & View Toggles */}
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Cari ID (KLM...), Pasien, Dokter, Faskes, Diagnosis ICD-10, Sindikat, atau Modus..."
                    value={claimSearch}
                    onChange={(e) => setClaimSearch(e.target.value)}
                    className="pl-9 pr-9 text-xs sm:text-sm bg-background/80"
                  />
                  {claimSearch && (
                    <button
                      onClick={() => setClaimSearch("")}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      <X className="h-3.5 w-3.5" />
                    </button>
                  )}
                </div>

                {/* View Toggles & Table vs Grid */}
                <div className="flex items-center gap-2">
                  <div className="flex items-center rounded-lg border border-border p-1 bg-background/60">
                    <button
                      onClick={() => setViewMode("table")}
                      className={cn(
                        "flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md font-medium transition-colors",
                        viewMode === "table"
                          ? "bg-primary text-primary-foreground shadow-xs"
                          : "text-muted-foreground hover:text-foreground"
                      )}
                      title="Tampilan Tabel"
                    >
                      <List className="h-3.5 w-3.5" />
                      <span className="hidden sm:inline">Tabel</span>
                    </button>
                    <button
                      onClick={() => setViewMode("grid")}
                      className={cn(
                        "flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md font-medium transition-colors",
                        viewMode === "grid"
                          ? "bg-primary text-primary-foreground shadow-xs"
                          : "text-muted-foreground hover:text-foreground"
                      )}
                      title="Tampilan Grid Kartu"
                    >
                      <Grid className="h-3.5 w-3.5" />
                      <span className="hidden sm:inline">Kartu</span>
                    </button>
                  </div>

                  {isClaimFilterActive && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={resetClaimFilters}
                      className="h-8 text-xs text-muted-foreground hover:text-destructive gap-1"
                    >
                      <RefreshCw className="h-3 w-3" />
                      Reset Filter
                    </Button>
                  )}
                </div>
              </div>

              {/* Row 2: Cascading Dropdown Filters */}
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-6 lg:grid-cols-6 pt-2 border-t border-border/50">
                {/* Filter Risiko */}
                <div className="space-y-1">
                  <label className="text-[11px] font-medium text-muted-foreground">Tingkat Risiko</label>
                  <Select value={riskFilter} onValueChange={setRiskFilter}>
                    <SelectTrigger className="h-8 text-xs bg-background/60">
                      <SelectValue placeholder="Semua Risiko" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Semua Risiko</SelectItem>
                      <SelectItem value="low">Rendah (Low - 240)</SelectItem>
                      <SelectItem value="medium">Sedang (Medium - 10)</SelectItem>
                      <SelectItem value="high">Tinggi (High - 14)</SelectItem>
                      <SelectItem value="fraud">Fraud (36)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Filter Status */}
                <div className="space-y-1">
                  <label className="text-[11px] font-medium text-muted-foreground">Status Verifikasi</label>
                  <Select value={statusFilter} onValueChange={setStatusFilter}>
                    <SelectTrigger className="h-8 text-xs bg-background/60">
                      <SelectValue placeholder="Semua Status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Semua Status</SelectItem>
                      <SelectItem value="auto_clear">Auto-Clear (240)</SelectItem>
                      <SelectItem value="review">Manual Review (24)</SelectItem>
                      <SelectItem value="escalate">Escalate (36)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Filter Layanan */}
                <div className="space-y-1">
                  <label className="text-[11px] font-medium text-muted-foreground">Jenis Layanan</label>
                  <Select value={serviceFilter} onValueChange={setServiceFilter}>
                    <SelectTrigger className="h-8 text-xs bg-background/60">
                      <SelectValue placeholder="Semua Layanan" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Semua Layanan</SelectItem>
                      <SelectItem value="rawat inap">Rawat Inap</SelectItem>
                      <SelectItem value="rawat jalan">Rawat Jalan</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Filter Modus */}
                <div className="space-y-1">
                  <label className="text-[11px] font-medium text-muted-foreground">Modus Kecurangan</label>
                  <Select value={modusFilter} onValueChange={setModusFilter}>
                    <SelectTrigger className="h-8 text-xs bg-background/60">
                      <SelectValue placeholder="Semua Modus" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Semua Modus</SelectItem>
                      <SelectItem value="none">Normal (Tanpa Modus)</SelectItem>
                      {distinctModi.map((m) => (
                        <SelectItem key={m} value={m}>
                          {formatModusLabel(m)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Filter Sindikat */}
                <div className="space-y-1">
                  <label className="text-[11px] font-medium text-muted-foreground">Jaringan Sindikat</label>
                  <Select value={syndicateFilter} onValueChange={setSyndicateFilter}>
                    <SelectTrigger className="h-8 text-xs bg-background/60">
                      <SelectValue placeholder="Semua Sindikat" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Semua</SelectItem>
                      <SelectItem value="syndicate_only">Hanya Sindikat (Ada)</SelectItem>
                      <SelectItem value="no_syndicate">Tanpa Sindikat</SelectItem>
                      {distinctSyndicates.map((s) => (
                        <SelectItem key={s} value={s}>
                          {s}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Toggle Kontradiksi Narasi */}
                <div className="space-y-1 flex flex-col justify-end">
                  <label className="text-[11px] font-medium text-muted-foreground">Kontradiksi</label>
                  <button
                    type="button"
                    onClick={() => setContradictionOnly(!contradictionOnly)}
                    aria-pressed={contradictionOnly}
                    className={cn(
                      "flex h-8 w-full items-center justify-between rounded-md border px-2.5 cursor-pointer text-xs transition-colors",
                      contradictionOnly
                        ? "border-amber-500/50 bg-amber-500/15 text-amber-700 dark:text-amber-400 font-semibold"
                        : "border-input bg-background/60 text-muted-foreground hover:bg-accent"
                    )}
                  >
                    <span className="flex items-center gap-1">
                      <AlertTriangle className="h-3 w-3 text-amber-500" />
                      <span>Kontradiksi ({metrics.contradictions})</span>
                    </span>
                    <Switch
                      checked={contradictionOnly}
                      onCheckedChange={setContradictionOnly}
                      className="pointer-events-none scale-75"
                    />
                  </button>
                </div>
              </div>

              {/* Row 3: Sorting & Results Count */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 pt-2 border-t border-border/50 text-xs text-muted-foreground">
                <div className="flex items-center gap-2">
                  <span>
                    Ditemukan <strong className="text-foreground">{filteredClaims.length}</strong> dari 300 berkas
                  </span>
                  {isClaimFilterActive && (
                    <Badge variant="secondary" className="text-[10px] h-4">
                      Filter Aktif
                    </Badge>
                  )}
                </div>

                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1.5">
                    <span>Urutkan:</span>
                    <Select value={sortBy} onValueChange={setSortBy}>
                      <SelectTrigger className="h-7 w-[180px] text-xs bg-background/60">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="fraud-desc">Skor Fraud (Tertinggi)</SelectItem>
                        <SelectItem value="fraud-asc">Skor Fraud (Terendah)</SelectItem>
                        <SelectItem value="cost-desc">Biaya (Tertinggi)</SelectItem>
                        <SelectItem value="cost-asc">Biaya (Terendah)</SelectItem>
                        <SelectItem value="date-desc">Tanggal (Terbaru)</SelectItem>
                        <SelectItem value="date-asc">Tanggal (Terlama)</SelectItem>
                        <SelectItem value="los-desc">Lama Rawat (LOS Terpanjang)</SelectItem>
                        <SelectItem value="id-asc">ID Klaim (A-Z)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <span>Baris:</span>
                    <Select
                      value={String(pageSize)}
                      onValueChange={(val) => setPageSize(Number(val))}
                    >
                      <SelectTrigger className="h-7 w-[70px] text-xs bg-background/60">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="10">10</SelectItem>
                        <SelectItem value="25">25</SelectItem>
                        <SelectItem value="50">50</SelectItem>
                        <SelectItem value="100">100</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>
            </Card>

            {/* View Mode: TABLE */}
            {viewMode === "table" && (
              <Card className="border-border/80 overflow-hidden">
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader className="bg-muted/40">
                      <TableRow className="hover:bg-transparent">
                        <TableHead className="w-[110px] text-xs font-semibold">ID & Tanggal</TableHead>
                        <TableHead className="min-w-[180px] text-xs font-semibold">Pasien & RS</TableHead>
                        <TableHead className="min-w-[170px] text-xs font-semibold">Dokter & Layanan</TableHead>
                        <TableHead className="min-w-[210px] text-xs font-semibold">Diagnosis (ICD-10)</TableHead>
                        <TableHead className="text-right text-xs font-semibold">Biaya (Rp)</TableHead>
                        <TableHead className="text-center text-xs font-semibold min-w-[120px]">
                          Skor Fraud
                        </TableHead>
                        <TableHead className="text-center text-xs font-semibold">Status</TableHead>
                        <TableHead className="min-w-[140px] text-xs font-semibold">Modus & Sindikat</TableHead>
                        <TableHead className="text-center w-[80px] text-xs font-semibold">Aksi</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {paginatedClaims.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={9} className="h-32 text-center text-muted-foreground">
                            <div className="flex flex-col items-center justify-center gap-2">
                              <AlertCircle className="h-6 w-6 text-muted-foreground/60" />
                              <p className="text-sm font-medium">Tidak ada klaim yang cocok dengan kriteria filter.</p>
                              <Button variant="outline" size="sm" onClick={resetClaimFilters} className="text-xs">
                                Reset Semua Filter
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ) : (
                        paginatedClaims.map((claim) => {
                          const riskInfo = getRiskBadge(claim.risiko);
                          const statusInfo = getStatusBadge(claim.status);

                          return (
                            <TableRow
                              key={claim.id}
                              className={cn(
                                "cursor-pointer transition-colors group",
                                claim.risiko === "fraud"
                                  ? "hover:bg-rose-500/5 bg-rose-500/[0.02]"
                                  : claim.risiko === "high"
                                  ? "hover:bg-orange-500/5 bg-orange-500/[0.02]"
                                  : "hover:bg-accent/40"
                              )}
                              onClick={() => setSelectedClaim(claim)}
                            >
                              {/* ID & Date */}
                              <TableCell className="font-mono text-xs py-3">
                                <div className="font-bold text-foreground group-hover:text-primary flex items-center gap-1">
                                  <span>{claim.id}</span>
                                  {claim.kontradiksiNarasi && (
                                    <span title="Terdeteksi Kontradiksi Narasi Rekam Medis">
                                      <AlertTriangle className="h-3 w-3 text-amber-500 inline shrink-0" />
                                    </span>
                                  )}
                                </div>
                                <div className="text-[10px] text-muted-foreground">{claim.tanggal}</div>
                              </TableCell>

                              {/* Patient & Hospital */}
                              <TableCell className="text-xs py-3">
                                <div className="font-medium text-foreground line-clamp-1">{claim.pasien}</div>
                                <div className="text-[11px] text-muted-foreground flex items-center gap-1 line-clamp-1">
                                  <Building2 className="h-3 w-3 shrink-0" />
                                  <span>{claim.faskes}</span>
                                </div>
                              </TableCell>

                              {/* Doctor & Service */}
                              <TableCell className="text-xs py-3">
                                <div className="font-medium text-foreground line-clamp-1">{claim.dokter}</div>
                                <div className="text-[11px] text-muted-foreground flex items-center gap-1">
                                  <span className="capitalize">{claim.layanan}</span>
                                  <span>·</span>
                                  <span>LOS {claim.losHari} hr</span>
                                </div>
                              </TableCell>

                              {/* Diagnosis ICD-10 */}
                              <TableCell className="text-xs py-3">
                                <div className="font-medium line-clamp-1" title={claim.diagnosisIcd10}>
                                  {claim.diagnosisIcd10}
                                </div>
                                <div className="text-[11px] text-muted-foreground line-clamp-1" title={claim.prosedurIcd9}>
                                  {claim.prosedurIcd9}
                                </div>
                              </TableCell>

                              {/* Cost */}
                              <TableCell className="text-right text-xs font-semibold py-3">
                                <span className={claim.biayaRp > 20000000 ? "text-rose-600 dark:text-rose-400 font-bold" : ""}>
                                  {formatRupiah(claim.biayaRp)}
                                </span>
                              </TableCell>

                              {/* Fraud Score & Risk */}
                              <TableCell className="text-center py-3">
                                <div className="flex flex-col items-center gap-1">
                                  <div className="flex items-center gap-1.5 font-mono text-xs font-bold">
                                    <span>{(claim.skorFraud * 100).toFixed(0)}%</span>
                                    <Badge
                                      variant="outline"
                                      className={cn("h-4 px-1 text-[9px] uppercase font-bold", riskInfo.className)}
                                    >
                                      {claim.risiko}
                                    </Badge>
                                  </div>
                                  <div className="w-16 h-1.5 rounded-full bg-muted overflow-hidden">
                                    <div
                                      className={cn(
                                        "h-full rounded-full transition-all",
                                        claim.skorFraud >= 0.7
                                          ? "bg-rose-500"
                                          : claim.skorFraud >= 0.4
                                          ? "bg-amber-500"
                                          : "bg-emerald-500"
                                      )}
                                      style={{ width: `${Math.min(100, Math.max(5, claim.skorFraud * 100))}%` }}
                                    />
                                  </div>
                                </div>
                              </TableCell>

                              {/* Status */}
                              <TableCell className="text-center py-3">
                                <span
                                  className={cn(
                                    "inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold border",
                                    statusInfo.className
                                  )}
                                >
                                  {claim.status === "auto_clear"
                                    ? "Auto Clear"
                                    : claim.status === "review"
                                    ? "Review"
                                    : "Escalate"}
                                </span>
                              </TableCell>

                              {/* Modus & Syndicate */}
                              <TableCell className="text-xs py-3">
                                {claim.modus ? (
                                  <div className="space-y-0.5">
                                    <div className="text-[11px] font-semibold text-rose-600 dark:text-rose-400">
                                      {formatModusLabel(claim.modus)}
                                    </div>
                                    {claim.sindikat && (
                                      <Badge variant="outline" className="text-[9px] h-3.5 px-1 bg-violet-500/10 text-violet-600 dark:text-violet-400 border-violet-500/30">
                                        {claim.sindikat}
                                      </Badge>
                                    )}
                                  </div>
                                ) : (
                                  <span className="text-[11px] text-muted-foreground italic">Normal</span>
                                )}
                              </TableCell>

                              {/* Actions */}
                              <TableCell className="text-center py-3">
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    setSelectedClaim(claim);
                                  }}
                                  className="h-7 w-7 p-0"
                                  title="Lihat Detail Klaim"
                                >
                                  <Eye className="h-3.5 w-3.5 text-muted-foreground group-hover:text-primary" />
                                </Button>
                              </TableCell>
                            </TableRow>
                          );
                        })
                      )}
                    </TableBody>
                  </Table>
                </div>
              </Card>
            )}

            {/* View Mode: GRID KARTU */}
            {viewMode === "grid" && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {paginatedClaims.length === 0 ? (
                  <div className="col-span-full h-40 flex flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-border p-6 text-center">
                    <AlertCircle className="h-6 w-6 text-muted-foreground" />
                    <p className="text-sm font-medium">Tidak ada klaim yang cocok dengan filter yang dipilih.</p>
                    <Button variant="outline" size="sm" onClick={resetClaimFilters} className="text-xs">
                      Reset Filter
                    </Button>
                  </div>
                ) : (
                  paginatedClaims.map((claim) => {
                    const riskInfo = getRiskBadge(claim.risiko);
                    const statusInfo = getStatusBadge(claim.status);

                    return (
                      <Card
                        key={claim.id}
                        onClick={() => setSelectedClaim(claim)}
                        className={cn(
                          "p-4 gap-3 border-border/80 bg-card/60 cursor-pointer transition-all card-hover group relative",
                          claim.risiko === "fraud"
                            ? "hover:border-rose-500/50 bg-rose-500/[0.02]"
                            : claim.risiko === "high"
                            ? "hover:border-orange-500/50 bg-orange-500/[0.02]"
                            : "hover:border-primary/50"
                        )}
                      >
                        {/* Header: ID, Date, Badges */}
                        <div className="flex items-start justify-between gap-2">
                          <div>
                            <div className="flex items-center gap-1.5 font-mono text-sm font-bold text-foreground group-hover:text-primary">
                              <span>{claim.id}</span>
                              {claim.sindikat && (
                                <Badge variant="outline" className="text-[10px] h-4 px-1 bg-violet-500/10 text-violet-600 border-violet-500/30">
                                  {claim.sindikat}
                                </Badge>
                              )}
                            </div>
                            <div className="text-[11px] text-muted-foreground">{claim.tanggal}</div>
                          </div>

                          <div className="flex flex-col items-end gap-1">
                            <Badge variant="outline" className={cn("text-[10px] h-5 px-1.5 font-bold uppercase", riskInfo.className)}>
                              {claim.risiko} ({(claim.skorFraud * 100).toFixed(0)}%)
                            </Badge>
                            <span className={cn("text-[9px] px-1.5 py-0.2 rounded border font-medium", statusInfo.className)}>
                              {claim.status}
                            </span>
                          </div>
                        </div>

                        {/* Medical Info */}
                        <div className="space-y-1 text-xs">
                          <div className="font-semibold text-foreground line-clamp-1">{claim.pasien}</div>
                          <div className="text-muted-foreground flex items-center gap-1 text-[11px] line-clamp-1">
                            <Building2 className="h-3 w-3 shrink-0" />
                            <span>{claim.faskes}</span>
                            <span>·</span>
                            <span className="capitalize">{claim.layanan}</span>
                          </div>
                          <div className="text-muted-foreground flex items-center gap-1 text-[11px] line-clamp-1">
                            <Stethoscope className="h-3 w-3 shrink-0" />
                            <span>{claim.dokter}</span>
                          </div>
                        </div>

                        {/* Diagnosis */}
                        <div className="rounded-lg bg-muted/40 p-2 text-xs space-y-1">
                          <div className="font-medium text-foreground line-clamp-1" title={claim.diagnosisIcd10}>
                            {claim.diagnosisIcd10}
                          </div>
                          <div className="text-[11px] text-muted-foreground line-clamp-1" title={claim.prosedurIcd9}>
                            {claim.prosedurIcd9}
                          </div>
                        </div>

                        {/* Contradiction Warning Pill if applicable */}
                        {claim.kontradiksiNarasi && (
                          <div className="flex items-center gap-1.5 rounded-md border border-amber-500/30 bg-amber-500/10 px-2.5 py-1 text-[11px] font-medium text-amber-700 dark:text-amber-400">
                            <AlertTriangle className="h-3.5 w-3.5 text-amber-500 shrink-0" />
                            <span className="line-clamp-1">Inkonsistensi Narasi Rekam Medis vs Tagihan</span>
                          </div>
                        )}

                        {/* Modus notification */}
                        {claim.modus && (
                          <div className="text-[11px] font-semibold text-rose-600 dark:text-rose-400 flex items-center gap-1">
                            <ShieldAlert className="h-3.5 w-3.5 shrink-0" />
                            <span>Modus: {formatModusLabel(claim.modus)}</span>
                          </div>
                        )}

                        {/* Footer: Financial & Actions */}
                        <div className="flex items-center justify-between pt-2 border-t border-border/60 text-xs">
                          <div>
                            <div className="text-[10px] text-muted-foreground">Total Biaya (LOS {claim.losHari}h)</div>
                            <div className="font-bold text-foreground">
                              {formatRupiah(claim.biayaRp)}
                            </div>
                          </div>

                          <Button
                            variant="secondary"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedClaim(claim);
                            }}
                            className="h-7 text-xs px-2.5"
                          >
                            Detail Klaim
                          </Button>
                        </div>
                      </Card>
                    );
                  })
                )}
              </div>
            )}

            {/* Pagination Controls */}
            {filteredClaims.length > 0 && (
              <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-3 text-xs text-muted-foreground">
                <div>
                  Menampilkan{" "}
                  <strong className="text-foreground">
                    {Math.min(filteredClaims.length, (currentPage - 1) * pageSize + 1)}
                  </strong>{" "}
                  sampai{" "}
                  <strong className="text-foreground">
                    {Math.min(filteredClaims.length, currentPage * pageSize)}
                  </strong>{" "}
                  dari <strong className="text-foreground">{filteredClaims.length}</strong> klaim
                </div>

                <div className="flex items-center gap-1">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                    aria-label="Halaman sebelumnya"
                    className="h-8 px-2 text-xs"
                  >
                    <ChevronLeft className="h-3.5 w-3.5 mr-1" />
                    Sebelumnya
                  </Button>

                  <div className="flex items-center gap-1 px-2">
                    <span className="font-semibold text-foreground">{currentPage}</span>
                    <span>/</span>
                    <span>{totalPages}</span>
                  </div>

                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                    disabled={currentPage === totalPages}
                    aria-label="Halaman selanjutnya"
                    className="h-8 px-2 text-xs"
                  >
                    Selanjutnya
                    <ChevronRight className="h-3.5 w-3.5 ml-1" />
                  </Button>
                </div>
              </div>
            )}
          </TabsContent>

          {/* ========================================================================= */}
          {/* TAB 2: KNOWLEDGE BASE & RISET (33 ITEM)                                   */}
          {/* ========================================================================= */}
          <TabsContent value="research" className="space-y-4 focus-visible:outline-none">
            {/* Filter Card for Research */}
            <Card className="p-4 gap-4 border-border/80 bg-card/60">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Cari riset AI, algoritma (MHGSL, SHAP, DP-CTGAN), regulasi (UU PDP), atau metrik..."
                    value={researchSearch}
                    onChange={(e) => setResearchSearch(e.target.value)}
                    className="pl-9 pr-9 text-xs sm:text-sm bg-background/80"
                  />
                  {researchSearch && (
                    <button
                      onClick={() => setResearchSearch("")}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      <X className="h-3.5 w-3.5" />
                    </button>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  <div className="flex items-center rounded-lg border border-border p-1 bg-background/60">
                    <button
                      onClick={() => setResearchViewMode("grid")}
                      className={cn(
                        "flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md font-medium transition-colors",
                        researchViewMode === "grid"
                          ? "bg-primary text-primary-foreground shadow-xs"
                          : "text-muted-foreground hover:text-foreground"
                      )}
                    >
                      <Grid className="h-3.5 w-3.5" />
                      <span>Kartu</span>
                    </button>
                    <button
                      onClick={() => setResearchViewMode("table")}
                      className={cn(
                        "flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md font-medium transition-colors",
                        researchViewMode === "table"
                          ? "bg-primary text-primary-foreground shadow-xs"
                          : "text-muted-foreground hover:text-foreground"
                      )}
                    >
                      <List className="h-3.5 w-3.5" />
                      <span>Tabel</span>
                    </button>
                  </div>

                  {isResearchFilterActive && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={resetResearchFilters}
                      className="h-8 text-xs text-muted-foreground hover:text-destructive gap-1"
                    >
                      <RefreshCw className="h-3 w-3" />
                      Reset
                    </Button>
                  )}
                </div>
              </div>

              {/* Dropdown Filters */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-2 border-t border-border/50">
                {/* Kategori */}
                <div className="space-y-1">
                  <label className="text-[11px] font-medium text-muted-foreground">Kategori Riset</label>
                  <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                    <SelectTrigger className="h-8 text-xs bg-background/60">
                      <SelectValue placeholder="Semua Kategori" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Semua Kategori (8)</SelectItem>
                      {distinctCategories.map((c) => (
                        <SelectItem key={c} value={c}>
                          {c}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Relevansi */}
                <div className="space-y-1">
                  <label className="text-[11px] font-medium text-muted-foreground">Tingkat Relevansi</label>
                  <Select value={relevanceFilter} onValueChange={setRelevanceFilter}>
                    <SelectTrigger className="h-8 text-xs bg-background/60">
                      <SelectValue placeholder="Semua Relevansi" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Semua Relevansi</SelectItem>
                      <SelectItem value="Kritis">Kritis (11 item)</SelectItem>
                      <SelectItem value="Tinggi">Tinggi (18 item)</SelectItem>
                      <SelectItem value="Pendukung">Pendukung (4 item)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Status Verifikasi */}
                <div className="space-y-1">
                  <label className="text-[11px] font-medium text-muted-foreground">Status Verifikasi</label>
                  <Select value={verificationFilter} onValueChange={setVerificationFilter}>
                    <SelectTrigger className="h-8 text-xs bg-background/60">
                      <SelectValue placeholder="Semua Status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Semua Status</SelectItem>
                      <SelectItem value="Terverifikasi">Terverifikasi (18 item)</SelectItem>
                      <SelectItem value="Sebagian Terverifikasi">Sebagian Terverifikasi (11 item)</SelectItem>
                      <SelectItem value="Perlu Verifikasi">Perlu Verifikasi (4 item)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </Card>

            {/* Research View Mode: GRID */}
            {researchViewMode === "grid" && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredResearch.map((item) => (
                  <Card
                    key={item.id}
                    onClick={() => setSelectedResearch(item)}
                    className="p-5 gap-3.5 border-border/80 bg-card/60 hover:border-indigo-500/50 cursor-pointer transition-all card-hover group flex flex-col justify-between"
                  >
                    <div className="space-y-3">
                      {/* Top Badges */}
                      <div className="flex flex-wrap items-center gap-1.5">
                        <Badge variant="outline" className="text-[10px] h-5 px-1.5 font-semibold bg-muted/50">
                          {item.kategori}
                        </Badge>
                        <Badge
                          variant="outline"
                          className={cn("text-[10px] h-5 px-1.5 font-semibold", getRelevanceBadge(item.relevansi))}
                        >
                          {item.relevansi}
                        </Badge>
                        <Badge
                          variant="outline"
                          className={cn("text-[10px] h-5 px-1.5 font-semibold", getVerificationBadge(item.statusVerifikasi))}
                        >
                          {item.statusVerifikasi}
                        </Badge>
                      </div>

                      {/* Title */}
                      <h3 className="text-sm font-bold text-foreground group-hover:text-primary transition-colors leading-snug">
                        {item.item}
                      </h3>

                      {/* Description */}
                      <p className="text-xs text-muted-foreground line-clamp-3 leading-relaxed">
                        {item.deskripsi}
                      </p>

                      {/* Technical Approach Highlight */}
                      <div className="rounded-lg border border-border/50 bg-muted/40 p-2.5 text-xs">
                        <div className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground mb-1">
                          Pendekatan Teknis
                        </div>
                        <p className="text-foreground line-clamp-2 leading-relaxed">
                          {item.pendekatanTeknis}
                        </p>
                      </div>
                    </div>

                    {/* Footer Actions */}
                    <div className="flex items-center justify-between pt-3 border-t border-border/50 text-xs">
                      {item.sumberRiset ? (
                        <a
                          href={item.sumberRiset}
                          target="_blank"
                          rel="noopener noreferrer"
                          onClick={(e) => e.stopPropagation()}
                          className="inline-flex items-center gap-1 text-primary hover:underline font-medium text-[11px]"
                        >
                          <ExternalLink className="h-3 w-3" />
                          <span>Buka Paper / Rujukan</span>
                        </a>
                      ) : (
                        <span className="text-[11px] text-muted-foreground italic">Dokumentasi Internal</span>
                      )}

                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedResearch(item);
                        }}
                        className="h-7 text-xs px-2"
                      >
                        Detail Telaah
                      </Button>
                    </div>
                  </Card>
                ))}
              </div>
            )}

            {/* Research View Mode: TABLE */}
            {researchViewMode === "table" && (
              <Card className="border-border/80 overflow-hidden">
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader className="bg-muted/40">
                      <TableRow>
                        <TableHead className="min-w-[220px] text-xs font-semibold">Judul Riset / Komponen</TableHead>
                        <TableHead className="w-[140px] text-xs font-semibold">Kategori</TableHead>
                        <TableHead className="w-[100px] text-xs font-semibold">Relevansi</TableHead>
                        <TableHead className="w-[140px] text-xs font-semibold">Status Verifikasi</TableHead>
                        <TableHead className="min-w-[200px] text-xs font-semibold">Deskripsi</TableHead>
                        <TableHead className="text-center w-[120px] text-xs font-semibold">Rujukan</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredResearch.map((item) => (
                        <TableRow
                          key={item.id}
                          onClick={() => setSelectedResearch(item)}
                          className="cursor-pointer hover:bg-accent/40"
                        >
                          <TableCell className="font-semibold text-xs py-3 text-foreground">
                            {item.item}
                          </TableCell>
                          <TableCell className="text-xs py-3">
                            <Badge variant="outline" className="text-[10px]">
                              {item.kategori}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-xs py-3">
                            <Badge
                              variant="outline"
                              className={cn("text-[10px]", getRelevanceBadge(item.relevansi))}
                            >
                              {item.relevansi}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-xs py-3">
                            <Badge
                              variant="outline"
                              className={cn("text-[10px]", getVerificationBadge(item.statusVerifikasi))}
                            >
                              {item.statusVerifikasi}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-xs py-3 text-muted-foreground line-clamp-2">
                            {item.deskripsi}
                          </TableCell>
                          <TableCell className="text-center text-xs py-3">
                            {item.sumberRiset ? (
                              <a
                                href={item.sumberRiset}
                                target="_blank"
                                rel="noopener noreferrer"
                                onClick={(e) => e.stopPropagation()}
                                className="inline-flex items-center gap-1 text-primary hover:underline text-xs"
                              >
                                <ExternalLink className="h-3 w-3" />
                                <span>Tautan</span>
                              </a>
                            ) : (
                              <span className="text-muted-foreground text-[11px]">-</span>
                            )}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </Card>
            )}
          </TabsContent>

          {/* ========================================================================= */}
          {/* TAB 3: RINGKASAN DOKUMEN NOTION (ARSITEKTUR, INTEROP, GROUND TRUTH)        */}
          {/* ========================================================================= */}
          <TabsContent value="notion_summary" className="space-y-6 focus-visible:outline-none">
            {/* Header intro */}
            <Card className="p-6 border-border/80 bg-gradient-to-br from-primary/5 via-card to-background">
              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary/10 border border-primary/20 text-primary">
                  <Cpu className="h-6 w-6" />
                </div>
                <div className="space-y-1">
                  <h2 className="text-lg font-bold sm:text-xl">
                    Dokumentasi Arsitektur Sistem & Spesifikasi Notion Aegis-JKN
                  </h2>
                  <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
                    Ringkasan terstruktur dari seluruh dokumen riset teknis, rancangan alur data,
                    dan konfigurasi ground truth yang disinkronkan secara langsung dari basis data Notion Aegis-JKN.
                  </p>
                </div>
              </div>
            </Card>

            {/* 3 Main Pillars Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Pillar 1: Multi-Channel Graph MHGSL */}
              <Card className="p-5 gap-3 border-border/80 bg-card/60 flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-primary font-semibold text-sm">
                    <Network className="h-4 w-4" />
                    <span>3 Saluran Graf MHGSL</span>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    Representasi heterogen yang memisahkan kanal graf agar sinyal relasi tidak saling meredam:
                  </p>
                  <ul className="space-y-2 text-xs">
                    <li className="rounded-md bg-muted/40 p-2">
                      <strong className="text-foreground">1. Kanal Topologi ($A_{`\\text{topo}`}$):</strong> Relasi eksplisit
                      Pasien $\leftrightarrow$ Dokter $\leftrightarrow$ Faskes $\leftrightarrow$ Rujukan. Mendeteksi
                      subgraf padat kolusi sindikat.
                    </li>
                    <li className="rounded-md bg-muted/40 p-2">
                      <strong className="text-foreground">2. Kanal Fitur ($A_{`\\text{feat}`}$):</strong> Graf kedekatan k-NN
                      berbasis kemiripan kosinus (Cosine Similarity) pada pola biaya, LOS, dan obat mahal.
                    </li>
                    <li className="rounded-md bg-muted/40 p-2">
                      <strong className="text-foreground">3. Kanal Semantik ($A_{`\\text{sem}`}$):</strong> Meta-path klinis
                      (Pasien $\to$ Diagnosis ICD-10 $\to$ Tindakan ICD-9 $\to$ Obat).
                    </li>
                  </ul>
                </div>
                <div className="pt-3 border-t border-border/50 text-[11px] text-muted-foreground">
                  Diproses oleh Channel-Specific GCN + Shared-Parameter GCN dengan Late Fusion.
                </div>
              </Card>

              {/* Pillar 2: Interoperabilitas SATUSEHAT */}
              <Card className="p-5 gap-3 border-border/80 bg-card/60 flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-cyan-600 dark:text-cyan-400 font-semibold text-sm">
                    <Fingerprint className="h-4 w-4" />
                    <span>Interoperabilitas SATUSEHAT</span>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    Menghubungkan ekosistem rekam medis nasional Kemenkes dan V-Claim BPJS:
                  </p>
                  <ul className="space-y-2 text-xs">
                    <li className="rounded-md bg-muted/40 p-2">
                      <strong className="text-foreground">Standar HL7 FHIR R4:</strong> Ingestion resource
                      `Patient`, `Encounter`, `Condition` (ICD-10), `Procedure` (ICD-9), dan `MedicationRequest`.
                    </li>
                    <li className="rounded-md bg-muted/40 p-2">
                      <strong className="text-foreground">Kepatuhan UU No. 27/2022 (UU PDP):</strong> Data kesehatan sebagai
                      data spesifik. Pelatihan model memakai generator sintetis DP-CTGAN dengan privasi diferensial.
                    </li>
                    <li className="rounded-md bg-muted/40 p-2">
                      <strong className="text-foreground">Integrasi V-Claim / E-Klaim:</strong> Komparasi tarif paket INA-CBG
                      vs biaya riil rumah sakit secara real-time sebelum klaim disetujui.
                    </li>
                  </ul>
                </div>
                <div className="pt-3 border-t border-border/50 text-[11px] text-muted-foreground">
                  Mengurangi waktu telaah berkas dari 20 menit menjadi 3 menit (efisiensi ×6,7).
                </div>
              </Card>

              {/* Pillar 3: Late Fusion & XAI */}
              <Card className="p-5 gap-3 border-border/80 bg-card/60 flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400 font-semibold text-sm">
                    <Sparkles className="h-4 w-4" />
                    <span>Late Fusion & XAI (SHAP)</span>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    Kombinasi ansambel yang mencegah false positive dan meredam alert fatigue auditor:
                  </p>
                  <ul className="space-y-2 text-xs">
                    <li className="rounded-md bg-muted/40 p-2">
                      <strong className="text-foreground">Late Fusion:</strong> Penggabungan output graf MHGSL
                      dengan model tabular XGBoost + SMOTE via pembobotan adaptif.
                    </li>
                    <li className="rounded-md bg-muted/40 p-2">
                      <strong className="text-foreground">Camouflage Masking:</strong> Algoritma filter khusus
                      untuk menggagalkan sindikat yang sengaja mencampurkan klaim wajar sebagai kamuflase.
                    </li>
                    <li className="rounded-md bg-muted/40 p-2">
                      <strong className="text-foreground">Explainable AI (SHAP):</strong> Auditor menerima kartu alasan
                      audit transparan (mis. probabilitas 92% dipicu tarif implan +40% dan durasi rawat +35%).
                    </li>
                  </ul>
                </div>
                <div className="pt-3 border-t border-border/50 text-[11px] text-muted-foreground">
                  AUPRC meningkat +20% dan false negatives ditekan hingga -42% vs model baseline.
                </div>
              </Card>
            </div>

            {/* Taksonomi 13 Modus Kecurangan JKN */}
            <Card className="p-5 gap-4 border-border/80 bg-card/60">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-base font-bold text-foreground">
                    Taksonomi 13 Modus Kecurangan JKN (Dataset Notion)
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    Distribusi anomali klaim yang berhasil dimodelkan dalam 300 berkas sintetis ground truth:
                  </p>
                </div>
                <Badge variant="outline" className="text-xs">
                  13 Modus Terdaftar
                </Badge>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 pt-2">
                {[
                  {
                    code: "upcoding",
                    name: "Upcoding",
                    desc: "Peningkatan derajat keparahan diagnosis (mis. gastroenteritis sederhana dikodekan tifoid dengan komplikasi) demi tarif INA-CBG lebih tinggi.",
                  },
                  {
                    code: "phantom_billing",
                    name: "Phantom Billing",
                    desc: "Penagihan klaim fiktif atas pasien atau prosedur yang tidak pernah dilakukan di faskes.",
                  },
                  {
                    code: "unbundling",
                    name: "Unbundling / Fragmentation",
                    desc: "Memecah satu paket pelayanan terpadu menjadi beberapa klaim terpisah untuk melipatgandakan klaim.",
                  },
                  {
                    code: "cloning",
                    name: "Cloning Rekam Medis",
                    desc: "Duplikasi narasi rekam medis dan terapi antar pasien secara identik untuk percepatan klaim massal.",
                  },
                  {
                    code: "drug_diversion",
                    name: "Drug Diversion",
                    desc: "Peresepan obat mahal melebihi indikasi medis untuk dialihkan ke pasar sekunder.",
                  },
                  {
                    code: "prolonged_stay",
                    name: "Prolonged Stay",
                    desc: "Memperpanjang lama rawat inap pasien tanpa justifikasi klinis untuk menjustifikasi komplikasi fiktif.",
                  },
                  {
                    code: "repeat_billing",
                    name: "Repeat Billing",
                    desc: "Mengajukan tagihan klaim ganda untuk satu kali tindakan medis pada tanggal yang berdekatan.",
                  },
                  {
                    code: "readmission_berulang",
                    name: "Readmisi Kilat Terencana",
                    desc: "Memulangkan pasien prematur kemudian mendaftarkannya kembali dalam hitungan hari demi paket baru.",
                  },
                  {
                    code: "iur_biaya",
                    name: "Iur Biaya Ilegal",
                    desc: "Memungut biaya tambahan kepada peserta JKN di luar ketentuan regulasi paket BPJS.",
                  },
                  {
                    code: "biaya_markup",
                    name: "Markup Biaya Alkes / Implan",
                    desc: "Penggelembungan harga perolehan bahan medis habis pakai melampaui plafon e-Katalog.",
                  },
                  {
                    code: "anomali_frekuensi",
                    name: "Anomali Frekuensi Kunjungan",
                    desc: "Pasien tercatat berkunjung berulang-ulang ke poliklinik spesialis tanpa progres klinis riil.",
                  },
                  {
                    code: "excessive_usage",
                    name: "Penggunaan Penunjang Berlebih",
                    desc: "Pemeriksaan radiologi atau laboratorium canggih tanpa indikasi diagnosis primer.",
                  },
                  {
                    code: "kontradiksi_narasi",
                    name: "Kontradiksi Narasi Rekam Medis",
                    desc: "Catatan subjektif/objektif dokter bertentangan dengan resume klaim (mis. pasien pulang rawat jalan dicatat rawat inap).",
                  },
                ].map((item, idx) => (
                  <div
                    key={item.code}
                    className="rounded-lg border border-border/60 bg-muted/30 p-3 space-y-1 hover:border-primary/40 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-xs text-foreground flex items-center gap-1.5">
                        <span className="text-[10px] text-muted-foreground font-mono">#{idx + 1}</span>
                        {item.name}
                      </span>
                      <code className="text-[10px] text-muted-foreground bg-muted px-1.5 py-0.5 rounded">
                        {item.code}
                      </code>
                    </div>
                    <p className="text-[11px] text-muted-foreground leading-relaxed">{item.desc}</p>
                  </div>
                ))}
              </div>
            </Card>

            {/* Ground Truth Matrix & Syndicates */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card className="p-5 gap-3 border-border/80 bg-card/60">
                <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
                  <FileCheck className="h-4 w-4 text-emerald-500" />
                  <span>Distribusi Ground Truth 300 Berkas</span>
                </h3>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Dataset Notion dikalibrasi merefleksikan rasio alami klaim di lapangan dengan sebaran ketat:
                </p>
                <div className="space-y-2 text-xs pt-1">
                  <div className="flex items-center justify-between p-2 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-700 dark:text-emerald-300">
                    <span>Auto-Clear (Klaim Normal / Sah)</span>
                    <strong className="font-mono">240 berkas (80.0%)</strong>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded-md bg-amber-500/10 border border-amber-500/20 text-amber-700 dark:text-amber-300">
                    <span>Manual Review (Ambigu / Perlu Telaah)</span>
                    <strong className="font-mono">24 berkas (8.0%)</strong>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded-md bg-rose-500/10 border border-rose-500/20 text-rose-700 dark:text-rose-300">
                    <span>Escalate (Fraud Terkonfirmasi / Penyidikan)</span>
                    <strong className="font-mono">36 berkas (12.0%)</strong>
                  </div>
                </div>
              </Card>

              <Card className="p-5 gap-3 border-border/80 bg-card/60">
                <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
                  <Network className="h-4 w-4 text-violet-500" />
                  <span>9 Sindikat Kolusi Berjejaring (Multi-Faskes)</span>
                </h3>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Ditemukan 9 kelompok kolusi terorganisir yang menghubungkan dokter DPJP, oknum manajemen RS,
                  dan fasilitas rujukan:
                </p>
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {[
                    "SYND-01 (RS_A & Dr. Hendra)",
                    "SYND-02 (RS_B & Dr. Gunawan)",
                    "SYND-03 (RS_C & Dr. Kartika)",
                    "SYND-04 (RS_D & Dr. Bambang)",
                    "SYND-05 (RS_E & Dr. Siti)",
                    "SYND-06 (RS_F & Dr. Anisa)",
                    "SYND-07 (RS_G & Dr. Mulyadi)",
                    "SYND-08 (RS_H & Dr. Rian)",
                    "SYND-09 (Klinik Pratama Farma)",
                  ].map((s) => (
                    <Badge
                      key={s}
                      variant="outline"
                      className="text-xs py-1 px-2 bg-violet-500/10 text-violet-600 dark:text-violet-400 border-violet-500/30 font-medium"
                    >
                      {s}
                    </Badge>
                  ))}
                </div>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>

      {/* ========================================================================= */}
      {/* SHEET DRAWER: DETAIL KLAIM JKN LENGKAP                                     */}
      {/* ========================================================================= */}
      <Sheet open={!!selectedClaim} onOpenChange={(open) => !open && setSelectedClaim(null)}>
        <SheetContent className="w-full sm:max-w-xl md:max-w-2xl overflow-y-auto p-6 space-y-5">
          {selectedClaim && (
            <>
              <SheetHeader className="p-0 space-y-1.5 border-b border-border/60 pb-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <SheetTitle className="font-mono text-lg font-extrabold text-foreground">
                      {selectedClaim.id}
                    </SheetTitle>
                    <Badge
                      variant="outline"
                      className={cn(
                        "text-xs px-2 py-0.5 font-bold uppercase",
                        getRiskBadge(selectedClaim.risiko).className
                      )}
                    >
                      {selectedClaim.risiko} ({(selectedClaim.skorFraud * 100).toFixed(0)}%)
                    </Badge>
                  </div>
                  <span
                    className={cn(
                      "text-xs px-2 py-0.5 rounded-full border font-semibold",
                      getStatusBadge(selectedClaim.status).className
                    )}
                  >
                    {getStatusBadge(selectedClaim.status).label}
                  </span>
                </div>
                <SheetDescription className="text-xs flex items-center gap-2">
                  <span>Tanggal Masuk: {selectedClaim.tanggal}</span>
                  <span>·</span>
                  <span className="capitalize">{selectedClaim.layanan}</span>
                  <span>·</span>
                  <span>LOS {selectedClaim.losHari} Hari</span>
                </SheetDescription>
              </SheetHeader>

              {/* Contradiction Alert Box (Crucial Highlight) */}
              {selectedClaim.kontradiksiNarasi && (
                <div className="rounded-xl border border-amber-500/40 bg-amber-500/10 p-3.5 space-y-1.5">
                  <div className="flex items-center gap-2 text-amber-700 dark:text-amber-400 font-bold text-xs sm:text-sm">
                    <AlertTriangle className="h-4 w-4 shrink-0 text-amber-500" />
                    <span>PERINGATAN: Kontradiksi Narasi Rekam Medis Terdeteksi</span>
                  </div>
                  <p className="text-xs text-amber-900/80 dark:text-amber-200/90 leading-relaxed">
                    Sistem mendeteksi ketidakcocokan signifikan antara catatan fisik tindakan/kondisi pasien
                    dalam rekam medis dengan kode ICD penagihan klaim BPJS Kesehatan. Rekomendasi audit mendalam.
                  </p>
                </div>
              )}

              {/* Financial & Hospital Information */}
              <div className="grid grid-cols-2 gap-3 rounded-xl border border-border/60 bg-muted/30 p-3.5 text-xs">
                <div>
                  <span className="text-[11px] text-muted-foreground block">Total Biaya Diajukan</span>
                  <span className="text-base font-bold text-foreground">
                    {formatRupiah(selectedClaim.biayaRp)}
                  </span>
                </div>
                <div>
                  <span className="text-[11px] text-muted-foreground block">Faskes / Rumah Sakit</span>
                  <span className="font-semibold text-foreground flex items-center gap-1">
                    <Building2 className="h-3.5 w-3.5 text-primary" />
                    {selectedClaim.faskes}
                  </span>
                </div>
                <div>
                  <span className="text-[11px] text-muted-foreground block">Rujukan Asal</span>
                  <span className="text-muted-foreground line-clamp-1" title={selectedClaim.rujukan}>
                    {selectedClaim.rujukan}
                  </span>
                </div>
                <div>
                  <span className="text-[11px] text-muted-foreground block">Alasan Berobat</span>
                  <span className="text-foreground line-clamp-1" title={selectedClaim.alasanBerobat}>
                    {selectedClaim.alasanBerobat}
                  </span>
                </div>
              </div>

              {/* Clinical & Patient Information */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                  <Stethoscope className="h-3.5 w-3.5 text-primary" />
                  <span>Detail Klinis & Tenaga Medis</span>
                </h4>
                <div className="space-y-2 rounded-xl border border-border/60 p-3.5 text-xs">
                  <div className="flex justify-between py-1 border-b border-border/40">
                    <span className="text-muted-foreground">Pasien:</span>
                    <span className="font-semibold text-foreground">{selectedClaim.pasien}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-border/40">
                    <span className="text-muted-foreground">Dokter Penanggung Jawab (DPJP):</span>
                    <span className="font-semibold text-foreground">{selectedClaim.dokter}</span>
                  </div>
                  <div className="flex flex-col py-1 border-b border-border/40 gap-0.5">
                    <span className="text-muted-foreground">Diagnosis Utama (ICD-10):</span>
                    <span className="font-medium text-foreground">{selectedClaim.diagnosisIcd10}</span>
                  </div>
                  <div className="flex flex-col py-1 border-b border-border/40 gap-0.5">
                    <span className="text-muted-foreground">Prosedur / Tindakan (ICD-9-CM):</span>
                    <span className="font-medium text-foreground">{selectedClaim.prosedurIcd9}</span>
                  </div>
                  <div className="flex flex-col py-1 gap-0.5">
                    <span className="text-muted-foreground">Terapi / Obat Diberikan:</span>
                    <span className="font-mono text-[11px] text-foreground">{selectedClaim.obat}</span>
                  </div>
                </div>
              </div>

              {/* Medical Record Narrative & Patient Feedback */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                  <FileText className="h-3.5 w-3.5 text-cyan-500" />
                  <span>Narasi Rekam Medis & Umpan Balik Pasien</span>
                </h4>
                <div className="space-y-2.5 rounded-xl border border-border/60 p-3.5 text-xs">
                  <div>
                    <span className="text-[11px] font-semibold text-muted-foreground block mb-1">
                      Catatan Narasi Rekam Medis Dokter:
                    </span>
                    <p className="rounded-md bg-muted/40 p-2.5 text-foreground leading-relaxed font-mono text-[11px]">
                      {selectedClaim.narasiRekamMedis}
                    </p>
                  </div>
                  {selectedClaim.umpanBalikPasien && (
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-[11px] font-semibold text-muted-foreground">
                          Umpan Balik Pasien:
                        </span>
                        <Badge
                          variant="outline"
                          className={cn(
                            "text-[9px] h-4 px-1",
                            selectedClaim.sentimen === "positif"
                              ? "bg-emerald-500/10 text-emerald-600 border-emerald-500/30"
                              : selectedClaim.sentimen === "negatif"
                              ? "bg-rose-500/10 text-rose-600 border-rose-500/30"
                              : "bg-slate-500/10 text-slate-600 dark:text-slate-400 border-slate-500/30"
                          )}
                        >
                          Sentimen: {selectedClaim.sentimen} ({selectedClaim.skorSentimen})
                        </Badge>
                      </div>
                      <p className="rounded-md bg-muted/30 p-2 text-foreground italic leading-relaxed">
                        "{selectedClaim.umpanBalikPasien}"
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* AI & MHGSL Graph Signals */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                  <Cpu className="h-3.5 w-3.5 text-indigo-500" />
                  <span>Analisis AI MHGSL & Explainability (XAI)</span>
                </h4>
                <div className="space-y-2.5 rounded-xl border border-border/60 p-3.5 text-xs">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="p-2 rounded-md bg-muted/40">
                      <span className="text-[10px] text-muted-foreground block">Modus Terindikasi</span>
                      <span className="font-semibold text-foreground">
                        {formatModusLabel(selectedClaim.modus)}
                      </span>
                    </div>
                    <div className="p-2 rounded-md bg-muted/40">
                      <span className="text-[10px] text-muted-foreground block">Sindikat Kolusi</span>
                      <span className="font-semibold text-foreground">
                        {selectedClaim.sindikat || "Non-Sindikat (Mandiri)"}
                      </span>
                    </div>
                  </div>

                  <div>
                    <span className="text-[11px] text-muted-foreground block mb-0.5">Sinyal Dominan SHAP</span>
                    <div className="rounded-md bg-muted/40 p-2 font-mono text-[11px] text-foreground">
                      {selectedClaim.sinyalShap}
                    </div>
                  </div>

                  <div>
                    <span className="text-[11px] text-muted-foreground block mb-0.5">
                      Kontribusi Saluran Graf (Topologi · Fitur · Semantik)
                    </span>
                    <div className="rounded-md bg-muted/40 p-2 font-mono text-[11px] text-foreground">
                      {selectedClaim.kontribusiSaluran}
                    </div>
                  </div>

                  <div>
                    <span className="text-[11px] text-muted-foreground block mb-0.5">Alasan Audit Sistem</span>
                    <p className="rounded-md bg-muted/40 p-2.5 text-foreground leading-relaxed text-[11px]">
                      {selectedClaim.alasan}
                    </p>
                  </div>
                </div>
              </div>

              {/* Notion Page Link Button */}
              <div className="pt-2 flex items-center justify-between text-xs">
                <span className="text-[11px] font-mono text-muted-foreground">
                  ID Notion: {selectedClaim.notionId ? `${selectedClaim.notionId.slice(0, 18)}...` : "-"}
                </span>
                <a
                  href={selectedClaim.notionId ? `https://app.notion.com/p/${selectedClaim.notionId.replace(/-/g, "")}` : "#"}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 rounded-lg border border-border px-3 py-1.5 text-xs font-medium text-foreground hover:bg-accent transition-colors"
                >
                  <ExternalLink className="h-3.5 w-3.5 text-primary" />
                  <span>Buka di Ruang Kerja Notion</span>
                </a>
              </div>
            </>
          )}
        </SheetContent>
      </Sheet>

      {/* ========================================================================= */}
      {/* SHEET DRAWER: DETAIL RISET LENGKAP                                         */}
      {/* ========================================================================= */}
      <Sheet open={!!selectedResearch} onOpenChange={(open) => !open && setSelectedResearch(null)}>
        <SheetContent className="w-full sm:max-w-xl md:max-w-2xl overflow-y-auto p-6 space-y-5">
          {selectedResearch && (
            <>
              <SheetHeader className="p-0 space-y-2 border-b border-border/60 pb-4">
                <div className="flex flex-wrap items-center gap-1.5">
                  <Badge variant="outline" className="text-xs bg-muted/50">
                    {selectedResearch.kategori}
                  </Badge>
                  <Badge
                    variant="outline"
                    className={cn("text-xs font-semibold", getRelevanceBadge(selectedResearch.relevansi))}
                  >
                    Relevansi: {selectedResearch.relevansi}
                  </Badge>
                  <Badge
                    variant="outline"
                    className={cn("text-xs font-semibold", getVerificationBadge(selectedResearch.statusVerifikasi))}
                  >
                    {selectedResearch.statusVerifikasi}
                  </Badge>
                </div>
                <SheetTitle className="text-base font-bold sm:text-lg leading-snug">
                  {selectedResearch.item}
                </SheetTitle>
              </SheetHeader>

              {/* Comprehensive Description */}
              <div className="space-y-1.5">
                <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                  Deskripsi & Inti Riset
                </h4>
                <p className="rounded-xl border border-border/60 bg-muted/20 p-3.5 text-xs text-foreground leading-relaxed">
                  {selectedResearch.deskripsi}
                </p>
              </div>

              {/* Technical Approach */}
              <div className="space-y-1.5">
                <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                  Pendekatan Teknis & Justifikasi Arsitektur
                </h4>
                <p className="rounded-xl border border-border/60 bg-muted/20 p-3.5 text-xs text-foreground leading-relaxed">
                  {selectedResearch.pendekatanTeknis}
                </p>
              </div>

              {/* Research Notes & Methodology */}
              <div className="space-y-1.5">
                <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                  Catatan Riset, Sumber Peer-Review & Verifikasi
                </h4>
                <p className="rounded-xl border border-border/60 bg-muted/20 p-3.5 text-xs text-foreground leading-relaxed font-mono text-[11px]">
                  {selectedResearch.catatanRiset}
                </p>
              </div>

              {/* External Link & Notion Link */}
              <div className="space-y-2 pt-2 border-t border-border/60">
                {selectedResearch.sumberRiset && (
                  <div className="flex items-center justify-between text-xs p-2.5 rounded-lg border border-primary/30 bg-primary/5">
                    <span className="text-muted-foreground">Tautan Dokumen Riset Asli:</span>
                    <a
                      href={selectedResearch.sumberRiset}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 font-semibold text-primary hover:underline"
                    >
                      <span>Buka Jurnal / Paper</span>
                      <ExternalLink className="h-3.5 w-3.5" />
                    </a>
                  </div>
                )}

                <div className="flex items-center justify-between text-xs pt-2">
                  <span className="font-mono text-[11px] text-muted-foreground">
                    UUID: {selectedResearch.id}
                  </span>
                  <a
                    href={selectedResearch.notionUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 rounded-lg border border-border px-3 py-1.5 text-xs font-medium text-foreground hover:bg-accent transition-colors"
                  >
                    <ExternalLink className="h-3.5 w-3.5 text-indigo-500" />
                    <span>Lihat di Halaman Notion</span>
                  </a>
                </div>
              </div>
            </>
          )}
        </SheetContent>
      </Sheet>
    </div>
  );
}
