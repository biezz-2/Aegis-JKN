import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = 'N:/HEALTHKATHON/analysis/reports/'
JOBS = [
    ('11-compliance.md', [(29, 50), (96, 140), (160, 200), (225, 280), (298, 320), (345, 400), (405, 435)]),
    ('06-graph-mhgsl.md', [(11, 32), (100, 160), (186, 215), (228, 300), (300, 400), (425, 480)]),
    ('21-numbers-of-record.md', [(40, 105), (128, 200), (218, 265)]),
]
for fname, ranges in JOBS:
    t = open(BASE + fname, encoding='utf-8', errors='replace').read().split('\n')
    print('=' * 20, fname, 'lines', len(t))
    for a, b in ranges:
        print('  --', a, '-', b)
        for i in range(a, min(b, len(t)) + 1):
            s = t[i - 1]
            if s.strip():
                print('   %4d| %s' % (i, s[:220]))
