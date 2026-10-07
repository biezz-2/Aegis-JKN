"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sigma, Copy, Check } from "lucide-react";
import { FORMULAS } from "./data";
import { cn } from "@/lib/utils";

// Render simple inline math as styled text (no KaTeX dependency)
function FormulaSymbol({ children }: { children: React.ReactNode }) {
  return (
    <span className="font-mono text-primary">{children}</span>
  );
}

export function MathFormulas() {
  const [active, setActive] = useState(0);
  const [copied, setCopied] = useState(false);
  const formula = FORMULAS[active];

  const copyLatex = () => {
    navigator.clipboard?.writeText(formula.latex);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <section id="math" className="relative py-16 sm:py-24">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6">
        <div className="mx-auto max-w-3xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4 }}
            className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-3 py-1 text-xs font-medium text-primary"
          >
            <Sigma className="h-3.5 w-3.5" />
            Formulasi Matematis
          </motion.div>
          <motion.h2
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="mt-4 text-3xl font-bold tracking-tight sm:text-4xl"
          >
            Dari <span className="gradient-text">Konvolusi Graf</span> hingga Prediksi
          </motion.h2>
          <p className="mt-4 text-muted-foreground">
            Empat persamaan inti MHGSL: konstruksi adjasensi fitur (cosine),
            konvolusi spesifik-saluran, GCN parameter-bersama, dan fusion +
            klasifikasi akhir.
          </p>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-5 lg:grid-cols-12">
          {/* Tabs */}
          <div className="lg:col-span-4">
            <div className="flex flex-row gap-2 lg:flex-col overflow-x-auto scrollbar-thin pb-2 lg:pb-0">
              {FORMULAS.map((f, i) => (
                <button
                  key={f.id}
                  onClick={() => setActive(i)}
                  className={cn(
                    "shrink-0 rounded-xl border p-3 text-left transition-all lg:w-full",
                    i === active
                      ? "border-primary/50 bg-primary/5 shadow-sm"
                      : "border-border/70 hover:border-border bg-card"
                  )}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-primary">
                      {f.legend}
                    </span>
                    <span className="text-[10px] font-semibold text-muted-foreground">
                      #{i + 1}
                    </span>
                  </div>
                  <div className="mt-1 text-xs font-medium">{f.title}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Formula display */}
          <div className="lg:col-span-8">
            <AnimatePresence mode="wait">
              <motion.div
                key={formula.id}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -16 }}
                transition={{ duration: 0.35 }}
                className="rounded-2xl border border-border/70 bg-gradient-to-br from-card to-primary/5 p-5 shadow-sm"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div className="text-[11px] font-semibold uppercase tracking-wide text-muted-foreground">
                      {formula.title}
                    </div>
                    <h3 className="mt-1 text-lg font-bold">
                      <FormulaSymbol>{formula.legend}</FormulaSymbol>
                    </h3>
                  </div>
                  <button
                    onClick={copyLatex}
                    className="rounded-md border border-border bg-background px-2 py-1 text-[10px] font-medium hover:bg-muted transition-colors"
                  >
                    {copied ? (
                      <span className="flex items-center gap-1 text-primary">
                        <Check className="h-3 w-3" /> Tersalin
                      </span>
                    ) : (
                      <span className="flex items-center gap-1">
                        <Copy className="h-3 w-3" /> Salin LaTeX
                      </span>
                    )}
                  </button>
                </div>

                {/* Formula card */}
                <div className="mt-4 overflow-x-auto rounded-xl border border-border/60 bg-background/80 p-4">
                  <div className="font-mono text-sm leading-relaxed text-foreground whitespace-pre">
                    <FormulaBlock latex={formula.latex} />
                  </div>
                </div>

                <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
                  {formula.desc}
                </p>

                {/* Symbol legend */}
                <div className="mt-4 rounded-xl bg-muted/40 p-3 text-[11px]">
                  <div className="font-semibold text-muted-foreground">Glosarium simbol</div>
                  <ul className="mt-1.5 grid grid-cols-1 gap-1 sm:grid-cols-2">
                    {symbolGlossary(formula.id).map((s) => (
                      <li key={s.s} className="flex gap-2">
                        <span className="font-mono text-primary shrink-0">{s.s}</span>
                        <span className="text-foreground/80">{s.d}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </section>
  );
}

// Hand-rendered formula blocks (since we don't bundle KaTeX).
function FormulaBlock({ latex }: { latex: string }) {
  // Render multi-line by splitting \\ into <div>
  const lines = latex.split("\\\\").map((l) => l.trim());
  return (
    <div className="space-y-1.5">
      {lines.map((line, i) => (
        <FormulaLine key={i} line={line} />
      ))}
    </div>
  );
}

function FormulaLine({ line }: { line: string }) {
  // Replace common LaTeX tokens with HTML for readability
  let html = line
    .replace(/\\mathbf\{([^}]+)\}/g, "<b class='text-primary'>$1</b>")
    .replace(/\\mathbb\{R\}/g, "ℝ")
    .replace(/\\sigma/g, "σ")
    .replace(/\\alpha/g, "α")
    .replace(/\\gamma/g, "γ")
    .replace(/\\theta/g, "θ")
    .replace(/\\quad/g, " &nbsp; ")
    .replace(/\\cdot/g, "·")
    .replace(/\\text\{([^}]+)\}/g, "<span class='text-foreground/70 italic'>$1</span>")
    .replace(/\\text\{Concat\}\\!?\(?\s*/g, "<span class='text-primary'>Concat</span>(")
    .replace(/\\text\{Sim\}\\?_\\mathcal\{M\}/g, "Sim<sub>ℳ</sub>")
    .replace(/\\tilde\{([^}]+)\}/g, "<span class='text-primary'>$1̃</span>")
    .replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, "<span class='inline-flex flex-col text-center align-middle'><span class='text-[0.85em] border-b border-current'>$1</span><span class='text-[0.85em]'>$2</span></span>")
    .replace(/\\sqrt\{([^}]+)\}/g, "√$1")
    .replace(/\\sqrt\{\\?frac\{([^}]+)\}\{([^}]+)\}\}/g, "√($1/$2)")
    .replace(/\\left\(([^)]+)\)\\right\)/g, "($1)")
    .replace(/\\left\(/g, "(")
    .replace(/\\right\)/g, ")")
    .replace(/\\sqrt/g, "√")
    .replace(/\\|/g, "‖")
    .replace(/\\tilde\{\\?mathbf\{D\}\}/g, "<b class='text-primary'>D̃</b>")
    .replace(/\\mathcal\{M\}/g, "ℳ")
    .replace(/\\geq/g, "≥")
    .replace(/\\leq/g, "≤")
    .replace(/\\neq/g, "≠")
    .replace(/\\hat\{([^}]+)\}/g, "<span class='text-primary'>$1̂</span>")
    .replace(/\\bar\{([^}]+)\}/g, "$1̄")
    .replace(/\\mathbf\{([^}]+)\}/g, "<b class='text-primary'>$1</b>")
    .replace(/\\mathbf\{D\}/g, "<b class='text-primary'>D</b>")
    .replace(/\\mathbf\{X\}/g, "<b class='text-primary'>X</b>")
    .replace(/\\mathbf\{W\}/g, "<b class='text-primary'>W</b>")
    .replace(/\\mathbf\{H\}/g, "<b class='text-primary'>H</b>")
    .replace(/\\mathbf\{x\}/g, "<b class='text-primary'>x</b>")
    .replace(/\\mathbf\{A\}/g, "<b class='text-primary'>A</b>")
    .replace(/_\{?\}?/g, "")
    .replace(/\^\{?\}?/g, "")
    .replace(/\\!|\\,|\\;/g, " ")
    .replace(/\\left|\\right/g, "");

  return (
    <div
      className="leading-relaxed"
      dangerouslySetInnerHTML={{ __html: html } as Record<string, string>}
    />
  );
}

