import csv, os, json, statistics, itertools
from collections import defaultdict
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
rows=list(csv.DictReader(open(V21,encoding="utf-8-sig",newline="")))
def N(s): return int(float(s))
ESC=394950000; REV=112420000
keyfns={
 "layanan":lambda r:r["layanan"],
 "faskes":lambda r:r["faskes_id"],
 "dx":lambda r:r["diagnosis_code"],
 "proc":lambda r:r["prosedur_code"],
 "dxproc":lambda r:(r["diagnosis_code"],r["prosedur_code"]),
 "faskes_layanan":lambda r:(r["faskes_id"],r["layanan"]),
 "layanan_los":lambda r:(r["layanan"],r["los_hari"]),
 "faskes_dx":lambda r:(r["faskes_id"],r["diagnosis_code"]),
 "faskes_los":lambda r:(r["faskes_id"],r["los_hari"]),
 "los":lambda r:r["los_hari"],
 "dokter":lambda r:r["dokter_id"],
 "dx_los":lambda r:(r["diagnosis_code"],r["los_hari"]),
 "sent":lambda r:r["sentimen"],
 "faskes_proc":lambda r:(r["faskes_id"],r["prosedur_code"]),
 "global":lambda r:"ALL",
}
pools={"nonfraud":[r for r in rows if r["is_fraud"].strip()!="1"],
       "autoclear":[r for r in rows if r["status"]=="auto_clear"],
       "all":rows}
aggs={"median":statistics.median,"mean":statistics.fmean,"min":min,"max":max}
results=[]
for pname,pool in pools.items():
    for kname,kf in keyfns.items():
        g=defaultdict(list)
        for r in pool: g[kf(r)].append(N(r["biaya_rp"]))
        for aname,agg in aggs.items():
            ref={k:agg(v) for k,v in g.items()}
            for floor0 in (False,True):
                for grp,target in (("escalate",ESC),("review",REV)):
                    sel=[r for r in rows if r["status"]==grp]
                    s=0; ok=True
                    for r in sel:
                        k=kf(r)
                        if k not in ref: ok=False; break
                        v=N(r["biaya_rp"])-ref[k]
                        s+= max(0,v) if floor0 else v
                    if ok:
                        results.append([pname,kname,aname,floor0,grp,round(s,2),s==target])
hits=[r for r in results if r[6]]
print("EXACT HITS:", json.dumps(hits,ensure_ascii=False))
results.sort(key=lambda r: abs(r[5]-(ESC if r[4]=="escalate" else REV)))
print("closest 12:")
for r in results[:12]: print(" ",r)
json.dump({"exact":hits,"all":results},open("out_brute.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
