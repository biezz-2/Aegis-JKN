import re, sys
path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")
items = []
for ln in lines:
    m = re.match(r"\[(\d+)\](?:<([^>]*)>)? ?(.*)$", ln)
    if m:
        items.append((int(m.group(1)), m.group(2) or "", m.group(3)))

PATS = {
    "accuracy93": r"93[,.]0\s*%",
    "precision9412": r"94[,.]12\s*%",
    "rocauc09825": r"0[,.]9825",
    "auprc09142": r"0[,.]9142",
    "masking894": r"89[,.]4\s*%",
    "fpr106": r"10[,.]6\s*%",
    "time45": r"(45\s*%|-45\s*%)",
    "throughput32": r"3[,.]2\s*(kali|x|times)",
    "sus825": r"82[,.]5",
    "rp507": r"507[,.]37\s*(Juta|juta|jt|JT)|Rp\s*507",
    "rp3526": r"3[,.]53\s*(Miliar|miliar)|3[,.]526",
    "rp8456": r"8[,.]46\s*(Juta|juta)",
    "plus286": r"\+\s*28[,.]6\s*%",
    "plus20": r"\+\s*20\s*%",
    "60anomali": r"\b60\s+(klaim|anomali)",
    "300berkas": r"300\s+(berkas|klaim|portofolio|baris)",
    "tidakme": r"1\s*:\s*15",
    "ratusan": r"ratusan miliar|triliunan",
    "rp150": r"150\s*\+?\s*Triliun|150\s*Triliun",
    "rp35miliar": r"35\s*(miliar|Miliar)",
}
for name, pat in PATS.items():
    hits = [(i, t) for i, st, t in items if re.search(pat, t)]
    print("### %-14s %d hits" % (name, len(hits)))
    for i, t in hits:
        print("   [%04d] %s" % (i, t[:400]))
    print()
