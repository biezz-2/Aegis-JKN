"""Search the 300-claim dataset for any (column, threshold) combination that
reproduces the archived headline metrics: acc 93.0%, prec 94.12%, ROC-AUC 0.9825,
AUPRC 0.9142, FPR 10.6%, masking resilience 89.4%.
"""
import csv, io, collections, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = "N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv"
rows = list(csv.DictReader(io.StringIO(open(P, "rb").read().decode("utf-8-sig"))))


def num(x):
    try:
        return float(x)
    except Exception:
        return None


def auc_ap(y, s):
    pairs = sorted(zip(s, y))
    n = len(y)
    P_ = sum(y)
    N_ = n - P_
    r = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and pairs[j + 1][0] == pairs[i][0]:
            j += 1
        a = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            r[k] = a
        i = j + 1
    sp = sum(r[k] for k in range(n) if pairs[k][1] == 1)
    auc = (sp - P_ * (P_ + 1) / 2.0) / (P_ * N_) if P_ and N_ else float("nan")
    tp = 0
    ap = 0.0
    prev = 0.0
    for idx in range(n - 1, -1, -1):
        sc, lb = pairs[idx]
        if lb == 1:
            tp += 1
            rec = tp / P_
            prec = tp / (n - idx)
            ap += prec * (rec - prev)
            prev = rec
    return auc, ap


y = [int(r["is_fraud"]) for r in rows]
P_ = sum(y)
N_ = len(y) - P_
print(f"n={len(rows)} P={P_} N={N_}")

TARGETS = {"acc93": 0.930, "prec9412": 0.9412, "auc9825": 0.9825,
           "auprc9142": 0.9142, "fpr106": 0.106, "res894": 0.894}

# candidate numeric columns
cands = []
for col in rows[0].keys():
    vals = [num(r[col]) for r in rows]
    if all(v is None for v in vals):
        continue
    if len(set(v for v in vals if v is not None)) > 60:
        continue
    cands.append(col)
print("candidate score columns:", cands)

found = collections.defaultdict(list)
for col in cands:
    s = [num(r[col]) or 0.0 for r in rows]
    if len(set(s)) < 2:
        continue
    for direction in (1, -1):
        ss = [x * direction for x in s]
        a, ap = auc_ap(y, ss)
        for name, val in (("auc9825", a), ("auprc9142", ap)):
            if abs(val - TARGETS[name]) < 5e-4:
                found[name].append((col, direction, round(val, 6)))
    # threshold sweep
    for t in sorted(set(s)):
        pred = [1 if x >= t else 0 for x in s]
        tp = sum(1 for i in range(len(y)) if pred[i] and y[i])
        fp = sum(1 for i in range(len(y)) if pred[i] and not y[i])
        fn = P_ - tp
        tn = N_ - fp
        if tp + fp == 0:
            continue
        acc = (tp + tn) / len(y)
        prec = tp / (tp + fp)
        fpr = fp / N_
        if abs(acc - TARGETS["acc93"]) < 5e-4:
            found["acc93"].append((col, t, round(acc, 6), round(prec, 6)))
        if abs(prec - TARGETS["prec9412"]) < 5e-4:
            found["prec9412"].append((col, t, round(prec, 6), round(acc, 6)))
        if abs(fpr - TARGETS["fpr106"]) < 5e-4:
            found["fpr106"].append((col, t, round(fpr, 6), round(acc, 6)))

for k in ("acc93", "prec9412", "auc9825", "auprc9142", "fpr106"):
    v = found.get(k, [])
    print(f"\n### {k}: {len(v)} hit(s)")
    for x in v[:12]:
        print("   ", x)

print("\n### AUC/AP of each candidate column (max achievable by a score column):")
for col in cands:
    s = [num(r[col]) or 0.0 for r in rows]
    if len(set(s)) < 2:
        continue
    a1, ap1 = auc_ap(y, s)
    a2, ap2 = auc_ap(y, [-x for x in s])
    print(f"   {col:24s} AUC={max(a1,a2):.4f} AP={max(ap1,ap2):.4f}")
