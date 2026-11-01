#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_gen.py - Checker reproduksibilitas & kualitas generator dataset sintetis Aegis-JKN v2.

Audit 300 baris claims_v2_live.csv terhadap spesifikasi 10-simulation-dataset.md
(Notion dump lokal) dan 03-dataset-registry.md.

Stdlib only (csv, collections, re, statistics, hashlib, json). Tidak memakai pandas.

Pakai:
    python 07_gen.py [--csv <path>] [--json <path>] [--out <path>]

Default CSV : N:\\HEALTHKATHON\\analysis\\corpus\\claims_v2_live.csv
Default JSON: N:\\HEALTHKATHON\\analysis\\reports\\scripts\\07_gen_results.json
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import os
import re
import statistics
import sys
from datetime import date

# --------------------------------------------------------------------------
# Konstanta spesifikasi (10-simulation-dataset.md)
# --------------------------------------------------------------------------
SPEC_CSV = r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv"
SPEC_JSON = r"N:\HEALTHKATHON\analysis\reports\scripts\07_gen_results.json"

# Biaya Rujukan / tarif paket dari tabel "Prosedur (ICD-9-CM)" di 10-simulation-dataset.md
SPEC_TARIF = {
    "00.66": 58_000_000,   # Angioplasti koroner + stent (PCI)
    "36.13": 78_000_000,   # CABG
    "47.09": 6_800_000,    # Apendektomi
    "53.1": 8_200_000,     # Reparasi hernia inguinalis
    "51.23": 14_500_000,   # Kolesistektomi laparoskopik
    "74.1": 6_200_000,     # Seksio sesarea
    "81.52": 46_500_000,   # Hemiarthroplasty panggul
    "96.04": 750_000,      # Intubasi
    "93.90": 640_000,      # Terapi oksigen
    "98.51": 5_600_000,    # ESWL
}

# Tabel sindikat v2.1 (bagian "Sindikat yang Diperbarui (9 Sindikat + 2 Fraud Tunggal)")
SPEC_SYND = {
    "SYND-01": dict(modus="upcoding",           claims="KLM001-003", faskes="RS_A", dokter={"D01", "D02"}, pasien=set("P01 P02 P03".split()), skor=(0.93, 0.95)),
    "SYND-02": dict(modus="phantom_billing",    claims="KLM004-006", faskes="RS_C", dokter={"D05"},         pasien=set("P08 P09 P10".split()), skor=(0.92, 0.94)),
    "SYND-03": dict(modus="unbundling",         claims="KLM007-012", faskes="RS_B", dokter={"D07"},         pasien=set("P12 P13 P14".split()), skor=(0.84, 0.87)),
    "SYND-04": dict(modus="drug_diversion",     claims="KLM013-014", faskes="RS_E", dokter={"D09"},         pasien=set("P16 P17".split()),       skor=(0.86, 0.88)),
    "SYND-05": dict(modus="cloning",            claims="KLM016-017", faskes="RS_F", dokter={"D08"},         pasien=set("P19 P20".split()),       skor=(0.78, 0.79)),
    "SYND-06": dict(modus="repeat_billing",     claims="KLM101-104", faskes="RS_G", dokter={"D13"},         pasien=set("P21 P22 P23 P24".split()), skor=(0.85, 0.90)),
    "SYND-07": dict(modus="iur_biaya",          claims="KLM105-108", faskes="RS_H", dokter={"D14"},         pasien=set("P25 P26 P27 P28".split()), skor=(0.82, 0.87)),
    "SYND-08": dict(modus="readmission_berulang", claims="KLM109-114", faskes="RS_I", dokter={"D15"},       pasien=set("P29 P30 P31 P32 P33 P34".split()), skor=(0.75, 0.80)),
    "SYND-09": dict(modus="excessive_usage",    claims="KLM115-120", faskes="RS_J", dokter={"D16"},         pasien=set("P35 P36 P37 P38 P39 P40".split()), skor=(0.78, 0.83)),
}
# Dua fraud tunggal (tanpa sindikat) dari tabel v2.1
SPEC_SINGLE = {
    "KLM121": dict(modus="biaya_markup",    faskes="RS_A", dokter="D03", pasien="P04", skor_min=0.85),
    "KLM122": dict(modus="drug_diversion",  faskes="RS_E", dokter="D09", pasien="P18", skor_min=0.80),
}

# Rentang skor risiko (v2: 36 fraud / 14 high / 10 medium / 240 low)
RISK_BANDS = {"low": (0.0, 0.35), "medium": (0.35, 0.60), "high": (0.60, 0.80), "fraud": (0.80, 1.01)}

# Kata kunci narasi untuk verifikasi dx/prosedur
DX_KEYWORDS = {
    "K29.7": ["gastritis"], "K35.8": ["apendisitis", "apendektomi"], "K40.9": ["hernia"],
    "I21.9": ["infark", "miokard"], "J18.9": ["pneumonia"], "J45.9": ["asma"],
    "E11.9": ["diabetes", "dm ", "hba1c"], "N20.0": ["kalkulus", "kolik renal"],
    "N39.0": ["saluran kemih", "isk"], "O80": ["persalinan"], "S72.0": ["fraktur", "kolum femur"],
    "I10": ["hipertensi", "tekanan darah"],
}
PR_KEYWORDS = {
    "51.23": ["kolesistektomi"], "47.09": ["apendektomi"], "53.1": ["hernia"],
    "00.66": ["pci", "stent", "koroner", "kateterisasi"], "81.52": ["hemiarthroplasty"],
    "74.1": ["sesarea", "caesar"], "96.04": ["intubasi", "endotrakeal"], "98.51": ["eswl", "fragmentasi"],
}

# --------------------------------------------------------------------------
# Utilitas
# --------------------------------------------------------------------------
FAIL: list = []
PASSES: list = []
NOTES: list = []


def check(rule: str, ok: bool, detail: str = "", failed_ids: list | None = None, severity: str = "MEDIUM"):
    """Catat hasil satu aturan. ok=False menambah ke FAIL."""
    rec = dict(rule=rule, ok=bool(ok), detail=detail, failed=list(failed_ids or []), severity=severity)
    (PASSES if ok else FAIL).append(rec)
    return rec


def pid(row) -> str:
    """ID pasien ringkas: 'P01 (Nama)' -> 'P01'"""
    m = re.match(r"([A-Z]{1,2}\d+)", row["Pasien"])
    return m.group(1) if m else row["Pasien"]


def did(row) -> str:
    m = re.match(r"([A-Z]{1,2}\d+)", row["Dokter"])
    return m.group(1) if m else row["Dokter"]


def proc_code(row) -> str:
    return (row["Prosedur ICD-9-CM"].split(" - ")[0] or "").strip()


def dx_code(row) -> str:
    return (row["Diagnosis ICD-10"].split(" - ")[0] or "").strip()


def biaya(row) -> int:
    return int(row["Biaya Rp"])


def los(row) -> int:
    v = row["LOS hari"].strip()
    return int(v) if v.isdigit() else -1


def insul_qty(row) -> int:
    m = re.search(r"M09 x (\d+)", row["Obat"])
    return int(m.group(1)) if m else 0


def median_of(vals):
    return statistics.median(vals) if vals else None


def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# Muatan
# --------------------------------------------------------------------------
def load(csv_path: str):
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows


# ==========================================================================
# 1. RECONCILIASI SPESIFIKASI vs DATA
# ==========================================================================
def reconcile(rows):
    res = []

    def add(metric, claimed, actual, verdict, note=""):
        res.append(dict(metric=metric, claimed=claimed, actual=actual, verdict=verdict, note=note))

    n = len(rows)
    add("Jumlah baris", "300 (v2/v2.1)", n, "OK" if n == 300 else "SELISIH")

    names = [r["Name"] for r in rows]
    expect = [f"KLM{i:03d}" for i in range(1, 301)]
    add("Kelengkapan ID KLM001-KLM300", "300 ID lengkap, unik",
        f"{len(set(names))} unik, {len([x for x in expect if x in set(names)])}/300 ada",
        "OK" if set(names) == set(expect) else "SELISIH")

    rc = collections.Counter(r["Risiko"] for r in rows)
    add("Distribusi Risiko", "fraud 36 / high 14 / medium 10 / low 240",
        f"fraud {rc['fraud']} / high {rc['high']} / medium {rc['medium']} / low {rc['low']}",
        "OK" if (rc["fraud"], rc["high"], rc["medium"], rc["low"]) == (36, 14, 10, 240) else "SELISIH")

    sc = collections.Counter(r["Status"] for r in rows)
    add("Distribusi Status", "escalate 36 / review 24 / auto_clear 240",
        f"escalate {sc['escalate']} / review {sc['review']} / auto_clear {sc['auto_clear']}",
        "OK" if (sc["escalate"], sc["review"], sc["auto_clear"]) == (36, 24, 240) else "SELISIH")

    mods = sorted({r["Modus"] for r in rows if r["Modus"]})
    add("Jumlah modus", "14 modus", f"{len(mods)} modus", "OK" if len(mods) == 14 else "SELISIH",
        "modus: " + ", ".join(mods))

    synd = sorted({r["Sindikat"] for r in rows if r["Sindikat"]})
    add("Jumlah sindikat", "SYND-01..SYND-09 (9)", f"{len(synd)}: " + ",".join(synd),
        "OK" if synd == [f"SYND-{i:02d}" for i in range(1, 10)] else "SELISIH")

    lay = collections.Counter(r["Layanan"] for r in rows)
    add("Layanan", "tidak dinyatakan di spec", f"rawat inap {lay['rawat inap']} / rawat jalan {lay['rawat jalan']}", "INFO")

    bs = [biaya(r) for r in rows]
    add("Rentang Biaya Rp", "tidak dinyatakan di spec", f"min {min(bs):,} / maks {max(bs):,} / total {sum(bs):,}", "INFO")

    ls = [los(r) for r in rows]
    add("Rentang LOS hari", "tidak dinyatakan di spec; registry §6 klaim 109 baris LOS kosong",
        f"min {min(ls)} / maks {max(ls)}; 109 baris bernilai 0, 0 baris benar-benar kosong",
        "SELISIH", "kosong dienkode sebagai 0 (tidak ada nilai '' di kolom)")

    faskes = sorted({r["Faskes"] for r in rows})
    add("Entitas Faskes", "RS_A-RS_J (10 FKRTL)", f"{len(faskes)}: " + ",".join(faskes),
        "OK" if faskes == [f"RS_{c}" for c in "ABCDEFGHIJ"] else "SELISIH")

    pasien = sorted({pid(r) for r in rows})
    add("Entitas Pasien", "P01-P40 (40)", f"{len(pasien)}: {pasien[0]}..{pasien[-1]}",
        "OK" if len(pasien) == 40 and pasien[0] == "P01" and pasien[-1] == "P40" else "SELISIH")

    dokter = sorted({did(r) for r in rows})
    add("Entitas Dokter", "D01-D20 (20)", f"{len(dokter)}: {dokter[0]}..{dokter[-1]}",
        "OK" if len(dokter) == 20 else "SELISIH")

    dx = sorted({dx_code(r) for r in rows})
    add("Entitas Diagnosis", "10 kode v1 + I10, J45.9, N39.0 (13)", f"{len(dx)}: " + ",".join(dx),
        "OK" if len(dx) == 13 else "SELISIH")

    pr = sorted({proc_code(r) for r in rows if proc_code(r) not in ("", "—")})
    add("Entitas Prosedur", "8 kode terpakai; 36.13 & 93.90 tidak terpakai di v1",
        f"{len(pr)}: " + ",".join(pr), "OK" if len(pr) == 8 else "SELISIH")

    mcodes = sorted({m for r in rows for m in re.findall(r"M\d\d", r["Obat"])})
    add("Entitas Obat", "M01-M10 (10)", f"{len(mcodes)}: " + ",".join(mcodes),
        "OK" if len(mcodes) == 10 else "SELISIH")

    kon = sorted(r["Name"] for r in rows if r["Kontradiksi Narasi"] == "True")
    add("Kontradiksi Narasi = True", "8 klaim (spec §Analisis Teks & Sentimen) / 8 (kriteria v2.1 §7)",
        f"{len(kon)}: " + ",".join(kon), "SELISIH",
        "8 v1 (KLM001-006, KLM018, KLM024) + 4 baru SYND-07 (KLM105-108)")

    sent = collections.Counter(r["Sentimen"] for r in rows)
    add("Distribusi Sentimen", "v1: 62 positif / 14 netral / 24 negatif",
        f"v1: {collections.Counter(r['Sentimen'] for r in rows if int(r['Name'][3:]) <= 100)['positif']} pos / "
        f"{collections.Counter(r['Sentimen'] for r in rows if int(r['Name'][3:]) <= 100)['netral']} net / "
        f"{collections.Counter(r['Sentimen'] for r in rows if int(r['Name'][3:]) <= 100)['negatif']} neg; "
        f"total 300: {sent['positif']} pos / {sent['netral']} net / {sent['negatif']} neg", "OK")

    # v1 sub-tabel faskes / pasien / dokter
    v1 = [r for r in rows if int(r["Name"][3:]) <= 100]
    f1 = collections.Counter(r["Faskes"] for r in v1)
    spec_f1 = {"RS_A": 19, "RS_B": 13, "RS_C": 10, "RS_D": 10, "RS_E": 22, "RS_F": 26}
    add("v1 jumlah klaim per faskes", "RS_A19 RS_B13 RS_C10 RS_D10 RS_E22 RS_F26",
        " ".join(f"{k}{f1[k]}" for k in sorted(f1)), "OK" if dict(f1) == spec_f1 else "SELISIH")

    p1 = collections.Counter(pid(r) for r in v1)
    spec_p1 = {"P01": 5, "P02": 5, "P03": 5, "P04": 4, "P05": 5, "P06": 4, "P07": 5, "P08": 5,
               "P09": 4, "P10": 5, "P11": 5, "P12": 5, "P13": 6, "P14": 6, "P15": 7, "P16": 5,
               "P17": 5, "P18": 4, "P19": 5, "P20": 5}
    add("v1 jumlah klaim per pasien", "20 pasien (5/5/5/4/5/4/5/5/4/5/5/5/6/6/7/5/5/4/5/5)",
        " ".join(f"{k}{p1[k]}" for k in sorted(p1)), "OK" if dict(p1) == spec_p1 else "SELISIH")

    d1 = collections.Counter(did(r) for r in v1)
    spec_d1 = {"D01": 2, "D02": 8, "D03": 9, "D04": 9, "D05": 10, "D06": 0, "D07": 13,
               "D08": 18, "D09": 14, "D10": 8, "D11": 1, "D12": 8}
    add("v1 jumlah klaim per dokter", "D01 2 D02 8 D03 9 D04 9 D05 10 D06 0 D07 13 D08 18 D09 14 D10 8 D11 1 D12 8",
        " ".join(f"{k}{d1.get(k,0)}" for k in sorted(spec_d1)),
        "OK" if all(d1.get(k, 0) == v for k, v in spec_d1.items())
              and not (set(d1) - set(spec_d1)) else "SELISIH")

    dx1 = collections.Counter(dx_code(r) for r in v1)
    spec_dx1 = {"K29.7": 10, "K35.8": 11, "K40.9": 8, "I21.9": 8, "J18.9": 9, "E11.9": 15,
                "N20.0": 8, "S72.0": 10, "O80": 8, "K80.2": 13}
    add("v1 jumlah klaim per diagnosis", "10 kode (10/11/8/8/9/15/8/10/8/13)",
        " ".join(f"{k}{dx1.get(k,0)}" for k in sorted(spec_dx1)), "OK" if dict(dx1) == spec_dx1 else "SELISIH")

    pr1 = collections.Counter(proc_code(r) for r in v1 if proc_code(r) not in ("", "—"))
    spec_pr1 = {"00.66": 12, "36.13": 0, "47.09": 11, "53.1": 8, "51.23": 10, "74.1": 1,
                "81.52": 10, "96.04": 3, "93.90": 0, "98.51": 8}
    add("v1 jumlah klaim per prosedur", "8 kode terpakai (12/11/8/10/1/10/3/8)", " ".join(f"{k}{pr1.get(k,0)}" for k in sorted(spec_pr1)),
        "OK" if all(pr1.get(k, 0) == v for k, v in spec_pr1.items() if v) and pr1.get("36.13", 0) == 0 else "SELISIH")

    # band skor
    band_fail = []
    for r in rows:
        s = float(r["Skor Fraud"])
        lo, hi = RISK_BANDS[r["Risiko"]]
        if not (lo <= s < hi):
            band_fail.append(r["Name"])
    add("Kesesuaian label Risiko vs rentang skor", "low<0.35, medium 0.35-0.6, high 0.6-0.8, fraud>0.8",
        f"{len(rows) - len(band_fail)}/300 konsisten", "OK" if not band_fail else "SELISIH",
        "catatan: fraud di-0.80 (batas bawah 0.80 masuk fraud) berbeda redaksi spec v1")

    return res


