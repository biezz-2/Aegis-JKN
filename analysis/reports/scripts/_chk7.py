import csv, sys, io, collections, re
sys.stdout = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_chk7.out", "w", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.DictReader(open(r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv", encoding="utf-8")))
byid = {r["Name"]: r for r in rows}

print("=== phantom rows, raw fields ===")
for i in ("KLM004", "KLM005", "KLM006"):
    r = byid[i]
    print(i, "| Pasien:", r["Pasien"], "| Obat:", repr(r["Obat"]))
    print("    Prosedur ICD-9-CM:", repr(r.get("Prosedur ICD-9-CM", "")))
    print("    Narasi:", repr(r["Narasi Rekam Medis"]))

nars = {byid[i]["Narasi Rekam Medis"] for i in ("KLM004", "KLM005", "KLM006")}
print("\nidentical narratives:", len(nars) == 1)
print("cols:", list(rows[0].keys()))

print("\n=== identifier-ish tokens in Narasi ===")
for r in rows:
    toks = re.findall(r"P\d{2}\b|NIK|tanggal lahir|\d{2}[./-]\d{2}[./-]\d{4}", r["Narasi Rekam Medis"])
    if toks:
        print(" ", r["Name"], toks, "|", r["Narasi Rekam Medis"][:150])

print("\n=== doctor/patient/faskes samples ===")
print("Pasien:", rows[0]["Pasien"], "|", rows[3]["Pasien"], "|", rows[2]["Pasien"])
print("Dokter:", rows[0].get("Dokter"), "|", rows[12].get("Dokter"))
print("Faskes:", rows[0].get("Faskes"), "|", rows[3].get("Faskes"))

print("\n=== t-sweep conflicts ===")
for t in (0.05, 0.10, 0.15, 0.16, 0.20, 0.25, 0.30, 0.31, 0.35, 0.40, 0.50, 0.60):
    wrong = 0
    for r in rows:
        s = float(r["Skor Sentimen"]); lab = r["Sentimen"]
        pred = "netral" if abs(s) < t else ("positif" if s > t else "negatif")
        if pred != lab:
            wrong += 1
    print(f"  t={t:<5} conflicts={wrong:<4} acc={100*(300-wrong)/300:.2f}%")
