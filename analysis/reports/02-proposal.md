# 02 - Peer-Review Akademis Proposal Riset dan Inovasi Aegis-JKN (Edisi Akademik Revisi 1.0)

Status: Laporan tinjauan internal · Peer review untuk pengajuan Healthkathon BPJS Kesehatan 2026
Tanggal tinjauan: 22 Oktober 2026
Dokumen yang direview: `analysis/corpus/01-proposal.md` (93 baris, Revisi 1.0)
Dokumen pembanding: `analysis/corpus/11-archive-proposal.md` (430 baris, naskah sumber)
Basis pemeriksaan: 15 berkas `analysis/corpus/*.md`, `claims_v2_live.csv` (300 baris × 29 kolom), `dataset_research_live.csv` (33 entri), `14-index.md` (1.939 baris)
Notion tidak diakses. Seluruh kutipan diambil dari salinan lokal.

---

## 1. Ringkasan Eksekutif

Revisi 1.0 adalah perbaikan tata kelola yang nyata dan tidak boleh diregresi. Klaim kinerja yang sebelumnya disajikan sebagai fakta turunannya pada `01-proposal.md:70` menjadi daftar angka "belum dinyatakan sebagai hasil tervalidasi", dataset dinyatakan eksplisit sebagai simulasi (`01-proposal.md:9`), kata "terbukti/riil" hilang, dan ambang klaim operasional dirumuskan sebagai syarat (`01-proposal.md:71`). Semua angka nominal pada `01-proposal.md:66-69` cocok 100% dengan `claims_v2_live.csv`. Tata kelola bukti adalah bagian terkuat dari naskah ini.

Korpus secara keseluruhan belum aman, dan sumber masalahnya bukan Rev 1.0 melainkan tiga hal berikut.

**Pertama, naskah arsip tetap hidup tanpa status.** `11-archive-proposal.md:326-336` masih menandai 93,00%, 94,12%, 0,9825, dan 89,40% sebagai "(Tervalidasi)", `:347` menlabeli Rp507.370.000 sebagai "(Penyelamatan Riil)", dan `:348` mengekstrapolasi ke "ratusan miliar hingga triliunan rupiah per tahun". Banner di `:4` tidak mengubah status isi tabel. Seluruh arsip juga tercermin tanpa kualifikasi di `14-index.md:490-883`, sehingga pembaca yang mencari indeks menemukan klaim terlarang lebih dulu sebelum banner.

**Kedua, angka "benchmark" itu sendiri tidak sahih secara metodologis.** Penghitungan ulang atas `claims_v2_live.csv` menunjukkan kolom `Skor Fraud` memisahkan label secara sempurna: fraud 0,80-0,95, non-fraud 0,04-0,79, tanpa tumpang tindih. Pada ambang 0,80 hasilnya tp=36, fp=0, fn=0, presisi 1,00, AUC 1,00. Rata-rata skor per status juga cocok persis dengan angka arsip (`11-archive-proposal.md:338`): auto_clear 0,0862 vs "0.086", review 0,5908 vs "0.591", escalate 0,8689 vs "0.869". Metrik arsip dihitung dari kolom skor sintetis yang justru menjadi label, bukan dari model yang dilatih. Ini persis skenario yang dilarang `08-training-protocol.md:22` ("Jika label dibentuk dari skor, memasukkan skor tersebut membuat evaluasi sirkular dan tidak membuktikan kemampuan deteksi independen"). Keputusan terbuka D-03 ("Reproduksi benchmark yang ditulis di proposal") di `02-architecture.md:111` masih berstatus Terbuka.

**Ketiga, rincian finansial arsip kontradiktif terhadap dataset yang menopangnya.** `11-archive-proposal.md:348` menyebut tiga modus terbesar sebagai Phantom Billing Rp134,25 Juta, Upcoding Rp127,68 Juta, dan Repeat Billing Rp61,60 Juta. Data aktual memberi tiga modus terbesar yang berbeda: upcoding Rp156.900.000, phantom_billing Rp134.250.000, dan iur_biaya Rp63.880.000. Angka Rp127,68 Juta untuk upcoding tidak ada di data.

Di sisi lain, revisi membawa kebalikan masalah: naskah sekarang tidak punya hipotesis falsifiable, tidak punya bagian kebaruan, dan nol penanda sitasi. Delapan belas entri daftar pustaka arsip (`11-archive-proposal.md:413-430`) semuanya referensi yatim karena tidak ada satu pun penanda `[n]` di badan naskah.

### Tabel Severity

| Severity | Jumlah | Ciri |
|---|---|---|
| KRITIS | 7 | Melanggar `00-dashboard.md:46-52` dan `04-evidence-matrix.md:90`; merusak keabsahan hasil; klaim terlarang tetap hidup di arsip dan indeks |
| MAYOR | 13 | Merusak validitas metodologis, konsistensi data, atau kelengkapan naskah akademik |
| MINOR | 5 | Ketelitian editorial, duplikasi dokumen, jejak revisi |
| **Total** | **25** | |

Rincian temuan ada di bagian 3 sampai 7. ID K = KRITIS, M = MAYOR, N = MINOR. Daftar ringkas per ID ada di Lampiran C.

---

## 2. Penilaian per Kriteria Akademik

Skor 1 (sangat lemah) sampai 5 (sangat baik).

| Kriteria | Skor | Alasan singkat dan bukti |
|---|---|---|
| Kejelasan rumusan masalah | 4 | `01-proposal.md:15-21` memuat lima pertanyaan yang runcing dan terikat pada unit klaim. Dedeksi: tidak ada kuantifikasi masalah nasional, sehingga urgensi tidak dapat diuji pembaca; `01-proposal.md:14` justru menyatakan angka nasional "harus didukung rujukan primer" tanpa memberi rujukan apa pun. |
| Tujuan penelitian | 4 | `01-proposal.md:22-28` memetakan lima tujuan ke lima pertanyaan; `01-proposal.md:75-82` memetakan tujuan ke tahap rencana kerja dengan kriteria selesai. Konsisten. |
| Hipotesis / pertanyaan riset | 3 | Pertanyaan ada (`01-proposal.md:15-21`) tetapi tidak falsifiable: tidak ada arah, ambang, atau variabel terukur. Bandingkan arsip `11-archive-proposal.md:292` yang punya Precision ≥ 90%, FPR ≤ 15%, waktu telaah 30-50%. Konsekuensi: proyek tidak dapat "gagal" secara terdefinisi. (M-02) |
| Metodologi | 4 | Pencegahan leakage (`01-proposal.md:46-47`), daftar metrik dengan kalibrasi (`01-proposal.md:48-49`), dan protokol artefak (`01-proposal.md:50-51`) sudah tepat. Dedeksi: tidak ada power analysis, ukuran sampel target, uji signifikansi, atau protokol multi-seed; `01-proposal.md:44` menaruh definisi node, edge, fitur, metapath pada "akan didokumentasikan". |
| Signifikansi | 3 | Dinyatakan pada `01-proposal.md:13` dan `:63-64`, tetapi penerima manfaat, jalur kebijakan, dan biaya tidak dihitung. `05-decision-scope.md:19` sendiri mencatat bahwa bobot penilaian kandidat "belum melalui lokakarya tim yang terdokumentasi". |
| Novelty / kebaruan | 2 | Tidak ada bagian kebaruan. Kontribusi pada `01-proposal.md:29` seluruhnya berupa artefak (arsitektur, spesifikasi data, protokol, antarmuka, dokumentasi), bukan klaim ilmiah yang berbeda dari literatur. Istilah "MHGSL" tidak muncul sama sekali di Rev 1.0 (28 kemunculan di arsip), sehingga diferensiasi utama proyek hilang. `05-decision-scope.md:71` sudah menegaskan "Kompleksitas graph learning bukan tujuan tersendiri". (M-03) |
| Struktur IMRaD | 3 | Ada Pendahuluan, Metodologi, dan Kesimpulan, serta §8 "Status Bukti dan Hasil". Dedeksi: tidak ada Hasil (hanya status klaim), tidak ada abstrak bahasa Inggris, tidak ada nomor tabel atau figur, dan belum ada Tinjauan Pustaka meski `06-research-notes.md:46-57` sudah menyediakan protokolnya. |
| Sitasi dan daftar pustaka | 1 | `01-proposal.md:85-91` memuat empat peraturan, satu URL, dan satu placeholder yang menyatakan metadata bibliografi "harus dicantumkan". Nol penanda sitasi dalam teks. Empat kelompok sumber awal sudah tersedia di `06-research-notes.md:58-64` tetapi belum diproses. (M-01) |
| Tata kelola bukti dan kualifikasi klaim | 5 | Rev 1.0 memenuhi `00-dashboard.md:79` (bedakan fakta dari rancangan), `:81` (sitasi spesifik), `:85` (catat perubahan), `:90` (status Tervalidasi butuh bukti pihak lain) dan `04-evidence-matrix.md:70-77`. Konsistensi istilah: "hasil sementara", "belum tervalidasi", "perlu rujukan primer", "nilai nominal ... tidak dengan sendirinya membuktikan". Tidak ada kata terlarang di Rev 1.0. |
| Rekonsiliasi angka dataset | 5 | Semua angka pada `01-proposal.md:66-69` cocok persis dengan `claims_v2_live.csv`: total Rp3.526.650.000, auto_clear Rp2.685.550.000, review Rp279.950.000, escalate Rp561.150.000; label 240/10/14/36 dan status 240/24/36 juga cocok. Satu-satunya dokumen di korpus yang benar secara numerik. |

