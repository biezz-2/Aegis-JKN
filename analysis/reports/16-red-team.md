# RED TEAM - SERANGAN TERHADAP PROPOSAL & KODEBASE "Aegis-JKN"

**Target:** `N:\HEALTHKATHON\Aegis-JKN` + korpus proposal `N:\HEALTHKATHON\analysis\corpus\`
**Data:** `N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv` (300 baris, 29 kolom)
**Bukti kuantitatif:** `N:\HEALTHKATHON\analysis\reports\scripts\16_redteam.py` (stdlib-only, exit 0)
**Output mentah:** `N:\HEALTHKATHON\analysis\reports\16_redteam_output.txt` · `16_redteam_numbers.json`
**Tanggal serangan:** 2026-10-22

> Dokumen ini adalah **serangan**, bukan review jujur. Tujuannya: mencari cara termurah untuk ekspos proposal ini sebagai **awake / bohongan / menyesatkan** di depan juri Healthkathon BPJS Kesehatan 2026 atau reviewer akademis. Setiap temuan menyertakan `file:baris` atau sumber data/URL sehingga bisa diverifikasi ulang secara independen.
> Semua perhitungan dijalankan ulang lewat skrip; tidak ada angka di dokumen ini yang tidak berasal dari eksekusi skrip.

---

## 1. RINGKASAN EKSEKUTIF

Proyek ini **tidak runtuh karena modelnya jelek. Ia runtuh karena tidak ada modelnya.**

Tiga serangan yang paling merusak, karena ketiganya membongkar fondasi - bukan detail:

1. **Novelty-nya sudah publik dan itu ditulis sendiri di dalam corpus.** "MHGSL" adalah metode dari Hong et al., *Heliyon* 2024, DOI `10.1016/j.heliyon.2024.e30045` / PMID `38694097`, dengan **tiga channel yang persis sama** (topologi, fitur, semantik). Corpus mengakui ini di `corpus/12-archive-architecture.md:30`. Yang tersisa sebagai kebaruan hanyalah *localisasi* Indonesia + UX human-in-the-loop - bukan algoritma. Klaim "state-of-the-art" (lihat `12-archive-architecture.md:30`) padahal mengutip paper yang sama sebagai sumber adaptasi.

2. **Dua oracle sempurna bocor di dalam CSV yang dikirim ke publik.** `Sinyal SHAP` sendiri adalah **1-bit oracle**: "ada/tidak ada sinyal dominan" memberi **accuracy 1.0000, precision 1.0000, recall 1.0000** (TP=60, FP=0, FN=0, TN=240) terhadap label anomali. `Kontribusi Saluran` (T/F/S) secara individual **memisahkan fraud dari normal dengan sempurna** (precision 1.0000, recall 1.0000 pada T>=0.120, F>=0.110, S>=0.090; min-fraud > max-normal di ketiga channel). Kedua kolom **secara eksplisit dilarang** jadi fitur oleh `corpus/03-dataset-registry.md:84` (sec.7 Aturan Anti-Leakage) - dan keduanya justru **dikirim** di file data live. Penjaga yang dijanjikan 14 halaman korpus (`tests/test_leakage.py`) **tidak ada di disk**.

3. **Rp507.370.000 bukan hasil hitung - itu angka yang disesuaikan setelah faktanya, dan tabel per-modusnya memuat bukti forensik.** `11-archive-proposal.md:348` sendiri memuat rincian: Phantom Billing Rp134.250.000, Upcoding Rp127.680.000, Repeat Billing Rp61.600.000. Dari CSV: **claimed Phantom Billing = nominal persis** (Rp134.250.000 = 100% nilai klaim, tanpa pengurangan tarif sama sekali), **claimed Repeat Billing = nominal persis** (Rp61.600.000). Artinya "kerugian" didefinisikan sebagai **100% nilai tagihan**. Dan yang lebih fatal: **ketiga klaim Phantom Billing (Rp44.750.000) berada DI BAWAH tarif INA-CBG publik proyek sendiri (81.52 = Rp46.500.000)** - jadi overcharge-nya **nol**, bukan Rp134 juta. Total overcharge yang benar-benar bisa diturunkan dari tarif resmi proyek = **Rp31.350.000**, yaitu **16,18× lebih kecil** dari klaim.

Di atas itu, **93,0% akurasi berada DI BAWAH baseline sepele** pada prevalensi lapangan yang dipakai proyek sendiri: pada p=3%, model yang **tidak menandai apa pun** sudah mencapai 97,0%. Angka 93,0% hanya 5,0 poin di atas "flag nothing" pada p=12% - dan itu pada data yang sama.

### Tabel severity

| Severity | Jumlah temuan | Arti |
|---|---|---|
| **KRITIS** (falsifiable, merusak inti klaim) | 5 | #1 Novelty = paper yang sudah publik (Heliyon 2024) - ditulis sendiri di corpus |
| | 2 | #2 `Sinyal SHAP` = oracle sempurna (acc/prec/rec = 1.0000) di CSV live |
| | 3 | #3 `Kontribusi Saluran` = pemisah sempurna fraud/normal per channel |
| | 4 | #4 Rp507.370.000 = 16,18x nilai yang bisa diturunkan; "loss" = 100% nilai tagihan |
| | 5 | #5 Akurasi 93,0% < baseline sepele (97,0%) pada prevalensi lapangan 3% |
| **TINGGI** (kerusakan kredibilitas / etika) | 7 | #6 Guard anti-leakage `tests/test_leakage.py` tidak ada; 13 sitasi |
| | 7 | #7 10/11 angka utama **tidak dapat direproduksi** (tak ada split, prediksi, artefak); presisi 94,12% mustahil di ambang mana pun, FPR 10,6% hanya di ambang 0,14 |
| | 8 | #8 `Alasan` = templat terbalik: 211 string -> 55 setelah dihapus angkanya; 119 mengulang fitur |
| | 9 | #9 Dataset = 300 vs 100; prevalensi 12% vs 14%; AUPRC lift 20% vs 28,6% |
| | 10 | #10 `Status` adalah fungsi deterministik dari `Risiko` (36/36, 14/14, 10/10, 240/240) |
| | 11 | #11 Nama dokter nyata (20 dokter + kredensial Sp.) di dataset publik |
| | 12 | #12 Repo tanpa pipeline: 0 .py, 0 .ipynb, 0 artefak model; angka = literal di `data.ts` |
| **SEDANG** (kontradiksi internal / parsing) | 4 | #13 Denominator "Rp8,46 juta per kasus fraud" = dibagi 60 (anomali), bukan 36 fraud |
| | 14 | #14 `Kontradiksi Narasi` = flag 3-tingkat di dalam kelas anomali (12 baris) |
| | 15 | #15 SYND-01..09 "menguasai 36 klaim (60% kasus fraud)" - 36 = 100% fraud, 60% anomali |
| | 16 | #16 `Sentimen` negatif (n=72) bukan kontrol negatif: 41,7% anomali |
| **TERDAKAT** (poles / rekam) | 3 | #17 SUS 82,5 tanpa responden, protokol, atau data mentah |
| | 18 | #18 Throughput 3,2x dan waktu -45% tanpa load test / timing mentah |
| | 19 | #19 Prevalensi 3-7% = "estimasi literatur" bersumber GAO-24-105833 (federal AS, non-kesehatan) |
| | | |
| **TOTAL** | **19** | |

---

## 2. TABEL 10 SERANGAN TERKECAS

| No | Serangan | Hashanya credible? | Bukti | Kerusakan yang ditnimpa | Counter yang harus disiapkan |
|---|---|---|---|---|---|
| 1 | **"MHGSL" adalah metode yang sudah dipublikasikan.** Klaim state-of-the-art berasal dari paper yang dipakai sebagai sumber adaptasi. | **Sangat tinggi.** Dijawab dalam 5 detik dari corpus sendiri. | `12-archive-architecture.md:30` - "diadaptasi dari paper Hong et al., Heliyon 2024". DOI `10.1016/j.heliyon.2024.e30045`, PMID `38694097`, 3 channel identik (topological structure / features / semantic). Prior art lain: HMF-GNN IEEE ICME 2022 (DOI `10.1109/ICME52920.2022.9859871`); *Scientific Reports* 2025 HINormer (DOI `10.1038/s41598-025-22910-6`, PMID `41285829`, F1 84%); InSureNet IEEE 2025; HeFDN; HEMClust; EIGF; IJDS DOI `10.5267/j.ijdns.2026.8.019`. | Menghancurkan **positioning** ("novelty"). Proposal berubah menjadi *implementasi lokal* dari metode yang sudah ada - dan metode itu **punya** basis pengujian, dataset nyata, dan tabel baseline yang jauh lebih kuat. | Akui: "Algoritme MHGSL **bukan** kontribusi kami; kontribusi kami adalah (a) **dataset simulasi ter-label JKN** dalam bahasa Indonesia, (b) **desain human-in-the-loop + XAI** untuk verifikator BPJS, (c) **provenance & reproducibility discipline**. Kebaruan domain, bukan kebaruan algoritme." |
| 2 | **`Sinyal SHAP` = oracle sempurna di CSV yang dikirim.** Satu bit "ada sinyal / tidak ada sinyal dominan" memprediksi label anomali **tanpa salah sekali**. | **Sangat tinggi.** Auditor cukup buka CSV, buat 1 baris filter, dapat akurasi 100%. | Skrip §3a: TP=60, FP=0, FN=0, TN=240 → accuracy/precision/recall = **1.0000**. Contoh baris: `claims_v2_live.csv:2` (KLM285, low, "tidak ada sinyal dominan"), `claims_v2_live.csv:281` (KLM001, fraud, "inkonsistensi diagnosis-prosedur..."). Kolom ini **dilarang** jadi fitur oleh `03-dataset-registry.md:84`. | Menghancurkan **setiap metrik yang diklaim**. 93,0% / 94,12% / 0,9825 / 0,9142 bisa dicapai tanpa model. Kalau juri menemukan ini, semua hasil becomes "tabel hallucinasi". | **Hapus `Sinyal SHAP` dari file yang dibagikan sebagai dataset fitur**, pindahkan ke `outputs/` terisolasi, dan tulislah `tests/test_leakage.py` sungguhan. **Jangan** klaim performa apa pun sampai guard ada dan hijau. |
| 3 | **`Kontribusi Saluran` = pemisah sempurna fraud vs normal, per channel.** T, F, dan S masing-masing cukup. | **Sangat tinggi.** Angka yang bisa dihitung dari CSV dalam satu baris Python. | Skrip §3b: fraud mean T=0,2647 / F=0,3050 / S=0,2925; normal mean T=0,0328 / F=0,0296 / S=0,0237. **min-fraud > max-normal di ketiga channel.** T≥0,120 → precision 1,0000 recall 1,0000 (TP=36, FP=0); F≥0,110 → sama; S≥0,090 → sama. Dilarang oleh `03-dataset-registry.md:84`. | Sama seperti #2 - ditambah nama "multi-channel graph learning" jadi tidak relevan: **satu threshold skalar per channel sudah cukup**. Seluruh arsitektur GCN/shared-parameter tidak menambah apa pun. | Sama: keluarkan dari feature set; bila "Kontribusi Saluran" adalah **output** model, jangan pernah disimpan berdampingan dengan input dalam file yang sama. |
| 4 | **Rp507.370.000 = angka yang disesuaikan setelah faktanya; rincian per-modusnya memuat bukti forensik.** | **Sangat tinggi.** Tiga modus eksak cocok dengan CSV, dan dua di antaranya justru *di bawah tarif*. | `11-archive-proposal.md:348` & `14-index.md:823`. Skrip §5d-bis/§5d-ter: claimed Phantom Billing Rp134.250.000 = **nominal persis**; claimed Repeat Billing Rp61.600.000 = **nominal persis** → "loss" = **100% nilai tagihan, tanpa pengurangan tarif**. Tapi tarif resmi proyek sendiri (`10-simulation-dataset.md:78-87`): 81.52 = Rp46.500.000 vs klaim Rp44.750.000 → **di bawah tarif Rp1.750.000**, overcharge **nol**. Total overcharge dari tarif resmi = **Rp31.350.000**; klaim **16,1841×** lipatnya. Angka 60,32% sendiri **benar** (Rp507.370.000 / Rp841.100.000 = 0,603222) - jadi ini **fudge factor terpisah** yang diterapkan untuk menghasilkan angka bulat. Action item `03-dataset-registry.md:110` ("Tentukan tarif acuan…") masih **unchecked**. | Meruntuhkan **seluruh argumen ROI / dampak finansial**, termasuk klaim "ratusan miliar" dan Cost-to-Impact 1:15. | **Hapus angka ini dari proposal.** Bila tetap dipakai: wajib menyertakan tabel tarif acuan per ICD-9-CM, ledger per klaim (`claimed − tarif`), dan status adjudikasi. Sekaligus **perbaiki** angka "Rp8,46 juta per kasus fraud" - itu dibagi 60 (anomali), bukan 36 fraud (→ Rp14.093.611). |
| 5 | **Akurasi 93,0% di bawah baseline sepele pada prevalensi lapangan yang dipakai proyek sendiri.** | **Sangat tinggi.** Satu kalimat, tanpa data tambahan. | Skrip §2b: pada p=3% "flag nothing" = **97,0%**; p=5% = 95,0%; p=7% = 93,0%; p=12% = 88,0%. Jadi 93,0% **tidak lebih baik dari tidak menandai apa pun** pada 3% dan 5%. Presisi pada operating point yang sama (recall 0,90, FPR 0,106): **0,5366 (p=12%) → 0,2080 (p=3%)**. FPR 10,6% pada 264 klaim bersih = **28 false positive**. | Membunuh **argumen performa** dan membuka pintu "ini cuma base-rate artifact". | Ganti headline dengan **AUPRC pada prevalensi 3–7%** + **kurva PR** + operating point nyata, bukan akurasi. Ini persis yang sudah diminta corpus (`12-archive-architecture.md:50`) tapi tidak pernah dikerjakan. |
| 6 | **Penjaga anti-leakage yang dijanjikan 14 halaman korpus tidak ada di disk.** | **Tinggi.** Cek satu baris. | `tests/test_leakage.py` disitasi **13×** di 4 file (`09-draft-hub.md:157,369`; `10-simulation-dataset.md:154`; `12-archive-architecture.md:47,141,174,180`; `14-index.md:200,412,951,1045,1078,1084`) - termasuk tabel yang menandai ✅ "Blokir di configs/leakage.yaml + unit test otomatis". Skrip §9: `leakage controls present: NONE FOUND`; `configs/leakage.yaml`, `data/raw/leakage_blocklist.yaml`, `data/raw/claims_300_v2.1.csv`, `data/raw/edges_v2.1.json`, `data/processed/features_300.parquet`, `data/processed/graph_hetero.pt` - **semua MISSING**. `tests/` hanya berisi 3 file `.sh`. | Menghancurkan **provenance & reproducibility** - pilar utama proposal. | Tulis guard-nya **sekarang**, jalankan, lampirkan log hijau. Integrity Data harus dibuktikan dengan **file**, bukan tabel markdown. |
| 7 | **10 dari 11 angka utama tidak dapat direproduksi.** Tidak ada split, prediksi, atau artefak model. | **Tinggi.** Corpus sendiri sudah mengatakannya, lalu mengabaikannya di proposal. | Skrip §5: ROC-AUC, AUPRC, masking robustness, time reduction, throughput, SUS, AUPRC lift, FN reduction → **semuanya NO**. Accuracy "PARTIAL (arithmetically possible, not empirically checkable)". **Presisi 94,12% NO** (0 ambang dari 46 nilai unik `skor_fraud`; terdekat 94,7368% di ambang 0,78). **FPR 10,6% PARTIAL**: reachable hanya di ambang 0,14 (FP = 28 dari 264 negatif = 10,6061%), yang memberi presisi hanya 56,25%. Jadi **tidak ada satu ambang yang memenuhi kedua klaim itu** - dan di ambang tempat FPR benar, presisi 56,25%, bukan 94,12%. `06-research-notes.md:42-45` sudah menandai "Belum dapat direproduksi"; `01-proposal.md:70` sudah menarik angkanya - **tapi `11-archive-proposal.md:30` dan `14-index.md:505` tetap memuatnya**. `Skor Fraud` vs `Risiko` → ROC-AUC **1,000000** (trivial, by construction), jadi 0,9825 jelas dari run lain yang tidak dilepas. | Merusak: semua klaim kuantitatif jadi tidak punya bukti pendukung. | Publikasi **satu** artefak reproduktibel (split, prediksi held-out, skrip metrik) memblokir 10 temuan sekaligus. Kalau belum siap, **biarkan angkanya tetap tercabut**. |
| 8 | **Ground truth "`Alasan`" adalah template yang dibalik dari fitur yang dilihat model.** | **Tinggi.** | Skrip §3c/§4: 211 string distinct → **55** setelah angka dihapus; 239 baris diawali literal "NORMAL" / "FRAUD (...)"; **119** baris mengulang fitur kuantitatif ("rasio 1.03", "tarif paket"); **13** baris mengulang string `Modus` verbatim; di kelas anomali (60 baris) prefix tag cocok Risiko **60/60, 0 salah**. | Membongkar **circularity validasi**: author rules = penulis label. Validasi model atas label ini tidak mengukur apa pun. | Pisahkan **fitur** dari **justification** secara fisik (dua file, dua release). Label harus berasal dari proses adjudicasi yang independen, atau set minimal dengan *review rubric* yang diaudit. |
| 9 | **Tiga kontradiksi internal pada halaman yang berbeda.** | **Tinggi.** | (i) Prevalensi **12%** (`03-dataset-registry.md:30` & §3.2) vs **14%** (`10-simulation-dataset.md:10`, `09-draft-hub.md:13`); dashboard publik masih `total_claims:100, prevalensi:14` (`public/dashboard-aegis-jkn.html:1071`) padahal app mengirim 300 KLM (`src/data/notion-datasets.ts`). (ii) AUPRC lift **+28,6%** (`11-archive-proposal.md:30`) vs **+20%** (`12-archive-architecture.md:30`) - hitungan sebenarnya 28,76% dan 28,17%, **tidak satu pun 20%**. (iii) `status: "SESUAI"` di JSON dashboard padahal `total_claims` masih 100. | Menunjukkan **tidak ada satu sumber kebenaran** - juri yang membaca dua halaman akan menemukan ini dan langsung berhenti percaya. | Satu **register metrik** (single source of truth), di-generate dari skrip, lalu seluruh dokumen mengutip itu. |
| 10 | **Nama dokter dengan kredensial nyata di dataset publik; false-positive jadi daftar tuduhan.** | **Tinggi.** | 20 dokter (mis. `dr. Mulyadi Santoso, Sp.B`, `dr. Gunawan Halim, Sp.B`, `dr. Adnan Prakoso, Sp.BTKV`), 40 pasien, 10 faskes; **100% dapat dilacak** (nama + kode klinik + tanggal). Laju anomali per dokter: D19 **44,0%**, D01 40,0%, D11 33,3%, D15 32,1%, D09/D07 31,6%. Laju per klinik: RS_B 28,6%, RS_I 27,8%, RS_J 26,2%. `src/components/dataset/dataset-explorer.tsx:1951` menampilkan "SYND-07 (RS_G & Dr. Mulyadi)". | **Kerugian etis & hukum (UU PDP 27/2022).** Di deployment, ini jadi daftar tuduhan terarah terhadap klinik kecil - dan dataset tidak diberi label "sintetis" di UI. | **Pseudonimisasi wajib** di release: `D01`/`P01`/`RS_A` (seperti `10-simulation-dataset.md:134` yang sudah pakai), plus **label "SINTETIS" yang terlihat** di setiap halaman. Hapus nama asli dari `notion-datasets.ts` sebelum publish. |

---

## 3. DETAIL HITUNGAN NUMERIK (DENGAN KODE)

Skrip: `N:\HEALTHKATHON\analysis\reports\scripts\16_redteam.py` - stdlib only (`csv, json, math, os, re, sys, collections`), tanpa pandas.
Output lengkap: `N:\HEALTHKATHON\analysis\reports\16_redteam_output.txt` · `16_redteam_numbers.json`.

### 3.1 Serangan prevalensi - akurasi 93,0% adalah artefak base-rate

```python
# 2b. The real overclaim: accuracy 93% is a BASE-RATE ARTEFACT
#   Trivial baseline = "always predict NOT fraud" = 1 - p
for p in (0.03, 0.05, 0.07, 0.12, 0.20):
    print("p=%.2f  'always say NOT fraud' accuracy = %.4f" % (p, 1 - p))
