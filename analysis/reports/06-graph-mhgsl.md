# Audit 06: Teori, Formula, Implementasi, dan Skala MHGSL (Multi-Channel Graph Structure Learning)

Tanggal audit: 22 Oktober 2026
Auditor: audit independen (machine learning research)
Ruang lingkup: `Aegis-JKN/docs/algorithms/mhgsl-theory.md`, `Aegis-JKN/docs/architecture/system-design.md`, `mechine-learning-deep-learning/notebooks/Aegis-JKN.ipynb`, `mechine-learning-deep-learning/backend/`, `Aegis-JKN/src/components/mhgsl/`, korpus Notion `analysis/corpus/`, data `claims_v2_live.csv` dan `claims_300_v2.1.csv`.

Perbedaan penting dari audit lain: **MHGSL diimplementasikan (benar) di repo `mechine-learning-deep-learning`**, bukan di repo web `Aegis-JKN`. Repo web hanya menampilkan visualisasi hardcode. Laporan ini mencakup keduanya.

---

## 1. Ringkasan Eksekutif

### 1.1 Status severity

| Severity | Jumlah | Ringkasan |
|---|---|---|
| **P0 (blocker)** | 9 | Metrik superiority dipublikasikan sebagai hasil ukur padahal adalah angka hardcode/adopsi literatur (C-01 s.d. C-05); klaim "Tier-3 PyTorch Geometric HeteroData" padahal implementasi memakai `GCNConv` homogen dan tidak ada `HeteroData` di kode (C-07); `W_top` negatif diklaim "membuktikan kamuflase" padahal softmax tidak bisa menghasilkan nilai negatif (C-08); klaim "zero data leakage terverifikasi" padahal graf dibangun sebelum split (C-20); **gabungan multi-channel terbukti lebih buruk daripada kanal individual (C-21, §5.5)**. Ditambah 6 temuan P0 non-tabel: `A_sem` backend memakai kolom label `sindikat`; split LOGO(faskes) menghapus 94,4% kasus fraud target dari konteks train; benchmark utama di cell 13 seluruhnya in-sample; fraud prevalence 12% bukan 1-3% seperti diklaim |
| **P1 (serius)** | 10 | Empat nilai `theta_feat` berbeda (0,50 / 0,75 / 0,85); "Attention Fusion" di teori = concat tanpa attention (C-11); SHAP per-saluran diimplementasikan sebagai L2-norm bukan Shapley (C-09); tidak ada masking/camouflage experiment (C-05, lihat §6.7); tidak ada ablation per-saluran; "Sequential Learning" tanpa temporal modeling; densitas graf 2-14% terlalu rendah untuk klaim "klaster padat" (C-10); klaim "subgraf padat" tidak terdefinisi/dihitung; klaim finansial Rp 507 juta sudah rekonsiliasi tapi tanpa dasar tarif (C-14); klaim skala "miliaran relasi" vs loop O(n²) Python (C-06, C-19) |
| **P2 (sedang)** | 2 | "Client-side MHGSL Inference" padahal komponennya heuristik konstanta hardcode, bukan model (C-17); definisi vektor cosine berbeda antar dokumen dan tidak ada di implementasi mana pun (C-18) |

### 1.2 Verdict akhir

**Teori**: MHGSL didefinisikan dengan cukup rapi sebagai *arsitektur multi-view GNN*, bukan sekadar ensemble, dan secara konseptual valid. Namun **(a)** mekanisme fusion yang diklaim ("Attention Fusion") di dokumen teori justru yang ditulis sebagai concat, **(b)** tidak ada teorema maupun justifikasi formal atas klaim keunggulan atas XGBoost, **(c)** penamaan "Sequential Learning" menyesatkan karena tidak ada pemodelan temporal sama sekali, dan **(d)** novelty berada di adaptasi terhadap domain, bukan pada metode. Yang lebih serius: **`12-archive-architecture.md:55` secara eksplisit menyatakan angka-angka benchmark adalah adaptasi literatur, bukan eksperimen internal**, sementara repo web menampilkannya sebagai hasil terukur.

**Implementasi**: Ada implementasi PyTorch/NumPy yang substantif di `mechine-learning-deep-learning` (notebook 22 sel + backend FastAPI dengan `torch_geometric.nn.GCNConv`). Yang bermasalah bukan ketiadaan implementasi, melainkan **desain evaluasinya tidak dapat menguji apa pun yang diklaim**: benchmark utama di-cell 13 dilatih dan dievaluasi pada data yang sama, graf dibangun sebelum split, dan channel semantik backend memakai kolom label.

**Skala**: 300 klaim, 40 pasien, 20 dokter, 10 faskes. Densitas kanal terukur: A_top 7,63%, A_feat 2,11%, A_sem 11,17%, A_homo 13,85% (off-diagonal, n=300). Parameter model 37.157 (d=34, d_h=48) = 1,5 parameter per edge. Kanal fitur 2,11% densitasnya **tidak membentuk "klaster padat"** seperti diklaim: pada ambang 0,85 hanya 1.892 dari 44.850 pasangan node yang terhubung, graf terbagi ke 41 komponen, dan struktur paling padat (densest-subgraph 48 node, max clique 10 node) **tidak berisi satu pun klaim fraud**. Lebih troubling: **permutation test menunjukkan gabungan kanal `A_homo` lebih buruk daripada acak (p=0,73)**, sementara kanal semantik yang membawa bobot UI tertinggi (0,41) juga tidak signifikans (p=0,14). Yang benar-benar membedakan sindikat hanya kanal topologi (p=0,008) dan kanal fitur (p<0,001).

---

## 2. Audit Teori

### 2.1 (a) Multi-channel heterogeneous GNN atau ensemble?

**Verdict: multi-channel GNN yang sah, bukan ensemble.** Alasannya: tiga kanal diproses oleh operator message-passing yang sama (`D^-1/2 Ã D^-1/2 X W`) atas matriks ketetanggaan berbeda, dengan parameter privat per kanal plus cabang shared-parameter, lalu digabung. Ini persis pola *multi-view GNN* / *multi-relational GCN* yang mapan (mis. R-GCN untuk multi-relasi, MAGNN/HGT untuk multi-view). Bentuknya valid.

Yang perlu diluruskan:
- Yang benar-benar baru bukan arsitekturnya, melainkan **dekomposisi kanal spesifik-domain** (topologi layanan, kemiripan atribut, metapath klinis).
- `mhgsl-theory.md:103` menyebut "konvolusi independen dan konvolusi berparameter bersama". Yang direalisasikan di notebook cell 9 (`MHGSLModel`, baris 67-114) adalah 4 cabang: `gcn_top`, `gcn_feat`, `gcn_sem` (privat) + `gcn_shared` (shared) di mana `gcn_shared` dijalankan pada ketiga adjacency. Ini **cocok** dengan rumus teori di `mhgsl-theory.md:161-172`. Bagus.
- Yang tidak konsisten: `mhgsl-theory.md:36` menyebut "3 saluran matriks ketetanggaan", benar. Tapi digabung dengan 4 blok (termasuk shared) menjadi `H_final ∈ R^{N×4d_h}` (`mhgsl-theory.md:178`). Implementasi notebook memberi classifier input `5*d_h` (fused + concat), `cell 9:86`. Perbedaan kecil, tapi menunjukkan teori dan kode tidak disinkronkan.

### 2.2 (b) Channel fusion mechanism: concat atau attention?

**Ini temuan P1 paling substansial.** Ada dua dokumen teori yang berbeda dan satu implementasi.

| Sumber | Mekanisme fusion yang tertulis | Attention? |
|---|---|---|
| `Aegis-JKN/docs/algorithms/mhgsl-theory.md:131-133` | `H(final) = Concat(H(top), H(feat), H(sem), H(shared))` | **Tidak ada** |
| `Aegis-JKN/docs/architecture/system-design.md:142-148` | Stage 5 titled "Multi-Channel **Attention** Fusion", body = konkatenasi + linear | **Tidak ada** |
| `corpus/11-archive-proposal.md:218-219` | `alpha_k = exp(q^T tanh(W_att H^(k)))/sum_j exp(...)` | **Ya** (rumus gating) |
| `notebooks/Aegis-JKN.ipynb` cell 9:51-65 | `MultiChannelAttention` = `nn.MultiheadAttention` + learnable `channel_weights` softmax | **Ya** |
| `backend/src/models/mhgsl.py:70-93` | `MultiChannelAttention` = `nn.MultiheadAttention` + `channel_weights` | **Ya** |

Masalahnya:
1. **Dokumen teori di repo web tidak memuat attention sama sekali.** Header Stage 5 di `system-design.md:142` menjanjikan "Attention Fusion" lalu hanya menulis concat. Ini overclaim kecil tapi nyata.
2. **Kode attention yang ada tidak sama dengan rumus di proposal.** `nn.MultiheadAttention` dengan `stacked` (n, 4, d_h) melakukan **self-attention antar-saluran** (setiap kanal dapat attend ke kanal lain), bukan gating skalar `alpha_k` per kanal. Yang dikalibrasi di `11-archive-proposal.md:220` adalah `W_feat=0.38, W_sem=0.41, W_top=-0.12` - ini **bukan** output dari `nn.MultiheadAttention` (yang menghasilkan bobot per-token per-head, bukan 3 bobot kanal). Jadi angka "bobot atensi optimal" tersebut tidak dapat dihasilkan oleh kode yang ada.
3. **Justifikasi `W_top` negatif bertentangan logis.** `11-archive-proposal.md:220` menyatakan nilai negatif `W_top = -0.12` "membuktikan fenomena penting: saluran topologi fisik sengaja direkayasa". Ini logika terbalik. Dalam `MultiChannelAttention` bobot `channel_weights` diinisialisasi `ones/4` lalu dipelajari lewat softmax, sehingga **tidak mungkin negatif** (`mhgsl.py:82`, `cell 9:57`). Nilai `-0.12` hanya muncul di (a) `data-uploader.tsx:132` sebagai konstanta hardcode frontend, (b) `backend/src/oasis/simulation.py:100` sebagai konstanta hardcode `channel_breakdown`, dan (c) `mhgsl-theory.md:230` sebagai contoh naratif. Tidak ada satu pun tempat di mana `-0.12` emerges dari bobot yang dipelajari. **Klaim "pembuktian matematis kamuflase" (`mhgsl-theory.md:236`) tidak memiliki basis komputasional.**

### 2.3 (c) Klaim "MHGSL outperform XGBoost/MLP": ada teorema?

**Tidak ada. Nol teorema, nol pembuktian, nol analisis teoretis.**

