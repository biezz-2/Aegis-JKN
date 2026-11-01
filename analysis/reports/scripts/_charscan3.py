import sys
sys.stdout.reconfigure(encoding="utf-8")
R = r"N:/HEALTHKATHON/analysis/reports/"
T = [
    ("01-governance.md", 18), ("01-governance.md", 122), ("01-governance.md", 284),
    ("05-evidence.md", 275), ("11-compliance.md", 83), ("11-compliance.md", 209),
    ("20-repo-artifact-integrity.md", 164), ("22-proposal-docx-audit.md", 168),
    ("22-proposal-docx-audit.md", 174), ("22-proposal-docx-audit.md", 176),
    ("22-proposal-docx-audit.md", 262), ("22-proposal-docx-audit.md", 298),
]
for f, n in T:
    L = open(R + f, encoding="utf-8").read().split("\n")
    print("### %s L%d" % (f, n))
    print(repr(L[n - 1]))
    print()
