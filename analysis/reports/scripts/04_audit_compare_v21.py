#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Perbandingan: dump Notion (analysis/corpus/claims_v2_live.csv) vs
claims_300_v2.1.csv (repo mechine-learning-deep-learning).

Fokus: konformitas data & konsistensi numerik antar dua sumber.
"""
import csv, os, re, sys, json, hashlib
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")

NOTION = r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv"
V21 = r"N:\HEALTHKATHON\mechine-learning-deep-learning\datasets\claims_300_v2.1.csv"

def h(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)
def n(v): return "" if v is None else str(v).strip()

notion = list(csv.DictReader(open(NOTION, encoding="utf-8-sig", newline="")))
v21 = list(csv.DictReader(open(V21, encoding="utf-8-sig", newline="")))

h("0. JEJAK SUMBER")
for p in (NOTION, V21):
    b = open(p, "rb").read()
    print(f"   {os.path.basename(p)}")
    print(f"      sha256 = {hashlib.sha256(b).hexdigest()}")
    print(f"      bytes  = {len(b)}")

h("1. HEADER & BARIS")
print("   Notion :", len(notion), "baris,", len(notion[0]), "kolom")
print("   v2.1   :", len(v21), "baris,", len(v21[0]), "kolom")
print("   header v2.1:")
for c in v21[0].keys():
    print("      -", c)

h("2. KUNCI BARIS")
nk = [r["Name"] for r in notion]
vk = [r.get("claim_id", "") for r in v21]
print("   Notion Name unik:", len(set(nk)), "| v2.1 claim_id unik:", len(set(vk)))
print("   claim_id v2.1 contoh:", vk[:3], "...", vk[-3:])
print("   pola claim_id:", "KLM###" if all(re.fullmatch(r"KLM\d{3}", x) for x in vk) else "LAIN")
print("   urutan claim_id terurut menaik:", vk == sorted(vk))
print("   himpunan claim_id == himpunan Name:",
      set(vk) == set(nk))
only_v = sorted(set(vk) - set(nk)); only_n = sorted(set(nk) - set(vk))
print("   hanya di v2.1:", only_v[:10], "hanya di Notion:", only_n[:10])

# index v2.1 by claim_id
V = {n(r.get("claim_id")): r for r in v21}
N = {n(r["Name"]): r for r in notion}
common = sorted(set(N) & set(V))

h("3. PETA KOLOM NOTION -> KOLOM v2.1")
MAP = {
    "Name": "claim_id", "Tanggal": "tanggal", "Pasien": "pasien_raw",
    "Dokter": "dokter_raw", "Faskes": "faskes_id", "Diagnosis ICD-10": "diagnosis_raw",
    "Prosedur ICD-9-CM": "prosedur_raw", "Obat": "obat", "LOS hari": "los_hari",
    "Biaya Rp": "biaya_rp", "Narasi Rekam Medis": "narasi_rekam_medis",
    "Kontradiksi Narasi": "kontradiksi_narasi", "Skor Fraud": "skor_fraud",
    "Risiko": "risiko", "Status": "status", "Modus": "modus", "Sindikat": "sindikat",
    "Alasan": "alasan", "Sinyal SHAP": "sinyal_shap",
    "Kontribusi Saluran": "kontribusi_saluran", "Skor Sentimen": "skor_sentimen",
    "Sentimen": "sentimen", "Umpan Balik Pasien": "umpan_balik_pasien",
    "Alasan Berobat": "alasan_berobat", "Layanan": "layanan", "Rujukan": "rujukan",
}

def norm_num(s):
    s = n(s)
    try: return f"{float(s):.6f}"
    except Exception: return s

def cmp_col(nk_, vk_, numeric=False):
    diffs = []
    for cid in common:
        a, b = n(N[cid][nk_]), n(V[cid][vk_])
        if numeric:
            a, b = norm_num(a), norm_num(b)
        if a != b:
            diffs.append((cid, a, b))
    return diffs

h("4. PERBANDINGAN PER KOLOM (300 baris)")
print(f"   {'kolom Notion':<24} {'kolom v2.1':<22} {'sama':>5} {'beda':>5}  contoh")
for nk_, vk_ in MAP.items():
    numeric = nk_ in ("Skor Fraud", "Skor Sentimen", "Biaya Rp", "LOS hari")
    d = cmp_col(nk_, vk_, numeric)
    flag = "OK" if not d else "BEDA"
    ex = ""
    if d:
        c, a, b = d[0]
        ex = f"{c}: notion={a!r} v21={b!r}" + (f" (+{len(d)-1} lain)" if len(d) > 1 else "")
    print(f"   {nk_:<24} {vk_:<22} {300-len(d):>5} {len(d):>5}  {flag} {ex}")

h("5. KOLOM HANYA DI v2.1")
onlyv = [c for c in v21[0] if c not in MAP.values()]
print("   ", onlyv)
for c in onlyv:
    vals = [n(r[c]) for r in v21]
    uniq = Counter(vals)
    print(f"   {c}: {len(uniq)} nilai unik; contoh {list(uniq.items())[:5]}")

h("6. SKOR 0,80 / KLM115 (kasus pembeda ambang)")
for cid in ("KLM115",):
    print(f"   Notion: skor={n(N[cid]['Skor Fraud'])} risiko={n(N[cid]['Risiko'])} status={n(N[cid]['Status'])} sindikat={n(N[cid]['Sindikat'])} modus={n(N[cid]['Modus'])}")
    v = V[cid]
    print(f"   v2.1  : skor={n(v['skor_fraud'])} risiko={n(v['risiko'])} status={n(v['status'])} is_fraud={n(v.get('is_fraud'))} sindikat={n(v['sindikat'])} modus={n(v['modus'])}")
edges = sorted({n(r['Skor Fraud']) for r in notion if 0.30 <= float(n(r['Skor Fraud'])) <= 0.85})
print("   skor di Notion dalam [0.30,0.85]:", edges)
print("   baris tepat di setiap ambang (Notion):")
for thr in (0.35, 0.60, 0.80):
    ids = [r["Name"] for r in notion if float(n(r["Skor Fraud"])) == thr]
    ids21 = [cid for cid in common if norm_num(V[cid]["skor_fraud"]) == f"{thr:.6f}"]
    print(f"      {thr}: Notion {ids} | v2.1 {ids21}")

h("7. ATURAN LOS")
for label, rows_, key in (("Notion", notion, "LOS hari"), ("v2.1", v21, "los_hari")):
    vals = [n(r[key]) for r in rows_]
    print(f"   {label}: kosong={sum(1 for v in vals if v=='')} | '0'={sum(1 for v in vals if v=='0')} | >0={sum(1 for v in vals if v not in ('','0'))} | unik={len(set(vals))}")
lz = [cid for cid in common if n(V[cid]["los_hari"]) != n(N[cid]["LOS hari"])]
print("   baris los_hari berbeda Notion vs v2.1:", len(lz), lz[:10])
# LOS=0 + layanan
for label, rows_, klos, klay in (("Notion", notion, "LOS hari", "Layanan"), ("v2.1", v21, "los_hari", "layanan")):
    c = Counter(n(r[klay]) for r in rows_ if n(r[klos]) == "0")
    print(f"   {label}: LOS=0 per layanan -> {dict(c)}")
    inap = sorted((r.get("claim_id") or r.get("Name")) for r in rows_
                  if n(r[klos]) == "0" and n(r[klay]) == "rawat inap")
    print(f"      rawat inap dengan LOS=0: {inap}")

h("8. IS_FRAUD vs RISIKO==fraud")
print("   v2.1 nilai is_fraud:", Counter(n(r["is_fraud"]) for r in v21))
mis = [cid for cid in common if (n(V[cid]["is_fraud"]).lower() in ("true","1","ya","yes"))
       != (n(N[cid]["Risiko"]) == "fraud")]
print("   baris is_fraud != (risiko==fraud) di Notion:", len(mis), mis[:20])
mis2 = [cid for cid in common if (n(V[cid]["is_fraud"]).lower() in ("true","1","ya","yes"))
        != (n(V[cid]["risiko"]) == "fraud")]
print("   baris is_fraud != (risiko==fraud) di v2.1 internal:", len(mis2), mis2[:20])

h("9. KONTRIBUSI SALURAN: Skor vs T+F+S")
def tfs(r, key="Kontribusi Saluran"):
    return tuple(float(x) for x in re.findall(r"[TFS] ([-\d.]+)", n(r[key])))
for label, rows_, ksk, kkan in (("Notion", notion, "Skor Fraud", "Kontribusi Saluran"),
                                ("v2.1", v21, "skor_fraud", "kontribusi_saluran")):
    nc = []
    for r in rows_:
        try: s = sum(tfs(r, kkan))
        except Exception: continue
        sk = float(n(r[ksk]))
        if abs(s - sk) > 1e-9: nc.append((r.get("Name") or r.get("claim_id"), round(sk - s, 3)))
    print(f"   {label}: tidak koinciden {len(nc)} baris; selisih min={min(x[1] for x in nc):+.3f} maks={max(x[1] for x in nc):+.3f}")
    print(f"      >0.02 (abs): {sum(1 for x in nc if abs(x[1])>0.02)}")

h("10. SINDIKAT & MODUS")
for label, rows_, ks, km in (("Notion", notion, "Sindikat", "Modus"), ("v2.1", v21, "sindikat", "modus")):
    print(f"   {label}: sindikat kosong={sum(1 for r in rows_ if not n(r[ks]))} terisi={sum(1 for r in rows_ if n(r[ks]))} modus kosong={sum(1 for r in rows_ if not n(r[km]))} terisi={sum(1 for r in rows_ if n(r[km]))}")
    print(f"      sindikat distinct: {sorted(Counter(n(r[ks]) for r in rows_ if n(r[ks])).items())}")
sd = [cid for cid in common if n(N[cid]["Sindikat"]) != n(V[cid]["sindikat"])]
md = [cid for cid in common if n(N[cid]["Modus"]) != n(V[cid]["modus"])]
print("   sindikat berbeda:", len(sd), sd[:10])
print("   modus berbeda:", len(md), md[:10])
# baris fraud tanpa sindikat
print("   Notion fraud tanpa sindikat:", sorted(r["Name"] for r in notion if n(r["Risiko"])=="fraud" and not n(r["Sindikat"])))
print("   v2.1  fraud tanpa sindikat:", sorted(r["claim_id"] for r in v21 if n(r["risiko"])=="fraud" and not n(r["sindikat"])))
# entitas sindikat per CSV v2.1 (pakai *_id)
print("\n   Entitas per sindikat di v2.1 (dari *_id, bukan rich text):")
ent = defaultdict(lambda: defaultdict(set))
for r in v21:
    s = n(r["sindikat"])
    if s:
        ent[s]["faskes"].add(n(r["faskes_id"]))
        ent[s]["dokter"].add(n(r["dokter_id"]))
        ent[s]["pasien"].add(n(r["pasien_id"]))
for s in sorted(ent):
    sc = [float(n(r["skor_fraud"])) for r in v21 if n(r["sindikat"]) == s]
    print(f"      {s}: faskes={sorted(ent[s]['faskes'])} dokter={sorted(ent[s]['dokter'])} pasien={sorted(ent[s]['pasien'])} skor={min(sc):.2f}-{max(sc):.2f} n={len(sc)}")
print("   v2.1 baris tanpa sindikat tapi risiko fraud:")
for r in v21:
    if n(r["risiko"])=="fraud" and not n(r["sindikat"]):
        print(f"      {r['claim_id']}: faskes={n(r['faskes_id'])} dokter={n(r['dokter_id'])} pasien={n(r['pasien_id'])} modus={n(r['modus'])} skor={n(r['skor_fraud'])}")

h("11. KONTRADIKSI NARASI / RUJUKAN 'undefined' / SENTINEL '—' / SHAP KONSTAN")
for label, rows_, kk, kr, kp, ko, km2, ksh in (
        ("Notion", notion, "Kontradiksi Narasi", "Rujukan", "Prosedur ICD-9-CM", "Obat", "Modus", "Sinyal SHAP"),
        ("v2.1", v21, "kontradiksi_narasi", "rujukan", "prosedur_raw", "obat", "modus", "sinyal_shap")):
    print(f"   {label}:")
    print(f"      Kontradiksi True = {sum(1 for r in rows_ if n(r[kk]).lower() in ('true','1','ya'))}")
    print(f"      Rujukan berisi 'undefined' = {sum(1 for r in rows_ if 'undefined' in n(r[kr]).lower())}")
    print(f"      Prosedur sentinel '—' = {sum(1 for r in rows_ if n(r[kp]) in ('—','-','–'))}")
    print(f"      Obat sentinel '—' = {sum(1 for r in rows_ if n(r[ko]) in ('—','-','–'))}")
    sh = defaultdict(set)
    for r in rows_:
        m = n(r[km2])
        if m: sh[m].add(n(r[ksh]))
    konstan = sorted(k for k, v in sh.items() if len(v) == 1)
    print(f"      modus dengan SHAP konstan = {len(konstan)}/{len(sh)}")

h("12. NILAI TAMBAHAN v2.1: *_id vs prefiks rich text Notion")
mm = []
for cid in common:
    a = n(N[cid]["Pasien"]).split(" (")[0]
    b = n(V[cid]["pasien_id"])
    if a != b: mm.append((cid, a, b))
print("   pasien_id (v2.1) vs prefiks Pasien (Notion): beda", len(mm), mm[:10])
mm2 = []
for cid in common:
    a = n(N[cid]["Dokter"]).split(" (")[0]
    b = n(V[cid]["dokter_id"])
    if a != b: mm2.append((cid, a, b))
print("   dokter_id (v2.1) vs prefiks Dokter (Notion): beda", len(mm2), mm2[:10])
mm3 = [(cid, n(N[cid]["Faskes"]), n(V[cid]["faskes_id"])) for cid in common if n(N[cid]["Faskes"]) != n(V[cid]["faskes_id"])]
print("   faskes_id (v2.1) vs Faskes (Notion): beda", len(mm3), mm3[:10])
# entitas unik
print("   entitas unik di v2.1: pasien", len({n(r['pasien_id']) for r in v21}),
      "| dokter", len({n(r['dokter_id']) for r in v21}),
      "| faskes", len({n(r['faskes_id']) for r in v21}))
# diagnosis_code vs prefiks
mmd = [(cid, n(N[cid]["Diagnosis ICD-10"]).split(" - ")[0], n(V[cid]["diagnosis_code"]))
       for cid in common if n(N[cid]["Diagnosis ICD-10"]).split(" - ")[0] != n(V[cid]["diagnosis_code"])]
print("   diagnosis_code vs prefiks diagnosis Notion: beda", len(mmd), mmd[:5])
mmp = [(cid, n(N[cid]["Prosedur ICD-9-CM"]).split(" - ")[0], n(V[cid]["prosedur_code"]))
       for cid in common if n(N[cid]["Prosedur ICD-9-CM"]).split(" - ")[0] != n(V[cid]["prosedur_code"])]
print("   prosedur_code vs prefiks prosedur Notion: beda", len(mmp), mmp[:8])

h("13. RINGKASAN TABEL PERBANDINGAN")
print("   kolom v2.1 yang tidak ada di dump Notion:", onlyv)
print("   baris yang TIDAK identik di seluruh kolom terpetakan:")
tot = 0
for nk_, vk_ in MAP.items():
    numeric = nk_ in ("Skor Fraud", "Skor Sentimen", "Biaya Rp", "LOS hari")
    d = cmp_col(nk_, vk_, numeric)
    tot += len(d)
print("      total sel berbeda:", tot)

h("14. KONSISTENSI SEMANTIK (per_baris, bukan per_kolom)")
# 14a. kontradiksi narasi: True/False vs 1/0
def truth(v):
    v = n(v).lower()
    if v in ("true", "1", "ya", "yes"): return True
    if v in ("false", "0", "tidak", "no", ""): return False
    return None
kbad = [cid for cid in common
        if truth(N[cid]["Kontradiksi Narasi"]) != truth(V[cid]["kontradiksi_narasi"])]
print("   14a. Kontradiksi Narasi semantik beda:", len(kbad), kbad[:10])
print("       True di Notion:", sum(1 for r in notion if truth(r["Kontradiksi Narasi"])),
      "| '1' di v2.1:", sum(1 for r in v21 if truth(r["kontradiksi_narasi"])))
# 14b. sindikat: '' vs 'none'
none_ids = sorted(r["claim_id"] for r in v21 if n(r["sindikat"]) == "none")
nt_empty = sorted(r["Name"] for r in notion if not n(r["Sindikat"]))
print("   14b. sindikat 'none' di v2.1:", len(none_ids), "| Sindikat kosong di Notion:", len(nt_empty),
      "| himpunan sama:", set(none_ids) == set(nt_empty))
print("       fraud tanpa sindikat di v2.1 (memakai 'none'):",
      sorted(r["claim_id"] for r in v21 if n(r["risiko"]) == "fraud" and n(r["sindikat"]) == "none"))
print("       entitas sindikat 'none' per klaim fraud:")
for r in v21:
    if n(r["risiko"]) == "fraud" and n(r["sindikat"]) == "none":
        print(f"          {r['claim_id']}: faskes={n(r['faskes_id'])} dokter={n(r['dokter_id'])} "
              f"pasien={n(r['pasien_id'])} modus={n(r['modus'])} skor={n(r['skor_fraud'])}")
# 14c. baris bermasalah: apakah baris yang sama di kedua sumber?
def ids_pred(rows_, key, pred):
    return sorted((r.get("Name") or r.get("claim_id")) for r in rows_ if pred(r))
pairs = [
    ("LOS=0", lambda r: n(r["los_hari"]) == "0", lambda r: n(r["LOS hari"]) == "0"),
    ("Rujukan 'undefined'", lambda r: "undefined" in n(r["rujukan"]).lower(),
     lambda r: "undefined" in n(r["Rujukan"]).lower()),
    ("Prosedur sentinel —", lambda r: n(r["prosedur_raw"]) == "—", lambda r: n(r["Prosedur ICD-9-CM"]) == "—"),
    ("Obat sentinel —", lambda r: n(r["obat"]) == "—", lambda r: n(r["Obat"]) == "—"),
    ("Skor!=T+F+S", lambda r: abs(sum(tfs(r, "kontribusi_saluran")) - float(n(r["skor_fraud"]))) > 1e-9,
     lambda r: abs(sum(tfs(r)) - float(n(r["Skor Fraud"]))) > 1e-9),
    ("Alasan kosong", lambda r: n(r["alasan"]) == "", lambda r: n(r["Alasan"]) == ""),
    ("Modus kosong", lambda r: n(r["modus"]) == "", lambda r: n(r["Modus"]) == ""),
]
print("   14c. apakah baris bermasalah SAMA di kedua sumber?")
for name, pv, pn in pairs:
    a, b = ids_pred(v21, None, pv), ids_pred(notion, None, pn)
    print(f"      {name:<24} v2.1={len(a):>3} notion={len(b):>3} himpunan_sama={set(a)==set(b)}"
          + ("" if set(a) == set(b) else f"  beda: {sorted(set(a)^set(b))[:8]}"))

h("15. TRUNCASI dokter_raw")
tr = [(r["claim_id"], n(r["dokter_raw"])) for r in v21
      if n(r["dokter_raw"]) != n(N[r["claim_id"]]["Dokter"])]
print("   baris terpotong:", len(tr))
print("   panjang nilai terpotong:", sorted({len(v) for _, v in tr}))
print("   prefiks nama yang terpotong:", sorted({v[:3] for _, v in tr}))
for c, v in tr[:3]:
    print(f"      {c}: {v!r} (len={len(v)}) vs Notion {n(N[c]['Dokter'])!r}")
# apakah ada kolom lain yang terpotong (bandingkan panjang maks)
print("   cek kolom rich text lain: apakah ada nilai v2.1 yang merupakan prefix dari Notion?")
for nk_, vk_ in MAP.items():
    if nk_ in ("Dokter",): continue
    pref = [(cid, n(V[cid][vk_]), n(N[cid][nk_])) for cid in common
            if n(V[cid][vk_]) != n(N[cid][nk_]) and n(N[cid][nk_]).startswith(n(V[cid][vk_])) and n(V[cid][vk_])]
    if pref:
        print(f"      {nk_}: {len(pref)} baris terpotong, contoh {pref[0]}")
# apakah truncation juga terjadi di claims_db.json / dataset_db.json?
import os
for fn in ("claims_db.json", "dataset_db.json"):
    p = os.path.join(os.path.dirname(V21), fn)
    if not os.path.exists(p): continue
    txt = open(p, encoding="utf-8", errors="replace").read()
    print(f"      {fn}: berisi 'Danur Wibisono, ' = {txt.count('Danur Wibisono, ')} kemunculan; "
          f"'Danur Wibisono, Sp.JP' = {txt.count('Danur Wibisono, Sp.JP')}")

h("16. STRUKTUR v2.1 UNTUK EVALUASI GRUP")
print("   claim_id urut menaik & unik:", [r["claim_id"] for r in v21] == sorted(set(r["claim_id"] for r in v21)))
print("   sumbu grup yang tersedia: pasien_id (40), faskes_id (10), dokter_id (20)")
gc = Counter(r["pasien_id"] for r in v21)
fc = Counter(r["faskes_id"] for r in v21)
dc = Counter(r["dokter_id"] for r in v21)
print(f"   klaim per pasien_id: min={min(gc.values())} maks={max(gc.values())} median={sorted(gc.values())[len(gc)//2]}")
print(f"   klaim per faskes_id : min={min(fc.values())} maks={max(fc.values())}")
print(f"   klaim per dokter_id : min={min(dc.values())} maks={max(dc.values())}")
print("  _overlap pasien_id x faskes_id (apakah pasien selalu di 1 faskes?):")
pf = defaultdict(set)
for r in v21: pf[r["pasien_id"]].add(r["faskes_id"])
print("      pasien di >1 faskes:", sum(1 for k, v in pf.items() if len(v) > 1))
pd_ = defaultdict(set)
for r in v21: pd_[r["dokter_id"]].add(r["faskes_id"])
print("      dokter di >1 faskes:", sum(1 for k, v in pd_.items() if len(v) > 1))
# Leakage: apakah skor_fraud == is_fraud deterministik?
print("   is_fraud deterministik dari risiko:",
      all(truth(r["is_fraud"]) == (n(r["risiko"]) == "fraud") for r in v21))
# apakah ada kolom label-leak di v2.1
print("   kolom v2.1 yang memuat label:", [c for c in v21[0] if c in
      ("risiko", "status", "is_fraud", "sindikat", "modus", "sinyal_shap",
       "kontribusi_saluran", "alasan", "skor_fraud")])
