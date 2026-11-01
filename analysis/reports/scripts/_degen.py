"""Verify the degenerate-label claim: does `skor_fraud` separate `is_fraud`
perfectly at EVERY threshold (precision 100%, FPR 0%)?"""
import csv, io, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = list(csv.DictReader(io.StringIO(
    open("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv", "rb").read().decode("utf-8-sig"))))

P = sum(1 for r in rows if r["is_fraud"].strip() in ("1", "1.0", "True", "true"))
N = len(rows) - P
print(f"population: P(fraud)={P} N(non-fraud)={N} total={len(rows)}")

print("\nthreshold | flagged | TP | FP | FN | TN | precision | FPR | recall")
for th in (0.10, 0.14, 0.20, 0.35, 0.40, 0.45, 0.50, 0.62, 0.65, 0.70, 0.80, 0.85, 0.90):
    tp = fp = 0
    for r in rows:
        s = float(r["skor_fraud"])
        y = r["is_fraud"].strip() in ("1", "1.0", "True", "true")
        if s >= th:
            if y: tp += 1
            else: fp += 1
    fn = P - tp
    tn = N - fp
    prec = tp / (tp + fp) if tp + fp else float("nan")
    fpr = fp / N if N else float("nan")
    rec = tp / P if P else float("nan")
    print(f"  {th:5.2f}   | {tp+fp:6d} | {tp:3d} | {fp:3d} | {fn:3d} | {tn:3d} | "
          f"{prec:9.4%} | {fpr:6.2%} | {rec:7.2%}")

print("\n=== score distribution by true label ===")
lo = [float(r["skor_fraud"]) for r in rows if r["is_fraud"].strip() not in ("1", "1.0", "True", "true")]
hi = [float(r["skor_fraud"]) for r in rows if r["is_fraud"].strip() in ("1", "1.0", "True", "true")]
print(f"  non-fraud n={len(lo)} min={min(lo):.2f} max={max(lo):.2f}")
print(f"  fraud     n={len(hi)} min={min(hi):.2f} max={max(hi):.2f}")
print(f"  separation gap: non-fraud max {max(lo):.2f} < fraud min {min(hi):.2f} -> "
      f"{'PERFECT' if max(lo) < min(hi) else 'NOT perfect'}")

print("\n=== status vs is_fraud ===")
import collections
c = collections.Counter((r["status"], r["risiko"], r["is_fraud"]) for r in rows)
for k, v in sorted(c.items()):
    print("  ", k, v)

print("\n=== is_fraud vs risiko ===")
c2 = collections.Counter((r["risiko"], r["is_fraud"]) for r in rows)
for k, v in sorted(c2.items()):
    print("  ", k, v)

print("\n=== proposal claims ===")
print("  precision 94.12% / ROC-AUC 0.9825 / AUPRC 0.9142 / FPR 10.6% / masking 89.4%")
print(f"  FPR 10.6% as a count of 264 negatives -> {0.106*264:.2f} FP")
for th in (0.10, 0.14, 0.20, 0.35, 0.40, 0.45, 0.62, 0.65, 0.80, 0.85):
    fp = sum(1 for r in rows if float(r["skor_fraud"]) >= th
             and r["is_fraud"].strip() not in ("1", "1.0", "True", "true"))
    print(f"    threshold {th:5.2f} -> FP = {fp}  (FPR {fp/N:.2%})")
