import sys
sys.stdout.reconfigure(encoding="utf-8")
p = r"N:/HEALTHKATHON/analysis/corpus/11-archive-proposal.md"
lines = open(p, encoding="utf-8").read().split("\n")
l30 = lines[29]
i = l30.find("serta menyelamatkan")
if i < 0:
    i = l30.find("menyelamatkan")
print("LINE 30 len:", len(l30))
print("TAIL:", repr(l30[max(0, i - 120):]))
print()
print("em-dash in corpus 11:", l30.count("\u2014"))
print("full L30:")
print(l30)