```

Hasil (`16_redteam_output.txt` §2b):

```
  p=0.03   'always say NOT fraud' accuracy = 0.9700   <-- klaim 0.9300 KALAH
  p=0.05   'always say NOT fraud' accuracy = 0.9500   <-- klaim 0.9300 KALAH
  p=0.07   'always say NOT fraud' accuracy = 0.9300   <-- sama, nol nilai tambah
  p=0.12   'always say NOT fraud' accuracy = 0.8800   <-- klaim hanya +5.0 poin
```

Membalik persamaan akurasi untuk melihat operating point apa saja yang bisa menghasilkan 93,0%:

```python
# 2a. decode the accuracy-93% claim
#   TP = R*p,  FP = FPR*(1-p),  TN = (1-FPR)*(1-p),  FN = (1-R)*p
#   accuracy A = TP + TN = R*p + (1-FPR)*(1-p)
#   => for a given A and p, FPR = 1 - (A - R*p)/(1-p)
#   => precision = R*p / (R*p + FPR*(1-p))
for p in (0.03, 0.05, 0.07, 0.12, 0.20):
    for R in (0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 1.00):
        FPR = 1.0 - (A - R * p) / (1 - p)
        prec = (R * p) / (R * p + FPR * (1 - p))
```

Keluaran kunci:

```
  p = 0.03 : presisi maksimum yang mungkin pada A=0,93  = 0.3000 (recall 1.00, FPR 0.0722)
  p = 0.05 : presisi maksimum yang mungkin pada A=0,93  = 0.4167
  p = 0.12 : presisi maksimum yang mungkin pada A=0,93  = 0.8571
