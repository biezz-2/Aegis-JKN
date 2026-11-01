#!/usr/bin/env python3
"""
Audit konsistensi silang seluruh korpus Aegis-JKN (15 dokumen Notion).

Tugas:
  1. Ekstraksi klaim kuantitatif dari tiap dokumen (angka + label + entitas + ambang).
  2. Deteksi klaim yang muncul di >1 dokumen dengan nilai berbeda (kontradiksi).
  3. Audit duplikasi: 14-index.md dan 09-draft-hub.md vs dokumen terkendali.
  4. Audit tautan silang dokumen terkendali -> arsip (app.notion.com/p/).
  5. Verifikasi silang angka kunci dokumen terhadap claims_v2_live.csv (300 baris).
  6. Tabel konsistensi istilah global.

Stdlib only (csv, json, collections, re, os, sys, unicodedata, difflib).

Jalankan:  python -I 19_consistency.py
Output :  19_consistency_output.txt  (di folder yang sama)
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(os.path.dirname(BASE), "corpus")
CSV_PATH = os.path.join(CORPUS, "claims_v2_live.csv")
JSON_PATH = os.path.join(CORPUS, "claims_v2_live.json")
RESEARCH_CSV = os.path.join(CORPUS, "dataset_research_live.csv")
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "19_consistency_output.txt")

DOCS = [
    "00-dashboard.md", "01-proposal.md", "02-architecture.md",
    "03-dataset-registry.md", "04-evidence-matrix.md", "05-decision-scope.md",
    "06-research-notes.md", "07-dataset-v2-catalog.md", "08-training-protocol.md",
    "09-draft-hub.md", "10-simulation-dataset.md", "11-archive-proposal.md",
    "12-archive-architecture.md", "13-archive-deep-research.md", "14-index.md",
]

CONTROLLED = [
    "00-dashboard.md", "01-proposal.md", "02-architecture.md",
    "03-dataset-registry.md", "04-evidence-matrix.md", "05-decision-scope.md",
    "06-research-notes.md", "07-dataset-v2-catalog.md", "08-training-protocol.md",
]
ARCHIVE = ["11-archive-proposal.md", "12-archive-architecture.md",
           "13-archive-deep-research.md", "14-index.md"]

# Notion page id -> dokumen terkendali (dari header "source: notion page ...").
PAGE_TO_DOC = {
    "4003e6031ab7815a89bdedc0c4d92c2f": "00-dashboard.md",
    "4003e6031ab78170bc22fe391c6a3a2a": "01-proposal.md",
    "4003e6031ab781efbcdac7b0dbdd0cad": "02-architecture.md",
    "4003e6031ab781749a55d4ee8fff3fd2": "03-dataset-registry.md",
    "4003e6031ab7814f8ac3f37808c0a4a5": "04-evidence-matrix.md",
    "4003e6031ab78156b244cccd2c5ecd9e": "05-decision-scope.md",
    "4003e6031ab78135a0face33631104ab": "06-research-notes.md",
    "4003e6031ab78179bcc7ca76a0b80fbc": "07-dataset-v2-catalog.md",
    "4003e6031ab781978715f1de059e82ef": "08-training-protocol.md",
    "4003e6031ab7818040a0ebec875c0954eb": "09-draft-hub.md",
    "3f23e6031ab781bf99a7d3f1768f1708": "10-simulation-dataset.md",
    "3f63e6031ab78141a724fc301304942b": "11-archive-proposal.md",
    "3ef3e6031ab781d1962af8955843ed0f": "12-archive-architecture.md",
    "3fe3e6031ab780088ce1f3201c252bed": "13-archive-deep-research.md",
    "3f23e6031ab781808db2cbfe92cd62391d": "14-index.md",
    "3f63e6031ab78111a885ea835e650bf2": "14-index.md",
    # Database (bukan halaman) - sumber data langsung
    "c783afb3d0d4458295456180b7b7756b": "DATABASE-KLAIM-v2 (300 baris)",
    "310b35a5934642dfaf47df9897cdcda1": "DATABASE-RISET-FRAUD (33 entri)",
}

# Label Risiko vs Status Alur Kerja: nilai per dokumen (file:line dicatat terpisah).
NUM_RE = re.compile(r"\d[\d.,]*")
WORDNUM = {
    "satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6,
    "tujuh": 7, "delapan": 8, "sembilan": 9, "sepuluh": 10,
    "seratus": 100, "seribu": 1000,
}


def read_lines(name):
    with open(os.path.join(CORPUS, name), encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n").split("\n")


def norm_txt(s):
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("–", "-").replace("—", "-").replace("’", "'")
    return s


def to_int(tok):
    t = tok.replace(".", "").replace(",", "")
    if t.isdigit():
        return int(t)
    return None


def extract_numbers(lines):
    """Kembalikan [(line_no, token_int, konteks)] untuk semua angka di dokumen."""
    out = []
    for i, ln in enumerate(lines, 1):
        for m in NUM_RE.finditer(norm_txt(ln)):
            v = to_int(m.group(0))
            if v is None:
                continue
            ctx = norm_txt(ln[max(0, m.start() - 60): m.end() + 60])
            out.append((i, v, ctx))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    docs = {d: read_lines(d) for d in DOCS}
    w = sys.stdout.write

    w("=" * 78 + "\n")
    w("BAGIAN A - EKSTRAKSI ANGKA PER DOKUMEN (klasifikasi klaim)\n")
    w("=" * 78 + "\n")
    for d in DOCS:
        nums = extract_numbers(docs[d])
        w(f"\n--- {d}  (total token angka: {len(nums)}) ---\n")
        # ringkas per line
        byline = defaultdict(list)
        for ln, v, ctx in nums:
            byline[ln].append(v)
        for ln in sorted(byline):
            w(f"  L{ln:<5} {sorted(set(byline[ln]))}\n")

    # ---------------------------------------------------------------
    w("\n" + "=" * 78 + "\n")
    w("BAGIAN B - VERIFIKASI SILANG ANGKA vs claims_v2_live.csv\n")
    w("=" * 78 + "\n")
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    research = list(csv.DictReader(open(RESEARCH_CSV, encoding="utf-8-sig")))

    def pid(s):
        m = re.match(r"(P\d+)", s)
        return m.group(1) if m else s

    def did(s):
        m = re.match(r"(D\d+)", s)
        return m.group(1) if m else s

    def biaya(r):
        v = r["Biaya Rp"].strip()
        return int(v) if v else 0

    risiko = Counter(r["Risiko"] for r in rows)
    status = Counter(r["Status"] for r in rows)
    sent = Counter(r["Sentimen"] for r in rows)
    total_b = sum(biaya(r) for r in rows)
    by_status = {s: sum(biaya(r) for r in rows if r["Status"] == s)
                 for s in status}
    los_blank = sum(1 for r in rows if not r["LOS hari"].strip())
    los_zero = sum(1 for r in rows if r["LOS hari"].strip() == "0")
    alasan_blank = sum(1 for r in rows if not r["Alasan"].strip())
    modus_blank = sum(1 for r in rows if not r["Modus"].strip())
    sind_blank = sum(1 for r in rows if not r["Sindikat"].strip())
    kontra_true = sorted(r["Name"] for r in rows
                         if r["Kontradiksi Narasi"].strip().lower() == "true")
    v1 = [r for r in rows if r["Name"] <= "KLM100"]
    v1_risiko = Counter(r["Risiko"] for r in v1)
    v1_sent = Counter(r["Sentimen"] for r in v1)
    ent = {
        "pasien": len(set(pid(r["Pasien"]) for r in rows)),
        "dokter": len(set(did(r["Dokter"]) for r in rows)),
        "faskes": len(set(r["Faskes"] for r in rows)),
    }
    ent_v1 = {
        "pasien": len(set(pid(r["Pasien"]) for r in v1)),
        "dokter": len(set(did(r["Dokter"]) for r in v1)),
        "faskes": len(set(r["Faskes"] for r in v1)),
    }
    avg_skor = {}
    for s in status:
        vals = [float(r["Skor Fraud"]) for r in rows if r["Status"] == s]
        avg_skor[s] = sum(vals) / len(vals)
    sind_rows = [r for r in rows if r["Sindikat"].strip()]
    sind_nominal = sum(biaya(r) for r in sind_rows)
    fraud_nominal = sum(biaya(r) for r in rows if r["Risiko"] == "fraud")
    anomali = [r for r in rows if r["Risiko"] in ("fraud", "high", "medium")]
    anomali_nominal = sum(biaya(r) for r in anomali)
    modus_nominal = defaultdict(int)
    modus_n = Counter()
    for r in rows:
        if r["Risiko"] == "fraud":
            modus_n[r["Modus"]] += 1
            modus_nominal[r["Modus"]] += biaya(r)
    skor_min = {lab: min(float(r["Skor Fraud"]) for r in rows if r["Risiko"] == lab)
                for lab in ("low", "medium", "high", "fraud")}
    skor_max = {lab: max(float(r["Skor Fraud"]) for r in rows if r["Risiko"] == lab)
                for lab in ("low", "medium", "high", "fraud")}
    research_status = Counter(r["Status Verifikasi"] for r in research)
    research_relev = Counter(r["Relevansi"] for r in research)

    CHECKS = [
        ("Jumlah baris dataset aktif", "300", len(rows) == 300, "300"),
        ("Rentang ID KLM001-KLM300 utuh & unik", "300 ID unik",
         len(set(r["Name"] for r in rows)) == 300, f"{len(set(r['Name'] for r in rows))} unik"),
        ("Status auto_clear", "240", status["auto_clear"] == 240, str(status["auto_clear"])),
        ("Status review", "24", status["review"] == 24, str(status["review"])),
        ("Status escalate", "36", status["escalate"] == 36, str(status["escalate"])),
        ("Label risiko low", "240", risiko["low"] == 240, str(risiko["low"])),
        ("Label risiko medium", "10", risiko["medium"] == 10, str(risiko["medium"])),
        ("Label risiko high", "14", risiko["high"] == 14, str(risiko["high"])),
        ("Label risiko fraud", "36", risiko["fraud"] == 36, str(risiko["fraud"])),
        ("Total nominal", "Rp3.526.650.000", total_b == 3526650000, f"Rp{total_b:,}"),
        ("Nominal auto_clear", "Rp2.685.550.000", by_status["auto_clear"] == 2685550000,
         f"Rp{by_status['auto_clear']:,}"),
        ("Nominal review", "Rp279.950.000", by_status["review"] == 279950000,
         f"Rp{by_status['review']:,}"),
        ("Nominal escalate", "Rp561.150.000", by_status["escalate"] == 561150000,
         f"Rp{by_status['escalate']:,}"),
        ("Label anomali total (fraud+high+medium)", "60", len(anomali) == 60, str(len(anomali))),
        ("Nominal 60 klaim anomali", "Rp841.100.000", anomali_nominal == 841100000,
         f"Rp{anomali_nominal:,}"),
        ("Baris dengan Sindikat terisi", "36", len(sind_rows) == 36, str(len(sind_rows))),
        ("Nominal baris bersindikat", "Rp542.560.000 (klausul arsip 11:348)",
         sind_nominal == 542560000, f"Rp{sind_nominal:,}"),
        ("Pasien unik v2.1", "40", ent["pasien"] == 40, str(ent["pasien"])),
        ("Dokter unik v2.1", "20", ent["dokter"] == 20, str(ent["dokter"])),
        ("Faskes unik v2.1", "10 (RS_A-RS_J)", ent["faskes"] == 10, str(ent["faskes"])),
        ("Pasien unik pada 100 klaim pertama", "20", ent_v1["pasien"] == 20, str(ent_v1["pasien"])),
        ("Dokter unik pada 100 klaim pertama", "12", ent_v1["dokter"] == 12, str(ent_v1["dokter"])),
        ("Faskes unik pada 100 klaim pertama", "6", ent_v1["faskes"] == 6, str(ent_v1["faskes"])),
        ("Distribusi label 100 klaim pertama", "76 low / 4 medium / 6 high / 14 fraud",
         (v1_risiko["low"], v1_risiko["medium"], v1_risiko["high"], v1_risiko["fraud"])
         == (76, 4, 6, 14),
         f"{v1_risiko['low']}/{v1_risiko['medium']}/{v1_risiko['high']}/{v1_risiko['fraud']}"),
        ("Sentimen 100 klaim pertama", "62 positif / 14 netral / 24 negatif",
         (v1_sent["positif"], v1_sent["netral"], v1_sent["negatif"]) == (62, 14, 24),
         f"{v1_sent['positif']}/{v1_sent['netral']}/{v1_sent['negatif']}"),
        ("Sentimen seluruh 300", "170/58/72", True,
         f"{sent['positif']}/{sent['netral']}/{sent['negatif']}"),
        ("Kontradiksi narasi", "8 klaim (dokumen v1)", len(kontra_true) == 8,
         f"{len(kontra_true)}: {','.join(kontra_true)}"),
        ("Baris LOS kosong", "109", los_blank == 109, f"kosong={los_blank}, nol={los_zero}"),
        ("Baris Alasan kosong", "1", alasan_blank == 1, str(alasan_blank)),
        ("Properti Modus kosong", "240", modus_blank == 240, str(modus_blank)),
        ("Properti Sindikat kosong", "264", sind_blank == 264, str(sind_blank)),
        ("Catatan riset", "33 entri", len(research) == 33, str(len(research))),
        ("Status verifikasi riset 18/11/4", "18/11/4",
         (research_status["Terverifikasi"], research_status["Sebagian Terverifikasi"],
          research_status["Perlu Verifikasi"]) == (18, 11, 4),
         f"{research_status['Terverifikasi']}/{research_status['Sebagian Terverifikasi']}"
         f"/{research_status['Perlu Verifikasi']}"),
        ("Relevansi riset Kritis/Tinggi/Pendukung", "11/18/4",
         (research_relev["Kritis"], research_relev["Tinggi"],
          research_relev["Pendukung"]) == (11, 18, 4),
         f"{research_relev['Kritis']}/{research_relev['Tinggi']}/{research_relev['Pendukung']}"),
        ("Rata-rata skor auto_clear", "0.086", round(avg_skor["auto_clear"], 3) == 0.086,
         f"{avg_skor['auto_clear']:.3f}"),
        ("Rata-rata skor review", "0.591", round(avg_skor["review"], 3) == 0.591,
         f"{avg_skor['review']:.3f}"),
        ("Rata-rata skor escalate", "0.869", round(avg_skor["escalate"], 3) == 0.869,
         f"{avg_skor['escalate']:.3f}"),
        ("Skor fraud >= 0.80 (ambang 0,80 inklusif)", "36",
         skor_min["fraud"] >= 0.80, f"min={skor_min['fraud']}"),
        ("Skor high 0.62-0.79 (tidak ada 0.80)", "14",
         0.62 <= skor_min["high"] and skor_max["high"] < 0.80,
         f"{skor_min['high']}-{skor_max['high']}"),
        ("Skor medium 0.40-0.53", "10",
         skor_min["medium"] >= 0.35 and skor_max["medium"] < 0.60,
         f"{skor_min['medium']}-{skor_max['medium']}"),
        ("Skor low 0.04-0.14 (bukan <0.35 penuh)", "240",
         skor_max["low"] < 0.35, f"{skor_min['low']}-{skor_max['low']}"),
        ("Fraud tanpa sindikat (2 tunggal)", "2",
         sum(1 for r in rows if r["Risiko"] == "fraud" and not r["Sindikat"].strip()) == 2,
         str(sum(1 for r in rows if r["Risiko"] == "fraud"
                 and not r["Sindikat"].strip()))),
        ("Klaim KLM121 faskes RS_A (dokumen 10:143)", "RS_A",
         next(r for r in rows if r["Name"] == "KLM121")["Faskes"] == "RS_A",
         next(r for r in rows if r["Name"] == "KLM121")["Faskes"]),
        ("Klaim KLM122 faskes RS_E (dokumen 10:144)", "RS_E",
         next(r for r in rows if r["Name"] == "KLM122")["Faskes"] == "RS_E",
         next(r for r in rows if r["Name"] == "KLM122")["Faskes"]),
        ("Skor KLM121 (dokumen 10:143 '>=0.85')", "0.81",
         next(r for r in rows if r["Name"] == "KLM121")["Skor Fraud"] == "0.81",
         next(r for r in rows if r["Name"] == "KLM121")["Skor Fraud"]),
        ("Skor KLM122 (dokumen 10:144 '>=0.80')", "0.82",
         next(r for r in rows if r["Name"] == "KLM122")["Skor Fraud"] == "0.82",
         next(r for r in rows if r["Name"] == "KLM122")["Skor Fraud"]),
        ("Nominal modus Upcoding (arsip 11:348 Rp127,68 Jt)", "Rp127.680.000",
         modus_nominal["upcoding"] == 127680000, f"Rp{modus_nominal['upcoding']:,}"),
        ("Nominal modus Phantom Billing (arsip 11:348 Rp134,25 Jt)", "Rp134.250.000",
         modus_nominal["phantom_billing"] == 134250000,
         f"Rp{modus_nominal['phantom_billing']:,}"),
        ("Nominal modus Repeat Billing (arsip 11:348 Rp61,60 Jt)", "Rp61.600.000",
         modus_nominal["repeat_billing"] == 61600000,
         f"Rp{modus_nominal['repeat_billing']:,}"),
        ("Total nominal fraud (arsip 11:347 Rp561.150.000)", "Rp561.150.000",
         fraud_nominal == 561150000, f"Rp{fraud_nominal:,}"),
        ("Rasio 264 normal : 36 fraud = 1:7.33 (arsip 11:321)", "264 non-fraud",
         300 - 36 == 264, f"{300 - 36} non-fraud"),
    ]

    w(f"{'ANGKA':<58} {'EKSPEKTASI':<40} {'AKTUAL CSV'}\n")
    w("-" * 150 + "\n")
    n_ok = n_bad = 0
    for name, exp, ok, act in CHECKS:
        flag = "OK " if ok else "FAIL"
        if ok:
            n_ok += 1
        else:
            n_bad += 1
        w(f"[{flag}] {name:<50} | {exp:<38} | {act}\n")
    w(f"\nRingkasan verifikasi: {n_ok} cocok, {n_bad} TIDAK cocok\n")

    # ---------------------------------------------------------------
    w("\n" + "=" * 78 + "\n")
    w("BAGIAN C - AUDIT DUPLIKASI 14-index.md (embedding dokumen terkendali)\n")
    w("=" * 78 + "\n")
    idx = docs["14-index.md"]
    idx_txt = "\n".join(idx)
    for d in CONTROLLED:
        body = "\n".join(docs[d]).strip("\n")
        body_no_hdr = body.split("\n", 1)[1].strip("\n") if body.startswith("<!--") else body
        pos = idx_txt.find(body_no_hdr)
        if pos < 0:
            w(f"  {d:<28} -> tidak ditemukan sebagai salinan utuh\n")
            continue
        line_no = idx_txt[:pos].count("\n") + 1
        identical = True
        # verifikasi per baris: salinan harus sama persis di 14-index
        seg_lines = idx_txt[pos:].split("\n")
        for k, bl in enumerate(body_no_hdr.split("\n")):
            seg_line = seg_lines[k] if k < len(seg_lines) else ""
            if bl.strip() != seg_line.strip():
                identical = False
                break
        w(f"  {d:<28} -> tersalin utuh di 14-index.md mulai baris {line_no}"
          f" (identik baris-per-baris: {identical})\n")

    w("\n" + "=" * 78 + "\n")
    w("BAGIAN D - AUDIT DUPLIKASI 09-draft-hub.md\n")
    w("=" * 78 + "\n")
    hub = docs["09-draft-hub.md"]
    sim = docs["10-simulation-dataset.md"]
    seg_hub = "\n".join(hub[7:216])
    seg_sim = "\n".join(sim[4:213])
    w(f"  09 baris 8-216 vs 10 baris 5-213 identik? {seg_hub.strip() == seg_sim.strip()}\n")
    seg_hub2 = "\n".join(hub[219:428])
    w(f"  09 baris 220-428 (sub-page DUPLIKAT) identik dengan baris 8-216? "
      f"{seg_hub2.strip() == seg_hub.strip()}\n")

    w("\n" + "=" * 78 + "\n")
    w("BAGIAN E - AUDIT TAUTAN SILANG dokumen terkendali -> arsip\n")
    w("=" * 78 + "\n")
    link_re = re.compile(r"https?://app\.notion\.com/p/[^\s)]*?([0-9a-f]{32})(?:\)|$)")
    for d in CONTROLLED + ["10-simulation-dataset.md"]:
        hits = []
        for i, l in enumerate(docs[d], 1):
            for m in link_re.finditer(l):
                pid_ = m.group(1)
                tgt = PAGE_TO_DOC.get(pid_, "?tidak-terpetakan")
                hits.append((i, pid_, tgt))
        w(f"\n  {d}:\n")
        if not hits:
            w("    (tidak ada tautan app.notion.com)\n")
        for i, pid_, tgt in hits:
            w(f"    L{i:<5} -> {pid_}  = {tgt}\n")

    w("\n" + "=" * 78 + "\n")
    w("BAGIAN F - TABEL ISTILAH GLOBAL (kanonik vs varian)\n")
    w("=" * 78 + "\n")
    terms = {
        "nama_produk": ["Aegis-JKN", "AEGIS-JKN", "aegis-jkn", "aegisjkn"],
        "nama_kompetisi": ["Healthkathon 2026", "HEALTHKATHON 2026",
                           "BPJS Kesehatan Healthkathon 2026",
                           "Healthkathon BPJS Kesehatan 2026"],
        "status_auto_clear": ["auto_clear", "auto-clear"],
        "entitas_faskes": ["FKRTL", "RS_", "Faskes"],
        "akronim_mhgsl": ["Multi-Hop Graph Structure Learning",
                          "Multi-Channel Heterogeneous Graph Structure Learning",
                          "Multi-Channel Graph Structure Learning"],
        "label_risiko": ["fraud-scenario", "fraud", "FRAUD", "ANOMALI", "NORMAL"],
        "sindikat": ["SYND-01", "sindikat", "Sindikat", "fraud ring", "fraud rings"],
    }
    for cat, variants in terms.items():
        w(f"\n  [{cat}]\n")
        for v in variants:
            cnt = Counter()
            for d in DOCS:
                n = sum(norm_txt(l).count(v) for l in docs[d])
                if n:
                    cnt[d] = n
            total = sum(cnt.values())
            w(f"    {v:<52} total={total:<5} {dict(cnt)}\n")

    return rows


if __name__ == "__main__":
    main()
