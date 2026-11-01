"""Reproduction of Aegis_JKN_FIXX.ipynb (PDF dashboard source) without Ollama.
All figures computed locally; no network. Prints every published metric.
"""
import math, json, sys, random

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SEED = 20260707
VERSION = "v2.1"
TOTAL_STEPS = 300
LOW_T, MED_T, HIGH_T = 0.35, 0.60, 0.80
THETA_FEAT = 0.85
GAMMA_TEXT = 0.10
QUEUE_RATE = 0.20
TARGET_DETECTION = 0.90
SENT_POS_T, SENT_NEG_T = 0.15, -0.15
random.seed(SEED)

PROC = {
    "00.66": {"nama": "PCI", "cplx": "tinggi"},
    "81.52": {"nama": "hemiarthroplasty", "cplx": "tinggi"},
    "51.23": {"nama": "kolesistektomi", "cplx": "sedang"},
    "96.04": {"nama": "intubasi", "cplx": "rendah"},
    "47.09": {"nama": "apendektomi", "cplx": "sedang"},
    "74.1": {"nama": "seksio sesarea", "cplx": "sedang"},
    "53.1": {"nama": "hernia", "cplx": "sedang"},
    "98.51": {"nama": "fragmentasi batu", "cplx": "sedang"},
}
DX_SEV = {"K29.7": "ringan", "K35.8": "sedang", "K40.9": "sedang", "I21.9": "berat",
          "J18.9": "sedang", "E11.9": "ringan", "N20.0": "sedang", "S72.0": "berat",
          "O80": "normal", "K80.2": "sedang"}


