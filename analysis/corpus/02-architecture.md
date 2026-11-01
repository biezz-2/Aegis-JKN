<!-- source: notion page 4003e603-1ab7-81ef-bcda-c7b0dbdd0cad -->

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