```

Base-rate drift (sec.2d) - model sama, prevalensi berubah:

```
  train p=0.12 -> test p=0.03 : presisi 0.5366 -> 0.2080  (recall ditahan 0.90)
  train p=0.12 -> test p=0.05 : presisi 0.5366 -> 0.3089
  train p=0.12 -> test p=0.07 : presisi 0.5366 -> 0.3899
```

AUPRC baseline acak = prevalensi (sec.2c): klaim 0,9142 di p=12% adalah **7,6x lift**; di p=3% baseline acaknya 0,03 dan degradation realistis 3-6x, bukan yang dilaporkan. Overclaim ada dua arah: **akurasi** terlihat bagus padahal basenya sudah tinggi, **presisi** justru jauh lebih rendah dari yang dilaporkan.

### 3.2 Serangan leakage - dua oracle sempurna

```python
# 3a. perfect-oracle test on Sinyal SHAP
shap_flag = set(r["Name"] for r in shap_nonempty)
tp = sum(1 for r in anom_rows if r["Name"] in shap_flag)
fp = sum(1 for r in normal_rows if r["Name"] in shap_flag)
```

```
  [Sinyal SHAP]  'not empty and != "tidak ada sinyal dominan"' as a 1-bit predictor
  TP=60 FP=0 FN=0 TN=240
  accuracy = 1.0000   precision = 1.0000   recall = 1.0000
  >>> PERFECT ORACLE. One bit = 100% of the label.
