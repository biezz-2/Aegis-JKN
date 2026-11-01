# 06 - Audit Metodologi & Protokol Evaluasi

## Aegis-JKN: Protocols 08, 10, 03, 02 vs implementasi aktual

| Aspek | Nilai |
|---|---|
| Sumber protokol | `analysis/corpus/08-training-protocol.md` (84 baris), `analysis/corpus/10-simulation-dataset.md` (213 baris), `analysis/corpus/03-dataset-registry.md` (111 baris), `analysis/corpus/02-architecture.md`, `analysis/corpus/05-decision-scope.md`, `analysis/corpus/06-research-notes.md` |
| Data primer | `analysis/corpus/claims_v2_live.csv` - 300 baris × 29 kolom, SHA-256 `d6fb95b9fbfb6bf47e9a99bcf57df0e38b00a13758b6d3ac14779e64a6121119` |
| Data implementasi | `mechine-learning-deep-learning/datasets/claims_300_v2.1.csv` - 300 baris × 31 kolom, SHA-256 `37cf22369ebf7a3c616219cb49b9c4406f00d75286b38cbf6c08b844e27fd4e8` |
| Kode implementasi | `mechine-learning-deep-learning/notebooks/Aegis-JKN.ipynb` (22 sel), `mechine-learning-deep-learning/backend/src/data/pipeline.py`, `backend/requirements.txt` |
| Skrip hitung | `analysis/reports/scripts/06_stats.py` (stdlib saja: `csv`, `math`, `random`, `statistics`, `collections`, `re`, `hashlib`, `os` - tanpa pandas) |
| Perintah replikasi | `python -X utf8 analysis/reports/scripts/06_stats.py` |
| Tanggal audit | 22 Oktober 2026 |
| Nature laporan | **Hanya masalah.** Laporan audit metodologi: seluruh isi hanya temuan, gap, dan konflik. Tidak ada bagian "hal yang sudah baik". |

---

## 1. Ringkasan Eksekutif

Protokol evaluasi Aegis-JKN tertulis rapi dan koheren secara normatif, tetapi **tidak memiliki satu pun artefak eksekusi untuk membuktikan apakah protokol itu bisa dijalankan**. Yang diuji adalah dokumen, bukan model. Hasil audit ini menunjukkan:

**A. Target ground truth tidak pernah ada.** Label `Risiko` pada 300 baris adalah keluaran aturan skor (bijektif terhadap `Skor Fraud`), `Status` adalah coarsening deterministik dari `Risiko` (akurasi 300/300), dan `Alasan` adalah label yang ditulis ulang dalam bentuk prosa. Blokir anti-leakage resmi (03 §7) sudah benar dalam satu hal: ia memblokir semua kolom yang **berlabel eksplisit**. Yang bocor justru kolom yang **tidak terlihat seperti label** - `Catatan` (kosong ⇔ `Risiko`=low, 240/240), `Skor Sentimen` (AUROC 0.909), `Sentimen` (100% turunan `Skor Sentimen`), `Kontradiksi Narasi` (flag yang disetel dari ground truth), `Umpan Balik Pasien` (keyword keluhan → 15/17 fraud), plus `claim_id` (KLM001–024 = 100% anomali). Blokir 7 kolom resmi **tidak** memblokir satupun dari ini.

**B. Angka kunci proyek tidak dapat direproduksi.** `06-research-notes.md` baris 42–43 sudah mencatat AUPRC 0,9142 dan "peningkatan AUPRC dibanding baseline" sebagai belum dapat direproduksi. Audit ini menemukan alasannya: benchmark di `Aegis-JKN.ipynb` sel 13 dilatih **dan** dievaluasi pada `X_clean` yang sama (`xgb_clf.fit(X_clean, y_target)` lalu `predict_proba(X_clean)`), tanpa test set tersisih, dengan target 38 kasus yang berbeda dari target evaluasi 36 kasus. Setiap metrik pada tabel benchmark adalah metrik in-sample.

**C. Ukuran sampel tidak mendukung protokol yang dirancang.** 300 baris dengan prevalensi 12% memberi 36 positif. Pada prevalensi produksi 3–7% (rentang yang dipakai 10 baris 175/180), jumlah positif turun ke 9–21. Lebar CI 95% AUPRC pada AUPRC 0,90 = **0,561** (prevalensi 3%) hingga 0,216 (12%). AUROC CI 95% = [0,764 ; 1,036] pada 3% - batas atas melewati 1. Perbedaan AUPRC 0,92 vs 0,88 yang menjadi kriteria "MHGSL menang" **tidak signifikan** pada semua ukuran sampel yang tersedia.

**D. Empat dari sepuluh kriteria "SESUAI" secara matematis mustahil atau bersirkular.** Kriteria 4 (hit-rate > 0 semua sindikat) mustahil karena SYND-05 berlabel `high`, bukan `fraud`. Kriteria 5 (konsistensi SHAP vs kolom `Alasan`) tidak teruji karena SHAP tidak pernah dihitung di kode mana pun, dan `Alasan` itu sendiri adalah label. Kriteria 6 (8 klaim kontradiksi) memiliki target ID yang di-hardcode di sel 15, jadi yang diuji adalah aturan teks, bukan model. Kriteria 3 tidak terukur karena benchmark in-sample.

**E. Protokol 8 minggu tidak memiliki prasyarat yang terpenuhi.** 7 dari 10 artefak v2.1 yang dijanjikan 10 baris 183–195 tidak ada di disk. `configs/leakage.yaml` tidak ada; `tests/test_leakage.py` tidak ada; `edges_v2.1.json`, `text_gt_v2.1.csv`, `features_300.parquet`, `metadata.json` tidak ada. `xgboost`, `imbalanced-learn`, `google-generativeai`, `ctgan` tidak ada di `backend/requirements.txt`. Kolom `seed`/`version`/`timestamp` yang dijanjikan tidak ada di CSV v2.1.

### Tabel severity

25 temuan. Kolom "Lokasi" menunjuk ke tempat temuan diuraikan; 20 di antaranya adalah baris tabel inkohérensi §3 (I-01…I-20), 5 sisanya temuan lintas-bagian yang diberi rujukan seksi.

| Severity | Jumlah | Lokasi | Cakupan |
|---|---|---|---|
| **KRITIS** | 7 | I-01, I-05, I-07, I-10, I-17, I-19, §5.2 | Target = keluaran aturan (bukan adjudikasi); `Status` deterministik terhadap `Risiko` (300/300); 4 versi daftar blokir berbeda; benchmark in-sample tanpa test set tersisih; edge graf dibangun dari kolom label (`sindikat`); 7 dari 10 artefak v2.1 hilang; kriteria sindikat mustahil (SYND-05 = `high`) |
| **TINGGI** | 8 | I-02, I-04, I-08, I-09, I-11, I-13, I-16, §6 | KLM115 mendispute ambang 0,80; tabel sindikat meleset 5/9; normalisasi di luar fold; θ_feat 0,85 vs 0,5; prevalensi 12% vs 3–7% tanpa uji; klaim QA 03 §6/77 salah; 4 dependensi fase tidak terpasang; daya statistik: CI AUPRC lebar 0,561 & 2 fold LOGO tanpa positif |
| **SEDANG** | 7 | I-03, I-06, I-12, I-14, I-18, I-20, §4.1 | 24 anomali v1 hilang status di v2.1 tanpa dicatat; `review_action` tidak pernah diuji; `Kontradiksi Narasi` 12 vs 8; LOS 0 mengaburkan "tidak berlaku" vs sinyal fraud; kolom `seed`/`version`/`timestamp` tidak ada; 2 dari 7 temuan QA 03 §6 meleset; 7+ kolom bocor di luar blokir resmi |
| **RINGAN** | 3 | I-15, §2.3, §8 | Angka 10 §108 (distribusi sentimen) usang tanpa penanda versi; 0 dari 6 artefak Tahap 0–5 (08 baris 30–35) ada di disk; checksum & seed belum dilampirkan (03 §11 butir 6 masih checkbox terbuka) |
| **Total** | **25** | | |

