# -*- coding: utf-8 -*-
"""
Module 2: BAB I (Pendahuluan), BAB II (RCA 5-Whys & Fishbone), BAB III (Value Proposition Aegis-JKN)
"""

import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from generate_aegis_proposal import (
    add_callout, add_heading_1, add_heading_2, add_heading_3,
    add_body, add_bullet, add_table_data
)

def build_bab_1_to_3(doc):
    # ==========================================
    # BAB I: PENDAHULUAN
    # ==========================================
    add_heading_1(doc, "BAB I: PENDAHULUAN")

    add_heading_2(doc, "1.1 Latar Belakang & Urgensi Nasional")
    add_body(doc, "Penyelenggaraan Program Jaminan Kesehatan Nasional (JKN) oleh Badan Penyelenggara Jaminan Sosial (BPJS) Kesehatan merupakan pilar fundamental dalam mewujudkan perlindungan kesehatan semesta (Universal Health Coverage) bagi seluruh rakyat Indonesia. Dengan cakupan kepesertaan yang telah melampaui 270 juta jiwa, BPJS Kesehatan mengelola salah satu ekosistem jaminan kesehatan dengan sistem single-payer terbesar di dunia. Keberhasilan program ini bergantung secara mutlak pada keberlanjutan likuiditas dan integritas Dana Jaminan Sosial (DJS) Kesehatan yang dihimpun dari iuran peserta dan subsidi pemerintah.")

    add_body(doc, "Secara operasional, skala masif ini menuntut sistem infrastruktur teknologi informasi BPJS Kesehatan untuk memproses rata-rata lebih dari dua juta lembar klaim layanan kesehatan setiap harinya yang diajukan oleh ribuan Fasilitas Kesehatan Rujukan Tingkat Lanjutan (FKRTL / Rumah Sakit) di seluruh penjuru tanah air. Di sisi lain, garis pertahanan verifikasi klaim di kantor cabang BPJS Kesehatan hanya didukung oleh sekitar 1.000 tenaga verifikator manusia. Ketimpangan rasio beban kerja ini sangat ekstrem: setiap verifikator secara teoritis memikul tanggung jawab menelaah rata-rata 2.000 lembar klaim per hari kerja, padahal kapasitas optimal telaah klinis mendalam seorang verifikator medis manusia hanya berkisar antara 50 hingga 70 berkas per hari.")

    add_body(doc, "Kesenjangan kapasitas kognitif yang mencapai 30 hingga 40 kali lipat ini memaksa proses verifikasi lapangan bertumpu pada pemeriksaan sampel acak (random sampling) dan aturan validasi administratif sederhana. Kondisi asimetri informasi yang sangat lebar antara pihak fasilitas kesehatan (penyedia layanan) dan pihak penjamin biaya (BPJS Kesehatan) ini membuka celah kerentanan sistemik yang memicu kebocoran anggaran DJS akibat klaim yang tidak sesuai ketentuan, inefisiensi penagihan, hingga tindakan kecurangan (fraud) yang terorganisir.")

    add_heading_2(doc, "1.2 Identifikasi Permasalahan Utama (Upcoding, Unbundling, & Fraud Rings)")
    add_body(doc, "Berdasarkan Peraturan Menteri Kesehatan Republik Indonesia Nomor 16 Tahun 2019 tentang Pencegahan dan Penanganan Kecurangan (Fraud) serta Pengendalian Gratifikasi dalam Penyelenggaraan JKN, potensi inefisiensi pembiayaan terbagi ke dalam beberapa tipologi kritis. Di lapangan, kecurangan klaim tidak lagi dilakukan secara sporadis oleh individu terisolasi, melainkan telah berevolusi menjadi pola kecurangan terstruktur yang melibatkan kolusi antarentitas:")

    add_bullet(doc, "Praktik manipulasi penetapan kode diagnosis utama atau penambahan kode diagnosis sekunder (komorbiditas/komplikasi) ke tingkat yang lebih parah (Severity Level I dinaikkan menjadi Level II atau III) tanpa didukung oleh rekam medis faktual, indikasi klinis, atau bukti pemeriksaan penunjang objektif (misalnya hasil biomarker laboratorium, hemodinamik, atau pencitraan radiologi). Contoh nyata adalah diagnosis gastritis ringan yang ditagihkan sebagai tindakan kateterisasi jantung PCI (kode 00.66) berbiaya puluhan juta rupiah, atau infark miokard akut tanpa bukti enzim jantung yang diklaim disertai syok kardiogenik guna melipatgandakan tarif klaim INA-CBG.", "a. Upcoding Severity Level: ")
    add_bullet(doc, "Penagihan klaim fiktif murni atas layanan medis atau tindakan bedah yang secara faktual tidak pernah diberikan kepada pasien. Modus ini sering disertai manipulasi durasi rawat inap (Length of Stay / LOS) yang dipersingkat secara ekstrem (misalnya tindakan bedah penggantian sendi panggul/hemiarthroplasty senilai Rp 44,75 juta dengan LOS hanya 1 hari tanpa rekam pemberian obat anestesi dan implan).", "b. Phantom Billing: ")
    add_bullet(doc, "Pemecahan satu paket prosedur tindakan terpadu yang seharusnya ditagihkan dalam satu episode kode INA-CBG menjadi beberapa klaim terpisah (misalnya prosedur kolesistektomi laparoskopi kode 51.23 yang ditagihkan terpisah dengan tindakan intubasi endotrakeal kode 96.04 pada hari yang sama) guna melipatgandakan penerimaan faskes.", "c. Unbundling (Fragmentasi Klaim): ")
    add_bullet(doc, "Kolusi rujukan terorganisir antara oknum dokter penanggung jawab pelayanan (DPJP) dengan fasilitas kesehatan tertentu melalui pola rujukan siklikal berulang pada interval terjadwal (7–8 hari pasca-kunjungan) untuk memaksimalkan utilitas klaim rawat jalan dan utilisasi kuota penagihan.", "d. Referral Churn & Fraud Ring: ")

    add_heading_2(doc, "1.3 Fenomena Topological Camouflage pada Ekosistem JKN")
    add_body(doc, "Tantangan terbesar yang membuat sistem pengawasan konvensional gagal mendeteksi sindikat kecurangan di BPJS Kesehatan adalah fenomena Kamuflase Topologis (Topological Camouflage). Pelaku kecurangan terorganisir telah mempelajari celah audit dan secara sengaja merancang struktur rujukan fisik mereka agar tampak normal dan patuh regulasi berjenjang (misalnya rujukan melalui FKTP yang sah, jadwal kunjungan yang tidak melampaui kuota ekstrem harian, dan penyebaran berkas ke beberapa dokter berbeda).")

    add_body(doc, "Akibatnya, jika dianalisis menggunakan metode audit konvensional, struktur graf topologi rujukan pelaku sindikat memiliki nilai sentralitas, derajat koneksi, dan koefisien pengelompokan yang identik dengan populasi fasilitas kesehatan normal. Model Machine Learning tabular (seperti XGBoost atau Random Forest) gagal mendeteksi pola ini karena mengevaluasi setiap berkas klaim secara terisolasi tanpa kesadaran relasional jaringan. Sementara itu, model graf homogen standar (seperti GCN atau GAT) juga gagal karena proses perataan tetangga (neighborhood aggregation) justru terkontaminasi oleh struktur kamuflase buatan pelaku. Diperlukan sebuah terobosan algoritma yang mampu membongkar kamuflase ini melalui integrasi multi-perspektif.")

    add_heading_2(doc, "1.4 Rumusan Masalah Inovasi")
    add_callout(doc, "RUMUSAN MASALAH UTAMA", "Tantangan Desain Sistem Fraud Intelligence Skala Nasional",
                "« Bagaimana merancang suatu sistem Fraud Intelligence & Clinical Decision Support System (CDSS) berbasis Multi-Hop Graph Structure Learning (MHGSL) yang mampu mendeteksi sindikat kecurangan terorganisir dan membongkar kamuflase topologi klaim JKN, dengan transparansi penalaran Explainable AI (XAI), kepatuhan mutlak terhadap UU PDP No. 27/2022, serta efisiensi komputasi yang siap menangani volume transaksi 2 juta klaim per hari? »")

    add_heading_2(doc, "1.5 Tujuan dan Sasaran Inovasi")
    add_body(doc, "Tujuan utama dari pengembangan Aegis-JKN adalah menghadirkan sistem pendukung keputusan cerdas bagi verifikator klaim BPJS Kesehatan guna mendeteksi anomali penagihan dan membongkar sindikat kecurangan secara dini, akurat, dan terukur. Sasaran strategis yang ditargetkan meliputi:")
    add_bullet(doc, "Mengembangkan mesin deteksi Multi-Channel Heterogeneous Graph Structure Learning (MHGSL) dengan dekomposisi 3 saluran (Topologi, Fitur, dan Semantik Metapath) yang terbukti unggul mendeteksi anomali relasional multi-hop dan kamuflase topologi.", "1. Sasaran Algoritmik: ")
    add_bullet(doc, "Mengintegrasikan pipeline Tri-Tier cerdas (Tier-1 Rule Engine <50 ms, Tier-2 Tabular XGBoost, dan Tier-3 PyTorch Geometric GNN + Multimodal Late Fusion) guna mencapai throughput pemrosesan tinggi yang hemat komputasi.", "2. Sasaran Arsitektural: ")
    add_bullet(doc, "Menyediakan lapisan Explainable AI (XAI) berbasis atribusi SHAP multi-saluran dan antarmuka visualisasi graf interaktif (Next.js 16) yang memangkas durasi telaah berkas verifikator sebesar 30-50% dan menekan alert fatigue.", "3. Sasaran Operasional: ")
    add_bullet(doc, "Menjamin kepatuhan absolut terhadap UU PDP No. 27/2022 dan UU Kesehatan No. 17/2023 melalui arsitektur private on-premise perimeter dengan salted SHA-256 pseudonymization dan de-identifikasi penuh data medis.", "4. Sasaran Kepatuhan Regulasi: ")
    add_bullet(doc, "Membuktikan kelayakan ekonomi sistem dengan target rasio Cost-to-Impact minimal 1 : 15 dalam melindungi Dana Jaminan Sosial (DJS) Kesehatan dari kebocoran pembiayaan.", "5. Sasaran Finansial: ")

    add_heading_2(doc, "1.6 Ruang Lingkup dan Batasan Sistem")
    add_body(doc, "Ruang lingkup inovasi Aegis-JKN difokuskan pada pengawasan klaim Fasilitas Kesehatan Rujukan Tingkat Lanjutan (FKRTL) rawat inap dan rawat jalan, mencakup sembilan modus sindikat kecurangan (SYND-01 s/d SYND-09) dengan interoperabilitas data standar SATUSEHAT HL7 FHIR R4 dan API V-Claim BPJS Kesehatan. Sistem diposisikan murni sebagai Clinical Decision Support System (CDSS) pendukung verifikator, bukan eksekutor vonis sanksi hukum otonom.")

    doc.add_page_break()

    # ==========================================
    # BAB II: ANALISIS AKAR MASALAH (ROOT CAUSE ANALYSIS)
    # ==========================================
    add_heading_1(doc, "BAB II: ANALISIS AKAR MASALAH (ROOT CAUSE ANALYSIS)")

    add_heading_2(doc, "2.1 Metodologi Analisis 5-Whys Kegagalan Deteksi Kolusi")
    add_body(doc, "Guna mengidentifikasi akar penyebab mengapa praktik kecurangan klaim dan sindikat rujukan terorganisir sulit dideteksi oleh mekanisme pengawasan eksisting, dilakukan penelusuran kausalitas mendalam menggunakan metodologi 5-Whys yang dirangkum pada Tabel 2.1.")

    t21_headers = ["Tingkat", "Pertanyaan Kausalitas", "Fakta / Kondisi Lapangan", "Implikasi Sistemik Aegis-JKN"]
    t21_data = [
        ["Why 1", "Mengapa sindikat kecurangan dan anomali klaim upcoding/unbundling lolos dari proses verifikasi BPJS?",
         "Verifikator manusia di kantor cabang BPJS Kesehatan hanya sempat menelaah sebagian kecil berkas klaim secara acak (sampling) akibat keterbatasan waktu.",
         "Dibutuhkan mesin triase cerdas yang memprioritaskan berkas anomali berisiko tinggi secara otomatis."],
        ["Why 2", "Mengapa verifikator manusia tidak dapat memeriksa seluruh berkas klaim yang masuk?",
         "Volume klaim harian mencapai >2.000.000 berkas, sementara jumlah verifikator hanya ~1.000 orang (beban 2.000 berkas/orang/hari vs kapasitas telaah 50-70 berkas/hari).",
         "Sistem harus memiliki arsitektur throughput tinggi yang mampu melakukan pra-penyaringan instan dalam fraksi milidetik."],
        ["Why 3", "Mengapa sistem verifikasi digital eksisting (V-Claim / E-Klaim) tidak mampu mendeteksi sindikat tersebut secara otomatis?",
         "Sistem eksisting hanya mengandalkan aturan administratif statis (rule-based deterministik) dan validasi kelengkapan berkas individual secara terisolasi.",
         "Dibutuhkan model AI yang mampu mengevaluasi korelasi implisit antar-klaim dan mendeteksi anomali statistik non-linear."],
        ["Why 4", "Mengapa model Machine Learning konvensional (seperti XGBoost / Random Forest) tetap gagal menangkap sindikat tersebut?",
         "Model tabular memperlakukan setiap klaim sebagai baris data independen (IID), buta terhadap struktur relasi jaringan antardokter, faskes, dan rujukan pasien.",
         "Diperlukan representasi data berbasis graf heterogen yang mampu memodelkan relasi kompleks multi-entitas."],
        ["Why 5", "Mengapa model graf homogen standar (GCN/GAT) tetap tidak mampu membongkar kolusi tersebut?",
         "Pelaku kecurangan menerapkan kamuflase topologis (topological camouflage) pada alur rujukan fisik agar tampak normal, sehingga meracuni algoritma perataan tetangga standar.",
         "Akar Masalah Fundamental: Ketiadaan model Multi-Channel Heterogeneous Graph Structure Learning (MHGSL) yang memisahkan kanal topologi, fitur, dan semantik metapath."]
    ]
    add_table_data(doc, t21_headers, t21_data, [50, 100, 120, 127])

    add_heading_2(doc, "2.2 Analisis Fishbone 4 Dimensi Kendala Audit Klaim JKN")
    add_body(doc, "Analisis akar masalah diperluas menggunakan kerangka diagram Fishbone (Ishikawa) 4 Dimensi (Man, Process, Technology/Data, Volume) guna memetakan seluruh faktor struktural penyebab inefisiensi pengawasan klaim, sebagaimana disajikan pada Tabel 2.2.")

    t22_headers = ["Dimensi Masalah", "Komponen Akar Penyebab Faktual", "Dampak pada Operasional Klaim JKN"]
    t22_data = [
        ["Man (Sumber Daya Manusia)",
         "1. Keterbatasan kapasitas verifikator (~1.000 orang untuk 2 juta klaim/hari).\n2. Kelelahan kognitif dan alert fatigue akibat ribuan false alarms pada sistem aturan lama.\n3. Disparitas latar belakang medis antarkantor cabang dalam menafsirkan resume klinis.",
         "Verifikasi mendalam tereduksi menjadi sekadar centang administratif; kasus fraud terstruktur lolos tanpa terdeteksi."],
        ["Process (Alur Bisnis & Audit)",
         "1. Paradigma audit bersifat post-facto (pasca-klaim dibayarkan), memicu risiko sengketa klaim (dispute) yang berlarut-larut dengan faskes.\n2. Ketiadaan mekanisme triase dinamis yang memilah berkas berdasarkan magnitude kerugian finansial.\n3. Penanganan audit rujukan dilakukan per-faskes secara parsial, tanpa visibilitas lintas-wilayah.",
         "Pengembalian kerugian DJS sangat lambat; faskes merasa diawasi secara tidak adil akibat ketiadaan transparansi bukti diskrepansi."],
        ["Technology & Data",
         "1. Aturan regex/deterministik konvensional kaku dan mudah diakali (gaming the system).\n2. Model ML tabular mengevaluasi klaim secara atomik (IID assumption), gagal menangkap kolusi multi-hop.\n3. Model graf standar terperangkap topological camouflage.\n4. Keterbatasan interoperabilitas data semantik antar-SIMRS.",
         "Sindikat kolusi dokter-faskes beroperasi tanpa hambatan di bawah radar sistem deteksi berbasis tabular."],
        ["Volume (Skala Transaksi)",
         "1. Ledakan volume 270+ juta peserta menghasilkan miliaran edge relasi kunjungan per tahun.\n2. Latensi komputasi inferensi graf pada seluruh data mentah berisiko membebani server transaksi inti.\n3. Ketiadaan arsitektur dual-path (streaming vs batch).",
         "Sistem rentan mengalami bottleneck dan antrean panjang jika dipaksakan menjalankan model AI berat secara serial."]
    ]
    add_table_data(doc, t22_headers, t22_data, [90, 150, 157])

    add_heading_2(doc, "2.3 Sintesis Akar Masalah: Kebutuhan Paradigma Graph Learning")
    add_body(doc, "Sintesis dari analisis 5-Whys dan Fishbone menunjukkan bahwa kegagalan deteksi fraud selama ini bukan semata-mata karena keterbatasan personel, melainkan karena ketiadaan paradigma representasi data yang tepat. Kecurangan terorganisir adalah masalah jaringan (network problem), bukan masalah baris data tabel (tabular problem). Oleh karena itu, solusi komputasi yang dibutuhkan adalah platform yang mampu memetakan interaksi multi-entitas ke dalam graf heterogen multi-saluran, membedah penyamaran topologis, dan menyajikannya secara terjelaskan kepada verifikator manusia.")

    doc.add_page_break()

    # ==========================================
    # BAB III: DESKRIPSI & VALUE PROPOSITION SOLUSI AEGIS-JKN
    # ==========================================
    add_heading_1(doc, "BAB III: DESKRIPSI & VALUE PROPOSITION SOLUSI AEGIS-JKN")

    add_heading_2(doc, "3.1 Gambaran Umum Platform Aegis-JKN")
    add_body(doc, "AEGIS-JKN adalah platform Fraud Intelligence dan Clinical Decision Support System (CDSS) generasi baru yang dirancang khusus untuk ekosistem BPJS Kesehatan. Sistem ini menggabungkan kekuatan penalaran berbasis aturan deterministik, klasifikasi statistik tabular, dan pembelajaran representasi graf heterogen multi-saluran (Multi-Hop Graph Structure Learning / MHGSL), yang diperkuat oleh simulasi multi-agen multimodal (OASIS) dan Explainable AI (XAI) dalam alur kerja Human-in-the-Loop.")

    add_heading_2(doc, "3.2 Value Proposition & Diferensiasi Strategis Multi-Channel")
    add_body(doc, "Aegis-JKN menghadirkan empat proposisi nilai utama yang menjadikannya terobosan strategis bagi BPJS Kesehatan:")
    add_bullet(doc, "Aegis-JKN memecah graf heterogen ke dalam 3 saluran matriks ketetanggaan terpisah: Saluran Topologi (A_top) untuk alur administrasi rujukan, Saluran Fitur (A_feat) untuk kemiripan atribut klinis dan biaya, serta Saluran Semantik Metapath (A_sem) untuk relasi penugasan klinis berbobot PathSim. Ketiganya diproses melalui dual-branch GCN (cabang privat dan cabang parameter-shared) yang disatukan oleh lapisan Attention Fusion otomatis.", "1. Terobosan Dekomposisi Tri-Channel MHGSL: ")
    add_bullet(doc, "Ketika pelaku sindikat merekayasa alur rujukan pada A_top agar tampak wajar (sehingga nilai atribusi SHAP phi_top < 0), sistem secara otomatis mendeteksi anomali kuat pada saluran fitur (phi_feat > 0) dan semantik (phi_sem > 0). Penyingkapan sinyal kontradiksi ini memberikan kemampuan membongkar fraud rings yang selama ini lolos dari audit konvensional.", "2. Pembongkaran Kamuflase Topologis (Camouflage Buster): ")
    add_bullet(doc, "Aegis-JKN tidak memberikan angka probabilitas kotak hitam yang membingungkan. Setiap berkas anomali dilengkapi penguraian kontribusi fitur SHAP per-kanal graf, visualisasi SVG interaktif subgraf sindikat, serta cuplikan bukti teks diskrepansi klinis yang siap diverifikasi dalam hitungan detik.", "3. Transparansi XAI & Mitigasi Alert Fatigue: ")
    add_bullet(doc, "Mengadopsi fork Discrete Event Simulator OASIS (CAMEL-AI v0.2.5) untuk memvalidasi ketahanan model terhadap 9 skenario sindikat secara sintetis sebelum diterjunkan ke data riil, menjamin kepatuhan penuh terhadap privasi data tanpa risiko etika.", "4. Validasi Pra-Deploy via Multi-Agent Simulation: ")

    add_heading_2(doc, "3.3 Analisis Komparatif Pendekatan Solusi")
    add_body(doc, "Tabel 3.1 menyajikan perbandingan komprehensif antara metode telaah manual, sistem rule-based murni, model Machine Learning tabular (XGBoost), model AI Generatif (LLM Black-Box), dan platform Aegis-JKN.")

    t31_headers = ["Parameter Komparasi", "Pemeriksaan Manual", "Rule-Based Murni", "Tabular ML (XGBoost)", "Pure LLM / Black-Box", "Aegis-JKN (Tri-Tier MHGSL)"]
    t31_data = [
        ["Kecepatan Telaah", "Sangat lambat (10-20 mnt/berkas)", "Instan (<10 ms)", "Sangat cepat (<50 ms)", "Lambat (1-5 dtk/berkas)", "Optimal (<50 ms rule, <500 ms stream)"],
        ["Deteksi Kolusi Multi-Hop", "Nol (terbatas ingatan verifikator)", "Nol (aturan bersifat lokal)", "Nol (asumsi independensi IID)", "Sangat rendah (konteks terbatas)", "Sangat Tinggi (Tri-Channel MHGSL GNN)"],
        ["Ketahanan Kamuflase", "Rendah (mudah terkecoh rujukan sah)", "Nol (mudah di-gaming)", "Rendah (terkecoh fitur rata-rata)", "Rendah (rawan halusinasi)", "Tinggi (89.4% akurasi pada 40% kamuflase)"],
        ["Explainability & Transparansi", "Tinggi (justifikasi manusia)", "Tinggi (log aturan ya/tidak)", "Sedang (SHAP tabular)", "Rendah (black-box / halusinasi)", "Sangat Tinggi (SHAP per-kanal & Graf SVG)"],
        ["Efisiensi Biaya Komputasi", "Sangat Mahal (biaya jam kerja)", "Sangat Murah (CPU rendah)", "Murah (CPU standar)", "Sangat Mahal (biaya API token)", "Sangat Efisien (On-premise Tri-Tier)"],
        ["Kepatuhan Privasi (UU PDP)", "Tinggi (akses internal)", "Tinggi (on-premise)", "Tinggi (on-premise)", "Rentan (kebocoran cloud API)", "Mutlak (Salted SHA-256 on-premise)"],
        ["Human Autonomy & Fail-Safe", "Manual penuh (100% manusia)", "Kaku (auto-reject rawan sengketa)", "Rentan salah vonis", "Risiko tinggi auto-hallucination", "Sempurna (CDSS murni + Safe-Mode Fallback)"]
    ]
    add_table_data(doc, t31_headers, t31_data, [60, 65, 65, 65, 65, 72])

    add_heading_2(doc, "3.4 Prinsip Right-Sized Hybrid Engineering & Dual-Path Processing")
    add_callout(doc, "PRINSIP RIGHT-SIZED HYBRID ENGINEERING", "Efisiensi Komputasi Melalui Integrasi Berlapis",
                "« Jangan pernah memaksakan seluruh beban 2 juta klaim harian ke dalam inferensi model graf yang berat. Selesaikan validasi administratif deterministik (<50 ms) di tingkat CPU, saring anomali statistik berbasis tabular, dan alokasikan komputasi Graph Neural Network secara cerdas untuk membongkar sindikat dan kamuflase terorganisir. »")

    add_body(doc, "Untuk menjamin skalabilitas komputasi pada volume transaksi BPJS Kesehatan (>2.000.000 klaim/hari), Aegis-JKN menerapkan arsitektur Dual-Path Processing: (1) Jalur Streaming Real-Time (<500 ms) yang mengevaluasi klaim individual menggunakan Redis feature-cache saat diunggah oleh faskes, serta (2) Jalur Daily Batch Graph Convolution yang melakukan pembaruan struktur graf nasional secara periodik menggunakan teknik subgraph sampling (GraphSAINT / Cluster-GCN). Pendekatan ini memastikan sistem beroperasi dengan efisiensi sumber daya maksimal tanpa mengorbankan akurasi deteksi.")

    doc.add_page_break()
    print("Bab 1 to 3 built successfully.")
