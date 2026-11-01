import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"

# report file -> (token, before, after)
QUERIES = {
    "20-repo-artifact-integrity.md": ("senatorsDeterministik", 300, 300),
    "03-architecture.md": ("menghapusProjection", 300, 300),
    "10-competition.md": ("Kelayakan implementasi", 300, 400),
    "15-code-quality.md": ("&-have", 350, 350),
    "14-language.md": ("sudah SHOULD", 300, 300),
    "15-code-quality.md ": ("lagiNeeded", 300, 300),
    "09-security.md": ("tidakURITY", 300, 300),
    "13-text-channel.md": ("labels are downstream", 300, 300),
    "11-compliance.md": ("own-administrative", 300, 300),
    "07-generator.md": ("memDnama", 300, 300),
    "08-frontend.md": ("mengPresentasikan", 300, 300),
    "21-numbers-of-record.md": ("NotionBV", 300, 300),
    "00-EXECUTIVE-SUMMARY.md": ("Where laporan", 300, 300),
    "17-roadmap.md": ("instrumentSUS", 300, 300),
}

files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {}
for fn in files:
    blobs[fn] = open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read()

for (rep, (tok, before, after)) in QUERIES.items():
    rep = rep.strip()
    owners = [fn for fn in files if rep in blobs[fn]]
    print("=" * 70)
    print("%s | token %r | owners: %s" % (rep, tok, [f[:10] for f in owners][:3]))
    for fn in owners[:2]:
        raw = blobs[fn]
        for m in list(re.finditer(re.escape(tok), raw))[:2]:
            i = m.start()
            print("   ", fn[:10], repr(raw[max(0, i - before):i + after]))
    print()