---

## 2. Rekonstruksi Protokol Evaluasi

### 2.1 Sumber split & ground truth

| Komponen | Protokol | Sumber |
|---|---|---|
| Target | `ground_truth_fraud` "yang diperiksa manusia dan memiliki provenance"; status "Belum disahkan" | 08 baris 15 |
| Sumber label | Risiko + Status tersedia "tetapi perlu audit asal label" | 08 baris 8 |
| Split | "cross-validation berulang atau stratified cross-validation setelah label diaudit"; jika kasus dari grup sama → split tingkat grup; "sisihkan test set final dan jangan mengubah threshold berdasarkan hasil test" | 08 baris 37 |
| Split kelompok | GroupKFold (pasien) + LeaveOneGroupOut (faskes) | 10 baris 156–157; 02 baris 67–68 |
| Metrik | PR-AUC, precision, recall, F1, confusion matrix, FPR, calibration, interval ketidakpastian; jangan Accuracy saja | 08 baris 38; 02 baris 74 |
| Baseline | rule sederhana, logistic regression, model pohon interpretable | 08 baris 33 |
| Artefak wajib | `manifest.json`, `label_audit.csv`, `data_quality_report.md`, `train.py`+`metrics.json`, `evaluation_report.md`, `review_log.csv` | 08 baris 30–35 |
| Repro | 10 butir wajib (nama/versi, waktu ekspor, jumlah baris, checksum, kamus data, daftar kolom, definisi target+ambang, aturan pembersihan, ID anggota split, seed+versi kode) | 03 baris 87–97 |
| Kriteria "SESUAI" | 7 kriteria, konsekuensi 3 tingkat (TIDAK SESUAI / DESAIN BELUM TERBUKTI UNGGUL) | 10 baris 196–206 |

### 2.2 Implementasi aktual (dari `Aegis-JKN.ipynb` + `pipeline.py`)

| Komponen | Implementasi | Deviasi dari protokol |
|---|---|---|
| Target latih | `y_target = (is_fraud==1) \| (sindikat != 'none')` → **38** kasus (sel 11) | Ground truth fraud = 36. 2 kasus (KLM016/017) bukan fraud |
| Target evaluasi | `y_fraud_gt = is_fraud` → **36** kasus (sel 11) | - |
| Sumber `is_fraud` | `pipeline.py:167` `df['is_fraud'] = (df['risiko'].str.lower()=='fraud')` | Target = label aturan, bukan label yang sah |
| Split | GroupKFold(5) by `pasien_id`; LOGO by `faskes_id` (sel 11) | Sesuai 10/02 |
| Graf | Dibangun di **seluruh 300 baris** (sel 7: `construct_multichannel_graphs(df_claims, X_clean, θ=0.85)`), dipakai utuh di setiap fold | 58,2% edge `A_top` melintasi fold GroupKFold(pasien) |
| Skala | `scaler.fit_transform(feat_df.values)` di luar loop fold (sel 5); `pipeline.py:229` `self.scaler.fit_transform(raw_X)` di atas 300 baris | 02 baris 69 mensyaratkan seluruh normalisasi hanya memakai data tiap fold |
| Benchmark | `xgb_clf.fit(X_clean, y_target)` → `predict_proba(X_clean)` (sel 13) | Tidak ada test set tersisih; 08 baris 37 mensyaratkan test set final |
| XAI | Tidak ada komputasi SHAP di kode mana pun | 10 baris 169 menjanjikan SHAP per-saluran |
| Teks | `TARGET_CONTRADICTION_IDS` = 8 ID hardcoded (sel 15) | Kriteria 6 menguji aturan, bukan model |
| Blokir | `FORBIDDEN_COLUMNS` 9 item + assertion substring-only (sel 5) | Assertion hanya cek nama fitur, bukan nilai; `LEAKAGE_COLUMNS` di `pipeline.py:37` tidak pernah dipakai (1 kemunculan di repo) |

### 2.3 Tahapan 0–5 (08 baris 29–35) vs artefak di disk

| Tahap | Artefak wajib | Ada? |
|---|---|---|
| 0. Bekukan sumber | `manifest.json` | ✗ |
| 1. Audit label | `label_audit.csv` | ✗ |
| 2. Siapkan fitur | `data_quality_report.md` | ✗ |
| 3. Baseline | `train.py`, `metrics.json` | ✗ (`backend/src/test_self_check.py` satu-satunya test; tidak ada `tests/` directory) |
| 4. Evaluasi | `evaluation_report.md` | ✗ |
| 5. Human review | `review_log.csv` | ✗ |

**0 dari 6 artefak wajib 08 ada di repo.**

---

## 3. Tabel Inkohérensi

