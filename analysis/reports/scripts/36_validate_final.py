import io, sys, os, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = 'N:/HEALTHKATHON/analysis/reports/'
DOC = BASE + '00-EXECUTIVE-SUMMARY.md'
doc = open(DOC, encoding='utf-8').read()
doc_lines = doc.split('\n')

# 1. every `file.md:N` or `file.md:N-M` reference must point to an existing line
files = {}
for fn in os.listdir(BASE):
    if fn.endswith('.md'):
        files[fn] = len(open(BASE + fn, encoding='utf-8', errors='replace').read().split('\n'))

pat = re.compile(r'`?([0-9A-Za-z\-_]+\.md):(\d+)(?:-(\d+))?')
bad = []
refs = collections.Counter()
for m in pat.finditer(doc):
    fn, a, b = m.group(1), int(m.group(2)), m.group(3)
    b = int(b) if b else a
    if fn not in files:
        bad.append(('MISSING FILE', fn, a, b))
        continue
    if a < 1 or b > files[fn] or a > b:
        bad.append(('OUT OF RANGE', fn, a, b, 'file has', files[fn]))
    refs[fn] += 1

print('== line-reference check ==')
print('distinct source files cited:', len(refs))
if bad:
    for x in bad:
        print('  BAD', x)
else:
    print('  all references in range')

# 2. source map consistency: F-item -> report
frows = [l for l in doc_lines if re.match(r'^\| F-\d\d ', l)]
f2src = collections.defaultdict(set)
for l in frows:
    fid = l.split('|')[1].strip()
    for m in re.finditer(r'`([0-9A-Za-z\-_]+\.md):', l):
        f2src[m.group(1)].add(fid)

maprows = [l for l in doc_lines if l.startswith('| `') and l.count('|') >= 4 and re.search(r'F-\d\d', l)]
print()
print('== source map check ==')
print('F-items:', len(frows), ' map rows:', len(maprows))
mapdict = {}
for l in maprows:
    fn = l.split('|')[1].strip().strip('`')
    ids = set(re.findall(r'F-\d\d', l))
    mapdict[fn] = ids
    if fn in f2src and ids != f2src[fn]:
        print('  MISMATCH', fn, 'map:', sorted(ids), 'actual:', sorted(f2src[fn]))
    elif fn not in f2src:
        print('  MAP-ONLY (not cited in F rows):', fn, sorted(ids))
for fn in f2src:
    if fn not in mapdict:
        print('  F-ROW-ONLY (missing from map):', fn, sorted(f2src[fn]))

# 3. F-id continuity
ids = [int(l.split('|')[1].strip().split('-')[1]) for l in frows]
print()
print('== F-id continuity ==')
print('  range', min(ids), '-', max(ids), 'count', len(ids), 'duplicates', len(ids) != len(set(ids)))
missing = [i for i in range(min(ids), max(ids) + 1) if i not in ids]
print('  gaps:', missing if missing else 'none')

# 4. table row column consistency
print()
print('== markdown table check ==')
incode = False
tbl = []
for i, l in enumerate(doc_lines, 1):
    if l.startswith('```'):
        incode = not incode
    if incode:
        continue
    if l.strip().startswith('|') and l.strip().endswith('|'):
        tbl.append((i, l.count('|')))
    else:
        if len(tbl) > 1:
            widths = set(w for _, w in tbl)
            if len(widths) > 1:
                print('  RAGGED table ending line', tbl[-1][0], 'widths', sorted(widths))
        tbl = []

# 5. non-ascii
print()
print('== non-ascii ==')
found = False
for i, l in enumerate(doc_lines, 1):
    for ch in l:
        if ord(ch) > 127:
            print('  line', i, repr(ch), hex(ord(ch)))
            found = True
if not found:
    print('  clean')
