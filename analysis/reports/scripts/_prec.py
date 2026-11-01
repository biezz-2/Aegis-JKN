"""Exhaustive scan over EVERY distinct threshold (all unique skor_fraud values):
can precision 94.12% be reached? Which thresholds give precision 100%?"""
import csv, io, sys
from fractions import Fraction
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = list(csv.DictReader(io.StringIO(
    open("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv", "rb").read().decode("utf-8-sig"))))
data = [(float(r["skor_fraud"]), r["is_fraud"].strip() in ("1", "1.0", "True", "true")) for r in rows]
P = sum(1 for _, y in data if y)
N = len(data) - P

TARGET = Fraction(9412, 10000)
print(f"P={P} N={N}; target precision = {float(TARGET):.4%} = 94/100? {Fraction(94,100)}")

hits = []
prec100 = []
for th in sorted({s for s, _ in data}):
    tp = sum(1 for s, y in data if s >= th and y)
    fp = sum(1 for s, y in data if s >= th and not y)
    if tp + fp == 0:
        continue
    pr = Fraction(tp, tp + fp)
    if pr == TARGET:
        hits.append((th, tp, fp))
    if pr == 1:
        prec100.append((th, tp, fp))

print(f"\nthresholds giving precision EXACTLY 94.12%: {len(hits)}")
for th, tp, fp in hits:
    print(f"   threshold {th:.2f}: TP={tp} FP={fp} flagged={tp+fp}")
print(f"\nthresholds giving precision 100%: {len(prec100)}")
for th, tp, fp in prec100:
    print(f"   threshold {th:.2f}: TP={tp} FP={fp} recall={tp/P:.2%}")

print("\n=== all thresholds: precision curve ===")
for th in sorted({s for s, _ in data}):
    tp = sum(1 for s, y in data if s >= th and y)
    fp = sum(1 for s, y in data if s >= th and not y)
    if tp + fp == 0:
        continue
    print(f"   th={th:5.2f} TP={tp:3d} FP={fp:3d} precision={tp/(tp+fp):8.4%} "
          f"FPR={fp/N:7.2%} recall={tp/P:7.2%}")

print("\n=== nearest reachable precisions to 94.12% ===")
seen = set()
near = []
for th in sorted({s for s, _ in data}):
    tp = sum(1 for s, y in data if s >= th and y)
    fp = sum(1 for s, y in data if s >= th and not y)
    if tp + fp == 0:
        continue
    pr = Fraction(tp, tp + fp)
    if pr in seen:
        continue
    seen.add(pr)
    near.append((abs(float(pr) - float(TARGET)), float(pr), tp, fp))
for d, pr, tp, fp in sorted(near)[:8]:
    print(f"   precision {pr:9.6%} (TP={tp}, FP={fp})  |diff|={d:.6f}")