**Rata-rata 3,4 / 5.** Naskah layak sebagai kerangka proposal setelah bagian 4, 5, dan 9 diperbaiki, tetapi belum layak sebagai naskah akademik final.

---

## 3. Tabel Audit Angka

Status: **AMAN** = muncul dengan kualifikasi sesuai `00-dashboard.md:46-52`; **TIDAK DIKUALIFIKASI** = disajikan sebagai fakta hasil; **KONFLIK** = disajikan sebagai hasil tetapi bertentangan dengan data aktif atau dengan dasbor.

### 3.1 Accuracy 93,0% / 93.00% (K-06, K-02)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:47` | "Accuracy 93,0%, precision 94,12%, ROC-AUC 0,9825, dan AUPRC 0,9142." (daftar "Belum boleh disebut hasil tervalidasi") | AMAN | Tidak diubah. |
| `01-proposal.md:70` | "Draf sebelumnya mencantumkan accuracy 93,0% ... Angka tersebut belum dinyatakan sebagai hasil tervalidasi dalam edisi ini" | AMAN | Pertahankan. Tambahkan rujukan silang ke `00-dashboard.md:47`. |
| `11-archive-proposal.md:15` | "Seluruh metrik teknis (Akurasi 93.0% ...) dihitung berbasis metodologi empiris portofolio 300 klaim terverifikasi yang dapat direplikasi secara objektif" | TIDAK DIKUALIFIKASI | Hapus frasa "dapat direplikasi secara objektif" dan "300 klaim terverifikasi". Bandingkan `00-dashboard.md:52` yang menuntut ID eksperimen, split, kode, prediksi, label pembanding, dan skrip perhitungan. |
| `11-archive-proposal.md:30` | "Evaluasi empiris ... membuktikan performa superior model MHGSL: Akurasi 93.0% ..." | TIDAK DIKUALIFIKASI | Ganti "membuktikan performa superior" dengan "hasil sementara pada data simulasi". |
| `11-archive-proposal.md:326` | Tabel 8.1: "93.00% (Tervalidasi)" | TIDAK DIKUALIFIKASI | Hapus label "(Tervalidasi)". Pelanggaran langsung `00-dashboard.md:90`. |
| `14-index.md:490`, `:505`, `:801` | "Seluruh metrik teknis (Akurasi 93.0% ...)" dan "93.00% (Tervalidasi)" | TIDAK DIKUALIFIKASI | Cap arsip per-baris pada indeks, atau keluarkan tabel KPI dari indeks. |

### 3.2 Precision 94,12% / 94.12% (K-06, K-02)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:47` | Daftar larangan | AMAN | Tidak diubah. |
| `01-proposal.md:70` | "precision 94,12% ... belum dinyatakan sebagai hasil tervalidasi dalam edisi ini" | AMAN | Pertahankan. |
| `11-archive-proposal.md:15`, `:30` | "Presisi 94.12% ... membuktikan performa superior" | TIDAK DIKUALIFIKASI | Sama seperti 3.1. |
| `11-archive-proposal.md:327` | Tabel 8.1: "94.12% (Tervalidasi)" | TIDAK DIKUALIFIKASI | Hapus "(Tervalidasi)". |
| `14-index.md:490`, `:505`, `:802` | Salinan arsip | TIDAK DIKUALIFIKASI | Cap arsip pada indeks. |

**Tambahan hasil verifikasi (lihat `16-red-team.md` §3.3 dan `21-colab-dashboard-provenance.md` H-5).** Presisi 94,12% tidak sekadar "tidak ada artefak", melainkan **tidak tercapai pada ambang mana pun**: pemindaian exhaustif atas 46 nilai unik `skor_fraud` pada dataset 300 menghasilkan 0 ambang dengan presisi 94,12%. Presisi terdekat adalah 94,7368% (ambang 0,78), lalu 92,3077% (0,74). Di ambang 0,80 presisi justru **100%** dengan FPR 0,00%, karena `skor_fraud` memisahkan kelas secara deterministik (non-fraud maksimum 0,79 < fraud minimum 0,80). Jadi angka 94,12% bukan hanya tanpa sumber, melainkan **lebih rendah dari apa yang data itu berikan tanpa model apa pun, dan mustahil dicapai**.

### 3.3 ROC-AUC 0,9825 (K-06, K-02)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:47` | Daftar larangan | AMAN | Tidak diubah. |
| `01-proposal.md:70` | "ROC-AUC 0,9825 ... belum dinyatakan sebagai hasil tervalidasi" | AMAN | Pertahankan. |
| `11-archive-proposal.md:15`, `:30` | "ROC-AUC 0.9825 ... membuktikan performa superior" | TIDAK DIKUALIFIKASI | Sama seperti 3.1. |
| `11-archive-proposal.md:328` | Tabel 8.1: "0.9825 (Tervalidasi)" | TIDAK DIKUALIFIKASI | Hapus "(Tervalidasi)". |
| `14-index.md:490`, `:505`, `:803` | Salinan arsip | TIDAK DIKUALIFIKASI | Cap arsip pada indeks. |

### 3.4 AUPRC 0,9142 (K-01, K-06, K-02)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:47` | Daftar larangan | AMAN | Tidak diubah. |
| `01-proposal.md:70` | "AUPRC 0,9142 ... belum dinyatakan sebagai hasil tervalidasi" | AMAN | Pertahankan. |
| `04-evidence-matrix.md:34` | "E-07 ... Belum tereproduksi pada audit ini" | AMAN | Sudah benar. |
| `06-research-notes.md:42` | "Belum dapat direproduksi dari artefak yang diperiksa" | AMAN | Sudah benar. |
| `14-index.md:1167`, `:1284`, `:1565`, `:1735` | Baris matriks bukti dan daftar larangan | AMAN | Sudah benar. |
| `11-archive-proposal.md:15`, `:30` | "AUPRC 0.9142 (+28.6% dibanding baseline XGBoost 0.71) ... membuktikan" | TIDAK DIKUALIFIKASI | Hapus "membuktikan"; label "simulasi sintetis, prevalensi oversampled". |
| `11-archive-proposal.md:329` | Tabel 8.1: "0.9142 (+28.6% vs XGBoost)" | TIDAK DIKUALIFIKASI | Hilangkan klaim banding; baseline 0,7100 tidak punya artefak. `08-training-protocol.md:33` mewajibkan "Baseline, split, seed, dan metrik dapat diulang". |
| `11-archive-proposal.md:338` | "Pengujian komparatif membuktikan keunggulan mutlak arsitektur MHGSL. Model baseline XGBoost hanya mencapai AUPRC sebesar 0.7100" | TIDAK DIKUALIFIKASI | Hapus. Bandingkan `12-archive-architecture.md:55` yang justru melabeli angka "+20%, reduksi false negatives 42%" sebagai "adaptasi literatur ... bukan hasil eksperimen internal". |
| `14-index.md:490`, `:505`, `:804`, `:813` | Salinan arsip | TIDAK DIKUALIFIKASI | Cap arsip pada indeks. |

### 3.5 Ketahanan masking 89,4% / 89.40% (K-06, K-02)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:48` | "Ketahanan masking 89,4% dan false positive rate 10,6%." | AMAN | Tidak diubah. |
| `01-proposal.md:70` | "ketahanan masking 89,4% ... belum dinyatakan sebagai hasil tervalidasi" | AMAN | Pertahankan. |
| `11-archive-proposal.md:30` | "ketahanan kamuflase mencapai 89.4% pada tingkat masking rujukan 40%" | TIDAK DIKUALIFIKASI | Hapus. `02-architecture.md:74` mewajibkan penjelasan "apa yang dimasking, berapa proporsi edge yang diubah, apakah label dipertahankan". |
| `11-archive-proposal.md:182` | Tabel perbandingan: "Tinggi (89.4% akurasi pada 40% kamuflase)" | TIDAK DIKUALIFIKASI | Kolom perbandingan memuat angka tanpa jejak. Ubah menjadi deskripsi kualitatif. |
| `11-archive-proposal.md:330` | Tabel 8.1: "89.40% (Tervalidasi)" | TIDAK DIKUALIFIKASI | Hapus "(Tervalidasi)". |
| `14-index.md:505`, `:657`, `:805` | Salinan arsip | TIDAK DIKUALIFIKASI | Cap arsip pada indeks. |

### 3.6 False positive rate 10,6% / 10.60% (K-06, K-02)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:48` | Daftar larangan | AMAN | Tidak diubah. |
| `01-proposal.md:70` | "false positive rate 10,6% ... belum dinyatakan sebagai hasil tervalidasi" | AMAN | Pertahankan. |
| `11-archive-proposal.md:30`, `:340` | "Penekanan False Positive Rate hingga 10.6% secara efektif melindungi verifikator dari kejenuhan kognitif" | TIDAK DIKUALIFIKASI | Hapus. |
| `11-archive-proposal.md:332` | Tabel 8.1: "10.60% (Menekan alert fatigue)" | TIDAK DIKUALIFIKASI | Hilangkan nilai. |
| `14-index.md:807`, `:1168` | Salinan arsip | TIDAK DIKUALIFIKASI | Cap arsip. |

**Catatan hasil verifikasi.** Angka 10,6% ini sebenarnya **dapat dihitung ulang** dari data aktif: ambang `skor_fraud ≥ 0,14` pada dataset 300 menghasilkan tepat FP = 28 dari 264 negatif, yaitu FPR = 10,6061% yang dibulatkan 10,6%. Yang tidak dapat dipertahankan adalah pemakaiannya **bersama** presisi 94,12%, karena presisi pada ambang 0,14 hanya 56,25%, dan tidak ada satu ambang yang memenuhi kedua angka itu. Kalau FPR tetap dipakai, tulis bersamanya: "10,61% pada ambang 0,14 di 300 klaim simulasi, presisi 56,25% pada ambang itu".

