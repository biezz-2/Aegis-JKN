<!-- source: notion page 4003e6031ab78179bcc7ca76a0b80fbc -->

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