"""Compliance check for report suite: CJK corruption + em-dash rule (Notion 00-dashboard.md:83)."""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CJK = re.compile(r"[一-鿿぀-ヿ가-힯]")
EM = chr(8212)
ED = chr(8211)

reports = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "*.md")))
reports = [os.path.normpath(p) for p in reports]

total_cjk = 0
total_em = 0
total_ed = 0
rows = []

for path in reports:
    text = open(path, encoding="utf-8").read()
    cjk = CJK.findall(text)
    em = text.count(EM)
    ed = text.count(ED)
    total_cjk += len(cjk)
    total_em += em
    total_ed += ed
    lines = text.count(chr(10))
    rows.append((os.path.basename(path), lines, len(cjk), em, ed))

print("%-38s %7s %6s %8s %8s" % ("file", "lines", "CJK", "em-dash", "en-dash"))
for name, lines, cjk, em, ed in rows:
    flag = "" if (cjk == 0 and em == 0) else "  <-- CHECK"
    print("%-38s %7d %6d %8d %8d%s" % (name, lines, cjk, em, ed, flag))

print()
print("files=%d  CJK=%d  em-dash=%d  en-dash=%d" % (len(rows), total_cjk, total_em, total_ed))

if total_cjk:
    print("\nCJK detail:")
    for path in reports:
        text = open(path, encoding="utf-8").read()
        for i, line in enumerate(text.split(chr(10)), 1):
            if CJK.search(line):
                print("  %s:%d: %s" % (os.path.basename(path), i, line[:180]))

if total_em:
    print("\nem-dash detail:")
    for path in reports:
        text = open(path, encoding="utf-8").read()
        for m in re.finditer(EM, text):
            ln = text[: m.start()].count(chr(10)) + 1
            print(
                "  %s:%d: ...%s..."
                % (
                    os.path.basename(path),
                    ln,
                    text[max(0, m.start() - 70) : m.end() + 40].replace(chr(10), " "),
                )
            )

sys.exit(0 if (total_cjk == 0 and total_em == 0) else 1)
