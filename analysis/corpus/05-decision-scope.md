<!-- source: notion page 4003e6031ab78156b244cccd2c5ecd9e -->

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