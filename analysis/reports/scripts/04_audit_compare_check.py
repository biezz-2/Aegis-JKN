#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asersi untuk seksi baru "Dump Notion vs claims_300_v2.1.csv" di 04-data-quality.md."""
import csv, os, re, sys, json
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")

NOTION = r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv"
V21 = r"N:\HEALTHKATHON\mechine-learning-deep-learning\datasets\claims_300_v2.1.csv"
DB = r"N:\HEALTHKATHON\mechine-learning-deep-learning\datasets\claims_db.json"

notion = list(csv.DictReader(open(NOTION, encoding="utf-8-sig", newline="")))
v21 = list(csv.DictReader(open(V21, encoding="utf-8-sig", newline="")))
N = {r["Name"].strip(): r for r in notion}
V = {r["claim_id"].strip(): r for r in v21}
common = sorted(set(N) & set(V))
n = lambda v: "" if v is None else str(v).strip()

CHECKS = []
def chk(label, got, exp):
    ok = got == exp
    CHECKS.append((ok, label, got, exp))
    print(f"{'OK ' if ok else 'GAGAL'}  {label}: got={got} exp={exp}")

print("=== ASERSI PERBANDINGAN DUMP NOTION vs claims_300_v2.1.csv ===\n")
print("-- A. identitas sumber --")
chk("baris Notion", len(notion), 300)
chk("baris v2.1", len(v21), 300)
chk("kolom Notion", len(notion[0]), 29)
chk("kolom v2.1", len(v21[0]), 31)
chk("claim_id == Name (himpunan)", set(V) == set(N), True)
chk("claim_id urut menaik", [r["claim_id"] for r in v21] == sorted(V), True)

print("\n-- B. kolom v2.1 yang tidak ada di dump Notion --")
MAP = {"Name":"claim_id","Tanggal":"tanggal","Pasien":"pasien_raw","Dokter":"dokter_raw",
       "Faskes":"faskes_id","Diagnosis ICD-10":"diagnosis_raw","Prosedur ICD-9-CM":"prosedur_raw",
       "Obat":"obat","LOS hari":"los_hari","Biaya Rp":"biaya_rp","Narasi Rekam Medis":"narasi_rekam_medis",
       "Kontradiksi Narasi":"kontradiksi_narasi","Skor Fraud":"skor_fraud","Risiko":"risiko",
       "Status":"status","Modus":"modus","Sindikat":"sindikat","Alasan":"alasan",
       "Sinyal SHAP":"sinyal_shap","Kontribusi Saluran":"kontribusi_saluran","Skor Sentimen":"skor_sentimen",
       "Sentimen":"sentimen","Umpan Balik Pasien":"umpan_balik_pasien","Alasan Berobat":"alasan_berobat",
       "Layanan":"layanan","Rujukan":"rujukan"}
chk("kolom eksklusif v2.1", sorted(c for c in v21[0] if c not in MAP.values()),
    ['diagnosis_code', 'dokter_id', 'is_fraud', 'pasien_id', 'prosedur_code'])

print("\n-- C. kolom yang identik pada 300 baris --")
def same(nk_, vk_, numeric=False):
    d = []
    for cid in common:
        a, b = n(N[cid][nk_]), n(V[cid][vk_])
        if numeric:
            try: a, b = f"{float(a):.6f}", f"{float(b):.6f}"
            except Exception: pass
        if a != b: d.append(cid)
    return d
IDENT = [("Tanggal","tanggal"),("Pasien","pasien_raw"),("Faskes","faskes_id"),
         ("Diagnosis ICD-10","diagnosis_raw"),("Prosedur ICD-9-CM","prosedur_raw"),("Obat","obat"),
         ("LOS hari","los_hari",True),("Biaya Rp","biaya_rp",True),
         ("Narasi Rekam Medis","narasi_rekam_medis"),("Skor Fraud","skor_fraud",True),
         ("Risiko","risiko"),("Status","status"),("Modus","modus"),("Alasan","alasan"),
         ("Sinyal SHAP","sinyal_shap"),("Kontribusi Saluran","kontribusi_saluran"),
         ("Skor Sentimen","skor_sentimen",True),("Sentimen","sentimen"),
         ("Umpan Balik Pasien","umpan_balik_pasien"),("Alasan Berobat","alasan_berobat"),
         ("Layanan","layanan"),("Rujukan","rujukan")]
