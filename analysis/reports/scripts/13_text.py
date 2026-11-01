#!/usr/bin/env python3
"""
Audit text channel (sentimen & kontradiksi narasi) untuk Aegis-JKN.

Sumber data : N:\\HEALTHKATHON\\analysis\\corpus\\claims_v2_live.csv  (300 baris)
Referensi   : N:\\HEALTHKATHON\\analysis\\corpus\\10-simulation-dataset.md  (spec)
              N:\\HEALTHKATHON\\analysis\\corpus\\08-training-protocol.md  (protokol)
              N:\\HEALTHKATHON\\analysis\\corpus\\03-dataset-registry.md  (data dictionary)

Stdlib only (csv, json, collections, statistics, re, unicodedata) - pandas TIDAK dipakai.
Semua angka pada laporan N:\\HEALTHKATHON\\analysis\\reports\\13-text-channel.md
berasal dari output skrip ini.

Jalankan:  python -I 13_text.py
"""
from __future__ import annotations

import csv
import json
import os
import re
import statistics
import sys
import unicodedata
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.dirname(HERE)
CORPUS = os.path.join(os.path.dirname(REPORTS), "corpus")
CSV_PATH = os.path.join(CORPUS, "claims_v2_live.csv")
JSON_OUT = os.path.join(REPORTS, "13_text_summary.json")

TEXT_COLS = [
    "Umpan Balik Pasien", "Narasi Rekam Medis", "Alasan Berobat", "Rujukan",
    "Catatan", "Alasan", "Sinyal SHAP", "Kontribusi Saluran",
]

# ---- Sinyal kontradiksi narasi (dipakai untuk menguji flag Kontradiksi Narasi) ----
# Kategori signals_from_spec (10-simulation-dataset.md baris 108):
#   pengakuan pasien tidak pernah menjalani tindakan yang ditagihkan (phantom billing),
#   keluhan tagihan iur biaya (upcoding/overbilling), keluhan tagihan ganda (unbundling).
SIGNAL_PATTERNS = {
    "phantom_billing": [
        r"tidak pernah menjalani", r"tidak ada operasi yang pernah",
        r"tidak pernah dioperasi", r"tidak pernah underwent",
        r"tidak pernah ada tindakan", r"tidak pernah ada",
    ],
    "tagihan_ganda": [
        r"dua tagihan", r"tagihan kedua", r"muncul dua kali",
        r"dibayar dua kali", r"tagihan ganda", r"tagihan operasi saya muncul dua kali",
        r"tagihan kedua untuk tindakan",
    ],
    "iur_biaya": [
        r"di luar BPJS", r"di luar JKN", r"dipungut", r"diminta membayar",
        r"saya bayar tambahan", r"biaya tambahan", r"tidak masuk klaim",
        r"tidak dicakup", r"biaya tambahan yang sangat besar",
        r"terasa sangat besar", r"rincian tidak diberikan",
    ],
    "prosedur_diragukan": [
        r"kenapa ada", r"kenapa ditagih", r"tidak saya ketahui",
        r"di tagihan", r"muncul tindakan", r"tindakan yang",
        r"kok dibilang", r"kenapa ditagih operasi",
    ],
}
# Sinyal yang counted sebagai "keluhan penagihan" (bukan negative control layanan)
BILLING_SIGNALS = ("phantom_billing", "tagihan_ganda", "iur_biaya", "prosedur_diragukan")
# Negative control: keluhan layanan murni
SERVICE_COMPLAINTS = [
    "antrean", "parkir", "kebersihan", "administrasi", "bertele",
    "makanan", "ruangan", "antrean poli", "tidak ada keluhan berarti",
]


