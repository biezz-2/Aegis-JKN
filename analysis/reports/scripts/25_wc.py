import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
t = open(r'N:/HEALTHKATHON/analysis/reports/00-EXECUTIVE-SUMMARY.md', encoding='utf-8').read().split('\n')
a = next(i for i, l in enumerate(t) if l.startswith('## 1. Ringkasan'))
b = next(i for i, l in enumerate(t) if l.startswith('## 2. Register'))
sec = '\n'.join(t[a:b])
print('section1 lines:', b - a, 'words:', len(re.findall(r'\S+', sec)))
print('total lines:', len(t))
