#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifikasi akhir: setiap angka yang dikutip di 04-data-quality.md dicek ulang."""
import csv, os, re, statistics, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
rows = list(csv.DictReader(open(os.path.join(CORPUS, "claims_v2_live.csv"),
                                encoding="utf-8-sig", newline="")))
n = lambda v: "" if v is None else str(v).strip()
def tfs(r): return tuple(re.findall(r"[TFS] ([-\d.]+)", n(r["Kontribusi Saluran"])))
def band(s):
    return "low" if s < 0.35 else "medium" if s < 0.60 else "high" if s < 0.80 else "fraud"

CHECKS = []
def chk(label, got, exp):
    ok = got == exp
    CHECKS.append((ok, label, got, exp))
    print(f"{'OK ' if ok else 'GAGAL'}  {label}: got={got} exp={exp}")

print("=== VERIFIKASI ANGKA LAPORAN 04-data-quality.md ===\n")
chk("jumlah baris", len(rows), 300)
chk("jumlah kolom CSV", len(rows[0]), 29)
chk("ID unik", len({r['Name'] for r in rows}), 300)
chk("total biaya", sum(int(n(r['Biaya Rp'])) for r in rows), 3526650000)
for s, v in (("auto_clear", 2685550000), ("review", 279950000), ("escalate", 561150000)):
    got = sum(int(n(r['Biaya Rp'])) for r in rows if n(r['Status']) == s)
    chk(f"nominal {s}", got, v)
chk("status auto_clear", sum(1 for r in rows if n(r['Status'])=='auto_clear'), 240)
chk("status review", sum(1 for r in rows if n(r['Status'])=='review'), 24)
chk("status escalate", sum(1 for r in rows if n(r['Status'])=='escalate'), 36)
for lab, v in (("low",240),("medium",10),("high",14),("fraud",36)):
    chk(f"risiko {lab}", sum(1 for r in rows if n(r['Risiko'])==lab), v)
chk("LOS == 0", sum(1 for r in rows if n(r['LOS hari'])=='0'), 109)
chk("LOS kosong", sum(1 for r in rows if n(r['LOS hari'])==''), 0)
chk("LOS==0 rawat jalan", sum(1 for r in rows if n(r['LOS hari'])=='0' and n(r['Layanan'])=='rawat jalan'), 106)
chk("LOS==0 rawat inap", sum(1 for r in rows if n(r['LOS hari'])=='0' and n(r['Layanan'])=='rawat inap'), 3)
chk("LOS==0 rawat inap IDs", sorted(r['Name'] for r in rows
    if n(r['LOS hari'])=='0' and n(r['Layanan'])=='rawat inap'), ['KLM008','KLM010','KLM012'])
chk("rawat jalan LOS=1 IDs", sorted(r['Name'] for r in rows
    if n(r['Layanan'])=='rawat jalan' and n(r['LOS hari'])=='1'),
    ['KLM029','KLM044','KLM059','KLM074','KLM089'])
chk("baris LOS=0 tanpa kata LOS di Alasan", sum(1 for r in rows
    if n(r['LOS hari'])=='0' and 'LOS' not in n(r['Alasan'])), 109)
chk("total biaya baris LOS=0", sum(int(n(r['Biaya Rp'])) for r in rows if n(r['LOS hari'])=='0'), 153310000)
chk("Alasan kosong", [r['Name'] for r in rows if n(r['Alasan'])==''], ['KLM031'])
chk("Modus kosong", sum(1 for r in rows if n(r['Modus'])==''), 240)
chk("Sindikat kosong", sum(1 for r in rows if n(r['Sindikat'])==''), 264)
chk("baris ber-Sindikat", sum(1 for r in rows if n(r['Sindikat'])), 36)
chk("fraud tanpa Sindikat", sorted(r['Name'] for r in rows
    if n(r['Risiko'])=='fraud' and not n(r['Sindikat'])), ['KLM121','KLM122'])
chk("high dengan Sindikat", sorted(r['Name'] for r in rows
    if n(r['Risiko'])=='high' and n(r['Sindikat'])), ['KLM016','KLM017'])
