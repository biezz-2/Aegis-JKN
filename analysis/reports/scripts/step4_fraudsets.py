import csv, json, os
from collections import Counter, defaultdict
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
def load(p):
    with open(p,"r",encoding="utf-8-sig",newline="") as f:
        r=csv.DictReader(f); return list(r)
vr=load(V21)
def num(s):
    s=(s or "").strip()
    try: return float(s) if "." in s else int(s)
    except: return None
A={r["claim_id"] for r in vr if r["is_fraud"].strip()=="1"}
B={r["claim_id"] for r in vr if r["risiko"].strip()=="fraud"}
C={r["claim_id"] for r in vr if r["sindikat"].strip() not in ("none","")}
out={}
out["A_eq_B"]=A==B
out["A_only"]=sorted(A-B); out["B_only"]=sorted(B-A)
out["A_eq_C"]=A==C; out["A_minus_C"]=sorted(A-C); out["C_minus_A"]=sorted(C-A)
out["B_eq_C"]=B==C; out["B_minus_C"]=sorted(B-C); out["C_minus_B"]=sorted(C-B)
# cross-tab
ct=Counter((r["is_fraud"].strip(), r["risiko"].strip(), r["status"].strip(), "SYND" if r["sindikat"].strip() not in ("none","") else "NOSYND") for r in vr)
out["crosstab"]={"|".join(k):v for k,v in sorted(ct.items())}
# detail of mismatches
mm=[r for r in vr if r["claim_id"] in (A^C) | (B^C)]
out["mismatch_rows"]=[{k:r[k] for k in ("claim_id","status","risiko","is_fraud","sindikat","modus","skor_fraud","biaya_rp")} for r in mm]
# what combination yields 507.370.000 ?
tot=sum(num(r["biaya_rp"]) for r in vr)
def sumset(ids): return sum(num(r["biaya_rp"]) for r in vr if r["claim_id"] in ids)
out["tot"]=tot
out["esc_total"]=sumset({r["claim_id"] for r in vr if r["status"]=="escalate"})
out["rev_total"]=sumset({r["claim_id"] for r in vr if r["status"]=="review"})
out["esc_rev_total"]=out["esc_total"]+out["rev_total"]
out["risiko_high_total"]=sumset({r["claim_id"] for r in vr if r["risiko"]=="high"})
out["risiko_fraud_high_total"]=sumset({r["claim_id"] for r in vr if r["risiko"] in ("fraud","high")})
out["nonlow_total"]=out["risiko_fraud_high_total"]
out["n_risiko_fraud_high"]=len({r["claim_id"] for r in vr if r["risiko"] in ("fraud","high")})
out["n_medi_high"]=len({r["claim_id"] for r in vr if r["risiko"] in ("medium","high")})
out["medi_high_total"]=sumset({r["claim_id"] for r in vr if r["risiko"] in ("medium","high")})
out["syndikat_total"]=sumset(C)
out["n_syndikat"]=len(C)
# is there a subset summing to 507.370.000? check escalate+review minus something
out["esc_rev_minus"]=out["esc_rev_total"]-out["esc_rev_total"]
# check 507.370.000 combos: median-based estimate? "overcharge" 507.370.000
target=507370000
out["target"]=target
out["esc_rev_minus_target"]=out["esc_rev_total"]-target
out["esc_minus_target"]=out["esc_total"]-target
# overcharge: maybe fraud_total - a "fair" reference? Try: sum of fraud biaya minus (mean biaya of matching non-fraud claims * 36)
import statistics
nonfraud_mean=statistics.mean([num(r["biaya_rp"]) for r in vr if r["is_fraud"].strip()!="1"])
out["nonfraud_mean_biaya"]=round(nonfraud_mean,2)
out["fraud_mean_biaya"]=round(statistics.mean([num(r["biaya_rp"]) for r in vr if r["is_fraud"].strip()=="1"]),2)
out["fraud_sum"]=out["esc_total"]
out["fraud_minus_nonfraudmean_x36"]=out["esc_total"]-nonfraud_mean*36
# look for combos of modus groups within escalate summing to 507.37
mods=defaultdict(list)
for r in vr:
    if r["status"]=="escalate": mods[r["modus"].strip()].append(r)
out["esc_modus_totals"]={k:sum(num(x["biaya_rp"]) for x in v) for k,v in mods.items()}
out["esc_modus_n"]={k:len(v) for k,v in mods.items()}
# Any subset of modus groups summing to 507370000?
ks=list(out["esc_modus_totals"]); import itertools
hits=[]
for n in range(1,len(ks)+1):
    for comb in itertools.combinations(ks,n):
        s=sum(out["esc_modus_totals"][k] for k in comb)
        if abs(s-target)<1: hits.append([comb,s])
out["modus_subset_exact_507370000"]=hits
# median-based: for each fraud claim, overcharge = biaya - median biaya of same layanan non-fraud
med_lay=defaultdict(list)
for r in vr:
    if r["is_fraud"].strip()!="1": med_lay[r["layanan"].strip()].append(num(r["biaya_rp"]))
over=0; over2=0
for r in vr:
    if r["is_fraud"].strip()=="1":
        m=statistics.median(med_lay[r["layanan"].strip()])
        over+=num(r["biaya_rp"])-m
        over2+=max(0, num(r["biaya_rp"])-m)
out["overcharge_median_by_layanan"]=round(over,2)
out["overcharge_median_by_layanan_floor0"]=round(over2,2)
med_all=statistics.median([num(r["biaya_rp"]) for r in vr])
out["overcharge_vs_global_median"]=round(sum(num(r["biaya_rp"])-med_all for r in vr if r["is_fraud"].strip()=="1"),2)
out["global_median_biaya"]=med_all
# ratio check
out["ratio_36_264"]=264/36
out["ratio_pct_36"]=100*36/300
out["507370000_div_60"]=507370000/60
out["507370000_div_36"]=507370000/36
out["841100000_div_60"]=841100000/60
out["841100000_div_36"]=841100000/36
# 36*avg
out["esc_avg_biaya"]=round(out["esc_total"]/36,2)
out["esc_rev_avg_biaya"]=round(out["esc_rev_total"]/60,2)
with open(os.path.join(BASE,r"analysis\reports\scripts\out_fraudsets.json"),"w",encoding="utf-8") as f:
    json.dump(out,f,ensure_ascii=False,indent=1)
print("OK")
