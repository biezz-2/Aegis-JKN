import csv, json, os, math
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
rows=list(csv.DictReader(open(V21,encoding="utf-8-sig",newline="")))
out={}
def N(s):
    try: return int(float(s))
    except: return 0
from collections import Counter
out["RS_A_claims"]=sum(1 for r in rows if r["faskes_id"]=="RS_A")
out["KLM001"]={k:rows[0][k] for k in ("claim_id","biaya_rp","los_hari","pasien_id","dokter_id","faskes_id","skor_fraud","status","sindikat","modus")}
out["SYND-01_ids"]=[r["claim_id"] for r in rows if r["sindikat"]=="SYND-01"]
out["SYND-01_biaya"]=[N(r["biaya_rp"]) for r in rows if r["sindikat"]=="SYND-01"]
out["SYND-01_dokters"]=sorted({r["dokter_id"] for r in rows if r["sindikat"]=="SYND-01"})
out["SYND-01_pasiens"]=sorted({r["pasien_id"] for r in rows if r["sindikat"]=="SYND-01"})
out["kontradiksi_1_count"]=sum(1 for r in rows if r["kontradiksi_narasi"].strip()=="1")
out["D01_claims"]=sum(1 for r in rows if r["dokter_id"]=="D01")
out["D01_biaya_sum"]=sum(N(r["biaya_rp"]) for r in rows if r["dokter_id"]=="D01")
# RS_A escalate claims
out["RS_A_escalate"]=sum(1 for r in rows if r["faskes_id"]=="RS_A" and r["status"]=="escalate")
# max skor_fraud RS_A
out["RS_A_max_skor"]=max(float(r["skor_fraud"]) for r in rows if r["faskes_id"]=="RS_A")
out["max_skor_all"]=max(float(r["skor_fraud"]) for r in rows)
out["max_skor_claim"]=[r["claim_id"] for r in rows if float(r["skor_fraud"])==max(float(x["skor_fraud"]) for x in rows)]
# PCI claims 00.66
out["n_prosedur_0066"]=sum(1 for r in rows if r["prosedur_code"]=="00.66")
out["n_0066_diag_K297"]=sum(1 for r in rows if r["prosedur_code"]=="00.66" and r["diagnosis_code"]=="K29.7")
out["n_0066_escalate"]=sum(1 for r in rows if r["prosedur_code"]=="00.66" and r["status"]=="escalate")
out["biaya_0066"]=sorted({N(r["biaya_rp"]) for r in rows if r["prosedur_code"]=="00.66"})
# A_top edges per notebook cell 7 algorithm
n=len(rows)
A_top=0
for i in range(n):
    for j in range(i+1,n):
        if rows[i]["pasien_id"]==rows[j]["pasien_id"] or rows[i]["dokter_id"]==rows[j]["dokter_id"] or (rows[i]["faskes_id"]==rows[j]["faskes_id"] and rows[i]["rujukan"]!="nan" and rows[i]["rujukan"]==rows[j]["rujukan"]):
            A_top+=2
A_top+=n
out["A_top_edges_notebook_alg"]=A_top
# pipeline.py algorithm (pi==pj or di==dj or hi==hj)
A_top2=n; 
for i in range(n):
    for j in range(i+1,n):
        if rows[i]["pasien_id"]==rows[j]["pasien_id"] or rows[i]["dokter_id"]==rows[j]["dokter_id"] or rows[i]["faskes_id"]==rows[j]["faskes_id"]:
            A_top2+=2
out["A_top_edges_pipeline_alg"]=A_top2
# prevalence
out["prevalensi_fraud"]=round(36/300*100,2)
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open("out_front.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
