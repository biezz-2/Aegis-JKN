"""Locate each CJK character in the report suite with tight context."""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
CJK = re.compile(r"[一-鿿぀-ヿ가-힯]")

for name in sorted(os.listdir(ROOT)):
    if not name.endswith(".md"):
        continue
    text = open(os.path.join(ROOT, name), encoding="utf-8").read()
    hits = list(CJK.finditer(text))
    if not hits:
        continue
    print("=" * 70)
    print(name, "-", len(hits), "CJK chars")
    for m in hits:
        ln = text[: m.start()].count(chr(10)) + 1
        ctx = text[max(0, m.start() - 55) : m.end() + 45].replace(chr(10), " ")
        print("  L%-4d %r" % (ln, ctx))
