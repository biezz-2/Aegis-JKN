#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit ronde 6: verifikasi pemetaan sindikat (pasien/dokter/faskes) & penutup."""
import csv, os, re, sys, statistics
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
rows = list(csv.DictReader(open(os.path.join(CORPUS, "claims_v2_live.csv"),
                                encoding="utf-8-sig", newline="")))
n = lambda v: "" if v is None else str(v).strip()
def h(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# ---- 1. PEMETAAN SINDIKAT: doc 10-simulation vs aktual
h("1. PEMETAAN SINDIKAT doc vs AKTUAL (id, faskes, dokter, pasien)")
DOC = {
 "SYND-01": ("KLM001-003", "RS_A", ["D01","D02"], ["P01","P02","P03"], 0.93, 1.00, "upcoding"),
 "SYND-02": ("KLM004-006", "RS_C", ["D05"], ["P08","P09","P10"], 0.92, 1.00, "phantom_billing"),
 "SYND-03": ("KLM007-012", "RS_B", ["D07"], ["P12","P13","P14"], 0.84, 0.87, "unbundling"),
 "SYND-04": ("KLM013-014", "RS_E", ["D09"], ["P16","P17"], 0.86, 0.88, "drug_diversion"),
 "SYND-05": ("KLM016-017", "RS_F", ["D08"], ["P19","P20"], 0.78, 0.79, "cloning"),
 "SYND-06": ("KLM101-104", "RS_G", ["D13"], ["P21","P22","P23","P24"], 0.85, 0.90, "repeat_billing"),
 "SYND-07": ("KLM105-108", "RS_H", ["D14"], ["P25","P26","P27","P28"], 0.82, 0.87, "iur_biaya"),
 "SYND-08": ("KLM109-114", "RS_I", ["D15"], ["P29","P30","P31","P32","P33","P34"], 0.75, 0.80, "readmission_berulang"),
 "SYND-09": ("KLM115-120", "RS_J", ["D16"], ["P35","P36","P37","P38","P39","P40"], 0.78, 0.83, "excessive_usage"),
}
mismatch = []
for s in sorted(DOC):
    ids, fsk, doks, pats, lo, hi, mod = DOC[s]
    grp = [r for r in rows if n(r["Sindikat"]) == s]
    a_ids = sorted(r["Name"] for r in grp)
    a_fsk = sorted(set(n(r["Faskes"]) for r in grp))
    a_dok = sorted(set(n(r["Dokter"]).split(" (")[0] for r in grp))
    a_pat = sorted(set(n(r["Pasien"]).split(" (")[0] for r in grp))
    a_mod = sorted(set(n(r["Modus"]) for r in grp))
    sc = [float(n(r["Skor Fraud"])) for r in grp]
    ok_id   = a_ids == sorted([f"KLM{i:03d}" for i in range(int(ids[3:6])+1, int(ids[8:11])+1)])
    ok_fsk  = a_fsk == [fsk]
    ok_dok  = a_dok == sorted(doks)
    ok_pat  = a_pat == sorted(pats)
    ok_mod  = a_mod == [mod]
    ok_sc   = all(lo - 1e-9 <= x <= hi + 1e-9 for x in sc)
    bad = [k for k, v in (("ID",ok_id),("faskes",ok_fsk),("dokter",ok_dok),
                          ("pasien",ok_pat),("modus",ok_mod),("skor",ok_sc)) if not v]
    print(f"\n{s}: {', '.join(bad) if bad else 'SEMUA COCOK'}")
    print(f"   ID    doc={ids:<12} akt={a_ids}")
    print(f"   faskes doc={fsk:<6} akt={a_fsk}")
    print(f"   dokter doc={sorted(doks)} akt={a_dok}")
    print(f"   pasien doc={sorted(pats)} akt={a_pat}")
    print(f"   modus  doc={mod:<20} akt={a_mod}")
    print(f"   skor   doc=[{lo}, {hi}] akt={min(sc):.2f}-{max(sc):.2f}")
    if bad: mismatch.append((s, bad, a_pat, sorted(pats), a_dok, sorted(doks)))

print("\nSINDIKAT DENGAN PEMETAAN TIDAK COCOK:", len(mismatch))
for m in mismatch: print("   ", m[0], "gagal:", m[1])

# ---- 2. Klaim tunggal (tanpa sindikat)
h("2. KLAIM TUNGGAL (doc: '-' sindikat)")
for nm, mod, fsk, dok, pat in (("KLM121","Biaya Markup","RS_A","D03","P04"),
                               ("KLM122","Drug Diversion","RS_E","D09","P18")):
    r = [x for x in rows if x["Name"] == nm][0]
    print(f"   {nm} doc: {mod} / {fsk} / {dok} / {pat}")
    print(f"          akt: {n(r['Modus'])} / {n(r['Faskes'])} / {n(r['Dokter'])} / {n(r['Pasien'])} "
          f"skor={n(r['Skor Fraud'])}")

# ---- 3. Skor sentimen gap
h("3. SENTIMEN: GAP ANTAR KELAS")
sneg = sorted(float(n(r["Skor Sentimen"])) for r in rows if n(r["Sentimen"])=="negatif")
sneu = sorted(float(n(r["Skor Sentimen"])) for r in rows if n(r["Sentimen"])=="netral")
spos = sorted(float(n(r["Skor Sentimen"])) for r in rows if n(r["Sentimen"])=="positif")
print(f"negatif: n={len(sneg)} rentang [{min(sneg)}, {max(sneg)}] unik={len(set(sneg))}")
print(f"netral : n={len(sneu)} rentang [{min(sneu)}, {max(sneu)}] unik={len(set(sneu))}")
print(f"positif: n={len(spos)} rentang [{min(spos)}, {max(spos)}] unik={len(set(spos))}")
print(f"gap negatif->netral: {min(sneu)-max(sneg):.2f} ; netral->positif: {min(spos)-max(sneu):.2f}")
print("baris netral di luar [0,0.2]:", sum(1 for x in sneu if not 0 <= x <= 0.2))
print("baris negatif > 0:", sum(1 for x in sneg if x > 0), "| positif < 0:", sum(1 for x in spos if x < 0))
print("rentang terdokumentasi 10-sim: -1 s.d. 1 -> semua dalam rentang:",
      all(-1 <= x <= 1 for x in sneg+sneu+spos))

# ---- 4. 3 baris tanpa pola obat
h("4. BARIS TANPA POLA OBAT 'Mxx x N satuan'")
for nm in ("KLM004","KLM005","KLM006"):
    r = [x for x in rows if x["Name"] == nm][0]
    print(f"   {nm}: Obat={n(r['Obat'])!r} | SHAP={n(r['Sinyal SHAP'])[:90]}")
print("   -> konsisten dengan Phantom Billing 'tanpa MedicationDispense' (doc 10-sim)")

# ---- 5. Em-dash pada Prosedur
h("5. NILAI KOSONG vs SENTINEL")
for c in ("Prosedur ICD-9-CM","Modus","Sindikat","Alasan","Catatan","LOS hari"):
    vals = Counter(n(r[c]) for r in rows)
    empt = sum(v for k, v in vals.items() if k == "")
    dash = sum(v for k, v in vals.items() if k in ("—", "-", "N/A", "null", "undefined"))
    print(f"   {c:<20} string kosong={empt:<4} sentinel/tanda={dash}  "
          f"nilai unik={len(vals)}")

# ---- 6. Rujukan: 'undefined' + duplikat nomor
h("6. RUJUKAN: NOMOR DUPLIKAT")
loc = defaultdict(list)
for r in rows:
    m = re.search(r"(RJ-\d{4}-\d+)", n(r["Rujukan"]))
    if m: loc[m.group(1)].append((r["Name"], n(r["Tanggal"]), n(r["Pasien"])))
for k, v in sorted(loc.items()):
    if len(v) > 1: print(f"   {k}: {v}")

# ---- 7. Cek status data: apakah 'Catatan' terisi hanya untuk non-low
h("7. CATATAN: KOLOM KOSONG PADA BARIS LOW?")
print("low dengan Catatan kosong :", sum(1 for r in rows if n(r["Risiko"])=="low" and not n(r["Catatan"])))
print("low dengan Catatan terisi :", sum(1 for r in rows if n(r["Risiko"])=="low" and n(r["Catatan"])))
print("non-low dengan Catatan kosong:", [(r["Name"], n(r["Risiko"]), n(r["Modus"]))
      for r in rows if n(r["Risiko"])!="low" and not n(r["Catatan"])])

# ---- 8. Biaya: rasio biaya/hari (apakah LOS=0 -> divide by zero?)
h("8. BIAYA PER HARI PADA BARIS LOS=0")
z = [(r["Name"], n(r["Biaya Rp"]), n(r["Layanan"]), n(r["Risiko"])) for r in rows if n(r["LOS hari"])=="0"]
print(f"baris LOS=0: {len(z)}; total biaya pada baris itu: Rp{sum(int(x[1]) for x in z):,}")
print("contoh:", z[:3])
print("-> biaya/hari tak terdefinisi; SHAP KLM008/010/012 justru memakai 'LOS 0' sebagai sinyal")

# ---- 9. Duplikat payload KLM101/102 & 103/104
h("9. DUPLEKAT DESKRIPSI (SYND-06 repeat billing)")
for pair in (("KLM101","KLM102"),("KLM103","KLM104")):
    a = [x for x in rows if x["Name"]==pair[0]][0]; b = [x for x in rows if x["Name"]==pair[1]][0]
    same = [c for c in a if n(a[c])==n(b[c]) and not c.startswith("_") and c!="Name"]
    diff = [c for c in a if n(a[c])!=n(b[c]) and not c.startswith("_") and c!="Name"]
    print(f"   {pair}: SAMA={len(same)} -> {same}")
    print(f"          BEDA={diff}")
