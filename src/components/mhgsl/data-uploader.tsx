"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload,
  FileText,
  X,
  Sparkles,
  Loader2,
  AlertCircle,
  Table,
  Calculator,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
import { useLang } from "./i18n";

// A simplified MHGSL-style fraud scoring demo for uploaded claim rows.
// Inputs (CSV/JSON keys): patient_id, doctor_id, faskes, procedure, diagnosis, los, cost, age
// We compute 3 channel scores + a fusion score using cosine-like similarity heuristics.

export interface ClaimRow {
  patient_id?: string;
  doctor_id?: string;
  faskes?: string;
  procedure?: string;
  cost?: number;
  los?: number;
  age?: number;
  diagnosis?: string;
  [key: string]: string | number | undefined;
}

export interface ScoredRow extends ClaimRow {
  topologyScore: number;
  featureScore: number;
  semanticScore: number;
  fusionScore: number;
  riskLabel: "low" | "medium" | "high" | "fraud";
}

const SAMPLE_CSV = `patient_id,doctor_id,faskes,procedure,diagnosis,los,cost,age
P001,D01,RS_A,S_mahal,Dx_ringan,3,42000000,42
P002,D01,RS_A,S_mahal,Dx_ringan,3,41500000,39
P003,D02,RS_A,S_mahal,Dx_ringan,3,41800000,45
P004,D03,RS_B,S_std,Dx_normal,2,3500000,28
P005,D03,RS_B,S_std,Dx_normal,1,2800000,33
P006,D04,RS_B,S_std,Dx_normal,2,3200000,51`;

function parseCSV(text: string): ClaimRow[] {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) return [];
  const headers = lines[0].split(",").map((h) => h.trim());
  return lines.slice(1).map((line) => {
    const vals = line.split(",").map((v) => v.trim());
    const obj: ClaimRow = {};
    headers.forEach((h, i) => {
      const v = vals[i];
      if (h === "los" || h === "cost" || h === "age") {
        obj[h] = Number(v) || 0;
      } else {
        obj[h] = v;
      }
    });
    return obj;
  });
}

function scoreRows(rows: ClaimRow[]): ScoredRow[] {
  // Group by doctor+faskes for topology concentration
  const doctorFaskesCounts: Record<string, number> = {};
  rows.forEach((r) => {
    const key = `${r.doctor_id || ""}|${r.faskes || ""}`;
    doctorFaskesCounts[key] = (doctorFaskesCounts[key] || 0) + 1;
  });

  // Compute feature similarity clusters
  // Build a normalized feature vector [los, age, cost_normalized]
  const maxCost = Math.max(...rows.map((r) => r.cost || 0), 1);
  const vectors = rows.map((r) => [
    (r.los || 0) / 10,
    (r.age || 0) / 100,
    (r.cost || 0) / maxCost,
  ]);

  return rows.map((r, i) => {
    // Topology: concentration of doctor+faskes (1 = all in one bucket, 0 = distributed)
    const key = `${r.doctor_id || ""}|${r.faskes || ""}`;
    const conc = doctorFaskesCounts[key] / rows.length;
    const topologyScore = Math.min(1, conc * 3);

    // Feature: similarity to other rows (avg cosine sim)
    let simSum = 0;
    let simCount = 0;
    for (let j = 0; j < rows.length; j++) {
      if (j === i) continue;
      const v = vectors[j];
      const dot = vectors[i][0] * v[0] + vectors[i][1] * v[1] + vectors[i][2] * v[2];
      const magI = Math.sqrt(vectors[i][0] ** 2 + vectors[i][1] ** 2 + vectors[i][2] ** 2);
      const magJ = Math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2);
      if (magI > 0 && magJ > 0) {
        simSum += dot / (magI * magJ);
        simCount++;
      }
    }
    const avgSim = simCount > 0 ? simSum / simCount : 0;
    const featureScore = Math.max(0, (avgSim - 0.6) * 2.5);

    // Semantic: heuristic for diagnosis-procedure mismatch
    // If diagnosis contains "ringan" or "mild" and procedure contains "mahal" or "expensive"
    const dx = (r.diagnosis || "").toLowerCase();
    const proc = (r.procedure || "").toLowerCase();
    const isDxMild = dx.includes("ringan") || dx.includes("mild");
    const isProcExpensive = proc.includes("mahal") || proc.includes("expensive") || proc.includes("complex");
    const semanticScore = isDxMild && isProcExpensive ? 0.9 : isDxMild || isProcExpensive ? 0.4 : 0.1;

    // Fusion: weighted combination (mirrors MHGSL approach: top -0.12 camouflage)
    const fusionScore = Math.max(
      0,
      Math.min(
        1,
        featureScore * 0.38 + semanticScore * 0.41 + topologyScore * (-0.12) + 0.3
      )
    );

    const riskLabel: ScoredRow["riskLabel"] =
      fusionScore >= 0.85 ? "fraud" : fusionScore >= 0.65 ? "high" : fusionScore >= 0.4 ? "medium" : "low";

    return {
      ...r,
      topologyScore,
      featureScore,
      semanticScore,
      fusionScore,
      riskLabel,
    };
  });
}