- `mhgsl-theory.md` tidak memuat lemma, teorema, proposition, atau analisis konvergensi apa pun. Seluruh dokumen adalah deskripsi arsitektur.
- Argumen "mengapa GCN/GAT gagal" (`mhgsl-theory.md:18`) adalah naratif: "proses message passing merata-ratakan informasi tetangga yang sengaja dikamuflasekan, menyebabkan oversmoothing dan label contamination". Ini **tidak** didukung. Oversmoothing terjadi pada graf homogen dengan GCN murni; pada graf heterogen dengan relation-specific weights (yang justru dilakukan MHGSL), hetero GNN seperti R-GCN/HGT justru **mengzoo** pola heterogen, bukan meratakan. Argumen ini tidak berlaku untuk baseline yang sebanding.
- Klaim superiority yang beredar: `11-archive-proposal.md:30` (Akurasi 93,0%, Presisi 94,12%, ROC-AUC 0,9825, AUPRC 0,9142, +28,6% vs XGBoost 0,71), `:338` ("keunggulan mutlak"), `:407`.
- **Yang menentukan**: `12-archive-architecture.md:55` menyatakan secara terbuka: *"seluruh metrik komparatif (AUPRC +20%, reduksi false negatives 42%) dilabeli sebagai adaptasi literatur dari Hong et al., Heliyon 2024 ... bukan hasil eksperimen internal; angka dikalibrasi ulang saat data pilot Fase 3 tersedia."*
- `04-evidence-matrix.md:34` (E-07): "Benchmark Aegis-JKN: AUPRC 0,9142 | Belum tereproduksi pada audit ini".
- `06-research-notes.md:42`: "AUPRC MHGSL 0,9142 ... Belum dapat direproduksi dari artefak yang diperiksa".
- **Jadi tim sendiri sudah tahu angka-angka ini bukan hasil ukur.** Yang bermasalah adalah repo web tetap menampilkannya sebagai fakta terukur (lihat §4.3 dan Tabel §7).

### 2.4 (d) Naming: "Sequential Learning" tanpa temporal modeling?

**Ya, misleading. Ini P1.**

Nama resmi dalam `mhgsl-theory.md:3` adalah *"Multi-Channel Heterogeneous Graph Structure Learning"* dan proposal menyebut *"Multi-Hop Graph Structure Learning"* (`11-archive-proposal.md:6`). Variasi "Sequential Learning" muncul di brief tugas dan pertanyaan Anda; di korpus, `02-architecture.md:31` hanya meminta "sifat temporal" didokumentasikan untuk tiap edge, dan `02-architecture.md:52` meminta afiliasi dokter "konsisten secara temporal".

**Fakta keras: tidak ada pemodelan temporal di mana pun.**
- Grep `sequential learning|temporal|time-aware|recurrent|LSTM|sequence model|chronolog|temporal split|time-order` di seluruh `corpus/*.md` → **hanya 2 hit**, keduanya di `02-architecture.md:31` dan `:52`, dan keduanya berupa *permintaan dokumentasi*, bukan implementasi.
- Di notebook: fitur temporal yang ada hanya kalender (`cell 5:28-31`: bulan, hari_dalam_minggu, hari_dalam_bulan, is_weekend). Ini **musim kalender**, bukan temporal graph learning. Tidak ada time-aware message passing, tidak ada temporal edge weight, tidak ada split berbasis waktu.
- Graf dibangun dari 300 baris sekaligus; node adalah **klaim**, bukan entitas, jadi tidak ada urutan intrinsik sama sekali.
- Literatur acuan: TGN (Zhao et al., 2020) dan TGAT (Xu et al., 2020) adalah standar temporal GNN; R-GCN (Schlichtkrull et al., 2018) dan HGT (Hu et al., 2020) untuk heterogen; GNNExplainer (Ying et al., 2019) untuk XAI. **MHGSL tidak berada di lineage mana pun.** Yang dikombinasikan adalah *multi-relational GCN* (multi-view) + *attention fusion* + *focal loss* (Lin et al., 2017), semuanya komponen mapan.

**Novelty defensible?** Setengah. Yang bisa diklaim: dekomposisi kanal ke tiga perspektif spesifik-asuransi-kesehatan + whimpy reweighting. Yang **tidak** bisa diklaim: algoritma baru. Klaim novelty harus di-QA terhadap Hong et al. 2024 yang **sudah mengimplementasikan desain 3-kanal yang sama persis** (lihat §2.5).

### 2.5 Standard benchmarking: apakah klaim novelty defensible?

**Pertanyaan yang harus dijawab: apakah MHGSL berbeda dari Hong et al. 2024?**

`corpus/12-archive-architecture.md:30` menyatakan MHGSL "diadaptasi dari paper Hong et al., Heliyon 2024" plus "varian multiview heterogeneous information network dengan augmented graph structure learning, IEEE 2025". `corpus/dataset_research_live.json:114` mendeskripsikan paper Hong sebagai: *"3 saluran graf - topologi (relasi entitas), fitur (KNN + cosine similarity), semantik (meta-path klinis) - diproses GCN spesifik-saluran + GCN parameter-bersama, lalu difusi & klasifikasi."*

**Ini deskripsi MHGSL persis.** Artinya:
- Arsitektur MHGSL = reimplementasi domain-adapted dari Hong et al. 2024, plus satu Sole addition: saluran **shared-parameter GCN**.
- Contoh bobot kanal `W_feat=0.38, W_sem=0.41, W_top=-0.12` (`11-archive-proposal.md:220`) adalah angka yang **identik** dengan `data-uploader.tsx:132` (`featureScore*0.38 + semanticScore*0.41 + topologyScore*(-0.12) + 0.3`) dan `backend/src/oasis/simulation.py:100` (`{"topology": -0.12, "feature": 0.38, "semantic": 0.41, "shared": 0.33}`). Ketiganya **konstanta hardcode yang sama**, bukan hasil kalibrasi.
- Verifikasi bibliografis tidak dapat diselesaikan karena mesin pencari yang diwajibkan (SearXNG) gagal: `brave (Suspended: too many requests)`, `duckduckgo (CAPTCHA)`, `google cse (Suspended)`. Jadi **claims Hong et al. 2024 belum diverifikasi independen**. Ini harus diselesaikan sebelum klaim novelty apa pun dipublikasikan. DOI yang dikutip `10.1016/j.heliyon.2024.e30045` → `https://www.cell.com/heliyon/fulltext/S2405-8440(24)06076-6`.

**Pola yang berulang**: konstanta yang dubbed "hasil kalibrasi empiris" (`11-archive-proposal.md:220` kata "Berdasarkan kalibrasi empiris") sebenarnya konstanta yang **dihardcode** di tiga file terpisah. Ini harus dianggap overclaim.

---

## 3. Audit Formula

### 3.1 Tabel formula dan masalah

