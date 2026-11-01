import csv, os, re, json, statistics
from collections import defaultdict
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
rows=list(csv.DictReader(open(V21,encoding="utf-8-sig",newline="")))
def N(s): return int(float(s))
# extract Rp amounts in alasan
pat=re.compile(r'([Pp]enghematan|overcharge|efisiensi|koreksi|selisih|selisih biaya|hemat)\D{0,60}?([0-9][0-9.,]*)\s*(?:juta|jt|ribu|rp)?', re.I)
res=[]
for r in rows:
    a=r["alasan"] or ""
    for m in re.finditer(r'([0-9][0-9.,]*)\s*(juta|jt|ribu|jt|Rp)', a):
        res.append((r["claim_id"], r["status"], m.group(0)))
print("all Rp amounts mentioned in 'alasan' (first 25):")
for x in res[:25]: print(" ",x)
print("total matches",len(res))
# unique claim-level: does any row mention 'overcharge'/'penghematan'?
kw=[r["claim_id"] for r in rows if re.search(r'penghematan|overcharge|efisiensi|koreksi', r["alasan"] or "", re.I)]
print("rows with keyword overcharge/penghematan/koreksi:",len(kw), kw[:10])
# print one full alasan of a review row and an escalate row
for cid in ("KLM016","KLM018","KLM121","KLM122","KLM100"):
    row=[r for r in rows if r["claim_id"]==cid]
    if row:
        print("="*10,cid,row[0]["status"],row[0]["modus"],row[0]["biaya_rp"])
        print(row[0]["alasan"])
