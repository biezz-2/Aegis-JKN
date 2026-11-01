import csv, json, os, statistics, collections
D = r"N:\HEALTHKATHON"
CSV = os.path.join(D, "analysis", "corpus", "claims_v2_live.csv")
rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
def f(x):
    try: return float(x)
    except: return None
print("=== 1. Circular benchmark check (Skor Fraud vs Risiko) ===")
byrisk = collections.defaultdict(list)
for r in rows:
    byrisk[r["Risiko"]].append(float(r["Skor Fraud"]))
for k,v in byrisk.items():
    print(f"  Risiko={k!r:12} n={len(v):3} min={min(v):.4f} max={max(v):.4f} mean={statistics.mean(v):.4f}")
print("  Status counts:", dict(collections.Counter(r["Status"] for r in rows)))
print("  Risiko counts:", dict(collections.Counter(r["Risiko"] for r in rows)))
byst = collections.defaultdict(list)
for r in rows: byst[r["Status"]].append(float(r["Skor Fraud"]))
print("  mean Skor Fraud per Status:")
for k,v in sorted(byst.items()): print(f"    {k:12} n={len(v):3} mean={statistics.mean(v):.4f}")
# separability
fr = [float(r["Skor Fraud"]) for r in rows if r["Risiko"]=="fraud"]
nf = [float(r["Skor Fraud"]) for r in rows if r["Risiko"]!="fraud"]
print(f"  fraud n={len(fr)} range {min(fr):.2f}-{max(fr):.2f}; nonfraud n={len(nf)} range {min(nf):.2f}-{max(nf):.2f}")
print(f"  overlap: max(nonfraud)={max(nf):.4f} >= min(fraud)={min(fr):.4f} ? {max(nf)>=min(fr)}")
# AUC by score
pairs = sum((1 if a>b else 0.5 if a==b else 0) for a in fr for b in nf)
print(f"  AUC(Skor Fraud as predictor of Risiko==fraud) = {pairs/(len(fr)*len(nf)):.6f}")
# threshold 0.80
tp=sum(1 for r in rows if r["Risiko"]=="fraud" and float(r["Skor Fraud"])>=0.80)
fp=sum(1 for r in rows if r["Risiko"]!="fraud" and float(r["Skor Fraud"])>=0.80)
fn=sum(1 for r in rows if r["Risiko"]=="fraud" and float(r["Skor Fraud"])<0.80)
tn=len(rows)-tp-fp-fn
print(f"  @thr0.80 tp={tp} fp={fp} fn={fn} tn={tn} precision={tp/max(1,tp+fp):.4f} recall={tp/max(1,tp+fn):.4f}")

print("\n=== 2. Dataset totals ===")
tot = sum(f(r["Biaya Rp"]) or 0 for r in rows)
print("  total Biaya Rp:", f"{tot:,.0f}".replace(",","."))
bys = collections.defaultdict(float); bysn=collections.Counter()
for r in rows: bys[r["Status"]] += f(r["Biaya Rp"]) or 0; bysn[r["Status"]]+=1
for k in bys: print(f"    {k:12} n={bysn[k]:3} Rp{bys[k]:,.0f}".replace(",","."))
print(" Rp3,53 Miliar?", abs(tot-3_530_000_000) < 30_000_000, " actual:", f"{tot:,.0f}".replace(",","."))
print("  Rp841,10 Juta (escalate+review)?", f"{bys['escalate']+bys['review']:,.0f}".replace(",","."))
print("  fraud count by Risiko:", dict(collections.Counter(r["Risiko"] for r in rows)))
print("  anomaly=fraud+tinggi?", sum(1 for r in rows if r["Risiko"] in ("fraud","tinggi")))
print("  Kontradiksi Narasi True:", sum(1 for r in rows if r["Kontradiksi Narasi"].strip().lower() in ("true","yes","1")))
print("  Sentimen counts:", dict(collections.Counter(r["Sentimen"] for r in rows)))
print("  Layanan counts:", dict(collections.Counter(r["Layanan"] for r in rows)))