chk("Kontradiksi True", sorted(r['Name'] for r in rows if n(r['Kontradiksi Narasi'])=='True'),
    ['KLM001','KLM002','KLM003','KLM004','KLM005','KLM006','KLM018','KLM024',
     'KLM105','KLM106','KLM107','KLM108'])
chk("Kontradiksi count", sum(1 for r in rows if n(r['Kontradiksi Narasi'])=='True'), 12)
chk("undef Rujukan", sum(1 for r in rows if 'undefined' in n(r['Rujukan']).lower()), 28)
chk("tanpa prosedur (sentinel —)", sum(1 for r in rows if n(r['Prosedur ICD-9-CM'])=='—'), 156)
chk("Obat sentinel —", sorted(r['Name'] for r in rows if n(r['Obat'])=='—'), ['KLM004','KLM005','KLM006'])
chk("entitas pasien unik", len({n(r['Pasien']).split(' (')[0] for r in rows}), 40)
chk("entitas dokter unik", len({n(r['Dokter']).split(' (')[0] for r in rows}), 20)
chk("entitas faskes unik", len({n(r['Faskes']) for r in rows}), 10)
chk("dx unik", len({n(r['Diagnosis ICD-10']).split(' - ')[0] for r in rows}), 13)
chk("proc unik (tanpa —)", len({n(r['Prosedur ICD-9-CM']).split(' - ')[0] for r in rows
    if n(r['Prosedur ICD-9-CM'])!='—'}), 8)
chk("obat M kode unik", len({m.group(1) for r in rows for m in re.finditer(r"(M\d{2})", n(r['Obat']))}), 10)
chk("Sinyal SHAP unik", len({n(r['Sinyal SHAP']) for r in rows}), 33)
chk("Umpan Balik unik", len({n(r['Umpan Balik Pasien']) for r in rows}), 36)
chk("tanggal unik", len({n(r['Tanggal']) for r in rows}), 138)
chk("rentang tanggal", (min(n(r['Tanggal']) for r in rows), max(n(r['Tanggal']) for r in rows)),
    ('2026-01-01','2026-06-27'))
chk("v2.1 kolom ada", [c for c in ("pasien_id","faskes_id","dokter_id","seed","version","timestamp")
    if c in rows[0]], [])
chk("kolom di luar kamus", sorted(set(rows[0]) - {"Name","Tanggal","Pasien","Dokter","Faskes",
    "Diagnosis ICD-10","Prosedur ICD-9-CM","Obat","LOS hari","Biaya Rp","Narasi Rekam Medis",
    "Kontradiksi Narasi","Skor Fraud","Risiko","Status","Modus","Sindikat","Alasan",
    "Sinyal SHAP","Kontribusi Saluran","Skor Sentimen","Sentimen","Umpan Balik Pasien","Catatan",
    "_notion_page_id","_last_edited"}), ['Alasan Berobat','Layanan','Rujukan'])
# ambang
chk("mismatch interpretasi >= (0.35/0.60/0.80)", sum(1 for r in rows
    if band(float(n(r['Skor Fraud']))) != n(r['Risiko'])), 0)
def band_gt(s):
    return "low" if s <= 0.35 else "medium" if s <= 0.60 else "high" if s <= 0.80 else "fraud"
chk("mismatch interpretasi > (0.35/0.60/0.80)", sum(1 for r in rows
    if band_gt(float(n(r['Skor Fraud']))) != n(r['Risiko'])), 1)
chk("baris skor tepat 0.35", [r['Name'] for r in rows if float(n(r['Skor Fraud']))==0.35], [])
chk("baris skor tepat 0.60", [r['Name'] for r in rows if float(n(r['Skor Fraud']))==0.60], [])
chk("baris skor tepat 0.80", [(r['Name'], n(r['Skor Fraud']), n(r['Risiko']))
    for r in rows if float(n(r['Skor Fraud']))==0.80], [('KLM115','0.8','fraud')])
# rentang label
for lab, lo, hi in (("low",0.04,0.14),("medium",0.40,0.53),("high",0.62,0.79),("fraud",0.80,0.95)):
    v = [float(n(r['Skor Fraud'])) for r in rows if n(r['Risiko'])==lab]
    chk(f"rentang skor {lab}", (min(v), max(v)), (lo, hi))
