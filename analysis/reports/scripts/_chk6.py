import csv, sys, io, collections
sys.stdout = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_chk6.out", "w", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.DictReader(open(r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv", encoding="utf-8")))
c = collections.defaultdict(collections.Counter)
for r in rows:
    c[r["Umpan Balik Pasien"].strip()][r["Sentimen"]] += 1
print("=== 36 strings: label + count ===")
for s, lab in sorted(c.items(), key=lambda x: -sum(x[1].values())):
    print(f"{sum(lab.values()):4}  {dict(lab)}  {s}")
SERVICE = ["antrean", "parkir", "kebersihan", "administrasi", "bertele", "makanan", "ruangan", "tidak ada keluhan berarti"]
def is_svc(s):
    s = s.lower(); return any(k in s for k in SERVICE)
print("\n=== per label: service vs non-service ===")
for lab in ("positif", "netral", "negatif"):
    sub = {s: v for s, v in c.items() if lab in v}
    svc = {s: v for s, v in sub.items() if is_svc(s)}
    ns = {s: v for s, v in sub.items() if not is_svc(s)}
    print(f"{lab}: unique={len(sub)} rows={sum(sum(v.values()) for v in sub.values())} | "
          f"svc {len(svc)}u/{sum(sum(v.values()) for v in svc.values())}r | "
          f"nonsvc {len(ns)}u/{sum(sum(v.values()) for v in ns.values())}r")
    for s, v in sorted(svc.items(), key=lambda x: -sum(x[1].values())):
        print(f"    [svc] {sum(v.values()):3} {s}")
