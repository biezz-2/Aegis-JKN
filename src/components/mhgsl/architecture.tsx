"use client";

import { motion } from "framer-motion";
import {
  Database,
  Share2,
  GitBranch,
  Merge,
  ShieldAlert,
  ArrowRight,
} from "lucide-react";
import { PIPELINE } from "./data";
import { useLang } from "./i18n";

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Database,
  Share2,
  GitBranch,
  Merge,
  ShieldAlert,
};

export function Architecture() {
  const { t } = useLang();
  return (
    <section id="architecture" className="relative py-16 sm:py-24 bg-muted/30">
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
            <GitBranch className="h-3.5 w-3.5" />
            {t.archBadge}
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl"
          >
            {t.archTitle1}{" "}
            <span className="gradient-text">SATUSEHAT FHIR</span> {t.archTitle2}{" "}
            <span className="gradient-text">{t.archTitle3}</span>
          </motion.h2>
          <p className="mt-4 text-muted-foreground">{t.archDesc}</p>
        </div>

        {/* Pipeline flow */}
        <div className="mt-12 grid grid-cols-1 gap-3 md:grid-cols-5">
          {PIPELINE.map((p, i) => {
            const Icon = iconMap[p.icon] ?? Database;
            return (
              <motion.div
                key={p.step}
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.45, delay: i * 0.08 }}
                className="relative"
              >
                <div className="card-hover flex h-full flex-col rounded-2xl border border-border/70 bg-card p-4 shadow-sm">
                  <div className="flex items-center justify-between">
                    <span className="rounded-md bg-primary/10 px-2 py-0.5 font-mono text-[11px] font-semibold text-primary">
                      {p.step}
                    </span>
                    <div
                      className="flex h-8 w-8 items-center justify-center rounded-lg"
                      style={{
                        background: "linear-gradient(135deg, color-mix(in oklch, var(--primary) 14%, transparent), color-mix(in oklch, var(--chart-2) 14%, transparent))",
                      }}
                    >
                      <Icon className="h-4 w-4 text-primary" />
                    </div>
                  </div>
                  <h3 className="mt-3 text-sm font-semibold leading-tight">
                    {t.archPipeline[i].title}
                  </h3>
                  <div className="text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
                    {t.archPipeline[i].subtitle}
                  </div>
                  <p className="mt-2 text-xs leading-relaxed text-foreground/75">
                    {t.archPipeline[i].desc}
                  </p>
                </div>

                {i < PIPELINE.length - 1 && (
                  <div
                    className="absolute -right-2.5 top-1/2 z-10 hidden -translate-y-1/2 md:block"
                    aria-hidden
                  >
                    <motion.div
                      initial={{ opacity: 0, x: -4 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.2 + i * 0.08 }}
                      className="flex h-5 w-5 items-center justify-center rounded-full border border-primary/40 bg-background text-primary"
                    >
                      <ArrowRight className="h-3 w-3" />
                    </motion.div>
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>

        {/* Legend: regulatory & data sources */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3"
        >
          <div className="rounded-2xl border border-border/70 bg-card p-4">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <Database className="h-3.5 w-3.5 text-primary" />
              {t.archDataSourcesTitle}
            </div>
            <ul className="mt-2 space-y-1 text-xs text-foreground/80">
              {t.archDataSources.map((d, i) => (
                <li key={d.name}>
                  <strong>{d.name}</strong>
                  {d.desc ? ` — ${d.desc}` : ""}
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border border-border/70 bg-card p-4">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <ShieldAlert className="h-3.5 w-3.5 text-amber-600" />
              {t.archPrivacyTitle}
            </div>
            <ul className="mt-2 space-y-1 text-xs text-foreground/80">
              {t.archPrivacy.map((d) => (
                <li key={d.name}>
                  <strong>{d.name}</strong> — {d.desc}
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border border-border/70 bg-card p-4">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <Merge className="h-3.5 w-3.5 text-teal-600" />
              {t.archOpsTitle}
            </div>
            <ul className="mt-2 space-y-1 text-xs text-foreground/80">
              {t.archOps.map((d) => (
                <li key={d.name}>
                  <strong>{d.name}</strong> — {d.desc}
                </li>
              ))}
            </ul>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
