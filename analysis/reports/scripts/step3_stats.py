import csv, json, os, statistics
from collections import Counter, defaultdict
BASE = r"N:\HEALTHKATHON"
LIVE = os.path.join(BASE, r"analysis\corpus\claims_v2_live.csv")
V21  = os.path.join(BASE, r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
OUT  = os.path.join(BASE, r"analysis\reports\scripts\out_stats.json")
def load(p):
    with open(p,"r",encoding="utf-8-sig",newline="") as f:
        r=csv.DictReader(f); return r.fieldnames,list(r)
_, lr = load(LIVE)
_, vr = load(V21)
R={}
def num(s):
    s=(s or "").strip()
    try: return float(s) if "." in s else int(s)
    except: return None

# --- v21 as canonical machine dataset ---
R["v21_n"]=len(vr)
ids=[r["claim_id"] for r in vr]
R["v21_id_min"]=min(ids); R["v21_id_max"]=max(ids)
R["v21_id_contiguous"]= (ids==[f"KLM{i:03d}" for i in range(1,301)])
R["v21_status"]=dict(Counter(r["status"].strip() for r in vr))
R["v21_risiko"]=dict(Counter(r["risiko"].strip() for r in vr))
R["v21_is_fraud"]=dict(Counter(r["is_fraud"].strip() for r in vr))
tot=sum(num(r["biaya_rp"]) for r in vr)
R["v21_total_biaya"]=tot
R["v21_total_biaya_human"]=f"{tot:,}".replace(",",".")
by_status=defaultdict(int); cnt_status=Counter()
for r in vr:
    by_status[r["status"].strip()]+=num(r["biaya_rp"]); cnt_status[r["status"].strip()]+=1
R["v21_biaya_by_status"]=dict(by_status)
R["v21_pct_status"]={k: round(100*cnt_status[k]/len(vr),4) for k in cnt_status}
R["v21_biaya_pct_status"]={k: round(100*by_status[k]/tot,4) for k in by_status}
by_risk=defaultdict(int)
for r in vr: by_risk[r["risiko"].strip()]+=num(r["biaya_rp"])
R["v21_biaya_by_risiko"]=dict(by_risk)

# three definitions of fraud
set_a={r["claim_id"] for r in vr if r["is_fraud"].strip()=="1"}
set_b={r["claim_id"] for r in vr if r["risiko"].strip()=="fraud"}
set_c={r["claim_id"] for r in vr if r["sindikat"].strip() not in ("none","")}
R["fraud_n_is_fraud"]=len(set_a); R["fraud_n_risiko_fraud"]=len(set_b); R["fraud_n_sindikat"]=len(set_c)
R["fraud_sets_identical"]= (set_a==set_b==set_c)
R["fraud_ids_sorted"]=sorted(set_a)
# status of fraud rows
R["fraud_status_counts"]=dict(Counter(r["status"].strip() for r in vr if r["claim_id"] in set_a))
R["review_ids_count"]=cnt_status["review"]
R["review_ids"]=sorted(r["claim_id"] for r in vr if r["status"].strip()=="review")
# escalate total
esc_ids={r["claim_id"] for r in vr if r["status"].strip()=="escalate"}
rev_ids=set(R["review_ids"])
R["escalate_n"]=len(esc_ids)
R["escalate_total"]=sum(num(r["biaya_rp"]) for r in vr if r["claim_id"] in esc_ids)
R["review_total"]=sum(num(r["biaya_rp"]) for r in vr if r["claim_id"] in rev_ids)
R["escalate_plus_review_n"]=len(esc_ids|rev_ids)
R["escalate_plus_review_total"]=sum(num(r["biaya_rp"]) for r in vr if r["claim_id"] in (esc_ids|rev_ids))
R["autoclear_total"]=sum(num(r["biaya_rp"]) for r in vr if r["status"].strip()=="auto_clear")
R["autoclear_n"]=cnt_status["auto_clear"]

# syndicate detail
syn=defaultdict(lambda: {"claims":0,"biaya":0,"faskes":set(),"pasien":set(),"dokter":set(),"status":Counter()})
for r in vr:
    s=r["sindikat"].strip()
    if s in ("none",""): continue
    d=syn[s]
    d["claims"]+=1; d["biaya"]+=num(r["biaya_rp"])
    d["faskes"].add(r["faskes_id"].strip())
    d["pasien"].add(r["pasien_id"].strip())
    d["dokter"].add(r["dokter_id"].strip())
    d["status"][r["status"].strip()]+=1
R["sindikat_detail"]={k:{"claims":v["claims"],"biaya":v["biaya"],"faskes_uniq":len(v["faskes"]),
   "pasien_uniq":len(v["pasien"]),"dokter_uniq":len(v["dokter"]),"status":dict(v["status"]),
   "faskes":sorted(v["faskes"])} for k,v in sorted(syn.items())}
R["n_syndicate"]=len(syn)
R["sindikat_total_biaya"]=sum(v["biaya"] for v in syn.values())

# skor_fraud distribution
sf_fraud=[num(r["skor_fraud"]) for r in vr if r["claim_id"] in set_a]
sf_non=[num(r["skor_fraud"]) for r in vr if r["claim_id"] not in set_a]
R["skor_fraud_min_fraud"]=min(sf_fraud); R["skor_fraud_max_fraud"]=max(sf_fraud)
R["skor_fraud_min_nonfraud"]=min(sf_non); R["skor_fraud_max_nonfraud"]=max(sf_non)
R["skor_fraud_overlap"]= not (min(sf_fraud) > max(sf_non))
# by status
R["skor_fraud_mean_by_status"]={}
for s in ["auto_clear","review","escalate"]:
    v=[num(r["skor_fraud"]) for r in vr if r["status"].strip()==s]
    R["skor_fraud_mean_by_status"][s]=round(statistics.mean(v),4)
    R.setdefault("skor_fraud_range_by_status",{})[s]=[min(v),max(v)]
R["skor_fraud_mean_all"]=round(statistics.mean([num(r["skor_fraud"]) for r in vr]),4)
R["skor_fraud_mean_fraud"]=round(statistics.mean(sf_fraud),4)
R["skor_fraud_mean_nonfraud"]=round(statistics.mean(sf_non),4)

# empties
R["v21_empty_counts"]={c: sum(1 for r in vr if (r[c] or "").strip()=="") for c in vr[0].keys()}
R["live_empty_counts"]={c: sum(1 for r in lr if (r[c] or "").strip()=="") for c in lr[0].keys()}

# ranges
R["biaya_min"]=min(num(r["biaya_rp"]) for r in vr); R["biaya_max"]=max(num(r["biaya_rp"]) for r in vr)
R["los_min"]=min(num(r["los_hari"]) for r in vr); R["los_max"]=max(num(r["los_hari"]) for r in vr)
R["biaya_mean"]=round(statistics.mean([num(r["biaya_rp"]) for r in vr]),2)
R["biaya_median"]=statistics.median([num(r["biaya_rp"]) for r in vr])
R["faskes_uniq"]=len({r["faskes_id"] for r in vr})
R["pasien_uniq"]=len({r["pasien_id"] for r in vr})
R["dokter_uniq"]=len({r["dokter_id"] for r in vr})
R["faskes_counts"]=dict(Counter(r["faskes_id"] for r in vr))
R["pasien_count_dist"]=dict(Counter(Counter(r["pasien_id"] for r in vr).values()))
R["layanan_counts"]=dict(Counter(r["layanan"] for r in vr))
R["sentimen_counts"]=dict(Counter(r["sentimen"] for r in vr))
R["kontradiksi_counts"]=dict(Counter(r["kontradiksi_narasi"] for r in vr))
R["tanggal_min"]=min(r["tanggal"] for r in vr); R["tanggal_max"]=max(r["tanggal"] for r in vr)
# modus counts for non-auto_clear
R["modus_all"]=dict(Counter(r["modus"].strip() for r in vr if r["modus"].strip()!=""))
# claim-level modal amounts for anomalies
esc=[r for r in vr if r["status"].strip()=="escalate"]
R["escalate_biaya_sorted"]=sorted(num(r["biaya_rp"]) for r in esc)
R["escalate_modus_biaya"]={}
for m in sorted({r["modus"].strip() for r in esc}):
    sel=[r for r in esc if r["modus"].strip()==m]
    R["escalate_modus_biaya"][m]={"n":len(sel),"biaya":sum(num(x["biaya_rp"]) for x in sel)}

# live vs v21 identity re-check for status+skor on the same claim
lmap={r["Name"]:r for r in lr}
R["live_total_biaya"]=sum(num(r["Biaya Rp"]) for r in lr)
R["live_status_same_as_v21"]= all(lmap[r["claim_id"]]["Status"].strip()==r["status"].strip() for r in vr)
R["live_biaya_same_as_v21"]= all(num(lmap[r["claim_id"]]["Biaya Rp"])==num(r["biaya_rp"]) for r in vr)
R["live_skor_same_as_v21"]= all(abs(num(lmap[r["claim_id"]]["Skor Fraud"])-num(r["skor_fraud"]))<1e-9 for r in vr)

with open(OUT,"w",encoding="utf-8") as f: json.dump(R,f,ensure_ascii=False,indent=1)
print("OK", OUT)