### 3.7 Penurunan waktu telaah 45% (K-06, K-02)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:49` | "Penurunan waktu telaah 45%, throughput 3,2 kali, dan SUS 82,5." | AMAN | Tidak diubah. |
| `01-proposal.md:70` | "Draf sebelumnya mencantumkan ... " (kualifikasi aktif atas seluruh angka) | AMAN | Pertahankan. |
| `11-archive-proposal.md:331` | Tabel 8.1: "45.0% (Hemat 5-10 mnt/berkas)" | TIDAK DIKUALIFIKASI | Hapus. `04-evidence-matrix.md:37` (E-10) menyatakan "Belum dibuktikan dengan artefak yang tersedia" dan "Jangan satukan dengan klaim E-09 sebelum sumbernya dipastikan". |
| `11-archive-proposal.md:340` | "Waktu telaah awal terpangkas 45%, dari 10-20 menit per berkas menjadi 3-5 menit" | TIDAK DIKUALIFIKASI | Hapus. Klaim 20 menit menjadi 3 menit juga bermasalah: `dataset_research_live.csv:3` mencatat "belum ditemukan studi publik BPJS tentang durasi verifikasi rata-rata per berkas" dengan status "Perlu Verifikasi". |
| `14-index.md:806`, `:815`, `:1169` | Salinan arsip | TIDAK DIKUALIFIKASI | Cap arsip. |

### 3.8 Throughput 3,2 kali / 3.2x (K-07)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:49` | "throughput 3,2 kali" (daftar larangan) | AMAN | Tidak diubah. |
| `01-proposal.md` | **Tidak ada** | AMAN (tidak dimuat) | Angka dihapus tanpa jejak. Pelanggaran `00-dashboard.md:84` dan `:85`. Lihat K-07. |
| `11-archive-proposal.md:333` | Tabel 8.1: "3.2x lipat kapasitas harian" | TIDAK DIKUALIFIKASI | Hapus. |
| `11-archive-proposal.md:350` | "verifikator mampu menyelesaikan telaah 3.2 kali lebih banyak berkas per jam kerja" | TIDAK DIKUALIFIKASI | Hapus. `01-proposal.md:81` masih menulis tahap "5. Evaluasi pengguna" dengan kriteria "Proses dan hasil usability" sebagai pekerjaan yang belum berjalan, sehingga A/B testing tidak punya protokol. |
| `14-index.md:808`, `:825`, `:1169` | Salinan arsip | TIDAK DIKUALIFIKASI | Cap arsip. |

### 3.9 SUS 82,5 / 82.5 (K-07)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:49` | "SUS 82,5" (daftar larangan) | AMAN | Tidak diubah. |
| `01-proposal.md` | **Tidak ada** | AMAN (tidak dimuat) | Angka dihapus tanpa jejak. Lihat K-07. |
| `11-archive-proposal.md:335` | Tabel 8.1: "82.5 / 100 (Kategori 'Excellent')" | TIDAK DIKUALIFIKASI | Hapus. |
| `11-archive-proposal.md:350` | "Evaluasi antarmuka menghasilkan skor System Usability Scale (SUS) sebesar 82.5/100 (kategori 'Grade A / Excellent')" | TIDAK DIKUALIFIKASI | Hapus. Tidak ada jumlah partisipan, kuesioner, atau n yang tercatat di mana pun dalam korpus. |
| `14-index.md:810`, `:825`, `:1169` | Salinan arsip | TIDAK DIKUALIFIKASI | Cap arsip. |

### 3.10 Estimasi penyelamatan Rp507.370.000 (K-04)

| Dokumen & baris | Konteks kutipan | Status | Perbaikan yang disarankan |
|---|---|---|---|
| `00-dashboard.md:39` | "perhitungan estimasi overcharge Rp507.370.000 belum dapat direproduksi per klaim dari properti database saat ini karena tarif pembanding, formula, dan status validasi independen belum tercatat secara lengkap" | AMAN | Sudah benar. |
| `00-dashboard.md:50` | "Penghematan atau penyelamatan finansial yang dihitung dari dataset." (larangan) | AMAN | Sudah benar. |
| `01-proposal.md:70` | "estimasi penyelamatan Rp507.370.000. Angka tersebut belum dinyatakan sebagai hasil tervalidasi dalam edisi ini ... Nilai nominal klaim yang tercatat tidak dengan sendirinya membuktikan besarnya overcharge atau nilai yang dapat diselamatkan" | AMAN | Pertahankan. |
| `04-evidence-matrix.md:38` | "E-11 ... Belum dapat direproduksi per klaim ... Tambahkan tarif acuan, formula, dan status adjudikasi ke database" | AMAN | Sudah benar. |
| `06-research-notes.md:45` | "Penghematan finansial ... Belum dapat direproduksi dari data biaya saja" | AMAN | Sudah benar. |
| `11-archive-proposal.md:15` | "estimasi penyelamatan overcharge tarif INA-CBG sebesar Rp 507,37 Juta ... dapat direplikasi secara objektif" | TIDAK DIKUALIFIKASI | Hapus klaim "dapat direplikasi secara objektif". Tidak ada tarif pembanding, formula, maupun adjudikasi. |
| `11-archive-proposal.md:347` | Tabel 8.2: "Rp 507.370.000 (Penyelamatan Riil)" | TIDAK DIKUALIFIKASI | Kata "Riil" dilarang eksplisit oleh `04-evidence-matrix.md:90`. |
| `11-archive-proposal.md:348` | "mendeteksi potensi kebocoran tarif (overcharge) sebesar Rp 507.370.000 (60.32% dari nominal klaim anomali, dengan rata-rata kerugian Rp 8.456.167 per kasus)" | **KONFLIK** | Angka 60,32% adalah 507.370.000 / 841.100.000, dan Rp8.456.167 adalah 507.370.000 / 60, yaitu angka pembagian, bukan estimasi kerugian. Tabel 8.2 pada `:345-346` memecah total itu menjadi Rp112.420.000 (review) dan Rp394.950.000 (escalate), yang persis 40,157% dari Rp279.950.000 dan 70,382% dari Rp561.150.000. Tidak ada subset klaim mana pun yang menjumlah menjadi kedua angka itu, sehingga keduanya adalah haircut proporsional yang tidak dijelaskan, bukan kalkulasi tarif. Hapus, atau ganti dengan tabel tarif acuan dan formula per klaim sesuai `02-architecture.md:112` (D-04, status Terbuka). |
| `11-archive-proposal.md:348` | "potensi dana DJS yang dapat diselamatkan mencapai ratusan miliar hingga triliunan rupiah per tahun" | **KONFLIK** | Ekstrapolasi dari dataset sintetis ke beban klaim Rp150+ Triliun. `05-decision-scope.md:64` menempatkan "klaim penghematan nasional yang diekstrapolasi dari dataset sintetis" sebagai out-of-scope, dan `04-evidence-matrix.md:74` melarang "Statistik nasional ... diekstrapolasi secara mekanis dari dataset sintetis". Hapus. |
| `14-index.md:822`, `:823` | Salinan arsip | TIDAK DIKUALIFIKASI / KONFLIK | Cap arsip pada indeks. |
| `14-index.md:1159`, `:1569` | Baris governance | AMAN | Sudah benar. |

### 3.11 Angka turunan lain yang bermasalah

| Angka | Dokumen & baris | Status | Perbaikan |
|---|---|---|---|
| Rasio Cost-to-Impact 1 : 15 | `11-archive-proposal.md:147`, `:334`, `:363`, `:402`, `:404`; `14-index.md:622`, `:809`, `:838`, `:877`, `:879` | TIDAK DIKUALIFIKASI | Klaim finansial tanpa model biaya. `dataset_research_live.csv:18` hanya memuat "asumsi 3% fraud" pada simulasi. Jadikan target, bukan capaian, atau hapus. |
| Override rate 12,4% | `11-archive-proposal.md:336`; `14-index.md:811` | TIDAK DIKUALIFIKASI | Tidak ada log review verifikator di korpus. Hapus. |
| Rp25 miliar, 3 rumah sakit swasta, 2024 | `13-archive-deep-research.md:3` | TIDAK DIKUALIFIKASI | Tanpa sumber. `13-archive-deep-research.md:4` sendiri mengharuskan pelacakan sumber primer. |
| 175.774 klaim FKRTL berpotensi fraud | `12-archive-architecture.md:116` | TIDAK DIKUALIFIKASI | Kutipan ACCH KPK tanpa URL primer dalam korpus; entri register ACCH (`dataset_research_live.csv:23`, `:29`) hanya menyokong modus fraud, bukan angka. |
| 1.000 verifikator, 2 juta klaim/hari | `11-archive-proposal.md:22`, `:128`; `12-archive-architecture.md:5` | TIDAK DIKUALIFIKASI | Sumber primer bukan sumber primer. `dataset_research_live.csv:25` mencatat angka 1.000 verifikator "bersumber dari dokumen sumber & repo Aegis-JKN; belum ditemukan rilis resmi BPJS independen". Lihat K-05. |
| 270 juta jiwa, 150+ Triliun | `11-archive-proposal.md:22`, `:162`, `:348` | TIDAK DIKUALIFIKASI | Tidak ada entri register yang memuat angka ini. |
| 12,4% override, 30-50% waktu telaah | `11-archive-proposal.md:145`, `:292` | TIDAK DIKUALIFIKASI | Tanpa protokol uji. |
| Rp20 trillions | Hanya di `dataset_research_live.csv:31` (sumber media sekunder) | AMAN di register | Jangan masuk proposal sebagai fakta. |
| 10.386 / 15.202 / 7.880 edges | `11-archive-proposal.md:209-211` | TIDAK DIKUALIFIKASI | Tidak ada berkas edge di korpus maupun di dataset. Angka tepi tidak dapat dihitung ulang. |
| W_feat 0,38, W_sem 0,41, W_top -0,12 | `11-archive-proposal.md:220` | TIDAK DIKUALIFIKASI | Angka hasil training tanpa checkpoint atau log training. |
| Rp542,56 Juta "sembilan sindikat" | `11-archive-proposal.md:348` | **KONFLIK** | Data aktual: 34 dari 36 klaim fraud punya ID sindikat, 8 ID berbeda, total Rp524.750.000. Dua klaim fraud tanpa sindikat: KLM121 biaya_markup Rp27.500.000 dan KLM122 drug_diversion Rp8.900.000. Lihat M-11. |
| "31 fitur" | `11-archive-proposal.md:321` | **KONFLIK** | CSV aktif punya 29 kolom, 2 di antaranya metadata internal, sehingga 27 kolom data. Lihat M-09. |
| Rp8.456.167 rata-rata kerugian | `11-archive-proposal.md:348` | **KONFLIK** | 507.370.000 / 60 = 8.456.166,67. Angka pembagian, bukan estimasi kerugian per kasus. |

