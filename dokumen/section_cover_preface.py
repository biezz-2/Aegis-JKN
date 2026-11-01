# -*- coding: utf-8 -*-
"""
Module 1: Cover, Lembar Pernyataan, Ringkasan Eksekutif, Daftar Isi & Tabel
"""

import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from generate_aegis_proposal import (
    add_callout, add_heading_1, add_heading_2, add_heading_3,
    add_body, add_bullet, add_table_data, set_cell_background,
    set_cell_margins, set_cell_borders
)

def build_cover_and_preface(doc):
    # ==========================================
    # HALAMAN COVER
    # ==========================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(12)
    p_inst.paragraph_format.space_after = Pt(4)
    r1 = p_inst.add_run("PROPOSAL INOVASI TEKNOLOGI KESEHATAN\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(14)
    r1.bold = True
    r1.font.color.rgb = RGBColor(31, 78, 121)

    r2 = p_inst.add_run("BPJS KESEHATAN HEALTHKATHON 2026\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(13)
    r2.bold = True

    r3 = p_inst.add_run("Kategori: Sistem Pengawasan Fasilitas Kesehatan (Pencegahan Upcoding, Unbundling, Phantom Billing, dan Sindikat Kolusi Rujukan)")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(10.5)
    r3.italic = True
    r3.font.color.rgb = RGBColor(80, 90, 100)

    # Line separator
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(8)
    p_line.paragraph_format.space_after = Pt(24)
    r_line = p_line.add_run("_______________________________________________________________________________")
    r_line.font.name = "Times New Roman"
    r_line.font.size = Pt(10)
    r_line.font.color.rgb = RGBColor(31, 78, 121)

    # Judul Utama
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(12)
    r_t = p_title.add_run("AEGIS-JKN: SISTEM FRAUD INTELLIGENCE & CLINICAL DECISION SUPPORT BERBASIS MULTI-HOP GRAPH STRUCTURE LEARNING (MHGSL) DAN MULTIMODAL SIMULATION UNTUK DETEKSI SINDIKAT KECURANGAN DAN ANOMALI KLAIM JKN")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(15)
    r_t.bold = True
    r_t.font.color.rgb = RGBColor(20, 45, 75)

    # Slogan
    p_slogan = doc.add_paragraph()
    p_slogan.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_slogan.paragraph_format.space_before = Pt(0)
    p_slogan.paragraph_format.space_after = Pt(40)
    r_s = p_slogan.add_run("« Detect Smarter. Protect JKN. »")
    r_s.font.name = "Times New Roman"
    r_s.font.size = Pt(12)
    r_s.bold = True
    r_s.italic = True
    r_s.font.color.rgb = RGBColor(31, 78, 121)

    # Pengusul
    p_team = doc.add_paragraph()
    p_team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_team.paragraph_format.space_before = Pt(30)
    p_team.paragraph_format.space_after = Pt(4)
    r_tm0 = p_team.add_run("Diajukan Oleh:\n")
    r_tm0.font.name = "Times New Roman"
    r_tm0.font.size = Pt(11)

    r_tm1 = p_team.add_run("TIM INOVATOR KANDIDAT 1 — AEGIS-JKN\n")
    r_tm1.font.name = "Times New Roman"
    r_tm1.font.size = Pt(12)
    r_tm1.bold = True
    r_tm1.font.color.rgb = RGBColor(31, 78, 121)

    r_tm2 = p_team.add_run("1. Lead Platform & Logic Architecture\n2. Research & Clinical Data Specialist\n3. Business Case & Strategic Impact Specialist\n")
    r_tm2.font.name = "Times New Roman"
    r_tm2.font.size = Pt(10.5)

    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(40)
    p_loc.paragraph_format.space_after = Pt(0)
    r_loc = p_loc.add_run("JAKARTA\n2026")
    r_loc.font.name = "Times New Roman"
    r_loc.font.size = Pt(12)
    r_loc.bold = True

    doc.add_page_break()

    # ==========================================
    # LEMBAR PERNYATAAN ORISINALITAS DAN INTEGRITAS
    # ==========================================
    add_heading_1(doc, "LEMBAR PERNYATAAN ORISINALITAS DAN INTEGRITAS")

    add_body(doc, "Yang bertanda tangan di bawah ini, kami selaku Tim Inovator Kandidat 1 peserta kompetisi BPJS Kesehatan Healthkathon 2026, dengan ini menyatakan bahwa proposal inovasi dengan judul:")

    add_callout(doc, "JUDUL KARYA INOVASI", "AEGIS-JKN: Sistem Fraud Intelligence & Clinical Decision Support Berbasis Multi-Hop Graph Structure Learning (MHGSL) dan Multimodal Simulation untuk Deteksi Sindikat Kecurangan dan Anomali Klaim JKN",
                "« Detect Smarter, Protect JKN — Menjaga Ketahanan Finansial Dana Jaminan Sosial (DJS) Melalui Deteksi Kolusi Multi-Hop dan Transparansi Akuntabilitas Medis. »")

    add_body(doc, "Adalah benar-benar hasil karya orisinal tim kami, belum pernah dipublikasikan secara komersial di tempat lain, dan tidak mengandung unsur plagiarisme atau pelanggaran hak kekayaan intelektual pihak mana pun. Bersama ini kami juga menyatakan komitmen integritas perancangan sistem sebagai berikut:")

    add_bullet(doc, "Seluruh perancangan arsitektur data Aegis-JKN mematuhi Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) dan Undang-Undang Nomor 17 Tahun 2023 tentang Kesehatan. Pengembangan purwarupa (MVP) sepenuhnya menggunakan dataset sintetis tervalidasi klinis dan data terbuka ter-deidentifikasi yang sah secara hukum, tanpa menggunakan data peserta JKN aktual tanpa izin resmi tertulis.", "1. Kepatuhan Regulasi Data Pribadi: ")
    add_bullet(doc, "Kami menolak klaim akurasi mutlak 100% dan tidak menyajikan angka penghematan anggaran yang spekulatif. Seluruh metrik teknis (Akurasi 93.0%, Presisi 94.12%, ROC-AUC 0.9825, AUPRC 0.9142) serta estimasi penyelamatan overcharge tarif INA-CBG sebesar Rp 507,37 Juta dihitung berbasis metodologi empiris portofolio 300 klaim terverifikasi yang dapat direplikasi secara objektif.", "2. Prinsip Anti-Overclaim & Transparansi Sains: ")
    add_bullet(doc, "Sistem dirancang murni sebagai pendukung keputusan klinis (Clinical Decision Support System / CDSS). Kecerdasan Buatan (AI) dilarang keras memiliki kewenangan menjatuhkan sanksi hukum, memvonis fraud secara sepihak, menolak klaim, ataupun memotong tarif secara otomatis (anti-automated adverse decision). Seluruh keputusan final tetap berada di bawah kendali penuh dan tanggung jawab verifikator manusia dan Tim Pencegahan Kecurangan (PK-JKN).", "3. Prinsip Human Autonomy & Fail-Safe AI: ")
    add_bullet(doc, "Pemilihan komponen teknologi (Tri-Tier Pipeline: Rule-Based, Tabular XGBoost, Tri-Channel MHGSL, dan Multi-Agent Simulation OASIS) didasarkan pada kebutuhan fungsional nyata dari throughput 2 juta klaim/hari, bukan demi mengejar kompleksitas komputasi yang berlebihan atau menambah beban operasional yang tidak perlu.", "4. Teknologi Tepat Guna (Right-Sized Hybrid Engineering): ")

    add_body(doc, "Demikian pernyataan ini kami buat dengan penuh rasa tanggung jawab, integritas moral, dan dedikasi demi mendukung keberlanjutan Program Jaminan Kesehatan Nasional (JKN) yang berkeadilan bagi seluruh rakyat Indonesia.")

    # Tanda Tangan
    tbl_ttd = doc.add_table(rows=2, cols=2)
    tbl_ttd.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = tbl_ttd.rows[0].cells[0]
    c1 = tbl_ttd.rows[0].cells[1]
    c2 = tbl_ttd.rows[1].cells[0]
    c3 = tbl_ttd.rows[1].cells[1]

    for cell in [c0, c1, c2, c3]:
        set_cell_background(cell, "FFFFFF")
        set_cell_margins(cell, top=60, bottom=60, left=100, right=100)

    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_p0 = p0.add_run("Mengetahui,\nPerwakilan Tim Teknis & Arsitektur\n\n\n\n\n( Tim Pengusul Kandidat 1 )")
    r_p0.font.name = "Times New Roman"
    r_p0.font.size = Pt(10.5)

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_p1 = p1.add_run("Jakarta, Oktober 2026\nPerwakilan Riset & Strategi Dampak\n\n\n\n\n( Tim Pengusul Kandidat 1 )")
    r_p1.font.name = "Times New Roman"
    r_p1.font.size = Pt(10.5)

    doc.add_page_break()

    # ==========================================
    # RINGKASAN EKSEKUTIF
    # ==========================================
    add_heading_1(doc, "RINGKASAN EKSEKUTIF")

    add_body(doc, "Program Jaminan Kesehatan Nasional (JKN) yang dikelola oleh BPJS Kesehatan merupakan salah satu sistem jaminan kesehatan semesta (Universal Health Coverage) terbesar dan paling kompleks di dunia, mencakup lebih dari 270 juta jiwa kepesertaan aktif dan memproses lebih dari dua juta klaim layanan kesehatan setiap harinya dari fasilitas kesehatan rujukan tingkat lanjutan (FKRTL) di seluruh Indonesia. Namun, pengelolaan skala masif ini dihadapkan pada ketimpangan rasio beban verifikasi yang sangat tajam, di mana hanya sekitar 1.000 verifikator klaim BPJS Kesehatan yang bertugas menelaah jutaan berkas tersebut (rasio beban mencapai 2.000 klaim per verifikator per hari, jauh melampaui kapasitas telaah mendalam manusia sebesar 50–70 berkas per hari). Keterbatasan kognitif dan fenomena kelelahan peringatan (alert fatigue) ini membuka celah asimetri informasi yang dimanfaatkan oleh oknum terorganisir untuk melakukan kecurangan klaim (fraud) terstruktur, khususnya upcoding severity level, phantom billing, unbundling prosedur, hingga sindikat kolusi rujukan dokter-faskes (fraud rings).")

    add_body(doc, "Tantangan paling kritis dalam deteksi kecurangan modern adalah fenomena Kamuflase Topologis (Topological Camouflage). Pelaku kecurangan terorganisir sengaja merekayasa alur rujukan administratif fisik agar tampak patuh regulasi berjenjang (sehingga terlihat normal pada model statistik tabular dan aturan deterministik), namun menyembunyikan anomali klastering biaya, durasi rawat (LOS), dan prosedur tidak lazim secara terselubung. Proposal ini mengusulkan solusi inovatif terpadu: AEGIS-JKN (Detect Smarter, Protect JKN), sebuah platform Fraud Intelligence dan Clinical Decision Support System (CDSS) berbasis arsitektur Multi-Hop Graph Structure Learning (MHGSL) yang dikombinasikan dengan simulasi multi-agen multimodal (OASIS) dalam kerangka kerja Human-in-the-Loop (HITL) yang akuntabel.")

    add_body(doc, "Keunggulan utama Aegis-JKN berakar pada lima pilar strategis:")
    add_bullet(doc, "Memodelkan interaksi layanan medis ke dalam graf heterogen yang didekomposisi ke dalam tiga saluran matriks ketetanggaan: (1) Saluran Topologi Fisik (A_top) untuk relasi penugasan DPJP dan rujukan faskes; (2) Saluran Kemiripan Fitur (A_feat) berbasis cosine similarity vektor atribut klinis-finansial (LOS, biaya INA-CBG, obat) guna mendeteksi anomali identik implisit; serta (3) Saluran Semantik Metapath (A_sem) yang memproyeksikan rantai rujukan klinis via PathSim untuk menyingkap ketidaksesuaian kompetensi dan rekayasa kode penagihan.", "1. Paradigma Deteksi Tri-Channel MHGSL: ")
    add_bullet(doc, "Mengombinasikan Tier-1 Deterministic Rule Engine (<50 ms) untuk menyaring 40-60% klaim normal/pelanggaran eksplisit Permenkes No. 16/2019, Tier-2 Tabular XGBoost untuk anomali statistik per klaim, dan Tier-3 PyTorch Geometric HeteroData GCN untuk ekstraksi sindikat multi-hop, yang disatukan via Late Fusion multimodal dengan narasi resume klinis.", "2. Arsitektur Tri-Tier & Right-Sized Engineering: ")
    add_bullet(doc, "Setiap flag anomali disertai dekomposisi atribusi SHAP per kanal graf (phi_top, phi_feat, phi_sem) serta visualisasi SVG interaktif klaster bipartite faskes-dokter, mengeliminasi sifat kotak hitam (black-box) dan langsung memandu verifikator ke bukti inkonsistensi klinis.", "3. Transparansi Penalaran (Explainable AI / XAI): ")
    add_bullet(doc, "Menerapkan prinsip anti-automated adverse decision di mana AI tidak memiliki hak veto penolakan klaim. Dilengkapi protokol darurat Safe-Mode Fallback yang otomatis membekukan saran AI jika tingkat penolakan (override) oleh verifikator melampaui 30%.", "4. Fail-Safe Human Autonomy & Active Learning: ")
    add_bullet(doc, "Seluruh arsitektur didesain beroperasi pada perimeter tertutup (private on-premise cloud) BPJS Kesehatan dengan enkripsi AES-256 dan salted SHA-256 pseudonymization, selaras penuh dengan standar SATUSEHAT HL7 FHIR R4 dan regulasi UU PDP No. 27/2022.", "5. Kepatuhan Ketat UU PDP No. 27/2022 & Interoperabilitas: ")

    add_body(doc, "Evaluasi empiris terhadap portofolio 300 berkas klaim tervalidasi klinis (Dataset v2.1 senilai Rp 3,53 Miliar) membuktikan performa superior model MHGSL: Akurasi 93.0%, Presisi 94.12%, ROC-AUC 0.9825, dan AUPRC 0.9142 (+28.6% dibanding baseline XGBoost 0.71). Model menunjukkan ketahanan kamuflase mencapai 89.4% pada tingkat masking rujukan 40%, serta 100% mendeteksi 9 pola sindikat terorganisir (SYND-01 s/d SYND-09). Pada portofolio sampel tersebut, sistem berhasil mengidentifikasi 60 klaim anomali dengan potensi penghematan/pencegahan kebocoran tarif INA-CBG riil sebesar Rp 507,37 Juta (rata-rata Rp 8,46 Juta per kasus fraud). Implementasi Aegis-JKN diproyeksikan memangkas durasi review awal sebesar 30-50% per berkas anomali, memberikan rasio Cost-to-Impact konservatif 1 : 15, serta menyelamatkan ratusan miliar rupiah Dana Jaminan Sosial (DJS) Kesehatan setiap tahunnya.")

    add_body(doc, "KATA KUNCI: Kecurangan Klaim JKN, Upcoding, Phantom Billing, Unbundling, Fraud Rings, Multi-Hop Graph Structure Learning (MHGSL), Topological Camouflage, Human-in-the-Loop, Explainable AI (XAI), UU Pelindungan Data Pribadi No. 27/2022.")

    doc.add_page_break()

    # ==========================================
    # DAFTAR ISI, DAFTAR TABEL & GAMBAR
    # ==========================================
    add_heading_1(doc, "DAFTAR ISI")

    toc_items = [
        ("LEMBAR PERNYATAAN ORISINALITAS DAN INTEGRITAS", "ii"),
        ("RINGKASAN EKSEKUTIF", "iii"),
        ("DAFTAR ISI", "iv"),
        ("DAFTAR TABEL & DAFTAR GAMBAR", "v"),
        ("BAB I: PENDAHULUAN", "1"),
        ("  1.1 Latar Belakang & Urgensi Nasional", "1"),
        ("  1.2 Identifikasi Permasalahan Utama (Upcoding, Unbundling, & Fraud Rings)", "2"),
        ("  1.3 Fenomena Topological Camouflage pada Ekosistem JKN", "3"),
        ("  1.4 Rumusan Masalah Inovasi", "4"),
        ("  1.5 Tujuan dan Sasaran Inovasi", "4"),
        ("  1.6 Ruang Lingkup dan Batasan Sistem", "5"),
        ("BAB II: ANALISIS AKAR MASALAH (ROOT CAUSE ANALYSIS)", "6"),
        ("  2.1 Metodologi Analisis 5-Whys Kegagalan Deteksi Kolusi", "6"),
        ("  2.2 Analisis Fishbone 4 Dimensi Kendala Audit Klaim JKN", "7"),
        ("  2.3 Sintesis Akar Masalah: Kebutuhan Paradigma Graph Learning", "9"),
        ("BAB III: DESKRIPSI & VALUE PROPOSITION SOLUSI AEGIS-JKN", "10"),
        ("  3.1 Gambaran Umum Platform Aegis-JKN", "10"),
        ("  3.2 Value Proposition & Diferensiasi Strategis Multi-Channel", "11"),
        ("  3.3 Analisis Komparatif Pendekatan Solusi (Manual vs Rule vs ML vs Aegis)", "12"),
        ("  3.4 Prinsip Right-Sized Hybrid Engineering & Dual-Path Processing", "14"),
        ("BAB IV: ARSITEKTUR & MEKANISME CARA KERJA SISTEM", "15"),
        ("  4.1 End-to-End Workflow Pipeline & Dual-Path Production Inference", "15"),
        ("  4.2 Modul 1: Ingestion Data, Normalisasi SATUSEHAT, & Tokenisasi Anonim", "16"),
        ("  4.3 Modul 2: Tier-1 Deterministic Rule-Based Pre-Filter", "17"),
        ("  4.4 Modul 3: Tier-2 Tabular Classifier & Tier-3 Tri-Channel MHGSL Engine", "18"),
        ("  4.5 Modul 4: Multimodal Late Fusion & Triase Risiko Dinamis", "20"),
        ("  4.6 Modul 5: Explainability Layer & Dekomposisi Atribusi SHAP", "21"),
        ("  4.7 Modul 6: Interactive Verifier Decision Support Interface (Next.js 16)", "22"),
        ("BAB V: TATA KELOLA DATA, KEAMANAN, DAN PRIVASI", "23"),
        ("  5.1 Kepatuhan Terhadap UU PDP No. 27/2022 & UU Kesehatan No. 17/2023", "23"),
        ("  5.2 Strategi De-identifikasi, Salted Pseudonymization, & Hashing", "24"),
        ("  5.3 Protokol Anti-Data Leakage v2.1 & Group Cross-Validation", "25"),
        ("  5.4 Arsitektur Penyimpanan & Perimeter Private Cloud BPJS Kesehatan", "26"),
        ("  5.5 Manajemen Akses (RBAC) & Immutable Audit Trail", "27"),
        ("BAB VI: KERANGKA HUMAN-IN-THE-LOOP & HUMAN AUTONOMY", "28"),
        ("  6.1 Filosofi Human-Centered AI dalam Pengawasan Klaim JKN", "28"),
        ("  6.2 Prinsip Utama: Fail-Safe AI & Hak Otonomi Verifikator", "29"),
        ("  6.3 Matriks Pembagian Peran Kerja AI vs Verifikator Manusia", "30"),
        ("  6.4 Alur Interaksi Verifikator & Safe-Mode Fallback Protocol", "31"),
        ("  6.5 Strategi Komprehensif Mitigasi Alert Fatigue & Halusinasi AI", "33"),
        ("BAB VII: RENCANA MINIMUM VIABLE PRODUCT (MVP) & SIMULASI", "36"),
        ("  7.1 Sasaran Pembuktian MVP & Hipotesis Teknis", "36"),
        ("  7.2 Use Case Spesifik: 9 Pola Sindikat Fraud Ring (SYND-01 s/d SYND-09)", "37"),
        ("  7.3 Integrasi Simulasi Multi-Agent OASIS (Discrete Event Simulator)", "38"),
        ("  7.4 Spesifikasi Ruang Lingkup MVP (In-Scope vs Out-of-Scope)", "40"),
        ("  7.5 Dataset Sintetis v2.1 Tervalidasi (300 Klaim INA-CBG/FHIR R4)", "41"),
        ("BAB VIII: PROYEKSI DAMPAK & KEY PERFORMANCE INDICATORS (KPI)", "43"),
        ("  8.1 Kerangka Evaluasi Multi-Dimensi", "43"),
        ("  8.2 Technical KPI & Hasil Validasi Benchmark Empiris", "44"),
        ("  8.3 Operational KPI & Efisiensi Waktu Telaah", "45"),
        ("  8.4 Economic KPI & Analisis Portofolio Sampel Rp 3,53 Miliar", "46"),
        ("  8.5 User Acceptance KPI & Pengujian A/B Baseline", "48"),
        ("BAB IX: ANALISIS KELAYAKAN (FEASIBILITY STUDY)", "49"),
        ("  9.1 Kelayakan Teknis (Technical Feasibility)", "49"),
        ("  9.2 Kelayakan Data & Interoperabilitas (SATUSEHAT & V-Claim)", "50"),
        ("  9.3 Kelayakan Operasional & Manajemen Perubahan (Change Management)", "51"),
        ("  9.4 Kelayakan Finansial & Efisiensi Infrastruktur On-Premise", "52"),
        ("  9.5 Struktur Organisasi & Kompetensi Tim Pengembang", "53"),
        ("BAB X: MANAJEMEN RISIKO & STRATEGI MITIGASI", "55"),
        ("  10.1 Identifikasi 12 Risiko Kritis Implementasi Aegis-JKN", "55"),
        ("  10.2 Matriks Manajemen Risiko Komprehensif", "56"),
        ("  10.3 Protokol Tanggap Darurat & Continuous Model Monitoring", "59"),
        ("BAB XI: ROADMAP PENGEMBANGAN & RENCANA IMPLEMENTASI", "60"),
        ("  11.1 Kerangka Kerja Stage-Gate Roadmap", "60"),
        ("  11.2 Rencana Pelaksanaan 8-12 Minggu Purwarupa & Roadmap 12 Bulan", "61"),
        ("  11.3 Indikator Keberhasilan Antar-Tahap (Stage-Gate Criteria)", "64"),
        ("BAB XII: KESIMPULAN & PENUTUP", "65"),
        ("  12.1 Sintesis Nilai Strategis Solusi Aegis-JKN", "65"),
        ("  12.2 Kesiapan Implementasi & Rekomendasi Menuju Healthkathon 2026", "66"),
        ("DAFTAR PUSTAKA & REFERENSI REGULASI", "67")
    ]

    for item, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.line_spacing = 1.05

        # Dots filler
        dots = " ." * int((72 - len(item)) / 2)
        r_txt = p_t.add_run(f"{item} {dots} {page}")
        r_txt.font.name = "Times New Roman"
        if item.startswith("BAB") or item.startswith("LEMBAR") or item.startswith("RINGKASAN") or item.startswith("DAFTAR"):
            r_txt.font.size = Pt(10.0)
            r_txt.bold = True
            r_txt.font.color.rgb = RGBColor(31, 78, 121)
        else:
            r_txt.font.size = Pt(9.5)

    doc.add_page_break()

    # DAFTAR TABEL & GAMBAR
    add_heading_1(doc, "DAFTAR TABEL & DAFTAR GAMBAR")

    p_dt = doc.add_paragraph()
    r_dt = p_dt.add_run("Daftar Tabel")
    r_dt.font.name = "Times New Roman"
    r_dt.font.size = Pt(11)
    r_dt.bold = True

    tables_list = [
        ("Tabel 2.1: Matriks Analisis 5-Whys Akar Masalah Kegagalan Deteksi Fraud Sindikat", "6"),
        ("Tabel 2.2: Analisis Fishbone 4 Dimensi Kendala Audit Klaim JKN Nasional", "8"),
        ("Tabel 3.1: Komparasi Pendekatan Audit Klaim: Manual vs Rule vs XGBoost vs Pure AI vs Aegis-JKN", "13"),
        ("Tabel 5.1: Matriks Kepatuhan Prinsip UU PDP No. 27/2022 pada Platform Aegis-JKN", "24"),
        ("Tabel 6.1: Matriks Pembagian Peran Kerja AI vs Verifikator Manusia (Human-in-the-Loop)", "30"),
        ("Tabel 7.1: Spesifikasi Ruang Lingkup MVP Aegis-JKN (In-Scope vs Out-of-Scope)", "40"),
        ("Tabel 7.2: Katalog 9 Pola Sindikat Fraud Ring (SYND-01 s/d SYND-09) pada Dataset v2.1", "42"),
        ("Tabel 8.1: Kerangka Key Performance Indicators (KPI) 4 Dimensi Aegis-JKN", "44"),
        ("Tabel 8.2: Ringkasan Analisis Finansial Portofolio 300 Klaim (Dataset v2.1 senilai Rp 3,53 Miliar)", "47"),
        ("Tabel 9.1: Struktur Organisasi dan Distribusi Kompetensi Tim Inovator", "54"),
        ("Tabel 10.1: Matriks Manajemen Risiko Komprehensif (12 Risiko Kritis & Rencana Mitigasi)", "56"),
        ("Tabel 11.1: Roadmap Implementasi 7 Tahap Berbasis Stage-Gate Framework (12 Bulan)", "62"),
    ]

    for item, page in tables_list:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(2)
        dots = " ." * int((72 - len(item)) / 2)
        r_txt = p_t.add_run(f"{item} {dots} {page}")
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(9.5)

    p_dg = doc.add_paragraph()
    p_dg.paragraph_format.space_before = Pt(12)
    r_dg = p_dg.add_run("Daftar Gambar")
    r_dg.font.name = "Times New Roman"
    r_dg.font.size = Pt(11)
    r_dg.bold = True

    figures_list = [
        ("Gambar 4.1: Arsitektur Alur Kerja End-to-End Aegis-JKN (Tri-Tier & Dual-Path Pipeline)", "16"),
        ("Gambar 4.2: Konstruksi Graf Heterogen Tri-Channel (Topologi, Fitur, Semantik Metapath)", "19"),
        ("Gambar 4.3: Mekanisme Fusi Atensi Multi-Channel & Deteksi Topological Camouflage", "20"),
        ("Gambar 6.1: Antarmuka Keputusan Verifikator dengan Visualisasi Klaster Bipartite Dokter-Faskes", "32"),
        ("Gambar 6.2: Alur Safe-Mode Fallback Protocol Pemutus Rekomendasi Otomatis (Threshold >30%)", "34"),
        ("Gambar 7.1: Topologi Simulasi Multi-Agent OASIS (20 Pasien, 12 Dokter, 6 RS)", "39"),
        ("Gambar 11.1: Diagram Alir Stage-Gate Progression Roadmap Aegis-JKN", "61")
    ]

    for item, page in figures_list:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(2)
        dots = " ." * int((72 - len(item)) / 2)
        r_txt = p_t.add_run(f"{item} {dots} {page}")
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(9.5)

    doc.add_page_break()
    print("Cover and preface built successfully.")
