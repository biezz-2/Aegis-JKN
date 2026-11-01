import sys, io, os, re, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'N:/HEALTHKATHON/analysis/reports/00-EXECUTIVE-SUMMARY.md'
t = open(p, encoding='utf-8').read()
lines = t.split('\n')
print('lines:', len(lines), 'words:', len(t.split()))
bad = {}
for i, l in enumerate(lines):
    for ch in l:
        o = ord(ch)
        if o < 128:
            continue
        if ch in '—–‐‑‒−':
            print('DASH', i+1, repr(ch), l[:120]); continue
        if 0x4E00 <= o <= 0x9FFF or 0x3040 <= o <= 0x30FF or 0xAC00 <= o <= 0xD7AF:
            print('CJK', i+1, repr(ch), l[:160]); continue
        bad.setdefault(ch, []).append(i+1)
for ch, ls in bad.items():
    print('NONASCII', repr(ch), unicodedata.name(ch, '?'), 'count', len(ls), 'first lines', ls[:6])
# table row count
for i, l in enumerate(lines):
    if l.startswith('| F-'):
        pass
print('F-items:', sum(1 for l in lines if re.match(r'^\| F-\d\d ', l)))
print('key-number rows:', sum(1 for l in lines if re.match(r'^\| \d+ \| ', l)))
