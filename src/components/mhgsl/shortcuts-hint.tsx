"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Keyboard, X } from "lucide-react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { useLang } from "./i18n";

const SHORTCUTS_ID = [
  { key: "T", action: { id: "Toggle theme", en: "Toggle theme" } },
  { key: "P", action: { id: "Print / Export PDF", en: "Print / Export PDF" } },
  { key: "G", action: { id: "Lompat ke graf", en: "Jump to graph" } },
  { key: "S", action: { id: "Lompat ke simulasi", en: "Jump to simulation" } },
  { key: "→", action: { id: "Tahap simulasi berikutnya", en: "Next simulation step" } },
  { key: "←", action: { id: "Tahap simulasi sebelumnya", en: "Previous simulation step" } },
];

export function ShortcutsHint() {
  const { lang } = useLang();
  return (
    <Popover>
      <PopoverTrigger asChild>
        <button
          aria-label="Keyboard shortcuts"
          title="Keyboard shortcuts"
          className="hidden sm:inline-flex h-9 w-9 items-center justify-center rounded-full border border-border bg-background/60 text-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
        >
          <Keyboard className="h-4 w-4" />
        </button>
      </PopoverTrigger>
      <PopoverContent
        align="end"
        sideOffset={6}
        className="w-72 p-3"
      >
        <div className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">
          {lang === "id" ? "Pintasan Keyboard" : "Keyboard Shortcuts"}
        </div>
        <ul className="space-y-1.5">
          {SHORTCUTS_ID.map((s) => (
            <li key={s.key} className="flex items-center justify-between text-xs">
              <span className="text-foreground/80">{lang === "id" ? s.action.id : s.action.en}</span>
              <kbd className="inline-flex h-5 min-w-5 items-center justify-center rounded-md border border-border bg-muted px-1.5 font-mono text-[10px] font-semibold shadow-sm">
                {s.key}
              </kbd>
            </li>
          ))}
        </ul>
      </PopoverContent>
    </Popover>
  );
}