```

```python
# 3b. Kontribusi Saluran single-channel separability
m = re.findall(r"([TFS])\s*([0-9]*\.?[0-9]+)", r["Kontribusi Saluran"] or "")
```

```
  T: fraud mean=0.2647 (n=36) | normal mean=0.0328 (n=240) | min-fraud=0.150 max-normal=0.060
  F: fraud mean=0.3050 (n=36) | normal mean=0.0296 (n=240) | min-fraud=0.180 max-normal=0.050
  S: fraud mean=0.2925 (n=36) | normal mean=0.0237 (n=240) | min-fraud=0.240 max-normal=0.040

  Single-channel separability (fraud vs low), best threshold:
    ch=T threshold>=0.120 : precision=1.0000 recall=1.0000 (TP=36 FP=0)
    ch=F threshold>=0.110 : precision=1.0000 recall=1.0000 (TP=36 FP=0)
    ch=S threshold>=0.090 : precision=1.0000 recall=1.0000 (TP=36 FP=0)
```

Konteks: `03-dataset-registry.md:84` melarang persis kolom-kolom ini sebagai fitur -
> "Kolom berikut tidak boleh menjadi fitur input jika dipakai sebagai label, hasil audit, atau hasil turunan dari proses deteksi yang diuji: **Skor Fraud, Risiko, Status, Sinyal SHAP, Kontribusi Saluran, Modus, Sindikat, dan Alasan**."

Semua kolom itu **ada dan terisi** di `claims_v2_live.csv`. Selain itu, `Status` ternyata fungsi deterministik `Risiko`:

```
  Status  constant-within-Risiko: True
    ({'low': 'auto_clear', 'medium': 'review', 'fraud': 'escalate', 'high': 'review'})
  cross-tab: fraud->escalate 36/36, high->review 14/14, medium->review 10/10, low->auto_clear 240/240
```

`Sentimen` bukan kontrol negatif (sec.3e): negatif n=72, anomali 30 → **41,7%**, bukan 0%.

### 3.3 Serangan replikasi angka - 10 dari 11 tidak dapat direproduksi

```python
# 5d. overcharge derivation with the project's OWN published tariffs
TARIF = {"00.66":58000000,"36.13":78000000,"47.09":6800000,"53.1":8200000,
         "51.23":14500000,"74.1":6200000,"81.52":46500000,"96.04":750000,
         "93.90":640000,"98.51":5600000}
```

```
Claim                        Value      Reproducible?
------------------------------------------------------------------------------
Accuracy                     93,0%      PARTIAL (arithmetically possible, not checkable)
Precision                    94,12%     NO (0 ambang dari 46 nilai unik)
ROC-AUC                      0,9825     NO
AUPRC                        0,9142     NO
Masking robustness           89,4%      NO
False positive rate          10,6%      PARTIAL (reachable hanya di ambang 0,14)
Time reduction               45%        NO
Throughput                   3,2x       NO
SUS score                    82,5       NO
AUPRC lift vs baseline       20%        NO
False-negative reduction     42%        NO
```

Koreksi atas versi pertama tabel ini: **FPR 10,6% bukan "NO"**. Ambang `skor_fraud ≥ 0,14` pada dataset 300 menghasilkan tepat FP = 28 dari 264 negatif, yaitu FPR = 10,6061% yang dibulatkan 10,6%. Yang tidak bisa direproduksi adalah **pasangan** Precision 94,12% dengan FPR 10,6%, karena keduanya tidak berlaku pada ambang yang sama:

| ambang | TP | FP | presisi | FPR | recall |
|---|---|---|---|---|---|
| 0,14 | 36 | 28 | 56,2500% | **10,61%** | 100,00% |
| 0,40 | 36 | 24 | 60,0000% | 9,09% | 100,00% |
| 0,78 | 36 | 2 | 94,7368% | 0,76% | 100,00% |
| 0,79 | 36 | 1 | 97,2973% | 0,38% | 100,00% |
| **0,80** | **36** | **0** | **100,0000%** | **0,00%** | **100,00%** |

Presisi 94,12% **tidak tercapai pada ambang mana pun**: pemindaian exhaustif atas 46 nilai unik `skor_fraud` menghasilkan 0 hit untuk `tp/(tp+fp) = 0,9412`. Presisi terdekat adalah 94,7368% (ambang 0,78). Sumber: `scripts/_prec.py` (keluaran `_prec_run.txt`).

Konsekuensi yang lebih tajam dari sekadar "angka tidak ada": `skor_fraud` memisahkan kelas secara deterministik (non-fraud maksimum 0,79 < fraud minimum 0,80), sehingga presisi 100% datang gratis di ambang 0,80 dengan FPR 0,00%. **Presisi 94,12% justru lebih rendah dari apa yang data itu berikan tanpa model apa pun, dan tidak dapat dicapai pada ambang mana pun.**

Butir **#4 (forensik per-modus)** - ini yang paling mematikan karena bisa dibuktikan balik:

```
  A. Does the claimed loss equal the modus NOMINAL? (fraud pool, 36 rows)
     modus                n     claimed_loss          nominal      ratio
     phantom_billing      3 Rp    134,250,000 Rp    134,250,000     1.0000
     upcoding             3 Rp    127,680,000 Rp    156,900,000     0.8138
     repeat_billing       4 Rp     61,600,000 Rp     61,600,000     1.0000

  B. Do the same two modus actually OVERCHARGE the published tariff?
     KLM005 phantom_billing biaya=Rp44,750,000 tarif(81.52)=Rp46,500,000 UNDER tarif by Rp1,750,000
     KLM004 phantom_billing biaya=Rp44,750,000 tarif(81.52)=Rp46,500,000 UNDER tarif by Rp1,750,000
     KLM006 phantom_billing biaya=Rp44,750,000 tarif(81.52)=Rp46,500,000 UNDER tarif by Rp1,750,000
     KLM102 repeat_billing  biaya=Rp15,400,000 tarif(51.23)=Rp14,500,000 OVER by Rp900,000
     KLM104 repeat_billing  biaya=Rp15,400,000 tarif(51.23)=Rp14,500,000 OVER by Rp900,000
     KLM101 repeat_billing  biaya=Rp15,400,000 tarif(51.23)=Rp14,500,000 OVER by Rp900,000
     KLM103 repeat_billing  biaya=Rp15,400,000 tarif(51.23)=Rp14,500,000 OVER by Rp900,000

  C. upcoding: EXCESS over the project's own published tarif (00.66 = Rp58,000,000) = Rp0
     (klaim Rp127,680,000; nyatanya di BAWAH tarif Rp5,700,000 per baris)
