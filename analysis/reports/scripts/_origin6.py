import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {fn: open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read() for fn in files}

QUERIES = [
    "kernel proposal",
    "initiator",
    "Skala",
    "sudah ala",
    "22-proposal-docx-audit",
    "inti",
    "inti proposal",
    "yang initiator",
    "Skala Saving",
    "rumah TBS",
    "rumah sakit",
    "tabel",
    "instrument SUS",
    "lembar",
]

for tok in QUERIES:
    shown = 0
    for fn in files:
        raw = blobs[fn]
        for m in re.finditer(re.escape(tok), raw):
            i = m.start()
            print("== %-11s | %-22s %r" % (fn[:10], tok, raw[max(0, i - 200):i + 200]))
            print()
            shown += 1
            break
        if shown >= 2:
            break
    if shown == 0:
        print("== NOT FOUND %r" % tok)
        print()