| # | Topik | Sumber A | Sumber B | Konflik | Dampak | Sumber perbaikan |
|---|---|---|---|---|---|---|
| I-01 | Definisi fraud | 08 baris 15: target = `ground_truth_fraud` "diperiksa manusia dan memiliki provenance" | 10 baris 113 & CSV: label = `Risiko` dari `Skor Fraud`; `pipeline.py:167` `is_fraud = (risiko=='fraud')` | Protokol mensyaratkan label independen; implementasi memakai label aturan sebagai target | Seluruh metrik yang dipublikasikan mengukur reproduksi aturan, bukan deteksi. **KRITIS** | 08 baris 21 (kolom adjudikasi) + 02 D-01 |
| I-02 | Ambang skor 0,80 | 10 baris 9 & 113: "di atas 0,8" / "lebih dari 0.8" = fraud | CSV: KLM115 `Skor Fraud`=0,80, `Risiko`=fraud | Baris tepat 0,80 dilabeli fraud, melanggar "> 0,8" | 1 baris mendispute klaim QA 03 §6 baris 77. 03 §4 baris 46 sudah memperingatkan ambang ambigu tapi tidak dikunci. **TINGGI** | 03 §4 (kunci ambang + versi) |
| I-03 | Ground truth v1 | 10 baris 8: anomali = KLM001–KLM024 (14 fraud + 10 medium/high) | 10 baris 113: total anomali v2 = 60 = 36 fraud + 14 high + 10 medium | 24 anomali v1 (KLM015–024: 6 high + 4 medium) **tidak lagi** berstatus ground truth anomali di v2.1; 10 tidak mencatat penurunan ini | Revisi ground truth terjadi tanpa changelog (03 §10 baris 104: "Berikutnya: Belum ditetapkan"). **SEDANG** | 10 baris 113 + 03 §10 |
| I-04 | Tabel sindikat | 10 baris 134–142 (SYND-01..09: pasien, dokter, faskes, skor) | CSV: **5 dari 9** meleset pada ≥1 field | SYND-03 (skor 0,84–0,87 → 0,85–0,87); SYND-06 (pasien P21–P24 → P21–P22; skor 0,85–0,90 → 0,89–0,92); SYND-07 (pasien P25–P28 → P23–P24; skor 0,82–0,87 → 0,82–0,85); SYND-08 (pasien P29–P34 → P25–P26; skor 0,75–0,80 → 0,86–0,89); SYND-09 (dokter D16 → D19; pasien P35–P40 → P27; skor 0,78–0,83 → 0,80–0,84) | Ground truth skenario v2.1 bukan data yang dianalisis. Kriteria hit-rate per sindikat dihitung terhadap ground truth yang salah. Faskes & rentang ID klaim selalu cocok - yang bergeser adalah entitas klinis dan skor. **TINGGI** | 10 baris 132–144 (tabel ground truth) |
| I-05 | Blokir leakage | 03 §7 baris 84: 8 kolom | 10 baris 127: 7 kolom ("Alasan" hilang); 08 baris 22: 4 kolom eksplisit + frasa umum; notebook sel 5: 9 kolom | Empat daftar blokir berbeda dalam empat dokumen | `Alasan` - kolom yang 100% menentukan label - tidak diblokir di 10 v2.1, yang justru jadi acuan kesiapan ML. **KRITIS** | 03 §7 (satu daftar kanonik) |
| I-06 | Definisi target | 02 baris 61–64: dua target terpisah `risk_triage` (4 kelas) dan `review_action` (3 kelas), "tidak boleh dipakai secara bergantian" | Notebook: `is_fraud` biner untuk semua; `Status` tidak pernah dipakai sebagai target | Yang dianalisis adalah turunan biner `risk_triage`, bukan `review_action`; tidak ada eksperimen pada target kedua | 02 §5.1 tidak terpenuhi. **SEDANG** | 02 baris 61 + 08 baris 15 |
| I-07 | Ekspektasi split | 08 baris 37: "sisihkan test set final dan jangan mengubah threshold berdasarkan hasil test" | Notebook sel 13: seluruh model dilatih & dinilai pada `X_clean` yang sama | Tidak ada test set final; threshold 0,5 dipakai di `compute_benchmark_metrics` tanpa validasi | Semua angka benchmark terlalu optimis; tidak mengukur generalisasi. **KRITIS** | 08 baris 37 |
| I-08 | Normalisasi per-fold | 02 baris 69: "seluruh pemilihan fitur, normalisasi, thresholding, dan kalibrasi hanya menggunakan data yang diizinkan dalam setiap fold" | Notebook sel 5: `scaler.fit_transform(feat_df.values)` di luar loop; `pipeline.py:229` scaler fit di atas 300 baris | Normalisasi dan frekuensi kode dihitung dengan informasi seluruh data | Kebocoran informasi fitur lintas fold; AUROC/AUPRC bias ke atas. **TINGGI** | 02 baris 69 |
| I-09 | Ambang kanal fitur | 10 baris 166 & notebook sel 7: `θ_feat = 0.85` | `pipeline.py:251` & `pipeline.py:327`: `theta_feat: float = 0.5` | Backend dan notebook menghitung kanal A_feat berbeda pada data yang sama | Dua implementasi "resmi" tidak dapat direproduksi satu sama lain. **TINGGI** | 10 baris 166 |
| I-10 | Kanal semantik | 02 baris 72: semantic = metapath diagnosis→prosedur→RS | `pipeline.py:293-307`: edge ditambahkan bila `sindikat` sama | Backend membangun edge graf dari kolom label | Graf backend berisi informasi ground truth. **KRITIS** | 02 baris 72 + 03 §7 |
| I-11 | Prevalensi | 10 baris 10 & 175 & 180: "produksi 3–7%", "AUPRC pada prevalensi 3–7% (downsampling)" | 10 baris 113: 36 fraud = 12%; 03 baris 100 & 06 baris 40: 12% bukan estimasi, 3–7% "belum layak digunakan sebagai fakta" | **MASALAH:** downsampling 12%→3% menghapus 25 dari 36 kasus = 69% sinyal; tidak ada pipeline downsampling di kode | Selisih prevalensi 2–4× menurunkan n_pos ke 9–21; CI AUPRC melebar hingga 0,561. **TINGGI** | 10 baris 178–181 + 06 baris 40 |
| I-12 | Kontradiksi Narasi | 10 baris 107: 8 klaim (KLM001–006, 018, 024) | CSV: **12** baris `True` (tambah KLM105–108/SYND-07) | Kriteria 6 menguji 8 ID, data menyediakan 12 | Kriteria tidak mengukur recall model atas ground truth yang benar. **SEDANG** | 10 baris 107 |
| I-13 | QA klaim | 03 §6 baris 77: "tidak ditemukan ketidaksesuaian antara label risiko dan rentang skor" | CSV: KLM115 skor 0,80 = fraud | Klaim QA salah | Mendorong ground truth. **TINGGI** | 03 §6 baris 77 |
| I-14 | QA LOS | 03 §6 baris 78: "109 baris memiliki kolom LOS hari kosong" | CSV: 0 baris kosong; 109 baris bernilai `"0"` | 0 adalah nilai LOS sah untuk rawat jalan (106 dari 109 baris), bukan missing | Penanganan missingness (02 §7, 03 §11 butir 4) belum diputuskan; 3 baris LOS=0 adalah kasus rawat inap yang justru fraud. **SEDANG** | 03 §11 |
| I-15 | Penanda sentimen | 10 baris 108: "Distribusi sentimen: 62 positif · 14 netral · 24 negatif" | CSV 300 baris: 170 positif / 58 netral / 72 negatif; 100 baris pertama: 62/14/24 ✓ | Angka 10 §108 hanya berlaku untuk 100 baris lama, sekarang dipakai sebagai spesifikasi 300 baris | Angka usang tanpa penanda versi. **RINGAN** | 10 baris 108 |
| I-16 | Dependensi Fase 1–3 | 10 baris 163, 172, 212: XGBoost + SMOTE, Gemini API, DP-CTGAN | `backend/requirements.txt`: tidak ada `xgboost`, `imbalanced-learn`, `google-generativeai`, `ctgan`; tidak ada kode SMOTE/Gemini/CTGAN di repo | Prasyarat fase tidak terpasang | Fase 1–3 tidak dapat dijalankan sesuai rencana. **TINGGI** | 10 baris 207–213 |
| I-17 | Artefak v2.1 | 10 baris 183–195: 8 file | Disk: hanya `claims_300_v2.1.csv` (7 dari 10 hilang) | `configs/leakage.yaml`, `tests/test_leakage.py`, `edges_v2.1.json`, `text_gt_v2.1.csv`, `features_300.parquet`, `metadata.json` tidak ada | Gate anti-leakage dijanjikan (`unit test gagal keras`) tidak ada; 10 baris 115 menyebut "10 kekurangan kritis yang harus diperbaiki" tanpa bukti perbaikan. **KRITIS** | 10 baris 114–131 |
| I-18 | Kolom metadata v2.1 | 10 baris 122–125, 187: `seed`, `version`, `timestamp` | `claims_300_v2.1.csv`: 31 kolom, ketiga kolom tidak ada | Butir 10 checklist repro ("seed dan versi kode") tak terpenuhi | 03 §8 butir 1, 10. **SEDANG** | 10 baris 187 |
| I-19 | Kriteria sindikat | 10 baris 196–206: kriteria 4 "Setiap SYND-01-SYND-09 hit-rate > 0" | SYND-05 (KLM016–017) berlabel `high` | Target fraud tidak pernah mencakup SYND-05 | Kriteria mustahil; `assert all_positive_hit` di sel 13 akan gagal bila `y_fraud_gt` dipakai, dan lolos hanya karena model dilatih pada `y_target` (38) yang **memuat** SYND-05. **KRITIS** | 10 baris 201 + label data |
| I-20 | Rekonsiliasi 03 §6 | 03 §6 baris 73–81 (7 temuan QA) | Hitung ulang dari CSV | 6/7 cocok; 2 meleset: baris 77 (KLM115) & baris 78 (0 vs kosong) | Klaim QA perlu dikoreksi. **SEDANG** | 03 §6 |

---

## 4. Audit Anti-Leakage Lanjutan

Blokir resmi 03 §7 (8 kolom) + 10 v2.1 (7 kolom) + 08 baris 22 (4 eksplisit) + notebook sel 5 (9 kolom) **tidak menemukan** kolom bocor berikut. Semua kolom di bawah **tidak** diblokir di dokumen mana pun, dan tiga di antaranya adalah proksi label sempurna.

### 4.1 Tabel temuan

