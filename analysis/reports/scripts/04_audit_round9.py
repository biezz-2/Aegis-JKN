#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 9: koreksi 3 bug di final_check (urutan, ambang selisih, parsing rasio)."""
import csv, os, re, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
rows = list(csv.DictReader(open(os.path.join(CORPUS, "claims_v2_live.csv"),
                                encoding="utf-8-sig", newline="")))
n = lambda v: "" if v is None else str(v).strip()
def tfs(r): return tuple(re.findall(r"[TFS] ([-\d.]+)", n(r["K Contributors Saluran"]))) if False else \
    tuple(re.findall(r"[TFS] ([-\d.]+)", n(r["Kontribusi Saluran"])))

print("=== 1. SELISIH > 0.02 : hitung ulang beberapa ambang ===")
for thr in (0.01, 0.015, 0.02, 0.025, 0.03, 0.05):
    c = sum(1 for r in rows
            if abs(float(n(r['Skor Fraud'])) - sum(float(x) for x in tfs(r))) > thr)
    print(f"   |selisih| > {thr}: {c}")
print("   (round3 melaporkan 21 dengan ambang 0.02; periksa presisi floating point)")

print("\n=== 2. DUPLEKAT: urutan baris vs urutan terurut ===")
sig = defaultdict(list)
for r in rows:
    sig[(n(r['Tanggal']), n(r['Pasien']), n(r['Diagnosis ICD-10']),
         n(r['Prosedur ICD-9-CM']), n(r['LOS hari']), n(r['Biaya Rp']))].append(r['Name'])
for k, v in sig.items():
    if len(v) > 1:
        print(f"   urutan file : {v}")
        print(f"   terurut     : {sorted(v)}")

print("\n=== 3. RASIO: parsing benar vs parsing salah ===")
def num_id(s):
    s = s.strip().replace(" ", "").replace("x", "")
    if "," in s and "." in s: s = s.replace(".", "").replace(",", ".")
    elif "," in s: s = s.replace(",", ".")
    return float(s)
TARIF = {"51.23":14500000,"00.66":58000000,"47.09":6800000,"53.1":8200000,"74.1":6200000,
         "81.52":46500000,"96.04":750000,"98.51":5600000}
ok = bad = 0; badlist = []
for r in rows:
    c = n(r['Prosedur ICD-9-CM']).split(' - ')[0]
    m = re.search(r"rasio\s+([\d.,]+x?)", n(r['Alasan']))
    if m and c in TARIF:
        cl = num_id(m.group(1).rstrip('x'))
        act = int(n(r['Biaya Rp'])) / TARIF[c]
        if abs(act - cl) <= 0.015: ok += 1
        else:
            bad += 1; badlist.append((r['Name'], c, cl, round(act,3)))
print(f"   parsing BENAR  -> cocok={ok} tidak_cocok={bad} {badlist}")
# parsing salah (khas bug final_check)
ok2 = bad2 = 0
for r in rows:
    c = n(r['Prosedur ICD-9-CM']).split(' - ')[0]
    m = re.search(r"rasio\s+([\d.,]+x?)", n(r['Alasan']))
    if m and c in TARIF:
        s = m.group(1).rstrip('x').replace('.', '').replace(',', '.')
        act = int(n(r['Biaya Rp'])) / TARIF[c]
        if abs(act - float(s)) <= 0.015: ok2 += 1
        else: bad2 += 1
print(f"   parsing SALAH -> cocok={ok2} tidak_cocok={bad2}  (that's the final_check bug)")

print("\n=== 4. SEBARAN SELISIH untuk menentukan ambang > 0.02 yang benar ===")
diffs = sorted((round(float(n(r['Skor Fraud'])) - sum(float(x) for x in tfs(r)), 4), r['Name'])
               for r in rows)
nz = [(d, i) for d, i in diffs if abs(d) > 1e-9]
print(f"   total tidak koinciden: {len(nz)}")
print("   nilai absolut di sekitar 0.02:")
for d, i in nz:
    if 0.015 <= abs(d) <= 0.045: print(f"      {i}: {d:+.4f}")
print(f"   count |d|>0.02 : {sum(1 for d,_ in nz if abs(d)>0.02)}")
print(f"   count |d|>0.015: {sum(1 for d,_ in nz if abs(d)>0.015)}")
print(f"   count |d|>0.025: {sum(1 for d,_ in nz if abs(d)>0.025)}")
