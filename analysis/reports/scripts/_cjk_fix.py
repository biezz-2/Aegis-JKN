"""Final CJK repair pass. Each mapping restores the Indonesian/English sentence
whose characters were corrupted mid-generation. Context was verified by reading
the surrounding clause before editing.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

FIXES = {
    "00-EXECUTIVE-SUMMARY.md": [
        ("Nilai argumentatif yang hilang正是 yang dicari juri",
         "Nilai argumentatif yang hilang正是 yang dicari juri".replace("正是", "memang")),
        ("SG-1b暫 corrected:", "SG-1b sementara, corrected:"),
        ("daftar kerja赞助 sustainability",
         "daftar kerja sustainability".replace("赞助", "")),
    ],
    "06-graph-mhgsl.md": [
        ("empat klaim novelty yang实际上是 adaptasi literatur",
         "empat klaim novelty yang sebenarnya adaptasi literatur"),
        ("`emerges` dari学习的 bobot", "`emerges` dari bobot yang dipelajari"),
        ("mendeskripsikan论文 Hong sebagai",
         "mendeskripsikan paper Hong sebagai"),
        ("Di graph sekecil ini,传播 neighborhood",
         "Di graph sekecil ini, neighborhood yang berkembang"),
        ("\" —變成了 **klaim**", "\" — menjadi **klaim**"),
        ("plus拆分 syndicate-level", "plus pemisahan syndicate-level"),
    ],
    "21-colab-dashboard-provenance.md": [
        ("akan把孩子 \"ambang lead 0,85\"", "akan membaca \"ambang lead 0,85\""),
    ],
}

CJK = re.compile(r"[一-鿿぀-ヿ가-힯]")

for name, pairs in FIXES.items():
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        continue
    text = open(path, encoding="utf-8").read()
    for a, b in pairs:
        if a == b:
            continue
        if a in text:
            text = text.replace(a, b)
            print("fixed  %-34s %s" % (name, a[:46]))
        else:
            print("MISS   %-34s %s" % (name, a[:46]))
    open(path, "w", encoding="utf-8").write(text)

print()
residual = 0
for name in sorted(os.listdir(ROOT)):
    if not name.endswith(".md"):
        continue
    text = open(os.path.join(ROOT, name), encoding="utf-8").read()
    for i, line in enumerate(text.split(chr(10)), 1):
        if CJK.search(line):
            residual += 1
            print("RESIDUAL %s:%d: %s" % (name, i, line[:200]))
print("residual CJK lines:", residual)
