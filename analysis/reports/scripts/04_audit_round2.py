#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit ronde 2: pendalaman temuan 04_audit.py."""
import csv, json, os, re, statistics, sys
from collections import Counter, defaultdict
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
rows = list(csv.DictReader(open(os.path.join(CORPUS, "claims_v2_live.csv"),
                                encoding="utf-8-sig", newline="")))
jrows = json.load(open(os.path.join(CORPUS, "claims_v2_live.json"), encoding="utf-8"))
n = lambda v: "" if v is None else str(v).strip()

def h(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# ---- A. LOS: kosong vs nol, CSV vs JSON
h("A. LOS: KOSONG atau NOL? (CSV vs JSON)")
csv_los_empty = [r["Name"] for r in rows if n(r["LOS hari"]) == ""]
csv_los_zero = [r["Name"] for r in rows if n(r["LOS hari"]) == "0"]
json_null = [j["Name"] for j in jrows if j.get("LOS hari") is None]
json_zero = [j["Name"] for j in jrows if j.get("LOS hari") == 0]
print(f"CSV LOS kosong (string ''): {len(csv_los_empty)}")
print(f"CSV LOS == '0'            : {len(csv_los_zero)}")
print(f"JSON LOS null             : {len(json_null)}")
print(f"JSON LOS == 0 (numerik)   : {len(json_zero)}")
print("-> 109 pada klaim = baris LOS bernilai 0, BUKAN sel kosong.")
by_lay = Counter(n(r["Layanan"]) for r in rows if n(r["LOS hari"]) == "0")
print("LOS=0 menurut Layanan:", dict(by_lay))
print("LOS>0 pada rawat jalan:", [(r["Name"], n(r["LOS hari"])) for r in rows
      if n(r["Layanan"]) == "rawat jalan" and n(r["LOS hari"]) not in ("", "0")])
print("LOS=0 pada rawat inap  :", [(r["Name"], n(r["Diagnosis ICD-10"]).split(" - ")[0],
      n(r["Prosedur ICD-9-CM"]).split(" - ")[0]) for r in rows
      if n(r["Layanan"]) == "rawat inap" and n(r["LOS hari"]) == "0"])

# ---- B. Sindikat x Risiko
h("B. SINDIKAT x RISIKO / STATUS")
sr = Counter((n(r["Sindikat"]) or "-", n(r["Risiko"])) for r in rows if n(r["Sindikat"]))
for k, v in sorted(sr.items()): print(f"   {k[0]:<10} {k[1]:<7} {v}")
fraud_no_synd = [(r["Name"], n(r["Modus"]), n(r["Skor Fraud"])) for r in rows
                 if n(r["Risiko"]) == "fraud" and not n(r["Sindikat"])]
print("Klaim fraud TANPA Sindikat:", fraud_no_synd)
sind_nonfraud = [(r["Name"], n(r["Sindikat"]), n(r["Risiko"]), n(r["Status"])) for r in rows
                 if n(r["Sindikat"]) and n(r["Risiko"]) != "fraud"]
print("Klaim BER-Sindikat tapi Risiko != fraud:", sind_nonfraud)
print("Total baris ber-Sindikat:", sum(1 for r in rows if n(r["Sindikat"])))
print("Total baris Risiko=fraud:", sum(1 for r in rows if n(r["Risiko"]) == "fraud"))

# ---- C. Klaim ID sindikat v2.1 vs aktual
h("C. SEBARAN ID KLAIM PER SINDIKAT (vs tabel 10-simulation-dataset.md)")
DOC_SYND = {"SYND-01": ("KLM001-003","RS_A","Upcoding"), "SYND-02": ("KLM004-006","RS_C","Phantom Billing"),
            "SYND-03": ("KLM007-012","RS_B","Unbundling"), "SYND-04": ("KLM013-014","RS_E","Drug Diversion"),
            "SYND-05": ("KLM016-017","RS_F","Cloning"), "SYND-06": ("KLM101-104","RS_G","Repeat Billing"),
            "SYND-07": ("KLM105-108","RS_H","Iur Biaya"), "SYND-08": ("KLM109-114","RS_I","Readmission Berulang"),
            "SYND-09": ("KLM115-120","RS_J","Excessive Usage")}
for s, (ids, fsk, mod) in sorted(DOC_SYND.items()):
    grp = [r for r in rows if n(r["Sindikat"]) == s]
    actual_ids = sorted(r["Name"] for r in grp)
    fakes = sorted(set(n(r["Faskes"]) for r in grp))
    docs = sorted(set(n(r["Dokter"]).split(" (")[0] for r in grp))
    pats = sorted(set(n(r["Pasien"]).split(" (")[0] for r in grp))
    modes = sorted(set(n(r["Modus"]) for r in grp))
    scores = [float(n(r["Skor Fraud"])) for r in grp]
    exp_lo, exp_hi = DOC_SYND_R = None, None
    print(f"\n{s}  doc: {ids} / {fsk} / {mod}")
    print(f"   aktual ID : {actual_ids}")
    print(f"   aktual fsk: {fakes} (doc {fsk})  dokter: {docs}  pasien: {pats}")
    print(f"   modus     : {modes}   skor: {min(scores):.2f}-{max(scores):.2f}")
    print(f"   label     : {dict(Counter(n(r['Risiko']) for r in grp))}")

# ---- D. Alasan: isi untuk rawat jalan LOS 0 & baris tanpa prosedur
h("D. ISI 'ALASAN' UNTUK BARIS LOS=0 DAN BARIS TANPA PROSEDUR")
rj = [r for r in rows if n(r["Layanan"]) == "rawat jalan" and n(r["LOS hari"]) == "0"][0]
print("CONTOH rawat jalan LOS=0 ->", rj["Name"], "\n   ", n(rj["Alasan"])[:600])
nopro = [r for r in rows if n(r["Prosedur ICD-9-CM"]) in ("", "—")][0]
print("\nCONTOH tanpa prosedur ->", nopro["Name"], "\n   ", n(nopro["Alasan"])[:600])
print("\nBaris tanpa prosedur:", sum(1 for r in rows if n(r["Prosedur ICD-9-CM"]) in ("", "—")))
print("Alasan pada baris tanpa prosedur mengandung frasa 'ditindaki':",
      sum(1 for r in rows if n(r["Prosedur ICD-9-CM"]) in ("", "—") and "ditindaki" in n(r["Alasan"])))
print("Alasan pada baris LOS=0 mengandung 'LOS 0 hari':",
      sum(1 for r in rows if n(r["LOS hari"]) == "0" and "LOS 0 hari" in n(r["Alasan"])))
print("Contoh frasa LOS pada baris LOS=0:")
for r in [x for x in rows if n(x["LOS hari"]) == "0"][:3]:
    m = re.search(r"LOS[^;]*", n(r["Alasan"]))
    print("   ", r["Name"], "|", m.group(0) if m else "(tidak ada frasa LOS)")

# ---- E. Verifikasi 'rasio' di Alasan terhadap tarif acuan 10-simulation-dataset.md
h("E. VERIFIKASI ANGKA DI DALAM 'ALASAN' (rasio biaya, median LOS)")
TARIF = {"51.23": 14500000, "00.66": 58000000, "36.13": 78000000, "47.09": 6800000, "53.1": 8200000,
         "74.1": 6200000, "81.52": 46500000, "96.04": 750000, "93.90": 640000, "98.51": 5600000}
bad_ratio, checked = [], 0
for r in rows:
    code = n(r["Prosedur ICD-9-CM"]).split(" - ")[0]
    m = re.search(r"rasio\s+([\d.,]+)", n(r["Alasan"]))
    if m and code in TARIF:
        claimed = float(m.group(1).replace(".", "").replace(",", "."))
        actual = int(n(r["Biaya Rp"])) / TARIF[code]
        checked += 1
        if abs(claimed - actual) > 0.02:
            bad_ratio.append((r["Name"], code, claimed, round(actual, 3)))
print(f"Baris dengan klaim 'rasio X' diverifikasi terhadap tarif acuan: {checked}")
print(f"Rasio tidak cocok (>0,02): {len(bad_ratio)}")
for b in bad_ratio[:20]: print("   ", b)

# median LOS per dx, bandingkan dengan 'median pneumonia 5 hari' dsb
los_by_dx = defaultdict(list)
for r in rows:
    if n(r["LOS hari"]) not in ("", "0"):
        los_by_dx[n(r["Diagnosis ICD-10"]).split(" - ")[0]].append(int(n(r["LOS hari"])))
print("\nMedian LOS (baris LOS>0) per diagnosis:")
for k in sorted(los_by_dx):
    print(f"   {k}: n={len(los_by_dx[k])} median={statistics.median(los_by_dx[k])} "
          f"min={min(los_by_dx[k])} max={max(los_by_dx[k])}")
claims_median = [(r["Name"], m.group(0)) for r in rows
                 for m in [re.search(r"median\s+\w+\s*:?\s*\d+\s*hari", n(r["Alasan"]))]
                 if m]
print("\nKlaim median di Alasan:", claims_median)

# ---- F. Tanggal vs Rujukan vs urutan
h("F. TANGGAL, RUJUKAN, URUTAN")
ruj_future = []
for r in rows:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", n(r["Rujukan"]))
    if m and m.group(1) > n(r["Tanggal"]):
        ruj_future.append((r["Name"], n(r["Tanggal"]), m.group(1)))
print("Tanggal klaim SEBELUM tanggal rujukan:", ruj_future)
ids_sorted = [r["Name"] for r in rows]
tang = [n(r["Tanggal"]) for r in rows]
print("Baris terurut menaik menurut Tanggal?", tang == sorted(tang))
print("Baris terurut menaik menurut Name?  ", ids_sorted == sorted(ids_sorted))
print("Contoh urutan tidak menaik:", [(ids_sorted[i], tang[i], ids_sorted[i+1], tang[i+1])
                                     for i in range(len(tang)-1) if tang[i] > tang[i+1]][:5])
print("Tanggal unik:", len(set(tang)), "| rentang:", min(tang), "..", max(tang))
print("'_last_edited' unik:", dict(Counter(n(r["_last_edited"]) for r in rows)))
# rujukan duplikat
rj_c = Counter(n(r["Rujukan"]) for r in rows)
print("Nilai Rujukan duplikat:", [(k, v) for k, v in rj_c.items() if v > 1][:10])
undef = sorted(r["Name"] for r in rows if "undefined" in n(r["Rujukan"]).lower())
print(f"\nBaris 'undefined' pada Rujukan: {len(undef)}")
print(undef)
print("Dari 300 baris, 'kunjungan langsung (tanpa rujukan)':",
      sum(1 for r in rows if "kunjungan langsung" in n(r["Rujukan"])))

# ---- G. Outlier biaya per grup dx/prosedur (lebih bermakna)
h("G. OUTLIER BIAYA DALAM GRUP (dx+prosedur+layanan)")
grp = defaultdict(list)
for r in rows:
    key = (n(r["Diagnosis ICD-10"]).split(" - ")[0], n(r["Prosedur ICD-9-CM"]).split(" - ")[0])
    grp[key].append((int(n(r["Biaya Rp"])), r["Name"], n(r["Risiko"]), n(r["Layanan"])))
for key in sorted(grp):
    v = grp[key]
    if len(v) < 4: continue
    vals = sorted(x[0] for x in v)
    q1 = statistics.quantiles(vals, n=4)[0]; q3 = statistics.quantiles(vals, n=4)[2]
    iqr = q3 - q1
    hi = q3 + 1.5 * iqr
    out = [x for x in v if x[0] > hi]
    if out:
        print(f"   {key[0]:<8}/{key[1]:<8} n={len(v)} Q1={q1:,.0f} Q3={q3:,.0f} pagar={hi:,.0f}")
        for o in sorted(out, key=lambda x: -x[0]):
            print(f"        {o[1]}  Rp{o[0]:,}  risiko={o[2]} layanan={o[3]}")

# ---- H. Baris tanpa prosedur:apakah sesuai "Pasangan klinis" yang diklaim
h("H. PASANGAN KLINIS UNTUK BARIS TANPA PROSEDUR (dx -> '-')")
tbp = [r for r in rows if n(r["Prosedur ICD-9-CM"]) in ("", "—")]
c = Counter(n(r["Diagnosis ICD-10"]).split(" - ")[0] for r in tbp)
print("Diagnosis pada baris tanpa prosedur:", dict(c))
print("Layanan:", dict(Counter(n(r["Layanan"]) for r in tbp)))
print("Alasan pada 3 baris tanpa prosedur:")
for r in tbp[:3]: print("   ", r["Name"], "|", n(r["Alasan"])[:200])

# ---- I. Kloning: KLM016/017
h("I. KLAIM KLONING (SYND-05 = KLM016-017)")
for nm in ("KLM016", "KLM017"):
    r = [x for x in rows if x["Name"] == nm][0]
    print(f"   {nm}: tanggal={n(r['Tanggal'])} pasien={n(r['Pasien'])} dokter={n(r['Dokter'])} "
          f"faskes={n(r['Faskes'])} dx={n(r['Diagnosis ICD-10'])} proc={n(r['Prosedur ICD-9-CM'])} "
          f"LOS={n(r['LOS hari'])} biaya={n(r['Biaya Rp'])}")
a = [x for x in rows if x["Name"] == "KLM016"][0]; b = [x for x in rows if x["Name"] == "KLM017"][0]
same = [c for c in a if n(a[c]) == n(b[c]) and c not in ("Name","_notion_page_id","_last_edited")]
diff = [c for c in a if n(a[c]) != n(b[c]) and c not in ("Name","_notion_page_id","_last_edited")]
print("   kolom yang SAMA:", same)
print("   kolom yang BEDA:", diff)

# ---- J. KLM031 detail + KLM121/122/115
h("J. DETAIL BARIS PROBLEMATIK")
for nm in ("KLM031", "KLM115", "KLM121", "KLM122", "KLM015"):
    r = [x for x in rows if x["Name"] == nm][0]
    print(f"\n--- {nm}")
    for k, v in r.items():
        if k.startswith("_"): continue
        print(f"   {k:>22}: {n(v)[:220]}")

# ---- K. Entitas: nama pasien/dokter unik & afiliasi dokter-faskes
h("K. AFILIASI DOKTER-FA SKES & KONSISTENSI NAMA")
aff = defaultdict(set)
for r in rows: aff[n(r["Dokter"]).split(" (")[0]].add(n(r["Faskes"]))
multi = {k: v for k, v in aff.items() if len(v) > 1}
print("Dokter yang terakhir di >1 faskes:", multi)
print("Jumlah pasangan (dokter,faskes):", len({(n(r['Dokter']).split(' (')[0], n(r['Faskes'])) for r in rows}))
# nama dokter unik?
dn = Counter(n(r["Dokter"]) for r in rows)
print("Nama dokter dengan >1 ejaan:", {k: v for k, v in dn.items() if v > 1})
pn = Counter(n(r["Pasien"]) for r in rows)
print("Nama pasien dengan >1 ejaan:", {k: v for k, v in pn.items() if v > 1})

# ---- L. Distribusi label untuk 100-klaim pertama (uji konsistensi dengan doc v100)
h("L. KONSISTENSI DOKUMEN v100 vs DATA AKTUAL 300")
first100 = sorted(rows, key=lambda r: int(r["Name"][3:]))[:100]
print("KLM001-100 Risiko:", dict(Counter(n(r["Risiko"]) for r in first100)))
print("KLM001-100 Sentimen:", dict(Counter(n(r["Sentimen"]) for r in first100)))
print("KLM001-100 Status:", dict(Counter(n(r["Status"]) for r in first100)))
print("dok v100: risiko 76 low/4 medium/6 high/14 fraud; sentimen 62 pos/14 net/24 neg")
print("dok v2: 36 fraud/14 high/10 medium/240 low; sentimen aktual 170 pos/58 net/72 neg")
print("jumlah klaim KLM001-KLM024 (ground truth anomali v100):",
      sum(1 for r in first100 if n(r["Risiko"]) != "low"))

# ---- M. Skor Fraud: sebaran & pola per modus
h("M. SEBARAN SKOR FRAUD PER MODUS")
by_mod = defaultdict(list)
for r in rows:
    if n(r["Modus"]): by_mod[n(r["Modus"])].append(float(n(r["Skor Fraud"])))
for k in sorted(by_mod):
    v = by_mod[k]
    print(f"   {k:<22} n={len(v):<3} min={min(v):.2f} maks={max(v):.2f}")
print("\nKorelasi Kontribusi Saluran vs Skor Fraud (per label):")
for lab in ("low","medium","high","fraud"):
    grp2 = [(r["Name"],) for r in rows if n(r["Risiko"]) == lab]
    tfs = []
    for r in rows:
        if n(r["Risiko"]) != lab: continue
        vals = {}
        for part in n(r["Kontribusi Saluran"]).split("·"):
            m = re.match(r"\s*([TFS])\s+([-\d.]+)", part)
            if m: vals[m.group(1)] = float(m.group(2))
        tfs.append((sum(vals.values()), float(n(r["Skor Fraud"])), vals))
    if len(tfs) > 2:
        print(f"   {lab}: n={len(tfs)} T+F+S range={min(t[0] for t in tfs):.2f}-{max(t[0] for t in tfs):.2f} "
              f"skor range={min(t[1] for t in tfs):.2f}-{max(t[1] for t in tfs):.2f}")
        print(f"        contoh (T,F,S)->skor: {[(t[2], t[1]) for t in tfs[:3]]}")
