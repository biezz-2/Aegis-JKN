# Kandidat Ide Hackathon BPJS Kesehatan

> **Sumber Notion:** [Kandidat Ide Hackathon BPJS Kesehatan](https://app.notion.com/p/3f63e6031ab78111a885ea835e650bf2)  
> **ID Halaman:** `3f63e603-1ab7-8111-a885-ea835e650bf2`

---

> 🎯 Deteksi Efisiensi & Kecurangan Program JKN (Aegis-JKN Healthkathon BPJS)

Dokumen ini berisi pemetaan 3 kandidat ide solusi untuk pencegahan kebocoran dana dan peningkatan efisiensi operasional BPJS Kesehatan, hasil ekstraksi dan analisis berkas proposal.
---
## Kandidat 1: Anomali Diagnosa Jantung & Saraf (Upcoding)

> 🏥 Kategori: Efisiensi Risiko Fasilitas Kesehatan (Upcoding & Unbundling)

- **Masalah: **Faskes memanipulasi kode diagnosis pasien ke tingkat keparahan yang lebih tinggi (severity level III) atau memecah klaim tindakan yang seharusnya satu paket untuk mendapatkan tarif INA-CBG yang jauh lebih besar.
- **Bukti: **Temuan KPK dan BPJS sering menyoroti lonjakan drastis pada tagihan klaim penyakit kronis (seperti katarak, jantung, bedah saraf) di faskes tertentu yang tidak sejalan dengan profil epidemiologi wilayah tersebut.
- **Siapa yang Terdampak: **Finansial BPJS Kesehatan (mengalami kebocoran dana hingga triliunan rupiah) dan pasien sesungguhnya (antrean faskes penuh oleh tindakan medis yang diada-adakan).
- **Mekanisme Masalah: **Dokter atau koder di rumah sakit menambahkan komplikasi sekunder pada sistem e-Klaim yang tidak tercatat dalam rekam medis elektronik (EMR) pasien, memanfaatkan celah verifikasi manual BPJS yang memakan waktu lama.
- **Solusi Hipotesis: **Ekstraksi dan pencocokan otomatis menggunakan model bahasa lokal (Local LLM). Membangun pipeline yang membaca narasi teks pada EMR pasien, lalu mencocokkannya dengan kode ICD-10 yang diinput faskes. Jika ada ketidaksesuaian (misalnya EMR menyebut 'batuk ringan' tapi klaim menyebut 'pneumonia berat'), sistem langsung menahan klaim dan mengirimkan notifikasi flagging otomatis ke verifikator BPJS sebelum dana cair.
---
## Kandidat 2: Sindikat Joki Pasien (Penyalahgunaan Identitas)

> 👤 Kategori: Efisiensi Risiko Peserta JKN (Penyalahgunaan Identitas)

- **Masalah: **Pasien menggunakan kartu JKN milik orang lain (kerabat atau sewaan) untuk mengakses layanan kesehatan berbiaya tinggi (cuci darah, operasi, kemoterapi).
- **Bukti: **Laporan investigasi lapangan menunjukkan adanya ketidakcocokan identitas fisik pasien dengan data di sistem, terutama di faskes tingkat lanjut yang memiliki antrean panjang dan pengawasan visual minim.
- **Siapa yang Terdampak: **BPJS Kesehatan (membayar layanan untuk pihak yang tidak berhak) dan pemilik kartu asli (riwayat medisnya menjadi kacau, berisiko malapraktik di masa depan).
- **Mekanisme Masalah: **Faskes mengejar kecepatan pelayanan karena antrean membeludak, sehingga petugas administrasi sering melewatkan verifikasi fisik KTP/wajah dan hanya memindai nomor kartu atau NIK.
- **Solusi Hipotesis: **Modul Face Verification mandiri berbasis PWA (Progressive Web App). Pasien melakukan lapor diri (check-in) secara mandiri di mesin kiosk atau HP masing-masing melalui web app. Kamera akan menangkap wajah pasien dan mencocokkannya dengan database kependudukan/BPJS. Jika skor kecocokan rendah, akses sistem antrean terkunci dan dialihkan ke verifikasi manual.
---
## Kandidat 3: Manipulasi Gaji Pekerja (Under-reporting Upah)

> 💼 Kategori: Efisiensi Risiko Pemberi Kerja (Under-reporting Upah)

- **Masalah: **Perusahaan atau badan usaha dengan sengaja melaporkan gaji karyawan lebih rendah dari yang sebenarnya (biasanya disamakan dengan UMR) agar beban iuran 4% yang ditanggung perusahaan menjadi seminimal mungkin.
- **Bukti: **Terdapat selisih masif jika data iuran BPJS Kesehatan dikomparasi dengan data pelaporan pajak PPh 21 dari Direktorat Jenderal Pajak (DJP) atau standar gaji industri di wilayah tersebut.
- **Siapa yang Terdampak: **Peserta JKN/Pekerja (kelas rawat inap berpotensi turun) dan BPJS Kesehatan (kehilangan potensi penerimaan iuran yang signifikan).
- **Mekanisme Masalah: **HRD memanipulasi struktur slip gaji dengan mengecilkan 'Gaji Pokok' dan membesarkan 'Tunjangan Tidak Tetap' khusus untuk pelaporan ke BPJS, memanfaatkan minimnya integrasi data antar instansi pemerintah.
- **Solusi Hipotesis: **Platform agregasi data dan whistleblowing otomatis. Membuat sistem dashboard analitik yang mendeteksi anomali pelaporan gaji berdasarkan wilayah dan sektor industri. Solusi ini dilengkapi dengan bot pelaporan anonim (misalnya via Telegram/WhatsApp) bagi pekerja untuk mengunggah slip gaji asli mereka. Sistem akan secara otomatis memvalidasi bukti tersebut dan mengkalkulasi estimasi denda perusahaan.
---
## Rekomendasi Pilihan dan Justifikasi

> ⭐ PILIHAN UTAMA: Kandidat 1 (Anomali Diagnosa Jantung & Saraf / Upcoding). CADANGAN: Kandidat 3.

- **Alasan Pemilihan Kandidat 1: **Memiliki relevansi tertinggi terhadap mitigasi kebocoran Dana Jaminan Sosial (DJS) terbesar. Fraud klaim rujukan tingkat lanjut menyumbang porsi pemborosan dana BPJS paling masif.
- **Analisis Risiko Kandidat 2: **Kandidat 2 berisiko dianggap redundan karena BPJS Kesehatan sudah mengimplementasikan fitur biometrik FRIDAY / Face Recognition di aplikasi Mobile JKN dan loket faskes.
- **Posisi Kandidat 3: **Kandidat 3 sangat prospektif dari sisi revenue recovery, namun membutuhkan integrasi lintas kementerian (DJP Kemenkeu dan Kemenaker) yang memiliki friksi birokrasi lebih tinggi.
## Matriks Perbandingan Strategis 3 Kandidat

| **Parameter** | **Kandidat 1 (Upcoding)** | **Kandidat 2 (Joki Pasien)** | **Kandidat 3 (Under-reporting Upah)** |
| --- | --- | --- | --- |
| Potensi Efisiensi DJS | Sangat Tinggi (Triliunan) | Sedang hingga Tinggi | Tinggi (Iuran) |
| Kompleksitas Teknis | Sedang (NLP / Local LLM) | Rendah ke Sedang (Vision/PWA) | Rendah (Data Cross-match) |
| Risiko Redundansi | Rendah (Belum ada verifikasi otomatis) | Tinggi (Sudah ada FRIDAY Mobile JKN) | Rendah (Kanal baru) |
| Hambatan Regulasi | Internal BPJS & Faskes | Izin Akses Kependudukan / Dukcapil | Tinggi (Kemenkeu DJP & Kemenaker) |
| Rekomendasi Akhir | Pilihan Utama (Aegis-JKN) | Tidak Direkomendasikan | Cadangan Strategis |
