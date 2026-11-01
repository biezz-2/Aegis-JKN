import csv, os, statistics, collections, re
D = r"N:\HEALTHKATHON"
rows = list(csv.DictReader(open(os.path.join(D,"analysis","corpus","claims_v2_live.csv"), encoding="utf-8-sig")))
fr = [r for r in rows if r["Risiko"]=="fraud"]
nf = [r for r in rows if r["Risiko"]!="fraud"]
K = "Kontribusi Saluran"
print("sample fraud:", [r[K] for r in fr[:4]])
print("sample nonfraud:", [r[K] for r in nf[:4]])
def parse(m):
    return [float(x.replace(",",".")) for x in re.findall(r"(\d+[.,]\d+)", m)]
for idx,name in [(0,"T"),(1,"F"),(2,"S")]:
    fv=[parse(r[K])[idx] for r in fr if len(parse(r[K]))>=3]
    nv=[parse(r[K])[idx] for r in nf if len(parse(r[K]))>=3]
    print(f"  {name}: fraud n={len(fv)} min={min(fv):.3f} mean={statistics.mean(fv):.4f} | normal n={len(nv)} max={max(nv):.3f} mean={statistics.mean(nv):.4f} | minfraud>maxnormal={min(fv)>max(nv)}")
    best=None
    for t in sorted(set(fv+nv)):
        tp=sum(1 for x in fv if x>=t); fp=sum(1 for x in nv if x>=t)
        if tp>=30 and tp+fp>0 and tp/(tp+fp)==1.0:
            best=t; break
    print(f"     threshold precision=1.0 tp>=30: {best}")
al=[r["Alasan"] for r in rows]
stripped=[re.sub(r"\d+[.,]?\d*","",a) for a in al]
print("\nAlasan distinct:",len(set(al)),"after digit strip:",len(set(stripped)))
print("prefix FRAUD/NORMAL:",sum(1 for a in al if a.strip().startswith(("FRAUD","NORMAL"))))
for col in ["Umpan Balik Pasien","Narasi Rekam Medis","Alasan Berobat"]:
    print(f"  unique {col}: {len(set(r[col] for r in rows))} / 300")
# Sindikat
print("\nSindikat counts:", dict(collections.Counter(r["Sindikat"] for r in rows)))