# kanal
nc = [r for r in rows if abs(sum(float(x) for x in tfs(r)) - float(n(r['Skor Fraud']))) > 1e-9]
chk("baris Skor != T+F+S", len(nc), 42)
chk("  breakdown non-koinciden", {lab: sum(1 for r in nc if n(r['Risiko'])==lab)
    for lab in ("low","medium","high","fraud")}, {"low":0,"medium":10,"high":9,"fraud":23})
chk("  selisih > 0.02 (pembulatan 2 desimal)", sum(1 for r in nc
    if abs(round(float(n(r['Skor Fraud'])) - sum(float(x) for x in tfs(r)), 4)) > 0.02), 21)
nd = sorted(r['Name'] for r in rows if band(sum(float(x) for x in tfs(r))) != n(r['Risiko']))
chk("label tidak derivable dari kanal", nd, ['KLM123','KLM124','KLM125','KLM126','KLM127',
    'KLM128','KLM129','KLM130','KLM131','KLM132','KLM133','KLM134','KLM135','KLM136'])
chk("  breakdown derivable", {lab: sum(1 for r in rows
    if n(r['Risiko'])==lab and band(sum(float(x) for x in tfs(r))) != n(r['Risiko']))
    for lab in ("low","medium","high","fraud")}, {"low":0,"medium":6,"high":8,"fraud":0})
# outlier biaya
b = sorted(int(n(r['Biaya Rp'])) for r in rows)
q1, q3 = statistics.quantiles(b, n=4)[0], statistics.quantiles(b, n=4)[2]
chk("biaya median", statistics.median(b), 4475000)
chk("biaya Q1", q1, 1150000)
chk("biaya Q3", q3, 9337500)
chk("biaya min", b[0], 700000); chk("biaya max", b[-1], 63500000)
chk("outlier atas IQR", sum(1 for x in b if x > q3 + 1.5*(q3-q1)), 44)
chk("pagar atas IQR", q3 + 1.5*(q3-q1), 21618750)
chk("biaya > 50jt", sum(1 for x in b if x > 50000000), 23)
chk("biaya < 1jt", sum(1 for x in b if x < 1000000), 29)
chk("rasio maks/min", round(b[-1]/b[0]), 91)
# sentimen
for lab, lo, hi, cnt in (("negatif",-0.90,-0.30,72),("netral",0.05,0.15,58),("positif",0.60,0.85,170)):
    v = [float(n(r['Skor Sentimen'])) for r in rows if n(r['Sentimen'])==lab]
    chk(f"sentimen {lab} n", len(v), cnt)
    chk(f"sentimen {lab} rentang", (round(min(v),2), round(max(v),2)), (lo,hi))
chk("negatif skor>0", sum(1 for r in rows if n(r['Sentimen'])=='negatif' and float(n(r['Skor Sentimen']))>0), 0)
chk("positif skor<0", sum(1 for r in rows if n(r['Sentimen'])=='positif' and float(n(r['Skor Sentimen']))<0), 0)
# biaya nonnegatif & integer
chk("biaya negatif", sum(1 for r in rows if int(n(r['Biaya Rp']))<0), 0)
chk("biaya non-integer", sum(1 for r in rows if not re.fullmatch(r"\d+", n(r['Biaya Rp']))), 0)
# duplikat
sig = defaultdict(list)
for r in rows:
    sig[(n(r['Tanggal']),n(r['Pasien']),n(r['Diagnosis ICD-10']),n(r['Prosedur ICD-9-CM']),
         n(r['LOS hari']),n(r['Biaya Rp']))].append(r['Name'])
chk("grup duplikat", sorted(sorted(v) for v in sig.values() if len(v)>1),
    [['KLM101','KLM102'],['KLM103','KLM104']])
sig2 = defaultdict(list)
for r in rows:
    sig2[tuple(n(r[c]) for c in rows[0] if c not in ("Name","_notion_page_id","_last_edited"))].append(r['Name'])
chk("grup payload identik penuh", len([v for v in sig2.values() if len(v)>1]), 0)
# jumlah kolom data identik antar baris kembar (Name diabaikan)
biz_cols = [c for c in rows[0] if not c.startswith("_")]
D = {r['Name'].strip(): r for r in rows}
def ident_cols(a, b):
    return sum(1 for c in biz_cols if n(D[a][c]) == n(D[b][c]))