| # | Formula | Lokasi | Masalah | Perbaikan |
|---|---|---|---|---|
| F1 | `Sim_feat = (x_i·x_j)/(‖x_i‖‖x_j‖)` | `mhgsl-theory.md:61-63` | Cosine **hanya bermakna pada vektor non-negatif**. Vektor yang memuat `biaya_rp` bisa bernilai negatif (biaya per hari, selisih) atau `skor_sentimen` bisa negatif → cosine bisa negatif, ambang 0,85 jadi tak bermakna. Tidak ada-transformasi log/di-centering. | Terapkan transformasi log1p pada biaya, z-score per-fitur, atau gunakan **1 − normalized Euclidean distance**. Deteksi anomali multivariat lebih tepat dengan Mahalanobis/Isolation Forest daripada cosine. |
| F2 | `A_feat_ij = Sim` bila `φ(v_i)=φ(v_j)` **dan** `Sim > θ` | `mhgsl-theory.md:67-72` | **Restriksi same-type undocumented** dan tidak konsisten dengan implementasi: `notebooks` cell 7:34 tidak membatasi tipe node sama sekali (semua 300 klaim adalah satu tipe), backend `pipeline.py:283` juga tidak. Teori ≠ kode. | Tulis satu definisi kanonik di satu dokumen; generator notebook (`notebooks/build_notebook.py:318`) harus mengimpor definisi itu, bukan menduplikasi. |
| F3 | `θ_feat` = **0,75** | `mhgsl-theory.md:74` | Kontradiksi dengan empat nilai lain (lihat §3.2). Tidak ada justifikasi empiris. | Pilih satu nilai lewat **sensitivity sweep in-fold** dan laporkan kurva AUPRC vs θ. |
| F4 | Bobot contoh `0,92 / 0,88 / 0,85` | `mhgsl-theory.md:74` | Angka naratif yang **diberi bobot tinggi persis di atas ambang**, tapi tidak dapat direproduksi dari data mana pun. Tidak adavenance. | Hapus, atau ganti dengan hasil terukur. |
| F5 | `C_M = A_(D,Dx)·A_(Dx,S)·A_(S,RS)` | `mhgsl-theory.md:87-89` | **Ok secara matematis**, tapi **tidak ada satupun implementasi** yang menghitung PathSim. `notebooks` cell 7:41-56 mengimplementasikan `A_sem` sebagai **skor hand-crafted** (`0,45` dx sama + `0,45` prosedur sama + `0,10` faskes sama, ambang 0,55), bukan PathSim. `backend/src/data/pipeline.py:301-309` memakai "same diagnosis-procedure pair **atau sindikat sama**". Ketiganya berbeda, dan tidak satupun adalah PathSim. | Implementasikan PathSim sesuai definisi, atau ubah teks teori agar mendeskripsikan yang benar-benar dijalankan. |
| F6 | `A_sem_ij = 2·C(i,j)/(C(i,i)+C(j,j))` | `mhgsl-theory.md:93-95` | PathSim yang benar. **Tapi** `11-archive-proposal.md:211` menulis `s(u,v) = (2·|p_u->v|)/(|p_u->u|+|p_v->v|)`, sama. Masalahnya bukan rumus, tapi **tidak ada yang mengimplementasikannya** (lihat F5). | Sama seperti F5. |
| F7 | `H^(k) = σ(D̃^-1/2 Ã^(k) D̃^-1/2 X W^(k))` | `mhgsl-theory.md:152-154` | **Benar** dan cocok dengan `cell 9:12-15` (`torch.matmul(norm_adj, x)` lalu Linear) dan `backend/src/models/mhgsl.py` via `GCNConv`. Satu-satunya catatan: `mhgsl-theory.md:159` menyebut LeakyReLU slope 0,2, dan `cell 9:31` memang pakai `negative_slope=0.2`, **cocok**. Ini bagian terkuat dari teori. | Pertahankan. |
| F8 | `H^(shared) = (1/3)Σ_k H^(shared,k)` | `mhgsl-theory.md:170-172` | **Benar**, cocok `cell 9:100` dan `mhgsl.py:157`. | Pertahankan. |
| F9 | `H^(final) = [H_top‖H_feat‖H_sem‖H_shared]` | `mhgsl-theory.md:180-182` | Disebut "Attention-Based Fusion" di diagram `mhgsl-theory.md:131` padahal **murni concat**. Untuk header "Attention" di `system-design.md:142` juga concat. | Ubah nama menjadi "Concatenation Fusion" di kedua dokumen, atau implementasikan gating sesuai `11-archive-proposal.md:219`. |
| F10 | `ŷ = Sigmoid(H_final W_cls + b)` | `mhgsl-theory.md:186-188` | Dimensi: `H_final ∈ R^{N×4d_h}` → `W_cls ∈ R^{4d_h×1}`. Namun implementasi `cell 9:86` memakai `Linear(5*d_h, d_h)` lalu `Linear(d_h,1)`, yaitu **2 lapis**, bukan 1. Teori dan kode berbeda. | Sinkronkan. |
| F11 | Focal Loss, `α=0,75, γ=2,0` | `mhgsl-theory.md:190-197` | Rumus **benar** dan cocok `cell 9:116-128` (alpha applied ke loss_pos, 1-alpha ke loss_neg, sesuai standar). Tepat sitasi Lin et al. 2017 (`11-archive-proposal.md:425`). **Bagus.** | Pertahankan. Catatan: α=0,75 mengasumsikan prevansi minoritas; data aktual 12%. |
| F12 | `ŷ = φ0 + φ_top + φ_feat + φ_sem + φ_shared + Σφ_attr` | `mhgsl-theory.md:205-207` | Additivitas SHAP hanya berlaku jika output model benar-benar **linear dalam feature**.-output sigmoid **tidak** linear → SHAP "per-channel" yang ditambahkan langsung ke probabilitas **tidak valid** secara matematis unless computed on logit space. | Komputasi SHAP di logit space (DeepSHAP pada logit), atau label sebagai "channel contribution score" non-Shapley. |
| F13 | `φ_c(x) = Σ_{S⊆C\{c}} ...` | `mhgsl-theory.md:211-213` | Rumus Shapley **benar**. Tapi implementasi **bukan Shapley**: `backend/src/models/mhgsl.py:195-205` menghitung `torch.norm(outputs['topological'][node_idx])` per kanal, yaitu **L2 norm dari embedding**, bukan marginal expectation. `data-uploader.tsx:127-134` juga bukan SHAP, hanya penjumlahan konstanta. | Implementasikan DeepSHAP/Explainer secara benar, atau ganti label "SHAP" dengan "channel norm score". |
| F14 | `CamouflageSignature` ⇔ `ŷ≥0,85 ∧ φ_top<0 ∧ φ_feat>λ_feat ∧ φ_sem>λ_sem` | `mhgsl-theory.md:218-225` | **Kontradiksi antar dokumen**: `11-archive-proposal.md:223` memakai `Risk Score ≥ 0.80` dan `φ_feat>0.30, φ_sem>0.35`; `mhgsl-theory.md:220` memakai `≥0.85` dengan `λ` tanpa nilai. Selain itu `λ_feat`/`λ_sem` **tidak pernah didefinisikan** di dokumen mana pun. | Satu definisi, semua parameter diberi nilai eksplisit. |
| F15 | `φ_top = -0.12` "membuktikan adanya upaya kamuflase aktif" | `mhgsl-theory.md:236` | **Klaim falsifiable yang tidak diuji.** `φ_top` negatif bisa muncul dari model apa pun yang belajar mengabaikan kanal topologi; ia **tidak bukti intent**. `02-architecture.md:38` sendiri menyatakan "SHAP tidak boleh digambarkan sebagai bukti kausal". Kontradiksi langsung dengan prinsip proyek sendiri. | Ubah menjadi "indikasi anomali topologi (deskriptif)" dan acknowledge `02-architecture.md:38`. |
| F16 | `p_fused = p_graph + 0,10·f_text·(1−p_graph)` | `11-archive-proposal.md:~230`, `math-formulas.tsx:248-251` | Gate yang masuk akal. **Tapi `f_text` didefinisikan sebagai `[-1, +1]`** di proposal ("|f_text| indeks diskrepansi ... rentang -1.0 hingga +1.0") sementara `math-formulas.tsx:284` menulis `f_text: sinyal sentimen teks [0, 1]`. Dengan `f_text` negatif, `p_fused` bisa turun **di bawah** `p_graph`, sehingga "sinyal teks hanya menaikkan prioritas" (klaim di `12-archive-architecture.md:86`) **tidak berlaku**. | Seragamkan domain `f_text` ke [0,1], atau tuliskan secara eksplisit bahwa teks bisa menurunkan skor dan memang itu perilaku yang diinginkan. |

### 3.2 Ketidakkonsistenan `theta_feat` (P1)

**Empat nilai berbeda untuk hiperparameter yang sama:**

| Nilai | Lokasi | Artefak |
|---|---|---|
| **0,85** | `notebooks/Aegis-JKN.ipynb` cell 7:5, 83 (`build_notebook.py:318,396`) | Notebook utama (yang menjalankan eksperimen) |
| **0,75** | `Aegis-JKN/docs/algorithms/mhgsl-theory.md:74`; `Aegis-JKN/docs/architecture/system-design.md:106` | Dokumen teori repo web |
| **0,50** | `backend/src/data/pipeline.py:251, 327`; `backend/src/oasis/simulation.py:76`; `corpus/11-archive-proposal.md:210` | Backend produksi + proposal |
| **0,50** | `corpus/09-draft-hub.md:15`, `10-simulation-dataset.md:12`, `14-index.md:58` | Korpus ringkasan |

Artinya **dokumen teori, notebook eksperimen, dan backend yang benar-benar melayani API memakai tiga ambang berbeda.** Tidak ada justifikasi empiris untuk salah pun. `02-architecture.md:36` justru menyatakan: *"Threshold kemiripan, definisi metapath, normalisasi, dan bobot kanal merupakan hiperparameter. Semua harus dipilih hanya berdasarkan data pelatihan dan validasi yang telah ditetapkan."* - belum dilakukan.

### 3.3 Dampak ambang terhadap densitas (terukur)

Reproduksi persis cell 7 dengan data nyata (n=300, `X_clean` hasil StandardScaler atas 34 fitur). Angka di bawah adalah **edge berarah** (2× pasangan tak berurut), densitas relatif terhadap `n² = 89.700`:

| θ | pasangan tak berurut > θ | edge berarah | densitas terhadap n² |
|---|---|---|---|
| 0,50 | 3.613 | 7.226 | 8,06% |
| 0,75 | 2.044 | 4.088 | 4,56% |
| **0,85** | **946** | **1.892** | **2,11%** |
| 0,90 | 485 | 970 | 1,08% |
| 0,95 | 176 | 352 | 0,39% |

Distribusi cosine off-diagonal: min −0,5496, maks 1,0000, mean 0,0003, median −0,0607. **Kanal fitur pada θ=0,85 hanya 2,11% padat.** Klaim "membentuk klaster padat di A_feat" (`mhgsl-theory.md:74`) dan "Sangat kuat (klaster padat)" (`src/components/mhgsl/data.ts:251`) **tidak didukung secara kuantitatif**: pada densitas 2,11% graf fitur terbagi ke **41 komponen terhubung** (terbesar 35 node, 20 node terisolasi) dengan **clique maksimum tepat 10 node** (§5.5). Bandingkan: feature channel di `data.ts:127-130` yang ditampilkan di UI hanya 4 edge.

### 3.4 Normalisasi: apakah ada?

**Ada, tapi hanya di satu tempat.** `notebooks` cell 5:58-59 menerapkan `StandardScaler` ke seluruh 34 fitur **sebelum** cosine. Ini membuat cosine layak (mean 0, median −0,06 - bukan degenerate seperti yang saya perkirakan dari data mentah). Jadi temuan "cosine tanpa normalisasi → semua pasangan lolos ambang" **tidak berlaku untuk notebook**.

Tapi:
- `corpus/11-archive-proposal.md:210` menyebut fitur cosine adalah "(LOS, biaya INA-CBG, **usia**, kuantitas obat)" - 4 fitur. Notebook memakai 34 fitur yang **tidak termasuk usia, LOS, atau kuantitas obat** sebagai elemen cosine; LOS/biaya masuk sebagai `los_hari`/`biaya_rp`/`biaya_per_hari` (3 dari 34) dan obat masuk hanya sebagai `jumlah_obat` (jumlah jenis obat, **bukan** kuantitas). **Definisi vektor cosine berbeda antar dokumen.**
- `Aegis-JKN/src/components/mhgsl/data.ts:156` menyatakan kanal fitur memakai "(LOS, usia, rasio biaya)" - **ketiga ini tidak ada di implementasi mana pun**.

---

## 4. Implementasi: Real vs Mock

### 4.1 Peta repositori (terverifikasi)

| Artefak | Status | Bukti |
|---|---|---|
| `mechine-learning-deep-learning/notebooks/Aegis-JKN.ipynb` | **REAL** (22 sel, PyTorch, 3 kanal) | cell 7 (graf), cell 9 (model), cell 11 (CV), cell 13 (benchmark) |
| `mechine-learning-deep-learning/backend/src/models/mhgsl.py` | **REAL** (382 baris, `torch_geometric.nn.GCNConv`) | `:15` import GCNConv, `:95` `class MHGSLModel` |
| `mechine-learning-deep-learning/backend/src/data/pipeline.py` | **REAL** (konstruksi 3 kanal + edge_index) | `:247-325` |
| `mechine-learning-deep-learning/backend/src/api/main.py` | **REAL** (FastAPI, train/predict/oasis) | `:180` `/api/model/train`, `:245` `/api/model/predict` |
| `Aegis-JKN/src/components/mhgsl/multi-channel-graph.tsx` | **MOCK** (SVG statis) | 11 node + 20 edge hardcode di `data.ts:87-137` |
| `Aegis-JKN/src/components/mhgsl/comparison.tsx` | **MOCK** (angka hardcode) | `data.ts:249-300` |
| `Aegis-JKN/src/components/mhgsl/data-uploader.tsx` | **MOCK** (heuristik) | `:79-137` |
| `Aegis-JKN/src/components/mhgsl/math-formulas.tsx` | **MOCK** (JSX statis) | `:155-258` |
| `Aegis-JKN/src/components/mhgsl/simulation.tsx` | **MOCK** (animasi hardcode) | `CHANNEL_PROGRESS` konstanta |

### 4.2 Detail: graf web adalah mock hardcode

