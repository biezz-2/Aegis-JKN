import json, os, re, gzip, base64, csv, io, hashlib, sys
BASE=r"N:\HEALTHKATHON"
d=json.load(open("nb_main_dump.json",encoding="utf-8"))
src=d[3]['src']
m=re.search(r'EMBEDDED_CLAIMS_CSV_B64\s*=\s*"([^"]+)"', src)
if not m:
    print("NOT FOUND"); sys.exit()
b64=m.group(1)
raw=gzip.decompress(base64.b64decode(b64)).decode("utf-8")
rows=list(csv.DictReader(io.StringIO(raw)))
print("embedded rows",len(rows),"cols",len(rows[0]))
print("cols:",list(rows[0].keys()))
out={"embedded_n":len(rows),"embedded_cols":list(rows[0].keys()),
     "embedded_md5":hashlib.md5(raw.encode()).hexdigest()}
# compare to v21
p=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
vr=list(csv.DictReader(open(p,encoding="utf-8-sig",newline="")))
raw2=open(p,encoding="utf-8-sig").read()
out["v21_md5"]=hashlib.md5(raw2.encode()).hexdigest()
# compare field by field on claim_id
emap={r.get("claim_id"):r for r in rows}
vmap={r["claim_id"]:r for r in vr}
out["emb_ids"]=sorted(emap.keys())[:3]; out["emb_ids_n"]=len(emap)
out["emb_has_is_fraud"]="is_fraud" in rows[0]
out["emb_has_sindikat"]="sindikat" in rows[0]
out["emb_has_skor_fraud"]="skor_fraud" in rows[0]
common=set(emap)&set(vmap)
out["n_common"]=len(common)
diffs={}
for c in rows[0]:
    if c in vr[0]:
        n=sum(1 for k in common if (emap[k].get(c) or "").strip()!=(vmap[k].get(c) or "").strip())
        if n: diffs[c]=n
out["diffs"]=diffs
# status counts of embedded
from collections import Counter
if "status" in rows[0]: out["emb_status"]=dict(Counter(r["status"].strip() for r in rows))
if "is_fraud" in rows[0]: out["emb_is_fraud"]=dict(Counter(r["is_fraud"].strip() for r in rows))
if "biaya_rp" in rows[0]:
    out["emb_total_biaya"]=sum(int(float(r["biaya_rp"])) for r in rows)
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open("out_embed.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
