"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  ShieldAlert,
  Stethoscope,
  Hospital,
  User,
  TrendingUp,
  Calendar,
  AlertTriangle,
  Lightbulb,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { type FraudEntityProfile } from "./data";
import { cn } from "@/lib/utils";

const roleIcon: Record<string, React.ComponentType<{ className?: string }>> = {
  Pasien: User,
  Dokter: Stethoscope,
  Faskes: Hospital,
  Prosedur: TrendingUp,
  Diagnosis: AlertTriangle,
};

const channelColor: Record<string, string> = {
  topology: "oklch(0.55 0.14 165)",
  feature: "oklch(0.62 0.13 200)",
  semantic: "oklch(0.7 0.16 70)",
};

const channelLabel: Record<string, string> = {
  topology: "Topologi",
  feature: "Fitur",
  semantic: "Semantik",
};

const riskColor: Record<string, string> = {
  low: "oklch(0.55 0.14 165)",
  medium: "oklch(0.7 0.16 70)",
  high: "oklch(0.7 0.18 50)",
  fraud: "oklch(0.62 0.22 20)",
};

export function FraudDrilldownModal({
  profile,
  open,
  onOpenChange,
}: {
  profile: FraudEntityProfile | null;
  open: boolean;
  onOpenChange: (v: boolean) => void;
}) {
  if (!profile) return null;

  const Icon = roleIcon[profile.role] ?? User;
  const rColor = riskColor[profile.riskLevel];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto scrollbar-thin p-0 gap-0">
        <DialogHeader className="px-5 pt-5 pb-3 border-b border-border">
          <DialogTitle className="flex items-center gap-3 text-base">
            <span
              className="flex h-9 w-9 items-center justify-center rounded-xl"
              style={{ background: rColor }}
            >
              <Icon className="h-4.5 w-4.5 text-white" />
            </span>
            <div className="flex-1">
              <div className="text-base font-bold leading-tight">{profile.label}</div>
              <div className="text-[11px] text-muted-foreground font-normal">
                Peran: {profile.role} · Tipe: {profile.type}
              </div>
            </div>
            <Badge
              className="capitalize"
              style={{
                background: `${rColor}20`,
                color: rColor,
                border: `1px solid ${rColor}40`,
              }}
            >
              {profile.riskLevel}
            </Badge>
          </DialogTitle>
          <DialogDescription className="sr-only">
            Detail investigasi entitas {profile.label}
          </DialogDescription>
        </DialogHeader>

        <div className="p-5 space-y-5">
          {/* Risk score gauge */}
          <div className="rounded-xl border border-border bg-muted/30 p-4">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                Skor Fraud MHGSL
              </span>
              <span
                className="text-2xl font-bold tabular-nums"
                style={{ color: rColor }}
              >
                {profile.riskScore.toFixed(2)}
              </span>
            </div>
            <Progress
              value={profile.riskScore * 100}
              className="h-2.5"
              style={
                {
                  // @ts-expect-error CSS var
                  "--progress-foreground": rColor,
                } as React.CSSProperties
              }
            />
            <p className="mt-2 text-xs leading-relaxed text-foreground/85">
              {profile.summary}
            </p>
          </div>

          {/* Metrics grid */}
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-wide text-muted-foreground mb-2">
              Metrik Kunci
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {profile.metrics.map((m) => (
                <div
                  key={m.label}
                  className={cn(
                    "rounded-lg border p-2.5 text-center",
                    m.flag
                      ? "border-rose-200 bg-rose-50 dark:bg-rose-500/10 dark:border-rose-500/30"
                      : "border-border bg-card"
                  )}
                >
                  <div
                    className={cn(
                      "text-base font-bold tabular-nums",
                      m.flag && "text-rose-600 dark:text-rose-400"
                    )}
                  >
                    {m.value}
                  </div>
                  <div className="text-[10px] text-muted-foreground mt-0.5">
                    {m.label}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* SHAP-like evidence attribution */}
          <div>
            <div className="flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wide text-muted-foreground mb-2">
              <ShieldAlert className="h-3.5 w-3.5 text-amber-600" />
              Atribusi Bukti per Saluran
            </div>
            <div className="space-y-1.5">
              {profile.evidence
                .sort((a, b) => b.weight - a.weight)
                .map((ev, i) => {
                  const ch = channelColor[ev.source];
                  const pct = Math.max(5, ev.weight * 100);
                  return (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -8 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.06 }}
                      className="flex items-center gap-2"
                    >
                      <span
                        className="inline-flex items-center rounded-md px-1.5 py-0.5 text-[9px] font-semibold uppercase w-16 shrink-0"
                        style={{ background: `${ch}20`, color: ch }}
                      >
                        {channelLabel[ev.source]}
                      </span>
                      <div className="flex-1 text-[11px] text-foreground/85 leading-snug">
                        {ev.text}
                      </div>
                      <div className="w-14 text-right font-mono text-[10px] tabular-nums shrink-0" style={{ color: ch }}>
                        +{ev.weight.toFixed(2)}
                      </div>
                    </motion.div>
                  );
                })}
            </div>
          </div>

          {/* Timeline */}
          <div>
            <div className="flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wide text-muted-foreground mb-2">
              <Calendar className="h-3.5 w-3.5 text-primary" />
              Linimasa Anomali
            </div>
            <ol className="relative border-l-2 border-border pl-4 space-y-2.5 ml-1.5">
              {profile.timeline.map((t, i) => (
                <motion.li
                  key={i}
                  initial={{ opacity: 0, x: -6 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 + i * 0.05 }}
                  className="relative"
                >
                  <span
                    className="absolute -left-[21px] top-1 h-2.5 w-2.5 rounded-full ring-2 ring-background"
                    style={{ background: rColor }}
                  />
                  <div className="text-[10px] font-mono text-muted-foreground">
                    {t.date}
                  </div>
                  <div className="text-xs text-foreground/90">{t.event}</div>
                </motion.li>
              ))}
            </ol>
          </div>

          {/* Recommended action */}
          <div
            className="rounded-xl border-l-4 p-3"
            style={{
              borderColor: rColor,
              background: `${rColor}0a`,
            }}
          >
            <div className="flex items-start gap-2">
              <Lightbulb className="h-4 w-4 shrink-0 mt-0.5" style={{ color: rColor }} />
              <div>
                <div className="text-[11px] font-semibold uppercase tracking-wide text-muted-foreground">
                  Rekomendasi Tindakan (HITL)
                </div>
                <p className="mt-0.5 text-xs leading-relaxed text-foreground/90">
                  {profile.recommendedAction}
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-dashed border-border bg-muted/20 p-2 text-center text-[10px] text-muted-foreground">
            Data sintetis untuk purwarupa · keputusan akhir tetap di tangan
            verifikator (Human-in-the-Loop) · kepatuhan UU PDP No. 27/2022
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
