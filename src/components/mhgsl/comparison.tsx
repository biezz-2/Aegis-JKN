"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  BarChart3,
  TableProperties,
  Radar as RadarIcon,
  Check,
  Minus,
  AlertOctagon,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  LabelList,
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Legend,
  Line,
  LineChart,
} from "recharts";
import { COMPARISON_ROWS, AUPRC_DATA, RADAR_DATA, RADAR_METRICS, METRIC_DETAIL } from "./data";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DataUploader } from "./data-uploader";
import { useLang } from "./i18n";
import { cn } from "@/lib/utils";

function strengthBadge(v: string) {
  const lower = v.toLowerCase();
  if (lower.includes("sangat kuat") || lower.includes("sangat tinggi"))
    return { icon: Check, color: "oklch(0.55 0.14 165)", bg: "oklch(0.55 0.14 165 / 0.12)" };
  if (lower.includes("kuat") || lower.includes("tinggi"))
    return { icon: Check, color: "oklch(0.55 0.14 165)", bg: "oklch(0.55 0.14 165 / 0.1)" };
  if (lower.includes("lemah") || lower.includes("rendah"))
    return { icon: AlertOctagon, color: "oklch(0.62 0.22 20)", bg: "oklch(0.62 0.22 20 / 0.12)" };
  return { icon: Minus, color: "oklch(0.55 0.06 0)", bg: "oklch(0 0 0 / 0.04)" };
}

// Convert RADAR_DATA into recharts-compatible shape per metric axis
const radarChartData = RADAR_METRICS.map((metric) => {
  const point: Record<string, string | number> = { metric };
  RADAR_DATA.forEach((m) => {
    point[m.method] = m.values[metric as keyof typeof m.values];
  });
  return point;
});

