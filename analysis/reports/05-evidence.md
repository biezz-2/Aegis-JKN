# Audit Kualitas Bukti dan Sitasi - Aegis-JKN

Tanggal audit: 22 Oktober 2026
Auditor: research verifier (audit kemitraan bukti & sitasi)
Ruang lingkup: `analysis/corpus/04-evidence-matrix.md`, `analysis/corpus/dataset_research_live.csv` (33 baris), `analysis/corpus/06-research-notes.md`, `analysis/corpus/01-proposal.md`, `analysis/corpus/05-decision-scope.md`, `analysis/corpus/03-dataset-registry.md`
Metode verifikasi: MCP SearXNG (`searxng_web_search` → `web_url_read`). Semua akses web dilakukan 22 Oktober 2026. Sumber primer yang tidak dapat diakses ditandai **TIDAK TERVERIFIKASI**, bukan "salah".

---

## 1. Ringkasan Eksekutif

Register 33 barus memuat 22 URL unik; seluruh 22 diperiksa (20 disorot di §4, sisanya sebagai pembanding/substitusi). Hasil: **16 URL hidup apa adanya, 2 domain mati total, 1 tautan 404, 3 diblokir (403/JS) tetapi substansi terverifikasi lewat jalur pengganti**, sehingga **21 dari 22 klaim sumber memiliki bukti akses**, sementara **9 klaim memiliki ketidaksesuaian substansi** (judul/tahun/isi/atribusi) terhadap apa yang ditulis di register.

Temuan utama:

1. **Kesalahan hukum material pada UU PDP (register baris 4).** Deskripsi menyatakan "Sanksi pidana Pasal 65-66: 5-6 tahun penjara, denda hingga Rp5 miliar". Pasal 65 dan Pasal 66 adalah pasal **perilaku**, bukan pasal pidana. Pasal yang memuat sanksi pidana adalah **Pasal 67** (5 tahun/Rp5 miliar; 4 tahun/Rp4 miliar; 5 tahun/Rp5 miliar untuk pelanggaran Pasal 65) dan **Pasal 68** (penjara paling lama **6 tahun** dan/atau denda paling banyak **Rp6.000.000.000** - bukan Rp5 miliar). Catatan Riset pada baris yang sama juga salah ("Pasal 66 'pidana paling lama 6 tahun' & denda Rp5 M") dan **bertentangan dengan Deskripsi baris itu sendiri**. Ini adalah satu-satunya kesalahan yang dapat merugikan secara hukum di depan juri.
2. **Angka benchmark AUPRC tidak ada di sumber yang dikutip.** Full text paper MHGSL (Heliyon 10(9):e30045, 2024, PMC11061682) diperiksa penuh: string "AUPRC"/"precision-recall"/"Area Under the Precision-Recall" **tidak muncul sama sekali (0 kemunculan)**; metrik yang dipakai adalah ACC, AUC, F1 (Medical-A) serta F1 dan Precision (Medical-B). Angka "+20% AUPRC" dan "false negative −42%" **tidak ditemukan**; kemunculan "20%" pada paper hanyalah ukuran proporsi data latih (20%/40%/60%). Sumber tidak mendukung klaim.
3. **Dua sitasi berisiko fabrikasi tidak dapat dilacak.** "MHINAGSL (IEEE Access 2025, multiview heterogeneous, F1 0,92)" (baris 10) → 0 hasil di Crossref `query.title=MHINAGSL` dan 0 hasil di OpenAlex `title.search:MHINAGSL`. "Studi triase auditor berbasis SHAP+RAG (MDPI 2025)" (baris 1) → pencarian Crossref jurnal MDPI *Applied Sciences* 2025 tidak menghasilkan studi yang cocok (yang terdekat: TRAG - RAG untuk *emergency triage* 2026; XAI Ethereum 2025). Keduanya **TIDAK TERVERIFIKASI** dan harus dihapus atau diganti.
4. **Dua baris bergantung pada domain yang tidak ada.** `siap-lafki.or.id` (baris 21 & 29) dan `acch.kpk.go.id` (baris 22 & 28) gagal di-resolve DNS (gaierror) dan tidak dapat diakses. Baris 29 ("Estimasi fraud 3–7%") adalah dasar kuantifikasi ROI dan tetap berstatus "Perlu Verifikasi" dengan sumber yang tidak hidup. Artikel ACCH *rupanya* ada (Djasri, Rahma & Hasri 2016, *Integritas* 2(1):113–133, terverifikasi lewat republicasi mutupelayanankesehatan.net, Google Scholar, dan sitasi *IJHP* 10.51601/ijhp.v5i3.341), tetapi URL yang dicantumkan tidak hidup.
5. **Label "Terverifikasi" (18 baris) tidak mencerminkan hierarki A–D.** 6 di antaranya gagal atau hanya sebagian lolos verifikasi langsung: Zenodo 21717009 ternyata **PREreview atas sebuah preprint** (bukan artikel ilmiah); URL journalcenter pada baris 23 **404**; researchgate (baris 25) **403**; subdomain `web.bpjs-kesehatan.go.id` (baris 26) **403**; baris 18 dan 27 bersumber dari halaman pemasaran (level D) untuk klaim Kritis; baris 12 tidak mencatat status **sandbox-only** halaman SATUSEHAT, padahal 04 §4 E-02 mewajibkannya.
6. **Dua baris "Terverifikasi" hanya bersumber dari repositori sendiri** (baris 24 "±1.000 verifikator", baris 33 purwarupa) - pelanggaran langsung atas instruksi 04 §4 E-04 ("Hindari menjadikan repositori internal sebagai satu-satunya sumber") dan 04 §3 (level D tidak boleh menjadi satu-satunya dasar klaim berisiko tinggi).

Secara umum register **sangat jujur pada baris 2, 8, 11, 29** (status "Perlu Verifikasi", catatan mengakui angka belum ditemukan) - ini justru bukti kualitas proses. Yang bermasalah adalah baris yang berlabel "Terverifikasi" padahal isinya salah, mati, atau bertipe salah; di situlah risiko publikasi berada.

### Tabel severity

| Severity | Jumlah | Cakupan |
|---|---|---|
| **Kritis** | 4 | Salah rujukan pasal & denda UU PDP; angka AUPRC tidak didukung sumber paper; domain mati untuk baris 21/29 (termasuk prevalensi 3–7% sebagai basis ROI); label "Terverifikasi" sistemik tidak mencerminkan strength hierarchy A–D |
| **Tinggi** | 6 | Dua sitasi tidak dapat dilacak (MHINAGSL; SHAP+RAG MDPI 2025); baris 19 sumber tidak memuat modus yang diklaim; baris 18 & 27 klaim Kritis/Tinggi hanya bersumber level D; baris 24 bersumber tunggal repo sendiri; baris 26 klaim "SK fiktif kolusif" tidak didukung sumber |
| **Sedang** | 8 | Judul resmi Permenkes 16/2019 salah di 04 §5 dan 01-proposal; status baris 20 bertentangan dengan 04 E-03; atribusi angka Rp20 T; pencampuran skala 2026 dan 2022 pada baris 31 plus sumber tanpa URL; status sandbox SATUSEHAT tidak dicatat; baris 5 & 9 berbagi satu URL; 6 baris tanpa sumber; klaim 113,47 T & "BBC Indonesia" tanpa URL |
| **Rendah** | 6 | Skema register tidak memuat kolom strength/reviewer/kutipan sesuai 04 §7; penyebutan "DPO" untuk Pasal 53; "kompetisi tahunan ke-6" tidak sesuai hitungan edisi; AUPRC 0,91 (README) vs 0,9142 (proposal); "pendaftaran sudah ditutup" tidak bersumber dari artikel yang dikutip; 06-research-notes hanya 8 dari 12 klaim 04 |

**Total temuan: 24** (Kritis 4, Tinggi 6, Sedang 8, Rendah 6).

---

## 2. Audit Evidence Matrix (04-evidence-matrix.md, §4 Register Klaim Prioritas)