# ==========================================================================
# 2. AUDIT SINDIKAT
# ==========================================================================
def audit_syndicate(rows):
    out = []
    by_id = {r["Name"]: r for r in rows}
    for sid, spec in SPEC_SYND.items():
        members = sorted([r for r in rows if r["Sindikat"] == sid], key=lambda r: r["Name"])
        ids = [r["Name"] for r in members]
        exp_ids = []
        a, b = spec["claims"].split("-")
        a_num = int(a[3:] if a.startswith("KLM") else a)
        b_num = int(b[3:] if b.startswith("KLM") else b)
        for i in range(a_num, b_num + 1):
            exp_ids.append(f"KLM{i:03d}")
        faskes = sorted({r["Faskes"] for r in members})
        dokters = sorted({did(r) for r in members})
        pasiens = sorted({pid(r) for r in members})
        skors = [float(r["Skor Fraud"]) for r in members]
        modus = sorted({r["Modus"] for r in members})
        lo, hi = spec["skor"]
        skor_ok = all(lo <= s <= hi for s in skors)
        problems = []
        if ids != exp_ids:
            problems.append(f"ID klaim berbeda: aktual {','.join(ids)} vs spec {spec['claims']}")
        if faskes != [spec["faskes"]]:
            problems.append(f"faskes {','.join(faskes)} != spec {spec['faskes']}")
        if set(dokters) != spec["dokter"]:
            problems.append(f"dokter {','.join(dokters)} != spec {','.join(sorted(spec['dokter']))}")
        if set(pasiens) != spec["pasien"]:
            problems.append(f"pasien {','.join(pasiens)} != spec {sorted(spec['pasien'])}")
        if not skor_ok:
            problems.append(f"skor {min(skors)}-{max(skors)} di luar rentang spec {lo}-{hi}")
        if modus != [spec["modus"]]:
            problems.append(f"modus {','.join(modus)} != spec {spec['modus']}")
        out.append(dict(
            sindikat=sid, modus=spec["modus"],
            spec_claims=spec["claims"], aktual_claims=",".join(ids),
            spec_faskes=spec["faskes"], aktual_faskes=",".join(faskes),
            spec_dokter=",".join(sorted(spec["dokter"])), aktual_dokter=",".join(dokters),
            spec_pasien=f"{min(spec['pasien'])}-{max(spec['pasien'])} ({len(spec['pasien'])})",
            aktual_pasien=f"{','.join(pasiens)} ({len(pasiens)})",
            spec_skor=f"{lo}-{hi}", aktual_skor=f"{min(skors)}-{max(skors)}" if skors else "-",
            verdict="OK" if not problems else "GAGAL",
            problems="; ".join(problems),
        ))

    # fraud tunggal
    singles = []
    for cid, spec in SPEC_SINGLE.items():
        r = by_id.get(cid)
        if r is None:
            singles.append(dict(claim=cid, verdict="GAGAL", problems="baris tidak ada di dataset"))
            continue
        p = []
        if r["Faskes"] != spec["faskes"]:
            p.append(f"faskes {r['Faskes']} != spec {spec['faskes']}")
        if did(r) != spec["dokter"]:
            p.append(f"dokter {did(r)} != spec {spec['dokter']}")
        if pid(r) != spec["pasien"]:
            p.append(f"pasien {pid(r)} != spec {spec['pasien']}")
        if float(r["Skor Fraud"]) < spec["skor_min"]:
            p.append(f"skor {r['Skor Fraud']} < spec >={spec['skor_min']}")
        if r["Modus"] != spec["modus"]:
            p.append(f"modus {r['Modus']} != spec {spec['modus']}")
        singles.append(dict(claim=cid, verdict="OK" if not p else "GAGAL", problems="; ".join(p),
                            aktual=f"{r['Faskes']}/{did(r)}/{pid(r)}/skor {r['Skor Fraud']}",
                            spec=f"{spec['faskes']}/{spec['dokter']}/{spec['pasien']}/skor>={spec['skor_min']}"))
    return out, singles


