import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = r'N:/HEALTHKATHON/analysis/reports'
checks = [
    ('03-architecture.md', ['Rule engine', 'ignoreBuildErrors', 'leakage', 'θ_feat']),
    ('07-generator.md', ['KLM004', 'seed', '9/9', 'phantom']),
    ('13-text-channel.md', ['lookup', 'Modus', 'KLM001']),
    ('17-roadmap.md', ['10 hari', 'B-01', 'G-03']),
    ('16-red-team.md', ['Heliyon', '97,0', '0.986']),
    ('15-code-quality.md', ['test_leakage', 'ignoreBuildErrors', 'tsc --noEmit', 'npm test']),
]
for f, ps in checks:
    t = open(os.path.join(d, f), encoding='utf-8', errors='replace').read().split('\n')
    print('==' * 6, f)
    for i, l in enumerate(t):
        for p in ps:
            if p in l:
                print('  ', i + 1, '|', l.strip()[:140])
                break
