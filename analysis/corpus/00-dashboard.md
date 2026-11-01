<!-- source: notion page 4003e603-1ab7-815a-89bd-edc0c4d92c2f -->

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