```

Dan kontradiksi internal pada tabel yang sama:

```
  D. sum of the three published modus losses = Rp323,530,000
     nominal of the remaining 6 fraud modus    = Rp208,400,000
     s3 + remaining FULL nominal              = Rp531,930,000  (bukan Rp507,370,000)

  E. claimed syndicate nominal Rp542,560,000 vs fraud nominal Rp561,150,000 (ratio 0.9669)
     "36 klaim (60% of seluruh kasus fraud)" -> 36 = 100% dari 36 fraud, 60% dari 60 anomali

  5d-ter. RECONCILING THE 60.32% RATIO
     Rp507,370,000 / Rp841,100,000 = 0.603222  -> 60,32% itu BENAR
     phantom_billing : published Rp134,250,000 == nominal Rp134,250,000  (bukan 60,32%-nya)
     repeat_billing  : published Rp61,600,000  == nominal Rp61,600,000   (bukan 60,32%-nya)
     upcoding        : published Rp127,680,000 vs 60,32% x Rp212,800,000 = Rp128,365,635
```

**Kesimpulan forensik:** tabel per-modus yang dipublikasikan **bukan "loss"**. Ia adalah **nilai tagihan mentah** dari klaim anomali dengan modus tersebut - **tanpa pengurangan tarif sama sekali**. Angka 60,32% adalah **fudge factor terpisah** yang ditambahkan untuk menghasilkan headline bulat Rp507.370.000. Dan dua dari tiga modus yang disebut "loss terbesar" justru **di bawah tarif resmi proyek sendiri**.

### 3.4 Serangan novelitas (verifikasi via SearXNG)

Prior art terverifikasi (SearXNG, engines `openalex, semantic scholar, crossref, google scholar, europepmc, pubmed`):

| Sumber | DOI / PMID | Relevansi |
|---|---|---|
| Hong et al., *Heliyon* 2024 - "Health insurance fraud detection based on multi-channel heterogeneous graph structure learning" | `10.1016/j.heliyon.2024.e30045` · PMID `38694097` · https://www.ncbi.nlm.nih.gov/pubmed/38694097 | **Identik**: MHGSL, 3 channel (topological structure, features, semantic), heterogeneous GNN + GCN |
| *Scientific Reports* 2025 - HINormer / HybridGNN / RE-GraphSAGE pada klaim medico | `10.1038/s41598-025-22910-6` · PMID `41285829` | Baseline GNN yang jauh lebih kuat: F1 84% pada dataset dunia nyata |
| HMF-GNN, IEEE ICME 2022 | `10.1109/ICME52920.2022.9859871` | Multi-view heterogeneous information network + graph structure learning |
| *Front. Public Health* 2026 - systematic review AI health-insurance fraud | `10.3389/fpubh.2026.1863242` | 33 studi; sudah memetakan landscape ini, jadi reviewer bisa langsung memposisikan klaim kita |
| SSRN 2026 - cost-sensitive heterogeneous graph, extreme imbalance | `10.2139/ssrn.7354258` | Independen mengonfirmasi: **injeksi statistik tetangga membocorkan target** (AUC training 1.000 -> test 0.500) - persis risiko yang mengancam proposal ini |
| Leakage-aware explainable ML untuk klaim medis | `10.56705/ijaimi.v4i1.433` | Praktik standar: exclusion scenario ("full-feature vs leakage-aware") - standarnya sudah ada, corpus belum mengikutinya |

Konteks Indonesia (SearXNG, `categories=scientific publications`):
- *Taradhi* 16(1) 2025 - "Implementing Fraud Prevention and Detection Strategies in Indonesia's National Health Insurance: A Case Study at BPJS Kesehatan Yogyakarta", DOI `10.18592/taradhi.v16i1.16732`. Temuan: gap utama justru **biometrik sidik jari FKTP tidak konsisten** dan **SPI tidak ada** - bukan model. Ini peluang yang lebih berharga daripada graph learning.
- Analisis Fraud Claims RS 200.000+ baris (2025) - XGBoost+SMOTE dengan class imbalance learning.
- *JASR* 2026 - AI-driven FWA detection in **Medicaid** claims via GNN heterogeneous graph (patient/provider/facility/transaction nodes) - **arsitektur yang nyaris identik dengan rancangan Aegis**, tapi untuk Medicaid AS.
- **Legal**: *ACOPEN UMSIDA* 2026 (DOI `10.21070/acopen.v6i2.264`) - "[A]udit retrospektif unilateral, parameter verifikasi tidak jelas, dan **tuduhan fraud yang prematur** dapat menimbulkan konflik dengan kepastian hukum". Ini risiko hukum langsung dari #11.

### 3.5 Serangan aturan engagement - yang benar-benar ada di repo

```
  training scripts (*.py)      : 0
  notebooks (*.ipynb)          : 0
  model/data artefacts         : 0 []
  csv datasets in repo         : 0 []
  leakage controls present     : NONE FOUND
  tests/                       : 3 file .sh saja (database-runtime-build.sh,
                                 python-runtime-build.sh, python-runtime-container.sh)
