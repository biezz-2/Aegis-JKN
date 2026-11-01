# Audit Bahasa, Terminologi, dan Ejaan Dokumen Aegis-JKN

**Lingkup:** 15 berkas `.md` di `N:\HEALTHKATHON\analysis\corpus\`
**Dasar aturan:** `00-dashboard.md` §7 "Standar Dokumen" (baris 74-85)
**Metode:** penghitungan dengan skrip Python (census karakter, tokenisasi, deteksi tabel tanpa baris pemisah Notion, pencocokan definisi singkatan, deteksi modalitas, metrik keterbacaan)
**Tanggal audit:** 22 Oktober 2026
**Bahasa laporan:** Bahasa Indonesia

---

## 1. Ringkasan Eksekutif

Korpus 15 dokumen berisi 62.131 kata, 2.387 kalimat, 535 baris tabel. Aturan em-dash dipenuhi **sempurna**: nol em-dash, nol en-dash, nol figure dash, nol horizontal bar, nol minus sign, dan nol double-hyphen dalam prosa. Pelanggaran terberat justru berada pada empat aturan lain: singkatan tanpa definisi, header dokumen yang tidak lengkap, tabel tanpa satuan/denominator, dan klaim "terbukti/tervalidasi" yang langsung bertentangan dengan `00-dashboard.md` §4.

Bukti utama: `11-archive-proposal.md` dan `12-archive-architecture.md` menyatakan angka-if benchmark sebagai "terbukti" dan "tervalidasi", sementara `00-dashboard.md:46-52` secara eksplisit mendaftar angka yang sama dalam daftar "Belum boleh disebut hasil tervalidasi". `04-evidence-matrix.md:87` bahkan melarang kata "terbukti" dan "tervalidasi" sebelum syarat bukti terpenuhi, dan `11-archive-proposal.md:15` mengklaim "Prinsip Anti-Overclaim" yang justru dilanggar oleh `11-archive-proposal.md:30`.

### Tabel severity

| Kategori | Temuan | Severitas | Dampak |
|---|---|---|---|
| Modalitas fakta vs rancangan | 41 kaproksimasi "terbukti/tervalidasi/dibuktikan" pada 2 dokumen arsip + 41 di `14-index.md`; 6 klaim eksplisit yang bertentangan langsung dengan `00-dashboard.md:46-52` | **Kritis** | Klaim publik yang Bertentangan dengan bukti |
| Klaim eksternal tanpa sitasi | 53 baris berskala nasional (2 juta klaim/hari, 1.000 verifikator, 175.774 klaim ACCH KPK, Rp25 miliar) tanpa URL/sumber primer | **Kritis** | Risiko reputasi dan kebocoran data |
| Tabel tanpa satuan/denominator | 41 dari 51 tabel numerik kekurangan satuan pada kolom hitungan; 43 dari 51 tanpa baris Total/denominator; 47 dari 51 punya salah satu | **Tinggi** | Angka tidak dapat diuji |
| Singkatan tanpa definisi | 113 pasangan (dokumen, singkatan) tidak terdefinisikan pada pemakaian pertama; 741 kemunculan | **Tinggi** | Pelanggaran §7 butir 1 |
| Header dokumen tidak lengkap | 8 dari 15 dokumen tidak memuat keempat field Status/Versi/Tanggal/Tujuan | **Tinggi** | Pelanggaran §7 butir 2 |
| Konsistensi istilah | 7 konsep dengan varian majemuk (auto_clear/auto-clear, escalate/eskalasi, review/telaah, purwarupa/prototipe/MVP, dll.) | **Sedang** | Sulit dicari dan dibandingkan |
| Duplikasi konten | 83 baris tabel duplikat di `09-draft-hub.md` (baris 17-113 diulang pada 220-325; sub-halaman kedua diberi label eksplisit "ARSIP SUMBER DUPLIKAT" pada baris 217); `09-draft-hub.md` memuat 212 baris yang menduplikasi `10-simulation-dataset.md` | **Sedang** | Risiko divergensi |
| Em-dash | 0 pelanggaran | **Lulus** | Sesuai §7 butir 8 |
| Bahasa(is) campuran | 449 "&", 58 "vs", 47 "→", kata Inggris tanpa padanan ("skor", "leakage", "ground truth", "overcharge") | **Sedang** | Gaya tidak seragam |
| Kekosongan dokumen | 14-index.md 30.391 kata = 48,9% korpus; 3 dokumen controlled tidak punya alasan | **Sedang** | Risiko aksesibilitas dokumen |

---

## 2. Tanda Panjang: Em-dash, En-dash, dan Double Hyphen

### 2.1 Hasil census karakter (semua 15 berkas)

| Karakter | Kode | Jumlah | Status |
|---|---|---|---|
| Em-dash | U+2014 | **0** | Lulus |
| En-dash | U+2013 | **0** | Lulus |
| Figure dash | U+2012 | **0** | Lulus |
| Horizontal bar | U+2015 | **0** | Lulus |
| Minus sign | U+2212 | **0** | Lulus |
| Double hyphen `--` | ASCII | 96 | Lulus (seluruhnya non-prosa) |

Klasifikasi 96 kemunculan `--` (hasil hitung ulang di seluruh korpus): 36 pada baris separator tabel Markdown (`12-archive-architecture.md:45`, `14-index.md:949`), 26 pada baris pagar tabel `| - | - |` (`11-archive-proposal.md:20`, `14-index.md:495`), 30 pada pagar YAML frontmatter (`11-archive-proposal.md:5`, `12-archive-architecture.md:8,20`, `14-index.md:7,15,23,31,480,912,924`), dan 4 di dalam URL Figma. **Tidak ada satu pun `--` dalam prosa.** Aturan §7 butir 8 terpenuhi 100%.

### 2.2 Masalah substitute: spasi-hyphen sebagai pengganti tanda pisah

Aturan em-dash dipenuhi secara formal, tetapi 21 lokasi prosa memakai spasi-hyphen (` - `) sebagai tanda pisah arteriaktif. Secara tipografis ini setara em-dash yang dihindari, sehingga intent aturan belum terpenuhi.

| File:baris | Kutipan | Perbaikan yang disarankan |
|---|---|---|
| `12-archive-architecture.md:31` | "...seluruh angka benchmark tersebut diberi label adaptasi literatur - berasal dari eksperimen MHGSL pada data asuransi kesehatan riil" | Ganti dengan koma atau titik dua |
| `12-archive-architecture.md:54` | "Tim belum memegang dataset klaim JKN riil - data peserta dan faskes dilarang digunakan tanpa izin resmi." | Titik dua |
| `12-archive-architecture.md:116` | "...angka estimasi literatur untuk simulasi/ROI - belum berbasis dataset riil JKN" | Titik dua |
| `12-archive-architecture.md:5` | "...risiko inefisiensi, khususnya anomali penagihan dan tindakan kecurangan terstruktur (fraud), yang pada akhirnya mengancam ketahanan finansial program JKN" | Koma |
| `12-archive-architecture.md:6` | "...merupakan ide yang tidak hanya sangat layak (feasible), tetapi juga memegang urgensi strategis yang fundamental" | Koma |
| `09-draft-hub.md:111` | "Sentimen negatif bukan otomatis fraud - klaim normal dengan keluhan layunan negatif..." | Titik dua |
| `10-simulation-dataset.md:108` | "Sentimen negatif bukan otomatis fraud - klaim normal..." | Titik dua |
| `11-archive-proposal.md:8` | "Diajukan Oleh:TIM INOVATOR KANDIDAT 1 - AEGIS-JKN" | Titik dua |
| `14-index.md:154`, `14-index.md:366`, `14-index.md:483` | Duplikat dari `09-draft-hub.md:111` dan `11-archive-proposal.md:8` | Ikuti perbaikan sumber |
| `09-draft-hub.md:6`, `10-simulation-dataset.md:3`, `14-index.md:49`, `14-index.md:261` | "100 klaim, privacy-by-design - bukan data peserta riil" | Titik dua |
| `09-draft-hub.md:114`, `10-simulation-dataset.md:11` | "## Ekspansi v2 - 300 Klaim, Kolom Alasan, dan Kesiapan ML/DL" | Titik dua |
| `08-training-protocol.md:17` | `| Prediksi selisih biaya verifikasi | FKTP nonkapitasi | PNK17 - PNK18 |` | Rentang: "PNK17 sampai PNK18" |

---

## 3. Audit Singkatan (Aturan §7 butir 1)

Singkatan diperiksa pada 29 token: MHGSL, XAI, SHAP, AUPRC, AUROC, ROC-AUC, SMOTE, LOS, ICD-10, ICD-9-CM, FORNAS, FEP, FKRTL, FHIR, PyG, XGBoost, MLP, RAG, LLM, SP2D, INA-CBG, DSP, DP-CTGAN, DPO, GNN, GCN, EMR, PWA, NLP.

**Total pasangan (dokumen, singkatan): 133. Tidak terdefinisikan pada pemakaian pertama: 113 (85%). Total kemunculan pada dokumen yang bermasalah: 741.**

Kasus per dokumen:

| File | Pasangan tak terdefinisi | Total pasangan | Singkatan bermasalah (pertama di baris) |
|---|---|---|---|
| `00-dashboard.md` | 3 | 3 | AUPRC (47), LOS (36), ROC-AUC (47) |
| `01-proposal.md` | 4 | 4 | AUPRC (70), ROC-AUC (49), SHAP (91), XGBoost (43) |
| `02-architecture.md` | 4 | 4 | AUPRC (74), ROC-AUC (74), SHAP (38), XGBoost (28) |
| `03-dataset-registry.md` | 4 | 4 | ICD-10 (54), ICD-9-CM (55), LOS (57), SHAP (67) |
| `04-evidence-matrix.md` | 4 | 4 | AUPRC (34), SHAP (39), XAI (39), XGBoost (50) |
| `05-decision-scope.md` | 0 | 0 | (tidak ada singkatan; paling bersih) |
| `06-research-notes.md` | 4 | 4 | AUPRC (42), MHGSL (42), SHAP (28), XGBoost (24) |
| `07-dataset-v2-catalog.md` | 2 | 2 | FKRTL (6), ICD-10 (3) |
| `08-training-protocol.md` | 5 | 5 | AUPRC (39), FKRTL (27), ICD-10 (12), LOS (25), SHAP (22) |
| `09-draft-hub.md` | 15 | 18 | AUPRC, AUROC, DP-CTGAN, FHIR, FKRTL, FORNAS, ICD-10, ICD-9-CM, LLM, MHGSL, MLP, NLP, PyG, SMOTE, XGBoost |
| `10-simulation-dataset.md` | 15 | 18 | (sama dengan `09-draft-hub.md`) |
| `11-archive-proposal.md` | 15 | 20 | AUPRC, EMR, FORNAS, GCN, GNN, ICD-10, ICD-9-CM, INA-CBG, MHGSL, NLP, PWA, PyG, ROC-AUC, SHAP, XAI |
| `12-archive-architecture.md` | 17 | 21 | AUROC, DP-CTGAN, DPO, FHIR, FKRTL, FORNAS, ICD-10, ICD-9-CM, LLM, MHGSL, MLP, NLP, PyG, SHAP, SMOTE, XAI, XGBoost |
| `13-archive-deep-research.md` | 1 | 1 | LLM (14) |
| `14-index.md` | 20 | 25 | AUPRC, AUROC, DP-CTGAN, DPO, EMR, FHIR, FKRTL, FORNAS, GCN, GNN, ICD-9-CM, LLM, MHGSL, MLP, NLP, PWA, PyG, ROC-AUC, SMOTE, XGBoost |

### 3.1 Tabel singkatan terparah (12 teratas, diurutkan jumlah kemunculan di dokumen bermasalah)

| Singkatan | Arti | Kemunculan di dokumen bermasalah | Dokumen yang mendefinisikan (tepat pada pemakaian pertama) | Dokumen yang TIDAK mendefinisikan | Lokasi pemakaian pertama (file:baris) |
|---|---|---|---|---|---|
| MHGSL | Multi-Hop Graph Structure Learning | 138 | **tidak ada** | 6: `06`, `09`, `10`, `11`, `12`, `14` | `06-research-notes.md:42`, `09-draft-hub.md:6`, `10-simulation-dataset.md:3`, `11-archive-proposal.md:6`, `12-archive-architecture.md:3`, `14-index.md:49` |
| XGBoost | Extreme Gradient Boosting | 86 | `11-archive-proposal.md:17` | 8: `01`, `02`, `04`, `06`, `09`, `10`, `12`, `14` | `01-proposal.md:43`, `02-architecture.md:28`, `04-evidence-matrix.md:50`, `06-research-notes.md:24`, `09-draft-hub.md:166`, `12-archive-architecture.md:25`, `14-index.md:209` |
| FKRTL | Fasilitas Kesehatan Rujukan Tingkat Lanjutan | 70 | `11-archive-proposal.md:22` | 6: `07`, `08`, `09`, `10`, `12`, `14` | `07-dataset-v2-catalog.md:6`, `08-training-protocol.md:27`, `09-draft-hub.md:9`, `10-simulation-dataset.md:6`, `12-archive-architecture.md:15`, `14-index.md:52` |
| AUPRC | Area Under the Precision-Recall Curve | 50 | `12-archive-architecture.md:30` | 10: `00`, `01`, `02`, `04`, `06`, `08`, `09`, `10`, `11`, `14` | `00-dashboard.md:47`, `01-proposal.md:70`, `02-architecture.md:74`, `04-evidence-matrix.md:34`, `06-research-notes.md:42`, `08-training-protocol.md:39`, `09-draft-hub.md:178`, `11-archive-proposal.md:15`, `14-index.md:221` |
| SHAP | SHapley Additive exPlanations | 40 | `09-draft-hub.md:113`, `10-simulation-dataset.md:110`, `14-index.md:156` (lewat nama kolom, bukan definisi) | 8: `01`, `02`, `03`, `04`, `06`, `08`, `11`, `12` | `01-proposal.md:91`, `02-architecture.md:38`, `03-dataset-registry.md:67`, `04-evidence-matrix.md:39`, `06-research-notes.md:28`, `08-training-protocol.md:22`, `11-archive-proposal.md:27`, `12-archive-architecture.md:3` |
| LLM | Large Language Model | 36 | `11-archive-proposal.md:178` | 5: `09`, `10`, `12`, `13`, `14` | `09-draft-hub.md:104`, `10-simulation-dataset.md:101`, `12-archive-architecture.md:51`, `13-archive-deep-research.md:14`, `14-index.md:14` |
| FHIR | Fast Healthcare Interoperability Resources | 34 | `11-archive-proposal.md:29` | 4: `09`, `10`, `12`, `14` | `09-draft-hub.md:14`, `10-simulation-dataset.md:11`, `12-archive-architecture.md:3`, `14-index.md:57` |
| ICD-10 | International Classification of Diseases, Revision 10 | 31 | `14-index.md:14` | 7: `03`, `07`, `08`, `09`, `10`, `11`, `12` | `03-dataset-registry.md:54`, `07-dataset-v2-catalog.md:3`, `08-training-protocol.md:12`, `09-draft-hub.md:14`, `11-archive-proposal.md:196`, `12-archive-architecture.md:17` |
| PyG | PyTorch Geometric | 27 | **tidak ada** | 5: `09`, `10`, `11`, `12`, `14` | `09-draft-hub.md:170`, `10-simulation-dataset.md:167`, `11-archive-proposal.md:355`, `12-archive-architecture.md:110`, `14-index.md:213` |
| MLP | Multi-Layer Perceptron | 23 | **tidak ada** | 4: `09`, `10`, `12`, `14` | `09-draft-hub.md:167`, `10-simulation-dataset.md:164`, `12-archive-architecture.md:109`, `14-index.md:210` |
| DP-CTGAN | Differential Privacy Conditional Table GAN | 23 | **tidak ada** | 4: `09`, `10`, `12`, `14` | `09-draft-hub.md:215`, `10-simulation-dataset.md:212`, `12-archive-architecture.md:48`, `14-index.md:258` |
| ICD-9-CM | International Classification of Diseases, Ninth Revision, Clinical Modification | 22 | **tidak ada** | 6: `03`, `09`, `10`, `11`, `12`, `14` | `03-dataset-registry.md:55`, `09-draft-hub.md:14`, `10-simulation-dataset.md:11`, `11-archive-proposal.md:196`, `12-archive-architecture.md:17`, `14-index.md:57` |

Empat singkatan **tidak pernah didefinisikan di dokumen mana pun** dan karena itu paling berisiko bagi pembaca: PyG (27 kemunculan), MLP (23), DP-CTGAN (23), ICD-9-CM (22). Delapan singkatan lain juga tanpa definisi sama sekali di seluruh korpus: FORNAS (20), ROC-AUC (16), NLP (14), AUROC (12), SMOTE (11), DPO (6), EMR (4), PWA (4).

Singkatan yang **tidak** bermasalah (terdefinisi dengan benar pada pemakaian pertama): `05-decision-scope.md` (0 singkatan), `11-archive-proposal.md` XGBoost@17, FKRTL@22, LOS@23, FHIR@29, LLM@178; `12-archive-architecture.md` INA-CBG@12, GNN@29, AUPRC@30, GCN@30; `09-draft-hub.md` XAI@171, `10-simulation-dataset.md` XAI@168, `14-index.md` XAI@214, ICD-10@14.

Tiga singkatan dalam daftar istilah yang **tidak muncul sama sekali** di korpus dan sebaiknya dihapus dari glosarium: FEP, RAG, SP2D, DSP.

---

## 4. Audit Header Dokumen (Aturan §7 butir 2)

Persyaratan: "Awali dengan status, versi, tanggal, dan tujuan."

| File | Status? | Versi? | Tanggal? | Tujuan? | Catatan |
|---|---|---|---|---|---|
| `00-dashboard.md` | Ya (`:4`) | Ya (`:6`) | Ya (`:5`) | **Tidak** | Tujuan hanya diuraikan di §1 baris 9, bukan di header |
| `01-proposal.md` | Ya (`:4`) | Ya (`:3`) | Ya (`:5`) | **Tidak** | Tujuan di §3 baris 22, bukan di header |
| `02-architecture.md` | Ya (`:4`) | Ya (`:3`) | Ya (`:5`) | Ya (`:7`) | Lengkap |
| `03-dataset-registry.md` | Ya (`:4`) | Ya (`:3`) | Ya (`:5`) | Ya (`:8`) | Lengkap |
| `04-evidence-matrix.md` | Ya (`:4`) | Ya (`:3`) | Ya (`:5`) | Ya (`:7`) | Lengkap |
| `05-decision-scope.md` | Ya (`:4`) | Ya (`:3`) | Ya (`:5`) | Ya (`:8`) | Lengkap |
| `06-research-notes.md` | Ya (`:4`) | Ya (`:3`) | Ya (`:5`) | Ya (`:6`) | Lengkap |
| `07-dataset-v2-catalog.md` | **Tidak** | **Tidak** | **Tidak** | **Tidak** | Header hanya prosa baris 3; tidak ada status/versi/tanggal |
| `08-training-protocol.md` | **Tidak** | **Tidak** | **Tidak** | Parsial | Header prosa baris 3; sumber Notion baris 4 |
| `09-draft-hub.md` | **Tidak** | Parsial (`:7` "CATATAN VERSI") | **Tidak** | **Tidak** | Baris 4-5 adalah heading Notion, bukan block header |
| `10-simulation-dataset.md` | **Tidak** | Parsial (`:4`) | **Tidak** | **Tidak** | Hanya callout emoji |
| `11-archive-proposal.md` | **Tidak** | Parsial (`:4` "CATATAN EDITORIAL") | **Tidak** | **Tidak** | Baris 3 judul menyatu tanpa spasi |
| `12-archive-architecture.md` | **Tidak** | **Tidak** | **Tidak** | **Tidak** | Hanya callout baris 3-4 |
| `13-archive-deep-research.md` | **Tidak** | **Tidak** | **Tidak** | **Tidak** | Baris 3 prosa kasar tanpa header |
| `14-index.md` | **Tidak** | Parsial | **Tidak** | **Tidak** | Callout baris 4-5 |

**8 dari 15 dokumen tidak memuat keempat field.** Yang paling parah adalah `12-archive-architecture.md` (dokumen yang memuat 17 singkatan tak terdefinisi dan 6 klaim "terbukti"), `13-archive-deep-research.md` (23 baris, tanpa header sama sekali), dan `07-dataset-v2-catalog.md` (katalog data tanpa status/tanggal).

---

## 5. Konsistensi Istilah (Aturan §7 butir 3)

Kasus sensitivitas tinggi: `02-architecture.md:64` menyatakan "Keduanya tidak boleh dipakai secara bergantian. Status kerja merupakan keputusan operasional, sedangkan label risiko merupakan anotasi atau output model." Varian di bawah melanggar perintah itu sendiri.

| Konsep | Varian yang dipakai (jumlah kemunculan) | Di dokumen mana | Terminologi kanonik yang disarankan |
|---|---|---|---|
| Status kerja auto-clear | `auto_clear` (8), `auto-clear` (12), `auto clear` (0) | `auto_clear`: `00-dashboard.md:32`, `03-dataset-registry.md:19,33,43`, `14-index.md:1152,1440,1454,1464`. `auto-clear`: `01-proposal.md:9,37,67`, `02-architecture.md:63`, `11-archive-proposal.md:204,338`, `14-index.md:679,813,1223,1251,1281,1369` | **`auto_clear`** (nilai data mentah, sama dengan nama field Notion) dengan label Indonesia "selesai otomatis". Jangan tulis `auto-clear` di teks formal. |
| Status kerja escalate | `escalate` (20), `eskalasi` (2) | `eskalasi`: `03-dataset-registry.md:43`, `14-index.md:1464`. `escalate`: `00-dashboard.md:34`, `01-proposal.md:9,37,69`, `02-architecture.md:63`, `03-dataset-registry.md:21,35,45,66`, `14-index.md` | **`escalate`** sebagai nilai data; teks naratif memakai "eskalasi". Tambahkan glosarium. |
| Status kerja review | `review` (44), `telaah` (46), `reviewer` (6), `verifikator` (137) | `reviewer`: `00-dashboard.md`, `02-architecture.md`, `08-training-protocol.md`, `14-index.md` (3). `review`: tersebar di 7 dokumen. `telaah`: tersebar di 9 dokumen | **`review`** sebagai nilai data; "telaah" hanya untuk aktivitas manusia; **`verifikator`** menggantikan `reviewer` (istilah ini sudah dominan di `11-archive-proposal.md` dan `14-index.md`). |
| Label risiko | `low` (83), `medium` (47), `high` (137), `fraud` (376), `normal` (48) versus `rendah` (30), `sedang` (50), `tinggi` (70) | `03-dataset-registry.md:39-42` menetapkan set label Inggris. `rendah`/`sedang`/`tinggi` muncul di `05-decision-scope.md`, `09-draft-hub.md:70-78` (kolom "Derajat" berhadapan dengan kolom "Risiko" berisi `high`/`low`/`fraud` dalam baris yang sama), `11-archive-proposal.md`, `12-archive-architecture.md:142`, `14-index.md` | **`low`/`medium`/`high`/`fraud`** untuk nilai data; `rendah`/`sedang`/`tinggi` untuk kalimat. Kasus `09-draft-hub.md:70-78` harus dibersihkan karena dua sistem label berada dalam satu tabel. |
| Fenomena fraud | `fraud` (376), `kecurangan` (60), `anomali` (141) | Semua dokumen. `11-archive-proposal.md` memuat ketiganya (fraud 37, anomali 39, kecurangan 32); `14-index.md` (fraud 216, anomali 81, kecurangan 51) | **"kecurangan"** dalam prosa Indonesia; `fraud` hanya sebagai nama label/field; `anomali` untuk sinyal statistik, bukan kasus terbukti. |
| Data simulasi | `sintetis` (146), `synthetic` (0), `mock` (0), `fake` (0) | Semua dokumen | **`sintetis`** (konsisten, tidak ada varian). Pertahankan. |
| Purwarupa | `purwarupa` (49), `prototipe` (4), `prototype` (0), `MVP` (53) | `prototipe`: `08-training-protocol.md:3,8` (2x) dan `14-index.md` (2x). `purwarupa`: 49x, `MVP`: 53x tersebar | **`purwarupa`** untuk produk/artefak; `MVP` hanya bila lingkup formalnya telah didefinisikan; buang `prototipe` di `08-training-protocol.md`. |
| Machine learning | `machine learning` (12), `ML` (35), `ML/DL` (10), `pembelajaran mesin` (0) | `machine learning`: `11-archive-proposal.md:138,157,178`, `12-archive-architecture.md:7`, `14-index.md`. `ML/DL`: `09-draft-hub.md:114,154,172,213` dan duplikatnya | **"pembelajaran mesin"** pada teks naratif; `ML`/`DL` pada nama komponen teknis saja (mis. "Baseline ML & DL"). |
| Graf | `graph learning` (10), `graph neural network` (4), `GNN` (22), `GCN` (22), `pembelajaran graf` (2) | `graph learning`: `00-dashboard.md:55`, `01-proposal.md:10`, `04-evidence-matrix.md:51`, `05-decision-scope.md:71`. `GNN`/`GCN`: `11-archive-proposal.md:26,138,144,158,173,181,316`, `12-archive-architecture.md:29,30` | **"pembelajaran graf"** untuk konsep; `GNN`/`GCN` tetap sebagai nama teknik. |
| Explainable AI | `XAI` (42), `Explainable AI` (22), `explainability` (2) | `04-evidence-matrix.md:39`, `11-archive-proposal.md:27`, `12-archive-architecture.md:3`, `14-index.md`. `explainability`: `00-dashboard.md`, `14-index.md` | **`Explainable AI (XAI)`** pada kemunculan pertama per dokumen, lalu `XAI`. Buang `explainability` sebagai kata benda. |
| Overcharge | `overcharge` (18), `selisih biaya verifikasi` (1) | `00-dashboard.md:39,50`, `03-dataset-registry.md:37`, `11-archive-proposal.md:346,348`, `14-index.md` | **"selisih tarif yang tidak sah"** atau **"overcharge"**; pilih satu dan konsisten. |
| Leakage | `leakage` (82), `kebocoran data` (0) | Semua dokumen; `12-archive-architecture.md:46,47` (16x) | **`kebocoran label`** untuk prosa; `leakage` untuk nama file/rule (`leakage.yaml`). |
| Data set | `dataset` (107), `data set` (0) | Semua dokumen | **"data set"** (KBBI) pada teks naratif; `dataset` dipertahankan hanya bila merupakan nama variabel kode atau nama entri database. |
| Biaya vs nominal | `biaya` (139), `nominal` (32) | `00-dashboard.md:35` ("Total nominal klaim sintetis"), `03-dataset-registry.md:32-37`, `11-archive-proposal.md:343` | **"nominal klaim"** untuk nilai rupiah pada tabel; "biaya" untuk konsep. Saat ini tertukar. |

---

## 6. Pemisahan Fakta, Rancangan, Hipotesis, Hasil Uji, dan Estimasi (Aturan §7 butir 4)

### 6.1 Kontradiksi langsung dengan `00-dashboard.md` §4

`00-dashboard.md:46-52` mendaftar lima kelompok angka yang "Belum boleh disebut hasil tervalidasi". Pengaudit menemukan keenamnya diklaim sebagai fakta di dokumen arsip:

| # | File:baris | Kutipan | Angka yang Dilarang | Kontradiksi dengan |
|---|---|---|---|---|
| 1 | `11-archive-proposal.md:30` | "Evaluasi empiris terhadap portofolio 300 berkas klaim tervalidasi klinis ... **membuktikan performa superior model MHGSL**: Akurasi 93.0%, Presisi 94.12%, ROC-AUC 0.9825, dan AUPRC 0.9142 (+28.6% dibanding baseline XGBoost 0.71)" | 93,0% / 94,12% / 0,9825 / 0,9142 | `00-dashboard.md:47` |
| 2 | `11-archive-proposal.md:326-330` | Tabel metrik: "93.00% (Tervalidasi)", "94.12% (Tervalidasi)", "0.9825 (Tervalidasi)", "89.40% (Tervalidasi)" | Akurasi, presisi, ROC-AUC, ketahanan masking | `00-dashboard.md:47-48` |
| 3 | `11-archive-proposal.md:348` | "sistem **berhasil mendeteksi** potensi kebocoran tarif (overcharge) sebesar Rp 507.370.000 (60.32% dari nominal klaim anomali ...)" | Penghematan/penyelamatan finansial | `00-dashboard.md:50` |
| 4 | `11-archive-proposal.md:346` | "Rp 394.950.000 (**Overcharge Terbukti**)" | Overcharge | `00-dashboard.md:50` + `04-evidence-matrix.md:87` |
| 5 | `11-archive-proposal.md:402` | "Rasio Cost-to-Impact **terbukti** ≥ 1 : 15" | Penghematan | `00-dashboard.md:50` |
| 6 | `12-archive-architecture.md:30` | "Arsitektur ini **terbukti mendominasi AUPRC** (Area Under the Precision-Recall Curve) hingga +20% dibandingkan baseline" | AUPRC 0,9142 dan selisih +20% vs +28,6% | `00-dashboard.md:47` + `04-evidence-matrix.md:34` |
| 7 | `11-archive-proposal.md:338` | "Pengujian komparatif **membuktikan keunggulan mutlak** arsitektur MHGSL ... MHGSL mencapai AUPRC 0.9142 (peningkatan +28.6%)" | AUPRC | `00-dashboard.md:47` |
| 8 | `11-archive-proposal.md:410` | "300 klaim tervalidasi klinis yang **telah membuktikan** kemampuan menyelamatkan lebih dari setengah miliar rupiah" | Penghematan | `00-dashboard.md:50` |

### 6.2 Pelanggaran oleh dokumen yang sama yang menginxkankan aturan

| File:baris | Kutipan | Masalah |
|---|---|---|
| `11-archive-proposal.md:15` | "Prinsip Anti-Overclaim & Transparansi Sains: Kami **menolak** klaim akurasi mutlak 100% dan **tidak menyajikan** angka penghematan anggaran yang spekulatif" | Dokumen yang sama menyajikan Akurasi 93,0% sebagai "Tervalidasi" (`:326`) dan penghematan Rp507.370.000 sebagai "Penyelamatan Riil" (`:347`) |
| `04-evidence-matrix.md:87` | "Hindari kata 'terbukti', 'riil', 'akurat secara superior', dan 'tervalidasi' sebelum syarat bukti dipenuhi" | Larangan dilanggar oleh `11-archive-proposal.md:30,142,143,320,326-333,342,346,348,402,410` dan `12-archive-architecture.md:5,6,30,115` |
| `04-evidence-matrix.md:34` (E-07) | "Benchmark Aegis-JKN: AUPRC 0,9142, **Belum tereproduksi pada audit ini**" | `11-archive-proposal.md:338` menyatakan "terbukti" atas angka yang sama |
| `04-evidence-matrix.md:37` (E-10) | "Klaim waktu telaah berkurang 45 persen, **Belum dibuktikan dengan artefak yang tersedia" | `11-archive-proposal.md:350` menyatakan SUS 82,5 dan throughput 3,2x sebagai hasil |
| `00-dashboard.md:39` | "perhitungan estimasi overcharge Rp507.370.000 **belum dapat direproduksi per klaim** ... tarif pembanding, formula, dan status validasi independen belum tercatat" | `11-archive-proposal.md:346,348` menyebut "Rp 394.950.000 (Overcharge Terbukti)" dan "rata-rata kerugian Rp 8.456.167 per kasus" |
| `11-archive-proposal.md:4` | "Angka benchmark dan finansial pada naskah sumber **belum dianggap tervalidasi** sampai artefak replikasi dilampirkan" | `:30`, `:320` ("Dataset Sintetis v2.1 Tervalidasi"), `:326-333` |
| `12-archive-architecture.md:5` | "...**terbukti mampu** memberikan nilai penghematan ekonomi yang nyata" | Klaim EXISTS tanpa bukti |
| `12-archive-architecture.md:115` | "Jenama Aegis-JKN (**tervalidasi oleh purwarupa**)" | "tervalidasi" untuk branding, bukan bukti |
| `12-archive-architecture.md:127` | "Desain Aegis-JKN **sudah 85% sempurna**, tetapi 10 kekurangan kritis ... harus diperbaiki" | Angka "85% sempurna" tanpa definisi atau dasar pengukuran |
| `09-draft-hub.md:119`, `10-simulation-dataset.md:116`, `14-index.md:162` | "✅ Perubahan yang Sudah Diimplementasikan di v2.1" | Status implementasi diklaim sebelum artefak kode tersedia |
| `09-draft-hub.md:209`, `10-simulation-dataset.md:206` | "⚠️ DESAIN BELUM TERBUKTI UNGGUL (fallback ke XGBoost + fitur graf turunan)" | Menyatakan "belum terbukti unggul" di dokumen yang lain menyatakan "terbukti unggul" |

### 6.3 Modalitas yang tercampur dalam satu dokumen

| File | Kata "simulasi" | "estimasi" | "target" | "tervalidasi" | "terbukti" | "hipotesis" |
|---|---|---|---|---|---|---|
| `11-archive-proposal.md` | 12 | 8 | 6 | 14 | 5 | 1 |
| `12-archive-architecture.md` | 9 | 5 | 4 | 3 | 2 | 1 |
| `14-index.md` | 73 | 40 | 43 | 41 | 9 | 13 |
| `00-dashboard.md` (controlled) | 6 | 4 | 2 | 4 (semua negatif) | 0 | 0 |

---

## 7. Audit Satuan dan Denominator Tabel (Aturan §7 butir 5)

Metode: 51 tabel dengan ≥1 kolom numerik terdeteksi. Ekspor Notion tidak memancarkan baris `|---|`, sehingga baris `|` berurutan diperlakukan sebagai satu tabel. Klasifikasi:

- **Kekurangan satuan:** kolom numerik yang header-nya tidak menyebut satuan dan sel-selnya tidak membawa satuan inline (contoh kolom `Jumlah`, `Kosong`, `Umur`, `Skor Maks`, `Tempat Tidur`, `Jumlah variabel`).
- **Kekurangan denominator:** tabel tanpa baris `Total` atau penanda dasar yang setara. Sel `Total nominal klaim sintetis` pada `00-dashboard.md:35` dan `14-index.md:1155` adalah baris KPI, bukan baris total tabel, dan karena itu tidak dihitung sebagai denominator.

**Hasil hitung ulang: 41 dari 51 tabel (80%) kekurangan satuan pada kolom hitungan. 43 dari 51 tabel (84%) tidak punya baris Total/denominator. 37 tabel mengalami keduanya, 4 tabel hanya kehilangan satuan, 6 tabel hanya kehilangan denominator, dan 4 tabel sudah aman. Total 47 dari 51 tabel (92%) punya setidaknya satu masalah.**

| File | Baris | Header tabel | Masalah satuan | Masalah denominator |
|---|---|---|---|---|
| `00-dashboard.md` | 29 | Indikator \| Hasil pemeriksaan baca saja | kolom **Hasil pemeriksaan baca saja**: 3/9 sel tanpa satuan (contoh 240, 24, 36) | **tidak ada baris Total/denominator** |
| `03-dataset-registry.md` | 11 | Versi \| Jumlah data \| Tujuan \| Ketentuan | kolom **Jumlah data**: 1/3 sel tanpa satuan (contoh Belum ditetapkan) | **tidak ada baris Total/denominator** |
| `03-dataset-registry.md` | 18 | Status \| Jumlah \| Persentase | kolom **Jumlah**: 4/4 sel tanpa satuan (contoh 240, 24, 36) | baris Total ada |
| `03-dataset-registry.md` | 24 | Label risiko \| Jumlah \| Persentase | kolom **Jumlah**: 5/5 sel tanpa satuan (contoh 240, 10, 14) | baris Total ada |
| `03-dataset-registry.md` | 32 | Status \| Nominal klaim | tidak ada (satuan sudah dinyatakan di header) | baris Total ada |
| `04-evidence-matrix.md` | 11 | Dimensi \| Kategori \| Jumlah | kolom **Jumlah**: 6/6 sel tanpa satuan (contoh 18, 11, 4) | **tidak ada baris Total/denominator** |
| `07-dataset-v2-catalog.md` | 8 | ID \| File sumber \| Baris / isi \| Dimensi \| Peran \| Catatan utama | tidak ada (satuan sudah dinyatakan di header) | **tidak ada baris Total/denominator** |
| `07-dataset-v2-catalog.md` | 17 | Variabel \| Label sumber \| Tipe hasil baca \| Kosong | kolom **Kosong**: 18/18 sel tanpa satuan (contoh 0, 0, 0) | **tidak ada baris Total/denominator** |
| `07-dataset-v2-catalog.md` | 43 | Variabel \| Label sumber \| Tipe hasil baca \| Kosong \| Catatan | kolom **Kosong**: 21/21 sel tanpa satuan (contoh 0, 0, 0) | **tidak ada baris Total/denominator** |
| `07-dataset-v2-catalog.md` | 66 | File referensi \| Sheet atau lingkup \| Jumlah baris \| Isu yang ditemukan | tidak ada (satuan sudah dinyatakan di header) | **tidak ada baris Total/denominator** |
| `07-dataset-v2-catalog.md` | 72 | Sheet sumber metadata \| Jumlah variabel \| Keterangan | kolom **Jumlah variabel**: 4/4 sel tanpa satuan (contoh 18, 26, 55) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 24 | ID \| Nama \| Kota \| Kepemilikan \| Kelas \| Tempat Tidur \| Jumlah Klaim \| Skor Maks  | kolom **Tempat Tidur**: 6/6 sel tanpa satuan (contoh 412, 280, 350); kolom **Skor Maks**: 6/6 sel tanpa satuan (contoh 0.95, 0.87, 0.94) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 32 | ID \| Nama \| Spesialisasi \| Faskes \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 12/12 sel tanpa satuan (contoh 0.94, 0.95, 0.74) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 46 | ID \| Nama \| Umur \| Gender \| Kelas Rawat \| Segmen \| Kota \| Jumlah Klaim \| Skor Ma | kolom **Umur**: 20/20 sel tanpa satuan (contoh 58, 63, 55); kolom **Kelas Rawat**: 20/20 sel tanpa satuan (contoh 2, 2, 1); kolom **Skor Maks**: 20/20 sel tanpa satuan (contoh 0.94, 0.95, 0.93) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 68 | Kode \| Nama \| Derajat \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0.79, 0.13) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 80 | Kode \| Nama \| Kompleksitas \| Biaya Rujukan \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0, 0.79) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 236 | ID \| Nama \| Kota \| Kepemilikan \| Kelas \| Tempat Tidur \| Jumlah Klaim \| Skor Maks  | kolom **Tempat Tidur**: 6/6 sel tanpa satuan (contoh 412, 280, 350); kolom **Skor Maks**: 6/6 sel tanpa satuan (contoh 0.95, 0.87, 0.94) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 244 | ID \| Nama \| Spesialisasi \| Faskes \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 12/12 sel tanpa satuan (contoh 0.94, 0.95, 0.74) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 258 | ID \| Nama \| Umur \| Gender \| Kelas Rawat \| Segmen \| Kota \| Jumlah Klaim \| Skor Ma | kolom **Umur**: 20/20 sel tanpa satuan (contoh 58, 63, 55); kolom **Kelas Rawat**: 20/20 sel tanpa satuan (contoh 2, 2, 1); kolom **Skor Maks**: 20/20 sel tanpa satuan (contoh 0.94, 0.95, 0.93) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 280 | Kode \| Nama \| Derajat \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0.79, 0.13) | **tidak ada baris Total/denominator** |
| `09-draft-hub.md` | 292 | Kode \| Nama \| Kompleksitas \| Biaya Rujukan \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0, 0.79) | **tidak ada baris Total/denominator** |
| `10-simulation-dataset.md` | 21 | ID \| Nama \| Kota \| Kepemilikan \| Kelas \| Tempat Tidur \| Jumlah Klaim \| Skor Maks  | kolom **Tempat Tidur**: 6/6 sel tanpa satuan (contoh 412, 280, 350); kolom **Skor Maks**: 6/6 sel tanpa satuan (contoh 0.95, 0.87, 0.94) | **tidak ada baris Total/denominator** |
| `10-simulation-dataset.md` | 29 | ID \| Nama \| Spesialisasi \| Faskes \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 12/12 sel tanpa satuan (contoh 0.94, 0.95, 0.74) | **tidak ada baris Total/denominator** |
| `10-simulation-dataset.md` | 43 | ID \| Nama \| Umur \| Gender \| Kelas Rawat \| Segmen \| Kota \| Jumlah Klaim \| Skor Ma | kolom **Umur**: 20/20 sel tanpa satuan (contoh 58, 63, 55); kolom **Kelas Rawat**: 20/20 sel tanpa satuan (contoh 2, 2, 1); kolom **Skor Maks**: 20/20 sel tanpa satuan (contoh 0.94, 0.95, 0.93) | **tidak ada baris Total/denominator** |
| `10-simulation-dataset.md` | 65 | Kode \| Nama \| Derajat \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0.79, 0.13) | **tidak ada baris Total/denominator** |
| `10-simulation-dataset.md` | 77 | Kode \| Nama \| Kompleksitas \| Biaya Rujukan \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0, 0.79) | **tidak ada baris Total/denominator** |
| `11-archive-proposal.md` | 343 | Kategori Portofolio Klaim \| Jumlah Berkas \| Persentase Berkas \| Total Nominal Klaim \ | tidak ada (satuan sudah dinyatakan di header) | baris Total ada |
| `11-archive-proposal.md` | 375 | No \| Identifikasi Risiko \| Potensi Dampak \| Tingkat \| Strategi Mitigasi Preventif &  | tidak ada (satuan sudah dinyatakan di header) | **tidak ada baris Total/denominator** |
| `14-index.md` | 67 | ID \| Nama \| Kota \| Kepemilikan \| Kelas \| Tempat Tidur \| Jumlah Klaim \| Skor Maks  | kolom **Tempat Tidur**: 6/6 sel tanpa satuan (contoh 412, 280, 350); kolom **Skor Maks**: 6/6 sel tanpa satuan (contoh 0.95, 0.87, 0.94) | **tidak ada baris Total/denominator** |
| `14-index.md` | 75 | ID \| Nama \| Spesialisasi \| Faskes \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 12/12 sel tanpa satuan (contoh 0.94, 0.95, 0.74) | **tidak ada baris Total/denominator** |
| `14-index.md` | 89 | ID \| Nama \| Umur \| Gender \| Kelas Rawat \| Segmen \| Kota \| Jumlah Klaim \| Skor Ma | kolom **Umur**: 20/20 sel tanpa satuan (contoh 58, 63, 55); kolom **Kelas Rawat**: 20/20 sel tanpa satuan (contoh 2, 2, 1); kolom **Skor Maks**: 20/20 sel tanpa satuan (contoh 0.94, 0.95, 0.93) | **tidak ada baris Total/denominator** |
| `14-index.md` | 111 | Kode \| Nama \| Derajat \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0.79, 0.13) | **tidak ada baris Total/denominator** |
| `14-index.md` | 123 | Kode \| Nama \| Kompleksitas \| Biaya Rujukan \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0, 0.79) | **tidak ada baris Total/denominator** |
| `14-index.md` | 279 | ID \| Nama \| Kota \| Kepemilikan \| Kelas \| Tempat Tidur \| Jumlah Klaim \| Skor Maks  | kolom **Tempat Tidur**: 6/6 sel tanpa satuan (contoh 412, 280, 350); kolom **Skor Maks**: 6/6 sel tanpa satuan (contoh 0.95, 0.87, 0.94) | **tidak ada baris Total/denominator** |
| `14-index.md` | 287 | ID \| Nama \| Spesialisasi \| Faskes \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 12/12 sel tanpa satuan (contoh 0.94, 0.95, 0.74) | **tidak ada baris Total/denominator** |
| `14-index.md` | 301 | ID \| Nama \| Umur \| Gender \| Kelas Rawat \| Segmen \| Kota \| Jumlah Klaim \| Skor Ma | kolom **Umur**: 20/20 sel tanpa satuan (contoh 58, 63, 55); kolom **Kelas Rawat**: 20/20 sel tanpa satuan (contoh 2, 2, 1); kolom **Skor Maks**: 20/20 sel tanpa satuan (contoh 0.94, 0.95, 0.93) | **tidak ada baris Total/denominator** |
| `14-index.md` | 323 | Kode \| Nama \| Derajat \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0.79, 0.13) | **tidak ada baris Total/denominator** |
| `14-index.md` | 335 | Kode \| Nama \| Kompleksitas \| Biaya Rujukan \| Jumlah Klaim \| Skor Maks \| Risiko | kolom **Skor Maks**: 10/10 sel tanpa satuan (contoh 0.95, 0, 0.79) | **tidak ada baris Total/denominator** |
| `14-index.md` | 818 | Kategori Portofolio Klaim \| Jumlah Berkas \| Persentase Berkas \| Total Nominal Klaim \ | tidak ada (satuan sudah dinyatakan di header) | baris Total ada |
| `14-index.md` | 850 | No \| Identifikasi Risiko \| Potensi Dampak \| Tingkat \| Strategi Mitigasi Preventif &  | tidak ada (satuan sudah dinyatakan di header) | **tidak ada baris Total/denominator** |
| `14-index.md` | 1149 | Indikator \| Hasil pemeriksaan baca saja | kolom **Hasil pemeriksaan baca saja**: 3/9 sel tanpa satuan (contoh 240, 24, 36) | **tidak ada baris Total/denominator** |
| `14-index.md` | 1432 | Versi \| Jumlah data \| Tujuan \| Ketentuan | kolom **Jumlah data**: 1/3 sel tanpa satuan (contoh Belum ditetapkan) | **tidak ada baris Total/denominator** |
| `14-index.md` | 1439 | Status \| Jumlah \| Persentase | kolom **Jumlah**: 4/4 sel tanpa satuan (contoh 240, 24, 36) | baris Total ada |
| `14-index.md` | 1445 | Label risiko \| Jumlah \| Persentase | kolom **Jumlah**: 5/5 sel tanpa satuan (contoh 240, 10, 14) | baris Total ada |
| `14-index.md` | 1453 | Status \| Nominal klaim | tidak ada (satuan sudah dinyatakan di header) | baris Total ada |
| `14-index.md` | 1542 | Dimensi \| Kategori \| Jumlah | kolom **Jumlah**: 6/6 sel tanpa satuan (contoh 18, 11, 4) | **tidak ada baris Total/denominator** |
| `14-index.md` | 1773 | ID \| File sumber \| Baris / isi \| Dimensi \| Peran \| Catatan utama | tidak ada (satuan sudah dinyatakan di header) | **tidak ada baris Total/denominator** |
| `14-index.md` | 1782 | Variabel \| Label sumber \| Tipe hasil baca \| Kosong | kolom **Kosong**: 18/18 sel tanpa satuan (contoh 0, 0, 0) | **tidak ada baris Total/denominator** |
| `14-index.md` | 1808 | Variabel \| Label sumber \| Tipe hasil baca \| Kosong \| Catatan | kolom **Kosong**: 21/21 sel tanpa satuan (contoh 0, 0, 0) | **tidak ada baris Total/denominator** |
| `14-index.md` | 1831 | File referensi \| Sheet atau lingkup \| Jumlah baris \| Isu yang ditemukan | tidak ada (satuan sudah dinyatakan di header) | **tidak ada baris Total/denominator** |
| `14-index.md` | 1837 | Sheet sumber metadata \| Jumlah variabel \| Keterangan | kolom **Jumlah variabel**: 4/4 sel tanpa satuan (contoh 18, 26, 55) | **tidak ada baris Total/denominator** |

**Tabel yang lolos audit (4 dari 51):** `03-dataset-registry.md:32`, `11-archive-proposal.md:343`, `14-index.md:818`, `14-index.md:1453`.

**Tabel di luar deteksi otomatis yang tetap bermasalah:** `12-archive-architecture.md:179` (Metrik & Protokol Validasi v2.1) memuat ambang "≥90% fraud terdeteksi (antrian ≤20%)" tanpa menyebut denominator 36 klaim fraud, dan baris "AUPRC & AUROC MHGSL ≥ baseline" tanpa nilai absolut maupun selisih. Tabel ini tidak masuk hitungan 51 karena kolomnya tidak dominan numerik.

**Tabel berformat blockquote:** `12-archive-architecture.md:44` dan `14-index.md:948` (Masalah | Risiko | Solusi di v2.1) tidak tertangkap deteksi baris `|` biasa dan tidak memuat kolom numerik.

**Catatan rekonsiliasi:** `07-dataset-v2-catalog.md:66` menjumlahkan 1.859 + 1.552 + 1.979 + 1.030 = 6.420 baris, sedangkan `07-dataset-v2-catalog.md:6` menyebut total 6.514.039 baris. Tabel 1 di `:8` memuat 143.496 + 6.362.523 + 8.020 = 6.514.039 baris. Selisih 94.619 baris antara Tabel 1 dan Tabel 5 perlu rekonsiliasi.

---

## 8. Klaim Eksternal Tanpa Sitasi Spesifik (Aturan §7 butir 6)

Pola yang dicari: baris yang memuat angka berskala nasional atau eksternal, tanpa URL dan tanpa nama sumber primer. Ditemukan **53 baris unik** (file:baris) di seluruh korpus, tersebar di 9 berkas. Ke-27 baris di `14-index.md` adalah duplikat dari dokumen sumber, sehingga ada **26 baris unik di luar `14-index.md`**.

Sebagian besar baris ini bukan angka yang berasal dari luar, melainkan pengulangan angka nasional yang sama (2 juta klaim/hari, 270 juta jiwa, 1.000 verifikator) di 14 titik berbeda pada `11-archive-proposal.md` dan 5 titik pada `12-archive-architecture.md`. Karena itu, satu sitasi primer yang benar (URL, tanggal, nomor tabel) dapat menutup seluruh 19 baris itu sekaligus.

### 8.1 Sebaran per berkas

| Berkas | Jumlah baris | Nomor baris |
|---|---|---|
| `11-archive-proposal.md` | 14 | 17, 22, 127, 128, 140, 155, 162, 188, 189, 348, 372, 378, 401, 408 |
| `12-archive-architecture.md` | 5 | 5, 98, 103, 116, 181 |
| `14-index.md` | 27 | duplikat dari 9, 10, 11, 12 |
| `09-draft-hub.md` | 2 | 202, 414 |
| `01-proposal.md` | 1 | 14 |
| `04-evidence-matrix.md` | 1 | 30 |
| `06-research-notes.md` | 1 | 38 |
| `10-simulation-dataset.md` | 1 | 199 |
| `13-archive-deep-research.md` | 1 | 3 |
| **Total** | **53** | |

### 8.2 Klaim yang paling merusak kredibilitas (12 teratas)

| # | File:baris | Klaim eksternal | Sumber yang seharusnya ada |
|---|---|---|---|
| 1 | `13-archive-deep-research.md:3` | "Kasus yang di report oleh BPJS tahun 2024 melibatkan 3 rumah sakit swasta di jawa tengah dan sumatra utara dengan total kerugian mencapat RP25 miliar." | Laporan BPK/ACCH KPK 2024 dengan nomor kasus dan URL. Tidak ada. Ejaan juga salah: "di report" (harusnya "dilaporkan"), "RP25" (harusnya "Rp25 miliar"), "jawa tengah dan sumatra utara" (nama wilayah harus kapital). |
| 2 | `11-archive-proposal.md:22` | "lebih dari 270 juta jiwa kepesertaan aktif dan memproses lebih dari dua juta klaim ... hanya sekitar 1.000 verifikator ... kapasitas telaah 50-70 berkas per hari" | Statistik resmi BPJS Kemenkes. Tidak ada URL. |
| 3 | `11-archive-proposal.md:128` | "memproses rata-rata lebih dari dua juta lembar klaim ... didukung oleh sekitar 1.000 tenaga verifikator manusia" | Sama; tanpa sitasi |
| 4 | `11-archive-proposal.md:155` | "Volume klaim harian mencapai >2.000.000 berkas, sementara jumlah verifikator hanya ~1.000 orang" | Sama; tabel yang mengoleksi angka nasional tanpa sumber |
| 5 | `11-archive-proposal.md:162` | "Keterbatasan kapasitas verifikator (~1.000 orang untuk 2 juta klaim/hari)" | Sama |
| 6 | `11-archive-proposal.md:188` | "Jangan pernah memaksakan seluruh beban 2 juta klaim harian ke dalam inferensi model graf yang berat" | Angka yang sama tanpa sumber |
| 7 | `11-archive-proposal.md:189` | "pada volume transaksi BPJS Kesehatan (>2.000.000 klaim/hari)" | Sama |
| 8 | `11-archive-proposal.md:408` | "sistem ini dirancang siap menangani beban transaksi riil lebih dari dua juta klaim per hari" | Sama |
| 9 | `12-archive-architecture.md:5` | "sistem infrastruktur teknologi informasi BPJS Kesehatan harus memproses lebih dari dua juta klaim layanan kesehatan setiap harinya ... verifikasi hanya didukung oleh sekitar 1.000 petugas verifikator" | Sama; tanpa URL |
| 10 | `12-archive-architecture.md:116` | "ACCH KPK mencatat 175.774 klaim FKRTL berpotensi fraud hingga Juni 2015" | ACCH KPK 2015, seharusnya ada URL. Menariknya `12-archive-architecture.md:30-31` justru memakai URL Heliyon/Scientific Reports untuk klaim algoritma, sehingga inkonsistensi sitasi terlihat jelas. |
| 11 | `12-archive-architecture.md:103` | "Gemini 1.5 Flash ... berbiaya rendah ($0.10-$1.50 per 1M token input) ... Gemini 1.5 Pro ($2.00 per 1M token)" | Halaman tarif resmi Google AI Studio. Tidak ada URL. |
| 12 | `14-index.md:11-12`, `:39` | "Temuan KPK dan BPJS sering menyoroti lonjakan drastis pada tagihan klaim penyakit kronis ...", "kebocoran dana hingga **triliunan** rupiah", "Potensi Efisiensi DJS \| Sangat Tinggi (**Triliunan**)" | Angka orde-besaran tanpa sumber dan tanpa tahun. "sering menyoroti" adalah klaim frekuensi tanpa satu pun kasus bernama. |

### 8.3 Klaim yang sudah ditandai dengan benar oleh dokumen controlled (bukan pelanggaran)

| File:baris | Isi | Penilaian |
|---|---|---|
| `01-proposal.md:14` | "Angka nasional terkait volume klaim, jumlah verifikator, nilai kerugian, dan prevalensi fraud harus didukung rujukan primer yang spesifik sebelum digunakan sebagai fakta dalam versi final publikasi." | Pernyataan normatif yang benar, tetapi justru membuktikan bahwa aturan ini sudah seharusnya namun dilanggar oleh `11-archive-proposal.md` dan `12-archive-architecture.md`. |
| `04-evidence-matrix.md:30` (E-03) | "Volume klaim nasional per hari \| Sebagian terverifikasi" | Status parsial, tetapi tidak disertai sumber mana yang sudah terverifikasi. |
| `06-research-notes.md:38` | "Volume klaim harian nasional \| Perlu validasi spesifik" | Masih terbuka tanpa sumber. |

**Pola kontradiktif yang harus dicatat:** `12-archive-architecture.md:30-31` memakai URL academic (Heliyon 2024, Scientific Reports 2025) untuk klaim algoritma, tetapi `:5`, `:103`, `:116` yang memuat angka nasional justru tanpa sumber. `14-index.md:474` memuat tautan Figma sebagai bukti, sementara `:11-12` tidak.

---

## 9. Gaya Bahasa dan Tanda Baca Lainnya

### 9.1 Kalimat berbau "AI" / kata pengisi

Hanya 3 lokasi (murni, tanpa duplikasi di `14-index.md`):

| File:baris | Kutipan | Perbaikan |
|---|---|---|
| `12-archive-architecture.md:5` | "...yang **pada akhirnya** mengancam ketahanan finansial program JKN secara keseluruhan." | Hapus; tulis "dan mengancam ..." |
| `12-archive-architecture.md:6` | "...merupakan ide yang **tidak hanya sangat layak (feasible), tetapi juga memegang urgensi strategis yang fundamental**." | Tulis versi faktual: " Gagasan ini layak dan strategis." |
| `11-archive-proposal.md:303` | "admisi rawat inap <30 hari dengan diagnosis identik **tanpa jeda klinis wajar** untuk meraup klaim INA-CBG ganda" | Frasa emotif; ganti dengan kriteria objektif |

Duplikat: `14-index.md:909` (`pada akhirnya`), `14-index.md:910` (frasa "tidak hanya ... tetapi juga"), `14-index.md:778` (tanpa jeda klinis wajar).

### 9.2 Kalimat pasif (density `di-` + kata kerja)

| File | Jumlah | per 1.000 kata |
|---|---|---|
| `04-evidence-matrix.md` | 12 | **12,2** (tertinggi) |
| `01-proposal.md` | 14 | 8,4 |
| `06-research-notes.md` | 8 | 8,2 |
| `03-dataset-registry.md` | 7 | 5,9 |
| `00-dashboard.md` | 6 | 5,9 |
| `05-decision-scope.md` | 4 | 5,4 |
| `08-training-protocol.md` | 6 | 4,8 |
| `02-architecture.md` | 5 | 4,2 |
| `12-archive-architecture.md` | 13 | 3,4 |
| `14-index.md` | 109 | 3,6 |
| `11-archive-proposal.md` | 27 | 2,6 |
| `07-dataset-v2-catalog.md` | 3 | 2,7 |
| `09-draft-hub.md` | 2 | 0,4 |
| `10-simulation-dataset.md` | 1 | 0,4 |
| `13-archive-deep-research.md` | 0 | 0,0 |

### 9.3 Campuran bahasa Inggris-Indonesia

| Istilah Inggris | Kemunculan | Berkas |
|---|---|---|
| `&` (dan) | 449 | `14-index.md` (220), `11-archive-proposal.md` (149), `09-draft-hub.md` (32), `12-archive-architecture.md` (31), `10-simulation-dataset.md` (15) |
| `vs` (versus) | 58 | `14-index.md` (28), `11-archive-proposal.md` (20), `09-draft-hub.md` (4) |
| `→` (panah) | 47 | `14-index.md` (20), `09-draft-hub.md` (14), `10-simulation-dataset.md` (7) |
| `skor` | 88 | `14-index.md` (43), `11-archive-proposal.md` (10), `03-dataset-registry.md` (8) |
| `leakage` | 82 | `14-index.md` (38), `12-archive-architecture.md` (16), `09-draft-hub.md` (12) |
| `ground truth` | 27 | `14-index.md` (13), `08-training-protocol.md` (6), `12-archive-architecture.md` (1) |
| `overcharge` | 18 | `14-index.md` (9), `03-dataset-registry.md` (3), `00-dashboard.md` (2) |
| `fallback` | 17 | `14-index.md` (7), `09-draft-hub.md` (6), `10-simulation-dataset.md` (3) |
| `hit-rate` | 7 | `14-index.md` (3), `09-draft-hub.md` (2) |
| `Baseline first` | 2 | `02-architecture.md:15`, `14-index.md` |
| `Fail-safe behavior` | 2 | `02-architecture.md:13`, `14-index.md` |
| `Human-in-the-loop` | 2 | `02-architecture.md:10`, `14-index.md` |

Tiga heading prinsip di `02-architecture.md:10,13,15` (`Human-in-the-loop`, `Fail-safe behavior`, `Baseline first`) tidak diterjemahkan, sementara dokumen controlled lain memakai bahasa Indonesia penuh.

### 9.4 Salah ketik dan ejaan (dokumen arsip)

| File:baris | Teks salah | Yang benar |
|---|---|---|
| `11-archive-proposal.md:3` | "PROPOSAL INOVASI TEKNOLOGI **KESEHATANBPJS** KESEHATAN HEALTHKATHON **2026Kategori**:" | "KESEHATAN BPJS KESEHATAN ... 2026" + baris baru + "Kategori:" |
| `11-archive-proposal.md:8` | "Diajukan **Oleh:TIM** INOVATOR KANDIDAT 1 - AEGIS-JKN1. Lead Platform..." | "Diajukan Oleh: TIM ... AEGIS-JKN" + baris baru per Mata |
| `12-archive-architecture.md:6` | "...merupaka ide..." | "merupakan ide" |
| `13-archive-deep-research.md:8` | "kelemahan **verivikasi** berkas elektronik" | "verifikasi" |
| `13-archive-deep-research.md:9` | "**Penyalahgunaaan** data peserta" | "Penyalahgunaan" |
| `14-index.md:478`, `:483`, `:910`, `:1105`, `:1106` | Duplikat dari atas | Ikuti perbaikan sumber |

Tanda baca non-standar lain: `13-archive-deep-research.md:15` dan `14-index.md:1112` memuat non-breaking space (`U+00A0`) pada "Kata Kunci:". `13-archive-deep-research.md:3` memakai "RP25 miliar" (huruf kapital untuk mata uang, bukan "Rp25 miliar") dan "jawa tengah" (nama wilayah harus "Jawa Tengah").

### 9.5 Struktur bullet berlebihan

| File | Baris bullet | Total baris | Rasio |
|---|---|---|---|
| `14-index.md` | 516 | 1.939 | 26,6% |
| `09-draft-hub.md` | 138 | 432 | 31,9% |
| `12-archive-architecture.md` | 21 | 193 | 10,9% |
| `10-simulation-dataset.md` | 69 | 212 | 32,5% |
| `00-dashboard.md` | 48 | 94 | 51,1% |
| `02-architecture.md` | 55 | 115 | 47,8% |
| `05-decision-scope.md` | 28 | 76 | 36,8% |
| `04-evidence-matrix.md` | 39 | 86 | 45,3% |

---

## 10. Metrik Keterbacaan per Dokumen

Definisi: kata = token `[\w'-]+`; kalimat = pecah pada `(?<=[.!?])\s+` setelah kolom tabel dibuang; jargon = 39 token teknis (MHGSL, XAI, SHAP, AUPRC, AUROC, ROC-AUC, SMOTE, LOS, ICD-10, ICD-9-CM, FORNAS, FEP, FKRTL, FHIR, PyG, XGBoost, MLP, RAG, LLM, SP2D, INA-CBG, DSP, GNN, GCN, EMR, PWA, NLP, DPO, DP-CTGAN, CDSS, DJS, ACCH, OASIS, Kaggle, FPR, ML, DL, LOGO).

| File | Kata | Kalimat | Kata/kalimat | Jargon | % jargon | Jenis jargon | Baris bullet | Baris tabel | Heading | Kalimat "AI" | Kalimat pasif |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `00-dashboard.md` | 1.019 | 64 | 15,9 | 4 | 0,39 | 3 | 48 | 12 | 18 | 0 | 6 |
| `01-proposal.md` | 1.669 | 89 | 18,8 | 6 | 0,36 | 4 | 29 | 7 | 23 | 0 | 14 |
| `02-architecture.md` | 1.190 | 72 | 16,5 | 6 | 0,50 | 5 | 55 | 16 | 21 | 0 | 5 |
| `03-dataset-registry.md` | 1.196 | 58 | 20,6 | 8 | 0,67 | 4 | 30 | 48 | 15 | 0 | 7 |
| `04-evidence-matrix.md` | 981 | 54 | 18,2 | 6 | 0,61 | 4 | 39 | 20 | 11 | 0 | 12 |
| `05-decision-scope.md` | 736 | 53 | **13,9** | 0 | **0,00** | 0 | 28 | 6 | 13 | 0 | 4 |
| `06-research-notes.md` | 970 | 51 | 19,0 | 8 | 0,82 | 4 | 25 | 9 | 18 | 0 | 8 |
| `07-dataset-v2-catalog.md` | 1.122 | 35 | 32,1 | 20 | 1,78 | 2 | 6 | 64 | 11 | 0 | 3 |
| `08-training-protocol.md` | 1.261 | 47 | 26,8 | 12 | 0,95 | 6 | 9 | 22 | 5 | 0 | 6 |
| `09-draft-hub.md` | 4.628 | 119 | 38,9 | 121 | 2,61 | 21 | 138 | 194 | 29 | 0 | 2 |
| `10-simulation-dataset.md` | 2.270 | 58 | 39,1 | 60 | 2,64 | 21 | 69 | 97 | 12 | 0 | 1 |
| `11-archive-proposal.md` | 10.583 | 365 | 29,0 | 206 | 1,95 | 27 | 59 | 93 | 75 | 1 | 27 |
| `12-archive-architecture.md` | 3.856 | 117 | 33,0 | 153 | **3,97** | **27** | 21 | 38 | 23 | 2 | 13 |
| `13-archive-deep-research.md` | 259 | 23 | **11,3** | 3 | 1,16 | 1 | 11 | 0 | 1 | 0 | 0 |
| `14-index.md` | 30.391 | 1.182 | 25,7 | 565 | 1,86 | 35 | 516 | 535 | 282 | 3 | 109 |
| **TOTAL** | **62.131** | **2.387** | **26,0** | **1.178** | **1,90** | | **516+** | **535** | **282** | **6** | **109** |

### 10.1 Temuan per metrik

- **Paling padat jargon:** `12-archive-architecture.md` (3,97% dari seluruh kata adalah token teknis, 27 jenis berbeda) disusul `10-simulation-dataset.md` (2,64%), `09-draft-hub.md` (2,61%), `11-archive-proposal.md` (1,95%).
- **Paling mudah dibaca:** `13-archive-deep-research.md` (11,3 kata/kalimat, 259 kata, 0 kalimat pasif) - tetapi ini karena isinya sangat pendek dan masih kasar (lihat §9.4). Di antara dokumen controlled: `05-decision-scope.md` (13,9 kata/kalimat, 0 token jargon sama sekali).
- **Rata-rata kalimat terpanjang:** `10-simulation-dataset.md` (39,1) dan `09-draft-hub.md` (38,9) - ini konsekuensi duplikasi tabel, bukan gaya menulis.
- **Dokumen dengan rasio bullet tertinggi:** `00-dashboard.md` (51,1% baris adalah bullet) dan `02-architecture.md` (47,8%).
- **Dokumen terbesar:** `14-index.md` (30.391 kata = 48,9% dari korpus) berisi 83 baris tabel duplikat (`14-index.md:60-142` = `09-draft-hub.md:17-99`).

---

## 11. Rekomendasi

| Prioritas | Rekomendasi | Filesystem | Pemicu |
|---|---|---|---|
| P0 | Turunkan status seluruh klaim "terbukti/tervalidasi" di dokumen arsip menjadi "estimasi/hipotesis", atau tambahkan blok "CATATAN EDITORIAL" yang menandai angka tersebut belum tervalidasi | `11-archive-proposal.md:30,143,320,326-333,338,342,346,348,402,410`; `12-archive-architecture.md:5,6,30,115,127` | Sekarang: bertentangan langsung dengan `00-dashboard.md:46-52` |
| P0 | Tambahkan sitasi primer (URL + tahun + nomor tabel) untuk setiap angka nasional: 2 juta klaim/hari, 1.000 verifikator, 175.774 klaim ACCH KPK, Rp25 miliar, tarif Gemini | `11-archive-proposal.md:22,128,155,162,188,189,410`; `12-archive-architecture.md:5,103,116`; `13-archive-deep-research.md:3` | Sebelum dipakai sebagai argumen |
| P1 | Definisikan 29 singkatan pada pemakaian pertama di setiap dokumen, atau buat satu blok "Definisi Singkatan" di `00-dashboard.md` dan rujuk silang | Semua, khususnya `09`, `10`, `12`, `14` | 113 pasangan tanpa definisi |
| P1 | Tambahkan block header (Status, Versi, Tanggal, Tujuan) pada 8 dokumen yang belum punya | `07`, `08`, `09`, `10`, `11`, `12`, `13`, `14` | Pelanggaran §7 butir 2 |
| P1 | Tambahkan satuan pada header kolom (contoh: "Jumlah (klaim)", "Umur (tahun)", "Skor Maks (0-1)") dan baris Total pada 41 tabel; sisa 4 tabel: `03:32`, `11:343`, `14:818`, `14:1453` | `00:29`, `03:11,18,24`, `04:11`, `07:8,17,43,66,72`, `09:24,32,46,68,80` (+duplikat), `10:21,29,43,65,77`, `11:375` (+duplikat), `12:179` | Pelanggaran §7 butir 5 |
| P1 | Hapus duplikasi 83 baris tabel `09-draft-hub.md` (baris 229-325 identik dengan 17-113) dan jadikan `10-simulation-dataset.md` sebagai sub-halaman `09` | `09-draft-hub.md` | Risiko divergensi data |
| P2 | Terapkan glosarium kanonik (lihat §12) dan normalisasi 7 konsep terminologi | Semua | Pelanggaran §7 butir 3 |
| P2 | Ganti 21 spasi-hyphen prosa dengan koma/titik dua | `12:5,6,31,54,116`, `09:6,111,114`, `10:3,108`, `11:8`, `14:49,154,261,366,483` | Semantik em-dash tersembunyi |
| P2 | Perbaiki 8 salah ketik dan 2 non-breaking space | `11:3,8`, `12:6`, `13:3,8,9,15`, `14:478,483,910,1105,1106,1112` | Kualitas ejaan |
| P2 | Pecah `14-index.md` (30.391 kata) menjadi indeks tautan saja; hapus isi duplikat | `14-index.md` | 48,9% korpus |
| P3 | Terjemahkan 3 heading prinsip dan konsolidasikan 449 "&" / 58 "vs" | `02:10,13,15`; `11`; `14` | Gaya bahasa |

---

## 12. Glosarium Kanonik

| Singkatan | Definisi kanonik | Dokumen kanonik (tempat definisi) | Peringatan penggunaan |
|---|---|---|---|
| MHGSL | Multi-Hop Graph Structure Learning | `02-architecture.md` | 138 kemunculan di 6 dokumen; hanya 1 terdefinisi |
| XAI | Explainable AI | `01-proposal.md:10` (kata kunci) | 28 kemunculan; 3 varian (XAI / Explainable AI / explainability) |
| SHAP | SHapley Additive exPlanations | `01-proposal.md:91` | 40 kemunculan; definisi asli hanya di `12-archive-architecture.md:38` |
| AUPRC | Area Under the Precision-Recall Curve | `02-architecture.md:74` | 50 kemunculan; sering dianggap sinonim dengan accuracy |
| AUROC / ROC-AUC | Area Under the Receiver Operating Characteristic Curve | `02-architecture.md:74` | Dua ejaan berbeda untuk konsep sama |
| SMOTE | Synthetic Minority Over-sampling Technique | `08-training-protocol.md` | 11 kemunculan; metode oversampling |
| LOS | Length of Stay (hari rawat) | `03-dataset-registry.md:57` | 7 kemunculan; 109 baris kosong (lihat `00-dashboard.md:36`) |
| ICD-10 | International Classification of Diseases, Revision 10 | `03-dataset-registry.md:54` | 31 kemunculan |
| ICD-9-CM | International Classification of Diseases, Ninth Revision, Clinical Modification | `03-dataset-registry.md:55` | 22 kemunculan |
| FORNAS | Formularium Nasional | `09-draft-hub.md:91` | 22 kemunculan; dipakai sebagai heading tabel obat |
| FEP | (tidak teridentifikasi dalam korpus) | - | 0 kemunculan; hapus dari daftar istilah |
| FKRTL | Fasilitas Kesehatan Rujukan Tingkat Lanjutan | `11-archive-proposal.md:22` | 70 kemunculan |
| FHIR | Fast Healthcare Interoperability Resources (R4) | `11-archive-proposal.md:29` | 34 kemunculan |
| PyG | PyTorch Geometric | `08-training-protocol.md` | 27 kemunculan; belum terdefinisi di mana pun |
| XGBoost | Extreme Gradient Boosting | `01-proposal.md:43` | 86 kemunculan; 1x terdefinisi saja |
| MLP | Multi-Layer Perceptron | `08-training-protocol.md` | 23 kemunculan; belum terdefinisi di mana pun |
| RAG | Retrieval-Augmented Generation | (tidak ada di korpus) | 0 kemunculan; hapus dari daftar istilah |
| LLM | Large Language Model | `11-archive-proposal.md:178` | 36 kemunculan |
| SP2D | (tidak teridentifikasi dalam korpus) | - | 0 kemunculan; hapus dari daftar istilah |
| INA-CBG | Indonesian Case-Based Grouping (tarif Claims National) | `12-archive-architecture.md:12` | 18 kemunculan; basis hitungan overcharge |
| DSP | (tidak teridentifikasi dalam korpus) | - | 0 kemunculan; hapus dari daftar istilah |
| DP-CTGAN | Differential Privacy Conditional Table GAN | `12-archive-architecture.md:48` | 23 kemunculan; generator augmentasi |
| DPO | Direct Preference Optimization | `12-archive-architecture.md:91` | 6 kemunculan; fase roadmap |
| GNN | Graph Neural Network | `12-archive-architecture.md:29` | 14 kemunculan |
| GCN | Graph Convolutional Network | `12-archive-architecture.md:30` | 16 kemunculan |
| EMR | Electronic Medical Record | `11-archive-proposal.md:383` | 5 kemunculan |
| PWA | Progressive Web Application | `11-archive-proposal.md:384` | 4 kemunculan |
| NLP | Natural Language Processing | `09-draft-hub.md:104` | 14 kemunculan |

### 12.1 Istilah kanonik (non-singkatan)

| Konsep | Istilah kanonik | Dilarang | Sumber aturan |
|---|---|---|---|
| Status kerja | `auto_clear`, `review`, `escalate` | `auto-clear`, `auto clear`, `eskalasi` sebagai nilai data | `03-dataset-registry.md:43-45` |
| Label risiko | `low`, `medium`, `high`, `fraud` | `rendah`/`sedang`/`tinggi` di kolom data, `medium/high` | `03-dataset-registry.md:39-42` |
| Aktivitas manusia | telaah, verifikasi, validasi | `review`/`reviewer` di teks naratif | `02-architecture.md:64` |
| Fenomena | kecurangan, anomali, modus | `fraud` sebagai kata Indonesia | `11-archive-proposal.md:22` |
| Data simulasi | sintetis | `synthetic`, `mock`, `fake` | `00-dashboard.md:44` |
| Produk | purwarupa | `prototipe`, `prototype` | `01-proposal.md:6` |
| Machine learning | pembelajaran mesin | `machine learning` di teks formal | `02-architecture.md:15` |
| Graf | pembelajaran graf | `graph learning` di teks formal | `06-research-notes.md` |
| Nilai uang | nominal klaim | `biaya` di kolom tabel | `00-dashboard.md:35` |
| Kebocoran label | kebocoran label | `leakage` di prosa | `08-training-protocol.md:22` |

---

## Lampiran: Metodologi dan Batasan

**Skrip audit** (Python 3.11): `dash2.py` (census tanda panjang), `dash3.py`/`dash4.py` (klasifikasi double hyphen), `abbr2.py` (census singkatan + deteksi definisi), `hdr.py` (ekstraksi header + pola klaim eksternal), `t3.py`/`t7.py` (audit satuan/denominator tabel), `d.py` (varian terminologi), `ext3.py` (klaim numerik tanpa sumber), `metrics2.py` (metrik keterbacaan), `dup.py` (duplikasi baris tabel), `typo.py` (ejaan).

**Batasan yang diketahui:**
1. Ekspor Notion tidak memancarkan baris separator `|---|`. Semua 51 tabel dideteksi dari baris `|` berurutan. Risiko: tabel yang dipisah paragraf terlewat. Verifikasi manual terhadap tabel non-numerik juga dilakukan.
2. Deteksi definisi singkatan berbasis pola (nama panjang dalam kurung, "adalah", "berarti", "merupakan"). Singkatan yang didefinisikan lewat tabel/kolom (mis. "Sinyal SHAP" sebagai nama kolom) dianggap terdefinisi.
3. `03-dataset-registry.md:66` (1.859 + 1.552 + 1.979 + 1.030 = 6.420) tidak cocok dengan total 6.514.039 di `:6`; ini temuan rekonsiliasi yang perlu diperiksa terpisah, bukan kesimpulan audit bahasa.
4. Angka "48,9%" untuk proporsi `14-index.md` dihitung terhadap 62.131 kata korpus penuh.
5. Semua lokasi file:baris merujuk pada berkas di `N:\HEALTHKATHON\analysis\corpus\` pada keadaan 22 Oktober 2026.
