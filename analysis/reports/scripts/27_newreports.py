import io, sys, json, csv, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = 'N:/HEALTHKATHON/'
corpus = BASE + 'analysis/corpus/claims_v2_live.csv'
ml = BASE + 'mechine-learning-deep-learning/datasets/claims_300_v2.1.csv'

def load(p):
    with open(p, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

rows = load(corpus)
print('corpus rows', len(rows), 'cols', len(rows[0]))

# 1) LOGO(faskes): sindikat per faskes, fraud per sindikat
from collections import defaultdict
syn_faskes = defaultdict(set)
syn_fraud = defaultdict(int)
faskes_fraud = defaultdict(int)
for r in rows:
    s = (r.get('Sindikat') or '').strip()
    if s.upper().startswith('SYND'):
        syn_faskes[s].add((r.get('Faskes') or '').strip())
    risk = (r.get('Risiko') or '').strip().lower()
    if risk == 'fraud':
        faskes_fraud[(r.get('Faskes') or '').strip()] += 1
        if s.upper().startswith('SYND'):
            syn_fraud[s] += 1
multi = {k: v for k, v in syn_faskes.items() if len(v) > 1}
print('syndicates spanning >1 faskes:', len(multi), list(multi)[:5])
tot_unseen = 0
for s in sorted(syn_faskes):
    fs = sorted(syn_faskes[s])
    held = fs[0]
    unseen_fraud = syn_fraud[s]  # whole syndicate held out with its faskes
    tot_unseen += unseen_fraud
    print(' ', s, fs, 'fraud=', syn_fraud[s], 'heldout_fraud=', unseen_fraud)
print('fraud in fully-held-out syndicates:', tot_unseen, 'of', sum(syn_fraud.values()))

# 2) Skor Fraud == T+F+S ?
hit = miss = 0
for r in rows:
    t = (r.get('Kontribusi Saluran') or '').strip()
    parts = [p.strip() for p in t.split('+')]
    try:
        s = sum(float(p) for p in parts if p)
    except ValueError:
        continue
    sf = float(r.get('Skor Fraud') or 0)
    if abs(s - sf) < 0.011: hit += 1
    else: miss += 1
print('Skor Fraud == T+F+S within 0.011:', hit, 'mismatch:', miss)

# 3) dokter_raw truncation in ML csv vs corpus
mlrows = load(ml)
print('ml rows', len(mlrows))
c = {r.get('Name'): r for r in rows}
diff = 0
for r in mlrows:
    nm = r.get('Name')
    a = (r.get('dokter_raw') or '')
    b = (c.get(nm, {}).get('Dokter') or '')
    if a != b:
        diff += 1
        if diff <= 3:
            print('  DIFF', nm, '| ml=', a, '| notion=', b)
print('dokter_raw differing rows:', diff)

# 4) text ground truth: contradiction flag vs modus
flag_true = [r.get('Name') for r in rows if (r.get('Kontradiksi Narasi') or '').strip().lower() in ('true', '1')]
print('Kontradiksi Narasi True count:', len(flag_true))
print(' ', ' '.join(x.replace('KLM','') for x in flag_true))
