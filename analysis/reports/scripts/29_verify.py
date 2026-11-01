import io, sys, csv, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE='N:/HEALTHKATHON/'
def load(p):
    with open(p,encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
ml = load(BASE+'mechine-learning-deep-learning/datasets/claims_300_v2.1.csv')
M = {r['claim_id'].strip(): r for r in ml}
# separability
fr = [float(m['skor_fraud']) for m in M.values() if str(m['is_fraud']).strip()=='1']
nf = [float(m['skor_fraud']) for m in M.values() if str(m['is_fraud']).strip()!='1']
print('fraud n=%d min=%.2f max=%.2f' % (len(fr), min(fr), max(fr)))
print('nonfraud n=%d min=%.2f max=%.2f' % (len(nf), min(nf), max(nf)))
print('overlap:', max(nf) >= min(fr))
# T+F+S tolerance sweep
def parse(v):
    tot=0.0
    for p in re.split(r'[·+|,]', str(v)):
        mm=re.findall(r'-?\d+(?:\.\d+)?', p)
        if mm: tot+=float(mm[-1])
    return tot
for tol in (0.0005, 0.005, 0.011, 0.02, 0.05):
    hit=sum(1 for m in M.values() if abs(parse(m['kontribusi_saluran'])-float(m['skor_fraud']))<tol)
    print('T+F+S tol %.4f -> match %d / 300 (mismatch %d)' % (tol, hit, 300-hit))
# 14 rows risiko not derivable
bad=[]
for cid,m in M.items():
    s=parse(m['kontribusi_saluran']); risk=str(m['risiko']).strip().lower()
    if risk in ('fraud',):
        ok = s>=0.80
    elif risk=='high': ok = 0.60<=s<0.80
    elif risk=='medium': ok = 0.35<=s<0.60
    else: ok = s<0.35
    if not ok: bad.append((cid, round(s,4), m['skor_fraud'], risk))
print('risiko not derivable from T+F+S at 0.35/0.60/0.80:', len(bad), bad[:8])
# status vs risiko determinism
mism=sum(1 for m in M.values() if not ((str(m['risiko']).strip().lower()=='fraud' and str(m['status']).strip().lower()=='escalate') or (str(m['risiko']).strip().lower() in ('high','medium') and str(m['status']).strip().lower()=='review') or (str(m['risiko']).strip().lower()=='low' and str(m['status']).strip().lower()=='auto_clear')))
print('status/risiko mismatches:', mism)
# 100-claim payload meta
import json
p=json.load(open(BASE+'Aegis-JKN/public/payload-aegis-jkn.json',encoding='utf-8'))
print('\npayload top keys:', list(p.keys()))
print('meta:', json.dumps(p.get('meta'), ensure_ascii=False)[:600])
print('kpi:', json.dumps(p.get('kpi'), ensure_ascii=False)[:600])
