# Aegis-JKN User Manual & Navigation Guide

### Comprehensive Operational Manual for Verifiers, Auditors, and Healthkathon Reviewers

---

## 1. Platform Overview & Interface Layout

Aegis-JKN dirancang sebagai antarmuka komando tunggal (*single-pane-of-glass*) yang intuitif untuk verifikator BPJS Kesehatan. Seluruh informasi disajikan dalam tata letak vertikal modular yang saling terhubung melalui *anchor links* dan pintasan papan ketik (*keyboard shortcuts*).

Struktur antarmuka terdiri dari 8 seksi utama:
1. **Header & Navigation Bar**: Status sistem, tautan seksi cepat, toggle bahasa, toggle tema, dan tombol uploader klaim.
2. **Hero Dashboard**: Ringkasan rasio beban kerja nasional (2.000.000 klaim vs 1.000 verifikator) dan indikator performa utama.
3. **Pilar Risiko Kecurangan**: Taksonomi risiko faskes, peserta, dan badan usaha.
4. **Arsitektur MHGSL**: Pipeline 5 tahap pemrosesan data SATUSEHAT FHIR ke graf.
5. **Multi-Channel Graph Explorer**: Kanvas graf interaktif 3 kanal (Topologi, Fitur, Semantik).
6. **Simulasi Upcoding 4 Langkah**: Rekonstruksi investigasi klaim dengan pembongkaran kamuflase SHAP.
7. **Sindikat Kolusi & Drilldown Modal**: Peta jaringan fraud ring dan profil audit entitas tersangka.
8. **Suite Evaluasi Benchmark**: Perbandingan multi-metrik terhadap model machine learning standar.

---

## 2. Global Controls, Theme, and Internationalization

### 2.1. Language Switcher (Dukungan Dwibahasa ID / EN)
Platform dilengkapi sistem kamus bilingual penuh (*Aegis-i18n*).
- **Lokasi Tombol**: Di sisi kanan Navbar (ikon bola dunia atau badge `[ID] / [EN]`).
- **Fungsi**: Mengalihkan seluruh istilah antarmuka, terminologi medis, metrik evaluasi, dan narasi investigasi secara instan antara Bahasa Indonesia (ID) dan Bahasa Inggris (EN).
- **Persistensi**: Pilihan bahasa tersimpan di state memori peramban selama sesi aktif.

### 2.2. Theme Switcher (Dark Mode / Light Mode)
Antarmuka mendukung mode gelap dan terang berstandar kontras WCAG 2.1 AA berbasis palet OKLCH.
- **Lokasi Tombol**: Di sisi kanan Navbar (ikon Matahari / Bulan).
- **Pintasan Keyboard**: Tekan tombol `t` pada keyboard untuk berpindah mode secara instan.
- **Efek**: Elemen latar, kartu audit, kanvas graf SVG, dan diagram Recharts secara dinamis menyesuaikan kontras tanpa memerlukan pemuatan ulang halaman.

### 2.3. Print & PDF Export
- **Pintasan Keyboard**: Tekan tombol `p` pada keyboard.
- **Fungsi**: Membuka dialog cetak sistem operasi yang telah diformat khusus via CSS `@media print`, menghasilkan laporan audit yang rapi untuk lampiran investigasi fisik atau berkas persidangan P2PK.

---

## 3. Keyboard Shortcuts Reference

Aegis-JKN mengaktifkan pintasan tombol global untuk mempercepat navigasi verifikator. Seluruh pintasan diabaikan secara otomatis saat verifikator sedang mengetik di dalam formulir input teks.

| Tombol | Deskripsi | Aksi yang Dijalankan |
|---|---|---|
| `t` | **Toggle Theme** | Mengubah tampilan antara Dark Mode dan Light Mode |
| `p` | **Print / PDF** | Membuka antarmuka cetak laporan dokumen audit |
| `g` | **Scroll to Graph** | Menggulir layar langsung ke Multi-Channel Graph Explorer |
| `s` | **Scroll to Simulation** | Menggulir layar langsung ke Simulasi Upcoding 4 Langkah |
| `→` | **Next Simulation Step** | Melangkah ke tahap simulasi berikutnya |
| `←` | **Prev Simulation Step** | Kembali ke tahap simulasi sebelumnya |

---

## 4. Section-by-Section Operational Guide

### 4.1. Multi-Channel Graph Explorer
Modul ini memungkinkan verifikator membedah relasi jaringan dari tiga perspektif yang berbeda:

1. **Memilih Kanal Graf**:
   - Klik tab **Topology Graph ($A^{(top)}$)**: Menampilkan alur pelayanan medis nyata (Pasien $\to$ Dokter $\to$ RS $\to$ Tindakan).
   - Klik tab **Feature Graph ($A^{(feat)}$)**: Menampilkan sisi sintetis berdasarkan kemiripan kosinus atribut (panah putus-putus antara $P_1-P_2$ dan $P_2-P_3$).
   - Klik tab **Semantic Graph ($A^{(sem)}$)**: Menampilkan jalur perilaku tingkat tinggi (relasi komposit antara Dokter $D_1/D_2$ dengan $Dx_{ringan}$ dan $S_{mahal}$).
2. **Inspeksi Simpul**:
   - Arahkan kursor (*hover*) pada simpul mana pun untuk melihat nama entitas, peran, dan keterangan klinis.
   - Klik simpul untuk melihat rincian in-degree dan out-degree pada panel informasi bawah.