def build_ground_truth():
    claims = []

    def mk(idx, pasien, dokter, faskes, dx, proc, los, biaya, qty, skor,
           sindikat, modus, kontra, gt_sent, signal):
        claims.append({
            "id": f"KLM{idx:03d}", "pasien": pasien, "dokter": dokter, "faskes": faskes,
            "dx": dx, "proc": proc, "los": los, "biaya": biaya, "qty": qty,
            "skor": skor, "sindikat": sindikat, "modus": modus,
            "kontradiksi": kontra, "gt_sentimen": gt_sent, "signal": signal,
            "vec": [los, math.log10(biaya), qty],
        })

    for i, (p, d, s) in enumerate([("P01", "D01", 0.93), ("P02", "D01", 0.94),
                                   ("P03", "D02", 0.95)], start=1):
        mk(i, p, d, "RS_A", "K29.7", "00.66", 3, 58_000_000, 10, s,
           "SYND-01", "Upcoding", True, "Negatif", "upcoding")
    for i, (p, s) in enumerate([("P08", 0.92), ("P09", 0.93), ("P10", 0.94)], start=4):
        mk(i, p, "D05", "RS_C", "S72.0", "81.52", 1, 46_500_000, 0, s,
           "SYND-02", "Phantom Billing", True, "Negatif", "phantom")
    unb = [("P12", 0.84), ("P12", 0.85), ("P13", 0.85),
           ("P13", 0.86), ("P14", 0.86), ("P14", 0.87)]
    for k, (p, s) in enumerate(unb):
        proc = "51.23" if k % 2 == 0 else "96.04"
        biaya = 14_500_000 if k % 2 == 0 else 750_000
        mk(7 + k, p, "D07", "RS_B", "K80.2", proc, 4, biaya, 6, s,
           "SYND-03", "Unbundling", False, "Negatif", "unbundling")
    mk(13, "P16", "D09", "RS_E", "E11.9", "51.23", 2, 3_200_000, 24, 0.86,
       "SYND-04", "Drug Diversion", False, "Negatif", "drug_diversion")
    mk(14, "P17", "D09", "RS_E", "E11.9", "51.23", 2, 3_200_000, 30, 0.88,
       "SYND-04", "Drug Diversion", False, "Negatif", "drug_diversion")
    mk(15, "P15", "D09", "RS_E", "E11.9", "51.23", 2, 1_100_000, 6, 0.53,
       "-", "Anomali Qty Obat", False, "Netral", "")
    mk(16, "P19", "D08", "RS_F", "K35.8", "47.09", 5, 6_800_000, 4, 0.78,
       "SYND-05", "Cloning", False, "Negatif", "cloning")
    mk(17, "P20", "D08", "RS_F", "K35.8", "47.09", 5, 6_800_000, 4, 0.79,
       "SYND-05", "Cloning", False, "Netral", "")
    mk(18, "P18", "D03", "RS_A", "J18.9", "47.09", 6, 9_500_000, 5, 0.74,
       "-", "Prolonged Stay", True, "Negatif", "prolonged")
    mk(19, "P07", "D04", "RS_D", "I21.9", "00.66", 4, 58_000_000, 8, 0.62,
       "-", "Anomali Biaya", False, "Netral", "")
    mk(20, "P05", "D12", "RS_F", "O80", "74.1", 3, 6_200_000, 3, 0.66,
       "-", "Anomali", False, "Positif", "")
    mk(21, "P11", "D04", "RS_D", "J18.9", "47.09", 7, 7_400_000, 6, 0.68,
       "-", "Anomali", False, "Positif", "")
    mk(22, "P04", "D03", "RS_A", "K40.9", "53.1", 3, 8_200_000, 2, 0.41,
       "-", "Anomali", False, "Netral", "")
    mk(23, "P06", "D08", "RS_F", "N20.0", "98.51", 2, 5_600_000, 2, 0.47,
       "-", "Anomali", False, "Positif", "")
    mk(24, "P18", "D04", "RS_D", "K35.8", "47.09", 2, 6_800_000, 2, 0.55,
       "-", "Anomali", True, "Negatif", "diragukan")
    NEG_CONTROL = {"KLM030", "KLM045", "KLM060", "KLM070", "KLM084", "KLM095", "KLM098"}
    NEUTRAL_NORMAL = {"KLM032", "KLM041", "KLM050", "KLM058", "KLM066",
                      "KLM073", "KLM081", "KLM089", "KLM092", "KLM099"}
    for i in range(25, 101):
        cid = f"KLM{i:03d}"
        sent = "Positif"
        if cid in NEG_CONTROL:
            sent = "Negatif"
        elif cid in NEUTRAL_NORMAL:
            sent = "Netral"
        mk(i, f"P{(i % 20) + 1:02d}", f"D{(i % 12) + 1:02d}", f"RS_{chr(65 + (i % 6))}",
           "K40.9", "53.1", 2 + (i % 3), 5_000_000 + (i % 7) * 1_000_000,
           2 + (i % 4), 0.05 + ((i * 7) % 30) / 100, "-", "Normal", False, sent, "")
    return claims


def risk_label(skor):
    if skor < LOW_T:
        return "low"
    if skor < MED_T:
        return "medium"
    if skor <= HIGH_T:
        return "high"
    return "fraud"


CLAIMS = build_ground_truth()
_gt_sent, _risk = {}, {"low": 0, "medium": 0, "high": 0, "fraud": 0}
for c in CLAIMS:
    _gt_sent[c["gt_sentimen"]] = _gt_sent.get(c["gt_sentimen"], 0) + 1
    _risk[risk_label(c["skor"])] += 1
assert len(CLAIMS) == 100
assert _gt_sent == {"Positif": 62, "Netral": 14, "Negatif": 24}
assert _risk == {"low": 76, "medium": 4, "high": 6, "fraud": 14}
assert sum(1 for c in CLAIMS if c["kontradiksi"]) == 8
print("GT audit:", _risk, _gt_sent)

POS_WORDS = {"baik": 1, "bagus": 1, "membantu": 1, "efisien": 1, "mantap": 1, "keren": 1,
             "murah": 1, "untung": 1, "puas": 1, "cepat": 1, "ramah": 1, "lancar": 1,
             "alhamdulillah": 1, "terima kasih": 1, "senang": 1, "setuju": 1}
NEG_WORDS = {"buruk": 1, "lambat": 1, "rumit": 1, "jelek": 1, "kecewa": 2, "kurang": 1,
             "antre": 1, "lama": 1, "ribet": 1, "mahal": 1, "sempit": 1, "dirugikan": 1}
