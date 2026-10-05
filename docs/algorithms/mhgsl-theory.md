# Theoretical and Mathematical Foundations of MHGSL

### Multi-Channel Heterogeneous Graph Structure Learning & Camouflage Detection

---

## 1. Introduction: The Problem of Topological Camouflage

Dalam skema penipuan asuransi kesehatan (khususnya skema kapitasi dan INA-CBG BPJS Kesehatan), pelaku kecurangan terorganisir telah mengembangkan mekanisme penghindaran (*evasion techniques*) canggih. Salah satu pola paling sulit dideteksi adalah **Topological Camouflage** (Kamuflase Topologis).

Secara formal, kamuflase topologi terjadi ketika pelaku penipuan sengaja membuat struktur interaksi layanan medis mereka menyerupai pola rujukan klinis yang normal:
- Pasien dirujuk melalui fasilitas kesehatan primer (FKTP) yang tampak sah.
- Alur rujukan fisik pasien ke dokter spesialis di rumah sakit (FKRTL) mengikuti regulasi berjenjang yang ada.
- Volume rujukan per dokter dibuat tidak melebihi kuota ekstrem pada tingkat individu.

Pada graf rujukan standar $G^{(top)} = (\mathcal{V}, \mathcal{E}^{(top)})$, simpul-simpul pelaku kecurangan memiliki derajat (*degree*), sentralitas (*betweenness*), dan koefisien pengelompokan (*clustering coefficient*) yang identik dengan populasi dokter dan faskes normal. Akibatnya:
1. **Model Tabular (XGBoost, Random Forest)** gagal karena mengevaluasi setiap klaim secara independen tanpa mempertimbangkan kesamaan atribut implisit antar-klaim.
2. **Homogeneous Graph Neural Networks (GCN, GAT)** gagal karena proses *message passing* merata-ratakan informasi tetangga yang sengaja dikamuflasekan, menyebabkan fenomena *oversmoothing* dan *label contamination*.

Untuk memecahkan kebuntuan ini, **Multi-Channel Heterogeneous Graph Structure Learning (MHGSL)** mengonstruksi ruang representasi multi-perspektif yang membedah jaringan dari sudut pandang topologi, kemiripan fitur atribut, dan relasi semantik tingkat tinggi.

---

## 2. Heterogeneous Graph Definition & Channel Formulation

Didefinisikan sebuah graf heterogen layanan kesehatan:

$$\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{T}_v, \mathcal{T}_e, \phi, \psi)$$

Di mana:
- $\mathcal{V}$ adalah himpunan seluruh simpul, dengan fungsi pemetaan tipe simpul $\phi: \mathcal{V} \to \mathcal{T}_v$.
- $\mathcal{T}_v = \{Pasien, Dokter, Faskes, Prosedur, Diagnosis\}$.
- $\mathcal{E}$ adalah himpunan seluruh sisi relasi, dengan fungsi pemetaan tipe relasi $\psi: \mathcal{E} \to \mathcal{T}_e$.
- $\mathbf{X} \in \mathbb{R}^{|\mathcal{V}| \times d}$ adalah matriks fitur awal seluruh simpul, di mana $\mathbf{x}_i \in \mathbb{R}^d$ merepresentasikan vektor atribut klinis dan demografis simpul $v_i$ (misal: usia, jenis kelamin, lama rawat inap/LOS, total biaya klaim, kode tarif regional).

MHGSL memproyeksikan graf heterogen ke dalam 3 saluran matriks ketetanggaan (*adjacency matrices*) terpisah:

$$\mathbb{A} = \left\{ \mathbf{A}^{(top)}, \mathbf{A}^{(feat)}, \mathbf{A}^{(sem)} \right\}$$

---

## 3. Mathematical Channel Formulations

### 3.1. Topology Channel ($\mathbf{A}^{(top)}$)
Matriks $\mathbf{A}^{(top)} \in \{0, 1\}^{|\mathcal{V}| \times |\mathcal{V}|}$ merepresentasikan keterhubungan operasional fisik yang tercatat dalam berkas pelayanan:

$$
A^{(top)}_{ij} = \begin{cases} 
1, & \text{jika } (v_i, v_j) \in \mathcal{E}_{referral} \cup \mathcal{E}_{practice} \cup \mathcal{E}_{treatment} \\ 
0, & \text{lainnya} 
\end{cases}
$$