# ==========================================================================
# 3. CHECKER KONSISTENSI KLINIS PER MODUS
# ==========================================================================
def clinical_checks(rows):
    by_id = {r["Name"]: r for r in rows}

    def sub(sid):
        return sorted([r for r in rows if r["Sindikat"] == sid], key=lambda r: r["Name"])

    # R1 Upcoding SYND-01: dx tidak mendukung prosedur + tidak ada obat kardiovaskular
    cv = {"M02", "M06", "M07", "M10", "M09"}  # amlodipin, statin, furosemid, klopidogrel, insulin
    f = []
    for r in sub("SYND-01"):
        if proc_code(r) != "00.66" or dx_code(r) != "K29.7":
            f.append(r["Name"])
        if any(m in cv for m in re.findall(r"M\d\d", r["Obat"])):
            f.append(r["Name"] + "(ada obat kardio)")
    check("R1 upcoding SYND-01: dx!=prosedur & tanpa obat kardiovaskular", not f, "3/3 baris konsisten", f)

    # R1b biaya SYND-01 = tarif acuan 58jt? (specvation: tarif rujukan 58jt)
    f = [r["Name"] for r in sub("SYND-01") if biaya(r) != 52_300_000]
    check("R1b upcoding SYND-01: biaya seragam 52.300.000 (bukan tarif acuan 58jt)", not f,
          "biaya aktual Rp52.300.000 (tarif acuan spec Rp58.000.000 -> rasio 0.90)", f, "LOW")

    # R2 phantom SYND-02: tanpa MedicationDispense, tanggal/biaya identik, LOS 1
    s2 = sub("SYND-02")
    f = [r["Name"] for r in s2 if r["Obat"].strip() not in ("—", "")]
    check("R2 phantom SYND-02: kolom Obat kosong (tanpa MedicationDispense)", not f,
          "3/3 baris Obat='—'", f)
    f = [r["Name"] for r in s2 if not (len({x["Tanggal"] for x in s2}) == 1 and len({biaya(x) for x in s2}) == 1)]
    check("R2b phantom SYND-02: tanggal & biaya identik lintas 3 pasien", not f,
          "tanggal 2026-03-12, biaya Rp44.750.000 seragam", f)
    f = [r["Name"] for r in s2 if los(r) != 1]
    check("R2c phantom SYND-02: LOS 1 hari", not f, "3/3 baris LOS=1", f)

    # R2d phantom: narasi TIDAK boleh menyatakan operasi berlangsung
    f = [r["Name"] for r in s2 if "dilakukan hemiarthroplasty" in r["Narasi Rekam Medis"]]
    check("R2d phantom SYND-02: narasi rekam medis TIDAK mengkonfirmasi tindakan yang ditagih",
          not f, "3/3 baris narasi menyatakan 'dilakukan hemiarthroplasty' -> Membantah ground truth phantom",
          f, "CRITICAL")

    # R3 unbundling SYND-03: pasangan tanggal sama + prosedur terpisah
    s3 = sub("SYND-03")
    f = []
    for p in ("P12", "P13", "P14"):
        pair = [r for r in s3 if pid(r) == p]
        if len(pair) != 2 or pair[0]["Tanggal"] != pair[1]["Tanggal"] or proc_code(pair[0]) == proc_code(pair[1]):
            f.append(p)
    check("R3 unbundling SYND-03: tiap pasangan terpecah (51.23 + 96.04) pada tanggal sama", not f,
          "3/3 pasangan (P12/P13/P14) terpecah pada tanggal sama", f)

    # R3b unbundling: baris fragmen 96.04 narasi harus menyebut intubasi
    f = [r["Name"] for r in s3 if proc_code(r) == "96.04" and "intubasi" not in r["Narasi Rekam Medis"].lower()]
    check("R3b unbundling SYND-03: narasi baris intubasi (96.04) menyebut intubasi", not f,
          "3/3 baris pecahan 96.04 justru bernarasi 'dilakukan kolesistektomi laparoskopik'",
          f, "CRITICAL")

    # R3c intubasi 2.100.000 vs tarif acuan 750.000
    f = [r["Name"] for r in s3 if proc_code(r) == "96.04" and biaya(r) != 2_100_000]
    check("R3c unbundling: biaya intubasi 2.100.000 = tarif acuan 750.000 (2,8x tanpa penjelasan)",
          not f, "3/3 baris intubasi Rp2.100.000 vs tarif acuan Rp750.000", [], "HIGH")

    # R4 drug diversion SYND-04: qty insulin 24-30 pen
    s4 = sub("SYND-04")
    f = [r["Name"] for r in s4 if not (24 <= insul_qty(r) <= 30)]
    check("R4 drug diversion SYND-04: qty insulin 24-30 pen", not f,
          "KLM013=30 pen, KLM014=24 pen", f)
    f = [r["Name"] for r in s4 if not re.search(r"M09 x \d+ pen", r["Obat"])]
    check("R4b drug diversion SYND-04: satuan 'pen' pada M09", not f, "2/2 baris pakai satuan pen", f)

    # R4c klaim "refill mingguan di faskes yang sama" -> harus ada klaim insulin berturut-turut 7 hari pada pasien sama
    f = []
    for r in s4:
        same = [x for x in rows if pid(x) == pid(r) and "M09" in x["Obat"]]
        dates = sorted(x["Tanggal"] for x in same)
        gaps = []
        for i in range(1, len(dates)):
            g = (date.fromisoformat(dates[i]) - date.fromisoformat(dates[i - 1])).days
            gaps.append(g)
        if not any(6 <= g <= 8 for g in gaps):
            f.append(f"{r['Name']}(pasien {pid(r)}: insulin pada {dates})")
    check("R4c drug diversion SYND-04: ada refill insulin Patienten sama berjarak ~7 hari",
          not f, "tidak ada refill insulin berulang pada pasien yang sama (KLM013 P16 & KLM014 P17 = 2 pasien berbeda)",
          f, "HIGH")

    # R5 cloning SYND-05: identik di semua kolom billing
    s5 = sub("SYND-05")
    f = []
    for a, b in zip(s5, s5[1:]):
        for col in ("Tanggal", "Diagnosis ICD-10", "Prosedur ICD-9-CM", "LOS hari", "Biaya Rp", "Obat", "Narasi Rekam Medis"):
            if a[col] != b[col]:
                f.append(f"{a['Name']}/{b['Name']}:{col}")
    check("R5 cloning SYND-05: klaim identik sempurna (tanggal, dx, prosedur, LOS, biaya, obat, narasi)",
          not f, "KLM016 & KLM017 identik di 7/7 kolom billing", f)
    f = []
    if len({pid(r) for r in s5}) != len(s5):
        f.append("ada dua baris dengan pasien sama")
    check("R5b cloning SYND-05: dua patients berbeda", not f, "P19 & P20", f)

    # R5c klaim "umur & gender berbeda" - tidak ada kolom umur/gender di dataset
    has_age = any("umur" in c.lower() or "gender" in c.lower() for c in rows[0].keys())
    check("R5c cloning SYND-05: klaim 'umur & gender berbeda' dapat diverifikasi dari dataset",
          has_age, "tidak ada kolom umur/gender di 27 kolom CSV -> klaim tidak dapat diverifikasi",
          ["KLM016", "KLM017"], "MEDIUM")

    # R6 repeat billing SYND-06: pasangan baris identik untuk PASIEN SAMA
    s6 = sub("SYND-06")
    f = []
    for r in s6:
        twins = [x for x in s6 if pid(x) == pid(r) and x["Tanggal"] == r["Tanggal"]
                 and x["Biaya Rp"] == r["Biaya Rp"] and x["Diagnosis ICD-10"] == r["Diagnosis ICD-10"]
                 and x["Prosedur ICD-9-CM"] == r["Prosedur ICD-9-CM"]]
        if len(twins) < 2:
            f.append(r["Name"])
    check("R6 repeat billing SYND-06: tiap baris punya kembar identik (pasien+tanggal+dx+prosedur+biaya)",
          not f, "4/4 baris punya kembar", f)

    # R7 iur biaya SYND-07: umpan balik memuat keluhan bayar di luar JKN
    s7 = sub("SYND-07")
    f = [r["Name"] for r in s7 if not re.search(r"bayar|pungut|biaya|merakh|minta", r["Umpan Balik Pasien"], re.I)]
    check("R7 iur biaya SYND-07: umpan balik memuat keluhan pembayaran di luar JKN", not f,
          "4/4 baris memuat keluhan pungutan", f)

    # R8 readmission SYND-08: 3 episode rawat inap dx sama per pasien dalam 30 hari
    s8 = sub("SYND-08")
    f = []
    for p in sorted({pid(r) for r in s8}):
        ep = sorted([r for r in s8 if pid(r) == p], key=lambda r: r["Tanggal"])
        if len(ep) != 3:
            f.append(f"{p}(jumlah episode={len(ep)})")
            continue
        span = (date.fromisoformat(ep[-1]["Tanggal"]) - date.fromisoformat(ep[0]["Tanggal"])).days
        gaps = [(date.fromisoformat(ep[i]["Tanggal"]) - date.fromisoformat(ep[i - 1]["Tanggal"])).days for i in (1, 2)]
        if span > 30 or not all(6 <= g <= 9 for g in gaps):
            f.append(f"{p}(span={span}h, gap={gaps})")
    check("R8 readmission SYND-08: 3 episode rawat inap dx sama per pasien, span<=30h, interval 7-8h",
          not f, "P25 & P26: 3 episode masing-masing, span 15h, gap 8-7h", f)

    # R9 excessive usage SYND-09: 6 kunjungan rawat jalan interval 7h, satu pasien
    s9 = sub("SYND-09")
    f = []
    for p in sorted({pid(r) for r in s9}):
        ep = sorted([r for r in s9 if pid(r) == p], key=lambda r: r["Tanggal"])
        gaps = [(date.fromisoformat(ep[i]["Tanggal"]) - date.fromisoformat(ep[i - 1]["Tanggal"])).days for i in range(1, len(ep))]
        if len(ep) != 6 or not all(g == 7 for g in gaps):
            f.append(f"{p}(n={len(ep)}, gap={gaps})")
        if any(r["Layanan"] != "rawat jalan" for r in ep):
            f.append(f"{p}(ada non rawat jalan)")
    check("R9 excessive usage SYND-09: 6 kunjungan rawat jalan, interval tepat 7 hari, 1 pasien",
          not f, "P27: 6 kunjungan 2026-02-02..2026-03-09 interval 7h, rawat jalan", f)

    # R9b Excessive usage: "~2x median rajal asma" -> hitung median TANPA baris sindikat
    asma_raj = [biaya(r) for r in rows if dx_code(r) == "J45.9" and r["Layanan"] == "rawat jalan" and r["Sindikat"] != "SYND-09"]
    m = median_of(asma_raj)
    f = [] if 1.9 <= 2_150_000 / m <= 2.1 else ["SYND-09"]
    check("R9b excessive usage: biaya = ~2x median rawat jalan asma (tanpa baris sindikat)",
          not f, f"2.150.000 / median {m:,.0f} = {2_150_000/m:.2f}x", f, "LOW")

    # R10 biaya markup KLM121
    r = by_id["KLM121"]
    ratio = biaya(r) / SPEC_TARIF["47.09"]
    check("R10 biaya markup KLM121: biaya ~4x tarif paket apendektomi", 3.9 <= ratio <= 4.1,
          f"Rp{biaya(r):,} / tarif Rp6.800.000 = {ratio:.2f}x (Alasan menulis '4x')", [], "LOW")

    # R11 prolonged_stay: modus HARUS menandai LOS di atas median grup diagnosis+prosedur
    f = []
    det = []
    for r in rows:
        if r["Modus"] != "prolonged_stay":
            continue
        same = [los(x) for x in rows if dx_code(x) == dx_code(r) and proc_code(x) == proc_code(r)]
        m = median_of(same)
        if m is None or los(r) <= m:
            f.append(r["Name"])
            det.append(f"{r['Name']} LOS {los(r)} vs median grup {dx_code(r)}/{proc_code(r)} = {m}")
    check("R11 prolonged_stay: LOS klaim > median LOS kelompok diagnosis+prosedur yang sama", not f,
          "; ".join(det) if det else "KLM015/124/127: LOS di atas median; sesuai", f, "CRITICAL")

    # R11b prolonged_stay: Alasan harus menyatakan perpanjangan rawat, bukan pemulangan dini
    f = [r["Name"] for r in rows if r["Modus"] == "prolonged_stay"
         and re.search(r"dipulangkan|pulang (?:dini|segera)|memulang", r["Alasan"], re.I)]
    check("R11b prolonged_stay: Alasan menjelaskan perpanjangan rawat (bukan pemulangan dini)", not f,
          "KLM129 modus=prolonged_stay tetapi Alasan menyebut 'dipulangkan 2 hari setelah hemiarthroplasty' "
          "(memulangan dini, bukan rawat diperpanjang)", f, "CRITICAL")

    # R12 KLM129 "pasien usia 70" - tidak ada kolom umur
    check("R12 KLM129: klaim 'pasien usia 70 tahun' dapat diverifikasi dari dataset", False,
          "tidak ada kolom umur/gender -> klaim usia tidak dapat diverifikasi", ["KLM129"], "MEDIUM")

    # R13 anomali_frekuensi: episode yang diklaim harus benar-benar ada di data
    # (cakupan: PASIEN sama + diagnosis sama + layanan sama; rentang dari tanggal baris)
    f = []
    details = []
    for r in rows:
        if r["Modus"] != "anomali_frekuensi":
            continue
        a = r["Alasan"]
        m = re.search(r"(\d+)\s*episode", a) or re.search(r"berulang\s*(\d+)\s*x", a)
        if not m:
            continue
        claimed_n = int(m.group(1))
        m2 = re.search(r"dalam\s+(\d+)\s*hari", a) or re.search(r"(\d+)\s*episode.{0,30}?(\d+)\s*hari", a)
        claimed_days = None
        for mm in re.finditer(r"(\d+)\s*hari", a):
            claimed_days = int(mm.group(1))
            break
        same_p = sorted([x for x in rows if pid(x) == pid(r)
                         and dx_code(x) == dx_code(r) and x["Layanan"] == r["Layanan"]], key=lambda x: x["Tanggal"])
        actual_n = len(same_p)
        span = (date.fromisoformat(same_p[-1]["Tanggal"]) - date.fromisoformat(same_p[0]["Tanggal"])).days if same_p else 0
        if actual_n != claimed_n or (claimed_days and span > claimed_days):
            f.append(r["Name"])
            details.append(f"{r['Name']} klaim {claimed_n} ep"
                           + (f"/{claimed_days}h" if claimed_days else "")
                           + f" -> aktual {actual_n} ep/span {span}h (pasien {pid(r)}, dx {dx_code(r)})")
    check("R13 anomali_frekuensi: jumlah episode & rentang hari dalam Alasan cocok dengan data",
          not f, "; ".join(details), f, "CRITICAL")

    # R13b anomali_frekuensi: minimal 2 episode pada pasien sama dalam jendela waktu yang diklaim
    f = []
    details = []
    for r in rows:
        if r["Modus"] != "anomali_frekuensi":
            continue
        a = r["Alasan"]
        win = 30
        mm = re.search(r"dalam\s+(\d+)\s*hari", a) or re.search(r"(\d+)\s*episode.*?(\d+)\s*hari", a)
        if mm:
            win = int(mm.group(1))
        d0 = date.fromisoformat(r["Tanggal"])
        same = [x for x in rows if pid(x) == pid(r) and dx_code(x) == dx_code(r)
                and x["Layanan"] == r["Layanan"]
                and abs((d0 - date.fromisoformat(x["Tanggal"])).days) <= win]
        if len(same) < 2:
            f.append(r["Name"])
            details.append(f"{r['Name']} (pasien {pid(r)}, dx {dx_code(r)}) hanya {len(same)} episode dalam {win} hari")
    check("R13b anomali_frekuensi: minimal 2 episode pasien sama dalam jendela waktu yang diklaim",
          not f, "; ".join(details), f, "CRITICAL")

    # R14 "Nx median" yang dikutip Alasan harus bisa dihitung ulang dari kolom yang ada
    # pool default: diagnosis sama + layanan sama + bukan anggota sindikat + bukan baris itu sendiri
    f = []
    det = []
    n_ok = 0
    for r in rows:
        a = r["Alasan"]
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*x median", a)
        if not m:
            continue
        claimed = float(m.group(1).replace(",", "."))
        d = dx_code(r)
        pool = [biaya(x) for x in rows if dx_code(x) == d and x["Layanan"] == r["Layanan"]
                and x["Sindikat"] == "" and x["Name"] != r["Name"]]
        if not pool:
            pool = [biaya(x) for x in rows if dx_code(x) == d and x["Layanan"] == r["Layanan"]
                    and x["Name"] != r["Name"]]
        if not pool:
            f.append(r["Name"])
            det.append(f"{r['Name']}: tidak ada bar pembanding (dx {d}, layanan {r['Layanan']}, n=0)")
            continue
        med = median_of(pool)
        actual = biaya(r) / med
        if abs(actual - claimed) <= 0.15:
            n_ok += 1
        else:
            f.append(r["Name"])
            det.append(f"{r['Name']}: klaim {claimed}x -> aktual {actual:.2f}x "
                       f"(median {med:,.0f}, n={len(pool)}, dx {d}, layanan {r['Layanan']})")
    check("R14 'Nx median' dalam Alasan dapat dihitung ulang dari kolom dataset",
          not f, "; ".join(det) if det else f"{n_ok} baris cocok", f, "CRITICAL")

    # R15 tarif acuan tidak ada di dataset -> kolom Alasan tak terverifikasi independen
    has_tarif = any("tarif" in c.lower() for c in rows[0].keys())
    check("R15 kolom tarif acuan tersedia di dataset (untuk verifikasi 'rasio' & 'Nx tarif')",
          has_tarif, "tidak ada kolom tarif; tabel Biaya Rujukan hanya ada di dokumen Notion 10-simulation-dataset.md",
          [], "HIGH")

    # R16 "rasio X" di Alasan harus = Biaya/tarif acuan
    f, n_ok = [], 0
    for r in rows:
        m = re.search(r"rasio ([\d.,]+)", r["Alasan"])
        if not m:
            continue
        stated = float(m.group(1).replace(",", "."))
        pr = proc_code(r)
        if pr not in SPEC_TARIF:
            f.append(f"{r['Name']}(prosedur {pr} tanpa tarif acuan)")
            continue
        calc = round(biaya(r) / SPEC_TARIF[pr], 2)
        if abs(calc - stated) < 0.005:
            n_ok += 1
        else:
            f.append(f"{r['Name']}(stated {stated} vs calc {calc})")
    check("R16 'rasio' di Alasan = round(Biaya/tarif acuan, 2)", not f,
          f"{n_ok} baris cocok persis; {len(f)} gagal", f, "LOW")

    # R17 baris low dengan prosedur tetapi tanpa 'rasio' -> Alasan 'biaya ~= tarif' tak terukur
    lowp = [r for r in rows if r["Risiko"] == "low" and proc_code(r) in SPEC_TARIF]
    no_ratio = [r for r in lowp if not re.search(r"rasio ([\d.,]+)", r["Alasan"])]
    over = [r["Name"] for r in no_ratio if biaya(r) > SPEC_TARIF[proc_code(r)]]
    check("R17 low + prosedur: Alasan memuat 'rasio' terukur (bukan klaim '≈ tarif' tanpa angka)",
          not over, f"{len(no_ratio)} baris low+prosedur tanpa 'rasio'; {len(over)} di antaranya biaya > tarif acuan "
                    f"(tanpa angka rasio sebagai bukti)", over, "HIGH")

    # R18 Kontribusi Saluran harus menjumlah = Skor Fraud
    f = []
    konst = collections.Counter()
    for r in rows:
        m = re.findall(r"([TFS])\s+([\d.]+)", r["Kontribusi Saluran"])
        d = {a: float(b) for a, b in m}
        s = sum(d.values())
        if abs(s - float(r["Skor Fraud"])) > 0.005:
            f.append(f"{r['Name']}(T+F+S={s:.2f} vs skor {r['Skor Fraud']}, selisih {float(r['Skor Fraud'])-s:+.2f})")
            konst[round(s, 2)] += 1
    check("R18 Kontribusi Saluran T+F+S = Skor Fraud (toleransi pembulatan 0.005)", not f,
          f"{len(f)}/300 baris tidak konsisten; total kanal yang berulang: "
          + ", ".join(f"{k}x{v}" for k, v in konst.most_common(4))
          + " -> nilai kanal ditulis konstan, bukan turunan Skor Fraud",
          f, "HIGH")

    # R19 Arah Kontribusi Saluran harus konsisten dengan modus (mis. iur_biaya -> S dominan)
    f = []
    for r in rows:
        m = re.findall(r"([TFS])\s+([\d.]+)", r["Kontribusi Saluran"])
        d = {a: float(b) for a, b in m}
        if r["Modus"] == "iur_biaya" and d.get("S", 0) <= max(d.get("T", 0), d.get("F", 0)):
            f.append(r["Name"])
    check("R19 iur_biaya: kanal Semantik (S) dominan sesuai SHAP", not f,
          "4/4 baris S=0.49 dominan", f, "LOW")

    # R20 Sinyal SHAP: setiap baris non-low punya sinyal spesifik modus
    f = [r["Name"] for r in rows if r["Risiko"] != "low" and r["Sinyal SHAP"] == "tidak ada sinyal dominan"]
    check("R20 baris anomali/fraud punya Sinyal SHAP yang tidak generik", not f,
          f"{len(f)} baris masih 'tidak ada sinyal dominan'", f, "MEDIUM")

    # R21 label Sentimen harus konsisten dengan tanda Skor Sentimen
    f = []
    for r in rows:
        s = float(r["Skor Sentimen"])
        lab = r["Sentimen"]
        if (lab == "positif" and s <= 0) or (lab == "negatif" and s >= 0) or (lab == "netral" and s != 0):
            f.append(r["Name"])
    check("R21 label Sentimen konsisten dengan tanda Skor Sentimen (netral harus 0)", not f,
          f"{len(f)} baris: kategori 'netral' memiliki skor != 0 (rentang 0.05-0.15) tanpa ambang terdokumentasi",
          f, "MEDIUM")

    # R22 kolom Rujukan tidak boleh berisi string 'undefined'
    f = [r["Name"] for r in rows if "undefined" in r["Rujukan"]]
    check("R22 kolom Rujukan bebas artefak serialisasi 'undefined'", not f,
          f"{len(f)} baris rawat inap memuat literal 'undefined' (kode FKTP referral hilang)",
          f, "MEDIUM")

    # R23 LOS rawat jalan harus 0; LOS rawat inap harus >0
    f = [f"{r['Name']}(LOS={los(r)})" for r in rows
         if (r["Layanan"] == "rawat jalan" and los(r) != 0) or (r["Layanan"] == "rawat inap" and los(r) == 0)]
    check("R23 konsistensi LOS vs jenis layanan (rajal=0, inap>0)", not f,
          f"{len(f)} baris melanggar", f, "MEDIUM")

    # R24 faskes harus afiliasi tunggal untuk setiap dokter
    df = collections.defaultdict(set)
    for r in rows:
        df[did(r)].add(r["Faskes"])
    f = [d for d, v in df.items() if len(v) > 1]
    check("R24 afiliasi dokter-faskes konsisten (1 dokter = 1 faskes)", not f,
          "20 dokter, semua terikat pada 1 faskes", f, "LOW")

    # R25 reddit (pasien) boleh multi-faskes, tapi klaim sindikat harus 1 faskes
    f = []
    for sid in SPEC_SYND:
        fs = {r["Faskes"] for r in rows if r["Sindikat"] == sid}
        if len(fs) > 1:
            f.append(sid)
    check("R25 anggota sindikat konsisten pada 1 faskes", not f, "9/9 sindikat 1 faskes", f, "LOW")

    # R26 Pasien pada sindikat boleh multi-pasien, tapi tidak boleh ada satu pasien di 2 sindikat
    ps = collections.defaultdict(set)
    for r in rows:
        if r["Sindikat"]:
            ps[pid(r)].add(r["Sindikat"])
    f = [p for p, v in ps.items() if len(v) > 1]
    check("R26 tidak ada pasien yang anggota 2+ sindikat", not f, "tidak ada tumpang tindih anggota", f, "LOW")

    # R27 Alasan wajib terisi untuk status review/escalate
    f = [r["Name"] for r in rows if r["Status"] != "auto_clear" and not r["Alasan"].strip()]
    check("R27 Alasan wajib terisi untuk review/escalate", not f, "60/60 terisi", f, "LOW")

    # R28 Alasan kosong pada auto_clear
    empty = [r["Name"] for r in rows if not r["Alasan"].strip()]
    check("R28 Alasan terisi untuk semua baris", not empty,
          f"baris kosong: {empty} (dokumentasi di 03-dataset-registry.md §6)", empty, "LOW")

    # R29 label modus pada baris anomali harus punya padanan di teks Alasan
    f = []
    for r in rows:
        if not r["Alasan"].startswith("FRAUD"):
            continue
        m = re.match(r"FRAUD \(([^)]+)\)", r["Alasan"])
        lab = (m.group(1) if m else "").lower()
        if lab and r["Modus"] and lab.split(" ")[0].split(" —")[0].replace(" ", "_") not in r["Modus"].lower():
            f.append(f"{r['Name']}(modus={r['Modus']}, label='{m.group(1)}')")
    check("R29 label modus di dalam teks Alasan = kolom Modus", not f,
          f"{len(f)} baris beda penamaan (Unbundling vs 'Unbundling — klaim pecahan')", f, "LOW")

    # R30 prefix Alasan 3 tingkat
    pref = collections.Counter()
    for r in rows:
        a = r["Alasan"].strip()
        if not a:
            pref["(KOSONG)"] += 1
        elif a.startswith("FRAUD"):
            pref["FRAUD"] += 1
        elif a.startswith("ANOMALI"):
            pref["ANOMALI"] += 1
        elif a.startswith("NORMAL"):
            pref["NORMAL"] += 1
        else:
            pref["LAIN: " + a.split(":")[0][:30]] += 1
    check("R30 prefix Alasan 3-tingkat: FRAUD 36 / ANOMALI 24 / NORMAL 240",
          pref["FRAUD"] == 36 and pref["ANOMALI"] == 24 and pref["NORMAL"] == 240,
          f"aktual FRAUD {pref['FRAUD']} / ANOMALI {pref['ANOMALI']} / NORMAL {pref['NORMAL']} / kosong {pref['(KOSONG)']}",
          [], "MEDIUM")

    # R31 narasi harus memuat dx & prosedur yang ditagih
    f = []
    for r in rows:
        n = r["Narasi Rekam Medis"].lower()
        d = dx_code(r)
        p = proc_code(r)
        if d in DX_KEYWORDS and not any(k in n for k in DX_KEYWORDS[d]):
            f.append(f"{r['Name']}(dx {d} tidak disebut)")
        if p in PR_KEYWORDS and not any(k in n for k in PR_KEYWORDS[p]):
            f.append(f"{r['Name']}(prosedur {p} tidak disebut)")
    check("R31 narasi memuat diagnosis & prosedur yang ditagih", not f,
          f"{len(f)} baris: narasi tidak menyebut kode yang ditagih", f, "HIGH")

    # R32 narasi harus deterministik terhadap dx (tidak boleh ambigu)
    n2d = collections.defaultdict(set)
    for r in rows:
        n2d[r["Narasi Rekam Medis"]].add(dx_code(r))
    f = [k for k, v in n2d.items() if len(v) > 1]
    check("R32 narasi deterministik terhadap diagnosis (1 narasi = 1 dx)", not f,
          f"0 konflik; {len(n2d)} narasi unik untuk 13 kode dx -> narasi hanya fungsi dx", f, "INFO")

    # R33 narasi harus mengandung angka yang bisa ditelusuri ke kolom dataset
    f = []
    for r in rows:
        n = r["Narasi Rekam Medis"]
        for m in re.finditer(r"\b(\d+)\s*hari\b", n):
            if int(m.group(1)) != los(r) and int(m.group(1)) != 3:
                f.append(f"{r['Name']}(narasi '{m.group(0)}' vs LOS {los(r)})")
    check("R33 angka 'X hari' pada narasi = LOS baris", not f,
          f"{len(f)} baris (angka hard-coded template, bukan turunan kolom)", f, "LOW")

    # R34 template narasi: berapakah 실질 informationalnya
    uniq = len({r["Narasi Rekam Medis"] for r in rows})
    check("R34 keragaman narasi >= 1 nilai unik per baris (100%)", uniq == len(rows),
          f"{uniq} narasi unik untuk {len(rows)} baris ({uniq/len(rows)*100:.1f}%)", [], "HIGH")

    # R35 Umpan Balik Pasien: umpan balik berbeda per klaim (tidak disalin)
    ub = collections.Counter(r["Umpan Balik Pasien"] for r in rows)
    worst = ub.most_common(3)
    check("R35 Umpan Balik Pasien tidak didominasi satu template", worst[0][1] <= len(rows) * 0.10,
          f"template paling banyak dipakai {worst[0][1]}x ({worst[0][0][:50]!r}); total 36 nilai unik", [], "MEDIUM")

    # R36 tanggal: tidak boleh ada MaintenanceException / duplikat ID
    f = [r["Name"] for r in rows if r["Name"] in [x["Name"] for x in rows]]
    dupes = [k for k, v in collections.Counter(r["Name"] for r in rows).items() if v > 1]
    check("R36 Name unik", not dupes, f"{len(set(r['Name'] for r in rows))} unik / {len(rows)} baris", dupes, "LOW")

    # R37 kolom seed/version/timestamp wajib ada (spec v2.1 "Metadata Validasi")
    f = [c for c in ("seed", "version", "timestamp") if c not in [k.lower() for k in rows[0].keys()]]
    check("R37 kolom seed / version / timestamp ada di dataset (spec v2.1 Metadata Validasi)",
          not f, f"tidak ada kolom: {', '.join(f)} - seed 20260707 & version v2.1 hanya tertulis di dokumen", f, "CRITICAL")

    # R38 artefak v2.1 wajib (struktur file di spec)
    base = os.path.dirname(os.path.abspath(SPEC_CSV))
    root = os.path.dirname(os.path.dirname(base))  # N:\HEALTHKATHON
    required = [
        (os.path.join(root, "Aegis-JKN", "data", "raw", "claims_300_v2.1.csv"), "data/raw/claims_300_v2.1.csv"),
        (os.path.join(root, "Aegis-JKN", "data", "raw", "edges_v2.1.json"), "data/raw/edges_v2.1.json"),
        (os.path.join(root, "Aegis-JKN", "data", "raw", "text_gt_v2.1.csv"), "data/raw/text_gt_v2.1.csv"),
        (os.path.join(root, "Aegis-JKN", "data", "raw", "leakage_blocklist.yaml"), "data/raw/leakage_blocklist.yaml"),
        (os.path.join(root, "Aegis-JKN", "data", "processed", "features_300.parquet"), "data/processed/features_300.parquet"),
        (os.path.join(root, "Aegis-JKN", "data", "processed", "graph_hetero.pt"), "data/processed/graph_hetero.pt"),
        (os.path.join(root, "Aegis-JKN", "data", "processed", "metadata.json"), "data/processed/metadata.json"),
        (os.path.join(root, "Aegis-JKN", "configs", "leakage.yaml"), "configs/leakage.yaml"),
        (os.path.join(root, "Aegis-JKN", "tests", "test_leakage.py"), "tests/test_leakage.py"),
    ]
    missing = [label for path, label in required if not os.path.exists(path)]
    check("R38 artefak wajib struktur file v2.1 tersedia di repo Aegis-JKN",
          not missing, f"hilang {len(missing)}/{len(required)}: " + ", ".join(missing), missing, "CRITICAL")

    # R39 generator dataset (skrip yang menghasilkan 300 baris) harus ada
    gen = []
    for cand in ("Aegis-JKN", "mechine-learning-deep-learning", "analysis"):
        for dirpath, dirnames, filenames in os.walk(os.path.join(root, cand)):
            dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git", "venv", "__pycache__", ".next")]
            for fn in filenames:
                if fn.endswith(".py"):
                    fp = os.path.join(dirpath, fn)
                    try:
                        txt = open(fp, encoding="utf-8", errors="ignore").read()
                    except OSError:
                        continue
                    if ("SYND-0" in txt or "KLM0" in txt) and ("seed" in txt or "random" in txt) and "generate" in txt.lower():
                        gen.append(os.path.relpath(fp, root))
    check("R39 generator dataset (skrip yang menghasilkan 300 baris) ada di repo",
          bool(gen), "tidak ditemukan skrip generator yang menghasilkan 300 baris; satu-satunya "
                     "np.random.seed(20260707) ada di mechine-learning-deep-learning/backend/src/data/pipeline.py:103 "
                     "(_generate_fallback_dataset) yang membuat 100 baris dummy, bukan 300 baris final", gen, "CRITICAL")

    # R40 checksum / metadata.json untuk artefak ekspor
    meta_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git", "venv", "__pycache__", ".next", "Notion-docs")]
        for fn in filenames:
            if fn.lower() in ("metadata.json", "checksum.txt", "checksums.txt", "sha256sums.txt", "manifest.json"):
                meta_files.append(os.path.relpath(os.path.join(dirpath, fn), root))
    check("R40 metadata.json / berkas checksum untuk artefak dataset (03-registry §8)",
          bool(meta_files), f"ditemukan: {meta_files if meta_files else 'tidak ada berkas metadata/checksum'}", [], "HIGH")

    return pref


