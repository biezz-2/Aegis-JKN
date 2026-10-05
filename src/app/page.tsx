"use client";

import * as React from "react";
import { Navbar } from "@/components/mhgsl/navbar";
import { Hero } from "@/components/mhgsl/hero";
import { ProblemSection } from "@/components/mhgsl/problem-section";
import { Architecture } from "@/components/mhgsl/architecture";
import { MultiChannelGraph } from "@/components/mhgsl/multi-channel-graph";
import { Simulation } from "@/components/mhgsl/simulation";
import { MathFormulas } from "@/components/mhgsl/math-formulas";
import { Comparison } from "@/components/mhgsl/comparison";
import { FraudRing } from "@/components/mhgsl/fraud-ring";
import { Roadmap } from "@/components/mhgsl/roadmap";
import { Footer } from "@/components/mhgsl/footer";
import { BackToTop } from "@/components/mhgsl/back-to-top";
import { useTheme } from "next-themes";
import { useKeyboardShortcuts, type ShortcutDef } from "@/components/mhgsl/use-keyboard-shortcuts";
import { toast } from "sonner";

export default function Home() {
  const { setTheme, resolvedTheme } = useTheme();

  const shortcuts = React.useMemo<ShortcutDef[]>(
    () => [
      {
        key: "t",
        description: "Toggle theme",
        handler: () => {
          const isDark = (typeof document !== "undefined" && document.documentElement.classList.contains("dark")) || resolvedTheme === "dark";
          setTheme(isDark ? "light" : "dark");
          toast.success(isDark ? "Mode terang aktif" : "Mode gelap aktif");
        },
      },
      {
        key: "p",
        description: "Print / Export PDF",
        handler: () => {
          if (typeof window !== "undefined") window.print();
        },
      },
      {
        key: "g",
        description: "Scroll to graph",
        handler: () => {
          document.getElementById("graph")?.scrollIntoView({ behavior: "smooth" });
        },
      },
      {
        key: "s",
        description: "Scroll to simulation",
        handler: () => {
          document.getElementById("simulation")?.scrollIntoView({ behavior: "smooth" });
        },
      },
      {
        key: "ArrowRight",
        description: "Next simulation step (when simulation in view)",
        handler: () => {
          const btn = document.querySelector<HTMLButtonElement>(
            "#simulation button:not([disabled])"
          );
          // Try to find the "Next" button specifically
          const nextBtn = Array.from(
            document.querySelectorAll<HTMLButtonElement>("#simulation button")
          ).find((b) => b.textContent?.trim() === "Next");
          (nextBtn || btn)?.click();
        },
      },
      {
        key: "ArrowLeft",
        description: "Previous simulation step",
        handler: () => {
          const prevBtn = Array.from(
            document.querySelectorAll<HTMLButtonElement>("#simulation button")
          ).find((b) => b.textContent?.trim() === "Prev");
          prevBtn?.click();
        },
      },
    ],
    [setTheme, resolvedTheme]
  );
  useKeyboardShortcuts(shortcuts);

  return (
    <div
      id="top"
      className="relative flex min-h-screen flex-col bg-background"
    >
      <Navbar />
      <main className="flex-1">
        <Hero />
        <ProblemSection />
        <Architecture />
        <MultiChannelGraph />
        <Simulation />
        <MathFormulas />
        <Comparison />
        <FraudRing />
        <Roadmap />
      </main>
      <Footer />
      <BackToTop />
    </div>
  );
}