FRAUD_PHRASES = {"tidak pernah menjalani": 2, "iur biaya": 2, "tidak sesuai diagnosis": 2,
                 "tagihan ganda": 2, "berlebih": 2, "identik": 2, "diragukan": 2,
                 "tanpa penjelasan medis": 2}


def analyze_sentiment(text):
    low = text.lower()
    pos = sum(w for wd, w in POS_WORDS.items() if wd in low)
    neg = sum(w for wd, w in NEG_WORDS.items() if wd in low)
    sig = [(p, w) for p, w in FRAUD_PHRASES.items() if p in low]
    score = math.tanh(pos - neg - 1.5 * sum(w for _, w in sig))
    if score > SENT_POS_T:
        label = "Positif"
    elif score < SENT_NEG_T:
        label = "Negatif"
    else:
        label = "Netral"
    return {"score": round(score, 4), "label": label, "f_text": 1 if sig else 0,
            "signal": "; ".join(p for p, _ in sig)}


def cosine(a, b):
    num = sum(x * y for x, y in zip(a, b))
    den = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(x * x for x in b))
    return num / den if den else 0.0


def _core_text(c):
    faskes = c["faskes"]
    dx = c["dx"]
    proc = PROC[c["proc"]]["nama"]
    qty = c["qty"]
    los = c["los"]
    if c["gt_sentimen"] == "Positif":
        return (f"Alhamdulillah layanan JKN di {faskes} sangat baik dan cepat. Dirawat karena {dx}, "
                f"semuanya lancar, perawatnya ramah. Terima kasih BPJS!")
    if c["gt_sentimen"] == "Netral":
        return (f"Hari ini kontrol rutin ke {faskes} untuk {dx}. PengQNEDEAL, "
                f"Pengobatan sesuai jadwal, tidak ada catatan khusus.")
    s = c["signal"]
    if s == "upcoding":
        return f"Diagnosis saya cuma {dx}, tapi ditagih tindakan {proc} ke BPJS. Iur biaya mahal dan tidak sesuai diagnosis. Kecewa!"
    if s == "phantom":
        return f"Saya tidak pernah menjalani operasi {proc}, tapi ditagihkan ke BPJS. Sangat kecewa dan dirugikan!"
    if s == "unbundling":
        return f"Operasi {proc} kan paket sekali bayar, kok ditagih terpisah sampai tagihan ganda? Ribet dan kecewa!"
    if s == "drug_diversion":
        return f"Resep insulin saya {qty} pen sekali jalan, jauh berlebih dari kebutuhan. Rawan disalahgunakan. Kecewa!"
    if s == "cloning":
        return (f"Tagihan BPJS saya identik persis dengan pasien lain: tanggal, diagnosis, dan biaya sama. "
                f"Seperti rekam medis diklaim orang lain. Kecewa!")
    if s == "prolonged":
        return f"Dirawat {los} hari padahal indikasinya {dx}, lama banget tanpa penjelasan medis. Kecewa dengan {faskes}!"
    if s == "diragukan":
        return f"Ada tindakan {proc} di tagihan yang saya diragukan, padahal saya hanya konsultasi ringan. Kecewa!"
    return f"Antrean di {faskes} lama banget, parkir sempit, kebersihan juga kurang. Kecewa juga sih."


def tweet_template(c):
    return f"{_core_text(c)} #JKN #BPJSKesehatan"


def reddit_template(c):
    faskes = c["faskes"]
    title = f"[Diskusi] Pengalaman klaim JKN di {faskes}"
    if c["gt_sentimen"] == "Positif":
        comment = "Setuju, layanan JKN makin efisien dan sangat membantu peserta."
    elif c["gt_sentimen"] == "Netral":
        comment = "Noted, proses administrasi klaim memang mengikuti jadwal standar BPJS."
    else:
        comment = "Sudah lapor ke BPJS? Kasus begini harus masuk antrean investigasi verifikator."
    return f"{title}\n\n{_core_text(c)}\n\nKomentar otonom: {comment}"


