import csv, os, json, statistics, itertools
from collections import defaultdict
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
rows=list(csv.DictReader(open(V21,encoding="utf-8-sig",newline="")))
def N(s): return int(float(s))
out={}
# modus totals across ALL 60 anomaly rows (escalate+review) and per modus
by_modus=defaultdict(lambda: {"n":0,"biaya":0,"ids":[]})
for r in rows:
    if r["status"] in ("escalate","review"):
        m=r["modus"].strip()
        by_modus[m]["n"]+=1; by_modus[m]["biaya"]+=N(r["biaya_rp"]); by_modus[m]["ids"].append(r["claim_id"])
out["modus_anom60"]={k:{"n":v["n"],"biaya":v["biaya"]} for k,v in sorted(by_modus.items())}
# median-based overcharge, split by status
for grp in ("escalate","review"):
    nf=defaultdict(list)
    for r in rows:
        if r["status"]!=grp and r["is_fraud"].strip()!="1": nf[r["layanan"].strip()].append(N(r["biaya_rp"]))
    s=0; s2=0
    for r in rows:
        if r["status"]==grp:
            m=statistics.median(nf[r["layanan"].strip()])
            s+=N(r["biaya_rp"])-m; s2+=max(0,N(r["biaya_rp"])-m)
    out[f"overcharge_median_layanan_{grp}"]=round(s,2)
    out[f"overcharge_median_layanan_floor0_{grp}"]=round(s2,2)
    # vs global median of all non-fraud
    allnf=[N(r["biaya_rp"]) for r in rows if r["is_fraud"].strip()!="1"]
    gm=statistics.median(allnf)
    out[f"overcharge_globalmedian_{grp}"]=round(sum(N(r["biaya_rp"])-gm for r in rows if r["status"]==grp),2)
    # vs 0.7 factor
    out[f"frac70_{grp}"]=round(0.7*sum(N(r["biaya_rp"]) for r in rows if r["status"]==grp),2)
    out[f"frac7032_{grp}"]=round(0.7032*sum(N(r["biaya_rp"]) for r in rows if r["status"]==grp),2)
    tot=sum(N(r["biaya_rp"]) for r in rows if r["status"]==grp)
    out[f"total_{grp}"]=tot
    out[f"target_{grp}"]= 394950000 if grp=="escalate" else 112420000
    out[f"ratio_{grp}"]=round((394950000 if grp=="escalate" else 112420000)/tot,6)
# subset sum within escalate for 394950000 and within review for 112420000 (all sizes)
def subset(rows_sel, target):
    vals=[(r["claim_id"],N(r["biaya_rp"])) for r in rows_sel]
    G=1000; tg=target//G
    reach={0:[]}
    for cid,b in vals:
        if b%G: continue
        bk=b//G; new={}
        for s,path in reach.items():
            ns=s+bk
            if ns<=tg and ns not in reach and ns not in new: new[ns]=path+[(cid,b)]
        reach.update(new)
        if tg in reach: return reach[tg]
    return None
esc=[r for r in rows if r["status"]=="escalate"]
rev=[r for r in rows if r["status"]=="review"]
out["esc_subset_394950000"]=subset(esc,394950000)
out["rev_subset_112420000"]=subset(rev,112420000)
# Upcoding: proposal says 127.68 jt
out["upcoding_all_anom"]=by_modus["upcoding"]["biaya"]
out["upcoding_all_ids"]=by_modus["upcoding"]["ids"]
out["upcoding_all_biaya_list"]=[ (r["claim_id"],r["status"],N(r["biaya_rp"])) for r in rows if r["modus"].strip()=="upcoding"]
# phantom billing all
out["phantom_all"]=by_modus["phantom_billing"]["biaya"]
out["repeat_all"]=by_modus["repeat_billing"]["biaya"]
# syndicate totals
syn=defaultdict(int)
for r in rows:
    if r["sindikat"].strip() not in ("none",""): syn[r["sindikat"].strip()]+=N(r["biaya_rp"])
out["syndikat_totals"]=dict(sorted(syn.items()))
out["syndikat_sum"]=sum(syn.values())
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open("out_over.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