| Kolom | Diblokir resmi? | Bukti kebocoran (dihitung ulang) | Dampak | Rekomendasi |
|---|---|---|---|---|
| **`Catatan`** | Tidak | Kosong ⇔ `Risiko`=low, **240/240 bijektif** (0 baris low punya Catatan; 60 baris non-low semuanya punya). AUROC(fraud vs low) = **1,000** | Proksi label sempurna; model cukup "is Catatan empty" | **TAMBAHKAN blokir** |
| **`Skor Sentimen`** | Tidak | AUROC(fraud vs low) = **0,909**; AUROC(anomali vs low) = 0,850. Rerata fraud = −0,374 vs low = +0,459 | Model sentimen menebak fraud tanpa bukti klinis | **TAMBAHKAN blokir** |
| **`Sentimen`** | Tidak | **100% turunan** `Skor Sentimen`: `Sentimen = band(Skor Sentimen, \|s\|≤0,15→netral)`, 0/300 penyimpangan. AUROC = 0,732 | Redundan dari `Skor Sentimen` | **TAMBAHKAN blokir** |
| **`Umpan Balik Pasien`** | Tidak | 17 baris memuat keyword keluhan → 15 fraud + 2 high. **P(fraud \| keluhan-kunci) = 15/17 = 88,2%**. Teks nyaris identik per skenario | Saluran teks "mendeteksi" label | **TAMBAHKAN blokir** atau etiket |
| **`Kontradiksi Narasi`** | Tidak | Flag biner: 12 `True` = 10 fraud + 2 high; 288 `False` = 240 low + 24 high + 24 fraud. AUROC = 0,639 | Flag yang disetel dari ground truth; 10 baris 106 menyebutnya "ground truth label" | **TAMBAHKAN blokir** (atau jadikan target eksplisit) |
| **`Name` / `claim_id`** | Tidak | KLM001–KLM024 = **24/24 anomali** (P(fraud)=58,3%); 36 anomali sisanya berada di KLM101–KLM136. AUROC numerik = 0,194 (arah terbalik, tetap informatif) | Kebocoran urutan generator; model ID bisa menebak label | **Blokir sebagai fitur**, izinkan sebagai metadata split |
| **`_last_edited`** | Tidak | 3 timestamp; seluruh 36 fraud berada di 2 timestamp | Artefak pipeline generator, bukan data klinis | **Buang** |
| **`faskes_id` / `dokter_id` (freq-enc)** | Hanya sebagai ID (03 §7 baris 85) | `pipeline.py:222-226` menghitung frekuensi. RS_D = 0/14 fraud, RS_F = 0/32 fraud, RS_B = 6/21 = 28,6% | Frekuensi = proksi label, dan tetap dipakai di backend yang tidak memblokir kolom apa pun | **Blokir freq-enc**; izinkan ID hanya sebagai metadata split |
| **`Pasien` (nama + id)** | Tidak | Nama sintetis tertanam di rich text; P01–P20 adalah ground truth v1 (10 baris 6) | Entitas bisa dihafal | **Blokir nama**; ID hanya metadata split |
| **`Prosedur ICD-9-CM` = 96.04** | Tidak | n=3, **3/3 fraud - presisi 100%**. P(fraud\|kode)=1,000 (AUROC biner hanya 0,542 karena 33 fraud lain bernilai 0) | Satu nilai kode = penanda fraud | Audit artefak generator |
| **Pasangan (dx, prosedur)** | Tidak | 2 pasangan dengan presisi 100%, n≥2: (K29.7 + 00.66) dan (K80.2 + 96.04), masing-masing 3/3 fraud | Kebocoran semantik pada pasangan | Audit artefak generator; laporkan sebagai batas |
| `Alasan` | 03 §7 ya; **10 v2.1 tidak** | Prefix `FRAUD`/`ANOMALI`/`NORMAL` menentukan `Risiko` **300/300** | Sudah diblokir di 03, hilang di 10 | **Sinkronkan 10 baris 127** |
| `Modus` | Ya | Terisi ⇔ `Risiko`≠low, 60/60 | - | Tetap blokir |
| `Sindikat` | Ya | P(fraud \| Sindikat terisi) = 34/36 = **94,4%**; bukan subset fraud (SYND-05 = high; KLM121/122 = fraud tanpa sindikat) | - | Tetap blokir |
| `Sinyal SHAP` | Ya | "tidak ada sinyal dominan" ⇔ `Risiko`=low, 300/300 | - | Tetap blokir |
| `Kontribusi Saluran` | Ya | max(low)=0,06 < min(medium)=0,09 < min(fraud)=0,15 → separabel sempurna lewat max-channel | - | Tetap blokir |

### 4.2 Temuan struktural

1. **Blokir resmi bertumpu pada asumsi bahwa label selalu terlihat sebagai label.** Semua 8 kolom yang diblokir 03 §7 memang adalah keluaran proses deteksi. Kebocoran yang tidak tertangkap datang dari kolom yang *terlihat* netral (catatan bebas, skor sentimen, teks keluhan, flag kontradiksi) tapi isinya ditulis oleh generator yang sama dengan label. Yang perlu diuji bukan "apakah kolom ini bernama Risiko", melainkan "apakah nilai kolom ini adalah fungsi dari label".

2. **Assertion anti-leakage notebook hanya memeriksa nama, bukan nilai** (sel 5): `leakage_found = [c for c in feature_names if any(f.lower() in c.lower() for f in FORBIDDEN_COLUMNS)]`. Fitur yang diberi nama `panjang_feedback`, `skor_sentimen`, `kontradiksi_narasi` lolos. Assertion ini tidak akan menangkap kebocoran mana pun di §4.1.

3. **`LEAKAGE_COLUMNS` di `backend/src/data/pipeline.py:37-40` didefinisikan tetapi tidak pernah dipakai** - satu kemunculan di seluruh repo (`is_fraud`, `claim_id` tidak termasuk di 03 §7). Backend `extract_features` justru memasukkan `skor_sentimen` (baris 198), `kontradiksi_narasi` (baris 203), frekuensi `faskes_id`/`dokter_id` (baris 222–226), dan `X_clean` dihitung dengan scaling di atas seluruh 300 baris (baris 229).

4. **Kode klinis tertentu menyempurnakan label.** Ada **5 kode klinis tunggal dengan presisi 100%** (semua baris berlabel fraud, n≥2): `Prosedur ICD-9-CM` = 96.04 (intubasi, 3/3), tiga nilai `Obat` (3/3 masing-masing), dan `Alasan Berobat` "Demam dan batuk berdahak…" (6/6). Ditambah 2 pasangan (dx, prosedur) dengan presisi 100%: (K29.7 + 00.66) dan (K80.2 + 96.04), masing-masing 3/3. Ini bukan pelanggaran aturan blokir (kolom ini bukan kolom label), tetapi membuktikan bahwa dataset sintetis punya label yang dapat ditebak dari kombinasi kode, sehingga benchmark "MHGSL vs baseline" mengukur kemampuan mengingat generator, bukan generalisasi klinis. Catatan: presisi 100% bukan AUROC 1,000 - AUROC indikator biner ini hanya 0,542 karena 33 fraud lain bernilai 0.

5. **Frasa "kebocoran" di 08 baris 22 sebenarnya sudah benar, tapi tidak diimplementasikan.** 08 baris 22/25 menyebut "kolom yang dihitung langsung dari aturan label" sebagai pengecualian. Tidak ada artefak yang mengimplementasikan frasa ini (I-05, I-17).

---

## 5. Pemetaan Risiko → Status dan Konsekuensinya

### 5.1 Fungsi yang ditemukan

Crosstab `Risiko` × `Status` dari 300 baris:

| Risiko | Status | n |
|---|---|---|
| low | auto_clear | 240 |
| medium | review | 10 |
| high | review | 14 |
| fraud | escalate | 36 |

Fungsi yang memetakan label ke status:

```
f(Risiko) = auto_clear  jika Risiko = low
          = review      jika Risiko ∈ {medium, high}
          = escalate    jika Risiko = fraud
```

**Akurasi fungsi terhadap data: 300/300 = 100,0%.** Fungsi ini deterministik, banyak-ke-satu (`medium` dan `high` sama-sama dipetakan ke `review`), dan terbalik sepenuhnya.

### 5.2 Konsekuensi

1. **`Status` tidak dapat menjadi target.** 02 baris 61–64 justru mensyaratkan `review_action` sebagai target kedua yang sah. Karena `Status` adalah coarsening deterministik dari `Risiko`, menjalankan `review_action` tidak menambah informasi apa pun - dia hanya mengulang `risk_triage` pada resolusi lebih kasar. Model yang "memprediksi Status" secara identik memprediksi `Risiko ∈ {medium, high, fraud}`.