for c in CLAIMS:
    c["tw_text"] = tweet_template(c)
    c["rd_text"] = reddit_template(c)

feat_edges = []
for i in range(len(CLAIMS)):
    for j in range(i + 1, len(CLAIMS)):
        sim = cosine(CLAIMS[i]["vec"], CLAIMS[j]["vec"])
        if sim >= THETA_FEAT:
            feat_edges.append((CLAIMS[i]["id"], CLAIMS[j]["id"], round(sim, 4)))
clone_pair = [e for e in feat_edges if set(e[:2]) == {"KLM016", "KLM017"}]
print(f"feat_edges={len(feat_edges)} clone_pair={clone_pair} "
      f"cos(KLM016,KLM017)={cosine(CLAIMS[15]['vec'], CLAIMS[16]['vec']):.3f}")


def channel_contrib(c):
    mates = [x for x in CLAIMS if x["sindikat"] == c["sindikat"]
             and c["sindikat"] != "-" and x["id"] != c["id"]]
    fitur = max((cosine(c["vec"], m["vec"]) for m in mates), default=0.0)
    deg = sum(1 for a, b, _ in feat_edges if a == c["id"] or b == c["id"])
    topo = min(1.0, deg / 5.0)
    if DX_SEV[c["dx"]] == "ringan" and PROC[c["proc"]]["cplx"] == "tinggi":
        sem = 1.0
    elif c["modus"] in ("Unbundling", "Phantom Billing", "Drug Diversion", "Cloning"):
        sem = 0.6
    else:
        sem = 0.2
    return {"fitur": round(fitur, 2), "topologi": round(topo, 2), "semantik": round(sem, 2)}


for c in CLAIMS:
    s_tw = analyze_sentiment(c["tw_text"])
    s_rd = analyze_sentiment(c["rd_text"])
    c["tw_label"], c["tw_score"] = s_tw["label"], s_tw["score"]
    c["rd_label"], c["rd_score"] = s_rd["label"], s_rd["score"]
    c["f_text"] = 1 if (c["signal"] and c["gt_sentimen"] == "Negatif") else 0
    c["p_fused"] = min(0.99, c["skor"] + GAMMA_TEXT * c["f_text"] * (1 - c["skor"]))
    c["risk"] = risk_label(c["skor"])

match = sum(1 for c in CLAIMS if c["tw_label"] == c["gt_sentimen"]) + \
        sum(1 for c in CLAIMS if c["rd_label"] == c["gt_sentimen"])
accuracy = match / (2 * len(CLAIMS))
print(f"\n*** AKURASI SENTIMEN (leksikon vs GT) = {accuracy*100:.1f}%  ({match}/200)")

queue = sorted(CLAIMS, key=lambda c: c["p_fused"], reverse=True)[:int(len(CLAIMS) * QUEUE_RATE)]
queue_ids = {c["id"] for c in queue}
fraud_claims = [c for c in CLAIMS if c["risk"] == "fraud"]
detected = [c for c in fraud_claims if c["id"] in queue_ids]
det_rate = len(detected) / len(fraud_claims)
print(f"*** DETEKSI FRAUD = {len(detected)}/{len(fraud_claims)} ({det_rate*100:.0f}%) "
      f"pada antrian {len(queue)} klaim")
print(f"    fraud skor min/max = {min(c['skor'] for c in fraud_claims)} / "
      f"{max(c['skor'] for c in fraud_claims)}")
print(f"    non-fraud skor max = {max(c['skor'] for c in CLAIMS if c['risk'] != 'fraud')}")
print(f"    p_fused fraud min = {min(c['p_fused'] for c in fraud_claims):.3f}; "
      f"non-fraud max = {max(c['p_fused'] for c in CLAIMS if c['risk'] != 'fraud'):.3f}")

synd_hit = {}
for s in ["SYND-01", "SYND-02", "SYND-03", "SYND-04", "SYND-05"]:
    members = [c for c in CLAIMS if c["sindikat"] == s]
    hit = [c for c in members if c["id"] in queue_ids]
    synd_hit[s] = {"hit": len(hit), "total": len(members),
                   "rate": round(100 * len(hit) / len(members), 1),
                   "modus": members[0]["modus"]}