for item in IDENT:
    nk_, vk_ = item[0], item[1]
    num = len(item) > 2
    chk(f"kolom identik: {nk_}", len(same(nk_, vk_, num)), 0)

print("\n-- D. kolom dengan perbedaan(format) --")
chk("Dokter: baris beda (truncasi)", len(same("Dokter","dokter_raw")), 32)
chk("Kontradiksi Narasi: baris beda (format)", len(same("Kontradiksi Narasi","kontradiksi_narasi")), 300)
chk("Sindikat: baris beda (format)", len(same("Sindikat","sindikat")), 264)
chk("total sel berbeda", sum(len(same(*i[:2], i[2] if len(i) > 2 else False)) for i in IDENT)
    + len(same("Dokter","dokter_raw")) + len(same("Kontradiksi Narasi","kontradiksi_narasi"))
    + len(same("Sindikat","sindikat")), 596)
# rekap jumlah kolom: 26 kolom dump Notion berpasangan -> 23 identik / 2 format / 1 isi
PAIR_DIFF = {"Dokter","Kontradiksi Narasi","Sindikat"}
chk("jumlah kolom dump Notion berpasangan dengan v2.1", len(MAP), 26)
chk("Name == claim_id (kunci baris)", len(same("Name","claim_id")), 0)
chk("jumlah kolom berpasangan yang identik 300 baris",
    len([i for i in IDENT if not same(i[0], i[1], len(i) > 2)]) + (1 if not same("Name","claim_id") else 0), 23)
chk("jumlah kolom beda format", len([k for k in PAIR_DIFF if k != "Dokter"]), 2)
chk("jumlah kolom beda isi (truncasi)", len([k for k in PAIR_DIFF if k == "Dokter"]), 1)
chk("Catatan ada di dump Notion tapi tidak di v2.1", ("Catatan" in notion[0], "Catatan" in v21[0]), (True, False))

print("\n-- E. kesetaraan semantik --")
def truth(v):
    v = n(v).lower()
    if v in ("true","1","ya","yes"): return True
    if v in ("false","0","tidak","no",""): return False
    return None
chk("Kontradiksi Narasi semantik beda", len([c for c in common
    if truth(N[c]["Kontradiksi Narasi"]) != truth(V[c]["kontradiksi_narasi"])]), 0)
chk("Kontradiksi True di kedua sumber", (sum(1 for r in notion if truth(r["Kontradiksi Narasi"])),
    sum(1 for r in v21 if truth(r["kontradiksi_narasi"]))), (12, 12))
none_v = sorted(r["claim_id"] for r in v21 if n(r["sindikat"]) == "none")
empty_n = sorted(r["Name"] for r in notion if not n(r["Sindikat"]))
chk("sindikat 'none' v2.1 == Sindikat kosong Notion", set(none_v) == set(empty_n), True)
chk("jumlah sindikat kosong", len(none_v), 264)
chk("Sindikat: 36 terisi identik", len([c for c in common if n(N[c]["Sindikat"]) and n(N[c]["Sindikat"]) == n(V[c]["sindikat"])]), 36)

print("\n-- F. is_fraud --")
chk("nilai is_fraud", dict(Counter(n(r["is_fraud"]) for r in v21)), {'0': 264, '1': 36})
chk("is_fraud != (risiko==fraud) vs Notion", len([c for c in common
    if truth(V[c]["is_fraud"]) != (n(N[c]["Risiko"]) == "fraud")]), 0)
chk("is_fraud != (risiko==fraud) internal v2.1", len([c for c in common
    if truth(V[c]["is_fraud"]) != (n(V[c]["risiko"]) == "fraud")]), 0)