2. **`Status` tidak dapat menjadi fitur.** 03 §7 sudah memblokirnya, dan pemblokiran itu benar: sebagai fitur, `Status` mengembalikan label dengan akurasi 100% (4 nilai kategorikal). Setiap metrik yang dilaporkan dengan `Status` sebagai fitur adalah pengukuran ulang label.

3. **Kelas `review` (24 kasus = 8,0%) terlalu kecil untuk eksperimen.** 24 kasus, dipecah menjadi `medium` (10) dan `high` (14) yang keduanya berstatus `review`. Dengan GroupKFold(5) by pasien, `review` tersebar di 5 fold dengan rata-rata 4,8 kasus/fold; dengan LOGO by faskes, 2 dari 10 fold tidak punya satu pun kasus `review` - AUROC per fold tidak terdefinisi.

4. **`Status` sebagai label tidak menambah cakupan anomali.** 03 baris 30 sudah memperingatkan: "Jangan menyamakan seluruh 264 klaim non-fraud dengan klaim normal". Kelompok `fraud` (36) + `review` (24) = 60 anomali, identik dengan `Risiko` non-low. Jadi tidak ada jalur informasi tambahan.

5. **Butir 3 checklist repro 03 §8 ("definisi target") gagal di dua level**: target belum disahkan (08 baris 15 "Belum disahkan") dan `Status` secara deterministik tidak bisa dipakai.

### 5.3 Apakah `fraud` dapat direplikasi dari `Risiko` = 36? Tidak - arah terbalik

Pertanyaan yang sebenarnya diajukan adalah: apakah ground truth "fraud" bisa dibangkitkan dari `Risiko`? Jawabannya ya, secara deterministik:

```
is_fraud = 1 jika Risiko == 'fraud'  (36/36)
```

`pipeline.py:167` melakukan hal ini persis. Karena itu:

- **`fraud` bukan variabel yang diuji, melainkan variabel yang dibaca ulang.** AUPRC/AUROC terhadap `is_fraud` mengukur seberapa baik model meniru `Skor Fraud` yang sudah di-threshold, bukan seberapa baik model menemukan fraud.
- **Replikasi `Risiko` dari `Skor Fraud` (aturan 10 baris 9):**
  - Aturan A (`> 0.8` = fraud, `≤ 0.80` = high): **1 mismatch** - KLM115 skor 0,80 → `high` menurut aturan, tetapi data melabeli `fraud`.
  - Aturan B (`≥ 0.80` = fraud): **0 mismatch**.
  - Rentang skor per label: low 0,04–0,14 · medium 0,40–0,53 · high 0,62–0,79 · fraud 0,80–0,95. Tidak ada tumpang tindih.
  - Kesimpulan: `Risiko` **adalah** `Skor Fraud` yang di-threshold, dengan ambang 0,80 eksklusif dalam redaksi dokumen dan inklusif dalam data. Satu baris (KLM115) membedakan kedua definisi.
- **Implikasi untuk I-07:** benchmark in-sample + target = label aturan berarti tabel benchmark mengukur **kemampuan meniru aturan** pada data yang sama. Angka AUPRC tinggi yang mungkin muncul bukan bukti apa pun tentang deteksi fraud.

---

## 6. Power Analysis: 300 Baris Tidak Cukup untuk Protokol yang Dirancang

### 6.1 Asumsi

- Distribusi binomial: `n_pos` kasus fraud, `n_neg` = 300 − `n_pos`.
- Empat skenario prevalensi: 3%, 5%, 7% (produksi, 10 baris 175/180) dan 12% (dataset aktual, 10 baris 113).
- Skor laten model: dua populasi normal, `AUROC` target 0,90, disimulasikan dengan `mu = sqrt(2)·Φ⁻¹(AUROC)`, σ=1.
- `AP` dihitung step-wise (`average_precision`).
- CI: bootstrap percentile, B=1200 resample, seed 20260707 (stratified pada label); AUROC memakai Hanley–McNeil; proporsi memakai Wilson score interval.
- Uji perbedaan: **paired** bootstrap (resample baris yang sama untuk kedua model), 800 iterasi; dua model berbagi 30% "kasus sulit" agar korelasi error realistis.

Semua dihitung di `06_stats.py` §8. Asumsi skrip, bukan angka manual.

### 6.2 AUPRC - lebar interval 95% (bootstrap)

| Prevalensi | n_pos | n_neg | Baseline AP | AP titik | CI 95% | **Lebar CI** |
|---|---|---|---|---|---|---|
| 3% | 9 | 291 | 0,030 | 0,435 | [0,217 ; 0,778] | **0,561** |
| 5% | 15 | 285 | 0,050 | 0,512 | [0,276 ; 0,745] | **0,469** |
| 7% | 21 | 279 | 0,070 | 0,545 | [0,343 ; 0,746] | **0,403** |
| 12% | 36 | 264 | 0,120 | 0,776 | [0,664 ; 0,879] | **0,216** |

**Pembacaan:** pada prevalensi produksi bawah 3–7%, CI AUPRC 95% selebar ±0,20 sampai ±0,28. Ambang keputusan AUPRC yang biasa dipakai (0,50) berada **di dalam** CI pada semua skenario. Tidak ada perbedaan AUPRC yang lebih kecil dari ~0,40 yang dapat dibedakan dari baseline acak pada 300 baris.

### 6.3 AUROC - CI 95% (Hanley–McNeil, AUROC sebenarnya 0,90)

| Prevalensi | n_pos | n_neg | AUROC | CI 95% | Lebar |
|---|---|---|---|---|---|
| 3% | 9 | 291 | 0,900 | [0,764 ; **1,036**] | 0,271 |
| 5% | 15 | 285 | 0,900 | [0,795 ; **1,005**] | 0,210 |
| 7% | 21 | 279 | 0,900 | [0,811 ; **0,989**] | 0,178 |
| 12% | 36 | 264 | 0,900 | [0,832 ; 0,968] | 0,137 |

**Pembacaan:** pada prevalensi 3% dan 5%, batas atas CI melewati 1,0 - estimator AUROC dengan 9–15 positif tidak informatif. Pada 12% (36 positif) CI masih ±0,07.

### 6.4 Recall - kriteria 2 "≥90% dari 36 fraud"

| Skenario | Recall | CI 95% (Wilson) | Lebar |
|---|---|---|---|
| dataset 12% (n_pos=36) | 32/36 = 88,9% | [74,7% ; 95,6%] | 20,9 pp |
| downsampling 7% (n_pos=21) | 19/21 = 90,5% | [71,1% ; 97,3%] | 26,3 pp |
| downsampling 5% (n_pos=15) | 13/15 = 86,7% | [62,1% ; 96,3%] | 34,1 pp |
| downsampling 3% (n_pos=9) | 8/9 = 88,9% | [56,5% ; 98,0%] | 41,5 pp |

**Pembacaan:** target 90% memiliki CI yang **mengandung 90%** dan lebar 21–42 pp. Kriteria "≥90% terdeteksi" pada 300 baris tidak membedakan model 88% dari model 100%. Tidak ada aturan statistik yang bermakna.

### 6.5 Presisi antrian top-20% (60 klaim)

| Komposisi | Presisi | CI 95% |
|---|---|---|
| 32/36 fraud di 60 teratas | 53,3% | [40,9% ; 65,4%] |
| 34/36 fraud | 56,7% | [44,1% ; 68,4%] |
| 38/60 (termasuk 2 non-fraud) | 63,3% | [50,7% ; 74,4%] |

### 6.6 Hit-rate per sindikat (kriteria 4)

