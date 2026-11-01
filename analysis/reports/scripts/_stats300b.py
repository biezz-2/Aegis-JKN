import csv, collections, hashlib, io
p = "N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv"
raw = open(p,'rb').read()
print("sha256 nb-embedded:", hashlib.sha256(raw).hexdigest())
for q in ["N:/HEALTHKATHON/analysis/corpus/claims_v2_live.csv",
          "N:/HEALTHKATHON/mechine-learning-deep-learning/datasets/claims_300_v2.1.csv"]:
    try:
        r = open(q,'rb').read()
        print("sha256", q, hashlib.sha256(r).hexdigest(), len(r), "bytes")
    except Exception as e:
        print("MISSING", q, e)

rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
def vc(col):
    c = collections.Counter(r[col] for r in rows)
    print(f"\n-- {col} ({len(c)} distinct)")
    for k,v in c.most_common(20): print(f"   {k!r}: {v}")
for col in ["is_fraud","status","risiko","sindikat","modus","sentiment","layanan","kontradiksi_narasi"]:
    vc(col)
tot = sum(float(r['biaya_rp'] or 0) for r in rows)
print("\ntotal biaya_rp:", f"{tot:,.0f}")
print("ids:", rows[0]['claim_id'], "...", rows[-1]['claim_id'])
# cross tab sindikat x is_fraud
ct = collections.Counter((r['sindikat'], r['is_fraud']) for r in rows)
print("\nsindikat x is_fraud:")
for k in sorted(ct): print("  ", k, ct[k])
# status x nominal
bynom = collections.defaultdict(float); bycnt = collections.Counter()
for r in rows:
    bynom[r['status']] += float(r['biaya_rp'] or 0); bycnt[r['status']] += 1
print("\nnominal per status:")
for s in bynom: print(f"   {s}: n={bycnt[s]} nominal={bynom[s]:,.0f}")
