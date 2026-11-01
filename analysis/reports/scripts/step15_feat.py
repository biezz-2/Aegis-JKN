import csv, os, json, math, statistics
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
rows=list(csv.DictReader(open(V21,encoding="utf-8-sig",newline="")))
def N(s): return int(float(s))
# Rebuild notebook cell 5 features (no StandardScaler needed for edge count? cos sim changes with scaling, so replicate)
from collections import Counter
import datetime
def dt_parse(s): 
    y,m,d=[int(x) for x in s.split("-")]; return datetime.date(y,m,d)
feat={}
feat["biaya_rp"]=[float(r["biaya_rp"]) for r in rows]
feat["los_hari"]=[float(r["los_hari"]) for r in rows]
feat["biaya_per_hari"]=[float(r["biaya_rp"])/max(float(r["los_hari"]),1.0) for r in rows]
feat["skor_sentimen"]=[float(r["skor_sentimen"]) for r in rows]
bulan=[];dow=[];dom=[];wknd=[]
for r in rows:
    d=dt_parse(r["tanggal"]); bulan.append(float(d.month)); dow.append(float(d.weekday())); dom.append(float(d.day)); wknd.append(1.0 if d.weekday()>=5 else 0.0)
feat["bulan"]=bulan; feat["hari_dalam_minggu"]=dow; feat["hari_dalam_bulan"]=dom; feat["is_weekend"]=wknd
feat["is_rawat_inap"]=[1.0 if r["layanan"]=="rawat inap" else 0.0 for r in rows]
feat["panjang_narasi"]=[float(len(str(r["narasi_rekam_medis"]))) for r in rows]
feat["jumlah_kata_narasi"]=[float(len(str(r["narasi_rekam_medis"]).split())) for r in rows]
feat["panjang_feedback"]=[float(len(str(r["umpan_balik_pasien"]))) for r in rows]
feat["jumlah_obat"]=[float(len(str(r["obat"]).split(";")) if str(r["obat"])!="—" else 0) for r in rows]
for col in ("diagnosis_code","prosedur_code"):
    tot=Counter(r[col] for r in rows); n=len(rows)
    freq={k:v/n for k,v in tot.items()}
    feat[col+"_freq"]=[freq.get(r[col],0.0) for r in rows]
for dx,_ in Counter(r["diagnosis_code"] for r in rows).most_common(10):
    feat["dx_"+dx]=[1.0 if r["diagnosis_code"]==dx else 0.0 for r in rows]
for pr,_ in Counter(r["prosedur_code"] for r in rows).most_common(10):
    feat["proc_"+pr]=[1.0 if r["prosedur_code"]==pr else 0.0 for r in rows]
cols=list(feat.keys())
M=[[feat[c][i] for c in cols] for i in range(len(rows))]
out={"n_features":len(cols),"n_rows":len(rows)}
# StandardScaler (population std, sklearn uses ddof=0)
def scale(M):
    n=len(M); p=len(M[0])
    mu=[sum(M[i][j] for i in range(n))/n for j in range(p)]
    var=[sum((M[i][j]-mu[j])**2 for i in range(n))/n for j in range(p)]
    sd=[math.sqrt(v) if v>1e-12 else 1.0 for v in var]
    return [[(M[i][j]-mu[j])/sd[j] for j in range(p)] for i in range(n)]
Xs=scale(M)
def cos_edges(X,theta):
    n=len(X)
    norms=[math.sqrt(sum(v*v for v in X[i])) or 1.0 for i in range(n)]
    cnt=0
    for i in range(n):
        for j in range(i+1,n):
            dot=sum(X[i][k]*X[j][k] for k in range(len(X[i])))
            s=dot/(norms[i]*norms[j])
            if s>theta: cnt+=2
    return cnt+n
out["feat_edges_theta085_scaled"]=cos_edges(Xs,0.85)
out["feat_edges_theta085_raw"]=cos_edges(M,0.85)
out["feat_edges_theta05_scaled"]=cos_edges(Xs,0.5)
# A_sem
n=len(rows); cnt=0
for i in range(n):
    for j in range(i+1,n):
        sim=0.0
        if rows[i]["diagnosis_code"]==rows[j]["diagnosis_code"]: sim+=0.45
        if rows[i]["prosedur_code"]==rows[j]["prosedur_code"]: sim+=0.45
        if rows[i]["faskes_id"]==rows[j]["faskes_id"]: sim+=0.10
        if sim>=0.55: cnt+=2
out["A_sem_edges"]=cnt+n
out["A_homo_edges"]=None
# A_top per notebook (7140) and pipeline (10386) already known
# review: als 'n_common' 300, ds
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open("out_feat.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