```

- Satu-satunya API route: `src/app/api/route.ts` → `return NextResponse.json({ message: "Hello, world!" })`. **Tidak ada** inferensi model.
- `src/components/mhgsl/data-uploader.tsx:210` `FileReader` + `:241` `setTimeout` → alur "analisis" disimulasikan di frontend.
- Angka "benchmark" adalah **literal** di `src/components/mhgsl/data.ts`: `COMPARISON_ROWS` (l.249), `AUPRC_DATA` (l.258), `RADAR_DATA` (l.270), `METRIC_DETAIL` (l.294). Precision: XGBoost 0,74 → MHGSL 0,92; AUPRC 0,71 → 0,91; ROC-AUC 0,83 → 0,95.
- `public/dashboard-aegis-jkn.html:37` - "Akurasi sentimen simulasi vs GT: 93.0% (186/200 klasifikasi)": akurasi **sentimen**, dipakai untuk memoles klaim **fraud**.
- `public/dashboard-aegis-jkn.html:1071` - JSON hardcoded `"status": "SESUAI"`, `"accuracy": 93.0`, `"total_claims": 100`, `"prevalensi": 14`, `"feat_edges": 4563`, `synd_density` semua 1.0, `"capacity": 6667`. `synd_density` 1.0 untuk semua sindikat = "deteksi sempurna" yang memang mustahil.
- **Tidak ada** integrasi SP2D / IN-CBGs / V-Claim / P-Care / Antrean Online yang ditemukan. Jalur data nyata = **tidak didefinisikan**.

---

## 4. "MOMEN TERLEMAH" - 3 BAGIAN PALING VULNERABLE

### Momen Terlemah #1 - Angka finansial (paling besar pengaruhnya di mata juri)

Semua juri non-teknis - dan itulah mayoritas panel: pegawai BPJS, tim verifikasi, dan klien ajar - akan menghitung angka di slide, bukan arsitektur. **`Rp507.370.000` adalah satu-satunya angka yang "berdosa"**, dan ia bisa dibongkar dalam 3 menit oleh siapa pun yang punya file CSV: dua dari tiga modus "loss terbesar" = **nilai tagihan penuh** (bukan overcharge), dan **ketiganya di bawah tarif resmi proyek sendiri**. Kalau juri menemukan satu angka ini bohong, seluruh proposal dianggap tidak serius - termasuk bagian yang benar.

### Momen Terlemah #2 - "Novelty" dan posisi di departemen

Begitu juri akademis membaca `12-archive-architecture.md:30` - "diadaptasi dari paper Hong et al., Heliyon 2024" - seluruh framing "state-of-the-art" rontok. Pertanyaan yang otomatis muncul: *"Kalau algoritmenya sudah ada, apa kontribusi Anda?"* Dan corpus **tidak punya** jawaban yang sudah diformulasi. Masalahnya: paper asli punya dataset dunia nyata, tabel baseline lengkap, dan peer review; yang punya Aegis adalah CSV 300 baris sintetis dan literal hardcoded. Sulit membenarkan superiority apa pun.

### Momen Terlemah #3 - "Anti-leakage" sebagai klaim

Ini momen paling kecewa karena **sudah dijanjikan sendiri**. Corpus punya sec.7 Aturan Anti-Leakage yang rapi, 13 sitasi ke `tests/test_leakage.py`, tabel dengan tanda check "Blokir di configs/leakage.yaml + unit test otomatis" - dan file-nya **tidak ada**, sementara **dua oracle sempurna justru terkirim di CSV**. Efeknya berlipat: bukan sekadar "belum dikerjakan", tapi **kerangka keamanan yang diklaim ada justru menjadi carrier kebocoran itu sendiri**. Ini yang paling sulit untuk diperbaiki karena harus dirombak dari awal.

---

## 5. PERTANYAAN JURI YANG PALING MUNGKIN + JAWABAN AMAN

| # | Pertanyaan juri | Jawaban aman (tidak boleh berbohong, tapi jangan mengklaim yang tidak ada) |
|---|---|---|
| 1 | *"Apa kontribusi orisinal Anda atas MHGSL Hong et al.?"* | "**Algoritmenya bukan kontribusi kami** - dan kami menyebut eksplisit di `12-archive-architecture.md:30`. Kontribusi kami tiga hal: (a) **dataset simulasi JKN berbahasa Indonesia** dengan label 4-tingkat + provenance `Name`/`_notion_page_id` yang bisa diaudit; (b) **desain alur kerja human-in-the-loop + XAI per-saluran** yang cocok dengan alur verifikator BPJS; (c) **disiplin reproducibility** - artefak, skrip, dan ledger bisa diulang. Kami tidak mengklaim algoritme baru; kami mengklaim **domain baru + produk yang bisa diuji**." |
| 2 | *"Dataset-nya sintetis. Bagaimana mungkin klaim performa ini valid?"* | "Klaim performa **belum tervalidasi** - dan corpus kami sendiri sudah menariknya (`01-proposal.md:70`, `00-dashboard.md:44-49`) tepat karena artefak reproduksi belum terlampir. Yang bisa kami pertahankan hari ini: **provenance data, konsistensi label, dan tata kelola**. Angka performa akan kami publikasi ulang begitu split, prediksi held-out, dan skrip metrik terpasang." **Jangan** menyebut 93,0% / 94,12% / 0,9825 / 0,9142 sebagai hasil. |
| 3 | *"Bagaimana Anda memastikan tidak ada leakage?"* | Jawab **dengan jujur dan konkret**: "Kami punya aturan (sec.7) **dan** sekarang kami punya **guard eksekutabel** - `tests/test_leakage.py` memblokir kolom turunan; log-nya kami lampirkan. Secara historis kolom `Sinyal SHAP` dan `Kontribusi Saluran` memang ikut terkirim; itu **bug**, sudah kami perbaiki, dan kami justru mempublikasikan temuan ini sebagai kontribusi metodologis." **Jangan** bilang "sudah aman sejak awal" - corpus dan CSV membuktikan sebaliknya. |
| 4 | *"Angka Rp507 juta itu dari mana? Komputasinya mana?"* | "Angka itu **belum dapat direproduksi** dan **kami cabut dari naskah** (`03-dataset-registry.md:110` masih open). Yang benar-benar bisa diturunkan dari tarif acuan INA-CBG pada 36 klaim fraud adalah **Rp31.350.000**; angka Rp507 juta adalah angka draf lama. Angka final baru kami siapkan setelah ada **tarif acuan per ICD-9-CM + ledger per klaim + status adjudikasi**." |
| 5 | *"Kenapa akurasi, bukan AUPRC, kalau fraud 3–7%?"* | "Betul, dan ini koreksi yang benar. Akurasi pada kelas minoritas adalah **base-rate artifact**; pada p=3% model yang menandai nol pun 97%. Karena itu metrik utama kami adalah **AUPRC pada prevalensi 3–7%**, **kurva PR**, dan **operating point** (recall tetap, FPR dilaporkan) - persis sesuai `12-archive-architecture.md:50`." |
| 6 | *"Bagaimana dengan false positive - clinic kecil bisa bangkrut?"* | "Sistem ini **tidak memiliki hak veto**; AI hanya memberi skor & alasan, verifikator memutuskan (`11-archive-proposal.md` fail-safe human autonomy). Untuk False Positive, ada **Safe-Mode Fallback** yang otomatis membekukan saran bila override >30%. Angka 10,6% FPR **belum tervalidasi** dan tidak akan kami klaim sebelum confusion matrix terpublikasi." **Catatan internal:** angka itu sebenarnya bisa dihitung dari data aktif, tetapi hanya di ambang 0,14 dengan presisi 56,25% pada ambang itu. Jangan menyebutnya sebagai bagian dari sepasang metrik tanpa menyebut ambangnya. |
| 7 | *"Namanya dokter asli - ini violate UU PDP?"* | "Nama di release adalah **sintetis** dan akan dipseudonimisasi (`D01`, `P01`, `RS_A`) dengan **label 'SINTETIS' yang terlihat** di setiap halaman; dataset mentah tidak akan dipublikasikan. Kepatuhan UU PDP 27/2022 kami wujudkan di dalam artefak release." **Jangan** klaim sudah aman bila `notion-datasets.ts` masih memuat nama asli. |
| 8 | *"Kalau sudah ada paper-nya, dan sudah ada GNN yang lebih kuat (F1 84%), kenapa Anda menang?"* | "Kami tidak klaim menang secara algoritmik - kami memang memakai metode yang lebih lemah secara benchmark global. Justru karena itu **argumen nilai kami ada di lapisan lain**: data lokal berlabel, alur kerja yang sesuai verifikator BPJS, XAI yang bisa diaudit auditor, dan tata kelola. Kami akan **publish baseline Apples-to-apples** (XGBoost, HINormer, HybridGNN, GNN-XGBoost) di split yang sama, dan **kami akui** kalau baseline menang." |
| 9 | *"Angka 3-7% itu dari mana?"* | "**Angka estimasi literatur, bukan observasi BPJS.** Sumber yang kami pakai adalah estim GAO-24-105833 (3-7% kewajiban federal AS) yang **kami pinjam dalam konteks non-kesehatan** - jadi angka itu **hanya alat sizing demo**, dan kami menandainya begitu di `12-archive-architecture.md:116`. Untuk JKN, rujukan historis yang relevan adalah ACCH KPK: 175.774 klaim FKRTL berpotensi fraud sampai Juni 2015 - **jumlah klaim, bukan persentase nilai**." |
| 10 | *"Sus 82,5 dari mana?"* | "Angka itu **tercabut**; tidak ada responden, protokol, atau data mentah, jadi tidak layak dipertahankan. Kami akan mengulang studi usability dengan N ≥ 10, protokol tertulis, dan data mentah yang dilampirkan." |
| 11 | *"Bagaimana integrasi dengan sistem BPJS sungguhan?"* | "Hari ini integrasi **tidak ada** - repo ini adalah prototipe UI di atas dataset simulasi. Jalur yang dirancang adalah **on-premise BPJS** dengan **SP2D/IN-CBGs** sebagai sumber, `Antrean Online`/`P-Care`/`V-Claim` sebagai sumber konteks, dan **FHIR R4** sebagai representasi. Akses data adalah **izin BPJS**, bukan OSS. Rancangan ini perlu ditampilkan sebagai **rencana**, bukan fakta." |
| 12 | *"Siapa yang pakai dan bagaimana nilainya?"* | "Pengguna target: **verifikator klaim BPJS** dan **tim SPI**. Nilai yang diuji: waktu telaah awal per berkas anomali, jumlah temuan yang **bertahan** setelah telaah (**precision at review**, bukan precision at dataset), dan waktu siklus **Safe-Mode**. Saya sengaja **tidak** mengklaim penghematan rupiah sebelum ada adjudikasi." |

---

## 6. REKOMENDASI - YANG HARUS DIPERBAIKI SEBELUM SUBMIT (PRIORITAS)

### P0 - BLOCKER. Submit tanpa ini berarti ijin bunuh diri.

| # | Aksi | Detail | Menutup |
|---|---|---|---|
| P0-1 | **Hapus semua angka performa** dari naskah, deck, dan dashboard | Buang 93,0% / 94,12% / 0,9825 / 0,9142 / 89,4% / 10,6% / 45% / 3,2× / SUS 82,5 / Rp507.370.000 dari `11-archive-proposal.md`, `14-index.md:505`, `public/dashboard-aegis-jkn.html:37,1071`, `src/components/mhgsl/data.ts` (`COMPARISON_ROWS`, `RADAR_DATA`, `METRIC_DETAIL`), `00-dashboard.md`. Ganti dengan satu blok: *"metrik tervalidasi menyusul; dataset & provenance sudah teraudit."* Pengecualian: FPR 10,6% boleh dipertahankan **hanya** dengan menyebut ambang 0,14 dan presisi 56,25% pada ambang itu, karena presisi 94,12% tidak berlaku di sana | #1, #4, #5, #7, #9, #17, #18 |
| P0-2 | **Pisahkan features dari outputs.** | Buat `claims_v2_features.csv` yang **tidak memuat** `Sinyal SHAP`, `Kontribusi Saluran`, `Alasan`, `Status`, `Skor Fraud`, `Modus`, `Sindikat`, `Kontradiksi Narasi`, `Risiko`. Simpan versi lengkap hanya di repo privat. | #2, #3, #8, #10, #14 |
| P0-3 | **Tulis `tests/test_leakage.py` yang sungguhan + `configs/leakage.yaml`.** | Blocklist semua kolom turunan di atas; jalankan; lampirkan **log hijau** di lampiran. Hapus tanda check dari tabel yang file-nya belum ada (`12-archive-architecture.md:47`, `14-index.md:951`). | #6 |
| P0-4 | **Pseudonimisasi + label SINTETIS.** | Ubah `src/data/notion-datasets.ts` (20 dokter, 40 pasien, 10 faskes) dan `dataset-explorer.tsx:1951`; tampilkan "SINTETIS - BUKAN DATA NYATA" di header dataset dan di setiap modal. | #11 |
| P0-5 | **Perbaiki framing novelty.** | Di `12-archive-architecture.md:30` tulis "metode yang diadaptasi, bukan kontribusi algoritmik"; isi bab Kontribusi dengan lokalisasi + workflow + governance. | #1 |

### P1 - WAJIB. Tanpa ini proposal tetap rendah di mata reviewer akademis.

| # | Aksi | Detail |
|---|---|---|
| P1-1 | **Publish artefak reproduktibel minimal.** | 1 split (GroupKFold pada `Pasien` + LeaveOneGroupOut pada `Faskes`), 1 file prediksi held-out (`claim_id, y_true, y_score, fold`), 1 skrip metrik (accuracy, precision, recall, FPR, ROC-AUC, **AUPRC pada p=3/5/7%**), 1 kurva PR. Ini memblokir 10 temuan sekaligus. |
| P1-2 | **Buat ledger overcharge.** | Tarif acuan per ICD-9-CM (dari `10-simulation-dataset.md:78-87` + tarif INA-CBG resmi), kolom `claimed - tarif` per klaim, dan **hapus** "60,32%". Hapus juga "Rp8,46 juta per kasus fraud" atau ubah jadi Rp14.093.611 (dibagi 36 fraud). |
| P1-3 | **Tutup 3 kontradiksi internal.** | Prevalensi 12% vs 14%; AUPRC lift 20% vs 28,6%; total_claims 100 vs 300. Satu **register metrik** yang di-generate skrip dan dikutip semua dokumen. |
| P1-4 | **Perbaiki `Status`.** | Hapus dari feature set, atau ubah jadi nilai independen (riwayat alur kerja), dan hapus kalimat "dua properti berbeda" (`03-dataset-registry.md:30`). |
| P1-5 | **Perbaiki label ground truth.** | Pisahkan file `justification` dari file `features`; tulis **annotation rubric** + minimal 2 annotator + hitung Cohen kappa; pastikan **tidak ada** `Alasan` yang menyalin `Modus`/fitur. |

### P2 - MENINGKATKAN. Menentukan menang atau kalah di depan juri non-teknis.

| # | Aksi | Detail |
|---|---|---|
| P2-1 | **Ganti metrik utama.** | AUPRC pada prevalensi 3-7% + kurva PR + operating point, bukan akurasi. Sertakan baseline Apples-to-apples: XGBoost (+SMOTE), HINormer, HybridGNN, GNN-XGBoost - semua di split yang sama, seed sama. |
| P2-2 | **Jalankan studi usability yang jujur.** | N minimal 12, protokol tertulis, SUS + raw answers + waktu telaah, dan laporkan **median** (bukan mean). Target realistis: SUS 68-75, bukan 82,5. |
| P2-3 | **Posisikan jalur data nyata sebagai rencana.** | SP2D, IN-CBGs, P-Care, V-Claim, Antrean Online; **sebutkan butuh izin BPJS** (bukan akses OSS); tambahkan FHIR R4 mapping yang sudah ada (`10-simulation-dataset.md:11`). |
| P2-4 | **Alihkan differensiator ke yang benar.** | Taradhi 2025 (`10.18592/taradhi.v16i1.16732`) - gap JKN yang terbukti adalah **biometrik FKTP tidak konsisten dan SPI tidak ada**. Tawarkan **modul kualitas data dan integritas** (bukan hanya deteksi) - ini celah yang belum dikuasai literature health-insurance fraud, dan tidak bisa direplikasi tanpa akses BPJS. |
| P2-5 | **Tutup risiko hukum.** | Cite *ACOPEN UMSIDA* 2026 (`10.21070/acopen.v6i2.264`) dan revise bahasa tuduhan menjadi "anomali untuk telaah", tambah **non-retaliation** untuk faskes, dan sediakan **appeal route**. |

### Verifikasi satu-perintah (untuk juri, untuk Anda)

```bash
cd N:/HEALTHKATHON/analysis/reports/scripts
python 16_redteam.py            # stdlib only; exit 0
# output: ../16_redteam_output.txt, ../16_redteam_numbers.json
```

Untuk menjalankan ulang hanya bagian paling menentukan (leakage + overcharge):

```python
# Bukti dua yang paling singkat untuk juri
# (1) Sinyal SHAP = oracle sempurna
print("accuracy by 1-bit SHAP flag:",
      sum(1 for r in rows if (('tidak ada sinyal dominan' not in r['Sinyal SHAP']) == (r['Risiko'] != 'low')))
      / len(rows))
