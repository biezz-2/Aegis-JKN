"use client";

import * as React from "react";
import { Languages } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import { useLang, type Lang } from "./i18n";

export function LangToggle({ className }: { className?: string }) {
  const { lang, setLang } = useLang();

  return (
    <div
      className={cn(
        "relative inline-flex h-9 items-center rounded-full border border-border bg-background/60 p-0.5",
        className
      )}
    >
      {(["id", "en"] as Lang[]).map((l) => (
        <button
          key={l}
          type="button"
          aria-label={`Switch to ${l === "id" ? "Bahasa Indonesia" : "English"}`}
          onClick={() => setLang(l)}
          className={cn(
            "relative inline-flex h-8 items-center justify-center gap-1 rounded-full px-2.5 text-[11px] font-semibold transition-colors",
            lang === l
              ? "text-primary-foreground"
              : "text-muted-foreground hover:text-foreground"
          )}
        >
          {lang === l && (
            <motion.span
              layoutId="lang-active"
              className="absolute inset-0 rounded-full bg-primary shadow-sm"
              transition={{ type: "spring", stiffness: 380, damping: 30 }}
            />
          )}
          <span className="relative z-10 uppercase">{l}</span>
        </button>
      ))}
    </div>
  );
}
