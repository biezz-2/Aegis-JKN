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
]

out = []
for f in sorted(glob.glob(os.path.join(ROOT, "*.md"))):
    txt = open(f, encoding="utf-8").read()
    for i, line in enumerate(txt.split("\n"), 1):
        for j, ch in enumerate(line):
            cp = ord(ch)
            for name, lo, hi in RANGES:
                if lo <= cp <= hi:
                    ctx = line[max(0, j - 45):j + 45]
                    marked = ctx[:45] + "[" + ch + "]" + ctx[46:] if j >= 45 else ctx[:j] + "[" + ch + "]" + ctx[j + 1:]
                    out.append((os.path.basename(f), i, name, unicodedata.name(ch, "?"), marked))
                    break

for f, i, name, nm, marked in out:
    print("%-32s L%-5d %-9s %-34s %s" % (f, i, name, nm, marked))
print()
print("TOTAL:", len(out))
