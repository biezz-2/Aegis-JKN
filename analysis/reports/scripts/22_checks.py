#!/usr/bin/env python3
"""22_checks.py - quality checks over extracted docx paragraphs.
Usage: python -I 22_checks.py <paragraphs.txt>
"""
import sys, re, unicodedata

path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")

items = []
for ln in lines:
    m = re.match(r"\[(\d+)\](?:<([^>]*)>)? ?(.*)$", ln)
    if m:
        items.append((int(m.group(1)), m.group(2) or "", m.group(3)))

text = "\n".join(t for _, _, t in items)

print("=== EM DASH / DASH AUDIT ===")
for name, ch in [("em-dash U+2014", "—"), ("en-dash U+2013", "–"),
                 ("horiz-bar U+2015", "―"), ("minus U+2212", "−")]:
    print("%s: %d" % (name, text.count(ch)))

# per BAB
print("\n--- em-dash per BAB ---")
cur = "PRE-BAB (front matter)"
counts = {}
for i, st, t in items:
    m = re.match(r"BAB ([IVX]+):", t.strip())
    if m:
        cur = "BAB " + m.group(1)
    counts.setdefault(cur, [0, 0])
    counts[cur][0] += t.count("—")
    counts[cur][1] += 1
for k, v in counts.items():
    if v[0] or k.startswith("BAB"):
        print("%-14s em-dash=%d  paras=%d" % (k, v[0], v[1]))

print("\n=== PLACEHOLDERS ===")
for pat in [r"TBD", r"\bTODO\b", r"XXX", r"Lorem", r"\[placeholder\]", r"placeholder",
            r"\bFIXME\b", r"\?\?\?", r"\[insert", r"isi di sini", r"\[\]", r"\bN/A\b",
            r"\[JUDUL KARYA INOVASI\]", r"<[^>]{2,30}>"]:
    hits = [(i, t) for i, _, t in items if re.search(pat, t)]
    if hits:
        print("PATTERN %s -> %d hits" % (pat, len(hits)))
        for i, t in hits[:8]:
            print("   [%04d] %s" % (i, t[:180]))

print("\n=== SIGATURE / DATE / TEAM ===")
for i, st, t in items:
    if re.search(r"Mengetahui|Meterai|Tanda tangan|Ttd|ttd|NIP|Nama Penulis|Kepala|Nomor|NIK|NIB|Tanggal|Cimahi|JAKARTA", t, re.I):
        print("[%04d] %s" % (i, t[:300]))

print("\n=== PROTOTYPE / PURWARUPA MENTIONS ===")
for i, st, t in items:
    if re.search(r"purwarupa|prototype|purwarupa|bukan produksi|proof of concept|PoC", t, re.I):
        print("[%04d] %s" % (i, t[:260]))

print("\n=== SINTETIS MENTIONS ===")
for i, st, t in items:
    if re.search(r"sintetis|synthetic", t, re.I):
        print("[%04d] %s" % (i, t[:260]))

print("\n=== FIGURE CAPTION REFERENCES IN BODY (Gambar X.Y) ===")
for i, st, t in items:
    for m in re.finditer(r"Gambar\s+\d+\.\d+", t):
        print("[%04d] %s :: %s" % (i, m.group(0), t[:120]))

print("\n=== TABLE CAPTION REFERENCES IN BODY ===")
for i, st, t in items:
    for m in re.finditer(r"Tabel\s+\d+\.\d+", t):
        print("[%04d] %s :: %s" % (i, m.group(0), t[:120]))

print("\n=== ACRONYM FIRST OCCURRENCE ===")
acr = ["MHGSL", "CDSS", "CDS", "XAI", "SHAP", "FPR", "AUPRC", "ROC-AUC", "SUS",
       "OASIS", "SATUSEHAT", "FHIR", "DPJP", "FKRTL", "DJS", "INA-CBG", "RBAC",
       "HSM", "PWA", "LOGO", "TKMKB", "PK-JKN", "FIS", "ICDP-10", "ICD-9"]
for a in acr:
    first = None
    cnt = 0
    for i, st, t in items:
        c = len(re.findall(re.escape(a), t))
        if c:
            cnt += c
            if first is None:
                first = (i, t[:150])
    if first:
        print("%-10s total=%-4d first=[%04d] %s" % (a, cnt, first[0], first[1]))
    else:
        print("%-10s NOT FOUND" % a)

print("\n=== TITLE CONSISTENCY: Aegis-JKN vs DETECT-JKN ===")
for i, st, t in items:
    if "DETECT-JKN" in t.upper() or "Detect-JKN" in t:
        print("[%04d] %s" % (i, t[:200]))