| Sindikat | n | fraud | CI 95% hit-rate(1/n) | Status |
|---|---|---|---|---|
| SYND-01 | 3 | 3 | [6% ; 79%] | mungkin, tidak informatif |
| SYND-02 | 3 | 3 | [6% ; 79%] | mungkin, tidak informatif |
| SYND-03 | 6 | 6 | [3% ; 56%] | mungkin, tidak informatif |
| SYND-04 | 2 | 2 | [9% ; 91%] | mungkin, tidak informatif |
| **SYND-05** | 2 | **0** | - | **MUSTAHIL** (label `high`) |
| SYND-06 | 4 | 4 | [5% ; 70%] | mungkin, tidak informatif |
| SYND-07 | 4 | 4 | [5% ; 70%] | mungkin, tidak informatif |
| SYND-08 | 6 | 6 | [3% ; 56%] | mungkin, tidak informatif |
| SYND-09 | 6 | 6 | [3% ; 56%] | mungkin, tidak informatif |

Setiap sindikat punya n ≤ 6. CI 95% hit-rate mencakup 0 dan 1 untuk semua sindikat. **Tidak ada sindikat yang bisa diuji secara bermakna pada 300 baris.**

### 6.7 Deteksi perbedaan AUPRC MHGSL vs baseline (paired bootstrap)

Simulasi: AUROC 0,92 vs 0,88, 30% kasus sulit bersama.

| n_pos | ΔAUPRC titik | CI 95% | Signifikan? |
|---|---|---|---|
| 21 (prevalensi 7%) | +0,135 | [−0,155 ; +0,395] | **Tidak** |
| **36 (prevalensi 12%, dataset aktual)** | +0,139 | [−0,045 ; +0,327] | **Tidak** |
| 100 | +0,106 | [+0,027 ; +0,192] | Ya |
| 200 | −0,005 | [−0,047 ; +0,034] | Tidak |

**Pada n=36 (ukuran dataset sebenarnya), peningkatan AUPRC yang dituntut kriteria 3 tidak dapat dibedakan dari nol.** 06 baris 43 sudah mencatat "Peningkatan AUPRC dibanding baseline - Belum dapat direproduksi dari artefak yang diperiksa"; hasil ini menunjukkan itu bukan sekadar masalah artefak, tetapi **masalah daya statistik**.

### 6.8 Minimum `n_pos` untuk membedakan AUPRC 0,80 vs 0,90

| n_pos | prevalensi | CI 95% ΔAUPRC | Signifikan? |
|---|---|---|---|
| 36 | 12% | [−0,060 ; +0,300] | Tidak |
| **60** | **20%** | **[+0,011 ; +0,283]** | **Ya** |
| 100 | 33% | [+0,090 ; +0,264] | Ya |
| 150 | 50% | [+0,019 ; +0,152] | Ya |
| 200 | 67% | [−0,046 ; +0,066] | Tidak |

**Ambang praktis: ≥60 kasus positif** (prevalensi 20% pada 300 baris) dibutuhkan untuk membedakan ΔAUPRC 0,10. Pada prevalensi produksi 3–7%, itu berarti **857–2000 baris** - bukan 300.

### 6.9 Konsekuensi struktural pada split

| Split | Fold | n | fraud | prevalensi | Catatan |
|---|---|---|---|---|---|
| GroupKFold(5, pasien) | 0 | 61 | 11 | 18,0% | |
| | 1 | 60 | 9 | 15,0% | |
| | 2 | 60 | 4 | 6,7% | |
| | 3 | 60 | 10 | 16,7% | |
| | 4 | 59 | **2** | 3,4% | recall 2 kasus → CI ±60 pp |
| LOGO(faskes) | RS_A | 29 | 3 | 10,3% | |
| | RS_B | 21 | 6 | 28,6% | |
| | RS_C | 16 | 3 | 18,8% | |
| | **RS_D** | 14 | **0** | 0,0% | **AUPRC tidak terdefinisi** |
| | RS_E | 28 | 2 | 7,1% | |
| | **RS_F** | 32 | **0** | 0,0% | **AUPRC tidak terdefinisi** |
| | RS_G | 45 | 5 | 11,1% | |
| | RS_H | 37 | 5 | 13,5% | |
| | RS_I | 36 | 6 | 16,7% | |
| | RS_J | 42 | 6 | 14,3% | |

**2 dari 10 fold LOGO tidak punya satu pun kasus fraud.** Notebook sel 11 menangani ini dengan `f_auprc = average_precision_score(...) if fraud_cnt > 0 else 1.0` - artinya fold tanpa positif diberi **AUPRC = 1,0**, nilai terbaik yang mungkin. Ini bukan sekadar kelemahan statistik: ia mengubah "tidak ada data" menjadi "performa sempurna", dan laporan mana pun yang menghitung rata-rata AUPRC per fold akan menampilkan angka RS_D dan RS_F sebagai 1,0000.

---

## 7. Kriteria "SESUAI": Mana yang Tidak Dapat Diuji

Kriteria 10 baris 196–206, dinilai terhadap 300 baris aktual:

| # | Kriteria | Status | Bukti |
|---|---|---|---|
| 1 | Integritas Data: 300 baris utuh, 0 kebocoran fitur | **GAGAL TERBUKTI** | Blokir resmi 7–9 kolom; 7+ kolom bocor di luar daftar (`Catatan` bijektif 240/240, `Skor Sentimen` AUROC 0,909, `Sentimen` 100% turunan, `Umpan Balik Pasien` 15/17 fraud, `Kontradiksi Narasi` flag dari ground truth, `claim_id` 24/24 anomali, `_last_edited`). 10 baris 115 sendiri menyatakan v2 "BELUM SESUAI" karena 10 kekurangan kritis; 7 artefak perbaikan masih hilang. |
| 2 | ≥90% dari 36 fraud terdeteksi di antrian ≤20% | **SANGAT LEMAH** | Recall 32/36 CI95% = [74,7% ; 95,6%], lebar 20,9 pp. Presisi top-20% = 53,3% CI95% = [40,9% ; 65,4%]. 2 fold LOGO tanpa positif. |
| 3 | AUPRC & AUROC MHGSL ≥ baseline XGBoost/MLP | **TIDAK TERUKUR** | Benchmark in-sample (sel 13). Tanpa test set tersisih, perbedaan in-sample antar model pada data yang sama tidak punya cakupan statistik. n=36 → ΔAUPRC CI [−0,045 ; +0,327] = tidak signifikan. 06 baris 42–43 sudah mencatat AUPRC 0,9142 sebagai belum dapat direproduksi. |
| 4 | Setiap SYND-01–09 hit-rate > 0 | **MUSTAHIL** | SYND-05 = KLM016–017 berlabel `high`, bukan `fraud` → hit-rate 0 pasti. Selain itu n ≤ 6 per sindikat → CI95% [3% ; 91%] mencakup 0 dan 1. Kriteria tidak dapat dibedakan dari acak. |
| 5 | Konsistensi XAI: SHAP sejalan dengan kolom `Alasan` | **TIDAK TERUJIAN** | SHAP tidak pernah dihitung (grep repo: 11 kemunculan `shap`, semua adalah nama kolom `sinyal_shap` / `A_sym`). `shap` ada di `requirements.txt` tapi tidak diimpor di mana pun. `Alasan` sendiri adalah label (prefix FRAUD/ANOMALI/NORMAL menentukan `Risiko` 300/300) → uji "konsistensi" hanya mengukur kesamaan label dengan label. |
| 6 | Saluran Teks: 8 klaim kontradiksi masuk daftar prioritas | **SIRKULAR / TRIVIAL** | `TARGET_CONTRADICTION_IDS` di-hardcode (sel 15); aturan teks dikunci ke (prosedur = 00.66/81.52/74.1) × keyword umpan balik yang hanya muncul pada 17 baris. Yang lolos adalah definisi, bukan model. Selain itu data menyediakan **12** klaim kontradiksi, bukan 8 (I-12). |
| 7 | Kejujuran Label: metrik disertai "simulasi sintetis, prevalensi oversampled" | **TERPENUHI (prosedural)** | Disclaimer tercetak di tabel benchmark (sel 12/13). Syarat formal, bukan empiris. |

**Ringkasan: 1 dari 7 kriteria terpenuhi secara substantif. 4 dari 7 (kriteria 3, 4, 5, 6) tidak dapat diuji dengan desain saat ini.**

