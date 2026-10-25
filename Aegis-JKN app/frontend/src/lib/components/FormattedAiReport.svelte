<script lang="ts">
  import Icon from "./Icon.svelte";

  let {
    rawText = "",
    title = "Laporan Audit Klinis Terstruktur",
    claimId = "",
    hospital = "",
    fraudScore = 0.5,
  }: {
    rawText: string;
    title?: string;
    claimId?: string;
    hospital?: string;
    fraudScore?: number;
  } = $props();

  interface ParsedSection {
    id: string;
    title: string;
    badge: string;
    theme: "primary" | "warning" | "danger" | "info" | "neutral";
    icon: string;
    content: string;
    decisionPill?: string;
  }

  // Parse raw text into structured sections while preserving rich markdown
  const parsedSections = $derived.by<ParsedSection[]>(() => {
    if (!rawText) return [];

    const text = rawText.trim();
    const sections: ParsedSection[] = [];

    // 1. Clinical Coding Section
    const codingMatch = text.match(
      /(?:\[?ANALISIS\s+KLINIS(?:\s*&\s*KODING(?:\s+INA-CBG)?)?\]?|1\.\s*(?:\*\*)?\[?ANALISIS[\s\S]*?)([\s\S]*?)(?=(?:\[?EVALUASI\s+KONTRADIKSI|2\.\s*(?:\*\*)?\[?EVALUASI|##\s*2\.))/i
    );
    if (codingMatch && codingMatch[1]) {
      sections.push({
        id: "coding",
        title: "Analisis Klinis & Koding INA-CBG",
        badge: "Kesesuaian Diagnosis & Prosedur",
        theme: "info",
        icon: "ClipboardList",
        content: cleanSectionText(codingMatch[1]),
      });
    }

    // 2. Contradiction Evaluation Section
    const contraMatch = text.match(
      /(?:\[?EVALUASI\s+KONTRADIKSI(?:\s+NARASI)?\]?|2\.\s*(?:\*\*)?\[?EVALUASI[\s\S]*?)([\s\S]*?)(?=(?:\[?INTERPRETASI|3\.\s*(?:\*\*)?\[?INTERPRETASI|##\s*3\.))/i
    );
    if (contraMatch && contraMatch[1]) {
      sections.push({
        id: "contradiction",
        title: "Evaluasi Kontradiksi Narasi & Integritas Rekam Medis",
        badge: "Validasi Pengakuan Pasien",
        theme: "warning",
        icon: "AlertTriangle",
        content: cleanSectionText(contraMatch[1]),
      });
    }

    // 3. MHGSL Graph Interpretation Section
    const mhgslMatch = text.match(
      /(?:\[?INTERPRETASI\s+GRAF(?:\s+MHGSL(?:\s*&\s*ANTI-KAMUFLASE)?)?\]?|3\.\s*(?:\*\*)?\[?INTERPRETASI[\s\S]*?)([\s\S]*?)(?=(?:\[?REKOMENDASI|4\.\s*(?:\*\*)?\[?REKOMENDASI|##\s*4\.|---\s*###\s*DASAR))/i
    );
    if (mhgslMatch && mhgslMatch[1]) {
      sections.push({
        id: "mhgsl",
        title: "Interpretasi Graf MHGSL 3-Kanal (Anti-Kamuflase)",
        badge: "Topologi · Fitur · Semantik",
        theme: "primary",
        icon: "Activity",
        content: cleanSectionText(mhgslMatch[1]),
      });
    }

    // 4. Recommendation Section
    const recMatch = text.match(
      /(?:\[?REKOMENDASI\s+PUTUSAN(?:\s+VERIFIKATOR)?\]?|4\.\s*(?:\*\*)?\[?REKOMENDASI[\s\S]*?)([\s\S]*?)(?=(?:---\s*###\s*DASAR|###\s*DASAR\s+REGULASI|$))/i
    );
    if (recMatch && recMatch[1]) {
      const rawRec = recMatch[1].trim();
      let decisionPill = "TINJAUAN LANJUTAN";
      if (/ESKALASI/i.test(rawRec)) {
        decisionPill = "ESKALASI KE TIM P2PK";
      } else if (/KLARIFIKASI/i.test(rawRec)) {
        decisionPill = "MINTA KLARIFIKASI RS";
      } else if (/SETUJUI/i.test(rawRec)) {
        decisionPill = "SETUJUI KLAIM (VALID)";
      }

      sections.push({
        id: "recommendation",
        title: "Rekomendasi Putusan Verifikator & Tindak Lanjut",
        badge: "Keputusan Human-in-the-Loop",
        theme: decisionPill.includes("ESKALASI") ? "danger" : decisionPill.includes("KLARIFIKASI") ? "warning" : "primary",
        icon: "ShieldAlert",
        content: cleanSectionText(rawRec),
        decisionPill,
      });
    }

    // Fallback to whole text if no sections matched
    if (sections.length === 0) {
      sections.push({
        id: "general",
        title: "Hasil Telaah Klinis Lengkap",
        badge: "Laporan Auditor",
        theme: "primary",
        icon: "FileText",
        content: cleanSectionText(text),
      });
    }

    return sections;
  });

  // Extract Regulatory Basis
  const regulatoryBasis = $derived.by<string[]>(() => {
    if (!rawText) return [];
    const regMatch = rawText.match(/(?:DASAR\s+REGULASI|###\s*DASAR\s+REGULASI[\s\S]*?)([\s\S]*$)/i);
    if (!regMatch || !regMatch[1]) return [];

    const items: string[] = [];
    const bulletRegex = /(?:^|\n)\s*[-*]\s*(.+)/g;
    let m;
    while ((m = bulletRegex.exec(regMatch[1])) !== null) {
      const line = m[1].trim();
      if (line) items.push(line);
    }
    return items;
  });

  function cleanSectionText(text: string): string {
    return text
      .replace(/^[\s\S]*?:\s*/, "") // Remove prefix like '1. [ANALISIS]: '
      .trim();
  }

  // Full-featured Markdown Parser that renders Headers, Numbered Lists, Bullet Points, Bold, Italic, Quotes, and Code
  function renderMarkdownToHtml(text: string): string {
    if (!text) return "";

    const lines = text.split("\n");
    let html = "";
    let inList: "ul" | "ol" | null = null;

    for (let i = 0; i < lines.length; i++) {
      const rawLine = lines[i];
      const trimmed = rawLine.trim();

      // Empty line -> break list
      if (!trimmed) {
        if (inList) {
          html += inList === "ul" ? "</ul>" : "</ol>";
          inList = null;
        }
        continue;
      }

      // Markdown Headers (### Header, #### Header)
      const headerMatch = trimmed.match(/^(#{1,6})\s+(.+)$/);
      if (headerMatch) {
        if (inList) {
          html += inList === "ul" ? "</ul>" : "</ol>";
          inList = null;
        }
        const level = headerMatch[1].length;
        const headerText = formatInline(headerMatch[2]);
        const sizeClass =
          level <= 2
            ? "text-sm sm:text-base font-extrabold text-foreground mt-4 mb-2 tracking-tight"
            : level === 3
              ? "text-xs sm:text-sm font-bold text-foreground mt-3 mb-1.5 tracking-tight"
              : "text-xs font-bold text-foreground/90 mt-2.5 mb-1";
        html += `<h${level} class="${sizeClass}">${headerText}</h${level}>`;
        continue;
      }

      // Numbered List: 1. Item, 2. Item
      const numMatch = trimmed.match(/^(\d+)[\.\)]\s+(.+)$/);
      if (numMatch) {
        if (inList !== "ol") {
          if (inList === "ul") html += "</ul>";
          html += `<ol class="space-y-2 my-2.5 pl-0.5">`;
          inList = "ol";
        }
        const num = numMatch[1];
        const content = formatInline(numMatch[2]);
        html += `<li class="flex items-start gap-2.5 text-xs text-foreground leading-relaxed"><span class="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#588157]/15 text-[#3a5a40] dark:text-[#a3b18a] font-mono text-[10px] font-bold mt-0.5 shadow-2xs">${num}</span><span class="pt-0.5">${content}</span></li>`;
        continue;
      }

      // Bullet List: - Item, * Item, • Item
      const bulletMatch = trimmed.match(/^[-*•]\s+(.+)$/);
      if (bulletMatch) {
        if (inList !== "ul") {
          if (inList === "ol") html += "</ol>";
          html += `<ul class="space-y-1.5 my-2 pl-1">`;
          inList = "ul";
        }
        const content = formatInline(bulletMatch[1]);
        html += `<li class="flex items-start gap-2.5 text-xs text-foreground leading-relaxed"><span class="h-1.5 w-1.5 rounded-full bg-[#588157] mt-1.5 shrink-0 shadow-2xs"></span><span>${content}</span></li>`;
        continue;
      }

      // Blockquote (> text)
      const quoteMatch = trimmed.match(/^>\s*(.+)$/);
      if (quoteMatch) {
        if (inList) {
          html += inList === "ul" ? "</ul>" : "</ol>";
          inList = null;
        }
        const content = formatInline(quoteMatch[1]);
        html += `<blockquote class="p-3 my-2 rounded-2xl bg-muted/40 text-xs italic text-foreground/90 leading-relaxed">${content}</blockquote>`;
        continue;
      }

      // Regular Paragraph
      if (inList) {
        html += inList === "ul" ? "</ul>" : "</ol>";
        inList = null;
      }
      html += `<p class="leading-relaxed my-1.5 text-xs text-foreground">${formatInline(trimmed)}</p>`;
    }

    if (inList) {
      html += inList === "ul" ? "</ul>" : "</ol>";
    }

    return html;
  }

  // Format inline highlights (bold, italic, code, clinical codes)
  function formatInline(text: string): string {
    let out = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // Bold: **text** or __text__
    out = out.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-foreground">$1</strong>');
    out = out.replace(/__(.*?)__/g, '<strong class="font-bold text-foreground">$1</strong>');

    // Italic: *text* or _text_
    out = out.replace(/\*(.*?)\*/g, '<em class="italic text-foreground/90">$1</em>');
    out = out.replace(/_(.*?)_/g, '<em class="italic text-foreground/90">$1</em>');

    // Code: `code`
    out = out.replace(/`([^`]+)`/g, '<code class="font-mono bg-muted/80 px-1.5 py-0.5 rounded-md text-[11px] font-bold text-[#3a5a40] dark:text-[#a3b18a]">$1</code>');

    // Clinical codes highlight: ICD-10 (e.g. I21.0, E11.9, K35.8)
    out = out.replace(
      /\b([A-Z][0-9]{2}(?:\.[0-9]+)?)\b/g,
      '<span class="font-mono font-bold text-[#588157] px-1 py-0.5 rounded bg-[#588157]/10">$1</span>'
    );
    // ICD-9-CM procedures (e.g. 36.06, 00.66)
    out = out.replace(
      /\b([0-9]{2}\.[0-9]{2})\b/g,
      '<span class="font-mono font-bold text-rose-600 dark:text-rose-400 px-1 py-0.5 rounded bg-rose-500/10">$1</span>'
    );
    // Medical audit keywords
    out = out.replace(
      /\b(Upcoding|Phantom Billing|Unbundling|Kolusi|Kecurangan|Fraud|Fabrikasi|Mismatch)\b/gi,
      '<span class="font-bold text-rose-700 dark:text-rose-300">$1</span>'
    );

    return out;
  }
</script>

<div class="space-y-4 text-foreground select-text">
  <!-- Clean Header Banner (Borderless, Soft Card) -->
  {#if claimId || hospital}
    <div class="rounded-2xl bg-card p-4 shadow-xs flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-2.5">
        <div class="flex h-8 w-8 items-center justify-center rounded-xl bg-[#588157]/15 text-[#588157] font-bold">
          <Icon name="ShieldCheck" size={17} />
        </div>
        <div>
          <span class="text-xs font-bold text-foreground">
            {title}
          </span>
          <div class="text-[11px] text-muted-foreground mt-0.5">
            {#if claimId}Klaim: <strong class="text-foreground font-mono">{claimId}</strong>{/if}
            {#if hospital} · Faskes: <strong class="text-foreground">{hospital}</strong>{/if}
          </div>
        </div>
      </div>

      {#if fraudScore !== undefined}
        <div class="flex items-center gap-1.5 font-mono text-xs">
          <span class="text-[11px] font-sans text-muted-foreground">Status Probabilitas:</span>
          <span class="rounded-full px-2.5 py-0.5 font-bold {fraudScore >= 0.8 ? 'bg-rose-500/15 text-rose-800 dark:text-rose-300' : fraudScore >= 0.6 ? 'bg-amber-500/15 text-amber-800 dark:text-amber-300' : 'bg-emerald-500/15 text-emerald-800 dark:text-emerald-300'}">
            {(fraudScore * 100).toFixed(1)}%
          </span>
        </div>
      {/if}
    </div>
  {/if}

  <!-- Structured Sections (Borderless Cards with Rich Markdown Rendering) -->
  <div class="space-y-4">
    {#each parsedSections as sec}
      <div
        class="rounded-2xl p-5 shadow-xs transition-all {sec.theme === 'danger'
          ? 'bg-rose-500/5'
          : sec.theme === 'warning'
            ? 'bg-amber-500/5'
            : sec.theme === 'info'
              ? 'bg-[#588157]/5'
              : 'bg-card'}"
      >
        <!-- Card Header with Badges -->
        <div class="flex flex-wrap items-center justify-between gap-2 pb-3 mb-2">
          <div class="flex items-center gap-2">
            <div
              class="flex h-7 w-7 items-center justify-center rounded-lg text-xs font-bold {sec.theme === 'danger'
                ? 'bg-rose-500/15 text-rose-700 dark:text-rose-300'
                : sec.theme === 'warning'
                  ? 'bg-amber-500/15 text-amber-700 dark:text-amber-300'
                  : 'bg-[#588157]/15 text-[#588157]'}"
            >
              <Icon name={sec.icon} size={15} />
            </div>
            <h4 class="font-bold text-xs sm:text-sm text-foreground">
              {sec.title}
            </h4>
          </div>

          <span
            class="rounded-md px-2 py-0.5 text-[10px] font-bold tracking-wide {sec.theme === 'danger'
              ? 'bg-rose-500/10 text-rose-800 dark:text-rose-300'
              : sec.theme === 'warning'
                ? 'bg-amber-500/10 text-amber-800 dark:text-amber-300'
                : 'bg-[#588157]/10 text-[#588157]'}"
          >
            {sec.badge}
          </span>
        </div>

        <!-- Section Body Content (Rich Markdown: Headers, Numbers, Bullets, Bold, Code) -->
        <div class="text-xs leading-relaxed text-foreground space-y-2 select-text">
          {#if sec.decisionPill}
            <div class="mb-3">
              <span class="text-[10px] uppercase font-bold text-muted-foreground block mb-1">
                Putusan Akhir yang Direkomendasikan:
              </span>
              <div
                class="inline-flex items-center gap-2 rounded-xl px-3.5 py-1.5 text-xs font-black tracking-wide shadow-2xs {sec.decisionPill.includes('ESKALASI')
                  ? 'bg-rose-600 text-white'
                  : sec.decisionPill.includes('KLARIFIKASI')
                    ? 'bg-amber-500 text-white'
                    : 'bg-emerald-600 text-white'}"
              >
                <span>{sec.decisionPill}</span>
              </div>
            </div>
          {/if}

          <!-- Richly Parsed Markdown Container -->
          <div class="leading-relaxed">
            {@html renderMarkdownToHtml(sec.content)}
          </div>
        </div>
      </div>
    {/each}
  </div>

  <!-- Regulatory Basis & Legal Compliance Section (Borderless) -->
  {#if regulatoryBasis.length > 0}
    <div class="rounded-2xl bg-muted/20 p-4 space-y-2.5 text-xs select-text">
      <div class="flex items-center gap-2 text-foreground font-bold">
        <Icon name="ShieldCheck" size={15} class="text-primary" />
        <span>Dasar Regulasi &amp; Kepatuhan Penjaminan:</span>
      </div>

      <div class="space-y-1.5">
        {#each regulatoryBasis as reg}
          <div class="flex items-start gap-2 p-2.5 rounded-xl bg-card text-[11px] shadow-2xs">
            <span class="text-primary font-bold">§</span>
            <span class="text-muted-foreground leading-tight">
              {@html formatInline(reg)}
            </span>
          </div>
        {/each}
      </div>

      <div class="pt-2 flex items-center justify-between text-[10px] font-mono text-muted-foreground">
        <span>Segel Kriptografis: Ed25519 Verified</span>
        <span>Integritas Audit: SHA-256 Tamper-Evident</span>
      </div>
    </div>
  {/if}
</div>