`Aegis-JKN/src/components/mhgsl/data.ts:87-109` mendefinisikan **11 node** dengan koordinat piksel literal (`x: 110, y: 90`) dan `risk` yang sudah ditentukan. `data.ts:111-137` mendefinisikan **20 edge** hardcode (12 topologi, 4 fitur, 4 semantik), termasuk bobot fitur `0.92, 0.88, 0.85, 0.79` dan bobot semantik `0.81, 0.83, 0.94, 0.71` yang persis sama dengan angka di `mhgsl-theory.md:74`.

`multi-channel-graph.tsx` **tidak** menjalankan perhitungan apa pun: hanya memetakan array ke `<line>`/`<path>` SVG (`:328-374`). Overlay metapath (`:54-57`) adalah konstanta `["d1","dxMild","sExpensive","rs"]`. Komponen "detailed node panel" (`:453-507`) menghitung degree dari array hardcode, bukan dari graf.

**Tidak ada file `.py`, `.ipynb`, `.pt`, `.pth`, atau `edges.json` di repo web `Aegis-JKN`** (verified: `find . -name "*.py" -not -path "*/node_modules/*"` → 0 hasil; `find . -name "*.ipynb"` → 0; `find . -name "edges.json" -o -name "*.pt" -o -name "*.pth"` → 0). Repo web adalah **Next.js presentational saja**; `package.json` tidak memuat satu pun dependensi ML.

### 4.3 Backend produksi: trained on full data, metrics hardcoded

`backend/src/api/main.py:180-243` (`/api/model/train`) memuat data, membangun graf, lalu `trainer.train_epoch(X, edges, y)` pada **seluruh 300 baris tanpa split**. `main.py:228` `trainer.evaluate(X, edges, y)` juga in-sample. Tidak ada `GroupKFold`/`LeaveOneGroupOut` di seluruh `backend/`.

`backend/src/api/main.py:365-400` (`/api/metrics`) mengembalikan **angka hardcode**: XGBoost 0,71 (`main.py:395`) / GNN 0,78 (`:396`) / Hybrid 0,85 (`:397`) / MHGSL 0,91 (`:398`), identik dengan `Aegis-JKN/src/components/mhgsl/data.ts:258-265`. Jadi **frontend dan backend menyajikan angka yang sama yang tidak pernah dihitung** dari model mana pun.

### 4.4 Grep bukti (ringkas)

```
$ grep -rn "torch|PyG|torch_geometric|HeteroData|xgboost|shap|sklearn" Aegis-JKN/
  → 0 file .py / .ipynb; hanya .md, .ts, .tsx, bun.lock, package-lock.json
$ find Aegis-JKN -name "*.py" -not -path "*/node_modules/*" | wc -l   → 0
$ find Aegis-JKN -name "*.ipynb" -not -path "*/node_modules/*" | wc -l → 0
$ find mechine-learning-deep-learning -name "*.py" -not -path "*/venv/*"
  → backend/src/models/mhgsl.py, backend/src/data/pipeline.py,
    backend/src/api/main.py, backend/src/oasis/simulation.py, +2
$ grep -rn "torch_geometric" mechine-learning-deep-learning/backend/
  → backend/src/models/mhgsl.py:15  from torch_geometric.nn import GCNConv
```

### 4.5 Klaim "PyTorch Geometric HeteroData GCN" (P0)

`11-archive-proposal.md:26` dan `:316` mengklaim "Tier-3 **PyTorch Geometric HeteroData** GCN". Yang ada:
- `backend/src/models/mhgsl.py:15` memakai `GCNConv` **homogen** (satu `edge_index` per kanal), bukan `HeteroData`.
- `notebooks` cell 9 **tidak memakai PyTorch Geometric sama sekali** - semuanya `torch.matmul(norm_adj, x)` manual.
- **Tidak ada `HeteroData` di seluruh repo ML.** (grep `HeteroData` → 0 di kode, hanya di teks proposal.)
- `12-archive-architecture.md:49` sudah mengakui: *"#4 Graf Belum Terintegrasi | CSV tabular saja tidak cukup untuk MHGSL | Bangun ulang graf HeteroData dari CSV + edges.json di pipeline"*, artinya **belum ada `edges.json`** (verified: tidak ada file itu).

---

## 5. Analisis Skala & Feasibility

### 5.1 Skala terukur (data nyata, 300 baris)

| Entitas | Jumlah | Sumber |
|---|---|---|
| Klaim | 300 | `claims_300_v2.1.csv` |
| Pasien | 40 | `pasien_id` unik |
| Dokter | 20 | `dokter_id` unik; **0 dokter berpraktik di >1 faskes** |
| Faskes | 10 | `faskes_id` unik |
| Diagnosis | 13 | `diagnosis_code` unik |
| Prosedur | 8 | `prosedur_code` unik |
| Sindikat | 9 | SYND-01..09, total 36 klaim |
| Label fraud | **36 (12,0%)** | `is_fraud==1` |

**Fraud prevalence = 12,0%**, bukan 1-3% seperti diklaim `mhgsl-theory.md:191` ("rasio fraud aktual berkisar 1% - 3%"). Ini menggeser seluruh *prior* Focal Loss, threshold, dan baseline AUPRC. AUPRC random baseline pada 12% = **0,12**, bukan ~0,03. Klaim AUPRC 0,91 berarti 7,6× baseline; pada 3% berarti 30×.

### 5.2 Densitas kanal (reproduksi cell 7, n=300)

| Kanal | Edge (termasuk self-loop) | Edge off-diag | Densitas off-diag | Densitas terhadap n² |
|---|---|---|---|---|
| A_top | 7.140 | 6.840 | **7,63%** | 7,93% |
| A_feat (θ=0,85) | 2.192 | 1.892 | **2,11%** | 2,44% |
| A_sem | 10.318 | 10.018 | **11,17%** | 11,46% |
| A_homo | 12.726 | 12.426 | **13,85%** | 14,14% |

Tiga densitas (A_feat 2,11%) **tidak mendukung** klaim "klaster padat". Bandingkan densitas graf acak pada 300 node: complete graph = 89.700 edge. 1.892 edge = **2,1% dari complete graph**.

### 5.3 Derajat pada level entitas (graf heterogen nyata)

Rekonstruksi dari 300 klaim (P↔D, D↔F, F↔S, D↔Dx, Dx↔S):
- Node: **91** (P=40, D=20, F=10, S=8, Dx=13)
- Edge: **204**
- Derajat: min 2, maks 99, mean 26,11, median 12
- Derajat per tipe: P mean 7,50 (maks 12) · D mean 45,00 (maks 99) · F mean 44,40 (maks 77) · S mean 36,00 (maks 62) · Dx mean 34,15 (maks 64)

**Ketidakseimbangan ekstrem**: dokter/faskes/prosedur memiliki derajat 5-6× pasien. Dengan message passing 2 lapis, **seluruh 1-2 hop dari Pasien** sudah menjangkau hampir semua simpul derajat tinggi. Artinya: **informasi kanal topologi untuk setiap klaim/kasien praktis identik** (granularitas node-to-node hilang). Di graph sekecil ini, neighborhood tumpang tindih dan degree-based features didominasi oleh "faskes mana".

### 5.4 Parameter vs data

Dengan `d=34`, `d_h=48` (dari `cell 9:131-137`):

| Komponen | Parameter |
|---|---|
| 4 cabang GCN (2 layer masing-masing) | 16.128 |
| `MultiChannelAttention` | 9.412 |
| Classifier (5·d_h→d_h→1) | 11.617 |
| **Total** | **37.157** |

- **Parameter : edge = 37.157 : 24.852 ≈ 1,5 : 1** (A_homo) atau **182 : 1** terhadap A_feat saja.
- **Parameter : baris data = 37.157 : 300 ≈ 124 : 1**. Dengan 36 contoh positif dan 10 fold, **overfitting hampir pasti** tanpa regularisasi berat; `weight_decay=1e-4` (`cell 11:23`) sangat ringan untuk rasio ini.
- Kepastian statistik: pada 10 fold LOGO, tiap fold holdout punya **rata-rata 3,6 kasus fraud** (36/10). AUPRC per fold dengan 0-6 positif memiliki interval-bootstrap yang sangat lebar. Perbandingan 0,91 vs 0,71 **tidak dapat dibedakan** pada 36 kasus positif.

### 5.5 "Subgraf padat" (dense subgraph): klaim tanpa definisi, dan hasil hitungannya berlawanan dengan klaim

`src/components/mhgsl/data.ts:251` menyatakan MHGSL "Sangat kuat (**klaster padat**)" untuk deteksi sindikat. Istilah "subgraf padat"/"dense subgraph" **tidak terdefinisi** di seluruh repo:
- Grep `densest|clique|community|louvain|cluster_coeff|dense_subgraph` di `backend/src/` dan notebook → **0 hasil**. Tidak ada algoritma densest-subgraph (mis. Charikar peeling), tidak ada community detection, tidak ada perhitungan koefisien pengelompokan.
- `mhgsl-theory.md:16` menyebut "koefisien pengelompokan (*clustering coefficient*)" sebagai alat untuk mendeskripsikan kamuflase, tapi **tidak ada kalkulasi** di mana pun.

Karena tidak ada definisi, audit ini menghitung sendiri struktur "padat" pada data nyata (A_feat θ=0,85, 1.892 edge di 300 node) untuk menguji apakah klaimnya punya dasar:

| Struktur terukur di A_feat (θ=0,85) | Nilai | Komposisi fraud |
|---|---|---|
| Komponen terhubung | 41 (terbesar 35 node; 20 node terisolasi) | komponen terbesar (35 node) berisi **2** fraud; komponen kedua (29 node) berisi **7** fraud; komponen ketiga (29 node) berisi **0** fraud |
| Clique maksimum (Bron-Kerbosch, exact) | **10 node** | **0 / 10 fraud** (5 pasien, 2 dokter, 2 faskes, 1 sindikat) |
| k-core tertinggi | core-7, **14 node** | - |
| Densest-subgraph (Charikar peeling) | avg-degree 23,08, 48 node | **0 / 48 fraud** |

**Hasilnya justru melawan klaim.** Struktur paling "padat" di kanal fitur (densest-subgraph 48 node, clique 10 node) **tidak mengandung satu pun klaim fraud**. Struktur paling padat terbentuk dari klaim non-fraud yang memang mirip karena fitur biaya/LOS yang serupa. Yang terukur pada klaim fraud (36 node) jauh lebih lemah: A_feat degree fraud rata-rata hanya 2,72 dengan **6 dari 36 node fraud terisolasi** (tidak punya edge fitur apa pun), max clique dalam subgraph fraud = 6 node, dan enam komponen fraud terbesar hanya berukuran 3-6 node.

