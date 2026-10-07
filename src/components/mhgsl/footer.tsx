"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Network, ShieldCheck, Activity, Github, Heart } from "lucide-react";
import { useLang } from "./i18n";

export function Footer() {
  const { t } = useLang();
  const linkColumns = [
    { title: t.footerModulViz, items: t.footerModulItems },
    { title: t.footerSumber, items: t.footerSumberItems },
    { title: t.footerEco, items: t.footerEcoItems },
  ];

  return (
    <footer className="relative mt-auto border-t border-border/70 bg-gradient-to-b from-background to-muted/40">
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/40 to-transparent" />
      <div className="container mx-auto max-w-7xl px-4 py-12 sm:px-6">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="md:col-span-1"
          >
            <div className="flex items-center gap-2.5">
              <div
                className="flex h-9 w-9 items-center justify-center rounded-xl shadow-sm"
                style={{
                  background:
                    "linear-gradient(135deg, var(--primary), var(--chart-2))",
                }}
              >
                <Network className="h-4.5 w-4.5 text-primary-foreground" />
              </div>
              <div>
                <div className="text-sm font-bold">{t.navBrand}</div>
                <div className="text-[10px] text-muted-foreground">{t.footerTagline}</div>
              </div>
            </div>
            <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
              {t.footerDesc}
            </p>
            <div className="mt-3 flex flex-wrap gap-2 text-[10px]">
              <span className="inline-flex items-center gap-1 rounded-md bg-primary/10 px-2 py-0.5 font-semibold text-primary">
                <ShieldCheck className="h-3 w-3" /> {t.footerPrivacyBadge}
              </span>
              <span className="inline-flex items-center gap-1 rounded-md bg-amber-100 px-2 py-0.5 font-semibold text-amber-700 dark:bg-amber-500/15 dark:text-amber-300">
                <Activity className="h-3 w-3" /> {t.footerHitlBadge}
              </span>
            </div>
          </motion.div>

          {linkColumns.map((col) => (
            <div key={col.title}>
              <div className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                {col.title}
              </div>
              <ul className="mt-3 space-y-2">
                {col.items.map((it) => (
                  <li key={it.label}>
                    {it.href.startsWith("/") ? (
                      <Link
                        href={it.href}
                        className="text-xs text-foreground/80 hover:text-primary transition-colors"
                      >
                        {it.label}
                      </Link>
                    ) : (
                      <a
                        href={it.href}
                        className="text-xs text-foreground/80 hover:text-primary transition-colors"
                        target={it.href.startsWith("http") ? "_blank" : undefined}
                        rel={it.href.startsWith("http") ? "noopener noreferrer" : undefined}
                      >
                        {it.label}
                      </a>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-10 flex flex-col items-center justify-between gap-3 border-t border-border/60 pt-5 text-[11px] text-muted-foreground sm:flex-row">
          <div className="flex items-center gap-1.5">
            <span>{t.footerCopyright}</span>
            <span className="text-primary/40">·</span>
            <span className="inline-flex items-center gap-1">
              <Heart className="h-3 w-3 text-rose-500" /> Detect Smarter, Protect JKN
            </span>
          </div>
          <div className="flex items-center gap-3">
            <a href="#top" className="hover:text-primary transition-colors">
              {t.footerBackTop}
            </a>
            <span className="text-muted-foreground/40">|</span>
            <a
              href="https://github.com/biezz-2/Aegis-JKN"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 hover:text-primary transition-colors"
            >
              <Github className="h-3 w-3" /> {t.footerSource}
            </a>
          </div>
        </div>

        <div className="mt-4 rounded-lg border border-dashed border-border/60 bg-muted/20 p-2 text-center text-[10px] text-muted-foreground">
          {t.footerDisclaimer}
        </div>
      </div>
    </footer>
  );
}