### 3.12 Angka yang direkonsiliasi dengan benar (AMAN, tanpa temuan)

| Angka | Dokumen & baris | Status |
|---|---|---|
| Total Rp3.526.650.000, auto_clear Rp2.685.550.000, review Rp279.950.000, escalate Rp561.150.000 | `01-proposal.md:66-69`; `00-dashboard.md:39`; `11-archive-proposal.md:344-346` | AMAN (cocok dengan CSV) |
| Distribusi 240 low / 10 medium / 14 high / 36 fraud; 240 auto_clear / 24 review / 36 escalate | `01-proposal.md:37` | AMAN (cocok dengan CSV) |
| 109 baris dengan LOS hari bermasalah | `00-dashboard.md:36`; `03-dataset-registry.md:78` | AMAN pada hitungan, KESALAHAN pada representasi (lihat M-12) |

---

## 4. Klaim Kuantitatif Tanpa Sitasi Primer

### 4.1 Revisi 1.0 tidak memiliki sitasi apa pun (M-01, severity MAYOR)

- `01-proposal.md:85-91` memuat empat peraturan, satu URL SATUSEHAT, dan satu placeholder: "Referensi teknis XGBoost, graph neural networks, SHAP, dan evaluasi model harus dicantumkan dengan metadata bibliografi lengkap dan hubungan yang jelas dengan klaim yang didukung." Ini pengakuan bahwa daftar pustaka belum ada.
- Nol penanda sitasi dalam badan teks Rev 1.0. Tidak ada pola `[n]`, `(Author, year)`, maupun `et al.`. Tidak ada satu klaim pun yang punya rujukan dekat. Pelanggaran `00-dashboard.md:81` ("Semua klaim eksternal memiliki sitasi spesifik") dan `04-evidence-matrix.md:71` ("Fakta eksternal harus memiliki sitasi dekat dengan klaim").
- `06-research-notes.md:58-64` sudah menyediakan sumber awal yang siap diproses, termasuk konvensi: "setiap klaim kuantitatif perlu dilacak ke sumber primer apabila tersedia". Sumber itu belum dipakai.

### 4.2 Daftar pustaka arsip adalah referensi yatim (M-01)

`11-archive-proposal.md:413-430` memuat 18 entri, 8 di antaranya artikel peer-reviewed (PathSim, HAN, GCN, PyG, Focal Loss, SHAP, GraphSAINT, OASIS). Dicek pada badan naskah baris 1 sampai 411: **tidak ada satu pun penanda `[n]`**. Ke-18 entri adalah referensi yatim, melanggar `04-evidence-matrix.md:85` ("Daftar pustaka tidak memuat sumber yang tidak pernah dikutip dalam teks") secara literal. Ironisnya, arsip juga punya daftar pustaka yang jauh lebih lengkap daripada Rev 1.0, sehingga revisi justru mengurangi kapasitas sitasi.

### 4.3 Klaim di arsip yang tidak dapat ditelusuri ke sumber primer

| Klaim | Lokasi | Masalah |
|---|---|---|
| "Akurasi 93.0%, Presisi 94.12%, ROC-AUC 0.9825, AUPRC 0.9142" | `11-archive-proposal.md:15` | Dinyatakan "dapat direplikasi secara objektif" tanpa ID eksperimen, split, kode, atau skrip. Pencarian `*.{ts,tsx,py,json,md,csv}` di repo aplikasi tidak menemukan satupun angka ini. |
| "+28.6% dibanding baseline XGBoost 0.71" | `11-archive-proposal.md:30`, `:329`, `:338` | Angka baseline tidak punya artefak. Bandingkan `08-training-protocol.md:33`. |
| "AUPRC meningkat 20% dan false negatives turun 42% dibanding baseline XGBoost" | `12-archive-architecture.md:30`, `:55` | `dataset_research_live.csv:9` mencatat "angka spesifik +20% AUPRC / -42% FN tidak ditemukan di sumber terbuka"; status register "Perlu Verifikasi". Tidak ada sitasi dalam badan proposal yang menunjuk sumber ini. |
| "1.000 verifikator", "2 juta klaim/hari", "270+ juta jiwa" | `11-archive-proposal.md:22`, `:128`, `:162`, `:372`; `12-archive-architecture.md:5` | `dataset_research_live.csv:25`: "Angka 1.000 verifikator bersumber dari dokumen sumber & repo Aegis-JKN; belum ditemukan rilis resmi BPJS independen". Sumber primer proyek sendiri bukan sumber independen. |
| "175.774 klaim FKRTL berpotensi fraud hingga Juni 2015" | `12-archive-architecture.md:116` | Tidak ada entri register yang memuat angka ini. |
| "10.386 / 15.202 / 7.880 edges" | `11-archive-proposal.md:209-211` | Tidak dapat dihitung ulang tanpa artefak graf. |
| "31 fitur standar INA-CBG/FHIR R4" | `11-archive-proposal.md:321` | CSV aktif punya 27 kolom data. |
| "bobot atensi optimal W_feat 0,38, W_sem 0,41, W_top -0,12" | `11-archive-proposal.md:220` | Tanpa checkpoint atau log training. |
| "Heliyon, 10(4), e26115" | `11-archive-proposal.md:429` | Konflik metadata: entri register yang terverifikasi menunjuk Hong et al., DOI 10.1016/j.heliyon.2024.e30045 (`dataset_research_live.csv:11`), sedangkan arsip menulis e26115 dengan penulis "Heliyon Medical Intelligence Group". Dua identitas berbeda untuk sumber yang sama, dan arsip tidak pernah mengutipnya di teks. Verifikasi eksternal via SearXNG gagal pada dua percobaan (engine brave dan google cse suspended, duckduckgo CAPTCHA). Status laporan: **referensi tidak terverifikasi, kemungkinan salah kutipan**, bukan klaim fabrikasi. (N-05) |
| "Laporan Pengelolaan Program JKN dan Kinerja Keuangan BPJS Kesehatan Tahun 2023" | `11-archive-proposal.md:413` | Entri [1] tidak pernah dikutip di teks dan tidak ada di `dataset_research_live.csv`. |

### 4.4 Klaim yang aman justru kehilangan substansi

`01-proposal.md:14` menyatakan angka nasional "harus didukung rujukan primer yang spesifik sebelum digunakan sebagai fakta dalam versi final publikasi". Secara tata kelola ini benar, tetapi konsekuensinya adalah naskah sekarang **tidak memiliki kuantifikasi masalah sama sekali** (Pendahuluan `:11-14` sepenuhnya kualitatif). Ini bukan temuan BAHAYA, melainkan celah yang harus ditutup pada revisi berikutnya, bukan dibiarkan selamanya.

---

## 5. Inkonsistensi Internal

### I-01 (M-04, MAYOR) - Skala ambang risiko berbeda antara arsip dan dataset

- Arsip `11-archive-proposal.md:229-231`: Hijau "Skor < 0.35", Kuning "Skor 0.35 s/d 0.70", Merah "Skor > 0.70".
- Dataset `09-draft-hub.md:12` dan `:116`, `10-simulation-dataset.md:9` dan `:113`: "skor <0.35 low; 0.35-0.6 medium; 0.6-0.8 high; lebih dari 0.8 fraud".

Dampak terukur di `claims_v2_live.csv`: 5 dari 14 baris berlabel `high` memiliki `Skor Fraud` ≥ 0,70 (rata-rata label high 0,6829). Di bawah skala arsip, 5 baris itu seharusnya Merah dan masuk eskalasi, tetapi status aktualnya `review`. Skala 0,35/0,60/0,80 yang dipakai proyek konsisten dengan data; skala arsip tidak. `03-dataset-registry.md:46` sudah menandai varian kalimat versi 100 klaim tetapi belum menandai konflik arsip ini.

### I-02 (M-05, MAYOR) - Batas label pada 0,80 belum eksplisit

