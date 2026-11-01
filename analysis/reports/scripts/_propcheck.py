"""Reconcile 11-archive-proposal.md financial + syndicate claims against the 300-claim dataset."""
import csv, io, collections, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = list(csv.DictReader(io.StringIO(
    open("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv", "rb").read().decode("utf-8-sig"))))
def f(x):
    return float(x)
tot = sum(int(f(r["biaya_rp"])) for r in rows)
print("total nominal:", f"{tot:,}")
fraud = [r for r in rows if r["is_fraud"].strip() in ("1", "1.0", "True", "true")]
print("is_fraud rows:", len(fraud), "nominal:", f"{sum(int(f(r['biaya_rp'])) for r in fraud):,}")
by_status = collections.defaultdict(lambda: [0, 0])
for r in rows:
    s = r["status"]
    by_status[s][0] += 1
    by_status[s][1] += int(f(r["biaya_rp"]))
print("status breakdown:")
for s, (n, v) in sorted(by_status.items()):
    print(f"   {s:14s} n={n:3d} nominal={v:,}")
nac = [r for r in rows if r["status"] != "auto_clear"]
print("non-auto_clear:", len(nac), "nominal:", f"{sum(int(f(r['biaya_rp'])) for r in nac):,}")
tgt = 507_370_000
print(f"target {tgt:,} = {tgt/ sum(int(f(r['biaya_rp'])) for r in nac):.4%} of non-auto_clear nominal")
print(f"target/60 = {tgt/60:,.0f}   target/36 = {tgt/36:,.0f}")

print("\n=== syndicate breakdown ===")
syn = collections.defaultdict(lambda: [0, 0])
for r in rows:
    s = r["sindikat"]
    if s and s.lower() not in ("none", "-", ""):
        syn[s][0] += 1
        syn[s][1] += int(f(r["biaya_rp"]))
for s, (n, v) in sorted(syn.items()):
    print(f"   {s:10s} n={n:3d} nominal={v:,}")
print("claims with is_fraud=1 but sindikat none/none:",
      sum(1 for r in fraud if not r["sindikat"] or r["sindikat"].lower() in ("none", "-")))
tot_synd = sum(v[0] for v in syn.values())
tot_synd_val = sum(v[1] for v in syn.values())
print(f"total sindikat-covered: n={tot_synd} ({tot_synd/len(fraud):.1%} of 36 fraud) nominal={tot_synd_val:,}")

print("\n=== modus breakdown (fraud only) ===")
md = collections.defaultdict(lambda: [0, 0])
for r in fraud:
    md[r["modus"]][0] += 1
    md[r["modus"]][1] += int(f(r["biaya_rp"]))
for s, (n, v) in sorted(md.items(), key=lambda kv: -kv[1][1]):
    print(f"   {s:22s} n={n:3d} nominal={v:,}")
