import csv, collections, re, sys

path = sys.argv[1]
rows = list(csv.DictReader(open(path, encoding='utf-8')))
print('TOTAL ROWS', len(rows))

c = collections.Counter((r['Modus'].strip(), r['Sindikat'].strip()) for r in rows if r['Modus'].strip())
print('=== MODUS x SINDIKAT ===')
for k, v in sorted(c.items()):
    print('  ', k, v)

reg = [r for r in rows if 'Puskesmas' in (r.get('Rujukan') or '')]
print('rows with named Puskesmas referral:', len(reg))

fk = collections.Counter()
for r in reg:
    m = re.search(r'Puskesmas\s+([^,]+)', r['Rujukan'])
    fk[m.group(1).strip() if m else '?'] += 1
print('FKTP counts:', dict(fk))

doc_fk = collections.defaultdict(collections.Counter)
for r in reg:
    m = re.search(r'Puskesmas\s+([^,]+)', r['Rujukan'])
    if not m:
        continue
    doc_fk[r['Dokter'].split('(')[0].strip()][m.group(1).strip()] += 1
print('=== doctor -> FKTP (collusion signal) ===')
for d in sorted(doc_fk):
    print('  ', d, 'n=', sum(doc_fk[d].values()), dict(doc_fk[d]))

# faskes -> FKTP
fas_fk = collections.defaultdict(collections.Counter)
for r in reg:
    m = re.search(r'Puskesmas\s+([^,]+)', r['Rujukan'])
    if not m:
        continue
    fas_fk[r['Faskes']][m.group(1).strip()] += 1
print('=== faskes -> FKTP ===')
for f in sorted(fas_fk):
    print('  ', f, 'n=', sum(fas_fk[f].values()), dict(fas_fk[f]))

# Does the "Sindikat" field ever encode a referral-based ring? check the 36 fraud rows
print('=== 36 fraud rows: modus/rujaman/patient ===')
for r in rows:
    if r['Risiko'].strip() == 'fraud':
        print('  ', r['Name'], '|', r['Modus'], '|', r['Sindikat'], '|', r['Faskes'], '|', r['Dokter'].split('(')[0].strip(), '|', r['Pasien'], '|', (r.get('Rujukan') or '')[:60])

# Do syndicate members share the same patient? (key collusion signature)
print('=== syndicate member overlap: same patient or same doctor across different faskes ===')
syn = collections.defaultdict(list)
for r in rows:
    s = r['Sindikat'].strip()
    if s:
        syn[s].append(r)
for s, rs in sorted(syn.items()):
    pats = {x['Pasien'] for x in rs}
    docs = {x['Dokter'].split('(')[0].strip() for x in rs}
    fks = {x['Faskes'] for x in rs}
    print(f'  {s}: n={len(rs)} patients={len(pats)} doctors={len(docs)} faskes={len(fks)} modus={ {x["Modus"] for x in rs} }')
