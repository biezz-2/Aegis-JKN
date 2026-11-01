"""Second-pass em-dash sweep: keep only genuinely quoted data values.

Keep rule: the em-dash is immediately wrapped by backticks, straight double
quotes, or asterisks (bold). Everything else is report prose and must go,
per Notion 00-dashboard.md:83 "Dokumen formal tidak menggunakan em-dash."
"""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

EM = chr(8212)
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
paths = sorted(glob.glob(os.path.join(ROOT, "*.md")))

KEEP_PAIRS = (("`", "`"), ('"', '"'), ("*", "*"))


def is_quoted(text, i):
    prev = text[i - 1] if i > 0 else ""
    nxt = text[i + 1] if i + 1 < len(text) else ""
    for a, b in KEEP_PAIRS:
        if prev == a and nxt == b:
            return True
    return False


changed = {}
for path in paths:
    text = open(path, encoding="utf-8").read()
    out = []
    last = 0
    n = 0
    for m in re.finditer(EM, text):
        if is_quoted(text, m.start()):
            continue
        out.append(text[last : m.start()])
        out.append("-")
        last = m.end()
        n += 1
    if n:
        out.append(text[last:])
        open(path, "w", encoding="utf-8").write("".join(out))
        changed[os.path.basename(path)] = n

for k, v in sorted(changed.items(), key=lambda kv: -kv[1]):
    print("%-38s %d" % (k, v))
print("total replaced:", sum(changed.values()))
