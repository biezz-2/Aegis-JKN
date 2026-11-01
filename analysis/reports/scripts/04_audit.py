#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit conformance: Aegis-JKN Data Dictionary (corpus/03-dataset-registry.md) vs
data nyata (corpus/claims_v2_live.csv / .json).

Stdlib only (csv, json, re, statistics, collections, datetime).
Jalankan:  python -X utf8 04_audit.py
Output:    seluruh angka untuk laporan N:/HEALTHKATHON/analysis/reports/04-data-quality.md
"""
import csv
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")

CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
CSV_PATH = os.path.join(CORPUS, "claims_v2_live.csv")
JSON_PATH = os.path.join(CORPUS, "claims_v2_live.json")

OUT = {}          # kumpulan hasil
FINDINGS = []     # (severity, kategori, judul, detail)


def finding(sev, cat, title, detail=""):
    FINDINGS.append((sev, cat, title, detail))


def h(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------- load
with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    CSV_COLS = list(reader.fieldnames)
    ROWS = list(reader)

with open(JSON_PATH, encoding="utf-8") as f:
    JROWS = json.load(f)

h("0. MEMUAT DATA")
print(f"CSV rows={len(ROWS)} cols={len(CSV_COLS)}")
print(f"JSON rows={len(JROWS)}")
print("CSV columns:", CSV_COLS)

# JSON harus punya key yang sama dengan header CSV
jkeys = list(JROWS[0].keys())
print("JSON keys == CSV header (set):", set(jkeys) == set(CSV_COLS))
print("JSON-only keys:", sorted(set(jkeys) - set(CSV_COLS)))
print("CSV-only keys:", sorted(set(CSV_COLS) - set(jkeys)))


def norm(v):
    """Normalisasi nilai string dari CSV."""
    if v is None:
        return ""
    return str(v).strip()


def nonempty(r, c):
    return norm(r.get(c)) != ""


def num(v):
    try:
        return float(str(v).strip())
    except Exception:
        return None


# ---------------------------------------------------------------- 7. ID
h("7. VERIFIKASI ID KLM001-KLM300")
ids = [norm(r["Name"]) for r in ROWS]
id_pat_bad = [i for i in ids if not re.fullmatch(r"KLM\d{3}", i)]
id_nums = sorted(int(i[3:]) for i in ids if re.fullmatch(r"KLM\d{3}", i))
dupes = sorted([k for k, v in Counter(ids).items() if v > 1])
missing = [n for n in range(1, 301) if n not in set(id_nums)]
lower = [i for i in ids if i != i.upper()]
padded = [i for i in ids if len(i) != 6]
print(f"total={len(ids)} unik={len(set(ids))} duplikat={dupes}")
print(f"pola KLM\\d{{3}} melanggar: {id_pat_bad}")
print(f"min={id_nums[0]} max={id_nums[-1]} jumlah=300; angka hilang: {missing}")
print(f"huruf kecil: {lower} | panjang != 6: {padded}")
print(f"page_id unik: {len(set(norm(r['_notion_page_id']) for r in ROWS))}")
OUT["id_ok"] = (not dupes and not missing and not id_pat_bad and not lower
                and not padded and len(ids) == 300)
print("KLAIM 'ID tidak terputus KLM001-KLM300' ->", "BENAR" if OUT["id_ok"] else "SALAH")

# ---------------------------------------------------------------- 2. angka
h("2. VERIFIKASI ANGKA KLAIM (03 §3/§6, 00 §3)")
status_c = Counter(norm(r["Status"]) for r in ROWS)
risiko_c = Counter(norm(r["Risiko"]) for r in ROWS)
print("Status:", dict(status_c))
print("Risiko:", dict(risiko_c))
los_empty = [r["Name"] for r in ROWS if not nonempty(r, "LOS hari")]
alasan_empty = [r["Name"] for r in ROWS if not nonempty(r, "Alasan")]
modus_empty = [r["Name"] for r in ROWS if not nonempty(r, "Modus")]
sind_empty = [r["Name"] for r in ROWS if not nonempty(r, "Sindikat")]
print(f"LOS kosong = {len(los_empty)}  -> {los_empty if len(los_empty) <= 12 else '(daftar panjang, lihat skrip)'}")
print(f"Alasan kosong = {len(alasan_empty)} -> {alasan_empty}")
print(f"Modus kosong = {len(modus_empty)}")
print(f"Sindikat kosong = {len(sind_empty)}")

total_biaya = sum(int(num(r["Biaya Rp"]) or 0) for r in ROWS)
print(f"Total nominal = Rp{total_biaya:,}".replace(",", "."))
per_status = defaultdict(int)
for r in ROWS:
    per_status[norm(r["Status"])] += int(num(r["Biaya Rp"]) or 0)
for s in sorted(per_status):
    print(f"  nominal {s} = Rp{per_status[s]:,}".replace(",", "."))
print("  jumlah per-status =", sum(per_status.values()), "== total:", sum(per_status.values()) == total_biaya)

# ---------------------------------------------------------------- 3. label vs skor
h("3. KONSISTENSI LABEL RISIKO vs SKOR FRAUD")


def label_ge(s, lo, hi):
    """Keputusan dengan >= pada batas bawah (konservatif: <=0.35 low)."""
    if s < 0.35:
        return "low"
    if s < 0.60:
        return "medium"
    if s < 0.80:
        return "high"
    return "fraud"


def label_gt(s):
    """Keputusan dengan > pada batas bawah (ambang 'lebih dari 0.8' = fraud)."""
    if s <= 0.35:
        return "low"
    if s <= 0.60:
        return "medium"
    if s <= 0.80:
        return "high"
    return "fraud"


mismatch_ge, mismatch_gt = [], []
for r in ROWS:
    s = num(r["Skor Fraud"])
    if label_ge(s, 0.35, 0.60) != norm(r["Risiko"]):
        mismatch_ge.append((r["Name"], s, norm(r["Risiko"])))
    if label_gt(s) != norm(r["Risiko"]):
        mismatch_gt.append((r["Name"], s, norm(r["Risiko"])))
print(f"Mismatch dengan interpretasi '>= batas bawah' (0.35/0.60/0.80 masuk kelas atas): {len(mismatch_ge)}")
for m in mismatch_ge:
    print("   ", m)
print(f"Mismatch dengan interpretasi '> batas bawah' (0.35/0.60/0.80 masuk kelas bawah): {len(mismatch_gt)}")
for m in mismatch_gt:
    print("   ", m)

edge = []
for r in ROWS:
    s = num(r["Skor Fraud"])
    for edgeval in (0.35, 0.60, 0.80):
        if abs(s - edgeval) < 1e-9:
            edge.append((r["Name"], s, norm(r["Risiko"]), edgeval))
print("\nBaris dengan skor PERSIS pada batas (0,35 / 0,60 / 0,80):")
for e in edge:
    print("   ", e)
print("Jumlah baris tepat di batas:", len(edge))

# skor tertinggi di kelas high & terendah di kelas fraud
hs = [num(r["Skor Fraud"]) for r in ROWS if norm(r["Risiko"]) == "high"]
fs = [num(r["Skor Fraud"]) for r in ROWS if norm(r["Risiko"]) == "fraud"]
print(f"max skor kelas high = {max(hs)} ; min skor kelas fraud = {min(fs)}")
print("Baris high dengan skor >= 0.80:",
      [(r["Name"], num(r["Skor Fraud"])) for r in ROWS
       if norm(r["Risiko"]) == "high" and num(r["Skor Fraud"]) >= 0.80])
print("Baris fraud dengan skor < 0.80:",
      [(r["Name"], num(r["Skor Fraud"])) for r in ROWS
       if norm(r["Risiko"]) == "fraud" and num(r["Skor Fraud"]) < 0.80])

# ambang implisit dari data
print("\nAmbang implisit (min skor tiap label, maks skor tiap label):")
for lab in ("low", "medium", "high", "fraud"):
    vals = [num(r["Skor Fraud"]) for r in ROWS if norm(r["Risiko"]) == lab]
    print(f"   {lab}: min={min(vals)} maks={max(vals)} n={len(vals)}")

# ---------------------------------------------------------------- 4. lintas kolom
h("4. KONSISTENSI LINTAS KOLOM")
sr = Counter((norm(r["Status"]), norm(r["Risiko"])) for r in ROWS)
print("Status x Risiko:")
for k, v in sorted(sr.items()):
    print(f"   {k[0]:<11} {k[1]:<7} {v}")
auto_nonlow = [(r["Name"], norm(r["Risiko"]), num(r["Skor Fraud"]))
               for r in ROWS if norm(r["Status"]) == "auto_clear" and norm(r["Risiko"]) != "low"]
esc_nonfraud = [(r["Name"], norm(r["Risiko"])) for r in ROWS
                if norm(r["Status"]) == "escalate" and norm(r["Risiko"]) != "fraud"]
rev_fraud = [(r["Name"], num(r["Skor Fraud"])) for r in ROWS
             if norm(r["Status"]) == "review" and norm(r["Risiko"]) == "fraud"]
print(f"auto_clear dengan Risiko != low: {len(auto_nonlow)} {auto_nonlow}")
print(f"escalate dengan Risiko != fraud: {len(esc_nonfraud)} {esc_nonfraud}")
print(f"review dengan Risiko = fraud: {len(rev_fraud)} {rev_fraud}")

print("\nSindikat x Modus:")
sm = Counter((norm(r["Sindikat"]), norm(r["Modus"])) for r in ROWS)
for k, v in sorted(sm.items()):
    print(f"   {k[0] or '(kosong)':<12} | {k[1] or '(kosong)':<22} {v}")
print("Sindikat terisi tanpa Modus:",
      [(r["Name"], r["Sindikat"]) for r in ROWS if nonempty(r, "Sindikat") and not nonempty(r, "Modus")])
print("Modus terisi tanpa Sindikat (per modus):",
      dict(Counter(norm(r["Modus"]) for r in ROWS
                   if nonempty(r, "Modus") and not nonempty(r, "Sindikat"))))

# rentang skor sindikat v2.1 (10-simulation-dataset.md tabel "Sindikat yang Diperbarui")
SYND_RANGE = {
    "SYND-01": (0.93, 1.01, "Upcoding"),
    "SYND-02": (0.92, 1.01, "Phantom Billing"),
    "SYND-03": (0.84, 0.87, "Unbundling"),
    "SYND-04": (0.86, 0.88, "Drug Diversion"),
    "SYND-05": (0.78, 0.79, "Cloning"),
    "SYND-06": (0.85, 0.90, "Repeat Billing"),
    "SYND-07": (0.82, 0.87, "Iur Biaya"),
    "SYND-08": (0.75, 0.80, "Readmission Berulang"),
    "SYND-09": (0.78, 0.83, "Excessive Usage"),
}
print("\nCek rentang skor per sindikat vs tabel 10-simulation-dataset.md:")
synd_issues = []
for r in ROWS:
    s = norm(r["Sindikat"])
    if not s:
        continue
    sc = num(r["Skor Fraud"])
    lo, hi, modus_doc = SYND_RANGE.get(s, (None, None, None))
    if lo is None:
        synd_issues.append((r["Name"], s, sc, "sindikat tak dikenal"))
        continue
    if not (lo - 1e-9 <= sc <= hi + 1e-9):
        synd_issues.append((r["Name"], s, sc, f"di luar rentang dok [{lo}, {hi}]"))
    if modus_doc and norm(r["Modus"]).lower().replace(" ", "_") != modus_doc.lower().replace(" ", "_"):
        synd_issues.append((r["Name"], s, sc, f"modus '{norm(r['Modus'])}' != '{modus_doc}'"))
for i in synd_issues:
    print("   ", i)
print("Total pelanggaran sindikat:", len(synd_issues))

# Alasan vs label
print("\nCek prefiks 'Alasan' vs label Risiko:")
prefix_map = defaultdict(Counter)
for r in ROWS:
    a = norm(r["Alasan"])
    p = a.split(":")[0].strip() if a else "(KOSONG)"
    prefix_map[norm(r["Risiko"])][p] += 1
for lab in ("low", "medium", "high", "fraud"):
    print(f"   {lab}: {dict(prefix_map[lab])}")

# Alasan wajib isi bila review/escalate
missing_alasan_review = [(r["Name"], norm(r["Status"]), norm(r["Risiko"]))
                         for r in ROWS if norm(r["Status"]) in ("review", "escalate")
                         and not nonempty(r, "Alasan")]
print("Baris review/escalate dengan Alasan kosong:", missing_alason if False else missing_alasan_review)

# Kontribusi Saluran parse
def parse_kontrib(s):
    out = {}
    for part in norm(s).split("·"):
        m = re.match(r"\s*([TFS])\s+([-\d.]+)", part)
        if m:
            out[m.group(1)] = float(m.group(2))
    return out


kbad = []
ksum = []
for r in ROWS:
    k = parse_kontrib(r["Kontribusi Saluran"])
    if set(k) != {"T", "F", "S"}:
        kbad.append((r["Name"], norm(r["Kontribusi Saluran"])))
    else:
        ksum.append((r["Name"], k["T"] + k["F"] + k["S"], num(r["Skor Fraud"])))
print("\nBaris dengan Kontribusi Saluran tidak lengkap (T/F/S):", kbad[:10], "total", len(kbad))
if ksum:
    diffs = [(n, round(t - sc, 6)) for n, t, sc in ksum]
    uniq = sorted(set(round(d, 4) for _, d in diffs))
    print(f"Jumlah kanal (T+F+S) dikurangi Skor Fraud -> nilai unik: {uniq}")
    print("  Contoh:", diffs[:5])

# ---------------------------------------------------------------- pairwise klinis
h("4b. PAIRWISE KLINIS (dx -> prosedur) DAN OBAT")
pairs = Counter()
for r in ROWS:
    dx = norm(r["Diagnosis ICD-10"]).split(" - ")[0]
    pr = norm(r["Prosedur ICD-9-CM"]).split(" - ")[0]
    pairs[(dx, pr)] += 1
for k, v in sorted(pairs.items()):
    print(f"   {k[0]:<8} -> {k[1]:<8} n={v}")

# dx tanpa prosedur
dx_no_proc = sorted(set(norm(r["Diagnosis ICD-10"]) for r in ROWS if not nonempty(r, "Prosedur ICD-9-CM")))
proc_none = [r["Name"] for r in ROWS if norm(r["Prosedur ICD-9-CM"]) in ("", "-", "—")]
print("Diagnosis tanpa prosedur:", dx_no_proc)
print("Baris prosedur kosong/tanda hubung:", proc_none)

# dx/proc vs label modus (klausul pairwise)
print("\nBaris dengan dx/proc yang bertentangan dengan modus skenario:")
for r in ROWS:
    m = norm(r["Modus"])
    dx = norm(r["Diagnosis ICD-10"]).split(" - ")[0]
    pr = norm(r["Prosedur ICD-9-CM"]).split(" - ")[0]
    bad = None
    if m == "upcoding" and not (dx == "K29.7" and pr == "00.66"):
        bad = f"upcoding dx={dx} proc={pr}"
    if m == "phantom_billing" and pr != "81.52":
        bad = f"phantom_billing proc={pr}"
    if m == "unbundling" and not (pr in ("51.23", "96.04")):
        bad = f"unbundling proc={pr}"
    if m == "cloning" and pr != "81.52":
        bad = f"cloning proc={pr}"
    if bad:
        print("   ", r["Name"], m, bad)

# Obat: parsing kode + satuan
print("\nSatuan obat yang dipakai:")
sat = Counter()
for r in ROWS:
    for m in re.finditer(r"(M\d{2})\s*x\s*(\d+)\s*([a-zA-Z]+)", norm(r["Obat"])):
        sat[m.group(3)] += 1
print("   ", dict(sat))
print("Obat dengan qty ekstrem (>=12):")
for r in ROWS:
    for m in re.finditer(r"(M\d{2})\s*x\s*(\d+)\s*([a-zA-Z]+)", norm(r["Obat"])):
        if int(m.group(2)) >= 12:
            print("   ", r["Name"], m.group(0), "|", norm(r["Obat"]))
print("Baris tanpa pola Mxx x N satuan:",
      [r["Name"] for r in ROWS if not re.findall(r"M\d{2}\s*x\s*\d+\s*[a-zA-Z]+", norm(r["Obat"]))])

# ---------------------------------------------------------------- 5. skema v2.1
h("5. SKEMA v2.1 vs AKTUAL")
CLAIMED_V21 = ["pasien_id", "faskes_id", "dokter_id", "seed", "version", "timestamp"]
present = [c for c in CLAIMED_V21 if c in CSV_COLS]
absent = [c for c in CLAIMED_V21 if c not in CSV_COLS]
print("Kolom v2.1 diklaim ada di CSV:", present)
print("Kolom v2.1 diklaim ada tapi TIDAK ada di CSV:", absent)
extra = [c for c in CSV_COLS if c not in CLAIMED_V21 and not c.startswith("_")]
print("Kolom ekstra di CSV yang tidak ada di kamus §5:", extra)

def uniq_pat(r):
    return norm(r["Pasien"]).split(" (")[0].strip()

ent = {
    "pasien": set(uniq_pat(r) for r in ROWS),
    "dokter": set(norm(r["Dokter"]).split(" (")[0].strip() for r in ROWS),
    "faskes": set(norm(r["Faskes"]) for r in ROWS),
    "diagnosis": set(norm(r["Diagnosis ICD-10"]).split(" - ")[0] for r in ROWS),
    "prosedur": set(norm(r["Prosedur ICD-9-CM"]).split(" - ")[0] for r in ROWS if nonempty(r, "Prosedur ICD-9-CM")),
    "obat": set(m.group(1) for r in ROWS for m in re.finditer(r"(M\d{2})", norm(r["Obat"]))),
}
CLAIMED_ENT = {"pasien": 40, "dokter": 20, "faskes": 10}
print("\nEntitas unik aktual vs klaim v2.1:")
for k, v in ent.items():
    c = CLAIMED_ENT.get(k)
    print(f"   {k:<10} aktual={len(v):<4} klaim={(c if c else 'tidak diklaim')}")
print("   Pasien:", sorted(ent["pasien"]))
print("   Dokter:", sorted(ent["dokter"]))
print("   Faskes:", sorted(ent["faskes"]))
print("   Obat:", sorted(ent["obat"]))
# entitas v2.1 diklaim P01-P40 / D01-D20 / RS_A-RS_J
p_missing = [f"P{i:02d}" for i in range(1, 41) if f"P{i:02d}" not in ent["pasien"]]
d_missing = [f"D{i:02d}" for i in range(1, 21) if f"D{i:02d}" not in ent["dokter"]]
f_missing = [f"RS_{c}" for c in "ABCDEFGHIJ" if f"RS_{c}" not in ent["faskes"]]
print("Pasien P01-P40 tidak ada:", p_missing)
print("Dokter D01-D20 tidak ada:", d_missing)
print("Faskes RS_A-RS_J tidak ada:", f_missing)

# ---------------------------------------------------------------- 6. masalah data
h("6. MASALAH DATA NYATA")
# 6a duplikat near-identical
sig = defaultdict(list)
for r in ROWS:
    sig[(norm(r["Tanggal"]), norm(r["Pasien"]), norm(r["Diagnosis ICD-10"]),
         norm(r["Prosedur ICD-9-CM"]), norm(r["LOS hari"]), norm(r["Biaya Rp"]))].append(r["Name"])
dupe_groups = {k: v for k, v in sig.items() if len(v) > 1}
print(f"6a. Grup duplikat (tanggal+pasien+dx+proc+LOS+biaya identik): {len(dupe_groups)}")
for k, v in dupe_groups.items():
    print("   ", v, k)

# 6b duplikat payload identik kecuali ID
sig2 = defaultdict(list)
for r in ROWS:
    payload = tuple(norm(r[c]) for c in CSV_COLS
                    if c not in ("Name", "_notion_page_id", "_last_edited"))
    sig2[payload].append(r["Name"])
dup2 = {k: v for k, v in sig2.items() if len(v) > 1}
print(f"\n6b. Grup dengan SELURUH payload identik (kecuali ID): {len(dup2)}")
for k, v in dup2.items():
    print("   ", v)

# 6c tanggal
dates = []
bad_date = []
for r in ROWS:
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", norm(r["Tanggal"]))
    if not m:
        bad_date.append((r["Name"], norm(r["Tanggal"])))
        continue
    try:
        dates.append((r["Name"], date(int(m.group(1)), int(m.group(2)), int(m.group(3)))))
    except ValueError:
        bad_date.append((r["Name"], norm(r["Tanggal"])))
print(f"\n6c. Format tanggal tidak valid: {bad_date}")
ds = sorted(d for _, d in dates)
print(f"   rentang: {ds[0]} .. {ds[-1]}")
print(f"   jumlah unik tanggal: {len(set(ds))}")
print(f"   '_last_edited' unik: {len(set(norm(r['_last_edited']) for r in ROWS))} ->",
      sorted(set(norm(r['_last_edited']) for r in ROWS))[:3])

# 6d outlier biaya: IQR dan MAD
biaya = sorted(int(num(r["Biaya Rp"]) or 0) for r in ROWS)


def iqr_outliers(vals):
    q1 = statistics.quantiles(vals, n=4)[0]
    q3 = statistics.quantiles(vals, n=4)[2]
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return lo, hi, q1, q3


lo, hi, q1, q3 = iqr_outliers(biaya)
med = statistics.median(biaya)
mad = statistics.median([abs(b - med) for b in biaya])
print(f"\n6d. Biaya: min={biaya[0]:,} median={med:,.0f} Q1={q1:,.0f} Q3={q3:,.0f} max={biaya[-1]:,}")
print(f"   IQR fence: [{lo:,.0f}, {hi:,.0f}]  -> outlier atas: {sum(1 for b in biaya if b > hi)}")
print(f"   MAD={mad:,.0f} -> robust z>3.5: {sum(1 for b in biaya if 0.6745*(b-med)/mad > 3.5)}")
out_rows = sorted([(r["Name"], int(num(r["Biaya Rp"])), norm(r["Risiko"]), norm(r["Status"]))
                    for r in ROWS if num(r["Biaya Rp"]) > hi], key=lambda x: -x[1])
print("   Baris biaya di atas pagar IQR:")
for o in out_rows:
    print("     ", o)
print(f"   Rasio biaya: maks/min = {biaya[-1]/biaya[0]:,.0f}x")
print(f"   Baris biaya < 1.000.000: {sum(1 for b in biaya if b < 1000000)}")

# 6e kolom wajib kosong
print("\n6e. Baris dengan kolom wajib kosong (Name/Status/Risiko/Skor Fraud/Tanggal/Biaya/Pasien/Dokter/Faskes/Diagnosis/Narasi):")
req = ["Name", "Status", "Risiko", "Skor Fraud", "Tanggal", "Biaya Rp",
       "Pasien", "Dokter", "Faskes", "Diagnosis ICD-10", "Narasi Rekam Medis"]
for c in req:
    miss = [r["Name"] for r in ROWS if not nonempty(r, c)]
    if miss:
        print(f"    {c}: {len(miss)} -> {miss}")
print("    (kolom di luar daftar wajib: tidak ada baris kosong di atas berarti lengkap)")

# 6f Alasan tidak cocok label
print("\n6f. Alasan tidak cocok dengan label Risiko:")
mismatch_alasan = []
for r in ROWS:
    a = norm(r["Alasan"])
    lab = norm(r["Risiko"])
    if not a:
        mismatch_alasan.append((r["Name"], lab, "(KOSONG)"))
        continue
    up = a.upper()
    if lab == "fraud" and not up.startswith("FRAUD"):
        mismatch_alasan.append((r["Name"], lab, a[:70]))
    elif lab == "high" and not (up.startswith("ANOMALI TINGGI") or up.startswith("ANOMALI SEDANG")):
        mismatch_alasan.append((r["Name"], lab, a[:70]))
    elif lab == "medium" and not (up.startswith("ANOMALI SEDANG") or up.startswith("ANOMALI TINGGI")):
        mismatch_alasan.append((r["Name"], lab, a[:70]))
    elif lab == "low" and not up.startswith("NORMAL"):
        mismatch_alasan.append((r["Name"], lab, a[:70]))
for m in mismatch_alasan:
    print("    ", m)
print("    total:", len(mismatch_alasan))

# 6g Kontradiksi Narasi
print("\n6g. Kontradiksi Narasi True:", sum(1 for r in ROWS if norm(r["Kontradiksi Narasi"]) == "True"))
kontr = [(r["Name"], norm(r["Risiko"]), norm(r["Modus"])) for r in ROWS
         if norm(r["Kontradiksi Narasi"]) == "True"]
print("    ", kontr)
# klaim 10: 8 klaim kontradiksi (KLM001-006, KLM018, KLM024)
claimed_kontr = {"KLM001", "KLM002", "KLM003", "KLM004", "KLM005", "KLM006", "KLM018", "KLM024"}
actual_kontr = {k[0] for k in kontr}
print("    klaim 10-simulation: 8 klaim (KLM001-006, KLM018, KLM024)")
print("    aktual:", sorted(actual_kontr))
print("    tidak cocok:", sorted(actual_kontr - claimed_kontr), "| hilang:", sorted(claimed_kontr - actual_kontr))

# 6h sentimen: klaim 62 positif / 14 netral / 24 negatif (untuk 100 klaim) vs 300
print("\n6h. Distribusi sentimen aktual (300 baris):", dict(Counter(norm(r["Sentimen"]) for r in ROWS)))
print("    klaim v100: 62 positif / 14 netral / 24 negatif")

# 6i Skor Sentimen vs kategori
print("\n6i. Skor Sentimen vs kategori Sentimen:")
sent_stat = defaultdict(list)
sent_mismatch = []
for r in ROWS:
    s = num(r["Skor Sentimen"])
    c = norm(r["Sentimen"])
    sent_stat[c].append(s)
    if s is None:
        sent_mismatch.append((r["Name"], c, s))
for c, v in sent_stat.items():
    print(f"    {c}: n={len(v)} min={min(v):.2f} maks={max(v):.2f} mean={statistics.mean(v):.3f}")
# apakah label sentimen monoton dengan skor?
neg_pos_overlap = sum(1 for r in ROWS
                       if norm(r["Sentimen"]) == "negatif" and (num(r["Skor Sentimen"]) or 0) > 0)
pos_neg_overlap = sum(1 for r in ROWS
                      if norm(r["Sentimen"]) == "positif" and (num(r["Skor Sentimen"]) or 0) < 0)
print(f"    'negatif' dengan skor > 0: {neg_pos_overlap} ; 'positif' dengan skor < 0: {pos_neg_overlap}")

# 6j Rujukan: 'undefined'
undef = [(r["Name"], norm(r["Rujukan"])) for r in ROWS if "undefined" in norm(r["Rujukan"]).lower()]
print(f"\n6j. Baris dengan 'undefined' pada kolom Rujukan: {len(undef)}")
for u in undef[:15]:
    print("    ", u)
ruj_pat = Counter(re.sub(r"^Puskesmas [^·]+·\s*", "", norm(r["Rujukan"])).split("·")[0].strip() for r in ROWS)
print("    prefiks rujukan (setelah nama puskesmas):", dict(list(ruj_pat.items())[:8]))

# 6k alasan obat vs dx (pairwise)dx->obat
print("\n6k. dx -> obat (klasifikasi correspondance):")
dx_obat = defaultdict(Counter)
for r in ROWS:
    dx = norm(r["Diagnosis ICD-10"]).split(" - ")[0]
    for m in re.finditer(r"(M\d{2})", norm(r["Obat"])):
        dx_obat[dx][m.group(1)] += 1
for dx in sorted(dx_obat):
    print(f"    {dx:<8} {dict(dx_obat[dx])}")

# ---------------------------------------------------------------- ringkasan temuan
h("RINGKASAN TEMUAN (dipakai untuk tabel severity di laporan)")
SEV_ORDER = {"KRITIS": 0, "TINGGI": 1, "SEDANG": 2, "RINGAN": 3}
sev_count = Counter(s for s, _, _, _ in FINDINGS)
print("Severity:", dict(sev_count))
for s, c, t, d in sorted(FINDINGS, key=lambda x: (SEV_ORDER[x[0]], x[1])):
    print(f"  [{s}] {c}: {t}")
    if d:
        print(f"        {d}")

# ---------------------------------------------------------------- dump JSON hasil
with open(os.path.join(os.path.dirname(__file__), "04_audit_results.json"), "w",
          encoding="utf-8") as f:
    json.dump({
        "n_rows": len(ROWS),
        "n_cols": len(CSV_COLS),
        "id_ok": OUT["id_ok"],
        "status": dict(status_c),
        "risiko": dict(risiko_c),
        "los_kosong": len(los_empty),
        "alasan_kosong": len(alasan_empty),
        "modus_kosong": len(modus_empty),
        "sindikat_kosong": len(sind_empty),
        "total_biaya": total_biaya,
        "nominal_per_status": dict(per_status),
        "mismatch_threshold_ge": mismatch_ge,
        "mismatch_threshold_gt": mismatch_gt,
        "edge_scores": edge,
        "v21_missing": absent,
        "entitas": {k: len(v) for k, v in ent.items()},
        "sentimen": dict(Counter(norm(r["Sentimen"]) for r in ROWS)),
        "kontradiksi_ids": sorted(actual_kontr),
    }, f, ensure_ascii=False, indent=1)
print("\n[ditulis] 04_audit_results.json di folder scripts/")