Uji signifikasi enrichment sindikat (permutation test 20.000 iterasi, 36 node sindikat vs 36 node acak, pasangan berarah):

| Kanal | pasangan sindikat terobservasi | mean permutasi | p | interpretasi |
|---|---|---|---|---|
| A_top | 63 | 49,2 | **0,008** | signifikan tipis |
| A_feat | 50 | 13,4 | **< 0,001** | **enrichment terkuat (3,7×)** |
| A_sem | 82 | 72,2 | 0,138 | **tidak signifikans** |
| A_homo | 85 | 89,7 | 0,730 | **tidak signifikans (lebih rendah dari acak)** |

Ini membongkar asumsi dasar "multi-channel": **gabungan ketiga kanal (`A_homo`) justru menghapus pengayaan sindikat yang ada di kanal individual.** Kanal semantik (yang membawa bobot 0,41 dalam konstanta UI) tidak membedakan sindikat dari acak, dan A_homo lebih buruk dari acak. Yang benar-benar membedakan sindikat hanya kanal topologi dan kanal fitur.

**Klaim "mendeteksi klaster padat" (C-10) tidak dapat dioperasionalkan, dan ketika dioperasionalkan, hasilnya berlawanan dengan klaim.**

---

## 6. Audit Desain Evaluasi & Ablation

### 6.1 Split yang BENAR-BENAR dijalankan (verifikasi di kode)

`notebooks/Aegis-JKN.ipynb` cell 11:
- **Evaluasi 1** (`cell 11:14-47`): `GroupKFold(n_splits=5)` dengan `groups=df_claims['pasien_id']`. **Bukan** faskes.
- **Evaluasi 2** (`cell 11:53-80`): `LeaveOneGroupOut()` dengan `groups=df_claims['faskes_id']`.

Jadi koreksi terhadap duga-an awal: **LOGO memang memakai `faskes_id`**. Konfirmasi ini, bukan dugaan.

### 6.2 Dampak: setiap sindikat hidup di SATU faskes saja

Data nyata (`claims_300_v2.1.csv`), 9 sindikat:

| Sindikat | n | fraud | faskes | span faskes | dokter |
|---|---|---|---|---|---|
| SYND-01 | 3 | 3 | RS_A | **1** | D01, D02 |
| SYND-02 | 3 | 3 | RS_C | **1** | D05 |
| SYND-03 | 6 | 6 | RS_B | **1** | D07 |
| SYND-04 | 2 | 2 | RS_E | **1** | D09 |
| SYND-05 | 2 | **0** | RS_F | **1** | D08 |
| SYND-06 | 4 | 4 | RS_G | **1** | D13 |
| SYND-07 | 4 | 4 | RS_H | **1** | D14 |
| SYND-08 | 6 | 6 | RS_I | **1** | D15 |
| SYND-09 | 6 | 6 | RS_J | **1** | D19 |

**Tidak ada sindikat yang melintasi lebih dari satu faskes.** Implikasi pada LOGO(faskes):

| Fold holdout | n_val | fraud | sindikat di val | unseen di train | fraud dari sindikat unseen |
|---|---|---|---|---|---|
| RS_A | 29 | 3 | SYND-01 | SYND-01 | 3 |
| RS_C | 16 | 3 | SYND-02 | SYND-02 | 3 |
| RS_B | 21 | 6 | SYND-03 | SYND-03 | 6 |
| RS_E | 28 | 2 | SYND-04 | SYND-04 | 2 |
| RS_F | 32 | 0 | SYND-05 | SYND-05 | 0 |
| RS_D | 14 | 0 | - | - | 0 |
| RS_G | 45 | 5 | SYND-06 | SYND-06 | 4 |
| RS_H | 37 | 5 | SYND-07 | SYND-07 | 4 |
| RS_I | 36 | 6 | SYND-08 | SYND-08 | 6 |
| RS_J | 42 | 6 | SYND-09 | SYND-09 | 6 |
| **TOTAL** | **300** | **36** | | | **34 (94,4%)** |

**Pada LOGO(faskes), 34 dari 36 kasus fraud (94,4%) berasal dari sindikat yang TIDAK PERNAH muncul di fold training.** Model tidak mungkin mendeteksi pola sindikat (posisi, komposisi, relasi) yang belum pernah dilihat. Yang terukur di LOGO adalah generalisasi ke **faskes baru** - bukan generalisasi ke **sindikat baru**. Keduanya klaim berbeda.

Pada `GroupKFold(5)` by `pasien_id`: setiap sindikat punya 1-3 pasien berdekatan. Emulasi greedy: 4 dari 5 fold memiliki **semua** sindikatnya terlihat di train; hanya fold 0 yang punya SYND-09 unseen (6 kasus fraud). Total **6/36 (16,7%)** fraud dari sindikat unseen.

### 6.3 Verdict dampak (nilai koreksi)

Duga-an awal "deteksi sindikat jadi tidak terukur" **benar untuk LOGO(faskes)**, dan **hampir tidak berlaku untuk GroupKFold(pasien)**. Yang perlu diperbaiki di narasi:
- **LOGO(faskes) tidak boleh dipakai untuk klaim "deteksi sindikat/fraud ring"**. Ia sah untuk klaim "generalisasi ke fasilitas baru" - tapi itu klaim yang lebih lemah dan tidak ada di dokumen.
- **Hit-rate per sindikat di cell 13 tidak dihitung pada split apa pun** (lihat §6.5) - jadi ia tidak boleh dipakai untuk mendukung klaim mana pun tentang generalisasi.
- Untuk mengukur klaim sindikat yang sebenarnya (deteksi pola kolusi yang belum pernah terlihat), split yang benar adalah **grouped by sindikat** (hold-out sindikat), yang **tidak ada** di notebook.

### 6.4 Graph leakage: adjacency dibangun SEBELUM split (P0)

**Ya, terjadi. Dikonfirmasi di kode.**

`notebooks/Aegis-JKN.ipynb` cell 7:83:
```python
graphs = construct_multichannel_graphs(df_claims, X_clean, theta_feat=0.85)
```
Dieksekusi **sekali di luar loop fold**. Lalu di `cell 11:29` dan `cell 11:67`:
```python
logits, _ = fold_model(X_tensor, graphs['adj_top'], graphs['adj_feat'], graphs['adj_sem'])
loss = criterion(logits[tr_idx], y_target_tensor[tr_idx])
```
`X_tensor` juga **seluruh 300 baris** (`cell 11:5`), diindeks per fold (`tr_idx`, `val_idx`).

Artinya:
1. **Adjacency node validasi sudah ada di matriks training.** `A_top` dibangun dengan aturan "same patient OR same doctor OR same faskes + rujukan identik" (`cell 7:17-24`) → node validasi **terhubung** ke node training melalui faskes yang sama. Message passing di node training menerima informasi node validasi.
2. **Normalisasi `D^-1/2 Ã D^-1/2` dihitung sekali di atas 300 node** (`cell 7:62-70`), sehingga derajat node training bergantung pada keberadaan node validasi.
3. **`A_feat` threshold 0,85 ditentukan di atas seluruh 300 node** (`cell 7:34`) - hyperparameter "dipilih" dengan melihat data test.
4. **Feature scaler di-fit di atas 300 baris** (`cell 5:58-59` `scaler.fit_transform(feat_df.values)`), termasuk `diagnosis_code`/`prosedur_code` frequency dan top-10 dummy selection (`cell 5:46-53`) yang memakai seluruh data.
5. **Backend lebih ekstrem**: `pipeline.py:327-333` `run_pipeline()` membangun graf di luar loop training, dan `api/main.py:180-243` tidak punya split sama sekali.

**Skala dampaknya**: pada 300 baris dengan 40 pasien di 10 faskes, **setiap node training terhubung ke sebagian besar node validasi** lewat kanal topologi (degree faskes rata-rata 44). Jadi aliran informasi dari validasi ke training hampir total.

### 6.5 Benchmark utama di cell 13: seluruhnya in-sample (P0)

`notebooks/Aegis-JKN.ipynb` cell 13 - ini yang menghasilkan tabel yang ditampilkan di UI:

| Model | Baris | Cara |
|---|---|---|
| XGBoost | `cell 13:7-8` | `xgb_clf.fit(X_clean, y_target)` → `predict_proba(X_clean)` (**in-sample**) |
| Tabular MLP | `cell 13:36-37` | dilatih di `X_tensor` penuh → dievaluasi di `X_tensor` penuh (**in-sample**) |
| Homogeneous GCN | `cell 13:64-66` | dilatih di `X_tensor` penuh, adjacency penuh (**in-sample + graph leakage**) |
| **MHGSL** | `cell 13:80-82` | `final_mhgsl(X_tensor, graphs['adj_*'])` penuh (**in-sample + graph leakage**) |
| Metrik | `cell 13:111` | `compute_benchmark_metrics(y_fraud_gt, probs)` - **tanpa split** |

`cell 13:93-100` `compute_benchmark_metrics` tidak menerima parameter fold. Tidak ada out-of-fold. **Tabel AUPRC "XGBoost 0,71 / GNN 0,78 / Hybrid 0,85 / MHGSL 0,91" di `Aegis-JKN/src/components/mhgsl/data.ts:258-265` bukan hasil benchmark - ia hasil in-sample pada data yang sama, dan bahkan itu pun tidak disimpan ke file mana pun (notebook tanpa output: 0 karakter output di `notebooks/Aegis-JKN.ipynb`).**

### 6.6 Hit-rate per sindikat: tidak ada validasi (P0)

`cell 13:130-149` menghitung hit-rate per sindikat dari `probs_mhgsl` - **probabilitas in-sample** (`cell 13:90`). Tidak ada fold, tidak ada holdout.

`cell 13:154-155`:
```python
all_positive_hit = (synd_df['Hit-Rate'] > 0).all()
assert all_positive_hit, "PELANGGARAN: Ada sindikat dengan hit-rate 0!"
```
**Assertion ini adalah gate yang menjamin hasil**, bukan validasi. Karena probabilitas di atas 0,5 pada data in-sample hampir pasti menghasilkan hit-rate > 0 untuk semua sindikat, assertion ini **hanya bisa gagal jika model benar-benar salah total**. `cell 13:159` mencetak "Verifikasi: Setiap sindikat WAJIB memiliki Hit-Rate > 0% [STATUS: TERPENUHI 100%]" - menjadi **klaim**, padahal sebenarnya hanya memeriksa bahwa model tidak gagal total.

Selain itu, `is_fraud` ground truth: SYND-05 punya 2 klaim tapi **0 fraud** (lihat tabel §6.2). Jadi 2 dari 9 sindikat **tidak punya label positif** - hit-rate-nya dihitung terhadap `s_probs >= 0.5` atas klaim yang ground-truth-nya bukan fraud. Klaim "100% mendeteksi 9 pola sindikat" (`11-archive-proposal.md:30`) tidak dapat dibedakan dari noise pada SYND-05.

