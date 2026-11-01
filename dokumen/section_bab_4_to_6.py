# -*- coding: utf-8 -*-
"""
Module 3: BAB IV (Arsitektur Pipeline & Formulasi MHGSL), BAB V (Tata Kelola Data & UU PDP), BAB VI (Human-in-the-Loop & XAI)
"""

import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from generate_aegis_proposal import (
    add_callout, add_heading_1, add_heading_2, add_heading_3,
    add_body, add_bullet, add_table_data
)

def build_bab_4_to_6(doc):
    # ==========================================
    # BAB IV: ARSITEKTUR & MEKANISME CARA KERJA SISTEM
    # ==========================================
    add_heading_1(doc, "BAB IV: ARSITEKTUR & MEKANISME CARA KERJA SISTEM")

    add_heading_2(doc, "4.1 End-to-End Workflow Pipeline & Dual-Path Production Inference")
    add_body(doc, "Arsitektur sistem Aegis-JKN dirancang sebagai sistem pendukung keputusan (Clinical Decision Support System / CDSS) berbasis microservices yang mengintegrasikan alur data dari fasilitas kesehatan hingga antarmuka verifikator BPJS Kesehatan. Alur kerja end-to-end terbagi ke dalam enam modul komputasi terpadu yang beroperasi melalui mekanisme Dual-Path Production Inference:")

    add_bullet(doc, "Klaim individual yang baru diajukan oleh FKRTL diproses dalam waktu <500 milidetik melalui cache fitur in-memory Redis, mengevaluasi aturan deterministik dan skoring graf lokal untuk memberikan indikasi awal sebelum berkas masuk ke antrean verifikasi cabang.", "1. Streaming Real-Time Scoring Path (<500 ms): ")
    add_bullet(doc, "Setiap malam (off-peak hours), mesin graf mengeksekusi konvolusi graf skala penuh terhadap miliaran relasi nasional menggunakan algoritma subgraph sampling (GraphSAINT / Cluster-GCN) guna memperbarui pemetaan sindikat kolusi (fraud rings) dan mendeteksi kamuflase lintas-wilayah.", "2. Daily Batch Graph Convolution Path: ")

    add_heading_2(doc, "4.2 Modul 1: Ingestion Data, Normalisasi SATUSEHAT, & Tokenisasi Anonim")
    add_body(doc, "Modul Ingestion bertugas menyadap dan menyelaraskan berkas klaim digital yang masuk melalui API V-Claim BPJS Kesehatan dan ekosistem SATUSEHAT Kemenkes RI. Setiap berkas dinormalisasi ke dalam standar format HL7 FHIR R4 yang mencakup resource: (1) Claim (total biaya penagihan, kode INA-CBG); (2) Encounter (durasi rawat/LOS, jenis rawat inap/jalan, tanggal masuk); (3) Condition (kode diagnosis ICD-10 utama dan sekunder); (4) Procedure (kode tindakan ICD-9-CM); serta (5) MedicationDispense / MedicationRequest (rincian obat dan restriksi FORNAS).")

    add_body(doc, "Sesuai mandat UU PDP No. 27/2022, seluruh data identitas langsung (PII) seperti NIK, Nomor Kartu JKN, Nama Peserta, dan Nomor Rekam Medis langsung ditokenisasi in-memory menggunakan algoritma salted SHA-256 sebelum data disimpan ke dalam basis data analitik. Nomor identitas entitas (Pasien, Dokter, Faskes) diisolasi hanya untuk keperluan konstruksi topologi graf dan validasi kelompok (group cross-validation).")

    add_heading_2(doc, "4.3 Modul 2: Tier-1 Deterministic Rule-Based Pre-Filter")
    add_body(doc, "Modul kedua mengeksekusi saringan aturan deterministik berbasis regulasi baku Kementerian Kesehatan (Permenkes No. 16/2019, Permenkes No. 26/2021, dan Formularium Nasional / FORNAS). Aturan deterministik dijalankan secara instan di tingkat CPU dengan latensi <50 ms per berkas:")
    add_bullet(doc, "Validasi kesesuaian tindakan medis terhadap usia dan jenis kelamin (misal: penagihan prosedur histerektomi pada pasien pria, atau tindakan katarak senilis pada pasien neonatus).", "a. Inkompatibilitas Demografis: ")
    add_bullet(doc, "Pendeteksian klaim ganda atas pasien, diagnosis, dan tanggal pelayanan yang identik pada faskes yang sama atau faskes berbeda.", "b. Duplikasi Klaim Mutlak: ")
    add_bullet(doc, "Pendeteksian pemecahan prosedur laparoskopi dan laparotomi atau tindakan intubasi pada paket pembedahan yang sama (pelanggaran unbundling eksplisit).", "c. Restriksi Prosedur & Paket INA-CBG: ")
    add_bullet(doc, "Pengecekan batas kuota restriksi obat khusus FORNAS dan durasi rawat inap minimum klinis (misal: penagihan klaim rawat inap bedah mayor dengan LOS 0 hari).", "d. Batas Kritis FORNAS & LOS: ")
    add_body(doc, "Filter Tier-1 ini secara instan meloloskan 40-60% klaim normal (fast-track auto-clear) dan menandai pelanggaran administratif kasar, sehingga komputasi cerdas dapat difokuskan pada berkas-berkas anomali klinis dan sindikat.")

    add_heading_2(doc, "4.4 Modul 3: Tier-2 Tabular Classifier & Tier-3 Tri-Channel MHGSL Engine")
    add_body(doc, "Bagi klaim yang memerlukan analisis mendalam, berkas dialirkan ke Tier-2 Tabular Classifier (XGBoost) untuk penyaringan statistik 10 fitur bersih (log_biaya, los_hari, log_cost_per_day, rasio frekuensi faskes-dokter, dsb.), serta Tier-3 Tri-Channel Multi-Hop Graph Structure Learning (MHGSL) yang menjadi keunggulan inti Aegis-JKN.")

    add_heading_3(doc, "4.4.1 Formulasi Matematis Graf Heterogen")
    add_body(doc, "Didefinisikan sebuah graf heterogen layanan kesehatan G = (V, E, Tv, Te), di mana himpunan simpul V mencakup lima tipe entitas: Pasien (P), Dokter DPJP (D), Faskes / RS (RS), Prosedur ICD-9-CM (Proc), dan Diagnosis ICD-10 (Diag), yang dihubungkan oleh relasi interaksi medis E. Graf ini didekomposisi ke dalam 3 saluran matriks ketetanggaan:")

    add_bullet(doc, "Memetakan relasi fisik operasional penugasan DPJP dan alur rujukan faskes. Pada dataset portofolio 300 klaim, saluran ini memetakan 10.386 edges.", "1. Saluran Topologi Fisik (A_top): ")
    add_bullet(doc, "Menghubungkan entitas berdasarkan kemiripan kosinus vektor atribut klinis dan biaya (LOS, biaya INA-CBG, usia, kuantitas obat) dengan ambang batas theta_feat >= 0.50 (menghasilkan 15.202 edges). Saluran ini mendeteksi klaster klaim yang identik secara implisit meskipun diajukan pada berkas berbeda.", "2. Saluran Kemiripan Fitur (A_feat): ")
    add_bullet(doc, "Memproyeksikan relasi klinis komposit Dokter -> Diagnosis -> Prosedur -> Faskes berbobot PathSim ternormalisasi: s(u,v) = (2 * |p_u->v|) / (|p_u->u| + |p_v->v|), menghasilkan 7.880 edges. Saluran ini menyingkap ketidakwajaran kompetensi medis dan anomali kode penagihan.", "3. Saluran Semantik Metapath (A_sem): ")

    add_heading_3(doc, "4.4.2 Dual-Branch Graph Convolutional Network & Attention Fusion")
    add_body(doc, "Untuk setiap saluran k in {top, feat, sem}, representasi simpul diproses melalui arsitektur Dual-Branch GCN:")
    add_body(doc, "• Cabang Privat per Saluran (menangkap dinamika spesifik kanal):")
    add_body(doc, "   H^(k) = sigma( D_tilde_(k)^(-1/2) * A_tilde^(k) * D_tilde_(k)^(-1/2) * X * W^(k) )")
    add_body(doc, "• Cabang Parameter-Shared (menangkap invarian struktural lintas-kanal):")
    add_body(doc, "   H^(shared) = (1/3) * sum_k [ sigma( D_tilde_(k)^(-1/2) * A_tilde^(k) * D_tilde_(k)^(-1/2) * X * W^(shared) ) ]")
    add_body(doc, "Kedua cabang digabungkan dan diproses melalui lapisan Multi-Channel Attention Fusion dengan vektor atensi q:")
    add_body(doc, "   alpha_k = exp( q^T * tanh( W_att * H^(k) ) ) / sum_j [ exp( q^T * tanh( W_att * H^(j) ) ) ]")
    add_body(doc, "Berdasarkan kalibrasi empiris, bobot atensi optimal model adalah W_feat = 0.38, W_sem = 0.41, dan W_top = -0.12. Nilai negatif pada W_top membuktikan fenomena penting: saluran topologi fisik sering sengaja direkayasa oleh sindikat, sehingga model secara cerdas memberikan penalti pada relasi topologi normal palsu dan memprioritaskan saluran fitur dan semantik.")

    add_heading_3(doc, "4.4.3 Penyingkapan Kamuflase Topologis via XAI")
    add_body(doc, "Kamuflase topologi terdeteksi secara formal ketika nilai atribusi SHAP (phi) memenuhi kondisi:")
    add_body(doc, "   Camouflage Signature <=> (Risk Score >= 0.80) AND (phi_top < 0) AND (phi_feat > 0.30) AND (phi_sem > 0.35)")
    add_body(doc, "Untuk mengatasi ketimpangan kelas ekstrem (class imbalance) di mana kasus fraud hanya mencakup sebagian kecil populasi, pelatihan model dioptimalkan menggunakan fungsi Focal Loss (alpha = 0.75, gamma = 2.0).")

    add_heading_2(doc, "4.5 Modul 4: Multimodal Late Fusion & Triase Risiko Dinamis")
    add_body(doc, "Aegis-JKN menggabungkan skor probabilitas graf (p_graph) dengan analisis teks resume medis naratif dan keluhan interaksi sosial pasien (f_text) yang diekstraksi via modul NLP klinis lokal / simulasi OASIS. Fusi multimodal dieksekusi melalui formulasi Late Fusion:")

    add_callout(doc, "FORMULA MULTIMODAL LATE FUSION", "Integrasi Probabilitas Graf dan Sinyal Narasi Klinis",
                "« p_fused = p_graph + 0.10 × f_text × (1 - p_graph) »\nDi mana f_text mewakili indeks diskrepansi narasi klinis (rentang -1.0 hingga +1.0). Formula ini menjamin bahwa korelasi graf tetap menjadi sinyal utama, sementara bukti naratif bertindak sebagai penguat probabilitas diskrepansi.")

    add_body(doc, "Berdasarkan nilai p_fused, sistem membagi berkas klaim ke dalam Dynamic Prioritization Queue tiga warna:")
    add_bullet(doc, "Skor < 0.35. Bebas anomali mayor, berkas diarahkan ke alur verifikasi otomatis atau fast-track sampling 5%.", "• Antrean Hijau (Low Risk / Auto-Clear): ")
    add_bullet(doc, "Skor 0.35 s/d 0.70. Berkas memiliki anomali administratif atau ketidaksesuaian ringan, membutuhkan telaah verifikator standar (waktu telaah ~2 menit).", "• Antrean Kuning (Medium Risk / Audit Review): ")
    add_bullet(doc, "Skor > 0.70. Terindikasi kuat upcoding berat, phantom billing, atau bagian dari sindikat kolusi multi-faskes. Berkas diprioritaskan di posisi teratas dashboard dengan tanda bahaya merah.", "• Antrean Merah (High Risk / Escalate): ")

    add_heading_2(doc, "4.6 Modul 5: Explainability Layer & Dekomposisi Atribusi SHAP")
    add_body(doc, "Lapisan Explainable AI (XAI) bertugas mendekomposisi skor risiko menjadi bukti nyata yang dapat diverifikasi manusia dalam hitungan detik. Modul ini menyajikan:")
    add_bullet(doc, "Grafik kontribusi nilai SHAP yang menunjukkan apakah anomali didorong oleh deviasi biaya (A_feat), ketidaksesuaian diagnosis-prosedur (A_sem), atau relasi rujukan mencurigakan.", "1. Waterfall Dekomposisi Saluran: ")
    add_bullet(doc, "Tabel perbandingan berdampingan yang menyorot inkonsistensi klinis (misal: kode klaim tindakan PCI kateterisasi jantung vs tidak adanya rekam pemberian obat antiplatelet atau enzim Troponin).", "2. Matriks Diskrepansi Klinis: ")
    add_bullet(doc, "Subgraf interaktif yang menampilkan lingkaran kolusi antardokter dan faskes yang terlibat dalam pola klaim berulang.", "3. Visualisasi Subgraf Sindikat: ")

    add_heading_2(doc, "4.7 Modul 6: Interactive Verifier Decision Support Interface (Next.js 16)")
    add_body(doc, "Antarmuka pengguna (Frontend) dibangun di atas arsitektur modern Next.js 16.1.1 (App Router), React 19, Tailwind CSS v4 (oklch color space), Radix UI, dan Recharts. Fitur utama antarmuka (terletak di src/components/mhgsl/) meliputi:")
    add_bullet(doc, "Visualisasi graf dinamis berbasis SVG yang memungkinkan verifikator berpindah layer antara Topologi, Fitur, dan Semantik secara interaktif.", "• multi-channel-graph.tsx: ")
    add_bullet(doc, "Modal profil audit mendalam yang menyajikan riwayat klaim faskes, matriks bukti diskrepansi, dan visualisasi waterfall atribusi SHAP.", "• fraud-drilldown-modal.tsx: ")
    add_bullet(doc, "Visualisasi klaster bipartite faskes-dokter untuk mengidentifikasi konsentrasi rujukan siklikal sindikat penagihan.", "• fraud-ring.tsx: ")
    add_bullet(doc, "Formulir interaktif untuk pengunggahan batch berkas klaim (CSV/JSON) dengan kalkulasi skor risiko instan.", "• data-uploader.tsx: ")

    doc.add_page_break()

    # ==========================================
    # BAB V: TATA KELOLA DATA, KEAMANAN, DAN PRIVASI
    # ==========================================
    add_heading_1(doc, "BAB V: TATA KELOLA DATA, KEAMANAN, DAN PRIVASI")

    add_heading_2(doc, "5.1 Kepatuhan Terhadap UU PDP No. 27/2022 & UU Kesehatan No. 17/2023")
    add_body(doc, "Data rekam medis dan riwayat penagihan klaim pasien diklasifikasikan secara tegas sebagai Data Pribadi Spesifik berdasarkan Pasal 4 ayat (3) Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP). Pelanggaran terhadap kerahasiaan data medis membawa konsekuensi sanksi pidana dan denda administratif berat. Tabel 5.1 merangkum kepatuhan platform Aegis-JKN terhadap enam prinsip utama UU PDP.")

    t51_headers = ["Prinsip UU PDP (Pasal 16)", "Implementasi Konkret pada Platform Aegis-JKN", "Instrumen Verifikasi Teknis"]
    t51_data = [
        ["Tujuan Terbatas & Spesifik", "Pemrosesan data terbatas murni untuk audit anomali klaim dan deteksi kecurangan DJS Kesehatan; dilarang untuk komersialisasi pihak ketiga.", "Data Processing Agreement & Service Boundary Locks"],
        ["Minimisasi Data (Data Minimization)", "Hanya menyerap variabel medis dan biaya yang esensial untuk penilaian anomali (10 fitur input bersih); atribut PII sensitif dihapus seketika.", "Ingestion Pipeline Schema Whitelist & PII Stripper"],
        ["Akurasi & Integritas", "Penyelarasan kode diagnosis dan prosedur mengacu pada standar resmi Kemenkes (ICD-10, ICD-9-CM, SATUSEHAT HL7 FHIR R4).", "FHIR Syntactic Validator & Checksum Verification"],
        ["Keamanan Pemrosesan", "Enkripsi simetris end-to-end (AES-256) pada data diam (at-rest) dan TLS 1.3 pada data transit; isolasi jaringan private on-premise cloud.", "Penetration Testing & ISO/IEC 27001 Security Controls"],
        ["Pembatasan Penyimpanan", "Data de-identifikasi transaksi mentah hanya disimpan selama masa retensi audit aktif (5 tahun sesuai regulasi rekam medis).", "Automated Retention Archiving & Crypto-Shredding"],
        ["Akuntabilitas & Transparansi", "Seluruh riwayat skoring, perubahan rekomendasi, dan tindakan override verifikator dicatat dalam log audit kekal (immutable audit trail).", "Append-Only Cryptographic Audit Log (SHA-256 Hash Chaining)"]
    ]
    add_table_data(doc, t51_headers, t51_data, [80, 190, 127])

    add_heading_2(doc, "5.2 Strategi De-identifikasi, Salted Pseudonymization, & Hashing")
    add_body(doc, "Aegis-JKN mengadopsi standar de-identifikasi HIPAA Safe Harbor yang diselaraskan dengan regulasi nasional. Delapan belas elemen pengenal langsung (nama pasien, NIK, alamat presisi, nomor telepon, nomor kartu BPJS) dieliminasi sebelum persistensi data. Nomor identitas unik (ID Pasien, ID Dokter, ID Faskes) dienkripsi menggunakan salted SHA-256 dengan garam dinamis (dynamic cryptographic salt) yang disimpan secara terisolasi pada Hardware Security Module (HSM) BPJS Kesehatan. Dengan mekanisme ini, proses re-identifikasi hanya dapat dilakukan oleh otoritas resmi BPJS jika ditemukan indikasi kecurangan yang memerlukan tindakan penegakan hukum.")

    add_heading_2(doc, "5.3 Protokol Anti-Data Leakage v2.1 & Group Cross-Validation")
    add_body(doc, "Salah satu kelemahan fatal pada purwarupa AI kesehatan generasi awal adalah kebocoran data (data leakage) yang menghasilkan akurasi semu. Pada Aegis-JKN Dataset v2.1, diterapkan Protokol Anti-Leakage ketat:")
    add_bullet(doc, "Delapan kolom analitik hasil audit (skor_fraud, risiko, status, sinyal_shap, kontribusi_saluran, modus, sindikat, alasan) dieksklusi secara absolut dari vektor fitur masukan model training.", "1. Eliminasi Score Leakage: ")
    add_bullet(doc, "ID entitas (pasien_id, dokter_id, faskes_id) diisolasi hanya untuk konstruksi edge graf dan tidak dijadikan fitur prediktif langsung pada model tabular.", "2. Eliminasi Entity Leakage: ")
    add_bullet(doc, "Validasi model menggunakan skema GroupKFold (5-split berbasis pasien_id) dan Leave-One-Group-Out (LOGO berbasis faskes_id) guna menjamin model mampu mendeteksi anomali pada faskes dan pasien baru yang belum pernah dilihat sebelumnya.", "3. Evaluasi Kelompok Ketat: ")

    add_heading_2(doc, "5.4 Arsitektur Penyimpanan & Perimeter Private Cloud BPJS Kesehatan")
    add_body(doc, "Seluruh infrastruktur komputasi Aegis-JKN didesain beroperasi secara penuh di dalam perimeter tertutup (private on-premise cloud) data center BPJS Kesehatan. Sistem menolak tegas pengiriman payload data klaim ke penyedia API LLM publik komersial pihak ketiga (seperti OpenAI atau Anthropic public API) guna mencegah risiko kebocoran data kedaulatan kesehatan nasional. Seluruh proses inferensi graf dan NLP klinis dieksekusi secara lokal menggunakan framework open-source teruji (PyTorch Geometric, HuggingFace transformers on-premise, vLLM / Ollama).")

    add_heading_2(doc, "5.5 Manajemen Akses (RBAC) & Immutable Audit Trail")
    add_body(doc, "Akses terhadap platform dikendalikan secara ketat melalui Role-Based Access Control (RBAC) dengan pemisahan peran: (1) Verifikator Cabang (akses telaah klaim dan input keputusan); (2) Tim Investigasi Kecurangan / PK-JKN (akses investigasi sindikat dan graf lintas-wilayah); (3) Administrator TI (pemeliharaan sistem tanpa akses melihat rekam medis riil). Seluruh interaksi dicatat dalam append-only audit trail yang dilengkapi stempel waktu kriptografis.")

    doc.add_page_break()

    # ==========================================
    # BAB VI: KERANGKA HUMAN-IN-THE-LOOP & HUMAN AUTONOMY
    # ==========================================
    add_heading_1(doc, "BAB VI: KERANGKA HUMAN-IN-THE-LOOP & HUMAN AUTONOMY")

    add_heading_2(doc, "6.1 Filosofi Human-Centered AI dalam Pengawasan Klaim JKN")
    add_body(doc, "Penerapan Kecerdasan Buatan dalam domain pelayanan kesehatan menuntut kepatuhan etika tingkat tinggi. Aegis-JKN menganut filosofi Human-Centered AI yang berpegang pada prinsip bahwa teknologi dirancang untuk memperkuat kapasitas kognitif manusia (cognitive augmentation), bukan menggantikan kebijaksanaan dan pertimbangan klinis verifikator. Verifikasi klaim bukan sekadar kalkulasi matematis, melainkan penilaian yang melibatkan etika kedokteran, konteks kedaruratan medis, dan keadilan sosial.")

    add_heading_2(doc, "6.2 Prinsip Utama: Fail-Safe AI & Hak Otonomi Verifikator")
    add_callout(doc, "PRINSIP FAIL-SAFE AI & HUMAN AUTONOMY", "Larangan Keputusan Sepihak oleh Kecerdasan Buatan",
                "« AI diperbolehkan membuat kekeliruan dalam memberikan indikasi atau rekomendasi awal; yang dilarang keras adalah sistem AI yang mampu mengeksekusi vonis penolakan klaim, pemotongan biaya, atau penjatuhan sanksi hukum secara sepihak tanpa telaah dan persetujuan verifikator manusia (Anti-Automated Adverse Decision). »")

    add_body(doc, "Sesuai pedoman etika AI WHO (2021) dan regulasi sengketa klaim BPJS Kesehatan, setiap fasilitas kesehatan memiliki hak hukum untuk mendapatkan penjelasan rasional atas setiap penundaan atau penolakan klaim (Right to Explanation & Due Process). Oleh karena itu, Aegis-JKN memposisikan diri secara tegas sebagai pemberi rekomendasi (advisory engine), di mana 100% keputusan final berada di tangan verifikator manusia.")

    add_heading_2(doc, "6.3 Matriks Pembagian Peran Kerja AI vs Verifikator Manusia")
    add_body(doc, "Tabel 6.1 merinci pembagian tanggung jawab fungsional antara sistem Aegis-JKN dan verifikator manusia di lingkungan BPJS Kesehatan.")

    t61_headers = ["Dimensi Tugas", "Fungsi Sistem Aegis-JKN (AI / Engine)", "Wewenang Verifikator Manusia (BPJS)"]
    t61_data = [
        ["Pemrosesan Berkas Skala Besar", "Menyaring jutaan berkas klaim harian secara paralel; memilah klaim normal ke jalur cepat (<50 ms).", "Memvalidasi hasil penyaringan dan memfokuskan energi telaah pada berkas antrean merah."],
        ["Deteksi Sindikat & Anomali", "Menganalisis keterhubungan multi-hop (topologi, fitur, semantik) dan membongkar penyamaran rujukan.", "Menilai rasionalitas medis dan meninjau konteks khusus faskes/pasien."],
        ["Penyusunan Bukti (Evidence)", "Mendekomposisi atribusi SHAP per-kanal dan mengekstrak matriks diskrepansi kode vs fakta.", "Menelaah keabsahan bukti dokumen penunjang klinis asli."],
        ["Keputusan Penolakan / Dispute", "Dilarang memvonis. Sistem hanya memberikan rekomendasi: Normal / Review / Escalate.", "Memiliki hak tunggal mengeksekusi keputusan: Konfirmasi, Dismiss (Override), atau Eskalasi TKMKB."],
        ["Umpan Balik Model (Active Learning)", "Mencatat log keputusan manusia beserta alasan overrides untuk kalibrasi ulang model.", "Memberikan label koreksi klinis yang menjadi bahan retraining model graf."]
    ]
    add_table_data(doc, t61_headers, t61_data, [90, 150, 157])

    add_heading_2(doc, "6.4 Alur Interaksi Verifikator & Safe-Mode Fallback Protocol")
    add_body(doc, "Saat menelaah berkas pada antrean merah atau kuning, verifikator disajikan antarmuka split-screen yang menampilkan ringkasan klaim berdampingan dengan matriks diskrepansi dan visualisasi subgraf sindikat. Verifikator memiliki tiga opsi tindakan:")
    add_bullet(doc, "Verifikator menyetujui temuan anomali sistem dan meneruskan berkas ke proses klarifikasi faskes atau penyesuaian kode tarif INA-CBG.", "1. Konfirmasi Anomali (Confirm): ")
    add_bullet(doc, "Verifikator menolak rekomendasi AI karena terdapat justifikasi klinis yang sah dalam rekam medis. Verifikator wajib memilih alasan override (misal: komplikasi tak terduga saat operasi).", "2. Batalkan Flag (Override / Dismiss): ")
    add_bullet(doc, "Jika terindikasi keterlibatan sindikat kolusi multi-faskes, berkas dieskalasi ke Tim Pencegahan Kecurangan (PK-JKN) dan Tim Kendali Mutu dan Kendali Biaya (TKMKB).", "3. Eskalasi Khusus (Escalate): ")

    add_body(doc, "Sebagai mekanisme pengaman kegagalan (fail-safe) tingkat korporat, Aegis-JKN dilengkapi protokol darurat Safe-Mode Fallback Protocol: Jika dalam kurun waktu 24 jam tingkat penolakan rekomendasi (override rate) oleh verifikator melampaui ambang batas 30%, sistem secara otomatis membekukan penyajian skor AI dan kembali ke mode verifikasi standar berbasis aturan deterministik. Kondisi ini otomatis memicu peringatan darurat ke tim teknis untuk melakukan investigasi data drift atau perubahan pedoman klinis baru.")

    add_heading_2(doc, "6.5 Strategi Komprehensif Mitigasi Alert Fatigue & Halusinasi AI")
    add_body(doc, "Fenomena alert fatigue (kejenuhan kognitif verifikator akibat sistem terlalu sering membunyikan alarm palsu) dimitigasi secara sistemik melalui:")
    add_bullet(doc, "Antrean merah hanya dipicu jika skor risiko > 0.70 dan delta tarif INA-CBG signifikan, sehingga verifikator tidak dibebani oleh peringatan bernilai rendah.", "1. Ambang Batas Selektif: ")
    add_bullet(doc, "Alih-alih menyajikan ribuan klaim satu per satu, sistem mengelompokkan klaim berdasarkan klaster sindikat (bipartite cluster), memungkinkan verifikator menyelesaikan audit atas puluhan klaim terkait dalam satu kali penelaahan.", "2. Agregasi Klaster Sindikat: ")
    add_bullet(doc, "Menolak penggunaan model generatif bebas halusinasi untuk penulisan kesimpulan medis; sistem hanya menyajikan matriks ekstraktif berbasis kode baku ICD-10/ICD-9 dan fakta numerik rekam medis.", "3. Ekstraksi Fakta Deterministik Tanpa Halusinasi: ")

    doc.add_page_break()
    print("Bab 4 to 6 built successfully.")