function symbolGlossary(id: string) {
  const base = [
    { s: "𝐗", d: "matriks fitur input (|V| × d)" },
    { s: "𝐀^(k)", d: "adjasensi saluran k" },
    { s: "Ã", d: "A + I (self-loop)" },
    { s: "D̃", d: "matriks derajat diagonal" },
    { s: "𝐖^(k)", d: "bobot spesifik saluran k" },
    { s: "σ(·)", d: "fungsi aktivasi (ReLU/LeakyReLU)" },
    { s: "θ_feat", d: "ambang batas kemiripan fitur" },
    { s: "ℳ", d: "metapath semantik" },
  ];
  if (id === "fusion") {
    return [
      ...base.slice(0, 4),
      { s: "Concat", d: "penggabungan vektor 4 saluran" },
      { s: "𝐖_cls", d: "bobot klasifikasi akhir" },
      { s: "ŷᵢ", d: "probabilitas fraud klaim i" },
      { s: "b", d: "bias lapisan linier" },
    ];
  }
  if (id === "late-fusion") {
    return [
      { s: "p_fused", d: "skor probabilitas kecurangan terpadu (graf + teks)" },
      { s: "p_graph", d: "probabilitas fraud keluaran model graf MHGSL" },
      { s: "f_text", d: "sinyal sentimen teks / keluhan media sosial [0, 1]" },
      { s: "γ (0.10)", d: "bobot pelemah sinyal teks (bounded contribution)" },
    ];
  }
  return base;
}
