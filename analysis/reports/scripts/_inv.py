import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))

PATS = ["corrupted/garbled", "garbled text", "corrupted text", "spliced", "garble"]

for fn in files:
    raw = open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read()
    for p in PATS:
        for m in re.finditer(re.escape(p), raw):
            i = m.start()
            print("### %s | %s" % (fn[:10], p))
            print(raw[max(0, i - 400):i + 2500].replace("\\n", "\n"))
            print()
            break