# ==========================================================================
# 4. AUDIT NARASI vs KODE
# ==========================================================================
def narrative_audit(rows):
    uniq = collections.Counter(r["Narasi Rekam Medis"] for r in rows)
    low_uniq = {r["Narasi Rekam Medis"] for r in rows if r["Risiko"] == "low"}
    res = dict(
        total_rows=len(rows),
        unique_narasi=len(uniq),
        unique_narasi_low=len(low_uniq),
        unique_umpan_balik=len({r["Umpan Balik Pasien"] for r in rows}),
        unique_alasan=len({r["Alasan"] for r in rows}),
        unique_alasan_fraud=len({r["Alasan"] for r in rows if r["Risiko"] == "fraud"}),
        unique_alasan_low=len({r["Alasan"] for r in rows if r["Risiko"] == "low"}),
        unique_rujukan=len({r["Rujukan"] for r in rows}),
        unique_alasan_berobat=len({r["Alasan Berobat"] for r in rows}),
        top=uniq.most_common(10),
    )
    # narasi per dx
    per_dx = collections.defaultdict(set)
    for r in rows:
        per_dx[dx_code(r)].add(r["Narasi Rekam Medis"])
    res["narasi_per_dx"] = {k: len(v) for k, v in sorted(per_dx.items())}
    # angka pada narasi vs kolom
    numeric = collections.Counter()
    for r in rows:
        for m in re.finditer(r"\d+(?:[.,]\d+)?", r["Narasi Rekam Medis"]):
            numeric[m.group(0)] += 1
    res["angka_narasi"] = numeric.most_common(15)
    # narasi yang tidak pernah menyebut nilai kolom (LOS/biaya)
    res["narasi_tanpa_angka_kolom"] = sum(1 for r in rows if not re.search(r"\d", r["Narasi Rekam Medis"]))
    return res


