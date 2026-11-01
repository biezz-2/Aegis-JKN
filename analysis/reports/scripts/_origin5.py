import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {fn: open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read() for fn in files}

QUERIES = [
    "perlu harmonisasi",
    "Prioritas P3 (",
    "P3 (",
    "kurung",
    "Closure criteria, ",
    "kernelDAY",
    "yaituInitializer",
    "SkalaSaving",
    "sudahala",
    "sudah SHOULD",
    "tidak lagiNeeded",
    "kontennyaWizard",
    "sudah terisi",
    "labels are",
    "notebookUsesIt",
    "senatorsDeterministik",
    "menghapusProjection",
    "perREADME",
    "on-prem",
    "dataPoints",
]

for tok in QUERIES:
    shown = 0
    for fn in files:
        raw = blobs[fn]
        for m in re.finditer(re.escape(tok), raw):
            i = m.start()
            print("== %-11s | %-24s %r" % (fn[:10], tok, raw[max(0, i - 220):i + 220]))
            print()
            shown += 1
            break
        if shown >= 2:
            break
    if shown == 0:
        print("== NOT FOUND %r" % tok)
        print()
