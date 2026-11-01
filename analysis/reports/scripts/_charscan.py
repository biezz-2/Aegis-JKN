import re, glob, sys, os, unicodedata

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"N:/HEALTHKATHON/analysis/reports"

RANGES = [
    ("CYRILLIC", 0x0400, 0x04FF),
    ("GREEK", 0x0370, 0x03FF),
    ("CJK", 0x4E00, 0x9FFF),
    ("CJK_EXT", 0x3400, 0x4DBF),
    ("HIRAGANA", 0x3040, 0x309F),
    ("KATAKANA", 0x30A0, 0x30FF),
    ("HANGUL", 0xAC00, 0xD7AF),
    ("THAI", 0x0E00, 0x0E7F),
    ("ARABIC", 0x0600, 0x06FF),
    ("HEBREW", 0x0590, 0x05FF),
    ("DEVANAGARI", 0x0900, 0x097F),
    ("EMOJI", 0x1F300, 0x1FAFF),
]

out = []
for f in sorted(glob.glob(os.path.join(ROOT, "*.md"))):
    txt = open(f, encoding="utf-8").read()
    lines = txt.split("\n")
    for i, line in enumerate(lines, 1):
        for j, ch in enumerate(line):
            cp = ord(ch)
            for name, lo, hi in RANGES:
                if lo <= cp <= hi:
                    out.append((os.path.basename(f), i, name, hex(cp), unicodedata.name(ch, "?"), line.strip()[:150]))
                    break
        # em-dash / en-dash / curly quotes
        for ch, nm in (("\u2014", "EMDASH"), ("\u2013", "ENDASH"), ("\u2018", "LSQUO"), ("\u2019", "RSQUO"), ("\u201c", "LDQUO"), ("\u201d", "RDQUO"), ("\u2212", "MINUS")):
            if ch in line:
                out.append((os.path.basename(f), i, nm, hex(ord(ch)), ch, line.strip()[:150]))

print("TOTAL FLAGS:", len(out))
by = {}
for r in out:
    by.setdefault(r[2], []).append(r)
for k in sorted(by):
    print()
    print("### %s  x%d" % (k, len(by[k])))
    seen = set()
    for f, i, nm, cp, nmv, l in by[k]:
        key = (f, l)
        if key in seen:
            continue
        seen.add(key)
        print("  %-32s L%-5d %s  %s" % (f, i, nmv, l))
