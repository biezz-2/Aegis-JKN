import csv, sys
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.reader(open(r"N:/HEALTHKATHON/analysis/corpus/dataset_research_live.csv", encoding="utf-8")))
hdr = rows[0]
for i, r in enumerate(rows[1:], 1):
    blob = " ".join(r)
    if "Medical" in blob or "MIMIC" in blob or "review" in blob.lower():
        print("=== row", i, "item:", r[hdr.index("Item")])
        for k, v in zip(hdr, r):
            if k.startswith("_"):
                continue
            print("   %-24s %s" % (k, v[:300]))
        print()
