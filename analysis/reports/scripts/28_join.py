import io, sys, csv, re
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = 'N:/HEALTHKATHON/'
def load(p):
    with open(p, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))
corpus = load(BASE+'analysis/corpus/claims_v2_live.csv')
ml = load(BASE+'mechine-learning-deep-learning/datasets/claims_300_v2.1.csv')
C = {r['Name'].strip(): r for r in corpus}
M = {r['claim_id'].strip(): r for r in ml}

def parse_tfs(v):
    tot = 0.0; ok = True
    for p in re.split(r'[·+|,]', str(v)):
        p = p.strip()
        if not p: continue
        mm = re.findall(r'-?\d+(?:\.\d+)?', p)
        if not mm: continue
        try: tot += float(mm[-1])
        except ValueError: ok = False
    return tot

hit = miss = 0; mism = []
for cid, m in M.items():
    tot = parse_tfs(m['kontribusi_saluran'])
    sf = float(m['skor_fraud'])
    if abs(tot - sf) < 0.011: hit += 1
    else:
        miss += 1
        if len(mism) < 6: mism.append((cid, round(tot,4), sf, m['kontribusi_saluran'], m['risiko']))
print('Skor Fraud == T+F+S (<0.011):', hit, ' mismatch:', miss)
for x in mism: print('   ', x)

los = [(cid, str(m['los_hari']).strip()) for cid, m in M.items()]
zeros = [c for c,v in los if v in ('0','0.0','')]
empty = [c for c,v in los if v=='']
print('\nLOS==0 rows:', len(zeros), ' LOS empty rows:', len(empty))
inap0 = [(c, M[c]['layanan'], M[c]['diagnosis_code'], M[c]['prosedur_code'], M[c]['sindikat']) for c in zeros if 'inap' in M[c]['layanan'].lower()]
print('inap with LOS 0:', inap0)
# rawat jalan with LOS >=1
jl = [(c, M[c]['los_hari']) for c,v in los if 'jalan' in M[c]['layanan'].lower() and v not in ('0','0.0','')]
print('rawat jalan with LOS>=1:', len(jl), jl[:6])
# undefined literal in Rujukan
und = [c for c,m in M.items() if 'undefined' in str(m['rujukan'])]
print('\nRujukan contains "undefined":', len(und), und[:6])
# sentinel em dash in prosedur
em = [c for c,m in M.items() if str(m['prosedur_code']).strip() in ('-','\u2014','')]
print('prosedur_code empty/dash rows:', len(em))
# sentimen counts
from collections import Counter
print('\nsentimen:', Counter(str(m['sentimen']).strip().lower() for m in M.values()))
print('risiko:', Counter(str(m['risiko']).strip().lower() for m in M.values()))
print('status:', Counter(str(m['status']).strip().lower() for m in M.values()))
print('is_fraud:', Counter(str(m['is_fraud']).strip() for m in M.values()))
print('kontradiksi_narasi:', Counter(str(m['kontradiksi_narasi']).strip() for m in M.values()))
