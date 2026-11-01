import csv, collections, io
def load(p):
    raw=open(p,'rb').read()
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
nb = load("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv")
live = load("N:/HEALTHKATHON/analysis/corpus/claims_v2_live.csv")
def f(x):
    try: return float(x)
    except: return None

# --- live dataset leakage check ---
print("=== LIVE dataset ===")
print("Risiko:", collections.Counter(r['Risiko'] for r in live))
print("Status:", collections.Counter(r['Status'] for r in live))
print("Sindikat:", collections.Counter(r['Sindikat'] for r in live).most_common(12))
sf = [f(r['Skor Fraud']) for r in live]
print("Skor Fraud none count:", sum(1 for x in sf if x is None))
sf = [x for x in sf if x is not None]
print("Skor Fraud min/max:", min(sf), max(sf))
# risi fraud => ground truth proxy
y = [1 if r['Risiko']=='fraud' else 0 for r in live]
s = [f(r['Skor Fraud']) or 0.0 for r in live]
P=sum(y); N=len(y)-P
print(f"live P(fraud)={P} N={N}")
pairs=sorted(zip(s,y))
n=len(y); r=[0.0]*n; i=0
while i<n:
    j=i
    while j+1<n and pairs[j+1][0]==pairs[i][0]: j+=1
    a=(i+j)/2.0+1
    for k in range(i,j+1): r[k]=a
    i=j+1
sp=sum(r[k] for k in range(n) if pairs[k][1]==1)
auc=(sp-P*(P+1)/2.0)/(P*N)
tp=0; ap=0.0; prev=0.0
for idx in range(n-1,-1,-1):
    sc,lb=pairs[idx]
    if lb==1:
        tp+=1; rec=tp/P; prec=tp/(n-idx); ap+=prec*(rec-prev); prev=rec
print(f"LIVE skor_fraud vs risiko==fraud: AUC={auc:.4f} AP={ap:.4f}")
# also vs status escalate
y2 = [1 if r['Status']=='escalate' else 0 for r in live]
P2=sum(y2); N2=len(y2)-P2
pairs=sorted(zip(s,y2)); n=len(y2); r=[0.0]*n; i=0
while i<n:
    j=i
    while j+1<n and pairs[j+1][0]==pairs[i][0]: j+=1
    a=(i+j)/2.0+1
    for k in range(i,j+1): r[k]=a
    i=j+1
sp=sum(r[k] for k in range(n) if pairs[k][1]==1)
print(f"LIVE skor_fraud vs status==escalate: AUC={(sp-P2*(P2+1)/2.0)/(P2*N2):.4f}")

print("\n=== THRESHOLD SWEEP on nb skor_fraud (y=is_fraud, P=36) ===")
y=[int(r['is_fraud']) for r in nb]
s=[f(r['skor_fraud']) or 0.0 for r in nb]
P=sum(y); N=len(y)-P
hits_93=[]; hits_9412=[]; hits_9825=[]; hits_9142=[]
for t in sorted(set(s)) + [x/1000 for x in range(500,1000,5)]:
    pred=[1 if x>=t else 0 for x in s]
    tp=sum(1 for i in range(len(y)) if pred[i] and y[i]); fp=sum(1 for i in range(len(y)) if pred[i] and not y[i])
    fn=P-tp; tn=N-fp
    acc=(tp+tn)/len(y); prec=tp/(tp+fp) if tp+fp else 0.0; rec=tp/P
    f1=2*prec*rec/(prec+rec) if prec+rec else 0.0
    fpr=fp/N
    if abs(acc-0.930)<0.0005: hits_93.append((t,acc,prec,rec,f1,fpr))
    if abs(prec-0.9412)<0.0005: hits_9412.append((t,acc,prec,rec,f1,fpr))
print("thresholds giving accuracy 93.0%:", hits_93[:5] or "NONE")
print("thresholds giving precision 94.12%:", hits_9412[:5] or "NONE")
print("\nfull sweep (t, acc, prec, rec, f1, fpr) for t>=0.5:")
seen=set()
for t in sorted(set(s)):
    if t < 0.5: continue
    pred=[1 if x>=t else 0 for x in s]
    tp=sum(1 for i in range(len(y)) if pred[i] and y[i]); fp=sum(1 for i in range(len(y)) if pred[i] and not y[i])
    fn=P-tp; tn=N-fp
    acc=(tp+tn)/len(y); prec=tp/(tp+fp) if tp+fp else 0.0; rec=tp/P
    print(f"  t={t:.4f} acc={acc*100:.2f} prec={prec*100:.2f} rec={rec*100:.2f} fpr={fp/N*100:.2f} fp={fp}")