print("\n-- G. KLM115 (kasus pembeda ambang 0,80) --")
k = "KLM115"
chk("KLM115 skor Notion", n(N[k]["Skor Fraud"]), "0.8")
chk("KLM115 skor v2.1", n(V[k]["skor_fraud"]), "0.8")
chk("KLM115 risiko Notion", n(N[k]["Risiko"]), "fraud")
chk("KLM115 risiko v2.1", n(V[k]["risiko"]), "fraud")
chk("KLM115 is_fraud v2.1", n(V[k]["is_fraud"]), "1")
chk("KLM115 sindikat", (n(N[k]["Sindikat"]), n(V[k]["sindikat"])), ("SYND-09", "SYND-09"))
chk("baris skor tepat 0.80 di Notion", [r["Name"] for r in notion
    if float(n(r["Skor Fraud"])) == 0.80], ["KLM115"])
chk("baris skor tepat 0.80 di v2.1", [r["claim_id"] for r in v21
    if float(n(r["skor_fraud"])) == 0.80], ["KLM115"])
chk("baris skor tepat 0.35", [r["Name"] for r in notion
    if float(n(r["Skor Fraud"])) == 0.35], [])
chk("baris skor tepat 0.60", [r["Name"] for r in notion
    if float(n(r["Skor Fraud"])) == 0.60], [])

print("\n-- H. aturan LOS (identik di kedua sumber) --")
for lbl, rows_, kk in (("Notion", notion, "LOS hari"), ("v2.1", v21, "los_hari")):
    vals = [n(r[kk]) for r in rows_]
    chk(f"{lbl}: LOS kosong", sum(1 for v in vals if v == ""), 0)
    chk(f"{lbl}: LOS == '0'", sum(1 for v in vals if v == "0"), 109)
los_diff = [c for c in common if n(N[c]["LOS hari"]) != n(V[c]["los_hari"])]
chk("baris los_hari berbeda", len(los_diff), 0)
chk("v2.1 LOS=0 rawat inap", sorted(r["claim_id"] for r in v21
    if n(r["los_hari"]) == "0" and n(r["layanan"]) == "rawat inap"),
    ["KLM008", "KLM010", "KLM012"])

print("\n-- I. pola bermasalah identik di kedua sumber --")
def tfs(r, key): return tuple(float(x) for x in re.findall(r"[TFS] ([-\d.]+)", n(r[key])))
def ids(rows_, key, pred): return sorted((r.get("Name") or r.get("claim_id")) for r in rows_ if pred(r))
PAT = [
    ("LOS=0", 109,
     lambda r: n(r["LOS hari"]) == "0", lambda r: n(r["los_hari"]) == "0"),
    ("Rujukan 'undefined'", 28,
     lambda r: "undefined" in n(r["Rujukan"]).lower(), lambda r: "undefined" in n(r["rujukan"]).lower()),
    ("Prosedur sentinel —", 156,
     lambda r: n(r["Prosedur ICD-9-CM"]) == "—", lambda r: n(r["prosedur_raw"]) == "—"),
    ("Obat sentinel —", 3,
     lambda r: n(r["Obat"]) == "—", lambda r: n(r["obat"]) == "—"),
    ("Skor != T+F+S", 42,
     lambda r: abs(sum(tfs(r, "Kontribusi Saluran")) - float(n(r["Skor Fraud"]))) > 1e-9,
     lambda r: abs(sum(tfs(r, "kontribusi_saluran")) - float(n(r["skor_fraud"]))) > 1e-9),
    ("Alasan kosong", 1,
     lambda r: n(r["Alasan"]) == "", lambda r: n(r["alasan"]) == ""),
    ("Modus kosong", 240,
     lambda r: n(r["Modus"]) == "", lambda r: n(r["modus"]) == ""),
]
for name, exp, pn, pv in PAT:
    a = ids(notion, None, pn)
    b = ids(v21, None, pv)
    chk(f"{name}: jumlah Notion", len(a), exp)
    chk(f"{name}: jumlah v2.1", len(b), exp)
    chk(f"{name}: himpunan ID sama", set(a) == set(b), True)

print("\n-- J. sindikat: pemetaan entitas --")
ent = defaultdict(lambda: defaultdict(set))
for r in v21:
    s = n(r["sindikat"])
    if s and s != "none":
        ent[s]["f"].add(n(r["faskes_id"])); ent[s]["d"].add(n(r["dokter_id"])); ent[s]["p"].add(n(r["pasien_id"]))
