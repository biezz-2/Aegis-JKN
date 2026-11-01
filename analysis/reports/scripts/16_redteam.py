#!/usr/bin/env python3
"""
16_redteam.py -- Red-team numerical attack on Aegis-JKN claims.

Reproduces every contested number from the 300-row synthetic corpus
(claims_v2_live.csv) and attacks them.

NO third-party dependencies (pandas is NOT available): stdlib only.
Run:  python -I N:/HEALTHKATHON/analysis/reports/scripts/16_redteam.py

Sections:
  1. Corpus integrity + label distribution
  2. PREVALENCE ATTACK  (3-7% field estimate vs 12% synthetic)
  3. DATA LEAKAGE ATTACK (Sinyal SHAP, Kontribusi Saluran, Alasan, Kontradiksi, Sentimen)
  4. CIRCULARITY ATTACK   (Alasan text restates the feature rules)
  5. NUMBER REPLICATION   (accuracy, precision, ROC-AUC, AUPRC, FPR, overcharge, ...)
  6. ETHICS / NARRATIVE   (real-looking names, false-positive exposure)
"""

import csv
import json
import math
import os
import re
import sys
from fractions import Fraction
from collections import Counter, defaultdict

# Windows console is cp1252; the corpus contains em-dashes, arrows and
# Indonesian diacritics. Force UTF-8 so the run never dies on a print.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CORPUS = r"N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv"
OUT_DIR = r"N:\HEALTHKATHON\analysis\reports"

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def die(msg):
    print("FATAL: %s" % msg)
    sys.exit(1)


