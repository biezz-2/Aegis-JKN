<!-- source: notion page 3ef3e603-1ab7-81d1-962a-f8955843ed0f -->

> **{'type': 'emoji', 'emoji': '🛡️'}** Sistem Aegis-JKN - Dokumen Strategis & Teknis Healthkathon BPJS Kesehatan 2026: 'Detect Smarter, Protect JKN'. Analisis kelayakan, arsitektur pemodelan multi-dimensi (MHGSL Multi-Channel Heterogeneous Graph Structure Learning + XAI/SHAP), interoperabilitas SATUSEHAT FHIR & V-Claim, kepatuhan UU PDP No. 27/2022, serta kerangka proposal presentasi 20 slide.
> **{'type': 'emoji', 'emoji': '💡'}** CATATAN EDITORIAL | Dokumen strategi sumber. Rujukan teknis terkendali adalah [Arsitektur Sistem dan Metodologi Teknis](https://app.notion.com/p/02-Aegis-JKN-Arsitektur-Sistem-dan-Metodologi-Teknis-4003e6031ab781efbcdac7b0dbdd0cad) dan [Research Evidence Matrix](https://app.notion.com/p/04-Research-Evidence-Matrix-and-Reference-Governance-4003e6031ab7814f8ac3f37808c0a4a5). Status implementasi dan klaim hasil perlu ditetapkan berdasarkan bukti, bukan rancangan saja.
Pengelolaan program Jaminan Kesehatan Nasional (JKN) oleh BPJS Kesehatan merupakan salah satu inisiatif jaminan sosial terbesar dan paling kompleks di dunia. Setiap harinya, sistem infrastruktur teknologi informasi BPJS Kesehatan harus memproses lebih dari dua juta klaim layanan kesehatan yang diajukan oleh berbagai tingkatan fasilitas kesehatan di seluruh Indonesia. Tantangan operasional terbesar yang dihadapi saat ini adalah ketidakseimbangan rasio antara volume klaim harian tersebut dengan kapasitas sumber daya manusia, di mana proses verifikasi hanya didukung oleh sekitar 1.000 petugas verifikator. Celah rasio yang sangat lebar ini secara empiris membuka ruang yang signifikan terhadap risiko inefisiensi, khususnya anomali penagihan dan tindakan kecurangan terstruktur (fraud), yang pada akhirnya mengancam ketahanan finansial program JKN secara keseluruhan.
Gagasan untuk mengembangkan sebuah aplikasi berbasis kecerdasan buatan (AI) yang bertugas mengekstraksi dokumen medis, menganalisis pola penagihan, dan mendeteksi anomali kecurangan merupakan ide yang tidak hanya sangat layak (feasible), tetapi juga memegang urgensi strategis yang fundamental. Berdasarkan parameter Healthkathon BPJS Kesehatan 2026 yang mengusung tema besar 'Detect Smarter, Protect JKN', dewan juri secara eksplisit mencari solusi yang melampaui analisis statistik deskriptif dasar. Ekosistem saat ini menuntut sebuah purwarupa sistem AI fungsional yang berpusat pada manusia (human-centric), terintegrasi dengan arsitektur rekam medis nasional, patuh secara absolut terhadap regulasi pelindungan data pribadi, dan terbukti mampu memberikan nilai penghematan ekonomi yang nyata.
Laporan riset analitik ini disusun untuk memberikan pemantapan pengetahuan (knowledge solidification) secara mendalam dan komprehensif. Melalui analisis ini, kerangka logika akan diurai mulai dari arsitektur teknis pemodelan Machine Learning tingkat lanjut, integrasi interoperabilitas ekosistem layanan kesehatan digital Indonesia, kepatuhan tata kelola privasi data, hingga strategi taktis dalam merancang kerangka logika aplikasi dan draf proposal yang siap memenangkan kompetisi.
---
## 1. Analisis Kelayakan Ide dan Identifikasi Ruang Lingkup Masalah
Membangun alat kecerdasan buatan untuk mengotomatisasi telaah dokumen medis merupakan langkah mitigasi yang berpotensi merevolusi ekosistem BPJS Kesehatan. Namun, sebuah solusi teknologi yang tidak memiliki jangkar pada permasalahan spesifik di lapangan akan berakhir sebagai sekadar gimik teknologi. Untuk membangun proposisi nilai yang meyakinkan, pengembang harus terlebih dahulu memahami taksonomi kecurangan yang menjadi fokus utama dalam efisiensi risiko JKN.
Fokus permasalahan yang diuraikan oleh BPJS Kesehatan terbagi ke dalam tiga pilar risiko utama:
- Risiko Fasilitas Kesehatan (Faskes): Area dengan potensi kebocoran finansial terbesar. Modus mencakup Phantom Billing (klaim layanan fiktif), Upcoding (manipulasi diagnosis untuk tarif INA-CBG lebih tinggi), Unbundling (pemecahan satu paket klaim), Prolonged Stay (perpanjangan hari rawat tanpa indikasi medis), dan Cloning rekam medis antar-pasien.
- Risiko Peserta JKN: Berakar pada manipulasi identitas dan penyalahgunaan hak layanan, seperti peminjaman kartu kepesertaan oleh pihak tidak berhak, kolusi penerbitan surat keterangan sakit fiktif, hingga manipulasi peresepan obat berbiaya tinggi untuk dijual kembali (drug diversion).
- Risiko Pemberi Kerja: Manipulasi administratif korporasi untuk menghindari kewajiban finansial, meliputi under-reporting upah (melaporkan gaji lebih rendah untuk memangkas iuran 4%), penahanan setoran iuran pekerja, dan misklasifikasi status hubungan kerja.
> **{'type': 'emoji', 'emoji': '🎯'}** Rekomendasi Strategis: Hindari membangun 'super app' yang mengklaim menyelesaikan semua masalah sekaligus. Fokuskan logika sistem pada satu use case bernilai tinggi misalnya mendeteksi upcoding dan phantom billing pada Fasilitas Kesehatan Rujukan Tingkat Lanjut (FKRTL). Presisi dan akurasi tinggi pada cakupan terukur jauh lebih bernilai di mata dewan juri daripada konsep luas tanpa kedalaman fungsional.
| Area Risiko JKN | Modus Operandi Utama | Pendekatan Solusi Logika AI |
| Fasilitas Kesehatan | Phantom Billing, Upcoding, Unbundling, Prolonged Stay, Cloning Rekam Medis. | Analisis anomali frekuensi kunjungan pasien, deteksi inkonsistensi diagnosis (ICD-10) vs tindakan (ICD-9-CM), serta pemodelan jaringan dokter-pasien. |
| Peserta Individual | Penyalahgunaan identitas, kolusi surat fiktif, penumpukan obat (drug diversion). | Autentikasi biometrik, analisis pola pergerakan geografis klaim, dan clustering pengambilan obat kronis yang melebihi dosis rasional. |
| Pemberi Kerja | Under-reporting upah, pendaftaran sebagian, manipulasi mutasi pekerja. | Ekstraksi dokumen penggajian (OCR/NLP), pemodelan silang data perpajakan, dan deteksi anomali tren pembayaran iuran bulanan. |
---
## 2. Pemantapan Basis Pengetahuan Kecerdasan Buatan dan Machine Learning
> ⚠️ PEMBERITAHUAN PERBAIKAN ARSITEKTUR (v2.1 - 2026-10-07)
> Analisis terbaru mengidentifikasi 10 kekurangan kritis dalam desain Aegis-JKN v2. Perbaikan berikut WAJIB diimplementasikan untuk memastikan platform validasi memenuhi syarat anti-leakage, group-aware evaluation, dan reproduksibilitas. Semua perbaikan ini akan diintegrasikan ke dalam roadmap Fase 0-3 dan protokol validasi.
Membangun solusi AI yang secara nyata berfungsi dan memberikan dampak positif membutuhkan transisi dari sistem penegakan aturan statis menuju pemodelan dinamis berbasis data. Lanskap kecerdasan buatan untuk industri asuransi kesehatan telah berevolusi secara signifikan, menuntut pengembang untuk memadukan berbagai paradigma komputasi guna mencapai akurasi optimal.
### 2.1. Keterbatasan Sistem Berbasis Aturan dan Transisi ke XGBoost
Selama bertahun-tahun, sistem pendeteksi kecurangan di sektor asuransi dan layanan kesehatan bertumpu pada rule-based systems yang ditulis secara manual oleh pakar klinis dan auditor. Sebagai contoh, sistem memblokir klaim prosedur persalinan pada pasien pria. Meskipun efektif untuk anomali mendasar, sistem ini memiliki kelemahan fatal: pelaku penipuan terus beradaptasi menghindari batasan parameter statis.
Oleh karena itu, Extreme Gradient Boosting (XGBoost) menjadi standar baseline industri untuk klasifikasi data tabular terstruktur. XGBoost membangun ansambel pohon keputusan (decision trees) secara sekuensial untuk mengoreksi residual prediksi sebelumnya. Pada data log penagihan klaim, model XGBoost secara konsisten memetakan pola non-linier berdimensi tinggi dengan skor F1 dan akurasi yang melampaui regresi logistik maupun SVM.
### 2.2. Inovasi Multi-Channel Heterogeneous Graph Structure Learning (MHGSL) untuk Deteksi Sindikat
XGBoost memproses setiap baris data secara independen dan mengabaikan topologi relasional antar-entitas. Padahal, kasus kecurangan layanan kesehatan skala besar umumnya melibatkan sindikat kolusi (fraud rings). [Graph Neural Networks (GNN) ](https://www.ibm.com/id-id/think/topics/graph-neural-network)memungkinkan ekosistem jaminan kesehatan direpresentasikan sebagai graf heterogen multidimensi, di mana pasien, dokter, rumah sakit, dan klaim menjadi simpul (nodes), sedangkan interaksi rujukan, peresepan, dan diagnosis menjadi sisi (edges).
Standar emas (state-of-the-art) yang diadopsi purwarupa Aegis-JKN adalah MHGSL (Multi-Channel Heterogeneous Graph Structure Learning), diadaptasi dari paper [Hong et al., Heliyon 2024](https://www.cell.com/heliyon/fulltext/S2405-8440(24)06076-6) serta varian [multiview heterogeneous information network dengan augmented graph structure learning, IEEE 2025](https://ieeexplore.ieee.org/document/10795440/): satu ekosistem JKN direpresentasikan sebagai tiga saluran graf paralel-topologi (relasi rujukan fisik), fitur (kemiripan cosine antar-vektor fitur, dengan ambang batas θ_feat), dan semantik (metapath klinis). Tiap saluran diproses oleh GCN spesifik-saluran W⁽ᵏ⁾, kemudian GCN parameter-bersama W⁽ˢʰᵃʳᵉᵈ⁾ memaksa konsistensi representasi lintas-saluran, sebelum embedding ketiga saluran difusi dan diproyeksikan ke Sigmoid menjadi probabilitas kecurangan beratribusi SHAP. Arsitektur ini terbukti mendominasi AUPRC (Area Under the Precision-Recall Curve) hingga +20% dibandingkan baseline XGBoost, menekan false negatives hingga 42%, dan menembus kamuflase sindikat yang lolos dari model tabular maupun hibrida GNN + XGBoost tunggal.
Sampai dataset riil JKN tersedia, seluruh angka benchmark tersebut diberi label adaptasi literatur - berasal dari eksperimen MHGSL pada data asuransi kesehatan riil ([Heliyon 2024](https://www.cell.com/heliyon/fulltext/S2405-8440(24)06076-6)) dan studi GNN klaim medis ([Scientific Reports 2025](https://www.nature.com/articles/s41598-025-22910-6)) - bukan hasil eksperimen internal.
Melalui mekanisme message-passing, MHGSL mengidentifikasi subgraf padat anomali sebagai collusive communities: klaim individu tampak valid dan lolos seleksi tabular, tetapi pola agregat simpul pasien-dokter-faskes yang terlalu rapat (kederajatan keterhubungan tinggi) terdeteksi sebagai satu unit sindikat terstruktur-bukan sekadar klaim individual. Kamuflase pada satu saluran terbongkar oleh dua saluran lainnya.
| Karakteristik Metodologi | Model Ensemble Tabular (XGBoost) | Graph Neural Networks (GNN) | MHGSL (Multi-Channel Graph Structure Learning) |
| Fokus Analisis Data | Atribut tunggal baris data secara independen (usia, jenis layanan, total tagihan). | Relasi, topologi, dan sentralitas antar-entitas di dalam ekosistem. | Fusi tiga saluran graf (topologi, fitur, semantik) melalui GCN spesifik-saluran dan GCN parameter-bersama. |
| Kelebihan Utama | Komputasi cepat, efisiensi memori tinggi, ketahanan terhadap missing values. | Unggul mendeteksi fraud rings, kolusi faskes, dan perulangan pasien tidak wajar. | Menembus kamuflase sindikat lintas-saluran: anomali numerik, komunitas kolusi, dan inkonsistensi semantik terdeteksi simultan. |
| Metrik Evaluasi Dominan | F1-Score tinggi pada prediksi kejadian biner terisolasi. | Meminimalisir False Negatives dari taktik penipuan siber modern. | Mendominasi pengujian AUPRC melawan XGBoost, GNN, maupun hibrida; false negatives turun hingga 42%. |
### 2.3. Explainable AI (XAI) sebagai Solusi atas Alert Fatigue
Tingkat akurasi tinggi tidak akan memiliki nilai operasional apabila pengguna akhir tidak mempercayainya. Model AI tradisional sering kali berupa 'black box' yang menghasilkan skor tanpa penalaran analitis, memicu fenomena alert fatigue bagi verifikator. Modul Explainable AI berbasis SHAP (SHapley Additive exPlanations) menghitung kontribusi marjinal tiap variabel terhadap hasil prediksi final.
> Contoh Atribusi Transparan SHAP pada Dasbor Auditor: 'Probabilitas kecurangan 92% didorong oleh ketidakwajaran durasi rawat inap (+35%) dan penggunaan implan berbiaya tinggi pada diagnosis primer yang tergolong ringan (+40%).'
### 2.4. Strategi Validasi Pra-Dataset: Literatur, Benchmark Publik, dan Simulasi Sintetis
> ⚠️ PEMBERITAHUAN PERBAIKAN DATASET & ARSITEKTUR (v2.1 - 2026-10-07)
> Dataset Aegis-JKN v2 (300 klaim) BELUM SESUAI untuk validasi platform karena 10 kekurangan kritis yang diidentifikasi dalam analisis terbaru. Perbaikan berikut WAJIB diimplementasikan untuk memastikan platform validasi memenuhi syarat anti-leakage, group-aware evaluation, dan reproduksibilitas:
> 
> | No | Masalah | Risiko | Solusi di v2.1 |
> |----|---------|--------|----------------|
> | 1 | Entity Leakage | Pasien/dokter/faskes yang sama muncul di train & test → metrik overestimated | ✅ Tambah kolom pasien_id, faskes_id, dokter_id + GroupKFold/LeaveOneGroupOut |
> | 2 | Score Leakage | Kolom turunan sistem (Skor Fraud, Sinyal SHAP, dll.) bocor ke fitur | ✅ Blokir di configs/leakage.yaml + unit test otomatis (test_leakage.py) |
> | 3 | n=300 Terlalu Kecil | Hasil hanya indikatif, varian tinggi antar-fold | ✅ Repeat CV (≥10 seed) + augmentasi DP-CTGAN (SDV) |
> | 4 | Graf Belum Terintegrasi | CSV tabular saja tidak cukup untuk MHGSL | ✅ Bangun ulang graf HeteroData dari CSV + edges.json di pipeline |
> | 5 | Oversampling 12% | AUPRC terlalu bagus (bias prevalensi) | ✅ Laporkan AUPRC pada prevalensi 3-7% (downsampling) |
> | 6 | LLM (Gemini) Bergantung API | Pipeline terblokir jika API key hilang | ✅ Modul opsional (toggle via configs/text.yaml), fallback ke heuristic lokal |
> 
> Lihat detail lengkap di halaman [Dataset Simulasi Aegis-JKN v2.1](https://app.notion.com/p/3f23e6031ab781bf99a7d3f1768f1708).
Tim belum memegang dataset klaim JKN riil - data peserta dan faskes dilarang digunakan tanpa izin resmi. Agar kelayakan tetap bisa dibuktikan tanpa data riil, strategi validasi disusun bertingkat:
- Pelabelan angka benchmark: seluruh metrik komparatif (AUPRC +20%, reduksi false negatives 42%) dilabeli sebagai adaptasi literatur dari [Hong et al., Heliyon 2024](https://www.cell.com/heliyon/fulltext/S2405-8440(24)06076-6) dan studi GNN klaim medis ([Scientific Reports 2025](https://www.nature.com/articles/s41598-025-22910-6)), bukan hasil eksperimen internal; angka dikalibrasi ulang saat data pilot Fase 3 tersedia.
- Dataset publik pembanding: pipeline diuji pada dataset publik [Healthcare Provider Fraud Detection (Kaggle, lisensi CC0)](https://www.kaggle.com/datasets/rohitrox/healthcare-provider-fraud-detection-analysis) berisi klaim rawat inap, rawat jalan, dan data beneficiary dengan label fraud level provider - struktur entitasnya kompatibel dengan graf pasien-dokter-faskes-prosedur MHGSL.
- Data sintetis DP-CTGAN: generator data sintetis privacy-by-design menjadi basis utama pengujian pipeline dengan distribusi yang meniru skema klaim INA-CBG (Subbab 4.2).
- Simulasi skenario purwarupa: kasus upcoding terselubung di RS_A pada purwarupa web menjadi uji konsep interaktif yang memperagakan akumulasi kontribusi tiap saluran terhadap skor fraud.
- Peta literatur baseline: review klasifikasi ML deteksi fraud kesehatan ([Journal of Big Data 2025](https://link.springer.com/article/10.1186/s40537-025-01295-3)) dan tinjauan sistematis ML klaim kesehatan ([PubMed 2024](https://pubmed.ncbi.nlm.nih.gov/39756221/)) memosisikan XGBoost, GNN, dan metode graf heterogen sebagai baseline pembanding.
> Implikasi metodologis: proposal harus jujur menyatakan posisi riset saat ini sebagai tahap pra-dataset - angka kinerja adalah target/proyeksi literatur, dan jalur pembuktiannya adalah eksperimen pada dataset publik + data sintetis, menuju validasi pilot 5 FKRTL pada Fase 3.
---
## 3. Arsitektur Interoperabilitas: V-Claim dan SATUSEHAT
> 📌 Catatan Tambahan untuk Arsitektur v2.1:
> - Kolom pasien_id, faskes_id, dokter_id akan digunakan untuk mapping ke FHIR R4 (Patient, Organization, Practitioner).
> - Graf HeteroData akan dibangun dari edges.json (70+ edges) dengan 3 saluran (topologi, fitur, semantik).
> - Anti-leakage diimplementasikan via configs/leakage.yaml dan unit test otomatis.
Aplikasi pendeteksi fraud harus terintegrasi dengan ekosistem digital layanan kesehatan nasional agar memiliki kelayakan deployment yang nyata di mata dewan juri.
### 3.1. Penyadapan Data melalui SATUSEHAT dan Standar HL7 FHIR R4
Sesuai Permenkes No. 24 Tahun 2022 tentang Rekam Medis Elektronik, pertukaran data medis nasional menggunakan protokol HL7 FHIR R4. Modul kunci yang diekstrak sebagai fitur Machine Learning meliputi:
- Encounter: Merekam episode kunjungan dan admisi pasien; mendeteksi anomali kunjungan berulang serta masa rawat inap berkepanjangan (prolonged stay).
- Condition: Menarik data diagnosis bersandi ICD-10 untuk menelusuri indikasi upcoding dan exaggerasi keparahan klinis.
- MedicationRequest & MedicationDispense: Memvalidasi keselarasan peresepan dokter dan penyerahan fisik farmasi terhadap panduan klinis dan Formularium Nasional (FORNAS).
- Composition: Mengekstraksi narasi bebas Resume Medis Elektronik untuk mendeteksi inkonsistensi antara deskripsi tindakan operasi dan penagihan akhir.
### 3.2. Integrasi Middleware dengan BPJS V-Claim dan E-Klaim
Solusi AI ditempatkan sebagai middleware layer antara SIMRS faskes dan server penagihan BPJS Kesehatan (V-Claim / E-Klaim). Sebelum berkas klaim final dikirimkan, berkas dipindai oleh mesin inferensi. Berkas dengan skor risiko rendah diproses otomatis tanpa hambatan, sedangkan berkas berisiko tinggi dialihkan ke panel antrean investigasi verifikator sebelum pencairan dana disetujui.
### 3.3. Analisis Narasi Klinis dan Sentimen Pasien (Modul LLM)
Selain saluran graf dan tabular, Aegis-JKN memproses saluran teks melalui modul LLM (Gemini) yang menganalisis empat sumber narasi pada setiap klaim:
- Alasan berobat (Encounter.reasonCode): keluhan utama pasien saat admit. Keluhan yang tidak sebangun dengan diagnosis atau tindakan yang ditagih merupakan indikasi awal upcoding.
- Rujukan (ServiceRequest): asal FKTP, nomor, tanggal, dan jenis rujukan. Rujukan yang tidak wajar atau tanggal rujukan yang bertentangan dengan tanggal layanan menjadi sinyal pendukung.
- Narasi Resume Medis Elektronik (Composition): deskripsi bebas tindakan yang benar-benar dilakukan, dibandingkan secara semantik dengan kode billing (ICD-10, ICD-9-CM, dan item obat).
- Umpan balik pasien (survei kepuasan, non-FHIR): kutipan pengalaman pasien pasca-layanan.
Dari keempat sumber tersebut, modul menghasilkan tiga sinyal tekstual:
1. Konsistensi narasi vs kode billing - misalnya narasi menyatakan pasien hanya menjalani endoskopi lambung, sementara tagihan memuat tindakan kateterisasi jantung (indikasi upcoding).
1. Kontradiksi pengakuan pasien - pasien menyatakan tindakan tertentu tidak pernah dilakukan namun ditagihkan (indikator kuat phantom billing).
1. Analisis sentimen keluhan - sentimen negatif terkait iur biaya, tagihan ganda, atau tindakan yang diragukan pasien menaikkan prioritas pemeriksaan.
Penting ditegaskan bahwa sentimen negatif bukan bukti fraud. Keluhan murni layanan (antrean panjang, sikap staf) berfungsi sebagai negative control: sistem harus mampu membedakan keluhan layanan dari keluhan penagihan. Skor tekstual tidak berdiri sendiri, melainkan dikonfirmasi silang dengan skor graf MHGSL melalui late fusion - sinyal teks hanya menaikkan prioritas investigasi bila konsisten dengan sinyal saluran topologi, fitur, dan semantik.
Untuk validasi dini modul ini sebelum data nyata tersedia, dataset simulasi 100 klaim sintetis telah disiapkan dengan ground truth tekstual: distribusi sentimen 62 positif, 14 netral, 24 negatif, dengan 8 klaim bertanda kontradiksi narasi pasien-billing sebagai kasus uji prioritas investigasi.
---
## 4. Analisis Kepatuhan Privasi Data, Etika, dan Keamanan Sistem (UU PDP)
### 4.1. Implikasi Hukum UU No. 27 Tahun 2022 (UU PDP)
Pasal 4 Ayat (2) UU PDP menetapkan data kesehatan, data biometrik, dan genetika sebagai 'Data Pribadi Spesifik' dengan standar kepatuhan tertinggi: persetujuan eksplisit, enkripsi mutakhir, penunjukan Data Protection Officer (DPO), serta kewajiban pelaporan kebocoran maksimal 3x24 jam. Pelanggaran membawa sanksi pidana 5-6 tahun dan denda miliaran rupiah (Pasal 65 & 66). Mengingat aturan Healthkathon 2026 melarang penggunaan data peserta riil tanpa izin resmi, penggunaan data asli faskes secara sembarangan berakibat diskualifikasi langsung.
### 4.2. Navigasi Privasi: Data Sintetis dengan Diferensial Privasi (DP-CTGAN)
Untuk mengatasi tantangan privasi, arsitektur menggunakan Conditional Tabular GAN dengan Differential Privacy (DP-CTGAN). Model generatif ini mempelajari distribusi statistik historis dan menghasilkan jutaan baris data rekam medis sintetis yang valid secara matematis namun mustahil direkayasa balik (reverse-engineering) untuk melacak identitas pasien asli (privacy-by-design).
### 4.3. Federated Learning untuk Ekstensibilitas Skala Nasional
Dalam visi jangka panjang, arsitektur Federated Learning mengirimkan algoritma ke server lokal faskes di balik firewall. Algoritma berlatih secara lokal pada data rumah sakit, lalu hanya mengirimkan pembaruan parameter matematis (bobot model) ke peladen pusat BPJS Kesehatan. Pendekatan ini memastikan model terus berkembang cerdas tanpa pernah memindahkan data rekam medis mentah ke internet publik.
---
## 5. Paradigma Operasional Taktis: Human-in-the-Loop (HITL) dan Active Learning
AI dilarang secara etis dan hukum untuk menolak klaim pengobatan secara otonom mutlak. Paradigma Human-in-the-Loop (HITL) memposisikan AI sebagai augmentasi kepakaran auditor manusia, bukan pengganti. AI melakukan pra-penyaringan 100% volume klaim dan mengeskalasi anomali atau kasus ambiguitas ke tim verifikator.
Keputusan verifikator (konfirmasi kecurigaan atau penolakan alarm palsu) dijadikan sinyal umpan balik (reward signals). Melalui Active Learning dan Direct Preference Optimization (DPO), bobot model dikalibrasi ulang secara berkesinambungan sehingga tingkat alarm palsu terus menurun seiring waktu operasional.
---
## 6. Kelayakan Ekonomi dan Manajemen Tokenomics Large Language Models (LLM)
Pemanfaatan model bahasa besar (LLM) seperti Google Gemini untuk ekstraksi teks rekam medis bebas memerlukan kalkulasi biaya per token (Tokenomics) yang terukur:
- Skema Biaya Operasional Gemini API: Gemini 1.5 Flash dialokasikan untuk pemrosesan curah (batch processing) berbiaya rendah ($0.10-$1.50 per 1M token input) pada ribuan diagnosis rawat jalan berisiko rendah. Gemini 1.5 Pro ($2.00 per 1M token) digunakan secara selektif untuk analisis mendalam pada kasus klaim rawat inap kritis dan ambigu.
- Proyeksi Nilai Ekonomi (ROI): Biaya komputasi API sebesar beberapa sen dolar per klaim sangat terjustifikasi secara ekonomi apabila mampu mencegah pencairan tagihan fiktif atau upcoding operasi bedah yang bernilai jutaan hingga puluhan juta rupiah.
---
## 7. Kerangka Logika Penyusunan Proposal Healthkathon 2026
> 📌 Pembaruan Roadmap untuk Proposal:
> - Fase 0: Fondasi & Audit Data (Minggu 1) → Dataset v2.1 + leakage.yaml + unit test
> - Fase 1: Baseline ML & DL (Minggu 2-3) → XGBoost + MLP + fitur graf turunan
> - Fase 2: Graf Heterogen & MHGSL (Minggu 4-6) → PyG HeteroData + SHAP per-saluran
> - Fase 3: Validasi Final (Minggu 7-8) → Benchmark Kaggle + DP-CTGAN + laporan validasi
> - Protokol Keputusan: Platform SESUAI jika ≥90% fraud terdeteksi (group-aware) dan MHGSL ≥ baseline.
Proposal diproyeksikan dalam format presentasi maksimal 20 slide (PDF <= 10 MB) dengan struktur sembilan bab strategis:
| Bagian | Fokus Isi & Penekanan Narasi |
| 1. Identitas & Positioning | Jenama Aegis-JKN (tervalidasi oleh purwarupa), tagline 'MHGSL Fraud Intelligence' berbasis XAI & multi-channel graph, fokus spesifik pada Efisiensi Risiko Faskes (Upcoding & Unbundling). |
| 2. Definisi Masalah & Urgensi | Kontras rasio 2.000.000 klaim harian vs 1.000 verifikator; mitigasi kebocoran dana jaminan sosial dengan data kuantitatif. Label estimasi: potensi fraud 3-7% dari total nilai klaim nasional adalah angka estimasi literatur untuk simulasi/ROI - belum berbasis dataset riil JKN; konteks nasional: ACCH KPK mencatat 175.774 klaim FKRTL berpotensi fraud hingga Juni 2015. |
| 3. Rancangan Solusi & Keunggulan | Transisi dari rule-based ke model adaptif; deteksi sindikat dengan MHGSL (tiga saluran graf: topologi, fitur, semantik) dan transparansi fitur dengan SHAP. |
| 4. Arsitektur Teknis & Data Pipeline | Alur: SATUSEHAT HL7 FHIR (Encounter, Condition, Medication) + API V-Claim -> Konstruksi 3 Saluran Graf (topologi, fitur, semantik) -> GCN Spesifik-Saluran + Parameter-Bersama -> Fusion + Sigmoid -> Dasbor Skor Fraud + SHAP. |
| 5. Validasi & Showcase Purwarupa | Purwarupa web interaktif Aegis-JKN ([aegisjkn.vercel.app](http://aegisjkn.vercel.app/)): visualisasi multi-channel graph, simulasi kasus upcoding terselubung di FKRTL (RS_A) dengan akumulasi kontribusi tiap saluran terhadap skor fraud, peragaan message-passing sindikat, benchmark AUPRC, dan formulasi matematis MHGSL. |
| 6. Cetak Biru Roadmap Implementasi | Fase 1 (0-3 bln: generator DP-CTGAN, baseline XGBoost + SMOTE, skema ingestion FHIR R4), Fase 2 (3-6 bln: SHAP per-saluran, integrasi V-Claim middleware, UAT dengan verifikator), Fase 3 (>6 bln: pilot 5 FKRTL, MHGSL + Active Learning/DPO, federated learning bayangan & HITL). |
| 7. Kuantifikasi Dampak & ROI | Reduksi waktu telaah per berkas dari 20 menit menjadi 3 menit; kapasitas efektif verifikator naik dari ±1.000 menjadi ±6.700 berkas; estimasi penghematan pilot 5 FKRTL (asumsi 3% fraud pada tagihan operasi bedah - label estimasi simulasi, bukan data riil) dan efisiensi cadangan DJS. |
| 8. Matriks Risiko, Etika & Privasi | Mitigasi data imbalanced (SMOTE), kepatuhan UU PDP No. 27/2022, privacy-by-design, serta retensi keputusan akhir di tangan auditor. |
| 9. Komposisi Tim & Keahlian | Tiga personel inti: Data Engineer (FHIR/GNN), UI/UX & XAI Developer (visualisasi klinis), serta Health Business & Regulatory Analyst. |
---
## 8. Kesimpulan dan Rekomendasi Arsitektural
> 🎯 Kesimpulan Terbaru (v2.1 - 2026-10-07):
> 1. Desain Aegis-JKN sudah 85% sempurna, tetapi 10 kekurangan kritis (terutama entity leakage, score leakage, dan integrasi graf) harus diperbaiki.
> 2. Dataset v2.1 (dengan kolom pasien_id, faskes_id, dokter_id) sudah sesuai untuk validasi platform.
> 3. Platform terbaik: Custom stack Ubuntu + PyTorch Geometric + XGBoost + MLflow + Streamlit.
> 4. MHGSL (PyG) + SHAP per-saluran adalah pilihan terbaik untuk deteksi fraud graf-sensitif.
> 5. Protokol validasi: Platform dinyatakan SESUAI jika ≥90% fraud terdeteksi (group-aware) dan MHGSL ≥ baseline.
Inisiatif pengembangan platform AI deteksi kecurangan klaim menjawab langsung tantangan ketimpangan kapasitas verifikasi di lingkungan BPJS Kesehatan. Agar mampu bertransformasi menjadi solusi kelas enterprise yang kredibel bagi pemangku kebijakan, arsitektur pemodelan harus berpusat pada MHGSL (Multi-Channel Heterogeneous Graph Structure Learning) yang memadukan tiga perspektif graf-topologi, fitur, dan semantik-melalui GCN spesifik-saluran dan parameter-bersama, dengan baseline tabular XGBoost sebagai pembanding.
Sistem wajib memberikan transparansi melalui Explainable AI (SHAP) untuk meredam alert fatigue. Melalui integrasi interoperabilitas SATUSEHAT HL7 FHIR dan V-Claim, jaminan privasi data berbasis DP-CTGAN dan Federated Learning, serta adopsi paradigma Human-in-the-Loop, solusi ini memadukan kepatuhan regulasi, efisiensi komputasi, dan empati keputusan klinis yang siap menjadi kandidat terdepan dalam Healthkathon BPJS Kesehatan 2026. Karena dataset riil belum tersedia, kredibilitas proposal Aegis-JKN dibangun melalui strategi validasi bertingkat (Subbab 2.4): pelabelan benchmark literatur, pengujian pada dataset publik, data sintetis DP-CTGAN, dan simulasi skenario pada purwarupa web.
---
## 🔧 LAMPIRAN: PERBAIKAN TEKNIS v2.1 (2026-10-07)
### 📌 Daftar Perubahan Dataset (v2 → v2.1)
| Aspek | v2 (Saat Ini) | v2.1 (Diperbarui) | Alasan |
| Kolom Grouping | Tidak ada | pasien_id, faskes_id, dokter_id | Anti-entity leakage |
| Metadata | Tidak ada | seed, version, timestamp | Reproduksibilitas |
| Leakage Blocklist | Tidak ada | configs/leakage.yaml | Blokir kolom turunan sistem |
| Unit Test | Tidak ada | tests/test_leakage.py | Validasi anti-leakage |
| Prevalensi | 12% (oversampled) | 12% + 3-7% (downsampling) | Realistis untuk produksi |
| Graf | CSV saja | HeteroData (3 saluran) | MHGSL siap pakai |
### 🏗️ Struktur Repositori v2.1
```javascript
aegis-jkn/
├── data/
│   ├── raw/
│   │   ├── claims_300_v2.1.csv       # + kolom grouping & metadata
│   │   ├── edges_v2.1.json           # 70+ edges (graf heterogen)
│   │   ├── text_gt_v2.1.csv          # Ground truth teks
│   │   └── leakage_blocklist.yaml    # Kolom terlarang
│   ├── processed/
│   │   ├── features_300.parquet     # Fitur bersih
│   │   └── graph_hetero.pt           # PyG HeteroData
├── configs/
│   ├── leakage.yaml                 # Blocklist kolom leakage
│   ├── model_xgb.yaml               # Hyperparameter XGBoost
│   ├── model_mlp.yaml               # Hyperparameter MLP
│   ├── model_mhgsl.yaml             # Hyperparameter MHGSL
│   └── text.yaml                    # Toggle LLM (on/off)
├── src/
│   ├── ingest.py                    # Muat & audit data
│   ├── features.py                  # Feature engineering
│   ├── graph_builder.py             # Konstruksi graf 3-saluran
│   ├── models/
│   │   ├── baseline_xgb.py         # XGBoost + SMOTE
│   │   ├── baseline_mlp.py          # MLP PyTorch
│   │   └── mhgsl.py                  # MHGSL (PyG)
│   ├── evaluate.py                  # GroupKFold, metrik, threshold sweep
│   ├── xai.py                       # SHAP per-saluran
│   └── report.py                    # Generate laporan
├── tests/
│   └── test_leakage.py              # Gagal keras jika leakage
├── mlruns/                          # MLflow artifacts
└── reports/                         # Laporan validasi
```
### 📊 Metrik & Protokol Validasi v2.1
| Kriteria | Ambang | Metode Verifikasi |
| Integritas Data | 300 baris utuh, 0 leakage | test_leakage.py |
| Deteksi Fraud | ≥90% fraud terdeteksi (antrian ≤20%) | evaluate.py (GroupKFold) |
| Metrik Utama | AUPRC & AUROC MHGSL ≥ baseline | evaluate.py (paired t-test) |
| Per-Sindikat | SYND-01-SYND-09 hit-rate > 0 | evaluate.py (per-sindikat analysis) |
| Konsistensi XAI | SHAP sejalan dengan Alasan | xai.py (korelasi SHAP vs Alasan) |
| Saluran Teks | 8 klaim kontradiksi masuk prioritas | text_processor.py |
| Kejujuran Label | Semua metrik berlabel "simulasi sintetis" | report.py |
### 🚀 Rencana Pelaksanaan (8 Minggu)
| Fase | Tujuan | Durasi | Output |
| Fase 0 | Fondasi & Audit Data | Minggu 1 | Dataset v2.1, leakage.yaml, unit test |
| Fase 1 | Baseline ML & DL | Minggu 2-3 | XGBoost + MLP + fitur graf turunan |
| Fase 2 | Graf Heterogen & MHGSL | Minggu 4-6 | PyG HeteroData, MHGSL, SHAP per-saluran |
| Fase 3 | Validasi Final & LLM | Minggu 7-8 | Laporan validasi, benchmark Kaggle, DP-CTGAN |
> Target: Platform SESUAI siap untuk Healthkathon 2026 dan pilot 5 FKRTL.
---