| Klaim (ID 04) | Sumber | Jenis | Status verifikasi | Relevansi | Kesenjangan |
|---|---|---|---|---|---|
| E-01 Kewajiban pelindungan data pribadi | UU 27/2022 via pasal.id | A (resmi) | Terverifikasi per pasal (4(2), 20, 46, 51, 53, 67, 68) | Kritis | 04 sudah benar meminta rujukan pasal, tetapi register baris 4 menyimpang: salah pasal (65–66 vs 67–68) dan salah nominal denda (Rp5 M vs Rp6 M). 04 belum pernah memicu perbaikan baris 4. |
| E-02 Rekam medis & interoperabilitas SATUSEHAT | satusehat.kemkes.go.id modul klaim BPJS; Permenkes 24/2022 | A | URL hidup; **halaman memuat banner "Modul ini sedang dalam tahap pengembangan (hanya tersedia di Environment Sandbox)"** yang tidak direkam di register | Kritis | Status sandbox/produksi, versi (dokumentasi v7.23), dan tanggal akses tidak ada di kolom Sumber Riset maupun Catatan Riset baris 12 - persis yang diminta 04 §4 E-02. |
| E-03 Volume klaim nasional per hari | Kontan (Dirut BPJS Ghufron Mukti, 17 Sep 2025) | C (media) | Register: "Terverifikasi"; 04: "Sebagian terverifikasi" | Kritis | Kontradiksi status. Sumber menyebut "**transaksi** klaim … lebih dari 2 juta transaksi per hari" (2025), register menulis "2.000.000 klaim layanan kesehatan **per hari kerja**" - qualifiers "per hari kerja" tidak ada di sumber. Sumber primer (rilis/laporan BPJS) belum dilacak. |
| E-04 Jumlah verifikator & rasio beban kerja | **Hanya** github.com/biezz-2/Aegis-JKN (README: 2.000.000 klaim vs 1.000 verifikator) | D (repo sendiri) | Sebagian Terverifikasi | Kritis | Pelanggaran langsung instruksi E-04. Tidak ada rilis resmi BPJS yang menyebut angka ini; belum ditemukan kandidat sumber independen. |
| E-05 Prevalensi fraud 3–7% | siap-lafki.or.id (domain mati, DNS gagal) | D/tidak hidup | Perlu Verifikasi | Tinggi | Sumber tidak hidup. Pembanding yang dipakai register (review Journal of Big Data, USD 300 miliar/tahun AS) adalah **ordinalitas kerugian, bukan laju prevalensi** - tidak mendukung 3–7%. Sumber primer JKN yang relevan belum dipakai, padahal tersedia: Djasri et al. 2016 (Integritas KPK 2(1):113–133) dan review *IJHP* 5(3) 2025 (10.51601/ijhp.v5i3.341). |
| E-06 Potensi kerugian nasional | Kompas 21 Sep 2024; LAFKI; ACCH KPK | C, sebagian mati | Sebagian Terverifikasi | Tinggi | Angka Rp20 T **bukan berasal dari BPJS**: '../../../ articulation according to BPJS (Irfan Humaidi) "membantah" dan menyebutnya potensi sektor kesehatan umum; asalnya Wake-up Wakil Ketua KPK **Alexander Marwata** (19 Sep 2024): "10 persen dari pengeluaran untuk kesehatan masyarakat, sekitar Rp 20 triliun secara nominal". Atribusi asal ini wajib direkam sesuai E-06 ("pisahkan angka yang diberitakan, perkiraan, dan temuan yang telah diaudit"). Sumber LAFKI mati. |
| E-07 Benchmark AUPRC 0,9142 | Artikel Heliyon MHGSL (PMC11061682) | B | Belum tereproduksi | Tinggi | Paper **tidak memuat AUPRC sama sekali** (0 kemunculan). Angka 0,9142 di proposal §8 tidak punya asal; README repo sendiri menyebut AUPRC 0,91 (selisih 0,0042). Perlu artefak eksperimen internal, bukan artikel eksternal (04 §8 butir 3). |
| E-08 AUPRC +20% & FN −42% vs XGBoost | cell.com Heliyon (403) → full text via EuropePMC | B | Perlu Verifikasi | Tinggi | **Angka tidak ada di paper.** "20%" yang muncul = proporsi data latih (20%/40%/60%). "42%"/"false negative" = 0 kemunculan. Sumber juga tidak membandingkan MHGSL dengan XGBoost pada tabel utama (XGBoost/LR/RF hanya pada §5.2.4 classifier hilir, Fig. 9, bukan tabel hasil). Catatan register sudah jujur, tetapi sumber tetap dipakai sebagai sandaran di presentasi. |
| E-09 20 menit → 3 menit per berkas | - (asumsi internal) | - | Perlu Verifikasi | Tinggi | Sumber tidak ada; register juga tidak mengaitkannya ke sumber apa pun (baris 2 tanpa Sumber Riset). Aman secara editorial, tetapi 04 §7 tetap meminta entri sumber. |
| E-10 Waktu telaah −45% | - | - | Belum dibuktikan | Rendah/Tinggi | Tidak ada di 04-matriks klaim dan 06-research-notes; sumber tidak ada. Harus tetap terpisah dari E-09. |
| E-11 Estimasi penyelamatan Rp507.370.000 | Angka nominal dataset v2 (03 §3.3) | A (internal) | Belum dapat direproduksi per klaim | Tinggi | 03 §3.3 menyatakan total nominal Rp3.526.650.000 "tidak dengan sendirinya membuktikan … nilai yang dapat diselamatkan"; tarif acuan & formula adjudikasi tidak ada. Tidak boleh disandingkan dengan data klaim nasional. |
| E-12 SHAP/XAI | AI Review 59(4) 2026, DOI 10.1007/s10462-026-11516-7 | B | Terverifikasi (metadata) | Kritis | Artikel XAI **terverifikasi** (judul, jurnal, tahun 2026 sah - terbit 17 Feb 2026, diindeks 4 Okt 2026). Namun catatan baris 1 menyebut satu referensi tambahan ("studi triase auditor berbasis SHAP+RAG, MDPI 2025") yang **tidak dapat dilacak** → fabrikasi berisiko. Selain itu, 01-proposal §Referensi masih menulis "TODO" untuk metadata XGBoost/GNN/SHAP. |

---

## 3. Statistik Register 33 Baris

Sumber: `analysis/corpus/dataset_research_live.csv` (33 baris, kolom Status Verifikasi, Relevansi, Sumber Riset, Deskripsi, Kategori, Pendekatan Deteksi/Teknis, Catatan Riset, Item).

### 3.1 Status Verifikasi × Relevansi

| Status Verifikasi | Kritis | Tinggi | Pendukung | Total |
|---|---|---|---|---|
| Terverifikasi | 10 | 6 | 2 | **18** |
| Sebagian Terverifikasi | 1 | 9 | 1 | **11** |
| Perlu Verifikasi | 0 | 3 | 1 | **4** |
| **Total** | **11** | **18** | **4** | **33** |

### 3.2 Kategori

| Kategori | Jumlah |
|---|---|
| Modus Fraud | 9 |
| Teknologi AI | 8 |
| Konteks & Statistik | 6 |
| Roadmap & Operasional | 4 |
| Metrik & Validasi | 2 |
| Sumber Data & Interoperabilitas | 2 |
| Regulasi & Kepatuhan | 1 |
| Ekonomi & ROI | 1 |
| **Total** | **33** |

### 3.3 Distribusi lain

| Metrik | Nilai |
|---|---|
| Baris tanpa `Sumber Riset` | 6 (baris 2, 6, 14, 15, 16, 17) |
| Baris dengan URL | 27 |
| URL unik | 22 |
| URL dipakai lebih dari sekali | 5 (zenodo 21717009 ×2; cell.com heliyon ×2; siap-lafki ×2; acch.kpk ×2; github repo sendiri ×2) |
| Baris Kritis | 11 (baris 1, 4, 7, 10, 13, 18, 20, 24, 25, 32, 33) |
| Baris "Terverifikasi" yang gagal/partial saat audit ini | 6 (baris 5, 12, 18, 23, 25, 26) |

### 3.4 Rekonsiliasi dengan 04 §2

Angka pada 04 §2 **cocok persis** dengan register: 33 entri; status 18/11/4; relevansi 11/18/4. Tidak ada penyimpangan aritmetika. Inkonsistensi 04 ↔ register ada pada **level status per klaim** (§4 baris E-03) dan **judul peraturan** (04 §5 butir 3).

---

## 4. Hasil Verifikasi URL

Semua diakses 22 Oktober 2026 lewat SearXNG `web_url_read`. Kolom "Verdict": **OK** (cocok), **PARTIAL** (sebagian isi tidak ditemukan / tidak sinkron), **MISMATCH** (isi atau atribusi berbeda dari yang ditulis register), **DEAD** (URL tidak hidup), **TIDAK TERVERIFIKASI** (gagal diakses tanpa jalur pengganti).