---

## 8. Checklist Protokol Reproduksibilitas (03 §8)

Sepuluh butir wajib dari 03 baris 87–97, diperiksa terhadap 08 (training protocol) dan artefak aktual:

| # | Butir 03 §8 | Status | Bukti |
|---|---|---|---|
| 1 | nama dan versi dataset | ✗ | 08 baris 8 menyebut "Klaim Aegis-JKN v2, 300 baris" tapi tidak pernah mengunci nama/versi; 10 baris 114–131 menyebut v2.1; 03 §2 baris 13 masih "Dataset aktif v2"; CSV v2.1 tidak punya kolom `version`. |
| 2 | waktu ekspor | ✗ | 08 tidak menyebutnya. CSV Notion hanya punya `_last_edited` (3 timestamp) - bukan waktu ekspor eksperimen. |
| 3 | jumlah baris | ✓ | 08 baris 37 ("300 baris"), 03 §3.1 (300), CSV = 300. |
| 4 | checksum berkas | ✗ | 08 tidak menyebut checksum. 03 §8 butir 4 dan 03 §11 butir 6 masih checkbox terbuka (`- [ ] Lampirkan checksum dan seed`). Kami menghitungnya: `d6fb95b9…` / `37cf2236…` - tapi itu hasil audit ini, bukan artefak proyek. |
| 5 | kamus data | ◐ | 03 §5 (baris 47–72) memuat kamus 24 properti, tapi 08 §Tahap 2 hanya menyebut `data_quality_report.md` sebagai artefak; tidak ada file kamus data. |
| 6 | daftar kolom dipakai & dikecualikan | ◐ | Empat daftar berbeda: 03 §7 (8 kolom), 10 baris 127 (7 kolom), 08 baris 22 (4 eksplisit + frasa), notebook sel 5 (9 kolom). Tidak ada satu pun yang konsisten satu sama lain. |
| 7 | definisi target dan ambang | ✗ | 08 baris 15 menyatakan target "Belum disahkan"; 08 tidak menyebut angka ambang. 10 menyebut 0,35/0,60/0,80; 03 §4 baris 46 mencatat ambang ambigu. KLM115 (skor 0,80 = fraud) **mendispute** aturan "di atas 0,8". |
| 8 | aturan pembersihan | ◐ | 08 §Tahap 2 & §Preprocessing (baris 40–44) ada (kode ICD-10 sebagai teks, sentinel 999, validasi PNK02, PNK17=PNK18). Tapi tidak ada `manifest.json`/artefak yang dihasilkan; aturan LOS 0 (109 baris) belum diputuskan (03 §11 butir 4 terbuka). |
| 9 | ID anggota train, validation, test | ✗ | 08 baris 37 menyebut "sisihkan test set final" (prinsip). Implementasi: **tidak ada test set tersisih sama sekali** - benchmark dilatih & dievaluasi pada `X_clean` yang sama (sel 13). Tidak ada manifest split. |
| 10 | seed dan versi kode | ◐ | 08 §Tahap 3 & §Referensi (baris 84) menyebut "seed, versi library"; 10 baris 123 menyebut seed 20260707. Tapi: kolom `seed` tidak ada di CSV v2.1; `requirements.txt` tidak terkunci versi (`torch>=2.0.0` dst); tidak ada skrip evaluator yang tersimpan; `requirements.txt` tidak memuat `xgboost`/`imbalanced-learn` yang dipakai notebook. |

**Rekap: TERPENUHI 1 · SEBAGIAN 4 · GAGAL 5 (dari 10 butir wajib).**

Checklist ini diperkuat 02 §5.5 (10 artefak wajib per eksperimen) dan 08 §Tahap 0–5 (6 artefak): **0 dari 6 artefak Tahap 0–5 ada.**

---

## 9. Realisme Jadwal 8 Minggu / 4 Fase

Rencana 10 baris 207–213. Pemeriksaan prasyarat fase terhadap apa yang benar-benar ada di disk:

| Fase | Minggu | Prasyarat yang dibutuhkan | Prasyarat yang ADA | Prasyarat yang HILANG | Penilaian |
|---|---|---|---|---|---|
| **0. Fondasi & Audit Data** | 1 | Dataset v2.1, `leakage.yaml`, unit test | `claims_300_v2.1.csv` (300 baris, 31 kolom) | `configs/leakage.yaml` ✗, `configs/text.yaml` ✗, `tests/test_leakage.py` ✗, `data/raw/leakage_blocklist.yaml` ✗, `edges_v2.1.json` ✗, `text_gt_v2.1.csv` ✗, `features_300.parquet` ✗, `metadata.json` ✗, kolom `seed`/`version`/`timestamp` ✗ | **Tidak mungkin.** 7 dari 10 artefak fase 0 tidak ada. Selain itu 10 baris 115 menyatakan v2 "BELUM SESUAI" karena 10 kekurangan kritis - dan audit ini menemukan **7 kebocoran tambahan di luar daftar**, jadi biaya Fase 0 naik, bukan turun. |
| **1. Baseline ML & DL** | 2–3 | XGBoost + SMOTE, MLP, fitur graf turunan | MLP (PyTorch) ada di notebook sel 13; `pipeline.py` punya feature engineering | `xgboost` **tidak ada** di `requirements.txt` (notebook jatuh ke `GradientBoostingClassifier` via `HAS_XGB`), `imbalanced-learn`/SMOTE **tidak ada** dan tidak ada kode SMOTE di repo, `train.py`+`metrics.json` ✗, `evaluation_report.md` ✗, `manifest.json` ✗ | **Tidak realistis.** Baseline yang dijanjikan "XGBoost + SMOTE" secara faktual adalah GradientBoosting tanpa SMOTE, dan tidak ada skrip training yang bisa dijalankan ulang. |
| **2. Graf Heterogen & MHGSL** | 4–6 | PyG `HeteroData`, MHGSL, SHAP per-saluran | `torch-geometric` ada di requirements; model MHGSL terimplementasi di notebook sel 9; `backend/models/mhgsl_model.pth` ada | `graph_hetero.pt` ✗ (yang ada `mhgsl_model.pth` - nama berbeda, provenance tidak jelas), **SHAP tidak dihitung di mana pun** (import `shap` tidak ada di repo), `shap` hanya di requirements | **Tidak realistis.** Fase 2 mencakup "SHAP per-saluran" yang tidak memiliki satu baris kode pun. Ditambah I-09 (θ 0,85 vs 0,5) dan I-10 (edge semantik dari `sindikat`) yang membuat kanal tidak reproducible. |
| **3. Validasi Final & LLM** | 7–8 | Laporan validasi, benchmark Kaggle, DP-CTGAN, Gemini | - | `google-generativeai` ✗ di requirements, `configs/text.yaml` ✗, `ctgan` ✗ di requirements, tidak ada kode Gemini/CTGAN, `evaluation_report.md` ✗, `review_log.csv` ✗ | **Tidak realistis.** Tiga dependensi fase (Gemini, DP-CTGAN, laporan validasi) tidak terpasang. Notebook OASIS (sel 17) adalah simulasi agen dengan fallback deterministik - bukan integrasi Gemini. |

**Tambahan: prasyarat tak tertulis yang tidak terpenuhi di Fase mana pun**

- **Label ground truth independen.** 08 baris 21 mensyaratkan kolom adjudikasi (`ground_truth_fraud`, `evidence_source`, `reviewer_1`, `reviewer_2`, `adjudication_date`, `label_confidence`, `exclusion_reason`). Tidak ada satu pun kolom itu di CSV. 02 D-01 "Tetapkan definisi final label fraud dan anomali" masih **Terbuka**. Tanpa ini, Fase 1–3 yang aparentemente sudah "dikerjakan" di notebook justru menghasilkan angka yang tidak valid.
- **Test set tersisih.** 08 baris 37. Tidak ada di Fase mana pun pada rencana.
- **Manifest split + daftar ID.** 02 baris 70, 03 §8 butir 9. Tidak ada.
- **Daya statistik.** Min 60 kasus positif untuk membedakan ΔAUPRC 0,10 (§6.8) -butuh 857–2000 baris pada prevalensi produksi. Rencana tidak menyebut pengumpulan data tambahan sama sekali.

