#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit ronde 5: verifikasi penutup."""
import csv, os, re, sys, statistics
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
rows = list(csv.DictReader(open(os.path.join(CORPUS, "claims_v2_live.csv"),
                                encoding="utf-8-sig", newline="")))
n = lambda v: "" if v is None else str(v).strip()
def h(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# 1. Kolom 03 §5 vs CSV
h("1. KOLOM 03 §5 vs CSV")
DICT = ["Name","Tanggal","Pasien","Dokter","Faskes","Diagnosis ICD-10","Prosedur ICD-9-CM","Obat",
        "LOS hari","Biaya Rp","Narasi Rekam Medis","Kontradiksi Narasi","Skor Fraud","Risiko","Status",
        "Modus","Sindikat","Alasan","Sinyal SHAP","Kontribusi Saluran","Skor Sentimen","Sentimen",
        "Umpan Balik Pasien","Catatan"]
csvc = list(rows[0].keys())
biz = [c for c in csvc if not c.startswith("_")]
print("properti di kamus §5:", len(DICT))
print("kolom bisnis di CSV :", len(biz))
print("ADA di kamus tapi TIDAK di CSV:", sorted(set(DICT) - set(csvc)))
print("ADA di CSV tapi TIDAK di kamus:", sorted(set(biz) - set(DICT)))
print("kolom metadata Notion:", [c for c in csvc if c.startswith("_")])

# 2. _last_edited per rowgy
h("2. _last_edited: PETELAJAN")
le = defaultdict(list)
for r in rows: le[n(r["_last_edited"])].append(r["Name"])
for k in sorted(le): print(f"   {k}: n={len(le[k])} -> {le[k][:8]}{'...' if len(le[k])>8 else ''}")

# 3. KLM031: apakah satu-satunya yang diedit terpisah
h("3. KLM031")
r = [x for x in rows if x["Name"] == "KLM031"][0]
print("   _last_edited:", n(r["_last_edited"]), "| Alasan kosong:", n(r["Alasan"]) == "")
print("   risiko/status:", n(r["Risiko"]), n(r["Status"]))

# 4. Baris rawat inap LOS=0 & rawat jalan LOS=1
h("4. ANOMALI LOS vs LAYANAN")
print("rawat inap LOS=0 :", [(r["Name"], n(r["Diagnosis ICD-10"]).split(" - ")[0],
      n(r["Prosedur ICD-9-CM"]).split(" - ")[0], n(r["Sindikat"]), n(r["Risiko"]))
      for r in rows if n(r["Layanan"]) == "rawat inap" and n(r["LOS hari"]) == "0"])
print("rawat jalan LOS=1:", [(r["Name"], n(r["Diagnosis ICD-10"]).split(" - ")[0], n(r["Risiko"]),
      n(r["Biaya Rp"])) for r in rows if n(r["Layanan"]) == "rawat jalan" and n(r["LOS hari"]) == "1"])

# 5. Klaim 03 §6 "tidak ditemukan ketidaksesuaian label risiko vs rentang skor"
h("5. KLAIM §6: LABEL RISIKO vs RENTANG SKOR (dua interpretasi ambang)")
def lg(s, incl):  # incl=True -> s>=batas masuk kelas atas
    if s < 0.35 or (not incl and s <= 0.35): return "low"
    if s < 0.60 or (not incl and s <= 0.60): return "medium"
    if s < 0.80 or (not incl and s <= 0.80): return "high"
    return "fraud"
mm_i = [(r["Name"], n(r["Skor Fraud"]), n(r["Risiko"])) for r in rows if lg(float(n(r["Skor Fraud"])), True) != n(r["Risiko"])]
mm_e = [(r["Name"], n(r["Skor Fraud"]), n(r["Risiko"])) for r in rows if lg(float(n(r["Skor Fraud"])), False) != n(r["Risiko"])]
print("interpretasi '>= batas masuk kelas atas' (konsisten dengan data):", len(mm_i), "mismatch")
print("interpretasi '> batas masuk kelas atas' (konsisten dengan 10-sim §v2):", len(mm_e), "mismatch", mm_e)

# 6. Biaya vs alasan: apakah 'rasio' muncul untuk semua baris ber-acuan
h("6. COVERAGE 'RASIO' DI DALAM ALASAN")
TARIF = {"51.23":14500000,"00.66":58000000,"47.09":6800000,"53.1":8200000,"74.1":6200000,
         "81.52":46500000,"96.04":750000,"98.51":5600000}
tot=has=0
for r in rows:
    c = n(r["Prosedur ICD-9-CM"]).split(" - ")[0]
    if c in TARIF:
        tot += 1
        if "rasio" in n(r["Alasan"]): has += 1
print(f"baris dengan prosedur ber-acuan: {tot} | yang menyebut 'rasio': {has}")

# 7. Status/label mapping matrix final
h("7. MATRIKS STATUS x RISIKO (final)")
for k, v in sorted(Counter((n(r["Status"]), n(r["Risiko"])) for r in rows).items()):
    print(f"   {k[0]:<11} {k[1]:<7} {v}")
print("review = medium+high:", sum(1 for r in rows if n(r["Status"])=="review"),
      "| escalate = fraud:", sum(1 for r in rows if n(r["Status"])=="escalate"))
print("auto_clear = low:", sum(1 for r in rows if n(r["Status"])=="auto_clear" and n(r["Risiko"])=="low"))

# 8. Sindikat fraud count
h("8. HITUNGAN SINDIKAT")
sf = [r for r in rows if n(r["Risiko"])=="fraud" and n(r["Sindikat"])]
sh = [r for r in rows if n(r["Risiko"])=="high" and n(r["Sindikat"])]
nf = [r["Name"] for r in rows if n(r["Risiko"])=="fraud" and not n(r["Sindikat"])]
print(f"fraud DENGAN sindikat : {len(sf)}  -> {sorted(set(n(r['Sindikat']) for r in sf))}")
print(f"high DENGAN sindikat   : {len(sh)} -> {sorted(set(n(r['Sindikat']) for r in sh))} {sorted(r['Name'] for r in sh)}")
print(f"fraud TANPA sindikat  : {len(nf)} -> {nf}")
print("Total baris ber-sindikat:", sum(1 for r in rows if n(r["Sindikat"])))

# 9. Entitas: apakah nama Pasien unik per ID
h("9. ENTITAS PASIEN: ID -> NAMA")
pn = defaultdict(set)
for r in rows: pn[n(r["Pasien"]).split(" (")[0]].add(n(r["Pasien"]))
print("pasien dengan >1 nama:", {k: v for k, v in pn.items() if len(v) > 1})
dn = defaultdict(set)
for r in rows: dn[n(r["Dokter"]).split(" (")[0]].add(n(r["Dokter"]))
print("dokter dengan >1 nama:", {k: v for k, v in dn.items() if len(v) > 1})
print("cek ID rawam (tanpa nama) unik?", len({n(r['Pasien']).split(' (')[0] for r in rows}))

# 10. Umpan balik: apakah 36 template.bs
h("10. UMPAN BALIK PASIEN: TEMPLATE")
ub = Counter(n(r["Umpan Balik Pasien"]) for r in rows)
print("jumlah unik:", len(ub))
print("distribusi:", dict(Counter(ub.values())))

# 11. Skor sentimen: apakah 1 template per label sentimen
h("11. SKOR SENTIMEN: hub dengan label")
for lab in ("negatif","netral","positif"):
    v = sorted(float(n(r["Skor Sentimen"])) for r in rows if n(r["Sentimen"])==lab)
    if lab == "positif":
        gap = "-"
    elif lab == "negatif":
        pos = [x for x in v if x > 0]
        gap = round(min(pos) - max(v), 3) if pos else "n/a"
    else:
        gap = ""
    print(f"   {lab:<8} n={len(v)} min={min(v):.2f} maks={max(v):.2f} "
          f"nilai unik={len(set(v))} gap_ke_kelas_berikut={gap}")
print("cek: rentang negatif < 0 < netral 0..0.2 < positif >0.5 -> konsisten, "
      "TIDAK ada baris netral dengan skor di luar [0,0.2]:",
      sum(1 for r in rows if n(r["Sentimen"])=="netral" and not (0 <= float(n(r["Skor Sentimen"])) <= 0.2)))
