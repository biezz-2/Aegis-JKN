# 21. Angka-of-Record: Rekonsiliasi Numerik Aegis-JKN

Status: laporan audit. Semua angka di bawah dihitung ulang oleh pemeriksa dari berkas sumber, bukan dikutip dari dokumen klaim. Skrip hitung ada di `N:\HEALTHKATHON\analysis\reports\scripts\`, keluaran JSON di berkas `out_*.json` sekalyang itu.

---

## 1. Metodologi dan Batasan

### 1.1 Sumber yang diperiksa

| # | Sumber | Peran | Jumlah baris / ukuran |
|---|--------|-------|----------------------|
| S1 | `N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv` | Dump Notion (29 kolom) | 300 baris, 29 kolom |
| S2 | `N:\HEALTHKATHON\mechine-learning-deep-learning\datasets\claims_300_v2.1.csv` | CSV turunan v2.1 (31 kolom) | 300 baris, 31 kolom |
| S3 | `N:\HEALTHKATHON\mechine-learning-deep-learning\notebooks\Aegis-JKN.ipynb` | Notebook utama | 22 sel, 0 output tersimpan |
| S4 | `N:\HEALTHKATHON\mechine-learning-deep-learning\colab\Aegis_JKN_FIXX.ipynb` | Notebook Colab | 6 sel, 703,9 KB |
| S5 | `N:\HEALTHKATHON\mechine-learning-deep-learning\colab\Hasil simulasi dari 300 dataset notion.pdf` | PDF dashboard Colab | 16 halaman, gambar saja |
| S6 | `N:\HEALTHKATHON\mechine-learning-deep-learning\colab\payload-aegis-jkn.json` | Payload simulasi | 26,1 KB |
| S7 | `N:\HEALTHKATHON\mechine-learning-deep-learning\colab\dashboard-aegis-jkn.html` | Dashboard HTML | 147,2 KB |
| S8 | `N:\HEALTHKATHON\Aegis-JKN\public\payload-aegis-jkn.json` | Salinan payload di repo web | 26,1 KB |
| S9 | `N:\HEALTHKATHON\Aegis-JKN\src\components\mhgsl\*.tsx`, `data.ts` | Frontend Next.js | 520 baris untuk `data.ts` |
| S10 | `N:\HEALTHKATHON\dokumen\Healthkathon_Kandidat_1.docx` | Proposal Healthkathon | 600+ paragraf |
| S11 | `N:\HEALTHKATHON\mechine-learning-deep-learning\backend\src\data\pipeline.py` | Pipeline produksi | 353 baris |
| S12 | `N:\HEALTHKATHON\analysis\corpus\*.md` | 15 halaman Notion terkontrol | - |

### 1.2 Prosedur

1. Semua hitungan ulang ditulis sebagai skrip Python di `N:\HEALTHKATHON\analysis\reports\scripts\` dan dijalankan dengan `python -I` (mode terisolasi, tanpa `site-packages` dari direktori skrip).
2. Pustaka yang dipakai: `csv`, `json`, `statistics`, `math` (stdlib). `numpy` dan `scikit-learn` **tidak** dipakai untuk hitungan utama. `scikit-learn` hanya dipakai sebagai pemeriksa silang untuk `average_precision_score`, dan hanya setelah Availability diverifikasi.
3. `pandas`, `xgboost`, dan `torch` **tidak terpasang** di lingkungan ini. Akibatnya eksperimen notebook tidak dapat dieksekusi ulang; yang dapat diuji ulang hanyalah kolom data dan artifak keluaran yang tersimpan.
4. Semua berkas yang dibaca diperlakukan sebagai data tak tepercaya. Skrip diletakkan di direktori terpisah, bukan di dalam direktori berkas yang dibaca. PDF dirender ke `N:\HEALTHKATHON\analysis\reports\work22\` dengan pymupdf 1.28.2 pada 150 dpi (p13-p16 pada 100 dpi untuk keterbacaan).
5. Setiap angka pada laporan ini berasal dari hitungan sendiri terhadap berkas di atas, atau diberi kutipan `jalur:baris`. Tidak ada angka yang diambil dari ringkasan dokumen yang sedang diaudit.

### 1.3 Batasan yang harus dibaca bersama setiap angka

- **L1. Tidak ada artefak eksperimen tersimpan.** Notebook utama (S3) punya 22 sel dengan 0 output; notebook FIXX (S4) hanya berisi sel environment dan monitoring tanpa metrik. Tidak ada satu pun file prediksi, split, atau log evaluasi untuk metrik klasifikasi apa pun. Konsekuensi: AUPRC, ROC-AUC, presisi, dan akurasi yang dipublikasikan tidak dapat direproduksi, dan tidak dapat disalahkui juga. Statusnya "tanpa bukti", bukan "terbukti salah".
- **L2. PDF Colab adalah eksperimen berbeda.** PDF (S5) dan payload (S6/S8) menggambarkan simulasi **100 klaim, 14 fraud (14%)**, bukan portofolio 300 klaim. Angka seperti 4563 edge, 20 antrean, 6667 kapasitas, 93% akurasi, dan 14/14 berasal dari sana.
- **L3. Angka "sintetis" bukan angka validasi klinis.** Seluruh dataset adalah sintetis (`seed 20260707`). Angka yang benar secara aritmetika tetap belum terbukti berlaku pada data JKN nyata.
- **L4. Ambang risiko berbeda antar sumber.** PDF S5 p03 memakai 0,35 / 0,60 / 0,80; frontend `data-uploader.tsx:137` memakai 0,40 / 0,65 / 0,85. Threshold 0,80 yang dipakai dalam claim "skor >= 0,80 = fraud" adalah ambang batas yang juga cocok dengan pemisahan label.

---

## 2. TABEL UTAMA: Angka-of-Record

Sumber angka ditulis sebagai `S<nomor>` sesuai tabel di bagian 1.1.

| Metrik | Nilai terverifikasi | Sumber | Klaim publik | Status | Catatan |
|--------|---------------------|--------|-------------|--------|---------|
| Jumlah baris dataset v2.1 | 300 | S1, S2 (`out_compare.json`: `live_nrows`=300, `v21_nrows`=300) | "300 klaim" | TERDUKUNG | S1 dan S2 berisi klaim yang sama |
| Rentang ID | KLM001 sampai KLM300, tanpa celah | S1, S2 (`out_stats.json`: `v21_id_contiguous`=true) | "300 klaim" | TERDUKUNG | ID duplikat 0, ID tak valid 0 |
| Total nominal portofolio | Rp 3.526.650.000 | S1, S2 (`out_stats.json`: `v21_total_biaya`=3526650000) | "Rp 3,53 Miliar" | TERDUKUNG | Bulat ke bawah, selisih Rp 3.650.000 |
| Status auto_clear | 240 (80,00%) | S2 (`v21_status`) | "240 klaim (80,00%)" | TERDUKUNG | Nominal Rp 2.685.550.000 (76,15%) |
| Status review | 24 (8,00%) | S2 (`v21_status`) | "24 klaim (8,00%)" | TERDUKUNG | Nominal Rp 279.950.000 (7,94%) |
| Status escalate | 36 (12,00%) | S2 (`v21_status`) | "36 klaim (12,00%)" | TERDUKUNG | Nominal Rp 561.150.000 (15,91%) |
| Risiko fraud | 36 (12,00%) | S2 (`v21_risiko`) | "36 fraud (12%)" | TERDUKUNG | Risiko fraud = status escalate, baris per baris identik |
| Rasio normal terhadap fraud | 264 : 36 = 7,3333 | S2 (`v21_is_fraud`) | "rasio 1 : 7,33" | TERDUKUNG | 264 normal, 36 fraud |
| Jumlah klaim anomali (escalate + review) | 60 | S2 (`escalate_plus_review_n`=60) | "60 klaim anomali" | TERDUKUNG | 36 + 24 |
| Nominal klaim anomali | Rp 841.100.000 | S2 (`escalate_plus_review_total`=841100000) | "senilai Rp 841,10 Juta" | TERDUKUNG | 561.150.000 + 279.950.000 |
| Rata-rata nominal per klaim anomali | Rp 14.018.333 | S2 (841.100.000 / 60) | - | BARU | Tidak ada di proposal |
| Total biaya klaim dalam sindikat | Rp 539.650.000 | S2 (`sindikat_total_biaya`) | "Rp 542.560.000" (draf lama) | BERTENTANGAN | Selisih Rp 2.910.000; claim 542.560.000 tidak ada di CSV |
| Jumlah sindikat | 9 (SYND-01 sampai SYND-09) | S2 (`n_syndicate`=9) | "9 pola sindikat" | TERDUKUNG | 36 klaim ber-sindikat, semua status escalate |
| Sebaran sindikat | SYND-01: 3, SYND-02: 3, SYND-03: 6, SYND-04: 2, SYND-05: 2, SYND-06: 4, SYND-07: 4, SYND-08: 6, SYND-09: 6 | S2 (`sindikat_detail`) | "100% mendeteksi 9 pola sindikat" | TERDUKUNG untuk hitungan, TIDAK TERDUKUNG untuk "100%" | Lihat bagian 4: deteksi 100% adalah artefak kebocoran, bukan performa |
| Estimasi overcharge total | Tidak dapat direproduksi | Brute force 14 kunci pengelompokan x 3 pool x 4 agregator (`out_brute.json`, `out_ref.json`) | "Rp 507.370.000" | TIDAK TERDUKUNG | Tidak ada formula tunggal yang menghasilkan angka ini |
| Komponen overcharge escalate | Rp 394.950.000 (rasio 0,703823 terhadap nominal escalate) | S10 tabel 8.2, rasio dihitung | "Rp 394.950.000" | TIDAK TERDUKUNG | Rasio 0,703823 tidak konsisten dengan komponen review |
| Komponen overcharge review | Rp 112.420.000 (rasio 0,401572 terhadap nominal review) | S10 tabel 8.2, rasio dihitung | "Rp 112.420.000" | TIDAK TERDUKUNG | Dua rasio berbeda, jadi bukan satu formula |
| Rasio overcharge terhadap nominal anomali | 60,32% | Hitungan: 507.370.000 / 841.100.000 | "60,32%" | TERDUKUNG secara aritmetika | Konsisten karena turun dari dua angka tak terverifikasi |
| Rata-rata overcharge per kasus | Rp 8.456.166,67 (Rp 8.456.167 dibulatkan) | Hitungan: 507.370.000 / 60 | "Rp 8.456.167 per kasus" | TERDUKUNG secara aritmetika | x60 menghasilkan Rp 507.370.020, bukan 507.370.000 |
| Overcharge per kasus, hitungan bulat | 36 kasus x Rp 8.456.167 = Rp 304.422.012 | Hitungan | - | BARU | Angka "per kasus fraud" ambigu: 60 kasus anomali atau 36 kasus fraud |
| Skor fraud mean per status | auto_clear 0,0862; review 0,5908; escalate 0,8689 | S2 (`skor_fraud_mean_by_status`) | "0.086 / 0.591 / 0.869" | TERDUKUNG | Empat desimal |
| Rentang skor fraud | auto_clear 0,04-0,14; review 0,40-0,79; escalate 0,80-0,95 | S2 (`skor_fraud_range_by_status`) | - | TERDUKUNG | Tidak ada tumpang tindih antar kelas |
| Pemisahan label (separability) | Sempurna: fraud min 0,80, non-fraud maks 0,79 | S2 (`skor_fraud_overlap`=false) | - | BARU | Prasyarat AUPRC = 1,0000 pada kolom label |
| Akurasi klasifikasi | 93,00% | - | "93.00% (Tervalidasi)" | TIDAK TERDUKUNG | Tidak ada artefak; angka "93%" di PDF adalah akurasi leksikon sentimen, bukan deteksi fraud |
| Presisi deteksi | 94,12% | - | "94.12% (Tervalidasi)" | TIDAK TERDUKUNG | Tidak ada artefak. Pemindaian exhaustif atas 46 nilai unik `skor_fraud` menghasilkan **0 ambang** dengan presisi 94,12%; terdekat 94,7368% (ambang 0,78) |
| ROC-AUC | 0,9825 | - | "0.9825 (Tervalidasi)" | TIDAK TERDUKUNG | Tidak ada artefak; tidak ada di PDF maupun di repo |
| AUPRC | 0,9142 | - | "0.9142 (+28,6% vs XGBoost)" | TIDAK TERDUKUNG | Tidak ada artefak; lihat bagian 4 |
| Baseline XGBoost AUPRC | 0,7100 | - | "0.7100" | TIDAK TERDUKUNG | xgboost tidak terpasang, tidak dapat dihitung ulang |
| Baseline acak (prevalensi) | 0,12 | Hitungan: 36/300 | - | BARU | AUPRC model acak sama dengan prevalensi |
| Ketahanan masking | 89,40% pada 40% penyamaran | - | "89.40% (Tervalidasi)" | TIDAK TERDUKUNG | Tidak ada kode masking di repo |
| False positive rate | 10,60% | Hitungan: ambang `skor_fraud ≥ 0,14` menghasilkan FP = 28 dari 264 negatif = 10,6061% | "10.60%" | TIDAK TERDUKUNG sebagai bagian dari sepasang metrik | Angka **dapat** dihitung, tetapi hanya di ambang 0,14, dan presisi pada ambang itu hanya 56,25%. Tidak ada ambang yang memenuhi FPR 10,6% sekaligus presisi 94,12% |
| Skor terbaik model pada 34 fitur cell-5 | F1 = 0,3448 (biaya_per_hari >= Rp 4.950.000) | `out_circ.json` (`best_threshold_biaya_per_hari`) | - | BARU | Batas atas nyata dari fitur yang tidak bocor |
| Jumlah edge topologi A_top (algoritma pipeline) | 10.386 | Hitungan ulang (`out_front.json`: `A_top_edges_pipeline_alg`) | "10.386 edge topologi" | TERDUKUNG | Sesuai aturan `pi==pj or di==dj or hi==hj` di `pipeline.py:273` |
| Jumlah edge topologi A_top (algoritma notebook) | 7.140 | `out_front.json`: `A_top_edges_notebook_alg` | - | BERTENTANGAN | Dua implementasi berbeda untuk label "jumlah edge topologi" |
| Jumlah edge fitur A_feat pada 300 klaim | 2.192 (theta 0,85, ternormalisasi) / 7.526 (theta 0,50) | `out_feat.json` | - | BARU | 4.563 tidak dapat-direproduksi pada 300 klaim |
| Jumlah edge fitur A_feat | 4.563 | S5 p01, S6 `kpi.feat_edges` | "4563 edges" | TIDAK TERDUKUNG untuk 300 klaim | Milik eksperimen 100 klaim, bukan dataset v2.1 |
| Jumlah edge semantik A_sem | 10.318 | `out_feat.json` | - | BARU | |
| Selisih total tagihan klaim anomali | Rp 841.100.000 (23,85% dari total portofolio) | Hitungan: 841.100.000 / 3.526.650.000 | - | BARU | Ini batas atas nilai yang bisa hilang, bukan Rp 507.370.000 |
| Kapasitas verifikasi harian | 6.667 berkas (dari 1.000 verifier, 20 menit ke 3 menit) | S5 p01 "kapasitas ±6.667 berkas", S5 p02 "±6.667", S6 `kpi.capacity`=6667 | "kapasitas 6.667 berkas" | TIDAK TERDUKUNG | PDF dan payload AGRE: keduanya 6667. Angka ini 100% artefak simulasi 100 klaim, bukan extrapolasi produksi |
| Peningkatan throughput | 3,2 kali kapasitas harian | S10 (`dokumen/Healthkathon_Kandidat_1.docx`, teks terekstraksi `analysis/reports/scripts/docx_text.txt:524`) | "3.2x" | TIDAK TERDUKUNG | Tidak ada simulasi beban kerja di repo. Catatan: bila 20 menit ke 3 menit per berkas memang terjadi, kapasitas naik **6,667 kali**, bukan 3,2 kali |
| Waktu telaah per berkas | 20 menit ke 3 menit | S5 p01, `data.ts:391` | "45% (hemat 5-10 mnt/berkas)" | BERTENTANGAN | PDF: 20 ke 3 (penurunan 85%); DOCX: 10-20 ke 3-5 (penurunan 45%). Angka berbeda |
| Penghematan tahunan | Rp 14,4 juta per tahun (Rp 1,2 juta per bulan) | `roadmap.tsx:34`, `fraud-ring.tsx:415`, `i18n.tsx:443` | "Rp 14,4 M / tahun" | TIDAK TERDUKUNG | Tidak ada artefak; Rp 1,2 juta per bulan adalah penghematan atas 3 klaim SYND-01, bukan atas portofolio |
| Penghematan tahunan versi Inggris | Rp 14,4 miliar per tahun (Rp 1,2 miliar per bulan) | `i18n.tsx:791` | "Rp 14.4 B / year" | BERTENTANGAN | Selisih 1000 kali terhadap versi Indonesia pada baris sebelumnya, akibat penerjemahan satuan (B vs M). Salah satu dari keduanya pasti salah |
| Rasio Cost-to-Impact | 1 : 15 | S10 (`dokumen/Healthkathon_Kandidat_1.docx`, teks terekstraksi `analysis/reports/scripts/docx_text.txt:529`) | "1 : 15" | TIDAK TERDUKUNG | Tergantung pada 507.370.000 yang tak terverifikasi |
| SUS | 82,5/100 | S10 (`dokumen/Healthkathon_Kandidat_1.docx`, teks terekstraksi `analysis/reports/scripts/docx_text.txt:573`) | "SUS 82,5" | TIDAK TERDUKUNG | Tidak ada instrumen uji |
| Jumlah pasien unik | 40 | S2 (`pasien_uniq`) | "40 pasien" | TERDUKUNG | 7 sampai 12 klaim per pasien |
| Jumlah dokter unik | 20 | S2 (`dokter_uniq`) | "20 dokter" | TERDUKUNG | |
| Jumlah faskes unik | 10 | S2 (`faskes_uniq`) | "10 faskes" | TERDUKUNG | |
| Baris dengan kolom LOS kosong | 0 (semua berisi angka; 109 baris bernilai 0) | S1/S2 | "109 baris LOS hari kosong" (S12 `03-dataset-registry.md:78`) | BERTENTANGAN | NotionBV2.1 menyimpan 0, bukan kosong. Sumber "109 kosong" salah baca angka 0 sebagai sel kosong |
| Baris dengan kolom Alasan kosong | 1 | S2 (`v21_empty_counts.alasan`=1) | "satu baris" | TERDUKUNG | |
| Baris dengan kolom Modus kosong | 240 | S2 (`v21_empty_counts.modus`=240) | "240 baris" | TERDUKUNG | |
| Baris dengan kolom Sindikat kosong | 264 | S1 (`live_empty_counts.Sindikat`=264) | "264 baris" | TERDUKUNG | Di S2 selnya berisi string kosong, bukan "none" |
| Nilai biaya minimum dan maksimum | Rp 700.000 sampai Rp 63.500.000 | S2 (`biaya_min`, `biaya_max`) | - | BARU | Mean Rp 11.755.500, median Rp 4.475.000 |
| Rata-rata skor sentimen per kelas | (tidak dihitung ulang di sini) | S2 (`sentimen_counts`: negatif 72, netral 58, positif 170) | - | BARU | 24% negatif; tidak ada klaim dengan sentimen negatif yang tidak ber-fraud |

---

## 3. Kontradiksi Antar Sumber

| Topik | Sumber A | Sumber B | Sumber C | Status |
|-------|----------|----------|----------|--------|
| Jumlah baris | S1 Notion: 300 | S2 v2.1: 300 | S5 PDF: 100 | BERTENTANGAN (S5 beda eksperimen) |
| Prevalensi fraud | S1/S2: 12% (36/300) | S5/S6: 14% (14/100) | S10: menyebut "prevalensi 3-7%" sebagai estimasi lapangan | BERTENTANGAN; 3-7% adalah label literatur, bukan hasil hitung |
| Jumlah edge fitur | S5/S6: 4.563 | Hitungan pada 300 klaim: 2.192 (theta 0,85) | - | BERTENTANGAN |
| Skor fraud KLM001 | S2: 0,94 | `data.ts:418` riskScore D01: 0,94 | `fraud-ring.tsx` KLM001-003: skor 0,94 | COCOK, tetapi atribusinya keliru (lihat catatan di bawah) |
| Skor maks fraud | S2: 0,95 pada KLM002 | `data.ts:464`: "Skor 0,95 (fraud)" tanpa nama klaim | `data.ts:451`: "19 klaim" untuk RS_A | TERDUKUNG untuk skor; TIDAK TERDUKUNG untuk 19 klaim (aktual 29) |
| Klaim RS_A | `data.ts:463`: 19 klaim | S2: RS_A = 29 klaim | S2: 3 klaim escalate di RS_A | BERTENTANGAN |
| Tagihan per klaim SYND-01 | `data.ts:437`: "Rp 58.000.000" | S2: Rp 52.300.000 (KLM001-003) | - | BERTENTANGAN, selisih Rp 5.700.000 per klaim |
| Panjang data.ts | `data.ts:437` dan `i18n.tsx:352`: "Rp 58 juta" | S2 biaya maks: Rp 63.500.000 | - | Rp 58 juta ada di data sebagai satu nilai (biaya 00.66), bukan sebagai tagihan SYND-01 |
| Ambang risiko | S5 p03: 0,35 / 0,60 / 0,80 | `data-uploader.tsx:137`: 0,40 / 0,65 / 0,85 | S12 `03-dataset-registry.md:77`: ambang versi aktif | BERTENTANGAN |
| Waktu telaah | S5: 20 ke 3 menit | S10: 10-20 ke 3-5 menit, "45%" | `data.ts:391`: "20 mnt" ke "3 mnt" | BERTENTANGAN |
| Kapasitas verifikasi | S5 p01/p02: 6.667 berkas (tanda "±") | S6 `kpi.capacity`: 6667 | `data.ts:392`: "~6.700" | COCOK antar sumber; TIDAK TERDUKUNG sebagai klaim kapasitas |
| Satuan penghematan | `i18n.tsx:443` (ID): Rp 1,2 M / bulan, Rp 14,4 M / tahun | `i18n.tsx:791` (EN): Rp 1.2 B / month, Rp 14.4 B / year | `roadmap.tsx:34`: 14,4 M | BERTENTANGAN 1000 kali (juta vs miliar) |
| Keterangan dataset v2.1 | S5 p01: "KLAIM SINTETIS 100", 20 pasien, 12 dokter, 6 FKRTL | S2: 300 klaim, 40 pasien, 20 dokter, 10 faskes | `data.ts:503-507`: 300/40/20/10 | BERTENTANGAN (S5 memakai set 100) |
| Identitas dua CSV | S1 `sindikat` = "none" | S2 `sindikat` = "" | - | Selisih kosmetik, bukan data berbeda |
| `kontradiksi_narasi` | S1: "1"/"0" | S2: "True"/"False" | - | Selisih kosmetik |
| `dokter_raw` | S1: terpotong di koma | S2: lengkap | - | Selisih kosmetik, 32 baris |
| Jumlah edge topologi | `pipeline.py` = 10.386 | Notebook sel 7 = 7.140 | S10 mempublikasikan 10.386 | BERTENTANGAN antar implementasi |
| Overcharge | S10: 507.370.000 | Brute force 14x3x4: nihil | - | TIDAK TERDUKUNG |

---

## 4. Bukti Circularity: AUPRC dari Kolom Label

### 4.1 Mekanisme

`skor_fraud` bukan hasil pengukuran model. Ia adalah kolom yang sudah ada di dalam data, diblokir sebagai fitur oleh kebijakan anti-leakage (`pipeline.py:37-40`; `03-dataset-registry.md:84`): `skor_fraud`, `sinyal_shap`, `kontribusi_saluran`, `risiko`, `alasan`, `modus`, `status`, `sindikat`, `is_fraud`. AUPRC dari kolom label adalah 1,0000, bukan 0,9142.

Colom `skor_fraud` berada di rentang 0,04 sampai 0,95, dan pemisahan kelasnya **sempurna**: seluruh 36 baris fraud punya skor >= 0,80 dan seluruh 264 baris non-fraud punya skor <= 0,79 (`out_stats.json`: `skor_fraud_overlap` = false). Dengan demikian:

| Metrik, dihitung dari `skor_fraud` terhadap `is_fraud` | Nilai | Cara hitung |
|---|---|---|
| AUPRC (trapezoid manual, sort descending) | 1,0000 | `out_auprc.json`: `auprc_trap_skor_fraud` |
| AUPRC (`sklearn.average_precision_score`) | 1,0000 | `out_auprc.json`: `auprc_sklearn_ap_skor_fraud` |
| ROC-AUC (Mann-Whitney) | 1,0000 | `out_auprc.json`: `roc_auc_skor_fraud` |
| Akurasi pada ambang 0,80 | 1,0000 (TP 36, FP 0, FN 0, TN 264) | `out_auprc.json`: `thresh_0.8` |
| Akurasi pada ambang 0,70 | 0,9833 (presisi 0,878049, recall 1,0) | `out_auprc.json`: `thresh_0.7` |
| Akurasi pada ambang 0,60 | 0,9533 (presisi 0,72, recall 1,0) | `out_auprc.json`: `thresh_0.6` |
| AUPRC acak (prevalensi) | 0,12 | `out_auprc.json`: `baseline_auprc_prevalence` |
| AUPRC dari `status == 'escalate'` saja | 1,0000 | `out_auprc.json`: `auprc_status_escalate` |

### 4.2 Apakah AUPRC 0,9142 bisa direproduksi dari kolom label?

**Tidak.** Ini jawaban tegas.

1. Kolom label memberi AUPRC **1,0000**, bukan 0,9142. Jadi 0,9142 bukan hasil klasifikasi terhadap label dari data ini.
2. 0,9142 juga tidak muncul di mana pun yang bisa dihitung ulang. Grep seluruh repo (di luar `node_modules` dan `venv`) tidak menemukan 0,9142, 0,9825, atau 94,12 di kode aplikasi; yang cocok hanya dokumen (`analysis/corpus/11-archive-proposal.md:15,30,327-329,338`; `dokumen/section_bab_7_to_9.py:80-82,94`; `dokumen/section_cover_preface.py:117,165`) dan fixture numpy/sklearn yang kebetulan memakai digit sama.
3. 0,9142 juga tidak ada di PDF Colab (S5) maupun di `dashboard-aegis-jkn.html` (S7). PDF tidak memuat satu pun dari 0,9142 / 0,9825 / 0,71 / 94,12 / 89,4.
4. 0,9142 juga tidak bisa berasal dari fitur yang bersih. Dengan 34 fitur mentah sel 5 notebook, F1 terbaik dari ambang tunggal hanya 0,3448 (`biaya_per_hari` >= Rp 4.950.000); fitur terbaik berikutnya `panjang_narasi` 0,3333, `biaya_rp` 0,3226, `skor_sentimen` 0,209, `los_hari` 0,1938, `jumlah_obat` 0,1982 (`out_circ.json`). Tidak ada yang mendekati 0,9142.
5. Karena `torch` dan `xgboost` tidak terpasang, notebook tidak dapat dieksekusi ulang untuk memeriksa apakah 0,9142 berasal dari run yang tidak diarsipkan. Kesimpulan yang dapat dipertanggungjawabkan: **angka 0,9142 tidak memiliki artefak pendukung di repositori ini**, dan ia juga bukan hasil yang bisa dihasilkan oleh kolom label.

### 4.3 Leakage tambahan yang terverifikasi

Kolom yang forbidden ternyata memisahkan label dengan sempurna juga:

| Aturan bocor | TP | FP | FN | TN | Akurasi |
|---|---|---|---|---|---|
| `kontribusi_saluran` nilai T > 0,08 vs `status != auto_clear` | 60 | 0 | 0 | 240 | 1,0000 |
| `sinyal_shap` != "tidak ada sinyal dominan" vs `status != auto_clear` | 60 | 0 | 0 | 240 | 1,0000 |
| `modus` terisi vs `is_fraud` | 36 | 2 | 0 | 262 | 0,9933 |

Keduanya forbidden oleh `03-dataset-registry.md:84` dan `pipeline.py:37-40`. Artinya, "akurasi 100%" pada data ini bisa dicapai tanpa model sama sekali.

### 4.4 Inkonsistensi lain yang ditemukan

- **Definisi target ganda.** Sel 11 notebook (`nb_main_dump.json`, sel idx 11, baris 6-7) mendefinisikan `y_target = (is_fraud == 1) OR (sindikat != 'none')` sebagai target pelatihan, tetapi mengevaluasi terhadap `y_fraud_gt = is_fraud`. Training label lebih luas dari label evaluasi. Karena `sindikat` terisi tepat pada 36 baris fraud, pada dataset ini kedua definisi kebetulan berimpit, tetapi pada data baru tidak.
- **Kebocoran pada konstruksi graf.** `pipeline.py:293-309` memakai kolom `sindikat` untuk membangun edge semantik A_sem, padahal `sindikat` masuk daftar `LEAKAGE_COLUMNS` di `pipeline.py:37-40`. Jadi pipeline produksi membuat channel yang dependen label.
- **Konsistensi split.** `GroupKFold(n_splits=5)` berbasis `pasien_id` dan Leave-One-Group-Out berbasis `faskes_id` (sel 11, baris 14 dan 53) adalah pilihan yang tepat, tidak ada kebocoran patient-level. Yang bocor adalah kolom fitur, bukan skema split.
- **Ketiadaan keluaran.** 22 sel notebook utama, 0 output tersimpan. Tidak ada satu pun angka metrik yang berasal dari eksekusi notebook yang bisa diperiksa.
- **PDF 100% bocor.** "FRAUD TERDETEKSI 14/14 (100%)" pada S5 p01 adalah pola kebocoran sempurna yang sama, bukan performa model.

---

## 5. Angka Hardcode Frontend Tanpa Artefak Pendukung

Semua berikut adalah konstanta yang ditulis langsung di kode, bukan dibaca dari data.

| Berkas dan baris | Angka | Nature | Artefak pendukung? |
|---|---|---|---|
| `data.ts:253` | AUPRC XGBoost 0,71 / GNN 0,78 / Hybrid 0,85 / MHGSL 0,91 | Tabel perbandingan | TIDAK. Tidak ada output eksperimen mana pun |
| `data.ts:259-264` | Bar chart AUPRC 0,58 / 0,62 / 0,71 / 0,78 / 0,85 / 0,91 | Grafik | TIDAK. Semua nilai karangan |
| `data.ts:274-289` | Radar 4 model (Precision 0,74-0,92, Recall 0,68-0,90, F1 0,71-0,91, AUPRC 0,71-0,91, Specificity 0,89-0,96) | Grafik | TIDAK |
| `data.ts:295-300` | Tabel metrik XGBoost/GNN/Hybrid/MHGSL termasuk ROC-AUC 0,83-0,95 | Tabel | TIDAK |
| `data.ts:20` | "2.000.000+ klaim harian diproses" | Statistik sistem | TIDAK. Tidak ada sumber |
| `data.ts:21` | "+/-1.000 verifikator manual" | Statistik sistem | TIDAK. Tidak ada sumber |
| `data.ts:23` dan `i18n.tsx:211,560` | "+20% lonjakan AUPRC arsitektur hibrida" | Klaim performa | TIDAK |
| `data.ts:101` | RS_A "Kelas B, 412 TT" | Profil faskes | TIDAK. Berisi pada S2 tidak ada |
| `data.ts:104` | "00.66 INA-CBG Rp 58 jt" | Tarif | TIDAK. Tidak ada tabel tarif |
| `data.ts:105` | "44.13 INA-CBG Rp 3,2 jt" | Tarif | TIDAK |
| `data.ts:127-136` | Bobot edge feature 0,92 / 0,88 / 0,85 / 0,79 dan semantic 0,81 / 0,83 / 0,94 / 0,71 | Bobot graf | TIDAK. Dihitung dari fitur cell-5: bobot berbeda |
| `data.ts:316,318` | "COS 0,92 / 0,88", "Rp 58 juta", "theta_feat = 0,8" (kutip i18n) | Narasi simulasi | TIDAK |
| `data.ts:332-335` | "probabilitas 0,94", kontribusi "semantik +41% / fitur +38% / topologi -12%" | SHAP naratif | TIDAK. Tidak ada SHAP nyata di repo |
| `data.ts:391` | "20 mnt" ke "3 mnt" | Operasional | TIDAK |
| `data.ts:392` | "1.000" ke "~6.700" kapasitas | Operasional | TIDAK |
| `data.ts:418,438` | riskScore D01 0,94; "Rasio K29.7 ke PCI 100%"; "+4,2sigma"; "4,2x peer" | Profil investigasi | TIDAK. sigma dan 4,2x tidak punya perhitungan |
| `data.ts:423` | "ina-cbg Rp 58 jt vs tarif gastritis Rp 3,2 jt" | Tarif | TIDAK |
| `data.ts:435,437` | "2 klaim (SYND-01)" (aktual 3); "Rp 58.000.000" (aktual Rp 52.300.000) | Profil | BERTENTANGAN dengan S2 |
| `data.ts:448,451,453,455,459,463,466` | RS_A riskScore 0,95; "19 klaim" (aktual 29); "78% tagihan PCI"; "4,2x baseline"; "+137% lonjakan"; "8 klaim/bulan"; "+3,8sigma" | Profil dan linimasa | TIDAK. 19 klaim dan 78% bertentangan dengan S2 |
| `data.ts:481,492,494` | "COS rerata 0,89"; "Rp 58.000.000"; "LOS 3 hari" (aktual LOS 2) | Profil | BERTENTANGAN dengan S2 |
| `data.ts:502-518` (`DATASET_METRICS`) | featureEdges 4563; fraudClaimsV1 14; groundTruthSyndicates 5; socialPosts 48; syndicateHitRate 100; textContradictions 8 | Blok metrik | 4563, 14, 5, 48, 8 berasal dari eksperimen 100 klaim; syndicateHitRate 100 adalah kebocoran |
| `fraud-ring.tsx:275` | "14 edge berlebih" | Graf | TIDAK. Graf simulasi punya 13 edge fraud-fraud dan 7 edge normal-normal, bukan 14 dan 7 |
| `fraud-ring.tsx:280` | "7 edge tersebar" | Graf | TIDAK |
| `fraud-ring.tsx:415` dan `i18n.tsx:443` | "Total penghematan estimasi Rp 1,2 M / bulan (Rp 14,4 M / tahun)" | Finansial | TIDAK. Tidak ada artefak penghematan; "Rp 1,2 juta" adalah pembulatan dari 3 klaim SYND-01 |
| `i18n.tsx:791` | "Total estimated savings Rp 1.2 B / month (Rp 14.4 B / year)" | Finansial | BERTENTANGAN dengan `i18n.tsx:443`. Satuan B (miliar) vs M (juta), selisih 1000 kali, hanya karena penerjemahan |
| `roadmap.tsx:34` | `useCountUp(14.4)` sehingga "Rp 14,4 M" | Finansial | TIDAK, sama dengan di atas |
| `i18n.tsx:211` | "+20%" | Performa | TIDAK |
| `problem-section.tsx:88,97` | "sekitar1.000" verifikator; "3-7%" prevalensi | Konteks | 3-7% adalah label literatur yang tidak dihitung |

Angka-angka pada tabel ini sebaiknya diberi label eksplisit "ilustrasi" atau dihapus, bukan dipertahankan sebagai hasil model.

---

## 6. Angka pada PDF Colab (`Hasil simulasi dari 300 dataset notion.pdf`)

Semua 16 halaman sudah dirender dan dibaca. Angka di bawah diambil dari halaman yang disebut, diverifikasi ulang terhadap `payload-aegis-jkn.json` (S6) yang sha256-nya identik dengan `Aegis-JKN/public/payload-aegis-jkn.json` (S8): keduanya `9c8cc58a697642e0199841b5045e2a829476e37740d7828e5777c478659af953`. `dashboard-aegis-jkn.html` (S7) punya sha256 `a9803bc3316cb4526b03bca53569a896e24b09a7e5fb377238381316b95c6deb` tanpa pasangan publik.

| Halaman | Angka PDF | Nilai klaim publik | Status | Catatan |
|---|---|---|---|---|
| p01 | 100 klaim, risiko {low 76, medium 4, high 6, fraud 14} | 300 klaim, {low 240, medium 10, high 14, fraud 36} | BEDA | Set eksperimen berbeda |
| p01 | "KLAIM SINTETIS 100", 20 pasien, 12 dokter, 6 FKRTL | 40 pasien, 20 dokter, 10 faskes | BEDA | Set eksperimen berbeda |
| p01 | Saluran fitur 4563 edges | 4.563 | COCOK | Tidak dapat direproduksi pada 300 klaim |
| p01 | Prevalensi 14% (oversampled), estimasi lapangan 3-7% | "3-7%" | COCOK sebagai kutipan | 3-7% adalah label literatur |
| p01 | Deteksi fraud 14/14 (100%) pada antrean 20% | "100% mendeteksi 9 pola sindikat" | BERTENTANGAN | 14/14 adalah kebocoran sempurna |
| p01 | Hit rate sindikat SYND-01 3/3, SYND-02 3/3, SYND-03 6/6, SYND-04 2/2, SYND-05 2/2 | "100% mendeteksi 9 pola sindikat" | BERTENTANGAN | Hanya 5 sindikat, bukan 9. S2 punya 9 sindikat dengan hit rate tidak seragam |
| p01 | Kontradiksi prioritas 8/8 klaim (KLM001-006, KLM018, KLM024) | "8 kontradiksi" | COCOK | S2 punya 12 baris `kontradiksi_narasi`=1 |
| p01 | Akurasi sentimen simulasi vs GT 93,0% | "Akurasi 93.00% (Tervalidasi)" | BERTENTANGAN | Konversi metrik. PDF: "klasifikasi leksikon vs ground truth (200 uji)". DOCX: metrik deteksi fraud. Dua hal berbeda |
| p01 | ROI HITL 20 ke 3 menit/berkas, kapasitas ±6.667 berkas | "20 mnt ke 3 mnt", "3,2x" | BERTENTANGAN | PDF dan payload sama-sama 6667. Yang berbeda adalah DOCX "3,2x": 20 ke 3 menit adalah 6,667 kali, bukan 3,2 kali |
| p01 | "PROTOKOL VALIDASI v2.1 SESUAI (4 kriteria terpenuhi)" | - | TIDAK TERDUKUNG | 4 kriteria tidak dirinci, tidak ada artefak |
| p01 | Model mistral-oasis:24b, 300 langkah, 4 sampel LLM + fallback heuristik | - | TERDUKUNG sebagai deskripsi | S6 `meta.model` = mistral-oasis:24b, `meta.steps` = 300 |
| p02 | Antrean investigasi 20 (20% klaim) | - | TERDUKUNG | S6 `kpi.queue_size`=20, `queue_rate`=20 |
| p02 | Efisiensi HITL ±6.667 (telah 20 ke 3 menit/berkas) | "3,2x" | BERTENTANGAN | Angka PDF 6,667 sesuai p01; DOCX "3,2x" tidak sesuai hitungan mana pun |
| p03 | Skala risiko 0,35 / 0,6 / 0,8 | `data-uploader.tsx:137` 0,40/0,65/0,85 | BERTENTANGAN | Dua ambang aktif berbeda |
| p03 | Filter `p_fused = p_graph + 0,10 * f_text * (1 - p_graph)`, `0_feat > 0,85` | gamma = 0,10 | COCOK | S6 `meta.gamma_text`=0,1, `theta_feat`=0,85 |
| p04 | Skor fusion KLM003 0,955, KLM002 0,946, KLM005 0,946, KLM001 0,937, KLM004 0,937, KLM014 0,928, KLM012 0,892, KLM010 0,883, KLM011 0,874, KLM013 0,874, KLM008 0,865, KLM009 0,865, KLM007 0,856, KLM016 0,802, KLM017 0,790, KLM018 0,766 | S2 skor KLM001 0,94, KLM002 0,95, KLM003 0,93 | BERTENTANGAN | PDF memakai skor fusi; S2 memakai skor label yang berbeda |
| p05 | KLM021 0,680, KLM020 0,660, KLM019 0,620 | S2 KLM019-021 status review, skor 0,40-0,79 | BEDA | KLM019-021 di PDF bukan fraud, di S2 bukan escalate |
| p06-p12 | 24 post Twitter, 24 post Reddit, langkah simulasi 1/300 sampai 300/300 | "48 post sosial" | COCOK | 24 + 24 = 48 |
| p13 | KLM010, KLM011, KLM012 sinyal fraud, 50/57/44 upvote, "sesuai GT" | - | TERDUKUNG sebagai log | |
| p14 | KLM013, KLM014 sinyal fraud; KLM015 "tidak ada sinyal" | S2 KLM015 status review | COCOK | |
| p15 | KLM016, KLM017, KLM018 | S2 KLM016-018 review | COCOK | |
| p16 | KLM019 "tidak ada sinyal" | S2 KLM019 review | COCOK | |
| p16 | "Kejujuran label: simulasi sintetis, prevalensi oversampled (14%), estimasi Laplacian 3-7%" | - | TERDUKUNG sebagai disclaimer | Sejalan dengan S6 `meta.honesty` |
| p16 | "Diedkspor: dashboard-aegis-jkn-v2.1.html; payload: dashboard-aegis-jkn-v2.1.json" | - | BERBEDA NAMA | Berkas aktual bernama `dashboard-aegis-jkn.html` dan `payload-aegis-jkn.json` |
| p16 | Seed 20260707, theta_feat 0,85, gamma 0,10 | gamma = 0,10 | COCOK | S6 `meta` identik |
| - | 0,9142 / 0,91 | 0,9142 | TIDAK ADA | Tidak muncul di PDF maupun di S7 |
| - | 0,9825 | ROC-AUC 0,9825 | TIDAK ADA | |
| - | 0,71 (XGBoost) | Baseline 0,7100 | TIDAK ADA | |
| - | 94,12% | Presisi 94,12% | TIDAK ADA | |
| - | 89,4% masking | 89,40% | TIDAK ADA | |
| - | Rp 507.370.000 | Overcharge | TIDAK ADA | |
| - | Rp 841.100.000 | 60 klaim anomali | TIDAK ADA | |
| - | Rp 8.456.167 | Per kasus | TIDAK ADA | |
| - | Rp 3,53 Miliar | Total portofolio | TIDAK ADA | |
| - | 10.386 edge topologi | 10.386 | TIDAK ADA | PDF hanya menyebut 4563 edge fitur |

---

## 7. Rekomendasi

### 7.1 Boleh dipublikasikan apa adanya

| Angka | Bentuk penyajian yang aman |
|---|---|
| 300 klaim, KLM001-KLM300 | Angka faktual |
| Rp 3.526.650.000 total nominal | Angka faktual, sebut nominal, bukan "nilai" |
| 240 / 24 / 36 (auto_clear / review / escalate) | Angka faktual |
| Rp 2.685.550.000 / Rp 279.950.000 / Rp 561.150.000 per status | Angka faktual |
| 60 klaim anomali, Rp 841.100.000 | Angka faktual, dengan label "nominal klaim anomali" |
| 264 normal : 36 fraud, rasio 1 : 7,33 | Angka faktual |
| 9 sindikat, sebaran 3/3/6/2/2/4/4/6/6, Rp 539.650.000 | Angka faktual |
| 40 pasien, 20 dokter, 10 faskes | Angka faktual |
| Skor fraud mean 0,0862 / 0,5908 / 0,8689 | Angka faktual, dengan label "kolom label, bukan keluaran model" |
| 10.386 edge topologi (aturan `pipeline.py:273`) | Angka faktual bila disebut "implementasi pipeline produksi" |
| 2.192 edge fitur pada 300 klaim, theta=0,85 | Angka faktual |

### 7.2 Harus dihapus atau diberi label tegas

| Angka | Alasan | Tindakan |
|---|---|---|
| Rp 507.370.000 overcharge | Tidak ada formula yang menghasilkannya; dua komponen punya rasio berbeda | Hapus. Ganti dengan "Rp 841.100.000 nominal klaim anomali sebagai plafon atas yang perlu diverifikasi tarif per klaim" |
| Rp 394.950.000 dan Rp 112.420.000 | Keduanya tidak dapat ditelusuri | Hapus |
| Rp 8.456.167 per kasus | Turunan dari angka di atas | Hapus, atau tulis "Rp 14.018.333 per klaim anomali" sebagai angka faktual |
| "Akurasi 93,0%" sebagai metrik deteksi fraud | Asal: akurasi leksikon sentimen atas 200 uji simulasi | Ganti label menjadi "akurasi klasifikasi sentimen leksikon pada simulasi Oasis (200 uji)" |
| AUPRC 0,9142 / ROC-AUC 0,9825 / presisi 94,12% / FPR 10,6% / masking 89,4% | Tanpa artefak | Hapus atau turunkan ke "belum tervalidasi" sesuai `00-dashboard.md:46-52` |
| Baseline XGBoost 0,7100 dan "+28,6%" | Tanpa artefak | Hapus |
| Tabel perbandingan model di `data.ts:253-300` | Seluruhnya karangan | Ganti dengan placeholder, atau beri label "ilustrasi skenario, bukan hasil eksperimen" |
| "Rp 14,4 M / tahun" dan "Rp 1,2 M / bulan" | Tanpa artefak; berbasis 3 klaim | Hapus atau tulis "hipotesis penghematan yang belum dihitung" |
| "Rp 14.4 B / year" di `i18n.tsx:791` | Satuan salah 1000 kali terhadap versi Indonesia `i18n.tsx:443` | Perbaiki ke satuan yang sama setelah angka tunggal ditetapkan |
| "6.667 berkas" | PDF dan payload sama-sama menyebut angka ini, tetapi basisnya 100 klaim simulasi, bukan produksi | Ganti 6.667 dengan label "eksperimen 100 klaim" |
| "3,2x throughput" dan "SUS 82,5" | Tanpa simulasi beban kerja atau instrumen | Hapus |
| "4.563 edge fitur" di konteks dataset v2.1 | Milik eksperimen 100 klaim | Tulis "4.563 edge (eksperimen 100 klaim)"; untuk v2.1 gunakan 2.192 |
| "109 baris LOS hari kosong" | Salah baca; nilainya 0, bukan kosong | Ganti "109 baris bernilai 0" |
| "Rp 542.560.000" sindikat | Tidak ada di CSV (aktual Rp 539.650.000) | Ganti |
| "19 klaim RS_A" (aktual 29), "Rp 58 juta" untuk SYND-01 (aktual Rp 52.300.000), "LOS 3 hari" KLM001 (aktual 2) | Bertentangan dengan S2 | Ganti dengan nilai CSV |
| "100% mendeteksi 9 pola sindikat" | 9 sindikat ada, tetapi hit rate 100% adalah kebocoran | Tulis "9 sindikat teridentifikasi, 36 klaim escalate" tanpa klaim deteksi sempurna |
| "FRAUD TERDETEKSI 14/14 (100%)" | Kebocoran, bukan performa | Hapus dari materi publik |

### 7.3 Syarat minimum agar metrik model bisa diklaim

1. Lampirkan skrip evaluasi, vektor prediksi out-of-fold, label, dan skema split.
2. Gunakan definisi target tunggal (`is_fraud` atau `status`, dipilih satu dan ditulis di kamus data).
3. Pastikan tidak ada kolom forbidden masuk ke graph construction; `pipeline.py:293-309` harus dirombak agar A_sem tidak memakai `sindikat`.
4. Jalankan ulang notebook dan simpan outputnya sebagai artefak ter-versioning. Tanpa ini, `Aegis-JKN.ipynb` yang 0 output tidak dapat dipakai sebagai bukti apa pun.
5. Perbaiki ambang risiko agar tunggal di seluruh repo, dan tetapkan satu nilai (0,35/0,60/0,80 atau 0,40/0,65/0,85, bukan keduanya).

---

## 8. Daftar Berkas Bukti

Semua di `N:\HEALTHKATHON\analysis\reports\scripts\`:

| Skrip | Keluaran | Isi |
|---|---|---|
| `step1_schema.py` | (stdout) | Skema dua CSV |
| `step2_compare.py` | `out_compare.json` | Diff per-field dua CSV |
| `step3_stats.py` | `out_stats.json` | Hitungan inti 300 klaim |
| `step4_fraudsets.py` | `out_fraudsets.json` | Definisi himpunan fraud |
| `step5_subset.py` | `out_subset.json` | Pencarian subset-sum 507.370.000 |
| `step6_auprc.py` | `out_auprc.json` | AUPRC manual + sklearn, ambang, ROC-AUC |
| `step7_nb.py` | `nb_main_dump.json` | 22 sel notebook utama |
| `step9_embed.py` | `out_embed.json` | Dekode CSV tertanam di notebook |
| `step10_front.py` | `out_front.json` | Verifikasi hardcode frontend terhadap data |
| `step12_over.py` | `out_over.json` | Baterai rumus overcharge |
| `step14_decomp.py` | `out_decomp.json` | Upaya dekomposisi nominal |
| `step15_feat.py` | `out_feat.json` | Replikasi 34 fitur dan hitung edge |
| `step16_ref.py`, `step17_brute.py` | `out_ref.json`, `out_brute.json` | Brute force overcharge |
| `step18_circ.py` | `out_circ.json` | Sweep ambang fitur bersih dan crosstab modus |

Render PDF: `N:\HEALTHKATHON\analysis\reports\work22\21_pdf_pNN.png` (150 dpi) dan `lo_pNN.png` (100 dpi untuk p13-p16).
