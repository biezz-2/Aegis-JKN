import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"

TOKENS = [
    "kualitas &-have",
    "senatorsDeterministik",
    "menghapusProjection",
    "on-prem plan",
    "dataPoints",
    "instrumentSUS",
    "klaimAUPRC",
    "looked-but-not-verified",
    "saatQgshow",
    "notebookUsesIt",
    "Never global",
    "never global",
    "memDnama",
    "tidakURITY",
    "definisioki",
    "NotionBV",
    "Where laporan",
    "sudah SHOULD",
    "tidak lagiNeeded",
    "kontennyaWizard",
    "mengPresentasikan",
    "labels are downstream",
    "own-administrative",
    "survive the period",
    "danSecara",
    "danAJAX",
    "tetapiOUN",
    "adaMinimal",
    "rumahTBS",
    "shown in kurung",
    "failing into",
    "forHmengisi",
]

files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
for tok in TOKENS:
    hits = 0
    for fn in files:
        p = os.path.join(TASKS, fn)
        try:
            raw = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        i = raw.find(tok)
        if i >= 0:
            print("== %s | %s" % (fn[:10], tok))
            print("   ", repr(raw[max(0, i - 260):i + 260]))
            print()
            hits += 1
            if hits >= 2:
                break
    if hits == 0:
        print("== NOT FOUND: %s" % tok)
        print()