EXPECT = {"SYND-01":("RS_A",{"D01","D02"},{"P01","P02","P03"}),
          "SYND-02":("RS_C",{"D05"},{"P08","P09","P10"}),
          "SYND-03":("RS_B",{"D07"},{"P12","P13","P14"}),
          "SYND-04":("RS_E",{"D09"},{"P16","P17"}),
          "SYND-05":("RS_F",{"D08"},{"P19","P20"}),
          "SYND-06":("RS_G",{"D13"},{"P21","P22"}),
          "SYND-07":("RS_H",{"D14"},{"P23","P24"}),
          "SYND-08":("RS_I",{"D15"},{"P25","P26"}),
          "SYND-09":("RS_J",{"D19"},{"P27"})}
for s, (f, d, p) in EXPECT.items():
    chk(f"{s} faskes", ent[s]["f"], {f})
    chk(f"{s} dokter", ent[s]["d"], d)
    chk(f"{s} pasien", ent[s]["p"], p)
chk("KLM121 entitas (v2.1)", (n(V["KLM121"]["faskes_id"]), n(V["KLM121"]["dokter_id"]),
    n(V["KLM121"]["pasien_id"]), n(V["KLM121"]["modus"])), ("RS_G","D13","P29","biaya_markup"))
chk("KLM122 entitas (v2.1)", (n(V["KLM122"]["faskes_id"]), n(V["KLM122"]["dokter_id"]),
    n(V["KLM122"]["pasien_id"]), n(V["KLM122"]["modus"])), ("RS_H","D14","P30","drug_diversion"))
chk("fraud tanpa sindikat di v2.1 ('none')", sorted(r["claim_id"] for r in v21
    if n(r["risiko"]) == "fraud" and n(r["sindikat"]) == "none"), ["KLM121","KLM122"])

print("\n-- K. entitas unik --")
chk("pasien unik v2.1", len({n(r['pasien_id']) for r in v21}), 40)
chk("dokter unik v2.1", len({n(r['dokter_id']) for r in v21}), 20)
chk("faskes unik v2.1", len({n(r['faskes_id']) for r in v21}), 10)
chk("pasien_id == prefiks Pasien Notion", len([c for c in common
    if n(V[c]["pasien_id"]) != n(N[c]["Pasien"]).split(" (")[0]]), 0)
chk("dokter_id == prefiks Dokter Notion", len([c for c in common
    if n(V[c]["dokter_id"]) != n(N[c]["Dokter"]).split(" (")[0]]), 0)
chk("diagnosis_code == prefiks dx Notion", len([c for c in common
    if n(V[c]["diagnosis_code"]) != n(N[c]["Diagnosis ICD-10"]).split(" - ")[0]]), 0)
chk("prosedur_code == prefiks proc Notion", len([c for c in common
    if n(V[c]["prosedur_code"]) != n(N[c]["Prosedur ICD-9-CM"]).split(" - ")[0]]), 0)

print("\n-- L. truncasi dokter_raw --")
tr = sorted(c for c in common if n(V[c]["dokter_raw"]) != n(N[c]["Dokter"]))
chk("jumlah baris terpotong", len(tr), 32)
chk("baris terpotong == baris D04+D16",
    set(tr) == {c for c in common if n(V[c]["dokter_id"]) in ("D04","D16")}, True)
chk("panjang nilai terpotong", sorted({len(n(V[c]['dokter_raw'])) for c in tr}), [24])
chk("nilai terpotong hanya D04/D16", sorted({n(V[c]['dokter_raw'])[:3] for c in tr}), ['D04','D16'])
chk("suffix Sp.JP hilang (tanpa strip)", sorted({V[c]['dokter_raw'] for c in tr}),
    ['D04 (dr. Danur Wibisono, ', 'D16 (dr. Prasetyo Utomo, '])
chk("panjang nilai terpotong (tanpa strip)", sorted({len(V[c]['dokter_raw']) for c in tr}), [25])
# akar cause: claims_db.json punya 3 segmen rich_text, segmen tengah punya href
db = json.load(open(DB, encoding="utf-8"))
segs = Counter()
href_rows = 0
for r in db["results"]:
    dk = r["properties"].get("Dokter", {}).get("rich_text", [])
    segs[len(dk)] += 1
    if len(dk) > 1: href_rows += 1