### 6.7 Metrik: AUPRC/AUROC appropriate?

**Secara pemilihan: ya. Secara implementasi: tidak.**

- AUPRC + AUROC + confusion matrix + FPR + calibration adalah **pilihan yang tepat** untuk kelas tidak seimbang dan **sudah diwajibkan** oleh `02-architecture.md:74` dan `08-training-protocol.md:34,38`. Bagus.
- **Masalah 1 (P0):** prevalensi aktual 12%, bukan 1-3%. AUPRC random baseline = 0,12. Semua angka perlu dipresentasikan **relatif terhadap baseline 0,12**, dan `02-architecture.md:74` meminta "jumlah kasus pada tiap kelas dan ambang keputusan" - yang tidak ada di UI.
- **Masalah 2 (P0):** `y_target` yang dilatih (`cell 11:6`) adalah `((is_fraud == 1) | (sindikat != 'none'))` - jadi target mencakup sindikat. Tapi metrik dievaluasi terhadap `y_fraud_gt` (`cell 11:7`) = `is_fraud` saja. **Training target dan evaluation target berbeda**; model dilatih untuk tugas lebih besar lalu dinilai dengan metrik tugas lebih kecil. Tidak salah secara formal, tapi harus dinyatakan eksplisit dan konsisten di semua laporan.
- **Masalah 3 (P1):** `02-architecture.md:72` mensyaratkan "Ablation harus menghilangkan satu kanal pada satu waktu". **Tidak ada ablation di notebook maupun backend.** Yang ada hanya baseline homogen (`A_homo`, `cell 7:59`) yang menggabungkan ketiga kanal - itu bukan ablation, itu model berbeda.
- **Masalah 4 (P1):** **Eksperimen masking/kamuflase tidak diimplementasikan.** Grep `masking|mask_ratio|robustness_test|perturb` di `backend/src/` dan notebook → **0 hasil**. Klaim "ketahanan kamuflase 89,4% pada tingkat masking rujukan 40%" (`11-archive-proposal.md:30`, `:338`) **tidak ada kode yang mengukurnya**. `12-archive-architecture.md:74` bahkan meminta explain: "jelaskan apa yang dimasking, berapa proporsi edge yang diubah, apakah label dipertahankan" - belum dikerjakan.
- **Masalah 5 (P1):** `02-architecture.md:69` mensyaratkan "seluruh pemilihan fitur, normalisasi, thresholding, dan kalibrasi hanya menggunakan data yang diizinkan dalam setiap fold". **Dilanggar** (§6.4).

### 6.8 XAI per-saluran: secara teknis mungkin?

**Secara teknis: ya, tapi implementasi sekarang bukan SHAP dan tidak valid secara matematis.**

- **Terverifikasi salah**: `backend/src/models/mhgsl.py:195-205` `get_channel_contributions` menghitung `torch.norm(outputs['topological'][node_idx])` per kanal - **L2 norm dari embedding**, bukan Shapley value. `data-uploader.tsx:102-134` bahkan lebih sederhana: rata-rata cosine + konstanta.
- **Masalah matematis mendasar** (F12): additivitas SHAP terhadap probabilitas sigmoid tidak holds. Output sigmoid non-linear → dekomposisi additif hanya valid di **logit space** (DeepSHAP pada logit) atau terhadap log-odds.
- **Bisa dilakukan dengan benar**: shap `DeepExplainer` pada logit, dengan 4 "feature groups" = kanal (via masker kanal), memberi φ yang additif terhadap logit. Channel-group SHAP sudah ada di literatur (GNNExplainer, SubgraphX). Secara teknis **mudah** dan **tidak memerlukan model tambahan** - cukup memakai model PyTorch yang sudah ada.
- **Yang benar-benar mustahil**: `mhgsl-theory.md:236` menyimpulkan φ_top<0 "membuktikan adanya upaya kamuflase aktif". SHAP adalah atribusi terhadap output model, **bukan** deteksi intent. `02-architecture.md:38` sudah menyatakan "SHAP tidak boleh digambarkan sebagai bukti kausal" - prinsip proyek sendiri, dilanggar oleh dokumen teori.

---

## 7. TABEL OVERCLAIM

