import csv, os, statistics, collections
D = r"N:\HEALTHKATHON"
rows = list(csv.DictReader(open(os.path.join(D,"analysis","corpus","claims_v2_live.csv"), encoding="utf-8-sig")))
def f(x):
    try: return float(x)
    except: return None
anom_status = [r for r in rows if r["Status"] in ("review","escalate")]
print("anomali by Status (review+escalate):", len(anom_status))
print("fraud by Risiko:", sum(1 for r in rows if r["Risiko"]=="fraud"))
print("Risiko high count:", sum(1 for r in rows if r["Risiko"]=="high"))

print("\n=== SHAP oracle test (deteksi 'sinyal dominan' text) vs label anomali ===")
def has_signal(s):
    s=(s or "").lower()
    neg = ("tidak ada" in s) or ("tidak ditemukan" in s) or ("nihil" in s)
    return not neg
for lab_name, sel in [("Risiko fraud", [r for r in rows if r["Risiko"]=="fraud"]),
                       ("Risiko high", [r for r in rows if r["Risiko"]=="high"]),
                       ("Status anomali", anom_status),
                       ("Status auto_clear", [r for r in rows if r["Status"]=="auto_clear"])]:
    tp=sum(1 for r in sel if has_signal(r["Sinyal SHAP"]))
    print(f"  {lab_name:20} n={len(sel):3} flagged 'ada sinyal' = {tp}  ({tp/len(sel)*100:.1f}%)")
print("  sample SHAP values:", [r["Sinyal SHAP"][:60] for r in rows[:4]])

print("\n=== Kontribusi Saluran separability ===")
vals = collections.defaultdict(list)
for r in rows:
    m = r["Kontribusi Saluran"]
    nums = re.findall(r"(\d+[.,]\d+)", m) if False else []
import re
for r in rows:
    m=r["Kontribusi Saluran"]; nums=re.findall(r"\d+[.,]\d+", m)
    if len(nums)>=3:
        vals["T"].append((float(nums[0].replace(",",".")), r["Risiko"]=="fraud"))
        vals["F"].append((float(nums[1].replace(",",".")), r["Risiko"]=="fraud"))
        vals["S"].append((float(nums[2].replace(",",".")), r["Risiko"]=="fraud"))
for k,v in vals.items():
    fr=[x for x,lab in v if lab]; nf=[x for x,lab in v if not lab]
    print(f"  {k}: fraud n={len(fr)} min={min(fr):.3f} mean={statistics.mean(fr):.4f} | nonfraud n={len(nf)} max={max(nf):.3f} mean={statistics.mean(nf):.4f} | min-fraud>max-normal? {min(fr)>max(nf)}")
print("  sample Kontribusi:", rows[0]["Kontribusi Saluran"], "||", rows[36]["Kontribusi Saluran"])

print("\n=== Finansial ===")
bys=collections.defaultdict(float); byn=collections.Counter()
for r in rows:
    mod=r["Modus"]; bys[mod]+= f(r["Biaya Rp"]) or 0; byn[mod]+=1
for k,v in sorted(bys.items(), key=lambda x:-x[1]):
    print(f"    {k:20} n={byn[k]:3} Rp{v:,.0f}".replace(",","."))
esc = sum(f(r["Biaya Rp"]) for r in rows if r["Status"]=="escalate")
print(f"  Rp507.370.000 / Rp841.100.000 = {507370000/841100000*100:.2f}%")
print(f"  Rp507.370.000 / 60 = {507370000/60:,.0f}".replace(",","."))
print(f"  Rp507.370.000 / 36 = {507370000/36:,.0f}".replace(",","."))
