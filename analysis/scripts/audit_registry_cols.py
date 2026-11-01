import csv, io, sys
sys.stdout.reconfigure(encoding='utf-8')
rows = list(csv.DictReader(io.open('N:/HEALTHKATHON/analysis/corpus/claims_v2_live.csv', encoding='utf-8-sig')))
cols = list(rows[0].keys())
reg = open('N:/HEALTHKATHON/analysis/corpus/03-dataset-registry.md', encoding='utf-8').read()
miss = [c for c in cols if c not in reg and c not in ('_notion_page_id', '_last_edited')]
print('CSV cols not mentioned in 03-dataset-registry.md:', miss)
print('total CSV cols:', len(cols))
for f in ['07-dataset-v2-catalog.md', '08-training-protocol.md']:
    L = open('N:/HEALTHKATHON/analysis/corpus/' + f, encoding='utf-8').read().split('\n')
    print('==', f)
    for i, l in enumerate(L[:6]):
        print('  ', i + 1, '|', l[:130])
