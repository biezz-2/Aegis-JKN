import csv, json, os, sys, statistics
BASE=r"N:\HEALTHKATHON"
V21=os.path.join(BASE,r"mechine-learning-deep-learning\datasets\claims_300_v2.1.csv")
def load(p):
    with open(p,"r",encoding="utf-8-sig",newline="") as f:
        r=csv.DictReader(f); return list(r)
vr=load(V21)
y=[int(r["is_fraud"].strip()) for r in vr]
s=[float(r["skor_fraud"]) for r in vr]
st=[r["status"].strip() for r in vr]
P=sum(y); N=len(y)-P
def auprc_trap(y,s):
    # sort desc by score
    pairs=sorted(zip(s,y), key=lambda t:(-t[0], t[1]==0))
    tp=0; fp=0
    pts=[(0.0,1.0)]
    for sc,lab in pairs:
        if lab==1: tp+=1
        else: fp+=1
        prec=tp/(tp+fp); rec=tp/P
        pts.append((rec,prec))
    # trapezoid over recall
    area=0.0
    for i in range(1,len(pts)):
        r0,p0=pts[i-1]; r1,p1=pts[i]
        area += (r1-r0)*(p0+p1)/2
    return area
def auprc_sk(y,s):
    from sklearn.metrics import average_precision_score, precision_recall_curve
    ap=average_precision_score(y,s)
    return ap
def auprc_step(y,s):
    # step-wise (sklearn precision_recall_curve trapezoid variant = average_precision)
    from sklearn.metrics import precision_recall_curve
    pr,re,_=precision_recall_curve(y,s)
    return None
res={}
res["n"]=len(y); res["P"]=P; res["N"]=N; res["prevalence"]=P/len(y)
res["auprc_trap_skor_fraud"]=round(auprc_trap(y,s),6)
res["auprc_sklearn_ap_skor_fraud"]=round(auprc_sk(y,s),6)
# perfect-separation check
res["min_score_fraud"]=min(sc for sc,l in zip(s,y) if l==1)
res["max_score_nonfraud"]=max(sc for sc,l in zip(s,y) if l==0)
res["separable"]= min(sc for sc,l in zip(s,y) if l==1) > max(sc for sc,l in zip(s,y) if l==0)
# accuracy if threshold 0.8
for t in [0.5,0.6,0.7,0.8]:
    pred=[1 if sc>=t else 0 for sc in s]
    acc=sum(1 for a,b in zip(pred,y) if a==b)/len(y)
    tp=sum(1 for a,b in zip(pred,y) if a==1 and b==1); fp=sum(1 for a,b in zip(pred,y) if a==1 and b==0)
    fn=sum(1 for a,b in zip(pred,y) if a==0 and b==1)
    prec=tp/(tp+fp) if tp+fp else 0; rec=tp/(tp+fn) if tp+fn else 0
    res[f"thresh_{t}"]={"acc":round(acc,6),"precision":round(prec,6),"recall":round(rec,6),
        "fpr":round(fp/N,6)}
# AUC via rank (Mann-Whitney)
def auc(y,s):
    order=sorted(range(len(s)), key=lambda i:s[i])
    # handle ties by average rank
    ranks=[0.0]*len(s); i=0
    while i<len(s):
        j=i
        while j+1<len(s) and s[order[j+1]]==s[order[i]]: j+=1
        r=(i+j)/2+1
        for k in range(i,j+1): ranks[order[k]]=r
        i=j+1
    sp=sum(ranks[i] for i in range(len(s)) if y[i]==1)
    n1=P; n0=N
    return (sp - n1*(n1+1)/2)/(n1*n0)
res["roc_auc_skor_fraud"]=round(auc(y,s),6)
# also: AUPRC using skor_fraud as predictor of is_fraud where is_fraud defined as (is_fraud==1)|(sindikat!='none')
y2=[1 if (int(r["is_fraud"].strip())==1 or r["sindikat"].strip() not in ("none","")) else 0 for r in vr]
res["P_y2"]=sum(y2); res["prevalence_y2"]=sum(y2)/len(y2)
res["auprc_trap_y2"]=round(auprc_trap(y2,s),6)
res["roc_auc_y2"]=round(auc(y2,s),6)
# baseline: random AUPRC = prevalence
res["baseline_auprc_prevalence"]=round(P/len(y),6)
# AUPRC of a trivial perfect predictor
res["auprc_perfect"]=1.0
# Does status alone give AUPRC 1? status==escalate
s3=[1.0 if x=="escalate" else 0.0 for x in st]
res["auprc_status_escalate"]=round(auprc_trap(y,s3),6)
# review rows: skor 0.4-0.79, is_fraud 0 -> they are FP if threshold at 0.4
# Try to find whether 0.9142 is reachable by some combination
target=0.9142
# test: predicted fraud if skor>=t, AP over t grid
best=None
for ti in range(400,960):
    t=ti/1000
    pred=[1 if sc>=t else 0 for sc in s]
    # average precision of binary predictor
    tp=sum(1 for a,b in zip(pred,y) if a==1 and b==1); fp=sum(1 for a,b in zip(pred,y) if a==1 and b==0); fn=sum(1 for a,b in zip(pred,y) if a==0 and b==1)
    if tp==0: continue
    prec=tp/(tp+fp); rec=tp/P
    f1=2*prec*rec/(prec+rec)
    if best is None or f1>best[1]: best=(t,f1,prec,rec,acc if False else 0)
res["best_f1_threshold"]=best
with open(os.path.join(BASE,r"analysis\reports\scripts\out_auprc.json"),"w",encoding="utf-8") as f:
    json.dump(res,f,ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False,indent=1))
