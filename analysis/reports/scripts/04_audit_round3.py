#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit ronde 3: perbaikan parsing rasio, verifikasi v100, sisa item."""
import csv, json, os, re, statistics, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"N:\HEALTHKATHON\analysis\corpus"
rows = list(csv.DictReader(open(os.path.join(CORPUS, "claims_v2_live.csv"),
                                encoding="utf-8-sig", newline="")))
n = lambda v: "" if v is None else str(v).strip()
def h(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

def num_id(s):
    """'rasio 1.03' -> 1.03 ; 'rasio 1,03' -> 1.03 ; desimal koma gaya ID."""
    s = s.strip().replace(" ", "").replace("x", "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    return float(s)

# ---- 1. Rasio biaya di Alasan vs tarif acuan (parsing diperbaiki)
h("1. RASIO BIAYA DI 'ALASAN' vs TARIF ACUAN (parsing desimal ID diperbaiki)")
TARIF = {"51.23": 14500000, "00.66": 58000000, "47.09": 6800000, "53.1": 8200000,
         "74.1": 6200000, "81.52": 46500000, "96.04": 750000, "98.51": 5600000}
ok, bad = [], []
for r in rows:
    code = n(r["Prosedur ICD-9-CM"]).split(" - ")[0]
    m = re.search(r"rasio\s+([\d.,]+x?)", n(r["Alasan"]))
    if m and code in TARIF:
        claimed = num_id(m.group(1).rstrip("x"))
        actual = int(n(r["Biaya Rp"])) / TARIF[code]
        rec = (r["Name"], code, claimed, round(actual, 3), round(actual - claimed, 3))
        (ok if abs(actual - claimed) <= 0.015 else bad).append(rec)
print(f"rasio terverifikasi: {len(ok)+len(bad)} | cocok: {len(ok)} | tidak cocok: {len(bad)}")
for b in bad: print("   ", b)

# ---- 2. Verifikasi tabel v100 (Pasien/Dokter/Faskes/Dx/Proc/Obat) vs KLM001-KLM100
h("2. VERIFIKASI TABEL DOKUMEN v100 vs SUB-SET KLM001-KLM100")
v100 = sorted(rows, key=lambda r: int(r["Name"][3:]))[:100]
DOC_PATIENT = {  # P01..P20 : (jumlah klaim, skor maks)
 "P01":(5,0.94),"P02":(5,0.95),"P03":(5,0.93),"P04":(4,0.11),"P05":(5,0.66),
 "P06":(4,0.13),"P07":(5,0.62),"P08":(5,0.92),"P09":(4,0.94),"P10":(5,0.93),
 "P11":(4,0.68),"P12":(5,0.85),"P13":(6,0.86),"P14":(6,0.87),"P15":(7,0.53),
 "P16":(5,0.88),"P17":(5,0.86),"P18":(4,0.74),"P19":(5,0.78),"P20":(5,0.79)}
DOC_DOKTER = {"D01":(2,0.94),"D02":(8,0.95),"D03":(9,0.74),"D04":(9,0.68),"D05":(10,0.94),
 "D06":(0,0),"D07":(13,0.87),"D08":(18,0.79),"D09":(14,0.88),"D10":(8,0.13),
 "D11":(1,0.62),"D12":(8,0.66)}
DOC_FASKES = {"RS_A":(19,0.95),"RS_B":(13,0.87),"RS_C":(10,0.94),"RS_D":(10,0.68),
 "RS_E":(22,0.88),"RS_F":(26,0.79)}
pat = defaultdict(list); dok = defaultdict(list); fsk = defaultdict(list)
for r in v100:
    pat[n(r["Pasien"]).split(" (")[0]].append(float(n(r["Skor Fraud"])))
    dok[n(r["Dokter"]).split(" (")[0]].append(float(n(r["Skor Fraud"])))
    fsk[n(r["Faskes"])].append(float(n(r["Skor Fraud"])))
print(f"{'entitas':<8} {'doc_n':>6} {'akt_n':>6} {'doc_maks':>9} {'akt_maks':>9}  status")
for grp, doc, label in ((pat, DOC_PATIENT, "pasien"), (dok, DOC_DOKTER, "dokter"), (fsk, DOC_FASKES, "faskes")):
    for k in sorted(doc):
        dn, dsc = doc[k]
        av = grp.get(k, [])
        an = len(av); amax = max(av) if av else 0
        st = "OK" if (dn == an and abs(dsc - amax) < 0.005) else "BEDA"
        print(f"{k:<8} {dn:>6} {an:>6} {dsc:>9.2f} {amax:>9.2f}  {st}")
    ent = set(grp) - set(doc)
    if ent: print(f"   entitas v100 di luar tabel: {sorted(ent)}")

# ---- 3. Biaya: negatif / nol / non-integer
h("3. BIAYA: TIPE & KELAS")
vals = [n(r["Biaya Rp"]) for r in rows]
print("non-integer:", [v for v in vals if not re.fullmatch(r"\d+", v)][:10])
print("negatif:", sum(1 for v in vals if int(v) < 0), "| nol:", sum(1 for v in vals if int(v) == 0))
print("nilai < 1.000.000:", sum(1 for v in vals if int(v) < 1000000),
      sorted(int(v) for v in vals if int(v) < 1000000)[:12])
print("nilai > 50.000.000:", sum(1 for v in vals if int(v) > 50000000))

# ---- 4. Biaya vs tarif acuan: berapa klaim melampaui tarif paket
h("4. BIAYA vs TARIF PAKET ACUAN")
rows_t = []
for r in rows:
    code = n(r["Prosedur ICD-9-CM"]).split(" - ")[0]
    if code in TARIF:
        rows_t.append((r["Name"], code, int(n(r["Biaya Rp"])), round(int(n(r["Biaya Rp"])) / TARIF[code], 2),
                       n(r["Risiko"]), n(r["Layanan"])))
ratios = [x[3] for x in rows_t]
print(f"baris dengan prosedur ber-acuan: {len(rows_t)}; rasio median={statistics.median(ratios)} "
      f"min={min(ratios)} max={max(ratios)}")
print("rasio > 1.5 (indikasi overcharge, label low):")
for x in sorted(rows_t, key=lambda y: -y[3]):
    if x[3] > 1.5:
        print(f"   {x[0]} {x[1]} Rp{x[2]:,} rasio={x[3]} risiko={x[4]} layanan={x[5]}")
print("rasio < 0.5 (biaya jauh di bawah tarif):")
for x in sorted(rows_t, key=lambda y: y[3]):
    if x[3] < 0.5: print(f"   {x[0]} {x[1]} Rp{x[2]:,} rasio={x[3]} risiko={x[4]} layanan={x[5]}")

# ---- 5. Narasi Rekam Medis: apakah mendeskripsikan prosedur yang ditagih
h("5. NARASI vs KODE (deteksi narasi generik yang tidak cocok)")
nar = defaultdict(Counter)
for r in rows:
    nar[n(r["Diagnosis ICD-10"]).split(" - ")[0]][n(r["Narasi Rekam Medis"])[:60]] += 1
for k in sorted(nar):
    print(f"   {k}: {len(nar[k])} varian narasi")
    for v, c in nar[k].most_common(3): print(f"       [{c}] {v}")

# ---- 6. Row-order: apakah CSV terurut apa
h("6. URUTAN BARIS CSV")
print("10 ID pertama:", [r["Name"] for r in rows])
print("10 ID terakhir:", [r["Name"] for r in rows[-10:]])
pid = [n(r["_notion_page_id"]) for r in rows]
print("_notion_page_id terurut menaik?", pid == sorted(pid))
print("Name terurut menaik?", [r["Name"] for r in rows] == sorted(r["Name"] for r in rows))
print("Tanggal terurut menaik?", [n(r['Tanggal']) for r in rows] == sorted(n(r['Tanggal']) for r in rows))

# ---- 7. Skor Fraud: pola pengulangan (determinisme generator)
h("7. POLA SKOR FRAUD / KONTRIBUSI SALURAN")
kontr = defaultdict(set)
for r in rows:
    vals = tuple(re.findall(r"[TFS] ([-\d.]+)", n(r["Kontribusi Saluran"])))
    kontr[(n(r["Risiko"]), vals)].add(float(n(r["Skor Fraud"])))
print("Pola (Risiko, T/F/S) -> himpunan skor:")
for k in sorted(kontr, key=lambda x: (x[0], x[1])):
    v = sorted(kontr[k])
    print(f"   {k[0]:<7} {k[1]} -> {v}")
print("\nJumlah (Risiko, T/F/S) unik:", len(kontr))

# ---- 8. Skor Fraud = jumlah kanal?tes eksak
h("8. APAKAH SKOR FRAUD = T+F+S?")
exact, notexact = [], []
for r in rows:
    vals = [float(x) for x in re.findall(r"[TFS] ([-\d.]+)", n(r["Kontribusi Saluran"]))]
    s = float(n(r["Skor Fraud"]))
    (exact if abs(sum(vals) - s) < 1e-9 else notexact).append((r["Name"], sum(vals), s, round(s - sum(vals), 3)))
print(f"tepat: {len(exact)} | tidak tepat: {len(notexact)}")
print("contoh tidak tepat:", notexact[:12])
print("Toleransi 0.01:", sum(1 for x in notexact if abs(x[3]) <= 0.01))
print("Selisih >0.02:", sum(1 for x in notexact if abs(x[3]) > 0.02))
print("Selisih per label:")
for lab in ("low","medium","high","fraud"):
    d = [x[3] for x in notexact if [r for r in rows if r['Name']==x[0]][0]['Risiko'] == lab]
    if d: print(f"   {lab}: n={len(d)} min={min(d):.3f} maks={max(d):.3f}")

# ---- 9. KLM127 & baris biaya tinggi lain: apakah high/fraud sesuai
h("9. BARIS BIAYA TERTINGGI: KONTEKS")
for nm in ("KLM127", "KLM047", "KLM019", "KLM123"):
    r = [x for x in rows if x["Name"] == nm][0]
    print(f"\n{nm}: biaya={n(r['Biaya Rp'])} risiko={n(r['Risiko'])} status={n(r['Status'])} "
          f"dx={n(r['Diagnosis ICD-10'])} proc={n(r['Prosedur ICD-9-CM'])} LOS={n(r['LOS hari'])}")
    print("   SHAP:", n(r["Sinyal SHAP"])[:150])
    print("   Alasan:", n(r["Alasan"])[:250])

# ---- 10. Alasan: modus di dalam teks vs kolom Modus
h("10. MODUS DI DALAM TEKS ALASAN vs KOLOM MODUS")
mis = []
for r in rows:
    a = n(r["Alasan"]).upper()
    m = n(r["Modus"])
    if not m: continue
    key = m.upper().replace("_", " ")
    # ambil kata kunci modus dari prefaks FRAUD (...)
    mm = re.match(r"FRAUD \(([^)]+)\)", n(r["Alasan"]))
    if mm:
        txt = mm.group(1).upper().replace("—", "-").strip()
        first = txt.split("-")[0].strip().upper()
        if first.replace(" ", "_") != m.upper() and first[:5] != m.upper()[:5]:
            mis.append((r["Name"], m, txt))
print("Prefiks FRAUD (...) yang tidak cocok dengan kolom Modus:")
for x in mis: print("   ", x)
print("total:", len(mis))
print("\nBaris modus non-fraud (anomali/overbilling/prolonged_stay) dengan kolom Sindikat kosong:",
      sum(1 for r in rows if n(r["Modus"]) and n(r["Risiko"]) != "fraud" and not n(r["Sindikat"])))
print("Baris modus non-fraud yang TIDAK punya 'Catatan':",
      [(r["Name"], n(r["Modus"])) for r in rows
       if n(r["Modus"]) and n(r["Risiko"]) != "fraud" and not n(r["Catatan"])][:12])
print("Catatan kosong pada baris fraud:",
      [(r["Name"]) for r in rows if n(r["Risiko"]) == "fraud" and not n(r["Catatan"])])

# ---- 11. Umpan Balik Pasien & sentimen vs label fraud
h("11. UMPAN BALIK PASIEN vs LABEL")
ub = Counter(n(r["Umpan Balik Pasien"]) for r in rows)
print("jumlah umpan balik unik:", len(ub))
print("paling sering:", ub.most_common(6))
fraud_neg = sum(1 for r in rows if n(r["Risiko"]) == "fraud" and n(r["Sentimen"]) == "negatif")
low_neg = sum(1 for r in rows if n(r["Risiko"]) == "low" and n(r["Sentimen"]) == "negatif")
print(f"baris fraud dengan sentimen negatif: {fraud_neg}/36")
print(f"baris low dengan sentimen negatif   : {low_neg}/240 (negative control per 10-simulation-dataset.md)")

# ---- 12. Simpan ringkasan final
h("12. RINGKASAN AKHIR")
res = {
 "rasio_ok": len(ok), "rasio_bad": len(bad),
 "biaya_negatif": sum(1 for r in rows if int(n(r["Biaya Rp"])) < 0),
 "biaya_nol": sum(1 for r in rows if int(n(r["Biaya Rp"])) == 0),
 "skor_beda_kanal": sorted(x[0] for x in notexact),
}
print(json.dumps(res, ensure_ascii=False, indent=1))
