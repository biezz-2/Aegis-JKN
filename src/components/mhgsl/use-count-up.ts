"use client";

import * as React from "react";

/**
 * useCountUp — animates a number from 0 to `end` once the element enters the viewport.
 * Supports integers, decimal values, and large-number formatting (e.g. 2.000.000).
 */
export function useCountUp(
  end: number,
  options: {
    duration?: number;
    decimals?: number;
    startOnView?: boolean;
    suffix?: string;
    prefix?: string;
    separator?: string;
  } = {}
) {
  const {
    duration = 1800,
    decimals = 0,
    startOnView = true,
    prefix = "",
    suffix = "",
    separator = ".",
  } = options;

  const ref = React.useRef<HTMLSpanElement | null>(null);
  const [display, setDisplay] = React.useState(0);
  const [started, setStarted] = React.useState(false);
  const rafRef = React.useRef<number | null>(null);

  // Trigger on view
  React.useEffect(() => {
    if (!startOnView || !ref.current) {
      setStarted(true);
      return;
    }
    const el = ref.current;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting) {
          setStarted(true);
          observer.disconnect();
        }
      },
      { threshold: 0.4 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [startOnView]);

  // Animate
  React.useEffect(() => {
    if (!started) return;
    const start = performance.now();
    const easeOutExpo = (t: number) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t));
    const tick = (now: number) => {
      const t = Math.min((now - start) / duration, 1);
      const eased = easeOutExpo(t);
      setDisplay(end * eased);
      if (t < 1) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        setDisplay(end);
      }
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [started, end, duration]);

  const formatted = (() => {
    const fixed = display.toFixed(decimals);
    const [intPart, decPart] = fixed.split(".");
    const withSep = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, separator);
    return `${prefix}${decPart ? `${withSep},${decPart}` : withSep}${suffix}`;
  })();

  return { ref, display: formatted, raw: display };
}
