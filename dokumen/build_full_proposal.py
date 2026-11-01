# -*- coding: utf-8 -*-
"""
Master Build Script: Proposal Inovasi Healthkathon BPJS Kesehatan 2026
Aegis-JKN: Clinical Decision Support & Fraud Intelligence Platform
Menggabungkan seluruh modul BAB I s/d BAB XII, Cover, Lembar Pernyataan,
Ringkasan Eksekutif, Daftar Isi, Daftar Tabel/Gambar, dan Daftar Pustaka.
Menghasilkan dokumen resmi: Healthkathon_Kandidat_1.docx
"""

import os
import sys
import time

from generate_aegis_proposal import create_document
from section_cover_preface import build_cover_and_preface
from section_bab_1_to_3 import build_bab_1_to_3
from section_bab_4_to_6 import build_bab_4_to_6
from section_bab_7_to_9 import build_bab_7_to_9
from section_bab_10_to_12 import build_bab_10_to_12

def main():
    print("=" * 70)
    print("MEMULAI PROSES ASSEMBLY PROPOSAL INOVASI AEGIS-JKN...")
    print("Target Dokumen: Healthkathon_Kandidat_1.docx")
    print("=" * 70)
    start_time = time.time()

    # 1. Inisialisasi dokumen dasar (A4, 4-3-3-3 cm margins, headers/footers)
    print("\n[1/6] Menginisialisasi dokumen dasar & layout A4 (4-3-3-3 cm)...")
    doc = create_document()

    # 2. Cover, Lembar Orisinalitas, Ringkasan Eksekutif, Daftar Isi, Tabel, Gambar
    print("[2/6] Membangun Cover, Lembar Pernyataan, Ringkasan Eksekutif & Struktur Dokumen...")
    build_cover_and_preface(doc)

    # 3. BAB I (Pendahuluan), BAB II (RCA 5-Whys & Fishbone), BAB III (Value Proposition)
    print("[3/6] Membangun Bab I s/d Bab III (Urgensi 2 Juta Klaim, RCA, Value Prop)...")
    build_bab_1_to_3(doc)

    # 4. BAB IV (Arsitektur Pipeline & Formulasi MHGSL), BAB V (Tata Kelola Data), BAB VI (HITL & XAI)
    print("[4/6] Membangun Bab IV s/d Bab VI (MHGSL Formulas, Late Fusion, UU PDP, HITL)...")
    build_bab_4_to_6(doc)

    # 5. BAB VII (Rencana MVP & Simulasi OASIS), BAB VIII (KPI & Portofolio Rp 3.53B), BAB IX (Feasibility)
    print("[5/6] Membangun Bab VII s/d Bab IX (9 Sindikat, KPI, Benchmark Rp 507 Juta, Tim)...")
    build_bab_7_to_9(doc)

    # 6. BAB X (Manajemen Risiko), BAB XI (Roadmap 12 Bulan), BAB XII (Kesimpulan & Daftar Pustaka)
    print("[6/6] Membangun Bab X s/d Bab XII (12 Risiko, Stage-Gate Roadmap, Pustaka)...")
    build_bab_10_to_12(doc)

    # Output file
    output_path = os.path.join(os.path.dirname(__file__), "Healthkathon_Kandidat_1.docx")
    print(f"\nMenyimpan file ke: {output_path}...")
    doc.save(output_path)

    elapsed = time.time() - start_time
    file_size_kb = os.path.getsize(output_path) / 1024

    print("=" * 70)
    print(f"ASSEMBLY BERHASIL DISELESAIKAN DALAM {elapsed:.2f} DETIK!")
    print(f"File Output: {output_path}")
    print(f"Ukuran File: {file_size_kb:.2f} KB")
    print("Jumlah Paragraf: ", len(doc.paragraphs))
    print("Jumlah Tabel: ", len(doc.tables))
    print("=" * 70)

if __name__ == "__main__":
    main()