`09-draft-hub.md:12` dan `10-simulation-dataset.md:9` menulis "lebih dari 0.8 fraud", bukan "≥ 0.8". Pada `claims_v2_live.csv` ada tepat satu baris fraud dengan `Skor Fraud` = 0,80, yaitu KLM115 (RS_J, D19, excessive_usage, Rp2.150.000, status escalate). Dengan operator "lebih dari", baris itu seharusnya bukan fraud. Ini persis kasus yang di-flag `03-dataset-registry.md:46`: "Catatan versi 100 klaim sebelumnya menggunakan frasa yang bisa dibaca sebagai skor 0,80 tidak termasuk kelas fraud, sedangkan database aktif memiliki skor fraud 0,80." Belum ditutup. `03-dataset-registry.md:46` juga menuntut "ambang skor harus disimpan di satu tempat dan diberi versi" dan "batas interval perlu ditulis tanpa celah atau tumpang tindih".

### I-03 (M-06, MAYOR) - Tabel sindikat arsip dan dataset memakai ID yang sama untuk skenario berbeda

`11-archive-proposal.md:296-304` mendefinisikan SYND-01..09 dengan faskes, dokter, dan klaim yang berbeda total dari `09-draft-hub.md:134-147`. Contoh konkret:

| ID | Arsip `11-archive-proposal.md:296-304` | Dataset `09-draft-hub.md:134-147` |
|---|---|---|
| SYND-04 | Drug Diversion, RS_D, D09+D10, KLM013-015, "≥ 0.88 (Escalate)" | Drug Diversion, RS_E, D09, KLM013-014, "0.86-0.88" |
| SYND-05 | Cloning, RS_E, D11, KLM016-018, "≥ 0.90 (Escalate)" | Cloning, RS_F, D08, KLM016-017, "0.78-0.79" |
| SYND-06 | Referral Churn Berulang, RS_G, D13+D14, KLM019-024, "0.82-0.86 (Escalate)" | Repeat Billing, KLM101-104, RS_G, D13, "0.85-0.90" |
| SYND-09 | Kolusi Multi-Faskes, RS_G+RS_C, D15+D19, KLM033-036, "≥ 0.89 (Escalate)" | Excessive Usage, KLM115-120, RS_J, D16, "0.78-0.83" |

Pada data aktual, KLM016 dan KLM017 (SYND-05 versi dataset) berlabel `high` dengan status `review`, bukan `fraud`/`escalate`, dan skornya 0,78 serta 0,79. Artinya satu namespace ID dipakai untuk dua ground truth berbeda. Siapa pun yang mereplikasi berdasarkan ID akan mengambil skenario yang keliru.

### I-04 (M-07, MAYOR) - Komposisi dataset berbeda antara arsip dan data aktual

`11-archive-proposal.md:321`: "Komposisi dataset terdiri atas 264 klaim normal (88%) dan 36 klaim fraud sindikat (12%) dengan rasio imbalance 1 : 7.33, merefleksikan kondisi lapangan yang realistis." Data aktual: 240 low + 24 medium/high, sehingga 264 baris non-fraud, di mana 24 adalah anomali yang masih perlu telaah, bukan normal. `03-dataset-registry.md:30` melarang hal ini eksplisit: "Jangan menyamakan seluruh 264 klaim non-fraud dengan klaim normal, karena kategori medium dan high masih memerlukan telaah." `01-proposal.md:37` sudah menyusunnya dengan benar, jadi ini regresi arsip yang belum dicatat di changelog. Frasa "merefleksikan kondisi lapangan yang realistis" juga bertentangan dengan `03-dataset-registry.md:100` ("Distribusi 12% label fraud adalah distribusi skenario sintetis, bukan estimasi prevalensi aktual") dan `10-simulation-dataset.md:179-181` ("12% fraud (oversampled by design) ... Hanya untuk simulasi dan validasi model").

### I-05 (M-08, MAYOR) - Ambang kanal fitur berbeda

`11-archive-proposal.md:210` memakai `theta_feat >= 0.50` untuk kanal kemiripan fitur (menghasilkan 15.202 edges). `09-draft-hub.md:15` dan `10-simulation-dataset.md:12` memakai "cosine similarity ... dengan ambang 0.85"; `10-simulation-dataset.md:166` menulis "Fitur (cosine θ=0.85)". Dua nilai untuk parameter yang sama, tanpa versioning.

### I-06 (M-12, MAYOR) - "109 baris LOS kosong" salah pada tingkat representasi

`00-dashboard.md:36` menulis "| Kolom LOS hari kosong | 109 baris |" dan `03-dataset-registry.md:78` menulis "109 baris memiliki kolom LOS hari kosong". Pada `claims_v2_live.csv` tidak ada satu pun sel LOS yang benar-benar kosong; 109 baris berisi literal string `"0"` (81 auto_clear, 14 review, 14 escalate). Jumlah dan sebarannya cocok, sehingga ini beda representasi nol versus kosong, bukan beda hitung. Selama nol diperlakukan sebagai durasi rawat nol, pemeriksaan kualitas data produksi keliru, dan `01-proposal.md:39` ("pemeriksaan nilai kosong") akan lolos tanpa menandai apa pun.

### I-07 (N-01, MINOR) - Klaim "anti-overclaim" di arsip bertentangan dengan isi arsip sendiri

`11-archive-proposal.md:15` menyatakan "Kami menolak klaim akurasi mutlak 100% dan tidak menyajikan angka penghematan anggaran yang spekulatif", lalu di paragraf yang sama menyebut "estimasi penyelamatan overcharge tarif INA-CBG sebesar Rp 507,37 Juta". Kalimat kebijakan dan isi saling membatalkan dalam satu paragraf.

### I-08 (N-01, MINOR) - "Tervalidasi klinis" bertentangan dengan status audit label

`11-archive-proposal.md:30` menyebut "portofolio 300 berkas klaim tervalidasi klinis" dan `:321` "300 berkas klaim tervalidasi klinis dengan 31 fitur". `08-training-protocol.md:8` mencatat "Field Risiko dan Status tersedia, tetapi perlu audit asal label", dan `:20` mencatat "deskripsi database masih menyebut versi 100 baris dan ground truth KLM001 sampai KLM024". `02-architecture.md:109` (D-01 "Tetapkan definisi final label fraud dan anomali") masih status Terbuka.

### I-09 (M-09, MAYOR) - "31 fitur" versus 27 kolom aktual

`11-archive-proposal.md:321` menyebut "31 fitur standar INA-CBG/FHIR R4". `claims_v2_live.csv` memiliki 29 kolom, dua di antaranya metadata internal (`_notion_page_id`, `_last_edited`), sehingga 27 kolom data. Angka fitur yang dipakai untuk mendeskripsikan skema model tidak cocok dengan artefak.

### I-10 (M-10, MAYOR) - Peringkat modus dan nominal arsip tidak cocok dengan data

`11-archive-proposal.md:348` menyebut tiga modus terbesar sebagai Phantom Billing Rp134,25 Juta, Upcoding Rp127,68 Juta, dan Repeat Billing Rp61,60 Juta. Data aktual (36 baris fraud, kolom `Modus` dan `Biaya Rp`):

| Modus | Jumlah | Nominal | Peringkat data | Peringkat arsip |
|---|---|---|---|---|
| upcoding | 3 | Rp156.900.000 | 1 | 2 (Rp127,68 Juta) |
| phantom_billing | 3 | Rp134.250.000 | 2 | 1 (Rp134,25 Juta) |
| iur_biaya | 4 | Rp63.880.000 | 3 | tidak disebut |
| repeat_billing | 4 | Rp61.600.000 | 4 | 3 (Rp61,60 Juta) |
| unbundling | 6 | Rp52.800.000 | 5 | tidak disebut |
| biaya_markup | 1 | Rp27.500.000 | 6 | tidak disebut |
| drug_diversion | 3 | Rp26.030.000 | 7 | tidak disebut |
| readmission_berulang | 6 | Rp25.290.000 | 8 | tidak disebut |
| excessive_usage | 6 | Rp12.900.000 | 9 | tidak disebut |

Peringkat modus pada arsip tidak cocok dengan data, dan nominal upcoding Rp127,68 Juta tidak ada di data. Ini bukti Tabel 8.2 arsip tidak diturunkan dari database yang dirujuk.

### I-11 (M-11, MAYOR) - "Sembilan sindikat menguasai 36 klaim senilai Rp542,56 Juta" tidak cocok dengan data

Data aktual: 8 ID sindikat (SYND-01, 02, 03, 04, 06, 07, 08, 09) pada 34 baris dengan total Rp524.750.000. Dua baris fraud tanpa sindikat: KLM121 (biaya_markup, Rp27.500.000, P29, RS_G) dan KLM122 (drug_diversion, Rp8.900.000, P30, RS_H), total Rp36.400.000. SYND-05 hanya pada KLM016 dan KLM017 yang berlabel `high`. Pernyataan arsip salah pada jumlah ID, jumlah klaim, dan nominal.

### I-12 (M-13, MAYOR) - Deskripsi dataset 100 klaim belum diverifikasi dan ada duplikasi tanpa cap

`08-training-protocol.md:8` dan `:20` mencatat bahwa deskripsi database masih menyebut 100 baris dan ground truth KLM001-KLM024. `09-draft-hub.md:219` menandai dirinya sebagai duplikat: "Isi yang diambil melalui Notion tampak sama dengan dokumentasi dataset 100 klaim. Jangan gunakan halaman ini sebagai versi data kedua sebelum pemilik proyek mengonfirmasi perbedaan skema atau versi." Namun `10-simulation-dataset.md` tidak memakai cap "duplikat" yang sama, sehingga korpus tetap menyajikan dua salinan dataset 100-klaim di dua dokumen yang berbeda tanpa penanda pada salah satunya. Bandingkan `14-index.md:260` yang memuat heading "ARSIP SUMBER DUPLIKAT".

