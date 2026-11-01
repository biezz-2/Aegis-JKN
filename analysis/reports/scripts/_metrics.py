import csv, collections, io, math, hashlib

def load(p):
    raw = open(p,'rb').read()
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))), raw

nb, _ = load("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv")
live, raw_live = load("N:/HEALTHKATHON/analysis/corpus/claims_v2_live.csv")

print("=== rows nb vs live:", len(nb), len(live))
print("live cols:", list(live[0].keys()))
print("live sha:", hashlib.sha256(raw_live).hexdigest())

def f(x):
    try: return float(x)
    except: return None

def curve_metrics(y, s):
    """Compute accuracy/precision/recall/F1/ROC-AUC/AUPRC from score s."""
    pairs = sorted(zip(s, y))
    n = len(y); P = sum(y); N = n - P
    # AUC via rank (Mann-Whitney) with ties
    ranks = {}
    i = 0; r = [0.0]*n
    while i < n:
        j = i
        while j+1 < n and pairs[j+1][0] == pairs[i][0]: j += 1
        avg = (i+j)/2.0 + 1
        for k in range(i, j+1): r[k] = avg
        i = j+1
    sum_pos = sum(r[k] for k in range(n) if pairs[k][1]==1)
    auc = (sum_pos - P*(P+1)/2.0)/(P*N) if P and N else float('nan')
    # AUPRC (average precision)
    tp = 0; ap = 0.0; prev_rec = 0.0
    for idx in range(n-1, -1, -1):
        sc, lb = pairs[idx]
        if lb == 1:
            tp += 1
            rec = tp/P if P else 0
            prec = tp/(n-idx)
            ap += prec*(rec-prev_rec); prev_rec = rec
    # threshold sweep
    best = None
    for t in sorted(set(s)):
        pred = [1 if x >= t else 0 for x in s]
        tp = sum(1 for i in range(n) if pred[i] and y[i]); fp = sum(1 for i in range(n) if pred[i] and not y[i])
        fn = P - tp; tn = N - fp
        acc = (tp+tn)/n
        prec = tp/(tp+fp) if tp+fp else 0.0
        rec = tp/P if P else 0.0
        f1 = 2*prec*rec/(prec+rec) if prec+rec else 0.0
        if best is None or f1 > best[4]:
            best = (t, acc, prec, rec, f1, tp, fp, fn, tn)
    return auc, ap, best

for label, rows in [("nb (300)", nb), ("live", live)]:
    if 'is_fraud' not in rows[0]: continue
    y = [int(r['is_fraud']) for r in rows]
    print(f"\n===== {label}: n={len(rows)} P={sum(y)} ({sum(y)/len(y)*100:.2f}%)")
    # candidate score columns
    for col in ['skor_fraud','skor_sentimen']:
        if col not in rows[0]: continue
        s = [f(r[col]) or 0.0 for r in rows]
        auc, ap, best = curve_metrics(y, s)
        print(f"  {col}: AUC={auc:.4f} AP={ap:.4f} bestF1thr={best[0]:.4f} acc={best[1]*100:.2f}% prec={best[2]*100:.2f}% rec={best[3]*100:.2f}% f1={best[4]:.4f} (tp{best[5]},fp{best[6]},fn{best[7]},tn{best[8]})")
    # fixed threshold 0.85 and 0.5
    for col in ['skor_fraud']:
        if col not in rows[0]: continue
        s = [f(r[col]) or 0.0 for r in rows]
        for t in (0.5, 0.6, 0.7, 0.8, 0.85, 0.9):
            pred = [1 if x>=t else 0 for x in s]
            tp=sum(1 for i in range(len(y)) if pred[i] and y[i]); fp=sum(1 for i in range(len(y)) if pred[i] and not y[i])
            fn=sum(y)-tp; tn=len(y)-tp-fp
            prec = tp/(tp+fp) if tp+fp else 0.0
            print(f"    thr={t}: acc={(tp+tn)/len(y)*100:.2f}% prec={prec*100:.2f}% rec={tp/sum(y)*100:.2f}% fpr={fp/(len(y)-sum(y))*100:.2f}%")
