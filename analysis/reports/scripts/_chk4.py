import csv, sys, io, collections, re
sys.stdout = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_chk4.out", "w", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.DictReader(open(r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv", encoding="utf-8")))
def kid(r):
    return int(re.sub(r"\D", "", r["Name"]))
sample = sorted(rows, key=kid)[:30]
print("sample IDs:", [r["Name"] for r in sample])
c = collections.Counter(r["Sentimen"] for r in sample)
print("sample label dist:", dict(c))
SERVICE = ["antrean", "parkir", "kebersihan", "administrasi", "bertele", "makanan", "ruangan", "tidak ada keluhan berarti"]
def is_svc(s):
    s = s.lower(); return any(k in s for k in SERVICE)
for lab in ("positif", "netral", "negatif"):
    sub = [r for r in sample if r["Sentimen"] == lab]
    u = collections.Counter(r["Umpan Balik Pasien"].strip() for r in sub)
    svc = {s: n for s, n in u.items() if is_svc(s)}
    nonsvc = {s: n for s, n in u.items() if not is_svc(s)}
    print(f"\n{lab}: rows={len(sub)} unique={len(u)} service={len(svc)}u/{sum(svc.values())}r nonservice={len(nonsvc)}u/{sum(nonsvc.values())}r")
    for s, n in sorted(nonsvc.items(), key=lambda x: -x[1]):
        print(f"    x{n} {s}")
    for s, n in sorted(svc.items(), key=lambda x: -x[1]):
        print(f"    [svc] x{n} {s}")
