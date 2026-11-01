import csv, io, collections, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = list(csv.DictReader(io.StringIO(
    open("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv", "rb").read().decode("utf-8-sig"))))
print("rows:", len(rows))
mx = collections.defaultdict(float)
for r in rows:
    mx[r["diagnosis_code"]] = max(mx[r["diagnosis_code"]], float(r["skor_fraud"]))
for k in ("K29.7","K35.8","K40.9","I21.9","J18.9","E11.9","N20.0","S72.0","O80","K80.2"):
    print(f"  {k:8s} n={sum(1 for r in rows if r['diagnosis_code']==k):3d} skor_max={mx[k]:.2f}")
print()
# pasien doc counts from 10-simulation-dataset.md
doc = open("N:/HEALTHKATHON/analysis/corpus/10-simulation-dataset.md", encoding="utf-8").read()
import re
print("=== lines mentioning 36.13 ===")
for l in doc.split("\n"):
    if "36.13" in l or "78.000.000" in l or "Coronary" in l:
        print("  ", l.strip()[:180])
print()
print("=== dokter table lines ===")
for l in doc.split("\n"):
    if re.match(r"\s*\|\s*D\d\d\s*\|", l):
        print("  ", l.strip()[:180])