3. **Sorot Metapath Anomali**:
   - Klik tombol **Sorot Metapath Upcoding**: Jalur melingkar $D \to Dx \to S \to RS$ akan menyala terang dengan animasi pulsa, menandakan siklus penagihan abnormal.

### 4.2. 4-Step Upcoding Simulation & SHAP Interpretation
Modul ini mendemonstrasikan bagaimana model mendeteksi kamuflase topologis secara bertahap:

1. **Kontrol Simulasi**:
   - Tombol **Next** / **Prev**: Berpindah langkah secara manual (atau gunakan tombol panah `→` / `←`).
   - Tombol **Auto-Play** / **Pause**: Menjalankan simulasi berurutan dengan jeda 3 detik per tahap.
   - Tombol **Reset**: Mengembalikan simulasi ke Langkah 01.
2. **Interpretasi Indikator Langkah**:
   - **Langkah 1 (Klaim Masuk)**: Skor Fraud $0.32$ (Status: Wajar). Topologi tampak seperti rujukan rumah sakit umum.
   - **Langkah 2 (Analisis Fitur)**: Skor Fraud $0.61$ (Status: Review). Terdeteksi klaster pasien dengan LOS identik 3 hari.
   - **Langkah 3 (Analisis Semantik)**: Skor Fraud $0.84$ (Status: Tinggi). Terdeteksi anomali pemasangan diagnosis ringan dengan bedah mahal.
   - **Langkah 4 (Fusion & Klasifikasi SHAP)**: Skor Fraud $0.94$ (Status: Fraud Terkonfirmasi).
3. **Membaca Diagram Dekomposisi SHAP**:
   - **Bar Merah/Oranye (Positif)**: Menunjukkan faktor pendorong kecurangan. Metapath semantik ($+41\%$) dan kesamaan fitur ($+38\%$).
   - **Bar Hijau/Biru (Negatif)**: Menunjukkan faktor peredam kecurangan semu. Topologi rujukan ($-12\%$) membuktikan adanya **upaya kamuflase** yang disengaja oleh pelaku.

### 4.3. Syndicate Collusion Ring & Audit Drilldown
Modul ini memvisualisasikan bagaimana jaringan kolusi beroperasi dan menyediakan berkas audit lengkap:

1. **Toggle Subgraf Padat**:
   - Klik tombol **Sembunyikan highlight / Tampilkan subgraf padat**: Mengaktifkan lingkaran halo merah pada komunitas anomali dokter-faskes.
2. **Animasi Message-Passing**:
   - Klik tombol simulasi aliran pesan untuk melihat bagaimana bobot risiko menyebar dari simpul faskes ke dokter dan pasien terkait.
3. **Membuka Modal Audit Mendalam (Drilldown Modal)**:
   - Klik pada simpul berisiko tinggi yang memiliki lingkaran animasi (misal: simpul **D₁**, **RS_A**, atau **P₁**).
   - Modal audit akan terbuka menyajikan informasi investigasi:
     - **Profil Entitas**: Nama lengkap, peran pelayanan, dan skor risiko fraud ($0.0 - 1.0$).
     - **Ringkasan Kasus**: Narasi deskriptif temuan penyimpangan.
     - **Bukti Forensik per Kanal**: Bobot pembuktian matematis dari kanal semantik, fitur, dan topologi.
     - **Kronologi Insiden**: Linimasa historis klaim mencurigakan.
     - **Metrik Utama**: Volume klaim 30 hari, deviasi peer ($+4.2\sigma$), dan total rupiah klaim.
     - **Rekomendasi Tindakan Verifikator**: Rekomendasi audit lapangan, penangguhan klaim, atau klarifikasi pasien.

### 4.4. Self-Service Data Uploader (Evaluasi Klaim Mandiri)
Modul ini memungkinkan penguji atau verifikator mengevaluasi berkas klaim khusus:

1. **Membuka Uploader**:
   - Klik tombol **Uji Data Mandiri** atau **Score Custom Claims** di Navbar atau bagian header.
2. **Memasukkan Data**:
   - **Metode A**: Klik tombol **Gunakan Contoh Data CSV** untuk mengisi data klaim sintetis otomatis.
   - **Metode B**: Seret (*drag & drop*) berkas `.csv` atau `.json` ke dalam area uploader.
   - **Metode C**: Salin dan tempel data berformat teks CSV langsung ke area input.
3. **Menjalankan Penilaian**:
   - Klik tombol **Hitung Skor MHGSL**. Mesin inferensi klien akan mengalkulasi skor topologi, fitur, dan semantik untuk setiap baris.
4. **Membaca Hasil Evaluasi**:
   - Setiap baris klaim akan diberi atribut skor kanal ($0.00 - 1.00$), skor fusi akhir, dan badge tingkat risiko:
     - **Fraud** (Skor $\ge 0.85$): Warna Merah Tua - Indikasi kuat kecurangan sindikat.
     - **High** (Skor $0.65 - 0.84$): Warna Oranye - Memerlukan tinjauan berkas fisik.
     - **Medium** (Skor $0.40 - 0.64$): Warna Kuning - Perlu konfirmasi kode diagnosis.
     - **Low** (Skor $< 0.40$): Warna Hijau - Klaim bersih dan layak diterbitkan FPK.
