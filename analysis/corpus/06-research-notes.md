<!-- source: notion page 4003e603-1ab7-8135-a0fa-ce33631104ab -->

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