chk("KLM016 vs KLM017 kolom identik", ident_cols('KLM016','KLM017'), 20)
chk("KLM101 vs KLM102 kolom identik", ident_cols('KLM101','KLM102'), 25)
chk("KLM103 vs KLM104 kolom identik", ident_cols('KLM103','KLM104'), 25)
chk("jumlah kolom data dump Notion", len(biz_cols), 27)
# v100 subset
v100 = sorted(rows, key=lambda r: int(r['Name'][3:]))[:100]
chk("v100 risiko", dict(Counter(n(r['Risiko']) for r in v100)),
    {'low':76,'medium':4,'high':6,'fraud':14})
chk("v100 sentimen", dict(Counter(n(r['Sentimen']) for r in v100)),
    {'positif':62,'netral':14,'negatif':24})
chk("P11 klaim dlm v100", sum(1 for r in v100 if n(r['Pasien']).startswith('P11 (')), 5)
# median LOS
los_dx = defaultdict(list)
for r in rows:
    if n(r['LOS hari']) not in ('0',''):
        los_dx[n(r['Diagnosis ICD-10']).split(' - ')[0]].append(int(n(r['LOS hari'])))
chk("median LOS J18.9", statistics.median(los_dx['J18.9']), 5)
chk("median LOS I21.9", statistics.median(los_dx['I21.9']), 5)
chk("median LOS S72.0", statistics.median(los_dx['S72.0']), 6.5)
# sindikat
chk("pasien di sindikat", sorted({n(r['Pasien']).split(' (')[0] for r in rows if n(r['Sindikat'])}),
    ['P01','P02','P03','P08','P09','P10','P12','P13','P14','P16','P17','P19','P20',
     'P21','P22','P23','P24','P25','P26','P27'])
chk("pasien P28-P40 tanpa sindikat", len([p for p in {n(r['Pasien']).split(' (')[0] for r in rows}
    if p >= 'P28' and p not in {n(r['Pasien']).split(' (')[0] for r in rows if n(r['Sindikat'])}]), 13)
# SHAP konstan per modus
sm = defaultdict(set)
for r in rows:
    if n(r['Modus']): sm[n(r['Modus'])].add(n(r['Sinyal SHAP']))
chk("modus dengan SHAP konstan", sorted(k for k,v in sm.items() if len(v)==1),
    ['biaya_markup','cloning','excessive_usage','iur_biaya','phantom_billing',
     'readmission_berulang','repeat_billing'])
chk("jumlah modus", len(sm), 13)
# non-low
chk("baris non-low", sum(1 for r in rows if n(r['Risiko'])!='low'), 60)
chk("Catatan terisi = non-low", sum(1 for r in rows if n(r['Catatan'])), 60)
chk("low dengan Catatan terisi", sum(1 for r in rows if n(r['Risiko'])=='low' and n(r['Catatan'])), 0)
# modus non-fraud tanpa sindikat
chk("modus non-fraud tanpa Sindikat", sum(1 for r in rows
    if n(r['Modus']) and n(r['Risiko'])!='fraud' and not n(r['Sindikat'])), 22)
# modus di prefiks Alasan
chk("prefiks FRAUD tidak cocok Modus", sum(1 for r in rows
    if n(r['Risiko'])=='fraud' and re.match(r"FRAUD \(([^)]+)\)", n(r['Alasan'])) and
    re.match(r"FRAUD \(([^)]+)\)", n(r['Alasan'])).group(1).upper().split('—')[0].split('-')[0].strip()
    .replace(' ','_') not in (n(r['Modus']).upper()+'_', n(r['Modus']).upper())), 0)
# rasio di Alasan
TARIF = {"51.23":14500000,"00.66":58000000,"47.09":6800000,"53.1":8200000,"74.1":6200000,
         "81.52":46500000,"96.04":750000,"98.51":5600000}
def num_id(s):
    s = s.strip().replace(" ", "").replace("x", "")
    if "," in s and "." in s: s = s.replace(".", "").replace(",", ".")
    elif "," in s: s = s.replace(",", ".")
    return float(s)