export function Comparison() {
  const [activeMethod, setActiveMethod] = useState<string>("MHGSL");
  const { t } = useLang();

  return (
    <section id="compare" className="relative py-16 sm:py-24 bg-muted/30">
      <div className="absolute inset-0 bg-dots opacity-50" aria-hidden />
      <div className="container relative mx-auto max-w-7xl px-4 sm:px-6">
        <div className="mx-auto max-w-3xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
            className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-3 py-1 text-xs font-medium text-primary"
          >
            <BarChart3 className="h-3.5 w-3.5" />
            {t.compareBadge}
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl"
          >
            {t.compareTitle1} <span className="gradient-text">{t.compareTitle2}</span>
          </motion.h2>
          <p className="mt-4 text-muted-foreground">
            {t.compareDesc}
          </p>

          {/* Quick action: try your own data */}
          <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
            <DataUploader />
          </div>
        </div>

        <Tabs defaultValue="chart" className="mt-10">
          <div className="flex justify-center">
            <TabsList className="flex-wrap h-auto">
              <TabsTrigger value="chart" className="gap-1.5">
                <BarChart3 className="h-3.5 w-3.5" /> AUPRC
              </TabsTrigger>
              <TabsTrigger value="radar" className="gap-1.5">
                <RadarIcon className="h-3.5 w-3.5" /> Radar Multi-Metrik
              </TabsTrigger>
              <TabsTrigger value="metrics" className="gap-1.5">
                <BarChart3 className="h-3.5 w-3.5" /> Metrik Detail
              </TabsTrigger>
              <TabsTrigger value="table" className="gap-1.5">
                <TableProperties className="h-3.5 w-3.5" /> Matriks
              </TabsTrigger>
            </TabsList>
          </div>

          {/* AUPRC Bar Chart */}
          <TabsContent value="chart" className="mt-6">
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="rounded-2xl border border-border/70 bg-card p-4 sm:p-6 shadow-sm"
            >
              <div className="mb-3 flex items-center justify-between">
                <div>
                  <div className="text-sm font-semibold">
                    Area Under Precision-Recall Curve (AUPRC)
                  </div>
                  <div className="text-[11px] text-muted-foreground">
                    Skor relatif (0–1) · semakin tinggi = lebih sedikit false negatives
                  </div>
                </div>
                <div className="text-right text-[10px] text-muted-foreground">
                  Δ MHGSL vs XGBoost
                  <div className="font-bold text-primary text-base">+0.20</div>
                </div>
              </div>

              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={AUPRC_DATA}
                    layout="vertical"
                    margin={{ top: 8, right: 60, bottom: 8, left: 0 }}
                  >
                    <defs>
                      <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stopColor="var(--chart-1)" stopOpacity={0.85} />
                        <stop offset="100%" stopColor="var(--chart-4)" stopOpacity={0.95} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid
                      horizontal={false}
                      stroke="var(--border)"
                      strokeDasharray="3 3"
                    />
                    <XAxis
                      type="number"
                      domain={[0, 1]}
                      tick={{ fontSize: 10, fill: "var(--muted-foreground)" }}
                      tickLine={false}
                      axisLine={false}
                    />
                    <YAxis
                      type="category"
                      dataKey="method"
                      width={110}
                      tick={{ fontSize: 11, fill: "var(--foreground)" }}
                      tickLine={false}
                      axisLine={false}
                    />
                    <Tooltip
                      cursor={{ fill: "color-mix(in oklch, var(--primary) 14%, transparent)" }}
                      contentStyle={{
                        borderRadius: 10,
                        border: "1px solid var(--border)",
                        background: "var(--card)",
                        color: "var(--foreground)",
                        fontSize: 11,
                      }}
                      formatter={(v: number) => [v.toFixed(2), "AUPRC"]}
                    />
                    <Bar dataKey="auprc" radius={[0, 6, 6, 0]} barSize={22}>
                      {AUPRC_DATA.map((d, i) => (
                        <Cell
                          key={i}
                          fill={i === AUPRC_DATA.length - 1 ? "url(#barGrad)" : d.color}
                          fillOpacity={i === AUPRC_DATA.length - 1 ? 1 : 0.7}
                        />
                      ))}
                      <LabelList
                        dataKey="auprc"
                        position="right"
                        formatter={(v: number) => v.toFixed(2)}
                        style={{ fontSize: 10, fontWeight: 600, fill: "var(--foreground)" }}
                      />
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="mt-3 grid grid-cols-3 gap-2 text-center text-[11px]">
                <div className="rounded-lg bg-muted/40 p-2">
                  <div className="font-bold text-primary">+20%</div>
                  <div className="text-muted-foreground">lonjakan AUPRC</div>
                </div>
                <div className="rounded-lg bg-muted/40 p-2">
                  <div className="font-bold text-primary">×3</div>
                  <div className="text-muted-foreground">perspektif graf</div>
                </div>
                <div className="rounded-lg bg-muted/40 p-2">
                  <div className="font-bold text-primary">−42%</div>
                  <div className="text-muted-foreground">false negatives</div>
                </div>
              </div>
            </motion.div>
          </TabsContent>

          {/* Radar Chart */}
          <TabsContent value="radar" className="mt-6">
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="rounded-2xl border border-border/70 bg-card p-4 sm:p-6 shadow-sm"
            >
              <div className="mb-3 flex items-center justify-between flex-wrap gap-2">
                <div>
                  <div className="text-sm font-semibold">Radar Multi-Metrik</div>
                  <div className="text-[11px] text-muted-foreground">
                    5 metrik kinerja: Precision · Recall · F1 · AUPRC · Specificity
                  </div>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {RADAR_DATA.map((m) => (
                    <button
                      key={m.method}
                      onClick={() => setActiveMethod(m.method)}
                      className={cn(
                        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-[10px] font-medium transition-all",
                        activeMethod === m.method
                          ? "border-transparent text-white shadow-sm"
                          : "border-border bg-background hover:bg-muted"
                      )}
                      style={
                        activeMethod === m.method
                          ? { background: m.color }
                          : undefined
                      }
                    >
                      <span
                        className="h-2 w-2 rounded-full"
                        style={{ background: m.color, opacity: activeMethod === m.method ? 1 : 0.7 }}
                      />
                      {m.method}
                    </button>
                  ))}
                </div>
              </div>

              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarChartData} outerRadius="72%">
                    <PolarGrid stroke="var(--border)" />
                    <PolarAngleAxis
                      dataKey="metric"
                      tick={{ fontSize: 11, fill: "var(--muted-foreground)" }}
                    />
                    <PolarRadiusAxis
                      domain={[0, 1]}
                      tick={{ fontSize: 9, fill: "var(--muted-foreground)" }}
                      angle={90}
                    />
                    {RADAR_DATA.map((m) => (
                      <Radar
                        key={m.method}
                        name={m.method}
                        dataKey={m.method}
                        stroke={m.color}
                        fill={m.color}
                        fillOpacity={activeMethod === m.method ? 0.35 : 0.08}
                        strokeOpacity={activeMethod === m.method ? 1 : 0.3}
                        strokeWidth={activeMethod === m.method ? 2.5 : 1}
                        isAnimationActive
                      />
                    ))}
                    <Legend
                      wrapperStyle={{ fontSize: 11 }}
                      iconType="circle"
                      iconSize={8}
                    />
                    <Tooltip
                      contentStyle={{
                        borderRadius: 10,
                        border: "1px solid var(--border)",
                        background: "var(--card)",
                        color: "var(--foreground)",
                        fontSize: 11,
                      }}
                      formatter={(v: number, name: string) => [Number(v).toFixed(2), name]}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              <div className="mt-3 rounded-lg bg-primary/5 border border-primary/20 p-3 text-xs">
                <span className="font-semibold text-primary">{activeMethod}</span> unggul di
                seluruh 5 metrik. {" "}
                {activeMethod === "MHGSL"
                  ? "Skor F1 0.91 → minimasi false negatives pada sindikat kolusi."
                  : `Skor F1 ${RADAR_DATA.find((m) => m.method === activeMethod)?.values["F1-Score"].toFixed(2)} — coba bandingkan dengan MHGSL (0.91).`}
              </div>
            </motion.div>
          </TabsContent>

          {/* Metric Detail Table */}
          <TabsContent value="metrics" className="mt-6">
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="grid grid-cols-1 gap-5 lg:grid-cols-5"
            >
              <div className="lg:col-span-3 overflow-x-auto rounded-2xl border border-border/70 bg-card shadow-sm scrollbar-thin">
                <table className="w-full min-w-[560px] text-left text-xs">
                  <thead>
                    <tr className="border-b border-border/70 bg-muted/40">
                      <th className="px-3 py-2.5 font-semibold text-muted-foreground">Metrik</th>
                      <th className="px-3 py-2.5 font-semibold text-right">XGBoost</th>
                      <th className="px-3 py-2.5 font-semibold text-right">GNN</th>
                      <th className="px-3 py-2.5 font-semibold text-right">Hybrid</th>
                      <th className="px-3 py-2.5 font-semibold text-right text-primary">MHGSL ★</th>
                    </tr>
                  </thead>
                  <tbody>
                    {METRIC_DETAIL.map((row, i) => (
                      <tr key={row.metric} className={i % 2 === 0 ? "bg-card" : "bg-muted/20"}>
                        <td className="px-3 py-2.5">
                          <div className="font-medium text-foreground/90">{row.metric}</div>
                          <div className="text-[10px] text-muted-foreground">{row.desc}</div>
                        </td>
                        {(["xgboost", "gnn", "hybrid", "mhgsl"] as const).map((m) => {
                          const v = row[m];
                          const isBest = v === Math.max(row.xgboost, row.gnn, row.hybrid, row.mhgsl);
                          return (
                            <td
                              key={m}
                              className={cn(
                                "px-3 py-2.5 text-right tabular-nums font-mono",
                                m === "mhgsl" && "bg-primary/5",
                                isBest ? "font-bold text-primary" : "text-muted-foreground"
                              )}
                            >
                              {v.toFixed(2)}
                              {isBest && <span className="ml-1 text-[9px]">★</span>}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="lg:col-span-2 rounded-2xl border border-border/70 bg-card p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  Tren AUPRC per Metode
                </div>
                <div className="mt-2 h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                      data={[
                        { epoch: "E1", MHGSL: 0.71, Hybrid: 0.68, GNN: 0.62, XGBoost: 0.58 },
                        { epoch: "E2", MHGSL: 0.78, Hybrid: 0.74, GNN: 0.68, XGBoost: 0.63 },
                        { epoch: "E3", MHGSL: 0.84, Hybrid: 0.79, GNN: 0.72, XGBoost: 0.66 },
                        { epoch: "E4", MHGSL: 0.88, Hybrid: 0.83, GNN: 0.75, XGBoost: 0.69 },
                        { epoch: "E5", MHGSL: 0.91, Hybrid: 0.85, GNN: 0.78, XGBoost: 0.71 },
                      ]}
                      margin={{ top: 6, right: 6, bottom: 6, left: -20 }}
                    >
                      <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
                      <XAxis dataKey="epoch" tick={{ fontSize: 10, fill: "var(--muted-foreground)" }} tickLine={false} axisLine={false} />
                      <YAxis domain={[0.5, 0.95]} tick={{ fontSize: 10, fill: "var(--muted-foreground)" }} tickLine={false} axisLine={false} />
                      <Tooltip
                        contentStyle={{
                          borderRadius: 10,
                          border: "1px solid var(--border)",
                          background: "var(--card)",
                          color: "var(--foreground)",
                          fontSize: 11,
                        }}
                      />
                      <Line type="monotone" dataKey="MHGSL" stroke="oklch(0.62 0.22 20)" strokeWidth={2.5} dot={{ r: 3 }} />
                      <Line type="monotone" dataKey="Hybrid" stroke="oklch(0.5 0.16 70)" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="GNN" stroke="oklch(0.55 0.14 165)" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="XGBoost" stroke="oklch(0.62 0.13 200)" strokeWidth={2} dot={false} strokeDasharray="4 4" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <p className="mt-2 text-[10px] text-muted-foreground">
                  Konvergensi AUPRC selama 5 epoch pelatihan. MHGSL mengejar ketertinggalan
                  paling cepat berkat representasi multi-saluran.
                </p>
              </div>
            </motion.div>
          </TabsContent>

          {/* Comparison matrix */}
          <TabsContent value="table" className="mt-6">
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="overflow-x-auto rounded-2xl border border-border/70 bg-card shadow-sm scrollbar-thin"
            >
              <table className="w-full min-w-[640px] text-left text-xs">
                <thead>
                  <tr className="border-b border-border/70 bg-muted/40">
                    <th className="px-3 py-2.5 font-semibold text-muted-foreground">
                      Metrik
                    </th>
                    <th className="px-3 py-2.5 font-semibold">XGBoost</th>
                    <th className="px-3 py-2.5 font-semibold">GNN</th>
                    <th className="px-3 py-2.5 font-semibold">Hybrid</th>
                    <th className="px-3 py-2.5 font-semibold text-primary">
                      MHGSL ★
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {COMPARISON_ROWS.map((row, i) => (
                    <tr
                      key={row.metric}
                      className={i % 2 === 0 ? "bg-card" : "bg-muted/20"}
                    >
                      <td className="px-3 py-2.5 font-medium text-foreground/90">
                        {row.metric}
                      </td>
                      {(["xgboost", "gnn", "hybrid", "mhgsl"] as const).map((m) => {
                        const v = row[m];
                        const b = strengthBadge(v);
                        const Icon = b.icon;
                        return (
                          <td
                            key={m}
                            className={
                              "px-3 py-2.5 " + (m === "mhgsl" ? "bg-primary/5" : "")
                            }
                          >
                            <div className="flex items-start gap-1.5">
                              <Icon
                                className="h-3 w-3 mt-0.5 shrink-0"
                                style={{ color: b.color }}
                              />
                              <span
                                className={m === "mhgsl" ? "font-semibold text-foreground" : "text-muted-foreground"}
                              >
                                {v}
                              </span>
                            </div>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </motion.div>
          </TabsContent>
        </Tabs>
      </div>
    </section>
  );
}
