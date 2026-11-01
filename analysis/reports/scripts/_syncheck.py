"""Reconcile the proposal's per-syndicate and per-modus rupiah figures against
BOTH dataset versions (300-claim notebook CSV and corpus claims_v2_live.csv)."""
import csv, io, collections, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load(p):
    return list(csv.DictReader(io.StringIO(open(p, "rb").read().decode("utf-8-sig"))))

def money(s):
    s = (s or "").replace("Rp", "").replace(".", "").strip()
    try:
        return int(float(s))
    except Exception:
        return 0

def report(name, rows, cost_col, synd_col, modus_col, fraud_col):
    print(f"\n########## {name}  (n={len(rows)}) ##########")
    tot = sum(money(r[cost_col]) for r in rows)
    print("total nominal:", f"{tot:,}")
    fraud = [r for r in rows if (r.get(fraud_col, "") or "").strip().lower() in ("1", "1.0", "true")]
    print("fraud n:", len(fraud), "nominal:", f"{sum(money(r[cost_col]) for r in fraud):,}")
    syn = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        s = (r.get(synd_col) or "").strip()
        if s and s.lower() not in ("none", "-"):
            syn[s][0] += 1
            syn[s][1] += money(r[cost_col])
    print(f"syndicate members: n={sum(v[0] for v in syn.values())} "
          f"nominal={sum(v[1] for v in syn.values()):,}")
    for s, (n, v) in sorted(syn.items()):
        print(f"   {s:12s} n={n:3d} nominal={v:,}  (Rp {v/1e6:.2f} Juta)")
    md = collections.defaultdict(lambda: [0, 0])
    for r in fraud:
        md[(r.get(modus_col) or "").strip()][0] += 1
        md[(r.get(modus_col) or "").strip()][1] += money(r[cost_col])
    print("  modus (fraud only):")
    for s, (n, v) in sorted(md.items(), key=lambda kv: -kv[1][1]):
        print(f"   {s:22s} n={n:3d} nominal={v:,}  (Rp {v/1e6:.2f} Juta)")
    print("  proposal: Phantom Rp134,25 | Upcoding Rp127,68 | Repeat Rp61,60 Juta; "
          "SYND-01..09 = 36 klaim, 60% kasus fraud, Rp542,56 Juta")

report("300-claim claims_300_v2.1.csv (notebook payload)",
       load("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv"),
       "biaya_rp", "sindikat", "modus", "is_fraud")

corpus = load("N:/HEALTHKATHON/analysis/corpus/claims_v2_live.csv")
# corpus has no is_fraud column; derive fraud = Risiko == fraud
for r in corpus:
    r["_is_fraud"] = "1" if (r.get("Risiko") or "").strip().lower() == "fraud" else "0"
report("corpus claims_v2_live.csv", corpus,
       "Biaya Rp", "Sindikat", "Modus", "_is_fraud")
