import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {fn: open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read() for fn in files}

ANCHORS = [
    "P3** =",
    "P2** = kualitas",
    "kualitas &",
    "Demo butuh internet",
    "text channel labels",
    "label kanal teks",
    "hilir dari `Modus`",
    "leakage label",
    "tidak ada ambang tertulis",
    "sudah SHOULD",
    "SHOULD namun dilanggar",
    "definisi asli",
    "tidak lagi",
    "Wizard",
    "kontennya",
    "instrument",
    "saatQg",
    "Demo butuh",
    "notebook",
    "deterministiknya",
    "cara pembangkitan",
    "dataPoints",
    "titik data",
    "sintetis dipublikasikan",
    "on-prem plan",
    "rencana on-prem",
    "Mestinya",
    "periode transisi",
    "period of transition",
    "own-administrative",
    "administrasi internal",
    "Skala Saving",
    "Skala penghematan",
    "yaitu",
    "squarely",
    "kernel proposal",
    "kelengkapan",
]

for anchor in ANCHORS:
    seen = {}
    for fn in files:
        raw = blobs[fn]
        for m in re.finditer(re.escape(anchor), raw):
            i = m.start()
            w = raw[max(0, i - 70):i + 90]
            seen.setdefault(w, []).append(fn[:10])
    print("=" * 72)
    print("## %r  (%d unique)" % (anchor, len(seen)))
    for w, owners in list(seen.items())[:5]:
        print("   %r" % w)
    print()
