"use client";

import { motion } from "framer-motion";
import {
  TrendingUp,
  Calendar,
  ShieldCheck,
  Gauge,
  ArrowRight,
} from "lucide-react";
import { useLang } from "./i18n";
import { useCountUp } from "./use-count-up";
import { cn } from "@/lib/utils";

const statusMeta: Record<
  string,
  { id: { label: string; cls: string }; en: { label: string; cls: string } }
> = {
  active: {
    id: { label: "Berlangsung", cls: "bg-primary/10 text-primary border-primary/30" },
    en: { label: "Active", cls: "bg-primary/10 text-primary border-primary/30" },
  },
  next: {
    id: { label: "Berikutnya", cls: "bg-amber-100 text-amber-700 border-amber-200 dark:bg-amber-500/15 dark:text-amber-300 dark:border-amber-500/30" },
    en: { label: "Next", cls: "bg-amber-100 text-amber-700 border-amber-200 dark:bg-amber-500/15 dark:text-amber-300 dark:border-amber-500/30" },
  },
  future: {
    id: { label: "Visi jangka panjang", cls: "bg-muted text-muted-foreground border-border" },
    en: { label: "Long-term vision", cls: "bg-muted text-muted-foreground border-border" },
  },
};

function SavingsCounter() {
  const { ref, raw } = useCountUp(14.4, { duration: 2000, decimals: 1, separator: "," });
  return (
    <span ref={ref} className="tabular-nums">
      Rp {raw.toFixed(1).replace(".", ",")} M
    </span>
  );
}

export function Roadmap() {
  const { t, lang } = useLang();
  return (
    <section className="relative py-16 sm:py-24 bg-muted/30">
      <div className="absolute inset-0 bg-dots opacity-50" aria-hidden />
      <div className="container relative mx-auto max-w-7xl px-4 sm:px-6">
        <div className="grid grid-cols-1 gap-10 lg:grid-cols-2 lg:items-center">
          {/* ROI side */}
          <div>
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4 }}
              className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-3 py-1 text-xs font-medium text-primary"
            >
              <Gauge className="h-3.5 w-3.5" />
              {t.roiBadge}
            </motion.div>
            <motion.h2
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl"
            >
              {t.roiTitle1}{" "}
              <span className="text-muted-foreground line-through">{t.roiTitle2}</span>{" "}
              {lang === "id" ? "ke" : "to"}{" "}
              <span className="gradient-text">{t.roiTitle3}</span> {t.roiTitle4}
            </motion.h2>
            <p className="mt-4 text-sm text-muted-foreground">{t.roiDesc}</p>

            <div className="mt-6 space-y-2.5">
              {t.roiStats.map((r, i) => (
                <motion.div
                  key={r.label}
                  initial={{ opacity: 0, x: -12 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4, delay: i * 0.08 }}
                  className="flex items-center justify-between rounded-xl border border-border/70 bg-card p-3"
                >
                  <div className="text-xs text-muted-foreground">{r.label}</div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-muted-foreground line-through">
                      {r.before}
                    </span>
                    <ArrowRight className="h-3 w-3 text-primary" />
                    <span className="text-sm font-bold text-primary">{r.after}</span>
                  </div>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mt-5 rounded-2xl border border-primary/30 bg-gradient-to-br from-primary/10 to-primary/5 p-4 relative overflow-hidden"
            >
              {/* Decorative shimmer */}
              <div
                className="pointer-events-none absolute -top-12 -right-12 h-32 w-32 rounded-full opacity-20 blur-2xl"
                style={{ background: "var(--primary)" }}
                aria-hidden
              />
              <div className="relative">
                <div className="flex items-center gap-2 text-sm font-semibold text-primary">
                  <TrendingUp className="h-4 w-4" />
                  {t.roiSavingsTitle}
                </div>
                <div className="mt-1 text-3xl font-bold">
                  <SavingsCounter />
                  <span className="ml-2 text-sm font-medium text-muted-foreground">
                    {t.roiSavingsSub}
                  </span>
                </div>
                <p className="mt-1 text-xs text-muted-foreground">{t.roiSavingsDesc}</p>
              </div>
            </motion.div>
          </div>

          {/* Roadmap side */}
          <div>
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4 }}
              className="inline-flex items-center gap-2 rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700 dark:bg-amber-500/15 dark:text-amber-300 dark:border-amber-500/30"
            >
              <Calendar className="h-3.5 w-3.5" />
              {t.roadmapBadge}
            </motion.div>
            <h2 className="mt-4 text-2xl font-bold tracking-tight sm:text-3xl">
              {t.roadmapTitle}
            </h2>

            <div className="mt-5 space-y-3">
              {t.roadmapPhases.map((phase, i) => {
                const statusOrder: ("active" | "next" | "future")[] = ["active", "next", "future", "future"];
                const status = statusOrder[i] ?? "future";
                const meta = statusMeta[status][lang];
                return (
                  <motion.div
                    key={phase.phase}
                    initial={{ opacity: 0, x: 12 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.4, delay: i * 0.1 }}
                    className="relative rounded-2xl border border-border/70 bg-card p-4"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-xs font-bold text-primary">
                          {phase.phase}
                        </span>
                        <span className="text-xs text-muted-foreground">
                          {phase.period}
                        </span>
                      </div>
                      <span
                        className={cn(
                          "rounded-full border px-2 py-0.5 text-[10px] font-medium",
                          meta.cls
                        )}
                      >
                        {meta.label}
                      </span>
                    </div>
                    <div className="mt-1.5 text-sm font-semibold">{phase.title}</div>
                    <ul className="mt-2 space-y-1">
                      {phase.items.map((it) => (
                        <li
                          key={it}
                          className="flex items-start gap-1.5 text-xs text-muted-foreground"
                        >
                          <ShieldCheck className="mt-0.5 h-3 w-3 shrink-0 text-primary/70" />
                          {it}
                        </li>
                      ))}
                    </ul>
                  </motion.div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
