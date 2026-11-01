import csv, sys, io, collections
sys.stdout = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_chk9.out", "w", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.DictReader(open(r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv", encoding="utf-8")))
nar = collections.Counter(r["Narasi Rekam Medis"].strip() for r in rows)
print("unique narasi:", len(nar))
for s, c in nar.most_common(8):
    print(f"  x{c:<3} {s[:95]}")
print("\n--- Rujukan sample with undefined ---")
n = 0
for r in rows:
    if "undefined" in r["Rujukan"]:
        print("  ", r["Name"], repr(r["Rujukan"]))
        n += 1
        if n >= 3:
            break
print("\n--- feedback max/min len check ---")
fl = [len(r["Umpan Balik Pasien"].strip()) for r in rows]
print("min", min(fl), "max", max(fl))
nl = [len(r["Narasi Rekam Medis"].strip()) for r in rows]
print("narasi min", min(nl), "max", max(nl))
al = [len(r["Alasan Berobat"].strip()) for r in rows]
print("alasan berobat min", min(al), "max", max(al))
