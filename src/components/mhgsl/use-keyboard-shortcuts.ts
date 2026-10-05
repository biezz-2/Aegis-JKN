"use client";

import * as React from "react";

type ShortcutHandler = (e: KeyboardEvent) => void;

export interface ShortcutDef {
  key: string;
  description: string;
  handler: ShortcutHandler;
  ctrlKey?: boolean;
  metaKey?: boolean;
  shiftKey?: boolean;
  altKey?: boolean;
}

/**
 * useKeyboardShortcuts — registers global keyboard shortcuts.
 * Skips when the user is typing in an input/textarea/contentEditable.
 */
export function useKeyboardShortcuts(shortcuts: ShortcutDef[]) {
  React.useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      const tag = target?.tagName?.toUpperCase();
      if (
        tag === "INPUT" ||
        tag === "TEXTAREA" ||
        tag === "SELECT" ||
        target?.isContentEditable
      ) {
        return;
      }
      for (const s of shortcuts) {
        const keyMatch =
          e.key.toLowerCase() === s.key.toLowerCase();
        const ctrlMatch = !!s.ctrlKey === (e.ctrlKey || e.metaKey);
        const shiftMatch = !!s.shiftKey === e.shiftKey;
        const altMatch = !!s.altKey === e.altKey;
        if (keyMatch && ctrlMatch && shiftMatch && altMatch) {
          e.preventDefault();
          s.handler(e);
          break;
        }
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [shortcuts]);
}