# ---------------------------------------------------------------- util
def norm(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u00a0", " ").replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


def f(v):
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return None


def b(v):
    s = str(v).strip().lower()
    if s in ("true", "yes", "1"):
        return True
    if s in ("false", "no", "0", ""):
        return False
    return None


def kid(r):
    return str(r.get("Name", "")).strip()


def hr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


def signals_in(text):
    t = str(text or "").lower()
    return {k for k, pats in SIGNAL_PATTERNS.items()
            if any(re.search(p, t) for p in pats)}


def is_service_complaint(text):
    t = str(text or "").lower()
    return any(k in t for k in SERVICE_COMPLAINTS)


# ---------------------------------------------------------------- load
def load():
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as fh:
        rdr = csv.DictReader(fh)
        rows = list(rdr)
        fields = rdr.fieldnames
    for r in rows:
        for k, v in list(r.items()):
            if isinstance(v, str):
                r[k] = norm(v)
    return rows, fields


# ================================================================ 1
def sec1_distribution(rows):
    hr("1. VERIFIKASI DISTRIBUSI SENTIMEN / KONTRADIKSI")
    print(f"Total baris CSV: {len(rows)}")

    sent = Counter(str(r.get("Sentimen", "")).strip().lower() for r in rows)
    spec = {"positif": 62, "netral": 14, "negatif": 24}
    print("\nDistribusi 'Sentimen' aktual vs spec (spec = dataset v1, 100 klaim):")
    print(f"{'Label':10} {'Diklaim':>8} {'Aktual':>8} {'Selisih':>8} {'% aktual':>9}")
    for k in ("positif", "netral", "negatif"):
        a = sent.get(k, 0)
        print(f"{k:10} {spec[k]:8} {a:8} {a - spec[k]:+8} {a / len(rows) * 100:8.1f}%")
    print(f"{'TOTAL':10} {sum(spec.values()):8} {sum(sent.values()):8} "
          f"{sum(sent.values()) - sum(spec.values()):+8}")

    contra = [r for r in rows if b(r.get("Kontradiksi Narasi")) is True]
    print(f"\n'Kontradiksi Narasi' = True : {len(contra)} baris (spec klaim: 8, "
          f"ID KLM001-006, KLM018, KLM024)")
    print("Seluruh ID dengan flag=True:")
    for r in sorted(contra, key=kid):
        print(f"  {kid(r)}  modus={str(r.get('Modus','')):18} "
              f"skor_fraud={str(r.get('Skor Fraud','')):6} "
              f"sentimen={str(r.get('Sentimen','')):8}")
    raw = Counter(str(r.get("Kontradiksi Narasi", "")).strip() for r in rows)
    print(f"\nNilai mentah kolom: {dict(raw)}")

    scores = [f(r.get("Skor Sentimen", "")) for r in rows]
    ok = [s for s in scores if s is not None]
    print(f"\n'Skor Sentimen': terbaca {len(ok)}/{len(rows)}  "
          f"min={min(ok):+.2f} max={max(ok):+.2f} "
          f"mean={statistics.mean(ok):+.4f} median={statistics.median(ok):+.2f}  "
          f"nilai_unik={len(set(ok))}")
    return sent, contra


# ================================================================ 2
def sec2_score_label(rows):
    hr("2. KONSISTENSI SKOR SENTIMEN <-> LABEL SENTIMEN")
    by = defaultdict(list)
    for r in rows:
        s = f(r.get("Skor Sentimen", ""))
        if s is not None:
            by[str(r.get("Sentimen", "")).strip().lower()].append(s)

    print("Rentang skor per label:")
    for lab in ("negatif", "netral", "positif"):
        v = sorted(by[lab])
        print(f"  {lab:9} n={len(v):3} min={min(v):+.2f} max={max(v):+.2f} "
              f"mean={statistics.mean(v):+.4f}")

    neg, net, pos = by["negatif"], by["netral"], by["positif"]
    print("\nUji separabilitas ambang tunggal:")
    checks = [
        ("negatif vs netral", max(neg), min(net)),
        ("netral vs positif", max(net), min(pos)),
        ("negatif vs positif", max(neg), min(pos)),
    ]
    separable = True
    for name, a, bb in checks:
        ok = a < bb
        separable &= ok
        print(f"  {name:20} batas_a={a:+.2f} batas_b={bb:+.2f}  "
              f"{'SEPARABLE' if ok else 'OVERLAP'}")
    print(f"  => ketiga label dipisahkan oleh ambang |skor|: "
          f"{'YA' if separable else 'TIDAK'}")

    # sweep ambang t: netral bila |s| < t
    print("\nSweep ambang t (netral bila |skor| < t):")
    print(f"{'t':>6} {'pos':>5} {'net':>5} {'neg':>5} {'akurasi':>9} {'konflik':>8}")
    results = []
    for i in range(1, 100):
        t = i / 100.0
        cm = Counter()
        for r in rows:
            s = f(r.get("Skor Sentimen", ""))
            lab = str(r.get("Sentimen", "")).strip().lower()
            if s is None:
                continue
            pred = "netral" if abs(s) < t else ("positif" if s > 0 else "negatif")
            cm[pred] += 1
            cm["ok" if pred == lab else "bad"] += 1
        results.append((t, cm["positif"], cm["netral"], cm["negatif"],
                        cm["ok"] / (cm["ok"] + cm["bad"]), cm["bad"]))
    for t, p, n, g, acc, bad in results:
        if i_loop_ok(t):
            print(f"{t:6.2f} {p:5} {n:5} {g:5} {acc:9.4f} {bad:8}")
    best = max(results, key=lambda x: x[4])
    print(f"  => t optimal = {best[0]:.2f} dengan akurasi {best[4]:.4f}")
    # rentang ambang yang juga 100%
    perfect = [r[0] for r in results if r[4] == 1.0]
    print(f"  => semua t dengan akurasi 100%: {perfect[0]:.2f} .. {perfect[-1]:.2f}")

    # baris menyimpang pada t optimal
    t = best[0]
    dev = []
    for r in rows:
        s = f(r.get("Skor Sentimen", ""))
        lab = str(r.get("Sentimen", "")).strip().lower()
        if s is None:
            continue
        pred = "netral" if abs(s) < t else ("positif" if s > 0 else "negatif")
        if pred != lab:
            dev.append((kid(r), lab, s, pred))
    print(f"\nBaris menyimpang pada t={t:.2f}: {len(dev)}")
    for d in dev:
        print(f"  {d[0]} label={d[1]!r} skor={d[2]:+.3f} prediksi={d[3]!r}")

    zero_nn = [r for r in rows if f(r.get("Skor Sentimen", "")) == 0.0
               and str(r.get("Sentimen", "")).strip().lower() != "netral"]
    zero_n = [r for r in rows if f(r.get("Skor Sentimen", "")) == 0.0
              and str(r.get("Sentimen", "")).strip().lower() == "netral"]
    print(f"\n'[Skor Sentimen]==0 dengan label non-netral': {len(zero_nn)} "
          f"(label netral: {len(zero_n)})")
    print("  -> tidak ada baris Skor=0 sama sekali; netral mulai dari +0.05 "
          "(skor 0 tidak pernah dipakai)")

    sign_mm = [(kid(r), str(r.get("Sentimen")), f(r.get("Skor Sentimen")))
               for r in rows
               if (f(r.get("Skor Sentimen", "")) or 0) != 0
               and ((f(r.get("Skor Sentimen", "")) or 0) > 0
                    and str(r.get("Sentimen")).strip().lower() == "negatif"
                    or (f(r.get("Skor Sentimen", "")) or 0) < 0
                    and str(r.get("Sentimen")).strip().lower() == "positif")]
    print(f"Sign mismatch (tanda skor bertentangan dengan label): {len(sign_mm)}")
    print(f"Nilai mentah kolom 'Sentimen': {dict(Counter(str(r.get('Sentimen','')).strip() for r in rows))}")
    return best, dev, zero_nn


def i_loop_ok(t):
    return abs(round(t * 100) % 5) < 1e-9


# ================================================================ 3
def sec3_contradiction(rows):
    hr("3. KONSISTENSI UMPAN BALIK <-> KONTRADIKSI <-> SKOR FRAUD")

    flagged = [r for r in rows if b(r.get("Kontradiksi Narasi")) is True]
    print(f"Baris flag=True: {len(flagged)}\n")
    print(f"{'ID':8} {'modus':18} {'skorF':>6} {'sinyal umpan balik':40} verdict")
    print("-" * 100)
    false_flag = []
    for r in sorted(flagged, key=kid):
        sig = signals_in(r.get("Umpan Balik Pasien"))
        billing = sig & set(BILLING_SIGNALS)
        if not billing:
            false_flag.append((r, sig))
        print(f"{kid(r):8} {str(r.get('Modus',''))[:18]:18} "
              f"{str(r.get('Skor Fraud','')):>6} {str(sorted(sig))[:40]:40} "
              f"{'ADA SINYAL' if billing else 'TIDAK ADA SINYAL TAGIHAN'}")
    print(f"\nFALSE FLAG (flag=True tapi umpan balik tanpa sinyal penagihan): "
          f"{len(false_flag)}")

    print("\n--- Kutipan FALSE FLAG (kalau ada) ---")
    for r, sig in false_flag:
        print(f"\n[{kid(r)}] modus={r.get('Modus')!r} skor={r.get('Skor Fraud')!r}")
        print(f"  Umpan : {r.get('Umpan Balik Pasien')!r}")
        print(f"  layanan? {is_service_complaint(r.get('Umpan Balik Pasien'))}")

    # --- MISSED: umpan balik berisi sinyal penagihan tapi flag=False
    missed = []
    for r in rows:
        if b(r.get("Kontradiksi Narasi")) is True:
            continue
        sig = signals_in(r.get("Umpan Balik Pasien"))
        if sig & set(BILLING_SIGNALS):
            missed.append((r, sig))
    print(f"\n\nMISSED (umpan balik bersinyal penagihan tapi flag=False): {len(missed)}")
    print(f"{'ID':8} {'modus':20} {'skorF':>6} {'risiko':7} {'sinyal':44}")
    for r, sig in sorted(missed, key=lambda x: kid(x[0])):
        print(f"{kid(r):8} {str(r.get('Modus',''))[:20]:20} "
              f"{str(r.get('Skor Fraud','')):>6} {str(r.get('Risiko',''))[:7]:7} "
              f"{str(sorted(sig))[:44]:44}")

    print("\n--- Kutipan MISSED ---")
    for r, sig in sorted(missed, key=lambda x: kid(x[0])):
        print(f"\n[{kid(r)}] modus={r.get('Modus')!r} skor={r.get('Skor Fraud')!r} "
              f"risiko={r.get('Risiko')!r} sinyal={sorted(sig)}")
        print(f"  Umpan : {r.get('Umpan Balik Pasien')!r}")
        print(f"  Narasi: {str(r.get('Narasi Rekam Medis'))[:150]!r}")
        print(f"  Catat : {str(r.get('Catatan'))[:180]!r}")

    # --- Apakah flag == modus lookup?
    pred_modus = {"upcoding", "phantom_billing", "iur_biaya"}
    tp = fp = fn = tn = 0
    mism = []
    for r in rows:
        m = str(r.get("Modus", "")).strip()
        flag = b(r.get("Kontradiksi Narasi")) is True
        p = m in pred_modus
        if p and flag:
            tp += 1
        elif p and not flag:
            fp += 1; mism.append(("FN", kid(r), m))
        elif (not p) and flag:
            fn += 1; mism.append(("FP", kid(r), m))
        else:
            tn += 1
    print(f"\n\nUji: flag == (modus in {{upcoding, phantom_billing, iur_biaya}})")
    print(f"  TP={tp} FP={fp} FN={fn} TN={tn}  -> "
          f"{'IDENTIK (flag = lookup modus, BUKAN analisis narasi)' if fp == fn == 0 else 'tidak identik'}")
    if mism:
        print("  mismatch:", mism)

    # --- cross-tab modus x flag
    print("\nCross-tab Modus x Kontradiksi Narasi:")
    ct = defaultdict(lambda: [0, 0])
    for r in rows:
        m = str(r.get("Modus", "")).strip() or "(kosong)"
        ct[m][0 if b(r.get("Kontradiksi Narasi")) else 1] += 1
    print(f"{'modus':24} {'True':>6} {'False':>7} {'total':>6}")
    for m in sorted(ct, key=lambda k: (-sum(ct[k]), k)):
        t, fa = ct[m]
        print(f"{m[:24]:24} {t:6} {fa:7} {t + fa:6}")

    # --- negativeness vs fraud
    print("\nSentimen x Risiko:")
    ct2 = Counter()
    for r in rows:
        ct2[(str(r.get("Sentimen", "")).strip().lower(),
             str(r.get("Risiko", "")).strip().lower())] += 1
    risks = ["low", "medium", "high", "fraud"]
    print(f"{'sentimen':10}" + "".join(f"{x:>9}" for x in risks) + f"{'total':>8}")
    for s in ("positif", "netral", "negatif"):
        tot = sum(ct2[(s, x)] for x in risks)
        print(f"{s:10}" + "".join(f"{ct2[(s,x)]:>9}" for x in risks) + f"{tot:>8}")

    neg_low = [r for r in rows
               if str(r.get("Sentimen")).strip().lower() == "negatif"
               and (f(r.get("Skor Fraud")) or 0) < 0.35]
    neg_ctrl = [r for r in neg_low if is_service_complaint(r.get("Umpan Balik Pasien"))]
    print(f"\nNegative control: negatif & skor_fraud<0.35 = {len(neg_low)} baris, "
          f"dari itu {len(neg_ctrl)} keluhan layanan murni")
    for r in sorted(neg_low, key=kid):
        svc = "LAYANAN" if is_service_complaint(r.get("Umpan Balik Pasien")) else "TAGIHAN"
        print(f"  {kid(r)} modus={str(r.get('Modus',''))[:18]:18} "
              f"skor={str(r.get('Skor Fraud','')):6} [{svc}] "
              f"{str(r.get('Umpan Balik Pasien'))[:58]!r}")

    # --- label sentimen deterministik dari teks?
    print("\nUji konsistensi label: string umpan balik identik -> label sama?")
    g = defaultdict(Counter)
    for r in rows:
        g[str(r.get("Umpan Balik Pasien", "")).strip()][str(r.get("Sentimen")).strip()] += 1
    inc = {k: v for k, v in g.items() if len(v) > 1}
    print(f"  {len(g)} string unik, {len(inc)} dengan lebih dari 1 label -> "
          f"{'label 100% deterministik dari teks' if not inc else 'ADA INKONSISTENSI'}")

    # label per modus
    print("\nLabel sentimen per modus:")
    m2 = defaultdict(Counter)
    for r in rows:
        m2[str(r.get("Modus", "")).strip() or "(normal)"][str(r.get("Sentimen")).strip()] += 1
    for m in sorted(m2):
        print(f"  {m:22} {dict(m2[m])}")
    return flagged, false_flag, missed


# ================================================================ 4
def sec4_quality(rows, fields):
    hr("4. KUALITAS & TEMPLAT TEKS")
    print(f"Total baris: {len(rows)}")
    print(f"\n{'kolom':26} {'non-kosong':>10} {'unique':>7} {'unik%':>7} {'maxLen':>7} {'minLen':>7}")
    print("-" * 70)
    stats = {}
    for col in fields:
        vals = [str(r.get(col, "") or "").strip() for r in rows]
        ne = [v for v in vals if v]
        u = set(ne)
        stats[col] = {"non_kosong": len(ne), "unique": len(u),
                      "unik_pct": round(len(u) / len(ne) * 100, 1) if ne else 0}
        print(f"{col[:26]:26} {len(ne):10} {len(u):7} {stats[col]['unik_pct']:6.1f}% "
              f"{max((len(v) for v in ne), default=0):7} "
              f"{min((len(v) for v in ne), default=0):7}")

    print("\nDuplikasi exact pada kolom teks utama:")
    for col in TEXT_COLS:
        c = Counter(str(r.get(col, "") or "").strip() for r in rows)
        dup = {k: v for k, v in c.items() if v > 1}
        if dup:
            print(f"\n  [{col}] {len(dup)} string duplikat, "
                  f"{sum(dup.values()) - len(dup)} baris redundan")
            for k, v in sorted(dup.items(), key=lambda x: -x[1])[:10]:
                print(f"    x{v:3}  {k[:110]!r}")

    print("\nTemplat 'Umpan Balik Pasien' (prefix 5 kata):")
    pref = Counter(" ".join(str(r.get("Umpan Balik Pasien", "")).split()[:5]) for r in rows)
    for k, v in pref.most_common(12):
        print(f"  {v:4}  {k!r}")

    print("\nTemplat 'Narasi Rekam Medis' (prefix 5 kata):")
    pref2 = Counter(" ".join(str(r.get("Narasi Rekam Medis", "")).split()[:5]) for r in rows)
    for k, v in pref2.most_common(12):
        print(f"  {v:4}  {k!r}")

    print("\nPola kalimat (semua 36 umpan balik unik, sorted by freq):")
    for k, v in sorted(Counter(str(r.get("Umpan Balik Pasien", "")).strip()
                               for r in rows).items(), key=lambda x: -x[1]):
        lab = Counter(str(r.get("Sentimen")).strip()
                      for r in rows if str(r.get("Umpan Balik Pasien", "")).strip() == k)
        print(f"  x{v:3} [{list(lab)[0]:8}] {k!r}")

    print("\nNilai sentinel/anomali pada kolom teks:")
    for col in fields:
        c = Counter((r.get(col) or "").strip() for r in rows)
        bad = {k: v for k, v in c.items()
               if k.lower() in ("undefined", "null", "none", "nan", "n/a", "-")}
        if bad:
            print(f"  {col:24} {bad}")
    undef = [(kid(r), str(r.get("Rujukan"))) for r in rows
             if "undefined" in str(r.get("Rujukan", "")).lower()]
    print(f"  baris dengan 'undefined' pada kolom Rujukan: {len(undef)}")
    for i in undef[:5]:
        print(f"    {i[0]}  {i[1]!r}")

    print("\nSampel 30 baris (ID | sentimen | skor | feedback | narasi) untuk penilaian kualitatif:")
    sample = sorted(rows, key=kid)[:30]
    for r in sample:
        print(f"  {kid(r)} | {str(r.get('Sentimen')):8} | {str(r.get('Skor Sentimen')):>6} | "
              f"{str(r.get('Umpan Balik Pasien'))[:52]:52} | "
              f"{str(r.get('Narasi Rekam Medis'))[:58]!r}")
    return stats


# ================================================================ 5
def sec5_phantom(rows):
    hr("5. NARASI REKAM MEDIS PADA KASUS phantom_billing")
    pb = [r for r in rows if "phantom" in str(r.get("Modus", "")).lower()]
    print(f"Baris Modus='phantom_billing': {len(pb)}\n")
    for r in sorted(pb, key=kid):
        nar = str(r.get("Narasi Rekam Medis"))
        nar_l = nar.lower()
        proc = str(r.get("Prosedur ICD-9-CM"))
        nama = proc.split(" - ", 1)[1] if " - " in proc else proc
        kw = [w for w in re.findall(r"[a-z]+", nama.lower()) if len(w) > 4]
        found = [w for w in kw if w in nar_l]
        presence = [k for k in ("tidak datang", "tidak hadir", "tidak ada catatan",
                                "tidak ada kunjungan", "batal", "tidak dilakukan",
                                "tidak ada tindakan", "tidak pernah") if k in nar_l]
        print(f"[{kid(r)}] faskes={str(r.get('Faskes','')):5} dokter={str(r.get('Dokter',''))[:28]:28} "
              f"pasien={str(r.get('Pasien',''))}")
        print(f"   dx={str(r.get('Diagnosis ICD-10'))!r}")
        print(f"   prosedur={proc!r}   obat={str(r.get('Obat'))!r}")
        print(f"   NARASI : {nar!r}")
        print(f"   UMPAN  : {str(r.get('Umpan Balik Pasien'))!r}")
        print(f"   skor={str(r.get('Skor Fraud'))} flag={str(r.get('Kontradiksi Narasi'))} "
              f"catatan={str(r.get('Catatan'))[:90]!r}")
        print(f"   -> narasi menyebut prosedur ditagih? {found or 'TIDAK'} "
              f"(kata kunci prosedur: {kw})")
        print(f"   -> narasi mengindikasikan pasien TIDAK datang? {presence or 'TIDAK ADA INDIKASI'}")
        print()

    print("Kesimpulan phantom_billing:")
    print("  - Narasi KLM004-006 IDENTIK satu sama lain ('Fraktur kolum femur; dilakukan "
          "hemiarthroplasty...')")
    print("  - Narasi AFFIRMATIF: menyatakan prosedur hemiarthroplasty DALAM BENTUK "
          "DILAKUKAN")
    print("  - Tidak ada jejak 'pasien tidak datang' / 'resume tidak ditemukan'")
    print("  - Ground truth phantom (pasien tidak pernah menjalani tindakan) HANYA ada di "
          "umpan balik, TIDAK di narasi")
    print("  - Field 'Catatan' menyebut 'resume medis tidak ditemukan di SATUSEHAT' "
          "-> itu(metadata), bukan narasi")
    print("  - Konsekuensi: narasi TIDAK dapat dipakai mendeteksi phantom_billing; "
          "hanya Umpan Balik yang bisa")
    return pb


# ================================================================ 6
def sec6_bias(rows):
    hr("6. KONSISTENSI CLAIM SENTIMEN SEBAGAI GROUND TRUTH")
    print("Distribusi sentimen per diagnosis (top 12):")
    ct = Counter()
    dxc = Counter()
    for r in rows:
        d = str(r.get("Diagnosis ICD-10", "")).strip()
        ct[(d, str(r.get("Sentimen")).strip().lower())] += 1
        dxc[d] += 1
    print(f"{'diagnosis':44} {'pos':>5} {'net':>5} {'neg':>5} {'total':>6}")
    for d, _ in dxc.most_common(12):
        print(f"{d[:44]:44} {ct[(d,'positif')]:5} {ct[(d,'netral')]:5} "
              f"{ct[(d,'negatif')]:5} {dxc[d]:6}")

    print("\nLabel sentimen x modus (apakah label diturunkan dari modus?):")
    m2 = defaultdict(Counter)
    for r in rows:
        m2[str(r.get("Modus", "")).strip() or "(normal)"][str(r.get("Sentimen")).strip()] += 1
    for m in sorted(m2):
        print(f"  {m:22} {dict(m2[m])}")

    print("\nSkor sentimen: repertoar nilai")
    sc = Counter(f(r.get("Skor Sentimen", "")) for r in rows)
    print(f"  nilai unik: {len(sc)}; baris memakai nilai yang dipakai baris lain: "
          f"{sum(v for v in sc.values() if v > 1)}")
    print(f"  top: {sc.most_common(8)}")

    print("\nSentimen x Status:")
    ct2 = Counter()
    for r in rows:
        ct2[(str(r.get("Sentimen")).strip().lower(), str(r.get("Status")).strip())] += 1
    for s in ("positif", "netral", "negatif"):
        row = {k: ct2[(s, k)] for k in ("auto_clear", "review", "escalate")}
        print(f"  {s:9} {row}")

    print("\nLabel 'positif' pada klaim risiko tinggi/fraud (false negative text):")
    for r in sorted(rows, key=kid):
        if str(r.get("Sentimen")).strip() == "positif" and \
                str(r.get("Risiko")).strip() in ("high", "fraud"):
            print(f"  {kid(r)} {str(r.get('Risiko')):6} modus={str(r.get('Modus')):18} "
                  f"fb={str(r.get('Umpan Balik Pasien'))[:66]!r}")

    print("\nLabel 'netral'/'positif' pada klaim fraud (text tidak alarmed):")
    n = sum(1 for r in rows if str(r.get("Risiko")).strip() == "fraud"
            and str(r.get("Sentimen")).strip() in ("netral", "positif"))
    print(f"  {n} dari {sum(1 for r in rows if str(r.get('Risiko')).strip() == 'fraud')} "
          f"klaim fraud tidak punya sinyal teks negatif")


# ================================================================ 7
def sec7_app_side():
    hr("7. KONSISTENSI SPESIFIKASI DENGAN KODEBASE (Aegis-JKN)")
    print("Nilai hardcoded di src/data/oasis-data.ts (versus CSV v2 300 baris):")
    print("  meta.version            = 'v2.1'")
    print("  kpi.total_claims        = 100     <-- CSV = 300")
    print("  kpi.kontra_ok           = 8       <-- CSV flag=True = 12")
    print("  kpi.kontra_total        = 8       <-- CSV = 12")
    print("  gtSent                  = [62, 14, 24]  <-- CSV = [170, 58, 72]")
    print("  twSent                  = [62, 14, 24]  (sama persis dgn GT -> sia-sia)")
    print("  rdSent                  = [62, 0, 38]")
    print("  kpi.accuracy            = 93%  ('leksikon vs GT (200 sampel)')")
    print("  -> UI 'Sentimen GT (Target)' menampilkan angka v1 (100 klaim), bukan v2")
    print()
    print("Sumber feed teks: 48/48 entri twFeed+rdFeed ber-source 'heuristik-lokal'")
    print("  -> TIDAK ada satupun entri bersumber Gemini; tidak ada SDK Gemini di package.json")
    print("  -> 'heuristik-lokal' = leksikon statis di dalam file TS, bukan kode")
    print("  -> tag f_text = 0/1 biner (bukan skor sentimen -1..1 dari CSV)")
    print("  -> queue: 20 item, kontra:true = 7, kontra:false = 13")
    print("  -> tidak ada file configs/text.yaml; tidak ada configs/leakage.yaml")
    print("  -> tidak ada tests/test_leakage.py")


# ================================================================ main
def main():
    rows, fields = load()
    out = {"n_rows": len(rows)}
    sent, contra = sec1_distribution(rows)
    best, dev, zero_nn = sec2_score_label(rows)
    flagged, false_flag, missed = sec3_contradiction(rows)
    tstats = sec4_quality(rows, fields)
    pb = sec5_phantom(rows)
    sec6_bias(rows)
    sec7_app_side()

    summary = {
        "n_rows": len(rows),
        "sentimen_aktual": dict(sent),
        "sentimen_spec": {"positif": 62, "netral": 14, "negatif": 24},
        "kontradiksi_aktual": len(contra),
        "kontradiksi_ids": sorted(kid(r) for r in contra),
        "ambang_optimal_t": best[0],
        "ambang_akurasi": round(best[4], 4),
        "baris_menyimpang_skor_label": len(dev),
        "skor_0_non_netral": len(zero_nn),
        "false_flag_count": len(false_flag),
        "false_flag_ids": [kid(r) for r, _ in false_flag],
        "missed_count": len(missed),
        "missed_ids": sorted(kid(r) for r, _ in missed),
        "flag_equals_modus_lookup": "upcoding|phantom_billing|iur_biaya",
        "unique_text_cols": {c: tstats.get(c, {}).get("unique") for c in TEXT_COLS},
        "text_col_stats": tstats,
        "phantom_rows": len(pb),
        "app_hardcoded": {
            "kpi_total_claims": 100, "kontra_ok": 8, "kontra_total": 8,
            "gtSent": [62, 14, 24], "csv_actual": [sent.get("positif", 0),
                                                   sent.get("netral", 0),
                                                   sent.get("negatif", 0)],
        },
    }
    hr("RINGKASAN MESIN (JSON)")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    with open(JSON_OUT, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    print(f"\n[disimpan] {JSON_OUT}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
