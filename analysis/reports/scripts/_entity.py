"""Verify 10-simulation-dataset.md entity tables against the FIXX ground truth,
and compute the mean nominal of the 60 non-auto_clear claims."""
import collections, sys, os, re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"N:/HEALTHKATHON/analysis/reports/scripts")

# reuse ground truth builder
import importlib.util
spec = importlib.util.spec_from_file_location("fx", r"N:/HEALTHKATHON/analysis/reports/scripts/_fixx_repro.py")
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
CLAIMS = fx.CLAIMS
PROC = fx.PROC
DX_SEV = fx.DX_SEV

print("=== ENTITY TABLE CHECK: 10-simulation-dataset.md vs FIXX ground truth ===")
by_faskes = collections.Counter(c["faskes"] for c in CLAIMS)
by_dok = collections.Counter(c["dokter"] for c in CLAIMS)
by_pas = collections.Counter(c["pasien"] for c in CLAIMS)
by_dx = collections.Counter(c["dx"] for c in CLAIMS)
by_proc = collections.Counter(c["proc"] for c in CLAIMS)

doc_faskes = {"RS_A": (19, 0.95, "fraud"), "RS_B": (13, 0.87, "fraud"),
              "RS_C": (10, 0.94, "fraud"), "RS_D": (10, 0.68, "high"),
              "RS_E": (22, 0.88, "fraud"), "RS_F": (26, 0.79, "high")}
print("\nFASKES   doc(n,skor,risk)  actual(n,skor_max,risk)")
for f in sorted(doc_faskes):
    sub = [c for c in CLAIMS if c["faskes"] == f]
    smax = max(c["skor"] for c in sub)
    risks = sorted(set(c["risk"] for c in sub), key=lambda r: ["low", "medium", "high", "fraud"].index(r))
    dn, ds, dr = doc_faskes[f]
    flag = "" if dn == len(sub) else "  <== N MISMATCH"
    dflag = "" if abs(ds - smax) < 1e-9 else f"  <== SKOR MISMATCH (doc {ds})"
    print(f"  {f}: doc({dn}, {ds}, {dr})  actual({len(sub)}, {smax:.2f}, {risks}){flag}{dflag}")

doc_dx = {"K29.7": (10, 0.95, "fraud"), "K35.8": (11, 0.79, "high"),
          "K40.9": (8, 0.13, "low"), "I21.9": (8, 0.13, "low"),
          "J18.9": (9, 0.74, "high"), "E11.9": (15, 0.88, "fraud"),
          "N20.0": (8, 0.13, "low"), "S72.0": (10, 0.94, "fraud"),
          "O80": (8, 0.66, "high"), "K80.2": (13, 0.87, "fraud")}
print("\nDIAGNOSIS  doc(n,skor,risk)  actual(n,skor_max,risk)")
for d, (dn, ds, dr) in doc_dx.items():
    sub = [c for c in CLAIMS if c["dx"] == d]
    smax = max(c["skor"] for c in sub)
    risks = sorted(set(c["risk"] for c in sub), key=lambda r: ["low", "medium", "high", "fraud"].index(r))
    flag = "" if dn == len(sub) else "  <== N MISMATCH"
    dflag = "" if abs(ds - smax) < 1e-9 else f"  <== SKOR MISMATCH (doc {ds})"
    print(f"  {d}: doc({dn}, {ds}, {dr})  actual({len(sub)}, {smax:.2f}, {risks}){flag}{dflag}")

doc_proc = {"00.66": (12, 0.95, "fraud"), "36.13": (0, 0, "low"),
            "47.09": (11, 0.79, "high")}
print("\nPROSEDUR (doc excerpt only)")
for d, (dn, ds, dr) in doc_proc.items():
    sub = [c for c in CLAIMS if c["proc"] == d]
    print(f"  {d}: doc({dn}, {ds}, {dr})  actual n={len(sub)}"
          + ("  <== PROCEDURE NOT IN NOTEBOOK PROC TABLE" if d not in PROC else ""))

print("\nPROSEDUR full from notebook:")
for p, n in sorted(by_proc.items()):
    sub = [c for c in CLAIMS if c["proc"] == p]
    print(f"  {p} ({PROC[p]['nama']}): n={n} skor_max={max(c['skor'] for c in sub):.2f} "
          f"tarif={PROC[p].get('tarif','?')}")

doc_pas = {"P01": (5, 0.94, "fraud"), "P02": (5, 0.95, "fraud"), "P03": (5, 0.93, "fraud"),
           "P04": (4, 0.11, "low"), "P05": (5, 0.66, "high"), "P06": (4, 0.13, "low"),
           "P07": (5, 0.62, "high"), "P08": (5, 0.92, "fraud"), "P09": (5, 0.94, "fraud"),
           "P10": (5, 0.93, "fraud"), "P11": (5, 0.68, "high"), "P12": (5, 0.85, "fraud"),
           "P13": (6, 0.86, "fraud"), "P14": (6, 0.87, "fraud"), "P15": (5, 0.53, "medium"),
           "P16": (5, 0.88, "fraud"), "P17": (5, 0.86, "fraud"), "P18": (4, 0.74, "high"),
           "P19": (4, 0.78, "high"), "P20": (5, 0.79, "high")}
print("\nPASIEN  doc(n,skor,risk)  actual(n,skor_max,risk)")
for p, (dn, ds, dr) in doc_pas.items():
    sub = [c for c in CLAIMS if c["pasien"] == p]
    smax = max(c["skor"] for c in sub)
    risks = sorted(set(c["risk"] for c in sub), key=lambda r: ["low", "medium", "high", "fraud"].index(r))
    flag = "" if dn == len(sub) else "  <== N MISMATCH"
    dflag = "" if abs(ds - smax) < 1e-9 else f"  <== SKOR MISMATCH (doc {ds})"
    print(f"  {p}: doc({dn}, {ds}, {dr})  actual({len(sub)}, {smax:.2f}, {risks}){flag}{dflag}")

print("\nDOKTER actual counts:", dict(sorted(by_dok.items())))

# 300-dataset: mean nominal of 60 non-auto_clear
import csv, io
P = "N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv"
rows = list(csv.DictReader(io.StringIO(open(P, "rb").read().decode("utf-8-sig"))))
def num(x):
    try:
        return float(x)
    except Exception:
        return 0.0
sixty = [r for r in rows if r["status"] != "auto_clear"]
print(f"\n300-dataset non-auto_clear: n={len(sixty)} "
      f"nominal={sum(num(r['biaya_rp']) for r in sixty):,.0f} "
      f"mean={sum(num(r['biaya_rp']) for r in sixty)/len(sixty):,.0f}")
TARGET = 507_370_000
print(f"target/60 = {TARGET/60:,.0f}  (proposal 'rata-rata Rp8,46 Juta per kasus fraud')")
