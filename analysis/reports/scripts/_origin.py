import sys, glob, re, os

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"

TARGETS = [
    ("a7cf2498a9485c4f1.output", "Sequential Learning", 320, 320, 4),
    ("ac31c607e00c90d21.output", "Prioritas P3", 160, 320, 4),
    ("ac31c607e00c90d21.output", "tetapiOUN", 260, 260, 3),
    ("ac31c607e00c90d21.output", "adaMinimal", 260, 260, 3),
    ("abef7738a09ac7d14.output", "saatQgshow", 220, 220, 3),
    ("abef7738a09ac7d14.output", "instrumentSUS", 260, 260, 3),
    ("abef7738a09ac7d14.output", "klaimAUPRC", 220, 220, 3),
    ("abef7738a09ac7d14.output", "looked-but-not-verified", 260, 260, 3),
    ("af0873cb18fb82878.output", "failing into", 300, 300, 3),
]

for fn, tok, before, after, limit in TARGETS:
    p = os.path.join(TASKS, fn)
    if not os.path.exists(p):
        print("MISSING FILE", fn)
        continue
    raw = open(p, encoding="utf-8", errors="replace").read()
    n = 0
    for m in re.finditer(re.escape(tok), raw):
        i = m.start()
        print("  %s | %r" % (fn[:10], raw[max(0, i - before):i + after]))
        print()
        n += 1
        if n >= limit:
            break
    if n == 0:
        print("  %s | token not found: %r" % (fn[:10], tok))
        print()
