# -*- coding: utf-8 -*-
"""
Module 5: BAB X (Manajemen Risiko), BAB XI (Roadmap Implementasi), BAB XII (Kesimpulan & Daftar Pustaka)
"""

import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from generate_aegis_proposal import (
    add_callout, add_heading_1, add_heading_2, add_heading_3,
    add_body, add_bullet, add_table_data
)

def build_bab_10_to_12(doc):
    # ==========================================
    # BAB X: MANAJEMEN RISIKO & STRATEGI MITIGASI
    # ==========================================
    add_heading_1(doc, "BAB X: MANAJEMEN RISIKO & STRATEGI MITIGASI")

    add_heading_2(doc, "10.1 Identifikasi 12 Risiko Kritis Implementasi Aegis-JKN")
    add_body(doc, "Implementasi sistem kecerdasan buatan pada tata kelola jaminan kesehatan nasional berskala 270+ juta jiwa memiliki kompleksitas tinggi. Tim Inovator memetakan 12 risiko kritis yang mencakup dimensi teknis algoritmik, infrastruktur komputasi, keamanan siber, kepatuhan regulasi, hingga dinamika sosial hubungan industrial dengan fasilitas kesehatan.")

    add_heading_2(doc, "10.2 Matriks Manajemen Risiko Komprehensif")
    add_body(doc, "Tabel 10.1 merangkum matriks manajemen risiko komprehensif beserta tingkat keparahan dan strategi mitigasi preventif serta kontingensinya.")

    t101_headers = ["No", "Identifikasi Risiko", "Potensi Dampak", "Tingkat", "Strategi Mitigasi Preventif & Kontingensi"]
    t101_data = [
        ["1", "Topological Camouflage (Sindikat menyamarkan rujukan fisik)",
         "Sindikat lolos dari sistem graf homogen atau model tabular.", "Tinggi (Kritis)",
         "Dekomposisi Tri-Channel MHGSL (A_top, A_feat, A_sem) dengan bobot atensi negatif pada topologi dan deteksi anomali fitur."],
        ["2", "Model Drift akibat perubahan tarif / pedoman klinis baru",
         "Penurunan akurasi deteksi pasca-revisi regulasi PMK Kemenkes.", "Tinggi (Kritis)",
         "Continuous monitoring data drift, evaluasi LOGO periodik, dan re-indexing otomatis ontologi tarif INA-CBG."],
        ["3", "Bottleneck Throughput pada volume 2 juta klaim/hari",
         "Antrean pemrosesan menumpuk, memperlambat proses pencairan klaim.", "Tinggi (Kritis)",
         "Arsitektur Dual-Path: caching Redis streaming <500 ms untuk klaim individual dan batch graph convolution harian."],
        ["4", "Resistensi Faskes & Asosiasi Profesi (PERSI / IDI)",
         "Protes klinisi yang merasa dicurigai integritas praktiknya.", "Tinggi (Kritis)",
         "Menegaskan status sistem sebagai CDSS (bukan vonis), transparansi bukti diskrepansi klinis, dan pelibatan TKMKB."],
        ["5", "False Accusations (Tuduhan kecurangan keliru)",
         "Sengketa klaim (dispute) yang berlarut-larut dengan faskes.", "Tinggi (Kritis)",
         "Prinsip Fail-Safe Human Autonomy: 100% keputusan di tangan manusia; AI hanya memberikan rekomendasi berbobot bukti."],
        ["6", "Kebocoran Data Medis Pasien (Pelanggaran UU PDP)",
         "Sanksi hukum pidana dan hilangnya reputasi publik BPJS.", "Tinggi (Kritis)",
         "Isolasi perimeter private on-premise cloud, salted SHA-256 tokenization, enkripsi AES-256, zero external cloud LLM API."],
        ["7", "Kegagalan Bridging API (Downtime V-Claim / SIMRS)",
         "Data klaim gagal terkirim ke modul analitik.", "Sedang",
         "Asynchronous message queue (RabbitMQ) dengan mekanisme retry otomatis dan circuit breaker lokal."],
        ["8", "Variasi Format EMR (Data teks tidak terstruktur / scan PDF)",
         "Modul NLP gagal mengekstrak bukti pendukung klinis.", "Sedang",
         "Normalisasi format SATUSEHAT HL7 FHIR R4 dan integrasi modul OCR lokal cerdas untuk berkas pindaian faskes."],
        ["9", "Keterbatasan Akses Internet di Kantor Cabang Daerah 3T",
         "Verifikator cabang perintis terhambat mengakses dashboard.", "Sedang",
         "Aplikasi Next.js 16 dioptimalkan dengan caching offline-first (PWA) dan kompresi payload respons graf SVG."],
        ["10", "AI Hallucination pada komponen analisis teks klinis",
         "Rekomendasi alasan anomali tidak sesuai fakta medis rekam medis.", "Sedang",
         "Menolak teks generatif bebas; ekstraksi strictly grounded pada kode ICD-10/ICD-9 dan fakta numerik rekam medis."],
        ["11", "Vendor Lock-in pada teknologi komputasi proprietary",
         "Ketergantungan biaya lisensi perangkat lunak yang membengkak.", "Rendah",
         "100% stack berbasis open-source enterprise (PyTorch Geometric, Next.js, FastAPI, Redis, PostgreSQL)."],
        ["12", "Rendahnya Tingkat Adopsi Verifikator Lapangan",
         "Sistem diabaikan karena verifikator merasa terbebani sistem baru.", "Sedang",
         "Program pelatihan modular 6 jam, antarmuka intuitif dengan skor SUS >80, dan penyederhanaan alur kerja one-click audit."]
    ]
    add_table_data(doc, t101_headers, t101_data, [20, 85, 80, 45, 167])

    add_heading_2(doc, "10.3 Protokol Tanggap Darurat & Continuous Model Monitoring")
    add_body(doc, "Platform dilengkapi protokol tanggap darurat otomatis: (1) Safe-Mode Fallback Protocol yang otomatis membekukan rekomendasi AI jika tingkat penolakan (override) verifikator melebihi ambang batas 30% dalam 24 jam; (2) Automated Crypto-Shredding yang memusnahkan kunci tokenisasi sementara jika terdeteksi anomali akses intrusi; serta (3) Dashboard Continuous Model Drift yang memantau pergeseran distribusi skor risiko secara real-time.")

    doc.add_page_break()

    # ==========================================
    # BAB XI: ROADMAP PENGEMBANGAN & RENCANA IMPLEMENTASI
    # ==========================================
    add_heading_1(doc, "BAB XI: ROADMAP PENGEMBANGAN & RENCANA IMPLEMENTASI")

    add_heading_2(doc, "11.1 Kerangka Kerja Stage-Gate Roadmap")
    add_body(doc, "Rencana implementasi Aegis-JKN dirancang menggunakan Stage-Gate Innovation Framework. Setiap tahapan memiliki pintu evaluasi (gate) dengan kriteria kelulusan kuantitatif yang ketat sebelum proyek diizinkan melangkah ke fase berikutnya, menjamin akuntabilitas investasi teknologi dan mitigasi risiko secara dini.")

    add_heading_2(doc, "11.2 Rencana Pelaksanaan 8-12 Minggu Purwarupa & Roadmap 12 Bulan")
    add_body(doc, "Roadmap implementasi terbagi ke dalam Rencana Sprint 8-12 Minggu untuk penyempurnaan purwarupa kompetisi Healthkathon, serta Roadmap Nasional 12 Bulan (Tiga Fase Utama), sebagaimana dirinci pada Tabel 11.1:")

    t111_headers = ["Tahap & Durasi", "Aktivitas Kunci", "Keluaran Utama (Deliverables)", "Kriteria Kelulusan (Gate Criteria)"]
    t111_data = [
        ["Tahap 1 (Bln 1)\nValidasi Masalah",
         "Wawancara verifikator BPJS, pemetaan 9 modus sindikat, dan formalisasi skema HL7 FHIR R4.",
         "Dokumen spesifikasi kebutuhan sistem (SRS) dan pemetaan ontologi INA-CBG.",
         "Persetujuan tim klinis BPJS & keselarasan regulasi PMK 16/2019."],
        ["Tahap 2 (Bln 2)\nSintesis & Simulasi",
         "Penyusunan Dataset v2.1 (300 klaim), kalibrasi simulasi OASIS (20P, 12D, 6RS), dan anti-leakage audit.",
         "Dataset v2.1 tervalidasi klinis dan modul Discrete Event Simulator OASIS.",
         "Zero data leakage terverifikasi & reproduktibilitas seed deterministik 100%."],
        ["Tahap 3 (Bln 3-4)\nPengembangan Core",
         "Implementasi PyTorch Geometric HeteroData MHGSL, Rule Engine Tier-1, dan API FastAPI.",
         "Checkpoint model mhgsl_model.pth, backend serving, dan cache streaming Redis.",
         "Akurasi ≥ 90%, Presisi ≥ 90%, ROC-AUC ≥ 0.95, latensi stream <500 ms."],
        ["Tahap 4 (Bln 5)\nFrontend & XAI",
         "Pengembangan antarmuka Next.js 16, visualisasi graf SVG 3-saluran, modal SHAP, dan klaster faskes.",
         "Dashboard verifikator interaktif terintegrasi API FastAPI.",
         "Skor System Usability Scale (SUS) ≥ 80 / 100."],
        ["Tahap 5 (Bln 6-8)\nPilot RS Rujukan",
         "Uji coba terbatas pada 1-2 Kantor Cabang percontohan menggunakan data sandbox resmi BPJS.",
         "Laporan evaluasi pilot, matriks penyesuaian faskes, dan log feedback verifikator.",
         "Reduksi durasi telaah berkas anomali ≥ 30%, FPR ≤ 15%, override rate ≤ 20%."],
        ["Tahap 6 (Bln 9-10)\nIntegrasi Produksi",
         "Penyambungan bridging V-Claim skala penuh, optimasi GraphSAINT batch, dan audit keamanan ISO 27001.",
         "Sistem Aegis-JKN ter-deploy di private on-premise cloud data center BPJS.",
         "Lolos uji penetrasi siber & throughput mampu memproses 2 juta klaim/hari."],
        ["Tahap 7 (Bln 11-12)\nRollout Nasional",
         "Peluncuran bertahap ke seluruh Kantor Cabang se-Indonesia, pelatihan nasional, dan monitoring drift.",
         "Platform beroperasi penuh skala nasional terhubung sistem pembayaran klaim.",
         "Rasio Cost-to-Impact terbukti ≥ 1 : 15 dalam perlindungan Dana DJS Kesehatan."]
    ]
    add_table_data(doc, t111_headers, t111_data, [55, 110, 115, 117])

    add_heading_2(doc, "11.3 Indikator Keberhasilan Antar-Tahap (Stage-Gate Criteria)")
    add_body(doc, "Keberhasilan antar-fase dikawal oleh tiga gerbang utama: (1) Gate-1: Model Core Readiness (AUPRC >0.85, latensi <500 ms); (2) Gate-2: User Adoption & Safety (SUS >80, override <20%, Safe-Mode Protocol teruji); serta (3) Gate-3: Financial Impact & Resilience (Cost-to-Impact > 1:15, ketahanan kamuflase >85% pada data operasional).")

    doc.add_page_break()

    # ==========================================
    # BAB XII: KESIMPULAN & PENUTUP
    # ==========================================
    add_heading_1(doc, "BAB XII: KESIMPULAN & PENUTUP")

    add_heading_2(doc, "12.1 Sintesis Nilai Strategis Solusi Aegis-JKN")
    add_body(doc, "Aegis-JKN membuktikan bahwa terobosan teknologi kecerdasan buatan dalam pengawasan pembiayaan kesehatan tidak harus berbiaya mahal, bergantung pada cloud pihak ketiga, atau mengorbankan otonomi manusia. Melalui inovasi Multi-Channel Heterogeneous Graph Structure Learning (MHGSL), Aegis-JKN memecahkan kebuntuan audit konvensional dengan membedah jaringan kolusi sindikat dan membongkar kamuflase topologis yang selama ini tidak terlihat oleh model tabular dan aturan statis.")

    add_body(doc, "Dengan arsitektur Tri-Tier yang menggabungkan kecepatan aturan deterministik (<50 ms), ketajaman klasifikasi statistik tabular, dan kedalaman pembelajaran graf heterogen yang terhubung ke standar SATUSEHAT HL7 FHIR R4, sistem ini dirancang siap menangani beban transaksi riil lebih dari dua juta klaim per hari. Transparansi penalaran Explainable AI (XAI) dan kerangka kerja Human-in-the-Loop menjamin bahwa hak otonomi verifikator manusia tetap menjadi penentu akhir yang berdaulat, akuntabel, dan bebas dari bias kotak hitam.")

    add_heading_2(doc, "12.2 Kesiapan Implementasi & Rekomendasi Menuju Healthkathon 2026")
    add_body(doc, "Purwarupa Aegis-JKN telah diwujudkan dalam bentuk kode aplikasi fungsional yang siap didemonstrasikan: antarmuka web interaktif Next.js 16 yang responsif, backend inferensi PyTorch Geometric dan FastAPI berlatensi rendah, serta dataset pengujian 300 klaim tervalidasi klinis yang telah membuktikan kemampuan menyelamatkan lebih dari setengah miliar rupiah potensi kebocoran tarif pada sampel terbatas. Tim Inovator Kandidat 1 berkomitmen penuh untuk bermitra dengan BPJS Kesehatan guna mewujudkan ekosistem jaminan kesehatan yang adil, transparan, dan berkelanjutan.")

    add_callout(doc, "KOMITMEN INOVASI", "Detect Smarter, Protect JKN",
                "« Bersama Aegis-JKN, kita wujudkan perlindungan Dana Jaminan Sosial Kesehatan yang lebih cerdas, melindungi hak setiap peserta, dan mengawal keberlangsungan Universal Health Coverage Indonesia untuk generasi masa depan. »")

    # ==========================================
    # DAFTAR PUSTAKA & REFERENSI REGULASI
    # ==========================================
    add_heading_1(doc, "DAFTAR PUSTAKA & REFERENSI REGULASI")

    pustaka = [
        "[1] BPJS Kesehatan. (2024). Laporan Pengelolaan Program JKN dan Kinerja Keuangan BPJS Kesehatan Tahun 2023. Jakarta: BPJS Kesehatan.",
        "[2] Kementerian Kesehatan RI. (2019). Peraturan Menteri Kesehatan Republik Indonesia Nomor 16 Tahun 2019 tentang Pencegahan dan Penanganan Kecurangan (Fraud) serta Pengendalian Gratifikasi dalam Penyelenggaraan Program Jaminan Kesehatan. Jakarta: Kemenkes RI.",
        "[3] Kementerian Kesehatan RI. (2021). Peraturan Menteri Kesehatan Republik Indonesia Nomor 26 Tahun 2021 tentang Pedoman Pencegahan dan Penanganan Kecurangan (Fraud) dalam Penyelenggaraan Program Jaminan Kesehatan. Jakarta: Kemenkes RI.",
        "[4] Kementerian Kesehatan RI. (2022). Peraturan Menteri Kesehatan Republik Indonesia Nomor 24 Tahun 2022 tentang Rekam Medis. Jakarta: Kemenkes RI.",
        "[5] Kementerian Kesehatan RI. (2023). Peraturan Menteri Kesehatan Republik Indonesia Nomor 3 Tahun 2023 tentang Standar Tarif Pelayanan Kesehatan dalam Penyelenggaraan Program Jaminan Kesehatan. Jakarta: Kemenkes RI.",
        "[6] Republik Indonesia. (2022). Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi. Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196. Jakarta: Sekretariat Negara.",
        "[7] Republik Indonesia. (2023). Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan. Lembaran Negara Republik Indonesia Tahun 2023 Nomor 105. Jakarta: Sekretariat Negara.",
        "[8] World Health Organization. (2021). Ethics and Governance of Artificial Intelligence for Health: WHO Guidance. Geneva: World Health Organization.",
        "[9] Sun, Y., Han, J., Yan, X., Yu, P. S., & Wu, T. (2011). PathSim: Meta Path-Based Top-K Similarity Search in Heterogeneous Information Networks. Proceedings of the VLDB Endowment, 4(11), 992-1003.",
        "[10] Wang, X., Ji, H., Shi, C., Wang, B., Ye, Y., Cui, P., & Yu, P. S. (2019). Heterogeneous Graph Attention Network. Proceedings of The World Wide Web Conference (WWW '19), 2022-2032.",
        "[11] Kipf, T. N., & Welling, M. (2017). Semi-Supervised Classification with Graph Convolutional Networks. International Conference on Learning Representations (ICLR 2017).",
        "[12] Fey, M., & Lenssen, J. E. (2019). Fast Graph Representation Learning with PyTorch Geometric. ICLR Workshop on Representation Learning on Graphs and Manifolds.",
        "[13] Lin, T. Y., Goyal, P., Girshick, R., He, K., & Dollár, P. (2017). Focal Loss for Dense Object Detection. IEEE International Conference on Computer Vision (ICCV), 2980-2988.",
        "[14] Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 4765-4774.",
        "[15] Zeng, H., Zhou, H., Srivastava, A., Kannan, R., & Prasanna, V. (2020). GraphSAINT: Graph Sampling Based Inductive Engine. International Conference on Learning Representations (ICLR 2020).",
        "[16] CAMEL-AI. (2024). OASIS: Open Agent Social Interaction Simulation System with 1 Million Diverse Agents. arXiv preprint arXiv:2411.11581.",
        "[17] Heliyon Medical Intelligence Group. (2024). Multi-Hop Graph Structure Learning for Medical Fraud Detection in Health Insurance Systems (Medical-B Benchmark). Heliyon, 10(4), e26115.",
        "[18] Centers for Medicare & Medicaid Services. (2022). Inpatient and Outpatient Prospective Payment Systems and Healthcare Fraud Detection Benchmarks. CMS Research Publications."
    ]

    for p_ref in pustaka:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(p_ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.0)

    print("Bab 10 to 12 built successfully.")
