import csv, os, json, statistics, itertools
from collections import defaultdict
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
rows=list(csv.DictReader(open(V21,encoding="utf-8-sig",newline="")))
def N(s): return int(float(s))
nonfraud=[r for r in rows if r["is_fraud"].strip()!="1"]
def refs():
    d={}
    def build(keyfn, pool, agg):
        g=defaultdict(list)
        for r in pool: g[keyfn(r)].append(N(r["biaya_rp"]))
        return {k:agg(v) for k,v in g.items()}
    for name,keyfn in [("layanan",lambda r:r["layanan"]),("faskes",lambda r:r["faskes_id"]),
                        ("dx",lambda r:r["diagnosis_code"]),("proc",lambda r:r["prosedur_code"]),
                        ("dxproc",lambda r:(r["diagnosis_code"],r["prosedur_code"])),
                        ("faskes_layanan",lambda r:(r["faskes_id"],r["layanan"])),
                        ("layanan_los",lambda r:(r["layanan"],r["los_hari"]))]:
        for aggname,agg in [("median",statistics.median),("mean",statistics.fmean)]:
            d[f"{name}_{aggname}"]=build(keyfn,nonfraud,agg)
    return d
R=refs()
res={}
for grp,target in (("escalate",394950000),("review",112420000)):
    sel=[r for r in rows if r["status"]==grp]
    hits=[]
    for name,m in R.items():
        for floor0 in (False,True):
            s=0; ok=True
            for r in sel:
                k=r["layanan"] if name=="layanan" else r["faskes_id"] if name=="faskes" else r["diagnosis_code"] if name=="dx" else r["prosedur_code"] if name=="proc" else (r["diagnosis_code"],r["prosedur_code"]) if name=="dxproc" else (r["faskes_id"],r["layanan"]) if name=="faskes_layanan" else (r["layanan"],r["los_hari"])
                if k not in m: ok=False; break
                v=N(r["biaya_rp"])-m[k]
                s+= max(0,v) if floor0 else v
            if ok: hits.append([name, floor0, round(s,2), abs(s-target)])
    hits.sort(key=lambda x:x[3])
    res[grp]={"target":target,"best":hits[:6]}
# global median of nonfraud
gm=statistics.median([N(r["biaya_rp"]) for r in nonfraud])
gmean=statistics.fmean([N(r["biaya_rp"]) for r in nonfraud])
res["global_median_nonfraud"]=gm; res["global_mean_nonfraud"]=round(gmean,2)
for grp,target in (("escalate",394950000),("review",112420000)):
    sel=[r for r in rows if r["status"]==grp]
    res[grp]["global_median"]=round(sum(N(r["biaya_rp"])-gm for r in sel),2)
    res[grp]["global_mean"]=round(sum(N(r["biaya_rp"])-gmean for r in sel),2)
    res[grp]["global_median_floor0"]=round(sum(max(0,N(r["biaya_rp"])-gm) for r in sel),2)
    # per-row: 30% haircut (i.e. 70% of biaya is fair) -> overcharge = 0.3*biaya
    res[grp]["haircut30"]=round(sum(0.3*N(r["biaya_rp"]) for r in sel),2)
    res[grp]["haircut40"]=round(sum(0.4*N(r["biaya_rp"]) for r in sel),2)
    res[grp]["haircut396"]=round(sum(0.396*N(r["biaya_rp"]) for r in sel),2)
    res[grp]["haircut4016"]=round(sum(0.4016*N(r["biaya_rp"]) for r in sel),2)
    res[grp]["total"]=sum(N(r["biaya_rp"]) for r in sel)
    res[grp]["n"]=len(sel)
    res[grp]["implied_ratio"]=round(target/sum(N(r["biaya_rp"]) for r in sel),6)
print(json.dumps(res,ensure_ascii=False,indent=1))
json.dump(res,open("out_ref.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