### I-13 (N-03, MINOR) - SHAP dan usability hilang tanpa jejak di Rev 1.0

`01-proposal.md:91` menyebut SHAP satu kali di placeholder daftar pustaka, dan tidak menyebut SUS di mana pun. Substansi explainability dan usability testing yang ada di arsip (`11-archive-proposal.md:220`, `:350`) hilang tanpa catatan, kecuali satu kalimat umum di `01-proposal.md:61` ("Alasan otomatis harus bersumber dari data terstruktur atau kutipan yang dapat diverifikasi").

### I-14 (N-02, MINOR) - `14-index.md` meneruskan arsip tanpa kualifikasi per-baris

`14-index.md` memuat banner editor di `:479`, `:908`, `:1101`, tetapi isi KPI `:801-811` dan `:813-825` tetap membaca "93.00% (Tervalidasi)", "0.9142 (+28.6% vs XGBoost)", dan "Rp 507.370.000 (Penyelamatan Riil)". Pembaca yang mencari indeks menemukan klaim terlarang lebih dulu sebelum banner.

### I-15 (N-04, MINOR) - Tabel proporsi arsip benar, tetapi headline utama tidak

`11-archive-proposal.md:344-346` benar secara aritmetika: 240/300 = 80,00%, 24/300 = 8,00%, 36/300 = 12,00%, Rp279.950.000/3.526.650.000 = 7,94%, Rp561.150.000/3.526.650.000 = 15,91%. Yang bermasalah hanya `:348` yang menggabungkan "60 klaim anomali" (24 review + 36 escalate) dengan "Rp 841,10 Juta" (benar: 279.950.000 + 561.150.000) lalu menyodorkan overcharge 507.370.000 = "60,32% dari nominal klaim anomali" tanpa sumber tarif. Dua headline sekaligus, satu tanpa sumber.

---

## 6. Revisi 1.0 versus Arsip: Apa yang Hilang, Apa yang Memburuk

Aturan `00-dashboard.md:84` berbunyi "Revisi tidak menghapus konten sumber yang masih diperlukan sebagai rekam jejak" dan `:85` "Perubahan substansial dicatat pada changelog". `00-dashboard.md:88` mencatat changelog Rev 1.0 hanya berisi "Membuat struktur dokumen terkendali, merapikan proposal dan metode, merekonsiliasi ringkasan dataset, serta membakukan tata kelola bukti". Karena itu, konten yang hilang di bawah ini **tidak tercatat sebagai keputusan revisi**: hilang tanpa jejak, bukan dihapus dengan sengaja.

### 6.1 Yang membaik (tidak boleh diregresi)

| Aspek | Arsip | Rev 1.0 | Penilaian |
|---|---|---|---|
| Kualifikasi klaim | `11-archive-proposal.md:326-336` "93.00% (Tervalidasi)" | `01-proposal.md:70` "belum dinyatakan sebagai hasil tervalidasi dalam edisi ini" | Masuk baik. |
| Status dataset | "300 berkas klaim tervalidasi klinis" (`:30`, `:321`) | "Dataset tersebut merupakan data simulasi dan tidak mewakili prevalensi atau kerugian aktual JKN" (`:9`) | Masuk baik. |
| Kata terlarang | "Penyelamatan Riil", "membuktikan performa superior" (`:30`, `:347`) | "hasil sementara", "perlu rujukan primer" (`:9`, `:14`) | Masuk baik. |
| Rekonsiliasi nominal | Tabel 8.2 (`:343-348`) | `01-proposal.md:66-69`, cocok 100% dengan CSV | Masuk baik. |
| Distribusi label | "264 klaim normal" (`:321`) | "240 low, 10 medium, 14 high, dan 36 fraud ... tidak seluruh klaim non-fraud dapat disebut normal" (`:37`) | Masuk baik. |
| Anti-leakage | Disebut sekilas di `:255-259` | Dirinci di `:46-47` plus `:39` (blokir kolom turunan) | Masuk baik. |
| Syarat klaim operasional | Tidak ada | `:71` "Sebelum publikasi, setiap hasil wajib dihubungkan dengan eksperimen tertentu, skrip perhitungan, prediksi, ground truth, dan definisi operasional metrik" | Masuk baik. |

### 6.2 Yang hilang (jejak konten yang dihapus tanpa rekam)

| Hilang | Dulu ada di | Dampak |
|---|---|---|
| **Blok hipotesis pembuktian** | `11-archive-proposal.md:292` (Precision ≥ 90%, FPR ≤ 15%, memangkas waktu review 30-50%) | Naskah sekarang tidak punya kriteria falsifikasi. Proyek tidak dapat gagal secara terdefinisi. Ini kelemahan akademik terbesar yang timbul dari revisi. (M-02) |
| **Analisis akar masalah (5-Why dan Fishbone 4 dimensi)** | `11-archive-proposal.md:151-167` | Analisis sebab-akibat hilang; masalah tampak sebagai kebutuhan, bukan sebagai kondisi yang harus dijelaskan. |
| **Matriks 12 risiko** | `11-archive-proposal.md:370-389` | Register risiko lenyap tanpa pengganti. Tidak ada risiko di Rev 1.0. |
| **Roadmap Stage-Gate 7 tahap / 12 bulan** | `11-archive-proposal.md:390-404` | `01-proposal.md:75-82` memiliki 6 tahap tanpa gerbang (gate) yang eksplisit dan tanpa kriteria AUPRC/SUS/override numerik. Justru gerbang numerik inilah yang paling berguna untuk turnaround 1 November, karena memisahkan yang boleh dipertahankan dari yang belum. |
| **Simulasi OASIS (20 pasien, 12 dokter, 6 RS)** | `11-archive-proposal.md:306-310` | Skenario perilaku agen hilang total. |
| **Kontrol akses berbasis peran, Active Learning, DPO** | `11-archive-proposal.md` (3, 2, dan beberapa penyebutan) | `01-proposal.md:63` menyebut "kontrol akses berbasis peran" secara umum, tanpa rancangan. Active Learning dan DPO tidak disebut. |
| **Framing INA-CBG dan Cost-to-Impact** | `11-archive-proposal.md` (19 dan 6 penyebutan) | `01-proposal.md:74` justru menyebut "definisi tarif acuan" sebagai syarat, jadi kerangka tarif hilang padahal ini bahan yang dibutuhkan D-04. |
| **Spesifikasi MHGSL: PathSim, ambang θ, fusion, bobot atensi, jumlah edge** | `11-archive-proposal.md:207-224` | `01-proposal.md:44` hanya menulis "Model graf heterogen ... dengan definisi node, edge, fitur, dan metapath yang didokumentasikan". Kebaruan teknis proyek hilang, dan yang tersisa di arsip justru angka yang tidak terverifikasi. (M-03) |
| **Focal Loss (alpha 0,75, gamma 2,0)** | `11-archive-proposal.md:224` | Hilang. |
| **Branding "MHGSL" itu sendiri** | 28 penyebutan di arsip | 0 penyebutan di Rev 1.0. Pembeda utama proyek terhadap baseline tabular hilang, padahal `06-research-notes.md:30` masih menanyakan "Apakah model graf memberikan peningkatan yang bermakna dibandingkan XGBoost dengan split, target, dan fitur yang sama?" |
| **Seluruh angka konteks nasional** | `11-archive-proposal.md:22`, `:128`, `:162`, `:372`; `12-archive-architecture.md:5` | 270 juta jiwa, 2 juta klaim/hari, 1.000 verifikator, rasio 2.000 klaim/verifikator/hari, 50-70 berkas/hari, Rp150+ Triliun. Semuanya hilang tanpa satu pun catatan kualifikasi, padahal tidak semuanya salah: sebagian bisa dipertahankan dengan rujukan primer. (K-05) |
| **Seluruh daftar pustaka** | `11-archive-proposal.md:413-430` (18 entri) | Rev 1.0 hanya punya placeholder. Kapasitas sitasi justru berkurang. (M-01) |
| **Perbandingan dengan pendekatan lain** | `11-archive-proposal.md:177-186` | Tabel pembanding hilang, termasuk kolom yang memuat "89.4% akurasi pada 40% kamuflase" tanpa jejak. |
| **Pasal anti-overclaim eksplisit** | `11-archive-proposal.md:15` | Seluruh prinsipnya hilang karena tidak ada lagi klaim yang perlu dilindungi. Ini konsekuensi logis, bukan regresi, tetapi mengurangi jejak keputusan. |

### 6.3 Apa yang memburuk

