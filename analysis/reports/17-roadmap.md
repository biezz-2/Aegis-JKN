# 17 - Roadmap, Gap Analysis Terintegrasi, dan Checklist Submission Aegis-JKN

Status: Rencana kerja eksekutif · Revisi 2.1 (terikat tanggal, koreksi repo eksperimen)
Tanggal penyusunan: 22 Oktober 2026
Ruang lingkup: Healthkathon BPJS Kesehatan 2026, tema "Detect Smarter, Protect JKN"
Sumber primer jadwal: `POST https://healthkathon.bpjs-kesehatan.go.id:8080/healthkathon/rest/referensi/siklus/list` (dicek 22 Okt 2026)
Basis audit: korpus Notion lokal (`N:\HEALTHKATHON\analysis\corpus\`), data `claims_v2_live.csv`, dan basis kode read-only `N:\HEALTHKATHON\Aegis-JKN\`

---

## 1. Ringkasan Eksekutif

### 1.1 Posisi kritis: jendela waktu bukan 14 hari ke depan, melainkan 10 hari ke belakang

Tanggal pendaftaran dan submit proposal **sudah ditutup** (14 Agu – 11 Okt 2026). Seleksi proposal juga selesai (12 – 18 Okt). Fase yang sedang aktif adalah **Submit project akhir (19 Okt – 1 Nov 2026)** dan **Coaching & Development (19 – 30 Okt 2026)**. Demo day / Grand Final jatuh pada **7 Nov 2026**. Dengan 872 tim terdaftar, posisi saat ini adalah **tim yang lolos seleksi proposal dan kini harus mengirim artefak proyek akhir**, bukan tim yang masih menyusun proposal.

Konsekuensi: seluruh work item P0 pada Dashboard §6 (00-dashboard.md:58-63) bukan "backlog prioritas" - ia adalah **blokir deliverable 1 Nov**. Tidak ada harian tersisa untuk membangun model MHGSL dari nol. Yang harus diperbaiki dalam 10 hari adalah **laub integritas bukti**, bukan cakupan fitur.

### 1.2 Dua jalur, dipisahkan tegas

**Jalur Submit (22 Okt – 1 Nov 2026, 10 hari kerja) - 17 backlog item (B-01..B-17: 16 item P0 + 1 item P1), menutup 16 gap (15 gap P0 + G-15).**
Fokus: hentikan overclaim, kunci definisi label, **perbaiki metodologi evaluasi**, lampirkan artefak eksperimen, rekonsiliasi angka, dan siapkan demo yang jujur. Kriteria sukses bukan "model menang", melainkan "setiap angka di layar dapat direproduksi juri dalam 5 menit, dan tidak ada angka yang tidak punya bukti".

**Jalur Riset (2 Nov 2026 dan sesudahnya) - 14 backlog item (B-18..B-31: 10 item P1 + 4 item P2), menutup 17 gap (13 gap P1 + 4 gap P2).**
Fokus: MHGSL, XAI per-saluran, uji tambah nilai graph learning, DP-CTGAN, pipeline data. Semua ini **boleh tidak ada** saat submit, dan harus dinyatakan sebagai rencana dengan kriteria penerimaan, bukan sebagai hasil.

### 1.3 Temuan paling berbahaya

Repositori app (`N:\HEALTHKATHON\Aegis-JKN\`) bukan satu-satunya basis kode proyek. Ada **repo git ketiga yang terpisah**, `N:\HEALTHKATHON\mechine-learning-deep-learning\` (remote `github.com/biezz-2/Aegis-JKN-mechine-learning-deep-learning.git`), berisi 1.818 baris Python di `backend/src/`, dataset CSV 31 kolom 300 baris, implementasi MHGSL, checkpoint model, dan notebook GroupKFold/LOGO. Audit awal yang hanya_rdonly repo app keliru menyimpulkan tidak ada kode ML - koreksi lengkapnya ada di §10.

Corrigendum tersebut **memperburuk**, bukan memperbaiki, beberapa temuan. Empat kelas temuan paling berbahaya:

1. **Metrik yang dilaporkan tidak mengukur apa yang dilatih (G-10, P0 teratas).** Di `notebooks/Aegis-JKN.ipynb` sel 11, model dilatih pada `y_target = (is_fraud==1) OR (sindikat!='none')` (38 positif) tetapi AUPRC/AUROC dihitung terhadap `y_fraud_gt = is_fraud` (36 positif). Selisihnya tepat 2 baris: **KLM016 dan KLM017** (`sindikat=SYND-05`, `risiko=high`, `status=review`, `modus=cloning`) - keduanya dilatih sebagai positif tetapi dinilai negatif saat pengukuran.
2. **Tabel benchmark dievaluasi in-sample (G-11, P0).** Di sel 13, XGBoost, MLP, Homogeneous GCN, dan MHGSL semuanya di-`fit` lalu di-`predict` pada matriks yang sama (`X_clean` / `X_tensor`), dan tabel benchmark dihitung dari probabilitas in-sample itu. Probabilitas out-of-fold GroupKFold yang sudah ada di sel 11 **tidak dipakai**. Konsekuensinya trigger M-01 (MHGSL vs baseline) tidak dapat dievaluasi dari output sekarang, dan angka yang ditampilkan UI (`data.ts:258-291`: AUPRC 0,71→0,91, Precision 0,92, Recall 0,90, F1 0,91) tidak berasal dari pipeline mana pun.
3. **Struktur graf dibangun dari kolom label (G-12, P0).** `backend/src/data/pipeline.py:293-307` membentuk sisi edge kanal semantik bila dua klaim berbagi nilai `sindikat`. Dari 3.790 pasangan edge semantik, 65 (1,7%) berasal dari kecocokan `sindikat` - kebocoran yang tidak tertangkap blokir kolom biasa karena kanal graf biasanya dianggap "netral".
4. **Overclaim finansial dan angka salah di layar presentasi (G-03, G-07).** `src/components/mhgsl/fraud-ring.tsx:415` "Rp 1,2 M/bulan (Rp 14,4 M/tahun)" dengan `roadmap.tsx:34` `useCountUp(14.4)`, diturunkan dari Rp507.370.000 yang dinyatakan belum dapat direproduksi (00-dashboard.md:39); `dataset-explorer.tsx:708` "240 Rawat Inap · 60 Jalan" vs data sebenarnya 189/111; `dataset-explorer.tsx:764` "Rp 3,53 M" untuk Rp3.526.650.000 (seharusnya Miliar), bertentangan dengan `:640` di halaman yang sama.

Temuan 1–3 berada di jalur bukti yang akan dibuka juri ("mana ground truth?", "itu hasil run mana?", "split-nya mana?"), dan ketiganya bisa dijawab salah dalam satu kalimat. Temuan 4 berada di layar, bukan lampiran.

### 1.4 Angka inti

| Metrik | Nilai |
|---|---|
| Total gap | 33 (15 P0, 14 P1, 4 P2) |
| Gap P0 | 15 |
| Gap P1 | 14 |
| Gap P2 | 4 |
| Total work item (backlog) | 31 (B-01..B-17 Jalur Submit, B-18..B-31 Jalur Riset) |
| Komposisi backlog | 16 item P0, 11 item P1, 4 item P2 |
| Cakupan gap | 16 gap ditutup Jalur Submit (15 P0 + G-15); 17 gap ditutup Jalur Riset (13 P1 + 4 P2) |
| Hari kerja tersisa ke submit | 10 |
| Gap harian teratas | G-10 (label training beda dengan ground truth), G-11 (benchmark in-sample), G-01 (definisi label), G-12 (graf dari kolom label) |
| Trigger paling kritis | AUPRC MHGSL (OOF) <= baseline XGBoost (OOF) pada split group-aware yang sama -> fallback ke XGBoost + fitur graf turunan, tampilkan "desain belum terbukti unggul" |
| Trigger kedua (bloker keras) | `y_train` != `y_eval` pada >=1 baris, atau benchmark dihitung in-sample -> **tidak boleh submit**; seluruh angka metrik dicabut |
| Staleness terdeteksi | Deadline di `src/data/notion-datasets.ts:383,385` (14 Sep) vs API resmi (1 Nov project akhir) |

---

## 2. Tabel Gap Analysis Terurut

Urut = kombinasi (a)/blockir submit lebih tinggi dari (b), (b) kritikalitas, (c) ketergantungan.

| ID | Gap | Jenis | Bukti (file:baris) | Kritikalitas | Effort | Dependensi | Kriteria penerimaan (terukur) |
|---|---|---|---|---|---|---|---|
| G-01 | Definisi label fraud/anomali/normal belum dikunci; ambigu ambang 0,80 (KLM115 dilabeli fraud dengan skor tepat 0,80) | data/governance | 00-dashboard.md:59; 03-dataset-registry.md:46; `analysis/reports/scripts/04_audit_results.json` → `edge_scores: [["KLM115","0.8","fraud"]]` | Kritis (P0) | S | - | 1 dokumen `docs/dataset/label-spec.md` v1.0 berisi definisi case per modus, aturan ambang dengan batas tertutup (`[0.80,1.00]`), dan keputusan eksplisit untuk KLM115; disetujui 2 peninjau (data + klinis) dengan nama & tanggal |
| G-02 | Angka benchmark di UI adalah konstanta hardcode yang TIDAK diturunkan dari keluaran notebook mana pun; notebook utama `Aegis-JKN.ipynb` punya 0 stored output sehingga angka hasil yang akan dibandingkan pun belum terekam | code/data | `src/components/mhgsl/data.ts:258-265`, `:270-291`, `:253`, `:23`; `mechine-learning-deep-learning/notebooks/Aegis-JKN.ipynb` (22 sel, **0 stored output** di 11 sel kode) | Kritis (P0) | M | G-05 | Setiap angka benchmark UI berasal dari `docs/experiments/metrics.json` yang dihasilkan skrip; notebook utama dijalankan ulang dan menyimpan output ke `docs/experiments/exp-001/`; `tests/test_metrics_provenance.py` lulus; 0 konstanta metrik hardcoded di `src/components/mhgsl/data.ts` |
| G-03 | Klaim penghematan Rp14,4 M/tahun dan Rp507.370.000 tampil di UI tanpa tarif acuan maupun formula | docs/data | `src/components/mhgsl/fraud-ring.tsx:415`; `src/components/mhgsl/roadmap.tsx:34`; 00-dashboard.md:39; 04-evidence-matrix.md E-11; 11-archive-proposal.md:347-348 | Kritis (P0) | M | G-04 | Angka finansial dihapus dari UI atau diberi label "proyeksi asumsi, belum tervalidasi" + tautan ke `docs/experiments/assumptions.md` yang memuat tarif acuan, formula, dan status adjudikasi per klaim; 0 klaim penghematan tanpa disclaimer |
| G-04 | Tarif acuan dan metode perhitungan overcharge per klaim belum ada | data | 00-dashboard.md:62; 02-architecture.md:112 (D-04); 03-dataset-registry.md:109 | Kritis (P0) | M | G-01 | `data/processed/tariff_reference.csv` berisi ≥1 tarif acuan per kombinasi ICD-9 yang dipakai (≥9 baris); `scripts/compute_overcharge.py` menghasilkan kolom overcharge untuk 60 klaim anomali; 100% baris punya nilai atau alasan "tidak dapat dihitung" |
| G-10 | **Label training dan label ground truth BERBEDA di notebook utama**: model dilatih pada `y_target = (is_fraud==1) \| (sindikat!='none')` (38 positif) tetapi AUPRC dihitung terhadap `y_fraud_gt = is_fraud` (36 positif). Selisih tepat 2 baris: KLM016 & KLM017 (`sindikat=SYND-05`, `risiko=high`, `status=review`, `modus=cloning`). Konsekuensi: metrik yang dilaporkan tidak mengukur apa yang dilatih, dan 2 baris `risiko=high` yang dilatih sebagai positif justru dihitung sebagai **negatif** ground truth (false positive yang tersembunyi) | code/model | `mechine-learning-deep-learning/notebooks/Aegis-JKN.ipynb` sel 11 (`y_target`, `y_fraud_gt`, `average_precision_score(f_gt, val_probs)`, `average_precision_score(y_fraud_gt, gkf_oof_probs)`); replikasi pada `datasets/claims_300_v2.1.csv`: positif `y_target`=38 vs `y_fraud_gt`=36, mismatch = KLM016+KLM017 | Kritis (P0) | S | G-01 | Satu fungsi label tunggal `build_target(df)` dipakai training DAN evaluasi; `y_train` == `y_eval` == 100% identik pada 300 baris (0 baris beda); KLM016 & KLM017 diputuskan eksplisit di `docs/dataset/label-spec.md` (entah fraud atau anomali-sindikat) dan dipindahkan ke kelas yang konsisten; `tests/test_label_consistency.py` asserting `set(y_train) == set(y_eval)` |
| G-11 | **Benchmark notebook dievaluasi IN-SAMPLE**: XGBoost, MLP, Homogeneous GCN, dan MHGSL semuanya di-`fit` dan di-`predict` pada matriks yang sama (`X_clean` / `X_tensor`), lalu tabel benchmark dihitung dari probabilitas in-sample itu. Probabilitas out-of-fold GroupKFold yang sudah dihitung di sel 11 TIDAK dipakai di tabel benchmark. Akibatnya tabel pembanding tidak sah sebagai pembanding model | code/model | `notebooks/Aegis-JKN.ipynb` sel 13: `xgb_clf.fit(X_clean, y_target)` → `probs_xgb = xgb_clf.predict_proba(X_clean)[:,1]`; `probs_mlp = torch.sigmoid(mlp_clf(X_tensor))`; `probs_homo = torch.sigmoid(homo_gcn(X_tensor, graphs['adj_homo']))`; `final_mhgsl` dilatih 130 epoch pada `X_tensor` lalu `probs_mhgsl = torch.sigmoid(logits)` pada `X_tensor` yang sama; `m = compute_benchmark_metrics(y_fraud_gt, probs)` | Kritis (P0) | M | G-10 | Tabel benchmark dihitung HANYA dari probabilitas out-of-fold (GroupKFold(5) group=`pasien_id` + LOGO group=`faskes_id`) pada split yang sama untuk keempat model; tidak ada satu pun `predict_proba` pada data latih di jalur benchmark; `tests/test_no_insample_eval.py` memindai notebook dan gagal bila `fit(` dan `predict` terjadi pada variabel matriks yang sama; angka M-01 dihitung dari OOF |
| G-12 | **Graf pada `pipeline.py` diturunkan dari kolom label `sindikat`**: kanal semantik membentuk sisi edge bila dua klaim berbagi nilai `sindikat`, yaitu struktur graf dibangun dari informasi label | code/model | `backend/src/data/pipeline.py:293-307` (`has_sindikat`, `sindikat_arr`, `sindikat_match = (s_i == sindikat_arr[j])`, `if same_pair or sindikat_match:`); kuantifikasi pada `datasets/claims_300_v2.1.csv`: 3.790 pasangan edge semantik unik, 65 di antaranya (1,7%) berasal dari kecocokan `sindikat`; bandingan kanal topologis 5.043 pasangan | Kritis (P0) | M | G-05 | `sindikat` (dan `modus`, `risiko`, `status`) DIHAPUS dari input pembentuk adjacency; kanal semantik hanya memakai `diagnosis_code`, `prosedur_code`, `faskes_id` (seperti sel 7 notebook, ambang 0,55); `tests/test_graph_features.py` asserting 0 sisi edge yang berasal dari kolom label; metrik dihitung ulang setelah perbaikan |
| G-13 | Kredensial API nyata tersimpan di disk pada `backend/.env` (`NOTION_TOKEN` 50 karakter, `OPENAI_API_KEY` 27 karakter, plus `DATABASE_URL` Postgres dan `REDIS_URL`). Berkas TIDAK ter-commit (repo punya `.gitignore` sendiri, `.env` diabaikan; `git ls-files` tidak mencantumkannya), tetapi nilai live ada di disk dan belum pernah dirotasi | code/security | `mechine-learning-deep-learning/backend/.env` (nilai TIDAK ditampilkan di dokumen ini demi keamanan); `.gitignore:37` memuat `.env`; `git check-ignore -v backend/.env` keluar 0; `git ls-files --error-unmatch backend/.env` gagal (untracked) | Tinggi (P0) | S | - | Kedua kredensial dirotasi di provider (Notion + OpenAI) sebelum 1 Nov dan nilai baru hanya disimpan di `.env` lokal; `backend/.env.example` (763 B) memuat seluruh nama variabel tanpa nilai; `grep -R "ntn_\|sk-" .` atas repo (tanpa `.env`) mengembalikan 0 hit; `docs/governance/secrets.md` mencatat tanggal rotasi dan siapa pemegang kredensial; tidak ada nilai rahasia yang tertulis di dokumen, commit, atau artefak demo |
| G-14 | **Dua salinan payload yang bisa berbeda sinkron**: `Aegis-JKN/public/payload-aegis-jkn.json` dan `mechine-learning-deep-learning/colab/payload-aegis-jkn.json` byte-identik (SHA-256 `9c8cc58a697642e0…`), keduanya berisi `kpi.total_claims: 100` sementara aplikasi memproses 300 klaim | data | `Aegis-JKN/public/payload-aegis-jkn.json` dan `mechine-learning-deep-learning/colab/payload-aegis-jkn.json` (SHA-256 identik `9c8cc58a…`); `kpi.total_claims: 100` vs 300 baris di app | Tinggi (P0) | S | G-09 | Satu file kanonik ditetapkan (`Aegis-JKN/public/` sebagai satu-satunya sumber yang di-import app); salinan di `colab/` dihapus atau diganti symlink/pointer; `scripts/check_consistency.py` membandingkan `kpi.total_claims` payload terhadap jumlah baris CSV dan gagal bila beda; 2 file payload tidak lagi punya SHA-256 yang sama persis |
| G-15 | `notebooks/02_model_training.ipynb` memakai data acak (`torch.randn` untuk X, `torch.randint` untuk y, `edge_index` acak) - **bukan eksperimen**. Tidak boleh pernah dikutip sebagai hasil, dan kemunculannya di repo berisiko dibaca juri sebagai eksperimen valid | code/model | `notebooks/02_model_training.ipynb` sel 3: `X = torch.randn(num_nodes, input_dim)`, `y = torch.randint(0, 2, (num_nodes,))`, `edge_index = torch.randint(0, num_nodes, (2, num_nodes * 2))`; notebook ini juga 0 stored output | Sedang (P1) | S | G-05 | Notebook diberi header markdown eksplisit "DEMO TOY DATA - BUKAN EKSPERIMEN, DILARANG MENGUTIP HASILNYA"; file dipindahkan ke `notebooks/toy/`; `docs/experiments/exp-001-baseline/REPORT.md` hanya merujuk notebook yang memakai `claims_300_v2.1.csv`; 0 artefak di paket submit berasal dari `02_model_training.ipynb` |
| G-05 | ArTEFAK eksperimen ADA di repo ketiga, tapi tidak ada `manifest.json` per eksperimen, tidak ada checksum berkas, dan tidak ada skrip hitung-metik yang bisa dijalankan ulang; hasil notebook tidak terekam (0 output) sehingga metrik tidak dapat direproduksi | code/data | `mechine-learning-deep-learning/backend/src/` 1.803 baris Python (pipeline.py 352, mhgsl.py 382, api/main.py 426, config.py 54, notion_client.py 93, test_self_check.py 65, oasis/ 428); `backend/src/data/pipeline.py:37-40` `LEAKAGE_COLUMNS` 10 kolom; `pipeline.py:103` `np.random.seed(20260707)`; `backend/models/mhgsl_model.pth` 161 KB; `notebooks/Aegis-JKN.ipynb` 22 sel 0 output; TIDAK ADA `manifest.json`, checksum, `docs/experiments/` | Kritis (P0) | M | G-01 | `manifest.json` per eksperimen berisi: nama+versi dataset, waktu ekspor, jumlah baris, SHA-256 berkas, seed, split ID, daftar fitur; `scripts/compute_metrics.py` dijalankan ulang menghasilkan `metrics.json` identik (2× konsekuen); output notebook tersimpan di `docs/experiments/exp-001/` |
| G-06 | Tidak ada proteksi anti-leakage; kolom turunan label (Skor Fraud, Risiko, Status, Sinyal SHAP, Kontribusi Saluran, Modus, Sindikat) masih ada di CSV dan di-ekspos ke front-end | code/data | `corpus/claims_v2_live.csv` header kolom 5, 9, 10, 13, 20, 25; 10-simulation-dataset.md:126-127; 08-training-protocol.md:22; `src/data/notion-datasets.ts:402` (300 record penuh termasuk kolom leakage) | Kritis (P0) | M | G-05 | `configs/leakage.yaml` memuat daftar blokir; `tests/test_leakage.py` gagal keras (exit≠0) bila 7 kolom terlarang masuk matriks fitur; tidak ada satu pun file CSV/TS yang ships kolom terlarang ke direktori `public/` |
| G-07 | Angka operasional berbeda antara proposal, arsip, dan aplikasi | data/docs | `src/components/dataset/dataset-explorer.tsx:708` (240/60 vs data 189/111) dan `:764` ("Rp 3,53 M" vs Rp3.526.650.000) vs `:640` ("Rp 3,53 Miliar"); 00-dashboard.md:63 | Tinggi (P0) | S | - | Skrip `scripts/check_consistency.py` membandingkan 12 angka kunci (jumlah baris, sebaran label, sebaran status, sebaran layanan, total biaya, LOS kosong, kontradiksi, dll.) terhadap data dan gagal bila beda; 0 selisih pada seluruh angka |
| G-08 | Deadline kompetisi di data riset Notion salah (14 Sep) vs API resmi (submit project akhir 1 Nov) | data/governance | `src/data/notion-datasets.ts:383` "Pendaftaran 14 Agustus–14 September 2026" dan `:385` "Pendaftaran sudah ditutup 14 Sep 2026"; API `siklus/list` kode 1-8 | Tinggi (P0) | S | - | Baris riset diperbarui mencantumkan 8 siklus resmi beserta tanggal dan sumber API; `docs/changelog.md` mencatat revisi 22 Okt 2026 (00-dashboard.md:85 aturan 10) |
| G-09 | Kolom grup untuk GroupKFold/LOGO **sudah ada** di CSV repo ML (31 kolom: `pasien_id`, `faskes_id`, `dokter_id`); yang benar-benar hilang hanya `seed`, `version`, `timestamp`. Klaim pada laporan 04-data-quality.md bahwa group-aware split tidak dapat diimplementasikan TIDAK benar untuk CSV repo ML | data | `mechine-learning-deep-learning/datasets/claims_300_v2.1.csv` 31 kolom (termasuk `pasien_id` c.7, `faskes_id` c.3, `dokter_id` c.5), 300 baris, KLM001-KLM300, TRACKED di git; `04_audit_results.json` → `v21_missing` hanya relevan bagi `corpus/claims_v2_live.csv`; 10-simulation-dataset.md:117-121 | Tinggi (P0) | S | - | 3 kolom metadata `seed`=20260707, `version`=v2.1, `timestamp` ISO-8601 ditambahkan ke CSV repo ML; `tests/test_schema.py` asserting no-null; laporan 04-data-quality.md dikoreksi agar tidak menyiratkan group-aware split mustahil |
| G-33 | Tanggal salah: deadline submit proposal sebagai pekerjaan depan - sudah ditutup | governance | API `siklus/list` kode 2 `aktif:0` (tglselesai 2026-10-11) | Tinggi (P0) | S | G-08 | Tidak ada artefak, checklist, atau presentasi yang menyebut "pendaftaran" atau "submit proposal" sebagai aksi tersisa; satu-satunya checklist submission berlabel "Submit project akhir ≤1 Nov 2026" |
| G-16 | "Data tidak berlaku" vs "data hilang" belum dibedakan (109 baris LOS bernilai 0, dideskripsikan sebagai "kosong") | data | 00-dashboard.md:36 ("109 baris kosong"); 03-dataset-registry.md:78, :82; data aktual: 109 baris `LOS hari` = "0" (bukan string kosong) | Sedang (P1) | S | G-07 | `docs/dataset/data-dictionary.md` menyatakan 4 nilai LOS: `N/A`, `unknown`, `<angka>`, `<kosong>`; 109 baris dipetakan ke `N/A` (rawat jalan) dengan justifikasi per layanan; `tests/test_los_policy.py` asserting 0 baris `LOS=0` tersisa |
| G-17 | Label "Alasan" berisi modus + pembenaran naratif, sehingga model bisa belajar membaca label | data/model | `corpus/claims_v2_live.csv` baris 2 kolom `Alasan` memuat string "FRAUD (Readmission Berulang): ...", `04_audit_results.json` `alasan_kosong: 1` (KLM031) | Sedang (P1) | S | G-06 | `Alasan` dipindah dari kandidat fitur ke tabel `label_audit.csv` terpisah (08-training-protocol.md:21); KLM031 diisi alasan terstruktur; `tests/test_leakage.py` menyertakan `Alasan` pada daftar blokir |
| G-18 | Angka "textContradictions: 8" vs data aktual 12 klaim kontradiktif | data | `src/components/mhgsl/data.ts:515` `textContradictions: 8`; `04_audit_results.json` `kontradiksi_ids` berisi 12 ID; 10-simulation-dataset.md:107 menyebut 8 klaim | Sedang (P1) | S | G-07 | Angka diseragamkan ke 12 dan sumbernya (kolom `Kontradiksi Narasi`) ditampilkan di UI; selisih nol pada `scripts/check_consistency.py` |
| G-19 | Distribusi sentimen berbeda antar sumber (62/14/24 pada 100 klaim vs 170/58/72 pada 300 klaim) tanpa penanda versi | data/docs | 10-simulation-dataset.md:108; data aktual `Sentimen`: positif 170, netral 58, negatif 72 | Sedang (P1) | S | G-07 | Setiap tabel sentimen diberi penanda versi dataset dan jumlah baris; skrip konsistensi menandai tabel tanpa versi sebagai gagal |
| G-20 | Tidak ada log audit atau jejak keputusan verifikator (human-in-the-loop) | code | `src/app/api/route.ts:3` mengembalikan `{"message":"Hello, world!"}`; `prisma/schema.prisma:1-33` hanya model `User`/`Post` scaffold default; `src/lib/db.ts` PrismaClient tidak terpakai | Sedang (P1) | M | G-05 | `prisma/schema.prisma` punya model `ReviewLog` (claim_id, action, reason, reviewer, timestamp) dan `AuditEvent`; `POST /api/review` menulis 1 baris dan mengembalikan id; `tests/test_review_log.py` asserting baris tersimpan |
| G-21 | "Hitung Skor MHGSL" di UI adalah heuristik fusion konstanta yang disamarkan sebagai model | code | `src/components/mhgsl/data-uploader.tsx:79-140` (`scoreRows`: rata-rata similaritas + `isDxMild && isProcExpensive ? 0.9` + `fusionScore * 0.38 + semanticScore * 0.41 + topologyScore * (-0.12) + 0.3`); label tombol `:188` | Tinggi (P1) | M | G-05 | Tombol dan dialog diberi label "Skor demonstrasi (heuristik, bukan model MHGSL terlatih)"; atau diganti pemanggilan API model asli bila G-05 selesai; teks formula `:203` diberi catatan "heuristik demo"; 1 screenshot QA mengonfirmasi |
| G-22 | Prevalensi 12% didiamkan sebagai "prevalensi field 3-7%" tanpa penanda yang konsisten di UI | docs/data | 10-simulation-dataset.md:178-181; `public/payload-aegis-jkn.json` `meta.honesty` menyebut 14% (dataset 100), `kpi.prevalensi: 14`; `src/components/mhgsl/problem-section.tsx:97` "3–7%" | Tinggi (P1) | S | G-07 | Setiap tampilan metrik anomali memakai satu string disclaimer yang diimpor dari satu konstanta: "simulasi sintetis, prevalensi oversampled"; 0 kemunculan angka prevalensi tanpa disclaimer di komponen `src/` |
| G-23 | API backend belum ada; halaman `/dataset` dan `/simulasi` membaca konstanta TS | code | `src/app/api/route.ts` (stub); `src/data/notion-datasets.ts:3` (33 entri riset inline), `:402` (300 klaim inline) | Sedang (P1) | M | G-05, G-09 | `GET /api/claims` mengembalikan JSON dari `data/processed/claims_300_v2.1.csv`; `GET /api/metrics` mengembalikan `docs/experiments/metrics.json`; 1 test integrasi asserting jumlah baris 300 |
| G-24 | Sitasi regulasi memakai sumber agregator, bukan portal resmi | docs | 04-evidence-matrix.md:29-35 (daftar peraturan resmi, "titik awal verifikasi, bukan opini hukum final"); 04-evidence-matrix.md E-01 "Perlu cek pasal spesifik" | Sedang (P1) | S | - | `docs/references/regulations.md` memuat minimal 4 peraturan dengan nomor pasal, URL portal resmi, tanggal akses, dan status berlaku; 0 klaim regulasi tanpa nomor pasal |
| G-25 | Pustaka belum lengkap; E-01..E-12 masih "Perlu Verifikasi" | docs | 04-evidence-matrix.md:19-31 (12 baris register klaim) | Sedang (P1) | S | G-24 | 12 baris E-01..E-12 punya status baru; 0 baris tersisa "Perlu Verifikasi"/"Belum tereproduksi"; setiap E-07..E-11 tertaut ke `docs/experiments/` |
| G-26 | Kepemilikan data, eksperimen, keamanan, dan proposal belum ditetapkan | governance | 00-dashboard.md:69; 05-decision-scope.md:73-77 (5 keputusan terbuka); 02-architecture.md:107-113 (D-01..D-06) | Tinggi (P1) | S | - | `docs/governance/owners.md` menamai owner + reviewer + backup untuk 4 domain; D-01..D-06 ditutup atau diberi status "ditunda, alasan dicatat"; 0 keputusan terbuka tanpa owner |
| G-27 | Tidak ada review klinis atas skenario dan kode diagnosis/prosedur | governance | 00-dashboard.md:65; 05-decision-scope.md:26, :75 | Sedang (P1) | M | G-26 | 2 peninjau klinis menandatangani `docs/dataset/clinical-review.md` yang menilai 13 modus; minimal 5 skenario dengan persetujuan tertulis; ketidaksetujuan dicatat sebagai known limitation |
| G-28 | Kode 999 tanpa deskripsi pada kamus ICD-10 diperlakukan ambigu | data | 07-dataset-v2-catalog.md:67-70, :81 | Rendah (P1) | S | - | `docs/dataset/icd-sentinel-policy.md` menetapkan perlakuan 999 sebagai sentinel (bukan kategori klinis); skrip validasi menandai 0 kode 999 sebagai kategori valid |
| G-29 | Tidak ada uji penerimaan antarmuka terdokumentasi; klaim SUS 82,5 belum ada artefaknya | UX/governance | 00-dashboard.md:49 ("SUS 82,5" belum boleh disebut tervalidasi), :71 | Rendah (P2) | M | - | Protokol uji 5 peserta + lembar instrumen SUS tersimpan di `docs/experiments/usability/`; skor SUS dilaporkan dengan n dan tanggal, atau klaim SUS dihapus dari materi |
| G-30 | Release notes dan pemisahan artefak dev vs eksperimen vs presentasi belum ada | governance | 00-dashboard.md:72-73; 03-dataset-registry.md:105 (changelog kosong) | Rendah (P2) | S | G-05 | `docs/changelog.md` berisi ≥1 entri per perubahan dataset/model; direktori `docs/experiments/`, `docs/presentasi/`, `docs/arsip/` ada dan terisi |
| G-31 | Pipeline ML/DL (MHGSL, XAI per-saluran, DP-CTGAN) belum dijalankan di atas data v2.1 yang benar dan belum menghasilkan artefak hasil. Implementasi MHGSL **sudah ada** di repo ketiga (`backend/src/models/mhgsl.py` 382 baris) dan OASIS sudah ada (`backend/src/oasis/` 428 baris) - yang belum ada adalah **hasilnya yang terekam**: 0 stored output di seluruh notebook repo ML, tidak ada `metrics.json`, tidak ada `docs/experiments/` | code/model | `backend/src/models/mhgsl.py` 382 baris (implementasi nyata, ada di repo ketiga, bukan di repo app); `backend/src/oasis/simulation.py` 338 + `agent_mapper.py` 90; `backend/models/mhgsl_model.pth` 164.825 B (checkpoint ada, provenance-nya tidak); `notebooks/Aegis-JKN.ipynb` 22 sel **0 output**, `02_model_training.ipynb` 11 sel **0 output**; `colab/Aegis_JKN_FIXX.ipynb` 6 sel **13 output** (setup Ollama/mistral-small3.1:24b, bukan eksperimen model); rencana 8 minggu 10-simulation-dataset.md:207-213 belum dijalankan | Sedang (P2) | L | G-05, G-06, G-09, G-10, G-11 | `scripts/train_mhgsl.py` menghasilkan `docs/experiments/exp-002-mhgsl/metrics.json` per 10-simulation-dataset.md:196-204 (≥90% dari 36 fraud di antrean ≤20%, AUPRC OOF ≥ baseline); kegagalan dilaporkan apa adanya sebagai negative result, bukan ditutupi |
| G-32 | Struktur repo yang diwajibkan 10-simulation-dataset.md:182-195 belum ada di kedua repo; repo ketiga hanya punya `datasets/` (3 berkas) tanpa `data/raw`, `data/processed`, `configs/`, `scripts/`, `scripts/seed/`, `docs/experiments/`, dan tanpa `tests/` | code/governance | `mechine-learning-deep-learning/` memuat `datasets/` (claims_300_v2.1.csv, claims_db.json 4.042.592 B, dataset_db.json 182.797 B), `backend/`, `notebooks/`, `colab/` - TIDAK ADA `configs/`, `scripts/`, `tests/`, `docs/`; `Aegis-JKN/` juga tidak punya direktori tersebut | Sedang (P2) | S | G-05 | Direktori dibuat di repo ML dengan README satu paragraf per direktori; `scripts/seed/` memuat generator deterministik yang mereproduksi 300 baris dengan checksum identik dari `claims_300_v2.1.csv` (SHA-256 `37cf22369ebf7a3c…`); `tests/` berisi minimal `test_leakage.py`, `test_schema.py`, `test_labels.py` |

**Total: 27 gap** (10 P0, 13 P1, 4 P2). Backlog §4 menyatukan 27 gap menjadi 25 item yang dimiliki (B-01..B-31).

---

## 3. Roadmap Terikat Tanggal (22 Okt – 7 Nov 2026)

### 3.1 Milestone bertanggal dan pemetaan critical path

| Tanggal | Milestone / Phase | Peran | Work item P0 Dashboard §6 di jalur ini | Deliverable yang harus ada di tanggal ini |
|---|---|---|---|---|
| 21–22 Okt 2026 | Baseline audit | Titik awal | - | Snapshot: `docs/experiments/baseline-2026-10-22.md` berisi 12 angka kunci + hash CSV |
| 22 Okt (Hari 1) | Kunci definisi label + **satu fungsi label** | Critical path | **P0-1** (00-dashboard.md:59) | `docs/dataset/label-spec.md` v1.0 disetujui 2 reviewer; `build_target(df)` tunggal dipakai training & evaluasi (B-12) |
| 22 Okt (Hari 1) | Tentukan owner | Critical path | P1-5 (00-dashboard.md:69) | `docs/governance/owners.md` |
| 23 Okt (Hari 2) | Bekukan sumber + checksum | Critical path | **P0-3** (00-dashboard.md:61) | `manifest.json` dengan SHA-256, seed, jumlah baris, ID split |
| 23 Okt (Hari 2) | Kunci versi dataset | Critical path | **P0-2** (00-dashboard.md:60) | `docs/dataset/version-registry.md` menandai 100 = v1 arsip, 300 = v2.1 aktif |
| 24 Okt (Hari 3) | Anti-leakage guard aktif + **graf bebas kolom label** | Critical path | P0-3 | `configs/leakage.yaml` + `tests/test_leakage.py` (gagal keras); `pipeline.py` tidak lagi memakai `sindikat` untuk adjacency (B-14) |
| 25 Okt (Hari 4) | Rekonsiliasi angka | Critical path | **P0-5** (00-dashboard.md:63) | `scripts/check_consistency.py` hijau pada 12 angka kunci |
| 26 Okt (Hari 5) | Stop overclaim di UI + rotasi kredensial | Critical path | P0-3, P0-5 | `data.ts` tanpa konstanta metrik; `fraud-ring.tsx:415` & `roadmap.tsx:34` dilabeli proyeksi-asumsi; `NOTION_TOKEN` & `OPENAI_API_KEY` sudah dirotasi (B-15) |
| 27 Okt (Hari 6) | Manifest eksperimen + **benchmark out-of-fold** | Critical path | **P0-3** | `docs/experiments/metrics.json` + `train.py` baseline XGBoost reproducible; tabel benchmark dihitung dari probabilitas OOF, bukan in-sample (B-13) |
| 28 Okt (Hari 7) | Tarif acuan + overcharge | Critical path | **P0-4** (00-dashboard.md:62) | `tariff_reference.csv` + `compute_overcharge.py` output 60 baris |
| 29 Okt (Hari 8) | Review klinis parsial | Non-blocking | P1-1 (00-dashboard.md:65) | `clinical-review.md` dengan ≥5 skenario ditandatangani |
| 30 Okt (Hari 9) | Coaching checkpoint + hardening | Non-blocking | P1-2..P1-4 | Kamus data LOS, sitasi pasal, pustaka; build lolos |
| **31 Okt** | **Final QA submit** | Gate | Semua | Checklist §8 terisi 100%, artefak ter-commit |
| **1 Nov 2026** | **SUBMIT PROJECT AKHIR** | Gate | - | Paket zip: kode, `manifest.json`, `metrics.json`, `label-spec.md`, `changelog.md`, video demo ≤5 menit |
| 2–4 Nov 2026 | Seleksi project akhir | - | - | Menutupi pertanyaan juri; tidak ada commit setelah 1 Nov |
| 5–6 Nov 2026 | Dry-run demo | - | - | Rehearsal ≥2×, tiap juri potentiil dapat mereplikasi ≤5 menit |
| **7 Nov 2026** | **DEMO DAY / GRAND FINAL** | Gate | - | Demo 8 menit + 4 menit Q&A; backup offline (video + PDF) |
| 8 Nov 2026 → | Jalur Riset | Post-competition | P1-1 residual, P2-1..P2-3, MHGSL, DP-CTGAN | Roadmap 8 minggu 4 fase (10-simulation-dataset.md:207-213) dijalankan sebagai sprint 8 minggu |

### 3.2 Peta critical path P0 → tanggal

| Dashboard P0 (00-dashboard.md) | Work item | Deadline | Kenapa blocker (bukti) | Kalau gagal |
|---|---|---|---|---|
| P0-1 Tetapkan definisi label fraud/anomali/normal | G-01 | **22 Okt (Hari 1)** | KLM115 skor 0,80 dilabeli fraud; ambang 0,35/0,60/0,80 documented ambigu (03-dataset-registry.md:46). Tanpa ini, semua metrik downstream tidak punya target yang sah (08-training-protocol.md:15-18) | Skor dan label shipped apa adanya; juri bisa-ironic "mana ground truth?" |
| P0-2 Tandai 100 klaim = versi awal, 300 = versi aktif | G-08, G-18, G-19, G-22, **G-14** | **23 Okt (Hari 2)** | 10-simulation-dataset.md:4 masih menyebut 100 sebagai demo awal; 08-training-protocol.md:8 "Deskripsi database masih menyebut 100 klaim dan KLM001 sampai KLM024"; `payload-aegis-jkn.json` `kpi.total_claims: 100` | Angka dataset berbeda antar slide; detection bias |
| P0-3 Lampirkan manifest + skrip untuk **seluruh metrik yang dipublikasikan** | G-02, G-05, G-06, G-21, G-23, **G-10, G-11, G-12** | **27 Okt (Hari 6)** | `data.ts:258-291` adalah konstanta; notebook utama 0 stored output; benchmark dihitung in-sample (sel 13); label training ≠ ground truth (sel 11); adjacency graf dari `sindikat` (`pipeline.py:293-307`); E-07 "Belum tereproduksi pada audit ini" | Klaim utama collapse saat ditanya juri. **Risiko fatal nomor 1** |
| P0-4 Tambahkan tarif acuan + metode overcharge per klaim | G-03, G-04 | **28 Okt (Hari 7)** | 00-dashboard.md:39 "belum dapat direproduksi per klaim"; 02-architecture.md:112 D-04 terbuka; E-11 "Belum dapat direproduksi" | Klaim Rp507.370.000 & Rp14,4 M harus ditarik dari seluruh materi |
| P0-5 Samakan angka operasional yang berbeda | G-07, G-33, **G-09, G-14** | **25 Okt (Hari 4)** | `dataset-explorer.tsx:708` (240/60 vs 189/111), `:764` ("Rp 3,53 M" vs Miliar); deadline salah di `notion-datasets.ts:383,385` | Kepercayaan juri pada integrity data runtuh; temuan "deadline salah" Máximo fatal |
| **P0-6 Kunci satu sumber label untuk training & evaluasi** | G-01, **G-10** | **22 Okt (Hari 1)** | `notebooks/Aegis-JKN.ipynb` sel 11: `y_target` (38 positif) ≠ `y_fraud_gt` (36 positif); mismatch KLM016 & KLM017 (SYND-05, `risiko=high`, `modus=cloning`) | Setiap metrik ditanyakan "mengukur apa?"; angka AUPRC kehilangan makna |
| **P0-7 Rotasi kredensial API** | **G-13** | **26 Okt (Hari 5)** | `backend/.env` memuat `NOTION_TOKEN` (50 B) + `OPENAI_API_KEY` (27 B) live di disk; git-ignored & untracked (aman dari commit), tetapi belum pernah dirotasi | Kredensial bocor (repo publik, Colab, tautan berbagi) → penyalahgunaan akun |
| **P0-8 Hilangkan kolom label dari pembentuk graf** | **G-12** | **24 Okt (Hari 3)** | `pipeline.py:293-307` `sindikat_match`; 65 dari 3.790 sisi semantik (1,7%) berasal dari kolom label | Model "mendeteksi" sindikat karena sindikat ada di graf, bukan karena pola klinis - fatal saat presentasi metode |
| P1-1 Review klinis | G-27 | 29 Okt (non-blocking) | 00-dashboard.md:65; 05-decision-scope.md:26 "Peninjauan klinis diperlukan untuk mendefinisikan ground truth" | Dinyatakan sebagai limitation eksplisit; klaim "ground truth klinis" dihindari |
| P1-2 Data dictionary + perlakuan LOS | G-16 | 30 Okt (non-blocking) | 00-dashboard.md:36 vs data (109 baris bernilai 0); 03-dataset-registry.md:109 | Ditandai known limitation di appendix |
| P1-3 Verifikasi regulasi + pasal | G-24 | 30 Okt (non-blocking) | 04-evidence-matrix.md:29-35, E-01 | Pasal ditambahkan minimal 4 peraturan |
| P1-4 Metadata bibliografi | G-25 | 30 Okt (non-blocking) | E-01..E-12 | 12 baris E-update |
| P1-5 Owner & reviewer | G-26 | 22 Okt (Hari 1) | 00-dashboard.md:69 | Traceability gap terakhir ditutup |
| P2-1..P2-3 | G-29, G-30, G-31, G-32 | ≥8 Nov (post) | 00-dashboard.md:71-73 | Dijadwalkan sprint 8 minggu |

### 3.3 Roadmap harian (Hari 1–14 = 22 Okt – 4 Nov 2026)

| Hari | Tanggal | Tugas | Deliverable | Kriteria selesai |
|---|---|---|---|---|
| 1 | 22 Okt | Kunci definisi label (G-01) + **satu fungsi label untuk training & evaluasi** (G-10) + tetapkan owner (G-26) | `docs/dataset/label-spec.md` v1.0, `backend/src/data/labels.py` `build_target()`, `docs/governance/owners.md` | 13 modus punya definisi case + aturan ambang tertutup; KLM115, KLM016, KLM017 diputuskan eksplisit; `y_train` == `y_eval` pada 300/300 baris; 4 domain punya owner+reviewer bernama |
| 2 | 23 Okt | Bekukan sumber: checksum, seed, split ID, versi (G-05, G-08, G-09, G-14) | `manifest.json`, `docs/dataset/version-registry.md` | SHA-256 3 berkas tercatat (`claims_300_v2.1.csv` = `37cf22369ebf7a3c…`); `seed=20260707` tertulis; ID split train/val/test tercatat; 100 klaim ditandai "v1 arsip"; `kpi.total_claims` payload disamakan ke 300; 31 kolom CSV repo ML + 3 kolom metadata tercatat |
| 3 | 24 Okt | Anti-leakage guard (G-06, G-17) + **graf bebas kolom label** (G-12) | `configs/leakage.yaml`, `tests/test_leakage.py`, `tests/test_graph_features.py` | 7 kolom terlarang + `Alasan` diblokir; test gagal keras bila ada yang bocor; `Alasan` dipindah ke `label_audit.csv`; `sindikat`/`modus`/`risiko`/`status` tidak lagi membentuk edge - 0 sisi dari kolom label |
| 4 | 25 Okt | Rekonsiliasi 12 angka kunci (G-07, G-18, G-19) + payload kanonik (G-14) | `scripts/check_consistency.py` | 0 selisih pada jumlah baris, sebaran label/status/layanan, total biaya, LOS, kontradiksi, sentimen, entitas |
| 5 | 26 Okt | Hentikan overclaim di UI (G-02, G-03, G-21, G-22) + rotasi kredensial (G-13) | Patch `data.ts`, `fraud-ring.tsx`, `roadmap.tsx`, `problem-section.tsx`, `notion-datasets.ts`; `backend/.env` baru | 0 konstanta metrik hardcode di `src/components/mhgsl/`; semua klaim finansial diberi disclaimer "proyeksi asumsi"; semua angka prevalensi memakai 1 konstanta disclaimer; `NOTION_TOKEN` & `OPENAI_API_KEY` sudah dirotasi, nilai lama tidak berlaku |
| 6 | 27 Okt | Baseline XGBoost reproducible (G-05, G-02) + **benchmark out-of-fold** (G-11) | `scripts/train.py`, `docs/experiments/metrics.json`, `docs/experiments/exp-001-baseline.md` | 1 command menghasilkan metrics.json; AUPRC/F1/confusion matrix terhitung; seed & split tertulis; angka UI dibaca dari file ini; tabel benchmark 4 model dihitung dari probabilitas OOF GroupKFold/LOGO - 0 `predict` in-sample; `tests/test_no_insample_eval.py` hijau |
| 7 | 28 Okt | Tarif acuan + overcharge per klaim (G-04) | `data/processed/tariff_reference.csv`, `scripts/compute_overcharge.py` | ≥9 baris tarif; 60 klaim anomali terhitung atau bertanda "tidak dapat dihitung"; output terikat checksum |
| 8 | 29 Okt | Review klinis parsial + model MHGSL level-1 (G-27, G-31) | `docs/dataset/clinical-review.md`, `scripts/train_mhgsl.py` (prototipe) | ≥5 skenario ditandatangani klinis; 1 skrip MHGSL berjalan di atas `claims_300_v2.1.csv` yang sama dengan baseline (bukan `torch.randn`) |
| 9 | 30 Okt | Kamus data, LOS, regulasi, pustaka (G-16, G-24, G-25) | `docs/dataset/data-dictionary.md`, `docs/references/regulations.md` | 4 nilai LOS resmi; 109 baris terpetakan; 4 peraturan dengan nomor pasal + tanggal akses; 12 baris E-update |
| 10 | 31 Okt | Hardening + build + review internal | `npm run build` hijau, `docs/changelog.md`, checklist §8 terisi | 0 error build; 0 item checklist kosong; 1 reviewer bukan anggota tim membaca proposal+artefak dan menyatakan "tidak menemukan klaim tanpa bukti" |
| 11 | 1 Nov | **SUBMIT PROJECT AKHIR** | Paket submit.zip + video demo ≤5 menit | Unggah berhasil, konfirmasi diterima dicatat, checksum zip tercatat di `docs/changelog.md` |
| 12 | 2 Nov | Seleksi: siapkan FAQ & bantahan | `docs/presentasi/faq-10-pertanyaan.md` | 10 pertanyaan teratas + jawaban berbasis `metrics.json` (bukan ingatan) |
| 13 | 3 Nov | Dry-run demo dengan rekrutan non-pengembang | Rehearsal notes | Tim non-pengembang bisa menjalankan demo ≤8 menit tanpa bantuan |
| 14 | 4 Nov | Buffer + backup offline demo | `docs/presentasi/demo-script.md`, `backup.mp4`, `backup.pdf` | Demo berjalan penuh dari repo bersih; 1 alur fallback (video) teruji |

---

## 4. Backlog Terurut

| ID | Gap | Work item | Jenis | Prioritas | Risiko yang diselesaikan | Owner type | Effort | Dependensi | Acceptance criteria (terukur) |
|---|---|---|---|---|---|---|---|---|---|
| B-01 | G-01| Kunci definisi label + aturan ambang | data/governance | P0 | Juri menolak ground truth; metrik tidak sah | Tim data + reviewer klinis | S | - | `label-spec.md` v1.0; 13 modus punya definisi case; ambang `[0.80,1.00]` tertulis; KLM115 diputuskan; 2 tanda tangan reviewer |
| B-02 | G-05, G-09| Bekukan sumber: manifest, checksum, seed, split | data | P0 | Angka berubah diam-diam saat Notion diperbarui (03-dataset-registry.md:100) | Tim data | S | B-01 | `manifest.json` berisi 10 field wajib; SHA-256 3 berkas; `seed=20260707`; ID train/val/test |
| B-03 | G-06, G-17| Kill anti-leakage guard | code/data | P0 | Evaluasi sirkular; klaim AUPRC tidak sah | ML engineer | M | B-02 | `configs/leakage.yaml` (7 kolom + `Alasan`); `tests/test_leakage.py` exit≠0 saat bocor; 0 kolom terlarang di `public/` |
| B-04 | G-02, G-03, G-21, G-22| Stop overclaim UI: metrik & finansial | code/docs | P0 | Overclaim di juri (risiko fatal #1) | Frontend + PM | M | B-02 | 0 konstanta metrik di `src/components/mhgsl/data.ts`; `fraud-ring.tsx:415` & `roadmap.tsx:34` berlabel proyeksi; disclaimer prevalence dari 1 konstanta |
| B-05 | G-07, G-18, G-19| Rekonsiliasi angka operasional | data/docs | P0 | Data terlihat tetapi belum diverifikasi | Tim data | S | - | `check_consistency.py` hijau di 12 angka; `dataset-explorer.tsx:708` & `:764` dikoreksi ke 189/111 & Rp3,53 Miliar |
| B-06 | G-08, G-33| Koreksi deadline kompetisi di data riset | data/governance | P0 | Dokumen salah tunjuk tenggat | PM | S | B-05 | `notion-datasets.ts:383,385` memuat 8 siklus API resmi + URL + tanggal akses; entri `docs/changelog.md` |
| B-07 | G-02| Baseline XGBoost reproducible | code/model | P0 | Angka di layar tanpa model | ML engineer | M | B-02, B-03 | 1 command → `metrics.json`; memuat AUPRC, AUROC, F1, confusion matrix, FPR, seed, split; re-run menghasilkan angka identik (2× konsekuen) |
| B-08 | G-03, G-04| Tarif acuan + overcharge per klaim | data | P0 | Klaim Rp507.370.000 tak terbukti | Tim data + keuangan | M | B-01 | `tariff_reference.csv` ≥9 baris; `compute_overcharge.py` memproses 60 klaim anomali; 100% baris punya nilai/alas an |
| B-09 | G-05| Manifest eksperimen + artefak replikasi | data | P0 | 04-evidence-matrix E-07 belum tereproduksi | Tim ML | M | B-07 | `docs/experiments/exp-001-baseline/` berisi config, prediksi `.npy`, label pembanding, split, `metrics.json`; `manifest.json` tertaut |
| B-10 | G-09| Tambah 3 kolom metadata v2.1 (`seed`, `version`, `timestamp`) | data | P0 | Data tidak dapat ditelusuri versinya; reproduksi mustahil | Tim data | S | B-02 | 3 kolom terisi 100% (`seed`=20260707, `version`=v2.1, `timestamp` ISO-8601); `test_schema.py` asserting no-null pada 34 kolom; `pasien_id`/`faskes_id`/`dokter_id` (40/10/20 entitas) dipakai split group-aware |
| B-11 | G-08, G-33| Perbaikan deadline checklist + artefak submit | governance | P0 | Bintang roadmap salah tunjuk | PM | S | B-06 | 1 checklist T-10..T-0 terisi; 0 artefak menyebut pendaftaran/submit proposal sebagai aksi tersisa |
| B-12 | G-10| Kunci satu fungsi label untuk training DAN evaluasi | code/model | P0 | Metrik yang dilaporkan tidak mengukur apa yang dilatih; juri menemukan AUPRC dihitung atas ground truth berbeda | ML engineer | S | B-01 | `build_target(df)` tunggal di repo ML; `y_train` == `y_eval` pada 300/300 baris; KLM016 & KLM017 diputuskan eksplisit di `label-spec.md`; `tests/test_label_consistency.py` hijau |
| B-13 | G-11| Hitung benchmark dari probabilitas out-of-fold, bukan in-sample | code/model | P0 | Tabel pembanding tidak sah; M-01 jadi tidak bermakna | ML engineer | M | B-12, B-03 | Empat model (XGBoost, MLP, Homogeneous GCN, MHGSL) dievaluasi hanya pada OOF GroupKFold(5)/LOGO dengan split identik; 0 `predict_proba` pada matriks latih di jalur benchmark; `tests/test_no_insample_eval.py` memindai notebook |
| B-14 | G-12| Hapus kolom label dari pembentuk adjacency | code/model | P0 | Struktur graf dibangun dari `sindikat` (65/3.790 sisi semantik) - kebocoran terselubung | ML engineer | M | B-12 | `pipeline.py` tidak lagi membaca `sindikat`/`modus`/`risiko`/`status` saat membuat adjacency; kanal semantik memakai `diagnosis_code`+`prosedur_code`+`faskes_id` ambang 0,55; `tests/test_graph_features.py` asserting 0 sisi dari kolom label; metrik dihitung ulang |
| B-15 | G-13| Rotasi kredensial API + pisahkan `.env` | code/security | P0 | Token Notion & kunci OpenAI live di disk; risiko penyalahgunaan bila pernah dibagikan | Tech lead | S | - | Kedua kredensial dirotasi di provider sebelum 1 Nov; `backend/.env.example` tanpa nilai; `grep -rE "ntn_\|sk-" .` di luar `.env` = 0 hit; `docs/governance/secrets.md` mencatat tanggal rotasi; 0 nilai rahasia di dokumen, commit, atau artefak demo |
| B-16 | G-14| Tetapkan payload kanonik tunggal | data | P0 | Dua salinan payload byte-identik bisa berbeda sinkron; `kpi.total_claims: 100` vs 300 | PM + frontend | S | B-05 | Hanya 1 file payload kanonik di `Aegis-JKN/public/`; salinan `colab/` dihapus atau jadi pointer; `check_consistency.py` membandingkan `kpi.total_claims` vs jumlah baris CSV dan gagal bila beda |
| B-17 | G-15| Tandai notebook data acak sebagai bukan eksperimen | code/model | P1 | `02_model_training.ipynb` pakai `torch.randn`/`torch.randint` - bisa dikutip juri sebagai eksperimen | ML engineer | S | - | Header markdown "DEMO TOY DATA - BUKAN EKSPERIMEN"; file dipindah ke `notebooks/toy/`; 0 artefak paket submit berasal dari notebook tersebut |
| B-18 | G-20| Model audit log + review log | code | P1 | Human-in-the-loop tanpa bukti | Backend engineer | M | B-07 | `ReviewLog` + `AuditEvent` di Prisma; `POST /api/review` menulis baris; `test_review_log.py` hijau |
| B-19 | G-23| API claims & metrics | code | P1 | Frontend baca konstanta | Backend engineer | M | B-10 | `GET /api/claims` → 300 baris; `GET /api/metrics` → `metrics.json`; 1 test integrasi |
| B-20 | G-21| Label jadi heuristik demo | code | P1 | Klaim "Hitung Skor MHGSL" menyesatkan | Frontend | M | B-04 | Tombol berlabel "heuristik demo, bukan model terlatih"; `data-uploader.tsx:203` diberi catatan |
| B-21 | G-22| Disclosure prevalensi terpusat | code | P1 | Prevalensi 12%vs3-7% membingungkan | Frontend | S | B-04 | 1 konstanta disclaimer dipakai di ≥5 lokasi; 0 kemunculan angka prevalensi tanpa disclaimer |
| B-22 | G-16, G-28| Data dictionary + kebijakan LOS | docs/data | P1 | 109 baris ambigu | Tim data | S | B-05 | 4 nilai LOS; 109 baris terpetakan `N/A` dengan justifikasi layanan; `test_los_policy.py` asserting 0 nilai 0 |
| B-23 | G-24| Sitasi regulasi + pasal | docs | P1 | Klaim kepatuhan tak substantif | Researcher | S | - | ≥4 peraturan dengan nomor pasal, URL portal resmi, tanggal akses, status berlaku |
| B-24 | G-25| Pustaka + update 12 baris evidence matrix | docs | P1 | Klaim tanpa sumber | Researcher | S | B-23 | E-01..E-12 punya status final; 0 "Perlu Verifikasi" |
| B-25 | G-27| Review klinis skenario | governance | P1 | Ground truth tanpa validasi klinis | Reviewer klinis eksternal | M | B-01, B-27 | ≥5 skenario ditandatangani; ketidaksetujuan dicatat sebagai limitation |
| B-26 | G-26| Perubahan database Notion → Git | governance | P1 | Notion rapuh sebagai source of truth | PM + tech lead | L | B-05 | Struktur §7 terimplementasi; `data/raw/` berisi 300 baris + checksum; Notion jadi read-only doc |
| B-27 | G-26| Source of truth & hak akses | governance | P1 | Update merusak data | PM | S | B-26 | `docs/governance/sot.md` menyebut Notion=dokumen, Git+CSV=truth, skrip=pipeline; editor Notion dibatasi |
| B-28 | G-30| Release notes + pisah artefak | governance | P2 | Artefak bercampur | PM | S | B-26 | `docs/changelog.md` ≥1 entri; `docs/experiments/`, `docs/presentasi/`, `docs/arsip/` ada |
| B-29 | G-29| Uji penerimaan UI + SUS | UX | P2 | Klaim SUS 82,5 tanpa artefak | UX researcher | M | B-04 | Protokol + lembar 5 peserta tersimpan; skor dengan n & tanggal, atau klaim dihapus |
| B-30 | G-32| Struktur repo + seed generator | code | P2 | Tidak reproducible | ML engineer | M | B-02 | Direktori §7 ada; seed generator mereproduksi 300 baris dengan SHA-256 identik CSV |
| B-31 | G-31| MHGSL lengkap + XAI per-saluran + uji tambah nilai | model | P2 | Desain belum terbukti unggul | ML engineer | L | B-07, B-10, B-13 | `train_mhgsl.py` menghasilkan AUPRC ≥ baseline pada split group-aware sama; jika tidak, dicatat sebagai negative result (bukan disembunyikan) |

---

## 5. Risk Register

| ID | Risiko | Kategori | Probabilitas | Dampak | Skor | Mitigasi | Owner | Early warning signal |
|---|---|---|---|---|---|---|---|---|
| R-01 | Overclaim di juri: angka AUPRC 0,91 / penghematan Rp14,4 M ditanya sumbernya dan tidak ada | Reputasi/kelayakan | Tinggi | Sangat tinggi | Kritis | B-04 + B-07 + B-09 + B-13: hapus konstanta, lampirkan `metrics.json` **berbasis OOF**, latih fallback; semua angka finansial diberi disclaimer | PM + ML engineer | Juri membuka `data.ts` dan bertanya "ini hasil run mana?"; tidak ada `metrics.json` di repo; tabel benchmark dihitung in-sample |
| R-02 | Model tidak outperform baseline XGBoost pada split group-aware yang sama | Teknis | Sedang–Tinggi | Tinggi | Tinggi | Trigger M-01 (lihat §6): fallback otomatis ke XGBoost + fitur graf turunan; negative result ditulis sebagai temuan, bukan disembunyikan. **Catatan: sebelum B-13 selesai, M-01 belum dapat dievaluasi sama sekali** | ML engineer | AUPRC MHGSL (OOF) < AUPRC XGBoost (OOF) pada fold yang sama; tabel benchmark masih in-sample |
| R-03 | Data leak: `Alasan`/label turunan masuk matriks fitur **atau** menjadi sisi edge graf | Teknis | Sedang | Sangat tinggi | Tinggi | B-03 + B-14: `configs/leakage.yaml` (fitur) + `configs/graph_inputs.yaml` (edge) + 2 test gagal keras; review manual matriks fitur dan fungsi adjacency sebelum run | ML engineer | `tests/test_leakage.py` di-skip atau di-comment; daftar fitur berubah tanpa review; `sindikat` masih dibaca di fungsi adjacency |
| R-04 | Waktu habis: 10 hari untuk 8 P0 + demo | Operasional | **Tinggi** | Sangat tinggi | Kritis | Critical path dibatasi 8 P0 (P0-1..P0-8); B-31 dan seluruh P2 di-defer; cutoff keras 30 Okt untuk fitur baru; B-12..B-14 dan B-15 boleh dikerjakan paruh hari | PM | 1 P0 belum hijau pada 26 Okt; >2 P0 belum hijau pada 28 Okt |
| R-05 | Dataset quality: 109 baris LOS ambigu, 1 baris `Alasan` kosong, label batas 0,80 | Data | Sedang | Tinggi | Tinggi | B-22 + B-01 + checker konsistensi | Tim data | `check_consistency.py` merah; `test_los_policy.py` gagal |
| R-06 | Privasi/ketentuan: data sintetis dibaca sebagai data peserta nyata | Kepatuhan | Sedang | Sangat tinggi | Tinggi | B-21 + B-04: disclaimer "simulasi sintetis, prevalensi oversampled" di setiap layar metrik; jangan masukkan data DM nyata ke app | PM | Ada baris DM realistis (nomor peserta/tanggal lahir) di CSV yang di-commit |
| R-07 | Ketergantungan Notion sebagai source of truth: update Notion merusak angka tanpa jejak | Operasional/data | Tinggi | Tinggi | Tinggi | B-26 + B-27: Notion jadi dokumen, Git+CSV+checksum jadi truth, skrip jadi pipeline; snapshot Notion pernah berubah tanpa changelog | PM + tech lead | `_last_edited` pada `claims_v2_live.csv` berubah tanpa commit Git; tidak ada checksum |
| R-08 | Dokumentasi salah (deadline 14 Sep di `notion-datasets.ts:383`) | Operasional | **Terbukti terjadi** | Tinggi | Tinggi | B-06: koreksi + `docs/changelog.md`; konfirmasi timeline dari API resmi satu kali | PM | Row riset bertanggal kadaluarsa |
| R-09 | Demo gagal di tempat (jaringan/offline/dependency) | Teknis | Sedang | Tinggi | Tinggi | Backup: video mp4 + PDF + repo offline; re-run demo di mesin bersih 2× | Frontend | Demo butuh internet saat demo |
| R-10 | Tim non-pengembang tidak bisa menjalankan demo (knowledge transfer) | Operasional | Sedang | Tinggi | Tinggi | `docs/presentasi/demo-script.md` langkah-per-langkah; dry-run Hari 13 dengan rekrutan | PM | Rehearsal butuh bantuan penulis kode |
| R-11 | Klasifikasi "-" by jReality: demo menampilkan graf sinetik mini (12 node, 18 edge) sebagai "graf JKN" | Reputasi | Sedang | Tinggi | Tinggi | Label eksplisit "graf demonstrasi 12 simpul"; tampilkan graf 300 klaim nyata sebagai tambahan | Frontend | Penampil menampilkan 12 simpul saat Claims 300 |
| R-12 | Regulasi: penggunaan data DM realistis tanpa dasar izin | Kepatuhan | Rendah | Sangat tinggi | Sedang–Tinggi | Jangan pakai file DM di app; hanya synthetic; tulis `docs/governance/privacy.md` | PM | Ada `PSTV01`/nomor peserta di data yang di-deploy |
| R-13 | Klaim "kurasi klinis tervalidasi" tanpa reviewer klinis | Reputasi | Sedang | Tinggi | Tinggi | B-25; sampai reviewer ada, tulis "skenario disusun tim, belum ditinjau klinis" | PM | Dokumen menyebut "tervalidasi klinis" |
| R-14 | Version drift dataset: app 300 baris, `payload-aegis-jkn.json` 100 baris. File yang sama(byte-identik, SHA-256 `9c8cc58a697642e0…`) ada di DUA tempat: `Aegis-JKN/public/` dan `mechine-learning-deep-learning/colab/`, sehingga ada dua salinan payload yang bisa berbeda sinkron | Data | **Terbukti terjadi** | Sedang | Sedang | B-05 checker mengbandingkan kedua salinan + app; hapus payload lama atau samakan ke v2.1; designate 1 file kanonik | PM | `kpi.total_claims: 100` vs 300 di app; `sha256sum` kedua salinan payload berbeda |
| R-15 | Juri paham split leakage (entitas sama di train & test) | Teknis | Sedang | Tinggi | Tinggi | B-13 + GroupKFold(group=`pasien_id`) + LeaveOneGroupOut(group=`faskes_id`) pada benchmark OOF | ML engineer | Split file hanya berisi ID klaim, bukan ID grup |
| R-16 | **Metrik yang dilaporkan tidak sah**: model dilatih pada `y_target` tetapi AUPRC dihitung terhadap `y_fraud_gt`; KLM016 & KLM017 dilatih sebagai fraud tetapi dihitung sebagai non-fraud | Teknis/metodologi | **Terbukti terjadi** | Sangat tinggi | **Kritis** | B-12: satu fungsi `build_target(df)` untuk training & evaluasi; `tests/test_label_consistency.py`; seluruh angka metrik yang sudah dipublikasikan ditarik sampai diperbaiki | ML engineer + PM | `set(y_train) != set(y_eval)` pada ≥1 baris; selisih `y_target.sum()` ≠ `y_fraud_gt.sum()` | 
| R-17 | **Tabel benchmark dievaluasi in-sample**: 4 model dilatih & diprediksi pada matriks yang sama; probabilitas OOF GroupKFold yang sudah ada tidak dipakai | Teknis/metodologi | **Terbukti terjadi** | Sangat tinggi | **Kritis** | B-13: benchmark hanya dari OOF GroupKFold(5)/LOGO pada split identik; `tests/test_no_insample_eval.py` memindai notebook; M-01 dihitung dari OOF | ML engineer | `fit(X)` lalu `predict(X)` pada variabel sama di sel benchmark; angka AUPRC OOF dan in-sample berbeda >0,02 | 
| R-18 | **Struktur graf diturunkan dari label `sindikat`** (65/3.790 sisi semantik) → model MHGSL bisa "mendeteksi" sindakat karena sindikat ada di edge, bukan dari pola klinis | Teknis/kebocoran | **Terbukti terjadi** | Tinggi | **Kritis** | B-14: hapus kolom label dari pembentuk adjacency; kanal semantik hanya `diagnosis_code`+`prosedur_code`+`faskes_id` (ambang 0,55); `tests/test_graph_features.py`; hitung ulang seluruh metrik | ML engineer | `sindikat` masih muncul di fungsi adjacency; AUPRC turun >0,05 setelah dihapus (tanda bahwa model VIDIP pada label) | 
| R-19 | **Kredensial live di disk** (`NOTION_TOKEN`, `OPENAI_API_KEY`) lalu di-share di repo publik/Colab/tautan | Keamanan | Sedang | Sangat tinggi | Tinggi | B-15: rotasi di provider sebelum 1 Nov; `backend/.env.example` tanpa nilai; `docs/governance/secrets.md`; 0 nilai rahasia di dokumen/commit/demo | Tech lead | Secret scanner finding; token dipakai dari IP tak dikenal; kredensial pernah muncul di log Colab |

---

## 6. Metrics & Trigger

| ID | Metrik | Ambang | Tindakan (stop / rollback / fallback) |
|---|---|---|---|
| M-01 | AUPRC MHGSL vs AUPRC XGBoost baseline, **keduanya dari probabilitas out-of-fold** pada split group-aware identik, seed sama | MHGSL < baseline XGBoost | **Fallback:** ship XGBoost + fitur graf turunan. Label di UI "desain belum terbukti unggul". Jangan tampilkan chart MHGSL sebagai superiority. Dokumentasikan sebagai negative result |
| M-02 | AUPRC MHGSL absolut | < 0,60 | Rollback ke rule engine; hapus klaim MHGSL dari materi demo |
| M-03 | Recall fraud pada antrean ≤20% (36 klaim fraud) | < 90% (i.e. < 32/36) | Turunkan ambang antrean ke 30% atau Statement trade-off; tulis "recall vs beban review" di slide |
| M-04 | Hit-rate per sindikat SYND-01..SYND-09 | 0 sindikat dengan hit-rate 0 | Tutup klaim "deteksi semua modus"; tampilkan heatmap mana yang miss + alasan |
| M-05 | Konsistensi XAI: SHAP vs kolom `Alasan` | < 80% klaim dengan 3 fitur teratas SHAP yang disebut di `Alasan` | Matikan SHAP panel, ganti tabel fitur teratas; jangan klaim SHAP "sejalan" |
| M-06 | Kebocoran fitur | `tests/test_leakage.py` exit≠0 saat kolom terlarang muncul | Blocker keras: jalankan ulang seluruh benchmark; angka yang sudah dipublikasikan dicabut |
| M-07 | Konsistensi angka UI vs data | 12 angka kunci, selisih ≠ 0 | Blocker keras: tidak boleh submit sampai hijau |
| M-08 | Baris gagal checker modus (mis. modus di luar 13, sindikat tanpa modus) | > 0% dari 300 baris (3 baris) | Regenerasi dataset dengan seed tetap + perbaiki generator; checksum berubah wajib |
| M-09 | Baris gagal validasi skema v2.1 (6 kolom wajib) | > 0 baris null | Regenerasi + `test_schema.py` hijau |
| M-10 | Konsistensi label vs ambang | ≥1 baris di ambang 0,80/0,60/0,35 | Terapkan aturan kelas tertutup; catat kasus KLM115 di `label-spec.md` |
| M-11 | Porsi klaim dengan `Alasan` terstruktur | ≥ 299/300 | Isi KLM031; bila tidak, keluar 1 baris dari benchmark dan nyatakan |
| M-12 | Prevalence gap UI | 0 kemunculan angka prevalensi tanpa disclaimer | Bloker keras sebelum submit |
| M-13 | Overclaim tersisa di `src/` | 0 konstanta metrik; 0 klaim finansial tanpa disclaimer | Bloker keras sebelum submit |
| M-14 | Checklist submission §8 | 100% terisi | Bloker keras: tidak submit |
| M-15 | Waktu build + smoke test | > 15 menit | Hapus fitur non-esensial, jalankan ulang |
| M-16 | Uji skeptis (reviewer non-tim) | ≥1 reviewer menyatakan "tidak menemukan klaim tanpa bukti" | Perbaiki temuan reviewer sebelum submit |
| M-17 | Jumlah file Notion dump di repo | 0 file `.md` dump mentah | Bersihkan sebelum submit |
| M-18 | Demo dry-run | Tim non-pengembang gagal > 2× | Perbaiki `demo-script.md`, ulang sampai 1× berurutan |
| M-19 | Derajat konsistensi preprocess train vs inferensi | Selisih 0 pada 12 transformasi | Stop deploy; sambungkan pipeline inferensi ke pipeline training |
| M-20 | Budget waktu tersisa hari ini | < 2 jam kerja tersisa tanpa P0 hijau | Umumkan P0 shipped apa adanya + limitation list; hentikan fitur baru |
| M-21 | **Konsistensi label training vs evaluasi** | `y_train` ≠ `y_eval` pada ≥1 baris (saat ini 2: KLM016, KLM017) | **Bloker keras: tidak boleh submit.** Perbaiki `build_target()`, hitung ulang seluruh metrik, cabut angka yang sudah dipublikasikan |
| M-22 | **Benchmark dihitung out-of-fold** | 1 model pun di `predict` pada matriks latih di jalur benchmark | **Bloker keras: tidak boleh submit.** Ganti sumber probabilitas tabel benchmark dengan OOF GroupKFold/LOGO; M-01 hanya sah bila computed dari OOF |
| M-23 | **Sisi graf dari kolom label** | ≥1 sisi edge berasal dari `sindikat`/`modus`/`risiko`/`status` | **Bloker keras.** Hapus dari adjacency, hitung ulang metrik, catat sebagai koreksi metodologi di changelog |
| M-24 | **Kredensial live masih dipakai** | `NOTION_TOKEN`/`OPENAI_API_KEY` belum dirotasi pada 30 Okt | Rotasi paksa; bila token pernah bocor, buat insiden keamanan dan ganti seluruh kredensial repo ML |

---

## 7. Rekomendasi Arsitektur Data & Migrasi dari Notion

### 7.1 Prinsip

Notion saat ini menjalankan tiga peran sekaligus: **editor dokumen**, **database**, dan **source of truth**. Ketiganya rapuh: tidak ada kolom formula, tidak ada validasi skema, tidak ada checksum, dan satu edit bisa merusak angka yang sudah dipublikasikan (00-dashboard.md:39-40; 03-dataset-registry.md:100 "Hasil tidak boleh berubah diam-diam ketika database Notion diperbarui").

Pemisahan peran yangdiusulkan:

| Peran | Dipindah ke | Aturan |
|---|---|---|
| Dokumen naratif, proposal, catatan riset | Notion (read-mostly) | Editor tetap di Notion; **tidak boleh** diedit setelah publish tanpa changelog |
| Data tabular (300 klaim, tarif, ground truth) | Git + CSV/JSON + checksum | Setiap perubahan = 1 commit; checksum wajib; kolom terlarang tidak boleh masuk repo |
| Pipeline, validasi, komputasi metrik | Skrip Python di `scripts/` | Skrip adalah satu-satunya sumber angka; output written ke `docs/experiments/` |
| Audit & keputusan human | Postgres (via Prisma) | `ReviewLog`, `AuditEvent` - append-only |

### 7.2 Struktur repo yang disarankan

```
aegis-jkn/
├── configs/
│   ├── leakage.yaml            # daftar kolom terlarang + aturan kebocoran
│   ├── thresholds.yaml         # ambang label 0.35/0.60/0.80 (sumber tunggal)
│   ├── split.yaml              # seed, fold, group column
│   └── text.yaml               # toggle Gemini / fallback heuristik
├── data/
│   ├── raw/
│   │   ├── claims_300_v2.1.csv          # snapshot Notion, immutable
│   │   ├── claims_300_v2.1.csv.sha256
│   │   ├── edges_v2.1.json              # 70+ edge graf heterogen
│   │   ├── text_gt_v2.1.csv             # ground truth sentimen & kontradiksi
│   │   └── leakage_blocklist.yaml       # (alias configs/leakage.yaml)
│   └── processed/
│       ├── claims_300_v2.1_clean.csv
│       ├── features_300.parquet
│       ├── graph_hetero.pt
│       ├── tariff_reference.csv
│       ├── metadata.json                # jumlah baris, seed, versi, timestamp
│       └── label_audit.csv              # ground_truth_fraud, evidence_source,
│                                        # reviewer_1, reviewer_2, adjudication_date,
│                                        # label_confidence, exclusion_reason
├── scripts/
│   ├── seed/
│   │   └── generate_claims.py   # deterministik, seed 20260707
│   ├── validate_schema.py
│   ├── check_consistency.py     # 12 angka kunci vs data & UI
│   ├── compute_overcharge.py
│   ├── train.py                 # baseline XGBoost
│   ├── train_mhgsl.py           # MHGSL (Jalur Riset)
│   └── compute_shap.py
├── tests/
│   ├── test_leakage.py          # gagal keras bila kolom terlarang masuk fitur
│   ├── test_schema.py
│   ├── test_los_policy.py
│   ├── test_review_log.py
│   ├── test_metrics_provenance.py
│   └── test_checksums.py
├── docs/
│   ├── dataset/
│   │   ├── label-spec.md
│   │   ├── data-dictionary.md
│   │   ├── version-registry.md
│   │   ├── clinical-review.md
│   │   └── icd-sentinel-policy.md
│   ├── experiments/
│   │   ├── exp-001-baseline/
│   │   │   ├── config.yaml
│   │   │   ├── predictions.npy
│   │   │   ├── metrics.json
│   │   │   └── REPORT.md
│   │   ├── baseline-2026-10-22.md
│   │   └── usability/
│   ├── governance/
│   │   ├── owners.md
│   │   ├── sot.md
│   │   └── privacy.md
│   ├── references/
│   │   └── regulations.md
│   ├── presentasi/
│   │   ├── demo-script.md
│   │   └── faq-10-pertanyaan.md
│   ├── changelog.md
│   └── arsip/
├── prisma/schema.prisma         # + ReviewLog, AuditEvent, Claim
└── src/                          # Next.js - hanya membaca data/processed via API
```

**Repo ketiga: `N:\HEALTHKATHON\mechine-learning-deep-learning\`** (remote `github.com/biezz-2/Aegis-JKN-mechine-learning-deep-learning.git`) adalah basis kode ML dan **tidak boleh dihapus**. Struktur target menyatukan repo app dan repo ML di bawah satu struktur; bila repositori tidak digabung (mempertahankan 3 remote), maka struktur di atas diimplementasikan **di dalam repo ML** dan repo app hanya consuming API + artefak build.

Isi repo ML saat ini (hasil inventaris 22 Okt 2026):

```
mechine-learning-deep-learning/
├── datasets/
│   ├── claims_300_v2.1.csv      # 248.154 B, 300 baris, 31 kolom, TRACKED di git
│   ├── claims_db.json           # 4.042.592 B (dump Notion mentah)
│   └── dataset_db.json          # 182.797 B
├── backend/
│   ├── .env                     # KREDENSIAL LIVE - git-ignored, untracked (lihat G-13)
│   ├── .env.example             # 763 B, nama variabel tanpa nilai
│   ├── requirements.txt
│   ├── models/mhgsl_model.pth   # 164.825 B (checkpoint, provenance tidak ada)
│   ├── data/oasis_results.json  # 29.511 B
│   └── src/                     # 1.818 baris Python
│       ├── data/pipeline.py     # 352  (LEAKAGE_COLUMNS:37-40, seed:103, adjacency:247-320)
│       ├── data/notion_client.py# 93
│       ├── models/mhgsl.py      # 382
│       ├── api/main.py          # 426  (6 endpoint REST + 1 WebSocket)
│       ├── oasis/simulation.py  # 338
│       ├── oasis/agent_mapper.py# 90
│       ├── utils/config.py      # 54
│       └── test_self_check.py   # 65
├── notebooks/
│   ├── Aegis-JKN.ipynb          # 125.043 B, 22 sel, **0 stored output**
│   ├── 02_model_training.ipynb  # 5.775 B, data acak - bukan eksperimen (G-15)
│   ├── 01_data_exploration.ipynb, 03_oasis_simulation.ipynb
│   ├── build_notebook.py, validate_notebook.py
├── colab/
│   ├── Aegis_JKN_FIXX.ipynb     # 720.813 B, 6 sel, 13 output (setup Ollama)
│   ├── payload-aegis-jkn.json   # byte-identik dengan Aegis-JKN/public/ (G-14)
│   └── Hasil simulasi dari 300 dataset notion.pdf  # 3.800.507 B, 16 hlm, IMAGE-ONLY
└── (TIDAK ADA) configs/ scripts/ tests/ docs/experiments/ data/raw/ data/processed/
```

### 7.3 Langkah migrasi konkret

| # | Langkah | Output | Kriteria selesai |
|---|---|---|---|
| MS-01 | Snapshot Notion satu kali ke `data/raw/` + hitung SHA-256 | `claims_300_v2.1.csv`, `.sha256` | Checksum file identik dengan hash di `manifest.json` |
| MS-02 | Kunci ambang label ke `configs/thresholds.yaml`; hapus ambang duplikat di dokumen | `thresholds.yaml` | 0 kemunculan angka 0,35/0,60/0,80 di luar `thresholds.yaml` pada kode & docs |
| MS-03 | Tulis `configs/leakage.yaml` (7 kolom terlarang + `Alasan`) | `leakage.yaml` | `tests/test_leakage.py` mendeteksi injeksi kolom terlarang dan exit≠0 |
| MS-04 | Pisahkan `Alasan`/`Catatan` ke `label_audit.csv` | `label_audit.csv` 300 baris | `claims_300_v2.1_clean.csv` 0 kolom `Alasan` |
| MS-05 | Tambah 3 kolom metadata v2.1 (`seed`, `version`, `timestamp`) - `pasien_id`/`faskes_id`/`dokter_id` sudah ada di CSV repo ML | CSV terisi | `test_schema.py` asserting no-null pada 34 kolom; `pasien_id`/`faskes_id`/`dokter_id` ada di 100% baris |
| MS-06 | Tulis `scripts/check_consistency.py` (12 angka kunci) | skrip | Skrip hijau pada repo bersih; merah pada 1 angka yang sengaja diubah (uji negatif) |
| MS-07 | Tulis `scripts/seed/generate_claims.py` deterministik | generator | SHA-256 output == SHA-256 `claims_300_v2.1.csv` |
| MS-08 | Bangun baseline `scripts/train.py` → `docs/experiments/exp-001-baseline/` | `metrics.json` | 2× run berturut-turut menghasilkan metrik identik |
| MS-09 | Arahkan UI agar membaca `metrics.json` via `GET /api/metrics` | API + patch UI | 0 konstanta metrik di `src/components/mhgsl/` |
| MS-10 | Kunci Notion: hanya dokumen; label DB "read-only arsip"; tempel pointer ke Git | halaman Notion terupdate | Halaman Notion memuat tautan commit + checksum |
| MS-11 | Pindahkan dump korpus Notion keluar repo ke `docs/arsip/` (tanpa `.md` mentah di root) | tree bersih | 0 file dump mentah di repo |
| MS-12 | Tambah `docs/changelog.md` + aturan PR: wajib lampirkan `metrics.json` bila UI menampilkan angka | changelog + CONTRIBUTING | ≥1 entri changelog per perubahan angka di UI |
| MS-13 | **Pindahkan repo ML ke dalam struktur §7.2** (atau dokumentasikan pemisahan 3 remote secara eksplisit) | `docs/governance/repo-map.md` | Setiap artefak eksperimen punya 1 lokasi kanonik; 0 duplikasi payload (G-14); `repo-map.md` memetakan repo app ↔ repo ML ↔ repo induk |
| MS-14 | **Konsolidasikan sumber label** ke `backend/src/data/labels.py` (`build_target`) dan hapus definisi label ganda di notebook | `labels.py` + notebook yang memakainya | `y_train` == `y_eval` pada 300/300 baris; 0 baris beda; `tests/test_label_consistency.py` hijau |
| MS-15 | **Bangun `scripts/` evaluasi out-of-fold** di repo ML: `scripts/train_baseline.py`, `scripts/evaluate_oof.py`, `scripts/train_mhgsl.py`, `scripts/compute_metrics.py` | `scripts/` + `docs/experiments/` | 1 command → `metrics.json`; tabel benchmark hanya dari OOF; 2× run berturut-turut menghasilkan metrik identik |
| MS-16 | **Terapkan blokir dua lapis**: kolom terlarang (G-06) DAN kolom yang tidak boleh membentuk edge (G-12) | `configs/leakage.yaml` (features) + `configs/graph_inputs.yaml` (edge builders) | 2 test terpisah hijau: `test_leakage.py` (fitur) dan `test_graph_features.py` (edge) |
| MS-17 | **Rotasi kredensial + pindahkan konfigurasi ke env saja** | `.env` baru + `docs/governance/secrets.md` | Token lama tidak berlaku; `grep -rE "ntn_\|sk-" .` di luar `.env` = 0 hit; 0 nilai rahasia di commit/dokumen/demo |

**Pola kerja yang harus berlaku mulai 23 Okt:** tidak ada angka baru yang masuk ke UI tanpa file sumber di `docs/experiments/`. Ini satu-satunya cara menjawab pertanyaan juri "itu hasil run mana?" dalam 10 detik.

---

## 8. Checklist Submission Healthkathon (relatif T-10 → T-0)

Basis: submit project akhir **1 Nov 2026** (T-0), demo day **7 Nov 2026** (T+6).

| T-x | Tanggal | Tugas | Deliverable | Status |
|---|---|---|---|---|
| T-10 | 22 Okt | Kunci definisi label + owner | `label-spec.md`, `owners.md` | ☐ |
| T-10 | 22 Okt | Baseline audit angka kunci | `baseline-2026-10-22.md` | ☐ |
| T-9 | 23 Okt | Manifest, checksum, seed, split, payload kanonik | `manifest.json`, `version-registry.md` | ☐ |
| T-8 | 24 Okt | Anti-leakage guard aktif + graf bebas kolom label | `leakage.yaml`, `test_leakage.py`, `test_graph_features.py` | ☐ |
| T-7 | 25 Okt | Rekonsiliasi 12 angka | `check_consistency.py` hijau | ☐ |
| T-6 | 26 Okt | Hentikan overclaim UI + koreksi deadline + rotasi kredensial | patch UI, `changelog.md`, `docs/governance/secrets.md` | ☐ |
| T-5 | 27 Okt | Baseline XGBoost reproducible + benchmark out-of-fold | `exp-001-baseline/metrics.json`, `test_no_insample_eval.py` | ☐ |
| T-4 | 28 Okt | Tarif acuan + overcharge | `tariff_reference.csv`, `compute_overcharge.py` | ☐ |
| T-3 | 29 Okt | Review klinis parsial | `clinical-review.md` | ☐ |
| T-2 | 30 Okt | Kamus data, LOS, regulasi, pustaka, changelog | 4 dokumen | ☐ |
| T-1 | 31 Okt | Build + review skeptis non-tim + video demo | build hijau, review notes, `demo.mp4` | ☐ |
| **T-0** | **1 Nov** | **Unggah project akhir** | bukti unggah + checksum zip di changelog | ☐ |
| T+1..T+3 | 2–4 Nov | Seleksi project akhir, siapkan FAQ | `faq-10-pertanyaan.md` | ☐ |
| T+4..T+5 | 5–6 Nov | Dry-run demo ×2 + backup offline | `demo-script.md`, `backup.mp4`, `backup.pdf` | ☐ |
| T+6 | 7 Nov | **Demo day / Grand Final** | presentasi 8 menit + Q&A 4 menit | ☐ |
| T+7 | 8 Nov | Retrospektif + buka Jalur Riset | `docs/changelog.md` entri baru | ☐ |

### 8.1 Checklist isi project akhir (yang harus ada di dalam paket T-0)

| # | Komponen | Kriteria ada & benar |
|---|---|---|
| 1 | Kode aplikasi | Repo buildable dari `npm ci && npm run build` tanpa error, ≤ 15 menit |
| 2 | **Kode repo ML** | `backend/src/` (1.818 baris) ikut terlampir, plus `scripts/` evaluasi out-of-fold; **bukan** hanya kode UI |
| 3 | Dataset v2.1 | 300 baris + 31 kolom (termasuk `pasien_id`/`faskes_id`/`dokter_id`) + 3 kolom metadata (`seed`, `version`, `timestamp`) + SHA-256 `37cf22369ebf7a3c…` di `manifest.json` |
| 4 | Manifest eksperimen | `docs/experiments/exp-001-baseline/` lengkap (config, prediksi OOF, metrics, split, REPORT) |
| 5 | Definisi label | `label-spec.md` v1.0 + tanda tangan 2 reviewer + keputusan eksplisit KLM115, KLM016, KLM017 |
| 6 | Bukti anti-leakage | `configs/leakage.yaml` + `tests/test_leakage.py` + `tests/test_graph_features.py` (lulus = tidak ada kolom terlarang di fitur maupun di edge) |
| 7 | **Bukti konsistensi label** | `tests/test_label_consistency.py` lulus: `y_train` == `y_eval` pada 300/300 baris |
| 8 | **Bukti evaluasi out-of-fold** | `tests/test_no_insample_eval.py` lulus; tabel benchmark hanya dari OOF GroupKFold/LOGO; `predictions_oof.npy` terlampir |
| 9 | Konsistensi angka | `check_consistency.py` hijau, 0 selisih pada 12 angka |
| 10 | Keterbatasan & disclaimer | 1 dokumen yang menyatakan: data sintetis, prevalensi oversampled, koreksi metodologi (label & in-sample), MHGSL belum terbukti unggul bila M-01 terpicu |
| 11 | Video demo | ≤ 5 menit, 1080p, tanpa audio wajib, subtitle |
| 12 | Slide | ≤ 20 slide; tiap angka di slide punya file sumber di `docs/experiments/` |
| 13 | Changelog | `docs/changelog.md` memuat entri 22 Okt 2026 (koreksi deadline + rekonsiliasi angka + koreksi metodologi) |
| 14 | **Tidak ada rahasia** | 0 nilai `NOTION_TOKEN`/`OPENAI_API_KEY` di paket; `.env` tidak ikut terlampir |

---

## 9. Catatan Metodologis

1. Semua baris "Bukti" menunjuk ke file yang dibaca langsung pada 22 Okt 2026, bukan ke ingatan dokumen. Verifikasi dapat diulang dengan `python -I analysis/reports/scripts/04_audit.py`.
2. Timeline Healthkathon diambil dari API resmi (`siklus/list`, dicek 22 Okt 2026), bukan dari baris riset Notion yang terbukti kedaluwarsa (`src/data/notion-datasets.ts:383,385`).
3. Angka backlog (jumlah baris, sebaran label/status/layanan, total biaya, LOS, kontradiksi, entitas, sentimen) dihitung ulang langsung dari `corpus/claims_v2_live.csv`; `analysis/reports/scripts/04_audit_results.json` memuat hasil yang sama dan dapat dibandingkan silang.
4. Repo `N:\HEALTHKATHON\Aegis-JKN\` diperlakukan read-only; tidak ada file yang diubah dalam proses menyusun dokumen ini.
5. Repo `N:\HEALTHKATHON\mechine-learning-deep-learning\` juga dibaca read-only. Verifikasi G-10/G-11/G-12 dilakukan dengan **replikasi ulang** pada `datasets/claims_300_v2.1.csv` (bukan hanya membaca kode): jumlah positif `y_target`=38, `y_fraud_gt`=36, himpunan selisih = {KLM016, KLM017}; SHA-256 kedua salinan payload dibandingkan dengan `hashlib`.
6. Batasan eksplisit: seluruh temuan bertumpu pada data sintetis 300 baris. Konsep "9 sindikat", "13 modus", dan "36 klaim fraud" adalah desain skenario, bukan temuan empiris terhadap JKN; batas ini wajib disebut di materi submit.
7. Nilai rahasia pada `backend/.env` **tidak pernah disalin ke dokumen ini**. Hanya nama variabel, panjang nilai, dan status git-ignore yang dicatat.
8. Revisi 2.1 (bagian §10) membatalkan dua klaim pada Revisi 2.0. Klaim lama tetap tercatat di tabel §10.2 agar jejak audit tetap dapat ditelusuri, tetapi **tidak boleh dipakai sebagai dasar keputusan lagi**.


---

## 10. Revisi: Repositori Eksperimen Terpisah

Bagian ini membatalkan dan mengoreksi Revisi 2.0 pada dua klaim yang terbukti salah, dan menambahkan enam temuan baru yang hanya terlihat setelah repo ketiga diperiksa.

### 10.1 Tiga repositori, bukan satu

| Repo | Peran | Isi terverifikasi | Status |
|---|---|---|---|
| `N:\HEALTHKATHON\Aegis-JKN\` | Repo **app** (Next.js 16) | UI demo, komponen MHGSL, `src/data/notion-datasets.ts` (300 record inline), `public/payload-aegis-jkn.json` | read-only untuk audit ini |
| `N:\HEALTHKATHON\mechine-learning-deep-learning\` | Repo **ML/eksperimen** (git, remote `github.com/biezz-2/Aegis-JKN-mechine-learning-deep-learning.git`) | `backend/src/` 1.818 baris Python, `backend/models/mhgsl_model.pth`, `backend/data/oasis_results.json`, `datasets/claims_300_v2.1.csv` (31 kolom, tracked), 5 notebook, `colab/` | read-only untuk audit ini |
| `N:\HEALTHKATHON\` | Repo **induk** | korpus Notion dump, `analysis/`, audit script | read-only untuk audit ini |

Implikasi: dokumen, aplikasi, dan eksperimen berada di tiga tempat berbeda tanpa peta rujukan. App membaca konstanta, eksperimen menghasilkan angka, dan tidak ada satu pun artefak yang mengikat keduanya. **G-32 dan MS-13 menutup ini.**

### 10.2 Tabel klaim vs bukti (Revisi 2.0 ke Revisi 2.1)

| # | Klaim lama (Revisi 2.0) | Status | Bukti aktual | Gap ID |
|---|---|---|---|---|
| 1 | G-05 "Tidak ada satupun artefak eksperimen: tidak ada skrip training, split, seed, manifest, checksum" | **SALAH** | Artefak ADA: `backend/src/data/pipeline.py` 352 baris dengan `LEAKAGE_COLUMNS` (10 kolom, baris 37-40) dan `np.random.seed(20260707)` (baris 103); `backend/src/models/mhgsl.py` 382 baris; `backend/models/mhgsl_model.pth` 164.825 B; `notebooks/Aegis-JKN.ipynb` dengan GroupKFold(5)/LOGO/XGBoost/MLP/GCN/SHAP. Yang hilang: `manifest.json` per eksperimen, checksum berkas, skrip hitung metrik yang bisa dijalankan ulang, dan **semua output notebook (0 stored output)** | G-05 (revisi) |
| 2 | G-02 "konstanta hardcode, tidak ada satu pun file `.py` di repo" | **SALAH** | Ada 1.818 baris Python di `backend/src/` (pipeline 352, mhgsl 382, api/main 426, oasis 428, config 54, notion_client 93, test_self_check 65). Yang benar: konstanta UI **tidak diturunkan dari keluaran notebook mana pun**, dan notebook utama punya **0 stored output**, sehingga angka hasil yang akan dibandingkan pun belum terekam | G-02 (revisi) |
| 3 | Implied "tidak ada `.py` yang menjalankan pipeline" | **SALAH** | `colab/Aegis_JKN_FIXX.ipynb` (720.813 B, 6 sel) dengan 13 output Colab asli: setup Ubuntu, btop/nvtop, Ollama + `mistral-small3.1:24b`, koneksi Ollama, simulasi OASIS. `colab/Hasil simulasi dari 300 dataset notion.pdf` (3.800.507 B, **16 halaman**, diverifikasi dari `/Count 16` pada objek `/Pages`) **image-only tanpa text layer** - `pdftotext` menghasilkan 16 byte form feed tanpa satu karakter pun. Halaman sudah dibaca manual setelah rotasi 90° (lihat `21-colab-dashboard-provenance.md`), jadi Discovery "belum dibaca siapa pun" sudah tidak berlaku | G-31 |
| 4 | G-09 "kolom `pasien_id`, `faskes_id`, `dokter_id` hilang -> GroupKFold/LOGO tidak dapat diimplementasikan" | **SALAH untuk CSV repo ML** | `datasets/claims_300_v2.1.csv` punya 31 kolom termasuk `pasien_id`, `faskes_id`, `dokter_id`; split group-aware **sudah diimplementasikan** di notebook sel 11. Yang benar hilang hanya `seed`, `version`, `timestamp` | G-09 (revisi) |
| 5 | - | **BARU (P0 teratas)** | Label training beda dengan ground truth: `y_target` 38 positif vs `y_fraud_gt` 36 positif; mismatch KLM016 & KLM017 | **G-10** |
| 6 | - | **BARU (P0)** | Tabel benchmark 4 model dihitung **in-sample** (`fit` lalu `predict` pada matriks sama); probabilitas OOF GroupKFold tidak dipakai | **G-11** |
| 7 | - | **BARU (P0)** | Adjacency kanal semantik diturunkan dari kolom label `sindikat` (`pipeline.py:293-307`); 65 dari 3.790 sisi | **G-12** |
| 8 | - | **BARU (P0)** | `backend/.env` memuat `NOTION_TOKEN` + `OPENAI_API_KEY` live; git-ignored & untracked (aman), rotasi tetap perlu | **G-13** |
| 9 | - | **BARU (P0)** | Dua salinan payload byte-identik (SHA-256 `9c8cc58a697642e0...`) di `Aegis-JKN/public/` dan `colab/`; `kpi.total_claims: 100` vs 300 | **G-14** |
| 10 | - | **BARU (P1)** | `notebooks/02_model_training.ipynb` memakai `torch.randn`/`torch.randint` - data acak, bukan eksperimen | **G-15** |

### 10.3 Revisi G-02 dan G-05 (teks final)

**G-02 (revisi).** Angka benchmark di UI adalah konstanta hardcode yang **tidak diturunkan dari keluaran notebook mana pun**. Notebook utama `Aegis-JKN.ipynb` (22 sel, 11 sel kode) punya **0 stored output**, sehingga (a) konstanta UI tidak punya sumber, dan (b) belum ada satu pun hasil eksperimen terekam yang bisa dibandingkan. Bukti: `src/components/mhgsl/data.ts:258-265` (AUPRC 0,71 ke 0,91), `:270-291` (Precision 0,92 / Recall 0,90 / F1 0,91), `:253`, `:23` ("+20% Lonjakan AUPRC").

**G-05 (revisi).** Artefak eksperimen **ada** di repo ketiga. Yang hilang: (a) `manifest.json` per eksperimen, (b) checksum berkas, (c) skrip hitung metrik yang bisa dijalankan ulang, (d) output notebook yang tersimpan, (e) `docs/experiments/`. Kriteria penerimaan tetap sama: 2× run berturut-turut menghasilkan `metrics.json` identik.

### 10.4 Dampak ke roadmap

Tambahan **5 gap P0 baru** (G-10..G-14) dan 1 gap P1 baru (G-15) mengubah critical path 27 Okt. Empat hari kerja tambahan yang harus disisipkan:

| Hari | Tanggal | Work item tambahan | Gagal bila |
|---|---|---|---|
| Hari 1 | 22 Okt | B-12 satu fungsi label (G-10) | metrik tidak punya ground truth tunggal |
| Hari 3 | 24 Okt | B-14 graf bebas kolom label (G-12) | metodologi graph learning tidak sah |
| Hari 5 | 26 Okt | B-15 rotasi kredensial (G-13) | risiko kebocoran kredensial |
| Hari 6 | 27 Okt | B-13 benchmark out-of-fold (G-11) | M-01 tidak dapat dievaluasi |

Baris §3.1, §3.2, dan §3.3 sudah diperbarui accordingly. Trigger M-21, M-22, M-23, dan M-24 adalah **bloker keras**: tidak boleh submit sampai hijau.

### 10.5 Yang TIDAK berubah

G-01 (ambang 0,80 belum terkunci), G-03 (Rp 14,4 M di UI), G-07 (angka salah di `dataset-explorer.tsx`), G-08 (deadline salah di `notion-datasets.ts:383,385`), R-14 (version drift payload), serta trigger M-01, M-06, M-07 tetap berlaku persis seperti pada Revisi 2.0. Koreksi ini tidak menyentuh temuan overclaim UI maupun dokumen - hanya memperjelas asal-usul angka dan metodologi yang mendasarinya.
