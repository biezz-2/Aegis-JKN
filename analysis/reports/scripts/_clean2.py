import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {fn: open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read() for fn in files}

# For each corrupted token, print unique windows wide enough to see a clean variant.
TOKENS = [
    "\u0642", "Dokumen\u0627\u0646\u062f", "\u0648\u0644\u0629", "\u0441\u0442\u0430\u0442\u0443\u0441",
    "\u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d", "\u062f\u0648\u0646", "\u0627\u0644\u0642\u0633\u0645",
    "\u0e1e\u0e32\u0e1a", "\u5be7", "\u0414\u0435\u043d", "\u652f\u6301", "\u4e8c\u91cd", "\u5e73\u5747\u503c",
    "rumahTBS", "TBS", "Closure criteria", "volumePlaceholder",
]

for tok in TOKENS:
    seen = {}
    for fn in files:
        raw = blobs[fn]
        for m in re.finditer(re.escape(tok), raw):
            i = m.start()
            w = raw[max(0, i - 110):i + 110]
            seen.setdefault(w, []).append(fn[:10])
    print("=" * 76)
    print("## %r  (%d unique)" % (tok, len(seen)))
    for w, owners in list(seen.items())[:8]:
        print("   %r" % w)
    print()