1. **Kehilangan hipotesis falsifiable** (M-02). Tanpa ambang, evaluasi tidak punya arah. `01-proposal.md:49` menuntut "Hasil perlu dilaporkan untuk setiap fold beserta rata-rata, variasi, dan interval ketidakpastian jika relevan" tanpa ada target yang membuat angka itu bermakna.
2. **Kehilangan kebaruan** (M-03). Tanpa bagian kebaruan dan tanpa spesifikasi MHGSL, tinjauan akan menyimpulkan naskah tidak berbeda dari purwarupa tabular biasa. `05-decision-scope.md:71` sudah menegaskan bahwa "Kompleksitas graph learning bukan tujuan tersendiri", jadi naskah perlu membalas pertanyaan itu secara eksplisit, bukan menghilang darinya.
3. **Kehilangan daftar pustaka** (M-01). Revisi yang memperketat klaim tanpa menambah rujukan membuat naskah lebih jujur tetapi lebih lemah secara akademik. Permintaan Healthkathon hampir pasti menuntut sitasi.
4. **Angka 3,2x dan 82,5 hilang tanpa jejak** (K-07). `00-dashboard.md:84-85` melarang penghapusan tanpa rekam. Angka ini justru yang paling berguna untuk turnaround, karena bisa dipertahankan sebagai target dengan label "belum diuji", asal dicatat statusnya.
5. **Ketiadaan status arsip** (K-02). Revisi tidak memindahkan `11-archive-proposal.md` ke status Diarsipkan yang jelas, dan `14-index.md` meneruskannya apa adanya. Risiko tertinggi dari seluruh korpus: angka terlarang tetap dapat dikutip juri sebagai temuan proyek.
6. **Definisi identitas data belum selesai** (M-05, M-06, M-13). Label sindikat, ambang 0,80, dan duplikasi 100-klaim masih hidup berdampingan tanpa keputusan yang tercatat.

---

## 7. Rekomendasi Terurut

Prioritas P0 = blokir submit 1 November 2026, P1 = wajib untuk versi naskah final, P2 = perbaikan kualitas.

### P0 - Selesaikan sebelum submit (blokir deliverable)

1. **K-02, K-03: bekukan arsip dan indeks.** Set status `11-archive-proposal.md` menjadi Diarsipkan dengan banner yang menunjuk `01-proposal.md` sebagai naskah terkendali, dan ubah label "(Tervalidasi)" pada `:326-330` menjadi "(draf, belum tervalidasi)". Pada `14-index.md`, ganti label status di `:801-811` dan `:813-825`, atau keluarkan tabel KPI dari indeks dan arahkan ke `00-dashboard.md:46-52`. Tanpa ini, juri bisa mengutip klaim terlarang sebagai temuan.
2. **K-01: hentikan penggunaan angka benchmark apa pun sampai D-03 ditutup.** Cabut klaim AUC 1,00, presisi 1,00, dan tp36/fp0/fn0 sebagai hasil model. Catatan kaki (footnote): angka tersebut hanya menunjukkan bahwa `Skor Fraud` memisahkan label secara sempurna, jadi hanya berguna sebagai sanity check data, bukan sebagai bukti kemampuan model. Isi `02-architecture.md:111` (D-03) dengan eksperimen nyata: GroupKFold berbasis pasien dan leave-one-facility-out, baseline XGBoost, ID eksperimen, berkas prediksi, dan skrip metrik.
3. **K-04: hapus atau ganti tiga klaim finansial di arsip** (`:347`, `:348`): "Penyelamatan Riil", "ratusan miliar hingga triliunan rupiah per tahun", dan "Rp8.456.167 per kasus". Jika overcharge harus tetap dibahas, gunakan tabel tarif acuan dan formula per klaim sesuai D-04 di `02-architecture.md:112`, dengan label eksplisit "simulasi, prevalensi oversampled".
4. **K-07: catat jejak penghapusan 3,2x dan 82,5** di changelog Rev 1.1 (`00-dashboard.md:85`), dan pertahankan keduanya sebagai target bertanda "belum diuji" pada rencana kerja. Usulan susunan: target throughput 2,0x dan target SUS ≥ 75, mengikuti ambang Tabel 8.1 arsip `:333` dan `:335`, dengan status "rencana, belum diukur".
5. **K-05: hapus angka konteks nasional tanpa rujukan primer** dari arsip (`:22`, `:128`, `:162`, `:372`) dan `12-archive-architecture.md:5`, atau ganti dengan rujukan resmi BPJS Kemenkes yang benar-benar ditemukan. Angka 1.000 verifikator sekarang bersumber dari repo proyek sendiri (`dataset_research_live.csv:25`), yang tidak dapat dipakai sebagai sumber primer.
6. **M-05, M-06, M-13: kunci definisi label sekali.** Tetapkan ambang eksplisit "≥ 0.80 adalah fraud" di satu dokumen yang diberi versi, sesuai `03-dataset-registry.md:46`, dan rekam keputusan 0,80 versus 0,81 untuk KLM115. Buat satu tabel namespace sindikat tunggal dan catat perbedaan arsip versus dataset (M-06) sebagai keputusan tertulis, bukan senyap. Cap `10-simulation-dataset.md` sebagai duplikat `09-draft-hub.md:219` dan hentikan pemakaian deskripsi 100-klaim di `:8` dan `:20` `08-training-protocol.md`.
7. **K-06 dan M-11, M-10, M-09: rekonsiliasi Tabel 8.1 dan 8.2 arsip dengan `claims_v2_live.csv`** atau tandai seluruh tabel sebagai "draf lama, tidak berlaku". Saat ini modus, nominal, hitungan sindikat, dan jumlah fitur semuanya salah.

### P1 - Wajib untuk versi naskah final

8. **M-01: isi daftar pustaka dan sitasi.** Proses empat kelompok sumber awal di `06-research-notes.md:58-64` menjadi daftar pustaka dengan penanda `[n]` yang muncul dekat klaim, minimal pada: definisi dan prevalensi fraud, metodologi split, evaluasi AUPRC pada kelas imbalance, SHAP, dan regulasi. Buang entri yang tidak pernah dikutip. Selaraskan `11-archive-proposal.md:429` dengan DOI terverifikasi `10.1016/j.heliyon.2024.e30045` (`dataset_research_live.csv:11`) atau keluarkan.
9. **M-02: kembalikan hipotesis falsifiable** di bawah §2 Rumusan Masalah, diturunkan menjadi ambang uji yang bisa gagal: AUPRC model graf > AUPRC XGBoost pada split dan seed yang sama, FPR ≤ 15% pada prevalensi simulasi 12%, dan AUPRC dilaporkan ulang pada prevalensi 3-7% sesuai `12-archive-architecture.md:50`. Setiap ambang harus punya status "hipotesis, belum diuji".
10. **M-03: tambahkan bagian kebaruan dan balas pertanyaan biaya graph learning** dari `06-research-notes.md:35`. Nyatakan apa yang berbeda dari baseline tabular dan dari literatur graph fraud yang dirujuk, dan sadari bahwa `05-decision-scope.md:71` menyatakan kompleksitas graph learning bukan tujuan tersendiri. Kembalikan spesifikasi MHGSL secara ringkas (node, edge, metapath, fusion) tanpa angka yang tidak terverifikasi.
11. **M-04, M-05, M-08, M-09, M-10, M-11, M-12: perbaiki konvensi angka dan ambang** (skala 0,35/0,60/0,80, operator ≥ pada 0,80, batas θ 0,85, 109 baris LOS sebagai nol bukan kosong, jumlah fitur 27, modus dan sindikat). Buat satu tabel "angka kanonik" yang dirujuk semua dokumen.
12. **Tambahkan bagian Tinjauan Pustaka** yang mengikuti protokol di `06-research-notes.md:46-57`, dan abstrak bahasa Inggris bila pedoman submit meminta.
13. **Pulihkan rencana kerja dengan gerbang terukur** seperti `:401-404` arsip, tetapi dengan status eksplisit "belum dijalankan" untuk tiap gerbang, sehingga daftar target tidak pernah dibaca sebagai capaian.

### P2 - Perbaikan kualitas

14. **N-01: hapus frasa "tervalidasi klinis"** dari `11-archive-proposal.md:30` dan `:321` sampai D-01 tertutup.
15. **N-02: kap per-baris arsip di `14-index.md`** dan pindahkan banner editor ke atas setiap blok yang memuat KPI.
16. **N-03: kembalikan struktur explainability dan usability** ke rencana kerja, dan isi `01-proposal.md:91` dengan rujukan SHAP yang sebenarnya.
17. **N-04: keluarkan angka turunan yang tidak dapat dihitung ulang** (jumlah edge, bobot atensi) dari arsip, atau lampirkan artefak hitungnya.
18. **N-05: verifikasi atau keluarkan entri Heliyon e26115**, dan catat hasilnya di changelog sebagai temuan sumber.

---

## Lampiran A - Ringkasan Angka Audit

