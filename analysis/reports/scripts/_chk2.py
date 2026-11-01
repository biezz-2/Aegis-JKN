import csv, sys, io, collections
sys.stdout = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_chk2.out", "w", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.DictReader(open(r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv", encoding="utf-8")))

cols = ["Umpan Balik Pasien", "Narasi Rekam Medis", "Alasan Berobat", "Rujukan",
        "Catatan", "Alasan", "Sinyal SHAP", "Kontribusi Saluran", "Diagnosis ICD-10"]
for c in cols:
    vals = [r[c].strip() for r in rows]
    ne = [v for v in vals if v]
    u = collections.Counter(ne)
    print(f"{c:24} nonempty={len(ne):4} unique={len(u):4} dup={len(ne)-len(u):4} "
          f"maxlen={max(len(v) for v in ne):4} minlen={min(len(v) for v in ne):3}")

print("\nRujukan contains 'undefined':", sum(1 for r in rows if "undefined" in r["Rujukan"]))
print("Rujukan == kunjungan langsung:", sum(1 for r in rows if r["Rujukan"].strip() == "kunjungan langsung (tanpa rujukan)"))
print("Sinyal SHAP == 'tidak ada sinyal dominan':", sum(1 for r in rows if r["Sinyal SHAP"].strip() == "tidak ada sinyal dominan"))
print("Alasan kosong:", [r["Name"] for r in rows if not r["Alasan"].strip()])
print("Obat == '—':", [r["Name"] for r in rows if r["Obat"].strip() == "—"])
print("Catatan kosong count:", sum(1 for r in rows if not r["Catatan"].strip()))

# narasi: dx-deviating rows
dev = [r for r in rows if "kateterisasi jantung" in r["Narasi Rekam Medis"]
       or "Tercatat tindakan" in r["Narasi Rekam Medis"]]
print("\nnarasi deviating rows:", [(r["Name"], r["Modus"]) for r in dev])

# modus monotone
m = collections.defaultdict(set)
for r in rows:
    if r["Modus"].strip():
        m[r["Modus"]].add(r["Sentimen"])
print("\nmodus:", len(m))
for k, v in sorted(m.items()):
    print(f"  {k:24} {sorted(v)}  {'MONOTON' if len(v)==1 else 'MULTI'}")
print("monoton:", sum(1 for v in m.values() if len(v) == 1), "dari", len(m))
