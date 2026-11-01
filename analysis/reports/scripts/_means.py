"""Verify the proposal's per-status mean skor_fraud claim:
'auto-clear 0.086, review 0.591, escalate 0.869'."""
import csv, io, collections, statistics, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for name, path in (
    ("claims_300_v2.1.csv (notebook payload)", "N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv"),
    ("corpus claims_v2_live.csv", "N:/HEALTHKATHON/analysis/corpus/claims_v2_live.csv"),
):
    rows = list(csv.DictReader(io.StringIO(open(path, "rb").read().decode("utf-8-sig"))))
    col = "skor_fraud" if "skor_fraud" in rows[0] else "Skor Fraud"
    st = "status" if "status" in rows[0] else "Status"
    print(f"\n### {name}")
    g = collections.defaultdict(list)
    for r in rows:
        g[r[st].strip()].append(float(r[col]))
    for k in sorted(g):
        v = g[k]
        print(f"   {k:12s} n={len(v):3d} mean={statistics.mean(v):.4f} "
              f"median={statistics.median(v):.4f} min={min(v):.2f} max={max(v):.2f}")
    print("   proposal claims: auto_clear 0.086 | review 0.591 | escalate 0.869")