| # | URL (sesuai register) | Hidup? | Judul cocok? | Tahun cocok? | Verdict | Temuan |
|---|---|---|---|---|---|---|
| 1 | link.springer.com/article/10.1007/s10462-026-11516-7 | Tidak (JS) | Ya | Ya (2026 sah) | OK | Dibaca via Crossref: "Methodological challenges in explainable AI for fraud detection: a systematic literature review", *Artificial Intelligence Review* 59(4), terbit 17 Feb 2026, 63 ref, lisensi CC BY-NC-ND. **Tahun 2026 bukan placeholder.** |
| 2 | link.springer.com/article/10.1186/s40537-025-01295-3 | Tidak (JS) | Ya | Ya (2025) | OK | Crossref + Semantic Scholar (DBLP journals/jbd/CurtisPKF25) + full text journalofbigdata.springeropen.com. Abstract memuat "estimated **$300 billion** lost annually in the United States" → angka row 29 terkonfirmasi **tetapi sebagai kerugian absolut AS, bukan laju prevalensi**. |
| 3 | www.cell.com/heliyon/fulltext/S2405-8440(24)06076-6 | Tidak (403) | Ya | Ya (2024) | MISMATCH | Full text via EuropePMC (PMC11061682): judul, 3 kanal, GCN bersama, attention fusion, tabel 6/7 **terverifikasi**. Namun **AUPRC = 0 kemunculan**, "+20%" hanya proporsi data latih, "42%"/false-negative tidak ada. Dataset China, **bukan JKN**. |
| 4 | zenodo.org/records/21717009 | Ya | **MISMATCH tipe** | Ya (2026) | MISMATCH | API Zenodo: judul "**PREreview of** 'Improving Medicare Fraud Detection Accuracy…'". Bukan artikel ilmiah; peer review komunitas atas preprint (DOI preprint 10.64898/2026.03.18.26348763). Isi mendukung argumen AUPRC>akurasi (Major Issue #1 "Accuracy is the wrong headline metric") dan menyebut SMOTE. Turunkan ke level C/D untuk baris 5, dan pisahkan untuk baris 9. |
| 5 | ml-research.github.io/papers/fang2022dpctgan.pdf | Ya | Ya | Ya (2022) | OK | PDF sah: Fang, Dhami, Kersting, "DP-CTGAN: Differentially Private Medical Data Generation using CTGANs", AIME 2022. Level B. |
| 6 | www.allalliedhealthschools.com/blog/…phantom | Ya | Ya | - | MISMATCH (kelas sumber) | Blog marketing sekolah anatomi/koding medis AS. Isi taksonomi cocok, tetapi **level D** dipakai sebagai satu-satunya dasar klaim **Kritis** (Phantom Billing, baris 18). |
| 7 | www.phillipsandcohen.com/upcoding-unbundling-fragmentation/ | Ya | Ya | - | MISMATCH (kelas sumber) | Halaman marketing/whistleblower firm hukum AS. **Level D** untuk klaim Unbundling (Tinggi, baris 27). |
| 8 | keuangan.kontan.co.id/news/klaim-layanan-bpjs-kesehatan-tembus-2-juta-per-hari | Ya | Ya | Ya (2025) | PARTIAL | Teks artikel: "Pada 2014 tercatat sekitar 252.000 transaksi klaim per hari … kini **lebih dari 2 juta transaksi per hari**" (Dirut Ghufron Mukti, 17 Sep 2025). Register menulis "±2.000.000 klaim **per hari kerja**" → "per hari kerja" tidak ada di sumber. Tidak ada angka verifikator di artikel. |
| 9 | money.kompas.com/read/2024/09/21/131900126/klarifikasi… | Ya | Ya | Ya (2024) | MISMATCH (atribusi) | Teks: BPJS (Irfan Humaidi) **membantah** angka Rp20 T sebagai kerugian BPJS; asal angka = Wakil Ketua KPK **Alexander Marwata**, 19 Sep 2024: "10 persen dari pengeluaran untuk kesehatan masyarakat, sekitar Rp 20 triliun secara nominal". |
| 10 | sustain.id/2024/10/04/fraud-dalam-pelayanan-kesehatan… | Ya | Ya | Ya (2024) | MISMATCH | Taksonomi yang disajikan (tabel "Risiko/Insiden Fraud JKN") berisi upcoding, diagnosis tidak perlu, klaim berlebih, rujukan tidak perlu, kartu orang lain, suplier obat, gelembungan iuran - **tidak memuat drug diversion / over-dosing / penumpukan obat**. Klaim baris 19 tidak didukung sumber. (Catatan positif: artikel ini mengutip Permenkes 16/2019 dengan **judul resmi yang benar** - lihat temuan 11.) |
| 11 | acch.kpk.go.id/id/component/content/article?id=672:korupsi-… | **DEAD** (DNS: gaierror) | - | - | TIDAK TERVERIFIKASI (URL) / substansi terkonfirmasi | URL tidak resolve. Artikel_exists: Djasri H., Rahma P.A., Hasri E.T., "Korupsi dalam Pelayanan Kesehatan di Era Jaminan Kesehatan Nasional…", *Integritas: Jurnal Antikorupsi* 2(1):113–133, 2016 - terkonfirmasi via mutupelayanankesehatan.net (republikasi + ringkasan), Google Scholar, dan sitasi *IJHP* 5(3) 2025. Angka dalam artikel: 175.774 klaim RS/FKRTL berpotensi fraud **nilai Rp440 miliar** sampai pertengahan 2015 - **bukan** prevalensi 3–7%. |
| 12 | siap-lafki.or.id/bpjs-kesehatan-dan-tantangan-fraud-20-triliun… | **DEAD** (DNS: gaierror) | - | - | TIDAK TERVERIFIKASI | Domain `siap-lafki.or.id` tidak resolve (gaierror, juga tanpa www).THON.Ada arsip (web.archive.org 404, Wayback 429). Dipakai baris 21 (under-reporting upah) dan baris 29 (prevalensi 3–7%). |
| 13 | journalcenter.org/index.php/inovasi/article/download/4767/3750/**18212** | **DEAD (404)** | - | - | MISMATCH (tautan) | URL register salah. URL benar `/download/4767/3750` hidup: "Fraud dalam Layanan BPJS Kesehatan : Kajian Etis dan Hukum Berdasarkan UU 17/2023", *Inovasi* Vol 3 No 3 Sept 2024, Hal 81–92, DOI 10.55606/inovasi.v4i1.4767 (DOI menyebut v4i1 - inkonsistensi internalvolume). Metode: **penelitian hukum normatif**, bukan empiris; memuat "cloning … penjiplakan klaim dari pasien lain" sebagai salah satu bentuk, tetapi **tanpa data kasus JKN**. |
| 14 | researchgate.net/publication/369679967_ANALISIS_KEJADIAN_UPCODING… | Tidak (403) | Ya | Ya (2023) | PARTIAL | Kanonik: Bina Generasi Jurnal Kesehatan 14(2) 2023, DOI 10.35907/bgjk.v14i2.220, Sariunita & Syakurah, "…di wilayah kerja BPJS Kesehatan Cabang Depok". **Studi kualitatif deskriptif** (1–30 Jul 2021) → **tidak memuat angka prevalensi**. Risiko: URL ResearchGate = mirror yang diblokir, seharusnya DOI/publisher. |
| 15 | web.bpjs-kesehatan.go.id/uploads/information/4bd28c6…pdf | Tidak (403, bot detection) | Ya | Ya (berlaku) | PARTIAL | PDF **"Panduan Layanan JKN-KIS"** hidup via `www.bpjs-kesehatan.go.id` (subdomain `web.` memblokir bot). Menguat Kewajiban Peserta no. 6: "Menjaga identitas peserta JKN-KIS agar tidak rusak, hilang atau dimanfaatkan oleh orang yang tidak berhak". **Tidak** memuat "surat keterangan sakit fiktif kolusif", tidak memuat volume klaim/jumlah verifikator, tidak memuat iuran/kode klaim spesifik. |
| 16 | www.liputan6.com/health/read/8270049/healthkathon-2026… | Ya | Ya | Ya (14 Agu 2026) | PARTIAL | Konfirmasi: kriteria kompetisi "efisiensi risiko pada peserta, fasilitas kesehatan, dan pemberi kerja"; pendaftaran 14 Agt–14 Sep 2026; pendekatan problem-first (Setiaji); Aly: Alex Budiyanto. **Tidak** memuat "kompetisi tahunan ke-6" maupun "pendaftaran sudah ditutup". Tema "Detect Smarter, Protect JKN" terkonfirmasi lewat kanal resmi BPJS (video "OFFICIAL LAUNCHING HEALTHKATHON 2026", 20 Agu 2026). |
| 17 | www.stabilitas.id/rasio-klaim-tembus-10872-bpjs-kesehatan-bayar-rumah-sakit-rp500-miliar-sehari/ | Ya | Ya | Ya (15 Jun 2026) | PARTIAL | Teks: rasio klaim (loss ratio) **108,72%**; "transaksi kesehatan itu sehari **2 juta transaksi** … pembayaran **Rp500 miliar** sehari"; Dirut Prihati Pujowaskito, rapat kerja Komisi IX DPR RI, 12 Jun 2026; defisit ~Rp2 T/bulan; proyeksi suntikan dana Rp20 T. **Tidak memuat "113,47 T/tahun"** - angka itu adalah **klaim 2022** (BPJS membayar Rp113,47 T; ANTARA/IDN Times, Jul 2023). |
| 18 | satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/ | Ya | Ya | - | PARTIAL | Halaman hidup (dokumentasi platform v7.23). Memuat banner: "**Modul ini sedang dalam tahap pengembangan (hanya tersedia di Environment Sandbox)**" → status ini **tidak direkam** di register, padahal 04 E-02 mewajibkannya. |
| 19 | peraturan.bpk.go.id/Details/245544/permenkes-no-24-tahun-2022 | Ya | Ya | Ya (2022) | OK | Resmi: Permenkes 24/2022 tentang Rekam Medis; berlaku 31 Agu 2022; mencabut Permenkes 269/2008. Level A. |
| 20 | peraturan.bpk.go.id/Details/129762/permenkes-no-16-tahun-2019 | Ya | **MISMATCH judul** | Ya (2019) | MISMATCH | Judul resmi: "…tentang **Pencegahan dan Penanganan Kecurangan (Fraud) Sera Pengenaan Sanksi Administrasi Terhadap Kecurangan (Fraud) Dalam Pelaksanaan Program Jaman Kesehatan**". Tetapkan 18 Jul 2019, berlaku 31 Jul 2019, mencabut Permenkes 36/2015, status Berlaku. **Berbeda** dari judul yang dicetak di 04 §5 butir 3 dan di 01-proposal ("…serta Pengendalian Gratifikasi"). |
| 21 | pasal.id/peraturan/uu/uu-no-27-tahun-2022 (+ pasal 4, 20, 46, 51, 53, 67, 68) | Ya | Ya | Ya (2022) | MISMATCH (klaim register) | Pasal 46(1): notifikasi **paling lambat 3×24 jam** ke subjek data **dan lembaga** (baris 4 benar). Pasal 53: penunjukan **pejabat atau petugas yang melaksanakan fungsi Pelindungan Data Pribadi** (bukan istilah "DPO" seperti ditulis register). Pasal 67: 5 thn/Rp5 M; 4 thn/Rp4 M; 5 thn/Rp5 M (pelanggaran Pasal 65). Pasal 68: **paling lama 6 thn dan/atau denda paling banyak Rp6.000.000.000** (pelanggaran Pasal 66). **Baris 4 salah pada pasal dan nominal denda.** |
| 22 | ai.google.dev/gemini-api/docs/pricing | Ya | Ya | Ya (halaman berjalan) | PARTIAL | Gemini 1.5 **sudah tidak terdaftar** (membenarkan catatan register). Harga terkini: Flash kelas 3.8/3.6 input **$0,75/1M** (naik $1,50 sejak 1 Jan 2027), Batch $0,375, Flash-Lite $0,30, Pro 3.1 Preview input $2,00 (≤200k) / $4,00 (>200k) dengan output $12,00/$18,00. Rentang "$0,10–1,50" di Deskripsi baris 11 **tidak sesuai** harga terkini. |

### 4.1 Substitusi untuk sumber yang diblokir (terverifikasi independen)

| Klaim register | Jalur pengganti | Hasil |
|---|---|---|
| Baris 10 (arsitektur MHGSL) | EuropePMC REST fullTextXML PMC11061682 | 3 kanal (topologi/fitur/semantik), meta-path, common path sampling, GCN spesifik + GCN bersama + attention fusion, Tabel 6 (Medical-A: MHGSL ACC 0,8977/AUC 0,8604/F1 0,8163 pada split 3:1:1) dan Tabel 7 (Medical-B: F1 0,8829 @20% vs StGNN 0,8519) - **struktur terverifikasi; AUPRC tidak ada** |
| Baris 10 (review Journal of Big Data sebagai pemverifikasi outperform) | journalofbigdata.springeropen.com (full text) | Review memang membahas Hong et al.: "MHGSL [23] achieves 0.895 F1" vs StGNN 0,875, MHAMFD 0,881, MBGNN 0,891, dan menyebut outperforms in F1/AUC/accuracy → **Catatan baris 10 tentang performanya benar**. Namun review juga menyebut dataset "Medical-1/Medical-2" (nama berbeda dari Medical-A/B di paper) dan dataset berasal dari "an unnamed insurance bureau" → **bukan JKN**. |
| Baris 4 (UU PDP) | pasal.id per pasal | Lihat baris 21 tabel. |
| Baris 22 & 28 (modus JKN dari kajian ACCH) | mutupelayanankesehatan.net + Google Scholar + iJHP review | Artikel 2016 ada; memuat bentuk fraud provider: upcoding, inflated bills, service unbundling, no medical value, standard of care; angka 175.774 klaim / Rp440 M. |
| Baris 21 & 29 | - | Tidak ada jalur pengganti; domain tidak ada. |

### 4.2 Ringkasan hitungan URL

| Metrik | Nilai |
|---|---|
| URL unik di register yang diperiksa | 22 |
| Hidup apa adanya saat diakses | **16** |
| Mati (DNS / 404) | **3** (siap-lafki, acch.kpk, journalcenter/18212) |
| Diblokir (403/JS) | **3** (researchgate, cell.com, web.bpjs-kesehatan) - substansi terverifikasi via jalur pengganti |
| Klaim sumber dengan bukti akses (langsung atau substitusi) | **21 dari 22** |
| **Mismatch substansi** (judul/tahun/isi/atribusi/kelas sumber) | **9** |
| Sitasi yang tidak dapat dilacak (risiko fabrikasi) | **2** (MHINAGSL; SHAP+RAG MDPI 2025) |

---

## 5. Indikasi Sumber Berisiko

### 5.1 Pola SEO / kualitas rendah

| Indikator | Temuan |
|---|---|
| Blog marketing dipakai sebagai satu-satunya sumber klaim Kritis | Baris 18 (allalliedhealthschools.com - sekolahrumpun bidang kesehatan AS, blog promosi SEO) untuk **Phantom Billing, Relevansi Kritis, "Terverifikasi"**. |
| Halaman marketing firma hukum | Baris 27 (phillipsandcohen.com - firm whistleblower AS) untuk **Unbundling**. |
| Blog konsultan Anti-Fraud / ISO 37001 | Baris 19 (sustain.id) - kadar air tinggi (kualitas rendah), level C/D; dipakai untuk modus Kritis. |
| Sitasi blog tanpa identitas penulis/peer review | Baris 11 & 12 (situs transaksi billing AS). |
| Parameter URL tanpa id melekat (lowercase, tanpa id/kategori) | `https://siap-lafki.or.id/bpjs-kesehatan-dan-tantangan-fraud-20-triliun-perspektif-ilmu-administrasi-dalam-pengelolaan-ja` - slug terpotong ("…pengelolaan-ja"), ciri URL yang disalin dari tampilan kategori/arsip, bukan artikel permanen. |
| Skema URL artikel yang mati | `journalcenter.org/…/download/4767/3750/18212` - segmen ekstra "18212" memberi 404; path asli hanya `/download/4767/3750`. |

### 5.2 Tahun 2026 dan volume placeholder

- **2026 bukan placeholder pada dua sumber yang diperiksa**: AI Review 59(4) (terbit 17 Feb 2026, DOI resolves) dan Zenodo PREreview (31 Jul 2026). Keduanya sah.
- Namun **dua rujukan 2026/2025 tidak dapat dilacak sama sekali**: "MHINAGSL - IEEE Access 2025, multiview heterogeneous, F1 0,92" dan "studi triase auditor berbasis SHAP+RAG (MDPI 2025)". Keduanya gagal masuk ke pola khas rujukan yang ditambahkan untuk mengisi celah, bukan dari penelusuran literatur. Rekomendasi: **hapus dari register** sampai ada DOI/DOI-terverifikasi.
- 

### 5.3 DOI yang tidak resolve

- DOI yang **resolve dan cocok**: 10.1016/j.heliyon.2024.e30045; 10.1186/s40537-025-01295-3; 10.1007/s10462-026-11516-7; 10.35907/bgjk.v14i2.220; 10.55606/inovasi.v4i1.4767 (dengan inkonsistensi volume v4i1 vs Vol 3 No 3); 10.5281/zenodo.21717009; 10.22146/jkesvo.69065 (sumber pengganti, belum dipakai); 10.51601/ijhp.v5i3.341 (sumber pengganti, belum dipakai).
- **Tidak ada DOI sama sekali** untuk: RAG paper MHGSL (hanya URL cell.com), ACCH KPK (URL mati), LAFKI (URL mati), Kompas/Kontan/Stabilitas/Liputan6 (media, wajar), BPJS PDF (dokumen resmi tanpa DOI - wajar).
- DOI paper MHGSL tidak pernah dicantumkan di kolom `Sumber Riset` register, padahal ada di Deskripsi baris 10 - **metadata DOI tidak konsisten** (04 §9 butir terakhir).

### 5.4 Judul artikel yang terlalu generik / penanda "referensi purwarupa"

Baris 1 Catatan: "studi triase auditor berbasis SHAP+RAG (MDPI 2025) **relevan sebagai referensi purwarupa**" - kalimat ini menandai sumber yang memang tidak pernah dibaca ("untuk purwarupa"), persis kategori "referensi purwarupa" yang diminta untuk diflag. Baris 15 (Federated Learning) dan baris 16 (DPO) secara eksplisit menyatakan belum ada sitasi kuat - ini jujur, tetapi berarti keduanya **tidak memiliki bukti** dan tidak boleh tampil sebagai klaim.

### 5.5 Risiko fabrikasi (ringkas)

| Item | Status verifikasi | Tindakan |
|---|---|---|
| "MHINAGSL (IEEE Access 2025, F1 0,92)" (baris 10) | **TIDAK TERVERIFIKASI** - 0 hasil Crossref title search, 0 hasil OpenAlex title search | Hapus atau ganti dengan DOI nyata |
| "studi triase auditor berbasis SHAP+RAG (MDPI 2025)" (baris 1) | **TIDAK TERVERIFIKASI** - tidak ada kandidat Cocok di Crossref MDPI Appl. Sci. 2025 | Hapus |
| "±1.000 verifikator" (baris 24) | Hanya sumber: repo sendiri | Cari sumber resmi BPJS atau turunkan jadi "asumsi tim" |
| "113,47 T/tahun" (baris 31) | Tanpa URL; angkanya sebenarnya klaim 2022 (Antara/IDN Times) | Tambahkan URL + tahun periode |
| "BBC Indonesia membahas risiko tekor Rp20 T" (baris 31) | Tanpa URL; tidak ada jejak publikasi BBC Indonesia untuk topik ini | Hapus |
| "durasi rawat +35% pada skor fraud 92%" (baris 22 Catatan) | Angka simulasi internal yang presented sebagai "atribusi SHAP di dokumen sumber" | Tandai sebagai output demo |

---

## 6. Inkonsistensi Silang Antar Tiga Dokumen

### 6.1 04-evidence-matrix ↔ register 33 baris

| # | Isu | Detail |
|---|---|---|
| I-1 | Judul Permenkes 16/2019 salah di 04 §5 butir 3 | 04 menulis "…serta Pengendalian Gratifikasi dalam Program Jaminan Kesehatan"; judul resmi (peraturan.bpk.go.id) adalah "…Sera Pengenaan Sanksi Administrasi Terhadap Kecurangan (Fraud) Dalam Pelaksanaan Program Jaman Kesehatan". Judul yang dipakai sustain.id justru yang benar → indikasi register lebih akurat dari dokumen governance. |
| I-2 | Status E-03 vs baris 20 | 04: "Sebagian terverifikasi"; register: "Terverifikasi" untuk sumber yang sama (media, level C). |
| I-3 | Instruksi E-04 tidak diterapkan ke baris 24 | 04 melarang repo internal sebagai satu-satunya sumber; baris 24 persis demikian (repo sendiri), dan berstatus "Sebagian Terverifikasi" tanpa sumber kedua. |
| I-4 | Format entri 04 §7 tidak terpenuhi | 04 §7 mewajibkan 11 field per baris (judul, penulis, tahun, jurnal, DOI/URL, **jenis sumber + strength A–D**, klaim spesifik, **kutipan/halaman/tabel**, **caveat**, **reviewer + tanggal verifikasi**, status + alasan). Skema CSV hanya punya 8 kolom; **tidak ada kolom strength A–D, reviewer, tanggal verifikasi, maupun kutipan/anchor**. Akibatnya aturan 04 §3 ("C dan D tidak boleh menjadi satu-satunya dasar klaim spesifik/berisiko tinggi") **tidak dapat dien.force secara mekanis**. |
| I-6 | Baris 5 & 9 berbagi satu URL | Satu Zenodo record dipakai untuk dua klaim berbeda (AUPRC utama; SMOTE) →encer dan melanggar aturan 04 §6 ("Hindari mengutip satu artikel untuk mendukung banyak klaim yang tidak diuji"). |

### 6.2 06-research-notes ↔ 04 / register

- **Tidak ada klaim di 06 yang absen dari 04/register** - ini bagian yang sehat: 06 §1–§8 konsisten dengan kerangka 04.
- Namun **06 §5 "Matriks Bukti Awal" hanya memuat 8 dari 12 klaim 04** (E-10 "waktu −45%" dan E-11 "Rp507.370.000" tidak masuk). 06 §6 sendiri sudah meminta secara normatif "tautkan klaim utama ke halaman dan tabel sumber" - belum dilakukan.
- 06 §7 "Sumber Awal" **tidak memuat anchor halaman/tabel** (berlawanan dengan 06 §6 sendiri).
- 06 §9 masih menandai "Verifikasi semua statistik nasional" sebagai belum dikerjakan, sementara register sudah menandai 6 statistik nasional sebagai "Terverifikasi" (baris 20, 26, 30, 31, 32 + baris 4) → **ketidaksesuaian status antar dokumen**.

### 6.3 Item register "Kritis" vs pemakaian di 01-proposal dan 05-decision-scope

11 baris Kritis: 1 (SHAP/XAI), 4 (UU PDP), 7 (XGBoost), 10 (MHGSL), 13 (SATUSEHAT/FHIR), 18 (Phantom billing), 20 (Volume 2 juta/hari), 24 (1.000 verifikator), 25 (Upcoding), 32 (Healthkathon), 33 (Purwarupa).

- **01-proposal memakai nol dari sebelas klaim Kritis tersebut secara kuantitatif.** Proposal memang sengaja tidak mengutip statistik eksternal mana pun (bagian §1 penutup dan §8 menyatakan semua angka draft "belum dinyatakan sebagai hasil tervalidasi") - **ini pilihan editorial yang benar dan harus dipertahankan**.
- Yang bermasalah: **status "Terverifikasi" pada register menciptakan rasa aman yang tidak berdasar**, karena tidak ada satupun yang dipakai di proposal. Status register dan pemakaian dokumen harus dipisah secara eksplisit.
- **05-decision-scope §3** justru **menolak** dua kandidat yang didukung register: Kandidat 2 (verifikasi identitas - baris 26 "Terverifikasi", "Penyalahgunaan identitas/kartu JKN", Relevansi Tinggi) dan Kandidat 3 (anomali upah/iuran - baris 21 & 28, keduanya bersumber dari domain mati). Artinya register mengutamakan jalur yang secara resmi ditolak; implikasi: pengumpulan sumber untuk kedua baris itu pekerjaan sia-sia dan statusnya jangan dipakai untuk justifikasi.
- 05 §5 "Out-of-scope" melarang klaim penghematan nasional yang diekstrapolasi dari dataset sintetis dan integrasi produksi V-Claim/SATUSEHAT - konsisten dengan 04 §8, tetapi **berbenturan dengan baris 31** ("Arus klaim ±Rp500 M/hari … sebagai basis proyeksi penghematan solusi") dan baris 12 (V-Claim) yang terdaftar sebagai "Terverifikasi".
- 05 §7 butir "Konfirmasi tema dan persyaratan resmi kompetisi dari sumber penyelenggara" - tema "Detect Smarter, Protect JKN" **terverifikasi** lewat kanal resmi BPJS (video peluncuran 20 Agu 2026) dan Liputan6; namun "kompetisi tahunan ke-6" (baris 32) tidak terbukti dan hitungan edisi yang benar adalah: 2019, 2020, 2021, 2022 (pertama Bernama Healthkathon), 2023 (Healthkathon 2.0), 2024, 2025, 2026 → **edisi ke-8 sebagai hackathon, ke-7 dengan nama Healthkathon**. Versi "enam tahun berturut-turut" berasal dari artikel IDN Times (Des 2025) yang merujuk periode 2019–2025.

---

## 7. Klaim yang Butuh Sitasi Primer tapi Hilang

| # | Klaim | Di mana muncul | Yang dibutuhkan | Status |
|---|---|---|---|---|
| G-1 | Prevalence fraud 3–7% JKN | Baris 29; baris 17 (skenario sensitivitas); 04 E-05 | Studi primer dengan definisi fraud + denominator (denominator = total nilai klaim) | **Hilang** - sumber mati; pembanding USD 300 miliar adalah ordinalitas, bukan laju |
| G-2 | Jumlah verifikator BPJS (±1.000) & rasio 2.000:1 | Baris 24; 04 E-04; argumen inti proposal | Rilis resmi/laporan resmi BPJS atau dokumen sumber resmi | **Hilang** - hanya repo sendiri |
| G-3 | Volume klaim "2 juta/hari" sebagai *hari kerja* | Baris 20; 04 E-03 | Laporan/kutipan resmi bertanggal (bukan media) | **Sebagian** - media sah, tetapi kualifikasi "per hari kerja" perlu dihapus atau sumber primer dicari |
| G-4 | "Korupsi/kerugian Rp20 T" | Baris 30; 04 E-06 | Sumber primer: pernyataan resmi KPK (pidana/temuan) + definisi "10% pengeluaran kesehatan masyarakat" | **Sebagian** - atribusi ke BPJS keliru; LAFKI mati |
| G-5 | Khazanah modus JKN (upcoding, phantom, cloning, unbundling, prolonged stay, drug diversion, penahanan iuran) | Baris 18–19, 21–23, 25, 27–28 | Kajian primer empiris JKN / audit resmi | **Hilang** - yang ada: normative legal study (baris 23), blog marketing (18, 27), blog konsultan (19), URL mati (21, 28), mirror 403 (25). **Alternatif siap pakai & belum dipakai**: Sugiarti, Masturoh & Fadly, "Menelusuri Potensi Fraud dalam Jaminan Kesehatan Nasional melalui Rekam Medis di Rumah Sakit", *Jurnal Kesehatan Vokasional* 7(1) Feb 2022, DOI 10.22146/jkesvo.69065 (87 dokumen, kode diagnosis taktep 31,03%, ketidaksesuaian tarif klaim 26,44%, 91,30% berupa kenaikan tarif); review *IJHP* 5(3) 2025 DOI 10.51601/ijhp.v5i3.341; Djasri et al. 2016 *Integritas* KPK 2(1):113–133 (terverifikasi via republicasi). |
| G-6 | "Plus 20% AUPRC, minus 42% false negative" | Baris 8; 04 E-08 | Tabel eksperimen paper asli **atau** artefak internal (prediksi, split, metrik) | **Hilang dan tidak ada di paper** - sumber yang dikutip tidak memuat AUPRC |
| G-7 | Benchmark AUPRC 0,9142 | 01-proposal §8; 04 E-07 | ID eksperimen + skrip metrik + split + prediksi | **Hilang** (README proyek sendiri menulis 0,91) |
| G-8 | Penghematan Rp507.370.000 | 01-proposal §8; 04 E-11 | Tarif acuan INA-CBG, formula per klaim, status adjudikasi | **Hilang** |
| G-9 | 20 menit → 3 menit; kapasitas ×6,7 | Baris 2; 04 E-09 | Protokol uji pengguna + data waktu mentah | **Hilang** - sumber internal tanpa sumber eksternal |
| G-10 | Biaya token LLM | Baris 11 | Kalkulator resmi Google **per tanggal** + model generasi terbaru | **Sebagian** - URL resmi ada, angkanya ($0,10–1,50) usang |
| G-11 | SHAP/XAI untuk audit klaim | Baris 1; 04 E-12 | Sitasi primer SHAP (Lundberg & Lee) + studi XAI fraud; referensi tambahan harus yang bisa dilacak | **Sebagian** - SLR AI Review sah; entri tambahan MDPI 2025 tidak terlacak |
| G-12 | Klaim UU PDP (pasal, sanksi, DPO, notifikasi 3×24 jam) | Baris 4; 04 E-01 | Naskah pasal resmi (JDIH BPK) per pasal | **Tersedia tapi disalahrujukan** - all clauses dapat diverifikasi, tetapi register menuliskan nomor pasal dan nominal denda yang keliru |
| G-13 | Regulasi: UU 17/2023 Kesehatan | 04 §5; 01-proposal Referensi | Verifikasi status & pasal (pasal.id: Berlaku, ditetapkan DPR RI, diundangkan 8 Agu 2023) | **Tersedia & konsisten** (satu-satunya peraturan yang clean) |
| G-14 | "Penanganan yang dibayangkan seperti surat keterangan sakit fiktif kolusif" | Baris 26 | Sumber resmi yang menyebut modus ini | **Hilang** - PDF BPJS hanya menyebut penyalahgunaan kartu/identitas |
| G-15 | Aturan UU PDP yang dirujuk proposal (persetujuan eksplisit, enkripsi, penunjukan petugas PDP) | Baris 4 | Pasal 4(2) data spesifik (benar), Pasal 20 dasar pemrosesan, Pasal 53 (istilah resmi: "pejabat atau petugas yang melaksanakan fungsi Pelindungan Data Pribadi"), Pasal 46(1) | **Sebagian** - substansi benar, istilah "DPO" bukan istilah UU |

---

## 8. Rekomendasi

**Prioritas 1 - sebelum gerbang publikasi (04 §9)**

1. **Perbaiki baris 4 (UU PDP)** menjadi: "Pasal 67 (pelanggaran Pasal 65): 5 tahun/Rp5 M; 4 tahun/Rp4 M; 5 tahun/Rp5 M. Pasal 68 (pelanggaran Pasal 66): penjara paling lama 6 tahun dan/atau denda paling banyak Rp6.000.000.000. Notifikasi kegagalan PDP: Pasal 46(1), paling lambat 3×24 jam kepada subjek data dan lembaga. Penunjukan petugas fungsi PDP: Pasal 53." Ganti istilah "DPO" dengan istilah Pasal 53. Level A.
2. **Turunkan status AUPRC.** Hapus "AUPRC +20% & FN −42%" sebagai klaim bersumber paper; pindahkan ke daftar "belum tereproduksi" dengan sumber = artefak internal. Tandai 0,9142 sebagai angka draf yang belum tervalidasi (sudah dilakukan di proposal §8 - pertahankan).
3. **Hapus dua sitasi tidak terlacak** (MHINAGSL; SHAP+RAG MDPI 2025) dari baris 1 dan 10 sampai ada DOI terverifikasi.
4. **Perbaiki URL mati**: journalcenter → `/download/4767/3750`; ajukan perbaikan/penggantian sumber untuk siap-lafki (baris 21, 29) dan acch.kpk (baris 22, 28) - misalnya dengan Djasri et al. 2016 via *Integritas* KPK/mutupelayanankesehatan.net, dan *IJHP* 5(3) 2025.
5. **Selaraskan status baris 20 dengan 04 E-03** ("Sebagian terverifikasi") dan hapus "per hari kerja" dari Deskripsi.

**Prioritas 2 - strengthen governance (2–3 hari kerja)**

6. **Tambahkan kolom pada register**: `Jenis Sumber & Strength (A–D)`, `Kutipan/Halaman/Tabel`, `Caveat`, `Reviewer`, `Tanggal Verifikasi`. Tanpa kolom strength, aturan 04 §3 tidak dapat ditegakkan. Terapkan aturan: baris dengan strength C/D **tidak boleh** berstatus "Terverifikasi" bila Relevansi = Kritis (menyentuh baris 18, 24, 27, 32, 33).
7. **Perbaiki judul Permenkes 16/2019 di 04 §5 butir 3 dan di 01-proposal Referensi** menjadi judul resmi dari peraturan.bpk.go.id.
8. **Tambahkan sumber primer empiris JKN** untuk khazanah modus dan prevalensi: Sugiarti et al. 2022 (DOI 10.22146/jkesvo.69065), Djasri et al. 2016, review *IJHP* 2025 (DOI 10.51601/ijhp.v5i3.341).Ketiganya menutup baris 18, 19, 21, 22, 23, 25, 27, 28 dengan level B dalam satu langkah.
9. **Perbarui baris 31**: pisahkan klaim 2026 (2 juta transaksi/hari, Rp500 M/hari, loss ratio 108,72% - Stabilitas) dari klaim 2022 (Rp113,47 T - ANTARA/IDN Times), tambahkan URL untuk yang kedua, dan hapus "BBC Indonesia" (tanpa sumber).
10. **Catat status sandbox SATUSEHAT** pada baris 12 (modul klaim BPJS = Environment Sandbox per banner), beserta versi dokumentasi (7.23) dan tanggal akses - Persis E-02.
11. **Perbarui baris 11** dengan harga Gemini terkini dan model generasi terbaru; hapus rentang "$0,10–1,50".

**Prioritas 3 - perbaikan substansi dan berbiaya rendah**

12. **Ganti sumber level D untuk baris 18 & 27** (phantom billing, unbundling) dengan literatur peer-review; jika tidak ada, turunkan relevansi ke "Pendukung" dan beri label eksploratif.
13. **Pisahkan satu URL untuk dua klaim** (baris 5 dan 9): gunakan referensi SMOTE primer (mis. Chawla et al. 2002, SMOTE, JAIR) dan rujukan AUPRC yang berbeda.
14. **Hapus "kompetisi tahunan ke-6"** dari baris 32; tulis "edisi 2026 (dilorca 2019–2026)". Pertahankan tema "Detect Smarter, Protect JKN" (terverifikasi kanal resmi).
15. **Selaraskan angka AUPRC README (0,91) vs proposal (0,9142)** atau gunakan satu sumber angka tunggal yang diberi label "belum tervalidasi".
16. **Lengkapi 06-research-notes §5** dengan E-10 dan E-11 agar 8 klaim menjadi 12, dan tambahkan anchor halaman/tabel di §7 sesuai §6 dokumen itu sendiri.
17. **Catat eksplisit di 04 §2** bahwa label status register adalah label status sumber, bukan status pemakaian di proposal - untuk mencegah "Terverifikasi" dibaca sebagai "siap dipublikasikan".

**Aturan konstan untuk pembaruan berikutnya:** setiap sumber baru wajib dicatat di lampiran §9 (URL + tanggal akses + temuan) sebelum statusnya dinaikkan; sumber yang gagal diakses ditandai **TIDAK TERVERIFIKASI** (bukan "tidak ada"), dan klaim yang tidak punya sumber primer tidak boleh menaikkan status ke status "Terverifikasi".

---

## 9. Lampiran - Log Sumber Web yang Diverifikasi

Semua entri diakses **22 Oktober 2026** melalui MCP SearXNG (`searxng_web_search` → `web_url_read`); jalur alternatif (Crossref, Semantic Scholar, OpenAlex, EuropePMC, PMC, GitHub API, peraturan.bpk.go.id, pasal.id) diakses sebagai substitusi bila URL asal gagal.

| # | URL | Tanggal akses | Temuan |
|---|---|---|---|
| 1 | https://link.springer.com/article/10.1007/s10462-026-11516-7 | 22 Okt 2026 | Baca langsung gagal (JS). Metadata via https://api.crossref.org/works/10.1007/s10462-026-11516-7: judul cocok, *Artificial Intelligence Review* 59(4), terbit 2026-02-17, lisensi CC BY-NC-ND, 63 referensi, 12 sitasi. Tahun 2026 sah. |
| 2 | https://link.springer.com/article/10.1186/s40537-025-01295-3 | 22 Okt 2026 | Baca langsung gagal. https://api.crossref.org/works/10.1186/s40537-025-01295-3 (vol 12, 2025, CC BY-NC-ND) + https://api.semanticscholar.org/graph/v1/paper/DOI:10.1186/s40537-025-01295-3 (DBLP journals/jbd/CurtisPKF25) + full text https://journalofbigdata.springeropen.com/articles/10.1186/s40537-025-01295-3. Judul/jurnal/tahun cocok; angka "$300 billion annually in the US" terkonfirmasi di abstract; memuat MHGSL F1 0,895 vs StGNN 0,875 / MHAMFD 0,881 / MBGNN 0,891. |
| 3 | https://www.cell.com/heliyon/fulltext/S2405-8440(24)06076-6 | 22 Okt 2026 | 403. Full text via https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11061682/fullTextXML (dan https://pmc.ncbi.nlm.nih.gov/articles/PMC11061682/). Judul "Health insurance fraud detection based on multi-channel heterogeneous graph structure learning", Heliyon 10(9):e30045, 2024, DOI 10.1016/j.heliyon.2024.e30045, PMID 38694097, PMCID PMC11061682, CC BY. **AUPRC/precision-recall: 0 kemunculan**; "42%": 0; "20%" = proporsi data latih. Metrik: ACC/AUC/F1 (Medical-A, Tabel 6), F1/Precision (Medical-B, Tabel 7). Statistik intro paper: USD 260 miliar/tahun (6% belanja kesehatan global), 3%–10% belanja medis (National Health Care Anti-Fraud Association), NHSA China 708.000 faskes/2021. |
| 4 | https://zenodo.org/records/21717009 | 22 Okt 2026 | https://zenodo.org/api/records/21717009: judul "PREreview of 'Improving Medicare Fraud Detection Accuracy in Deep Learning by Exploring Feature Selection and Data Sampling Techniques'", DOI 10.5281/zenodo.21717009, terbit 2026-07-31, preprint DOI 10.64898/2026.03.18.26348763. Isi: Chi-Square top-25 + SMOTE → 95,4% accuracy, F1 0,94, recall 0,98 Fraud; Major Issue #1 = "Accuracy is the wrong headline metric for imbalanced fraud detection". Tipe: peer review komunitas atas preprint (bukan artikel ilmiah). |
| 5 | https://ml-research.github.io/papers/fang2022dpctgan.pdf | 22 Okt 2026 | PDF hidup: Fang M.L., Dhami D.S., Kersting K., "DP-CTGAN: Differentially Private Medical Data Generation using CTGANs", AIME 2022. Judul/tahun cocok. |
| 6 | https://www.allalliedhealthschools.com/blog/fine-line-between-error-and-fraud-a-guide-to-upcoding-unbundling-and-phantom | 22 Okt 2026 | Hidup; judul cocok. Blog pendidikan/marketing sekolah allied health AS - level D. |
| 7 | https://www.phillipsandcohen.com/upcoding-unbundling-fragmentation/ | 22 Okt 2026 | Hidup; halaman marketing firm hukum whistleblower AS - level D. |
| 8 | https://keuangan.kontan.co.id/news/klaim-layanan-bpjs-kesehatan-tembus-2-juta-per-hari | 22 Okt 2026 | Hidup. "Pada 2014 tercatat sekitar 252.000 transaksi klaim per hari … kini lebih dari 2 juta transaksi per hari" (Ghufron Mukti, 17/9/2025). Tidak ada "per hari kerja", tidak ada angka verifikator, tidak ada Rp500 miliar. |
| 9 | https://money.kompas.com/read/2024/09/21/131900126/klarifikasi-bpjs-kesehatan-soal-potensi-kerugian-rp-20-triliun-akibat | 22 Okt 2026 | Hidup. BPJS (Irfan Humaidi) "membantah" Rp20 T sebagai kerugian BPJS; asal angka: Wakil Ketua KPK Alexander Marwata, 19/9/2024, "10 persen dari pengeluaran untuk kesehatan masyarakat, sekitar Rp 20 triliun secara nominal"; disebut juga phantom billing & manipulasi data peserta. |
| 10 | https://sustain.id/2024/10/04/fraud-dalam-pelayanan-kesehatan-di-indonesia-dan-strategi-pencegahnya/ | 22 Okt 2026 | Hidup. Taksonologi fraud JKN (upcoding, diagnosis tidak perlu, klaim berlebih, rujukan tidak perlu, kartu orang lain, suplier obat, iuran) - **tanpa drug diversion/over-dosing**. Mengutip Permenkes 16/2019 dengan **judul resmi yang benar**. |
| 11 | https://acch.kpk.go.id/id/component/content/article?id=672:korupsi-dalam-pelayanan-kesehatan-di-era-jaminan-kesehatan-na | 22 Okt 2026 | **GAGAL** - DNS tidak resolve (gaierror) pada domain maupun path alternatif. Substansi terkonfirmasi lewat https://mutupelayanankesehatan.net/publikasi-korupsi-dalam-pelayanan-kesehatan-di-era-jaminan-kesehatan-nasional-kajian-besarnya-potensi-dan-sistem-pengendalian-fraud/ (republikasi + ringkasan; 175.774 klaim FKRTL berpotensi fraud nilai Rp440 M per pertengahan 2015) dan https://scholar.google.co.in/citations?user=ahtFQsoAAAAJ (Integritas KPK 2(1):113–133, 2016) dan https://ijhp.net/index.php/IJHP/article/view/341. |
| 12 | https://siap-lafki.or.id/bpjs-kesehatan-dan-tantangan-fraud-20-triliun-perspektif-ilmu-administrasi-dalam-pengelolaan-ja | 22 Okt 2026 | **GAGAL** - DNS tidak resolve (www maupun non-www); web.archive.org 404; Wayback 429. TIDAK TERVERIFIKASI. |
| 13 | https://journalcenter.org/index.php/inovasi/article/download/4767/3750/18212 | 22 Okt 2026 | **404 DEAD**. URL benar https://journalcenter.org/index.php/inovasi/article/download/4767/3750 hidup: *Inovasi* Vol 3 No 3 Sept 2024 Hal 81–92, DOI 10.55606/inovasi.v4i1.4767 (DOI v4i1 vs volume 3 - inkonsistensi internal), metode hukum normatif, memuat "cloning … penjiplakan klaim dari pasien lain". |
| 14 | https://www.researchgate.net/publication/369679967_ANALISIS_KEJADIAN_UPCODING_BIAYA_PELAYANAN_KESEHATAN_DI_WILAYAH_KERJA | 22 Okt 2026 | 403 (mirror). Kanonik via https://api.crossref.org/works/10.35907/bgjk.v14i2.220: *Bina Generasi* 14(2) 2023, Sariunita & Syakurah, KC Depok, desain kualitatif deskriptif 1–30 Jul 2021, tanpa angka prevalensi. |
| 15 | https://web.bpjs-kesehatan.go.id/uploads/information/4bd28c6ea8f022040f6eb93cfcd6e723.pdf | 22 Okt 2026 | 403 (bot detection). PDF hidup via https://www.bpjs-kesehatan.go.id/uploads/information/4bd28c6ea8f022040f6eb93cfcd6e723.pdf: "Panduan Layanan JKN-KIS"; Kewajiban Peserta no. 6 "Menjaga identitas peserta JKN-KIS agar tidak rusak, hilang atau dimanfaatkan oleh orang yang tidak berhak"; 127 KC + 388 KK; **tanpa** volume/verifikator, **tanpa** "surat keterangan sakit fiktif". |
| 16 | https://www.liputan6.com/health/read/8270049/healthkathon-2026-digelar-bpjs-kesehatan-dorong-pemanfaatan-ai-untuk-perkualitas | 22 Okt 2026 | Hidup, terbit 14 Agu 2026 17:29 WIB. Kriteria: "efisiensi risiko pada peserta, fasilitas kesehatan, dan pemberi kerja"; pendaftaran 14 Agt–14 Sep 2026; approach problem-first (Setiaji, Dirut TI); Alex Budiyanto (Asosiasi Manajemen Data Indonesia). Tidak memuat "ke-6"/"pendaftaran sudah ditutup". Tema "Detect Smarter, Protect JKN" terkonfirmasi lewat https://www.youtube.com/watch?v=ylwNQM2bZH0 (kanal resmi BPJS, 20 Agu 2026). |
| 17 | https://www.stabilitas.id/rasio-klaim-tembus-10872-bpjs-kesehatan-bayar-rumah-sakit-rp500-miliar-sehari/ | 22 Okt 2026 | Hidup, 15 Jun 2026. Loss ratio 108,72%; "2 juta transaksi … Rp500 miliar sehari"; Dirut Prihati Pujowaskito, 12 Jun 2026; defisit ~Rp2 T/bulan; proyeksi gagal bayar Juli 2027; suntikan Rp20 T. Tidak memuat 113,47 T/tahun. |
| 18 | https://satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/ | 22 Okt 2026 | Hidup; banner "Portal Dokumentasi SATUSEHAT Versi 7.23"; halaman modul memuat peringatan modul masih dalam pengembangan ("hanya tersedia di Environment Sandbox"). |
| 19 | https://peraturan.bpk.go.id/Details/245544/permenkes-no-24-tahun-2022 | 22 Okt 2026 | Hidup; Permenkes 24/2022 tentang Rekam Medis, berlaku 31 Agu 2022, mencabut Permenkes 269/2008, status Berlaku. |
| 20 | https://peraturan.bpk.go.id/Details/129762/permenkes-no-16-tahun-2019 | 22 Okt 2026 | Hidup; judul resmi "Pencegahan dan Penanganan Kecurangan (Fraud) Sera Pengenaan Sanksi Administrasi Terhadap Kecurangan (Fraud) Dalam Pelaksanaan Program Jaman Kesehatan"; ditetapkan 18 Jul 2019, berlaku 31 Jul 2019, mencabut Permenkes 36/2015. |
| 21 | https://pasal.id/peraturan/uu/uu-no-27-tahun-2022 | 22 Okt 2026 | Hidup. Pasal 4(2) data spesifik; Pasal 20 dasar pemrosesan; Pasal 46(1) notifikasi 3×24 jam ke subjek data + lembaga; Pasal 51 prosesor; Pasal 53 penunjukan petugas fungsi PDP; Pasal 67 (5th/Rp5 M; 4th/Rp4 M; 5th/Rp5 M); Pasal 68 (6th & Rp6 M). |
| 22 | https://pasal.id/peraturan/uu/uu-no-17-tahun-2023 | 22 Okt 2026 | Hidup; "Undang-Undang Nomor 17 Tahun 2023 tentang KESEHATAN", ditetapkan DPR RI, diundangkan 8 Agu 2023, status Berlaku. |
| 23 | https://ai.google.dev/gemini-api/docs/pricing | 22 Okt 2026 | Hidup; Gemini 1.5 tidak lagi terdaftar; Flash 3.8/3.6 input $0,75/1M (→$1,50 sejak 1 Jan 2027), Batch $0,375; Flash-Lite $0,30; Pro 3.1 Preview $2,00/$4,00 input, $12,00/$18,00 output; 3 Flash Preview $0,50. |
| 24 | https://github.com/biezz-2/Aegis-JKN (+ https://api.github.com/repos/biezz-2/Aegis-JKN/readme) | 22 Okt 2026 | Hidup; README menyebut "2.000.000 klaim per hari … 1.000 petugas verifikator (rasio 2.000:1)" dan "**AUPRC 0.91**" (berbeda dari 0,9142 di proposal). Sumber level D (repo sendiri). |
| 25 | https://api.github.com/repos/sunchang0124/dp_cgans | 22 Okt 2026 | Repo ada: "A library to generate synthetic tabular or RDF data using Conditional GANs combined with Differential Privacy techniques". |
| 26 | https://api.github.com/repos/Irham-Najib-Azimul-Qowi/PatuhRadar | 22 Okt 2026 | Repo ada, **description null** → klaim "data UMP 38 provinsi (2024–2026)" TIDAK TERVERIFIKASI. |
| 27 | https://journal.ugm.ac.id/jkesvo/article/download/69056/33299 | 22 Okt 2026 | Hidup (PDF): Sugiarti, Masturoh & Fadly, *Jurnal Kesehatan Vokasional* 7(1) Feb 2022, DOI 10.22146/jkesvo.69065 - 87 dokumen, kode diagnosis taktep 31,03%, ketidaksesuaian tarif 26,44%, 91,30% kenaikan tarif; "Upcoding tidak selalu disebut fraud". Sumber primer pengganti untuk baris 25. |
| 28 | https://ijhp.net/index.php/IJHP/article/view/341 | 22 Okt 2026 | Hidup: "Analysis of Fraud in National Health Insurance in Indonesia: A Literature Review", *IJHP* 5(3) Aug 2025, DOI 10.51601/ijhp.v5i3.341 (SLR; menyebut Djasri et al. 2016 sebagai sumber primer). |
| 29 | https://mutupelayanankesehatan.net/publikasi-korupsi-dalam-pelayanan-kesehatan-di-era-jaminan-kesehatan-nasional-kajian-besarnya-potensi-dan-sistem-pengendalian-fraud/ | 22 Okt 2026 | Hidup: ringkasan/republikasi kajian Djasri, Rahma & Hasri; 175.774 klaim FKRTL, Rp440 M; upcoding, inflated bills, service unbundling, no medical value, standard of care. |
| 30 | https://www.idntimes.com/news/indonesia/bpjs-kesehatan-gelar-healthkathon-02-8j7n5-gqt6tl | 22 Okt 2026 | Hidup (9 Des 2025): "Kompetisi telah digelar selama **enam tahun berturut-turut** dengan lebih dari 14.000 peserta"; sejarah Healthkathon 2019 → 2025 (tema per tahun); 2026 menjadi edisi berikutnya. |
| 31 | https://www.idntimes.com/business/finance/bpjs-kesehatan-gelontorkan-klaim-csc-02-f5vsw-34t9x1 | 22 Okt 2026 | Hidup (18 Jul 2023): BPJS membayar klaim **Rp113,47 triliun** untuk 2022 - sumber Primer yang hilang untuk baris 31. |
| 32 | https://manajemen-pembiayaankesehatan.net/ | 22 Okt 2026 | Hidup, tetapi **tidak ditemukan artikel berisi "113,47 T"** pada arsip yang tersedia (hanya 3 entri terbaru: UHC/ekonomi); tidak dapat dipakai sebagai sumber angka. |
| 33 | https://healthkathon.bpjs-kesehatan.go.id/ | 22 Okt 2026 | Hidup (SPA, judul "Healthkathon 2026 BPJS Kesehatan"); REST API pada port 8080 membalas 404 untuk path yang dicoba; tidak ada teks tema/kriteria yang dapat diekstrak. |
| 34 | https://api.crossref.org/works?query.title=MHINAGSL | 22 Okt 2026 | **0 hasil** → "MHINAGSL (IEEE Access 2025)" tidak dapat dilacak. |
| 35 | https://api.openalex.org/works?filter=title.search:MHINAGSL | 22 Okt 2026 | **0 hasil** → konfirmasi independen. |
| 36 | https://api.crossref.org/journals/2076-3417/works?query.bibliographic=… (MDPI Appl. Sci., filter 2025) | 22 Okt 2026 | Tidak ada studi "triase auditor berbasis SHAP+RAG"; kandidat terdekat: TRAG (RAG untuk emergency triage, 2026), Ethereum XAI (2025), fraud telekomunikasi berbasis LLM (2026) - tidak cocok. |

**Catatan keterbatasan.** (a) Tiga URL tombol ditolak akses langsung (researchgate 403, cell.com 403, web.bpjs-kesehatan 403) sehingga kesimpulan diambil dari jalur substitute resmi (Crossref/Semantic Scholar/EuropePMC/publisher). (b) Dua domain (siap-lafki.or.id, acch.kpk.go.id) tidak resolve dari lingkungan audit maupun jaringan alternatif; keduanya ditandai TIDAK TERVERIFIKASI, bukan "tidak ada". (c) Kemampuan mesin pencari di belakang SearXNG berada dalam kondisi degraded (brave/duckduckgo/google cse sebagian diblokir); beberapa pencarian kueri whistleblower/keyword Indonesia tidak menghasilkan hasil, sehingga desain ulang register berbasis sumber primer tetap perlu diulang manual. (d) Verifikasi ini menilai **kesesuaian sumber dengan klaim**, bukan kebenaran isi artikel (audit metodologis masing-masing artikel berada di luar cakupan).
