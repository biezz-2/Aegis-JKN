"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Network,
  Activity,
  GitBranch,
  Sigma,
  BarChart3,
  GitMerge,
  Menu,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "./theme-toggle";
import { LangToggle } from "./lang-toggle";
import { ShortcutsHint } from "./shortcuts-hint";
import { GlossaryButton } from "./glossary";
import { useLang } from "./i18n";
import { Sheet, SheetContent, SheetTrigger, SheetHeader, SheetTitle } from "@/components/ui/sheet";

const NAV_ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  problem: Network,
  architecture: GitBranch,
  graph: Network,
  simulation: Activity,
  math: Sigma,
  compare: BarChart3,
  ring: GitMerge,
};

export function Navbar() {
  const { t } = useLang();
  const [scrolled, setScrolled] = useState(false);
  const [active, setActive] = useState("problem");
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActive(e.target.id);
        });
      },
      { rootMargin: "-40% 0px -55% 0px" }
    );
    t.navItems.forEach((n) => {
      const el = document.getElementById(n.id);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, [t]);

  return (
    <motion.header
      initial={{ y: -24, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className={cn(
        "sticky top-0 z-50 w-full transition-all duration-300",
        scrolled ? "glass shadow-sm" : "bg-transparent"
      )}
    >
      <div className="container mx-auto max-w-7xl px-4 sm:px-6">
        <div className="flex h-14 items-center justify-between gap-2">
          <a href="#top" className="flex items-center gap-2.5 shrink-0">
            <div
              className="flex h-8 w-8 items-center justify-center rounded-lg shadow-sm"
              style={{
                background:
                  "linear-gradient(135deg, var(--primary), var(--chart-2))",
              }}
            >
              <Network className="h-4 w-4 text-primary-foreground" />
            </div>
            <div className="hidden sm:block">
              <div className="text-sm font-bold leading-none">{t.navBrand}</div>
              <div className="text-[10px] text-muted-foreground leading-none mt-0.5">
                {t.navTagline}
              </div>
            </div>
          </a>

          <nav className="hidden lg:flex items-center gap-0.5 overflow-x-auto scrollbar-thin">
            {t.navItems.map((n) => (
              <a
                key={n.id}
                href={`#${n.id}`}
                className={cn(
                  "relative rounded-md px-3 py-1.5 text-xs font-medium transition-colors",
                  active === n.id
                    ? "text-primary"
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                {active === n.id && (
                  <motion.span
                    layoutId="nav-active"
                    className="absolute inset-0 rounded-md bg-primary/10"
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  />
                )}
                <span className="relative">{n.label}</span>
              </a>
            ))}
          </nav>

          <div className="flex items-center gap-1.5">
            <div className="hidden sm:block">
              <GlossaryButton />
            </div>
            <ShortcutsHint />
            <LangToggle />
            <ThemeToggle />
            {/* Desktop CTA */}
            <a
              href="#simulation"
              className="hidden sm:inline-flex items-center gap-1.5 rounded-full bg-primary px-3.5 py-1.5 text-xs font-medium text-primary-foreground shadow-sm transition-transform hover:scale-105"
            >
              <Activity className="h-3.5 w-3.5" />
              <span className="hidden md:inline">{t.navCta}</span>
            </a>

            {/* Mobile drawer trigger */}
            <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
              <SheetTrigger asChild>
                <button
                  aria-label={t.navOpenMenu}
                  className="lg:hidden inline-flex h-9 w-9 items-center justify-center rounded-full border border-border bg-background/60 text-foreground hover:bg-accent transition-colors"
                >
                  <Menu className="h-4 w-4" />
                </button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[300px] sm:w-[340px] p-0">
                <SheetHeader className="px-5 pt-5 pb-3 border-b border-border">
                  <SheetTitle className="flex items-center gap-2 text-left">
                    <div
                      className="flex h-7 w-7 items-center justify-center rounded-lg"
                      style={{
                        background:
                          "linear-gradient(135deg, var(--primary), var(--chart-2))",
                      }}
                    >
                      <Network className="h-3.5 w-3.5 text-primary-foreground" />
                    </div>
                    <span className="text-sm font-bold">{t.navQuickNav}</span>
                  </SheetTitle>
                </SheetHeader>
                <nav className="flex flex-col gap-1 p-3">
                  {t.navItems.map((n) => {
                    const Icon = NAV_ICONS[n.id] ?? Network;
                    return (
                      <a
                        key={n.id}
                        href={`#${n.id}`}
                        onClick={() => setMobileOpen(false)}
                        className={cn(
                          "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                          active === n.id
                            ? "bg-primary/10 text-primary"
                            : "text-foreground hover:bg-accent"
                        )}
                      >
                        <span
                          className={cn(
                            "flex h-7 w-7 items-center justify-center rounded-md",
                            active === n.id
                              ? "bg-primary/15 text-primary"
                              : "bg-muted text-muted-foreground"
                          )}
                        >
                          <Icon className="h-3.5 w-3.5" />
                        </span>
                        <span className="flex-1">{n.label}</span>
                        {active === n.id && (
                          <span className="h-1.5 w-1.5 rounded-full bg-primary" />
                        )}
                      </a>
                    );
                  })}
                </nav>
                <div className="px-5 py-4 border-t border-border mt-auto">
                  <a
                    href="#simulation"
                    onClick={() => setMobileOpen(false)}
                    className="flex items-center justify-center gap-2 rounded-full bg-primary px-4 py-2 text-xs font-medium text-primary-foreground shadow-sm"
                  >
                    <Activity className="h-3.5 w-3.5" />
                    {t.navCta}
                  </a>
                  <p className="mt-3 text-center text-[10px] text-muted-foreground">
                    {t.navBrand} · {t.navTagline}
                  </p>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </motion.header>
  );
}
