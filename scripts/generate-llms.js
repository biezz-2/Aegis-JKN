#!/usr/bin/env node
/**
 * Regenerate wiki/llms.txt (index) and wiki/llms-full.txt (concatenated pages)
 * from the pages listed in wiki/.index.json.
 *
 * Usage: node scripts/generate-llms.js
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const wiki = join(root, 'wiki');
const index = JSON.parse(readFileSync(join(wiki, '.index.json'), 'utf8'));

const BAR = '='.repeat(80);
const read = (rel) => readFileSync(join(wiki, rel), 'utf8');

/* ---------- llms.txt : human/agent-readable index ---------- */

const GROUP = { overview: 'Overview', concept: 'Concepts', guide: 'Guides', reference: 'Reference' };
const sections = [];
for (const [type, heading] of Object.entries(GROUP)) {
  const pages = index.pages.filter((p) => p.type === type);
  if (!pages.length) continue;
  sections.push(
    `## ${heading}\n` +
      pages.map((p) => `- [${p.title}](${p.path}): ${p.summary ?? p.tags.slice(0, 4).join(', ')}`).join('\n')
  );
}
const llmsTxt = `# Aegis-JKN Agent Wiki Index\n\n> ${index.description ?? 'MHGSL fraud intelligence for JKN/BPJS, plus the SvelteKit Dashboard Verifikator.'}\n\n${sections.join('\n\n')}\n`;
writeFileSync(join(wiki, 'llms.txt'), llmsTxt);

/* ---------- llms-full.txt : every page, verbatim ---------- */

const blocks = index.pages.map((p) => `${BAR}\nFILE: ${p.path}\n${BAR}\n\n${read(p.path)}`);
writeFileSync(join(wiki, 'llms-full.txt'), `﻿\n\n${blocks.join('\n\n')}`);

console.log(`llms.txt: ${index.pages.length} pages indexed`);
console.log(`llms-full.txt: ${blocks.length} blocks`);