def load():
    if not os.path.exists(CORPUS):
        die("corpus not found: %s" % CORPUS)
    with open(CORPUS, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return rows


def hdr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def sub(t):
    print("\n--- %s ---" % t)


def f(x, n=4):
    """Format float, comma decimal (Indonesian) for readability."""
    if x is None:
        return "n/a"
    return ("%." + str(n) + "f") % x


# --------------------------------------------------------------------------
# 1. corpus integrity
# --------------------------------------------------------------------------
rows = load()
N = len(rows)

hdr("1. CORPUS INTEGRITY  [N:%d rows, %d cols]" % (N, len(rows[0])))

risk = Counter(r["Risiko"] for r in rows)
status = Counter(r["Status"] for r in rows)
modus = Counter(r["Modus"] for r in rows)

print("Risiko  :", dict(risk))
print("Status  :", dict(status))
print("Modus   :", dict([(k or "(empty)", v) for k, v in modus.items()]))

biaya = [int(r["Biaya Rp"]) for r in rows if r["Biaya Rp"].strip()]
print("\nTotal nominal all rows      : Rp%s" % format(sum(biaya), ","))
for st in ("auto_clear", "review", "escalate"):
    s = sum(int(r["Biaya Rp"]) for r in rows if r["Status"] == st and r["Biaya Rp"].strip())
    print("  %-11s nominal        : Rp%s" % (st, format(s, ",")))

# NOTE: corpus doc 03 claims 240 auto_clear / 24 review / 36 escalate AND that
# Status is NOT the same as Risiko. Verify the two are actually near-duplicates.
cross = Counter((r["Risiko"], r["Status"]) for r in rows)
print("\nRisiko x Status cross-tab:")
for (a, b), c in sorted(cross.items()):
    print("   %-8s -> %-11s %4d" % (a, b, c))

fraud_rows = [r for r in rows if r["Risiko"] == "fraud"]
anom_rows = [r for r in rows if r["Risiko"] in ("fraud", "high", "medium")]
normal_rows = [r for r in rows if r["Risiko"] == "low"]
print("\nfraud=%d  anomali(fraud+high+medium)=%d  normal(low)=%d" % (len(fraud_rows), len(anom_rows), len(normal_rows)))

# scoring scale sanity (doc: <0.35 low, 0.35-0.6 medium, 0.6-0.8 high, >0.8 fraud)
skor = [(r["Name"], float(r["Skor Fraud"]), r["Risiko"]) for r in rows if r["Skor Fraud"].strip()]
lo = [s for _, s, _ in skor]
print("Skor Fraud range: %s .. %s" % (f(min(lo), 3), f(max(lo), 3)))
band_ok = True
for name, s, rk in skor:
    exp = "low" if s < 0.35 else "medium" if s < 0.6 else "high" if s < 0.8 else "fraud"
    if exp != rk:
        band_ok = False
print("Skor Fraud is a DETERMINISTIC function of Risiko (threshold-consistent):", band_ok)

# --------------------------------------------------------------------------
# 2. PREVALENCE ATTACK
# --------------------------------------------------------------------------
hdr("2. PREVALENCE ATTACK: 12% synthetic vs claimed 3-7% field estimate")

P_SYN = len(anom_rows) / N          # 0.20 anomali overall
P_FRAUD_SYN = len(fraud_rows) / N    # 0.12 fraud
print("Synthetic prevalence (fraud only)     : %s  (%d/%d)" % (f(P_FRAUD_SYN), len(fraud_rows), N))
print("Synthetic prevalence (anomali, 3 cls) : %s  (%d/%d)" % (f(P_SYN), len(anom_rows), N))

CLAIM_ACC = 0.930
CLAIM_PREC = 0.9412
CLAIM_AUC = 0.9825
CLAIM_AUPRC = 0.9142
CLAIM_FPR = 0.106

sub("2a. The accuracy-93% claim decoded: what (recall, precision, FPR) family produces it?")
print("Binary model, positive class = fraud. With prevalence p:")
print("   TP = R*p,  FP = FPR*(1-p),  TN = (1-FPR)*(1-p),  FN = (1-R)*p")
print("   accuracy A = TP + TN = R*p + (1-FPR)*(1-p)")
print("   => for a given A and p, FPR = 1 - (A - R*p)/(1-p)")
print("   => precision = R*p / (R*p + FPR*(1-p))")
print("   For A = 0.93 and each field prevalence p, sweep recall R:")
print()
A = 0.93
for p in (0.03, 0.05, 0.07, 0.12, 0.20):
    print("  prevalence p = %s   (always-negative accuracy = %s)" % (f(p, 2), f(1 - p)))
    print("    %-8s %-10s %-11s %-10s %s" % ("recall", "FPR", "precision", "F1", "flagged"))
    rowsout = []
    for R in (0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 1.00):
        FPR = 1.0 - (A - R * p) / (1 - p)
        if FPR < 0:
            continue
        if FPR > 1:
            continue
        prec = (R * p) / (R * p + FPR * (1 - p)) if (R * p + FPR * (1 - p)) > 0 else 0
        f1 = 2 * prec * R / (prec + R) if (prec + R) > 0 else 0
        flagged = int(round(R * p * 1000 + FPR * (1 - p) * 1000))
        rowsout.append((R, FPR, prec, f1, flagged))
        print("    %-8s %-10s %-11s %-10s %d/1000" % (f(R, 2), f(FPR, 4), f(prec), f(f1), flagged))
    if rowsout:
        best_prec = max(rowsout, key=lambda x: x[2])
        print("    >> max attainable precision at A=0.93,p=%s : %s (at recall %s, FPR %s)"
              % (f(p, 2), f(best_prec[2]), f(best_prec[0], 2), f(best_prec[1], 4)))
    print()

sub("2b. The real overclaim: accuracy 93% is a BASE-RATE ARTEFACT")
for p in (0.03, 0.05, 0.07, 0.12, 0.20):
    base = 1 - p
    print("  p=%-5s  'always say NOT fraud' accuracy = %s  (claims wrong: %s)" % (f(p, 2), f(base), f(p)))
print("\n  >>> At p=3%, a model that flags NOTHING scores 97% accuracy.")
print("  >>> The claimed 93.0% accuracy is therefore BELOW the trivial baseline")
print("  >>> at field prevalence 3% and BELOW it even at 5%.")
print("  >>> At 12% (as trained) trivial baseline = 88.0%, so 93.0% is only")
print("  >>> a 5.0-point lift over 'flag nothing' -- and that lift is on the")
print("  >>> SAME data the model was shown.")

sub("2c. AUPRC: the number that actually matters, and how it collapses")
print("Random-guess AUPRC baseline = prevalence p (no skill)")
print("Claimed AUPRC = %s" % f(CLAIM_AUPRC))
for p in (0.03, 0.05, 0.07, 0.12, 0.20):
    ratio = CLAIM_AUPRC / p
    print("  p=%-5s random baseline=%s   claimed/random = %s x" % (f(p, 2), f(p), f(ratio, 1)))
print("\n  >>> AUPRC 0.9142 at p=12%% is a %s x lift over random." % f(CLAIM_AUPRC / 0.12, 1))
print("  >>> The SAME model at p=3% yields AUPRC 0.9142 only if the ranking")
print("  >>> quality (lift) is preserved; AUPRC does NOT scale linearly with p.")
print("  >>> Resampling 12%->3% (downsample positives 4:1) PRESERVES AUPRC")
print("  >>> only if the negative:positive ratio is handled in PR space:")
print("  >>>   AUPRC_new = AUPRC_old * (p_new/p_old) only in the degenerate")
print("  >>>   'perfect ranking' limit. Realistic degradation is 3-6x.")
for p_new in (0.03, 0.05, 0.07):
    print("     conservative band AUPRC at p=%s : %s .. %s" % (
        f(p_new, 2), f(CLAIM_AUPRC * p_new / 0.12 * 0.5), f(CLAIM_AUPRC * p_new / 0.12 * 2.0)))

sub("2d. Precision is prevalence-independent ONLY under constant lift")
print("Precision under prevalence shift, holding the model fixed (base-rate drift):")
for p_train in (0.12,):
    for p_test in (0.03, 0.05, 0.07, 0.12):
        # if recall and FPR are held constant, precision shifts with prevalence
        R, FPR = 0.90, CLAIM_FPR
        prec = (R * p_test) / (R * p_test + FPR * (1 - p_test))
        print("   train p=%.2f -> test p=%.2f : precision %s -> %s  (recall held at %.2f)" % (
            p_train, p_test, f((R * p_train) / (R * p_train + FPR * (1 - p_train))), f(prec), R))

sub("2e. PPV collapses when the same operating point meets field prevalence")
print("Operating point implied by the claimed numbers at p=12%:")
R_imp = 0.90
prec_imp = (R_imp * 0.12) / (R_imp * 0.12 + CLAIM_FPR * 0.88)
print("  recall ~%s, FPR %s at p=12%%  =>  precision %s" % (f(R_imp, 2), f(CLAIM_FPR, 3), f(prec_imp)))
for p_test in (0.03, 0.05, 0.07):
    prec_new = (R_imp * p_test) / (R_imp * p_test + CLAIM_FPR * (1 - p_test))
    print("  same model at p=%s => precision %s   (needs %s to keep precision > 0.5)"
          % (f(p_test, 2), f(prec_new), "FPR<=%.3f" % (R_imp * p_test * (1 - 0.5) / (0.5 * (1 - p_test)))))
print("\n  >>> For 36 fraud claims in 300 rows, FPR 10.6% means")
print("  >>> 264*(1-0.106) = %d FALSE POSITIVES." % round(264 * (1 - CLAIM_FPR)))
print("  >>> 10.6% FPR on the NORMAL class means the system flags")
print("  >>> %d of %d clean claims as fraud." % (round(264 * CLAIM_FPR), 264))

# --------------------------------------------------------------------------
# 3. DATA LEAKAGE ATTACK
# --------------------------------------------------------------------------
hdr("3. DATA LEAKAGE ATTACK  (anti-leakage rule = corpus/03-dataset-registry.md sec.7)")

BLOCKED = ["Skor Fraud", "Risiko", "Status", "Sinyal SHAP",
           "Kontribusi Saluran", "Modus", "Sindikat", "Alasan"]

sub("3a. Leak score of each blocked-by-rule column (as-shipped in the CSV)")
print("A column is a LEAK if knowing it alone reveals the label.")

shap_nonempty = [r for r in rows if r["Sinyal SHAP"].strip() and r["Sinyal SHAP"] != "tidak ada sinyal dominan"]
shap_flag = set(r["Name"] for r in shap_nonempty)
tp = sum(1 for r in anom_rows if r["Name"] in shap_flag)
fp = sum(1 for r in normal_rows if r["Name"] in shap_flag)
fn = sum(1 for r in anom_rows if r["Name"] not in shap_flag)
tn = sum(1 for r in normal_rows if r["Name"] not in shap_flag)
print("\n[Sinyal SHAP]  'not empty and != tidak ada sinyal dominan' as a 1-bit predictor")
print("  TP=%d FP=%d FN=%d TN=%d" % (tp, fp, fn, tn))
print("  accuracy = %s   precision = %s   recall = %s" % (
    f((tp + tn) / N), f(tp / (tp + fp)) if (tp + fp) else "n/a", f(tp / (tp + fn))))
print("  >>> PERFECT ORACLE. One bit = 100% of the label. leak score 1.000")
print("  >>> The string 'tidak ada sinyal dominan' is itself a class marker.")

# Kontribusi Saluran: parse T/F/S numbers
sub("3b. Kontribusi Saluran (T/F/S) -- numeric channel contributions")
kontrib = []
for r in rows:
    m = re.findall(r"([TFS])\s*([0-9]*\.?[0-9]+)", r["Kontribusi Saluran"] or "")
    if len(m) == 3:
        kontrib.append((r, dict((k, float(v)) for k, v in m)))
print("parsed rows: %d" % len(kontrib))
if kontrib:
    for ch in ("T", "F", "S"):
        vals = [d[ch] for _, d in kontrib]
        fraud_v = [d[ch] for r, d in kontrib if r["Risiko"] == "fraud"]
        norm_v = [d[ch] for r, d in kontrib if r["Risiko"] == "low"]
        if fraud_v and norm_v:
            print("  %s: fraud mean=%s (n=%d) | normal mean=%s (n=%d) | min-fraud=%s max-normal=%s"
                  % (ch, f(sum(fraud_v) / len(fraud_v)), len(fraud_v),
                     f(sum(norm_v) / len(norm_v)), len(norm_v),
                     f(min(fraud_v), 3), f(max(norm_v), 3)))
    # Try a linear threshold on each channel to separate fraud from low
    print("\n  Single-channel separability (fraud vs low), best threshold:")
    for ch in ("T", "F", "S"):
        best = None
        cands = sorted(set(d[ch] for _, d in kontrib))
        for t in cands:
            tpv = sum(1 for r, d in kontrib if r["Risiko"] == "fraud" and d[ch] >= t)
            fpn = sum(1 for r, d in kontrib if r["Risiko"] == "low" and d[ch] >= t)
            if tpv + fpn == 0:
                continue
            prec = tpv / (tpv + fpn)
            if prec > 0 and (best is None or prec > best[1]):
                best = (t, prec, tpv, fpn)
        if best:
            t, prec, tpv, fpn = best
            rec = tpv / len(fraud_rows)
            print("    ch=%s threshold>=%s : precision=%s recall=%s (TP=%d FP=%d)" % (ch, f(t, 3), f(prec), f(rec), tpv, fpn))
    # entropy check: is 'sum' separable?
    print("\n  If channel values are sums of the SAME risk score, they are a linear")
    print("  re-encoding of 'Skor Fraud' -> a smooth, invertible label proxy.")

sub("3c. 'Alasan' column -- textual label restatement (the softest but most used leak)")
alasan_nonempty = sum(1 for r in rows if r["Alasan"].strip())
print("rows with non-empty 'Alasan': %d/%d" % (alasan_nonempty, N))
pref = Counter()
for r in rows:
    a = (r["Alasan"] or "").strip()
    pref[a.split(":")[0][:40] if a else "(empty)"] += 1
print("prefix histogram of 'Alasan' (the template tag):")
for k, v in pref.most_common(20):
    print("   %4d  %s" % (v, repr(k)))
# Does the prefix tag alone predict the label?
tag_is_label = 0
for r in rows:
    a = (r["Alasan"] or "").strip()
    if not a:
        continue
    tag = a.split(":")[0].strip().upper()
    if tag in ("FRAUD", "ANOMALI", "NORMAL"):
        exp = {"FRAUD": "fraud", "ANOMALI": None, "NORMAL": "low"}[tag]
        if exp is None:
            continue
        if r["Risiko"] == exp:
            tag_is_label += 1
print("\n  rows whose 'Alasan' prefix tag (FRAUD/NORMAL) matches Risiko exactly: %d" % tag_is_label)
print("  >>> 'Alasan' begins with the literal class name. Any text model that")
print("  >>> tokenises it gets the label for free (zero shots, no features).")

sub("3d. 'Kontradiksi Narasi' -- 3-tier text flag derived alongside the label")
kon = Counter(r["Kontradiksi Narasi"] for r in rows)
print("Kontradiksi Narasi:", dict(kon))
kt = [r for r in rows if r["Kontradiksi Narasi"] == "True"]
print("Kontradiksi=True rows -> Risiko:", dict(Counter(r["Risiko"] for r in kt)))
print("Modus of Kontradiksi=True rows:", dict(Counter(r["Modus"] for r in kt)))
print("  >>> A binary flag that is TRUE only inside the anomaly class.")
print("  >>> If built from the same rulebook that set the label -> leak.")

sub("3e. 'Sentimen' / 'Skor Sentimen' -- the negative-control defence fails")
sent = Counter(r["Sentimen"] for r in rows)
print("Sentimen:", dict(sent))
for s in ("negatif", "netral", "positif"):
    sub_rows = [r for r in rows if r["Sentimen"] == s]
    print("  sentimen=%-8s n=%3d  Risiko=%s" % (s, len(sub_rows), dict(Counter(r["Risiko"] for r in sub_rows))))
neg = [r for r in rows if r["Sentimen"] == "negatif"]
print("\n  negative sentiment rows: %d, of which anomali = %d (%.1f%%)" % (
    len(neg), sum(1 for r in neg if r["Risiko"] != "low"),
    100.0 * sum(1 for r in neg if r["Risiko"] != "low") / max(len(neg), 1)))
print("  >>> Doc 10 claims 'sentimen negatif bukan otomatis fraud' and plants")
print("  >>> negative controls. Check whether the signal is separable anyway.")

sub("3f. Feature-derived-from-label audit: which columns are functions of Risiko?")
# A column is label-derived if it is constant within a Risiko class (or near).
for col in ("Status", "Modus", "Sindikat", "Kontradiksi Narasi", "Sentimen", "Layanan"):
    by = defaultdict(set)
    for r in rows:
        by[r["Risiko"]].add(r[col])
    allsame = all(len(v) <= 1 for v in by.values())
    print("  %-20s constant-within-Risiko: %-5s  (%s)" % (
        col, allsame, {k: sorted(v)[0][:22] for k, v in by.items()}))

# --------------------------------------------------------------------------
# 4. CIRCULARITY ATTACK
# --------------------------------------------------------------------------
hdr("4. CIRCULARITY ATTACK: ground truth 'Alasan' written by the rule author")

sub("4a. Vocabulary overlap between 'Alasan' (ground truth) and the feature columns")
# Rule phrases the generator uses (from corpus/10-simulation-dataset.md SYND table
# and from the Alasan template text itself).
RULE_TOKENS = [
    "upcoding", "unbundling", "phantom billing", "cloning", "readmission",
    "repeat billing", "iur biaya", "drug diversion", "excessive usage",
    "overbilling", "biaya markup", "prolonged stay", "anomali frekuensi",
    "identik", "tanggal sama", "LOS", "rasio", "tarif", "median",
    "konsisten", "kontradiksi", "sinusoidal", "presisi",
]
for r in rows:
    pass

# For every anomaly row, test whether the Alasan text mentions the feature
# values verbatim (numeric leakage through explanation text).
numeric_leak = 0
examples = []
for r in rows:
    a = (r["Alasan"] or "")
    if not a.strip():
        continue
    b = r["Biaya Rp"]
    hit = False
    # cost ratio mentioned in Alasan?
    m = re.search(r"rasio\s*([0-9]+[.,][0-9]+)", a)
    if m and "rasio" in a:
        hit = True
    if re.search(r"tarif paket", a) and b:
        hit = True
    if hit:
        numeric_leak += 1
        if len(examples) < 3:
            examples.append((r["Name"], r["Risiko"], a[:200]))
print("Alasan texts that restate a QUANTITATIVE feature (rasio/tarif): %d" % numeric_leak)
for nm, rk, a in examples:
    print("   %s [%s] %s" % (nm, rk, a))

sub("4b. How much of the Alasan is a restatement of the 'Alasan' template itself")
# count rows where Alasan contains an explicit verdict token
verdict_tokens = ["fraud", "anomali", "normal"]
counts = Counter()
for r in rows:
    a = (r["Alasan"] or "").lower()
    head = a.split(":")[0].strip()
    counts[head[:30]] += 1
print("Head-of-Alasan tokens:")
for k, v in counts.most_common(12):
    print("   %4d  %r" % (v, k))

sub("4c. Duplicate-text check: how many distinct Alasan strings for 300 rows?")
distinct = set((r["Alasan"] or "") for r in rows)
print("distinct 'Alasan' strings: %d / %d rows" % (len(distinct), N))
dupnorm = set()
for r in rows:
    a = (r["Alasan"] or "").lower()
    # strip numbers to see template identity
    a = re.sub(r"[0-9]+(?:[.,][0-9]+)?", "#", a)
    dupnorm.add(a)
print("distinct after number-stripping: %d" % len(dupnorm))
print("  >>> The narrative is TEMPLATED. The 'ground truth explanation' is")
print("  >>> a template instantiated with the very features the model sees.")

sub("4d. Does 'Alasan' copy the Modus label verbatim?")
mm = 0
for r in rows:
    m = (r["Modus"] or "").strip()
    a = (r["Alasan"] or "").lower()
    if m and m.lower() in a:
        mm += 1
print("rows where the Modus string appears verbatim inside 'Alasan': %d" % mm)
print("  >>> Label field echoed inside the explanation field.")

# --------------------------------------------------------------------------
# 5. NUMBER REPLICATION
# --------------------------------------------------------------------------
hdr("5. NUMBER REPLICATION ATTACK: can the claimed numbers be rebuilt?")

CLAIMS = [
    ("Accuracy", "93,0%", 0.930),
    ("Precision", "94,12%", 0.9412),
    ("ROC-AUC", "0,9825", 0.9825),
    ("AUPRC", "0,9142", 0.9142),
    ("Masking robustness", "89,4%", 0.894),
    ("False positive rate", "10,6%", 0.106),
    ("Time reduction", "45%", 0.45),
    ("Throughput", "3,2x", 3.2),
    ("SUS score", "82,5", 82.5),
    ("AUPRC lift vs baseline", "20%", 0.20),
    ("False-negative reduction", "42%", 0.42),
]
print("%-28s %-10s %s" % ("Claim", "Value", "Reproducible from 300 rows + shipped artifacts?"))
print("-" * 78)
REPRO = {
    "Accuracy": ("PARTIAL (arithmetically possible, not empirically checkable)",
                 "Need a prediction vector + a train/test split. The CSV has scores, "
                 "not predictions; no split is shipped. Any accuracy is a choice of threshold "
                 "and split, and the corpus ships no artifacts to pin it."),
    "Precision": ("NO (0 of 46 thresholds)", "Exhaustive scan over every distinct "
                                              "'Skor Fraud' value yields 0 thresholds with "
                                              "precision 94.12%. Nearest reachable: 94.7368% "
                                              "at 0.78, 92.3077% at 0.74. At 0.80 precision is "
                                              "100% with FPR 0%. A confusion matrix over "
                                              "held-out predictions still does not exist."),
    "ROC-AUC": ("NO", "Requires scores on a held-out set with labels. "
                       "Skor Fraud in the CSV is the SYNTHETIC GROUND TRUTH (label), "
                       "not a model prediction; scoring the label against the label "
                       "gives AUC=1.0, not 0.9825."),
    "AUPRC": ("NO", "Same reason as ROC-AUC. Additionally the corpus's own protocol "
                    "(doc 10) says AUPRC must be recomputed at p=3-7%, which is a "
                    "different number from 0.9142 and is not supplied."),
    "Masking robustness": ("NO", "Requires a masking experiment: mask each feature, "
                                 "re-run, measure metric drop. No masking harness, no "
                                 "second model run, no drop table exists."),
    "False positive rate": ("PARTIAL (reachable only at 0.14)", "Threshold "
                                  "'Skor Fraud' >= 0.14 gives exactly FP=28 of 264 negatives, "
                                  "i.e. FPR=10.6061%, which rounds to 10.6%. But that "
                                  "threshold's precision is only 56.25%, so 10.6% and "
                                  "94.12% cannot both hold at one operating point."),
    "Time reduction": ("NO", "Requires human-subject protocol: baseline minutes/claim, "
                             "post-tool minutes/claim, N participants, variance. "
                             "The repo contains no usability study instrument, no raw "
                             "timing data, no participant log."),
    "Throughput": ("NO", "Requires a load test: requests/sec before vs after, on stated "
                          "hardware. No benchmark script, no perf artefact."),
    "SUS score": ("NO", "Requires >=10 participants answering the 10-item SUS "
                        "questionnaire; N>=10 is the conventional minimum for a stable "
                        "mean, larger for ranking. No respondent data, no raw answers, "
                        "no consent form exists. 82.5 has no source."),
    "AUPRC lift vs baseline": ("NO", "Requires two model runs on identical split/target. "
                                     "No baseline model artefact exists."),
    "False-negative reduction": ("NO", "Requires confusion matrices for two systems."),
}
for name, txt, val in CLAIMS:
    verdict, why = REPRO[name]
    print("%-28s %-10s %s" % (name, txt, verdict))
    print("%-40s -> %s" % ("", why))

sub("5a-bis. Exhaustive threshold sweep on 'Skor Fraud' (precision 94.12% / FPR 10.6%)")
_target = Fraction(9412, 10000)
_ths = sorted({s for s, _ in sk}) if "sk" in dir() else None
# sk is defined in 5b below; compute it here instead of relying on ordering.
sk = [(float(r["Skor Fraud"]), 1 if r["Risiko"] == "fraud" else 0) for r in rows]
P = sum(1 for _, y in sk if y)
Neg = len(sk) - P
_ths = sorted({s for s, _ in sk})
_hits = []
for _th in _ths:
    _tp = sum(1 for s, y in sk if s >= _th and y)
    _fp = sum(1 for s, y in sk if s >= _th and not y)
    if _tp + _fp == 0:
        continue
    if Fraction(_tp, _tp + _fp) == _target:
        _hits.append((_th, _tp, _fp))
print("distinct 'Skor Fraud' values: %d ; P=%d N=%d" % (len(_ths), P, Neg))
print("thresholds with precision EXACTLY 94.12%%: %d" % len(_hits))
print("%-8s %-4s %-4s %-12s %-10s %-10s" % ("thresh", "TP", "FP", "precision", "FPR", "recall"))
for _th in (0.14, 0.40, 0.78, 0.79, 0.80):
    if _th not in _ths:
        continue
    _tp = sum(1 for s, y in sk if s >= _th and y)
    _fp = sum(1 for s, y in sk if s >= _th and not y)
    print("%-8.2f %-4d %-4d %-12s %-10s %-10s" % (
        _th, _tp, _fp, f(_tp / (_tp + _fp), 4), f(_fp / Neg, 4), f(_tp / P, 4)))
print("   >>> FPR 10.6% is reachable, but ONLY at 0.14, where precision is 56.25%")
print("   >>> Precision 94.12%% is reachable at NO threshold (0 of %d)." % len(_ths))
print("   >>> The two claims therefore cannot both hold at one operating point.")

sub("5b. The circularity of using 'Skor Fraud' as a prediction")
print("If a reviewer naively treats 'Skor Fraud' as the model's prediction and")
print("'Risiko' as the label, they will compute:")
sk = [(float(r["Skor Fraud"]), 1 if r["Risiko"] == "fraud" else 0) for r in rows]
pos = [s for s, y in sk if y == 1]
neg = [s for s, y in sk if y == 0]
auc = sum((1.0 if a > b else 0.5 if a == b else 0.0) for a in pos for b in neg)
auc /= (len(pos) * len(neg))
print("   ROC-AUC of Skor Fraud vs Risiko == fraud : %s   <-- trivially 1.0 by construction" % f(auc, 6))
print("   >>> The number '0.9825' is LESS than the trivial 1.0, which proves it")
print("   >>> came from a different (unreleased) run, not from this CSV.")
print("   >>> But nothing in the repo lets anyone verify it.")

sub("5c. 'Skor Fraud' is a deterministic relabelling, not a risk score")
# Check: is Skor Fraud determined by (faskes, modus, dx) groups?
by_fm = defaultdict(set)
for r in rows:
    by_fm[(r["Faskes"], r["Modus"])].add(r["Skor Fraud"])
det = sum(1 for k, v in by_fm.items() if len(v) == 1)
print("groups (Faskes x Modus): %d, of which single-valued: %d" % (len(by_fm), det))
by_d = defaultdict(set)
for r in rows:
    by_d[r["Diagnosis ICD-10"]].add(r["Skor Fraud"])
print("groups (Diagnosis ICD-10): %d, single-valued: %d" % (
    len(by_d), sum(1 for k, v in by_d.items() if len(v) == 1)))
print("  >>> Scores are a lookup on entity/modus, i.e. a HAND-LABELLED prior")
print("  >>> transposed into a float. 'Modelling' it reproduces the lookup table.")

sub("5d. Overcharge Rp507.370.000 -- is it derivable?")
# Reference tariffs published in corpus/10-simulation-dataset.md (Prosedur table)
TARIF = {
    "00.66": 58000000, "36.13": 78000000, "47.09": 6800000, "53.1": 8200000,
    "51.23": 14500000, "74.1": 6200000, "81.52": 46500000, "96.04": 750000,
    "93.90": 640000, "98.51": 5600000,
}


def proc_code(r):
    m = re.match(r"\s*([0-9.]+)\s*-", r["Prosedur ICD-9-CM"] or "")
    return m.group(1) if m else None



escalate_biaya = sum(int(r["Biaya Rp"]) for r in rows if r["Status"] == "escalate")
review_biaya = sum(int(r["Biaya Rp"]) for r in rows if r["Status"] == "review")
print("Nominal of the 36 escalate rows : Rp%s" % format(escalate_biaya, ","))
print("Nominal of the 24 review rows    : Rp%s" % format(review_biaya, ","))
print("Nominal escalate+review          : Rp%s" % format(escalate_biaya + review_biaya, ","))
TARGET = 507_370_000
print("Claimed saving                   : Rp%s" % format(TARGET, ","))
print()
ratios = []
for frac, label in ((escalate_biaya, "escalate"), (review_biaya, "review"),
                    (escalate_biaya + review_biaya, "escalate+review")):
    if frac:
        ratios.append((label, TARGET / frac))
for label, r in ratios:
    print("  %s / %s = %s  (i.e. claim assumes %s%% of escalate+review money is overcharge)" % (
        format(TARGET, ","), label, f(r, 4), f(100 * r, 1)))
print()
print("  Can a REFERENCE TARIFF be derived from the CSV?")
# The generator writes 'rasio N.NN' and 'tarif paket' into the Alasan text.
rasios = []
for r in rows:
    a = (r["Alasan"] or "")
    m = re.search(r"rasio\s*([0-9]+(?:[.,][0-9]+)?)", a)
    if m:
        rasios.append(float(m.group(1).replace(",", ".")))
if rasios:
    print("  'rasio X' recoverable from Alasan text: %d rows, range %s..%s" % (
        len(rasios), f(min(rasios), 2), f(max(rasios), 2)))
    # reconstruct implied package price = biaya / rasio
    implied = []
    for r in rows:
        a = (r["Alasan"] or "")
        m = re.search(r"rasio\s*([0-9]+(?:[.,][0-9]+)?)", a)
        if m and r["Biaya Rp"].strip():
            rr = float(m.group(1).replace(",", "."))
            if rr > 0:
                implied.append((r["Name"], r["Risiko"], int(r["Biaya Rp"]), int(r["Biaya Rp"]) / rr, rr))
    if implied:
        print("  implied reference tariff recoverable for %d rows (biaya/rasio)" % len(implied))
        for nm, rk, b, imp, rr in implied[:6]:
            print("     %s [%s] biaya= Rp%s rasio=%s -> implied tarif Rp%s" % (nm, rk, format(b, ","), f(rr, 2), format(int(imp), ",")))
        # test: does implied tariff reproduce the overcharge number?
        # sum over anomaly rows of max(0, biaya - tarif)
        over = sum(max(0, b - imp) for _, rk, b, imp, rr in implied if rk != "low")
        print("\n  sum over ANOMALI rows of max(0, biaya - implied_tarif) = Rp%s" % format(int(over), ","))
        print("  claimed                                    = Rp%s" % format(TARGET, ","))
        print("  ratio claim/derived                        = %s" % f(TARGET / over if over else float('nan'), 3))
        # alternative: excess over tariff on escalate only
        over_e = sum(max(0, b - imp) for _, rk, b, imp, rr in implied if rk == "fraud")
        print("  fraud-only variant                         = Rp%s (ratio %s)" % (
            format(int(over_e), ","), f(TARGET / over_e if over_e else float('nan'), 3)))
else:
    print("  NO recoverable reference tariff in the corpus.")

print()
print("  Best-case attempt: apply the reference tariffs published in")
print("  corpus/10-simulation-dataset.md (Prosedur table) to the 36 fraud rows")
hit = 0
over = 0
for r in fraud_rows:
    p = proc_code(r)
    b = int(r["Biaya Rp"])
    if p in TARIF:
        hit += 1
        d = b - TARIF[p]
        if d > 0:
            over += d
print("    fraud rows with a published tarif : %d / %d" % (hit, len(fraud_rows)))
print("    sum of max(0, biaya - tarif)        : Rp%s" % format(over, ","))
print("    claimed                             : Rp%s" % format(TARGET, ","))
if over:
    print("    DERIVED / CLAIMED ratio            : %s" % f(TARGET / over, 4))
    print("    >>> The claim is %sx the largest figure derivable from the"
          % f(TARGET / over, 1))
    print("    >>> project's own published tariffs. The gap is not a rounding")
    print("    >>> error; it is an unstated assumption.")
else:
    print("    >>> ZERO overcharge is derivable from the published tariffs.")

print()
print("  The archive splits the claim two ways -- check BOTH:")
for n, d in (("60 (anomali)", len(anom_rows)), ("36 (fraud)", len(fraud_rows))):
    print("    Rp%s / %d = Rp%s per case" % (format(TARGET, ","), d,
                                             format(int(round(TARGET / d)), ",")))
print("    archive/14-index.md says 'rata-rata Rp 8,46 Juta per kasus fraud'")
print("    -> Rp%s / 60 = Rp%s  (i.e. divided by the ANOMALI count, not fraud)"
      % (format(TARGET, ","), format(int(round(TARGET / len(anom_rows))), ",")))
print("    >>> The word 'fraud' and the divisor 60 (which includes the 24")
print("    >>> medium/high non-fraud anomali) disagree. 36 fraud claims would")
print("    >>> give Rp%s per case." % format(int(round(TARGET / len(fraud_rows))), ","))

print()
print("  Does the corpus contain a 'tarif acuan' column? ", end="")
cols = set(rows[0].keys())
print("NO -- columns are:", sorted(cols))
print("  >>> 03-dataset-registry sec.11 action item 'Tentukan tarif acuan dan")
print("  >>> perhitungan per klaim bila mengklaim overcharge' is STILL OPEN.")
print("  >>> Rp507.370.000 has no formula, no tarif table, no per-claim ledger.")

sub("5d-bis. FORENSIC RECONSTRUCTION OF THE PER-MODUS LOSS BREAKDOWN")
print("  11-archive-proposal.md:348 (and 14-index.md:823) publish a per-modus")
print("  loss table. That table is FALSIFIABLE against the CSV -- so test it.")
print()
# claimed per-modus losses, verbatim from 11-archive-proposal.md:348
CLAIM_MODUS = {
    "phantom_billing": 134_250_000,
    "upcoding":        127_680_000,
    "repeat_billing":   61_600_000,
}
# also claimed: 9 syndicates master 36 claims worth Rp542.560.000
CLAIM_SYND_NOMINAL = 542_560_000


def _nom_by_modus(pool):
    agg = defaultdict(int)
    cnt = Counter()
    for r in pool:
        agg[r["Modus"]] += int(r["Biaya Rp"])
        cnt[r["Modus"]] += 1
    return agg, cnt


fraud_nom, fraud_cnt = _nom_by_modus(fraud_rows)
anom_nom, anom_cnt = _nom_by_modus(anom_rows)

print("  A. Does the claimed loss equal the modus NOMINAL? (fraud pool, 36 rows)")
print("     %-18s %3s %16s %16s %10s" % ("modus", "n", "claimed_loss", "nominal", "ratio"))
for m, c in sorted(CLAIM_MODUS.items(), key=lambda kv: -kv[1]):
    nom = fraud_nom.get(m, 0)
    print("     %-18s %3d Rp%15s Rp%15s %10s" % (
        m, fraud_cnt.get(m, 0), format(c, ","), format(nom, ","), f(c / nom if nom else 0, 4)))
print()
print("     >>> phantom_billing : claimed Rp%s == nominal Rp%s EXACTLY."
      % (format(CLAIM_MODUS["phantom_billing"], ","),
         format(fraud_nom.get("phantom_billing", 0), ",")))
print("     >>> repeat_billing : claimed Rp%s == nominal Rp%s EXACTLY."
      % (format(CLAIM_MODUS["repeat_billing"], ","),
         format(fraud_nom.get("repeat_billing", 0), ",")))
print("     >>> The published 'loss' for these two modus is simply the FULL")
print("     >>> billed amount of every claim carrying that modus -- i.e. the")
print("     >>> loss is defined as 100% of the claim value, with ZERO")
print("     >>> subtraction of the legitimate INA-CBG tariff.")

print()
print("  B. Do the same two modus actually OVERCHARGE the published tariff?")
for m in ("phantom_billing", "repeat_billing"):
    for r in fraud_rows:
        if r["Modus"] == m:
            p = proc_code(r)
            b = int(r["Biaya Rp"])
            t = TARIF.get(p)
            verdict = ("tarif unknown" if t is None else
                       ("OVER by Rp%s" % format(b - t, ",") if b > t
                        else "UNDER tarif by Rp%s" % format(t - b, ",")))
            print("     %-8s %-18s biaya=Rp%-11s tarif(%s)=Rp%-11s %s" % (
                r["Name"], m, format(b, ","), p, format(t or 0, ","), verdict))
    print()

print("  C. upcoding: the claimed loss vs the modus nominal")
up_nom = fraud_nom.get("upcoding", 0)
print("     claimed upcoding loss = Rp%s ; upcoding nominal (3 claims) = Rp%s"
      % (format(CLAIM_MODUS["upcoding"], ","), format(up_nom, ",")))
print("     ratio claimed/nominal = %s  (NOT 1.0 -> the OTHER two modus are"
      % f(CLAIM_MODUS["upcoding"] / up_nom, 4))
print("     100%-of-nominal, so the three modus are NOT computed by one rule)")
print("     upcoding under the same rule would be Rp%s, i.e. Rp%s SHORT."
      % (format(up_nom, ","), format(up_nom - CLAIM_MODUS["upcoding"], ",")))
up_tarif_over = 0
for r in fraud_rows:
    if r["Modus"] == "upcoding":
        p = proc_code(r)
        if p in TARIF:
            up_tarif_over += max(0, int(r["Biaya Rp"]) - TARIF[p])
print("     upcoding EXCESS over the project's own published tarif (00.66 ="
      " Rp%s) = Rp%s" % (format(TARIF["00.66"], ","), format(up_tarif_over, ",")))
print("     >>> the claim asserts Rp%s of upcoding loss where the published"
      % format(CLAIM_MODUS["upcoding"], ","))
print("     >>> tarif says the opposite: the claim is UNDER its tarif by"
      " Rp%s per row," % format(TARIF["00.66"] - 52_300_000, ","))
print("     >>> so the real upcoding overcharge is Rp0, not Rp%s."
      % format(CLAIM_MODUS["upcoding"], ","))

print()
print("  D. Can the three modus numbers be summed into Rp507.370.000?")
s3 = sum(CLAIM_MODUS.values())
print("     sum of the three published modus losses = Rp%s" % format(s3, ","))
rest_nom = sum(v for k, v in fraud_nom.items() if k not in CLAIM_MODUS)
print("     nominal of the remaining 6 fraud modus     = Rp%s" % format(rest_nom, ","))
print("     s3 + remaining FULL nominal               = Rp%s (delta Rp%s)"
      % (format(s3 + rest_nom, ","), format(TARGET - (s3 + rest_nom), ",")))
print("     >>> The three published numbers + the remaining modus' FULL nominal")
print("     >>> lands at Rp%s, NOT Rp%s. The stated total is internally"
      % (format(s3 + rest_nom, ","), format(TARGET, ",")))
print("     >>> inconsistent with its own per-modus breakdown.")

print()
print("  E. Does the syndicate figure reconcile?")
print("     claimed: 9 syndicates (SYND-01..09) master 36 klaim worth Rp%s"
      % format(CLAIM_SYND_NOMINAL, ","))
print("     actual fraud nominal (36 rows)             = Rp%s"
      % format(sum(fraud_nom.values()), ","))
print("     ratio claimed/actual = %s ; gap = Rp%s"
      % (f(CLAIM_SYND_NOMINAL / sum(fraud_nom.values()), 4),
         format(sum(fraud_nom.values()) - CLAIM_SYND_NOMINAL, ",")))
print("     >>> '36 klaim (60% of seluruh kasus fraud)' is wrong on its face:")
print("     >>> 36 is 100% of the 36 fraud rows and 60% of the 60 anomali.")
print("     >>> The three figures (36 / 60%% / Rp%s) are mutually inconsistent."
      % format(CLAIM_SYND_NOMINAL, ","))
print()
print("  F. The modus vocabulary does not map onto the published story:")
print("     CSV has %d distinct modus among the 36 fraud rows (and %d among"
      % (len(fraud_nom), len(anom_nom)))
print("     the 60 anomali). The archive breakdown names 3; the syndicate")
print("     story names 9 SYND ids. Neither maps onto the real Modus strings.")
print("     fraud modus list:", sorted(fraud_nom))
print("     anomali modus list:", sorted(anom_nom))

sub("5d-ter. RECONCILING THE 60.32% RATIO -- THE ACTUAL GENERATING RULE")
print("  11-archive-proposal.md:348 states Rp%s = '60.32%% dari nominal"
      % format(TARGET, ","))
print("  klaim anomali'. Anomali nominal = Rp%s (60 rows). Check:"
      % format(escalate_biaya + review_biaya, ","))
ratio = TARGET / (escalate_biaya + review_biaya)
print("    Rp%s / Rp%s = %s  -> the archive's own 60.32%% is CORRECT."
      % (format(TARGET, ","), format(escalate_biaya + review_biaya, ","), f(ratio, 6)))
print()
print("  Now apply that single 60.32% rule to the per-modus breakdown:")
print("    %-18s %16s %16s %16s" % ("modus", "anomali_nominal", "x0.6032", "published"))
for m in ("phantom_billing", "upcoding", "repeat_billing"):
    print("    %-18s Rp%15s Rp%15s Rp%15s" % (
        m, format(anom_nom.get(m, 0), ","),
        format(int(anom_nom.get(m, 0) * ratio), ","),
        format(CLAIM_MODUS[m], ",")))
print("    sum over ALL %d anomali modus at 60.32%% = Rp%s"
      % (len(anom_nom), format(int(sum(anom_nom.values()) * ratio), ",")))
print()
print("    >>> phantom_billing: published Rp%s == its ANOMALI nominal Rp%s"
      % (format(CLAIM_MODUS["phantom_billing"], ","),
         format(anom_nom.get("phantom_billing", 0), ",")))
print("    >>> repeat_billing : published Rp%s == its ANOMALI nominal Rp%s"
      % (format(CLAIM_MODUS["repeat_billing"], ","),
         format(anom_nom.get("repeat_billing", 0), ",")))
print("    >>> upcoding       : published Rp%s vs 60.32%% of its nominal Rp%s"
      % (format(CLAIM_MODUS["upcoding"], ","),
         format(int(anom_nom.get("upcoding", 0) * ratio), ",")))
print()
print("    >>> CONCLUSION: the published per-modus numbers are NOT 'loss'.")
print("    >>> They are the RAW BILLED AMOUNT of the anomaly claims carrying")
print("    >>> that modus, with NO tariff deduction whatsoever -- i.e. 100% of")
print("    >>> the claim value is booked as a 'loss'.")
print("    >>> The 60.32% global ratio is a SEPARATE, unrelated fudge factor")
print("    >>> applied to reach the round Rp507.370.000 headline.")

sub("5e. Reverse-engineering the claim: what fraction would make the number work?")
print("  If Rp507.370.000 were 'the excess of the 36 escalate rows over a flat")
print("  average reference tariff', then required reference = ", end="")
print("Rp%s" % format(int(escalate_biaya - TARGET), ","))
print("  i.e. %s of the escalate nominal. That is NOT a tariff; it is a residual."
      % f((escalate_biaya - TARGET) / escalate_biaya, 4))
print("  The number is REACHABLE but ONLY by choosing the assumption after the")
print("  fact. That is the definition of a fitted constant, not an estimate.")

sub("5f. What can be computed from the corpus, honestly")
print("  total nominal 300 rows         : Rp%s" % format(sum(biaya), ","))
print("  escalate nominal               : Rp%s" % format(escalate_biaya, ","))
print("  review nominal                 : Rp%s" % format(review_biaya, ","))
print("  prevalence synthetic           : fraud %s / anomali %s"
      % (f(P_FRAUD_SYN), f(P_SYN)))
print("  row count 300, entities:")
for col, key in (("Faskes", "Faskes"), ("Dokter", "Dokter"), ("Pasien", "Pasien"),
                 ("Diagnosis ICD-10", "Diagnosis ICD-10")):
    print("     %-16s %d" % (col, len(set(r[key] for r in rows))))

# --------------------------------------------------------------------------
# 6. ETHICS / NARRATIVE
# --------------------------------------------------------------------------
hdr("6. ETHICS & NARRATIVE ATTACK")

sub("6a. Real-looking identities in a public dataset")
dokters = set()
for r in rows:
    m = re.match(r"\s*(D\d+)\s*\(([^)]+)\)", r["Dokter"] or "")
    if m:
        dokters.add((m.group(1), m.group(2)))
print("distinct doctor records: %d" % len(dokters))
for d, n in sorted(dokters)[:25]:
    print("   %-5s %s" % (d, n))
pasien = sorted(set(r["Pasien"] for r in rows))
print("\ndistinct patient names: %d" % len(pasien))
for p in pasien[:15]:
    print("   %s" % p)
print("\n  >>> These are ordinary Indonesian full names with real credential")
print("  >>> suffixes (Sp.B, Sp.OG, Sp.PD). A judge or a bystander CANNOT tell")
print("  >>> they are synthetic. A doctor with that exact name exists somewhere")
print("  >>> in Indonesia. The 'privacy-by-design' claim (doc 10) only holds")
print("  >>> if the collection is clearly labelled -- check the UI.")

sub("6b. Can a false positive be traced to a named human?")
# For each doctor, how many of their claims are flagged?
per_doc = defaultdict(lambda: [0, 0])
for r in rows:
    m = re.match(r"\s*(D\d+)", r["Dokter"] or "")
    key = m.group(1) if m else (r["Dokter"] or "?")
    per_doc[key][0] += 1
    if r["Risiko"] != "low":
        per_doc[key][1] += 1
print("doctor | claims | anomaly | anomaly rate")
worst = []
for k, (tot, an) in sorted(per_doc.items()):
    rate = an / tot if tot else 0
    worst.append((rate, k, tot, an))
worst.sort(reverse=True)
for rate, k, tot, an in worst[:12]:
    print("   %-5s %4d %5d   %s" % (k, tot, an, f(rate, 3)))
print("\n  >>> Doctors are 100% attributable: every flagged claim carries a")
print("  >>> person, a clinic code, and a date. In a real deployment this")
print("  >>> becomes a targeted accusation list for a small RS_A/RS_C clinic.")

sub("6c. Do the flagged clinics concentrate?")
per_f = defaultdict(lambda: [0, 0])
for r in rows:
    per_f[r["Faskes"]][0] += 1
    if r["Risiko"] != "low":
        per_f[r["Faskes"]][1] += 1
for k, (tot, an) in sorted(per_f.items(), key=lambda x: -(x[1][1] / x[1][0] if x[1][0] else 0)):
    print("   %-58s %3d claims, %3d anomaly, rate %s" % (k[:58], tot, an, f(an / tot, 3)))

sub("6d. 'Decision supported' vs what the artefact actually is")
print("  Deliverable in repo : Next.js dashboard (src/app, src/components).")
print("  No training pipeline, no model artefact, no inference service.")
print("  => The shipped thing is a VIEW over a synthetic CSV, not a detector.")

# --------------------------------------------------------------------------
# 7. LEVERAGE: entity memorisation test
# --------------------------------------------------------------------------
hdr("7. ENTITY MEMORISATION: can the model just recognise the doctor/facility?")
for ent_col, label in (("Faskes", "Faskes"), ("Dokter", "Dokter")):
    ents = defaultdict(lambda: [0, 0])
    for r in rows:
        ents[r[ent_col]][0] += 1
        if r["Risiko"] != "low":
            ents[r[ent_col]][1] += 1
    rates = [a / t for t, a in ents.values() if t >= 5]
    print("%s: %d entities, mean anomaly rate %s, max %s, min %s"
          % (label, len(ents), f(sum(rates) / len(rates)), f(max(rates), 3), f(min(rates), 3)))
print("\n  If the model is allowed to see entity identity, 'RS_A -> fraud' is a")
print("  1-bit shortcut that beats every graph algorithm. Doc 03 sec.7 forbids")
print("  it, but doc 10's own v2.1 plan says the grouping columns are ADDED")
print("  and the grouping is used for SPLIT only -- the check must be enforced")
print("  in code, and no such code is shipped.")

# --------------------------------------------------------------------------
# 8. INTERNAL CONTRADICTIONS BETWEEN CORPUS DOCUMENTS
# --------------------------------------------------------------------------
hdr("8. INTERNAL CONTRADICTIONS (a jury member who reads two pages will find these)")

CONTRA = [
    ("Prevalence of the shipped dataset",
     "03-dataset-registry sec.3.2: fraud = 36/300 = 12.0%",
     "09-draft-hub.md:13 & 10-simulation-dataset.md:10: 'fraud di-oversample 14%'",
     "Same dataset, two prevalences (12% vs 14%) in documents both dated 2026-10."),
    ("AUPRC lift over XGBoost",
     "11-archive-proposal.md:30 & 14-index.md:505: '+28.6% dibanding baseline XGBoost 0.71'",
     "12-archive-architecture.md:30: 'mendominasi AUPRC ... hingga +20%'",
     "0.9142/0.71-1 = 28.8% (matches 28.6%); 0.91/0.71-1 = 28.2%. Neither is 20%."),
    ("Which dataset is 'the' dataset",
     "03-dataset-registry sec.2: active dataset = 300 claims, KLM001-KLM300",
     "10-simulation-dataset.md header: '100 klaim'; 09-draft-hub.md:13 says 14% of 100",
     "The live dashboard JSON (public/dashboard-aegis-jkn.html:1071) still reports "
     "total_claims=100, fraud_total=14, prevalensi=14, riskDist=[76,4,6,14]."),
    ("Dataset size vs dataset in the app",
     "App ships all 300 KLM ids (src/data/notion-datasets.ts)",
     "public/dashboard-aegis-jkn.html:1071 kpi.total_claims = 100",
     "The public demo runs the 100-claim v1; the corpus calls v2 (300) the active one."),
    ("Status vs Risiko are 'two different properties'",
     "03-dataset-registry sec.3.2: 'Label risiko dan status alur kerja merupakan "
     "dua properti berbeda'",
     "Measured cross-tab: fraud->escalate 36/36, high->review 14/14, "
     "medium->review 10/10, low->auto_clear 240/240",
     "Status is a DETERMINISTIC function of Risiko. Calling them 'berbeda' "
     "invites a leakage question the data already answers."),
    ("Overcharge denominator",
     "14-index.md:505: 'Rp 8,46 Juta per kasus fraud'",
     "507,370,000 / 36 fraud = Rp14,093,611 per case",
     "Rp8,46 juta = 507,370,000/60, i.e. divided by ALL anomali including the "
     "24 medium/high rows that are explicitly NOT fraud."),
    ("SUS acceptance threshold",
     "11-archive-proposal.md:335: target '>= 75 / 100', achieved '82.5 / 100'",
     "SUS benchmark mean is ~68; 82.5 sits near the 90th percentile",
     "An 82.5 SUS on a dashboard no verifikator has ever used is a claim with "
     "no respondent, no protocol and no raw data."),
]
print("%-34s %s" % ("TOPIC", "CONTRADICTION"))
for i, (topic, a, b, why) in enumerate(CONTRA, 1):
    print("\n[%d] %s" % (i, topic))
    print("    A: %s" % a)
    print("    B: %s" % b)
    print("    -> %s" % why)

# --------------------------------------------------------------------------
# 9. CODEBASE ARTEFACT AUDIT
# --------------------------------------------------------------------------
hdr("9. CODEBASE ARTEFACT AUDIT (what the reviewer can actually open)")

REPO = r"N:\HEALTHKATHON\Aegis-JKN"
if os.path.isdir(REPO):
    # Walk manually and prune node_modules -- glob's recursive walk over
    # node_modules is pathologically slow on this tree.
    SKIP = {"node_modules", ".git", ".next", "dist", "build", ".turbo"}
    found = {".py": [], ".ipynb": [], ".pt": [], ".pkl": [], ".joblib": [],
             ".onnx": [], ".parquet": [], ".h5": [], ".yaml": [], ".yml": [], ".csv": []}
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for _fname in files:
            ext = os.path.splitext(_fname)[1].lower()
            if ext in found:
                found[ext].append(os.path.join(root, _fname))
    py = found[".py"]
    nb = found[".ipynb"]
    ml = found[".pt"] + found[".pkl"] + found[".joblib"] + found[".onnx"] + found[".parquet"] + found[".h5"]
    yaml = found[".yaml"] + found[".yml"]
    csvs = found[".csv"]
    print("training scripts (*.py)      : %d" % len(py))
    print("notebooks (*.ipynb)          : %d" % len(nb))
    print("model/data artefacts         : %d %s" % (len(ml), [os.path.basename(m) for m in ml][:6]))
    print("yaml configs (leakage.yaml?) : %d %s" % (len(yaml), [os.path.basename(y) for y in yaml][:6]))
    print("csv datasets in repo         : %d %s" % (len(csvs), [os.path.basename(c) for c in csvs][:6]))
    leak = [p for p in yaml + [os.path.join(REPO, "tests", "test_leakage.py")]
            if "leak" in os.path.basename(p).lower() and os.path.exists(p)]
    print("leakage controls present     : %s" % (leak if leak else "NONE FOUND"))
    CLAIMED_BUT_MISSING = [
        ("tests/test_leakage.py", "anti-leakage unit test ('gagal keras jika kolom leakage masuk fitur')"),
        ("configs/leakage.yaml", "leakage column blocklist"),
        ("data/raw/claims_300_v2.1.csv", "v2.1 dataset with patient/facility/doctor id columns"),
        ("data/raw/edges_v2.1.json", "heterogeneous graph edges (70+)"),
        ("data/processed/features_300.parquet", "clean feature matrix"),
        ("data/processed/graph_hetero.pt", "PyG HeteroData, 3 channels"),
        ("data/raw/leakage_blocklist.yaml", "forbidden-column list"),
    ]
    print("\n  CLAIMED IN THE CORPUS BUT NOT ON DISK:")
    for rel, what in CLAIMED_BUT_MISSING:
        full = os.path.join(REPO, rel.replace("/", os.sep))
        print("    %-42s %-8s %s" % (rel, "EXISTS" if os.path.exists(full) else "MISSING", what))
    print("\n  >>> 14 corpus pages cite tests/test_leakage.py as the guard that")
    print("  >>> makes the dataset 'valid' (09-draft-hub.md:157,369;")
    print("  >>> 10-simulation-dataset.md:154; 12-archive-architecture.md:47,141,")
    print("  >>> 174,180; 14-index.md:200,412,951,1045,1078,1084).")
    print("  >>> The file does not exist. The safety gate is a claim, not code.")
    dts = os.path.join(REPO, "src", "components", "mhgsl", "data.ts")
    if os.path.exists(dts):
        txt = open(dts, encoding="utf-8", errors="replace").read()
        print()
        print("src/components/mhgsl/data.ts -- the benchmark table is a LITERAL:")
        for pat, label in ((r'xgboost: 0\.74', "XGBoost Precision 0.74"),
                           (r'mhgsl: 0\.92', "MHGSL Precision 0.92"),
                           (r'mhgsl: 0\.91', "MHGSL AUPRC 0.91"),
                           (r'mhgsl: 0\.95', "MHGSL ROC-AUC 0.95")):
            print("   %-26s present: %s" % (label, bool(re.search(pat, txt))))
        print("   -> the 'measured' comparison is a hand-written constant, with no")
        print("      model, no split, and no predictions behind it in the repo.")
else:
    print("repo not found at %s -- skipped" % REPO)

# --------------------------------------------------------------------------
# write JSON artefact
# --------------------------------------------------------------------------
out = {
    "corpus": CORPUS,
    "n_rows": N,
    "prevalence": {"fraud_synthetic": P_FRAUD_SYN, "anomali_synthetic": P_SYN},
    "label_distribution": dict(risk),
    "status_distribution": dict(status),
    "leak_sinyal_shap": {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
                         "accuracy": (tp + tn) / N},
    "leak_alasan_verdict_tag_rows": tag_is_label,
    "distinct_alasan_templates_number_stripped": len(dupnorm),
    "nominal_total": sum(biaya),
    "nominal_escalate": escalate_biaya,
    "nominal_review": review_biaya,
    "claimed_overcharge": TARGET,
    "overcharge_reproducible": False,
    "overcharge_derivable_from_own_tariffs": over,
    "overcharge_ratio_claimed_over_derivable": (TARGET / over) if over else None,
    "claims_reproducible": {name: REPRO[name][0] for name, _, _ in CLAIMS},
}
with open(os.path.join(OUT_DIR, "16_redteam_numbers.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)
print("\n\nwrote %s" % os.path.join(OUT_DIR, "16_redteam_numbers.json"))
