#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit ronde 8: verifikasi presisi angka untuk tabel laporan."""
import csv, os, re, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
rows = list(csv.DictReader(open(os.path.join(CORPUS, "claims_v2_live.csv"),
                                encoding="utf-8-sig", newline="")))
n = lambda v: "" if v is None else str(v).strip()
def h(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)
def tfs(r): return tuple(re.findall(r"[TFS] ([-\d.]+)", n(r["Kontribusi Saluran"])))
def band(s):
    return "low" if s < 0.35 else "medium" if s < 0.60 else "high" if s < 0.80 else "fraud"

h("A. POLA KANAL PER KELAS RISIKO (jumlah baris per pola T/F/S)")
pat = defaultdict(list)
for r in rows:
    pat[(n(r["Risiko"]), tfs(r))].append((r["Name"], float(n(r["Skor Fraud"]))))
for k in sorted(pat, key=lambda x: (x[0], x[1])):
    sc = sorted(v[1] for v in pat[k])
    print(f"   {k[0]:<7} {str(k[1]):<28} n={len(pat[k]):<3} skor={min(sc):.2f}-{max(sc):.2f} "
          f"{[v[0] for v in pat[k]] if len(pat[k])<=9 else '(9+)'}")
print("\nPOLA IKUTINYA per label:")
for lab in ("low","medium","high","fraud"):
    ps = Counter(tfs(r) for r in rows if n(r["Risiko"]) == lab)
    print(f"   {lab}: {len(ps)} pola")
    for p, c in ps.most_common(3):
        sc = sorted(float(n(r["Skor Fraud"])) for r in rows
                    if n(r["Risiko"]) == lab and tfs(r) == p)
        print(f"       {p} n={c} skor={min(sc):.2f}-{max(sc):.2f}")

h("B. BARIS YANG TIDAK KONINSIDEN (Skor != T+F+S)")
nc = []
for r in rows:
    s = sum(float(x) for x in tfs(r)); sc = float(n(r["Skor Fraud"]))
    if abs(s - sc) > 1e-9: nc.append((r["Name"], n(r["Risiko"]), round(s,3), sc, round(sc-s,3)))
print("total:", len(nc))
for lab in ("low","medium","high","fraud"):
    v = [x for x in nc if x[1] == lab]
    if v:
        print(f"   {lab}: n={len(v)} selisih min={min(x[4] for x in v):+.3f} "
              f"maks={max(x[4] for x in v):+.3f} >0.02: {sum(1 for x in v if abs(x[4])>0.02)}")
        print(f"       IDs: {[x[0] for x in v]}")

h("C. BARIS LABEL TIDAK DERIVABLE DARI T+F+S")
nd = []
for r in rows:
    s = sum(float(x) for x in tfs(r))
    if band(s) != n(r["Risiko"]):
        nd.append((r["Name"], n(r["Risiko"]), round(s,3), band(s), float(n(r["Skor Fraud"])),
                   round(float(n(r["Skor Fraud"]))-s,3)))
print("total:", len(nd))
for x in sorted(nd, key=lambda y: (y[1], y[0])):
    print(f"   {x[0]:<8} risiko={x[1]:<7} T+F+S={x[2]:<5} band={x[3]:<7} skor={x[4]:<5} selisih={x[5]:+.3f}")

h("D. CEK ULANG ANGKA LAPORAN")
print("baris:", len(rows), "| ID unik:", len({r['Name'] for r in rows}))
print("total biaya:", sum(int(n(r['Biaya Rp'])) for r in rows))
print("Los:", sum(1 for r in rows if n(r['LOS hari'])=='0'), "| LOS kosong:", sum(1 for r in rows if n(r['LOS hari'])==''))
print("Alasan kosong:", [r['Name'] for r in rows if n(r['Alasan'])==''])
print("Kontradiksi True:", sorted(r['Name'] for r in rows if n(r['Kontradiksi Narasi'])=='True'))
print("undef Rujukan:", sum(1 for r in rows if 'undefined' in n(r['Rujukan']).lower()))
print("P11 klaim (semua 300):", sum(1 for r in rows if n(r['Pasien']).startswith('P11 (')))
print("P11 klaim (KLM001-100):", sum(1 for r in rows if n(r['Pasien']).startswith('P11 (')
      and int(r['Name'][3:]) <= 100))
print("median LOS S72.0 (LOS>0):", sorted(int(n(r['LOS hari'])) for r in rows
      if n(r['Diagnosis ICD-10']).startswith('S72.0') and n(r['LOS hari']) not in ('0','')))
print("baris non-low:", sum(1 for r in rows if n(r['Risiko'])!='low'),
      "| Catatan terisi:", sum(1 for r in rows if n(r['Catatan'])))
print("pasien di sindikat:", sorted({n(r['Pasien']).split(' (')[0] for r in rows if n(r['Sindikat'])}))
