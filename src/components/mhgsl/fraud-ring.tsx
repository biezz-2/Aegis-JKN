"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { GitMerge, Users, Network, Search, MousePointerClick } from "lucide-react";
import { FRAUD_PROFILES, type FraudEntityProfile } from "./data";
import { FraudDrilldownModal } from "./fraud-drilldown-modal";

// A simplified fraud-ring illustration. We draw two communities:
// - A dense collusive fraud ring (left): tightly interconnected, shared diagnosis, repeated expensive procedures
// - A normal sparse community (right): distributed referrals, no anomaly
// User can toggle "highlight ring" to see how message-passing aggregates risk into the dense cluster.
// Clicking a fraud node opens a detailed drilldown modal.

const ringNodes = [
  // Fraud ring SYND-01 (left)
  { id: "p1", profileId: "p1", x: 110, y: 100, t: "patient", r: "fraud", label: "P01" },
  { id: "p2", x: 60, y: 200, t: "patient", r: "fraud", label: "P02" },
  { id: "p3", x: 110, y: 300, t: "patient", r: "fraud", label: "P03" },
  { id: "f4", profileId: "d1", x: 200, y: 160, t: "doctor", r: "fraud", label: "D01" },
  { id: "f5", x: 200, y: 240, t: "doctor", r: "fraud", label: "D02" },
  { id: "f6", profileId: "rs", x: 280, y: 200, t: "faskes", r: "fraud", label: "RS_A" },
  { id: "f7", x: 360, y: 200, t: "procedure", r: "fraud", label: "00.66" },
  // Normal community (right)
  { id: "n1", x: 520, y: 110, t: "patient", r: "low", label: "P04" },
  { id: "n2", x: 620, y: 80, t: "patient", r: "low", label: "P06" },
  { id: "n3", x: 620, y: 220, t: "patient", r: "low", label: "P07" },
  { id: "n4", x: 540, y: 320, t: "patient", r: "low", label: "P11" },
  { id: "n5", x: 480, y: 200, t: "doctor", r: "low", label: "D06" },
  { id: "n6", x: 620, y: 340, t: "doctor", r: "low", label: "D10" },
  { id: "n7", x: 700, y: 200, t: "faskes", r: "low", label: "RS_B" },
  { id: "n8", x: 700, y: 320, t: "procedure", r: "low", label: "44.13" },
];

const ringEdges = [
  // Fraud ring - dense
  ["f1", "f4"], ["f2", "f4"], ["f1", "f5"], ["f2", "f5"], ["f3", "f5"],
  ["f4", "f6"], ["f5", "f6"], ["f6", "f7"],
  ["f4", "f5"], // dokter kolusi
  ["f1", "f2"], ["f2", "f3"], // pasien similar feature
  ["f4", "f7"], ["f5", "f7"], // metapath semantic
  // Normal - sparse
  ["n1", "n5"], ["n2", "n5"], ["n3", "n5"], ["n4", "n6"],
  ["n5", "n7"], ["n6", "n7"], ["n7", "n8"],
].map(([a, b]) => ({ from: a, to: b }));

const typeColor: Record<string, string> = {
  patient: "oklch(0.55 0.14 165)",
  doctor: "oklch(0.62 0.13 200)",
  faskes: "oklch(0.7 0.16 70)",
  procedure: "oklch(0.62 0.22 20)",
};

// Map SVG node IDs back to ringNodes ids (alias)
const nodeMap: Record<string, (typeof ringNodes)[number]> = {};
ringNodes.forEach((n) => {
  nodeMap[n.id] = n;
});
// Handle aliases used in edges
const aliases: Record<string, string> = {
  f1: "p1", f2: "p2", f3: "p3",
};
Object.keys(aliases).forEach((alias) => {
  nodeMap[alias] = nodeMap[aliases[alias]];
});