Matriks ini merefleksikan alur fisik pasien $P_i \to$ dokter penanggung jawab $D_j \to$ faskes pelaksana $RS_k \to$ prosedur penanganan $S_m$.

### 3.2. Feature Channel ($\mathbf{A}^{(feat)}$) via Cosine Similarity
Untuk mendeteksi sindikat yang menduplikasi berkas atau melakukan klaim upcoding berjamaah, saluran fitur membangun relasi implisit antar-simpul bertipe sejenis berdasarkan kedekatan vektor fiturnya.

Kemiripan kosinus antara simpul $v_i$ dan $v_j$ didefinisikan sebagai:

$$
\text{Sim}_{feat}(\mathbf{x}_i, \mathbf{x}_j) = \frac{\mathbf{x}_i \cdot \mathbf{x}_j}{\|\mathbf{x}_i\|_2 \|\mathbf{x}_j\|_2} = \frac{\sum_{k=1}^d x_{ik} x_{jk}}{\sqrt{\sum_{k=1}^d x_{ik}^2} \sqrt{\sum_{k=1}^d x_{jk}^2}}
$$

Matriks ketetanggaan saluran fitur dibentuk dengan pemangkasan ambang batas (*thresholding*) $\theta_{feat} \in [0, 1]$:

$$
A^{(feat)}_{ij} = \begin{cases} 
\text{Sim}_{feat}(\mathbf{x}_i, \mathbf{x}_j), & \text{jika } \phi(v_i) = \phi(v_j) \text{ dan } \text{Sim}_{feat}(\mathbf{x}_i, \mathbf{x}_j) > \theta_{feat} \text{ untuk } i \neq j \\ 
0, & \text{lainnya} 
\end{cases}
$$

Dalam implementasi Aegis-JKN, nilai default $\theta_{feat} = 0.75$. Pasien $P_1, P_2, P_3$ dengan profil LOS identik 3,0 hari dan rasio biaya berhimpitan akan saling terhubung dengan bobot tinggi ($0.92, 0.88, 0.85$), membentuk klaster padat di $A^{(feat)}$ yang tidak terlihat di $A^{(top)}$.

### 3.3. Semantic Channel ($\mathbf{A}^{(sem)}$) via Metapath Discovery
Sebuah metapath $\mathcal{M}$ adalah skema relasi komposit yang menghubungkan tipe simpul $T_1$ ke $T_l$ melalui sekuens relasi:

$$\mathcal{M} = T_1 \xrightarrow{R_1} T_2 \xrightarrow{R_2} \cdots \xrightarrow{R_{l-1}} T_l$$

Untuk mendeteksi modus upcoding dan phantom billing, didefinisikan metapath komposit klinis:

$$\mathcal{M}_{upcoding} = \text{Dokter} \xrightarrow{\text{diagnoses}} \text{Diagnosis} \xrightarrow{\text{pairs\_with}} \text{Prosedur} \xrightarrow{\text{billed\_at}} \text{Faskes}$$

Matriks ketetanggaan semantik dihitung melalui perkalian terstandarisasi matriks relasi komposit (*commuting matrix*):

$$
\mathbf{C}_{\mathcal{M}} = \mathbf{A}_{(D, Dx)} \cdot \mathbf{A}_{(Dx, S)} \cdot \mathbf{A}_{(S, RS)}
$$

Di mana bobot tepi semantik ternormalisasi PathSim antar-pasangan entitas dihitung sebagai:

$$
A^{(sem)}_{ij} = \frac{2 \cdot C_{\mathcal{M}}(i, j)}{C_{\mathcal{M}}(i, i) + C_{\mathcal{M}}(j, j)}
$$

Metode ini secara khusus mengekspos dokter yang memiliki frekuensi tidak wajar dalam memasangkan diagnosis berbobot ringan ($Dx_{ringan}$, misal: faringitis atau dispepsia) dengan tindakan bedah bertarif INA-CBG tinggi ($S_{mahal}$).

---

## 4. Multi-Channel Graph Neural Network Architecture

Untuk memproses ketiga saluran secara simultan, MHGSL mengombinasikan konvolusi independen dan konvolusi berparameter bersama.

