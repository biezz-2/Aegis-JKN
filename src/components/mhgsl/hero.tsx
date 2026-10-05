"use client";

import { motion } from "framer-motion";
import { ShieldCheck, Activity, Network, ArrowDown, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { HERO_STATS } from "./data";
import { useCountUp } from "./use-count-up";
import { useLang } from "./i18n";

const accentMap: Record<string, string> = {
  primary: "text-primary",
  rose: "text-rose-600 dark:text-rose-400",
  amber: "text-amber-600 dark:text-amber-400",
  teal: "text-teal-600 dark:text-teal-400",
};

const accentGlow: Record<string, string> = {
  primary: "oklch(0.55 0.14 165)",
  rose: "oklch(0.62 0.22 20)",
  amber: "oklch(0.7 0.16 70)",
  teal: "oklch(0.62 0.13 200)",
};

function StatCard({
  stat,
  index,
}: {
  stat: (typeof HERO_STATS)[number];
  index: number;
}) {
  const { ref, display } = useCountUp(stat.numericValue, {
    duration: 1800 + index * 200,
    prefix: stat.prefix,
    suffix: stat.suffix,
  });

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.96, y: 12 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.32 + index * 0.06 }}
      className="card-hover group relative overflow-hidden rounded-2xl border border-border/70 bg-card/80 p-4 text-center shadow-sm sm:p-5"
    >
      {/* Gradient border glow on hover */}
      <div
        className="pointer-events-none absolute -inset-px rounded-2xl opacity-0 transition-opacity duration-300 group-hover:opacity-100"
        style={{
          background: `linear-gradient(135deg, ${accentGlow[stat.accent]}, transparent 60%)`,
          padding: 1,
          WebkitMask:
            "linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)",
          WebkitMaskComposite: "xor",
          maskComposite: "exclude",
        }}
        aria-hidden
      />
      <div
        className="absolute -top-px left-1/2 h-px w-2/3 -translate-x-1/2"
        style={{
          background: `linear-gradient(90deg, transparent, ${accentGlow[stat.accent]}, transparent)`,
        }}
        aria-hidden
      />
      <div
        className={`text-2xl font-bold tracking-tight sm:text-3xl ${accentMap[stat.accent]}`}
      >
        <span ref={ref} className="tabular-nums">
          {display}
        </span>
      </div>
      <div className="mt-1.5 text-xs text-muted-foreground sm:text-sm">
        {stat.label}
      </div>
      <div
        className="absolute bottom-0 left-0 h-1 w-full opacity-70 transition-opacity group-hover:opacity-100"
        style={{
          background: `linear-gradient(90deg, transparent, ${accentGlow[stat.accent]}66, transparent)`,
        }}
        aria-hidden
      />
    </motion.div>
  );
}

export function Hero() {
  const { t, lang } = useLang();

  return (
    <section className="relative overflow-hidden pt-10 pb-16 sm:pt-14 sm:pb-20">
      {/* Background layers */}
      <div className="absolute inset-0 bg-grid opacity-60" aria-hidden />
      <div
        className="absolute inset-0"
        aria-hidden
        style={{
          background:
            "radial-gradient(60% 50% at 50% 0%, color-mix(in oklch, var(--primary) 18%, transparent), transparent 70%)",
        }}
      />
      <div
        className="absolute -top-24 -right-20 h-72 w-72 rounded-full opacity-40 blur-3xl animate-float-slow"
        aria-hidden
        style={{ background: "color-mix(in oklch, var(--chart-3) 40%, transparent)" }}
      />
      <div
        className="absolute -bottom-32 -left-24 h-80 w-80 rounded-full opacity-30 blur-3xl animate-float-slow"
        aria-hidden
        style={{ background: "color-mix(in oklch, var(--primary) 40%, transparent)" }}
      />

      <div className="container relative mx-auto max-w-7xl px-4 sm:px-6">
        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-4 py-1.5 text-xs font-medium text-primary"
          >
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-pulse-ring rounded-full bg-primary/60" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-primary" />
            </span>
            {t.heroBadge}
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.05 }}
            className="mt-6 text-balance text-4xl font-bold leading-tight tracking-tight sm:text-5xl md:text-6xl"
          >
            {t.heroTitle1}{" "}
            <span className="gradient-text">MHGSL &amp; GNN</span>
            <br className="hidden sm:block" /> {t.heroTitle2}
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.12 }}
            className="mx-auto mt-6 max-w-2xl text-balance text-base text-muted-foreground sm:text-lg"
          >
            Multi-channel Heterogeneous Graph Structure Learning{" "}
            {lang === "id" ? "memadukan tiga perspektif graf—" : "fuses three graph perspectives—"}
            <strong className="text-foreground">{t.heroSubtitleTopologi}</strong>,{" "}
            <strong className="text-foreground">{t.heroSubtitleFitur}</strong>,{" "}
            {lang === "id" ? "dan" : "and"}{" "}
            <strong className="text-foreground">{t.heroSubtitleSemantik}</strong>
            {lang === "id" ? "—" : "—"}
            {t.heroSubtitleEnd}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mt-8 flex flex-wrap items-center justify-center gap-3"
          >
            <Button asChild size="lg" className="gap-2 group">
              <a href="#simulation">
                <Activity className="h-4 w-4 transition-transform group-hover:scale-110" />
                {t.heroCta1}
              </a>
            </Button>
            <Button
              asChild
              size="lg"
              variant="outline"
              className="gap-2 bg-background/60"
            >
              <a href="#architecture">
                <Network className="h-4 w-4" />
                {t.heroCta2}
              </a>
            </Button>
          </motion.div>

          {/* Inline mini badge */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.35 }}
            className="mt-5 inline-flex items-center gap-1.5 rounded-full bg-amber-100/70 px-3 py-1 text-[11px] font-medium text-amber-800 dark:bg-amber-500/15 dark:text-amber-300"
          >
            <Sparkles className="h-3 w-3" />
            {t.heroMiniBadge}
          </motion.div>
        </div>

        {/* Stats grid */}
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.28 }}
          className="mt-10 grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4"
        >
          {HERO_STATS.map((s, i) => (
            <StatCard key={s.label} stat={s} index={i} />
          ))}
        </motion.div>

        {/* Trust strip */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="mt-8 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs text-muted-foreground"
        >
          {t.heroTrust.map(([a, b]) => (
            <div key={a} className="flex items-center gap-1.5">
              <ShieldCheck className="h-3.5 w-3.5 text-primary/70" />
              <span className="font-semibold text-foreground/80">{a}</span>
              <span className="text-muted-foreground/80">·</span>
              <span>{b}</span>
            </div>
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.9, duration: 0.6 }}
          className="mt-8 flex justify-center"
        >
          <a
            href="#problem"
            className="inline-flex flex-col items-center gap-1 text-xs text-muted-foreground hover:text-primary transition-colors"
          >
            <span>{t.heroScroll}</span>
            <motion.span
              animate={{ y: [0, 6, 0] }}
              transition={{ repeat: Infinity, duration: 1.6, ease: "easeInOut" }}
            >
              <ArrowDown className="h-4 w-4" />
            </motion.span>
          </a>
        </motion.div>
      </div>
    </section>
  );
}
