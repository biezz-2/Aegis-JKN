import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = 'N:/HEALTHKATHON/analysis/reports/'
JOBS = [
    ('13-text-channel.md', [(25, 40), (142, 175), (251, 258), (381, 400), (403, 412)]),
    ('04-data-quality.md', [(369, 374), (410, 416), (43, 48)]),
    ('19-consistency.md', [(24, 30), (255, 260), (270, 276), (550, 556)]),
    ('10-competition.md', [(14, 15), (28, 35), (370, 382), (386, 412), (453, 470)]),
    ('16-red-team.md', [(20, 27), (34, 38), (60, 64), (183, 197), (318, 324), (373, 380)]),
    ('09-security.md', [(202, 203), (274, 281), (304, 320)]),
    ('21-colab-dashboard-provenance.md', [(50, 74), (78, 82), (100, 106), (126, 130), (164, 168), (196, 200), (248, 252), (294, 298), (312, 320)]),
    ('08-frontend.md', [(190, 220), (230, 234)]),
    ('20-repo-artifact-integrity.md', [(9, 14), (90, 95), (119, 140), (180, 185), (207, 221)]),
    ('02-proposal.md', [(39, 58), (134, 142), (164, 176), (247, 252)]),
    ('06-methodology.md', [(36, 40), (155, 160), (210, 216)]),
]
for fname, ranges in JOBS:
    t = open(BASE + fname, encoding='utf-8', errors='replace').read().split('\n')
    print('=' * 18, fname, 'lines', len(t))
    for a, b in ranges:
        print('  --', a, '-', b)
        for i in range(a, min(b, len(t)) + 1):
            s = t[i - 1]
            if s.strip():
                print('   %4d| %s' % (i, s[:190]))