| # | Klaim | File:baris | Bukti yang ada | Bukti yang dibutuhkan | Severity |
|---|---|---|---|---|---|
| C-01 | "Akurasi 93,0%, Presisi 94,12%, ROC-AUC 0,9825, AUPRC 0,9142 (+28,6% vs XGBoost 0,71)" | `corpus/11-archive-proposal.md:30`; `:329`; `:338` | **Nol**. `12-archive-architecture.md:55` menyatakan angka = adaptasi literatur. `04-evidence-matrix.md:34` (E-07) "Belum tereproduksi". `06-research-notes.md:42` "Belum dapat direproduksi". | Eksperimen out-of-fold di 300 baris + dataset publik, dengan split manifest, prediksi per klaim, dan skrip metrik (`02-architecture.md:75-86`) | **P0** |
| C-02 | "AUPRC +20%, false negatives −42% vs baseline" | `corpus/12-archive-architecture.md:30`; `Aegis-JKN/src/components/mhgsl/data.ts:23`; `i18n.tsx:211,560`; `comparison.tsx:203`; `dataset-explorer.tsx:1800`; `backend/src/api/main.py:365-397` | Nol. `12-archive-architecture.md:55` melabelinya adaptasi literatur. Angka di UI/backend **hardcode identik**. | Perbandingan out-of-fold XGBoost vs MHGSL di split yang sama, dengan CI bootstrap | **P0** |
| C-03 | "MHGSL AUPRC 0,91" ditampilkan sebagai hasil terukur | `Aegis-JKN/src/components/mhgsl/data.ts:264`; `comparison.tsx:377`; `backend/src/api/main.py:390` | **Tidak ada output notebook tersimpan** (`notebooks/Aegis-JKN.ipynb` = 0 karakter output). Angka berasal dari in-sample (`cell 13:111`). | Benchmark out-of-fold tersimpan sebagai artefak + UI membaca dari API hasil, bukan konstanta | **P0** |
| C-04 | "100% mendeteksi 9 pola sindikat terorganisir (SYND-01 s/d SYND-09)" | `corpus/11-archive-proposal.md:30`; `:376` | `cell 13:130-149` hit-rate in-sample; `cell 13:154` **assertion** (bukan validasi). SYND-05 punya **0 label fraud** (n=2), jadi hit-rate-nya noise. | Hit-rate out-of-fold **per sindikat**, dengan ground truth-review independen, plus split syndicate-level (hold-out sindikat) | **P0** |
| C-05 | "Ketahanan kamuflase 89,4% pada tingkat masking rujukan 40%" | `corpus/11-archive-proposal.md:30`; `:338` | **Tidak ada kode masking sama sekali** (grep `masking|perturb` → 0 di `backend/src/` dan notebook). | Implementasi eksperimen masking + laporan sesuai `02-architecture.md:74` (apa yang dimasking, % edge diubah, label dipertahankan, metrik) | **P0** |
| C-06 | "Memproses miliaran relasi antar-entitas" | `Aegis-JKN/docs/architecture/system-design.md:12` | Data = 300 klaim. Backend `pipeline.py:270-275` membangun A_top dengan loop Python ganda `for i: for j:` (O(n²) iterasi Python), dan `pipeline.py:281` menghitung `sim_matrix` 300×300 lewat dense dot product. Pada 300 klaim ini murah, tapi tidak akan menskala ke ribuan klaim. | Benchmark throughput nyata (claims/detik) pada 300 / 30k / 300k klaim, dengan justifikasi kompleksitas | **P1** |
| C-07 | "Tier-3 PyTorch Geometric HeteroData GCN" | `corpus/11-archive-proposal.md:26`; `:316`; `:398` | `backend/src/models/mhgsl.py:15` pakai `GCNConv` **homogen**, bukan `HeteroData`. Notebook cell 9 **tanpa PyG sama sekali** (manual `torch.matmul`). `HeteroData` = 0 di kode. `12-archive-architecture.md:49` mengakui "Graf Belum Terintegrasi" + `edges.json` belum ada. | Implementasi `HeteroData` sungguhan, atau koreksi deskripsi di seluruh dokumen | **P0** |
| C-08 | "Nilai negatif W_top = −0,12 membuktikan saluran topologi direkayasa" | `corpus/11-archive-proposal.md:220`; `Aegis-JKN/docs/algorithms/mhgsl-theory.md:236` | `MultiChannelAttention.channel_weights` diinisialisasi `ones/4` lalu softmax → **tidak mungkin negatif** (`mhgsl.py:82`, `cell 9:57`). Nilai −0,12 hanya konstanta hardcode di `data-uploader.tsx:132` dan `backend/src/oasis/simulation.py:100`. | Bobot kanal yang **dipelajari** + uji signifikasi; hapus klaim "membuktikan" | **P0** |
| C-09 | "SHAP Attribution Decomposition Engine" / "Atribusi per-saluran" | `Aegis-JKN/docs/algorithms/mhgsl-theory.md:144`; `:203-213`; `Aegis-JKN/src/components/mhgsl/data.ts:254`; `i18n.tsx:362-363`; `backend/src/models/mhgsl.py:181-205` | Implementasi = **L2 norm per kanal** (`mhgsl.py:201-204`), bukan Shapley marginal expectation. `data-uploader.tsx` = konstanta. Angka UI "semantic +41%, feature +38%, topology −12%" (`i18n.tsx:363`) adalah **literal yang sama** dengan konstanta hardcode fusion `data-uploader.tsx:132` dan `simulation.py:100`, bukan hasil atribusi model. | DeepSHAP pada logit space dengan channel masking, validasi additivitas (sum φ == logit − baseline) | **P1** |
| C-10 | "Deteksi Sindikat (Fraud Ring): Sangat kuat (klaster padat)" | `Aegis-JKN/src/components/mhgsl/data.ts:251` | "Subgraf padat" **tidak terdefinisi** di repo (grep `densest\|clique\|community\|louvain\|cluster_coeff` → 0). A_feat densitas hanya **2,11%** (1.892 edge / 300 node). **Ketika audit menghitungnya sendiri (§5.5), hasilnya berlawanan dengan klaim**: densest-subgraph A_feat (48 node) dan clique maksimum (10 node) **tidak berisi satu pun klaim fraud**; A_feat terbagi ke 41 komponen terhubung dengan 20 node terisolasi, dan 6 dari 36 node fraud terisolasi (tidak punya edge fitur). | Definisi formal (mis. densest-subgraph via Charikar) + nilai terukur + perbandingan terhadap baseline GNN pada metrik yang sama | **P1** |
| C-11 | "Multi-Channel **Attention** Fusion" | `Aegis-JKN/docs/architecture/system-design.md:142`; `Aegis-JKN/docs/algorithms/mhgsl-theory.md:131-133` | Kedua dokumen menulis **concat** (`mhgsl-theory.md:132` `H(final) = Concat(...)`); attention hanya ada di proposal (`11-archive-proposal.md:219`) dan di kode. | Sinkronkan istilah dengan isi, atau implementasikan gating sesuai rumus proposal | **P1** |
| C-12 | "Rasio fraud aktual 1% - 3%" | `Aegis-JKN/docs/algorithms/mhgsl-theory.md:191` | Data aktual: **36/300 = 12,0%** (`is_fraud==1`). `corpus/06-research-notes.md:41` sendiri: "Belum layak digunakan sebagai fakta". | Sumber primer dengan definisi fraud + denominator, **atau** koreksi ke angka data aktual | **P1** |
| C-13 | "Keunggulan mutlak arsitektur MHGSL" | `corpus/11-archive-proposal.md:338` | Tidak ada teorema, tidak ada benchmark valid, tidak ada ablation. | Lihat C-01. Plus uji signifikasi (paired t-test sudah direncanakan di `12-archive-architecture.md:182` tapi belum dijalankan) | **P1** |
| C-14 | "Estimasi penyelamatan Rp 507.370.000" / "60 klaim anomali" | `corpus/11-archive-proposal.md:30`; `:344-348` | **Rekonsiliasi internal sesuai** (koreksi atas duga-an awal audit ini): `11-archive-proposal.md:344-348` memecah 300 klaim menjadi auto_clear 240 (Rp 2.685.550.000), review 24 (Rp 279.950.000, koreksi Rp 112.420.000 = 40,16%), escalate 36 (Rp 561.150.000, overcharge Rp 394.950.000 = 70,38%). **Recompute dari `claims_300_v2.1.csv` cocok persis** di setiap angka: 240/24/36, Rp 2.685.550.000 / Rp 279.950.000 / Rp 561.150.000, total Rp 3.526.650.000, dan Rp 112.420.000 + Rp 394.950.000 = **Rp 507.370.000** (60,32% dari Rp 841.100.000, rata-rata Rp 8.456.167 per klaim). Jadi angka proposal **tertrace penuh ke data**. Yang **tidak** ada adalah *justifikasi*: tidak ada kolom overcharge per klaim, tidak ada tarif acuan INA-CBG, tidak ada status adjudikasi (tabel `:348` menyebut "Potensi Koreksi" dan "Overcharge Terbukti" tanpa sumber). `04-evidence-matrix.md:38` (E-11) sendiri menyatakan "Belum dapat direproduksi per klaim". | Tarif acuan INA-CBG per kode diagnosis/prosedur + tabel overcharge per klaim + status adjudikasi (review/confirm/reject) + daftar 60 klaim. Angka sudah benar, yang belum ada adalah *dasar tariff*-nya | **P1** |
| C-15 | "menyelamatkan ratusan miliar rupiah Dana Jaminan Sosial (DJS) Kesehatan setiap tahun." | `corpus/11-archive-proposal.md:30` | Ekstrapolasi dari 300 klaim sintetis tanpa basis rate. `06-research-notes.md:43` "Harus dibedakan dari potensi kerugian". | Analisis sensitivitas berbasis asumsi + sumber primer resmi | **P1** |
| C-16 | "MHGSL sebagai terobosan / State-of-the-art" | `corpus/11-archive-proposal.md:30`; `:407`; `corpus/12-archive-architecture.md:30` | `12-archive-architecture.md:30` **mengakui** MHGSL "diadaptasi dari paper Hong et al., Heliyon 2024" yang deskripsinya (3 kanal topologi/fitur/semantik + GCN spesifik + shared) **identik**. Novelty = adaptasi domain, bukan metode. | Verifikasi literatur (full-text Hong et al. 2024) + statement novelty yang jujur: "domain adaptation 3-kanal untuk klaim JKN" | **P1** |
| C-17 | "Client-side MHGSL Inference" | `Aegis-JKN/docs/architecture/system-design.md:195` | `data-uploader.tsx:28-30` komentar: "A **simplified** MHGSL-style fraud scoring **demo**". Bukan model MHGSL; heuristik konstanta hardcode. | Implementasi inferensi model terlatih di backend (sudah ada endpoint) atau label ulang eksplisit sebagai "demo heuristik" | **P2** |
| C-18 | "Cosine atas (LOS, biaya, qty obat)" | `corpus/10-simulation-dataset.md:12`; `14-index.md:58`; `09-draft-hub.md:15`; `Aegis-JKN/src/components/mhgsl/data.ts:156` | Implementasi notebook memakai **34 fitur** (cell 5:20-53) yang **tidak termasuk** usia, LOS sebagai elemen cosine, atau kuantitas obat (hanya `jumlah_obat` = jumlah jenis). `data.ts:156` menyebut "(LOS, usia, rasio biaya)" - tidak ada di kode mana pun. | Satu definisi vektor fitur cosine, dipakai bersama oleh notebook, backend, dan dokumen | **P2** |
| C-19 | "Kecepatan 2 juta klaim/hari" | `corpus/11-archive-proposal.md:17`; `:140` | `pipeline.py:271-283` loop Python ganda O(n²) untuk A_feat; `pipeline.py:276-280` loop O(n²) untuk A_top. 300 klaim = 90.000 iterasi Python. 2 juta/hari butuh redesign (blocking/Faiss/approx-NN). | Benchmark throughput + analisis kompleksitas | **P1** |
| **C-21** | **"Multi-channel lebih baik daripada satu kanal"** (implisit di seluruh argumen arsitektur 3 kanal) | `Aegis-JKN/docs/algorithms/mhgsl-theory.md:36-40`; `:178-182`; `Aegis-JKN/src/components/mhgsl/data.ts:250` | **Terbantah oleh data**: permutation test 20.000 iterasi atas 36 node sindikat (§5.5) menunjukkan pengayaan sindikat **hanya di A_top (p=0,008) dan A_feat (p<0,001)**, sedangkan **A_sem tidak signifikan (p=0,138)** dan **gabungan `A_homo` justru lebih buruk dari acak (p=0,730)**. Kanal semantik, yang membawa bobot tertinggi (0,41) di konstanta UI, **tidak membedakan sindikat dari pasangan acak**. Karena tidak ada ablation (§6.7), tidak ada satu pun bukti bahwa menggabungkan tiga kanal lebih baik daripada kanal topologi saja. | Ablation out-of-fold per kanal (E-03) + permutation test enrichment sindikat per kanal, dengan-bootstrap CI | **P0** |
| C-20 | "Berbasis bukti / zero data leakage terverifikasi & reproduktibilitas seed deterministik 100%" | `corpus/11-archive-proposal.md:398` | **Seed global ternyata ada dan benar**: `notebooks/Aegis-JKN.ipynb` cell 1 menyetel `SEED = 42` plus `random.seed`, `np.random.seed`, `torch.manual_seed`, `torch.cuda.manual_seed_all`; `cell 13:7,9` memakai `random_state=SEED` untuk XGBoost dan GradientBoosting. Yang **tidak** ada: `torch.use_deterministic_algorithms(True)` dan `cudnn.deterministic`, sehingga klaim "deterministik 100%" belum terpenuhi. Dan **graph leakage ada** (§6.4), sehingga "zero data leakage terverifikasi" **tidak benar**. | `torch.use_deterministic_algorithms(True)` + `cudnn.deterministic=True`, seed per fold, dan fix graph-per-fold | **P0** |

> Catatan: koreksi terhadap duga-an awal. Seed global **terbukti diset** di cell 1 notebook, jadi bagian "reproduktibilitas seed" dari klaim C-20 pada dasarnya terpenuhi. Yang gagal adalah (a) determinisme PyTorch level CUDA dan (b) klaim "zero data leakage", karena adjacency dibangun sebelum split (§6.4) dan benchmark cell 13 sepenuhnya in-sample (§6.5). Klaim C-20 tetap P0 karena bagian leakagenya, bukan karena seed.

---

## 8. Eksperimen Minimum untuk Membenarkan Klaim

Prasyarat: **hitung ulang adjacency per fold** (construct di dalam loop, dengan scaler & threshold di-fit hanya pada train) dan **simpan output ke file** (`notebooks/Aegis-JKN.ipynb` sekarang 0 karakter output).