**Kesimpulan jadwal: rencana 8 minggu mengasumsikan 4 prasyarat yang tidak ada (blokir leakage, label adjudikasi, test set, dependensi) dan 1 prasyarat yang mustahil (daya statistik pada 300 baris). Fase 0 sendiri tidak dapat diselesaikan dalam 1 minggu dengan sumber daya yang ada, dan harus mendahului semua angka yang sudah tercetak di proposal.**

---

## 10. Rekomendasi Berurutan

1. **Tarik semua angka performa dari artefak publikasi sampai protokol ini diperbaiki.** 06 baris 42–43 sudah benar; sekarang terbukti alasannya (benchmark in-sample, target = label aturan, n=36). Tidak ada tabel benchmark di proposal yang boleh dipublikasikan apa adanya.
2. **Tetapkan label ground truth independen sebelum apa pun yang lain** (08 baris 21, 02 D-01). Tanpa kolom adjudikasi, seluruh 25 temuan lain hanya mengoptimasi sasaran yang keliru. Ini satu-satunya langkah yang memblokir semua yang lain.
3. **Kunci satu blokir leakage kanonik** (I-05): 9 kolom resmi + 7 tambahan §4.1 = **16 kolom** minimum, dan wajib mengimplementasikan frasa 08 baris 22 ("kolom yang dihitung langsung dari aturan label") sebagai predicate nilai, bukan daftar nama. Assertion notebook (sel 5) harus memeriksa **korelasi/nilai**, bukan substring nama fitur. `LEAKAGE_COLUMNS` di `pipeline.py:37` harus benar-benar dipakai, atau dihapus.
4. **Buang `Status` sebagai target** dan tetapkan satu target eksplisit (§5.2). Jika `review_action` dibutuhkan, nyatakan bahwa ia berkorelasi sempurna dengan `risk_triage` dan tidak menambah bukti.
5. **Buang `Alasan` dari daftar fitur v2.1** (I-05) atau dengan demikian: `Alasan` harus menjadi **output yang dihasilkan model**, bukan ground truth yang dipakai untuk menilai.
6. **Tetapkan test set tersisih + normalisasi per-fold** (I-07, I-08). Tanpa ini, tidak ada satu pun metrik di notebook yang valid.
7. **Tetapkan ambang 0,80 secara eksplisit** (I-02): `≥ 0,80` (cocok dengan data) atau `> 0,80` (cocok dengan redaksi 10). Perbarui KLM115 atau redaksi 10 - pilih satu, catat di changelog 03 §10.
8. **Koreksi tabel ground truth sindikat** (I-04) dan **catat penurunan 24 anomali v1** (I-03) di changelog 03 §10, yang saat ini masih "Belum ditetapkan".
9. **Perbaiki `f_auprc = ... if fraud_cnt > 0 else 1.0`** di sel 11 (I-19, §6.9). Fold tanpa positif harus `nan` dan di-exclude, bukan diberi 1,0.
10. **Selaraskan implementasi ke spesifikasi**: θ_feat 0,85 di `pipeline.py:251/327` (I-09); hapus edge `sindikat` dari A_sem (I-10); samakan target latih vs target evaluasi (38 vs 36).
11. **Realakan kembali jadwal**: Fase 0 butuh 2–3 minggu (bukan 1) hanya untuk blokir + label + test set; sisipkan **Fase pengumpulan data** menuju ≥60 kasus positif (§6.8) sebelum klaim "MHGSL lebih baik" diuji; pindahkan SHAP per-saluran ke Fase 3 dengan implementasi nyata; hapus DP-CTGAN dan Gemini dari rencana 8 minggu (tidak ada dependensi, tidak ada kode, dan bukan prasyarat validasi).
12. **Buat 6 artefak Tahap 0–5 (08 baris 30–35) dan 10 artefak 02 §5.5** sebagai syarat sebelum eksperimen berikutnya dimulai. Saat ini 0 dari 6 ada.
13. **Cegah regresi**: `tests/test_leakage.py` (dijanjikan 10 baris 154) harus memblokir 16 kolom §4.1 dan gagal keras - dan `configs/leakage.yaml` harus menjadi satu-satunya sumber daftar, dipakai oleh notebook, `pipeline.py`, dan backend API.

---

## Lampiran A - Perintah replikasi

```
python -X utf8 analysis/reports/scripts/06_stats.py
```

Skrip `06_stats.py` (stdlib saja) menghasilkan 12 bagian: identitas artefak + SHA-256, crosstab Risiko→Status, replikasi ambang skor, segmentasi ground truth v1/v2, konfrontasi tabel sindikat, sindikat vs fraud, audit anti-leakage (AUROC tunggal, determinisme, kode klinis, pasangan dx+prosedur), reproduksi temuan QA 03 §6, tabel blokir yang disarankan, struktur grup & kebocoran lintas-fold, power analysis (bootstrap AP, Hanley–McNeil, Wilson, paired bootstrap), status kriteria SESUAI, checklist 10 butir 03 §8, audit keberadaan artefak v2.1, dan ringkasan angka.

## Lampiran B - Ringkasan angka

| Besaran | Nilai |
|---|---|
| Baris / kolom (Notion CSV) | 300 / 29 |
| Baris / kolom (CSV v2.1 repo ML) | 300 / 31 |
| Distribusi `Risiko` | low 240 · medium 10 · high 14 · fraud 36 (12,0%) |
| Distribusi `Status` | auto_clear 240 · review 24 · escalate 36 |
| Fungsi `Risiko`→`Status` deterministik | **300/300 = 100%** |
| Skor fraud per label | low .04–.14 · medium .40–.53 · high .62–.79 · fraud .80–.95 |
| Mismatch replikasi `Risiko` dari `Skor Fraud` | aturan A (`>0.8`) = **1** (KLM115) · aturan B (`≥0.80`) = **0** |
| `P(fraud \| Sindikat terisi)` | 34/36 = 94,4% |
| `P(fraud \| teks keluhan-kunci)` | 15/17 = 88,2% |
| `Kontradiksi Narasi = True` | 12 (10 fraud + 2 high) - dokumen menyebut 8 |
| AUROC `Skor Sentimen` (fraud vs low) | 0,909 |
| AUROC `Catatan` kosong (fraud vs low) | 1,000 (bijektif 240/240) |
| `Sentimen` turunan `Skor Sentimen` | 300/300 |
| Sidik jari tabel sindikat meleset vs 10 §v2.1 | **5 dari 9** |
| Fold LOGO tanpa kasus fraud | **2 dari 10** (RS_D, RS_F) |
| Edge `A_top` lintas fold GroupKFold(pasien) | 1990/3420 = 58,2% |
| CI 95% AUPRC @ AUPRC 0,90, prevalensi 3% | [0,217 ; 0,778], lebar **0,561** |
| CI 95% AUROC @ 0,90, prevalensi 3% | [0,764 ; 1,036] |
| CI 95% ΔAUPRC (0,92 vs 0,88), n=36 | [−0,045 ; +0,327] → **tidak signifikan** |
| Min `n_pos` untuk ΔAUPRC 0,10 signifikan | **60** (prevalensi 20% pada 300 baris) |
| Checklist 03 §8 | TERPENUHI 1 · SEBAGIAN 4 · GAGAL 5 |
| Artefak v2.1 ada / dijanjikan | 1 / 10 |
| Artefak Tahap 0–5 (08) ada | **0 / 6** |
| SHA-256 `claims_v2_live.csv` | `d6fb95b9fbfb6bf47e9a99bcf57df0e38b00a13758b6d3ac14779e64a6121119` |
| SHA-256 `claims_300_v2.1.csv` | `37cf22369ebf7a3c616219cb49b9c4406f00d75286b38cbf6c08b844e27fd4e8` |
