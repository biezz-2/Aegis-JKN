# Dataset Simulasi Aegis-JKN — 100 Klaim Sintetis

> **Sumber Notion:** [Dataset Simulasi Aegis-JKN — 100 Klaim Sintetis](https://app.notion.com/p/3f23e6031ab781bf99a7d3f1768f1708)  
> **ID Halaman:** `3f23e603-1ab7-81bf-99a7-d3f1768f1708`  
> **Pendamping Makalah:** [Aegis-JKN: Arsitektur dan Strategi Pengembangan](../03-arsitektur-dan-strategi-pengembangan.md)  
> **Aplikasi Purwarupa:** [aegisjkn.vercel.app](http://aegisjkn.vercel.app)

---

> 🗂️ Dataset sintetis untuk uji simulasi MHGSL pada purwarupa Aegis-JKN ([aegisjkn.vercel.app](http://aegisjkn.vercel.app)). 100 klaim, privacy-by-design — bukan data peserta riil, aman menurut Permenkes 24/2022 & UU PDP No. 27/2022. Pendamping makalah `[Tautan Dokumen]`.

## Ringkasan & Ground Truth
- Jumlah klaim: 100 (20 pasien · 12 dokter · 6 FKRTL · 10 diagnosis · 10 prosedur · 10 obat).
- Distribusi risiko: 76 low · 4 medium · 6 high · 14 fraud.
- Ground truth: klaim anomali = KLM001–KLM024 (14 fraud sindikat + 10 anomali medium/high); klaim normal = KLM025–KLM100.
- Skala risiko: skor \<0.35 low; 0.35–0.6 medium; 0.6–0.8 high; lebih dari 0.8 fraud.
- Catatan prevalensi: fraud di-oversample 14% untuk keperluan demo; estimasi lapangan 3–7% (label estimasi literatur).
- Mapping FHIR R4: klaim = Claim; pasien = Patient; dokter = Practitioner; faskes = Organization; diagnosis = Condition (ICD-10); prosedur = Procedure (ICD-9-CM); obat = MedicationRequest/Dispense; LOS = Encounter.length; biaya = [Claim.total](http://Claim.total); tanggal = Encounter.period.start.
- Saluran MHGSL: topologi = edges kunjungan/afiliasi/layanan/semantik; fitur = cosine similarity (LOS, biaya, qty obat) dengan ambang 0.85; semantik = metapath diagnosis ke prosedur.
## Sindikat Ground Truth

| ID | Modus | Faskes | Dokter | Pasien | Klaim | Skenario & Sinyal Deteksi | Skor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-01 | Upcoding | RS_A | D01, D02 | P01–P03 | KLM001–003 | Dx gastritis (K29.7) ditagih PCI (00.66); biaya & LOS identik; subgraf padat | ≥ 0.93 |
| SYND-02 | Phantom Billing | RS_C | D05 | P08–P10 | KLM004–006 | 3 klaim hemiarthroplasty tanggal & biaya identik, LOS 1, tanpa MedicationDispense | ≥ 0.92 |
| SYND-03 | Unbundling | RS_B | D07 | P12–P14 | KLM007–012 | Paket kolesistektomi (51.23) dipecah dengan intubasi (96.04) terpisah di tanggal sama | 0.84–0.87 |
| SYND-04 | Drug Diversion | RS_E | D09 | P16–P17 | KLM013–014 | Qty insulin 24–30 pen vs dosis rasional 1–2 pen/bulan; refill mingguan | 0.86–0.88 |
| SYND-05 | Cloning | RS_F | D08 | P19–P20 | KLM016–017 | Dua pasien berbeda dengan klaim identik sempurna (tanggal, dx, prosedur, LOS, biaya) | 0.78–0.79 (high) |

## Faskes

| ID | Nama | Kota | Kepemilikan | Kelas | Tempat Tidur | Jumlah Klaim | Skor Maks | Risiko |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RS_A | RS Aegis Medika A | Jakarta Selatan | Swasta | B | 412 | 19 | 0.95 | fraud |
| RS_B | RS Bakti Husada B | Surabaya | Swasta | C | 280 | 13 | 0.87 | fraud |
| RS_C | RS Cendana Medika C | Medan | Swasta | B | 350 | 10 | 0.94 | fraud |
| RS_D | RSUD Harapan D | Bandung | Pemerintah | B | 520 | 10 | 0.68 | high |
| RS_E | RS Bahari Medika E | Makassar | Swasta | C | 210 | 22 | 0.88 | fraud |
| RS_F | RSUD Giri Menang F | Yogyakarta | Pemerintah | C | 190 | 26 | 0.79 | high |

## Dokter

| ID | Nama | Spesialisasi | Faskes | Jumlah Klaim | Skor Maks | Risiko |
| --- | --- | --- | --- | --- | --- | --- |
| D01 | dr. Adnan Prakoso, Sp.BTKV | Bedah Toraks & Kardiovaskular | RS_A | 2 | 0.94 | fraud |
| D02 | dr. Barli Soemarno, Sp.B | Bedah Digestif | RS_A | 8 | 0.95 | fraud |
| D03 | dr. Citra Ayuningtyas, Sp.PD | Penyakit Dalam | RS_A | 9 | 0.74 | high |
| D04 | dr. Danur Wibisono, [Sp.JP](http://Sp.JP) | Kardiologi | RS_D | 9 | 0.68 | high |
| D05 | dr. Endra Kusuma, Sp.OT | Orthopedi & Traumatologi | RS_C | 10 | 0.94 | fraud |
| D06 | dr. Fitri Handayani, Sp.A | Anak | RS_B | 0 | 0 | low |
| D07 | dr. Gunawan Halim, Sp.B | Bedah Digestif | RS_B | 13 | 0.87 | fraud |
| D08 | dr. Hendra Maulana, Sp.B | Bedah Umum | RS_F | 18 | 0.79 | high |
| D09 | dr. Indah Pratiwi, Sp.PD | Penyakit Dalam | RS_E | 14 | 0.88 | fraud |
| D10 | dr. Joko Purnomo, Sp.S | Saraf | RS_E | 8 | 0.13 | low |
| D11 | dr. Kartika Sari, Sp.B | Bedah Umum | RS_D | 1 | 0.62 | high |
| D12 | dr. Lina Marlina, Sp.OG | Obstetri & Ginekologi | RS_F | 8 | 0.66 | high |

## Pasien

| ID | Nama | Umur | Gender | Kelas Rawat | Segmen | Kota | Jumlah Klaim | Skor Maks | Risiko |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P01 | Agus Raharjo | 58 | L | 2 | PBPU | Jakarta | 5 | 0.94 | fraud |
| P02 | Bunga Lestari | 63 | P | 2 | PBPU | Jakarta | 5 | 0.95 | fraud |
| P03 | Candra Wijaya | 55 | L | 1 | PBPU | Jakarta | 5 | 0.93 | fraud |
| P04 | Dewi Anggraeni | 34 | P | 3 | PBI | Bogor | 4 | 0.11 | low |
| P05 | Eka Putri | 27 | P | 3 | PBI | Yogyakarta | 5 | 0.66 | high |
| P06 | Fajar Nugroho | 71 | L | 2 | PBI | Surabaya | 4 | 0.13 | low |
| P07 | Gilang Saputra | 42 | L | 3 | PBPU | Bandung | 5 | 0.62 | high |
| P08 | Maryam Yusuf | 77 | P | 2 | PBPU | Medan | 5 | 0.92 | fraud |
| P09 | Idrus Hakim | 79 | L | 2 | PBPU | Medan | 4 | 0.94 | fraud |
| P10 | Kartini Ibrahim | 80 | P | 2 | PBI | Medan | 5 | 0.93 | fraud |
| P11 | Lukman Sutrisno | 66 | L | 1 | PBPU | Bandung | 5 | 0.68 | high |
| P12 | Maya Sari | 49 | P | 2 | PBPU | Surabaya | 5 | 0.85 | fraud |
| P13 | Nadia Rahmawati | 52 | P | 3 | PBPU | Surabaya | 6 | 0.86 | fraud |
| P14 | Odi Setiawan | 61 | L | 2 | PBPU | Surabaya | 6 | 0.87 | fraud |
| P15 | Purnama Sidik | 47 | L | 3 | PBI | Makassar | 7 | 0.53 | medium |
| P16 | Ratna Dewi | 58 | P | 2 | PBPU | Makassar | 5 | 0.88 | fraud |
| P17 | Slamet Riyadi | 61 | L | 2 | PBPU | Makassar | 5 | 0.86 | fraud |
| P18 | Tarmizi Karim | 69 | L | 3 | PBI | Jakarta | 4 | 0.74 | high |
| P19 | Umi Kalsum | 44 | P | 3 | PBPU | Yogyakarta | 5 | 0.78 | high |
| P20 | Wahyu Nugraha | 45 | L | 3 | PBPU | Yogyakarta | 5 | 0.79 | high |

## Diagnosis (ICD-10)

| Kode | Nama | Derajat | Jumlah Klaim | Skor Maks | Risiko |
| --- | --- | --- | --- | --- | --- |
| K29.7 | Gastritis, tanpa perdarahan | ringan | 10 | 0.95 | fraud |
| K35.8 | Apendisitis akut | sedang | 11 | 0.79 | high |
| K40.9 | Hernia inguinalis, tanpa obstruksi | sedang | 8 | 0.13 | low |
| I21.9 | Infark miokard akut, tidak spesifik | berat | 8 | 0.13 | low |
| J18.9 | Pneumonia, organisme tidak spesifik | sedang | 9 | 0.74 | high |
| E11.9 | Diabetes melitus tipe 2, tanpa komplikasi | ringan | 15 | 0.88 | fraud |
| N20.0 | Kalkulus ginjal | sedang | 8 | 0.13 | low |
| S72.0 | Fraktur kolum femur, tertutup | berat | 10 | 0.94 | fraud |
| O80 | Persalinan tunggal spontan | normal | 8 | 0.66 | high |
| K80.2 | Kolelitiasis, tanpa kolesistitis | sedang | 13 | 0.87 | fraud |

## Prosedur (ICD-9-CM)

| Kode | Nama | Kompleksitas | Biaya Rujukan | Jumlah Klaim | Skor Maks | Risiko |
| --- | --- | --- | --- | --- | --- | --- |
| 00.66 | Angioplasti koroner + stent (PCI) | tinggi | Rp 58.000.000 | 12 | 0.95 | fraud |
| 36.13 | Coronary artery bypass graft (CABG) | tinggi | Rp 78.000.000 | 0 | 0 | low |
| 47.09 | Apendektomi | sedang | Rp 6.800.000 | 11 | 0.79 | high |
| 53.1 | Reparasi hernia inguinalis | sedang | Rp 8.200.000 | 8 | 0.13 | low |
| 51.23 | Kolesistektomi laparoskopik | sedang | Rp 14.500.000 | 10 | 0.87 | fraud |
| 74.1 | Seksio sesarea | sedang | Rp 6.200.000 | 1 | 0.66 | high |
| 81.52 | Hemiarthroplasty panggul | tinggi | Rp 46.500.000 | 10 | 0.94 | fraud |
| 96.04 | Pemasangan pipa endotrakeal (intubasi) | rendah | Rp 750.000 | 3 | 0.87 | fraud |
| 93.90 | Terapi oksigen tekanan positif | rendah | Rp 640.000 | 0 | 0 | low |
| 98.51 | Fragmentasi batu saluran kemih (ESWL) | sedang | Rp 5.600.000 | 8 | 0.13 | low |

## Obat (FORNAS)

| Kode | Nama | Bentuk | FORNAS |
| --- | --- | --- | --- |
| M01 | Metformin 500 mg | tablet | Ya |
| M02 | Amlodipin 10 mg | tablet | Ya |
| M03 | Seftriakson 1 g | vial injeksi | Ya |
| M04 | Omeprazol 40 mg | vial injeksi | Ya |
| M05 | Salbutamol 2,5 mg nebules | nebulizer | Ya |
| M06 | Atorvastatin 20 mg | tablet | Ya |
| M07 | Furosemid 40 mg | tablet | Ya |
| M08 | Parasetamol 500 mg | tablet | Ya |
| M09 | Insulin glargin 100 UI/ml | pen isi ulang | Tidak |
| M10 | Klopidogrel 75 mg | tablet | Ya |

## Analisis Teks & Sentimen
Perluasan dataset untuk modul NLP/LLM (Gemini) dan analisis sentimen:
- **Alasan Berobat** — keluhan utama pasien saat admit (Encounter.reasonCode).
- **Rujukan** — asal FKTP, nomor, dan tanggal rujukan (FKTP ke FKRTL); kunjungan langsung untuk rawat jalan/kontrol.
- **Narasi Rekam Medis** — resume medis elektronik (Composition) untuk uji konsistensi narasi vs kode billing.
- **Umpan Balik Pasien** — kutipan survei kepuasan layanan sebagai basis analisis sentimen.
- **Sentimen & Skor Sentimen** — ground truth label (positif/netral/negatif) dan skor -1 s.d. 1.
- **Kontradiksi Narasi** — flag klaim yang narasinya bertentangan dengan penagihan (KLM001, KLM002, KLM003, KLM004, KLM005, KLM006, KLM018, KLM024 = 8 klaim).
Distribusi sentimen: 62 positif · 14 netral · 24 negatif. Sinyal sentimen fraud: pengakuan pasien tidak pernah menjalani tindakan yang ditagihkan (phantom billing), keluhan tagihan iur biaya (upcoding/overbilling), keluhan tagihan ganda (unbundling). Sentimen negatif bukan otomatis fraud — klaim normal dengan keluhan layunan negatif (antrean lama, parkir sempit, kebersihan) disertakan sebagai negative control.
## Database Klaim
Basis data 100 klaim (anak halaman ini) berisi seluruh baris dengan properti terfilter: Pasien, Dokter, Faskes, Diagnosis, Prosedur, Obat, Tanggal, LOS, Biaya, Skor Fraud, Risiko, Modus, Sindikat, Status, Kontribusi Saluran, Sinyal SHAP, dan Catatan. Gunakan filter Risiko = fraud atau Sindikat untuk mengecek deteksi simulasi. Versi JSON lengkap (termasuk 70 edges graf) tersedia di canvas "Dataset Simulasi Aegis-JKN".
## Ekspansi v2 — 300 Klaim, Kolom Alasan, dan Kesiapan ML/DL
Dataset diperluas dari 100 menjadi **300 klaim** (seed deterministik 20260707, seluruh baris baru KLM101—KLM300) dan setiap baris kini memiliki properti **Alasan** yang menjelaskan kenapa klaim tersebut fraud, anomali, atau normal.
**Distribusi label:** 36 fraud (12%), 14 high, 10 medium, 240 low; label anomali total 60 (20%). Skala risiko tetap: skor di bawah 0.35 low; 0.35—0.6 medium; 0.6—0.8 high; di atas 0.8 fraud.
### ⚠️ **PEMBERITAHUAN PERBAIKAN DATASET (v2.1 - 2026-10-07)**
> **Dataset saat ini (v2) BELUM SESUAI untuk validasi platform** karena **10 kekurangan kritis** yang harus diperbaiki. Versi **v2.1** akan menambahkan kolom dan fitur berikut untuk memenuhi syarat anti-leakage dan group-aware evaluation:
#### ✅ **Perubahan yang Sudah Diimplementasikan di v2.1:**
1. **Kolom Grouping Wajib** (Untuk Anti-Entity Leakage):
	- `pasien_id` (20 pasien → **P01-P40**)
	- `faskes_id` (6 FKRTL → **RS_A-RS_J**)
	- `dokter_id` (12 dokter → **D01-D20**)
	- *Tujuan*: Memungkinkan `GroupKFold` (pasien) dan `LeaveOneGroupOut` (faskes).
2. **Metadata Validasi**:
	- `seed` = `20260707` (deterministik)
	- `version` = `v2.1`
	- `timestamp` = Waktu generasi
3. **Blokir Kolom Leakage** (Di `configs/leakage.yaml`):
	- `Skor Fraud`, `Risiko`, `Status`, `Sinyal SHAP`, `Kontribusi Saluran`, `Modus`, `Sindikat` **DIHAPUS dari fitur** (hanya untuk evaluasi).
4. **Kolom Alasan 3-Tingkat** (Sudah ada di v2):
	- `FRAUD` (36 klaim)
	- `ANOMALI` (24 klaim: 14 high + 10 medium)
	- `NORMAL` (240 klaim)
#### 🔧 **Sindikat yang Diperbarui (9 Sindikat + 2 Fraud Tunggal):**

| ID | Modus | Klaim | Faskes | Dokter | Pasien | Skor | Keterangan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SYND-01 | Upcoding | KLM001—003 | RS_A | D01, D02 | P01—P03 | ≥0.93 | Dx gastritis (K29.7) → PCI (00.66) |
| SYND-02 | Phantom Billing | KLM004—006 | RS_C | D05 | P08—P10 | ≥0.92 | 3 klaim hemiarthroplasty identik |
| SYND-03 | Unbundling | KLM007—012 | RS_B | D07 | P12—P14 | 0.84—0.87 | Paket kolesistektomi dipecah |
| SYND-04 | Drug Diversion | KLM013—014 | RS_E | D09 | P16—P17 | 0.86—0.88 | Qty insulin 24—30 pen |
| SYND-05 | Cloning | KLM016—017 | RS_F | D08 | P19—P20 | 0.78—0.79 | Dua pasien, klaim identik |
| **SYND-06** | **Repeat Billing** | **KLM101—104** | **RS_G** | D13 | P21—P24 | **0.85—0.90** | Klaim dobel untuk episode sama |
| **SYND-07** | **Iur Biaya** | **KLM105—108** | **RS_H** | D14 | P25—P28 | **0.82—0.87** | Pungli luar JKN + klaim penuh |
| **SYND-08** | **Readmission Berulang** | **KLM109—114** | **RS_I** | D15 | P29—P34 | **0.75—0.80** | Readmission cepat tanpa indikasi |
| **SYND-09** | **Excessive Usage** | **KLM115—120** | **RS_J** | D16 | P35—P40 | **0.78—0.83** | Volume obat/layanan berlebih |
| - | Biaya Markup | KLM121 | RS_A | D03 | P04 | ≥0.85 | 4x tarif paket |
| - | Drug Diversion | KLM122 | RS_E | D09 | P18 | ≥0.80 | Volume insulin mustahil |

#### 📊 **Distribusi Entitas v2.1:**
- **Faskes**: RS_A—RS_J (10 FKRTL)
- **Dokter**: D01—D20 (20 dokter)
- **Pasien**: P01—P40 (40 pasien)
- **Diagnosis**: K29.7, K35.8, I10, J45.9, N39.0, dll.
- **Prosedur**: 00.66 (PCI), 51.23 (Kolesistektomi), dll.
#### 🛠️ **Kesiapan ML/DL (v2.1):**
1. **Anti-Leakage**:
	- `configs/leakage.yaml` **WAJIB** mem-blokir kolom turunan sistem.
	- **Unit test** (`tests/test_leakage.py`) gagal keras jika kolom leakage masuk fitur.
2. **Group-Aware Evaluation**:
	- `GroupKFold` (group=`pasien_id`)
	- `LeaveOneGroupOut` (group=`faskes_id`)
3. **Feature Engineering**:
	- Rasio biaya/tarif
	- Agregat 30 hari (pasien—dokter—faskes)
	- Flag duplikat, readmission, parsing kontribusi saluran
4. **Model Baseline**:
	- **XGBoost + SMOTE** (fallback: `sklearn.GradientBoosting`)
	- **MLP (PyTorch)** (fallback: `sklearn.MLPClassifier`)
5. **Graf Heterogen (MHGSL)**:
	- **3 Saluran**: Topologi (relasi), Fitur (cosine θ=0.85), Semantik (metapath)
	- **PyTorch Geometric (PyG)** + `HeteroData`
6. **XAI**:
	- **SHAP** (TreeExplainer untuk XGBoost, GradientSHAP untuk DL)
	- Per-saluran (topologi, fitur, semantik)
7. **Text Channel (Opsional)**:
	- **Gemini API** (toggle via `configs/text.yaml`)
	- Fallback: Heuristic lokal (`sklearn` + rule-based)
8. **Validasi**:
	- AUPRC/AUROC/F1 (prevalensi 3—7% untuk realistis)
	- Hit-rate per sindikat (SYND-01—SYND-09)
	- False negative analysis
#### ⚠️ **Catatan Prevalensi:**
- **12% fraud** (oversampled by design) → Hanya untuk **simulasi** dan **validasi model**.
- **Produksi**: Gunakan **AUPRC pada prevalensi 3—7%** (downsampling).
- **Semua metrik** **WAJIB** disertai label: *"simulasi sintetis, prevalensi oversampled".*
#### 📁 **Struktur File v2.1:**
```javascript
aegis-jkn/
├── data/
│   ├── raw/
│   │   ├── claims_300_v2.1.csv       # + kolom pasien_id, faskes_id, dokter_id, seed, version, timestamp
│   │   ├── edges_v2.1.json           # 70+ edges (graf heterogen)
│   │   ├── text_gt_v2.1.csv          # Ground truth teks (sentimen, kontradiksi)
│   │   └── leakage_blocklist.yaml    # Kolom terlarang
│   ├── processed/
│   │   ├── features_300.parquet     # Fitur bersih (tanpa leakage)
│   │   ├── graph_hetero.pt           # PyG HeteroData (3 saluran)
│   │   └── metadata.json             # Info dataset
```
#### 🎯 **Protokol Keputusan "SESUAI" (v2.1):**
Platform dinyatakan **✅ SESUAI** jika **SEMUA** kriteria terpenuhi:
1. ✅ **Integritas Data**: 300 baris utuh, 0 kebocoran fitur.
2. ✅ **Deteksi Fraud**: ≥90% dari 36 klaim fraud terdeteksi di antrian ≤20% (group-aware).
3. ✅ **Metrik Utama**: AUPRC & AUROC MHGSL ≥ baseline XGBoost/MLP.
4. ✅ **Per-Sindikat**: Setiap SYND-01—SYND-09 hit-rate \> 0.
5. ✅ **Konsistensi XAI**: SHAP sejalan dengan kolom `Alasan`.
6. ✅ **Saluran Teks**: 8 klaim kontradiksi masuk daftar prioritas.
7. ✅ **Kejujuran Label**: Semua metrik disertai catatan: *"simulasi sintetis, prevalensi oversampled".*
> **Jika kriteria 1—2 gagal → ❌ TIDAK SESUAI** (perbaiki dataset/generator).
> **Jika kriteria 3—4 gagal → ⚠️ DESAIN BELUM TERBUKTI UNGGUL** (fallback ke XGBoost + fitur graf turunan).
#### 🚀 **Rencana Pelaksanaan (8 Minggu):**

| Fase | Tujuan | Durasi | Output |
| --- | --- | --- | --- |
| **Fase 0** | Fondasi & Audit Data | Minggu 1 | Dataset v2.1, `leakage.yaml`, unit test |
| **Fase 1** | Baseline ML & DL | Minggu 2—3 | XGBoost + MLP + fitur graf turunan |
| **Fase 2** | Graf Heterogen & MHGSL | Minggu 4—6 | PyG HeteroData, MHGSL, SHAP per-saluran |
| **Fase 3** | Validasi Final & LLM | Minggu 7—8 | Laporan validasi, benchmark Kaggle, DP-CTGAN |

**Target**: Platform **SESUAI** siap untuk **Healthkathon 2026** dan **pilot 5 FKRTL**.
