import csv, sys, io
sys.stdout = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_chk1.out", "w", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.DictReader(open(r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv", encoding="utf-8")))
byid = {r["Name"]: r for r in rows}
for i in ["KLM001", "KLM002", "KLM003", "KLM018", "KLM024", "KLM012"]:
    r = byid[i]
    print(i, "| dx:", r["Diagnosis ICD-10"])
    print("   nar:", r["Narasi Rekam Medis"])
    print("   fb :", r["Umpan Balik Pasien"])
print("\n--- rows containing 'Tercatat tindakan' ---")
for r in rows:
    if "Tercatat tindakan" in r["Narasi Rekam Medis"]:
        print(r["Name"], "|", r["Modus"], "|", r["Narasi Rekam Medis"])
print("\n--- K29.7 narratives ---")
seen = set()
for r in rows:
    if r["Diagnosis ICD-10"].startswith("K29.7") and r["Narasi Rekam Medis"] not in seen:
        seen.add(r["Narasi Rekam Medis"])
        print("  ", repr(r["Narasi Rekam Medis"]))
