import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {fn: open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read() for fn in files}

# (label, token, before, after, max_hits)
QUERIES = [
    ("P3-heading", "Prioritas P3", 120, 260, 6),
    ("P3-heading-alt", "Prioritas P3 (", 60, 160, 6),
    ("volumePlaceholder", "volumePlaceholder", 260, 260, 6),
    ("Medical-A", "Medical-A", 300, 300, 4),
    ("Medical-1", "Medical-1", 300, 300, 4),
    ("survive", "survive", 220, 220, 4),
    ("own-administrative", "own-administrative", 200, 200, 4),
    ("on-prem plan", "on-prem plan", 220, 220, 4),
    ("dan-AJAX", "danAJAX", 200, 200, 3),
    ("senators", "senators", 200, 200, 3),
    ("dataPoints", "dataPoints", 200, 200, 3),
    ("labels are downstream of", "labels are downstream", 200, 200, 3),
    ("Closure criteria", "Closure criteria", 160, 200, 4),
    ("notebookUsesIt-ctx", "notebookUsesIt", 200, 200, 3),
    ("SUS", "lembar instrumen", 120, 200, 4),
]

for label, tok, before, after, cap in QUERIES:
    print("=" * 72)
    print("## %s  token=%r" % (label, tok))
    shown = 0
    for fn in files:
        raw = blobs[fn]
        for m in re.finditer(re.escape(tok), raw):
            i = m.start()
            print("  [%s] %r" % (fn[:10], raw[max(0, i - before):i + after]))
            shown += 1
            break
        if shown >= cap:
            break
    if shown == 0:
        print("  (not found)")
    print()
