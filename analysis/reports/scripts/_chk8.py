import csv, sys, io, re
sys.stdout = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_chk8.out", "w", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.DictReader(open(r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv", encoding="utf-8")))
byid = {r["Name"]: r for r in rows}
for i in ("KLM004", "KLM005", "KLM006"):
    r = byid[i]
    print(i, "| Dokter:", r["Dokter"], "| Faskes:", r["Faskes"], "| Sindikat:", r["Sindikat"])
    print("   Catatan:", repr(r["Catatan"]))
    print("   Alasan:", repr(r["Alasan"][:200]))
    print("   Umpan:", repr(r["Umpan Balik Pasien"]))
    print("   dx:", r["Diagnosis ICD-10"], "|LOS:", r["LOS hari"])

print("\n=== grep late fusion quote in architecture_full.md ===")
p = r"N:\HEALTHKATHON\Notion-docs\architecture_full.md"
for i, l in enumerate(io.open(p, encoding="utf-8").read().split("\n"), 1):
    if "late fusion" in l or "berdiri sendiri" in l or "dikonfirmasi silang" in l:
        print(f"  L{i}: {l[:260]}")
print("\n=== lines 179-186 ===")
for i, l in enumerate(io.open(p, encoding="utf-8").read().split("\n"), 1):
    if 179 <= i <= 186:
        print(f"  L{i}: {l[:300]}")
