import csv, os, json, statistics, itertools
from collections import defaultdict
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
rows=list(csv.DictReader(open(V21,encoding="utf-8-sig",newline="")))
def N(s): return int(float(s))
out={}
esc=[r for r in rows if r["status"]=="escalate"]; rev=[r for r in rows if r["status"]=="review"]
out["upcoding_esc"]=[(r["claim_id"],r["status"],N(r["biaya_rp"])) for r in rows if r["modus"].strip()=="upcoding"]
out["review_upcoding_sum"]=sum(N(r["biaya_rp"]) for r in rev if r["modus"].strip()=="upcoding")
out["esc_upcoding_sum"]=sum(N(r["biaya_rp"]) for r in esc if r["modus"].strip()=="upcoding")
out["upcoding_all_sum"]=sum(N(r["biaya_rp"]) for r in rows if r["modus"].strip()=="upcoding")
out["target_upcoding_127680000"]=127680000
# subset-sum for upcoding (all 5) to 127680000
def subset(vals, target):
    G=1000; tg=target//G; reach={0:[]}
    for cid,b in vals:
        if b%G: continue
        bk=b//G; new={}
        for s,p in reach.items():
            ns=s+bk
            if ns<=tg and ns not in reach and ns not in new: new[ns]=p+[(cid,b)]
        reach.update(new)
        if tg in reach: return reach[tg]
    return None
up=[(r["claim_id"],N(r["biaya_rp"])) for r in rows if r["modus"].strip()=="upcoding"]
out["upcoding_subset_127680000"]=subset(up,127680000)
# battery of formulas for escalate overcharge
def try_formulas(sel,label):
    res={}
    nonfraud=[r for r in rows if r["is_fraud"].strip()!="1"]
    # per-claim reference candidates
    med_lay=defaultdict(list); med_dx=defaultdict(list); med_dxproc=defaultdict(list)
    for r in nonfraud:
        med_lay[r["layanan"]].append(N(r["biaya_rp"]))
        med_dx[r["diagnosis_code"]].append(N(r["biaya_rp"]))
        med_dxproc[(r["diagnosis_code"],r["prosedur_code"])].append(N(r["biaya_rp"]))
    gm=statistics.median([N(r["biaya_rp"]) for r in nonfraud])
    def acc(ref_fn, floor0=False, factor=1.0):
        s=0
        for r in sel:
            ref=ref_fn(r)
            if ref is None: continue
            d=N(r["biaya_rp"])-ref
            s+= max(0,d) if floor0 else d
        return round(factor*s,2)
    res["median_layanan"]=acc(lambda r: statistics.median(med_lay[r["layanan"]]))
    res["median_layanan_floor0"]=acc(lambda r: statistics.median(med_lay[r["layanan"]]),True)
    res["median_dx"]=acc(lambda r: statistics.median(med_dx[r["diagnosis_code"]]) if med_dx[r["diagnosis_code"]] else None)
    res["median_dx_floor0"]=acc(lambda r: statistics.median(med_dx[r["diagnosis_code"]]) if med_dx[r["diagnosis_code"]] else None,True)
    res["global_median"]=acc(lambda r: gm)
    res["global_median_floor0"]=acc(lambda r: gm,True)
    res["frac70"]=round(0.7*sum(N(r["biaya_rp"]) for r in sel),2)
    res["frac7032"]=round(0.7032*sum(N(r["biaya_rp"]) for r in sel),2)
    res["frac7029"]=round(0.7029*sum(N(r["biaya_rp"]) for r in sel),2)
    res["total"]=sum(N(r["biaya_rp"]) for r in sel)
    res["n"]=len(sel)
    return res
out["formulas_escalate"]=try_formulas(esc,"esc")
out["formulas_review"]=try_formulas(rev,"rev")
out["target_escalate"]=394950000; out["target_review"]=112420000
out["ratio_6032_total"]=round(507370000/841100000,6)
out["sindikat_36_biaya"]=sum(N(r["biaya_rp"]) for r in rows if r["sindikat"].strip() not in ("none",""))
out["proposal_syndikat_542560000"]=542560000
out["diff_syndikat"]=542560000-out["sindikat_36_biaya"]
# 60% of 36 = 21.6 ; 36/60
out["36_of_60"]=60.0
out["36_of_36"]=100.0
# 8456167*60
out["8456167x60"]=8456167*60
out["8456167x36"]=8456167*36
out["507370000_over_841100000"]=507370000/841100000
# 127,68 jt upcoding vs 156.9
out["upcoding_diff"]=156900000-127680000
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open("out_decomp.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
