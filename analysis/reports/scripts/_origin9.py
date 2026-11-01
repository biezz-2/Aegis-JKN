import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {fn: open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read() for fn in files}

ANCHORS = [
    "Cakupan/pembagian",
    "Dokumen",
    "yang sama dengan `03` L98",
    "label status sumber, bukan",
    "Prinsip UU PDP (Pasal 16)",
    "berlaku tanpa",
    "Section 3",
    "pola yang sama tanpa label",
    "Cost-to-Impact 1 : 15 (L27",
    "kapasitas naik 6,667 kali",
    "penanda prinsip",
    "overcharge. Hapus",
    "Angka",
    "Gerbang",
    "Klaim",
    "benchmark",
    "pada baris",
    "pengcollectoran",
    "wasted effort",
    "looked-but-not-verified",
    "dataPoints",
    "data looked",
]

for anchor in ANCHORS:
    seen = {}
    for fn in files:
        raw = blobs[fn]
        for m in re.finditer(re.escape(anchor), raw):
            i = m.start()
            w = raw[max(0, i - 100):i + 120]
            seen.setdefault(w, []).append(fn[:10])
    print("=" * 74)
    print("## %r  (%d unique)" % (anchor, len(seen)))
    for w, owners in list(seen.items())[:8]:
        print("   %r" % w)
    print()
