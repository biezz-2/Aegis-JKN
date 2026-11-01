import re, sys
sys.stdout.reconfigure(encoding="utf-8")
t = open(r"N:/HEALTHKATHON/analysis/reports/scripts/_charscan.txt", encoding="utf-8").read()
blocks = re.split(r"(?m)^### ", t)
for b in blocks:
    if b.startswith(("ARABIC", "CJK", "CYRILLIC", "THAI", "EMOJI", "EMDASH")):
        print("### " + b.rstrip())
        print()
