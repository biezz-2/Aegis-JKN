import csv, json, os, itertools
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
def load(p):
    with open(p,"r",encoding="utf-8-sig",newline="") as f:
        r=csv.DictReader(f); return list(r)
vr=load(V21)
def num(s):
    s=(s or "").strip()
    try: return int(float(s))
    except: return 0
target=507370000
def search(rows, label):
    vals=[(r["claim_id"], num(r["biaya_rp"]), r["status"], r["modus"], r["sindikat"]) for r in rows]
    # DP over sums / 1000
    G=1000
    tg=target//G
    reach={0:[]}
    for cid,b,st,mo,sy in vals:
        if b%G: continue
        bk=b//G
        new={}
        for s,path in reach.items():
            ns=s+bk
            if ns<=tg and ns not in reach and ns not in new:
                new[ns]=path+[(cid,b,st,mo,sy)]
        reach.update(new)
    if tg in reach:
        return reach[tg]
    return None
esc=[r for r in vr if r["status"]=="escalate"]
hit=search(esc,"escalate")
res={"escalate_subset_for_507370000": hit}
if not hit:
    hit2=search(vr,"all")
    res["all300_subset_for_507370000"]=hit2
print(json.dumps(res,ensure_ascii=False,indent=1))
with open(os.path.join(BASE,r"analysis\reports\scripts\out_subset.json"),"w",encoding="utf-8") as f:
    json.dump(res,f,ensure_ascii=False,indent=1)
