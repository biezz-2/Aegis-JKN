import csv, json, io, os
BASE = r"N:\HEALTHKATHON"
LIVE = os.path.join(BASE, r"analysis\corpus\claims_v2_live.csv")
V21  = os.path.join(BASE, r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")

def sniff(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)
        return r.fieldnames, rows

lf, lr = sniff(LIVE)
vf, vr = sniff(V21)
print("LIVE cols", len(lf)); print(lf)
print("LIVE rows", len(lr))
print("V21 cols", len(vf)); print(vf)
print("V21 rows", len(vr))
# sample values of live columns
for c in lf:
    vals = [ (row.get(c) or "") for row in lr ]
    nonempty = [v for v in vals if v.strip()!=""]
    sample = nonempty[:3]
    print("LIVECOL", c, "empty=", len(vals)-len(nonempty), "sample=", json.dumps(sample, ensure_ascii=False)[:180])
