import csv, json, os, io
BASE = r"N:\HEALTHKATHON"
LIVE = os.path.join(BASE, r"analysis\corpus\claims_v2_live.csv")
V21  = os.path.join(BASE, r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
OUT  = os.path.join(BASE, r"analysis\reports\scripts\out_compare.json")

def load(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)

lf, lr = load(LIVE)
vf, vr = load(V21)
res = {}
res["live_ncols"] = len(lf); res["live_nrows"] = len(lr)
res["v21_ncols"] = len(vf); res["v21_nrows"] = len(vr)
res["live_cols"] = lf; res["v21_cols"] = vf

# index v21 by claim_id
vmap = {r["claim_id"]: r for r in vr}
lmap = {r["Name"]: r for r in lr}
res["live_ids_dupes"] = len(lr) - len(lmap)
res["v21_ids_dupes"] = len(vr) - len(vmap)
res["ids_only_live"] = sorted(set(lmap) - set(vmap))
res["ids_only_v21"] = sorted(set(vmap) - set(lmap))

# live id format check
bad = [k for k in lmap if not (len(k)==6 and k.startswith("KLM"))]
res["live_ids_malformed"] = bad[:20]

# order of live rows
res["live_order_first10"] = [r["Name"] for r in lr[:10]]
res["live_sorted_by_id"] = [r["Name"] for r in lr] == sorted(lmap.keys())

# field mapping live -> v21
MAP = {
 "tanggal":"Tanggal", "biaya_rp":"Biaya Rp", "risiko":"Risiko", "los_hari":"LOS hari",
 "status":"Status", "sindikat":"Sindikat", "skor_fraud":"Skor Fraud", "modus":"Modus",
 "faskes_id":"Faskes", "pasien_raw":"Pasien", "dokter_raw":"Dokter", "sentimen":"Sentimen",
 "skor_sentimen":"Skor Sentimen", "layanan":"Layanan", "rujukan":"Rujukan",
 "obat":"Obat", "sinyal_shap":"Sinyal SHAP", "kontribusi_saluran":"Kontribusi Saluran",
 "alasan":"Alasan", "narasi_rekam_medis":"Narasi Rekam Medis", "umpan_balik_pasien":"Umpan Balik Pasien",
 "kontradiksi_narasi":"Kontradiksi Narasi", "alasan_berobat":"Alasan Berobat",
 "diagnosis_raw":"Diagnosis ICD-10", "prosedur_raw":"Prosedur ICD-9-CM",
}
diffs = {}
for vk, lk in MAP.items():
    if lk not in lf or vk not in vf:
        diffs[vk] = "MISSING_COLUMN"
        continue
    ndiff = 0; examples = []
    for cid, vrow in vmap.items():
        lrow = lmap.get(cid)
        if lrow is None: continue
        a = (vrow[vk] or "").strip(); b = (lrow[lk] or "").strip()
        if a != b:
            ndiff += 1
            if len(examples) < 4: examples.append([cid, vk, a[:70], b[:70]])
    diffs[vk] = {"ndiff": ndiff, "examples": examples}
res["field_diffs"] = diffs

# identity of key fields for the same claim
def norm_num(s):
    try: return int(float(s))
    except: return s
# numeric compare for biaya_rp and los_hari
numd = {}
for vk in ["biaya_rp","los_hari","skor_fraud","skor_sentimen"]:
    lk = MAP[vk]; n=0; ex=[]
    for cid, vrow in vmap.items():
        lrow = lmap.get(cid)
        if lrow is None: continue
        a=(vrow[vk] or "").strip(); b=(lrow[lk] or "").strip()
        if vk=="biaya_rp" or vk=="los_hari":
            a2=norm_num(a); b2=norm_num(b); same = (a2==b2)
        elif vk in ("skor_fraud","skor_sentimen"):
            try: same = abs(float(a)-float(b))<1e-9
            except: same = (a==b)
        else: same = (a==b)
        if not same:
            n+=1
            if len(ex)<5: ex.append([cid, a, b])
    numd[vk]={"ndiff":n,"examples":ex}
res["numeric_diffs"] = numd

# is_fraud derivation check from live
from collections import Counter
res["live_status_counts"] = dict(Counter((r["Status"] or "").strip() for r in lr))
res["live_risiko_counts"] = dict(Counter((r["Risiko"] or "").strip() for r in lr))
res["live_sindikat_counts"] = dict(Counter((r["Sindikat"] or "").strip() for r in lr))
res["v21_status_counts"] = dict(Counter((r["status"] or "").strip() for r in vr))
res["v21_risiko_counts"] = dict(Counter((r["risiko"] or "").strip() for r in vr))
res["v21_is_fraud_counts"] = dict(Counter((r["is_fraud"] or "").strip() for r in vr))
res["v21_sindikat_counts"] = dict(Counter((r["sindikat"] or "").strip() for r in vr))
res["live_modus_counts"] = dict(Counter((r["Modus"] or "").strip() for r in lr))
res["v21_modus_counts"] = dict(Counter((r["modus"] or "").strip() for r in vr))
# v21 modus by status
res["v21_modus_by_status"] = {s: dict(Counter((r["modus"] or "").strip() for r in vr if r["status"]==s)) for s in set(r["status"] for r in vr)}
res["live_modus_by_status"] = {s: dict(Counter((r["Modus"] or "").strip() for r in lr if r["Status"]==s)) for s in set(r["Status"] for r in lr)}

with open(OUT,"w",encoding="utf-8") as f:
    json.dump(res,f,ensure_ascii=False,indent=1)
print("WROTE", OUT)