# ==========================================================================
# 5. AUDIT KOLOM ALASAN
# ==========================================================================
def alasan_audit(rows):
    pref = collections.Counter()
    templates = collections.Counter()
    for r in rows:
        a = r["Alasan"].strip()
        if not a:
            pref["(KOSONG)"] += 1
            continue
        head = a.split(":")[0].strip()
        pref[head] += 1
        templates[re.sub(r"[\d.,]+", "N", a)] += 1
    # NB: substring "rasio" juga cocok dengan kata "rasional" -> pakai regex "rasio <angka>"
    with_ratio = [r for r in rows if re.search(r"rasio ([\d.,]+)", r["Alasan"])]
    verifiable = 0
    unver = []
    for r in with_ratio:
        m = re.search(r"rasio ([\d.,]+)", r["Alasan"])
        pr = proc_code(r)
        if m and pr in SPEC_TARIF:
            calc = round(biaya(r) / SPEC_TARIF[pr], 2)
            if abs(calc - float(m.group(1).replace(",", "."))) < 0.005:
                verifiable += 1
        else:
            unver.append(r["Name"])
    return dict(
        prefix_distribution=dict(pref),
        n_with_ratio=len(with_ratio),
        n_ratio_verifiable=verifiable,
        n_ratio_unverifiable=len(unver),
        ratio_unverifiable_ids=unver[:20],
        distinct_templates=len(templates),
        top_templates=templates.most_common(5),
    )


