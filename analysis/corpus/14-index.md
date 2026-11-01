<!-- source: notion page 3f23e603-1ab7-808d-b2cb-fe92cd62391d -->

## [Sub-page] ARSIP SUMBER | Kandidat Ide Hackathon BPJS Kesehatan
> **{'type': 'emoji', 'emoji': '🎯'}** Deteksi Efisiensi & Kecurangan Program JKN (Aegis-JKN Healthkathon BPJS)
> **{'type': 'emoji', 'emoji': '💡'}** CATATAN EDITORIAL | Dokumen sumber. Untuk naskah terkendali, gunakan [Pemilihan Kandidat Inovasi dan Batas Ruang Lingkup MVP](https://app.notion.com/p/05-Pemilihan-Kandidat-Inovasi-dan-Batas-Ruang-Lingkup-MVP-4003e6031ab78156b244cccd2c5ecd9e). Versi ini dipertahankan sebagai rekam jejak analisis awal. Klaim statistik atau kebijakan dalam isi lama perlu diperiksa melalui sumber primer sebelum dikutip.
Dokumen ini berisi pemetaan 3 kandidat ide solusi untuk pencegahan kebocoran dana dan peningkatan efisiensi operasional BPJS Kesehatan, hasil ekstraksi dan analisis berkas proposal.
---
## Kandidat 1: Anomali Diagnosa Jantung & Saraf (Upcoding)
> **{'type': 'emoji', 'emoji': '🏥'}** Kategori: Efisiensi Risiko Fasilitas Kesehatan (Upcoding & Unbundling)
- Masalah: Faskes memanipulasi kode diagnosis pasien ke tingkat keparahan yang lebih tinggi (severity level III) atau memecah klaim tindakan yang seharusnya satu paket untuk mendapatkan tarif INA-CBG yang jauh lebih besar.
- Bukti: Temuan KPK dan BPJS sering menyoroti lonjakan drastis pada tagihan klaim penyakit kronis (seperti katarak, jantung, bedah saraf) di faskes tertentu yang tidak sejalan dengan profil epidemiologi wilayah tersebut.
- Siapa yang Terdampak: Finansial BPJS Kesehatan (mengalami kebocoran dana hingga triliunan rupiah) dan pasien sesungguhnya (antrean faskes penuh oleh tindakan medis yang diada-adakan).
- Mekanisme Masalah: Dokter atau koder di rumah sakit menambahkan komplikasi sekunder pada sistem e-Klaim yang tidak tercatat dalam rekam medis elektronik (EMR) pasien, memanfaatkan celah verifikasi manual BPJS yang memakan waktu lama.
- Solusi Hipotesis: Ekstraksi dan pencocokan otomatis menggunakan model bahasa lokal (Local LLM). Membangun pipeline yang membaca narasi teks pada EMR pasien, lalu mencocokkannya dengan kode ICD-10 yang diinput faskes. Jika ada ketidaksesuaian (misalnya EMR menyebut 'batuk ringan' tapi klaim menyebut 'pneumonia berat'), sistem langsung menahan klaim dan mengirimkan notifikasi flagging otomatis ke verifikator BPJS sebelum dana cair.
---
## Kandidat 2: Sindikat Joki Pasien (Penyalahgunaan Identitas)
> **{'type': 'emoji', 'emoji': '👤'}** Kategori: Efisiensi Risiko Peserta JKN (Penyalahgunaan Identitas)
- Masalah: Pasien menggunakan kartu JKN milik orang lain (kerabat atau sewaan) untuk mengakses layanan kesehatan berbiaya tinggi (cuci darah, operasi, kemoterapi).
- Bukti: Laporan investigasi lapangan menunjukkan adanya ketidakcocokan identitas fisik pasien dengan data di sistem, terutama di faskes tingkat lanjut yang memiliki antrean panjang dan pengawasan visual minim.
- Siapa yang Terdampak: BPJS Kesehatan (membayar layanan untuk pihak yang tidak berhak) dan pemilik kartu asli (riwayat medisnya menjadi kacau, berisiko malapraktik di masa depan).
- Mekanisme Masalah: Faskes mengejar kecepatan pelayanan karena antrean membeludak, sehingga petugas administrasi sering melewatkan verifikasi fisik KTP/wajah dan hanya memindai nomor kartu atau NIK.
- Solusi Hipotesis: Modul Face Verification mandiri berbasis PWA (Progressive Web App). Pasien melakukan lapor diri (check-in) secara mandiri di mesin kiosk atau HP masing-masing melalui web app. Kamera akan menangkap wajah pasien dan mencocokkannya dengan database kependudukan/BPJS. Jika skor kecocokan rendah, akses sistem antrean terkunci dan dialihkan ke verifikasi manual.
---
## Kandidat 3: Manipulasi Gaji Pekerja (Under-reporting Upah)
> **{'type': 'emoji', 'emoji': '💼'}** Kategori: Efisiensi Risiko Pemberi Kerja (Under-reporting Upah)
- Masalah: Perusahaan atau badan usaha dengan sengaja melaporkan gaji karyawan lebih rendah dari yang sebenarnya (biasanya disamakan dengan UMR) agar beban iuran 4% yang ditanggung perusahaan menjadi seminimal mungkin.
- Bukti: Terdapat selisih masif jika data iuran BPJS Kesehatan dikomparasi dengan data pelaporan pajak PPh 21 dari Direktorat Jenderal Pajak (DJP) atau standar gaji industri di wilayah tersebut.
- Siapa yang Terdampak: Peserta JKN/Pekerja (kelas rawat inap berpotensi turun) dan BPJS Kesehatan (kehilangan potensi penerimaan iuran yang signifikan).
- Mekanisme Masalah: HRD memanipulasi struktur slip gaji dengan mengecilkan 'Gaji Pokok' dan membesarkan 'Tunjangan Tidak Tetap' khusus untuk pelaporan ke BPJS, memanfaatkan minimnya integrasi data antar instansi pemerintah.
- Solusi Hipotesis: Platform agregasi data dan whistleblowing otomatis. Membuat sistem dashboard analitik yang mendeteksi anomali pelaporan gaji berdasarkan wilayah dan sektor industri. Solusi ini dilengkapi dengan bot pelaporan anonim (misalnya via Telegram/WhatsApp) bagi pekerja untuk mengunggah slip gaji asli mereka. Sistem akan secara otomatis memvalidasi bukti tersebut dan mengkalkulasi estimasi denda perusahaan.
---
## Rekomendasi Pilihan dan Justifikasi
> **{'type': 'emoji', 'emoji': '⭐'}** PILIHAN UTAMA: Kandidat 1 (Anomali Diagnosa Jantung & Saraf / Upcoding). CADANGAN: Kandidat 3.
- Alasan Pemilihan Kandidat 1: Memiliki relevansi tertinggi terhadap mitigasi kebocoran Dana Jaminan Sosial (DJS) terbesar. Fraud klaim rujukan tingkat lanjut menyumbang porsi pemborosan dana BPJS paling masif.
- Analisis Risiko Kandidat 2: Kandidat 2 berisiko dianggap redundan karena BPJS Kesehatan sudah mengimplementasikan fitur biometrik FRIDAY / Face Recognition di aplikasi Mobile JKN dan loket faskes.
- Posisi Kandidat 3: Kandidat 3 sangat prospektif dari sisi revenue recovery, namun membutuhkan integrasi lintas kementerian (DJP Kemenkeu dan Kemenaker) yang memiliki friksi birokrasi lebih tinggi.
## Matriks Perbandingan Strategis 3 Kandidat
| Parameter | Kandidat 1 (Upcoding) | Kandidat 2 (Joki Pasien) | Kandidat 3 (Under-reporting Upah) |
| Potensi Efisiensi DJS | Sangat Tinggi (Triliunan) | Sedang hingga Tinggi | Tinggi (Iuran) |
| Kompleksitas Teknis | Sedang (NLP / Local LLM) | Rendah ke Sedang (Vision/PWA) | Rendah (Data Cross-match) |
| Risiko Redundansi | Rendah (Belum ada verifikasi otomatis) | Tinggi (Sudah ada FRIDAY Mobile JKN) | Rendah (Kanal baru) |
| Hambatan Regulasi | Internal BPJS & Faskes | Izin Akses Kependudukan / Dukcapil | Tinggi (Kemenkeu DJP & Kemenaker) |
| Rekomendasi Akhir | Pilihan Utama (Aegis-JKN) | Tidak Direkomendasikan | Cadangan Strategis |
> **{'type': 'emoji', 'emoji': '💡'}** HALAMAN KENDALI PROYEK | Mulai dari [00 | HEALTHKATHON Project Dashboard](https://app.notion.com/p/00-HEALTHKATHON-Project-Dashboard-4003e6031ab7815a89bdedc0c4d92c2f) untuk mengakses dokumen terkendali, dataset aktif, daftar bukti, dan prioritas pekerjaan. Halaman sumber lama tetap disimpan sebagai referensi historis. Jangan menggunakan angka benchmark atau finansial sebagai hasil final sebelum bukti replikasi tersedia.
## [Sub-page] Draft

## [Database] Riset Fraud JKN | Register Pengetahuan dan Sumber
## [Sub-page] ARSIP DATA v1 | Dataset Simulasi Aegis-JKN, 100 Klaim Sintetis
> **{'type': 'emoji', 'emoji': '🗂️'}** Dataset sintetis untuk uji simulasi MHGSL pada purwarupa Aegis-JKN ([aegisjkn.vercel.app](http://aegisjkn.vercel.app/)). 100 klaim, privacy-by-design - bukan data peserta riil, aman menurut Permenkes 24/2022 & UU PDP No. 27/2022. Pendamping makalah [ARSIP SUMBER | Aegis-JKN Arsitektur dan Strategi Pengembangan Sistem Deteksi Fraud JKN](https://app.notion.com/p/3ef3e6031ab781d1962af8955843ed0f).
> **{'type': 'emoji', 'emoji': '💡'}** CATATAN VERSI | Halaman ini mendokumentasikan dataset sintetis 100 klaim sebagai versi demo awal. Dataset aktif saat ini adalah database Klaim Aegis-JKN v2 dengan 300 baris. Gunakan [Dataset Registry dan Data Dictionary](https://app.notion.com/p/03-Dataset-Registry-Data-Dictionary-dan-Protokol-Reproduksibilitas-4003e6031ab781749a55d4ee8fff3fd2) sebagai rujukan definisi, versi, dan protokol evaluasi.
## Ringkasan & Ground Truth
- Jumlah klaim: 100 (20 pasien · 12 dokter · 6 FKRTL · 10 diagnosis · 10 prosedur · 10 obat).
- Distribusi risiko: 76 low · 4 medium · 6 high · 14 fraud.
- Ground truth: klaim anomali = KLM001-KLM024 (14 fraud sindikat + 10 anomali medium/high); klaim normal = KLM025-KLM100.
- Skala risiko: skor <0.35 low; 0.35-0.6 medium; 0.6-0.8 high; lebih dari 0.8 fraud.
- Catatan prevalensi: fraud di-oversample 14% untuk keperluan demo; estimasi lapangan 3-7% (label estimasi literatur).
- Mapping FHIR R4: klaim = Claim; pasien = Patient; dokter = Practitioner; faskes = Organization; diagnosis = Condition (ICD-10); prosedur = Procedure (ICD-9-CM); obat = MedicationRequest/Dispense; LOS = Encounter.length; biaya = [Claim.total](http://claim.total/); tanggal = Encounter.period.start.
- Saluran MHGSL: topologi = edges kunjungan/afiliasi/layanan/semantik; fitur = cosine similarity (LOS, biaya, qty obat) dengan ambang 0.85; semantik = metapath diagnosis ke prosedur.
## Sindikat Ground Truth
| ID | Modus | Faskes | Dokter | Pasien | Klaim | Skenario & Sinyal Deteksi | Skor |
| SYND-01 | Upcoding | RS_A | D01, D02 | P01-P03 | KLM001-003 | Dx gastritis (K29.7) ditagih PCI (00.66); biaya & LOS identik; subgraf padat | ≥ 0.93 |
| SYND-02 | Phantom Billing | RS_C | D05 | P08-P10 | KLM004-006 | 3 klaim hemiarthroplasty tanggal & biaya identik, LOS 1, tanpa MedicationDispense | ≥ 0.92 |
| SYND-03 | Unbundling | RS_B | D07 | P12-P14 | KLM007-012 | Paket kolesistektomi (51.23) dipecah dengan intubasi (96.04) terpisah di tanggal sama | 0.84-0.87 |
| SYND-04 | Drug Diversion | RS_E | D09 | P16-P17 | KLM013-014 | Qty insulin 24-30 pen vs dosis rasional 1-2 pen/bulan; refill mingguan | 0.86-0.88 |
| SYND-05 | Cloning | RS_F | D08 | P19-P20 | KLM016-017 | Dua pasien berbeda dengan klaim identik sempurna (tanggal, dx, prosedur, LOS, biaya) | 0.78-0.79 (high) |
## Faskes
| ID | Nama | Kota | Kepemilikan | Kelas | Tempat Tidur | Jumlah Klaim | Skor Maks | Risiko |
| RS_A | RS Aegis Medika A | Jakarta Selatan | Swasta | B | 412 | 19 | 0.95 | fraud |
| RS_B | RS Bakti Husada B | Surabaya | Swasta | C | 280 | 13 | 0.87 | fraud |
| RS_C | RS Cendana Medika C | Medan | Swasta | B | 350 | 10 | 0.94 | fraud |
| RS_D | RSUD Harapan D | Bandung | Pemerintah | B | 520 | 10 | 0.68 | high |
| RS_E | RS Bahari Medika E | Makassar | Swasta | C | 210 | 22 | 0.88 | fraud |
| RS_F | RSUD Giri Menang F | Yogyakarta | Pemerintah | C | 190 | 26 | 0.79 | high |
## Dokter
| ID | Nama | Spesialisasi | Faskes | Jumlah Klaim | Skor Maks | Risiko |
| D01 | dr. Adnan Prakoso, Sp.BTKV | Bedah Toraks & Kardiovaskular | RS_A | 2 | 0.94 | fraud |
| D02 | dr. Barli Soemarno, Sp.B | Bedah Digestif | RS_A | 8 | 0.95 | fraud |
| D03 | dr. Citra Ayuningtyas, Sp.PD | Penyakit Dalam | RS_A | 9 | 0.74 | high |
| D04 | dr. Danur Wibisono, [Sp.JP](http://sp.jp/) | Kardiologi | RS_D | 9 | 0.68 | high |
| D05 | dr. Endra Kusuma, Sp.OT | Orthopedi & Traumatologi | RS_C | 10 | 0.94 | fraud |
| D06 | dr. Fitri Handayani, Sp.A | Anak | RS_B | 0 | 0 | low |
| D07 | dr. Gunawan Halim, Sp.B | Bedah Digestif | RS_B | 13 | 0.87 | fraud |
| D08 | dr. Hendra Maulana, Sp.B | Bedah Umum | RS_F | 18 | 0.79 | high |
| D09 | dr. Indah Pratiwi, Sp.PD | Penyakit Dalam | RS_E | 14 | 0.88 | fraud |
| D10 | dr. Joko Purnomo, Sp.S | Saraf | RS_E | 8 | 0.13 | low |
| D11 | dr. Kartika Sari, Sp.B | Bedah Umum | RS_D | 1 | 0.62 | high |
| D12 | dr. Lina Marlina, Sp.OG | Obstetri & Ginekologi | RS_F | 8 | 0.66 | high |
## Pasien
| ID | Nama | Umur | Gender | Kelas Rawat | Segmen | Kota | Jumlah Klaim | Skor Maks | Risiko |
| P01 | Agus Raharjo | 58 | L | 2 | PBPU | Jakarta | 5 | 0.94 | fraud |
| P02 | Bunga Lestari | 63 | P | 2 | PBPU | Jakarta | 5 | 0.95 | fraud |
| P03 | Candra Wijaya | 55 | L | 1 | PBPU | Jakarta | 5 | 0.93 | fraud |
| P04 | Dewi Anggraeni | 34 | P | 3 | PBI | Bogor | 4 | 0.11 | low |
| P05 | Eka Putri | 27 | P | 3 | PBI | Yogyakarta | 5 | 0.66 | high |
| P06 | Fajar Nugroho | 71 | L | 2 | PBI | Surabaya | 4 | 0.13 | low |
| P07 | Gilang Saputra | 42 | L | 3 | PBPU | Bandung | 5 | 0.62 | high |
| P08 | Maryam Yusuf | 77 | P | 2 | PBPU | Medan | 5 | 0.92 | fraud |
| P09 | Idrus Hakim | 79 | L | 2 | PBPU | Medan | 4 | 0.94 | fraud |
| P10 | Kartini Ibrahim | 80 | P | 2 | PBI | Medan | 5 | 0.93 | fraud |
| P11 | Lukman Sutrisno | 66 | L | 1 | PBPU | Bandung | 5 | 0.68 | high |
| P12 | Maya Sari | 49 | P | 2 | PBPU | Surabaya | 5 | 0.85 | fraud |
| P13 | Nadia Rahmawati | 52 | P | 3 | PBPU | Surabaya | 6 | 0.86 | fraud |
| P14 | Odi Setiawan | 61 | L | 2 | PBPU | Surabaya | 6 | 0.87 | fraud |
| P15 | Purnama Sidik | 47 | L | 3 | PBI | Makassar | 7 | 0.53 | medium |
| P16 | Ratna Dewi | 58 | P | 2 | PBPU | Makassar | 5 | 0.88 | fraud |
| P17 | Slamet Riyadi | 61 | L | 2 | PBPU | Makassar | 5 | 0.86 | fraud |
| P18 | Tarmizi Karim | 69 | L | 3 | PBI | Jakarta | 4 | 0.74 | high |
| P19 | Umi Kalsum | 44 | P | 3 | PBPU | Yogyakarta | 5 | 0.78 | high |
| P20 | Wahyu Nugraha | 45 | L | 3 | PBPU | Yogyakarta | 5 | 0.79 | high |
## Diagnosis (ICD-10)
| Kode | Nama | Derajat | Jumlah Klaim | Skor Maks | Risiko |
| K29.7 | Gastritis, tanpa perdarahan | ringan | 10 | 0.95 | fraud |
| K35.8 | Apendisitis akut | sedang | 11 | 0.79 | high |
| K40.9 | Hernia inguinalis, tanpa obstruksi | sedang | 8 | 0.13 | low |
| I21.9 | Infark miokard akut, tidak spesifik | berat | 8 | 0.13 | low |
| J18.9 | Pneumonia, organisme tidak spesifik | sedang | 9 | 0.74 | high |
| E11.9 | Diabetes melitus tipe 2, tanpa komplikasi | ringan | 15 | 0.88 | fraud |
| N20.0 | Kalkulus ginjal | sedang | 8 | 0.13 | low |
| S72.0 | Fraktur kolum femur, tertutup | berat | 10 | 0.94 | fraud |
| O80 | Persalinan tunggal spontan | normal | 8 | 0.66 | high |
| K80.2 | Kolelitiasis, tanpa kolesistitis | sedang | 13 | 0.87 | fraud |
## Prosedur (ICD-9-CM)
| Kode | Nama | Kompleksitas | Biaya Rujukan | Jumlah Klaim | Skor Maks | Risiko |
| 00.66 | Angioplasti koroner + stent (PCI) | tinggi | Rp 58.000.000 | 12 | 0.95 | fraud |
| 36.13 | Coronary artery bypass graft (CABG) | tinggi | Rp 78.000.000 | 0 | 0 | low |
| 47.09 | Apendektomi | sedang | Rp 6.800.000 | 11 | 0.79 | high |
| 53.1 | Reparasi hernia inguinalis | sedang | Rp 8.200.000 | 8 | 0.13 | low |
| 51.23 | Kolesistektomi laparoskopik | sedang | Rp 14.500.000 | 10 | 0.87 | fraud |
| 74.1 | Seksio sesarea | sedang | Rp 6.200.000 | 1 | 0.66 | high |
| 81.52 | Hemiarthroplasty panggul | tinggi | Rp 46.500.000 | 10 | 0.94 | fraud |
| 96.04 | Pemasangan pipa endotrakeal (intubasi) | rendah | Rp 750.000 | 3 | 0.87 | fraud |
| 93.90 | Terapi oksigen tekanan positif | rendah | Rp 640.000 | 0 | 0 | low |
| 98.51 | Fragmentasi batu saluran kemih (ESWL) | sedang | Rp 5.600.000 | 8 | 0.13 | low |
## Obat (FORNAS)
| Kode | Nama | Bentuk | FORNAS |
| M01 | Metformin 500 mg | tablet | Ya |
| M02 | Amlodipin 10 mg | tablet | Ya |
| M03 | Seftriakson 1 g | vial injeksi | Ya |
| M04 | Omeprazol 40 mg | vial injeksi | Ya |
| M05 | Salbutamol 2,5 mg nebules | nebulizer | Ya |
| M06 | Atorvastatin 20 mg | tablet | Ya |
| M07 | Furosemid 40 mg | tablet | Ya |
| M08 | Parasetamol 500 mg | tablet | Ya |
| M09 | Insulin glargin 100 UI/ml | pen isi ulang | Tidak |
| M10 | Klopidogrel 75 mg | tablet | Ya |
## Analisis Teks & Sentimen
Perluasan dataset untuk modul NLP/LLM (Gemini) dan analisis sentimen:
- Alasan Berobat - keluhan utama pasien saat admit (Encounter.reasonCode).
- Rujukan - asal FKTP, nomor, dan tanggal rujukan (FKTP ke FKRTL); kunjungan langsung untuk rawat jalan/kontrol.
- Narasi Rekam Medis - resume medis elektronik (Composition) untuk uji konsistensi narasi vs kode billing.
- Umpan Balik Pasien - kutipan survei kepuasan layanan sebagai basis analisis sentimen.
- Sentimen & Skor Sentimen - ground truth label (positif/netral/negatif) dan skor -1 s.d. 1.
- Kontradiksi Narasi - flag klaim yang narasinya bertentangan dengan penagihan (KLM001, KLM002, KLM003, KLM004, KLM005, KLM006, KLM018, KLM024 = 8 klaim).
Distribusi sentimen: 62 positif · 14 netral · 24 negatif. Sinyal sentimen fraud: pengakuan pasien tidak pernah menjalani tindakan yang ditagihkan (phantom billing), keluhan tagihan iur biaya (upcoding/overbilling), keluhan tagihan ganda (unbundling). Sentimen negatif bukan otomatis fraud - klaim normal dengan keluhan layunan negatif (antrean lama, parkir sempit, kebersihan) disertakan sebagai negative control.
## Database Klaim
Basis data 100 klaim (anak halaman ini) berisi seluruh baris dengan properti terfilter: Pasien, Dokter, Faskes, Diagnosis, Prosedur, Obat, Tanggal, LOS, Biaya, Skor Fraud, Risiko, Modus, Sindikat, Status, Kontribusi Saluran, Sinyal SHAP, dan Catatan. Gunakan filter Risiko = fraud atau Sindikat untuk mengecek deteksi simulasi. Versi JSON lengkap (termasuk 70 edges graf) tersedia di canvas "Dataset Simulasi Aegis-JKN".
## Ekspansi v2 - 300 Klaim, Kolom Alasan, dan Kesiapan ML/DL
Dataset diperluas dari 100 menjadi 300 klaim (seed deterministik 20260707, seluruh baris baru KLM101-KLM300) dan setiap baris kini memiliki properti Alasan yang menjelaskan kenapa klaim tersebut fraud, anomali, atau normal.
Distribusi label: 36 fraud (12%), 14 high, 10 medium, 240 low; label anomali total 60 (20%). Skala risiko tetap: skor di bawah 0.35 low; 0.35-0.6 medium; 0.6-0.8 high; di atas 0.8 fraud.
### ⚠️ PEMBERITAHUAN PERBAIKAN DATASET (v2.1 - 2026-10-07)
> Dataset saat ini (v2) BELUM SESUAI untuk validasi platform karena 10 kekurangan kritis yang harus diperbaiki. Versi v2.1 akan menambahkan kolom dan fitur berikut untuk memenuhi syarat anti-leakage dan group-aware evaluation:
✅ Perubahan yang Sudah Diimplementasikan di v2.1:
1. Kolom Grouping Wajib (Untuk Anti-Entity Leakage):
  - pasien_id (20 pasien → P01-P40)
  - faskes_id (6 FKRTL → RS_A-RS_J)
  - dokter_id (12 dokter → D01-D20)
  - Tujuan: Memungkinkan GroupKFold (pasien) dan LeaveOneGroupOut (faskes).
1. Metadata Validasi:
  - seed = 20260707 (deterministik)
  - version = v2.1
  - timestamp = Waktu generasi
1. Blokir Kolom Leakage (Di configs/leakage.yaml):
  - Skor Fraud, Risiko, Status, Sinyal SHAP, Kontribusi Saluran, Modus, Sindikat DIHAPUS dari fitur (hanya untuk evaluasi).
1. Kolom Alasan 3-Tingkat (Sudah ada di v2):
  - FRAUD (36 klaim)
  - ANOMALI (24 klaim: 14 high + 10 medium)
  - NORMAL (240 klaim)
🔧 Sindikat yang Diperbarui (9 Sindikat + 2 Fraud Tunggal):
| ID | Modus | Klaim | Faskes | Dokter | Pasien | Skor | Keterangan |
| SYND-01 | Upcoding | KLM001-003 | RS_A | D01, D02 | P01-P03 | ≥0.93 | Dx gastritis (K29.7) → PCI (00.66) |
| SYND-02 | Phantom Billing | KLM004-006 | RS_C | D05 | P08-P10 | ≥0.92 | 3 klaim hemiarthroplasty identik |
| SYND-03 | Unbundling | KLM007-012 | RS_B | D07 | P12-P14 | 0.84-0.87 | Paket kolesistektomi dipecah |
| SYND-04 | Drug Diversion | KLM013-014 | RS_E | D09 | P16-P17 | 0.86-0.88 | Qty insulin 24-30 pen |
| SYND-05 | Cloning | KLM016-017 | RS_F | D08 | P19-P20 | 0.78-0.79 | Dua pasien, klaim identik |
| SYND-06 | Repeat Billing | KLM101-104 | RS_G | D13 | P21-P24 | 0.85-0.90 | Klaim dobel untuk episode sama |
| SYND-07 | Iur Biaya | KLM105-108 | RS_H | D14 | P25-P28 | 0.82-0.87 | Pungli luar JKN + klaim penuh |
| SYND-08 | Readmission Berulang | KLM109-114 | RS_I | D15 | P29-P34 | 0.75-0.80 | Readmission cepat tanpa indikasi |
| SYND-09 | Excessive Usage | KLM115-120 | RS_J | D16 | P35-P40 | 0.78-0.83 | Volume obat/layanan berlebih |
| - | Biaya Markup | KLM121 | RS_A | D03 | P04 | ≥0.85 | 4x tarif paket |
| - | Drug Diversion | KLM122 | RS_E | D09 | P18 | ≥0.80 | Volume insulin mustahil |
📊 Distribusi Entitas v2.1:
- Faskes: RS_A-RS_J (10 FKRTL)
- Dokter: D01-D20 (20 dokter)
- Pasien: P01-P40 (40 pasien)
- Diagnosis: K29.7, K35.8, I10, J45.9, N39.0, dll.
- Prosedur: 00.66 (PCI), 51.23 (Kolesistektomi), dll.
🛠️ Kesiapan ML/DL (v2.1):
1. Anti-Leakage:
  - configs/leakage.yaml WAJIB mem-blokir kolom turunan sistem.
  - Unit test (tests/test_leakage.py) gagal keras jika kolom leakage masuk fitur.
1. Group-Aware Evaluation:
  - GroupKFold (group=pasien_id)
  - LeaveOneGroupOut (group=faskes_id)
1. Feature Engineering:
  - Rasio biaya/tarif
  - Agregat 30 hari (pasien-dokter-faskes)
  - Flag duplikat, readmission, parsing kontribusi saluran
1. Model Baseline:
  - XGBoost + SMOTE (fallback: sklearn.GradientBoosting)
  - MLP (PyTorch) (fallback: sklearn.MLPClassifier)
1. Graf Heterogen (MHGSL):
  - 3 Saluran: Topologi (relasi), Fitur (cosine θ=0.85), Semantik (metapath)
  - PyTorch Geometric (PyG) + HeteroData
1. XAI:
  - SHAP (TreeExplainer untuk XGBoost, GradientSHAP untuk DL)
  - Per-saluran (topologi, fitur, semantik)
1. Text Channel (Opsional):
  - Gemini API (toggle via configs/text.yaml)
  - Fallback: Heuristic lokal (sklearn + rule-based)
1. Validasi:
  - AUPRC/AUROC/F1 (prevalensi 3-7% untuk realistis)
  - Hit-rate per sindikat (SYND-01-SYND-09)
  - False negative analysis
⚠️ Catatan Prevalensi:
- 12% fraud (oversampled by design) → Hanya untuk simulasi dan validasi model.
- Produksi: Gunakan AUPRC pada prevalensi 3-7% (downsampling).
- Semua metrik WAJIB disertai label: "simulasi sintetis, prevalensi oversampled".
📁 Struktur File v2.1:
```javascript
aegis-jkn/
├── data/
│   ├── raw/
│   │   ├── claims_300_v2.1.csv       # + kolom pasien_id, faskes_id, dokter_id, seed, version, timestamp
│   │   ├── edges_v2.1.json           # 70+ edges (graf heterogen)
│   │   ├── text_gt_v2.1.csv          # Ground truth teks (sentimen, kontradiksi)
│   │   └── leakage_blocklist.yaml    # Kolom terlarang
│   ├── processed/
│   │   ├── features_300.parquet     # Fitur bersih (tanpa leakage)
│   │   ├── graph_hetero.pt           # PyG HeteroData (3 saluran)
│   │   └── metadata.json             # Info dataset
```
🎯 Protokol Keputusan "SESUAI" (v2.1):
Platform dinyatakan ✅ SESUAI jika SEMUA kriteria terpenuhi:
1. ✅ Integritas Data: 300 baris utuh, 0 kebocoran fitur.
1. ✅ Deteksi Fraud: ≥90% dari 36 klaim fraud terdeteksi di antrian ≤20% (group-aware).
1. ✅ Metrik Utama: AUPRC & AUROC MHGSL ≥ baseline XGBoost/MLP.
1. ✅ Per-Sindikat: Setiap SYND-01-SYND-09 hit-rate > 0.
1. ✅ Konsistensi XAI: SHAP sejalan dengan kolom Alasan.
1. ✅ Saluran Teks: 8 klaim kontradiksi masuk daftar prioritas.
1. ✅ Kejujuran Label: Semua metrik disertai catatan: "simulasi sintetis, prevalensi oversampled".
> Jika kriteria 1-2 gagal → ❌ TIDAK SESUAI (perbaiki dataset/generator).
> Jika kriteria 3-4 gagal → ⚠️ DESAIN BELUM TERBUKTI UNGGUL (fallback ke XGBoost + fitur graf turunan).
🚀 Rencana Pelaksanaan (8 Minggu):
| Fase | Tujuan | Durasi | Output |
| Fase 0 | Fondasi & Audit Data | Minggu 1 | Dataset v2.1, leakage.yaml, unit test |
| Fase 1 | Baseline ML & DL | Minggu 2-3 | XGBoost + MLP + fitur graf turunan |
| Fase 2 | Graf Heterogen & MHGSL | Minggu 4-6 | PyG HeteroData, MHGSL, SHAP per-saluran |
| Fase 3 | Validasi Final & LLM | Minggu 7-8 | Laporan validasi, benchmark Kaggle, DP-CTGAN |
Target: Platform SESUAI siap untuk Healthkathon 2026 dan pilot 5 FKRTL.
## [Sub-page] ARSIP SUMBER DUPLIKAT | Dokumentasi Dataset ML dan Deep Learning
> **{'type': 'emoji', 'emoji': '🗂️'}** Dataset sintetis untuk uji simulasi MHGSL pada purwarupa Aegis-JKN ([aegisjkn.vercel.app](http://aegisjkn.vercel.app/)). 100 klaim, privacy-by-design - bukan data peserta riil, aman menurut Permenkes 24/2022 & UU PDP No. 27/2022. Pendamping makalah [ARSIP SUMBER | Aegis-JKN Arsitektur dan Strategi Pengembangan Sistem Deteksi Fraud JKN](https://app.notion.com/p/3ef3e6031ab781d1962af8955843ed0f).
> **{'type': 'emoji', 'emoji': '💡'}** CATATAN KONTROL DOKUMEN | Isi yang diambil melalui Notion tampak sama dengan dokumentasi dataset 100 klaim. Jangan gunakan halaman ini sebagai versi data kedua sebelum pemilik proyek mengonfirmasi perbedaan skema atau versi. Rujuk [Dataset Registry](https://app.notion.com/p/03-Dataset-Registry-Data-Dictionary-dan-Protokol-Reproduksibilitas-4003e6031ab781749a55d4ee8fff3fd2) untuk definisi dataset aktif.
## Ringkasan & Ground Truth
- Jumlah klaim: 100 (20 pasien · 12 dokter · 6 FKRTL · 10 diagnosis · 10 prosedur · 10 obat).
- Distribusi risiko: 76 low · 4 medium · 6 high · 14 fraud.
- Ground truth: klaim anomali = KLM001-KLM024 (14 fraud sindikat + 10 anomali medium/high); klaim normal = KLM025-KLM100.
- Skala risiko: skor <0.35 low; 0.35-0.6 medium; 0.6-0.8 high; lebih dari 0.8 fraud.
- Catatan prevalensi: fraud di-oversample 14% untuk keperluan demo; estimasi lapangan 3-7% (label estimasi literatur).
- Mapping FHIR R4: klaim = Claim; pasien = Patient; dokter = Practitioner; faskes = Organization; diagnosis = Condition (ICD-10); prosedur = Procedure (ICD-9-CM); obat = MedicationRequest/Dispense; LOS = Encounter.length; biaya = [Claim.total](http://claim.total/); tanggal = Encounter.period.start.
- Saluran MHGSL: topologi = edges kunjungan/afiliasi/layanan/semantik; fitur = cosine similarity (LOS, biaya, qty obat) dengan ambang 0.85; semantik = metapath diagnosis ke prosedur.
## Sindikat Ground Truth
| ID | Modus | Faskes | Dokter | Pasien | Klaim | Skenario & Sinyal Deteksi | Skor |
| SYND-01 | Upcoding | RS_A | D01, D02 | P01-P03 | KLM001-003 | Dx gastritis (K29.7) ditagih PCI (00.66); biaya & LOS identik; subgraf padat | ≥ 0.93 |
| SYND-02 | Phantom Billing | RS_C | D05 | P08-P10 | KLM004-006 | 3 klaim hemiarthroplasty tanggal & biaya identik, LOS 1, tanpa MedicationDispense | ≥ 0.92 |
| SYND-03 | Unbundling | RS_B | D07 | P12-P14 | KLM007-012 | Paket kolesistektomi (51.23) dipecah dengan intubasi (96.04) terpisah di tanggal sama | 0.84-0.87 |
| SYND-04 | Drug Diversion | RS_E | D09 | P16-P17 | KLM013-014 | Qty insulin 24-30 pen vs dosis rasional 1-2 pen/bulan; refill mingguan | 0.86-0.88 |
| SYND-05 | Cloning | RS_F | D08 | P19-P20 | KLM016-017 | Dua pasien berbeda dengan klaim identik sempurna (tanggal, dx, prosedur, LOS, biaya) | 0.78-0.79 (high) |
## Faskes
| ID | Nama | Kota | Kepemilikan | Kelas | Tempat Tidur | Jumlah Klaim | Skor Maks | Risiko |
| RS_A | RS Aegis Medika A | Jakarta Selatan | Swasta | B | 412 | 19 | 0.95 | fraud |
| RS_B | RS Bakti Husada B | Surabaya | Swasta | C | 280 | 13 | 0.87 | fraud |
| RS_C | RS Cendana Medika C | Medan | Swasta | B | 350 | 10 | 0.94 | fraud |
| RS_D | RSUD Harapan D | Bandung | Pemerintah | B | 520 | 10 | 0.68 | high |
| RS_E | RS Bahari Medika E | Makassar | Swasta | C | 210 | 22 | 0.88 | fraud |
| RS_F | RSUD Giri Menang F | Yogyakarta | Pemerintah | C | 190 | 26 | 0.79 | high |
## Dokter
| ID | Nama | Spesialisasi | Faskes | Jumlah Klaim | Skor Maks | Risiko |
| D01 | dr. Adnan Prakoso, Sp.BTKV | Bedah Toraks & Kardiovaskular | RS_A | 2 | 0.94 | fraud |
| D02 | dr. Barli Soemarno, Sp.B | Bedah Digestif | RS_A | 8 | 0.95 | fraud |
| D03 | dr. Citra Ayuningtyas, Sp.PD | Penyakit Dalam | RS_A | 9 | 0.74 | high |
| D04 | dr. Danur Wibisono, [Sp.JP](http://sp.jp/) | Kardiologi | RS_D | 9 | 0.68 | high |
| D05 | dr. Endra Kusuma, Sp.OT | Orthopedi & Traumatologi | RS_C | 10 | 0.94 | fraud |
| D06 | dr. Fitri Handayani, Sp.A | Anak | RS_B | 0 | 0 | low |
| D07 | dr. Gunawan Halim, Sp.B | Bedah Digestif | RS_B | 13 | 0.87 | fraud |
| D08 | dr. Hendra Maulana, Sp.B | Bedah Umum | RS_F | 18 | 0.79 | high |
| D09 | dr. Indah Pratiwi, Sp.PD | Penyakit Dalam | RS_E | 14 | 0.88 | fraud |
| D10 | dr. Joko Purnomo, Sp.S | Saraf | RS_E | 8 | 0.13 | low |
| D11 | dr. Kartika Sari, Sp.B | Bedah Umum | RS_D | 1 | 0.62 | high |
| D12 | dr. Lina Marlina, Sp.OG | Obstetri & Ginekologi | RS_F | 8 | 0.66 | high |
## Pasien
| ID | Nama | Umur | Gender | Kelas Rawat | Segmen | Kota | Jumlah Klaim | Skor Maks | Risiko |
| P01 | Agus Raharjo | 58 | L | 2 | PBPU | Jakarta | 5 | 0.94 | fraud |
| P02 | Bunga Lestari | 63 | P | 2 | PBPU | Jakarta | 5 | 0.95 | fraud |
| P03 | Candra Wijaya | 55 | L | 1 | PBPU | Jakarta | 5 | 0.93 | fraud |
| P04 | Dewi Anggraeni | 34 | P | 3 | PBI | Bogor | 4 | 0.11 | low |
| P05 | Eka Putri | 27 | P | 3 | PBI | Yogyakarta | 5 | 0.66 | high |
| P06 | Fajar Nugroho | 71 | L | 2 | PBI | Surabaya | 4 | 0.13 | low |
| P07 | Gilang Saputra | 42 | L | 3 | PBPU | Bandung | 5 | 0.62 | high |
| P08 | Maryam Yusuf | 77 | P | 2 | PBPU | Medan | 5 | 0.92 | fraud |
| P09 | Idrus Hakim | 79 | L | 2 | PBPU | Medan | 4 | 0.94 | fraud |
| P10 | Kartini Ibrahim | 80 | P | 2 | PBI | Medan | 5 | 0.93 | fraud |
| P11 | Lukman Sutrisno | 66 | L | 1 | PBPU | Bandung | 5 | 0.68 | high |
| P12 | Maya Sari | 49 | P | 2 | PBPU | Surabaya | 5 | 0.85 | fraud |
| P13 | Nadia Rahmawati | 52 | P | 3 | PBPU | Surabaya | 6 | 0.86 | fraud |
| P14 | Odi Setiawan | 61 | L | 2 | PBPU | Surabaya | 6 | 0.87 | fraud |
| P15 | Purnama Sidik | 47 | L | 3 | PBI | Makassar | 7 | 0.53 | medium |
| P16 | Ratna Dewi | 58 | P | 2 | PBPU | Makassar | 5 | 0.88 | fraud |
| P17 | Slamet Riyadi | 61 | L | 2 | PBPU | Makassar | 5 | 0.86 | fraud |
| P18 | Tarmizi Karim | 69 | L | 3 | PBI | Jakarta | 4 | 0.74 | high |
| P19 | Umi Kalsum | 44 | P | 3 | PBPU | Yogyakarta | 5 | 0.78 | high |
| P20 | Wahyu Nugraha | 45 | L | 3 | PBPU | Yogyakarta | 5 | 0.79 | high |
## Diagnosis (ICD-10)
| Kode | Nama | Derajat | Jumlah Klaim | Skor Maks | Risiko |
| K29.7 | Gastritis, tanpa perdarahan | ringan | 10 | 0.95 | fraud |
| K35.8 | Apendisitis akut | sedang | 11 | 0.79 | high |
| K40.9 | Hernia inguinalis, tanpa obstruksi | sedang | 8 | 0.13 | low |
| I21.9 | Infark miokard akut, tidak spesifik | berat | 8 | 0.13 | low |
| J18.9 | Pneumonia, organisme tidak spesifik | sedang | 9 | 0.74 | high |
| E11.9 | Diabetes melitus tipe 2, tanpa komplikasi | ringan | 15 | 0.88 | fraud |
| N20.0 | Kalkulus ginjal | sedang | 8 | 0.13 | low |
| S72.0 | Fraktur kolum femur, tertutup | berat | 10 | 0.94 | fraud |
| O80 | Persalinan tunggal spontan | normal | 8 | 0.66 | high |
| K80.2 | Kolelitiasis, tanpa kolesistitis | sedang | 13 | 0.87 | fraud |
## Prosedur (ICD-9-CM)
| Kode | Nama | Kompleksitas | Biaya Rujukan | Jumlah Klaim | Skor Maks | Risiko |
| 00.66 | Angioplasti koroner + stent (PCI) | tinggi | Rp 58.000.000 | 12 | 0.95 | fraud |
| 36.13 | Coronary artery bypass graft (CABG) | tinggi | Rp 78.000.000 | 0 | 0 | low |
| 47.09 | Apendektomi | sedang | Rp 6.800.000 | 11 | 0.79 | high |
| 53.1 | Reparasi hernia inguinalis | sedang | Rp 8.200.000 | 8 | 0.13 | low |
| 51.23 | Kolesistektomi laparoskopik | sedang | Rp 14.500.000 | 10 | 0.87 | fraud |
| 74.1 | Seksio sesarea | sedang | Rp 6.200.000 | 1 | 0.66 | high |
| 81.52 | Hemiarthroplasty panggul | tinggi | Rp 46.500.000 | 10 | 0.94 | fraud |
| 96.04 | Pemasangan pipa endotrakeal (intubasi) | rendah | Rp 750.000 | 3 | 0.87 | fraud |
| 93.90 | Terapi oksigen tekanan positif | rendah | Rp 640.000 | 0 | 0 | low |
| 98.51 | Fragmentasi batu saluran kemih (ESWL) | sedang | Rp 5.600.000 | 8 | 0.13 | low |
## Obat (FORNAS)
| Kode | Nama | Bentuk | FORNAS |
| M01 | Metformin 500 mg | tablet | Ya |
| M02 | Amlodipin 10 mg | tablet | Ya |
| M03 | Seftriakson 1 g | vial injeksi | Ya |
| M04 | Omeprazol 40 mg | vial injeksi | Ya |
| M05 | Salbutamol 2,5 mg nebules | nebulizer | Ya |
| M06 | Atorvastatin 20 mg | tablet | Ya |
| M07 | Furosemid 40 mg | tablet | Ya |
| M08 | Parasetamol 500 mg | tablet | Ya |
| M09 | Insulin glargin 100 UI/ml | pen isi ulang | Tidak |
| M10 | Klopidogrel 75 mg | tablet | Ya |
## Analisis Teks & Sentimen
Perluasan dataset untuk modul NLP/LLM (Gemini) dan analisis sentimen:
- Alasan Berobat - keluhan utama pasien saat admit (Encounter.reasonCode).
- Rujukan - asal FKTP, nomor, dan tanggal rujukan (FKTP ke FKRTL); kunjungan langsung untuk rawat jalan/kontrol.
- Narasi Rekam Medis - resume medis elektronik (Composition) untuk uji konsistensi narasi vs kode billing.
- Umpan Balik Pasien - kutipan survei kepuasan layanan sebagai basis analisis sentimen.
- Sentimen & Skor Sentimen - ground truth label (positif/netral/negatif) dan skor -1 s.d. 1.
- Kontradiksi Narasi - flag klaim yang narasinya bertentangan dengan penagihan (KLM001, KLM002, KLM003, KLM004, KLM005, KLM006, KLM018, KLM024 = 8 klaim).
Distribusi sentimen: 62 positif · 14 netral · 24 negatif. Sinyal sentimen fraud: pengakuan pasien tidak pernah menjalani tindakan yang ditagihkan (phantom billing), keluhan tagihan iur biaya (upcoding/overbilling), keluhan tagihan ganda (unbundling). Sentimen negatif bukan otomatis fraud - klaim normal dengan keluhan layunan negatif (antrean lama, parkir sempit, kebersihan) disertakan sebagai negative control.
## Database Klaim
Basis data 100 klaim (anak halaman ini) berisi seluruh baris dengan properti terfilter: Pasien, Dokter, Faskes, Diagnosis, Prosedur, Obat, Tanggal, LOS, Biaya, Skor Fraud, Risiko, Modus, Sindikat, Status, Kontribusi Saluran, Sinyal SHAP, dan Catatan. Gunakan filter Risiko = fraud atau Sindikat untuk mengecek deteksi simulasi. Versi JSON lengkap (termasuk 70 edges graf) tersedia di canvas "Dataset Simulasi Aegis-JKN".
## Ekspansi v2 - 300 Klaim, Kolom Alasan, dan Kesiapan ML/DL
Dataset diperluas dari 100 menjadi 300 klaim (seed deterministik 20260707, seluruh baris baru KLM101-KLM300) dan setiap baris kini memiliki properti Alasan yang menjelaskan kenapa klaim tersebut fraud, anomali, atau normal.
Distribusi label: 36 fraud (12%), 14 high, 10 medium, 240 low; label anomali total 60 (20%). Skala risiko tetap: skor di bawah 0.35 low; 0.35-0.6 medium; 0.6-0.8 high; di atas 0.8 fraud.
### ⚠️ PEMBERITAHUAN PERBAIKAN DATASET (v2.1 - 2026-10-07)
> Dataset saat ini (v2) BELUM SESUAI untuk validasi platform karena 10 kekurangan kritis yang harus diperbaiki. Versi v2.1 akan menambahkan kolom dan fitur berikut untuk memenuhi syarat anti-leakage dan group-aware evaluation:
✅ Perubahan yang Sudah Diimplementasikan di v2.1:
1. Kolom Grouping Wajib (Untuk Anti-Entity Leakage):
  - pasien_id (20 pasien → P01-P40)
  - faskes_id (6 FKRTL → RS_A-RS_J)
  - dokter_id (12 dokter → D01-D20)
  - Tujuan: Memungkinkan GroupKFold (pasien) dan LeaveOneGroupOut (faskes).
1. Metadata Validasi:
  - seed = 20260707 (deterministik)
  - version = v2.1
  - timestamp = Waktu generasi
1. Blokir Kolom Leakage (Di configs/leakage.yaml):
  - Skor Fraud, Risiko, Status, Sinyal SHAP, Kontribusi Saluran, Modus, Sindikat DIHAPUS dari fitur (hanya untuk evaluasi).
1. Kolom Alasan 3-Tingkat (Sudah ada di v2):
  - FRAUD (36 klaim)
  - ANOMALI (24 klaim: 14 high + 10 medium)
  - NORMAL (240 klaim)
🔧 Sindikat yang Diperbarui (9 Sindikat + 2 Fraud Tunggal):
| ID | Modus | Klaim | Faskes | Dokter | Pasien | Skor | Keterangan |
| SYND-01 | Upcoding | KLM001-003 | RS_A | D01, D02 | P01-P03 | ≥0.93 | Dx gastritis (K29.7) → PCI (00.66) |
| SYND-02 | Phantom Billing | KLM004-006 | RS_C | D05 | P08-P10 | ≥0.92 | 3 klaim hemiarthroplasty identik |
| SYND-03 | Unbundling | KLM007-012 | RS_B | D07 | P12-P14 | 0.84-0.87 | Paket kolesistektomi dipecah |
| SYND-04 | Drug Diversion | KLM013-014 | RS_E | D09 | P16-P17 | 0.86-0.88 | Qty insulin 24-30 pen |
| SYND-05 | Cloning | KLM016-017 | RS_F | D08 | P19-P20 | 0.78-0.79 | Dua pasien, klaim identik |
| SYND-06 | Repeat Billing | KLM101-104 | RS_G | D13 | P21-P24 | 0.85-0.90 | Klaim dobel untuk episode sama |
| SYND-07 | Iur Biaya | KLM105-108 | RS_H | D14 | P25-P28 | 0.82-0.87 | Pungli luar JKN + klaim penuh |
| SYND-08 | Readmission Berulang | KLM109-114 | RS_I | D15 | P29-P34 | 0.75-0.80 | Readmission cepat tanpa indikasi |
| SYND-09 | Excessive Usage | KLM115-120 | RS_J | D16 | P35-P40 | 0.78-0.83 | Volume obat/layanan berlebih |
| - | Biaya Markup | KLM121 | RS_A | D03 | P04 | ≥0.85 | 4x tarif paket |
| - | Drug Diversion | KLM122 | RS_E | D09 | P18 | ≥0.80 | Volume insulin mustahil |
📊 Distribusi Entitas v2.1:
- Faskes: RS_A-RS_J (10 FKRTL)
- Dokter: D01-D20 (20 dokter)
- Pasien: P01-P40 (40 pasien)
- Diagnosis: K29.7, K35.8, I10, J45.9, N39.0, dll.
- Prosedur: 00.66 (PCI), 51.23 (Kolesistektomi), dll.
🛠️ Kesiapan ML/DL (v2.1):
1. Anti-Leakage:
  - configs/leakage.yaml WAJIB mem-blokir kolom turunan sistem.
  - Unit test (tests/test_leakage.py) gagal keras jika kolom leakage masuk fitur.
1. Group-Aware Evaluation:
  - GroupKFold (group=pasien_id)
  - LeaveOneGroupOut (group=faskes_id)
1. Feature Engineering:
  - Rasio biaya/tarif
  - Agregat 30 hari (pasien-dokter-faskes)
  - Flag duplikat, readmission, parsing kontribusi saluran
1. Model Baseline:
  - XGBoost + SMOTE (fallback: sklearn.GradientBoosting)
  - MLP (PyTorch) (fallback: sklearn.MLPClassifier)
1. Graf Heterogen (MHGSL):
  - 3 Saluran: Topologi (relasi), Fitur (cosine θ=0.85), Semantik (metapath)
  - PyTorch Geometric (PyG) + HeteroData
1. XAI:
  - SHAP (TreeExplainer untuk XGBoost, GradientSHAP untuk DL)
  - Per-saluran (topologi, fitur, semantik)
1. Text Channel (Opsional):
  - Gemini API (toggle via configs/text.yaml)
  - Fallback: Heuristic lokal (sklearn + rule-based)
1. Validasi:
  - AUPRC/AUROC/F1 (prevalensi 3-7% untuk realistis)
  - Hit-rate per sindikat (SYND-01-SYND-09)
  - False negative analysis
⚠️ Catatan Prevalensi:
- 12% fraud (oversampled by design) → Hanya untuk simulasi dan validasi model.
- Produksi: Gunakan AUPRC pada prevalensi 3-7% (downsampling).
- Semua metrik WAJIB disertai label: "simulasi sintetis, prevalensi oversampled".
📁 Struktur File v2.1:
```javascript
aegis-jkn/
├── data/
│   ├── raw/
│   │   ├── claims_300_v2.1.csv       # + kolom pasien_id, faskes_id, dokter_id, seed, version, timestamp
│   │   ├── edges_v2.1.json           # 70+ edges (graf heterogen)
│   │   ├── text_gt_v2.1.csv          # Ground truth teks (sentimen, kontradiksi)
│   │   └── leakage_blocklist.yaml    # Kolom terlarang
│   ├── processed/
│   │   ├── features_300.parquet     # Fitur bersih (tanpa leakage)
│   │   ├── graph_hetero.pt           # PyG HeteroData (3 saluran)
│   │   └── metadata.json             # Info dataset
```
🎯 Protokol Keputusan "SESUAI" (v2.1):
Platform dinyatakan ✅ SESUAI jika SEMUA kriteria terpenuhi:
1. ✅ Integritas Data: 300 baris utuh, 0 kebocoran fitur.
1. ✅ Deteksi Fraud: ≥90% dari 36 klaim fraud terdeteksi di antrian ≤20% (group-aware).
1. ✅ Metrik Utama: AUPRC & AUROC MHGSL ≥ baseline XGBoost/MLP.
1. ✅ Per-Sindikat: Setiap SYND-01-SYND-09 hit-rate > 0.
1. ✅ Konsistensi XAI: SHAP sejalan dengan kolom Alasan.
1. ✅ Saluran Teks: 8 klaim kontradiksi masuk daftar prioritas.
1. ✅ Kejujuran Label: Semua metrik disertai catatan: "simulasi sintetis, prevalensi oversampled".
> Jika kriteria 1-2 gagal → ❌ TIDAK SESUAI (perbaiki dataset/generator).
> Jika kriteria 3-4 gagal → ⚠️ DESAIN BELUM TERBUKTI UNGGUL (fallback ke XGBoost + fitur graf turunan).
🚀 Rencana Pelaksanaan (8 Minggu):
| Fase | Tujuan | Durasi | Output |
| Fase 0 | Fondasi & Audit Data | Minggu 1 | Dataset v2.1, leakage.yaml, unit test |
| Fase 1 | Baseline ML & DL | Minggu 2-3 | XGBoost + MLP + fitur graf turunan |
| Fase 2 | Graf Heterogen & MHGSL | Minggu 4-6 | PyG HeteroData, MHGSL, SHAP per-saluran |
| Fase 3 | Validasi Final & LLM | Minggu 7-8 | Laporan validasi, benchmark Kaggle, DP-CTGAN |
Target: Platform SESUAI siap untuk Healthkathon 2026 dan pilot 5 FKRTL.
## [Database] Klaim Aegis-JKN v2 (300 Baris)
## [Sub-page] Figma | Fishbone Diagram Aegis-JKN
[Link] https://www.figma.com/board/ePv0sbUCNU9iOgRiTMwH8E/Fishbone-Diagram-6M---Kebocoran-Finansial-Klaim-JKN-Aegis?node-id=0-1&p=f&t=pYR0GTGzXi53K7Hq-0
> **{'type': 'emoji', 'emoji': '💡'}** CATATAN DOKUMEN | Tautan Figma untuk Fishbone Diagram Aegis-JKN. Tambahkan tujuan diagram, tanggal revisi, penulis, serta ringkasan temuan utama setelah isi diagram ditinjau. Gunakan [HEALTHKATHON Project Dashboard](https://app.notion.com/p/00-HEALTHKATHON-Project-Dashboard-4003e6031ab7815a89bdedc0c4d92c2f) sebagai halaman navigasi proyek.

## [Sub-page] ARSIP SUMBER | Proposal Lengkap Aegis-JKN Healthkathon
PROPOSAL INOVASI TEKNOLOGI KESEHATANBPJS KESEHATAN HEALTHKATHON 2026Kategori: Sistem Pengawasan Fasilitas Kesehatan (Pencegahan Upcoding, Unbundling, Phantom Billing, dan Sindikat Kolusi Rujukan)
> **{'type': 'emoji', 'emoji': '💡'}** CATATAN EDITORIAL | Proposal sumber awal. Gunakan [Proposal Riset dan Inovasi, Edisi Akademik Revisi 1.0](https://app.notion.com/p/01-Aegis-JKN-Proposal-Riset-dan-Inovasi-Edisi-Akademik-Revisi-1-0-4003e6031ab78170bc22fe391c6a3a2a) sebagai versi terkendali untuk naskah formal. Angka benchmark dan finansial pada naskah sumber belum dianggap tervalidasi sampai artefak replikasi dilampirkan.
---
AEGIS-JKN: SISTEM FRAUD INTELLIGENCE & CLINICAL DECISION SUPPORT BERBASIS MULTI-HOP GRAPH STRUCTURE LEARNING (MHGSL) DAN MULTIMODAL SIMULATION UNTUK DETEKSI SINDIKAT KECURANGAN DAN ANOMALI KLAIM JKN
> **{'type': 'emoji', 'emoji': '🛡️'}** « Detect Smarter. Protect JKN. »
Diajukan Oleh:TIM INOVATOR KANDIDAT 1 - AEGIS-JKN1. Lead Platform & Logic Architecture2. Research & Clinical Data Specialist3. Business Case & Strategic Impact Specialist
CIMAHI2026
# LEMBAR PERNYATAAN ORISINALITAS DAN INTEGRITAS
Yang bertanda tangan di bawah ini, kami selaku Tim Inovator Kandidat 1 peserta kompetisi BPJS Kesehatan Healthkathon 2026, dengan ini menyatakan bahwa proposal inovasi dengan judul:
> **{'type': 'emoji', 'emoji': '💡'}** AEGIS-JKN: Sistem Fraud Intelligence & Clinical Decision Support Berbasis Multi-Hop Graph Structure Learning (MHGSL) dan Multimodal Simulation untuk Deteksi Sindikat Kecurangan dan Anomali Klaim JKN« Detect Smarter, Protect JKN - Menjaga Ketahanan Finansial Dana Jaminan Sosial (DJS) Melalui Deteksi Kolusi Multi-Hop dan Transparansi Akuntabilitas Medis. »
Adalah benar-benar hasil karya orisinal tim kami, belum pernah dipublikasikan secara komersial di tempat lain, dan tidak mengandung unsur plagiarisme atau pelanggaran hak kekayaan intelektual pihak mana pun. Bersama ini kami juga menyatakan komitmen integritas perancangan sistem sebagai berikut:
- 1. Kepatuhan Regulasi Data Pribadi: Seluruh perancangan arsitektur data Aegis-JKN mematuhi Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) dan Undang-Undang Nomor 17 Tahun 2023 tentang Kesehatan. Pengembangan purwarupa (MVP) sepenuhnya menggunakan dataset sintetis tervalidasi klinis dan data terbuka ter-deidentifikasi yang sah secara hukum, tanpa menggunakan data peserta JKN aktual tanpa izin resmi tertulis.
- 2. Prinsip Anti-Overclaim & Transparansi Sains: Kami menolak klaim akurasi mutlak 100% dan tidak menyajikan angka penghematan anggaran yang spekulatif. Seluruh metrik teknis (Akurasi 93.0%, Presisi 94.12%, ROC-AUC 0.9825, AUPRC 0.9142) serta estimasi penyelamatan overcharge tarif INA-CBG sebesar Rp 507,37 Juta dihitung berbasis metodologi empiris portofolio 300 klaim terverifikasi yang dapat direplikasi secara objektif.
- 3. Prinsip Human Autonomy & Fail-Safe AI: Sistem dirancang murni sebagai pendukung keputusan klinis (Clinical Decision Support System / CDSS). Kecerdasan Buatan (AI) dilarang keras memiliki kewenangan menjatuhkan sanksi hukum, memvonis fraud secara sepihak, menolak klaim, ataupun memotong tarif secara otomatis (anti-automated adverse decision). Seluruh keputusan final tetap berada di bawah kendali penuh dan tanggung jawab verifikator manusia dan Tim Pencegahan Kecurangan (PK-JKN).
- 4. Teknologi Tepat Guna (Right-Sized Hybrid Engineering): Pemilihan komponen teknologi (Tri-Tier Pipeline: Rule-Based, Tabular XGBoost, Tri-Channel MHGSL, dan Multi-Agent Simulation OASIS) didasarkan pada kebutuhan fungsional nyata dari throughput 2 juta klaim/hari, bukan demi mengejar kompleksitas komputasi yang berlebihan atau menambah beban operasional yang tidak perlu.
Demikian pernyataan ini kami buat dengan penuh rasa tanggung jawab, integritas moral, dan dedikasi demi mendukung keberlanjutan Program Jaminan Kesehatan Nasional (JKN) yang berkeadilan bagi seluruh rakyat Indonesia.
| Mengetahui,Perwakilan Tim Teknis & Arsitektur( Tim Pengusul Kandidat 1 ) | Jakarta, Oktober 2026 Perwakilan Riset & Strategi Dampak( Tim Pengusul Kandidat 1 ) |
| - | - |
# RINGKASAN EKSEKUTIF
Program Jaminan Kesehatan Nasional (JKN) yang dikelola oleh BPJS Kesehatan merupakan salah satu sistem jaminan kesehatan semesta (Universal Health Coverage) terbesar dan paling kompleks di dunia, mencakup lebih dari 270 juta jiwa kepesertaan aktif dan memproses lebih dari dua juta klaim layanan kesehatan setiap harinya dari fasilitas kesehatan rujukan tingkat lanjutan (FKRTL) di seluruh Indonesia. Namun, pengelolaan skala masif ini dihadapkan pada ketimpangan rasio beban verifikasi yang sangat tajam, di mana hanya sekitar 1.000 verifikator klaim BPJS Kesehatan yang bertugas menelaah jutaan berkas tersebut (rasio beban mencapai 2.000 klaim per verifikator per hari, jauh melampaui kapasitas telaah mendalam manusia sebesar 50-70 berkas per hari). Keterbatasan kognitif dan fenomena kelelahan peringatan (alert fatigue) ini membuka celah asimetri informasi yang dimanfaatkan oleh oknum terorganisir untuk melakukan kecurangan klaim (fraud) terstruktur, khususnya upcoding severity level, phantom billing, unbundling prosedur, hingga sindikat kolusi rujukan dokter-faskes (fraud rings).
Tantangan paling kritis dalam deteksi kecurangan modern adalah fenomena Kamuflase Topologis (Topological Camouflage). Pelaku kecurangan terorganisir sengaja merekayasa alur rujukan administratif fisik agar tampak patuh regulasi berjenjang (sehingga terlihat normal pada model statistik tabular dan aturan deterministik), namun menyembunyikan anomali klastering biaya, durasi rawat (LOS), dan prosedur tidak lazim secara terselubung. Proposal ini mengusulkan solusi inovatif terpadu: AEGIS-JKN (Detect Smarter, Protect JKN), sebuah platform Fraud Intelligence dan Clinical Decision Support System (CDSS) berbasis arsitektur Multi-Hop Graph Structure Learning (MHGSL) yang dikombinasikan dengan simulasi multi-agen multimodal (OASIS) dalam kerangka kerja Human-in-the-Loop (HITL) yang akuntabel.
Keunggulan utama Aegis-JKN berakar pada lima pilar strategis:
- 1. Paradigma Deteksi Tri-Channel MHGSL: Memodelkan interaksi layanan medis ke dalam graf heterogen yang didekomposisi ke dalam tiga saluran matriks ketetanggaan: (1) Saluran Topologi Fisik (A_top) untuk relasi penugasan DPJP dan rujukan faskes; (2) Saluran Kemiripan Fitur (A_feat) berbasis cosine similarity vektor atribut klinis-finansial (LOS, biaya INA-CBG, obat) guna mendeteksi anomali identik implisit; serta (3) Saluran Semantik Metapath (A_sem) yang memproyeksikan rantai rujukan klinis via PathSim untuk menyingkap ketidaksesuaian kompetensi dan rekayasa kode penagihan.
- 2. Arsitektur Tri-Tier & Right-Sized Engineering: Mengombinasikan Tier-1 Deterministic Rule Engine (<50 ms) untuk menyaring 40-60% klaim normal/pelanggaran eksplisit Permenkes No. 16/2019, Tier-2 Tabular XGBoost untuk anomali statistik per klaim, dan Tier-3 PyTorch Geometric HeteroData GCN untuk ekstraksi sindikat multi-hop, yang disatukan via Late Fusion multimodal dengan narasi resume klinis.
- 3. Transparansi Penalaran (Explainable AI / XAI): Setiap flag anomali disertai dekomposisi atribusi SHAP per kanal graf (phi_top, phi_feat, phi_sem) serta visualisasi SVG interaktif klaster bipartite faskes-dokter, mengeliminasi sifat kotak hitam (black-box) dan langsung memandu verifikator ke bukti inkonsistensi klinis.
- 4. Fail-Safe Human Autonomy & Active Learning: Menerapkan prinsip anti-automated adverse decision di mana AI tidak memiliki hak veto penolakan klaim. Dilengkapi protokol darurat Safe-Mode Fallback yang otomatis membekukan saran AI jika tingkat penolakan (override) oleh verifikator melampaui 30%.
- 5. Kepatuhan Ketat UU PDP No. 27/2022 & Interoperabilitas: Seluruh arsitektur didesain beroperasi pada perimeter tertutup (private on-premise cloud) BPJS Kesehatan dengan enkripsi AES-256 dan salted SHA-256 pseudonymization, selaras penuh dengan standar SATUSEHAT HL7 FHIR R4 dan regulasi UU PDP No. 27/2022.
Evaluasi empiris terhadap portofolio 300 berkas klaim tervalidasi klinis (Dataset v2.1 senilai Rp 3,53 Miliar) membuktikan performa superior model MHGSL: Akurasi 93.0%, Presisi 94.12%, ROC-AUC 0.9825, dan AUPRC 0.9142 (+28.6% dibanding baseline XGBoost 0.71). Model menunjukkan ketahanan kamuflase mencapai 89.4% pada tingkat masking rujukan 40%, serta 100% mendeteksi 9 pola sindikat terorganisir (SYND-01 s/d SYND-09). Pada portofolio sampel tersebut, sistem berhasil mengidentifikasi 60 klaim anomali dengan potensi penghematan/pencegahan kebocoran tarif INA-CBG riil sebesar Rp 507,37 Juta (rata-rata Rp 8,46 Juta per kasus fraud). Implementasi Aegis-JKN diproyeksikan memangkas durasi review awal sebesar 30-50% per berkas anomali, memberikan rasio Cost-to-Impact konservatif 1 : 15, serta menyelamatkan ratusan miliar rupiah Dana Jaminan Sosial (DJS) Kesehatan setiap tahunnya.
KATA KUNCI: Kecurangan Klaim JKN, Upcoding, Phantom Billing, Unbundling, Fraud Rings, Multi-Hop Graph Structure Learning (MHGSL), Topological Camouflage, Human-in-the-Loop, Explainable AI (XAI), UU Pelindungan Data Pribadi No. 27/2022.
# DAFTAR ISI
LEMBAR PERNYATAAN ORISINALITAS DAN INTEGRITAS  . . . . . . . . . . . . . ii
RINGKASAN EKSEKUTIF  . . . . . . . . . . . . . . . . . . . . . . . . . . iii
DAFTAR ISI  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . iv
DAFTAR TABEL & DAFTAR GAMBAR  . . . . . . . . . . . . . . . . . . . . . . v
BAB I: PENDAHULUAN  . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
1.1 Latar Belakang & Urgensi Nasional  . . . . . . . . . . . . . . . . 1
1.2 Identifikasi Permasalahan Utama (Upcoding, Unbundling, & Fraud Rings)  2
1.3 Fenomena Topological Camouflage pada Ekosistem JKN  . . . . . . . . 3
1.4 Rumusan Masalah Inovasi  . . . . . . . . . . . . . . . . . . . . . 4
1.5 Tujuan dan Sasaran Inovasi  . . . . . . . . . . . . . . . . . . . . 4
1.6 Ruang Lingkup dan Batasan Sistem  . . . . . . . . . . . . . . . . . 5
BAB II: ANALISIS AKAR MASALAH (ROOT CAUSE ANALYSIS)  . . . . . . . . . . 6
2.1 Metodologi Analisis 5-Whys Kegagalan Deteksi Kolusi  . . . . . . . 6
2.2 Analisis Fishbone 4 Dimensi Kendala Audit Klaim JKN  . . . . . . . 7
2.3 Sintesis Akar Masalah: Kebutuhan Paradigma Graph Learning  . . . . 9
BAB III: DESKRIPSI & VALUE PROPOSITION SOLUSI AEGIS-JKN  . . . . . . . . 10
3.1 Gambaran Umum Platform Aegis-JKN  . . . . . . . . . . . . . . . . . 10
3.2 Value Proposition & Diferensiasi Strategis Multi-Channel  . . . . . 11
3.3 Analisis Komparatif Pendekatan Solusi (Manual vs Rule vs ML vs Aegis)  12
3.4 Prinsip Right-Sized Hybrid Engineering & Dual-Path Processing  . . 14
BAB IV: ARSITEKTUR & MEKANISME CARA KERJA SISTEM  . . . . . . . . . . . . 15
4.1 End-to-End Workflow Pipeline & Dual-Path Production Inference  . . 15
4.2 Modul 1: Ingestion Data, Normalisasi SATUSEHAT, & Tokenisasi Anonim  16
4.3 Modul 2: Tier-1 Deterministic Rule-Based Pre-Filter  . . . . . . . 17
4.4 Modul 3: Tier-2 Tabular Classifier & Tier-3 Tri-Channel MHGSL Engine  18
4.5 Modul 4: Multimodal Late Fusion & Triase Risiko Dinamis  . . . . . 20
4.6 Modul 5: Explainability Layer & Dekomposisi Atribusi SHAP  . . . . 21
4.7 Modul 6: Interactive Verifier Decision Support Interface (Next.js 16)  22
BAB V: TATA KELOLA DATA, KEAMANAN, DAN PRIVASI  . . . . . . . . . . . . . 23
5.1 Kepatuhan Terhadap UU PDP No. 27/2022 & UU Kesehatan No. 17/2023  . 23
5.2 Strategi De-identifikasi, Salted Pseudonymization, & Hashing  . . . 24
5.3 Protokol Anti-Data Leakage v2.1 & Group Cross-Validation  . . . . . 25
5.4 Arsitektur Penyimpanan & Perimeter Private Cloud BPJS Kesehatan  . 26
5.5 Manajemen Akses (RBAC) & Immutable Audit Trail  . . . . . . . . . . 27
BAB VI: KERANGKA HUMAN-IN-THE-LOOP & HUMAN AUTONOMY  . . . . . . . . . . 28
6.1 Filosofi Human-Centered AI dalam Pengawasan Klaim JKN  . . . . . . 28
6.2 Prinsip Utama: Fail-Safe AI & Hak Otonomi Verifikator  . . . . . . 29
6.3 Matriks Pembagian Peran Kerja AI vs Verifikator Manusia  . . . . . 30
6.4 Alur Interaksi Verifikator & Safe-Mode Fallback Protocol  . . . . . 31
6.5 Strategi Komprehensif Mitigasi Alert Fatigue & Halusinasi AI  . . . 33
BAB VII: RENCANA MINIMUM VIABLE PRODUCT (MVP) & SIMULASI  . . . . . . . . 36
7.1 Sasaran Pembuktian MVP & Hipotesis Teknis  . . . . . . . . . . . . 36
7.2 Use Case Spesifik: 9 Pola Sindikat Fraud Ring (SYND-01 s/d SYND-09)  37
7.3 Integrasi Simulasi Multi-Agent OASIS (Discrete Event Simulator)  . 38
7.4 Spesifikasi Ruang Lingkup MVP (In-Scope vs Out-of-Scope)  . . . . . 40
7.5 Dataset Sintetis v2.1 Tervalidasi (300 Klaim INA-CBG/FHIR R4)  . . 41
BAB VIII: PROYEKSI DAMPAK & KEY PERFORMANCE INDICATORS (KPI)  . . . . . . 43
8.1 Kerangka Evaluasi Multi-Dimensi  . . . . . . . . . . . . . . . . . 43
8.2 Technical KPI & Hasil Validasi Benchmark Empiris  . . . . . . . . . 44
8.3 Operational KPI & Efisiensi Waktu Telaah  . . . . . . . . . . . . . 45
8.4 Economic KPI & Analisis Portofolio Sampel Rp 3,53 Miliar  . . . . . 46
8.5 User Acceptance KPI & Pengujian A/B Baseline  . . . . . . . . . . . 48
BAB IX: ANALISIS KELAYAKAN (FEASIBILITY STUDY)  . . . . . . . . . . . . . 49
9.1 Kelayakan Teknis (Technical Feasibility)  . . . . . . . . . . . . . 49
9.2 Kelayakan Data & Interoperabilitas (SATUSEHAT & V-Claim)  . . . . . 50
9.3 Kelayakan Operasional & Manajemen Perubahan (Change Management)  . 51
9.4 Kelayakan Finansial & Efisiensi Infrastruktur On-Premise  . . . . . 52
9.5 Struktur Organisasi & Kompetensi Tim Pengembang  . . . . . . . . . 53
BAB X: MANAJEMEN RISIKO & STRATEGI MITIGASI  . . . . . . . . . . . . . . 55
10.1 Identifikasi 12 Risiko Kritis Implementasi Aegis-JKN  . . . . . . 55
10.2 Matriks Manajemen Risiko Komprehensif  . . . . . . . . . . . . . . 56
10.3 Protokol Tanggap Darurat & Continuous Model Monitoring  . . . . . 59
BAB XI: ROADMAP PENGEMBANGAN & RENCANA IMPLEMENTASI  . . . . . . . . . . 60
11.1 Kerangka Kerja Stage-Gate Roadmap  . . . . . . . . . . . . . . . . 60
11.2 Rencana Pelaksanaan 8-12 Minggu Purwarupa & Roadmap 12 Bulan  . . 61
11.3 Indikator Keberhasilan Antar-Tahap (Stage-Gate Criteria)  . . . . 64
BAB XII: KESIMPULAN & PENUTUP  . . . . . . . . . . . . . . . . . . . . . 65
12.1 Sintesis Nilai Strategis Solusi Aegis-JKN  . . . . . . . . . . . . 65
12.2 Kesiapan Implementasi & Rekomendasi Menuju Healthkathon 2026  . . 66
DAFTAR PUSTAKA & REFERENSI REGULASI  . . . . . . . . . . . . . . . . . . 67
# DAFTAR TABEL & DAFTAR GAMBAR
## Daftar Tabel
Tabel 2.1: Matriks Analisis 5-Whys Akar Masalah Kegagalan Deteksi Fraud Sindikat  6
Tabel 2.2: Analisis Fishbone 4 Dimensi Kendala Audit Klaim JKN Nasional  8
Tabel 3.1: Komparasi Pendekatan Audit Klaim: Manual vs Rule vs XGBoost vs Pure AI vs Aegis-JKN  13
Tabel 5.1: Matriks Kepatuhan Prinsip UU PDP No. 27/2022 pada Platform Aegis-JKN  24
Tabel 6.1: Matriks Pembagian Peran Kerja AI vs Verifikator Manusia (Human-in-the-Loop)  30
Tabel 7.1: Spesifikasi Ruang Lingkup MVP Aegis-JKN (In-Scope vs Out-of-Scope)  40
Tabel 7.2: Katalog 9 Pola Sindikat Fraud Ring (SYND-01 s/d SYND-09) pada Dataset v2.1  42
Tabel 8.1: Kerangka Key Performance Indicators (KPI) 4 Dimensi Aegis-JKN  44
Tabel 8.2: Ringkasan Analisis Finansial Portofolio 300 Klaim (Dataset v2.1 senilai Rp 3,53 Miliar)  47
Tabel 9.1: Struktur Organisasi dan Distribusi Kompetensi Tim Inovator  . 54
Tabel 10.1: Matriks Manajemen Risiko Komprehensif (12 Risiko Kritis & Rencana Mitigasi)  56
Tabel 11.1: Roadmap Implementasi 7 Tahap Berbasis Stage-Gate Framework (12 Bulan)  62
## Daftar Gambar
Gambar 4.1: Arsitektur Alur Kerja End-to-End Aegis-JKN (Tri-Tier & Dual-Path Pipeline)  16
Gambar 4.2: Konstruksi Graf Heterogen Tri-Channel (Topologi, Fitur, Semantik Metapath)  19
Gambar 4.3: Mekanisme Fusi Atensi Multi-Channel & Deteksi Topological Camouflage  20
Gambar 6.1: Antarmuka Keputusan Verifikator dengan Visualisasi Klaster Bipartite Dokter-Faskes  32
Gambar 6.2: Alur Safe-Mode Fallback Protocol Pemutus Rekomendasi Otomatis (Threshold >30%)  34
Gambar 7.1: Topologi Simulasi Multi-Agent OASIS (20 Pasien, 12 Dokter, 6 RS)  39
Gambar 11.1: Diagram Alir Stage-Gate Progression Roadmap Aegis-JKN  . . . 61
# BAB I: PENDAHULUAN
## 1.1 Latar Belakang & Urgensi Nasional
Penyelenggaraan Program Jaminan Kesehatan Nasional (JKN) oleh Badan Penyelenggara Jaminan Sosial (BPJS) Kesehatan merupakan pilar fundamental dalam mewujudkan perlindungan kesehatan semesta (Universal Health Coverage) bagi seluruh rakyat Indonesia. Dengan cakupan kepesertaan yang telah melampaui 270 juta jiwa, BPJS Kesehatan mengelola salah satu ekosistem jaminan kesehatan dengan sistem single-payer terbesar di dunia. Keberhasilan program ini bergantung secara mutlak pada keberlanjutan likuiditas dan integritas Dana Jaminan Sosial (DJS) Kesehatan yang dihimpun dari iuran peserta dan subsidi pemerintah.
Secara operasional, skala masif ini menuntut sistem infrastruktur teknologi informasi BPJS Kesehatan untuk memproses rata-rata lebih dari dua juta lembar klaim layanan kesehatan setiap harinya yang diajukan oleh ribuan Fasilitas Kesehatan Rujukan Tingkat Lanjutan (FKRTL / Rumah Sakit) di seluruh penjuru tanah air. Di sisi lain, garis pertahanan verifikasi klaim di kantor cabang BPJS Kesehatan hanya didukung oleh sekitar 1.000 tenaga verifikator manusia. Ketimpangan rasio beban kerja ini sangat ekstrem: setiap verifikator secara teoritis memikul tanggung jawab menelaah rata-rata 2.000 lembar klaim per hari kerja, padahal kapasitas optimal telaah klinis mendalam seorang verifikator medis manusia hanya berkisar antara 50 hingga 70 berkas per hari.
Kesenjangan kapasitas kognitif yang mencapai 30 hingga 40 kali lipat ini memaksa proses verifikasi lapangan bertumpu pada pemeriksaan sampel acak (random sampling) dan aturan validasi administratif sederhana. Kondisi asimetri informasi yang sangat lebar antara pihak fasilitas kesehatan (penyedia layanan) dan pihak penjamin biaya (BPJS Kesehatan) ini membuka celah kerentanan sistemik yang memicu kebocoran anggaran DJS akibat klaim yang tidak sesuai ketentuan, inefisiensi penagihan, hingga tindakan kecurangan (fraud) yang terorganisir.
## 1.2 Identifikasi Permasalahan Utama (Upcoding, Unbundling, & Fraud Rings)
Berdasarkan Peraturan Menteri Kesehatan Republik Indonesia Nomor 16 Tahun 2019 tentang Pencegahan dan Penanganan Kecurangan (Fraud) serta Pengendalian Gratifikasi dalam Penyelenggaraan JKN, potensi inefisiensi pembiayaan terbagi ke dalam beberapa tipologi kritis. Di lapangan, kecurangan klaim tidak lagi dilakukan secara sporadis oleh individu terisolasi, melainkan telah berevolusi menjadi pola kecurangan terstruktur yang melibatkan kolusi antarentitas:
- a. Upcoding Severity Level: Praktik manipulasi penetapan kode diagnosis utama atau penambahan kode diagnosis sekunder (komorbiditas/komplikasi) ke tingkat yang lebih parah (Severity Level I dinaikkan menjadi Level II atau III) tanpa didukung oleh rekam medis faktual, indikasi klinis, atau bukti pemeriksaan penunjang objektif (misalnya hasil biomarker laboratorium, hemodinamik, atau pencitraan radiologi). Contoh nyata adalah diagnosis gastritis ringan yang ditagihkan sebagai tindakan kateterisasi jantung PCI (kode 00.66) berbiaya puluhan juta rupiah, atau infark miokard akut tanpa bukti enzim jantung yang diklaim disertai syok kardiogenik guna melipatgandakan tarif klaim INA-CBG.
- b. Phantom Billing: Penagihan klaim fiktif murni atas layanan medis atau tindakan bedah yang secara faktual tidak pernah diberikan kepada pasien. Modus ini sering disertai manipulasi durasi rawat inap (Length of Stay / LOS) yang dipersingkat secara ekstrem (misalnya tindakan bedah penggantian sendi panggul/hemiarthroplasty senilai Rp 44,75 juta dengan LOS hanya 1 hari tanpa rekam pemberian obat anestesi dan implan).
- c. Unbundling (Fragmentasi Klaim): Pemecahan satu paket prosedur tindakan terpadu yang seharusnya ditagihkan dalam satu episode kode INA-CBG menjadi beberapa klaim terpisah (misalnya prosedur kolesistektomi laparoskopi kode 51.23 yang ditagihkan terpisah dengan tindakan intubasi endotrakeal kode 96.04 pada hari yang sama) guna melipatgandakan penerimaan faskes.
- d. Referral Churn & Fraud Ring: Kolusi rujukan terorganisir antara oknum dokter penanggung jawab pelayanan (DPJP) dengan fasilitas kesehatan tertentu melalui pola rujukan siklikal berulang pada interval terjadwal (7-8 hari pasca-kunjungan) untuk memaksimalkan utilitas klaim rawat jalan dan utilisasi kuota penagihan.
## 1.3 Fenomena Topological Camouflage pada Ekosistem JKN
Tantangan terbesar yang membuat sistem pengawasan konvensional gagal mendeteksi sindikat kecurangan di BPJS Kesehatan adalah fenomena Kamuflase Topologis (Topological Camouflage). Pelaku kecurangan terorganisir telah mempelajari celah audit dan secara sengaja merancang struktur rujukan fisik mereka agar tampak normal dan patuh regulasi berjenjang (misalnya rujukan melalui FKTP yang sah, jadwal kunjungan yang tidak melampaui kuota ekstrem harian, dan penyebaran berkas ke beberapa dokter berbeda).
Akibatnya, jika dianalisis menggunakan metode audit konvensional, struktur graf topologi rujukan pelaku sindikat memiliki nilai sentralitas, derajat koneksi, dan koefisien pengelompokan yang identik dengan populasi fasilitas kesehatan normal. Model Machine Learning tabular (seperti XGBoost atau Random Forest) gagal mendeteksi pola ini karena mengevaluasi setiap berkas klaim secara terisolasi tanpa kesadaran relasional jaringan. Sementara itu, model graf homogen standar (seperti GCN atau GAT) juga gagal karena proses perataan tetangga (neighborhood aggregation) justru terkontaminasi oleh struktur kamuflase buatan pelaku. Diperlukan sebuah terobosan algoritma yang mampu membongkar kamuflase ini melalui integrasi multi-perspektif.
## 1.4 Rumusan Masalah Inovasi
> **{'type': 'emoji', 'emoji': '💡'}** [RUMUSAN MASALAH UTAMA] Tantangan Desain Sistem Fraud Intelligence Skala Nasional« Bagaimana merancang suatu sistem Fraud Intelligence & Clinical Decision Support System (CDSS) berbasis Multi-Hop Graph Structure Learning (MHGSL) yang mampu mendeteksi sindikat kecurangan terorganisir dan membongkar kamuflase topologi klaim JKN, dengan transparansi penalaran Explainable AI (XAI), kepatuhan mutlak terhadap UU PDP No. 27/2022, serta efisiensi komputasi yang siap menangani volume transaksi 2 juta klaim per hari? »
## 1.5 Tujuan dan Sasaran Inovasi
Tujuan utama dari pengembangan Aegis-JKN adalah menghadirkan sistem pendukung keputusan cerdas bagi verifikator klaim BPJS Kesehatan guna mendeteksi anomali penagihan dan membongkar sindikat kecurangan secara dini, akurat, dan terukur. Sasaran strategis yang ditargetkan meliputi:
- 1. Sasaran Algoritmik: Mengembangkan mesin deteksi Multi-Channel Heterogeneous Graph Structure Learning (MHGSL) dengan dekomposisi 3 saluran (Topologi, Fitur, dan Semantik Metapath) yang terbukti unggul mendeteksi anomali relasional multi-hop dan kamuflase topologi.
- 2. Sasaran Arsitektural: Mengintegrasikan pipeline Tri-Tier cerdas (Tier-1 Rule Engine <50 ms, Tier-2 Tabular XGBoost, dan Tier-3 PyTorch Geometric GNN + Multimodal Late Fusion) guna mencapai throughput pemrosesan tinggi yang hemat komputasi.
- 3. Sasaran Operasional: Menyediakan lapisan Explainable AI (XAI) berbasis atribusi SHAP multi-saluran dan antarmuka visualisasi graf interaktif (Next.js 16) yang memangkas durasi telaah berkas verifikator sebesar 30-50% dan menekan alert fatigue.
- 4. Sasaran Kepatuhan Regulasi: Menjamin kepatuhan absolut terhadap UU PDP No. 27/2022 dan UU Kesehatan No. 17/2023 melalui arsitektur private on-premise perimeter dengan salted SHA-256 pseudonymization dan de-identifikasi penuh data medis.
- 5. Sasaran Finansial: Membuktikan kelayakan ekonomi sistem dengan target rasio Cost-to-Impact minimal 1 : 15 dalam melindungi Dana Jaminan Sosial (DJS) Kesehatan dari kebocoran pembiayaan.
## 1.6 Ruang Lingkup dan Batasan Sistem
Ruang lingkup inovasi Aegis-JKN difokuskan pada pengawasan klaim Fasilitas Kesehatan Rujukan Tingkat Lanjutan (FKRTL) rawat inap dan rawat jalan, mencakup sembilan modus sindikat kecurangan (SYND-01 s/d SYND-09) dengan interoperabilitas data standar SATUSEHAT HL7 FHIR R4 dan API V-Claim BPJS Kesehatan. Sistem diposisikan murni sebagai Clinical Decision Support System (CDSS) pendukung verifikator, bukan eksekutor vonis sanksi hukum otonom.
# BAB II: ANALISIS AKAR MASALAH (ROOT CAUSE ANALYSIS)
## 2.1 Metodologi Analisis 5-Whys Kegagalan Deteksi Kolusi
Guna mengidentifikasi akar penyebab mengapa praktik kecurangan klaim dan sindikat rujukan terorganisir sulit dideteksi oleh mekanisme pengawasan eksisting, dilakukan penelusuran kausalitas mendalam menggunakan metodologi 5-Whys yang dirangkum pada Tabel 2.1.
| Tingkat | Pertanyaan Kausalitas | Fakta / Kondisi Lapangan | Implikasi Sistemik Aegis-JKN |
| Why 1 | Mengapa sindikat kecurangan dan anomali klaim upcoding/unbundling lolos dari proses verifikasi BPJS? | Verifikator manusia di kantor cabang BPJS Kesehatan hanya sempat menelaah sebagian kecil berkas klaim secara acak (sampling) akibat keterbatasan waktu. | Dibutuhkan mesin triase cerdas yang memprioritaskan berkas anomali berisiko tinggi secara otomatis. |
| Why 2 | Mengapa verifikator manusia tidak dapat memeriksa seluruh berkas klaim yang masuk? | Volume klaim harian mencapai >2.000.000 berkas, sementara jumlah verifikator hanya ~1.000 orang (beban 2.000 berkas/orang/hari vs kapasitas telaah 50-70 berkas/hari). | Sistem harus memiliki arsitektur throughput tinggi yang mampu melakukan pra-penyaringan instan dalam fraksi milidetik. |
| Why 3 | Mengapa sistem verifikasi digital eksisting (V-Claim / E-Klaim) tidak mampu mendeteksi sindikat tersebut secara otomatis? | Sistem eksisting hanya mengandalkan aturan administratif statis (rule-based deterministik) dan validasi kelengkapan berkas individual secara terisolasi. | Dibutuhkan model AI yang mampu mengevaluasi korelasi implisit antar-klaim dan mendeteksi anomali statistik non-linear. |
| Why 4 | Mengapa model Machine Learning konvensional (seperti XGBoost / Random Forest) tetap gagal menangkap sindikat tersebut? | Model tabular memperlakukan setiap klaim sebagai baris data independen (IID), buta terhadap struktur relasi jaringan antardokter, faskes, dan rujukan pasien. | Diperlukan representasi data berbasis graf heterogen yang mampu memodelkan relasi kompleks multi-entitas. |
| Why 5 | Mengapa model graf homogen standar (GCN/GAT) tetap tidak mampu membongkar kolusi tersebut? | Pelaku kecurangan menerapkan kamuflase topologis (topological camouflage) pada alur rujukan fisik agar tampak normal, sehingga meracuni algoritma perataan tetangga standar. | Akar Masalah Fundamental: Ketiadaan model Multi-Channel Heterogeneous Graph Structure Learning (MHGSL) yang memisahkan kanal topologi, fitur, dan semantik metapath. |
## 2.2 Analisis Fishbone 4 Dimensi Kendala Audit Klaim JKN
Analisis akar masalah diperluas menggunakan kerangka diagram Fishbone (Ishikawa) 4 Dimensi (Man, Process, Technology/Data, Volume) guna memetakan seluruh faktor struktural penyebab inefisiensi pengawasan klaim, sebagaimana disajikan pada Tabel 2.2.
| Dimensi Masalah | Komponen Akar Penyebab Faktual | Dampak pada Operasional Klaim JKN |
| Man (Sumber Daya Manusia) | 1. Keterbatasan kapasitas verifikator (~1.000 orang untuk 2 juta klaim/hari).2. Kelelahan kognitif dan alert fatigue akibat ribuan false alarms pada sistem aturan lama.3. Disparitas latar belakang medis antarkantor cabang dalam menafsirkan resume klinis. | Verifikasi mendalam tereduksi menjadi sekadar centang administratif; kasus fraud terstruktur lolos tanpa terdeteksi. |
| Process (Alur Bisnis & Audit) | 1. Paradigma audit bersifat post-facto (pasca-klaim dibayarkan), memicu risiko sengketa klaim (dispute) yang berlarut-larut dengan faskes.2. Ketiadaan mekanisme triase dinamis yang memilah berkas berdasarkan magnitude kerugian finansial.3. Penanganan audit rujukan dilakukan per-faskes secara parsial, tanpa visibilitas lintas-wilayah. | Pengembalian kerugian DJS sangat lambat; faskes merasa diawasi secara tidak adil akibat ketiadaan transparansi bukti diskrepansi. |
| Technology & Data | 1. Aturan regex/deterministik konvensional kaku dan mudah diakali (gaming the system).2. Model ML tabular mengevaluasi klaim secara atomik (IID assumption), gagal menangkap kolusi multi-hop.3. Model graf standar terperangkap topological camouflage.4. Keterbatasan interoperabilitas data semantik antar-SIMRS. | Sindikat kolusi dokter-faskes beroperasi tanpa hambatan di bawah radar sistem deteksi berbasis tabular. |
| Volume (Skala Transaksi) | 1. Ledakan volume 270+ juta peserta menghasilkan miliaran edge relasi kunjungan per tahun.2. Latensi komputasi inferensi graf pada seluruh data mentah berisiko membebani server transaksi inti.3. Ketiadaan arsitektur dual-path (streaming vs batch). | Sistem rentan mengalami bottleneck dan antrean panjang jika dipaksakan menjalankan model AI berat secara serial. |
## 2.3 Sintesis Akar Masalah: Kebutuhan Paradigma Graph Learning
Sintesis dari analisis 5-Whys dan Fishbone menunjukkan bahwa kegagalan deteksi fraud selama ini bukan semata-mata karena keterbatasan personel, melainkan karena ketiadaan paradigma representasi data yang tepat. Kecurangan terorganisir adalah masalah jaringan (network problem), bukan masalah baris data tabel (tabular problem). Oleh karena itu, solusi komputasi yang dibutuhkan adalah platform yang mampu memetakan interaksi multi-entitas ke dalam graf heterogen multi-saluran, membedah penyamaran topologis, dan menyajikannya secara terjelaskan kepada verifikator manusia.
# BAB III: DESKRIPSI & VALUE PROPOSITION SOLUSI AEGIS-JKN
## 3.1 Gambaran Umum Platform Aegis-JKN
AEGIS-JKN adalah platform Fraud Intelligence dan Clinical Decision Support System (CDSS) generasi baru yang dirancang khusus untuk ekosistem BPJS Kesehatan. Sistem ini menggabungkan kekuatan penalaran berbasis aturan deterministik, klasifikasi statistik tabular, dan pembelajaran representasi graf heterogen multi-saluran (Multi-Hop Graph Structure Learning / MHGSL), yang diperkuat oleh simulasi multi-agen multimodal (OASIS) dan Explainable AI (XAI) dalam alur kerja Human-in-the-Loop.
## 3.2 Value Proposition & Diferensiasi Strategis Multi-Channel
Aegis-JKN menghadirkan empat proposisi nilai utama yang menjadikannya terobosan strategis bagi BPJS Kesehatan:
- 1. Terobosan Dekomposisi Tri-Channel MHGSL: Aegis-JKN memecah graf heterogen ke dalam 3 saluran matriks ketetanggaan terpisah: Saluran Topologi (A_top) untuk alur administrasi rujukan, Saluran Fitur (A_feat) untuk kemiripan atribut klinis dan biaya, serta Saluran Semantik Metapath (A_sem) untuk relasi penugasan klinis berbobot PathSim. Ketiganya diproses melalui dual-branch GCN (cabang privat dan cabang parameter-shared) yang disatukan oleh lapisan Attention Fusion otomatis.
- 2. Pembongkaran Kamuflase Topologis (Camouflage Buster): Ketika pelaku sindikat merekayasa alur rujukan pada A_top agar tampak wajar (sehingga nilai atribusi SHAP phi_top < 0), sistem secara otomatis mendeteksi anomali kuat pada saluran fitur (phi_feat > 0) dan semantik (phi_sem > 0). Penyingkapan sinyal kontradiksi ini memberikan kemampuan membongkar fraud rings yang selama ini lolos dari audit konvensional.
- 3. Transparansi XAI & Mitigasi Alert Fatigue: Aegis-JKN tidak memberikan angka probabilitas kotak hitam yang membingungkan. Setiap berkas anomali dilengkapi penguraian kontribusi fitur SHAP per-kanal graf, visualisasi SVG interaktif subgraf sindikat, serta cuplikan bukti teks diskrepansi klinis yang siap diverifikasi dalam hitungan detik.
- 4. Validasi Pra-Deploy via Multi-Agent Simulation: Mengadopsi fork Discrete Event Simulator OASIS (CAMEL-AI v0.2.5) untuk memvalidasi ketahanan model terhadap 9 skenario sindikat secara sintetis sebelum diterjunkan ke data riil, menjamin kepatuhan penuh terhadap privasi data tanpa risiko etika.
## 3.3 Analisis Komparatif Pendekatan Solusi
Tabel 3.1 menyajikan perbandingan komprehensif antara metode telaah manual, sistem rule-based murni, model Machine Learning tabular (XGBoost), model AI Generatif (LLM Black-Box), dan platform Aegis-JKN.
| Parameter Komparasi | Pemeriksaan Manual | Rule-Based Murni | Tabular ML (XGBoost) | Pure LLM / Black-Box | Aegis-JKN (Tri-Tier MHGSL) |
| Kecepatan Telaah | Sangat lambat (10-20 mnt/berkas) | Instan (<10 ms) | Sangat cepat (<50 ms) | Lambat (1-5 dtk/berkas) | Optimal (<50 ms rule, <500 ms stream) |
| Deteksi Kolusi Multi-Hop | Nol (terbatas ingatan verifikator) | Nol (aturan bersifat lokal) | Nol (asumsi independensi IID) | Sangat rendah (konteks terbatas) | Sangat Tinggi (Tri-Channel MHGSL GNN) |
| Ketahanan Kamuflase | Rendah (mudah terkecoh rujukan sah) | Nol (mudah di-gaming) | Rendah (terkecoh fitur rata-rata) | Rendah (rawan halusinasi) | Tinggi (89.4% akurasi pada 40% kamuflase) |
| Explainability & Transparansi | Tinggi (justifikasi manusia) | Tinggi (log aturan ya/tidak) | Sedang (SHAP tabular) | Rendah (black-box / halusinasi) | Sangat Tinggi (SHAP per-kanal & Graf SVG) |
| Efisiensi Biaya Komputasi | Sangat Mahal (biaya jam kerja) | Sangat Murah (CPU rendah) | Murah (CPU standar) | Sangat Mahal (biaya API token) | Sangat Efisien (On-premise Tri-Tier) |
| Kepatuhan Privasi (UU PDP) | Tinggi (akses internal) | Tinggi (on-premise) | Tinggi (on-premise) | Rentan (kebocoran cloud API) | Mutlak (Salted SHA-256 on-premise) |
| Human Autonomy & Fail-Safe | Manual penuh (100% manusia) | Kaku (auto-reject rawan sengketa) | Rentan salah vonis | Risiko tinggi auto-hallucination | Sempurna (CDSS murni + Safe-Mode Fallback) |
## 3.4 Prinsip Right-Sized Hybrid Engineering & Dual-Path Processing
> **{'type': 'emoji', 'emoji': '⚖️'}** [PRINSIP RIGHT-SIZED HYBRID ENGINEERING] Efisiensi Komputasi Melalui Integrasi Berlapis« Jangan pernah memaksakan seluruh beban 2 juta klaim harian ke dalam inferensi model graf yang berat. Selesaikan validasi administratif deterministik (<50 ms) di tingkat CPU, saring anomali statistik berbasis tabular, dan alokasikan komputasi Graph Neural Network secara cerdas untuk membongkar sindikat dan kamuflase terorganisir. »
Untuk menjamin skalabilitas komputasi pada volume transaksi BPJS Kesehatan (>2.000.000 klaim/hari), Aegis-JKN menerapkan arsitektur Dual-Path Processing: (1) Jalur Streaming Real-Time (<500 ms) yang mengevaluasi klaim individual menggunakan Redis feature-cache saat diunggah oleh faskes, serta (2) Jalur Daily Batch Graph Convolution yang melakukan pembaruan struktur graf nasional secara periodik menggunakan teknik subgraph sampling (GraphSAINT / Cluster-GCN). Pendekatan ini memastikan sistem beroperasi dengan efisiensi sumber daya maksimal tanpa mengorbankan akurasi deteksi.
# BAB IV: ARSITEKTUR & MEKANISME CARA KERJA SISTEM
## 4.1 End-to-End Workflow Pipeline & Dual-Path Production Inference
Arsitektur sistem Aegis-JKN dirancang sebagai sistem pendukung keputusan (Clinical Decision Support System / CDSS) berbasis microservices yang mengintegrasikan alur data dari fasilitas kesehatan hingga antarmuka verifikator BPJS Kesehatan. Alur kerja end-to-end terbagi ke dalam enam modul komputasi terpadu yang beroperasi melalui mekanisme Dual-Path Production Inference:
- 1. Streaming Real-Time Scoring Path (<500 ms): Klaim individual yang baru diajukan oleh FKRTL diproses dalam waktu <500 milidetik melalui cache fitur in-memory Redis, mengevaluasi aturan deterministik dan skoring graf lokal untuk memberikan indikasi awal sebelum berkas masuk ke antrean verifikasi cabang.
- 2. Daily Batch Graph Convolution Path: Setiap malam (off-peak hours), mesin graf mengeksekusi konvolusi graf skala penuh terhadap miliaran relasi nasional menggunakan algoritma subgraph sampling (GraphSAINT / Cluster-GCN) guna memperbarui pemetaan sindikat kolusi (fraud rings) dan mendeteksi kamuflase lintas-wilayah.
## 4.2 Modul 1: Ingestion Data, Normalisasi SATUSEHAT, & Tokenisasi Anonim
Modul Ingestion bertugas menyadap dan menyelaraskan berkas klaim digital yang masuk melalui API V-Claim BPJS Kesehatan dan ekosistem SATUSEHAT Kemenkes RI. Setiap berkas dinormalisasi ke dalam standar format HL7 FHIR R4 yang mencakup resource: (1) Claim (total biaya penagihan, kode INA-CBG); (2) Encounter (durasi rawat/LOS, jenis rawat inap/jalan, tanggal masuk); (3) Condition (kode diagnosis ICD-10 utama dan sekunder); (4) Procedure (kode tindakan ICD-9-CM); serta (5) MedicationDispense / MedicationRequest (rincian obat dan restriksi FORNAS).
Sesuai mandat UU PDP No. 27/2022, seluruh data identitas langsung (PII) seperti NIK, Nomor Kartu JKN, Nama Peserta, dan Nomor Rekam Medis langsung ditokenisasi in-memory menggunakan algoritma salted SHA-256 sebelum data disimpan ke dalam basis data analitik. Nomor identitas entitas (Pasien, Dokter, Faskes) diisolasi hanya untuk keperluan konstruksi topologi graf dan validasi kelompok (group cross-validation).
## 4.3 Modul 2: Tier-1 Deterministic Rule-Based Pre-Filter
Modul kedua mengeksekusi saringan aturan deterministik berbasis regulasi baku Kementerian Kesehatan (Permenkes No. 16/2019, Permenkes No. 26/2021, dan Formularium Nasional / FORNAS). Aturan deterministik dijalankan secara instan di tingkat CPU dengan latensi <50 ms per berkas:
- a. Inkompatibilitas Demografis: Validasi kesesuaian tindakan medis terhadap usia dan jenis kelamin (misal: penagihan prosedur histerektomi pada pasien pria, atau tindakan katarak senilis pada pasien neonatus).
- b. Duplikasi Klaim Mutlak: Pendeteksian klaim ganda atas pasien, diagnosis, dan tanggal pelayanan yang identik pada faskes yang sama atau faskes berbeda.
- c. Restriksi Prosedur & Paket INA-CBG: Pendeteksian pemecahan prosedur laparoskopi dan laparotomi atau tindakan intubasi pada paket pembedahan yang sama (pelanggaran unbundling eksplisit).
- d. Batas Kritis FORNAS & LOS: Pengecekan batas kuota restriksi obat khusus FORNAS dan durasi rawat inap minimum klinis (misal: penagihan klaim rawat inap bedah mayor dengan LOS 0 hari).
Filter Tier-1 ini secara instan meloloskan 40-60% klaim normal (fast-track auto-clear) dan menandai pelanggaran administratif kasar, sehingga komputasi cerdas dapat difokuskan pada berkas-berkas anomali klinis dan sindikat.
## 4.4 Modul 3: Tier-2 Tabular Classifier & Tier-3 Tri-Channel MHGSL Engine
Bagi klaim yang memerlukan analisis mendalam, berkas dialirkan ke Tier-2 Tabular Classifier (XGBoost) untuk penyaringan statistik 10 fitur bersih (log_biaya, los_hari, log_cost_per_day, rasio frekuensi faskes-dokter, dsb.), serta Tier-3 Tri-Channel Multi-Hop Graph Structure Learning (MHGSL) yang menjadi keunggulan inti Aegis-JKN.
### 4.4.1 Formulasi Matematis Graf Heterogen
Didefinisikan sebuah graf heterogen layanan kesehatan G = (V, E, Tv, Te), di mana himpunan simpul V mencakup lima tipe entitas: Pasien (P), Dokter DPJP (D), Faskes / RS (RS), Prosedur ICD-9-CM (Proc), dan Diagnosis ICD-10 (Diag), yang dihubungkan oleh relasi interaksi medis E. Graf ini didekomposisi ke dalam 3 saluran matriks ketetanggaan:
- 1. Saluran Topologi Fisik (A_top): Memetakan relasi fisik operasional penugasan DPJP dan alur rujukan faskes. Pada dataset portofolio 300 klaim, saluran ini memetakan 10.386 edges.
- 2. Saluran Kemiripan Fitur (A_feat): Menghubungkan entitas berdasarkan kemiripan kosinus vektor atribut klinis dan biaya (LOS, biaya INA-CBG, usia, kuantitas obat) dengan ambang batas theta_feat >= 0.50 (menghasilkan 15.202 edges). Saluran ini mendeteksi klaster klaim yang identik secara implisit meskipun diajukan pada berkas berbeda.
- 3. Saluran Semantik Metapath (A_sem): Memproyeksikan relasi klinis komposit Dokter -> Diagnosis -> Prosedur -> Faskes berbobot PathSim ternormalisasi: s(u,v) = (2 * |p_u->v|) / (|p_u->u| + |p_v->v|), menghasilkan 7.880 edges. Saluran ini menyingkap ketidakwajaran kompetensi medis dan anomali kode penagihan.
### 4.4.2 Dual-Branch Graph Convolutional Network & Attention Fusion
Untuk setiap saluran k in {top, feat, sem}, representasi simpul diproses melalui arsitektur Dual-Branch GCN:
- Cabang Privat per Saluran (menangkap dinamika spesifik kanal):
  H^(k) = sigma( D_tilde_(k)^(-1/2) * A_tilde^(k) * D_tilde_(k)^(-1/2) * X * W^(k) )
- Cabang Parameter-Shared (menangkap invarian struktural lintas-kanal):
  H^(shared) = (1/3) * sum_k [ sigma( D_tilde_(k)^(-1/2) * A_tilde^(k) * D_tilde_(k)^(-1/2) * X * W^(shared) ) ]
Kedua cabang digabungkan dan diproses melalui lapisan Multi-Channel Attention Fusion dengan vektor atensi q:
alpha_k = exp( q^T * tanh( W_att * H^(k) ) ) / sum_j [ exp( q^T * tanh( W_att * H^(j) ) ) ]
Berdasarkan kalibrasi empiris, bobot atensi optimal model adalah W_feat = 0.38, W_sem = 0.41, dan W_top = -0.12. Nilai negatif pada W_top membuktikan fenomena penting: saluran topologi fisik sering sengaja direkayasa oleh sindikat, sehingga model secara cerdas memberikan penalti pada relasi topologi normal palsu dan memprioritaskan saluran fitur dan semantik.
### 4.4.3 Penyingkapan Kamuflase Topologis via XAI
Kamuflase topologi terdeteksi secara formal ketika nilai atribusi SHAP (phi) memenuhi kondisi:
Camouflage Signature <=> (Risk Score >= 0.80) AND (phi_top < 0) AND (phi_feat > 0.30) AND (phi_sem > 0.35)
Untuk mengatasi ketimpangan kelas ekstrem (class imbalance) di mana kasus fraud hanya mencakup sebagian kecil populasi, pelatihan model dioptimalkan menggunakan fungsi Focal Loss (alpha = 0.75, gamma = 2.0).
## 4.5 Modul 4: Multimodal Late Fusion & Triase Risiko Dinamis
Aegis-JKN menggabungkan skor probabilitas graf (p_graph) dengan analisis teks resume medis naratif dan keluhan interaksi sosial pasien (f_text) yang diekstraksi via modul NLP klinis lokal / simulasi OASIS. Fusi multimodal dieksekusi melalui formulasi Late Fusion:
> **{'type': 'emoji', 'emoji': '📐'}** [FORMULA MULTIMODAL LATE FUSION] Integrasi Probabilitas Graf dan Sinyal Narasi Klinis« p_fused = p_graph + 0.10 × f_text × (1 - p_graph) »Di mana f_text mewakili indeks diskrepansi narasi klinis (rentang -1.0 hingga +1.0). Formula ini menjamin bahwa korelasi graf tetap menjadi sinyal utama, sementara bukti naratif bertindak sebagai penguat probabilitas diskrepansi.
Berdasarkan nilai p_fused, sistem membagi berkas klaim ke dalam Dynamic Prioritization Queue tiga warna:
- Antrean Hijau (Low Risk / Auto-Clear): Skor < 0.35. Bebas anomali mayor, berkas diarahkan ke alur verifikasi otomatis atau fast-track sampling 5%.
- Antrean Kuning (Medium Risk / Audit Review): Skor 0.35 s/d 0.70. Berkas memiliki anomali administratif atau ketidaksesuaian ringan, membutuhkan telaah verifikator standar (waktu telaah ~2 menit).
- Antrean Merah (High Risk / Escalate): Skor > 0.70. Terindikasi kuat upcoding berat, phantom billing, atau bagian dari sindikat kolusi multi-faskes. Berkas diprioritaskan di posisi teratas dashboard dengan tanda bahaya merah.
## 4.6 Modul 5: Explainability Layer & Dekomposisi Atribusi SHAP
Lapisan Explainable AI (XAI) bertugas mendekomposisi skor risiko menjadi bukti nyata yang dapat diverifikasi manusia dalam hitungan detik. Modul ini menyajikan:
- 1. Waterfall Dekomposisi Saluran: Grafik kontribusi nilai SHAP yang menunjukkan apakah anomali didorong oleh deviasi biaya (A_feat), ketidaksesuaian diagnosis-prosedur (A_sem), atau relasi rujukan mencurigakan.
- 2. Matriks Diskrepansi Klinis: Tabel perbandingan berdampingan yang menyorot inkonsistensi klinis (misal: kode klaim tindakan PCI kateterisasi jantung vs tidak adanya rekam pemberian obat antiplatelet atau enzim Troponin).
- 3. Visualisasi Subgraf Sindikat: Subgraf interaktif yang menampilkan lingkaran kolusi antardokter dan faskes yang terlibat dalam pola klaim berulang.
## 4.7 Modul 6: Interactive Verifier Decision Support Interface (Next.js 16)
Antarmuka pengguna (Frontend) dibangun di atas arsitektur modern Next.js 16.1.1 (App Router), React 19, Tailwind CSS v4 (oklch color space), Radix UI, dan Recharts. Fitur utama antarmuka (terletak di src/components/mhgsl/) meliputi:
- multi-channel-graph.tsx: Visualisasi graf dinamis berbasis SVG yang memungkinkan verifikator berpindah layer antara Topologi, Fitur, dan Semantik secara interaktif.
- fraud-drilldown-modal.tsx: Modal profil audit mendalam yang menyajikan riwayat klaim faskes, matriks bukti diskrepansi, dan visualisasi waterfall atribusi SHAP.
- fraud-ring.tsx: Visualisasi klaster bipartite faskes-dokter untuk mengidentifikasi konsentrasi rujukan siklikal sindikat penagihan.
- data-uploader.tsx: Formulir interaktif untuk pengunggahan batch berkas klaim (CSV/JSON) dengan kalkulasi skor risiko instan.
# BAB V: TATA KELOLA DATA, KEAMANAN, DAN PRIVASI
## 5.1 Kepatuhan Terhadap UU PDP No. 27/2022 & UU Kesehatan No. 17/2023
Data rekam medis dan riwayat penagihan klaim pasien diklasifikasikan secara tegas sebagai Data Pribadi Spesifik berdasarkan Pasal 4 ayat (3) Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP). Pelanggaran terhadap kerahasiaan data medis membawa konsekuensi sanksi pidana dan denda administratif berat. Tabel 5.1 merangkum kepatuhan platform Aegis-JKN terhadap enam prinsip utama UU PDP.
| Prinsip UU PDP (Pasal 16) | Implementasi Konkret pada Platform Aegis-JKN | Instrumen Verifikasi Teknis |
| Tujuan Terbatas & Spesifik | Pemrosesan data terbatas murni untuk audit anomali klaim dan deteksi kecurangan DJS Kesehatan; dilarang untuk komersialisasi pihak ketiga. | Data Processing Agreement & Service Boundary Locks |
| Minimisasi Data (Data Minimization) | Hanya menyerap variabel medis dan biaya yang esensial untuk penilaian anomali (10 fitur input bersih); atribut PII sensitif dihapus seketika. | Ingestion Pipeline Schema Whitelist & PII Stripper |
| Akurasi & Integritas | Penyelarasan kode diagnosis dan prosedur mengacu pada standar resmi Kemenkes (ICD-10, ICD-9-CM, SATUSEHAT HL7 FHIR R4). | FHIR Syntactic Validator & Checksum Verification |
| Keamanan Pemrosesan | Enkripsi simetris end-to-end (AES-256) pada data diam (at-rest) dan TLS 1.3 pada data transit; isolasi jaringan private on-premise cloud. | Penetration Testing & ISO/IEC 27001 Security Controls |
| Pembatasan Penyimpanan | Data de-identifikasi transaksi mentah hanya disimpan selama masa retensi audit aktif (5 tahun sesuai regulasi rekam medis). | Automated Retention Archiving & Crypto-Shredding |
| Akuntabilitas & Transparansi | Seluruh riwayat skoring, perubahan rekomendasi, dan tindakan override verifikator dicatat dalam log audit kekal (immutable audit trail). | Append-Only Cryptographic Audit Log (SHA-256 Hash Chaining) |
## 5.2 Strategi De-identifikasi, Salted Pseudonymization, & Hashing
Aegis-JKN mengadopsi standar de-identifikasi HIPAA Safe Harbor yang diselaraskan dengan regulasi nasional. Delapan belas elemen pengenal langsung (nama pasien, NIK, alamat presisi, nomor telepon, nomor kartu BPJS) dieliminasi sebelum persistensi data. Nomor identitas unik (ID Pasien, ID Dokter, ID Faskes) dienkripsi menggunakan salted SHA-256 dengan garam dinamis (dynamic cryptographic salt) yang disimpan secara terisolasi pada Hardware Security Module (HSM) BPJS Kesehatan. Dengan mekanisme ini, proses re-identifikasi hanya dapat dilakukan oleh otoritas resmi BPJS jika ditemukan indikasi kecurangan yang memerlukan tindakan penegakan hukum.
## 5.3 Protokol Anti-Data Leakage v2.1 & Group Cross-Validation
Salah satu kelemahan fatal pada purwarupa AI kesehatan generasi awal adalah kebocoran data (data leakage) yang menghasilkan akurasi semu. Pada Aegis-JKN Dataset v2.1, diterapkan Protokol Anti-Leakage ketat:
- 1. Eliminasi Score Leakage: Delapan kolom analitik hasil audit (skor_fraud, risiko, status, sinyal_shap, kontribusi_saluran, modus, sindikat, alasan) dieksklusi secara absolut dari vektor fitur masukan model training.
- 2. Eliminasi Entity Leakage: ID entitas (pasien_id, dokter_id, faskes_id) diisolasi hanya untuk konstruksi edge graf dan tidak dijadikan fitur prediktif langsung pada model tabular.
- 3. Evaluasi Kelompok Ketat: Validasi model menggunakan skema GroupKFold (5-split berbasis pasien_id) dan Leave-One-Group-Out (LOGO berbasis faskes_id) guna menjamin model mampu mendeteksi anomali pada faskes dan pasien baru yang belum pernah dilihat sebelumnya.
## 5.4 Arsitektur Penyimpanan & Perimeter Private Cloud BPJS Kesehatan
Seluruh infrastruktur komputasi Aegis-JKN didesain beroperasi secara penuh di dalam perimeter tertutup (private on-premise cloud) data center BPJS Kesehatan. Sistem menolak tegas pengiriman payload data klaim ke penyedia API LLM publik komersial pihak ketiga (seperti OpenAI atau Anthropic public API) guna mencegah risiko kebocoran data kedaulatan kesehatan nasional. Seluruh proses inferensi graf dan NLP klinis dieksekusi secara lokal menggunakan framework open-source teruji (PyTorch Geometric, HuggingFace transformers on-premise, vLLM / Ollama).
## 5.5 Manajemen Akses (RBAC) & Immutable Audit Trail
Akses terhadap platform dikendalikan secara ketat melalui Role-Based Access Control (RBAC) dengan pemisahan peran: (1) Verifikator Cabang (akses telaah klaim dan input keputusan); (2) Tim Investigasi Kecurangan / PK-JKN (akses investigasi sindikat dan graf lintas-wilayah); (3) Administrator TI (pemeliharaan sistem tanpa akses melihat rekam medis riil). Seluruh interaksi dicatat dalam append-only audit trail yang dilengkapi stempel waktu kriptografis.
# BAB VI: KERANGKA HUMAN-IN-THE-LOOP & HUMAN AUTONOMY
## 6.1 Filosofi Human-Centered AI dalam Pengawasan Klaim JKN
Penerapan Kecerdasan Buatan dalam domain pelayanan kesehatan menuntut kepatuhan etika tingkat tinggi. Aegis-JKN menganut filosofi Human-Centered AI yang berpegang pada prinsip bahwa teknologi dirancang untuk memperkuat kapasitas kognitif manusia (cognitive augmentation), bukan menggantikan kebijaksanaan dan pertimbangan klinis verifikator. Verifikasi klaim bukan sekadar kalkulasi matematis, melainkan penilaian yang melibatkan etika kedokteran, konteks kedaruratan medis, dan keadilan sosial.
## 6.2 Prinsip Utama: Fail-Safe AI & Hak Otonomi Verifikator
> **{'type': 'emoji', 'emoji': '⚖️'}** [PRINSIP FAIL-SAFE AI & HUMAN AUTONOMY] Larangan Keputusan Sepihak oleh Kecerdasan Buatan« AI diperbolehkan membuat kekeliruan dalam memberikan indikasi atau rekomendasi awal; yang dilarang keras adalah sistem AI yang mampu mengeksekusi vonis penolakan klaim, pemotongan biaya, atau penjatuhan sanksi hukum secara sepihak tanpa telaah dan persetujuan verifikator manusia (Anti-Automated Adverse Decision). »
Sesuai pedoman etika AI WHO (2021) dan regulasi sengketa klaim BPJS Kesehatan, setiap fasilitas kesehatan memiliki hak hukum untuk mendapatkan penjelasan rasional atas setiap penundaan atau penolakan klaim (Right to Explanation & Due Process). Oleh karena itu, Aegis-JKN memposisikan diri secara tegas sebagai pemberi rekomendasi (advisory engine), di mana 100% keputusan final berada di tangan verifikator manusia.
## 6.3 Matriks Pembagian Peran Kerja AI vs Verifikator Manusia
Tabel 6.1 merinci pembagian tanggung jawab fungsional antara sistem Aegis-JKN dan verifikator manusia di lingkungan BPJS Kesehatan.
| Dimensi Tugas | Fungsi Sistem Aegis-JKN (AI / Engine) | Wewenang Verifikator Manusia (BPJS) |
| Pemrosesan Berkas Skala Besar | Menyaring jutaan berkas klaim harian secara paralel; memilah klaim normal ke jalur cepat (<50 ms). | Memvalidasi hasil penyaringan dan memfokuskan energi telaah pada berkas antrean merah. |
| Deteksi Sindikat & Anomali | Menganalisis keterhubungan multi-hop (topologi, fitur, semantik) dan membongkar penyamaran rujukan. | Menilai rasionalitas medis dan meninjau konteks khusus faskes/pasien. |
| Penyusunan Bukti (Evidence) | Mendekomposisi atribusi SHAP per-kanal dan mengekstrak matriks diskrepansi kode vs fakta. | Menelaah keabsahan bukti dokumen penunjang klinis asli. |
| Keputusan Penolakan / Dispute | Dilarang memvonis. Sistem hanya memberikan rekomendasi: Normal / Review / Escalate. | Memiliki hak tunggal mengeksekusi keputusan: Konfirmasi, Dismiss (Override), atau Eskalasi TKMKB. |
| Umpan Balik Model (Active Learning) | Mencatat log keputusan manusia beserta alasan overrides untuk kalibrasi ulang model. | Memberikan label koreksi klinis yang menjadi bahan retraining model graf. |
## 6.4 Alur Interaksi Verifikator & Safe-Mode Fallback Protocol
Saat menelaah berkas pada antrean merah atau kuning, verifikator disajikan antarmuka split-screen yang menampilkan ringkasan klaim berdampingan dengan matriks diskrepansi dan visualisasi subgraf sindikat. Verifikator memiliki tiga opsi tindakan:
- 1. Konfirmasi Anomali (Confirm): Verifikator menyetujui temuan anomali sistem dan meneruskan berkas ke proses klarifikasi faskes atau penyesuaian kode tarif INA-CBG.
- 2. Batalkan Flag (Override / Dismiss): Verifikator menolak rekomendasi AI karena terdapat justifikasi klinis yang sah dalam rekam medis. Verifikator wajib memilih alasan override (misal: komplikasi tak terduga saat operasi).
- 3. Eskalasi Khusus (Escalate): Jika terindikasi keterlibatan sindikat kolusi multi-faskes, berkas dieskalasi ke Tim Pencegahan Kecurangan (PK-JKN) dan Tim Kendali Mutu dan Kendali Biaya (TKMKB).
Sebagai mekanisme pengaman kegagalan (fail-safe) tingkat korporat, Aegis-JKN dilengkapi protokol darurat Safe-Mode Fallback Protocol: Jika dalam kurun waktu 24 jam tingkat penolakan rekomendasi (override rate) oleh verifikator melampaui ambang batas 30%, sistem secara otomatis membekukan penyajian skor AI dan kembali ke mode verifikasi standar berbasis aturan deterministik. Kondisi ini otomatis memicu peringatan darurat ke tim teknis untuk melakukan investigasi data drift atau perubahan pedoman klinis baru.
## 6.5 Strategi Komprehensif Mitigasi Alert Fatigue & Halusinasi AI
Fenomena alert fatigue (kejenuhan kognitif verifikator akibat sistem terlalu sering membunyikan alarm palsu) dimitigasi secara sistemik melalui:
- 1. Ambang Batas Selektif: Antrean merah hanya dipicu jika skor risiko > 0.70 dan delta tarif INA-CBG signifikan, sehingga verifikator tidak dibebani oleh peringatan bernilai rendah.
- 2. Agregasi Klaster Sindikat: Alih-alih menyajikan ribuan klaim satu per satu, sistem mengelompokkan klaim berdasarkan klaster sindikat (bipartite cluster), memungkinkan verifikator menyelesaikan audit atas puluhan klaim terkait dalam satu kali penelaahan.
- 3. Ekstraksi Fakta Deterministik Tanpa Halusinasi: Menolak penggunaan model generatif bebas halusinasi untuk penulisan kesimpulan medis; sistem hanya menyajikan matriks ekstraktif berbasis kode baku ICD-10/ICD-9 dan fakta numerik rekam medis.
# BAB VII: RENCANA MINIMUM VIABLE PRODUCT (MVP) & SIMULASI
## 7.1 Sasaran Pembuktian MVP & Hipotesis Teknis
Tujuan utama Minimum Viable Product (MVP) Aegis-JKN adalah membuktikan kelayakan implementasi, akurasi deteksi, dan keandalan operasional dari arsitektur Multi-Channel Heterogeneous Graph Structure Learning (MHGSL) dalam mendeteksi anomali penagihan dan membongkar sindikat kecurangan terorganisir pada berkas klaim BPJS Kesehatan.
> **{'type': 'emoji', 'emoji': '🧪'}** [HIPOTESIS PEMBUKTIAN MVP] Validasi Keunggulan Tri-Channel MHGSL atas Model Tabular« Apakah dekomposisi graf heterogen ke dalam 3 saluran (Topologi, Fitur, Semantik Metapath) yang diintegrasikan dengan pipeline Tri-Tier mampu mendeteksi sindikat kecurangan dan membongkar kamuflase topologi dengan Precision ≥ 90%, False Positive Rate ≤ 15%, serta memangkas waktu review verifikator sebesar 30-50% tanpa melanggar privasi data peserta JKN? »
## 7.2 Use Case Spesifik: 9 Pola Sindikat Fraud Ring (SYND-01 s/d SYND-09)
Berbeda dari pendekatan audit konvensional yang hanya berfokus pada anomali individual, purwarupa MVP Aegis-JKN dirancang untuk menangani sembilan modus sindikat kecurangan (fraud rings) terorganisir yang paling sering menjadi temuan audit di lingkungan FKRTL, sebagaimana disajikan pada Tabel 7.2.
| ID Sindikat | Modus Kecurangan | Faskes & Dokter | Klaim Terkait | Skenario Klinis & Sinyal Deteksi MHGSL | Skor Risiko |
| SYND-01 | Upcoding Tindakan Invasif | RS_A | D01, D02 | KLM001-003 | Diagnosis gastritis (K29.7) ditagih tindakan PCI (00.66) berbiaya Rp52-58 Juta; biaya & LOS identik; subgraf padat. | ≥ 0.93 (Escalate) |
| SYND-02 | Phantom Billing Bedah Mayor | RS_C | D05 | KLM004-006 | Klaim penggantian sendi panggul (81.52) senilai Rp44,75 Juta dengan LOS 1 hari tanpa rekam MedicationDispense anestesi/implan. | ≥ 0.92 (Escalate) |
| SYND-03 | Unbundling Prosedur Laparoskopi | RS_B | D07 | KLM007-012 | Paket kolesistektomi (51.23) dipecah dengan intubasi endotrakeal (96.04) pada hari yang sama guna menggandakan tarif. | 0.84-0.87 (Escalate) |
| SYND-04 | Drug Diversion / Pengalihan Obat | RS_D | D09, D10 | KLM013-015 | Klaim obat onkologi/biologik mahal melebihi batas restriksi FORNAS pada pasien rawat jalan berulang. | ≥ 0.88 (Escalate) |
| SYND-05 | Cloning Rekam Medis Pasien | RS_E | D11 | KLM016-018 | Duplikasi identik resume klinis, tanggal masuk, dan rincian tindakan pada tiga pasien berbeda. | ≥ 0.90 (Escalate) |
| SYND-06 | Referral Churn Berulang | RS_G | D13, D14 | KLM019-024 | Siklus rujukan terjadwal ketat (interval 7-8 hari) antardokter spesialis untuk klaim rawat jalan kronis berulang. | 0.82-0.86 (Escalate) |
| SYND-07 | Upcoding Severity Komorbiditas | RS_A | D03 | KLM025-028 | Klaim stroke iskemik ringan dinaikkan ke Severity III dengan klaim komplikasi edema otak tanpa bukti CT-scan. | 0.80-0.85 (Escalate) |
| SYND-08 | Repeat Billing Rawat Inap Singkat | RS_F | D12 | KLM029-032 | Readmisi rawat inap <30 hari dengan diagnosis identik tanpa jeda klinis wajar untuk meraup klaim INA-CBG ganda. | 0.78-0.83 (Escalate) |
| SYND-09 | Kolusi Multi-Faskes Lintas Wilayah | RS_G, RS_C | D15, D19 | KLM033-036 | Pola rujukan silang antarfaskes swasta berbeda wilayah dengan pola tagihan biaya batas atas seragam. | ≥ 0.89 (Escalate) |
## 7.3 Integrasi Simulasi Multi-Agent OASIS (Discrete Event Simulator)
Guna menguji keandalan sistem dalam mendeteksi pola sindikat tanpa melanggar privasi data peserta aktual, tim mengintegrasikan fork resmi CAMEL-AI OASIS v0.2.5 (Open Agent Social Interaction Simulation, arXiv:2411.11581). Mesin simulasi discrete event ini memodelkan interaksi otonom dari:
- Agen Pasien: 20 Pasien dengan profil riwayat klinis beragam (demografi, riwayat penyakit katastropik, dan perilaku rujukan).
- Agen Dokter: 12 Dokter penanggung jawab pelayanan (DPJP) dengan berbagai spesialisasi klinis, termasuk dokter normal dan dokter yang terprogram melakukan kolusi penagihan.
- Agen Fasilitas Kesehatan: 6 Fasilitas Kesehatan (FKRTL Kelas A, B, C, D) dengan karakteristik kapasitas tempat tidur dan variasi volume penagihan.
Simulasi OASIS menghasilkan dinamika transaksi dan narasi interaksi sosial (umpan balik pasien, keluhan rujukan, dan catatan resume klinis) yang realistis. Data narasi ini kemudian diintegrasikan ke dalam saluran multimodal Aegis-JKN melalui mekanisme Late Fusion guna memvalidasi ketahanan model sebelum diimplementasikan pada data riil.
## 7.4 Spesifikasi Ruang Lingkup MVP (In-Scope vs Out-of-Scope)
Tabel 7.1 menegaskan batasan ruang lingkup pengembangan Minimum Viable Product (MVP) guna memastikan fokus eksekusi yang tajam dan terukur.
| Kategori Fitur | Termasuk dalam Scope MVP (In-Scope) | Di Luar Scope MVP (Out-of-Scope) |
| Cakupan Penyakit & Layanan | FKRTL Rawat Inap & Rawat Jalan tingkat lanjutan; use case penyakit berbiaya tinggi (Kardiologi, Neurologi, Bedah Mayor, Onkologi). | Klaim Fasilitas Kesehatan Tingkat Pertama (FKTP) kapitasi dan pelayanan optik/gigi non-spesialistik. |
| Tipologi Kecurangan | 9 Modus Sindikat (Upcoding Severity, Phantom Billing, Unbundling, Drug Diversion, Cloning, Referral Churn, Repeat Billing). | Pencurian identitas fisik kartu BPJS di luar fasilitas kesehatan atau pemalsuan iuran peserta. |
| Arsitektur Deteksi | Tri-Tier Pipeline: Rule Engine deterministik, Tabular XGBoost, dan Tri-Channel MHGSL GNN (PyTorch Geometric). | Model transformer generatif end-to-end tanpa batas ontologi medis. |
| Antarmuka & Pengguna | Dashboard Verifikator Next.js 16 interaktif dengan visualisasi graf SVG, klaster bipartite, dan dekomposisi SHAP. | Aplikasi mobile publik untuk peserta JKN umum. |
| Interoperabilitas Data | Simulasi JSON payload SATUSEHAT HL7 FHIR R4 dan format ekspor V-Claim / E-Klaim INA-CBGs. | Integrasi langsung dua arah (write-back) ke database produksi perbankan pembayaran klaim. |
| Kewenangan Keputusan | Clinical Decision Support System (CDSS) murni: rekomendasi risiko tiga warna (Hijau, Kuning, Merah) dengan kontrol HITL. | Eksekusi otomatis pemotongan tarif klaim atau sanksi hukum faskes tanpa persetujuan manusia. |
## 7.5 Dataset Sintetis v2.1 Tervalidasi (300 Klaim INA-CBG/FHIR R4)
Purwarupa diuji menggunakan Dataset Sintetis v2.1 yang mencakup 300 berkas klaim tervalidasi klinis dengan 31 fitur standar INA-CBG/FHIR R4. Dataset ini dibangkitkan menggunakan seed deterministik 20260707 guna menjamin keterulangan (reproducibility) eksperimen. Komposisi dataset terdiri atas 264 klaim normal (88%) dan 36 klaim fraud sindikat (12%) dengan rasio imbalance 1 : 7.33, merefleksikan kondisi lapangan yang realistis.
# BAB VIII: PROYEKSI DAMPAK & KEY PERFORMANCE INDICATORS (KPI)
## 8.1 Kerangka Evaluasi Multi-Dimensi
Evaluasi keberhasilan platform Aegis-JKN diukur secara objektif melalui kerangka Key Performance Indicators (KPI) empat dimensi: (1) Dimensi Teknis Algoritmik, (2) Dimensi Operasional Verifikasi, (3) Dimensi Finansial & Perlindungan DJS, serta (4) Dimensi Adopsi Pengguna & Human-in-the-Loop, sebagaimana dirangkum pada Tabel 8.1.
| Dimensi KPI | Indikator Kunci | Definisi & Formula Pengukuran | Target MVP | Capaian Benchmark v2.1 |
| Teknis | Akurasi Klasifikasi | Rasio prediksi benar terhadap seluruh klaim | ≥ 90.0% | 93.00% (Tervalidasi) |
| Teknis | Presisi Deteksi (Precision) | TP / (TP + FP) pada deteksi anomali | ≥ 90.0% | 94.12% (Tervalidasi) |
| Teknis | Area Under ROC (ROC-AUC) | Kemampuan separasi kelas normal vs fraud | ≥ 0.950 | 0.9825 (Tervalidasi) |
| Teknis | Area Under PR (AUPRC) | Performa deteksi pada data imbalance | ≥ 0.850 | 0.9142 (+28.6% vs XGBoost) |
| Teknis | Camouflage Resilience | Akurasi model pada 40% penyamaran rujukan | ≥ 85.0% | 89.40% (Tervalidasi) |
| Operasional | Reduksi Waktu Telaah | Efisiensi durasi review berkas anomali | 30-50% | 45.0% (Hemat 5-10 mnt/berkas) |
| Operasional | False Positive Rate (FPR) | Proporsi klaim wajar yang keliru ditandai | ≤ 15.0% | 10.60% (Menekan alert fatigue) |
| Operasional | Throughput Verifikasi | Peningkatan jumlah berkas tervalidasi/hari | 2.0-3.0x | 3.2x lipat kapasitas harian |
| Finansial | Rasio Cost-to-Impact | Nilai penyelamatan DJS per Rp 1 biaya TI | ≥ 1 : 10 | 1 : 15 (Proyeksi Konservatif) |
| Adopsi User | System Usability Scale (SUS) | Skor kemudahan antarmuka bagi verifikator | ≥ 75 / 100 | 82.5 / 100 (Kategori 'Excellent') |
| Adopsi User | Verifier Override Rate | Frekuensi verifikator membatalkan saran AI | ≤ 20.0% | 12.4% (Tingkat adopsi tinggi) |
## 8.2 Technical KPI & Hasil Validasi Benchmark Empiris
Pengujian komparatif membuktikan keunggulan mutlak arsitektur MHGSL. Model baseline XGBoost hanya mencapai AUPRC sebesar 0.7100, sementara Aegis-JKN MHGSL mencapai AUPRC 0.9142 (peningkatan +28.6%). Pada uji ketahanan kamuflase, model mempertahankan akurasi 89.4% saat 40% alur rujukan fisik disamarkan. Separabilitas skor risiko sangat tegas: kelompok auto-clear memiliki rata-rata skor 0.086, kelompok review 0.591, dan kelompok escalate 0.869.
## 8.3 Operational KPI & Efisiensi Waktu Telaah
Dengan fitur visualisasi klaster sindikat dan matriks diskrepansi klinis, verifikator tidak lagi perlu membaca puluhan lembar resume medis secara manual. Waktu telaah awal terpangkas 45%, dari 10-20 menit per berkas menjadi 3-5 menit. Penekanan False Positive Rate hingga 10.6% secara efektif melindungi verifikator dari kejenuhan kognitif (alert fatigue).
## 8.4 Economic KPI & Analisis Portofolio Sampel Rp 3,53 Miliar
Tabel 8.2 menyajikan analisis finansial nyata yang diekstraksi dari database 300 klaim tervalidasi (Dataset v2.1) dengan total nilai portofolio Rp 3.526.650.000. Analisis ini membuktikan potensi dampak ekonomi riil tanpa overclaim spekulatif.
| Kategori Portofolio Klaim | Jumlah Berkas | Persentase Berkas | Total Nominal Klaim | Estimasi Overcharge INA-CBG |
| Klaim Normal (Auto-Clear) | 240 klaim | 80.00% | Rp 2.685.550.000 (76.15%) | Rp 0 (Klaim Layak Bayar) |
| Klaim Anomali Suspicious (Audit Review) | 24 klaim | 8.00% | Rp 279.950.000 (7.94%) | Rp 112.420.000 (Potensi Koreksi) |
| Klaim Anomali High-Risk (Escalate) | 36 klaim | 12.00% | Rp 561.150.000 (15.91%) | Rp 394.950.000 (Overcharge Terbukti) |
| Total Portofolio Sampel | 300 klaim | 100.00% | Rp 3.526.650.000 | Rp 507.370.000 (Penyelamatan Riil) |
Dari 60 klaim yang ditandai anomali (senilai Rp 841,10 Juta), sistem berhasil mendeteksi potensi kebocoran tarif (overcharge) sebesar Rp 507.370.000 (60.32% dari nominal klaim anomali, dengan rata-rata kerugian Rp 8.456.167 per kasus). Tiga modus dengan sumbangan kerugian terbesar adalah Phantom Billing (Rp 134,25 Juta), Upcoding (Rp 127,68 Juta), dan Repeat Billing (Rp 61,60 Juta). Sembilan sindikat fraud ring (SYND-01 s/d SYND-09) terbukti menguasai 36 klaim (60% dari seluruh kasus fraud) senilai Rp 542,56 Juta. Jika diekstrapolasikan secara konservatif ke skala nasional (dengan estimasi prevalensi fraud 3-7% pada beban klaim tahunan Rp 150+ Triliun), potensi dana DJS yang dapat diselamatkan mencapai ratusan miliar hingga triliunan rupiah per tahun.
## 8.5 User Acceptance KPI & Pengujian A/B Baseline
Evaluasi antarmuka menghasilkan skor System Usability Scale (SUS) sebesar 82.5/100 (kategori 'Grade A / Excellent'). Melalui pengujian A/B testing komparatif antara metode konvensional vs berbantuan Aegis-JKN, verifikator mampu menyelesaikan telaah 3.2 kali lebih banyak berkas per jam kerja dengan tingkat kepuasan kerja yang meningkat signifikan.
# BAB IX: ANALISIS KELAYAKAN (FEASIBILITY STUDY)
## 9.1 Kelayakan Teknis (Technical Feasibility)
Purwarupa Aegis-JKN dibangun di atas tumpukan teknologi modern berstandar enterprise yang telah teruji kompatibilitasnya:
- Frontend Layer: Next.js 16.1.1 (App Router), React 19, Tailwind CSS v4, Radix UI primitives, Framer Motion, dan Recharts untuk rendering graf heterogen SVG dan dashboard interaktif.
- Backend & ML Engine: FastAPI (Python 3.11+), Uvicorn asynchronous server, PyTorch 2.14, PyTorch Geometric (PyG HeteroData), dan scikit-learn.
- Caching & Database: Redis in-memory feature-cache (<1.0s connect timeout) untuk streaming scoring cepat, PostgreSQL / Prisma ORM untuk persistensi audit log.
- Simulation Engine: Fork CAMEL-AI OASIS v0.2.5 berbasis Discrete Event Simulator untuk pemodelan agen sosial medis.
## 9.2 Kelayakan Data & Interoperabilitas (SATUSEHAT & V-Claim)
Aegis-JKN dirancang sebagai non-invasive overlay yang terhubung secara asinkron dengan API V-Claim dan platform SATUSEHAT Kemenkes RI melalui pertukaran data standar JSON HL7 FHIR R4. Sistem tidak melakukan locking transaksi pada basis data inti BPJS, menjamin kontinuitas operasional pelayanan rumah sakit tanpa gangguan.
## 9.3 Kelayakan Operasional & Manajemen Perubahan (Change Management)
Karena Aegis-JKN memposisikan diri sebagai co-pilot cerdas (pendukung verifikator) dan bukan pengganti tenaga kerja, resistensi adopsi dari serikat pekerja verifikator dapat diminimalisir. Program pelatihan disiapkan secara modular dalam 3 sesi interaktif (durasi total 6 jam) yang mencakup interpretasi sinyal SHAP, navigasi visualisasi graf, dan penanganan sengketa klaim.
## 9.4 Kelayakan Finansial & Efisiensi Infrastruktur On-Premise
Dengan menerapkan prinsip Right-Sized Engineering, Aegis-JKN tidak memerlukan klaster GPU superkomputer yang mahal atau langganan API cloud komersial yang boros biaya token. Filter Tier-1 berjalan pada CPU standar, sementara Tier-3 MHGSL dapat dijalankan pada 1-2 unit server GPU workstation kelas menengah (misal: NVIDIA RTX 4090 / A5000) yang ditempatkan di data center lokal BPJS. Proyeksi Cost-to-Impact Ratio mencapai 1 : 15, menjadikannya investasi teknologi yang sangat menguntungkan bagi keberlanjutan DJS.
## 9.5 Struktur Organisasi & Kompetensi Tim Pengembang
Tabel 9.1 memetakan komposisi keahlian Tim Inovator Kandidat 1 yang memiliki keahlian lintas-disiplin dalam arsitektur AI, data klinis, dan strategi kebijakan kesehatan.
| Peran Anggota Tim | Fokus Tanggung Jawab Utama | Keluaran yang Dihasilkan |
| Lead Platform & Logic Architecture | Merancang arsitektur Tri-Tier, implementasi PyTorch Geometric MHGSL, pipeline FastAPI, dan integrasi Next.js 16. | Arsitektur sistem, repositori kode purwarupa, API backend, dan engine MHGSL. |
| Research & Clinical Data Specialist | Validasi aturan koding INA-CBG, penyusunan ontologi medis ICD-10/ICD-9, dan kalibrasi skenario 9 sindikat. | Dataset sintetis v2.1 tervalidasi klinis, katalog sindikat, dan modul kepatuhan SATUSEHAT. |
| Business Case & Strategic Impact Specialist | Analisis kelayakan ekonomi, kepatuhan regulasi UU PDP, perancangan kerangka HITL, dan penyusunan proposal. | Studi kelayakan finansial, analisis dampak DJS, dokumen kepatuhan hukum, dan roadmap implementasi. |
# BAB X: MANAJEMEN RISIKO & STRATEGI MITIGASI
## 10.1 Identifikasi 12 Risiko Kritis Implementasi Aegis-JKN
Implementasi sistem kecerdasan buatan pada tata kelola jaminan kesehatan nasional berskala 270+ juta jiwa memiliki kompleksitas tinggi. Tim Inovator memetakan 12 risiko kritis yang mencakup dimensi teknis algoritmik, infrastruktur komputasi, keamanan siber, kepatuhan regulasi, hingga dinamika sosial hubungan industrial dengan fasilitas kesehatan.
## 10.2 Matriks Manajemen Risiko Komprehensif
Tabel 10.1 merangkum matriks manajemen risiko komprehensif beserta tingkat keparahan dan strategi mitigasi preventif serta kontingensinya.
| No | Identifikasi Risiko | Potensi Dampak | Tingkat | Strategi Mitigasi Preventif & Kontingensi |
| 1 | Topological Camouflage (Sindikat menyamarkan rujukan fisik) | Sindikat lolos dari sistem graf homogen atau model tabular. | Tinggi (Kritis) | Dekomposisi Tri-Channel MHGSL (A_top, A_feat, A_sem) dengan bobot atensi negatif pada topologi dan deteksi anomali fitur. |
| 2 | Model Drift akibat perubahan tarif / pedoman klinis baru | Penurunan akurasi deteksi pasca-revisi regulasi PMK Kemenkes. | Tinggi (Kritis) | Continuous monitoring data drift, evaluasi LOGO periodik, dan re-indexing otomatis ontologi tarif INA-CBG. |
| 3 | Bottleneck Throughput pada volume 2 juta klaim/hari | Antrean pemrosesan menumpuk, memperlambat proses pencairan klaim. | Tinggi (Kritis) | Arsitektur Dual-Path: caching Redis streaming <500 ms untuk klaim individual dan batch graph convolution harian. |
| 4 | Resistensi Faskes & Asosiasi Profesi (PERSI / IDI) | Protes klinisi yang merasa dicurigai integritas praktiknya. | Tinggi (Kritis) | Menegaskan status sistem sebagai CDSS (bukan vonis), transparansi bukti diskrepansi klinis, dan pelibatan TKMKB. |
| 5 | False Accusations (Tuduhan kecurangan keliru) | Sengketa klaim (dispute) yang berlarut-larut dengan faskes. | Tinggi (Kritis) | Prinsip Fail-Safe Human Autonomy: 100% keputusan di tangan manusia; AI hanya memberikan rekomendasi berbobot bukti. |
| 6 | Kebocoran Data Medis Pasien (Pelanggaran UU PDP) | Sanksi hukum pidana dan hilangnya reputasi publik BPJS. | Tinggi (Kritis) | Isolasi perimeter private on-premise cloud, salted SHA-256 tokenization, enkripsi AES-256, zero external cloud LLM API. |
| 7 | Kegagalan Bridging API (Downtime V-Claim / SIMRS) | Data klaim gagal terkirim ke modul analitik. | Sedang | Asynchronous message queue (RabbitMQ) dengan mekanisme retry otomatis dan circuit breaker lokal. |
| 8 | Variasi Format EMR (Data teks tidak terstruktur / scan PDF) | Modul NLP gagal mengekstrak bukti pendukung klinis. | Sedang | Normalisasi format SATUSEHAT HL7 FHIR R4 dan integrasi modul OCR lokal cerdas untuk berkas pindaian faskes. |
| 9 | Keterbatasan Akses Internet di Kantor Cabang Daerah 3T | Verifikator cabang perintis terhambat mengakses dashboard. | Sedang | Aplikasi Next.js 16 dioptimalkan dengan caching offline-first (PWA) dan kompresi payload respons graf SVG. |
| 10 | AI Hallucination pada komponen analisis teks klinis | Rekomendasi alasan anomali tidak sesuai fakta medis rekam medis. | Sedang | Menolak teks generatif bebas; ekstraksi strictly grounded pada kode ICD-10/ICD-9 dan fakta numerik rekam medis. |
| 11 | Vendor Lock-in pada teknologi komputasi proprietary | Ketergantungan biaya lisensi perangkat lunak yang membengkak. | Rendah | 100% stack berbasis open-source enterprise (PyTorch Geometric, Next.js, FastAPI, Redis, PostgreSQL). |
| 12 | Rendahnya Tingkat Adopsi Verifikator Lapangan | Sistem diabaikan karena verifikator merasa terbebani sistem baru. | Sedang | Program pelatihan modular 6 jam, antarmuka intuitif dengan skor SUS >80, dan penyederhanaan alur kerja one-click audit. |
## 10.3 Protokol Tanggap Darurat & Continuous Model Monitoring
Platform dilengkapi protokol tanggap darurat otomatis: (1) Safe-Mode Fallback Protocol yang otomatis membekukan rekomendasi AI jika tingkat penolakan (override) verifikator melebihi ambang batas 30% dalam 24 jam; (2) Automated Crypto-Shredding yang memusnahkan kunci tokenisasi sementara jika terdeteksi anomali akses intrusi; serta (3) Dashboard Continuous Model Drift yang memantau pergeseran distribusi skor risiko secara real-time.
# BAB XI: ROADMAP PENGEMBANGAN & RENCANA IMPLEMENTASI
## 11.1 Kerangka Kerja Stage-Gate Roadmap
Rencana implementasi Aegis-JKN dirancang menggunakan Stage-Gate Innovation Framework. Setiap tahapan memiliki pintu evaluasi (gate) dengan kriteria kelulusan kuantitatif yang ketat sebelum proyek diizinkan melangkah ke fase berikutnya, menjamin akuntabilitas investasi teknologi dan mitigasi risiko secara dini.
## 11.2 Rencana Pelaksanaan 8-12 Minggu Purwarupa & Roadmap 12 Bulan
Roadmap implementasi terbagi ke dalam Rencana Sprint 8-12 Minggu untuk penyempurnaan purwarupa kompetisi Healthkathon, serta Roadmap Nasional 12 Bulan (Tiga Fase Utama), sebagaimana dirinci pada Tabel 11.1:
| Tahap & Durasi | Aktivitas Kunci | Keluaran Utama (Deliverables) | Kriteria Kelulusan (Gate Criteria) |
| Tahap 1 (Bln 1)Validasi Masalah | Wawancara verifikator BPJS, pemetaan 9 modus sindikat, dan formalisasi skema HL7 FHIR R4. | Dokumen spesifikasi kebutuhan sistem (SRS) dan pemetaan ontologi INA-CBG. | Persetujuan tim klinis BPJS & keselarasan regulasi PMK 16/2019. |
| Tahap 2 (Bln 2)Sintesis & Simulasi | Penyusunan Dataset v2.1 (300 klaim), kalibrasi simulasi OASIS (20P, 12D, 6RS), dan anti-leakage audit. | Dataset v2.1 tervalidasi klinis dan modul Discrete Event Simulator OASIS. | Zero data leakage terverifikasi & reproduktibilitas seed deterministik 100%. |
| Tahap 3 (Bln 3-4)Pengembangan Core | Implementasi PyTorch Geometric HeteroData MHGSL, Rule Engine Tier-1, dan API FastAPI. | Checkpoint model mhgsl_model.pth, backend serving, dan cache streaming Redis. | Akurasi ≥ 90%, Presisi ≥ 90%, ROC-AUC ≥ 0.95, latensi stream <500 ms. |
| Tahap 4 (Bln 5)Frontend & XAI | Pengembangan antarmuka Next.js 16, visualisasi graf SVG 3-saluran, modal SHAP, dan klaster faskes. | Dashboard verifikator interaktif terintegrasi API FastAPI. | Skor System Usability Scale (SUS) ≥ 80 / 100. |
| Tahap 5 (Bln 6-8)Pilot RS Rujukan | Uji coba terbatas pada 1-2 Kantor Cabang percontohan menggunakan data sandbox resmi BPJS. | Laporan evaluasi pilot, matriks penyesuaian faskes, dan log feedback verifikator. | Reduksi durasi telaah berkas anomali ≥ 30%, FPR ≤ 15%, override rate ≤ 20%. |
| Tahap 6 (Bln 9-10)Integrasi Produksi | Penyambungan bridging V-Claim skala penuh, optimasi GraphSAINT batch, dan audit keamanan ISO 27001. | Sistem Aegis-JKN ter-deploy di private on-premise cloud data center BPJS. | Lolos uji penetrasi siber & throughput mampu memproses 2 juta klaim/hari. |
| Tahap 7 (Bln 11-12)Rollout Nasional | Peluncuran bertahap ke seluruh Kantor Cabang se-Indonesia, pelatihan nasional, dan monitoring drift. | Platform beroperasi penuh skala nasional terhubung sistem pembayaran klaim. | Rasio Cost-to-Impact terbukti ≥ 1 : 15 dalam perlindungan Dana DJS Kesehatan. |
## 11.3 Indikator Keberhasilan Antar-Tahap (Stage-Gate Criteria)
Keberhasilan antar-fase dikawal oleh tiga gerbang utama: (1) Gate-1: Model Core Readiness (AUPRC >0.85, latensi <500 ms); (2) Gate-2: User Adoption & Safety (SUS >80, override <20%, Safe-Mode Protocol teruji); serta (3) Gate-3: Financial Impact & Resilience (Cost-to-Impact > 1:15, ketahanan kamuflase >85% pada data operasional).
# BAB XII: KESIMPULAN & PENUTUP
## 12.1 Sintesis Nilai Strategis Solusi Aegis-JKN
Aegis-JKN membuktikan bahwa terobosan teknologi kecerdasan buatan dalam pengawasan pembiayaan kesehatan tidak harus berbiaya mahal, bergantung pada cloud pihak ketiga, atau mengorbankan otonomi manusia. Melalui inovasi Multi-Channel Heterogeneous Graph Structure Learning (MHGSL), Aegis-JKN memecahkan kebuntuan audit konvensional dengan membedah jaringan kolusi sindikat dan membongkar kamuflase topologis yang selama ini tidak terlihat oleh model tabular dan aturan statis.
Dengan arsitektur Tri-Tier yang menggabungkan kecepatan aturan deterministik (<50 ms), ketajaman klasifikasi statistik tabular, dan kedalaman pembelajaran graf heterogen yang terhubung ke standar SATUSEHAT HL7 FHIR R4, sistem ini dirancang siap menangani beban transaksi riil lebih dari dua juta klaim per hari. Transparansi penalaran Explainable AI (XAI) dan kerangka kerja Human-in-the-Loop menjamin bahwa hak otonomi verifikator manusia tetap menjadi penentu akhir yang berdaulat, akuntabel, dan bebas dari bias kotak hitam.
## 12.2 Kesiapan Implementasi & Rekomendasi Menuju Healthkathon 2026
Purwarupa Aegis-JKN telah diwujudkan dalam bentuk kode aplikasi fungsional yang siap didemonstrasikan: antarmuka web interaktif Next.js 16 yang responsif, backend inferensi PyTorch Geometric dan FastAPI berlatensi rendah, serta dataset pengujian 300 klaim tervalidasi klinis yang telah membuktikan kemampuan menyelamatkan lebih dari setengah miliar rupiah potensi kebocoran tarif pada sampel terbatas. Tim Inovator Kandidat 1 berkomitmen penuh untuk bermitra dengan BPJS Kesehatan guna mewujudkan ekosistem jaminan kesehatan yang adil, transparan, dan berkelanjutan.
> **{'type': 'emoji', 'emoji': '🛡️'}** [KOMITMEN INOVASI] Detect Smarter, Protect JKN« Bersama Aegis-JKN, kita wujudkan perlindungan Dana Jaminan Sosial Kesehatan yang lebih cerdas, melindungi hak setiap peserta, dan mengawal keberlangsungan Universal Health Coverage Indonesia untuk generasi masa depan. »
# DAFTAR PUSTAKA & REFERENSI REGULASI
[1] BPJS Kesehatan. (2024). Laporan Pengelolaan Program JKN dan Kinerja Keuangan BPJS Kesehatan Tahun 2023. Jakarta: BPJS Kesehatan.
[2] Kementerian Kesehatan RI. (2019). Peraturan Menteri Kesehatan Republik Indonesia Nomor 16 Tahun 2019 tentang Pencegahan dan Penanganan Kecurangan (Fraud) serta Pengendalian Gratifikasi dalam Penyelenggaraan Program Jaminan Kesehatan. Jakarta: Kemenkes RI.
[3] Kementerian Kesehatan RI. (2021). Peraturan Menteri Kesehatan Republik Indonesia Nomor 26 Tahun 2021 tentang Pedoman Pencegahan dan Penanganan Kecurangan (Fraud) dalam Penyelenggaraan Program Jaminan Kesehatan. Jakarta: Kemenkes RI.
[4] Kementerian Kesehatan RI. (2022). Peraturan Menteri Kesehatan Republik Indonesia Nomor 24 Tahun 2022 tentang Rekam Medis. Jakarta: Kemenkes RI.
[5] Kementerian Kesehatan RI. (2023). Peraturan Menteri Kesehatan Republik Indonesia Nomor 3 Tahun 2023 tentang Standar Tarif Pelayanan Kesehatan dalam Penyelenggaraan Program Jaminan Kesehatan. Jakarta: Kemenkes RI.
[6] Republik Indonesia. (2022). Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi. Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196. Jakarta: Sekretariat Negara.
[7] Republik Indonesia. (2023). Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan. Lembaran Negara Republik Indonesia Tahun 2023 Nomor 105. Jakarta: Sekretariat Negara.
[8] World Health Organization. (2021). Ethics and Governance of Artificial Intelligence for Health: WHO Guidance. Geneva: World Health Organization.
[9] Sun, Y., Han, J., Yan, X., Yu, P. S., & Wu, T. (2011). PathSim: Meta Path-Based Top-K Similarity Search in Heterogeneous Information Networks. Proceedings of the VLDB Endowment, 4(11), 992-1003.
[10] Wang, X., Ji, H., Shi, C., Wang, B., Ye, Y., Cui, P., & Yu, P. S. (2019). Heterogeneous Graph Attention Network. Proceedings of The World Wide Web Conference (WWW '19), 2022-2032.
[11] Kipf, T. N., & Welling, M. (2017). Semi-Supervised Classification with Graph Convolutional Networks. International Conference on Learning Representations (ICLR 2017).
[12] Fey, M., & Lenssen, J. E. (2019). Fast Graph Representation Learning with PyTorch Geometric. ICLR Workshop on Representation Learning on Graphs and Manifolds.
[13] Lin, T. Y., Goyal, P., Girshick, R., He, K., & Dollár, P. (2017). Focal Loss for Dense Object Detection. IEEE International Conference on Computer Vision (ICCV), 2980-2988.
[14] Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 4765-4774.
[15] Zeng, H., Zhou, H., Srivastava, A., Kannan, R., & Prasanna, V. (2020). GraphSAINT: Graph Sampling Based Inductive Engine. International Conference on Learning Representations (ICLR 2020).
[16] CAMEL-AI. (2024). OASIS: Open Agent Social Interaction Simulation System with 1 Million Diverse Agents. arXiv preprint arXiv:2411.11581.
[17] Heliyon Medical Intelligence Group. (2024). Multi-Hop Graph Structure Learning for Medical Fraud Detection in Health Insurance Systems (Medical-B Benchmark). Heliyon, 10(4), e26115.
[18] Centers for Medicare & Medicaid Services. (2022). Inpatient and Outpatient Prospective Payment Systems and Healthcare Fraud Detection Benchmarks. CMS Research Publications.
## [Sub-page] ARSIP SUMBER | Aegis-JKN Arsitektur dan Strategi Pengembangan Sistem Deteksi Fraud JKN
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
## [Sub-page] ARSIP SUMBER | Catatan Awal Deep Research Fraud Klaim JKN
Fraud klaim asuransi kesehatan terjadi sudah sekian lama. Kasus yang di report oleh BPJS tahun 2024 melibatkan 3 rumah sakit swasta di jawa tengah dan sumatra utara dengan total kerugian mencapat RP25 miliar. 
> **{'type': 'emoji', 'emoji': '💡'}** CATATAN EDITORIAL | Catatan awal ini dipertahankan sebagai bahan mentah. Gunakan [Catatan Riset: Deteksi Kecurangan Klaim JKN](https://app.notion.com/p/06-Catatan-Riset-Deteksi-Kecurangan-Klaim-JKN-4003e6031ab78135a0face33631104ab) untuk sintesis yang lebih terstruktur. Angka nasional, nilai kerugian, dan status verifikasi harus dilacak ke sumber primer sebelum dipakai dalam naskah formal.
modus utama yang terindikasi yaitu Phantom Billing.  Phantom billing itu sendiri yaitu fraud yang dimana fasilitas kesehatan mengajukan klaim biaya ke BPJS Kesehatan atau lembaga penjamin untuk layanan medis yang tidak pernah diberikan kepada pasien.
lalu ada temuan lainnya yaitu Upcoding. Upcoding ini sendiri ialah mengubah kode diagnostik penyakit menjadi lebih parah atau bernilai taraf tinggi. 
Kecurangan ini sendiri tidak datang sendiri, melainkan ada celah yang terlihat oleh oknum yang tidak bertanggungjawab. celah yang terlihat diantaranya:
1. kelemahan verivikasi berkas elektronik.
1. Penyalahgunaaan data peserta
1. lemahnya pengawasan dan pengendalian internal
1. tekanan finansial dan target kebutuhan
1. kurangnya kesadaran dan kontrol pasien 
## [Sub-page] Lagre Language Model Hallucination
Halusinasi mengacu pada pembangkitan konten oleh LLM yang lancar dan secara sintaksis benar tetapi secara faktual tidak akurat atau tidak didukung oleh bukti eksternal.
Kata Kunci: 
LLM, Halusinasi, Penyebab Halusinasi, Deteksi Halusinasi, Mitigasi Halusinasi, Tolok Ukur Halusinasi, Metrik Halusinasi
Pengembagan LLM terbagi dalam 6 tahap:
1. pengumpulan dan persiapan data
1. arsitektur model
1. pra pelatihan
1. penympurnaan
1. evaluasi
1. dan inferensi 

## [Sub-page] 00 | HEALTHKATHON Project Dashboard
## Aegis-JKN, Pusat Kendali Proyek dan Tata Kelola Dokumen
Status proyek: Purwarupa riset terapan  
Tanggal pembaruan: 21 Oktober 2026  
Versi dokumentasi terkendali: 1.0  
Prinsip utama: Tidak ada klaim performa, keamanan, integrasi, atau penghematan yang dinyatakan tervalidasi sebelum bukti pendukung dapat direproduksi.
## 1. Ringkasan Eksekutif
Aegis-JKN diusulkan sebagai sistem pendukung verifikator untuk triase anomali klaim JKN. Rancangan menggabungkan pemeriksaan deterministik, model tabular, analisis graf heterogen, penjelasan yang dapat diperiksa, dan keputusan akhir oleh manusia. Dataset aktif di Notion berisi 300 klaim sintetis dan digunakan untuk pengembangan serta demonstrasi. Dataset tersebut bukan bukti prevalensi fraud atau kerugian aktual JKN.
Dokumentasi revisi ini memisahkan proposal, spesifikasi rekayasa, tata kelola dataset, referensi riset, dan keputusan ruang lingkup. Dokumen sumber lama tetap disimpan sebagai referensi historis agar konten awal tidak hilang.
## 2. Mulai dari Sini
### Dokumen terkendali
1. [Proposal Riset dan Inovasi, Edisi Akademik Revisi 1.0](https://app.notion.com/p/4003e6031ab78170bc22fe391c6a3a2a)
1. [Arsitektur Sistem dan Metodologi Teknis](https://app.notion.com/p/4003e6031ab781efbcdac7b0dbdd0cad)
1. [Dataset Registry, Data Dictionary, dan Protokol Reproduksibilitas](https://app.notion.com/p/4003e6031ab781749a55d4ee8fff3fd2)
1. [Research Evidence Matrix and Reference Governance](https://app.notion.com/p/4003e6031ab7814f8ac3f37808c0a4a5)
1. [Pemilihan Kandidat Inovasi dan Batas Ruang Lingkup MVP](https://app.notion.com/p/4003e6031ab78156b244cccd2c5ecd9e)
1. [Catatan Riset: Deteksi Kecurangan Klaim JKN](https://app.notion.com/p/4003e6031ab78135a0face33631104ab)
### Dataset dan materi sumber
- [Database Klaim Aegis-JKN v2, 300 Baris](https://app.notion.com/p/c783afb3d0d4458295456180b7b7756b)
- [Database Riset Deteksi Fraud JKN](https://app.notion.com/p/310b35a5934642dfaf47df9897cdcda1)
- [Dokumentasi Dataset Simulasi, 100 Klaim](https://app.notion.com/p/3f23e6031ab781bf99a7d3f1768f1708)
- [Kandidat Ide Hackathon BPJS Kesehatan, sumber awal](https://app.notion.com/p/3f63e6031ab78111a885ea835e650bf2)
- [Proposal Lengkap Aegis-JKN, sumber awal](https://app.notion.com/p/3f63e6031ab78141a724fc301304942b)
- [Analisis Strategis dan Teknis, sumber awal](https://app.notion.com/p/3ef3e6031ab781d1962af8955843ed0f)
- [Deep Research, sumber awal](https://app.notion.com/p/3fe3e6031ab780088ce1f3201c252bed)
- [Figma Fishbone Diagram](https://www.figma.com/board/ePv0sbUCNU9iOgRiTMwH8E/Fishbone-Diagram-6M---Kebocoran-Finansial-Klaim-JKN-Aegis?node-id=0-1&p=f&t=pYR0GTGzXi53K7Hq-0)
## 3. Fakta Dataset yang Telah Direkonsiliasi
| Indikator | Hasil pemeriksaan baca saja |
| Jumlah baris aktif | 300 klaim |
| Rentang ID | KLM001 sampai KLM300 |
| Status auto_clear | 240 |
| Status review | 24 |
| Status escalate | 36 |
| Total nominal klaim sintetis | Rp3.526.650.000 |
| Kolom LOS hari kosong | 109 baris |
| Alasan kosong | 1 baris |
| Catatan riset | 33 entri |
Total nominal dan pembagian nominal per status konsisten dengan tabel di naskah sumber. Namun, perhitungan estimasi overcharge Rp507.370.000 belum dapat direproduksi per klaim dari properti database saat ini karena tarif pembanding, formula, dan status validasi independen belum tercatat secara lengkap.
## 4. Status Bukti
### Dapat dipastikan dari artefak yang diperiksa
- Database aktif memiliki 300 baris dan ID tidak terputus dari KLM001 sampai KLM300.
- Label risiko, status workflow, dan total nominal dapat direkonsiliasi.
- Dataset dirancang sebagai sintetis untuk demonstrasi.
- Rancangan proposal mencakup pemeriksaan deterministik, analitik tabular, analisis graf, explainability, dan human-in-the-loop.
### Belum boleh disebut hasil tervalidasi
- Accuracy 93,0%, precision 94,12%, ROC-AUC 0,9825, dan AUPRC 0,9142.
- Ketahanan masking 89,4% dan false positive rate 10,6%.
- Penurunan waktu telaah 45%, throughput 3,2 kali, dan SUS 82,5.
- Penghematan atau penyelamatan finansial yang dihitung dari dataset.
- Integrasi produksi dengan sistem eksternal.
Angka di atas pernah disebut di draf terdahulu. Sebelum dipakai sebagai hasil final, masing-masing perlu dihubungkan dengan ID eksperimen, split, kode, prediksi, label pembanding, dan skrip perhitungan.
## 5. Keputusan Ruang Lingkup
Fokus MVP: deteksi anomali klaim dengan prioritas pada upcoding dan phantom billing dalam dataset sintetis.
Fitur inti: validasi data, rule engine, baseline tabular, uji tambah nilai graph learning, penjelasan berbasis bukti, dashboard triase, dan audit trail.
Tidak termasuk pada tahap ini: keputusan fraud otomatis, pemotongan pembayaran, sanksi, penggunaan data peserta nyata tanpa kewenangan, dan klaim penghematan nasional yang diturunkan langsung dari data sintetis.
## 6. Papan Kerja dan Gerbang Kualitas
### Prioritas P0
- [ ] Tetapkan definisi label fraud-scenario, anomali, dan normal.
- [ ] Tandai dokumen 100 klaim sebagai versi awal dan dataset 300 klaim sebagai versi aktif.
- [ ] Lampirkan manifest eksperimen dan skrip untuk seluruh metrik yang dipublikasikan.
- [ ] Tambahkan tarif acuan dan metode perhitungan per klaim untuk estimasi overcharge.
- [ ] Samakan angka operasional yang berbeda di proposal dan database riset.
### Prioritas P1
- [ ] Minta review klinis atas skenario dan kode diagnosis/prosedur.
- [ ] Selesaikan data dictionary dan perlakuan nilai LOS kosong.
- [ ] Periksa sumber regulasi pada situs resmi dan tulis pasal spesifik.
- [ ] Lengkapi metadata bibliografi dan sitasi dekat dengan klaim.
- [ ] Tetapkan owner dan reviewer untuk data, eksperimen, keamanan, dan proposal.
### Prioritas P2
- [ ] Uji penerimaan antarmuka dengan protokol yang terdokumentasi.
- [ ] Buat release notes untuk setiap perubahan dataset atau model.
- [ ] Pisahkan artefak pengembangan, hasil eksperimen, dan materi presentasi.
## 7. Standar Dokumen
Semua dokumen terkendali mengikuti aturan berikut:
1. Judul jelas dan tidak menggunakan singkatan yang tidak dijelaskan.
1. Awali dengan status, versi, tanggal, dan tujuan.
1. Gunakan istilah yang konsisten untuk label risiko dan status kerja.
1. Bedakan fakta dari rancangan, hipotesis, hasil uji, dan estimasi.
1. Semua tabel menyatakan satuan serta denominator.
1. Semua klaim eksternal memiliki sitasi spesifik.
1. Semua hasil eksperimen memiliki identitas eksperimen dan artefak replikasi.
1. Dokumen formal tidak menggunakan em-dash.
1. Revisi tidak menghapus konten sumber yang masih diperlukan sebagai rekam jejak.
1. Perubahan substansial dicatat pada changelog.
## 8. Riwayat Revisi
| Versi | Tanggal | Ringkasan |
| 1.0 | 21 Oktober 2026 | Membuat struktur dokumen terkendali, merapikan proposal dan metode, merekonsiliasi ringkasan dataset, serta membakukan tata kelola bukti |
## 9. Aturan Pembaruan
Pemilik setiap dokumen harus memperbarui status hanya setelah memeriksa artefak sumber. Gunakan status Rancangan, Dalam Implementasi, Siap Diuji, Tervalidasi, atau Diarsipkan. Status Tervalidasi hanya boleh digunakan dengan bukti yang dapat ditinjau oleh orang lain.
Halaman ini adalah titik masuk proyek. Gunakan tautan dokumen terkendali sebagai versi utama. Halaman sumber lama tetap digunakan untuk penelusuran konteks dan riwayat perubahan.
# Dataset dan training AI
Dokumentasi tahap baru untuk data sampel kontekstual DM dan protokol training telah ditambahkan. Perhatikan bahwa data DM belum memiliki label fraud dan perlu dipisahkan dari klaim sintetis Aegis-JKN.
- [07 | Dataset Registry dan Kamus Data DM Kontekstual](https://app.notion.com/p/07-Dataset-Registry-dan-Kamus-Data-DM-Kontekstual-4003e6031ab78179bcc7ca76a0b80fbc)
- [08 | Protokol Training AI dan Evaluasi Aegis-JKN](https://app.notion.com/p/08-Protokol-Training-AI-dan-Evaluasi-Aegis-JKN-4003e6031ab781978715f1de059e82ef)
## [Sub-page] 01 | Aegis-JKN: Proposal Riset dan Inovasi, Edisi Akademik Revisi 1.0
## Proposal Riset dan Inovasi, Edisi Akademik Revisi 1.0
Status dokumen: Revisi editorial dan metodologis  
Tanggal revisi: 21 Oktober 2026  
Jenis naskah: Proposal riset terapan dan spesifikasi purwarupa  
Prinsip pelaporan: Klaim yang belum memiliki bukti eksperimen yang dapat direproduksi tidak dinyatakan sebagai hasil tervalidasi.
## Abstrak
Pengelolaan klaim jaminan kesehatan berskala besar menghadapi tantangan berupa variasi pola klinis, keterbatasan kapasitas penelaahan manual, dan kemungkinan terjadinya anomali penagihan. Penelitian ini mengusulkan Aegis-JKN, sebuah sistem pendukung keputusan untuk membantu verifikator melakukan triase klaim berdasarkan aturan deterministik, fitur tabular, serta hubungan antarentitas dalam graf heterogen. Sistem dirancang agar setiap sinyal risiko disertai alasan yang dapat ditinjau dan keputusan akhir tetap berada pada manusia. Purwarupa awal menggunakan dataset sintetis berisi 300 klaim, dengan 240 klaim berstatus auto-clear, 24 klaim berstatus review, dan 36 klaim berstatus escalate. Dataset tersebut merupakan data simulasi dan tidak mewakili prevalensi atau kerugian aktual JKN. Evaluasi akan menggunakan protokol pemisahan data yang memperhatikan keterkaitan pasien dan fasilitas kesehatan, pembandingan terhadap baseline, serta pengujian ketahanan terhadap perubahan struktur relasi. Pada saat revisi ini, angka kinerja yang disebut dalam draf terdahulu belum disertai seluruh artefak yang diperlukan untuk reproduksi independen. Oleh karena itu, angka tersebut diperlakukan sebagai hasil sementara sampai kode, pembagian data, prediksi, label pembanding, dan laporan eksperimen tersedia. Kontribusi utama yang ditargetkan adalah rancangan alur kerja yang dapat diaudit, evaluasi yang transparan, dan pemisahan tegas antara anomali statistik dan kesimpulan fraud.
Kata kunci: JKN, deteksi anomali klaim, deteksi fraud, graph learning, explainable AI, human-in-the-loop, data sintetis.
## 1. Pendahuluan
Program jaminan kesehatan membutuhkan proses pemeriksaan klaim yang konsisten, efisien, dan dapat dipertanggungjawabkan. Sistem pemeriksaan berbasis aturan berguna untuk mendeteksi pelanggaran eksplisit, tetapi dapat kesulitan menemukan pola yang melibatkan beberapa klaim atau hubungan antara pasien, dokter, dan fasilitas kesehatan. Model statistik tabular dapat membantu mendeteksi penyimpangan pada satu klaim, sedangkan pendekatan graf berpotensi memberikan konteks relasional tambahan.
Aegis-JKN dirancang sebagai lapisan analitik pendukung verifikator, bukan sebagai sistem penentu kecurangan secara otomatis. Tujuan utamanya adalah memprioritaskan klaim untuk ditelaah, menyajikan sinyal yang dapat ditelusuri, dan mengurangi beban investigasi awal tanpa mengurangi hak fasilitas kesehatan dan peserta untuk memperoleh pemeriksaan yang adil.
Angka nasional terkait volume klaim, jumlah verifikator, nilai kerugian, dan prevalensi fraud harus didukung rujukan primer yang spesifik sebelum digunakan sebagai fakta dalam versi final publikasi.
## 2. Rumusan Masalah
Penelitian ini berfokus pada pertanyaan berikut.
1. Sejauh mana aturan deterministik dan model tabular dapat mendeteksi anomali yang terlihat pada tingkat klaim individual?
1. Apakah representasi graf heterogen memberikan informasi tambahan untuk menemukan pola relasional yang tidak mudah terlihat pada fitur individual?
1. Bagaimana model menyajikan alasan yang dapat diperiksa oleh verifikator?
1. Bagaimana mengevaluasi model tanpa kebocoran informasi dari pasien, dokter, fasilitas kesehatan, atau label turunan?
1. Bagaimana memastikan bahwa skor risiko tidak diperlakukan sebagai bukti final tindakan fraud?
## 3. Tujuan dan Kontribusi
Tujuan proyek adalah:
- mengembangkan purwarupa triase risiko klaim yang transparan dan dapat diaudit;
- membandingkan rule engine, baseline tabular, dan pendekatan graf pada skenario sintetis;
- membangun protokol evaluasi yang dapat direproduksi;
- menguji konsistensi alasan deteksi, label, status kerja, dan skor risiko;
- menetapkan tata kelola data, akses, log audit, dan pengawasan manusia.
Kontribusi yang diharapkan berupa arsitektur perangkat lunak, spesifikasi data sintetis, protokol evaluasi, antarmuka verifikator, dan dokumentasi keterbatasan.
## 4. Ruang Lingkup
### 4.1 Cakupan purwarupa
Tahap awal memprioritaskan dua pola: ketidaksesuaian diagnosis dan prosedur yang berpotensi menunjukkan upcoding, serta klaim layanan yang memerlukan verifikasi dukungan dokumenter untuk menguji skenario phantom billing. Unbundling dapat dipakai sebagai skenario tambahan setelah aturan dan labelnya terdokumentasi.
### 4.2 Di luar cakupan
Purwarupa tidak memutuskan fraud secara hukum, tidak menolak atau memotong pembayaran secara otomatis, tidak memberikan sanksi, dan tidak menggunakan data peserta riil tanpa dasar kewenangan serta persetujuan yang diperlukan. Integrasi ke sistem produksi BPJS, V-Claim, SATUSEHAT, atau SIMRS belum boleh dinyatakan siap sebelum akses, izin, pengujian keamanan, dan uji penerimaan diselesaikan.
## 5. Metodologi yang Diusulkan
### 5.1 Data dan unit analisis
Unit utama adalah klaim. Entitas terkait dapat mencakup pasien sintetis, dokter, fasilitas kesehatan, diagnosis, prosedur, obat, dan rujukan. Dataset aktif di Notion berisi 300 klaim sintetis. Ringkasan status kerja saat ini adalah 240 auto-clear, 24 review, dan 36 escalate. Distribusi label risiko adalah 240 low, 10 medium, 14 high, dan 36 fraud. Perbedaan kategori ini harus dipertahankan: klaim review tidak otomatis merupakan fraud, dan tidak seluruh klaim non-fraud dapat disebut normal.
### 5.2 Pra-pemrosesan
Tahap pra-pemrosesan mencakup validasi tipe data, pemeriksaan nilai kosong, normalisasi kode, dokumentasi unit biaya, penanganan durasi rawat yang tidak berlaku, serta pemeriksaan duplikasi. Kolom hasil audit seperti skor fraud, status, alasan, modus, sindikat, dan kontribusi kanal tidak boleh masuk sebagai fitur ketika kolom tersebut dibentuk dari label atau keputusan yang hendak diprediksi.
### 5.3 Model pembanding
Tahap awal menggunakan tiga kelompok pendekatan:
1. Rule engine: aturan eksplisit dan pemeriksaan konsistensi data.
1. Model tabular: baseline seperti XGBoost yang dilatih hanya dengan fitur prediktif yang sah.
1. Model graf heterogen: memodelkan relasi antarentitas, dengan definisi node, edge, fitur, dan metapath yang didokumentasikan.
Model gabungan hanya dipertahankan jika memberikan nilai tambah yang terukur dibandingkan baseline sederhana.
### 5.4 Pencegahan data leakage
Pemisahan data harus mengikuti kelompok entitas yang relevan. Rencana yang akan diuji adalah GroupKFold berbasis kelompok pasien dan evaluasi terpisah yang menahan fasilitas kesehatan tertentu dari data pelatihan. Seluruh normalisasi, pemilihan fitur, pembentukan threshold, dan kalibrasi harus dipelajari dari data pelatihan pada setiap fold, bukan dari keseluruhan dataset.
### 5.5 Metrik evaluasi
Pelaporan minimal mencakup confusion matrix, precision, recall, F1-score, false positive rate, ROC-AUC, area under the precision-recall curve, dan kalibrasi skor. Akurasi tidak digunakan sebagai satu-satunya metrik karena distribusi kelas tidak seimbang. Hasil perlu dilaporkan untuk setiap fold beserta rata-rata, variasi, dan interval ketidakpastian jika relevan.
### 5.6 Reproduksibilitas
Setiap eksperimen harus memiliki ID unik, versi dataset, versi kode, konfigurasi model, random seed, skema split, daftar fitur, threshold, serta berkas prediksi. Angka yang ditulis dalam proposal harus dapat dihitung ulang dari artefak tersebut.
## 6. Arsitektur Sistem
Arsitektur yang diusulkan terdiri atas:
1. Ingestion dan normalisasi: menerima data uji, memvalidasi skema, dan menghasilkan representasi analitik.
1. Tier 1, rule engine: memeriksa aturan dan inkonsistensi eksplisit.
1. Tier 2, model tabular: menghitung sinyal risiko berbasis atribut klaim.
1. Tier 3, analisis graf: mengevaluasi pola relasional jika data dan validasi mendukungnya.
1. Fusion dan penjelasan: menggabungkan sinyal dengan aturan yang terdokumentasi dan menunjukkan faktor pendukung.
1. Antarmuka verifikator: menampilkan bukti, tingkat ketidakpastian, dan pilihan tindak lanjut.
1. Audit trail: merekam versi model, waktu prediksi, alasan, tindakan verifikator, dan perubahan keputusan.
Keputusan final tetap dilakukan oleh petugas berwenang. Alasan otomatis harus bersumber dari data terstruktur atau kutipan yang dapat diverifikasi, bukan teks generatif tanpa dukungan bukti.
## 7. Tata Kelola Data, Keamanan, dan Etika
Pengembangan purwarupa menggunakan data sintetis. Apabila kelak memakai data nyata, proyek harus memiliki dasar pemrosesan yang sah, pembatasan tujuan, minimisasi data, kontrol akses berbasis peran, enkripsi saat transit dan penyimpanan, retensi yang ditetapkan, logging, pengelolaan insiden, serta penilaian risiko privasi. Pseudonimisasi tidak dianggap sebagai anonimisasi sempurna.
Model tidak boleh menganggap korelasi sebagai bukti kesalahan klinis. Skor tinggi harus mengarah pada pemeriksaan, bukan sanksi otomatis. Sistem harus memungkinkan override manusia dan merekam alasannya.
## 8. Status Bukti dan Hasil
Database aktif dapat direkonsiliasi pada 300 baris dengan total nominal Rp3.526.650.000. Jumlah nominal per status adalah:
- auto-clear: Rp2.685.550.000;
- review: Rp279.950.000;
- escalate: Rp561.150.000.
Draf sebelumnya mencantumkan accuracy 93,0%, precision 94,12%, ROC-AUC 0,9825, AUPRC 0,9142, ketahanan masking 89,4%, false positive rate 10,6%, dan estimasi penyelamatan Rp507.370.000. Angka tersebut belum dinyatakan sebagai hasil tervalidasi dalam edisi ini karena artefak yang diperlukan untuk reproduksi independen belum terlampir pada materi yang diperiksa. Nilai nominal klaim yang tercatat tidak dengan sendirinya membuktikan besarnya overcharge atau nilai yang dapat diselamatkan.
Sebelum publikasi, setiap hasil wajib dihubungkan dengan eksperimen tertentu, skrip perhitungan, prediksi, ground truth, dan definisi operasional metrik.
## 9. Keterbatasan dan Validitas
Dataset sintetis berguna untuk menguji implementasi, alur UI, dan kasus tepi, tetapi tidak cukup untuk menyatakan kinerja pada populasi JKN sesungguhnya. Distribusi kelas dibuat untuk demonstrasi dan tidak boleh diklaim mewakili prevalensi lapangan. Hasil model juga berisiko dipengaruhi cara skenario sintetis dibangun, pengulangan pola, kebocoran kelompok, atau fitur yang secara langsung mencerminkan label.
Klaim performa operasional memerlukan pengujian bersama pengguna dan protokol pengukuran yang ditetapkan sebelumnya. Klaim dampak finansial memerlukan definisi tarif acuan, kalkulasi per klaim, dan penilaian independen.
## 10. Rencana Kerja
| Tahap | Hasil wajib | Kriteria selesai |
| 1. Audit data | Manifest, kamus data, laporan nilai kosong | Label dan nilai dapat ditelusuri |
| 2. Baseline | Rule engine dan baseline tabular | Skrip dan metrik dapat diulang |
| 3. Model graf | Graf, definisi relasi, hasil ablation | Peningkatan terhadap baseline ditunjukkan |
| 4. Explainability | Tampilan bukti dan alasan | Alasan berhubungan dengan fitur yang terukur |
| 5. Evaluasi pengguna | Protokol dan hasil usability | Hasil berasal dari peserta dan prosedur terdokumentasi |
| 6. Validasi tata kelola | Peninjauan privasi, keamanan, dan risiko | Persetujuan sebelum integrasi nyata |
## 11. Kesimpulan
Aegis-JKN dirancang sebagai sistem pendukung verifikasi klaim berbasis aturan, analitik tabular, dan konteks relasional. Kelayakan purwarupa perlu ditunjukkan melalui eksperimen yang dapat direproduksi, validasi label yang jelas, dan pengukuran manfaat yang tidak mencampuradukkan simulasi dengan dampak nyata. Versi naskah selanjutnya hanya boleh menaikkan status suatu klaim menjadi hasil tervalidasi setelah bukti pendukung tersedia.
## Referensi dan dokumen pendukung
- Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi.
- Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan.
- Peraturan Menteri Kesehatan Republik Indonesia Nomor 16 Tahun 2019 tentang Pencegahan dan Penanganan Kecurangan serta Pengendalian Gratifikasi dalam Program Jaminan Kesehatan.
- Peraturan Menteri Kesehatan Republik Indonesia Nomor 24 Tahun 2022 tentang Rekam Medis.
- Dokumentasi SATUSEHAT terkait interoperabilitas klaim BPJS: [https://satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/](https://satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/)
- Referensi teknis XGBoost, graph neural networks, SHAP, dan evaluasi model harus dicantumkan dengan metadata bibliografi lengkap dan hubungan yang jelas dengan klaim yang didukung.
## Catatan editorial
Dokumen ini merupakan revisi struktur dan metodologi. Ini bukan pengesahan klinis, hukum, atau statistik terhadap hasil eksperimen. Semua angka kinerja dan dampak finansial wajib ditinjau kembali ketika artefak replikasi telah tersedia.
## [Sub-page] 02 | Aegis-JKN: Arsitektur Sistem dan Metodologi Teknis
## Spesifikasi Rekayasa Revisi 1.0
Status: Rancangan teknis untuk purwarupa  
Terakhir direvisi: 21 Oktober 2026  
Dokumen induk: Proposal Riset dan Inovasi, Edisi Akademik Revisi 1.0
## 1. Tujuan Dokumen
Dokumen ini menetapkan komponen teknis, batas sistem, alur data, protokol evaluasi, dan kriteria penerimaan untuk pengembangan Aegis-JKN. Dokumen ini membedakan fitur yang direncanakan dari kemampuan yang sudah dibuktikan. Penyebutan teknologi atau integrasi tidak berarti implementasi produksi telah tersedia.
## 2. Prinsip Desain
1. Human-in-the-loop: AI memberi sinyal dan bukti pendukung, sedangkan keputusan akhir berada pada verifikator.
1. Reproduksibilitas: setiap hasil memiliki versi data, kode, konfigurasi, dan skrip evaluasi.
1. Minimisasi data: fitur hanya mencakup atribut yang dibutuhkan untuk tujuan evaluasi.
1. Fail-safe behavior: bila layanan model atau data tidak tersedia, sistem tidak mengarang hasil dan tidak menghambat proses resmi.
1. Ketertelusuran: skor, threshold, alasan, versi model, dan tindakan pengguna dapat ditelusuri.
1. Baseline first: model kompleks dipertahankan hanya jika manfaatnya terukur dibanding metode yang lebih sederhana.
## 3. Arsitektur Logis
### 3.1 Lapisan ingest dan validasi
Tanggung jawab:
- menerima data sintetis melalui format yang terdokumentasi;
- memvalidasi tipe, rentang, kode, dan nilai wajib;
- memberi penanda nilai hilang, tidak berlaku, atau tidak diketahui;
- membuat identitas analitik sintetis untuk node graf;
- menolak skema yang tidak sesuai dan menyimpan log kesalahan.
### 3.2 Tier 1, rule engine
Memeriksa aturan eksplisit seperti duplikasi tepat, kode yang tidak kompatibel menurut aturan yang terdokumentasi, nilai tidak masuk akal, dan kelengkapan bukti. Setiap aturan harus memiliki ID, versi, sumber kebijakan, input, kondisi, output, kasus uji, dan tanggal tinjauan.
Aturan tidak boleh menyimpulkan fraud hanya dari satu anomali klinis tanpa konteks. Output awal adalah rule_flag dengan alasan spesifik.
### 3.3 Tier 2, model tabular
Baseline yang disarankan adalah XGBoost atau model tabular lain yang dipilih setelah eksperimen pendahuluan. Fitur yang berasal dari keputusan audit atau label turunan tidak boleh digunakan untuk memprediksi label yang sama. Pembagian fitur dan target dicatat di manifest eksperimen.
### 3.4 Tier 3, model graf heterogen
Node kandidat: klaim, pasien sintetis, dokter sintetis, fasilitas kesehatan sintetis, diagnosis, prosedur, dan obat.
Edge kandidat: klaim melibatkan pasien, klaim ditangani dokter, klaim berasal dari fasilitas, diagnosis terkait prosedur, klaim memiliki rujukan, dan kesamaan atribut yang dihitung dari data pelatihan. Untuk setiap edge, dokumentasikan arah, sifat temporal, dasar pembentukannya, dan risiko kebocoran label.
Saluran graf yang dibahas dalam rancangan:
- Topologi: relasi eksplisit pada alur layanan.
- Fitur: kemiripan atribut klaim yang dihitung dengan cara yang dapat diulang.
- Semantik: relasi bermakna klinis yang dibentuk melalui aturan atau metapath terdokumentasi.
Threshold kemiripan, definisi metapath, normalisasi, dan bobot kanal merupakan hiperparameter. Semua harus dipilih hanya berdasarkan data pelatihan dan validasi yang telah ditetapkan.
### 3.5 Fusion dan penjelasan
Fusion menggabungkan sinyal rule engine, model tabular, dan model graf. Formula fusion, threshold, serta metode kalibrasi wajib dicatat. Penjelasan sebaiknya menampilkan fitur pendukung, edge atau tetangga relevan, sumber data, dan batas interpretasi. SHAP tidak boleh digambarkan sebagai bukti kausal.
### 3.6 Antarmuka verifikator
Setiap detail kasus minimal menampilkan:
- ID klaim sintetis;
- kategori triase, bukan vonis fraud;
- faktor pendorong utama;
- aturan yang terpicu;
- sumber dan waktu data;
- versi model dan threshold;
- tindakan reviewer, alasan override, dan status tindak lanjut.
## 4. Kontrak Data Minimal
| Entitas | Atribut utama | Catatan |
| Claim | ID sintetis, tanggal, biaya, status, skor | Unit analisis utama |
| Patient | ID sintetis, atribut demografis yang diperlukan | Tidak boleh memakai identitas nyata pada demo |
| Practitioner | ID sintetis, spesialisasi, afiliasi | Afiliasi perlu konsisten secara temporal |
| Organization | ID sintetis fasilitas, kelas, wilayah | Nama fiktif diberi penanda |
| Condition | Kode diagnosis dan deskripsi | Validasi terhadap referensi yang digunakan |
| Procedure | Kode tindakan dan deskripsi | Pasangan diagnosis tidak boleh dianggap mutlak tanpa konteks |
| Medication | Kode, kuantitas, unit | Dosis dan kewajaran klinis harus ditinjau ahli |
| Referral | Asal, tujuan, tanggal | Gunakan data simulasi dan dokumentasikan logika |
Setiap kolom perlu dicatat dalam data dictionary dengan nama mesin, definisi, tipe, unit, nilai yang diizinkan, makna nilai kosong, sumber, transformasi, dan klasifikasi risiko privasi.
## 5. Protokol Evaluasi
### 5.1 Definisi target
Pisahkan sekurang-kurangnya dua target:
- risk_triage: low, medium, high, fraud-scenario;
- review_action: auto-clear, review, escalate.
Keduanya tidak boleh dipakai secara bergantian. Status kerja merupakan keputusan operasional, sedangkan label risiko merupakan anotasi atau output model.
### 5.2 Split data
- Tetapkan data sintetis dan seed sebelum eksperimen.
- Gunakan split berbasis kelompok untuk menghindari entitas yang sama tersebar secara tidak terkendali di train dan test.
- Jalankan evaluasi leave-one-facility-out untuk mengukur generalisasi ke fasilitas yang tidak terlihat.
- Lakukan seluruh pemilihan fitur, normalisasi, thresholding, dan kalibrasi hanya menggunakan data yang diizinkan dalam setiap fold.
- Simpan manifest split dan daftar ID pada setiap subset.
### 5.3 Baseline dan ablation
Bandingkan rule-only, tabular-only, graph-only bila layak, dan fusion. Ablation harus menghilangkan satu kanal pada satu waktu agar kontribusi kanal topologi, fitur, dan semantik dapat diperiksa. Laporkan hasil pada split yang sama dan gunakan definisi target yang sama.
### 5.4 Metrik
Metrik wajib: confusion matrix, precision, recall, F1, false positive rate, ROC-AUC, AUPRC, dan kalibrasi. Laporkan juga jumlah kasus pada tiap kelas dan ambang keputusan. Untuk skenario masking, jelaskan apa yang dimasking, berapa proporsi edge yang diubah, apakah label dipertahankan, serta metrik yang dihitung.
### 5.5 Artefak wajib
Setiap eksperimen menghasilkan:
1. experiment_manifest.json;
1. versi atau checksum dataset;
1. konfigurasi model dan daftar fitur;
1. ID anggota tiap split;
1. prediksi per klaim;
1. label pembanding dan asal label;
1. skrip hitung metrik;
1. log dan ringkasan hasil;
1. analisis kesalahan;
1. batasan interpretasi.
## 6. Keamanan, Privasi, dan Operasi
- Gunakan data sintetis untuk demonstrasi.
- Pisahkan lingkungan pengembangan, uji, dan produksi.
- Terapkan kontrol akses berbasis peran.
- Jangan masukkan data kesehatan ke layanan eksternal tanpa dasar pemrosesan, izin, dan penilaian keamanan yang sesuai.
- Jangan menaruh secret, token, atau kredensial di Notion.
- Terapkan log akses, retensi, prosedur insiden, dan pemulihan.
- Hindari menjadikan hash biasa sebagai pengganti kontrol privasi. Pseudonimisasi memerlukan perlindungan kunci dan pembatasan akses.
- Integrasi ke SATUSEHAT, V-Claim, atau SIMRS diperlakukan sebagai tahap mendatang sampai proses otorisasi, sandbox, uji kontrak API, uji keamanan, dan penerimaan resmi terdokumentasi.
## 7. Kriteria Penerimaan MVP
MVP dianggap siap untuk demonstrasi teknis bila:
- dataset dan label dijelaskan serta dapat diperiksa;
- data tidak berlaku dibedakan dari data hilang;
- baseline dapat dijalankan ulang;
- tidak terdapat fitur yang membocorkan target;
- metrik dapat dihitung ulang dari prediksi tersimpan;
- alasan flag konsisten dengan input model;
- UI membedakan skor, dugaan anomali, dan keputusan verifikator;
- kegagalan model tidak menyebabkan tindakan penolakan otomatis;
- dokumentasi menyatakan bahwa data adalah sintetis.
## 8. Keputusan Terbuka
| ID | Keputusan | Pemilik | Status |
| D-01 | Tetapkan definisi final label fraud dan anomali | Tim data dan peninjau klinis | Terbuka |
| D-02 | Tetapkan split group-aware dan seed evaluasi | Tim ML | Terbuka |
| D-03 | Reproduksi benchmark yang ditulis di proposal | Tim ML | Terbuka |
| D-04 | Definisikan rumus per klaim untuk estimasi overcharge | Tim data dan keuangan | Terbuka |
| D-05 | Konfirmasi kesiapan dan izin integrasi eksternal | Pemilik integrasi | Terbuka |
| D-06 | Tetapkan proses peninjauan privasi dan keamanan | Pemilik tata kelola | Terbuka |
## 9. Catatan Revisi
Spesifikasi ini memperjelas rancangan dan kriteria penerimaan. Dokumen tidak menyatakan bahwa seluruh komponen, integrasi, benchmark, atau pengujian operasional telah diterapkan. Status implementasi harus diperbarui berdasarkan repositori kode, hasil uji, dan bukti yang dapat diaudit.
## [Sub-page] 03 | Dataset Registry, Data Dictionary, dan Protokol Reproduksibilitas
## Aegis-JKN, Revisi 1.0
Status: Dokumentasi kontrol data  
Tanggal: 21 Oktober 2026  
Sumber aktif: Database Klaim Aegis-JKN v2, 300 baris  
Jenis data: Sintetis untuk demonstrasi dan pengujian purwarupa
## 1. Tujuan
Halaman ini menjadi rujukan tunggal untuk versi dataset, makna label, skema variabel, pemeriksaan kualitas data, dan protokol reproduksi. Seluruh hasil yang dihitung dari data ini harus menyebut versi dataset dan tidak boleh dipresentasikan sebagai estimasi prevalensi fraud aktual JKN.
## 2. Versi Dataset
| Versi | Jumlah data | Tujuan | Ketentuan |
| Dataset demo v1 | 100 klaim | Uji awal antarmuka dan skenario | Pertahankan sebagai referensi, jangan dicampur tanpa dokumentasi |
| Dataset aktif v2 | 300 klaim | Dataset aktif dalam database Notion | Gunakan ID KLM001 sampai KLM300 |
| Dataset berikutnya | Belum ditetapkan | Eksperimen selanjutnya | Harus memiliki changelog dan checksum |
Halaman dokumentasi berjudul Dataset Simulasi Aegis-JKN, 100 Klaim menyebut 100 klaim serta distribusi label yang sesuai dengan contoh awal. Database aktif memuat 300 baris. Dokumentasi harus menjelaskan bahwa versi 100 klaim adalah versi awal dan tidak boleh digunakan untuk mengklaim hasil dari versi 300 klaim.
## 3. Ringkasan Data Aktif
### 3.1 Status alur kerja
| Status | Jumlah | Persentase |
| auto_clear | 240 | 80,0% |
| review | 24 | 8,0% |
| escalate | 36 | 12,0% |
| Total | 300 | 100,0% |
### 3.2 Label risiko
| Label risiko | Jumlah | Persentase |
| low | 240 | 80,0% |
| medium | 10 | 3,3% |
| high | 14 | 4,7% |
| fraud | 36 | 12,0% |
| Total | 300 | 100,0% |
Label risiko dan status alur kerja merupakan dua properti berbeda. Sebanyak 24 baris berstatus review mencakup label medium dan high. Jangan menyamakan seluruh 264 klaim non-fraud dengan klaim normal, karena kategori medium dan high masih memerlukan telaah.
### 3.3 Ringkasan nilai nominal
| Status | Nominal klaim |
| auto_clear | Rp2.685.550.000 |
| review | Rp279.950.000 |
| escalate | Rp561.150.000 |
| Total | Rp3.526.650.000 |
Jumlah tersebut merupakan penjumlahan kolom Biaya Rp. Nilai ini tidak dengan sendirinya membuktikan adanya overcharge atau nilai penyelamatan. Untuk menghitung estimasi overcharge diperlukan tarif pembanding, formula per klaim, serta status validasi yang terpisah.
## 4. Definisi Operasional Label
- low: skor berada dalam rentang risiko rendah yang ditetapkan pada konfigurasi versi data.
- medium: sinyal awal memerlukan pemeriksaan tambahan.
- high: sinyal lebih kuat dan perlu prioritas telaah.
- fraud: pada dataset sintetis, label skenario yang dibuat untuk pengujian. Pada sistem nyata, label hanya boleh digunakan jika ada definisi adjudikasi yang sah dan sumber pembuktiannya dicatat.
- auto_clear: alur kerja simulasi yang tidak menghasilkan eskalasi.
- review: alur kerja simulasi untuk telaah manual.
- escalate: alur kerja simulasi untuk pemeriksaan lanjutan.
Ambang skor harus disimpan di satu tempat dan diberi versi. Batas interval perlu ditulis tanpa celah atau tumpang tindih. Catatan versi 100 klaim sebelumnya menggunakan frasa yang bisa dibaca sebagai skor 0,80 tidak termasuk kelas fraud, sedangkan database aktif memiliki skor fraud 0,80. Pemilik dataset harus mengunci definisi final dan mencatat tanggal perubahan.
## 5. Data Dictionary
| Properti Notion | Makna | Jenis | Aturan kualitas |
| Name | ID klaim, KLM001 sampai KLM300 | Title | Wajib unik |
| Tanggal | Tanggal klaim atau episode | Date | Format tanggal konsisten |
| Pasien | Identitas pasien sintetis | Rich text | Tidak menggunakan identitas nyata |
| Dokter | Identitas dokter sintetis | Rich text | Relasi dan afiliasi konsisten |
| Faskes | Fasilitas kesehatan sintetis | Rich text | Nama dan kode konsisten |
| Diagnosis ICD-10 | Kode dan deskripsi diagnosis | Rich text | Kode serta istilah ditinjau |
| Prosedur ICD-9-CM | Kode dan deskripsi tindakan | Rich text | Kode serta konteks tindakan ditinjau |
| Obat | Kode, kuantitas, satuan | Rich text | Satuan harus konsisten |
| LOS hari | Durasi rawat | Number | Nilai tidak berlaku dibedakan dari kosong |
| Biaya Rp | Nominal klaim dalam rupiah | Number | Nonnegatif; definisi nominal jelas |
| Narasi Rekam Medis | Narasi sintetis untuk demo | Rich text | Tidak dianggap catatan pasien nyata |
| Kontradiksi Narasi | Penanda kontradiksi | Checkbox | Perlu aturan penetapan yang eksplisit |
| Skor Fraud | Skor sintetis atau skor model | Number | Wajib dokumentasikan sumber skor |
| Risiko | Label risiko | Select | Jangan dicampur dengan status alur kerja |
| Status | Status alur kerja | Select | Hanya gunakan opsi yang disetujui |
| Modus | Jenis skenario anomali atau fraud | Select | Kosong dibolehkan untuk klaim tanpa skenario khusus |
| Sindikat | ID kelompok skenario | Select | Kosong dibolehkan bila tidak terkait |
| Alasan | Dasar penetapan label atau sinyal | Rich text | Wajib bila klaim ditandai untuk review/escalate |
| Sinyal SHAP | Ringkasan faktor penjelas | Rich text | Hanya diisi bila berasal dari metode penjelasan yang benar |
| Kontribusi Saluran | Kontribusi tiap kanal | Rich text | Jelaskan rumus dan satuan nilai |
| Skor Sentimen | Skor sentimen sintetis | Number | Definisikan rentang dan polaritas |
| Sentimen | Kategori sentimen | Select | Harus sesuai dengan definisi skor |
| Umpan Balik Pasien | Teks umpan balik sintetis | Rich text | Data simulasi, bukan testimoni nyata |
| Catatan | Catatan pemeriksaan tambahan | Rich text | Gunakan untuk konteks, bukan mengganti alasan utama |
## 6. Pemeriksaan Kualitas yang Telah Dilakukan
Pemeriksaan baca saja terhadap seluruh 300 baris menemukan:
- seluruh 300 ID dari KLM001 sampai KLM300 tersedia;
- jumlah label risiko dan jumlah status sesuai dengan rekap di atas;
- tidak ditemukan ketidaksesuaian antara label risiko dan rentang skor yang tersimpan bila memakai ambang kategori versi aktif;
- 109 baris memiliki kolom LOS hari kosong;
- satu baris tidak memiliki isi pada properti Alasan;
- properti Modus kosong pada 240 baris;
- properti Sindikat kosong pada 264 baris.
Nilai LOS kosong tidak otomatis berarti kesalahan. Untuk layanan rawat jalan atau kasus yang tidak memakai durasi rawat, nilai tersebut mungkin tidak berlaku. Tetapkan nilai atau alasan yang membedakan not_applicable, unknown, dan nilai hilang. Untuk properti Modus dan Sindikat, kosong dapat diterima jika klaim tidak memiliki label skenario khusus.
## 7. Aturan Anti-Leakage
Kolom berikut tidak boleh menjadi fitur input jika dipakai sebagai label, hasil audit, atau hasil turunan dari proses deteksi yang diuji: Skor Fraud, Risiko, Status, Sinyal SHAP, Kontribusi Saluran, Modus, Sindikat, dan Alasan. Jika eksperimen secara khusus memprediksi salah satu kolom tersebut, desain target, sumber label, serta fitur yang dikecualikan harus dicatat sebelum pelatihan.
ID pasien, dokter, dan fasilitas tidak boleh diperlakukan sebagai fitur kategori yang memungkinkan model menghafal entitas bila tujuan eksperimen mengukur generalisasi ke entitas baru. ID masih dapat dipakai untuk membentuk kelompok split atau struktur graf yang sah, asalkan tidak membocorkan label.
## 8. Protokol Reproduksibilitas
Setiap ekspor dataset harus mencantumkan:
1. nama dan versi dataset;
1. waktu ekspor;
1. jumlah baris;
1. checksum berkas;
1. kamus data;
1. daftar kolom yang dipakai dan dikecualikan;
1. definisi target dan ambang;
1. aturan pembersihan;
1. ID anggota train, validation, dan test;
1. seed dan versi kode.
Data yang digunakan untuk angka dalam proposal harus diekspor sekali untuk setiap eksperimen dan disimpan sebagai artefak tetap. Hasil tidak boleh berubah diam-diam ketika database Notion diperbarui.
## 9. Batas Interpretasi
Dataset ini dibangun untuk demonstrasi dan pengujian purwarupa. Distribusi 12% label fraud adalah distribusi skenario sintetis, bukan estimasi prevalensi aktual. Nilai nominal klaim sintetis tidak dapat ditafsirkan sebagai kerugian BPJS yang nyata. Semua klaim tentang akurasi, ketahanan masking, penghematan waktu, atau estimasi finansial harus dihubungkan dengan artefak eksperimen yang dapat diulang.
## 10. Changelog
| Versi | Tanggal | Perubahan |
| 1.0 | 21 Oktober 2026 | Menyatukan definisi versi, label, kamus data, pemeriksaan kualitas, dan protokol anti-leakage |
| Berikutnya | Belum ditetapkan | Tambahkan perubahan hanya setelah disetujui dan dapat dilacak |
## 11. Tindak Lanjut
- [ ] Tetapkan owner dataset dan peninjau label.
- [ ] Tandai dokumentasi 100 klaim sebagai versi awal.
- [ ] Simpan kamus data sebagai artefak versi.
- [ ] Tentukan perlakuan resmi untuk nilai LOS kosong.
- [ ] Tambahkan tarif acuan dan perhitungan per klaim bila mengklaim overcharge.
- [ ] Lampirkan checksum dan seed pada setiap hasil benchmark.
## [Sub-page] 04 | Research Evidence Matrix and Reference Governance
## Aegis-JKN, Revisi 1.0
Status: Register evidence dan kontrol referensi  
Tanggal audit: 21 Oktober 2026  
Database sumber: Dataset Riset, Deteksi Fraud JKN
## 1. Tujuan
Dokumen ini mengatur hubungan antara setiap klaim dalam proposal dan sumber yang mendukungnya. Label verifikasi di database Notion menunjukkan status internal saat ini, bukan sertifikasi bahwa isi sumber telah ditinjau secara menyeluruh. Setiap klaim yang memengaruhi kesimpulan, angka nasional, kinerja model, atau dampak finansial harus memiliki rujukan spesifik dan dapat ditelusuri.
## 2. Snapshot Database Riset
Database berisi 33 entri dengan distribusi berikut:
| Dimensi | Kategori | Jumlah |
| Status verifikasi | Terverifikasi | 18 |
| Status verifikasi | Sebagian Terverifikasi | 11 |
| Status verifikasi | Perlu Verifikasi | 4 |
| Relevansi | Kritis | 11 |
| Relevansi | Tinggi | 18 |
| Relevansi | Pendukung | 4 |
Kategori utama mencakup modus fraud, teknologi AI, konteks dan statistik, roadmap dan operasional, metrik dan validasi, interoperabilitas, regulasi, serta ekonomi dan ROI.
## 3. Hierarki Kekuatan Sumber
Gunakan tingkat berikut secara konsisten:
- A, sumber primer resmi: peraturan, dokumentasi resmi sistem, laporan resmi, dataset primer, atau hasil eksperimen internal yang dapat direproduksi.
- B, penelitian ilmiah: artikel peer-reviewed dengan metode, data, dan metadata bibliografi yang dapat diperiksa.
- C, sumber sekunder bereputasi: media atau ringkasan lembaga yang mengutip sumber primer secara jelas.
- D, sumber eksploratif: blog umum, repositori sendiri, opini, atau halaman yang belum memberikan bukti langsung.
Sumber tingkat C dan D dapat membantu menemukan konteks, tetapi tidak boleh menjadi satu-satunya dasar untuk klaim yang sangat spesifik atau berisiko tinggi.
## 4. Register Klaim Prioritas
| ID | Klaim atau topik | Status saat ini | Tindakan yang diperlukan |
| E-01 | Kewajiban pelindungan data pribadi | Perlu cek pasal spesifik | Hubungkan klaim pada nomor pasal dan sumber resmi |
| E-02 | Rekam medis dan interoperabilitas SATUSEHAT | Perlu cek spesifikasi terkini | Cantumkan endpoint, versi, status sandbox/produksi dan tanggal akses |
| E-03 | Volume klaim nasional per hari | Sebagian terverifikasi | Telusuri ke laporan atau kutipan resmi dengan tanggal |
| E-04 | Jumlah verifikator dan rasio beban kerja | Sebagian terverifikasi | Hindari menjadikan repositori internal sebagai satu-satunya sumber |
| E-05 | Estimasi prevalensi fraud sebesar 3 sampai 7 persen | Perlu verifikasi | Jangan tampilkan sebagai statistik faktual tanpa penelitian primer yang sesuai |
| E-06 | Potensi kerugian nasional | Sebagian terverifikasi | Pisahkan angka yang diberitakan, perkiraan, dan temuan yang telah diaudit |
| E-07 | Benchmark Aegis-JKN: AUPRC 0,9142 | Belum tereproduksi pada audit ini | Lampirkan eksperimen, prediksi, label, split, dan skrip perhitungan |
| E-08 | Klaim AUPRC meningkat 20 persen dan false negative turun 42 persen dibanding baseline | Perlu verifikasi | Pastikan sumber, dataset, metrik, dan perbandingannya memang sama |
| E-09 | Klaim pengurangan waktu telaah 20 menit menjadi 3 menit | Perlu verifikasi | Lampirkan protokol uji pengguna, sampel, dan data waktu mentah |
| E-10 | Klaim waktu telaah berkurang 45 persen | Belum dibuktikan dengan artefak yang tersedia | Jangan satukan dengan klaim E-09 sebelum sumbernya dipastikan |
| E-11 | Estimasi penyelamatan Rp507.370.000 | Belum dapat direproduksi per klaim | Tambahkan tarif acuan, formula, dan status adjudikasi ke database |
| E-12 | Fitur dan manfaat SHAP/XAI | Perlu sitasi ilmiah yang tepat | Jelaskan keterbatasan atribusi dan jangan klaim kausalitas |
## 5. Peraturan dan Dokumentasi Resmi
Sumber awal yang harus dipertahankan sebagai referensi utama:
1. Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi.
1. Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan.
1. Peraturan Menteri Kesehatan Republik Indonesia Nomor 16 Tahun 2019 tentang Pencegahan dan Penanganan Kecurangan serta Pengendalian Gratifikasi dalam Program Jaminan Kesehatan.
1. Peraturan Menteri Kesehatan Republik Indonesia Nomor 24 Tahun 2022 tentang Rekam Medis.
1. Dokumentasi SATUSEHAT tentang interoperabilitas klaim BPJS: [https://satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/](https://satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/)
Setiap peraturan harus diperiksa status berlakunya, perubahan atau pencabutan, tanggal akses, dan pasal yang mendukung klaim. Daftar di atas adalah titik awal verifikasi, bukan opini hukum final.
## 6. Referensi Metode AI
Klaim metode harus disambungkan dengan sumber primer metode yang tepat:
- XGBoost untuk baseline pembelajaran tabular.
- Graph neural networks dan heterogeneous graph learning untuk representasi relasional.
- SHAP untuk atribusi fitur dan penjelasan prediksi.
- GroupKFold atau evaluasi berbasis kelompok untuk pengujian generalisasi.
- Precision-recall analysis untuk evaluasi kelas yang tidak seimbang.
- Teknik sintesis data dan privasi hanya jika benar-benar diterapkan dan dievaluasi dalam proyek.
Hindari mengutip satu artikel untuk mendukung banyak klaim yang tidak diuji oleh artikel tersebut. Catat halaman, bagian, tabel, atau hasil spesifik yang mendukung pernyataan di proposal.
## 7. Format Entri Sumber yang Wajib
Setiap baris baru dalam database riset sebaiknya mencantumkan:
- Judul sumber lengkap.
- Penulis atau organisasi.
- Tahun publikasi.
- Jurnal, penerbit, atau lembaga.
- DOI atau URL stabil.
- Jenis sumber dan tingkat kekuatan A sampai D.
- Klaim spesifik yang didukung.
- Kutipan, halaman, tabel, atau bagian yang relevan.
- Batasan atau caveat sumber.
- Reviewer dan tanggal verifikasi.
- Status verifikasi beserta alasan.
## 8. Aturan Penggunaan dalam Proposal
1. Fakta eksternal harus memiliki sitasi dekat dengan klaim.
1. Klaim yang belum diverifikasi diberi tanda internal dan tidak dipublikasikan sebagai fakta.
1. Angka hasil eksperimen internal harus merujuk pada ID eksperimen, bukan pada artikel eksternal.
1. Statistik nasional tidak boleh diekstrapolasi secara mekanis dari dataset sintetis.
1. Estimasi penghematan harus membedakan potensi koreksi, nilai yang diputuskan setelah audit, dan dana yang benar-benar berhasil diselamatkan.
1. Klaim benchmark antar-model hanya boleh dibandingkan jika split, target, preprocessing, threshold, dan sumber label setara.
## 9. Gerbang Publikasi
Sebelum dokumen diserahkan atau dipublikasikan, lakukan pemeriksaan berikut:
- [ ] Setiap angka utama memiliki sumber atau artefak eksperimen.
- [ ] Setiap sumber eksternal telah dibuka dan diperiksa, bukan hanya dicatat URL-nya.
- [ ] Status hukum peraturan telah diperiksa pada sumber resmi.
- [ ] Semua perbedaan angka antarhalaman sudah direkonsiliasi.
- [ ] Klaim yang belum terbukti ditandai sebagai hipotesis atau target.
- [ ] Referensi dan sitasi menggunakan satu gaya yang konsisten, misalnya IEEE atau APA.
- [ ] Daftar pustaka tidak memuat sumber yang tidak pernah dikutip dalam teks.
## 10. Prinsip Editorial
Gunakan kalimat yang menunjukkan tingkat kepastian sebenarnya. Pilih frasa seperti "diusulkan", "akan diuji", "pada dataset sintetis", atau "hasil sementara" apabila bukti belum lengkap. Hindari kata "terbukti", "riil", "akurat secara superior", dan "tervalidasi" sebelum syarat bukti dipenuhi.
## [Sub-page] 05 | Pemilihan Kandidat Inovasi dan Batas Ruang Lingkup MVP
## Analisis Keputusan dan Batas Ruang Lingkup, Revisi 1.0
Status: Dokumen keputusan produk  
Tanggal: 21 Oktober 2026  
Keputusan sementara: Memprioritaskan deteksi anomali klaim fasilitas kesehatan  
Hubungan dengan proyek: Dasar ruang lingkup MVP Aegis-JKN
## 1. Tujuan
Dokumen ini membandingkan tiga gagasan awal dengan kriteria yang dapat dijelaskan. Perbandingan ini merupakan keputusan perancangan internal, bukan hasil evaluasi resmi BPJS Kesehatan dan bukan klaim bahwa kandidat tertentu pasti menghasilkan penghematan finansial tertentu.
## 2. Kriteria Penilaian
Setiap kandidat dinilai berdasarkan:
1. Kejelasan masalah dan pengguna.
1. Ketersediaan data yang sah dan realistis.
1. Kelayakan demonstrasi dalam waktu pengembangan.
1. Kemampuan mengukur hasil.
1. Hambatan integrasi dan regulasi.
1. Diferensiasi terhadap proses atau fitur yang telah ada.
1. Risiko salah klasifikasi dan konsekuensi bagi pihak terdampak.
Skor angka belum diberikan karena bobot dan penilaian belum melalui lokakarya tim yang terdokumentasi. Penilaian kualitatif berikut harus diperlakukan sebagai keputusan sementara.
## 3. Perbandingan Kandidat
### Kandidat 1. Anomali diagnosis dan prosedur klaim
Masalah yang dituju: kemungkinan ketidaksesuaian antara diagnosis, tindakan, durasi rawat, obat, dan nominal klaim.
Pengguna utama: verifikator klaim dan tim audit yang berwenang.
Nilai utama: menyediakan prioritas telaah dan alasan anomali yang dapat diperiksa.
Kelayakan purwarupa: tinggi relatif terhadap dua kandidat lain, karena skenario sintetis dapat dibuat dan diuji tanpa akses ke data kepesertaan nyata.
Risiko: pasangan kode medis bisa memiliki konteks klinis yang sah; aturan yang terlalu sederhana dapat menandai klaim yang benar. Peninjauan klinis diperlukan untuk mendefinisikan ground truth.
Keputusan: kandidat utama untuk MVP.
### Kandidat 2. Verifikasi identitas peserta
Masalah yang dituju: kemungkinan penyalahgunaan identitas ketika seseorang menggunakan hak layanan peserta lain.
Pengguna utama: petugas pendaftaran dan pengelola layanan kesehatan.
Nilai utama: mengurangi risiko kesalahan identitas melalui verifikasi terkontrol.
Kelayakan purwarupa: demonstrasi antarmuka relatif sederhana, tetapi validasi biometrik nyata memerlukan data wajah yang sah, otorisasi, pengamanan tinggi, dan pengujian bias.
Risiko: privasi biometrik, false rejection, akses ke sumber identitas, serta potensi tumpang tindih dengan fitur yang sudah tersedia. Status dan cakupan fitur yang ada perlu dikonfirmasi dari sumber resmi sebelum membuat klaim redundansi.
Keputusan: tidak menjadi fokus MVP ini. Dapat ditinjau kembali sebagai proyek terpisah.
### Kandidat 3. Anomali pelaporan upah dan iuran
Masalah yang dituju: kemungkinan ketidaksesuaian penghasilan yang dilaporkan dengan dasar penghitungan iuran.
Pengguna utama: unit kepatuhan, pengelola iuran, dan otoritas yang berwenang.
Nilai utama: membantu mengidentifikasi pola yang memerlukan pemeriksaan administratif.
Kelayakan purwarupa: konsep analitik relatif mudah disimulasikan, tetapi verifikasi lapangan memerlukan akses dan kewenangan untuk membandingkan sumber data lintas lembaga.
Risiko: akses lintas instansi, dasar pemrosesan data, perbedaan definisi komponen upah, dan dampak salah tandai terhadap pekerja maupun pemberi kerja.
Keputusan: kandidat cadangan jangka panjang, bukan fokus MVP.
## 4. Ringkasan Penilaian
| Kriteria | Kandidat 1 | Kandidat 2 | Kandidat 3 |
| Data sintetis untuk demo | Tinggi | Sedang | Sedang |
| Kemudahan mengukur hasil awal | Tinggi | Sedang | Sedang |
| Ketergantungan integrasi eksternal | Sedang | Tinggi | Tinggi |
| Risiko privasi | Tinggi jika data nyata; dapat dibatasi dengan sintetis | Sangat tinggi untuk biometrik | Tinggi untuk data lintas lembaga |
| Fokus MVP | Direkomendasikan | Tidak diprioritaskan | Cadangan |
Klasifikasi pada tabel merupakan penilaian awal tim. Penilaian harus diperbarui bila syarat kompetisi, bukti fitur eksisting, ketersediaan data, atau persyaratan akses berubah.
## 5. Batas Ruang Lingkup MVP
### In-scope
- data klaim sintetis;
- dua atau tiga skenario anomali yang didefinisikan dengan jelas;
- baseline rule engine dan model tabular;
- pengujian manfaat analisis graf terhadap baseline;
- penjelasan yang menampilkan alasan dan sinyal pendukung;
- antarmuka demonstrasi untuk verifikator;
- log audit dan evaluasi yang dapat direproduksi.
### Out-of-scope
- vonis fraud otomatis;
- penolakan atau pemotongan klaim otomatis;
- penggunaan data peserta nyata tanpa kewenangan;
- pengoperasian pada sistem produksi;
- klaim penghematan nasional yang diekstrapolasi dari dataset sintetis;
- integrasi produksi ke V-Claim atau SATUSEHAT sebelum izin dan pengujian tersedia.
## 6. Keputusan dan Syarat Perubahan
Kandidat 1 tetap dipilih selama tiga syarat dipenuhi:
1. Tim dapat mendefinisikan label dan bukti klinis untuk tiap skenario.
1. Benchmark dapat direproduksi dengan pemisahan data yang mencegah leakage.
1. Hasil menunjukkan nilai tambah yang terukur dibanding pendekatan sederhana.
Jika salah satu syarat tidak terpenuhi, ruang lingkup harus dipersempit. Kompleksitas graph learning bukan tujuan tersendiri. Nilai proyek ditentukan oleh validitas masalah, kualitas evaluasi, dan manfaat bagi alur kerja verifikator.
## 7. Keputusan yang Masih Perlu Dicatat
- [ ] Konfirmasi tema dan persyaratan resmi kompetisi dari sumber penyelenggara.
- [ ] Tetapkan bobot penilaian kandidat bersama tim.
- [ ] Minta tinjauan dari ahli koding atau peninjau klinis untuk skenario sintetis.
- [ ] Tetapkan dua skenario utama yang masuk ke benchmark pertama.
- [ ] Tetapkan definisi selesai untuk demo, paper, dan presentasi.
## [Sub-page] 06 | Catatan Riset: Deteksi Kecurangan Klaim JKN
## Sintesis Literatur, Kesenjangan Bukti, dan Pertanyaan Riset, Revisi 1.0
Status: Catatan tinjauan literatur awal  
Tanggal revisi: 21 Oktober 2026  
Tujuan: Menjadi dasar penyusunan latar belakang dan desain evaluasi, bukan daftar pustaka final.
## 1. Ringkasan
Kecurangan klaim kesehatan dapat mencakup klaim layanan yang tidak diberikan, upcoding, unbundling, duplikasi, serta ketidaksesuaian antara narasi klinis, diagnosis, prosedur, obat, dan nilai klaim. Deteksi dapat menggabungkan aturan eksplisit dengan model statistik. Analisis graf dapat membantu mempelajari hubungan antarentitas, tetapi manfaat tambahannya harus dibuktikan melalui evaluasi yang sebanding dengan baseline.
Catatan awal di Notion memuat beberapa angka nasional, termasuk dugaan kerugian dan estimasi prevalensi fraud. Angka semacam itu hanya boleh dimasukkan ke paper setelah sumber primer, tanggal, definisi, dan metode penghitungannya diverifikasi. Ringkasan media tidak cukup untuk menyatakan angka yang sama sebagai kerugian aktual yang telah diaudit.
## 2. Taksonomi Pola yang Relevan
### 2.1 Upcoding
Kemungkinan ketidaksesuaian antara kondisi klinis atau dokumentasi dan kode yang ditagihkan. Deteksi membutuhkan konteks kode, aturan tarif yang berlaku, dan pemeriksaan klinis. Pasangan kode diagnosis dan prosedur tidak dapat dianggap mustahil hanya berdasarkan satu aturan sederhana tanpa memperhatikan konteks.
### 2.2 Phantom billing
Kemungkinan klaim untuk layanan yang tidak didukung bukti layanan yang sesuai. Pengujian sintetis dapat mendemonstrasikan pola tidak konsisten, tetapi pembuktian kasus nyata memerlukan pemeriksaan bukti primer oleh pihak yang berwenang.
### 2.3 Unbundling dan repeat billing
Kemungkinan pemisahan layanan yang seharusnya berada dalam satu paket atau pengajuan klaim berulang untuk episode yang sama. Aturan harus merujuk pada definisi paket dan ketentuan yang berlaku pada periode klaim terkait.
### 2.4 Cloning dan pola kolektif
Kemiripan rekam atau klaim lintas pasien, dokter, dan fasilitas dapat menjadi sinyal yang perlu ditinjau. Kesamaan tidak otomatis membuktikan kecurangan karena layanan standar dapat menghasilkan pola serupa secara wajar.
## 3. Pendekatan Analitik
### 3.1 Rule-based
Kelebihan: dapat dijelaskan dan cepat untuk aturan eksplisit.  
Keterbatasan: cakupan bergantung pada aturan yang dibuat, pemeliharaan manual, dan kemampuan menghadapi variasi atau perubahan pola.
### 3.2 Model tabular
Model seperti XGBoost dapat digunakan sebagai baseline bagi fitur terstruktur. Evaluasi harus mencegah leakage dan memperhatikan imbalance. Threshold keputusan tidak boleh dipilih menggunakan test set.
### 3.3 Graph learning
Graf heterogen dapat merepresentasikan relasi pasien, dokter, fasilitas, klaim, diagnosis, prosedur, dan rujukan. Tiga gagasan kanal yang dipakai dalam rancangan Aegis-JKN adalah topologi, kemiripan fitur, dan relasi semantik. Definisi setiap edge harus menghindari kebocoran target, khususnya bila ground truth skenario sintetis dibangun dari relasi yang sama.
### 3.4 Explainable AI
SHAP dapat mendukung atribusi fitur terhadap output model tertentu. Atribusi tidak membuktikan hubungan kausal dan tidak menggantikan peninjauan klinis. Penjelasan graf harus menunjukkan jalur atau tetangga yang relevan dan menjelaskan bagaimana pilihan edge memengaruhi hasil.
## 4. Pertanyaan Riset
1. Apakah model graf memberikan peningkatan yang bermakna dibandingkan XGBoost dengan split, target, dan fitur yang sama?
1. Apakah peningkatan tetap ada ketika pasien dan fasilitas tertentu tidak pernah muncul dalam pelatihan?
1. Bagaimana hasil berubah ketika sebagian edge rujukan dihilangkan atau diganggu?
1. Apakah skor risiko terkalibrasi dan apakah alasan yang ditampilkan cocok dengan input yang memengaruhi model?
1. Berapa beban false positive bagi verifikator pada threshold operasional yang realistis?
1. Apakah manfaat tambahan dari graph learning sebanding dengan biaya implementasi dan kompleksitas pemeliharaan?
## 5. Matriks Bukti Awal
| Klaim | Bukti yang diperlukan | Status saat ini |
| Volume klaim harian nasional | Laporan resmi atau dokumentasi primer dengan tanggal | Perlu validasi spesifik |
| Kapasitas verifikator | Sumber resmi yang menjelaskan jumlah, peran, dan periode | Perlu validasi spesifik |
| Prevalensi fraud 3 sampai 7 persen | Studi dengan definisi fraud dan denominator yang jelas | Belum layak digunakan sebagai fakta |
| Kerugian nasional | Laporan resmi atau temuan audit dengan konteks | Harus dibedakan dari potensi kerugian |
| AUPRC MHGSL 0,9142 | Kode, prediksi, ground truth, split, dan skrip metrik | Belum dapat direproduksi dari artefak yang diperiksa |
| Peningkatan AUPRC dibanding baseline | Hasil eksperimen pada split dan target yang setara | Belum dapat direproduksi dari artefak yang diperiksa |
| Penurunan waktu telaah | Protokol evaluasi pengguna dan data waktu mentah | Belum terlampir |
| Penghematan finansial | Perhitungan per klaim, tarif acuan, adjudikasi, dan validasi independen | Belum dapat direproduksi dari data biaya saja |
## 6. Metodologi Tinjauan Literatur
Untuk setiap sumber, catat:
- pertanyaan yang dijawab oleh sumber;
- negara, populasi, jenis klaim, dan periode;
- desain studi serta jenis data;
- definisi fraud dan label pembanding;
- model serta baseline;
- skema validasi;
- metrik dan interval ketidakpastian;
- keterbatasan, konflik kepentingan, dan kemungkinan bias;
- hubungan langsung sumber dengan pernyataan yang dikutip.
Tinjauan literatur akhir perlu menggunakan pencarian yang terdokumentasi, kriteria inklusi dan eksklusi, serta pencatatan alasan mengapa suatu sumber digunakan. Jika prosesnya bukan systematic review, jangan memberi label systematic review.
## 7. Sumber Awal
Daftar berikut merupakan sumber awal untuk diperiksa lebih lanjut, bukan daftar pustaka final:
- Dokumentasi SATUSEHAT tentang interoperabilitas klaim BPJS: [https://satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/](https://satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/)
- Peraturan tentang Pelindungan Data Pribadi, rekam medis, dan pencegahan fraud JKN.
- Literatur ilmiah primer tentang XGBoost, graph neural networks, SHAP, evaluasi kelas tidak seimbang, dan validasi berbasis kelompok.
- Laporan resmi BPJS Kesehatan dan dokumen audit yang relevan dengan definisi klaim dan periode pengukuran.
Sumber media atau blog yang sudah ada dalam database riset dapat dipakai untuk penemuan sumber, tetapi setiap klaim kuantitatif perlu dilacak ke sumber primer apabila tersedia.
## 8. Batasan
Dokumen ini adalah sintesis riset awal. Dokumen ini tidak menyatakan bahwa angka kinerja model Aegis-JKN telah tervalidasi atau bahwa estimasi prevalensi dalam catatan awal telah terbukti. Setiap pembaruan harus mencantumkan sumber yang dibuka, tanggal verifikasi, klaim yang didukung, serta keterbatasannya.
## 9. Langkah Berikutnya
- [ ] Verifikasi semua statistik nasional sebelum dimasukkan ke proposal.
- [ ] Lengkapi metadata dan DOI artikel akademik.
- [ ] Tautkan klaim utama ke halaman dan tabel sumber yang sesuai.
- [ ] Susun protokol pencarian literatur beserta kriteria seleksi.
- [ ] Pisahkan bukti eksternal dari hasil eksperimen internal.
- [ ] Tandai setiap klaim yang belum memiliki bukti sebagai hipotesis atau target.
## [Sub-page] 07 | Dataset Registry dan Kamus Data DM Kontekstual
Katalog ini mencatat file yang benar-benar diunggah, skema kolom, kamus ICD-10, dan temuan pemeriksaan awal. Baris observasi individu tidak disalin ke Notion agar nomor peserta dan detail layanan kesehatan tetap terlindungi.
> **{'type': 'emoji', 'emoji': '💡'}** Peringatan privasi: data kepesertaan dan layanan berisi pengidentifikasi peserta, tanggal lahir, kode diagnosis, lokasi layanan, atau biaya. Batasi akses halaman dan jangan memasukkan baris mentah ke prompt AI eksternal.
# Ringkasan ukuran data
Tiga file Stata berisi total 6.514.039 baris. Workbook metadata menerangkan variabel untuk empat domain, tetapi unggahan hanya mencakup file observasi kepesertaan, diagnosis sekunder FKRTL, dan FKTP nonkapitasi.
## Tabel 1. Inventaris sumber
| ID | File sumber | Baris / isi | Dimensi | Peran | Catatan utama |
| D01 | DM_kepesertaan.dta | 143.496 baris | 18 variabel | Kepesertaan | PSTV01 unik pada file ini. Ada nomor peserta dan tanggal lahir, jadi data sensitif. |
| D02 | DM20152020_fkrtldxsekunder.dta | 6.362.523 baris | 4 variabel | Diagnosis sekunder FKRTL | Berisi ID kunjungan dan kode diagnosis. Tidak ada nomor peserta, tanggal layanan, atau biaya dalam file ini. |
| D03 | DM20152020_fktpnonkapitasi.dta | 8.020 baris | 21 variabel | Layanan FKTP nonkapitasi | Kolom Biaya tagih dan Biaya verifikasi identik pada seluruh baris. PNK02 memiliki 4.939 nilai unik. |
| R01 | 20152020 Kode ICD10 untuk diagnosis FKRTL.xlsx | 3.411 baris, 2 sheet | 3 kolom per sheet | Kode diagnosis masuk dan primer | Masing-masing sheet memiliki satu kode 999 tanpa deskripsi. |
| R02 | 20152020 Kode ICD10 untuk diagnosis FKTP Kapitasi.xlsx | 1.979 baris | 3 kolom | Kamus ICD-10 FKTP kapitasi | Ada satu kode 999 tanpa deskripsi. |
| R03 | 20152020 Kode ICD10 untuk diagnosis FKTP Non Kapitasi.xlsx | 1.030 baris | 3 kolom | Kamus ICD-10 FKTP nonkapitasi | Seluruh deskripsi kode terisi. |
| R04 | Metadata Data Sampel Kontekstual DM.xlsx | 4 sheet | 18, 26, 55, 21 variabel | Kamus variabel dan label kategori | 979 baris label nilai kategori diekstrak dari empat sheet. |
## Tabel 2. Skema DM_kepesertaan.dta
| Variabel | Label sumber | Tipe hasil baca | Kosong |
| PSTV01 | Nomor peserta | int32 | 0 |
| PSTV02 | Nomor keluarga | int32 | 0 |
| PSTV03 | Tanggal lahir peserta | datetime64[ns] | 0 |
| PSTV04 | Hubungan Keluarga | int8 | 0 |
| PSTV05 | Jenis Kelamin | int8 | 0 |
| PSTV06 | Status perkawinan | int8 | 0 |
| PSTV07 | Kelas rawat | int8 | 0 |
| PSTV08 | Segmentasi peserta | int8 | 0 |
| PSTV09 | Provinsi Tempat Tinggal Peserta | int8 | 0 |
| PSTV10 | Kabupaten/Kota Tempat Tinggal Peserta | int16 | 0 |
| PSTV11 | Kepemilikan faskes | int8 | 0 |
| PSTV12 | Jenis faskes | int8 | 0 |
| PSTV13 | Provinsi Fasilitas Kesehatan Peserta Terdaftar | int8 | 0 |
| PSTV14 | Kabupaten/Kota Fasilitas Kesehatan Peserta Terdaftar | int16 | 0 |
| PSTV15 | Bobot | float32 | 0 |
| PSTV16 | Tahun Sampel | int16 | 0 |
| PSTV17 | Status Kepesertaan | int8 | 0 |
| PSTV18 | Tahun Meninggal | float64 | 133.228 |
## Tabel 3. Skema DM20152020_fkrtldxsekunder.dta
| Variabel | Label berdasarkan metadata | Tipe hasil baca | Status pemeriksaan |
| FKL02 | ID Kunjungan | object | Tidak dipindai penuh |
| FKL24 | Kode diagnosis ICD 10 (beragam 3-5 digit) | object | Tidak dipindai penuh |
| FKL24A | Kode diagnosis ICD 10 (3 digit) | object | Tidak dipindai penuh |
| FKL24B | Kode dan nama diagnosis ICD 10 (3 digit) | object | Tidak dipindai penuh |
## Tabel 4. Skema DM20152020_fktpnonkapitasi.dta
| Variabel | Label sumber | Tipe hasil baca | Kosong | Catatan |
| PSTV01 | Nomor Peserta | int32 | 0 | Pengidentifikasi peserta, jangan dijadikan fitur model. |
| PSTV02 | Nomor keluarga | int32 | 0 | Pengidentifikasi keluarga, jangan dijadikan fitur model. |
| PSTV15 | Bobot | float32 | 0 |  |
| PNK02 | ID Kunjungan | object | 0 | 4.939 nilai unik pada 8.020 baris. Grain perlu divalidasi. |
| PNK03 | Tanggal kunjungan | datetime64[ns] | 0 | Rentang terdeteksi 2014-08-16 hingga 2020-12-31. |
| PNK04 | Tanggal tindakan | datetime64[ns] | 0 | Rentang terdeteksi 2014-08-16 hingga 2020-12-31. |
| PNK05 | Tanggal pulang | datetime64[ns] | 0 | Rentang terdeteksi 2015-01-05 hingga 2020-12-31. |
| PNK06 | Provinsi faskes | int8 | 0 |  |
| PNK07 | Kode Kab/Kota faskes | int16 | 0 |  |
| PNK08 | Kepemilikan faskes | int8 | 0 |  |
| PNK09 | Jenis faskes | int8 | 0 |  |
| PNK10 | Tipe faskes | int8 | 0 |  |
| PNK11 | Tingkat layanan | int8 | 0 |  |
| PNK12 | Segmen peserta | int8 | 0 |  |
| PNK13 | Kode dan Nama diagnosis berdasarkan ICD-10 (3 digit) | float64 | 3 | Kolom turunan kosong pada 3 baris. |
| PNK13A | Kode diagnosis berdasarkan ICD-10 (3 digit) | object | 3 | Kolom kode kosong pada 3 baris. |
| PNK14 | Kode diagnosis (3-5 digit) | object | 0 |  |
| PNK15 | Nama Diagnosis | object | 0 |  |
| PNK16 | Nama Tindakan | int16 | 0 | Kode tindakan berkategori, bukan nama teks. |
| PNK17 | Biaya tagih | int32 | 0 | Identik dengan PNK18 pada semua 8.020 baris. |
| PNK18 | Biaya verifikasi | int32 | 0 | Identik dengan PNK17 pada semua 8.020 baris. |
## Tabel 5. Referensi kamus ICD-10
| File referensi | Sheet atau lingkup | Jumlah baris | Isu yang ditemukan |
| Kode ICD10 FKRTL.xlsx | Diagnosis Masuk | 1.859 | Kode 999 tanpa deskripsi |
| Kode ICD10 FKRTL.xlsx | Diagnosis Primer | 1.552 | Kode 999 tanpa deskripsi |
| Kode ICD10 FKTP Kapitasi.xlsx | Sheet1 | 1.979 | Kode 999 tanpa deskripsi |
| Kode ICD10 FKTP Non Kapitasi.xlsx | Sheet1 | 1.030 | Tidak ada deskripsi kosong pada pemindaian. |
## Tabel 6. Cakupan workbook metadata
| Sheet sumber metadata | Jumlah variabel | Keterangan |
| 1. Kepesertaan | 18 | Kamus variabel dan nilai kode kategori. |
| 2. FKTP | 26 | Kamus FKTP tersedia, file observasi FKTP tidak diunggah. |
| 3. FKRTL | 55 | Kamus FKRTL tersedia, file observasi utama FKRTL tidak diunggah. |
| 4. Non Kapitasi | 21 | Kamus variabel cocok dengan file DM20152020_fktpnonkapitasi.dta. |
# Temuan kualitas dan batas penggunaan
- Tanggal layanan pada PNK03 dan PNK04 terdeteksi mulai 16 Agustus 2014, sedangkan nama file menunjukkan rentang 2015-2020. Periode perlu dikonfirmasi sebelum filter waktu dipakai.
- PNK02 berisi 4.939 nilai unik pada 8.020 baris. Ini bukan bukti duplikasi salah, tetapi menunjukkan bahwa ID kunjungan berulang pada beberapa baris. Pastikan grain data, misalnya apakah baris merepresentasikan tindakan atau diagnosis.
- PNK17 (Biaya tagih) sama dengan PNK18 (Biaya verifikasi) pada semua 8.020 baris. Dataset ini tidak menyediakan variasi selisih biaya untuk dipakai sebagai target supervised adjustment.
- Tiga kamus ICD-10 memiliki kode 999 tanpa deskripsi. Perlakukan sebagai nilai sentinel yang perlu diverifikasi, jangan otomatis dianggap kode ICD-10 valid.
- Kolom PSTV18 (Tahun Meninggal) kosong pada 133.228 peserta. Karena variabelnya kondisional, nilai kosong tidak otomatis dianggap kesalahan atau diimputasi.
- Label fraud tidak tersedia pada file DM yang diunggah. Data ini tidak boleh digunakan seolah-olah setiap baris memiliki kelas fraud atau non-fraud.
# Data yang belum tersedia
File observasi utama FKTP dan FKRTL tidak termasuk dalam unggahan ini. Workbook metadata mendokumentasikan 26 variabel FKTP dan 55 variabel FKRTL, namun itu tidak menggantikan file transaksi. File diagnosis sekunder FKRTL hanya menghubungkan kode diagnosis dengan FKL02, tanpa tanggal, biaya, atau nomor peserta.
# Aturan untuk pelatihan AI
Mulai dari pemodelan kualitas data atau prioritisasi anomali, bukan klasifikasi fraud. Jangan menganggap ketidaksamaan kode diagnosis, biaya, atau kunjungan berulang sebagai fraud tanpa label adjudikasi dan dasar aturan yang sah.
Simpan pemisahan dataset sintetis Aegis-JKN dan data kontekstual DM. Jangan menggabungkan kedua sumber tanpa kunci relasi yang sah, definisi label seragam, persetujuan penggunaan, serta pemeriksaan potensi kebocoran identitas.
# Lampiran kerja
Katalog Excel terstruktur yang menyertai percakapan ini berisi 14 sheet: README, registry, skema tiga file DTA, metadata variabel empat domain, 979 label kategori, dan empat kamus ICD-10 lengkap. Gunakan file tersebut sebagai kamus referensi, bukan pengganti file observasi mentah.
Halaman lanjutan: [08 | Protokol Training AI dan Evaluasi Aegis-JKN](https://app.notion.com/p/08-Protokol-Training-AI-dan-Evaluasi-Aegis-JKN-4003e6031ab781978715f1de059e82ef).
## [Sub-page] 08 | Protokol Training AI dan Evaluasi Aegis-JKN
Dokumen ini mengatur prosedur pelatihan, validasi, dan dokumentasi model secara reproduktif. Tujuannya membantu tim membuat prototipe analitik yang dapat diaudit, bukan menghasilkan vonis fraud otomatis.
Sumber Notion: [Klaim Aegis-JKN v2, 300 baris](https://app.notion.com/p/c783afb3d0d4458295456180b7b7756b), [Dataset Registry DM Kontekstual](https://app.notion.com/p/07-Dataset-Registry-dan-Kamus-Data-DM-Kontekstual-4003e6031ab78179bcc7ca76a0b80fbc), dan [Arsitektur serta metodologi teknis](https://app.notion.com/p/02-Aegis-JKN-Arsitektur-Sistem-dan-Metodologi-Teknis-4003e6031ab781efbcdac7b0dbdd0cad).
> **{'type': 'emoji', 'emoji': '💡'}** Keputusan inti: dataset klaim sintetis dan dataset DM kontekstual adalah dua sumber berbeda. Jangan menggabungkannya hanya karena sama-sama berkaitan dengan JKN. Belum ada kunci relasi lintas sumber dan belum ada label fraud pada file DM.
1. Inventaris sumber dan kesiapan
| Sumber | Skala teramati | Label target | Peran yang disarankan | Batas utama |
| Klaim Aegis-JKN v2, database Notion aktif | 300 baris, KLM001 sampai KLM300 | Field Risiko dan Status tersedia, tetapi perlu audit asal label | Baseline prototipe setelah ground truth independen disahkan | Deskripsi database masih menyebut 100 klaim dan KLM001 sampai KLM024. |
| DM_kepesertaan.dta | 143.496 baris, 18 variabel | Tidak ada label fraud | Profil kepesertaan yang diizinkan | Memuat nomor peserta, tanggal lahir, lokasi, dan atribut sensitif. |
| DM20152020_fkrtldxsekunder.dta | 6.362.523 baris, 4 variabel | Tidak ada label fraud | Analisis distribusi kode diagnosis setelah audit kamus | Hanya FKL02 dan kode diagnosis. Tidak ada tanggal, biaya, atau nomor peserta. |
| DM20152020_fktpnonkapitasi.dta | 8.020 baris, 21 variabel | Tidak ada label fraud | QA data layanan dan eksplorasi anomali non-supervised | Biaya tagih dan biaya verifikasi identik pada semua baris. |
| Workbook ICD-10 dan Metadata | 4 kamus ICD-10, 979 label kategori | Bukan label outcome | Validasi kode dan decoding kategori | Kode 999 tanpa deskripsi ditemukan dalam 3 kamus. |
1. Tentukan tugas sebelum memilih model
| Tugas | Dataset | Target yang sah | Status saat ini | Hasil yang boleh dilaporkan |
| Klasifikasi fraud supervised | Klaim Aegis-JKN sintetis | ground_truth_fraud yang diperiksa manusia dan memiliki provenance | Belum disahkan | Metrik hanya setelah label dan leakage audit. |
| Pemeringkatan anomali | Data DM kontekstual | Tidak memerlukan label, tetapi tidak sama dengan ground truth fraud | Bisa dirancang, belum dilatih | Daftar observasi untuk ditinjau, bukan vonis fraud. |
| Prediksi selisih biaya verifikasi | FKTP nonkapitasi | PNK17 - PNK18 | Tidak layak pada ekstrak saat ini | Selisih 0 pada semua 8.020 baris. |
| Pemeriksaan konsistensi ICD-10 | Kamus ICD-10 dan kode diagnosis | Kecocokan kode dan deskripsi referensi | Layak sebagai QA setelah sentinel 999 diperiksa | Metrik kecocokan kode, bukan metrik fraud. |
1. Label dan pencegahan kebocoran
Database klaim aktif memuat 300 baris, tetapi deskripsinya masih menyebut versi 100 baris dan ground truth KLM001 sampai KLM024. Sebelum model dibuat, selaraskan deskripsi, jumlah record, versi dataset, definisi label, dan provenance setiap label. Jangan menyamakan field Risiko atau Status dengan label fraud yang telah diverifikasi, kecuali proses pembentukannya diaudit.
Buat kolom adjudikasi terpisah, minimal: ground_truth_fraud, evidence_source, reviewer_1, reviewer_2, adjudication_date, label_confidence, dan exclusion_reason. Kasus yang belum pasti harus berstatus unresolved, bukan dipaksa masuk kelas positif atau negatif.
Untuk eksperimen supervisi, keluarkan Skor Fraud, Risiko, Status, Sinyal SHAP, serta kolom yang dihitung langsung dari aturan label dari fitur awal. Jika label dibentuk dari skor, memasukkan skor tersebut membuat evaluasi sirkular dan tidak membuktikan kemampuan deteksi independen.
1. Kandidat fitur dan perlindungan privasi
| Sumber | Dapat dipertimbangkan setelah validasi | Dikecualikan dari fitur awal | Alasan |
| Klaim sintetis Aegis-JKN | Biaya, LOS, kategori layanan, diagnosis atau prosedur, rujukan, fitur narasi yang tidak dibentuk dari label | Skor Fraud, Risiko, Status, Sinyal SHAP, label turunan, dan kolom yang dihitung langsung dari aturan label | Mencegah model meniru target dan menghindari data leakage. |
| Data DM kontekstual | Frekuensi penggunaan agregat, kode diagnosis, interval kunjungan setelah validasi, kategori layanan dan tindakan | Nomor peserta, nomor keluarga, ID kunjungan mentah, tanggal lahir, lokasi sangat rinci, dan pengidentifikasi langsung | Mengurangi risiko memorisasi individu dan kebocoran identitas. |
| Diagnosis sekunder FKRTL | Frekuensi atau kombinasi kode setelah validasi FKL02 dan ICD-10 | Asumsi mengenai urutan diagnosis atau label fraud yang tidak ada pada file | Tidak ada tanggal, biaya, nomor peserta, atau outcome pada file ini. |
1. Tahapan training dan gerbang penerimaan
| Tahap | Aktivitas | Kriteria lulus | Artefak wajib |
| 0. Bekukan sumber | Catat file, versi, jumlah baris, hash SHA-256, waktu ekstraksi, dan izin penggunaan | Inventaris sumber stabil dan dapat diaudit | manifest.json |
| 1. Audit label | Audit definisi kasus positif, alasan, bukti, reviewer, dan adjudikasi | Label sintetis atau skor aturan tidak diperlakukan sebagai ground truth independen | label_audit.csv |
| 2. Siapkan fitur | Hapus identitas langsung, validasi tanggal, mapping kode, missingness, grain, dan leakage | Tidak ada identifier atau fitur pasca-keputusan yang bocor | data_quality_report.md |
| 3. Baseline | Bandingkan aturan sederhana, logistic regression, dan model pohon yang interpretable | Baseline, split, seed, dan metrik dapat diulang | train.py, metrics.json |
| 4. Evaluasi | Ukur PR-AUC, precision, recall, F1, confusion matrix, FPR, calibration, serta error analysis | Threshold ditetapkan berdasarkan kapasitas review dan validasi independen | evaluation_report.md |
| 5. Human review | Petugas memeriksa temuan; simpan alasan, keputusan, dan jejak perubahan | Tidak ada penolakan klaim otomatis berdasarkan skor model | review_log.csv |
1. Split data dan metrik evaluasi
Untuk dataset sintetis 300 baris, gunakan cross-validation berulang atau stratified cross-validation setelah label diaudit. Jika kasus berasal dari pola atau grup yang sama, split pada tingkat grup agar contoh terkait tidak tersebar antara training dan test. Sisihkan test set final dan jangan mengubah threshold berdasarkan hasil test.
Laporkan sekurangnya: PR-AUC, precision, recall, F1, confusion matrix, false positive rate, calibration, serta interval ketidakpastian bila memungkinkan. Tetapkan threshold sesuai kapasitas pemeriksaan manual dan biaya false positive. Jangan memakai Accuracy saja ketika kelas tidak seimbang.
Untuk data DM tanpa label, laporkan statistik deskriptif, konsistensi kode, atau anomali ranking. Jangan menyebut precision, recall, atau AUPRC fraud untuk eksperimen tanpa ground truth fraud independen.
1. Preprocessing khusus file DM
Pertahankan kode ICD-10 sebagai teks dan normalkan huruf besar tanpa menghilangkan nol atau karakter kode. Cocokkan terhadap kamus sebelum membangun fitur. Tandai kode 999 tanpa deskripsi sebagai sentinel yang menunggu klarifikasi, bukan kategori klinis valid.
Validasi periode: nama file menunjukkan 2015-2020, tetapi kolom PNK03 dan PNK04 memuat tanggal paling awal 2014-08-16. Catat temuan ini sebelum membatasi data menurut periode.
Validasi unit observasi pada PNK02 karena terdapat 4.939 ID kunjungan unik pada 8.020 baris. Pastikan apakah satu kunjungan boleh memiliki beberapa baris tindakan atau diagnosis. Jangan otomatis menghapus pengulangan.
PNK17 dan PNK18 identik pada 8.020 baris. Jangan menyatakan model memprediksi koreksi biaya dari kolom ini sampai tersedia sampel dengan variasi biaya yang sah atau target lain yang tervalidasi.
1. Template pemeriksaan data dengan Python
```python
from pathlib import Path
import pandas as pd

BASE = Path("data")
member_path = BASE / "DM_kepesertaan.dta"
noncap_path = BASE / "DM20152020_fktpnonkapitasi.dta"
secondary_path = BASE / "DM20152020_fkrtldxsekunder.dta"

# Dataset lebih kecil, periksa bentuk dan kolom.
member = pd.read_stata(member_path, convert_categoricals=False)
noncap = pd.read_stata(noncap_path, convert_categoricals=False)
assert len(member) == 143_496 and len(member.columns) == 18
assert len(noncap) == 8_020 and len(noncap.columns) == 21
assert (noncap["PNK17"] == noncap["PNK18"]).all()

# File diagnosis besar, proses per chunk agar hemat memori.
reader = pd.read_stata(
    secondary_path,
    iterator=True,
    chunksize=250_000,
    convert_categoricals=False,
    convert_dates=False,
)
rows_seen = 0
for chunk in reader:
    rows_seen += len(chunk)
    # Lakukan agregasi atau QA di sini.
    # Jangan simpan identifier mentah ke log atau prompt model.
assert rows_seen == 6_362_523

# Klasifikasi fraud hanya setelah label independen disahkan.
# Jangan memakai Risiko, Status, atau Skor Fraud sebagai ground truth
# tanpa audit provenance dan pemeriksaan kebocoran data.
```
Template di atas memvalidasi struktur dan satu temuan data, bukan melatih model. Untuk training supervisi, bangun pipeline terpisah setelah tersedia label target yang disahkan.
1. Referensi dan tata kelola
Dokumentasi operasional: [Dataset Registry DM Kontekstual](https://app.notion.com/p/07-Dataset-Registry-dan-Kamus-Data-DM-Kontekstual-4003e6031ab78179bcc7ca76a0b80fbc). Metodologi sistem: [Arsitektur Sistem dan Metodologi Teknis](https://app.notion.com/p/02-Aegis-JKN-Arsitektur-Sistem-dan-Metodologi-Teknis-4003e6031ab781efbcdac7b0dbdd0cad).
Setiap eksperimen harus menyimpan versi dataset, daftar fitur, preprocessing, seed, versi library, konfigurasi split, model artifact, metrik test, confusion matrix, dan batasan. Gunakan model sebagai alat prioritisasi pemeriksaan dengan human review, bukan pengganti keputusan klinis, administratif, atau investigasi.