export function FraudRing() {
  const [highlight, setHighlight] = useState(true);
  const [showMsg, setShowMsg] = useState(false);
  const [hovered, setHovered] = useState<string | null>(null);
  const [openProfile, setOpenProfile] = useState<FraudEntityProfile | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const handleNodeClick = (profileId?: string) => {
    if (!profileId) return;
    const profile = FRAUD_PROFILES.find((p) => p.id === profileId);
    if (profile) {
      setOpenProfile(profile);
      setModalOpen(true);
    }
  };

  return (
    <section id="ring" className="relative py-16 sm:py-24">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6">
        <div className="mx-auto max-w-3xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
            className="inline-flex items-center gap-2 rounded-full border border-rose-200 bg-rose-50 px-3 py-1 text-xs font-medium text-rose-700 dark:bg-rose-500/15 dark:text-rose-300 dark:border-rose-500/30"
          >
            <GitMerge className="h-3.5 w-3.5" />
            Fraud Ring Detection · Sindikat Kolusi
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl"
          >
            Pesan Berjalan, <span className="gradient-text">Sindikat Tersingkap</span>
          </motion.h2>
          <p className="mt-4 text-muted-foreground">
            Model tabular memeriksa tiap klaim secara terisolasi—pelaku sindikat
            memanfaatkan celah dengan membagi peran. Melalui{" "}
            <strong className="text-foreground">message-passing</strong> pada graf
            heterogen, MHGSL mengidentifikasi subgraf padat anomali sebagai{" "}
            <strong className="text-foreground">collusive communities</strong>.
          </p>
          <div className="mt-3 inline-flex items-center gap-1.5 rounded-full bg-primary/5 border border-primary/20 px-3 py-1 text-[11px] text-primary">
            <MousePointerClick className="h-3 w-3" />
            Klik simpul berisiko fraud (P01 / D01 / RS_A) untuk lihat detail investigasi klinis
          </div>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-5 lg:grid-cols-5">
          {/* Graph */}
          <div className="lg:col-span-3">
            <div className="rounded-2xl border border-border/70 bg-card p-3 shadow-sm">
              <div className="flex items-center justify-between px-2 py-1">
                <div className="text-xs font-semibold">
                  Komunitas pasien–dokter–faskes
                </div>
                <button
                  onClick={() => setHighlight((h) => !h)}
                  className="rounded-full border border-border bg-background px-2.5 py-0.5 text-[11px] font-medium hover:bg-muted transition-colors"
                >
                  {highlight ? "Sembunyikan highlight" : "Tampilkan subgraf padat"}
                </button>
              </div>
              <svg
                viewBox="0 0 800 420"
                className="h-auto w-full"
                style={{ background: "radial-gradient(circle at 30% 50%, color-mix(in oklch, var(--background) 100%, var(--primary) 4%), var(--background))" }}
              >
                <defs>
                  <pattern id="ringGrid" width="28" height="28" patternUnits="userSpaceOnUse">
                    <path d="M 28 0 L 0 0 0 28" fill="none" stroke="color-mix(in oklch, var(--border) 80%, transparent)" strokeWidth="0.5" />
                  </pattern>
                </defs>
                <rect width="800" height="420" fill="url(#ringGrid)" opacity="0.4" />

                {/* Highlight subgraph halo */}
                {highlight && (
                  <motion.g
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5 }}
                  >
                    <ellipse
                      cx="200"
                      cy="200"
                      rx="180"
                      ry="140"
                      fill="color-mix(in oklch, var(--chart-4) 10%, transparent)"
                      stroke="color-mix(in oklch, var(--chart-4) 40%, transparent)"
                      strokeWidth="1.5"
                      strokeDasharray="4 4"
                    />
                    <text
                      x="200"
                      y="60"
                      textAnchor="middle"
                      fontSize="11"
                      fontWeight="700"
                      fill="var(--chart-4)"
                    >
                      ⚠ SUBGRAPH PADAT ANOMALI
                    </text>
                  </motion.g>
                )}

                {/* Edges */}
                {ringEdges.map((e, i) => {
                  const a = nodeMap[e.from];
                  const b = nodeMap[e.to];
                  if (!a || !b) return null;
                  const isFraudEdge = a.r === "fraud" && b.r === "fraud";
                  return (
                    <line
                      key={i}
                      x1={a.x}
                      y1={a.y}
                      x2={b.x}
                      y2={b.y}
                      stroke={
                        isFraudEdge
                          ? highlight
                            ? "color-mix(in oklch, var(--chart-4) 70%, transparent)"
                            : "color-mix(in oklch, var(--chart-1) 40%, transparent)"
                          : "color-mix(in oklch, var(--muted-foreground) 35%, transparent)"
                      }
                      strokeWidth={isFraudEdge && highlight ? 2 : 1}
                      strokeDasharray={isFraudEdge ? undefined : "4 4"}
                    />
                  );
                })}

                {/* Nodes */}
                {ringNodes.map((n) => {
                  const c = typeColor[n.t];
                  const hasProfile = !!n.profileId;
                  const isHovered = hovered === n.id;
                  return (
                    <g
                      key={n.id}
                      transform={`translate(${n.x}, ${n.y})`}
                      onMouseEnter={() => setHovered(n.id)}
                      onMouseLeave={() => setHovered(null)}
                      onClick={() => handleNodeClick(n.profileId)}
                      style={{ cursor: hasProfile ? "pointer" : "default" }}
                    >
                      {n.r === "fraud" && highlight && (
                        <circle
                          r="22"
                          fill="none"
                          stroke="var(--chart-4)"
                          strokeWidth="1"
                          opacity="0.4"
                          className="animate-pulse-ring"
                        />
                      )}
                      {hasProfile && isHovered && (
                        <circle r="22" fill="none" stroke={c} strokeWidth="1.5" opacity="0.6" />
                      )}
                      <circle
                        r={isHovered && hasProfile ? 17 : 15}
                        fill={c}
                        stroke="var(--background)"
                        strokeWidth="2"
                        style={{
                          filter: isHovered && hasProfile ? "drop-shadow(0 0 6px rgba(0,0,0,0.2))" : undefined,
                        }}
                      />
                      <text
                        y="3.5"
                        textAnchor="middle"
                        fontSize="9.5"
                        fontWeight="700"
                        fill="white"
                      >
                        {n.label}
                      </text>
                      <text
                        y="30"
                        textAnchor="middle"
                        fontSize="9"
                        fill="var(--foreground)"
                      >
                        {n.label}
                      </text>
                      {hasProfile && (
                        <text
                          y="-22"
                          textAnchor="middle"
                          fontSize="9"
                          fill={c}
                          opacity={isHovered ? 1 : 0.7}
                        >
                          ⓘ
                        </text>
                      )}
                    </g>
                  );
                })}
              </svg>

              <div className="grid grid-cols-2 gap-2 px-2 pb-1 text-[11px]">
                <div className="flex items-center gap-2 rounded-lg bg-rose-50 dark:bg-rose-500/10 p-2">
                  <span className="h-2.5 w-2.5 rounded-full bg-rose-500" />
                  <span className="font-semibold text-rose-700 dark:text-rose-300">Subgraf padat</span>
                  <span className="text-muted-foreground">14 edge berlebih</span>
                </div>
                <div className="flex items-center gap-2 rounded-lg bg-emerald-50 dark:bg-emerald-500/10 p-2">
                  <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
                  <span className="font-semibold text-emerald-700 dark:text-emerald-300">Komunitas sehat</span>
                  <span className="text-muted-foreground">7 edge tersebar</span>
                </div>
              </div>
            </div>
          </div>

          {/* Explanation */}
          <div className="lg:col-span-2 space-y-3">
            <div className="rounded-2xl border border-border/70 bg-card p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                <Network className="h-3.5 w-3.5 text-primary" />
                Mekanisme Message Passing
              </div>
              <ol className="mt-2 space-y-2 text-xs text-foreground/85">
                <li className="flex gap-2">
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-[10px] font-bold text-primary">
                    1
                  </span>
                  <span>
                    Tiap simpul mengagregasi fitur dari semua tetangga melalui
                    bobot adjasensi ternormalisasi.
                  </span>
                </li>
                <li className="flex gap-2">
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-[10px] font-bold text-primary">
                    2
                  </span>
                  <span>
                    Pada sindikat, simpul-simpul bertukar pesan intensif karena
                    derajat keterhubungan sangat tinggi.
                  </span>
                </li>
                <li className="flex gap-2">
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-[10px] font-bold text-primary">
                    3
                  </span>
                  <span>
                    Embedding simpul dalam klaster padat terdorong ke arah vektor
                    <strong> risiko fraud</strong> setelah beberapa lapisan.
                  </span>
                </li>
                <li className="flex gap-2">
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-[10px] font-bold text-primary">
                    4
                  </span>
                  <span>
                    Klasifikator mendeteksi collusive community sebagai satu unit
                    anomali terstruktur—bukan klaim individual.
                  </span>
                </li>
              </ol>
            </div>

            <div className="rounded-2xl border border-border/70 bg-card p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                <Users className="h-3.5 w-3.5 text-amber-600" />
                Mengapa Sindikat Berkamuflase Gagal
              </div>
              <ul className="mt-2 space-y-1.5 text-xs text-foreground/85">
                <li className="flex gap-2">
                  <span className="text-primary">▸</span>
                  <span>
                    Klaim individu tampak valid → lolos seleksi tabular,
                    tetapi pola agregat metapath tidak konsisten dengan praktik medis normal.
                  </span>
                </li>
                <li className="flex gap-2">
                  <span className="text-primary">▸</span>
                  <span>
                    Penambahan feature graph menangkap kemiripan tidak wajar antar-pasien
                    (LOS identik, biaya berhimpitan).
                  </span>
                </li>
                <li className="flex gap-2">
                  <span className="text-primary">▸</span>
                  <span>
                    Shared-parameter GCN memaksa konsistensi representasi lintas-saluran →
                    kamuflase pada satu saluran terbongkar oleh dua saluran lain.
                  </span>
                </li>
              </ul>
            </div>

            {/* Profile quick-access cards */}
            <div className="rounded-2xl border border-border/70 bg-card p-3">
              <div className="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground mb-2 px-1">
                Akses Cepat Profil Investigasi
              </div>
              <div className="space-y-1.5">
                {FRAUD_PROFILES.map((p) => (
                  <button
                    key={p.id}
                    onClick={() => {
                      setOpenProfile(p);
                      setModalOpen(true);
                    }}
                    className="w-full flex items-center gap-2 rounded-lg border border-border hover:border-primary/40 hover:bg-primary/5 transition-colors p-2 text-left"
                  >
                    <span
                      className="flex h-7 w-7 items-center justify-center rounded-md shrink-0"
                      style={{
                        background: typeColor[p.type],
                      }}
                    >
                      <span className="text-[9px] font-bold text-white">
                        {p.label.split(" ")[0]}
                      </span>
                    </span>
                    <div className="flex-1 min-w-0">
                      <div className="text-xs font-medium truncate">{p.label}</div>
                      <div className="text-[10px] text-muted-foreground">
                        Skor {p.riskScore.toFixed(2)} · {p.role}
                      </div>
                    </div>
                    <span
                      className="text-xs font-bold tabular-nums shrink-0"
                      style={{ color: typeColor[p.type] }}
                    >
                      →
                    </span>
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={() => setShowMsg(true)}
              className="w-full rounded-2xl border border-primary/30 bg-primary/5 p-3 text-left text-xs hover:bg-primary/10 transition-colors"
            >
              <div className="flex items-center gap-2 font-semibold text-primary">
                <Search className="h-3.5 w-3.5" />
                Verdict auditor
              </div>
              <p className="mt-1 text-[11px] text-muted-foreground">
                {showMsg
                  ? "Sindikat D01–D02 di RS_A (SYND-01) → klaim KLM001–003 upcoding ditarik ke antrean investigasi. Total penghematan estimasi Rp 1,2 M / bulan (Rp 14,4 M / tahun)."
                  : "Klik untuk melihat rekomendasi yang dihasilkan sistem..."}
              </p>
            </button>
          </div>
        </div>
      </div>

      <FraudDrilldownModal
        profile={openProfile}
        open={modalOpen}
        onOpenChange={setModalOpen}
      />
    </section>
  );
}
