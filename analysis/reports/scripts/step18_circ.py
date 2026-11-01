import csv, os, json, math, datetime, statistics
from collections import Counter, defaultdict
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
rows=list(csv.DictReader(open(V21,encoding="utf-8-sig",newline="")))
def N(s): return int(float(s))
def dparse(s):
    y,m,d=[int(x) for x in s.split("-")]; return datetime.date(y,m,d)
# replicate notebook cell5 features exactly
feat=defaultdict(list)
for r in rows:
    feat["biaya_rp"].append(float(r["biaya_rp"])); feat["los_hari"].append(float(r["los_hari"]))
    feat["biaya_per_hari"].append(float(r["biaya_rp"])/max(float(r["los_hari"]),1.0))
    feat["skor_sentimen"].append(float(r["skor_sentimen"]))
    d=dparse(r["tanggal"])
    feat["bulan"].append(float(d.month)); feat["hari_dalam_minggu"].append(float(d.weekday()))
    feat["hari_dalam_bulan"].append(float(d.day)); feat["is_weekend"].append(1.0 if d.weekday()>=5 else 0.0)
    feat["is_rawat_inap"].append(1.0 if r["layanan"]=="rawat inap" else 0.0)
    feat["panjang_narasi"].append(float(len(str(r["narasi_rekam_medis"]))))
    feat["jumlah_kata_narasi"].append(float(len(str(r["narasi_rekam_medis"]).split())))
    feat["panjang_feedback"].append(float(len(str(r["umpan_balik_pasien"]))))
    feat["jumlah_obat"].append(float(len(str(r["obat"]).split(";")) if str(r["obat"])!="—" else 0))
for col in ("diagnosis_code","prosedur_code"):
    tot=Counter(r[col] for r in rows); n=len(rows)
    freq={k:v/n for k,v in tot.items()}
    feat[col+"_freq"]=[freq.get(r[col],0.0) for r in rows]
for dx,_ in Counter(r["diagnosis_code"] for r in rows).most_common(10): feat["dx_"+dx]=[1.0 if r["diagnosis_code"]==dx else 0.0 for r in rows]
for pr,_ in Counter(r["prosedur_code"] for r in rows).most_common(10): feat["proc_"+pr]=[1.0 if r["prosedur_code"]==pr else 0.0 for r in rows]
cols=list(feat.keys())
out={"n_features_cell5":len(cols),"cols":cols}
# Now: is is_fraud a deterministic function of the feature set? Test rules
y=[int(r["is_fraud"]) for r in rows]
out["n_pos"]=sum(y)
# rule 1: modus != '' and modus in fraud modus set?
fraud_modus={"upcoding","phantom_billing","unbundling","drug_diversion","readmission_berulang","excessive_usage","repeat_billing","iur_biaya","biaya_markup"}
pred=[1 if r["modus"].strip() in fraud_modus else 0 for r in rows]
tp=sum(1 for a,b in zip(pred,y) if a==1 and b==1); fp=sum(1 for a,b in zip(pred,y) if a==1 and b==0); fn=sum(1 for a,b in zip(pred,y) if a==0 and b==1)
out["rule_modus_fraud"]={"tp":tp,"fp":fp,"fn":fn,"acc":round((tp+len(y)-fp-fn)/len(y),4)}
# rule 2: modus in (upcoding,phantom_billing,unbundling,drug_diversion) OR (los>=?) etc
# find single-feature thresholds that perfectly separate? check biaya_rp
for f in ("biaya_rp","los_hari","skor_sentimen","jumlah_obat","panjang_narasi","biaya_per_hari"):
    v=[feat[f][i] for i in range(len(rows))]
    best=None
    for t in sorted(set(v)):
        p=[1 if x>t else 0 for x in v]
        tp2=sum(1 for a,b in zip(p,y) if a==1 and b==1); fp2=sum(1 for a,b in zip(p,y) if a==1 and b==0); fn2=sum(1 for a,b in zip(p,y) if a==0 and b==1)
        f1=0 if tp2==0 else 2*tp2/(2*tp2+fp2+fn2)
        if best is None or f1>best[0]: best=(round(f1,4),t,tp2,fp2,fn2)
    out[f"best_threshold_{f}"]=best
# per-modus breakdown of fraud labels
out["modus_fraud_crosstab"]={m:{"n":sum(1 for r in rows if r["modus"].strip()==m),
   "fraud":sum(1 for r in rows if r["modus"].strip()==m and r["is_fraud"]=="1")} for m in sorted({r["modus"].strip() for r in rows})}
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open("out_circ.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
