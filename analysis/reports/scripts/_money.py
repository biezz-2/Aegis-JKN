"""Money + provenance checks, split into fast parts (no O(n^3) subset search)."""
import csv, io, collections, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = "N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv"
rows = list(csv.DictReader(io.StringIO(open(P, "rb").read().decode("utf-8-sig"))))


def num(x):
    try:
        return float(x)
    except Exception:
        return 0.0


tot = sum(num(r["biaya_rp"]) for r in rows)
fraud = [r for r in rows if r["is_fraud"] == "1"]
esc = [r for r in rows if r["status"] == "escalate"]
rev = [r for r in rows if r["status"] == "review"]
TARGET = 507_370_000

print(f"total nominal all 300 = {tot:,.0f}")
print(f"is_fraud=1  n={len(fraud):3d} nominal={sum(num(r['biaya_rp']) for r in fraud):,.0f}")
print(f"escalate    n={len(esc):3d} nominal={sum(num(r['biaya_rp']) for r in esc):,.0f}")
print(f"review      n={len(rev):3d} nominal={sum(num(r['biaya_rp']) for r in rev):,.0f}")
print(f"\ntarget overcharge = {TARGET:,}")
for label, subset in (("fraud", fraud), ("escalate", esc), ("review", rev),
                       ("review+escalate", rev + esc),
                       ("risiko!=low", [r for r in rows if r["risiko"] != "low"]),
                       ("auto_clear", [r for r in rows if r["status"] == "auto_clear"])):
    v = sum(num(r["biaya_rp"]) for r in subset)
    print(f"   nominal {label:16s} n={len(subset):3d} = {v:,.0f}  diff = {v-TARGET:,.0f}")

costs = [num(r["biaya_rp"]) for r in fraud]
print(f"\nfraud nominal mean = {sum(costs)/len(costs):,.0f}   (proposal claims Rp8,46M per case)")
print(f"60 x 8.46M = {60*8_460_000:,}   target/60 = {TARGET/60:,.0f}   "
      f"target/36 = {TARGET/36:,.0f}   target/24 = {TARGET/24:,.0f}")

print("\nmodus of is_fraud=1 claims:")
for k, v in collections.Counter(r["modus"] for r in fraud).most_common():
    sub = [r for r in fraud if r["modus"] == k]
    print(f"   {k:22s} n={v:2d} nominal={sum(num(r['biaya_rp']) for r in sub):,.0f}")

# how many claims would need to sum to the target at all?
srt = sorted((num(r["biaya_rp"]) for r in rows), reverse=True)
print(f"\nmax single claim = {srt[0]:,.0f}; "
      f"min #claims to reach target (greedy) = "
      f"{next(i+1 for i in range(len(srt)) if sum(srt[:i+1]) >= TARGET)}")
print("proposal claims 60 klaim anomali -> Rp507,37M; dataset has "
      f"{len(fraud)} fraud + {len(rev)} review = {len(fraud)+len(rev)} non-auto_clear claims")

print("\n=== provenance search (text files only) ===")
roots = [r"N:/HEALTHKATHON/mechine-learning-deep-learning",
         r"N:/HEALTHKATHON/analysis/corpus",
         r"N:/HEALTHKATHON/Aegis-JKN/src",
         r"N:/HEALTHKATHON/Aegis-JKN/docs"]
pats = ["masking", "kamuflase", "camouflage", "throughput", "sus ", "3,2", "3.2x", "45%"]
hits = collections.defaultdict(list)
for root in roots:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", "node_modules", ".next", "__pycache__", "work22")]
        for fn in filenames:
            if not fn.endswith((".py", ".md", ".ipynb", ".ts", ".tsx", ".json", ".html", ".txt", ".csv")):
                continue
            fp = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(fp) > 6_000_000:
                    continue
                t = open(fp, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            low = t.lower()
            for p in pats:
                idx = low.find(p.lower())
                if idx >= 0:
                    hits[p].append((fp, t[max(0, idx - 100):idx + 100].replace("\n", " ")))
for p in pats:
    print(f"\n### {p}: {len(hits.get(p, []))} file(s)")
    for fp, ctx in hits.get(p, [])[:6]:
        print(f"   {fp}\n      ...{ctx}...")
