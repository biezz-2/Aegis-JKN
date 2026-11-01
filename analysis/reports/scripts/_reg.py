import csv, sys
sys.stdout.reconfigure(encoding="utf-8")
rows = list(csv.reader(open(r"N:/HEALTHKATHON/analysis/corpus/dataset_research_live.csv", encoding="utf-8")))
hdr = rows[0]
print("HEADER:", hdr)
print("total rows (excl header):", len(rows) - 1)
print()
for i, r in enumerate(rows[1:], 1):
    item = r[hdr.index("Item")] if "Item" in hdr else ""
    src = r[hdr.index("Sumber Riset")]
    desc = r[hdr.index("Deskripsi")]
    st = r[hdr.index("Status Verifikasi")]
    cat = r[hdr.index("Kategori")]
    print("row=%-3d item=%-6s | %-16s | %-22s | %s" % (i, item, st[:16], cat[:22], src[:70]))
    if "Medical" in desc or "Medical" in src:
        print("        >>> DESCR: %s" % desc[:400])
        print("        >>> CATATAN: %s" % r[hdr.index("Catatan Riset")][:300])
