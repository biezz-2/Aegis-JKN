# Laporan Audit Konsistensi Silang - Aegis-JKN

**Tanggal audit:** 22 Oktober 2026
**Ruang lingkup:** 15 dokumen korpus Notion (`N:\HEALTHKATHON\analysis\corpus\`) + `claims_v2_live.csv` (300 baris) + `dataset_research_live.csv` (33 entri)
**Skrip verifikasi:** `N:\HEALTHKATHON\analysis\reports\scripts\19_consistency.py` (stdlib only) → output `19_consistency_output.txt`
**Metode:** ekstraksi token angka per dokumen (Bagian A skrip), verifikasi silang terhadap CSV (Bagian B), deteksi duplikasi (Bagian C–D), audit tautan (Bagian E), tabel istilah (Bagian F).

---

## 1. Ringkasan Eksekutif

Korpus Aegis-JKN terbagi menjadi **9 dokumen terkendali** (00–08) dan **6 halaman arsip** (09–14). Dokumen terkendali sudah direkonsiliasi secara internal: 44 dari 51 angka kunci cocok persis dengan CSV aktif. Yang **tidak** konsisten adalah lapisan arsip dan lapisan dataset-100-klaim, yang masih membawa angka, definisi, dan peta sindikat versi lama tanpa penanda kedalaman arsip yang memadai.

**Total temuan: 34 kontradiksi** - 9 kritis, 15 tinggi, 10 sedang.

### Tabel severity

| Severity | Jumlah | Ciri | Contoh |
|---|---|---|---|
| **KRITIS** | 9 | Angka yang akan dikutip juri sebagai fakta, tapi bertentangan dengan data aktif atau antar-dokumen | 93,0% akurasi & Rp507.370.000 dinyatakan "terverifikasi" di arsip 11:15 & 14:490 |
| **TINGGI** | 15 | Peta ground truth, definisi label, dan hitungan entitas yang berbeda antar-dokumen | Tabel sindikat 11:296-304 vs 10:134-142 - ID sama, isi berbeda |
| **SEDANG** | 10 | Duplikasi, tautan mati, ambang versi, dan inkonsistensi istilah | 09-draft-hub.md = 10-simulation-dataset.md dua kali (byte-identik) |

### Temuan paling berbahaya (3)

1. **`11-archive-proposal.md:15` dan `14-index.md:490`** menyatakan metrik 93,0% / 94,12% / 0,9825 / 0,9142 dan Rp507.370.000 "dihitung berbasis metodologi empiris portofolio 300 klaim **terverifikasi** … dapat direplikasi secara objektif" - bertentangan langsung dengan `00-dashboard.md:47-49` dan `01-proposal.md:70` yang menandai angka yang sama sebagai **"belum boleh disebut tervalidasi"**.
2. **Peta sindikat bentrok.** `11:296-304` menetapkan SYND-01..09 = KLM001–KLM036 dengan modus/faskes/dokter berbeda, sedangkan `10:134-142` menetapkan SYND-01..09 = KLM001–KLM120. ID identik, isi berbeda total. CSV aktif mengonfirmasi versi `10` (bukan `11`).
3. **Angka finansial arsip tidak reproducible.** `11:348` menyebut sindikatarthy = Rp542,56 Juta, Upcoding = Rp127,68 Juta; CSV aktual: **Rp539.650.000** dan **Rp156.900.000**.

---

## 2. Tabel Master Klaim

Klaim dikelompokkan per dokumen. Format: `nilai → sumber (file:baris)`. Tanda `-` berarti tidak disebut.

### 2.1 `00-dashboard.md` (pusat kendali)

| Klaim | Nilai | Baris |
|---|---|---|
| Tanggal pembaruan / versi | 21 Oktober 2026 / 1.0 | 5, 6 |
| Jumlah baris aktif | 300 klaim | 9, 30 |
| Rentang ID | KLM001–KLM300 | 31, 42 |
| Status auto_clear / review / escalate | 240 / 24 / 36 | 32-34 |
| Total nominal | Rp3.526.650.000 | 35 |
| LOS hari kosong | 109 baris | 36 |
| Alasan kosong | 1 baris | 37 |
| Catatan riset | 33 entri | 38 |
| Overcharge | Rp507.370.000 - **belum reproducible** | 39 |
| Metrik "belum tervalidasi" | 93,0% / 94,12% / 0,9825 / 0,9142 / 89,4% / 10,6% / 45% / 3,2x / SUS 82,5 | 47-49 |
| P0 open items | tandai 100 klaim sbg versi awal; samakan angka operasional | 60, 63 |
| Changelog | 1.0 - 21 Oktober 2026 | 88 |

### 2.2 `01-proposal.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Judul/versi | Edisi Akademik Revisi 1.0, 21 Oktober 2026 | 3, 5 |
| Ukuran dataset | 300 klaim | 9, 37 |
| Status | 240 auto-clear / 24 review / 36 escalate | 9, 37 |
| Label risiko | 240 low / 10 medium / 14 high / 36 fraud | 37 |
| Total nominal | Rp3.526.650.000 | 66 |
| Nominal per status | auto-clear Rp2.685.550.000; review Rp279.950.000; escalate Rp561.150.000 | 67-69 |
| Metrik draf (belum tervalidasi) | 93,0% / 94,12% / 0,9825 / 0,9142 / 89,4% / 10,6% / Rp507.370.000 | 70 |
| Model baseline | XGBoost | 43 |

### 2.3 `02-architecture.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Versi/tanggal | Revisi 1.0, 21 Oktober 2026 | 3, 5 |
| Baseline Tier-2 | XGBoost "atau model tabular lain" | 28 |
| Kanal graf | Topologi, Fitur, Semantik (3 kanal) | 33-36 |
| Dual target | `risk_triage` (low/medium/high/fraud-scenario) + `review_action` (auto-clear/review/escalate) | 60-64 |
| Split | leave-one-facility-out; group-aware | 65-70 |
| Metrik wajib | confusion matrix, precision, recall, F1, FPR, ROC-AUC, AUPRC, kalibrasi | 75 |
| Keputusan terbuka | D-01 s/d D-06, **semua "Terbuka"** | 108-114 |

### 2.4 `03-dataset-registry.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Versi/tanggal | Revisi 1.0, 21 Oktober 2026 | 3, 5 |
| Sumber aktif | Database Klaim v2, 300 baris | 6 |
| Tabel versi | v1 = 100 klaim; v2 = 300; berikutnya = belum ditetapkan | 12-14 |
| Status | 240 (80,0%) / 24 (8,0%) / 36 (12,0%) | 19-22 |
| Label risiko | 240 (80,0%) / 10 (3,3%) / 14 (4,7%) / 36 (12,0%) | 25-29 |
| Nominal per status | Rp2.685.550.000 / Rp279.950.000 / Rp561.150.000 / Rp3.526.650.000 | 33-36 |
| **Peringatan ambang 0,80** | versi 100 klaim bisa dibaca "0,80 tidak termasuk fraud", DB aktif punya skor fraud 0,80 | 46 |
| Kualitas | 109 LOS kosong; 240 Modus kosong; 264 Sindikat kosong | 78-81 |
| Anti-leakage | 8 kolom terlarang | 84 |
| Prevalensi | 12% = distribusi sintetis, bukan prevalensi aktual | 100 |
| Changelog | 1.0 - 21 Oktober 2026 | 103 |

### 2.5 `04-evidence-matrix.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Tanggal audit | 21 Oktober 2026 | 5 |
| Snapshot DB riset | 33 entri; status 18/11/4; relevansi 11/18/4 | 10-17 |
| E-07 | AUPRC 0,9142 - **belum tereproduksi** | 34 |
| E-08 | AUPRC +20%, FN −42% - perlu verifikasi | 35 |
| E-09 / E-10 | telaah 20→3 menit / −45% - dua klaim terpisah | 36-37 |
| E-11 | Rp507.370.000 - belum reproducible per klaim | 38 |
| Hierarki sumber | A/B/C/D | 22-25 |

### 2.6 `05-decision-scope.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Versi/tanggal | Revisi 1.0, 21 Oktober 2026 | 3, 5 |
| Kandidat utama | Kandidat 1 (anomali diagnosis/prosedur) | 27 |
| Kandidat ditolak | Kandidat 2 (biometrik) - redundancy perlu konfirmasi resmi | 34 |
| Cadangan | Kandidat 3 (upah/iuran) | 41 |
| Bobot kuantitatif | **belum ada** (tidak ada lokakarya terdokumentasi) | 19 |
| Syarat keputusan | 3 syarat | 67-70 |
| Checklist terbuka | 5 item belum dicentang | 73-77 |

### 2.7 `06-research-notes.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Versi/tanggal | Revisi 1.0, 21 Oktober 2026 | 3, 5 |
| Prevalensi | 3–7% - belum layak dipakai sebagai fakta | 40 |
| AUPRC MHGSL | 0,9142 - belum reproducible | 42 |
| Kanal | topologi, kemiripan fitur, relasi semantik | 26 |
| Baseline | XGBoost | 24, 30 |

### 2.8 `07-dataset-v2-catalog.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Total baris Stata | 6.514.039 | 6 |
| D01 DM_kepesertaan | 143.496 × 18 var | 9 |
| D02 fkrtldxsekunder | 6.362.523 × 4 var | 10 |
| D03 fktpnonkapitasi | 8.020 × 21 var; PNK02 4.939 unik | 11 |
| R01–R04 workbook | 3.411 / 1.979 / 1.030 baris; 4 sheet; 979 label | 12-15 |
| PSTV18 kosong | 133.228 | 35, 82 |
| Tanggal PNK03/04 | mulai 16 Agustus 2014 vs nama file 2015-2020 | 48, 78 |
| PNK17 = PNK18 | identik di 8.020 baris | 63-64, 80 |
| Kode sentinel 999 | 3 kamus ICD-10 | 12-14, 81 |
| Label fraud | **tidak tersedia** pada file DM | 83, 87 |

### 2.9 `08-training-protocol.md`

| Klaim | Nilai | Baris |
|---|---|---|
| **Deskripsi DB basi** | "masih menyebut 100 klaim dan KLM001 sampai KLM024" | 8 |
| **Ulangi masalah** | "deskripsinya masih menyebut versi 100 baris dan ground truth KLM001 sampai KLM024" | 20 |
| Tahap 0-5 | beku sumber → human review; artefak manifest.json…review_log.csv | 29-35 |
| Baseline Tahap 3 | **aturan sederhana + logistic regression + model pohon interpretable** (tanpa XGBoost/SMOTE/MLP) | 33 |
| Split | CV berulang / stratified, group split bila pola sama | 37 |
| Metrik minimal | PR-AUC, precision, recall, F1, CM, FPR, calibration, interval | 38 |
| Larangan DM | jangan sebut precision/recall/AUPRC fraud tanpa ground truth independen | 39 |
| Aturan wajib | dataset+fitur+seed+split+artifact+metrik+CM+batasan | 84 |

### 2.10 `09-draft-hub.md` / `10-simulation-dataset.md` (halaman dataset)

| Klaim | Nilai | Baris (10 / 09) |
|---|---|---|
| Jumlah klaim v1 | 100 (20 pasien, 12 dokter, 6 FKRTL, 10 dx, 10 proc, 10 obat) | 6 / 9 |
| Distribusi v1 | 76 low / 4 medium / 6 high / 14 fraud | 7 / 10 |
| Ground truth v1 | anomali = KLM001–KLM024 (14 fraud sindikat + 10 medium/high) | 8 / 11 |
| Skala risiko v1 | <0.35 low; 0.35–0.6 medium; 0.6–0.8 high; >0.8 fraud | 9 / 12 |
| Prevalensi | oversample 14%; lapangan 3–7% | 10 / 13 |
| Cosine threshold fitur | 0.85 | 12 / 15 |
| Tabel sindikat v1 | SYND-01..05 (KLM001–017) | 15-19 / 24-28 |
| Kontradiksi narasi | 8 klaim (KLM001-006, 018, 024) | 107 / 110 |
| Sentimen v1 | 62 positif / 14 netral / 24 negatif | 108 / 111 |
| Edge count | "70 edges graf" (L110) vs "70+ edges" (L188) | 110, 188 / 113, 191 |
| Ekspansi v2 | 100→300, seed 20260707, KLM101–KLM300 | 112 / 115 |
| Distribusi v2 | 36 fraud / 14 high / 10 medium / 240 low; anomali total 60 (20%) | 113 / 116 |
| Perbaikan v2.1 | 2026-10-07; 10 kekurangan kritis | 114-115 / 117-118 |
| Entitas v2.1 | faskes RS_A-RS_J; dokter D01-D20; pasien P01-P40 | 146-148 / 149-151 |
| Alasan 3-tingkat | FRAUD 36 / ANOMALI 24 (14 high + 10 medium) / NORMAL 240 | 129-131 / 132-134 |
| Sindikat v2.1 | SYND-01..09 + 2 fraud tunggal (KLM121, KLM122) | 134-145 / 137-148 |
| Entitas didokumentasikan | dx K29.7, K35.8, I10, J45.9, N39.0 | 144 / 147 |
| Model baseline | XGBoost + SMOTE; MLP (PyTorch); PyG HeteroData | 162-165 / 165-168 |
| XAI | SHAP TreeExplainer + GradientSHAP, per-saluran | 166-169 / 169-172 |
| Struktur file | claims_300_v2.1.csv, edges_v2.1.json, leakage_blocklist.yaml | 186-195 / 189-198 |
| Protokol SESUAI | 8 kriteria | 197-206 / 200-209 |
| Rencana | 8 minggu, Fase 0–3 | 207-213 / 210-216 |

### 2.11 `11-archive-proposal.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Metrik sebagai fakta | Akurasi 93,0% / Presisi 94,12% / ROC-AUC 0,9825 / AUPRC 0,9142 + Rp507,37 Juta "dapat direplikasi secara objektif" | 15 |
| Skala nasional | 270+ juta peserta; 2 juta klaim/hari; 1.000 verifikator; rasio 2.000/hari | 22, 127, 165 |
| Performa | +28,6% vs baseline XGBoost 0,71; masking 89,4%; 9 sindikat 100% | 30 |
| Anomali | 60 klaim; rata-rata Rp8,46 Juta/kapus; cost-to-impact 1:15 | 30 |
| Saluran graf | A_top 10.386 edges; A_feat 15.202 (θ≥0,50); A_sem 7.880 | 209-211 |
| Tabel sindikat v1 | SYND-01..09 = KLM001–KLM036 | 296-304 |
| Komposisi | 264 normal (88%) + 36 fraud sindikat (12%); rasio 1:7,33; 31 fitur | 321 |
| KPI "Tervalidasi" | 93,00% / 94,12% / 0,9825 / 0,9142 / 89,40% / FPR 10,60% / 3,2x / 1:15 / SUS 82,5 | 326-335 |
| Baseline | XGBoost AUPRC 0,7100; MHGSL 0,9142 | 338 |
| Waktu telaah | −45% (10-20 → 3-5 menit) | 340 |
| Finansial | 60 anomali Rp841,10 Juta; overcharge Rp507.370.000 (60,32%); rata-rata Rp8.456.167 | 348 |
| Modus nominal | Phantom Rp134,25 Jt; Upcoding Rp127,68 Jt; Repeat Rp61,60 Jt; sindikat Rp542,56 Jt | 348 |
| Roadmap | 8-12 minggu + 12 bulan | 393-394 |

### 2.12 `12-archive-architecture.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Versi | Perbaikan v2.1 - 2026-10-07 | 22, 41, 135 |
| "10 kekurangan kritis" | teks menyebut 10; **tabel hanya 6 baris** | 23, 42 vs 43-52 |
| AKronim MHGSL | Multi-Channel Graph Structure Learning | 30, 33 |
| Kinerja adaptasi literatur | AUPRC +20%; false negatives −42% | 30, 36, 55 |
| Graf | edges.json (70+ edges) | 65 |
| "85% sempurna" | "Desain Aegis-JKN sudah 85% sempurna" | 127 |
| Tautan v2.1 | label "Dataset Simulasi Aegis-JKN v2.1" → halaman yang isinya **100 klaim** | 53 |
| Struktur repo | baseline_xgb.py (XGBoost+SMOTE), baseline_mlp.py, mhgsl.py | 149-170 |
| Rencana | 8 minggu | 187-193 |

### 2.13 `13-archive-deep-research.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Kerugian nasional | RP25 miliar (3 RS swasta, Jawa Tengah + Sumatera Utara, 2024) | 3 |
| Catatan editorial | "Angka nasional, nilai kerugian, dan status verifikasi harus dilacak ke sumber primer" | 4 |
| Modus | Phantom Billing, Upcoding | 5-6 |
| Celah | 5 butir | 7-12 |
| LLM hallucination (halusinasi) | 6 tahap | 17-23 |

### 2.14 `14-index.md`

| Klaim | Nilai | Baris |
|---|---|---|
| Kandidat ide | 3 kandidat; utama = Upcoding; cadangan = Manipulasi gaji | 3-43 |
| Tabel perbandingan | "Belum ada verifikasi otomatis" vs biometrik FRIDAY | 38-43 |
| Kontrol proyek | "Jangan gunakan angka benchmark atau finansial sebagai hasil final" | 44 |
| Salinan 10-simulation | baris 51-259 | 51-259 |
| Salinan arsip proposal | metrik sebagai fakta | 490, 505 |
| Salinan 12-archive-architecture | 10.386 edges | 684-686 |
| Salinan dokumen terkendali 00–08 | 1122, 1216, 1308, 1423, 1533, 1619, 1695, 1767, 1857 | - |

---

## 3. Daftar Kontradiksi

| No | Topik | Versi A (file:baris) | Versi B (file:baris) | Konsekuensi | Sumber kebenaran yang disarankan |
|---|---|---|---|---|---|
| 1 | Status metrik 93,0%/0,9142 | `11-archive-proposal.md:15`, `14-index.md:490` - "terverifikasi … dapat direplikasi" | `00-dashboard.md:47-49`, `01-proposal.md:70` - "belum boleh disebut hasil tervalidasi" | Juris membaca arsip, mengutip akurasi 93% sebagai fakta | **00-dashboard.md:47-49** (status belum tervalidasi) |
| 2 | Status Rp507.370.000 | `11:15`, `11:348`, `14:490`, `14:823` - "Penyelamatan Riil" | `00:39`, `03:38`, `04:38` (E-11), `01:70` - belum reproducible per klaim | Klaim penghematan Rp0,5 miliar dipertanggungjawabkan sebagai hasil | **04-evidence-matrix.md:38** (E-11) |
| 3 | Peta sindikat SYND-01..09 | `11:296-304` = KLM001–KLM036, modus/faskes/dokter berbeda | `10:134-142` = KLM001–KLM120 | ID sindikat sama menunjuk klaim berbeda - tabel ground truth saling meniadakan | **10-simulation-dataset.md:134-142** (dikonfirmasi CSV) |
| 4 | SYND-04 | `11:299` = KLM013-015, RS_D, D09+D10 | `10:137` = KLM013-014, RS_E, D09 | Ground truth sindikat berbeda faskes & dokter | CSV: KLM013-014, RS_E, D09 → **10:137** |
| 5 | SYND-05 | `11:300` = KLM016-018, RS_E, D11, ≥0.90 | `10:138` = KLM016-017, RS_F, D08, 0.78-0.79 (high) | CSV: KLM016-017, RS_F, D08, **risiko=high** bukan fraud | **10:138** |
| 6 | SYND-06 | `11:301` = KLM019-024, "Referral Churn", RS_G, D13+D14 | `10:139` = KLM101-104, "Repeat Billing", RS_G, D13 | Sindikat claims menunjuk ID yang di CSV berlabel `low` | **10:139** |
| 7 | SYND-07 | `11:302` = KLM025-028, "Upcoding Severity", RS_A, D03 | `10:140` = KLM105-108, "Iur Biaya", RS_H, D14 | KLM025-028 di CSV = `low` | **10:140** |
| 8 | SYND-08 | `11:303` = KLM029-032, "Repeat Billing", RS_F, D12 | `10:141` = KLM109-114, "Readmission", RS_I, D15 | KLM029-032 di CSV = `low` | **10:141** |
| 9 | SYND-09 | `11:304` = KLM033-036, RS_G+RS_C, D15+D19 | `10:142` = KLM115-120, RS_J, D16 | KLM033-036 di CSV = `low`; 12 klaim tak dikenal_mapping | **10:142** |
| 10 | SYND-06/07/08/09 rentang pasien | `10:139-142` P21-P24 / P25-P28 / P29-P34 / P35-P40 | CSV: P21-P22 / P23-P24 / P25-P26 / **P27** | 11 dari 40 pasien disebut sebagai anggota sindikat tapi tidak ada klaimnya | **CSV** (`claims_v2_live.csv`) |
| 11 | SYND-09 dokter | `10:142` D16 | CSV: D19 |  | **CSV** |
| 12 | KLM121 | `10:143` - RS_A, D03, P04, ≥0.85 | CSV - RS_G, D13, P29, skor 0.81 | Baris "fraud tunggal" dipetakan ke faskes/dokter/pasien yang salah | **CSV** |
| 13 | KLM122 | `10:144` - RS_E, D09, P18, ≥0.80 | CSV - RS_H, D14, P30, skor 0.82 | idem | **CSV** |
| 14 | Nominal modus Upcoding | `11:348` Rp127,68 Juta | CSV Rp156.900.000 | Selisih Rp29,22 juta pada tabel finansial utama | **CSV** |
| 15 | Nominal sindikat | `11:348` Rp542,56 Juta | CSV Rp539.650.000 | Selisih Rp2,91 juta | **CSV** |
| 16 | Jumlah baris dataset | `10:3`, `10:6`, `11:321` - 100 klaim (v1) | `00:9,30`, `03:13`, `01:9,37` - 300 klaim (v2) | Dipakai dataset salah untuk klaim performa | **03-dataset-registry.md:12-14** (v1 = 100, v2 = 300) |
| 17 | Distribusi label | `10:7` - 76/4/6/14 (100 klaim) | `01:37`, `03:25-29` - 240/10/14/36 (300 klaim) | "14% prevalensi fraud" vs "12%" | **03:25-29** |
| 18 | Jumlah anomali | `10:113` - 60 (20%) | `10:8` - 24 anomali (KLM001-024: 14 fraud + 10 medium/high) | Kombinasi "36+14+10=60" disebut anomali total; versi v1 hanya 24 | **03:25-29** + **10:128-131** |
| 19 | Ground truth sindikat | `10:8` - anomali = KLM001–KLM024 | `11:296-304` - sindikat sampai KLM036 | Konflik langsung dengan No. 3 | **10:8** |
| 20 | Ambang skor 0,80 | `10:9` - "0.6-0.8 high; lebih dari 0.8 fraud" (bisa dibaca 0,80 = high) | `03:46` - peringatan eksplisit; CSV punya KLM115 = 0.8 berlabel fraud | Baris 0.80 akan terklasifikasi high di pipeline | **03:46** + definisi inklusif `skor ≥ 0.80` |
| 21 | Ambang medium | `10:9` - 0.35–0.6; `03:25-29` - medium = 10 baris | CSV medium 0.40–0.53 | Interval 0.54–0.59 & 0.35–0.39 kosong/tidak terisi | **03** + konfigurasi ambang terpusat |
| 22 | Jumlah dokter unik | `10:6` - 12 dokter | CSV 100 klaim pertama - **11** dokter (D06 tidak muncul) | Tabel master entitas overstated | **CSV** |
| 23 | Jumlah faskes | `10:6` - 6 FKRTL | CSV 100 pertama - RS_A..RS_F (6) ✓; v2.1 `10:119` - RS_A-RS_J (10) ✓ | - | **CSV** (konsisten) |
| 24 | Jumlah pasien | `10:6` - 20; `10:120` - P01-P40 (40) | CSV: 20 (v1) / 40 (v2) ✓ | - | **CSV** (konsisten) |
| 25 | Jumlah edge graf | `10:110` - "70 edges"; `10:188`, `12:65`, `12:150` - "70+ edges" | `11:209-211` - 10.386 + 15.202 + 7.880 = **33.468 edges** | Skala graf berbeda 478x; `edges_v2.1.json` belum pernah dibuat | **11:209-211** (untuk portofolio 300) |
| 26 | Baseline model | `10:162-163`, `12:167-168` - XGBoost+SMOTE, MLP | `08:33` - logistic regression + model pohon interpretable; **XGBoost/SMOTE/MLP tidak disebut** | Protokol training terkontrol tidak mengimplementasikan stack yang dirancang arsip | **08:33** (dokumen terkontrol) + revisi 08 agar menyebut stack final |
| 27 | Jumlah kekurangan v2.1 | `12:23`, `12:42`, `12:127`, `10:115` - "10 kekurangan kritis" | `12:43-52` - tabel hanya berisi **6 baris** | Checklist perbaikan tidak lengkap; 4 item hilang | **08 + 12** - susun ulang tabel hingga 10 baris |
| 28 | Angka "85% sempurna" | `12:127` - "Desain Aegis-JKN sudah 85% sempurna" | `00:7` - prinsip tanpa klaim performa tanpa bukti | Klaim kematangan tanpa artefak | **Hapus / ganti** "siap uji Fase 0–3" |
| 29 | Label halaman v2.1 | `12:53` - tautan "Dataset Simulasi Aegis-JKN v2.1" → `3f23e603…` | `10:4` - halaman itu berisi **100 klaim** | Tautan "lihat detail v2.1" justru membuka versi lama | **03-dataset-registry.md** (atau koreksi label tautan) |
| 30 | Jumlah klaim "kontradiksi narasi" | `10:107`, `10:203` - 8 klaim | CSV - **12 baris** `Kontradiksi Narasi = true` (KLM001-006, 018, 024, 105-108) | Kriteria protocol "Saluran Teks" tidak terpenuhi 8→12 | **CSV** (12) - perbarui `10:107` & `10:203` |
| 31 | Baris LOS kosong | `00:36`, `03:78` - 109 baris kosong | CSV - **0 baris kosong**, 109 baris bernilai `"0"` | Kualitas data: nol LOS bukan nol durat; akan salah tafsir | **CSV** - gunakan "109 baris bernilai 0" |
| 32 | Durasi rencana | `10:207-213`, `12:187-193` - 8 minggu | `11:393` - "8-12 Minggu"; `11:394` - roadmap 12 bulan | Jadwal punya dua sumber | **10:207** (8 minggu) + `11` sebagai rencana 12 bulan terpisah |
| 33 | Susunan tabel sindikat | `10:134-142` - 9 sindikat (7 v2.1 + 5 v1) | `11:296-304` - 9 sindikat beda | No. 3 | **10** |
| 34 | Label `auto_clear` vs `auto-clear` | `03:19`, `00:32` - `auto_clear` (snake_case, nilai DB) | `01:9,37`, `02:62` - `auto-clear` (kebab-case) | Query string kunci `auto_clear` tidak cocok di `01`/`02` | **`auto_clear`** (nilai literal DB) |

---

## 4. Audit `14-index.md` (229 KB, 1.939 baris)

### 4.1 (a) Duplikasi / pensonnyataan tata kelola dashboard

**Ya - 14-index adalah cermin penuh + arsip.** Verifikasi programatik (Bagian C skrip) mengonfirmasi **9 dokumen terkendali 00–08 tersalin utuh, identik baris-per-baris**:

| Dokumen | Mulai baris di 14-index | Identik baris-per-baris |
|---|---|---|
| 00-dashboard | 1123 | Ya |
| 01-proposal | 1217 | Ya |
| 02-architecture | 1309 | Ya |
| 03-dataset-registry | 1424 | Ya |
| 04-evidence-matrix | 1534 | Ya |
| 05-decision-scope | 1620 | Ya |
| 06-research-notes | 1696 | Ya |
| 07-dataset-v2-catalog | 1768 | Ya |
| 08-training-protocol | 1858 | Ya |

Selain itu 14-index memuat salinan `10-simulation-dataset` (baris 51–259), salinan `11-archive-proposal` (477–905), `12-archive-architecture` (906–1098), `13-archive-deep-research` (1099–1121), plus sub-page "ARSIP SUMBER DUPLIKAT" (260–471) yang menggandakan `10` untuk kedua kalinya.

Struktur navigasi 14-index sendiri **tidak** menduplikasi tata kelola - ia **mengganggu** tata kelola: sub-page "Draft" kosong (14:45), "Database Riset" (14:47), "Database Klaim v2" (14:472) disisipkan di tengah arsip, sehingga urutan baca dokumen terkendali (14:1122–1939) berada **di ujung file**, setelah 1.100 baris materi sumber lama.

### 4.2 (b) Angka yang SUDAH DIHAPUS di revisi tapi masih ada di 14-index

| Angka | Status di dokumen terkendali | Masih ada di 14-index |
|---|---|---|
| Accuracy 93,0% | "belum boleh disebut tervalidasi" (`00:47`) | Ya - `14:490`, `14:801` ("93.00% **Tervalidasi**"), `14:505` |
| Precision 94,12% | belum tervalidasi (`00:47`); **tidak tercapai pada ambang mana pun** (0 dari 46 nilai unik `skor_fraud`; terdekat 94,7368% di ambang 0,78) | Ya - `14:490`, `14:802` ("Tervalidasi"), `14:505` |
| ROC-AUC 0,9825 | belum tervalidasi (`00:47`) | Ya - `14:490`, `14:803` ("Tervalidasi"), `14:505` |
| AUPRC 0,9142 | belum tereproduksi (`04:34` E-07) | Ya - `14:490`, `14:804`, `14:505`, `14:813` |
| Rp507.370.000 | belum reproducible (`00:39`, `04:38`) | Ya - `14:490`, `14:822` ("Penyelamatan Riil"), `14:823` |
| 89,4% masking | belum tervalidasi (`00:48`) | Ya - `14:490`, `14:805` ("Tervalidasi"), `14:813` |
| FPR 10,6% | belum tervalidasi (`00:48`). Catatan: angka ini **dapat** dihitung dari data aktif, tapi hanya di ambang `skor_fraud ≥ 0,14` (FP 28 dari 264 negatif = 10,6061%), dan presisi pada ambang itu hanya 56,25% - jadi tidak berlaku bersama presisi 94,12% | Ya - `14:807`, `14:815` |
| Waktu telaah −45% | belum dibuktikan (`04:37` E-10) | Ya - `14:815` |
| Throughput 3,2x | belum tervalidasi (`00:49`) | Ya - `14:808`, `14:825` |
| SUS 82,5 | belum tervalidasi (`00:49`) | Ya - `14:810`, `14:825` |
| 10.386 / 15.202 / 7.880 edges | tidak ada di dokumen terkendali | Ya - `14:684-686` |
| 264 normal (88%) + rasio 1:7,33 | tidak ada di dokumen terkendali | Ya - `14:796` |
| Cost-to-Impact 1:15 | tidak ada di dokumen terkendali | Ya - `14:622`, `14:809`, `14:838`, `14:877` |
| 270+ juta peserta; 2 juta klaim/hari | `04:29-30` E-03/E-04 "sebagian terverifikasi" | Ya - `14:640`, `14:847` |

**Yang justru tidak ada:** label "belum tervalidasi" versi revisi hanya muncul di salinan dokumen terkendali (14:1159, 14:1284, 14:1569). Jadi 14-index memuat **kedua versi klaim sekaligus** - yang sudah di-cavet sebagai belum tervalidasi dan yang masih diarden sebagai fakta.

### 4.3 (c) Risiko jika juri membuka tautan lama

| Risiko | Mekanisme | Dampak |
|---|---|---|
| **R1 - Kutipan angka salah** | `14:490` dan `14:801-810` menyajikan metrik sebagai "Tervalidasi" | Klaim akurasi 93% & Saving Rp507 juta dapat dikutip juri sebagai hasil final - padahal `00:47` menyatakan sebaliknya |
| **R2 - Kontradiksi ground truth** | `14:684` (10.386 edges) vs `14:158` (70+ edges) dalam satu file | Juri tidak bisa menentukan mana ground truth |
| **R3 - Peta sindikat ganda** | `14:59-60` (SYND-01..05) vs `14:690-699` (SYND-01..09 versi arsip) | Verifikasi manual gagal |
| **R4 - Skala 270 juta peserta** | `14:640` tanpa catatan verifikasi | Klaim nasional tanpa sumber primer |
| **R5 - Jalur navigasi terputus** | Kontrol di `14:44` menunjuk dashboard; tapi dashboard ada di `14:1122` - jauh dari atas | Dokumen terkendali tenggelam |
| **R6 - Duplikasi-database** | `14:47` & `14:472` & `14:429` (di 09) menunjuk database yang sama | Risiko edit pada salinan, bukan pada master |

### 4.4 Rekomendasi: arsip, jangan hapus

**ARSIPKAN (pindahkan ke "ARSIP SUMBER / History"), JANGAN HAPUS.** Alasan:
- `14:5` dan `14:44` sudah memuat "CATATAN EDITORIAL" yang menyuruh pembaca memeriksa klaim lama - jadi nilainya historis (rekam jejak keputusan), bukan salah.
- Konten arsip menyimpan **konteks kandidat ide** (`14:8-43`) yang **tidak ada** di dokumen terkendali mana pun dan **tidak hilang** jika 11–13 tetap dipertahankan sebagai file terpisah (`11-archive-proposal.md` sudah memuatnya).
- Menghapus 14-index yang berisi 9 salinan dokumen terkendali akan memutus akses cepat dan membakar jejak revisi.

**Syarat arsip (3 perbaikan minimum):**
1. **Blokir akses** - beri banner di baris 1: *"DOKUMEN ARSIP. Tidak berlaku sebagai sumber klaim. Angka di bawah sudah disuperseded oleh 00-08."*
2. **Tambah penanda "SUDAH DISUPERSEDED"** pada setiap kemunculan angka terlarang (baris 490, 505, 622, 640, 657, 684-686, 796, 801-815, 822-825, 838, 847, 877).
3. **Pindahkan blok 1122-1939 ke ATAS file** agar dokumen terkendali ditemukan lebih dulu.

Alternatif yang lebih bersih: **pecah 14-index** - `14-index.md` (arsip) tetap, plus file baru `00-index-terkendali.md` berisi 9 dokumen terkendali yang tertaut. Tapi untuk kebutuhan sekarang,yar suffice minimal 3 perbaikan di atas.

---

## 5. Audit `09-draft-hub.md` (33 KB, 433 baris)

### 5.1 Duplikasi

Verifikasi programatik (Bagian D skrip):
- `09:8-216` ≡ `10:5-213` → **True** (byte-identik, 209 baris)
- `09:220-428` ≡ `09:8-216` → **True** (byte-identik)

Jadi **09-draft-hub memuat isi `10-simulation-dataset.md` dua kali berturut-turut**, dengan sub-page kedua diberi label "ARSIP SUMBER DUPLIKAT" (09:217) dan "CATATAN KONTROL DOKUMEN" (09:219) yang justru mengkonfirmasi duplikasi ini secara eksplisit.

### 5.2 Tabel konten unik

| Konten unik di 09 | Ada di dokumen terkendali? | Nilai/Referensi |
|---|---|---|
| Baris 4 - pointer `[Database] Riset Fraud JKN` | Ya (substansi di `04-evidence-matrix.md:6`) | 33 entri |
| Baris 5 - pointer `[Sub-page] ARSIP DATA v1` | Ya (`10:4-5` identik) | 100 klaim |
| Baris 217 - pointer `[Sub-page] ARSIP SUMBER DUPLIKAT` | **Tidak** - hanya di 09 | penanda duplikasi internal |
| Baris 219 - "CATATAN KONTROL DOKUMEN" | **Tidak** - hanya di 09 | unilaterally menyatakan jangan dipakai sebagai versi data kedua |
| Baris 429 - pointer `[Database] Klaim Aegis-JKN v2 (300 Baris)` | Ya (`00:20`) | 300 baris |
| Baris 430-431 - tautan **Figma Fishbone Diagram** | **Tidak** - hanya di 09 & `00:27` | `figma.com/board/ePv0sbUCNU9iOgRiTMwH8E/…node-id=0-1` |
| Baris 432 - "CATATAN DOKUMEN" Figma: minta tujuan, tanggal, penulis, ringkasan temuan | **Tidak** - hanya di 09 | tautan Figma juga ada di `00:27` tanpa catatan ini |

**Jawaban: tidak ada konten substansi yang hilang jika 09 diarsipkan.** Seluruh isi numerik 09 = 10 = duplikat. Yang hilang hanya **dua pointer navigasi** (baris 4 dan 429 menuju database Notion) dan **satu tautan Figma + catatan review** yang sudah ada di `00:27`.

### 5.3 Risiko divergensi (double source of truth)

| Risiko | Mekanisme | Dampak |
|---|---|---|
| **D1** | 09 dan 10 menyimpan ground truth sindikat identik di 2 halaman | Edit di salah satu tidak merambat; 14-index (yang menyalin keduanya) akan memuat 4 versi |
| **D2** | 09:110 & 09:322 (dan 10:107) menyebut "8 klaim kontradiksi" - CSV = 12 | Promo baseline sindikat bisa berbeda antar 09/10 |
| **D3** | 09:113/191 "70 edges" vs 09:191/403 "70+ edges" vs `11:209` "10.386 edges" | Tiga angka edge dalam satu file |
| **D4** | 09:117 "10 kekurangan kritis" (tanpa tabel) vs `12:43-52` (6 baris) | Penyebab root "10" tidak pernah diverifikasi |
| **D5** | 09:146-147 & 09:358-359 menduplikasi KLM121/122 dengan mapping RS_A/D03/P04 - CSV = RS_G/D13/P29 | Satu kesalahan ground truth dipecah jadi empat salinan |

**Rekomendasi: arsipkan 09, hapus blok duplikat 09:220-428, dan pertahankan 09:4, 09:429-432 sebagai halaman navigasi tipis** (atau pindahkan pointer Figma ke `00-dashboard.md:27` yang sudah ada). Sumber kebenaran: `10-simulation-dataset.md` untuk isi dataset; `03-dataset-registry.md` untuk definisi aktif.

---

## 6. Audit Tautan Silang: Dokumen Terkendali → Arsip

Hasil grep `app.notion.com/p/` pada 00–08 (Bagian E skrip):

| Dokumen terkontrol | Baris | Target | Wajar (riwayat) atau membingungkan (sumber aktif)? |
|---|---|---|---|
| 00-dashboard | 13 | 01-proposal | **Wajar** - dokumen terkendali |
| 00-dashboard | 14 | 02-architecture | **Wajar** |
| 00-dashboard | 15 | 03-dataset-registry | **Wajar** |
| 00-dashboard | 16 | 04-evidence-matrix | **Wajar** |
| 00-dashboard | 17 | 05-decision-scope | **Wajar** |
| 00-dashboard | 18 | 06-research-notes | **Wajar** |
| 00-dashboard | 20 | Database Klaim v2 (300 baris) | **Wajar** - sumber data aktif |
| 00-dashboard | 21 | Database Riset Fraud (33 entri) | **Wajar** - sumber data aktif |
| 00-dashboard | 22 | 10-simulation-dataset | **Membingungkan** - label "Dokumentasi Dataset Simulasi, 100 Klaim" di `00:22` sudah jujur, tapi `:22` adalah satu-satunya jalan ke 100 klaim yang tidak diberi tanda "versi awal" seperti `10:4` |
| 00-dashboard | 23 | 14-index (Kandidat Ide, sumber awal) | **Wajar** (riwayat) - tapi tanpa penanda "arsip" |
| 00-dashboard | 24 | 11-archive-proposal (Proposal Lengkap, sumber awal) | **Membingungkan** - halaman ini berisi metrik "Tervalidasi" (11:15, 11:326-335). Label "sumber awal" saja tidak cukup |
| 00-dashboard | 25 | 12-archive-architecture | **Membingungkan** - memuat "85% sempurna" (12:127) dan "10 kekurangan" yang tabelnya 6 baris |
| 00-dashboard | 26 | 13-archive-deep-research | **Wajar** - 13 sudah punya "CATATAN EDITORIAL" sendiri (13:4) |
| 00-dashboard | 94 | 07-dataset-v2-catalog | **Wajar** |
| 00-dashboard | 95 | 08-training-protocol | **Wajar** |
| 01–06 | - | (tidak ada tautan app.notion.com) | **Wajar** - dokumen mandiri, tanpa ketergantungan arsip |
| 07-dataset-v2-catalog | 91 | 08-training-protocol | **Wajar** |
| 08-training-protocol | 4, 83 | Database Klaim v2, 07, 02 | **Wajar** |
| 10-simulation-dataset | 3 | 12-archive-architecture | **Wajar (riwayat)** - 10 sudah punya "CATATAN VERSI" (10:4) yang menunjuk 03 sebagai rujukan definisi |
| 10-simulation-dataset | 4 | 03-dataset-registry | **Wajar** |

**Kesimpulan bagian 6:** dokumen terkendali 01–06 **sama sekali tidak pernah** menautkan 11/12/13/14. Semua penautkan ke arsip terkumpul di `00-dashboard.md:22-26` - 4 dari 7 tautan arsip hanya berlabel "sumber awal" tanpa penanda kedalaman arsip. **Perbaikan: ubah label `00:24-25` menjadi "ARSIP SUMBER - sudah superseded, jangan dikutip"**, dan tambahkan penanda yang sama di `00:23`.

Tidak ada **satu pun** dokumen terkendali yang menautkan `09-draft-hub.md` - konsisten dengan statusnya sebagai draft.

---

## 7. Verifikasi Angka vs `claims_v2_live.csv`

Skrip `19_consistency.py` Bagian B menjalankan **51 pemeriksaan**. Hasil: **44 cocok, 7 tidak cocok**.

| # | Angka | Dokumen (file:baris) | Aktual CSV | Status |
|---|---|---|---|---|
| 1 | Jumlah baris dataset aktif = 300 | `00:30`, `03:13`, `01:37` | 300 | ✓ |
| 2 | ID KLM001–KLM300 unik & tak terputus | `00:31,42` | 300 unik | ✓ |
| 3 | auto_clear = 240 | `00:32`, `03:19` | 240 | ✓ |
| 4 | review = 24 | `00:33`, `03:20` | 24 | ✓ |
| 5 | escalate = 36 | `00:34`, `03:21` | 36 | ✓ |
| 6 | risiko low = 240 | `01:37`, `03:25` | 240 | ✓ |
| 7 | risiko medium = 10 | `01:37`, `03:26` | 10 | ✓ |
| 8 | risiko high = 14 | `01:37`, `03:27` | 14 | ✓ |
| 9 | risiko fraud = 36 | `01:37`, `03:28` | 36 | ✓ |
| 10 | Total nominal = Rp3.526.650.000 | `00:35`, `03:36`, `01:66` | Rp3.526.650.000 | ✓ |
| 11 | Nominal auto_clear = Rp2.685.550.000 | `03:34`, `01:67` | Rp2.685.550.000 | ✓ |
| 12 | Nominal review = Rp279.950.000 | `03:35`, `01:68` | Rp279.950.000 | ✓ |
| 13 | Nominal escalate = Rp561.150.000 | `03:36`, `01:69` | Rp561.150.000 | ✓ |
| 14 | Label anomali total = 60 | `11:348`, `10:113` | 60 | ✓ |
| 15 | Nominal 60 klaim anomali = Rp841.100.000 | `11:348` | Rp841.100.000 | ✓ |
| 16 | Baris dengan Sindikat terisi = 36 | `11:348`, `10:134-145` | 36 | ✓ |
| 17 | **Nominal baris bersindikat = Rp542.560.000** | `11:348` | **Rp539.650.000** | ✗ |
| 18 | Pasien unik v2.1 = 40 | `10:120` | 40 | ✓ |
| 19 | Dokter unik v2.1 = 20 | `10:119` | 20 | ✓ |
| 20 | Faskes unik v2.1 = 10 (RS_A–RS_J) | `10:118` | 10 | ✓ |
| 21 | Pasien unik pada 100 klaim pertama = 20 | `10:6` | 20 | ✓ |
| 22 | **Dokter unik pada 100 klaim pertama = 12** | `10:6` | **11** (D06 tidak muncul) | ✗ |
| 23 | Faskes unik pada 100 klaim pertama = 6 | `10:6` | 6 (RS_A–RS_F) | ✓ |
| 24 | Distribusi label 100 klaim pertama = 76/4/6/14 | `10:7` | 76/4/6/14 | ✓ |
| 25 | Sentimen 100 klaim pertama = 62/14/24 | `10:108` | 62/14/24 | ✓ |
| 26 | **Kontradiksi narasi = 8 klaim** | `10:107`, `10:203` | **12** (KLM001-006, 018, 024, 105-108) | ✗ |
| 27 | **Baris LOS kosong = 109** | `00:36`, `03:78` | **kosong = 0, bernilai "0" = 109** | ✗ |
| 28 | Baris Alasan kosong = 1 | `00:37` | 1 | ✓ |
| 29 | Properti Modus kosong = 240 | `03:80` | 240 | ✓ |
| 30 | Properti Sindikat kosong = 264 | `03:81` | 264 | ✓ |
| 31 | Catatan riset = 33 entri | `00:38`, `04:10` | 33 | ✓ |
| 32 | Status verifikasi riset 18/11/4 | `04:12-14` | 18/11/4 | ✓ |
| 33 | Relevansi riset 11/18/4 | `04:15-17` | 11/18/4 | ✓ |
| 34 | Rata-rata skor auto_clear = 0,086 | `11:338` | 0.086 | ✓ |
| 35 | Rata-rata skor review = 0,591 | `11:338` | 0.591 | ✓ |
| 36 | Rata-rata skor escalate = 0,869 | `11:338` | 0.869 | ✓ |
| 37 | Ambang fraud ≥ 0,80 inklusif (min = 0,80) | `03:46` | min fraud = 0.8 (KLM115) | ✓ |
| 38 | Skor high 0,62–0,79 (tidak ada 0,80) | `10:9` | 0.62–0.79 | ✓ |
| 39 | Skor medium 0,40–0,53 | `10:9` | 0.40–0.53 | ✓ |
| 40 | Skor low 0,04–0,14 (bukan <0,35 penuh) | `10:9` | 0.04–0.14 | ✓ |
| 41 | Fraud tanpa sindikat = 2 tunggal | `10:134` | 2 (KLM121, KLM122) | ✓ |
| 42 | **KLM121 faskes = RS_A** | `10:143` | **RS_G** | ✗ |
| 43 | **KLM122 faskes = RS_E** | `10:144` | **RS_H** | ✗ |
| 44 | Skor KLM121 = 0,81 (dokumen "≥0,85") | `10:143` | 0.81 | ✓ (nilai) / dokumen overstated |
| 45 | Skor KLM122 = 0,82 (dokumen "≥0,80") | `10:144` | 0.82 | ✓ |
| 46 | **Nominal modus Upcoding = Rp127.680.000** | `11:348` | **Rp156.900.000** | ✗ |
| 47 | Nominal modus Phantom Billing = Rp134.250.000 | `11:348` | Rp134.250.000 | ✓ |
| 48 | Nominal modus Repeat Billing = Rp61.600.000 | `11:348` | Rp61.600.000 | ✓ |
| 49 | Total nominal fraud = Rp561.150.000 | `11:347` | Rp561.150.000 | ✓ |
| 50 | Rasio 264 non-fraud : 36 fraud = 1:7,33 | `11:321` | 264 / 36 | ✓ (label "normal" menyesatkan - 24 di antaranya anomali) |
| 51 | Komposisi sindikat per CSV: SYND-01 n=3, 02 n=3, 03 n=6, 04 n=2, 05 n=2, 06 n=4, 07 n=4, 08 n=6, 09 n=6 | `10:134-142` | identik | ✓ |

### Verifikasi tambahan (di luar skrip)

| Temuan | Sumber |
|---|---|
| SYND-05 (KLM016, KLM017) berlabel **high**, bukan **fraud** - padahal `10:138` menaruhnya di tabel sindikat fraud | CSV |
| KLM019–KLM036 di `11:301-304` seluruhnya berlabel **low** di CSV | CSV |
| SYND-06 → P21-P22; SYND-07 → P23-P24; SYND-08 → P25-P26; SYND-09 → **P27 saja** (bukan P35-P40) | CSV |
| 12 klaim dengan `Alasan` kosong - `00:37` benar | CSV |
| Alasan berjenjang: NORMAL 239, FRAUD 36, ANOMALI TINGGI 14, ANOMALI SEDANG 10, kosong 1 → **"ANOMALI 24"** benar (`10:129`) | CSV |
| Total edge 11:209-211 = 10.386 + 15.202 + 7.880 = **33.468**, bukan 70 | aritmetika |
| `10:120`-"P01-P40" vs CSV: 40 pasien ada, tetapi 11 di antaranya tidak dipakai sindikat | CSV |

---

## 8. Tabel Istilah Global

| Kategori | Kanonik yang disarankan | Varian yang dipakai | Lokasi varian |
|---|---|---|---|
| Nama produk | **Aegis-JKN** | `AEGIS-JKN` | 11:12, 11:23, 11:31, 11:140, 11:170, 11:206 (7×); 14 (7×) |
| | | `aegis-jkn` (lowercase, di path repo & URL) | 09:187 (tree `aegis-jkn/`), 12:146 |
| | | `aegisjkn` (domain, tanpa separator) | `http://aegisjkn.vercel.app` - 10:3, 09:6, 12:118, 14 (6×) |
| | | `Aegis JKN` (spasi) | - |
| Nama kompetisi | **Healthkathon 2026** | `HEALTHKATHON 2026` | 11 (1×), 14 (1×) |
| | | `BPJS Kesehatan Healthkathon 2026` | 11 (1×), 14 (1×) |
| | | `HEALTHKATHON Project Dashboard` (nama halaman dashboard) | 09:432, 14:44, 14:1122 |
| | | `Hackathon BPJS Kesehatan` | 14:3 |
| Akronim model | **MHGSL** + satu ekspansi kanonik | `Multi-Hop Graph Structure Learning` | 11:12, 23, 31, 140, 170, 206, 429 (7×); 14 (7×) |
| | | `Multi-Channel Heterogeneous Graph Structure Learning` | 11 (4×), 12:30 (4×), 14 (8×) |
| | | `Multi-Channel Graph Structure Learning` | 12:33, 12 (1×), 14 (1×) |
| | | `Tri-Channel MHGSL GNN` | 11:316 |
| | **Rekomendasi:** pilih **Multi-Channel Heterogeneous Graph Structure Learning (MHGSL)** karena itu satu-satunya yang sesuai dengan arsitektur 3 kanal + heterogeneous graph di `02:29-36`, dan cocok dengan judul tabel `12:33` |
| Label status | **`auto_clear`** (literal nilai DB) | `auto-clear` | 01:9, 01:37, 02:62, 11:30, 11:321, 11:338 (6×); 14 (6×) |
| | | `Auto-clear` | 02:62 |
| Label risiko | **`low` / `medium` / `high` / `fraud`** | `fraud-scenario` | 00:60, 02:60 |
| | | `NORMAL` / `ANOMALI` / `FRAUD` (nilai `Alasan`) | 10:129-131, 09:132-134 |
| | | `ANOMALI TINGGI` / `ANOMALI SEDANG` (nilai `Alasan` aktual) | CSV |
| | | `Hijau, Kuning, Merah` (traffic light) | 11:319 - **tidak dipakai di mana pun lagi** |
| Label biaya | **`Biaya Rp`** (nama kolom) | `biaya` / `log_biaya` | 11:206 |
| Istilah sindikat | **`Sindikat` (nilai kolom)** + `SYND-01`..`09` | `fraud ring` / `fraud rings` | 11 (5×), 12 (2×), 14 (7×) |
| | | `sindikat` | 09/10 |
| Entitas RS | **`Faskes` (nilai kolom, `RS_A`..`RS_J`)** | `FKRTL` | 10:6, 10:118, 11:149, 12:119 |
| | | `RS` / `rumah sakit` | 10:9, 11:150 |
| | | `RS_A` vs `RS Aegis Medika A` (nama vs ID) | 10:9, 10:22 |
| Graf | **3 kanal: Topologi / Fitur / Semantik** | `A_top` / `A_feat` / `A_sem` | 11:209-211 |
| | | `kanal` vs `saluran` | 02:36, 06:26 (`kanal`) vs 10:12, 11:209 (`saluran`) |
| | | `Tri-Channel` | 11:316 |
| Status HTTP/verifikasi | **`auto_clear` / `review` / `escalate`** | `Status` | 03:65 |
| | | `Alasan` 3-tingkat vs `Modus` | 10:126-131 |

---

## 9. Rekomendasi - Kanonik per Konflik

### Prioritas 1 - sebelum judges membaca (KRITIS)

| # | Aksi | File:baris |
|---|---|---|
| 1 | Tambahkan banner "ARSIP SUMBER - angka di halaman ini sudah disuperseded oleh dokumen 00–08. Jangan dikutip sebagai hasil final" di baris 1 | `11:1`, `12:1`, `14:1` |
| 2 | Ubah "Tervalidasi" → "Draf, belum tervalidasi" pada KPI table | `11:326-335`, `14:801-810` |
| 3 | Ubah "Rp507.370.000 (Penyelamatan Riil)" → "Rp507.370.000 (estimasi draf, belum reproducible per klaim)" | `11:347-348`, `14:822-823` |
| 4 | Hapus "Desain Aegis-JKN sudah 85% sempurna" → ganti "Desain v2.1 belum lolos 10 gerbang; lihat 08 §4" | `12:127` |
| 5 | Hapus "10 deficiency" → become "6 deficiency teridentifikasi (tabel berikut); tinjauan lanjutan-chief" | `12:23`, `12:42`, `10:115` |
| 6 | Perbaiki label tautan: hapus kata "v2.1" dari `12:53` (halaman itu berisi 100 klaim) | `12:53`, `14:957` |

### Prioritas 2 - konsistensi ground truth (TINGGI)

| # | Aksi | File:baris |
|---|---|---|
| 7 | **Hapus tabel sindikat arsip** `11:296-304` dan ganti pointer ke `10:134-142` (sudah dikonfirmasi CSV) | `11:296-304` |
| 8 | Perbaiki `10:139-142`: rentang pasien → P21-P22 / P23-P24 / P25-P26 / P27; dokter SYND-09 → D19 | `10:139-142` |
| 9 | Perbaiki `10:143-144`: KLM121 → RS_G/D13/P29/skor 0.81; KLM122 → RS_H/D14/P30/skor 0.82 | `10:143-144`, `09:146-147,358-359` |
| 10 | Perbaiki "12 dokter" → "11 dokter" (D06 tidak muncul di 100 klaim pertama) | `10:6`, `09:9` |
| 11 | Perbaiki "8 klaim kontradiksi" → 12, dan daftar ID diperbarui | `10:107`, `10:203`, `09:110,206,322,418` |
| 12 | Perbaiki "109 baris LOS kosong" → "109 baris bernilai 0 (tidak ada nilai kosong)" | `00:36`, `03:78` |
| 13 | Perbaiki nominal modus Upcoding → Rp156.900.000; sindikat → Rp539.650.000 | `11:348`, `14:823` |
| 14 | Kunci ambang skor di satu file konfigurasi dengan definisi inklusif: low <0.35; medium [0.35,0.60); high [0.60,0.80); fraud ≥0.80 | `10:9`, `03:46`, `08:37-38` |
| 15 | Sinkronkan baseline: `08:33` harus menyebut stack final (XGBoost+SMOTE, MLP) atau `10:162-163`/arsip disesuaikan | `08:33`, `10:162-163`, `12:167-168` |
| 16 | Satu kanon untuk edge count: pertahankan 33.468 (11:209-211) atau turunkan ke "belum dibangun"; hapus "70 edges" / "70+ edges" | `10:110,188`, `12:65,150`, `09:113,191` |

### Prioritas 3 - struktur & duplikasi (SEDANG)

| # | Aksi | File:baris |
|---|---|---|
| 17 | Arsipkan `14-index.md` dengan banner + 3 penanda superseded; pindahkan blok 1122-1939 ke atas | `14:1,490,505,622,640,657,684-686,796,801-825,838,847,877` |
| 18 | Arsipkan `09-draft-hub.md`; hapus blok duplikat `09:220-428`; pindahkan tautan Figma + catatan ke `00:27` | `09:217-428`, `00:27` |
| 19 | Perbarui label tautan dashboard: `00:22-25` → "ARSIP SUMBER - jangan dikutip sebagai sumber aktif" | `00:22-25` |
| 20 | Konsistenkan istilah: `auto_clear` (literal DB) dan `MHGSL = Multi-Channel Heterogeneous Graph Structure Learning` | `01:9,37`, `02:62`, `11:12,23,31,140,170,206,429`, `12:30,33` |
| 21 | Ganti "Tri-Channel"/"traffic light Hijau-Kuning-Merah" yang tidak lagi dipakai dengan istilah kanonik | `11:316`, `11:319` |
| 22 | Tutup D-01 s/d D-06 di `02:108-114` (status "Terbuka" sejak 21 Oktober) dan checklist `05:73-77` | `02:108-114`, `05:73-77` |

### Kanon final yang direkomendasikan

| Topik | Sumber kebenaran tunggal |
|---|---|
| Jumlah/komposisi dataset | `03-dataset-registry.md` + `claims_v2_live.csv` |
| Definisi label & ambang skor | `03-dataset-registry.md` §4 (dengan konfigurasi ambang terpusat) |
| Ground truth sindikat | `10-simulation-dataset.md:134-142` **setelah** dikoreksi ke CSV |
| Status bukti performa | `04-evidence-matrix.md` E-01..E-12 + `00-dashboard.md:47-49` |
| Prosedur pelatihan | `08-training-protocol.md` |
| Konten historis / rekam jejak | `11`, `12`, `13`, `14` (arsip, non-kuotatif) |

---

## Lampiran: Reproduksi

```
python -I N:\HEALTHKATHON\analysis\reports\scripts\19_consistency.py
# output: N:\HEALTHKATHON\analysis\reports\scripts\19_consistency_output.txt
```

Bagian A (ekstraksi angka/dokumen) · B (51 verifikasi CSV) · C (embedding 14-index) · D (duplikasi 09) · E (tautan silang) · F (istilah global).
