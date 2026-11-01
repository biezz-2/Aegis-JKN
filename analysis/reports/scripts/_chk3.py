import csv, sys, io, collections
sys.stdout = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_chk3.out", "w", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.DictReader(open(r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv", encoding="utf-8")))
m = collections.defaultdict(collections.Counter)
for r in rows:
    if r["Modus"].strip():
        m[r["Modus"]][r["Sentimen"]] += 1
for k, v in sorted(m.items()):
    tot = sum(v.values())
    parts = ", ".join(f"{lab} {n}/{tot}" for lab, n in sorted(v.items()))
    print(f"{k:24} {parts}  -> {'MONOTON' if len(v)==1 else 'MULTI'}")

print("\n--- normal rows by label ---")
n = collections.Counter(r["Sentimen"] for r in rows if not r["Modus"].strip())
print(n, "total", sum(n.values()))

print("\n--- skor sentimen unique/singleton ---")
sc = collections.Counter(r["Skor Sentimen"] for r in rows)
print("unique values:", len(sc))
print("rows sharing a repeated value:", sum(c for c in sc.values() if c > 1))
print("singleton values:", sum(1 for c in sc.values() if c == 1))
print("min/max:", min(float(x) for x in sc), max(float(x) for x in sc))
print("nilai 0:", sc.get("0.00", sc.get("0", 0)))

print("\n--- label range ---")
by = collections.defaultdict(list)
for r in rows:
    by[r["Sentimen"]].append(float(r["Skor Sentimen"]))
for k, v in by.items():
    print(f"{k:9} n={len(v):4} min={min(v):+.2f} max={max(v):+.2f} mean={sum(v)/len(v):+.4f}")

print("\n--- positive-labelled high risk ---")
print([r["Name"] for r in rows if r["Sentimen"] == "positif" and r["Risiko"] == "high"])
print("--- sentimen x risiko ---")
t = collections.Counter((r["Sentimen"], r["Risiko"]) for r in rows)
for s in ("positif", "netral", "negatif"):
    print(s, {k: t[(s, k)] for k in ("low", "medium", "high", "fraud")})