| # | Eksperimen | Protocol | Artifact wajib | Klaim yang dihidupkan |
|---|---|---|---|---|
| **E-01** | **Benchmark out-of-fold yang benar** | 5× repeated GroupKFold(5) by `pasien_id` (10 run, seed 0-9). Train & evaluate **hanya** pada fold. Z-score & θ di-fit pada train saja. Hitung AUPRC/AUROC/F1/P@Top20% + bootstrap CI (10k resample). | `fold_predictions.csv` (claim_id, fold, seed, y_true, y_prob, model) | C-01, C-02, C-03, C-13 |
| **E-02** | **Splits per-sindikat (yang benar untuk klaim sindikat)** | Hold-out sindikat: 9 fold, tiap fold menahan 1 sindikat. Laporkan hit-rate sindikat yang **belum pernah dilihat**. | `syndicate_holdout_results.csv` | C-04, C-10, dan inti klaim "deteksi fraud ring" |
| **E-03** | **Ablasi per-saluran** | 4 konfigurasi: top-only, feat-only, sem-only, dan full-3-saluran (shared selalu on). Plus full tanpa-shared. **Tidak ada `A_homo` sebagai pengganti ablation.** | `ablation_results.csv` (ΔAUPRC per kanal) | Kontribusi kanal, `02-architecture.md:72` |
| **E-04** | **Sensitivitas θ_feat** | Sweep θ ∈ {0,50, 0,65, 0,75, 0,85, 0,92, 0,95} di dalam fold (never global). Plot AUPRC vs θ. Ambil satu θ dan **laporkan kurvanya**. | `theta_sensitivity.csv` | F3, §3.2 (empat nilai berbeda) |
| **E-05** | **Eksperimen masking/kamuflase** | Mask X% edge topologi (X ∈ {0, 20, 40, 60%}), **pertahankan label**, ukur degradasi AUPRC tiap model. Laporkan apa yang dimasking, % edge, apakah label bertahan (`02-architecture.md:74`). | `masking_results.csv` | C-05 |
| **E-06** | **Logo(faskes) yang jujur** | Jalankan LOGO(faskes) yang sudah ada, tapi **laporkan bahwa 94,4% kasus fraud berasal dari sindikat unseen**; jangan gunakan untuk klaim sindikat. Tambahkan metrik "generalisasi faskes baru" terpisah. | `logo_faskes_report.md` | Membatasi narasi LOO vs sindikat (§6.3) |
| **E-07** | **SHAP per-saluran yang valid** | `DeepExplainer` pada **logit**, dengan masker channel-group. Verifikasi additivitas: `Σφ == logit − baseline` (toleransi 1e-4). Ganti `get_channel_contributions` (`mhgsl.py:181-205`) agar memakai ini. | `shap_channel_values.csv` + uji additivitas | C-09, dan hapus klaim "membuktikan intent" (C-08) |
| **E-08** | **Reproduksi dataset publik** | Jalankan pipeline yang sama pada [Kaggle Healthcare Provider Fraud Detection (CC0)](https://www.kaggle.com/datasets/rohitrox/healthcare-provider-fraud-detection-analysis) yang sudah direncanakan di `12-archive-architecture.md:56`. Ini satu-satunya cara validasi eksternal yang tersedia tanpa izin BPJS. | `public_dataset_results/` | C-01, C-16 |
| **E-09** | **Dasar tarif klaim keuangan** | Angka `Rp 507.370.000` **sudah rekonsiliasi** dengan data (lihat C-14). Yang belum ada adalah *dasar tariff*-nya: tarif acuan INA-CBG per kode diagnosis/prosedur, tabel overcharge per klaim, dan status adjudikasi per kasus. | `overcharge_derivation.csv` (60 klaim, tarif acuan, selisih, status adjudikasi) | C-14, C-15 |
| **E-10** | **Verifikasi literatur Hong et al. 2024** | Baca full-text `https://www.cell.com/heliyon/fulltext/S2405-8440(24)06076-6` (DOI 10.1016/j.heliyon.2024.e30045). Tetapkan tabel "apa yang sama / apa yang beda / apa yang baru" vs MHGSL. | `literature_comparison.md` | C-16, positioning novelty |
| **E-11** | **Baseline relatif terhadap prevalensi** | Setiap tabel wajib menampilkan AUPRC random-baseline (0,12 pada data ini) dan `precision@recall=0.9`. Ambang 0,85 harus dinyatakan sebagai **titik operating** dengan capacity review, bukan angka sakral. | `metrics_with_baseline.csv` | C-12, interpretasi metrik |
| **E-12** | **Benchmark throughput** | Ukur claims/detik pada 300 / 30k / 300k klaim dengan sparse ops (blocking/approx-NN), bukan loop O(n²) Python. | `throughput_benchmark.md` | C-06, C-19 |
| **E-13** | **Uji enrichment multi-channel** | Untuk tiap kanal (top, feat, sem, homo) hitung pairs sindikat vs pairs acak (permutation test ≥20.000 iterasi), plus densest-subgraph, max clique, dan k-core. Bandingkan dengan baseline acak dan laporkan **komposisi fraud** tiap struktur padat. Prasyarat: E-03. | `channel_enrichment.csv` + `dense_structure_report.md` | C-10, C-21 |

---

## 9. Lampiran: Ringkasan Angka Kunci (terukur)

| Metrik | Nilai | Sumber |
|---|---|---|
| Klaim / pasien / dokter / faskes / sindikat | 300 / 40 / 20 / 10 / 9 | `claims_300_v2.1.csv` |
| Label fraud | 36 (**12,0%**) | `is_fraud==1` |
| Densitas A_top (off-diag) | 7,63% (6.840 edge) | reproduksi cell 7 |
| Densitas A_feat @θ=0,85 (off-diag) | **2,11%** (1.892 edge) | reproduksi cell 7 |
| Densitas A_sem (off-diag) | 11,17% (10.018 edge) | reproduksi cell 7 |
| Densitas A_homo (off-diag) | 13,85% (12.426 edge) | reproduksi cell 7 |
| Pasangan > θ=0,85 | 946 dari 44.850 (2,11%); 1.892 edge berarah | reproduksi cell 7 |
| Densitas A_feat pada θ=0,50 (backend) | 8,06% (3.613 pasangan = 7.226 edge berarah) | reproduksi cell 7 |
| Graf entitas (P/D/F/S/Dx) | 91 node, 204 edge; derajat mean 26,11 median 12 maks 99 | rekonstruksi |
| Parameter MHGSL (d=34, d_h=48) | **37.157** (GCN 16.128 + Attn 9.412 + Clf 11.617) | hitung dari `cell 9` |
| Rasio parameter : baris data | 124 : 1 | 37.157 / 300 |
| Rasio parameter : edge A_homo | 1,5 : 1 | 37.157 / 24.852 |
| Fraud dalam sindikat unseen (LOGO faskes) | **34 / 36 = 94,4%** | dihitung dari data |
| Fraud dalam sindikat unseen (GroupKFold pasien) | 6 / 36 = 16,7% (hanya fold 0) | dihitung dari data |
| Kasus fraud per fold LOGO | rata-rata 3,6 (36/10) | dihitung dari data |
| Sindikat dengan 0 label fraud | 1 (SYND-05, n=2) | dihitung dari data |
| Total biaya 300 klaim | Rp 3.526.650.000 (cocok proposal `:344-347`) | dihitung dari data |
| Non-low (60 klaim) sum biaya | Rp 841.100.000 | dihitung dari data |
| fraud+high (50 klaim) sum biaya | Rp 830.250.000 | dihitung dari data |
| Rekonsiliasi "Penyelamatan Riil" | **Rp 112.420.000 (review 24) + Rp 394.950.000 (escalate 36) = Rp 507.370.000** | dihitung dari data, cocok `11-archive-proposal.md:347-348` |
| `Skor Fraud` == T+F+S | **258 / 300 baris identik** (13 lain dalam 0,011) | dihitung dari data |
| Baris dengan `φ_top` negatif | **0 / 300** (syarat CamouflageSignature) | dihitung dari data |
| Output tersimpan di `notebooks/Aegis-JKN.ipynb` | **0 karakter** | verifikasi |
| File `.py` / `.ipynb` di repo web `Aegis-JKN` | **0 / 0** | verifikasi |
| `HeteroData` di seluruh repo ML | **0 kemunculan di kode** | verifikasi |
| Eksperimen masking di repo ML | **0** | verifikasi |
| Ablasi per-saluran di repo ML | **0** | verifikasi |
| Perhitungan densest-subgraph / community | **0** | verifikasi |
| Komponen terhubung A_feat (θ=0,85) | 41 (terbesar 35 node); 20 node terisolasi | dihitung dari data |
| Clique maksimum A_feat (Bron-Kerbosch exact) | **10 node**, berisi **0/10 fraud** | dihitung dari data |
| k-core tertinggi A_feat | core-7, 14 node | dihitung dari data |
| Densest-subgraph A_feat (Charikar) | avg-degree 23,08, 48 node, **0/48 fraud** | dihitung dari data |
| A_feat: node fraud terisolasi | **6 / 36** | dihitung dari data |
| Enrichment sindikat A_top (perm test 20k) | 63 vs 49,2 mean acak, **p=0,008** | dihitung dari data |
| Enrichment sindikat A_feat (perm test 20k) | 50 vs 13,4 mean acak, **p<0,001** | dihitung dari data |
| Enrichment sindikat A_sem (perm test 20k) | 82 vs 72,2 mean acak, **p=0,138** (tidak signifikans) | dihitung dari data |
| Enrichment sindikat A_homo (perm test 20k) | 85 vs 89,7 mean acak, **p=0,730** (lebih buruk dari acak) | dihitung dari data |

**Catatan leakage label (P0 tambahan, Dataset):** kolom `Skor Fraud` pada `claims_v2_live.csv` adalah **jumlah deterministik** dari `Kontribusi Saluran` (T+F+S) pada 258 dari 300 baris (13 lainnya dalam toleransi pembulatan). Artinya skor akhir = jumlah kontribusi kanal, bukan hasil prediksi model. `08-training-protocol.md:22` sudah mewajibkan exclusion kolom ini dari fitur (dan `notebooks` cell 5:5-15 menerapkan `FORBIDDEN_COLUMNS` dengan benar untuk `skor_fraud`). Namun **dataset itu sendiri** constructed circularly, dan `Skor Fraud` dipakai sebagai **ground truth proxy** di UI (`data.ts` / `i18n.tsx`) sehingga angka yang ditampilkan vigorous ke back ke ground truth. Perlu dicatat agar tidak dipakai sebagai label.

---

## 10. Verdict Per Aspek

| Aspek | Verdict |
|---|---|
| Definisi MHGSL | **Valid secara akademis** sebagai multi-view heterogeneous GNN. Yang diklaim "Multi-Channel" memang bukan ensemble. |
| Novelty | **Defensif sebagai adaptasi domain, TIDAK defensible sebagai metode baru.** `12-archive-architecture.md:30` sendiri mengakui diadaptasi dari Hong et al. 2024. |
| Fusion mechanism | **Konsistensi rendah.** Teori & system-design = concat; proposal & kode = attention; bobot kanal = konstanta hardcode. |
| Klaim "> XGBoost" | **Tidak ada teorema, tidak ada benchmark valid, ada konfesi internal bahwa angkanya adaptasi literatur.** |
| Naming | **"Sequential Learning" misleading**: nol temporal modeling. |
| Implementasi | **Ada dan substansif** di `mechine-learning-deep-learning` (notebook + backend FastAPI/PyG). Repo web `Aegis-JKN` = **mock presentational** (SVG + konstanta). |
| Skala | **Tidak memadai** untuk klaim GNN: densitas A_feat 2,11%, parameter:baris = 124:1, 3,6 fraud/fold, 94,4% sindikat unseen di LOGO. |
| Evaluasi | **Rancangan Split benar (LOGO faskes ada), implementasi benchmarking salah**: cell 13 seluruhnya in-sample; graf & scaler dibangun sebelum split; tidak ada ablation; tidak ada masking. |
| XAI per-saluran | **Secara teknis mungkin** (DeepSHAP pada logit, channel masking), **implementasi sekarang bukan SHAP** (L2 norm) dan additivitas terhadap sigmoid tidak valid. |
| Overclaim | **21 klaim teridentifikasi**, 9 di level P0, 10 P1, 2 P2. Yang paling damaging: C-01/C-02/C-03/C-04/C-05, karena angka yang sama tampil di situs publik dan API backend sebagai hasil terukur, sementara `12-archive-architecture.md:55` menyatakan angka itu adaptasi literatur; lalu C-21, karena data menunjukkan gabungan kanal justru menghapus pengayaan sindikat yang ada di kanal individual. |
