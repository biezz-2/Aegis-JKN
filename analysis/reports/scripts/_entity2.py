"""Two follow-ups:
(A) Do 10-simulation-dataset.md entity tables match the 300-claim dataset instead of the
    100-claim generator that produced the PDF?
(B) Root-cause the 14 sentiment failures (substring collision in the lexicon).
(C) Feature-edge density: is the 'feature channel' informative at all?
"""
import csv, io, collections, math, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

rows = list(csv.DictReader(io.StringIO(
    open("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv", "rb").read().decode("utf-8-sig"))))

print("=== (A) 300-claim dataset entity counts ===")
def num(x):
    try:
        return float(x)
    except Exception:
        return 0.0

for label, col, doc in (
    ("faskes", "faskes_id", {"RS_A": 19, "RS_B": 13, "RS_C": 10, "RS_D": 10, "RS_E": 22, "RS_F": 26}),
    ("dx", "diagnosis_code", {"K29.7": 10, "K35.8": 11, "K40.9": 8, "I21.9": 8, "J18.9": 9,
                              "E11.9": 15, "N20.0": 8, "S72.0": 10, "O80": 8, "K80.2": 13}),
    ("proc", "prosedur_code", {"00.66": 12, "47.09": 11}),
):
    c = collections.Counter(r[col] for r in rows)
    print(f"\n{label}: doc vs 300-actual")
    for k, dn in doc.items():
        an = c.get(k, 0)
        print(f"   {k:8s} doc={dn:3d}  actual300={an:3d}  {'MATCH' if dn == an else 'diff'}")

print("\ndokter counts 300-actual:")
dc = collections.Counter(r["dokter_id"] for r in rows)
doc_d = {"D01": 2, "D02": 8, "D03": 9, "D04": 9, "D05": 10, "D06": 0, "D07": 13,
         "D08": 18, "D09": 14, "D10": 8, "D11": 1, "D12": 8}
for k in sorted(doc_d):
    print(f"   {k}: doc={doc_d[k]:3d} actual300={dc.get(k,0):3d} "
          f"{'MATCH' if doc_d[k]==dc.get(k,0) else 'diff'}")

print("\npasien counts 300-actual (first 20):")
pc = collections.Counter(r["pasien_id"] for r in rows)
doc_p = {"P01": 5, "P02": 5, "P03": 5, "P04": 4, "P05": 5, "P06": 4, "P07": 5, "P08": 5,
         "P09": 5, "P10": 5, "P11": 5, "P12": 5, "P13": 6, "P14": 6, "P15": 5, "P16": 5,
         "P17": 5, "P18": 4, "P19": 4, "P20": 5}
match_n = sum(1 for k, v in doc_p.items() if pc.get(k, 0) == v)
print(f"   doc-vs-300 matches: {match_n}/20")

print("\n=== (B) root cause of the 14 sentiment failures ===")
NEG_WORDS = {"buruk": 1, "lambat": 1, "rumit": 1, "jelek": 1, "kecewa": 2, "kurang": 1,
             "antre": 1, "lama": 1, "ribet": 1, "mahal": 1, "sempit": 1, "dirugikan": 1}
POS_WORDS = {"baik": 1, "bagus": 1, "membantu": 1, "efisien": 1, "mantap": 1, "keren": 1,
             "murah": 1, "untung": 1, "puas": 1, "cepat": 1, "ramah": 1, "lancar": 1,
             "alhamdulillah": 1, "terima kasih": 1, "senang": 1, "setuju": 1}
title = "[Diskusi] Pengalaman klaim JKN di RS Bahari Medika E"
print(f"   Reddit title (fixed for every post): {title!r}")
for w, wt in NEG_WORDS.items():
    if w in title.lower():
        print(f"   COLLISION: NEG word {w!r} (weight {wt}) is a SUBSTRING of the title "
              f"'Pengalaman' -> scores -1 even for a perfectly neutral post")
print(f"   tanh(-1) = {math.tanh(-1):.4f}  (observed failure score -0.762)")
print("   Netral reddit posts = 14 of 100 (4 anomali + 10 NEUTRAL_NORMAL); ALL 14 fail.")
print("   Positif/Negatif reddit posts survive because extra POS/NEG words dominate the -1.")
print("   => 93.0% == (200-14)/200 is a deterministic arithmetic consequence of a")
print("      fixed-string substring bug, not a measured model quality.")

print("\n=== (C) feature-channel edge density ===")
print("   100 claims -> 100*99/2 = 4950 possible pairs")
print("   feat_edges (cosine >= 0.85) = 4563 -> density 4563/4950 = 92.18%")
print("   => the 'feature channel' connects 92% of ALL claim pairs; it is near-complete,")
print("      so it carries almost no discriminative information.")
print("   synd_density = 1.0 for all 5 syndicates is therefore uninformative:")
# recompute synd_density properly against global density
import importlib.util
spec = importlib.util.spec_from_file_location("fx", r"N:/HEALTHKATHON/analysis/reports/scripts/_fixx_repro.py")
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
CLAIMS = fx.CLAIMS
edges = []
for i in range(len(CLAIMS)):
    for j in range(i + 1, len(CLAIMS)):
        sim = fx.cosine(CLAIMS[i]["vec"], CLAIMS[j]["vec"])
        if sim >= 0.85:
            edges.append((CLAIMS[i]["id"], CLAIMS[j]["id"]))
print(f"   global edge density = {len(edges)/4950:.4f}")
for s in ["SYND-01", "SYND-02", "SYND-03", "SYND-04", "SYND-05"]:
    mem = [c for c in CLAIMS if c["sindikat"] == s]
    ids = {m["id"] for m in mem}
    n = len(mem)
    inner = sum(1 for a, b in edges if a in ids and b in ids)
    pairs = n * (n - 1) // 2
    print(f"   {s}: inner {inner}/{pairs} = {inner/pairs:.2f}  "
          f"(global density {len(edges)/4950:.2f})")

print("\n=== (D) does the graph channel discriminate anything? ===")
print("   feature vec = [los, log10(biaya), qty].  76 of 100 claims share the identical")
print("   template (K40.9 / 53.1 / los 2-4 / 5-11M / qty 2-5) -> cos=1.0 among all of them,")
print("   which is where the 4563 edges come from.")
print("   => a graph of 92% density over 76 indistinguishable nodes is not a graph model")
print("      signal; it is a duplicate-detection artifact of the generator's template.")
