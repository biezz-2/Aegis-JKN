"use client";

import { useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  User,
  Stethoscope,
  Hospital,
  Syringe,
  ClipboardList,
  Layers,
  Info,
  Route,
} from "lucide-react";
import {
  MHGSL_NODES,
  MHGSL_EDGES,
  CHANNELS,
  NODE_TYPE_META,
  type GraphNode,
} from "./data";
import { cn } from "@/lib/utils";

const nodeIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  User,
  Stethoscope,
  Hospital,
  Syringe,
  ClipboardList,
};

const riskColors: Record<string, string> = {
  low: "oklch(0.55 0.14 165)",
  medium: "oklch(0.7 0.16 70)",
  high: "oklch(0.7 0.18 50)",
  fraud: "oklch(0.62 0.22 20)",
};

const channelVisibilityDefault: Record<string, boolean> = {
  topology: true,
  feature: true,
  semantic: true,
};

export function MultiChannelGraph() {
  const [activeChannel, setActiveChannel] = useState<"topology" | "feature" | "semantic" | "all">("all");
  const [visibility, setVisibility] = useState(channelVisibilityDefault);
  const [hovered, setHovered] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [showMetapath, setShowMetapath] = useState(false);

  // The semantic metapath ℳ: Doctor → Diagnosis → Procedure → Faskes
  // We trace D₁ → Dx ringan → S_mahal → RS_A and D₂ → Dx ringan → S_mahal → RS_A
  const metapathChains = [
    ["d1", "dxMild", "sExpensive", "rs"],
    ["d2", "dxMild", "sExpensive", "rs"],
  ] as const;

  const nodeMap = useMemo(() => {
    const m: Record<string, GraphNode> = {};
    MHGSL_NODES.forEach((n) => (m[n.id] = n));
    return m;
  }, []);

  const toggleChannel = (c: "topology" | "feature" | "semantic") => {
    setVisibility((v) => ({ ...v, [c]: !v[c] }));
  };

  const isActiveEdge = (kind: string) =>
    activeChannel === "all" ? visibility[kind] : activeChannel === kind;

  const isNodeHighlighted = (n: GraphNode) => {
    if (!hovered && !selected) return false;
    const focus = hovered || selected;
    if (focus === n.id) return true;
    return MHGSL_EDGES.some(
      (e) =>
        (e.from === focus && e.to === n.id) ||
        (e.to === focus && e.from === n.id)
    );
  };

  return (
    <section id="graph" className="relative py-16 sm:py-24">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6">
        <div className="mx-auto max-w-3xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
            className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-3 py-1 text-xs font-medium text-primary"
          >
            <Layers className="h-3.5 w-3.5" />
            Multi-Channel Graph Visualization
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl"
          >
            Satu Ekosistem, <span className="gradient-text">Tiga Perspektif Graf</span>
          </motion.h2>
          <p className="mt-4 text-muted-foreground">
            Toggle antar saluran untuk melihat bagaimana topologi fisik, kemiripan
            fitur, dan hubungan semantik metapath menyaring informasi berbeda—dan
            bagaimana gabungannya menembus kamuflase sindikat.
          </p>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-5 lg:grid-cols-3">
          {/* LEFT: Channel selector + legend */}
          <div className="space-y-4">
            <div className="rounded-2xl border border-border/70 bg-card p-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold">Tampilan Saluran</h3>
                <button
                  onClick={() =>
                    setActiveChannel((c) =>
                      c === "all" ? "topology" : c === "topology" ? "feature" : c === "feature" ? "semantic" : "all"
                    )
                  }
                  className="text-[11px] font-medium text-primary hover:underline"
                >
                  Mode: {activeChannel === "all" ? "Gabungan" : activeChannel === "topology" ? "Topologi" : activeChannel === "feature" ? "Fitur" : "Semantik"} →
                </button>
              </div>
              <div className="mt-3 space-y-2">
                {CHANNELS.map((c) => {
                  const id = c.id as "topology" | "feature" | "semantic";
                  const isOn = activeChannel === "all" ? visibility[id] : activeChannel === id;
                  return (
                    <button
                      key={c.id}
                      onClick={() => toggleChannel(id)}
                      className={cn(
                        "w-full rounded-xl border p-3 text-left transition-all",
                        isOn
                          ? "border-transparent shadow-sm"
                          : "border-border/70 bg-muted/30 opacity-60"
                      )}
                      style={
                        isOn
                          ? {
                              background: `${c.color}12`,
                              borderColor: `${c.color}55`,
                            }
                          : undefined
                      }
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span
                            className="h-3 w-3 rounded-full"
                            style={{ background: c.color }}
                          />
                          <span className="text-sm font-semibold">{c.title}</span>
                        </div>
                        <span className="font-mono text-[11px] text-muted-foreground">
                          {c.sub}
                        </span>
                      </div>
                      <p className="mt-1.5 text-[11px] leading-snug text-muted-foreground">
                        {c.description}
                      </p>
                      <div className="mt-1.5 font-mono text-[10px] text-muted-foreground/80">
                        {c.formula}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="rounded-2xl border border-border/70 bg-card p-4">
              <h3 className="text-sm font-semibold">Legenda Simpul</h3>
              <div className="mt-2 grid grid-cols-2 gap-1.5">
                {Object.entries(NODE_TYPE_META).map(([k, m]) => {
                  const Icon = nodeIcons[m.icon] ?? User;
                  return (
                    <div
                      key={k}
                      className="flex items-center gap-2 rounded-md px-2 py-1 text-xs"
                    >
                      <span
                        className="flex h-5 w-5 items-center justify-center rounded-full"
                        style={{ background: m.color }}
                      >
                        <Icon className="h-3 w-3 text-white" />
                      </span>
                      <span>{m.label}</span>
                    </div>
                  );
                })}
              </div>
              <div className="mt-3 border-t border-border/60 pt-2">
                <div className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">
                  Tingkat Risiko
                </div>
                <div className="mt-1.5 flex flex-wrap gap-2">
                  {Object.entries(riskColors).map(([k, c]) => (
                    <div key={k} className="flex items-center gap-1.5 text-[11px]">
                      <span
                        className="h-2.5 w-2.5 rounded-full ring-2"
                        style={{ background: c, boxShadow: `0 0 0 2px ${c}40` }}
                      />
                      <span className="capitalize text-muted-foreground">{k}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* CENTER: The graph */}
          <div className="lg:col-span-2">
            <div className="relative overflow-hidden rounded-2xl border border-border/70 bg-card shadow-sm">
              <div className="flex items-center justify-between border-b border-border/60 px-4 py-2.5 gap-2 flex-wrap">
                <div className="flex items-center gap-2 text-xs font-medium">
                  <span className="flex h-2 w-2">
                    <span className="absolute inline-flex h-2 w-2 animate-pulse-ring rounded-full bg-rose-400/60" />
                    <span className="relative h-2 w-2 rounded-full bg-rose-500" />
                  </span>
                  Sindikat D₁–D₂ · RS_A · 5 entitas berisiko fraud
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setShowMetapath((s) => !s)}
                    className={cn(
                      "inline-flex items-center gap-1 rounded-full border px-2.5 py-1 text-[10px] font-medium transition-colors",
                      showMetapath
                        ? "border-transparent text-white shadow-sm"
                        : "border-border bg-background hover:bg-muted"
                    )}
                    style={
                      showMetapath
                        ? { background: "var(--chart-3)" }
                        : undefined
                    }
                  >
                    <Route className="h-3 w-3" />
                    Metapath ℳ
                  </button>
                  <div className="hidden sm:flex items-center gap-1 text-[10px] text-muted-foreground">
                    <Info className="h-3 w-3" />
                    Klik simpul untuk detail
                  </div>
                </div>
              </div>

              <div className="relative">
                <svg
                  viewBox="0 0 700 460"
                  className="w-full h-auto"
                  style={{ background: "radial-gradient(circle at 50% 50%, color-mix(in oklch, var(--background) 100%, var(--primary) 3%), var(--background))" }}
                >
                  <defs>
                    <pattern id="bgGrid" width="28" height="28" patternUnits="userSpaceOnUse">
                      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="color-mix(in oklch, var(--border) 80%, transparent)" strokeWidth="0.5" />
                    </pattern>
                    <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
                      <path d="M0,0 L6,3 L0,6" fill="var(--muted-foreground)" />
                    </marker>
                    <marker id="metapathArrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
                      <path d="M0,0 L10,5 L0,10 L3,5 Z" fill="var(--chart-3)" />
                    </marker>
                  </defs>
                  <rect width="700" height="460" fill="url(#bgGrid)" opacity="0.4" />

                  {/* Metapath overlay */}
                  {showMetapath && (
                    <g>
                      {metapathChains.map((chain, ci) => {
                        const pathPoints = chain.map((id) => nodeMap[id]).filter(Boolean) as GraphNode[];
                        if (pathPoints.length < 2) return null;
                        const start = pathPoints[0];
                        const end = pathPoints[pathPoints.length - 1];
                        // Build a smooth path through all points
                        let d = `M ${start.x} ${start.y}`;
                        for (let i = 1; i < pathPoints.length; i++) {
                          const prev = pathPoints[i - 1];
                          const curr = pathPoints[i];
                          const midX = (prev.x + curr.x) / 2;
                          const midY = (prev.y + curr.y) / 2;
                          d += ` Q ${midX} ${midY - 50} ${curr.x} ${curr.y}`;
                        }
                        return (
                          <g key={`metapath-${ci}`}>
                            <path
                              d={d}
                              fill="none"
                              stroke="var(--chart-3)"
                              strokeWidth="3"
                              strokeLinecap="round"
                              opacity="0.5"
                              markerEnd="url(#metapathArrow)"
                            />
                            <path
                              d={d}
                              fill="none"
                              stroke="var(--chart-3)"
                              strokeWidth="3"
                              strokeLinecap="round"
                              className="metapath-flow"
                              opacity="0.9"
                              markerEnd="url(#metapathArrow)"
                            />
                            <text
                              x={(start.x + end.x) / 2}
                              y={Math.min(...pathPoints.map((p) => p.y)) - 40}
                              textAnchor="middle"
                              fontSize="10"
                              fontWeight="700"
                              fill="var(--chart-3)"
                              style={{ fontFamily: "monospace" }}
                            >
                              ℳ: D → Dx → S → RS {ci === 0 ? "(via D₁)" : "(via D₂)"}
                            </text>
                          </g>
                        );
                      })}
                    </g>
                  )}

                  {/* Edges */}
                  {MHGSL_EDGES.map((e, i) => {
                    const a = nodeMap[e.from];
                    const b = nodeMap[e.to];
                    if (!a || !b) return null;
                    const visible = isActiveEdge(e.kind);
                    const channel = CHANNELS.find((c) => c.id === e.kind)!;
                    const highlight = hovered || selected;
                    const isDim = highlight && highlight !== e.from && highlight !== e.to;

                    return (
                      <g key={`edge-${i}`} opacity={!visible ? 0 : isDim ? 0.15 : 0.85}>
                        {e.kind === "topology" ? (
                          <line
                            x1={a.x}
                            y1={a.y}
                            x2={b.x}
                            y2={b.y}
                            stroke={channel.color}
                            strokeWidth={highlight && (highlight === e.from || highlight === e.to) ? 2.5 : 1.4}
                            markerEnd="url(#arrow)"
                            className={highlight && (highlight === e.from || highlight === e.to) ? "flow-dash" : ""}
                          />
                        ) : (
                          <path
                            d={`M ${a.x} ${a.y} Q ${(a.x + b.x) / 2} ${(a.y + b.y) / 2 - 40} ${b.x} ${b.y}`}
                            fill="none"
                            stroke={channel.color}
                            strokeWidth={highlight && (highlight === e.from || highlight === e.to) ? 2.4 : 1.2}
                            strokeDasharray="5 4"
                            opacity={0.8}
                          />
                        )}
                        {e.weight && (highlight === e.from || highlight === e.to) && (
                          <text
                            x={(a.x + b.x) / 2}
                            y={(a.y + b.y) / 2 - 18}
                            textAnchor="middle"
                            fontSize="10"
                            fontFamily="monospace"
                            fill={channel.color}
                          >
                            w={e.weight.toFixed(2)}
                          </text>
                        )}
                      </g>
                    );
                  })}

                  {/* Nodes */}
                  {MHGSL_NODES.map((n) => {
                    const meta = NODE_TYPE_META[n.type];
                    const Icon = nodeIcons[meta.icon] ?? User;
                    const isFocus = hovered === n.id || selected === n.id;
                    const dim = (hovered || selected) && !isNodeHighlighted(n);
                    return (
                      <g
                        key={n.id}
                        transform={`translate(${n.x}, ${n.y})`}
                        onMouseEnter={() => setHovered(n.id)}
                        onMouseLeave={() => setHovered(null)}
                        onClick={() => setSelected((s) => (s === n.id ? null : n.id))}
                        className="cursor-pointer"
                        opacity={dim ? 0.4 : 1}
                      >
                        {n.risk === "fraud" && (
                          <circle
                            r="24"
                            fill="none"
                            stroke={riskColors.fraud}
                            strokeWidth="1.5"
                            opacity="0.5"
                            className="animate-pulse-ring"
                          />
                        )}
                        <circle
                          r={isFocus ? 22 : 18}
                          fill={meta.color}
                          stroke="white"
                          strokeWidth="2.5"
                          style={{ filter: isFocus ? "drop-shadow(0 0 8px rgba(0,0,0,0.2))" : undefined }}
                        />
                        {/* Inner icon */}
                        <foreignObject x={-9} y={-9} width="18" height="18">
                          <div className="flex h-[18px] w-[18px] items-center justify-center">
                            <Icon className="h-3 w-3 text-white" />
                          </div>
                        </foreignObject>
                        <text
                          y={isFocus ? 36 : 32}
                          textAnchor="middle"
                          fontSize="11"
                          fontWeight="600"
                          fill="oklch(0.18 0.025 200)"
                        >
                          {n.label}
                        </text>
                        {n.risk === "fraud" && (
                          <text
                            y={isFocus ? 48 : 44}
                            textAnchor="middle"
                            fontSize="8.5"
                            fontWeight="700"
                            fill={riskColors.fraud}
                          >
                            ⚠ FRAUD
                          </text>
                        )}
                      </g>
                    );
                  })}
                </svg>

                {/* Node detail panel */}
                <AnimatePresence>
                  {selected && (
                    <motion.div
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 8 }}
                      className="absolute bottom-3 left-3 right-3 rounded-xl border border-border/70 bg-card/95 p-3 shadow-lg backdrop-blur"
                    >
                      {(() => {
                        const n = nodeMap[selected];
                        if (!n) return null;
                        const meta = NODE_TYPE_META[n.type];
                        const inEdges = MHGSL_EDGES.filter((e) => e.to === n.id);
                        const outEdges = MHGSL_EDGES.filter((e) => e.from === n.id);
                        return (
                          <div>
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <span
                                  className="flex h-6 w-6 items-center justify-center rounded-full"
                                  style={{ background: meta.color }}
                                >
                                  <span className="text-[10px] font-bold text-white">
                                    {n.label}
                                  </span>
                                </span>
                                <div>
                                  <div className="text-xs font-semibold">{n.label}</div>
                                  <div className="text-[10px] text-muted-foreground">
                                    Tipe: {meta.label}
                                  </div>
                                </div>
                              </div>
                              <div className="flex items-center gap-1.5">
                                {n.risk && (
                                  <span
                                    className="rounded-full px-2 py-0.5 text-[10px] font-semibold capitalize"
                                    style={{
                                      background: `${riskColors[n.risk]}20`,
                                      color: riskColors[n.risk],
                                    }}
                                  >
                                    {n.risk}
                                  </span>
                                )}
                                <button
                                  onClick={() => setSelected(null)}
                                  className="text-muted-foreground hover:text-foreground text-xs"
                                >
                                  ✕
                                </button>
                              </div>
                            </div>
                            {n.note && (
                              <p className="mt-2 text-[11px] text-foreground/80">
                                {n.note}
                              </p>
                            )}
                            <div className="mt-2 grid grid-cols-2 gap-2 text-[10px]">
                              <div className="rounded-md bg-muted/40 p-1.5">
                                <div className="font-semibold text-muted-foreground">In-degree</div>
                                <div>{inEdges.length} edge</div>
                              </div>
                              <div className="rounded-md bg-muted/40 p-1.5">
                                <div className="font-semibold text-muted-foreground">Out-degree</div>
                                <div>{outEdges.length} edge</div>
                              </div>
                            </div>
                          </div>
                        );
                      })()}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Channel legend strip */}
              <div className="flex flex-wrap items-center gap-3 border-t border-border/60 px-4 py-2.5 text-[11px]">
                {CHANNELS.map((c) => (
                  <div key={c.id} className="flex items-center gap-1.5">
                    <span
                      className="h-3"
                      style={{
                        width: 16,
                        background: c.color,
                        borderRadius: c.id === "topology" ? 2 : 999,
                        opacity: isActiveEdge(c.id) ? 1 : 0.25,
                      }}
                    />
                    <span className={isActiveEdge(c.id) ? "text-foreground" : "text-muted-foreground/60"}>
                      {c.title}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
