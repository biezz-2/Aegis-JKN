import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
base = r'N:/HEALTHKATHON/Aegis-JKN/'
targets = {
    'src/components/mhgsl/i18n.tsx': [443, 791, 352],
    'src/components/mhgsl/data.ts': [391, 392, 437, 451, 463, 464, 503, 507, 418],
    'src/components/mhgsl/data-uploader.tsx': [137],
}
for f, lines in targets.items():
    p = base + f
    t = open(p, encoding='utf-8', errors='replace').read().split('\n')
    print('==' * 6, f)
    for n in lines:
        if n <= len(t):
            print('  ', n, '|', t[n-1].strip()[:230])
