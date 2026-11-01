import re, base64, gzip, csv, io, json, sys
src = open("21_main_nb.txt", encoding="utf-8", errors="replace").read()
m = re.search(r'EMBEDDED_CLAIMS_CSV_B64\s*=\s*"([^"]+)"', src)
if not m:
    print("NO MATCH"); sys.exit(1)
raw = gzip.decompress(base64.b64decode(m.group(1)))
out = "N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv"
open(out, "wb").write(raw)
rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
print("rows:", len(rows))
print("cols:", list(rows[0].keys()))
