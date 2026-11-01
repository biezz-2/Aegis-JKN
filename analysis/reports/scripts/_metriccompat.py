"""Cross-check the proposal's metric triple for mutual compatibility, and
the +28.6% arithmetic."""
import csv, io, json, sys
from fractions import Fraction
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

print("=== (1) +28,6% arithmetic ===")
print(f"  0.9142/0.71 - 1 = {(0.9142/0.71 - 1)*100:.4f}%  -> proposal says +28,6%")
print(f"  (0.91 - 0.71)/0.71 = {(0.91-0.71)/0.71*100:.4f}%  (using hardcoded MHGSL 0.91)")
print(f"  0.9142/0.71 = {0.9142/0.71:.6f}")

print("\n=== (2) what TP/FP ratios equal 94.12% exactly? ===")
for d in range(1, 120):
    for n in range(d, 120):
        if Fraction(n, d) == Fraction(9412, 10000):
            print(f"   {n}/{d} = {n/d:.6%}")

print("\n=== (3) are the three proposal metrics mutually compatible on ONE column? ===")
rows = list(csv.DictReader(io.StringIO(
    open("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv", "rb").read().decode("utf-8-sig"))))
data = [(float(r["skor_fraud"]), r["is_fraud"].strip() in ("1", "1.0", "True", "true")) for r in rows]
P = sum(1 for _, y in data if y); N = len(data) - P
print(f"  P={P} N={N}")
for th in sorted({s for s, _ in data}):
    tp = sum(1 for s, y in data if s >= th and y)
    fp = sum(1 for s, y in data if s >= th and not y)
    if tp + fp == 0: continue
    pr = tp/(tp+fp); fpr = fp/N
    tag = []
    if abs(pr - 0.9412) < 1e-9: tag.append("PRECISION=94.12%")
    if abs(fpr - 0.106) < 0.0005: tag.append("FPR=10.6%")
    if tp == P and fp == 0: tag.append("precision=100%, FPR=0%")
    if tag:
        print(f"   th={th:5.2f} TP={tp:3d} FP={fp:3d} prec={pr:8.4%} FPR={fpr:7.2%}  <-- {' | '.join(tag)}")
print("  (blank above = no threshold satisfies more than one of the three claims)")

print("\n=== (4) payload feed sizes / LLM sample count ===")
d = json.load(open("N:/HEALTHKATHON/mechine-learning-deep-learning/colab/payload-aegis-jkn.json", encoding="utf-8"))
for k in ("twFeed", "rdFeed"):
    v = d.get(k)
    print(f"  {k}: type={type(v).__name__} len={len(v) if v is not None else None}")
for k in ("gtSent", "twSent", "rdSent"):
    v = d.get(k)
    print(f"  {k}: len={len(v) if v is not None else None} "
          f"sample={json.dumps(v[0], ensure_ascii=False)[:200] if v else None}")
