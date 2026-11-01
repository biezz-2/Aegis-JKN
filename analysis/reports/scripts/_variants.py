import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {fn: open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read() for fn in files}

# For each anchor, print every UNIQUE 70-char window containing it (dedup across all files).
ANCHORS = [
    "harmonisasi dengan arsip",
    "jumlah skenario",
    "Closure criteria",
    "Prioritas P3",
    "per Absolutely",
    "Volume placeholder",
    "volume placeholder",
    "Skala",
    "triliunan",
    "determinist",
    "titik data",
    "dataPoints",
    "on-prem",
    "masa transisi",
    "transition",
    "hilir",
    "harus seharusnya",
    "SHOULD namun",
    "definisi",
    "diperlukan karena",
    "Wizard-of-Oz",
    "devDep",
    "Stretch",
    "instrumen",
    "saat demo",
    "saatQg",
    "notebook yang memakainya",
    "kernel",
    "inti proposal",
    "sudah ada di",
]

for anchor in ANCHORS:
    seen = {}
    for fn in files:
        raw = blobs[fn]
        for m in re.finditer(re.escape(anchor), raw):
            i = m.start()
            w = raw[max(0, i - 45):i + 55]
            seen.setdefault(w, []).append(fn[:10])
    print("=" * 72)
    print("## %r  (%d unique)" % (anchor, len(seen)))
    for w, owners in list(seen.items())[:6]:
        print("   %r" % w)
    print()