okc = badc = 0
for r in rows:
    c = n(r['Prosedur ICD-9-CM']).split(' - ')[0]
    m = re.search(r"rasio\s+([\d.,]+x?)", n(r['Alasan']))
    if m and c in TARIF:
        s = num_id(m.group(1))
        if abs(int(n(r['Biaya Rp']))/TARIF[c] - s) <= 0.015: okc += 1
        else: badc += 1
chk("rasio di Alasan cocok", okc, 72)
chk("rasio di Alasan tidak cocok", badc, 0)
chk("baris prosedur ber-acuan", sum(1 for r in rows
    if n(r['Prosedur ICD-9-CM']).split(' - ')[0] in TARIF), 144)
chk("baris ber-acuan yang menyebut 'rasio'", sum(1 for r in rows
    if n(r['Prosedur ICD-9-CM']).split(' - ')[0] in TARIF and 'rasio' in n(r['Alasan'])), 72)
# fraud sentimen negatif
chk("fraud sentimen negatif", sum(1 for r in rows
    if n(r['Risiko'])=='fraud' and n(r['Sentimen'])=='negatif'), 23)
chk("low sentimen negatif", sum(1 for r in rows
    if n(r['Risiko'])=='low' and n(r['Sentimen'])=='negatif'), 42)
# (tanggal,pasien) multi
sp = defaultdict(list)
for r in rows: sp[(n(r['Tanggal']), n(r['Pasien']))].append(r['Name'])
chk("(tanggal,pasien) >1 klaim", len([v for v in sp.values() if len(v)>1]), 9)
# Pasien claims per entity max
pc = Counter(n(r['Pasien']).split(' (')[0] for r in rows)
chk("P27 jumlah klaim", pc['P27'], 12)
# JSON sync
import json
jr = json.load(open(os.path.join(CORPUS,'claims_v2_live.json'),encoding='utf-8'))
chk("JSON rows", len(jr), 300)
chk("JSON keys == CSV header", set(jr[0].keys()) == set(rows[0].keys()), True)
chk("JSON LOS null", sum(1 for j in jr if j.get('LOS hari') is None), 0)
chk("JSON LOS == 0", sum(1 for j in jr if j.get('LOS hari') == 0), 109)
# sindikat skor range
SY = {"SYND-01":(0.93,1.01),"SYND-02":(0.92,1.01),"SYND-03":(0.84,0.87),"SYND-04":(0.86,0.88),
      "SYND-05":(0.78,0.79),"SYND-06":(0.85,0.90),"SYND-07":(0.82,0.87),"SYND-08":(0.75,0.80),
      "SYND-09":(0.78,0.83)}
viol = sorted(r['Name'] for r in rows if n(r['Sindikat']) in SY and
    not (SY[n(r['Sindikat'])][0]-1e-9 <= float(n(r['Skor Fraud'])) <= SY[n(r['Sindikat'])][1]+1e-9))
chk("baris skor sindikat di luar rentang dok", viol,
    ['KLM101','KLM102','KLM109','KLM110','KLM111','KLM112','KLM113','KLM114',
     'KLM119','KLM120'])
# dx->proc
pc_pair = Counter((n(r['Diagnosis ICD-10']).split(' - ')[0],
                   n(r['Prosedur ICD-9-CM']).split(' - ')[0]) for r in rows)
chk("dx K29.7 -> 00.66", pc_pair[('K29.7','00.66')], 3)
chk("dx O80 -> 74.1", pc_pair[('O80','74.1')], 1)
chk("dx E11.9 -> 00.66", pc_pair[('E11.9','00.66')], 1)
chk("tanpa prosedur", sum(1 for r in rows if n(r['Prosedur ICD-9-CM'])=='—'), 156)
chk("S72.0 -> 81.52", pc_pair[('S72.0','81.52')], 18)
chk("I21.9 -> 00.66", pc_pair[('I21.9','00.66')], 20)
chk("K80.2 -> 96.04", pc_pair[('K80.2','96.04')], 3)

print("\n" + "="*60)
bad = [c for c in CHECKS if not c[0]]
print(f"TOTAL CHECK: {len(CHECKS)} | OK: {len(CHECKS)-len(bad)} | GAGAL: {len(bad)}")
for b in bad: print("   GAGAL:", b[1], "got=", b[2], "exp=", b[3])
