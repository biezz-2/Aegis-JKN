<!-- source: notion page 4003e603-1ab7-8170-bc22-fe391c6a3a2a -->

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