const riskColor: Record<string, string> = {
  low: "oklch(0.55 0.14 165)",
  medium: "oklch(0.7 0.16 70)",
  high: "oklch(0.7 0.18 50)",
  fraud: "oklch(0.62 0.22 20)",
};

const channelColor: Record<string, string> = {
  topology: "oklch(0.55 0.14 165)",
  feature: "oklch(0.62 0.13 200)",
  semantic: "oklch(0.7 0.16 70)",
};

export function DataUploader() {
  const { t, lang } = useLang();
  const [open, setOpen] = React.useState(false);
  const [rows, setRows] = React.useState<ClaimRow[]>([]);
  const [scored, setScored] = React.useState<ScoredRow[] | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [dragOver, setDragOver] = React.useState(false);
  const inputRef = React.useRef<HTMLInputElement | null>(null);

  const t_local = {
    title: lang === "id" ? "Bandingkan Data Klaim Anda" : "Score Your Own Claim Data",
    desc:
      lang === "id"
        ? "Unggah CSV/JSON klaim Anda untuk dijalankan lewat skor MHGSL sederhana (topologi+fitur+semantik+fusi)."
        : "Upload your claim CSV/JSON to run through a simplified MHGSL scoring (topology+feature+semantic+fusion).",
    trigger: lang === "id" ? "Bandingkan Data" : "Compare Data",
    uploadHint:
      lang === "id"
        ? "Tarik file ke sini atau klik untuk memilih"
        : "Drag file here or click to select",
    formats: "CSV atau JSON · format: patient_id, doctor_id, faskes, procedure, diagnosis, los, cost, age",
    sample: lang === "id" ? "Muat sampel" : "Load sample",
    clear: lang === "id" ? "Bersihkan" : "Clear",
    close: lang === "id" ? "Tutup" : "Close",
    scoreBtn: lang === "id" ? "Hitung Skor MHGSL" : "Run MHGSL Scoring",
    errorParse: lang === "id" ? "Gagal parse file. Pastikan format CSV/JSON valid." : "Failed to parse file. Ensure valid CSV/JSON format.",
    errorEmpty: lang === "id" ? "Tidak ada baris terdeteksi." : "No rows detected.",
    rowsLabel: lang === "id" ? "baris dimuat" : "rows loaded",
    resultsTitle: lang === "id" ? "Hasil Skor" : "Scoring Results",
    channelTitle: lang === "id" ? "Skor per Saluran" : "Per-Channel Scores",
    channelTopo: lang === "id" ? "Topologi" : "Topology",
    channelFeat: lang === "id" ? "Fitur" : "Feature",
    channelSem: lang === "id" ? "Semantik" : "Semantic",
    channelFus: lang === "id" ? "Fusi" : "Fusion",
    rowLabel: lang === "id" ? "Klaim" : "Claim",
    verdict:
      lang === "id"
        ? "Verdict: skor ≥ 0.85 menandakan kemungkinan fraud → eskalasi ke verifikator."
        : "Verdict: score ≥ 0.85 indicates likely fraud → escalate to verifier.",
    formula: lang === "id" ? "Fusi = 0.38·Fitur + 0.41·Semantik + (-0.12)·Topologi + 0.30" : "Fusion = 0.38·Feature + 0.41·Semantic + (-0.12)·Topology + 0.30",
  };

  const handleFile = (file: File) => {
    setError(null);
    setScored(null);
    setLoading(true);
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const text = String(ev.target?.result || "");
        let parsed: ClaimRow[] = [];
        if (file.name.endsWith(".json") || text.trim().startsWith("[")) {
          parsed = JSON.parse(text);
          if (!Array.isArray(parsed)) throw new Error("not array");
        } else {
          parsed = parseCSV(text);
        }
        if (parsed.length === 0) {
          setError(t_local.errorEmpty);
        } else {
          setRows(parsed);
        }
      } catch {
        setError(t_local.errorParse);
      }
      setLoading(false);
    };
    reader.onerror = () => {
      setError(t_local.errorParse);
      setLoading(false);
    };
    reader.readAsText(file);
  };

  const runScoring = () => {
    if (rows.length === 0) return;
    setLoading(true);
    setTimeout(() => {
      setScored(scoreRows(rows));
      setLoading(false);
    }, 700);
  };

  const loadSample = () => {
    setError(null);
    setScored(null);
    setRows(parseCSV(SAMPLE_CSV));
  };

  const clear = () => {
    setRows([]);
    setScored(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <button
          className="inline-flex items-center gap-1.5 rounded-full border border-primary/30 bg-primary/5 px-3 py-1.5 text-xs font-medium text-primary hover:bg-primary/10 transition-colors"
          title={t_local.trigger}
        >
          <Upload className="h-3.5 w-3.5" />
          {t_local.trigger}
        </button>
      </DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto scrollbar-thin p-0 gap-0">
        <DialogHeader className="px-5 pt-5 pb-3 border-b border-border">
          <DialogTitle className="flex items-center gap-2 text-base">
            <span
              className="flex h-8 w-8 items-center justify-center rounded-lg shrink-0"
              style={{ background: "linear-gradient(135deg, var(--primary), var(--chart-2))" }}
            >
              <Sparkles className="h-4 w-4 text-white" />
            </span>
            <span>{t_local.title}</span>
          </DialogTitle>
          <DialogDescription className="text-xs">{t_local.desc}</DialogDescription>
        </DialogHeader>

        <div className="p-5 space-y-4">
          {/* Upload area */}
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              const file = e.dataTransfer.files?.[0];
              if (file) handleFile(file);
            }}
            onClick={() => inputRef.current?.click()}
            className={cn(
              "rounded-2xl border-2 border-dashed p-8 text-center cursor-pointer transition-all",
              dragOver
                ? "border-primary bg-primary/10"
                : "border-border hover:border-primary/40 hover:bg-primary/5"
            )}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".csv,.json"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFile(file);
              }}
            />
            {loading ? (
              <Loader2 className="mx-auto h-8 w-8 animate-spin text-primary" />
            ) : (
              <Upload className="mx-auto h-8 w-8 text-primary" />
            )}
            <div className="mt-2 text-sm font-medium">{t_local.uploadHint}</div>
            <div className="mt-1 text-[10px] text-muted-foreground">{t_local.formats}</div>
          </div>

          {/* Action buttons */}
          <div className="flex flex-wrap gap-2">
            <Button onClick={loadSample} variant="outline" size="sm" className="gap-1.5">
              <FileText className="h-3.5 w-3.5" />
              {t_local.sample}
            </Button>
            <Button
              onClick={runScoring}
              size="sm"
              disabled={rows.length === 0 || loading}
              className="gap-1.5"
            >
              <Calculator className="h-3.5 w-3.5" />
              {t_local.scoreBtn}
            </Button>
            {(rows.length > 0 || scored) && (
              <Button onClick={clear} variant="ghost" size="sm" className="gap-1.5 ml-auto">
                <X className="h-3.5 w-3.5" />
                {t_local.clear}
              </Button>
            )}
          </div>

          {error && (
            <div className="rounded-lg border border-rose-200 bg-rose-50 p-2.5 text-xs text-rose-700 dark:bg-rose-500/10 dark:border-rose-500/30 dark:text-rose-300 flex items-start gap-1.5">
              <AlertCircle className="h-3.5 w-3.5 shrink-0 mt-0.5" />
              {error}
            </div>
          )}

          {rows.length > 0 && !scored && (
            <div className="rounded-lg border border-border bg-muted/20 p-2.5 text-xs">
              <div className="flex items-center gap-1.5 font-semibold text-muted-foreground mb-1.5">
                <Table className="h-3.5 w-3.5" />
                {rows.length} {t_local.rowsLabel}
              </div>
              <div className="overflow-x-auto scrollbar-thin">
                <table className="w-full text-[10px] font-mono">
                  <thead>
                    <tr className="text-left text-muted-foreground">
                      <th className="px-1.5 py-1">patient</th>
                      <th className="px-1.5 py-1">doctor</th>
                      <th className="px-1.5 py-1">faskes</th>
                      <th className="px-1.5 py-1">procedure</th>
                      <th className="px-1.5 py-1">dx</th>
                      <th className="px-1.5 py-1">LOS</th>
                      <th className="px-1.5 py-1">cost</th>
                      <th className="px-1.5 py-1">age</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rows.slice(0, 6).map((r, i) => (
                      <tr key={i} className="border-t border-border/40">
                        <td className="px-1.5 py-0.5">{r.patient_id || "-"}</td>
                        <td className="px-1.5 py-0.5">{r.doctor_id || "-"}</td>
                        <td className="px-1.5 py-0.5">{r.faskes || "-"}</td>
                        <td className="px-1.5 py-0.5">{r.procedure || "-"}</td>
                        <td className="px-1.5 py-0.5">{r.diagnosis || "-"}</td>
                        <td className="px-1.5 py-0.5">{r.los ?? "-"}</td>
                        <td className="px-1.5 py-0.5">{r.cost ?? "-"}</td>
                        <td className="px-1.5 py-0.5">{r.age ?? "-"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {rows.length > 6 && (
                  <div className="text-center text-[10px] text-muted-foreground mt-1">
                    + {rows.length - 6} more
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Results */}
          <AnimatePresence>
            {scored && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-3"
              >
                <div className="flex items-center gap-2 text-sm font-semibold">
                  <Sparkles className="h-4 w-4 text-primary" />
                  {t_local.resultsTitle}
                </div>
                <div className="rounded-lg bg-muted/30 p-2 text-[10px] font-mono text-muted-foreground">
                  {t_local.formula}
                </div>

                {/* Per-claim score cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {scored.map((s, i) => {
                    const rColor = riskColor[s.riskLabel];
                    return (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -8 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.05 }}
                        className="rounded-xl border p-3"
                        style={{
                          borderColor: `${rColor}40`,
                          background: `${rColor}0a`,
                        }}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="text-xs font-semibold">
                            {t_local.rowLabel} {s.patient_id || `#${i + 1}`}
                          </div>
                          <span
                            className="rounded-full px-2 py-0.5 text-[10px] font-bold capitalize text-white"
                            style={{ background: rColor }}
                          >
                            {s.riskLabel}
                          </span>
                        </div>
                        <div className="flex items-center gap-3 text-[11px] mb-1.5">
                          <span className="font-bold tabular-nums" style={{ color: rColor }}>
                            {s.fusionScore.toFixed(2)}
                          </span>
                          <span className="text-muted-foreground">
                            {s.procedure} · {s.diagnosis}
                          </span>
                        </div>
                        <Progress
                          value={s.fusionScore * 100}
                          className="h-1.5 mb-2"
                          style={
                            { "--progress-foreground": rColor } as React.CSSProperties
                          }
                        />
                        {/* Per-channel breakdown */}
                        <div className="space-y-1">
                          {(["topologyScore", "featureScore", "semanticScore"] as const).map((k, j) => {
                            const label = j === 0 ? t_local.channelTopo : j === 1 ? t_local.channelFeat : t_local.channelSem;
                            const chColor = j === 0 ? channelColor.topology : j === 1 ? channelColor.feature : channelColor.semantic;
                            const v = s[k];
                            return (
                              <div key={k} className="flex items-center gap-2 text-[10px]">
                                <span className="w-14 text-muted-foreground shrink-0">{label}</span>
                                <div className="flex-1 h-1.5 rounded-full bg-muted/40 overflow-hidden">
                                  <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${Math.max(0, Math.min(1, v)) * 100}%` }}
                                    transition={{ duration: 0.5, delay: 0.1 + i * 0.05 + j * 0.03 }}
                                    className="h-full rounded-full"
                                    style={{ background: chColor, opacity: v >= 0 ? 0.85 : 0.4 }}
                                  />
                                </div>
                                <span className="font-mono tabular-nums w-10 text-right" style={{ color: chColor }}>
                                  {v >= 0 ? "+" : ""}
                                  {v.toFixed(2)}
                                </span>
                              </div>
                            );
                          })}
                        </div>
                      </motion.div>
                    );
                  })}
                </div>

                <div className="rounded-lg border-l-4 border-primary p-2.5 text-[11px] bg-primary/5">
                  <span className="font-semibold text-primary">{t_local.verdict}</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </DialogContent>
    </Dialog>
  );
}
