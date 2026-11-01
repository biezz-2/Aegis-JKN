<!-- source: notion page 4003e603-1ab7-8174-9a55-d4ee8fff3fd2 -->

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