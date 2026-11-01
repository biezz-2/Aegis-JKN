import re, glob, sys, os, unicodedata
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"N:/HEALTHKATHON/analysis/reports"
c = Counter()
where = {}
for f in sorted(glob.glob(os.path.join(ROOT, "*.md"))):
    for i, line in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
        for j, ch in enumerate(line):
            cp = ord(ch)
            if 0x0370 <= cp <= 0x03FF or cp == 0x2212:
                c[ch] += 1
                where.setdefault(ch, []).append((os.path.basename(f), i, line.strip()[:110]))
for ch, n in c.most_common():
    print("%-3s %-4s x%-4d  %s" % (ch, hex(ord(ch)), n, unicodedata.name(ch, "?")))
    for w in where[ch][:2]:
        print("      %-32s L%-5d %s" % w)
