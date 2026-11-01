import csv, os, statistics, re, collections
D = r"N:\HEALTHKATHON"
rows = list(csv.DictReader(open(os.path.join(D,"analysis","corpus","claims_v2_live.csv"), encoding="utf-8-sig")))
K="Kontribusi Saluran"
def parse(m): return [float(x.replace(",",".")) for x in re.findall(r"(\d+[.,]\d+)", m)]
sets = {
 "Risiko==fraud (36)": ([r for r in rows if r["Risiko"]=="fraud"], [r for r in rows if r["Risiko"]!="fraud"]),
 "Status anomali (60)": ([r for r in rows if r["Status"] in ("review","escalate")], [r for r in rows if r["Status"]=="auto_clear"]),
}
for lname,(pos,neg) in sets.items():
    print(f"\n--- {lname} ---")
    for idx,name in [(0,"T"),(1,"F"),(2,"S")]:
        pv=[parse(r[K])[idx] for r in pos if len(parse(r[K]))>=3]
        nv=[parse(r[K])[idx] for r in neg if len(parse(r[K]))>=3]
        print(f"  {name}: pos n={len(pv)} min={min(pv):.3f} mean={statistics.mean(pv):.4f} | neg n={len(nv)} max={max(nv):.3f} mean={statistics.mean(nv):.4f} | minpos>maxneg={min(pv)>max(nv)}")
        for t in [0.120,0.110,0.090]:
            tp=sum(1 for x in pv if x>=t); fp=sum(1 for x in nv if x>=t)
            if tp: print(f"      thr {t}: tp={tp} fp={fp} prec={tp/(tp+fp):.4f} rec={tp/len(pv):.4f}")
# check encoding of separator
print("\nraw sample repr:", repr(rows[0][K]))
print("\nunique Kontribusi Saluran strings:", len(set(r[K] for r in rows)))
print("distribution:", dict(collections.Counter(r[K] for r in rows).most_common(12)))