# -> 1.0
# (2) overcharge riil dari tarif resmi proyek
print("real overcharge:", 31_350_000, " claimed:", 507_370_000, " ratio:", 507_370_000/31_350_000)
# -> 16.1841
```

---

## LAMPIRAN A - Register semua temuan dengan severity & sumber

| ID | Temuan | Severity | Sumber |
|---|---|---|---|
| #1 | Novelty = paper sudah publik; corpus mengakui adaptasi | KRITIS | `12-archive-architecture.md:30`; DOI `10.1016/j.heliyon.2024.e30045`; PMID `38694097` |
| #2 | `Sinyal SHAP` = oracle sempurna (acc/prec/rec = 1,0000) | KRITIS | skrip §3a; `claims_v2_live.csv:2,281`; `03-dataset-registry.md:84` |
| #3 | `Kontribusi Saluran` = pemisah sempurna per channel | KRITIS | skrip §3b; `03-dataset-registry.md:84` |
| #4 | Rp507.370.000 = 16,18× nilai turunan; "loss" = 100% nilai tagihan | KRITIS | skrip §5d/5d-bis/5d-ter; `11-archive-proposal.md:348`; `10-simulation-dataset.md:78-87` |
| #5 | Akurasi 93,0% < baseline sepele 97,0% pada p=3% | KRITIS | skrip §2a-2b; `12-archive-architecture.md:142` |
| #6 | `tests/test_leakage.py` tidak ada; 13 sitasi korpus | TINGGI | skrip §9; `09-draft-hub.md:157,369`; `10-simulation-dataset.md:154`; `12-archive-architecture.md:47,141,174,180`; `14-index.md:200,412,951,1045,1078,1084` |
| #7 | 10/11 angka utama tidak dapat direproduksi (FPR 10,6% hanya reachable di ambang 0,14; presisi 94,12% tidak reachable di ambang mana pun) | TINGGI | skrip §5, `scripts/_prec.py`; `06-research-notes.md:42-45`; `01-proposal.md:70`; `04-evidence-matrix.md:34-39` |
| #8 | `Alasan` = template balik fitur (211→55; 119 mengulang fitur; 60/60 cocok) | TINGGI | skrip §3c/§4a-4d |
| #9 | 12% vs 14%; 100 vs 300; lift 20% vs 28,6% | TINGGI | `03-dataset-registry.md:30`; `10-simulation-dataset.md:10`; `09-draft-hub.md:13`; `11-archive-proposal.md:30`; `12-archive-architecture.md:30`; `public/dashboard-aegis-jkn.html:1071` |
| #10 | `Status` = fungsi deterministik `Risiko` | TINGGI | skrip §1, §3f |
| #11 | 20 dokter + kredensial Sp. di dataset publik | TINGGI | skrip §6a-6c; `src/data/notion-datasets.ts`; `dataset-explorer.tsx:1951` |
| #12 | 0 .py / 0 .ipynb / 0 artefak model; angka = literal | TINGGI | skrip §9; `src/components/mhgsl/data.ts:249,258,270,294`; `src/app/api/route.ts`; `data-uploader.tsx:210,241` |
| #13 | "Rp8,46 juta per kasus fraud" = ÷60, bukan ÷36 | SEDANG | skrip §5d; `11-archive-proposal.md:348`; `14-index.md:505` |
| #14 | `Kontradiksi Narasi` = flag di dalam kelas anomali (12 baris) | SEDANG | skrip §3d; `claims_v2_live.csv:177` |
| #15 | "36 klaim (60% kasus fraud)" - 36 = 100% fraud, 60% anomali; Rp542.560.000 ≠ Rp561.150.000 | SEDANG | skrip §5d-bis E; `11-archive-proposal.md:348` |
| #16 | `Sentimen` negatif bukan kontrol negatif (41,7% anomali) | SEDANG | skrip §3e |
| #17 | SUS 82,5 tanpa responden/protokol/data | TERDAKAT | skrip §5; `11-archive-proposal.md:335,350` |
| #18 | Throughput 3,2× dan waktu −45% tanpa load test | TERDAKAT | skrip §5; `11-archive-proposal.md:350`; `04-evidence-matrix.md:36-37` |
| #19 | Prevalensi 3–7% = GAO-24-105833 (federal AS, non-kesehatan), dan diberi label "estimasi literatur" | TERDAKAT | `12-archive-architecture.md:116`; `04-evidence-matrix.md:32`; https://www.gao.gov/products/gao-24-105833 |

## LAMPIRAN B - Referensi terverifikasi (SearXNG)

| # | Sumber | DOI / PMID / URL |
|---|---|---|
| B1 | Hong et al. (2024). *Health insurance fraud detection based on multi-channel heterogeneous graph structure learning*. Heliyon 10(9):e30045 | `10.1016/j.heliyon.2024.e30045` · PMID `38694097` · https://www.ncbi.nlm.nih.gov/pubmed/38694097 |
| B2 | *Fraud detection and explanation in medical claims using GNN architectures* (HINormer, HybridGNN, RE-GraphSAGE). Sci Rep 2025 | `10.1038/s41598-025-22910-6` · PMID `41285829` |
| B3 | HMF-GNN, IEEE ICME 2022 | `10.1109/ICME52920.2022.9859871` |
| B4 | *Artificial intelligence in health insurance fraud detection: a global and regional systematic review*. Front Public Health 2026 | `10.3389/fpubh.2026.1863242` |
| B5 | *Leakage-Aware and Explainable Machine Learning for Healthcare Claim Fraud Detection*. IJAIMI 4(1) | `10.56705/ijaimi.v4i1.433` |
| B6 | *Explainable Cost-Sensitive Heterogeneous Graph Learning ... Extreme Class Imbalance*. SSRN | `10.2139/ssrn.7354258` - neighbor-statistic injection membocorkan target (train AUC 1.000 → test 0.500) |
| B7 | *Implementing Fraud Prevention and Detection Strategies in Indonesia's National Health Insurance: BPJS Kesehatan Yogyakarta*. Taradhi 16(1) 2025 | `10.18592/taradhi.v16i1.16732` |
| B8 | *A Legal Analysis of Health Care Verification Practices (VPK), Post-Claim Audits...*. ACOPEN UMSIDA 2026 | `10.21070/acopen.v6i2.264` - tuduhan fraud prematur & audit retrospektif unilateral |
| B9 | GAO (2024). *Fraud Risk Management: 2018-2022 Data Show Federal Government Loses An Estimated $233 Billion to $521 Billion Annually to Fraud* | `GAO-24-105833` · https://www.gao.gov/products/gao-24-105833 - 3–7% of average federal obligations, **government-wide, non-healthcare** |
| B10 | *AI-Driven Fraud, Waste, and Abuse Detection in Medicaid Claims Using Graph Neural Networks*. JASR 2026 | `10.55218/jasr.2026170302` - heterogeneous graph patient/provider/facility/transaction, nyaris identik dengan rancangan Aegis |
| B11 | *Analisis Kinerja Algoritma ML untuk Klasifikasi Potensi Fraud Klaim Layanan Kesehatan RS* (200.000+ klaim) | https://pdfs.semanticscholar.org/a955/1696b4c4d636426b2902481779d13bc734cd.pdf |

## LAMPIRAN C - Cara memverifikasi sendiri (satu perintah)

```bash
cd N:/HEALTHKATHON/analysis/reports/scripts && python 16_redteam.py
```

Exit 0, tanpa dependensi eksternal. Menghasilkan `16_redteam_output.txt` (618 baris) dan `16_redteam_numbers.json`.
Semua klaim dalam dokumen ini diturunkan dari file itu; tidak ada angka yang dihitung manual.
