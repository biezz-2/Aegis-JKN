"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Play,
  Pause,
  RotateCcw,
  ChevronRight,
  Activity,
  ShieldAlert,
  TrendingUp,
  Layers,
} from "lucide-react";
import {
  SIM_STEPS,
  SHAP_ATTRS,
  CHANNELS,
  CHANNEL_PROGRESS,
} from "./data";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { useLang } from "./i18n";
import { cn } from "@/lib/utils";

const channelColor: Record<string, string> = {
  topology: "oklch(0.55 0.14 165)",
  feature: "oklch(0.62 0.13 200)",
  semantic: "oklch(0.7 0.16 70)",
  fusion: "oklch(0.62 0.22 20)",
};

const channelLabel: Record<string, { id: string; en: string }> = {
  topology: { id: "Topologi", en: "Topology" },
  feature: { id: "Fitur", en: "Feature" },
  semantic: { id: "Semantik", en: "Semantic" },
  fusion: { id: "Fusi", en: "Fusion" },
};

export function Simulation() {
  const { t, lang } = useLang();
  const [stepIdx, setStepIdx] = useState(0);
  const [playing, setPlaying] = useState(false);
  const step = SIM_STEPS[stepIdx];
  const progress = CHANNEL_PROGRESS[stepIdx];

  const next = () => setStepIdx((i) => Math.min(i + 1, SIM_STEPS.length - 1));
  const prev = () => setStepIdx((i) => Math.max(i - 1, 0));
  const reset = () => {
    setStepIdx(0);
    setPlaying(false);
  };

  // Auto-advance when playing using useEffect (cleaner than setTimeout in render)
  useEffect(() => {
    if (!playing) return;
    // If at the last step, stop playing via timeout to avoid setState-in-effect warning
    const id = setTimeout(() => {
      setStepIdx((i) => {
        if (i >= SIM_STEPS.length - 1) {
          setPlaying(false);
          return i;
        }
        return i + 1;
      });
    }, 2200);
    return () => clearTimeout(id);
  }, [playing, stepIdx]);

  const scoreColor =
    step.score >= 0.85
      ? "oklch(0.62 0.22 20)"
      : step.score >= 0.6
      ? "oklch(0.7 0.18 50)"
      : "oklch(0.55 0.14 165)";

  const tl = {
    simScaleSafe: t.simScaleSafe,
    simScaleReview: t.simScaleReview,
    simScaleEscalate: t.simScaleEscalate,
  };

  return (
    <section id="simulation" className="relative py-16 sm:py-24 bg-muted/30">
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
            <Activity className="h-3.5 w-3.5" />
            {t.simBadge}
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl"
          >
            {t.simTitle1} <span className="gradient-text">{t.simTitle2}</span>
          </motion.h2>
          <p className="mt-4 text-muted-foreground">{t.simDesc}</p>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-5 lg:grid-cols-3">
          {/* Step navigation */}
          <div className="space-y-2">
            <div className="rounded-2xl border border-border/70 bg-card p-3">
              <div className="px-1 text-[11px] font-semibold uppercase tracking-wide text-muted-foreground">
                {t.simStagesLabel}
              </div>
              <div className="mt-2 space-y-1.5">
                {SIM_STEPS.map((s, i) => {
                  const ch = channelColor[s.channel];
                  return (
                    <button
                      key={s.id}
                      onClick={() => setStepIdx(i)}
                      className={cn(
                        "relative w-full rounded-lg border p-2.5 text-left transition-all",
                        i === stepIdx
                          ? "border-transparent shadow-sm"
                          : "border-border/60 hover:border-border"
                      )}
                      style={
                        i === stepIdx
                          ? { background: `${ch}12`, borderColor: `${ch}55` }
                          : undefined
                      }
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span
                            className="flex h-6 w-6 items-center justify-center rounded-full text-[10px] font-bold text-white"
                            style={{ background: ch }}
                          >
                            {i + 1}
                          </span>
                          <span className="text-xs font-semibold">{s.title}</span>
                        </div>
                        {i === stepIdx && (
                          <ChevronRight className="h-3 w-3" style={{ color: ch }} />
                        )}
                      </div>
                      <div className="mt-0.5 pl-8 text-[10px] text-muted-foreground capitalize">
                        {lang === "id" ? "saluran:" : "channel:"} {channelLabel[s.channel]?.[lang] || s.channel}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="rounded-2xl border border-border/70 bg-card p-3">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wide text-muted-foreground">
                  {t.simControlsLabel}
                </span>
                <button
                  onClick={reset}
                  className="text-[10px] font-medium text-muted-foreground hover:text-primary inline-flex items-center gap-1"
                >
                  <RotateCcw className="h-3 w-3" /> {t.simReset}
                </button>
              </div>
              <div className="mt-2 flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={prev}
                  disabled={stepIdx === 0}
                  className="flex-1"
                >
                  {t.simPrev}
                </Button>
                <Button
                  size="sm"
                  onClick={() => setPlaying((p) => !p)}
                  className="flex-1 gap-1.5"
                  disabled={stepIdx === SIM_STEPS.length - 1 && !playing}
                >
                  {playing ? <Pause className="h-3 w-3" /> : <Play className="h-3 w-3" />}
                  {playing ? t.simPause : t.simAutoPlay}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={next}
                  disabled={stepIdx === SIM_STEPS.length - 1}
                  className="flex-1"
                >
                  {t.simNext}
                </Button>
              </div>
            </div>
          </div>

          {/* Active step content */}
          <div className="lg:col-span-2">
            <AnimatePresence mode="wait">
              <motion.div
                key={step.id}
                initial={{ opacity: 0, x: 16 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -16 }}
                transition={{ duration: 0.35 }}
                className="rounded-2xl border border-border/70 bg-card p-5 shadow-sm"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div
                      className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide"
                      style={{
                        background: `${channelColor[step.channel]}20`,
                        color: channelColor[step.channel],
                      }}
                    >
                      {lang === "id" ? "Tahap" : "Stage"} {stepIdx + 1} / {SIM_STEPS.length}
                    </div>
                    <h3 className="mt-2 text-xl font-bold">{step.title}</h3>
                  </div>
                  <div className="text-right">
                    <div className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">
                      {t.simScoreLabel}
                    </div>
                    <div
                      className="text-3xl font-bold tabular-nums"
                      style={{ color: scoreColor }}
                    >
                      {step.score.toFixed(2)}
                    </div>
                  </div>
                </div>

                <p className="mt-3 text-sm leading-relaxed text-foreground/85">
                  {step.desc}
                </p>

                <div
                  className="mt-4 rounded-xl border-l-4 p-3"
                  style={{
                    borderColor: channelColor[step.channel],
                    background: `${channelColor[step.channel]}0a`,
                  }}
                >
                  <div className="flex items-start gap-2">
                    <TrendingUp
                      className="h-4 w-4 shrink-0 mt-0.5"
                      style={{ color: channelColor[step.channel] }}
                    />
                    <div>
                      <div className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">
                        {t.simInsightLabel}
                      </div>
                      <p className="mt-0.5 text-xs leading-relaxed text-foreground/90">
                        {step.insight}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Progressive channel contribution — animated per step */}
                <div className="mt-4 rounded-xl border border-border/60 p-3">
                  <div className="flex items-center gap-1.5 text-[11px] font-semibold text-foreground/80 mb-2">
                    <Layers className="h-3.5 w-3.5 text-primary" />
                    {lang === "id" ? "Akumulasi kontribusi saluran" : "Channel contribution accumulation"}
                  </div>
                  <div className="space-y-2">
                    {(["topology", "feature", "semantic"] as const).map((ch) => {
                      const c = channelColor[ch];
                      const v = progress[ch] as number;
                      const isPos = v >= 0;
                      const visible = v !== 0;
                      return (
                        <div key={ch} className="flex items-center gap-2">
                          <div className="w-16 shrink-0 text-[10px] font-medium text-muted-foreground">
                            {channelLabel[ch][lang]}
                          </div>
                          <div className="relative flex-1 h-2.5 rounded-full bg-muted/50 overflow-hidden">
                            <div className="absolute left-1/2 top-0 h-full w-px bg-border/80" />
                            {visible && (
                              <motion.div
                                key={`${stepIdx}-${ch}`}
                                initial={{ width: 0 }}
                                animate={{
                                  width: `${Math.min(50, Math.abs(v) * 100)}%`,
                                }}
                                transition={{ duration: 0.5, ease: "easeOut" }}
                                className="absolute top-0 h-full rounded-full"
                                style={{
                                  background: c,
                                  left: isPos ? "50%" : `${50 - Math.min(50, Math.abs(v) * 100)}%`,
                                  opacity: 0.85,
                                }}
                              />
                            )}
                          </div>
                          <div
                            className="w-12 text-right text-[10px] font-mono tabular-nums"
                            style={{ color: c }}
                          >
                            {visible ? (isPos ? "+" : "") + v.toFixed(2) : "—"}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  <div className="mt-2.5 flex items-center justify-between border-t border-border/40 pt-2 text-[10px]">
                    <span className="font-semibold text-muted-foreground">{lang === "id" ? "Fusi" : "Fusion"}</span>
                    <span className="font-bold tabular-nums" style={{ color: channelColor.fusion }}>
                      {progress.fusion.toFixed(2)}
                    </span>
                  </div>
                </div>

                {/* Fraud score gauge */}
                <div className="mt-4">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="font-semibold text-muted-foreground">
                      {t.simProbLabel}
                    </span>
                    <span className="font-bold tabular-nums" style={{ color: scoreColor }}>
                      {(step.score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <Progress
                    value={step.score * 100}
                    className="mt-1.5 h-2.5"
                    style={{
                      // @ts-expect-error CSS var
                      "--progress-foreground": scoreColor,
                    } as React.CSSProperties}
                  />
                  <div className="mt-1.5 flex justify-between text-[10px] text-muted-foreground">
                    <span>{tl.simScaleSafe}</span>
                    <span>{tl.simScaleReview}</span>
                    <span>{tl.simScaleEscalate}</span>
                  </div>
                </div>

                {/* SHAP appears at final step */}
                {stepIdx === SIM_STEPS.length - 1 && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="mt-4 rounded-xl border border-amber-200 bg-amber-50/50 p-3 dark:border-amber-500/30 dark:bg-amber-500/10"
                  >
                    <div className="flex items-center gap-1.5 text-[11px] font-semibold text-amber-700 dark:text-amber-300">
                      <ShieldAlert className="h-3.5 w-3.5" />
                      {t.simShapTitle}
                    </div>
                    <div className="mt-2 space-y-1.5">
                      {SHAP_ATTRS.map((s) => {
                        const ch = channelColor[s.channel];
                        const isPos = s.shap >= 0;
                        return (
                          <div key={s.feature} className="flex items-center gap-2">
                            <div className="w-44 truncate text-[11px] text-foreground/85">
                              {s.feature}
                            </div>
                            <div className="relative flex-1 h-3 rounded-full bg-muted/60 overflow-hidden">
                              <div className="absolute left-1/2 top-0 h-full w-px bg-border" />
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${Math.abs(s.shap) * 200}%` }}
                                transition={{ duration: 0.5 }}
                                className="absolute top-0 h-full rounded-full"
                                style={{
                                  background: ch,
                                  left: isPos ? "50%" : `${50 - Math.abs(s.shap) * 100 * 2}%`,
                                  right: isPos ? undefined : "50%",
                                  opacity: 0.85,
                                }}
                              />
                            </div>
                            <div
                              className="w-12 text-right text-[11px] font-mono tabular-nums"
                              style={{ color: isPos ? "oklch(0.55 0.16 20)" : "oklch(0.55 0.14 165)" }}
                            >
                              {isPos ? "+" : ""}
                              {s.shap.toFixed(2)}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    <p className="mt-2 text-[11px] text-amber-800/80 dark:text-amber-200/80">
                      {t.simVerdict}
                    </p>
                  </motion.div>
                )}
              </motion.div>
            </AnimatePresence>

            {/* Step progress dots */}
            <div className="mt-3 flex items-center justify-center gap-1.5">
              {SIM_STEPS.map((s, i) => (
                <button
                  key={s.id}
                  onClick={() => setStepIdx(i)}
                  className="h-1.5 rounded-full transition-all"
                  style={{
                    width: i === stepIdx ? 28 : 12,
                    background:
                      i === stepIdx ? channelColor[s.channel] : "var(--muted)",
                  }}
                  aria-label={`${lang === "id" ? "Pergi ke tahap" : "Go to stage"} ${i + 1}`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