```
       +-------------------+       +-------------------+       +-------------------+
       |   Topology Graph  |       |   Feature Graph   |       |   Semantic Graph  |
       |      A(top)       |       |      A(feat)      |       |      A(sem)       |
       +-------------------+       +-------------------+       +-------------------+
                 |                           |                           |
        +--------+--------+         +--------+--------+         +--------+--------+
        |                 |         |                 |         |                 |
        v                 v         v                 v         v                 v
   +---------+       +---------++---------+       +---------++---------+       +---------+
   | Channel |       | Shared  || Channel |       | Shared  || Channel |       | Shared  |
   | Specific|       | Param   || Specific|       | Param   || Specific|       | Param   |
   | W(top)  |       | W(shared|| W(feat) |       | W(shared|| W(sem)  |       | W(shared|
   +---------+       +---------++---------+       +---------++---------+       +---------+
        |                 |         |                 |         |                 |
        v                 |         v                 |         v                 |
     H(top)               |      H(feat)              |       H(sem)              |
        |                 +---------+--------+--------+         |                 |
        |                                    |                  |                 |
        |                                    v                  |                 |
        |                                H(shared)              |                 |
        |                                    |                  |                 |
        +-------------------+----------------+------------------+                 |
                            |                                                     |
                            v                                                     |
             +-------------------------------------------------+                  |
             |       Attention-Based Fusion Layer              |                  |
             |  H(final) = Concat( H(top), H(feat), H(sem),    |                  |
             |                     H(shared) )                 |                  |
             +-------------------------------------------------+                  |
                                    |                                             |
                                    v                                             |
             +-------------------------------------------------+                  |
             |      Classification & Sigmoid Probability       |                  |
             |         y_hat = Sigmoid( H(final) * W_cls + b ) |                  |
             +-------------------------------------------------+                  |
                                    |                                             |
                                    v                                             |
             +-------------------------------------------------+                  |
             |    SHAP Attribution Decomposition Engine        |                  |
             |  phi(top) < 0  vs  phi(feat) > 0, phi(sem) > 0  |                  |
             +-------------------------------------------------+                  |
```

### 4.1. Channel-Specific GCN Layers
Untuk setiap saluran $k \in \{top, feat, sem\}$, dilakukan konvolusi spektral dengan matriks bobot privat $\mathbf{W}^{(k)} \in \mathbb{R}^{d \times d_h}$:

$$
\mathbf{H}^{(k)} = \sigma \left( \tilde{\mathbf{D}}_{(k)}^{-\frac{1}{2}} \tilde{\mathbf{A}}^{(k)} \tilde{\mathbf{D}}_{(k)}^{-\frac{1}{2}} \mathbf{X} \mathbf{W}^{(k)} \right)
$$

Di mana:
- $\tilde{\mathbf{A}}^{(k)} = \mathbf{A}^{(k)} + \mathbf{I}_N$ adalah matriks ketetanggaan dengan penambahan *self-loops*.
- $\tilde{\mathbf{D}}_{(k)}$ adalah matriks derajat diagonal: $\tilde{D}_{(k), ii} = \sum_j \tilde{A}^{(k)}_{ij}$.
- $\sigma(\cdot)$ adalah fungsi aktivasi non-linier (LeakyReLU dengan slope negatif 0.2).

### 4.2. Shared-Parameter GCN Layer
Untuk menangkap kesamaan struktural global dan bertindak sebagai regularisasi lintas saluran, lapisan GCN bersama menggunakan bobot $\mathbf{W}^{(shared)} \in \mathbb{R}^{d \times d_h}$:

$$
\mathbf{H}^{(shared,\, k)} = \sigma \left( \tilde{\mathbf{D}}_{(k)}^{-\frac{1}{2}} \tilde{\mathbf{A}}^{(k)} \tilde{\mathbf{D}}_{(k)}^{-\frac{1}{2}} \mathbf{X} \mathbf{W}^{(shared)} \right)
$$

Representasi bersama diagregasikan melalui operasi rata-rata saluran (*mean-pooling*):

$$
\mathbf{H}^{(shared)} = \frac{1}{3} \left( \mathbf{H}^{(shared,\, top)} + \mathbf{H}^{(shared,\, feat)} + \mathbf{H}^{(shared,\, sem)} \right)
$$

---

## 5. Multi-Channel Fusion & Classification

Seluruh representasi laten digabungkan ke dalam representasi terpadu $\mathbf{H}^{(final)} \in \mathbb{R}^{N \times 4d_h}$:

