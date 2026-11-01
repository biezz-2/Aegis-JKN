import re, sys, io

path = sys.argv[1]
src = open(path, encoding='utf-8').read()
lines = src.split('\n')

# match a double-quoted string literal followed by a % operator
lit_re = re.compile(r'"((?:[^"\\]|\\.)*)"')
spec_re = re.compile(r'%[-+#0-9.]*[a-zA-Z]')

bad = 0
for i, line in enumerate(lines, 1):
    if 'print(' not in line:
        continue
    for m in lit_re.finditer(line):
        lit = m.group(1)
        # does this literal feed a % operator?
        rest = line[m.end():]
        if not re.match(r'\s*%', rest):
            continue
        n_double = lit.count('%%')
        total = lit.count('%')
        consumed = total - 2 * n_double
        specs = spec_re.findall(lit)
        if consumed != len(specs):
            bad += 1
            print("LINE %d: consumed=%d specs=%d :: %s" % (i, consumed, len(specs), line.strip()[:130]))

print("---")
print("mismatched lines: %d" % bad)
