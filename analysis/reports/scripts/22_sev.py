import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = r'N:/HEALTHKATHON/analysis/reports'
pat = re.compile(r'^\|\s*\**\s*(CRITICAL|BLOCKER|KRITIS|HIGH|TINGGI|MEDIUM|SEDANG|LOW|RINGAN|P0|P1|P2)\s*\**\s*\|')
for f in sorted(x for x in os.listdir(d) if x.endswith('.md')):
    t = open(os.path.join(d, f), encoding='utf8', errors='replace').read().split('\n')
    out = []
    for i, l in enumerate(t):
        if pat.match(l):
            out.append((i + 1, l[:170]))
    if out:
        print('=' * 25, f)
        for n, l in out:
            print(n, '|', l)
