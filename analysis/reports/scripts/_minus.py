import re, glob, sys, os

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"N:/HEALTHKATHON/analysis/reports"
n = 0
for f in sorted(glob.glob(os.path.join(ROOT, "*.md"))):
    for i, line in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
        if "\u2212" in line:
            n += 1
            if n <= 30:
                for m in re.finditer("\u2212", line):
                    j = m.start()
                    print("%-30s L%-5d %r" % (os.path.basename(f), i, line[max(0, j - 40):j + 40]))
            break
print("lines with minus:", n)