# ==========================================================================
# MAIN
# ==========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=SPEC_CSV)
    ap.add_argument("--json", default=SPEC_JSON)
    args = ap.parse_args()

    if not os.path.exists(args.csv):
        print(f"ERROR: CSV tidak ditemukan: {args.csv}", file=sys.stderr)
        return 2

    rows = load(args.csv)
    print(f"[07_gen] {len(rows)} baris dimuat dari {args.csv}")

    recon = reconcile(rows)
    synd, singles = audit_syndicate(rows)
    pref = clinical_checks(rows)
    nar = narrative_audit(rows)
    al = alasan_audit(rows)

    ok_recon = sum(1 for r in recon if r["verdict"] == "OK")
    bad_recon = sum(1 for r in recon if r["verdict"] == "SELISIH")
    info_recon = sum(1 for r in recon if r["verdict"] == "INFO")

    print(f"[07_gen] Reconciliation: {ok_recon} OK / {bad_recon} SELISIH / {info_recon} INFO")
    print(f"[07_gen] Checker: {len(PASSES)} lulus / {len(FAIL)} gagal")

    sev_count = collections.Counter(f["severity"] for f in FAIL)
    print(f"[07_gen] Gagal per severity: {dict(sev_count)}")

    result = dict(
        meta=dict(
            csv=args.csv,
            csv_sha256=sha256_file(args.csv),
            n_rows=len(rows),
            n_cols=len(rows[0]),
            audited_at=date.today().isoformat(),
            spec_sources=[
                "analysis/corpus/10-simulation-dataset.md",
                "analysis/corpus/07-dataset-v2-catalog.md",
                "analysis/corpus/03-dataset-registry.md",
            ],
            column_fingerprints={
                c: sha256_text("\n".join(r[c] for r in sorted(rows, key=lambda x: x["Name"])))
                for c in ("Name", "Biaya Rp", "Skor Fraud", "Alasan", "Narasi Rekam Medis", "Diagnosis ICD-10")
            },
        ),
        reconciliation=recon,
        syndicate_audit=synd,
        fraud_tunggal_audit=singles,
        checker=dict(passed=PASSES, failed=FAIL, severity_counts=dict(sev_count),
                     prefix_distribution=dict(pref)),
        narrative=nar,
        alasan=al,
    )
    os.makedirs(os.path.dirname(args.json), exist_ok=True)
    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"[07_gen] hasil ditulis: {args.json}")

    # Ringkasan ke stdout
    print("\n--- GAGAL ---")
    for f_ in FAIL:
        ids = ", ".join(str(x) for x in f_["failed"][:8]) + (" ..." if len(f_["failed"]) > 8 else "")
        print(f"  [{f_['severity']}] {f_['rule']} :: {f_['detail']} :: {ids}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    sys.exit(main())
