#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit ronde 4: kontradiksi LOS, template kanal, median LOS,entropy."""
import csv, os, re, statistics, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
rows = list(csv.DictReader(open(os.path.join(CORPUS, "claims_v2_live.csv"),
                                encoding="utf-8-sig", newline="")))
n = lambda v: "" if v is None else str(v).strip()
def h(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

def tfs(r):
    return tuple(re.findall(r"[TFS] ([-\d.]+)", n(r["Kontribusi Saluran"])))

# ---- 1. Apakah Kontribusi Saluran konstan di dalam tiap modus?
h("1. KONTRIBUSI SALURAN: KONSTAN DI DALAM MODUS?")
by_mod = defaultdict(set)
for r in rows:
    if n(r["Modus"]): by_mod[n(r["Modus"])].add(tfs(r))
print("modus -> jumlah nilai T/F/S berbeda dalam modus tersebut:")
for k in sorted(by_mod):
    print(f"   {k:<22} n_baris={sum(1 for r in rows if n(r['Modus'])==k):<3} "
          f"pola_berbeda={len(by_mod[k])} -> {sorted(by_mod[k])}")
print("\nlow (tanpa modus): pola T/F/S unik =",
      len({tfs(r) for r in rows if not n(r["Modus"])}))

# ---- 2. Kontradiksi LOS: apakah 'Alasan' menyebut LOS > 0 pada baris LOS=0?
h("2. KONTRADIKSI: 'ALASAN' MENYEBUT LOS > 0 PADA BARIS LOS=0")
contra = []
for r in rows:
    if n(r["LOS hari"]) != "0": continue
    a = n(r["Alasan"])
    for m in re.finditer(r"LOS\s+(\d+)\s*hari", a):
        if int(m.group(1)) != 0:
            contra.append((r["Name"], n(r["LOS hari"]), m.group(0), a[:130]))
            break
print(f"baris LOS=0 yang 'Alasan'-nya menyebut LOS>0: {len(contra)}")
for c in contra[:15]: print("   ", c)
print("contoh lengkap 2 baris:")
for c in contra[:2]:
    r = [x for x in rows if x["Name"] == c[0]][0]
    print(f"\n   {c[0]} (LOS kolom={n(r['LOS hari'])}, Layanan={n(r['Layanan'])})")
    print("     Alasan:", n(r["Alasan"])[:400])
# berapa baris LOS=0 punya Alasan yang menyebut LOS sama sekali
withlos = [r for r in rows if n(r["LOS hari"]) == "0" and "LOS" in n(r["Alasan"])]
print(f"\nbaris LOS=0 dengan kata 'LOS' di Alasan: {len(withlos)} / 109")
withoutlos = [r["Name"] for r in rows if n(r["LOS hari"]) == "0" and "LOS" not in n(r["Alasan"])]
print("tanpa kata 'LOS':", len(withoutlos), withoutlos[:15])

# ---- 3. Median LOS yang diklaim vs aktual
h("3. MEDIAN LOS DIKLAIM vs AKTUAL")
los_dx = defaultdict(list)
for r in rows:
    if n(r["LOS hari"]) not in ("", "0"):
        los_dx[n(r["Diagnosis ICD-10"]).split(" - ")[0]].append(int(n(r["LOS hari"])))
print("median aktual (LOS>0) per dx:")
for k in sorted(los_dx):
    print(f"   {k:<8} n={len(los_dx[k]):<3} median={statistics.median(los_dx[k])}")
CLAIMS = [("KLM015", "median pneumonia 5 hari", "J18.9", 5),
          ("KLM127", "median 5", "I21.9", 5),
          ("KLM129", "median 7", "S72.0", 7),
          ("KLM123", "tarif 8,2 jt", "K40.9", None)]
for nm, txt, dx, exp in CLAIMS:
    r = [x for x in rows if x["Name"] == nm][0]
    act = statistics.median(los_dx[dx])
    print(f"   {nm}: Alasan '{txt}' | dx={dx} median aktual={act} "
          f"| LOS baris={n(r['LOS hari'])} | {'COCOK' if exp==act else 'BEDA' if exp else 'n/a'}")

# ---- 4. Kanal: apakah label bisa diturunkan dari T+F+S?
h("4. APAKAH LABEL BISA DITURUNKAN DARI T+F+S?")
amb = []
for r in rows:
    s = sum(float(x) for x in tfs(r))
    lab = "low" if s < 0.35 else "medium" if s < 0.60 else "high" if s < 0.80 else "fraud"
    if lab != n(r["Risiko"]): amb.append((r["Name"], round(s, 3), n(r["Risiko"]), lab,
                                         float(n(r["Skor Fraud"]))))
print(f"baris yang label Risiko TIDAK bisa diturunkan dari T+F+S: {len(amb)}")
for a in amb: print("   ", a)
print("\nRingkasan selisih Skor Fraud - (T+F+S):")
d = [(r["Name"], float(n(r["Skor Fraud"])) - sum(float(x) for x in tfs(r)),
      n(r["Risiko"])) for r in rows]
for lab in ("low", "medium", "high", "fraud"):
    v = [x[1] for x in d if x[2] == lab]
    print(f"   {lab:<7} n={len(v):<3} min={min(v):+.3f} maks={max(v):+.3f} "
          f"tanpa_koinciden={sum(1 for x in v if abs(x)>1e-9)}")

# ---- 5. 'Alasan' pada baris low apakah seragam (template) & info nyata?
h("5. 'ALASAN' PADA BARIS LOW: VARIASI")
low_a = [n(r["Alasan"]) for r in rows if n(r["Risiko"]) == "low"]
norm = [re.sub(r"Rp[\d.]+", "RpX", re.sub(r"\d+(\.\d+)?", "N", a)) for a in low_a]
print("jumlah baris low:", len(low_a), "| pola template unik:", len(set(norm)))
for t, c in Counter(norm).most_common(6):
    print(f"   [{c}] {t[:190]}")

# ---- 6. Biaya: pola template per dx+proc (determinisme generator)
h("6. BIAYA: POLA TEMPLATE")
bc = Counter((n(r["Diagnosis ICD-10"]).split(" - ")[0], n(r["Prosedur ICD-9-CM"]).split(" - ")[0],
              n(r["Biaya Rp"])) for r in rows)
print("kombinasi (dx,proc,biaya) unik:", len(bc))
for k, c in bc.most_common(12):
    print(f"   [{c}] {k[0]:<8} {k[1]:<8} Rp{int(k[2]):,}")

# ---- 7. Tanggal: pola & kepatuhan rentang
h("7. TANGGAL: DISTRIBUSI & DUPLIKASI")
td = Counter(n(r["Tanggal"]) for r in rows)
print("tanggal paling banyak:", td.most_common(5))
print("tanggal dipakai 1x:", sum(1 for v in td.values() if v == 1))
# apakah ada baris dengan tanggal identik + entitas identik (double-billing legit check)
same_day = defaultdict(list)
for r in rows:
    same_day[(n(r["Tanggal"]), n(r["Pasien"]))].append(r["Name"])
multi = {k: v for k, v in same_day.items() if len(v) > 1}
print(f"(tanggal,pasien) dengan >1 klaim: {len(multi)}")
for k, v in sorted(multi.items())[:20]:
    print("   ", k[1], k[0], v)

# ---- 8. Los: pola per layanan
h("8. LOS: POLA PER LAYANAN")
los_lay = defaultdict(Counter)
for r in rows: los_lay[n(r["Layanan"])][n(r["LOS hari"])] += 1
for k in sorted(los_lay): print(f"   {k}: {dict(los_lay[k])}")

# ---- 9. Rujukan: pola string
h("9. RUJUKAN: POLA")
rr = Counter()
for r in rows:
    v = n(r["Rujukan"])
    if v.startswith("kunjungan langsung"): rr["kunjungan langsung (tanpa rujukan)"] += 1
    elif "undefined" in v: rr["undefined"] += 1
    elif "Puskesmas" in v: rr["Puskesmas + no rujukan + tanggal"] += 1
    else: rr["lain: " + v[:50]] += 1
print(dict(rr))
# nomor rujukan duplikat
nums = [m.group(1) for r in rows for m in [re.search(r"(RJ-\d{4}-\d+)", n(r["Rujukan"]))] if m]
dupn = {k: v for k, v in Counter(nums).items() if v > 1}
print("nomor rujukan duplikat:", dupn)

# ---- 10. Entitas: 1 pasien appear multiple claims across sindikat - cek counts
h("10. JUMLAH KLAIM PER PASIEN (P01-P40) - konsistensi dengan tabel v100")
pc = Counter(n(r["Pasien"]).split(" (")[0] for r in rows)
for k in sorted(pc): print(f"   {k}: {pc[k]}")
print("total:", sum(pc.values()))

# ---- 11. Cek: apakah Sindikat/SHAP/Modus konsisten per baris (leakage-block consistency)
h("11. KONSISTENSI SINYAL SHAP vs MODUS")
sh = defaultdict(set)
for r in rows:
    if n(r["Modus"]): sh[n(r["Modus"])].add(n(r["Sinyal SHAP"])[:70])
for k in sorted(sh):
    print(f"   {k:<22} varian SHAP={len(sh[k])}")
    for v in sorted(sh[k])[:3]: print(f"       {v}")
