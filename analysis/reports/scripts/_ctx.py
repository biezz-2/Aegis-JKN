import sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"N:/HEALTHKATHON/analysis/reports/"


def show(f, pat, ctx=1):
    L = open(R + f, encoding="utf-8").read().split("\n")
    for i, l in enumerate(L, 1):
        if pat in l:
            print("### %s L%d" % (f, i))
            for j in range(max(0, i - 1 - ctx), min(len(L), i + ctx)):
                print("   %d| %s" % (j + 1, L[j][:500]))
            print()


show("00-EXECUTIVE-SUMMARY.md", "Where laporan")
show("14-language.md", "kurung")
show("05-evidence.md", "volumePlaceholder")
show("05-evidence.md", "wasted effort")
show("05-evidence.md", "both bersumber")
