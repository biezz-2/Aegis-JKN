#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit ronde 7: perbaikan parsing rentang ID + verifikasi final mapping."""
import csv, os, re, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
rows = list(csv.DictReader(open(os.path.join(CORPUS, "claims_v2_live.csv"),
                                encoding="utf-8-sig", newline="")))
n = lambda v: "" if v is None else str(v).strip()
def h(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

def expand(rng):
    a, b = rng.split("-")
    return [f"KLM{i:03d}" for i in range(int(a[3:]), int(b) + 1)]

DOC = {
 "SYND-01": ("KLM001-003","RS_A",["D01","D02"],["P01","P02","P03"],0.93,1.00,"upcoding"),
 "SYND-02": ("KLM004-006","RS_C",["D05"],["P08","P09","P10"],0.92,1.00,"phantom_billing"),
 "SYND-03": ("KLM007-012","RS_B",["D07"],["P12","P13","P14"],0.84,0.87,"unbundling"),
 "SYND-04": ("KLM013-014","RS_E",["D09"],["P16","P17"],0.86,0.88,"drug_diversion"),
 "SYND-05": ("KLM016-017","RS_F",["D08"],["P19","P20"],0.78,0.79,"cloning"),
 "SYND-06": ("KLM101-104","RS_G",["D13"],["P21","P22","P23","P24"],0.85,0.90,"repeat_billing"),
 "SYND-07": ("KLM105-108","RS_H",["D14"],["P25","P26","P27","P28"],0.82,0.87,"iur_biaya"),
 "SYND-08": ("KLM109-114","RS_I",["D15"],["P29","P30","P31","P32","P33","P34"],0.75,0.80,"readmission_berulang"),
 "SYND-09": ("KLM115-120","RS_J",["D16"],["P35","P36","P37","P38","P39","P40"],0.78,0.83,"excessive_usage"),
}
h("1. PEMETAAN SINDIKAT (parsing ID diperbaiki)")
bad_tab = []
for s in sorted(DOC):
    ids, fsk, doks, pats, lo, hi, mod = DOC[s]
    grp = [r for r in rows if n(r["Sindikat"]) == s]
    a_ids = sorted(r["Name"] for r in grp)
    a_fsk = sorted(set(n(r["Faskes"]) for r in grp))
    a_dok = sorted(set(n(r["Dokter"]).split(" (")[0] for r in grp))
    a_pat = sorted(set(n(r["Pasien"]).split(" (")[0] for r in grp))
    a_mod = sorted(set(n(r["Modus"]) for r in grp))
    sc = [float(n(r["Skor Fraud"])) for r in grp]
    checks = {
        "ID": a_ids == sorted(expand(ids)),
        "faskes": a_fsk == [fsk],
        "dokter": a_dok == sorted(doks),
        "pasien": a_pat == sorted(pats),
        "modus": a_mod == [mod],
        "skor": all(lo - 1e-9 <= x <= hi + 1e-9 for x in sc),
    }
    bad = [k for k, v in checks.items() if not v]
    print(f"\n{s}: {'SEMUA COCOK' if not bad else 'GAGAL -> ' + str(bad)}")
    print(f"   ID    doc={expand(ids)}")
    print(f"          akt={a_ids}")
    print(f"   faskes doc={fsk} akt={a_fsk} | dokter doc={sorted(doks)} akt={a_dok}")
    print(f"   pasien doc={sorted(pats)} akt={a_pat}")
    print(f"   modus doc={mod} akt={a_mod} | skor doc=[{lo},{hi}] akt={min(sc):.2f}-{max(sc):.2f}")
    if bad: bad_tab.append((s, bad))
print("\nSIND. dengan kegagalan pemetaan:", len(bad_tab))
for b in bad_tab: print("   ", b[0], b[1])

h("2. RINGKASAN PEMETAAN: DOKUMEN v2.1 KLAIM vs DATA")
h("3. PASIEN YANG DOKUMENTASI v2.1 (P01-P40) vs PEMAKAIAN NYATA")
for s in sorted(DOC):
    grp = [r for r in rows if n(r["Sindikat"]) == s]
    print(f"   {s}: {sorted(set(n(r['Pasien']).split(' (')[0] for r in grp))}")
print("\nPasien P01-P20 (dari tabel v100) tidak dipakai sindikat mana pun?")
used = set()
for s in DOC:
    used |= {n(r["Pasien"]).split(" (")[0] for r in rows if n(r["Sindikat"]) == s}
print("   P01-P20 yang muncul di sindikat:", sorted(p for p in used if p <= "P20"))
print("   P21-P40 yang muncul di sindikat:", sorted(p for p in used if p > "P20"))

h("4. VERIFIKASI ULANG: SEMUA BARIS UNIK, TOTAL, TOTAL BIAYA")
ids = [r["Name"] for r in rows]
print("baris:", len(rows), "| ID unik:", len(set(ids)))
print("total biaya:", sum(int(n(r["Biaya Rp"])) for r in rows))
print("checksum SHA256 file:")
import hashlib
for p in ("claims_v2_live.csv", "claims_v2_live.json"):
    hh = hashlib.sha256(open(os.path.join(CORPUS, p), "rb").read()).hexdigest()
    print(f"   {p}: {hh}")