| Angka | Status akhir | Corpus |
|---|---|---|
| Accuracy 93,0% | AMAN di Rev 1.0 dan dasbor; TIDAK DIKUALIFIKASI di arsip dan indeks | 4 dokumen |
| Precision 94,12% | AMAN di Rev 1.0 dan dasbor; TIDAK DIKUALIFIKASI di arsip dan indeks | 4 dokumen |
| ROC-AUC 0,9825 | AMAN di Rev 1.0 dan dasbor; TIDAK DIKUALIFIKASI di arsip dan indeks | 4 dokumen |
| AUPRC 0,9142 | AMAN di Rev 1.0, dasbor, matriks bukti, catatan riset; TIDAK DIKUALIFIKASI di arsip dan indeks | 6 dokumen |
| Ketahanan masking 89,4% | AMAN di Rev 1.0 dan dasbor; TIDAK DIKUALIFIKASI di arsip dan indeks | 4 dokumen |
| FPR 10,6% | AMAN di Rev 1.0 dan dasbor; TIDAK DIKUALIFIKASI di arsip dan indeks | 4 dokumen |
| Waktu telaah 45% | AMAN di Rev 1.0 dan dasbor; TIDAK DIKUALIFIKASI di arsip dan indeks | 4 dokumen |
| Throughput 3,2x | Hanya di dasbor (larangan) dan arsip (TIDAK DIKUALIFIKASI); hilang dari Rev 1.0 tanpa jejak | 2 dokumen |
| SUS 82,5 | Hanya di dasbor (larangan) dan arsip (TIDAK DIKUALIFIKASI); hilang dari Rev 1.0 tanpa jejak | 2 dokumen |
| Overcharge Rp507.370.000 | AMAN di Rev 1.0, dasbor, matriks bukti, catatan riset; TIDAK DIKUALIFIKASI dan KONFLIK di arsip dan indeks | 6 dokumen |
| Cost-to-Impact 1:15 | TIDAK DIKUALIFIKASI di arsip dan indeks | 2 dokumen |
| Override 12,4% | TIDAK DIKUALIFIKASI di arsip dan indeks | 2 dokumen |
| Rp25 miliar (2024, 3 RS swasta) | TIDAK DIKUALIFIKASI di arsip riset | 1 dokumen |
| 175.774 klaim FKRTL | TIDAK DIKUALIFIKASI di arsip arsitektur | 1 dokumen |
| 1.000 verifikator, 2 juta klaim/hari, 270 juta jiwa | TIDAK DIKUALIFIKASI di arsip dan arsip arsitektur | 2 dokumen |

Total kemunculan yang diperiksa: 165 baris pada 9 dokumen. Tidak ada angka lain di luar daftar ini yang lolos tanpa kualifikasi.

## Lampiran B - Metode Verifikasi

- Audit angka dilakukan dengan pencocokan pola pada seluruh `analysis/corpus/*.md` (15 berkas) terhadap 11 angka terlarang plus 15 angka turunan, dengan klasifikasi AMAN/TIDAK DIKUALIFIKASI/KONFLIK berdasarkan konteks kalimat, bukan pada keberadaan string saja.
- Angka dataset direkomputasi dari `claims_v2_live.csv` dengan Python stdlib (`csv`, `collections`, `statistics`, `re`). Perintah: `python -X utf8 -c "<skrip>"` di direktori corpus.
- Pemeriksaan sitasi dilakukan dengan regex penanda `[n]`, `(Author, year)`, dan `et al.` pada badan teks Rev 1.0 (baris 1-84) dan arsip (baris 1-411), dibandingkan dengan blok daftar pustaka.
- Verifikasi eksternal untuk `11-archive-proposal.md:429` dicoba dua kali lewat MCP SearXNG dan gagal karena engine brave dan google cse berstatus suspended serta duckduckgo memberi CAPTCHA. Hasil dicatat sebagai "tidak terverifikasi", bukan sebagai klaim fabrikasi.
- Notion tidak diakses. Seluruh bukti berasal dari salinan lokal.

## Lampiran C - Daftar Temuan per ID

| ID | Severity | Ringkasan | Lokasi utama |
|---|---|---|---|
| K-01 | KRITIS | Angka "benchmark" arsip terbukti berasal dari kolom `Skor Fraud` yang menjadi label (tp36/fp0/fn0, AUC 1,00, mean status 0,086/0,591/0,869). Evaluasi sirkular. | `11-archive-proposal.md:15`, `:30`, `:326-336`, `:338`; `claims_v2_live.csv` |
| K-02 | KRITIS | Arsip dan indeks tetap hidup tanpa status, memuat label "(Tervalidasi)" dan "(Penyelamatan Riil)" yang dilarang `00-dashboard.md:46-52`. | `11-archive-proposal.md:326-336`, `:347`; `14-index.md:801-825` |
| K-03 | KRITIS | `14-index.md` meneruskan klaim terlarang tanpa kualifikasi per-baris; banner editor jauh dari isi KPI. | `14-index.md:479`, `:801-811`, `:813-825` |
| K-04 | KRITIS | Rp507.370.000 adalah haircut proporsional (40,16% review, 70,38% escalate), bukan kalkulasi tarif; "Penyelamatan Riil" dan ekstrapolasi nasional melanggar `05-decision-scope.md:64`. | `11-archive-proposal.md:347`, `:348`; `14-index.md:822-823` |
| K-05 | KRITIS | Angka konteks nasional (1.000 verifikator, 2 juta klaim/hari, 270 juta jiwa, 150+ Triliun) bersumber dari repo proyek sendiri, bukan sumber primer. | `11-archive-proposal.md:22`, `:128`, `:162`, `:372`; `12-archive-architecture.md:5`; `dataset_research_live.csv:25` |
| K-06 | KRITIS | Kata "Tervalidasi", "membuktikan performa superior", "membuktikan keunggulan mutlak" dipakai untuk angka yang belum direproduksi. | `11-archive-proposal.md:15`, `:30`, `:326-336`, `:338`; `04-evidence-matrix.md:90` |
| K-07 | KRITIS | Throughput 3,2x dan SUS 82,5 dihapus dari Rev 1.0 tanpa jejak, padahal `00-dashboard.md:84-85` mewajibkan rekam jejak dan changelog. | `00-dashboard.md:49`, `:84-85`; `11-archive-proposal.md:333`, `:335`, `:350` |
| M-01 | MAYOR | Nol penanda sitasi di Rev 1.0; 18 entri daftar pustaka arsip semuanya referensi yatim. | `01-proposal.md:85-91`; `11-archive-proposal.md:413-430`; `04-evidence-matrix.md:71`, `:85` |
| M-02 | MAYOR | Blok hipotesis falsifiable hilang saat revisi; proyek tidak dapat gagal secara terdefinisi. | `11-archive-proposal.md:292`; `01-proposal.md:15-21` |
| M-03 | MAYOR | Tidak ada bagian kebaruan; spesifikasi MHGSL dan branding "MHGSL" hilang seluruhnya. | `01-proposal.md:29`, `:44`; `06-research-notes.md:35`; `05-decision-scope.md:71` |
| M-04 | MAYOR | Skala ambang arsip 0,35/0,70 bertentangan dengan skala dataset 0,35/0,60/0,80; 5 baris `high` seharusnya eskalasi. | `11-archive-proposal.md:229-231`; `09-draft-hub.md:12`; `10-simulation-dataset.md:9` |
| M-05 | MAYOR | Batas operator 0,80 belum eksplisit ("lebih dari" versus "≥"); satu baris fraud bernilai tepat 0,80. | `09-draft-hub.md:12`; `10-simulation-dataset.md:9`; `03-dataset-registry.md:46`; KLM115 |
| M-06 | MAYOR | Namespace sindikat sama untuk dua ground truth berbeda antara arsip dan dataset (SYND-04, 05, 06, 09). | `11-archive-proposal.md:296-304`; `09-draft-hub.md:134-147` |
| M-07 | MAYOR | "264 klaim normal (88%) ... merefleksikan kondisi lapangan yang realistis" bertentangan dengan registry dan dengan data aktual. | `11-archive-proposal.md:321`; `03-dataset-registry.md:30`, `:100` |
| M-08 | MAYOR | Ambang kanal fitur berbeda: theta_feat 0,50 versus cosine 0,85. | `11-archive-proposal.md:210`; `09-draft-hub.md:15`; `10-simulation-dataset.md:12`, `:166` |
| M-09 | MAYOR | "31 fitur" versus 27 kolom data aktual. | `11-archive-proposal.md:321`; `claims_v2_live.csv` |
| M-10 | MAYOR | Peringkat modus dan nominal arsip tidak cocok dengan data; nominal upcoding Rp127,68 Juta tidak ada di data. | `11-archive-proposal.md:348`; `claims_v2_live.csv` |
| M-11 | MAYOR | "Sembilan sindikat, 36 klaim, Rp542,56 Juta" salah pada jumlah ID, jumlah klaim, dan nominal. | `11-archive-proposal.md:348`; `claims_v2_live.csv` (KLM121, KLM122 tanpa sindikat) |
| M-12 | MAYOR | "109 baris LOS kosong" sebenarnya 109 baris berisi literal "0"; pemeriksaan kualitas data produksi keliru. | `00-dashboard.md:36`; `03-dataset-registry.md:78`; `01-proposal.md:39` |
| M-13 | MAYOR | Deskripsi dataset masih menyebut 100 klaim dan ground truth KLM001-KLM024; `10-simulation-dataset.md` tidak memakai cap duplikat. | `08-training-protocol.md:8`, `:20`; `09-draft-hub.md:219`; `14-index.md:260` |
| N-01 | MINOR | Klaim "anti-overclaim" di arsip bertentangan dengan isi paragraf yang sama; "tervalidasi klinis" bertentangan dengan status audit label yang terbuka. | `11-archive-proposal.md:15`, `:30`, `:321`; `08-training-protocol.md:8`; `02-architecture.md:109` |
| N-02 | MINOR | Banner editor di indeks tidak menjangkau isi KPI. | `14-index.md:479`, `:908`, `:1101` |
| N-03 | MINOR | SHAP dan usability testing hilang dari Rev 1.0 tanpa jejak selain placeholder daftar pustaka. | `01-proposal.md:61`, `:91`; `11-archive-proposal.md:220`, `:350` |
| N-04 | MINOR | Angka turunan yang tidak dapat dihitung ulang (jumlah edge, bobot atensi) tetap di arsip. | `11-archive-proposal.md:209-211`, `:220` |
| N-05 | MINOR | Entri Heliyon e26115 tidak terverifikasi dan konflik dengan DOI register terverifikasi; kemungkinan salah kutipan. | `11-archive-proposal.md:429`; `dataset_research_live.csv:9`, `:11` |