$$
\mathbf{H}^{(final)} = \left[ \mathbf{H}^{(top)} \,\|\, \mathbf{H}^{(feat)} \,\|\, \mathbf{H}^{(sem)} \,\|\, \mathbf{H}^{(shared)} \right]
$$

Vektor representasi akhir untuk setiap klaim atau simpul $v_i$ diproyeksikan ke probabilitas kecurangan:

$$
\hat{y}_i = \text{Sigmoid}\left( \mathbf{H}^{(final)}_i \mathbf{W}_{cls} + b \right) = \frac{1}{1 + e^{-(\mathbf{H}^{(final)}_i \mathbf{W}_{cls} + b)}}
$$

### Objective Function: Focal Binary Cross-Entropy
Mengingat ketidakseimbangan kelas ekstrem dalam klaim asuransi kesehatan (rasio fraud aktual berkisar 1% - 3%), model dilatih menggunakan **Focal Binary Cross-Entropy Loss**:

$$
\mathcal{L}_{focal} = - \frac{1}{N} \sum_{i=1}^N \left[ \alpha (1 - \hat{y}_i)^\gamma y_i \log(\hat{y}_i) + (1 - \alpha) \hat{y}_i^\gamma (1 - y_i) \log(1 - \hat{y}_i) \right]
$$

Parameter default: $\alpha = 0.75$, $\gamma = 2.0$.

---

## 6. SHAP Attribution & Camouflage Signature Formulation

Untuk memberikan transparansi audit kepada verifikator BPJS, Aegis-JKN menguraikan probabilitas prediksi $\hat{y}_i$ menjadi jumlah kontribusi aditif menggunakan nilai Shapley (*SHapley Additive exPlanations*):

$$
\hat{y}_i = \phi_0 + \phi_i^{(top)} + \phi_i^{(feat)} + \phi_i^{(sem)} + \phi_i^{(shared)} + \sum_{m} \phi_{i, m}^{(attr)}
$$

Di mana nilai kontribusi Shapley $\phi_c$ untuk saluran $c \in \{top, feat, sem\}$ dihitung melalui marginal expectation:

$$
\phi_c(x) = \sum_{S \subseteq \mathcal{C} \setminus \{c\}} \frac{|S|! (|\mathcal{C}| - |S| - 1)!}{|\mathcal{C}|!} \left[ f_x(S \cup \{c\}) - f_x(S) \right]
$$

### Definisi Matematis: Camouflage Signature
Kondisi kamuflase topologi didefinisikan secara formal sebagai konjungsi kondisi atribusi:

$$
\text{CamouflageSignature}(v_i) = \text{True} \iff \begin{cases} 
\hat{y}_i \ge \tau_{fraud} & (\text{Skor fraud keseluruhan tinggi, misal } \ge 0.85) \\ 
\phi_i^{(top)} < 0 & (\text{Topologi fisik menurunkan kecurigaan secara semu}) \\ 
\phi_i^{(feat)} > \lambda_{feat} & (\text{Kanal fitur mendeteksi anomali atribut kuat}) \\ 
\phi_i^{(sem)} > \lambda_{sem} & (\text{Kanal semantik mendeteksi metapath mencurigakan}) 
\end{cases}
$$

### Contoh Dekomposisi SHAP pada Kasus Simulasi
Pada kasus simulasi sindikat upcoding (Dr. A. Wijaya dan Pasien $P_1$):
- **Base Value ($\phi_0$)**: $0.20$
- **Topology Attribution ($\phi^{(top)}$)**: $-0.12$ (Jalur rujukan rumah sakit tampak normal dan teratur)
- **Feature Attribution ($\phi^{(feat)}$)**: $+0.38$ (LOS identik 3 hari dan biaya duplikat $P_1-P_2$)
- **Semantic Attribution ($\phi^{(sem)}$)**: $+0.41$ (Metapath Dx ringan $\to$ Bedah mahal berulang 14x)
- **Shared Attribution ($\phi^{(shared)}$)**: $+0.07$
- **Prediksi Akhir ($\hat{y}$)**: $0.20 - 0.12 + 0.38 + 0.41 + 0.07 = 0.94$ (**Fraud Terkonfirmasi**)

Kehadiran $\phi^{(top)} = -0.12$ secara matematis membuktikan adanya upaya kamuflase aktif yang berhasil dibongkar oleh saluran non-topologi.