chk("distribusi jumlah segmen rich_text kolom Dokter", dict(segs), {1: 268, 3: 32})
chk("baris dengan >1 segmen = baris terpotong", href_rows, 32)
# apakah rich_text lain juga multi-segmen?
multi = Counter()
for r in db["results"]:
    for pk, pv in r["properties"].items():
        rt = pv.get("rich_text") if isinstance(pv, dict) else None
        if rt and len(rt) > 1: multi[pk] += 1
chk("properti multi-segmen di claims_db.json", dict(multi), {'Dokter': 32})

# uji varian parser: mana yang menghasilkan nilai claims_300_v2.1.csv
def v_first(rt):   return rt[0]["plain_text"]
def v_join_sp(rt): return " ".join(x["text"]["content"] for x in rt)
def v_join_pl(rt): return "".join(x["plain_text"] for x in rt)
def v_md(rt):      return "".join(f"[{x['plain_text']}]({x['href']})" if x.get("href") else x["plain_text"] for x in rt)
VARIANTS = [("rich_text[0] saja", v_first), ('" ".join(text.content) [notion_client.py:60]', v_join_sp),
            ('"".join(plain_text) [fetch_corpus.py:43-50]', v_join_pl), ("markdown-link + href", v_md)]
multi_rows = [r for r in db["results"] if len(r["properties"]["Dokter"]["rich_text"]) > 1]
for label, fn in VARIANTS:
    hits = sum(1 for r in multi_rows
               if fn(r["properties"]["Dokter"]["rich_text"]) == V[r["properties"]["Name"]["title"][0]["plain_text"]]["dokter_raw"])
    chk(f"varian parser cocok pada 32 baris multi-segmen: {label}", hits, 32 if label.startswith("rich_text[0]") else 0)

print("\n-- M. sumbu evaluasi grup --")
gc = Counter(r["pasien_id"] for r in v21)
fc = Counter(r["faskes_id"] for r in v21)
dc = Counter(r["dokter_id"] for r in v21)
chk("pasien: min klaim", min(gc.values()), 6)
chk("pasien: max klaim", max(gc.values()), 12)
chk("faskes: min klaim", min(fc.values()), 14)
chk("faskes: max klaim", max(fc.values()), 45)
chk("dokter: min klaim", min(dc.values()), 2)
chk("dokter: max klaim", max(dc.values()), 33)
pf = defaultdict(set)
for r in v21: pf[r["pasien_id"]].add(r["faskes_id"])
chk("pasien di >1 faskes", sum(1 for k, v in pf.items() if len(v) > 1), 16)
pdf = defaultdict(set)
for r in v21: pdf[r["dokter_id"]].add(r["faskes_id"])
chk("dokter di >1 faskes", sum(1 for k, v in pdf.items() if len(v) > 1), 0)

print("\n-- N. headline numbers tetap berlaku di v2.1 --")
chk("v2.1 total biaya", sum(int(n(r["biaya_rp"])) for r in v21), 3526650000)
chk("v2.1 status auto_clear", sum(1 for r in v21 if n(r["status"]) == "auto_clear"), 240)
chk("v2.1 status review", sum(1 for r in v21 if n(r["status"]) == "review"), 24)
chk("v2.1 status escalate", sum(1 for r in v21 if n(r["status"]) == "escalate"), 36)
chk("v2.1 risiko low/medium/high/fraud",
    tuple(sum(1 for r in v21 if n(r["risiko"]) == x) for x in ("low","medium","high","fraud")),
    (240,10,14,36))
chk("v2.1 nominal auto_clear", sum(int(n(r["biaya_rp"])) for r in v21 if n(r["status"])=="auto_clear"), 2685550000)
chk("v2.1 nominal review", sum(int(n(r["biaya_rp"])) for r in v21 if n(r["status"])=="review"), 279950000)
chk("v2.1 nominal escalate", sum(int(n(r["biaya_rp"])) for r in v21 if n(r["status"])=="escalate"), 561150000)

print("\n" + "=" * 60)
bad = [c for c in CHECKS if not c[0]]
print(f"TOTAL CHECK: {len(CHECKS)} | OK: {len(CHECKS)-len(bad)} | GAGAL: {len(bad)}")
for b in bad: print("   GAGAL:", b[1], "got=", b[2], "exp=", b[3])
