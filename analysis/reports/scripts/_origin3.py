import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"

# (file glob prefix, token, before, after, limit)
QUERIES = [
    ("a7cf2498a9", "brief tugas", 400, 400, 3),
    ("a7cf2498a9", "AJAX", 300, 300, 3),
    ("ac31c607e0", "harmonisasi dengan arsip", 500, 300, 2),
    ("ac31c607e0", "Prioritas P3", 200, 400, 2),
    ("ac31c607e0", "Closure criteria", 200, 300, 2),
]

for pref, tok, before, after, limit in QUERIES:
    fn = None
    for f in sorted(os.listdir(TASKS)):
        if f.startswith(pref) and f.endswith(".output"):
            fn = f
            break
    if not fn:
        print("NO FILE for", pref)
        continue
    raw = open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read()
    n = 0
    for m in re.finditer(re.escape(tok), raw):
        i = m.start()
        print("== %s | %s" % (fn[:10], tok))
        print("   ", repr(raw[max(0, i - before):i + after]))
        print()
        n += 1
        if n >= limit:
            break
    if n == 0:
        print("== %s | NOT FOUND %r" % (fn[:10], tok))
        print()
