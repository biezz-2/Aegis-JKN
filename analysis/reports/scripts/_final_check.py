import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {fn: open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read() for fn in files}

ANCHORS = [
    "konstanta UI, bukan hasil pengukuran",
    "menutup instance konkret",
    "experimentally",
    "memuat prinsip",
    "kewajiban hukum",
    "dilarang",
    "Ini **bukan** bukti fabrikasi",
    "bukti bahwa nilai tersebut dapat dibangkitkan",
    "Klaim financial",
    "auto_clear",
    "klaim kuantitatif",
    "Ratusan miliar",
    "ratusan miliar",
]

for anchor in ANCHORS:
    seen = {}
    for fn in files:
        raw = blobs[fn]
        for m in re.finditer(re.escape(anchor), raw):
            i = m.start()
            w = raw[max(0, i - 110):i + 130]
            seen.setdefault(w, []).append(fn[:10])
    print("=" * 76)
    print("## %r  (%d unique)" % (anchor, len(seen)))
    for w, owners in list(seen.items())[:5]:
        print("   %r" % w)
    print()
