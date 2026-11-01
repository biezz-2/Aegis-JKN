<!-- source: notion page 4003e603-1ab7-814f-8ac3-f37808c0a4a5 -->

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