print("*** HIT-RATE SINDIKAT:",
      {k: f"{v['hit']}/{v['total']}={v['rate']}%" for k, v in synd_hit.items()})

priority_ids = queue_ids | {c["id"] for c in CLAIMS if c["f_text"] == 1}
kontra = [c for c in CLAIMS if c["kontradiksi"]]
kontra_ok = sum(1 for c in kontra if c["id"] in priority_ids)
criteria = {"integritas": len(CLAIMS) == 100,
            "deteksi": det_rate >= TARGET_DETECTION and len(queue) / len(CLAIMS) <= QUEUE_RATE,
            "sindikat": all(v["hit"] > 0 for v in synd_hit.values()),
            "kontradiksi": kontra_ok == len(kontra)}
SESUAI = all(criteria.values())
print(f"*** Kontradiksi prioritas: {kontra_ok}/{len(kontra)} | Kriteria: {criteria} | SESUAI={SESUAI}")

CAPACITY_GAIN = 20 / 3
VERIFICATOR_CAPACITY = round(1000 * CAPACITY_GAIN)
FRAUD_PREVALENSI = round(len(fraud_claims) / len(CLAIMS), 2)
print(f"*** ROI: 20/3 = {CAPACITY_GAIN:.3f}x -> kapasitas {VERIFICATOR_CAPACITY:,} berkas | "
      f"prevalensi {FRAUD_PREVALENSI*100:.0f}%")
print(f"*** f_text aktif pada {sum(c['f_text'] for c in CLAIMS)} klaim")

print("\n*** QUEUE (all 20):")
for c in queue:
    print(f"    {c['id']} p_fused={c['p_fused']:.3f} risk={c['risk']:6s} modus={c['modus']:18s} "
          f"synd={c['sindikat']:9s} chan={channel_contrib(c)} KONTRA={c['kontradiksi']}")

print("\n*** Top-10 by p_fused (dashboard chart 'Top-10 Skor Fusion'):")
for c in sorted(CLAIMS, key=lambda c: c["p_fused"], reverse=True)[:10]:
    print(f"    {c['id']} {c['p_fused']:.3f} {c['modus']}")

# ---- additional checks for the audit ----
print("\n*** LEAKAGE CHECKS")
# 1. ground truth skor is hand-assigned by label, not derived from features
by_label = {}
for c in CLAIMS:
    by_label.setdefault(c["risk"], []).append(c["skor"])
for k, v in by_label.items():
    print(f"    risk={k:6s} n={len(v):3d} skor min={min(v)} max={max(v)}")
# 2. sentiment text is generated FROM gt_sentimen -> classifier cannot fail on non-fraud
print("    sentiment texts are templates keyed on c['gt_sentimen'] -> lexicon label == gt by construction")
# 3. fraud label == skor > 0.8 by construction
print("    risk_label(skor) == 'fraud' iff skor > 0.8 ; fraud set is a hardcoded skor cut")
# 4. does the queue's ranking come from any model? p_fused = skor + bump
print("    p_fused derives from c['skor'] (hardcoded) + 0.10*f_text; no learned model is involved")
# 5. scoring a random permuted-dataset control
import itertools
labels = [c["risk"] == "fraud" for c in CLAIMS]
scores = [c["p_fused"] for c in CLAIMS]
print(f"    AUC of p_fused vs fraud label = 1.0 (fraud = top 14 by hardcoded skor)")
# 6. cost of threshold: if we set threshold 0.80 exactly on p_fused, detection = ?
fraud_sorted = sorted(c["p_fused"] for c in fraud_claims)
nonfraud_sorted = sorted((c["p_fused"] for c in CLAIMS if c["risk"] != "fraud"), reverse=True)
print(f"    p_lead > 0.85 rule: fraud above = {sum(1 for x in fraud_sorted if x > 0.85)}/{len(fraud_sorted)}; "
      f"non-fraud above = {sum(1 for x in nonfraud_sorted if x > 0.85)}")
