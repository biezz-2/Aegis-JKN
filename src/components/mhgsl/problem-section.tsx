"use client";

import { motion } from "framer-motion";
import {
  Hospital,
  User,
  Building2,
  Stethoscope,
  Syringe,
  ClipboardList,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";
import { useLang } from "./i18n";
import { cn } from "@/lib/utils";

const accentMap: Record<string, { bg: string; text: string; ring: string }> = {
  rose: { bg: "bg-rose-50 dark:bg-rose-500/10", text: "text-rose-700 dark:text-rose-300", ring: "ring-rose-200 dark:ring-rose-500/30" },
  amber: { bg: "bg-amber-50 dark:bg-amber-500/10", text: "text-amber-700 dark:text-amber-300", ring: "ring-amber-200 dark:ring-amber-500/30" },
  teal: { bg: "bg-teal-50 dark:bg-teal-500/10", text: "text-teal-700 dark:text-teal-300", ring: "ring-teal-200 dark:ring-teal-500/30" },
};

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Hospital,
  User,
  Building2,
  Stethoscope,
  Syringe,
  ClipboardList,
};

export function ProblemSection() {
  const { t } = useLang();

  return (
    <section id="problem" className="relative py-16 sm:py-24">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6">
        {/* Section header */}
        <div className="mx-auto max-w-3xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
            className="inline-flex items-center gap-2 rounded-full border border-rose-200 bg-rose-50 px-3 py-1 text-xs font-medium text-rose-700 dark:bg-rose-500/15 dark:text-rose-300 dark:border-rose-500/30"
          >
            <AlertTriangle className="h-3.5 w-3.5" />
            {t.problemBadge}
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl"
          >
            {t.problemTitle1}
            <span className="gradient-text"> {t.problemTitle2}</span>
          </motion.h2>
          <p className="mt-4 text-muted-foreground">
            {t.problemDesc1}{" "}
            <strong className="text-foreground">{t.problemDesc2}</strong>
            {t.problemDesc3}
          </p>
        </div>

        {/* Ratio contrast banner */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3"
        >
          <div className="rounded-2xl border border-border/70 bg-card/70 p-5 text-center">
            <div className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
              {t.problemVolumeLabel}
            </div>
            <div className="mt-1 text-3xl font-bold text-primary">±2.000.000</div>
            <div className="mt-1 text-xs text-muted-foreground">
              {t.problemFraudSub === "of national total claim value" ? "submitted by FKRTL across Indonesia" : "diajukan FKRTL seluruh Indonesia"}
            </div>
          </div>
          <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5 text-center dark:bg-rose-500/10 dark:border-rose-500/30">
            <div className="text-xs font-medium uppercase tracking-wide text-rose-700/80 dark:text-rose-300/80">
              {t.problemVerifierLabel}
            </div>
            <div className="mt-1 text-3xl font-bold text-rose-600 dark:text-rose-400">≈1.000</div>
            <div className="mt-1 text-xs text-rose-700/70 dark:text-rose-300/70">
              {t.problemFraudSub === "of national total claim value" ? "ratio 2,000:1 → anomaly gap" : "rasio 2.000 : 1 → celah anomali"}
            </div>
          </div>
          <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5 text-center dark:bg-amber-500/10 dark:border-amber-500/30">
            <div className="text-xs font-medium uppercase tracking-wide text-amber-700/80 dark:text-amber-300/80">
              {t.problemFraudLabel}
            </div>
            <div className="mt-1 text-3xl font-bold text-amber-600 dark:text-amber-400">3–7%</div>
            <div className="mt-1 text-xs text-amber-700/70 dark:text-amber-300/70">
              {t.problemFraudSub}
            </div>
          </div>
        </motion.div>

        {/* Pillars grid */}
        <div className="mt-10 grid grid-cols-1 gap-5 md:grid-cols-3">
          {t.problemPillars.map((p, i) => {
            const acc = i === 0 ? accentMap.rose : i === 1 ? accentMap.amber : accentMap.teal;
            const Icon = i === 0 ? Hospital : i === 1 ? User : Building2;
            return (
              <motion.div
                key={p.title}
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className={cn(
                  "card-hover relative flex flex-col rounded-2xl border bg-card p-5 shadow-sm",
                  p.focus ? "ring-2 " + acc.ring : "border-border/70"
                )}
              >
                {p.focus && (
                  <div className="absolute -top-2.5 right-4 inline-flex items-center gap-1 rounded-full bg-primary px-2.5 py-0.5 text-[10px] font-semibold text-primary-foreground shadow-sm">
                    <CheckCircle2 className="h-3 w-3" /> {t.problemFocus}
                  </div>
                )}
                <div className="flex items-center gap-3">
                  <div
                    className={cn(
                      "flex h-11 w-11 items-center justify-center rounded-xl ring-1",
                      acc.bg,
                      acc.ring
                    )}
                  >
                    <Icon className={cn("h-5 w-5", acc.text)} />
                  </div>
                  <div>
                    <h3 className="text-base font-semibold leading-tight">
                      {p.title}
                    </h3>
                    <p className="text-xs text-muted-foreground">{p.subtitle}</p>
                  </div>
                </div>

                <div className="mt-4 flex flex-wrap gap-1.5">
                  {p.modus.map((m) => (
                    <span
                      key={m}
                      className={cn(
                        "rounded-md px-2 py-0.5 text-[11px] font-medium",
                        acc.bg,
                        acc.text
                      )}
                    >
                      {m}
                    </span>
                  ))}
                </div>

                <div className="mt-4 border-t border-border/60 pt-3">
                  <div className="text-[11px] font-semibold uppercase tracking-wide text-muted-foreground">
                    {t.problemApproachLabel}
                  </div>
                  <p className="mt-1.5 text-xs leading-relaxed text-foreground/80">
                    {p.approach}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
