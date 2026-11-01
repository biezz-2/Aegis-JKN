import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = 'N:/HEALTHKATHON/analysis/reports/'

# (file, [(start, end), ...]) -- ranges to dump for eyeball verification
JOBS = [
    ('13-text-channel.md', [(18, 22), (30, 40), (43, 50), (95, 99), (140, 175), (218, 224), (248, 256), (330, 336), (378, 400), (402, 410), (468, 475), (528, 534)]),
    ('04-data-quality.md', [(36, 48), (58, 68), (74, 90), (340, 372), (410, 418), (455, 460), (486, 492), (545, 552), (560, 570)]),
    ('10-competition.md', [(10, 20), (28, 45), (240, 250), (278, 284), (290, 300), (370, 380), (385, 412), (415, 430), (450, 470)]),
    ('19-consistency.md', [(10, 30), (42, 48), (168, 175), (185, 190), (196, 200), (237, 242), (255, 260), (270, 276), (308, 312), (325, 330), (441, 446), (550, 556)]),
    ('02-proposal.md', [(60, 70), (73, 80), (85, 100), (108, 120), (132, 145), (152, 160), (162, 176), (196, 200), (247, 252), (408, 420), (438, 446)]),
]

for fname, ranges in JOBS:
    t = open(BASE + fname, encoding='utf-8', errors='replace').read().split('\n')
    print('=' * 20, fname, 'lines', len(t))
    for a, b in ranges:
        print('  --', a, '-', b)
        for i in range(a, min(b, len(t)) + 1):
            s = t[i - 1]
            if s.strip():
                print('   %4d| %s' % (i, s[:230]))
