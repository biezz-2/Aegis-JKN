import re, glob, os
base = "N:/HEALTHKATHON/analysis/reports/work22"
files = sorted(glob.glob(os.path.join(base, "hkchunks", "*.js"))) + [
    os.path.join(base, "main.js"), os.path.join(base, "runtime.js")]
for f in files:
    if not os.path.exists(f):
        continue
    d = open(f, encoding="utf-8", errors="replace").read()
    low = d.lower()
    if "referensi" in low or "siklus" in low:
        print("==", os.path.basename(f), len(d))
        for m in re.finditer(r".{140}(?:referensi|siklus).{180}", d, re.S | re.I):
            print("   ", m.group(0)[:330].replace("\n", " "))
