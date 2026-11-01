import csv, collections, re, sys

rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))

# 1. Does any Alasan / reason text mention referral, collusion, or puskesmas?
kw = ['rujukan', 'kolusi', 'puskesmas', 'fktp', 'k referrals']
print('=== KEYWORD MENTIONS in Alasan / Catatan / Modus ===')
for field in ['Alasan', 'Catatan', 'Modus', 'Sinyal SHAP']:
    c = collections.Counter()
    for r in rows:
        t = (r.get(field) or '').lower()
        for k in kw:
            if k in t:
                c[(field, k)] += 1
    for k, v in sorted(c.items()):
        print('  ', k, v)

print()
print('=== Does EVERY syndicate have exactly 1 faskes and refer only to its own Puskesmas? collusion check ===')
# collusion signature: a Puskesmas referring to MULTIPLE faskes (steering), or faskes receiving from MULTIPLE Puskesmas
fk_to_fas = collections.defaultdict(set)
fas_to_fk = collections.defaultdict(set)
for r in rows:
    m = re.search(r'Puskesmas\s+([^,]+)', r.get('Rujukan') or '')
    if not m:
        continue
    fk = m.group(1).strip()
    fk_to_fas[fk].add(r['Faskes'])
    fas_to_fk[r['Faskes']].add(fk)
print('FKTP -> number of distinct receiving faskes:')
for fk in sorted(fk_to_fas):
    print('   ', fk, '->', len(fk_to_fas[fk]), sorted(fk_to_fas[fk]))
print('Faskes -> number of distinct source Puskesmas:')
for f in sorted(fas_to_fk):
    print('   ', f, '->', len(fas_to_fk[f]), sorted(fas_to_fk[f]))

print()
print('=== Financial: total nominal + per status + nominal of the 36 fraud rows ===')
tot = sum(int(r['Biaya Rp']) for r in rows)
print('TOTAL nominal Rp', f'{tot:,}'.replace(',', '.'))
for st in ['auto_clear', 'review', 'escalate']:
    s = sum(int(r['Biaya Rp']) for r in rows if r['Status'].strip() == st)
    print('  ', st, 'Rp', f'{s:,}'.replace(',', '.'), 'n=', sum(1 for r in rows if r['Status'].strip() == st))
fr = [r for r in rows if r['Risiko'].strip() == 'fraud']
fs = sum(int(r['Biaya Rp']) for r in fr)
print('  36 fraud rows nominal Rp', f'{fs:,}'.replace(',', '.'))
print('  escalate+review nominal Rp', f'{sum(int(r["Biaya Rp"]) for r in rows if r["Status"].strip() in ("escalate","review")):,}'.replace(',', '.'))
print('  RATIO fraud-nominal/total = %.4f' % (fs / tot))
print('  claim Rp507.370.000 == ? escalate+review? ', 507370000 == sum(int(r['Biaya Rp']) for r in rows if r['Status'].strip() in ('escalate', 'review')))

print()
print('=== Overcharge / tarif acuan: any per-claim benchmark column? ===')
print('COLUMNS:', list(rows[0].keys()))
# look for max single claim
mx = max(rows, key=lambda r: int(r['Biaya Rp']))
print('max claim', mx['Name'], mx['Biaya Rp'], mx['Risiko'], mx['Modus'])

print()
print('=== sample Alasan for each modus (one row each) ===')
seen = set()
for r in rows:
    m = r['Modus'].strip()
    if m and m not in seen:
        seen.add(m)
        print('  ', m, '::', (r.get('Alasan') or '')[:220])
        print('      ->', (r.get('Catatan') or '')[:160])
