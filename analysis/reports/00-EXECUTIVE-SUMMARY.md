# 00 - Ringkasan Eksekutif dan Audit Konsolidasi Proyek Aegis-JKN

Status: Laporan audit internal, sintesis akhir
Tanggal audit: 22 Oktober 2026
Ruang lingkup: konsolidasi 24 laporan audit internal terhadap corpus proyek Aegis-JKN (Healthkathon 2026, BPJS Kesehatan), rekap 40 temuan, penilaian kesiapan, dan rencana aksi submit
Dasar: 24 laporan di `N:\HEALTHKATHON\analysis\reports\`, corpus data `analysis\corpus\claims_v2_live.csv` (300 baris), repositori `Aegis-JKN\` dan `mechine-learning-deep-learning\`, API resmi Healthkathon, dan PDF keluaran Colab 16 halaman
Metode: polling laporan selesai (idle 8 menit tercapai pada elapsed 1445 detik, log di `scripts\poll_log.txt`), lalu seluruh 24 laporan dibaca utuh, bukan hanya judulnya

---

## 1. Ringkasan Eksekutif

**Aegis-JKN adalah purwarupa riset untuk mendeteksi potensi fraud klaim JKN** yang menggabungkan tiga saluran data (topologi jaringan, kemiripan fitur, dan kanal semantik berbasis teks) di atas satu graf heterogen, dengan late fusion `p_fused = p_graph + gamma * f_text * (1 - p_graph)`. Produknya berupa aplikasi Next.js yang berjalan publik di `aegisjkn.vercel.app`, sebuah dashboard HTML mandiri, satu naskah proposal akademik Revisi 1.0, dan dataset simulasi 300 klaim. Tim sudah membangun basis yang tidak sedikit: arsitektur 7-tier dirinci, tata kelola PDP dirangkai dari UU PDP, matriks de-identifikasi 18 identifier, dan `00-dashboard.md:46-52` secara eksplisit mendaftarkan sembilan angka yang belum boleh disebut hasil tervalidasi.

**Yang sudah terverifikasi.** Angka struktural dataset cocok byte-per-byte dengan corpus: total nominal Rp3.526.650.000, 240 auto_clear / 24 review / 36 escalate, 36 klaim fraud senilai Rp561.150.000, 60 klaim anomali senilai Rp841.100.000, 12 klaim kontradiksi, 189 rawat inap / 111 rawat jalan, 170 sentimen positif / 58 netral / 72 negatif, 40 pasien, 20 dokter, 10 faskes, 9 sindikat. Angka eksternal 2 juta klaim per hari dan 650.000 berkas per hari dengan indikasi fraud sekitar 5 persen terverifikasi dari media primer. Deadline juga terverifikasi dari API resmi: submit project akhir aktif 19 Oktober sampai 1 November 2026 dan Grand Final 7 November 2026, jadi tersisa 16 hari kalender.

**Yang hanya diklaim, belum terbukti.** Sembilan angka headline utama tidak dapat direproduksi dari artefak mana pun: akurasi 93,0 persen, presisi 94,12 persen, ROC-AUC 0,9825, AUPRC 0,9142, ketahanan masking 89,4 persen, false positive rate 10,6 persen, penurunan waktu telaah 45 persen, throughput 3,2 kali, dan SUS 82,5. Satu koreksi perlu ditegaskan: FPR 10,6 persen dapat dihitung dari data aktif, tetapi hanya di ambang `skor_fraud` 0,14 (28 false positive dari 264 negatif = 10,6061 persen), dan presisi pada ambang itu hanya 56,25 persen. Presisi 94,12 persen tidak tercapai pada ambang mana pun, sehingga tidak ada operating point yang memenuhi kedua klaim itu. Batas atas nyata fitur yang tidak bocor jauh lebih rendah: F1 terbaik 0,3448, sementara AUPRC acak pada prevalensi ini 0,12. Angka baseline XGBoost AUPRC 0,71 tidak punya skrip pembanding, dan estimasi penghematan Rp507.370.000 tidak punya tarif acuan, formula, atau ledger per klaim. Korpus mengkonfirmasi sendiri penyebabnya: `12-archive-architecture.md:55` menyatakan seluruh metrik komparatif adalah adaptasi literatur Hong et al., Heliyon 2024, bukan hasil eksperimen internal, dan `04-evidence-matrix.md:34` menandai AUPRC 0,9142 sebagai belum tereproduksi. Angka pada PDF Colab juga tidak memuat satu pun dari angka benchmark itu.

**Tiga risiko terbesar.** Pertama, kebocoran label dan pembulatan benchmark. Delapan kolom turunan label (`Sinyal SHAP`, `Kontribusi Saluran`, `Alasan`, `Status`, `Skor Fraud`, `Modus`, `Sindikat`, `Kontradiksi Narasi`) ikut terbawa ke frontend dan berkas JSON publik, benchmark utama di sel 13 notebook dievaluasi in-sample tanpa split, dan graf dibangun sebelum split sehingga A_sem memakai kolom `sindikat` yang justru dilarang. Kedua, ground truth terpublikasi: `Aegis-JKN/public/payload-aegis-jkn.json` identik byte-per-byte dengan payload Colab dan memuat `gtSent`, `sentiment_gt`, serta `syndHit`. Ketiga, akumulasi kesalahan rujukan hukum: judul resmi Permenkes 16/2019 disalah kutip, Permenkes 24/2022 disebut sebagai dasar HL7 FHIR R4 padahal naskahnya nol kali menyebut FHIR, empat pasal UU PDP disematkan keliru, dan sembilan peraturan wajib tidak dicantumkan, termasuk PP 33/2026 sebagai aturan pelaksanaan UU PDP.

**Tiga kekuatan.** Tim menulis naskah Revisi 1.0 yang sengaja menurunkan sendiri klaimnya, hal yang jarang pada peserta lain. Dasbor kendali `00-dashboard.md` tidak memuat satu pun status Tervalidasi untuk angka mana pun, dan singkatan, satuan tabel, struktur dokumen sudah diaudit editorially. Aplikasi berjalan publik dengan 133 file ter-version, dataset explorer 2.159 baris fungsional, dan tata kelola PDP lengkap dari Pasal 16 UU PDP sampai Hybrid Safe-Mode. Implementasi ML di repo terpisah nyata, yaitu notebook 22 sel dan backend FastAPI dengan PyTorch Geometric, sehingga masalahnya bukan ketiadaan kode, melainkan cara kode itu dievaluasi.

**Tiga hal yang tidak boleh ditawar.** Hapus ground truth dari bundle publik sebelum submit, kunci definisi label dan ambangnya di satu file konfigurasi, dan jangan pernah menyebut angka tanpa artefak sebagai hasil, termasuk di arsip dan index. Sisa 16 hari tidak cukup untuk membangun pipeline analitik lengkap, memvalidasi ground truth secara klinis, dan menyiapkan demo yang meyakinkan sekaligus. Yang tersedia cukup untuk proposal jujur, satu pipeline evaluasi minimal yang bisa dijalankan ulang, dan submit lengkap secara administratif.

Rekomendasi akhir: jalur utama submit dengan menurunkan klaim dan menambah artefak yang bisa dijalankan ulang.

---

## 2. Register Temuan Konsolidasi (F-01 sampai F-40)

Temuan identik dari dua atau lebih laporan digabung menjadi satu baris dan seluruh sumbernya dicantumkan. Klaim yang dapat diperiksa ulang sudah diverifikasi ulang dengan skrip sendiri di `analysis\reports\scripts\`. Klaim yang tidak dapat diperiksa ditandai "(belum diverifikasi)". Angka-angka-of-record yang dipakai di bawah merujuk tabel kanonik `21-numbers-of-record.md` bagian 2.

| ID | Temuan | Sumber laporan | Dampak | Prioritas |
|---|---|---|---|---|
| F-01 | Sembilan angka headline (93,0%, 94,12%, 0,9825, 0,9142, 89,4%, 10,6%, 45%, 3,2x, SUS 82,5) tidak dapat direproduksi dari artefak mana pun; 10 dari 11 angka utama berstatus NO pada rekonstruksi. Presisi 94,12% tidak tercapai pada ambang mana pun (terdekat 94,7368% di ambang 0,78). Batas atas fitur yang tidak bocor hanya F1 0,3448, dan AUPRC acak pada prevalensi data ini 0,12 | `16-red-team.md:183-196`; `02-proposal.md:64-158`; `21-colab-dashboard-provenance.md:50-74`; `21-numbers-of-record.md:72-80`; `22-proposal-docx-audit.md:192-202` | Klaim inti produk tidak dapat dipertanggungjawabkan di depan juri | P0 |
| F-02 | Baseline XGBoost AUPRC 0,71 tidak punya skrip, split, seed, atau file prediksi; angka tersebut tetap hidup di UI dan API backend sebagai konstanta hardcode (`data.ts:253,261,264`; `backend/src/api/main.py:365-398`) | `16-red-team.md:188`; `08-frontend.md:196`; `06-graph-mhgsl.md:188` | Perbandingan performa tidak dapat diuji ulang | P0 |
| F-03 | Klaim finansial tanpa dasar: estimasi penghematan Rp507.370.000 (60,32% dari Rp841.100.000) tidak punya tarif acuan, formula, atau ledger per klaim, dan `Rp1,2 M/bulan` serta `Rp14,4 M/tahun` dihitung dari asumsi slider | `16-red-team.md:63,375`; `10-competition.md:375-380`; `02-proposal.md:164-176`; `17-roadmap.md:67`; `22-proposal-docx-audit.md:107-108,170,182` | Klaim berisiko ditafsirkan sebagai temuan nyata atas nama BPJS | P0 |
| F-04 | Ground truth dipublikasikan ke peramban: `Aegis-JKN/public/payload-aegis-jkn.json` identik byte-per-byte dengan payload Colab (md5 `31cc9fe8...`) dan memuat `gtSent`, `sentiment_gt`, serta `syndHit` | `21-colab-dashboard-provenance.md:50-74`; `09-security.md:309`; `21-numbers-of-record.md:223` | Model dapat mencapai target tanpa membaca data; reputasi rusak berat | P0 |
| F-05 | Leakage kolom turunan ke feature set dan ke ekspor: `Sinyal SHAP`, `Kontribusi Saluran`, `Alasan`, `Status`, `Skor Fraud`, `Modus`, `Sindikat`, `Kontradiksi Narasi` diekspor ke UI, 8 kolom terlarang menurut kamus data | `03-architecture.md:23,134,273`; `16-red-team.md:22,61-62`; `08-frontend.md:217` | Benchmark apa pun di atas data ini tidak bermakna | P0 |
| F-06 | Benchmark bersifat circular: `Risiko` adalah ambang dari `Skor Fraud`, `Status` adalah coarsening deterministik `Risiko`, `is_fraud` diturunkan dari `Risiko`. Pemisahan kelas sempurna (36 fraud pada 0,80-0,95 dan 264 non-fraud pada 0,04-0,79, tanpa tumpang tindih), sehingga AUPRC dan ROC-AUC dihitung dari kolom label bernilai 1,0000 | `06-methodology.md:38,155-160`; `04-data-quality.md:171`; `21-numbers-of-record.md:70-71,135-148` | Target bukan adjudikasi; metrik terutama mengukur ambang | P0 |
| F-07 | Klaim unit test anti-leakage `tests/test_leakage.py` dan `configs/leakage.yaml` tidak ada di disk, padahal dirujuk 13 kali di dalam corpus | `15-code-quality.md:16,110,446`; `03-architecture.md:273-274`; `16-red-team.md:37`; `20-repo-artifact-integrity.md:90-91` | Jaminan anti-leakage yang dijanjikan ke juri kosong | P0 |
| F-08 | Klaim novelty bertabrakan dengan sumber sendiri: MHGSL adalah metode Hong et al., Heliyon 2024, DOI 10.1016/j.heliyon.2024.e30045, dan corpus sendiri mengakui "diadaptasi dari"; `06-research-notes.md:42` menyatakan belum dapat direproduksi | `16-red-team.md:20,60`; `06-graph-mhgsl.md:429,444,451`; `04-evidence-matrix.md:34`; `06-research-notes.md:41-43` | Framing state-of-the-art runtuh saat dibaca juri akademis | P0 |
| F-09 | Angka 93,0% adalah akurasi leksikon sentimen (186 dari 200 uji) dan bukan akurasi deteksi fraud, dipakai sebagai KPI fraud di corpus dan dashboard; deterministik dari bug substring (kata "lama" cocok di "Pengalaman", 14 kegagalan dari 200 uji), dan berada di bawah baseline sepele 97,0% pada prevalensi 3% yang dipakai proyek sendiri | `21-colab-dashboard-provenance.md:64,100-105,126-130`; `16-red-team.md:26,36` | Salah kategori metrik inti | P0 |
| F-10 | 100% deteksi fraud (14 dari 14) dan 100% hit-rate sindikat adalah label by construction: himpunan fraud = ambang skor 0,80 yang dipilih agar pas, dan seluruh 16 klaim sindikat sengaja masuk antrean 20 | `21-colab-dashboard-provenance.md:65,67`; `06-graph-mhgsl.md:432` | Disajikan sebagai performa model padahal konsekuensi definisi | P0 |
| F-11 | Arsitektur 7-tier minus pipeline analitik: tidak ada rule engine Tier-1, tidak ada model di repo aplikasi, tidak ada split, tidak ada evaluator, tidak ada file prediksi | `03-architecture.md:21,32`; `08-frontend.md:232`; `20-repo-artifact-integrity.md:92` | Klaim arsitektur tidak punya implementasi | P0 |
| F-12 | Empat skala ambang risiko hidup berdampingan (0,35/0,60/0,80; 0,40/0,62/0,80; 0,40/0,65/0,85; 0,35/0,45/0,60/0,75) dan ambang 0,80 belum dikunci eksplisit, dengan KLM115 sebagai kasus batas | `15-code-quality.md:25`; `03-architecture.md:160-170`; `19-consistency.md:554`; `02-proposal.md:247-252` | Angka label tidak konsisten antar lapisan | P0 |
| F-13 | UI memuat 24 grup angka hardcoded tanpa kualifikasi, 5 di antaranya melanggar daftar larangan `00-dashboard.md:46-52` secara literal (93%, AUPRC 0,91, ROC-AUC 0,95, Precision 0,92, Rp 1,2 M per bulan), termasuk varian organisasional salah: 240 rawat inap / 60 jalan, 8 dari 8 kontradiksi, 14 edge berlebih, Rp 3,53 M, 16 dari 16 | `08-frontend.md:193-220`; `09-security.md:274-280`; `18-ux.md:369`; `21-numbers-of-record.md:186-217` | Overclaim dan angka salah terlihat langsung di layar juri | P0 |
| F-14 | `Kontradiksi Narasi` bukan hasil analisis narasi, melainkan lookup dari kolom `Modus` (TP 12, FP 0, FN 0, TN 288), dan label `Sentimen` juga diturunkan dari `Modus` | `13-text-channel.md:30,144-172,221` | Modul deteksi teks nol kemampuan | P0 |
| F-15 | Dataset 300 klaim tidak dapat direproduksi: skrip generator tidak ada di repo mana pun, tidak ada kolom seed, version, atau timestamp, tidak ada checksum, dan 9 dari 9 artefak wajib struktur v2.1 hilang; notebook utama 22 sel menyimpan 0 karakter output | `07-generator.md:15,23,170-171`; `20-repo-artifact-integrity.md:92-93`; `21-numbers-of-record.md:177`; `22-proposal-docx-audit.md:49-59,295` | Tidak ada satu pun artefak eksperimen yang bisa dijalankan ulang | P0 |
| F-16 | Ground truth bertentangan dengan data: narasi KLM004-KLM006 mengonfirmasi tindakan yang seharusnya ditagih phantom billing, dan 6 baris anomali frekuensi tidak punya episode yang cocok | `07-generator.md:17,163,167` | Skenario inti sindikat tidak konsisten | P0 |
| F-17 | Arsitektur dan index menghidupkan kembali klaim terlarang: `11-archive-proposal.md:15,30,326-330` dan `14-index.md:490,505` menyebut metrik sebagai Tervalidasi dan Rp507.370.000 sebagai Penyelamatan Riil, dan tetap ada klaim "dapat direplikasi secara objektif" | `02-proposal.md:70,173-176`; `19-consistency.md:26,28,310,327`; `01-governance.md:15` | Angka yang sengaja diturunkan tetap hidup di tempat juri membaca | P0 |
| F-18 | Klaim "Tier-3 PyTorch Geometric HeteroData GCN" tidak didukung implementasi: `backend/src/models/mhgsl.py:15` memakai `GCNConv` homogen satu `edge_index` per kanal, dan `HeteroData` nol kemunculan di seluruh repo ML; notebook utama berjalan tanpa PyG | `06-graph-mhgsl.md:204-210,435,505`; `21-numbers-of-record.md:188` | Arsitektur inti berbeda dari yang ditulis di naskah | P0 |
| F-19 | Evaluasi benchmark salah sejak awal: sel 13 notebook mem-fit lalu mem-predict pada matriks yang sama (XGBoost, MLP, GCN homogen, MHGSL), adjacency dan scaler dibangun sebelum split, A_sem dibangun dari kolom `sindikat` yang ada di daftar Leakage, dan hit-rate dijaga `assert` sehingga hasilnya pasti lolos | `06-graph-mhgsl.md:329,376-400`; `17-roadmap.md:34-35`; `21-numbers-of-record.md:174-176`; `22-proposal-docx-audit.md:112-130` | Tidak ada satu pun metrik yang valid untuk klaim performa | P0 |
| F-20 | Skala tidak memadai untuk klaim GNN: A_feat hanya 2.192 edge (densitas 2,11% pada ambang 0,85) dari 44.850 pasangan, parameter model 37.157 atau 124 per baris data, prevalensi aktual 36 dari 300 = 12,0% bukan 1-3% seperti diklaim, dan pada LOGO faskes 34 dari 36 kasus fraud (94,4%) berasal dari sindikat yang tidak pernah muncul di fold training | `06-graph-mhgsl.md:27,144,229,236-240,264,339-341,440,483-495` | Klaim klaster padat, klaster sindikat, dan rasio prevalensi runtuh | P0 |
| F-21 | XAI dan fusion tidak sesuai klaim: "SHAP Attribution Decomposition Engine" diimplementasikan sebagai L2 norm per kanal (`torch.norm`), additivitas terhadap logit tidak valid, "Attention Fusion" di dokumen teori sebenarnya concat tanpa attention, dan nilai negatif `W_top` = -0,12 tidak mungkin dihasilkan oleh softmax dari bobot yang dipelajari | `06-graph-mhgsl.md:56-57,93,118,418,436-439` | Penjelasan-per-saluran yang ditampilkan ke juri tidak mengukur apa pun | P0 |
| F-22 | Tidak ada bukti bahwa multi-channel lebih baik dari satu kanal: nol eksperimen masking, nol ablasi per-saluran, dan uji enrichment menemukan A_sem tidak signifikan (p = 0,138) serta A_homo lebih buruk dari acak (p = 0,730); densest-subgraph A_feat berisi 48 node tanpa satu pun kasus fraud | `06-graph-mhgsl.md:411,448,506-517` | Argumen arsitektur utama belum diuji | P1 |
| F-23 | Klaim privasi "aman menurut Permenkes 24/2022 dan UU PDP" bertentangan dengan empat dokumen sendiri yang menyatakan pseudonimisasi bukan anonimisasi; Pasal 34 UU PDP tentang penilaian dampak tidak disebut di mana pun, PP 71/2019 sebagai rezim PSE untuk hosting luar negeri tidak dicantumkan, dan tidak ada kontrol prompt injection, PII egress, maupun DPA untuk kanal LLM | `11-compliance.md:35,239-269,394-397,404`; `13-text-channel.md:37,394-395,405-412` | Risiko hukum dan kebocoran data pada demo publik | P0 |
| F-24 | Rujukan hukum salah kutip: judul resmi Permenkes 16/2019 disalah kutip sebagai "...serta Pengendalian Gratifikasi"; Permenkes 24/2022 disebut sebagai dasar HL7 FHIR R4 padahal nol kali menyebut HL7, FHIR, atau SATUSEHAT; sanksi pidana UU PDP disematkan ke Pasal 65 dan 66 yang sebenarnya Pasal 67 dan 68; "3x24 jam" disematkan ke Pasal 4 ayat (2) yang sebenarnya Pasal 46 ayat (1); "Data Pribadi Spesifik" disematkan ke Pasal 4 ayat (3) yang sebenarnya ayat (2) | `11-compliance.md:33-38,101,134,145-152,413-417`; `05-evidence.md:126-127`; `22-proposal-docx-audit.md:248-255` | Risiko integritas akademik dan kredibilitas hukum | P0 |
| F-25 | Sembilan peraturan wajib tidak dicantumkan di proposal: PP 33/2026 sebagai aturan pelaksanaan UU PDP (ditetapkan dan diundangkan 16 Juli 2026, berlaku 16 Januari 2027 menurut Pasal 225), PP 71/2019, PP 28/2024, Permenkes 6/2026, Kepmenkes HK.01.07/MENKES/1199/2025 (FORNAS baru, berlaku 1 April 2026), Permenkes 18/2022, Permenkes 3/2023, UU 13/2022 jo UU 1/2026, dan Peraturan BPJS 3/2024 | `11-compliance.md:43-44,388-405,429-431` | Gambaran kepatuhan tidak lengkap dan cepat kedaluwarsa | P1 |
| F-26 | Kode medis dan tarif tidak dapat diverifikasi: ICD-9-CM 00,66 dilabeli "angioplasty koroner plus stent" padahal 00,66 adalah PTCA tanpa stent (stent 36,06 dan 36,07), 93,90 dilabeli "terapi oksigen tekanan positif" padahal 93,90 adalah ventilasi mekanik non-invasif dengan IPPB pada 93,91, insulin glargine ditandai tidak ada di FORNAS padahal tercantum di Kepmenkes 1199/2025 bagian 16.2.2, nomor versi koding ICD-10 dan ICD-9-CM Versi 2010 wajib disebut tetapi tidak disebut, dan kolom tarif tanpa kode grup kasus INA-CBG | `11-compliance.md:38-41,182-187,306,314,333,340-343,421-423` | Tabel klinis dan tarif di demo terbukti salah | P1 |
| F-27 | Text channel tidak pernah dievaluasi: recall ground truth kontradiksi hanya 12 dari 24 (50%, 12 baris terlewat), teks sangat berulang (36 string umpan balik unik untuk 300 baris, 40 narasi unik, 18 alasan unik), `f_text` biner 0 atau 1 bukan skor -1 sampai 1, 48 dari 48 entri feed berlabel heuristik-lokal, dan `08-training-protocol.md` nol kali menyebut kanal teks | `13-text-channel.md:29-39,253-258,381-399,472-500` | Modul yang diklaim sebagai kontribusi tidak punya prosedur evaluasi | P1 |
| F-28 | Cacat kualitas data: `dokter_raw` terpotong 32 baris di `claims_300_v2.1.csv` (D04 pada 11 baris dan D16 pada 21 baris) sementara dump Notion utuh, 28 baris memuat literal `undefined` pada kolom Rujukan, 156 baris memakai sentinel garis panjang (U+2014) pada kolom prosedur, 109 baris bernilai LOS 0 sehingga menyatukan "tidak berlaku" dengan "sinyal fraud", dan 1 baris Alasan kosong | `04-data-quality.md:35,43-45,65,371-373,382,410-416,459-470` | Data gate gagal diam-diam dan merusak klaim "bersih" | P1 |
| F-29 | Angka operasional bentrok antar artefak: PDF Colab memakai 20 ke 3 menit per berkas sehingga kapasitas 6.667 berkas, tapi naskah DOCX mengklaim 3,2 kali, dan 20 ke 3 adalah 6,667 kali; versi Inggris `i18n.tsx:791` menulis Rp 14,4 miliar per tahun berhadapan dengan Rp 14,4 juta pada `i18n.tsx:443` (selisih 1000 kali); arsip menyebut nominal sindikat Rp542,56 juta dan modus Upcoding Rp127,68 juta, sedangkan CSV Rp539.650.000 dan Rp156.900.000 | `21-numbers-of-record.md:60,87-91,212`; `19-consistency.md:28,256-257`; `08-frontend.md:199-200`; `22-proposal-docx-audit.md:150-166,176-178,182-184` | Angka yang tampil di layar dan di naskah saling bertentangan | P1 |
| F-30 | Tabel SYND dan tabel entitas di korpus tidak cocok dengan data: 4 dari 9 baris salah pada pemetaan pasien, 5 dari 9 salah pada rentang skor, dan tabel entitas di `10-simulation-dataset.md` tidak cocok pada 6 dari 6 faskes, 10 dari 10 diagnosis, 12 dari 12 dokter, serta 20 dari 20 pasien | `10-competition.md:30,457`; `04-data-quality.md:346`; `19-consistency.md:27,257,275`; `21-colab-dashboard-provenance.md:166`; `22-proposal-docx-audit.md:134-148,180` | Tabel yang ditampilkan di demo terbukti salah | P1 |
| F-31 | Klaim eksternal berskala nasional tanpa sitasi primer: 53 baris (2 juta klaim per hari, 1.000 verifikator, 175.774 klaim ACCH KPK, Rp25 miliar) tanpa URL sumber, dan angka resmi KPK yang ditulis Rp25 miliar sebenarnya hampir Rp35 miliar (3 RS swasta); selain itu 113 pasangan singkatan tidak terdefinisi pada pemakaian pertama dengan 741 kemunculan, 41 dari 51 tabel tanpa satuan, dan 43 dari 51 tanpa baris Total | `14-language.md:22-24,72-74,219-223`; `10-competition.md:31,374,376`; `05-evidence.md:189`; `22-proposal-docx-audit.md:201,203` | Melanggar Standar Dokumen bagian 7 dan berisiko keliru faktual. Angka 872 dari `10-competition.md:72` juga penghitung API live lintas kategori dengan rincian 0/0/0 sehingga tidak boleh diklaim sebagai 872 tim di kategori Fasilitas Kesehatan, dan prevalensi 3-7% berasal dari GAO-24-105833 yang mengukur kewajiban federal AS non-kesehatan | P1 |
| F-32 | Integritas sitasi: dua sitasi fiktif ("MHINAGSL IEEE Access 2025 F1 0,92" dan "studi triase SHAP+RAG MDPI 2025" tidak ditemukan di Crossref maupun OpenAlex), 3 URL mati, 3 URL diblokir, dan 9 mismatch substansi pada register 22 URL | `05-evidence.md:142-150,187-192`; `14-language.md:22`; `22-proposal-docx-audit.md:90,270-271` | Risiko integritas akademik | P1 |
| F-33 | N dan desain evaluasi tidak menopang protokol: power analysis AUPRC menghasilkan interval 95 persen sangat lebar pada 300 baris dan AUROC 0,90 punya CI yang mencakup baseline, sementara normalisasi serta pemilihan hiperparameter dilakukan di luar fold (theta_feat 0,85 dipilih dari data fold train) | `06-methodology.md:39,213-330`; `03-architecture.md:121`; `06-graph-mhgsl.md:370`; `22-proposal-docx-audit.md:85-87` | Optimisme pada metrik validasi | P1 |
| F-34 | Empat ilustrasi klinis upcoding, phantom, dan unbundling, konsep Topological Camouflage, analisis 5-Whys, matriks PDP Pasal 16, matriks AI versus verifikator, dan 4 aturan Tier-1 hilang saat revisi, sementara kata "purwarupa" naik 7 kali dan "kolusi" 18 kali di arsip | `10-competition.md:32,418-428`; `17-roadmap.md:36` | Nilai argumentatif yang hilang justru yang dicari juri | P1 |
| F-35 | Kualitas build: `npm run build` lolos hanya karena `typescript.ignoreBuildErrors: true`, `npx tsc --noEmit` keluar kode 1 dengan 8 error, `npm run lint` gagal 5 error, `npm test` tidak ada, dan tidak ada CI di `.github/` | `15-code-quality.md:18,33-36,224-228`; `09-security.md:310` | Kualitas tipe dan pengujian tidak dijaga | P1 |
| F-36 | Permukaan serang: ekspor 27 kolom tanpa banner kualifikasi dan masih memuat kolom terlarang, `robots.txt` mengizinkan semua crawler, API publik tanpa rate limit, CORS, dan autentikasi, nol header keamanan di `next.config.ts` dan `vercel.json`, proxy Caddy meneruskan ke port pilihan klien tanpa TLS, serta 14 kerentanan npm | `09-security.md:202,306-320`; `08-frontend.md:319` | Risiko kebocoran data dan penyalahgunaan endpoint | P1 |
| F-37 | Kelolaan repo dan secret: `N:\HEALTHKATHON` adalah working tree tertinggal dengan 122 file terhapus sementara repo aplikasi sebenarnya `Aegis-JKN\` memiliki 133 file tracked sinkron dengan origin, tidak ada `.gitignore` di root sehingga `git add -A` akan meng-commit 9,1 GB data sampel BPJS, dan token Notion ter-hardcode di lima file skrip `Notion-docs\*.py` (token tidak pernah masuk history git, jadi cukup rotasi, bukan tulis ulang history) | `20-repo-artifact-integrity.md:9-13,25-35,119-140,180-185,207-221` | Risiko commit tidak sengaja dan secret bocor saat commit berikutnya | P1 |
| F-38 | Submit belum siap: 12 dari 20 item checklist submit kosong (C1 manifest, C2 baseline, C3 definisi label, C5 tabel SYND, C6 tarif, C8 posisi terhadap sistem berjalan, C9 video demo, C10 deck), Participant Guide tidak terbaca (403 untuk bot) sehingga daftar berkas wajib belum diketahui, akun portal belum terverifikasi, demo yang dideploy berjalan di 100 klaim sementara proposal memakai 300 klaim, dan kategori "Sindikat Kolusi Rujukan" padahal data nol sinyal kolusi | `10-competition.md:28-30,388-411,457-468` | Risiko tidak lolos seleksi project akhir. Deadline di corpus juga masih salah: `dataset_research_live.json` dan artikel IDN Times menyebut 14 September 2026, sedangkan API resmi menyatakan submit project akhir 19 Oktober sampai 1 November 2026 dan Grand Final 7 November 2026 | P1 |
| F-39 | Dokumen proposal yang dikirim tidak reproducible dari skrip repo: cover memuat kota CIMAHI dan tanggal 9 Oktober 2026 sedangkan skrip builder menyertakan JAKARTA dan "Jakarta, Oktober 2026"; dokumen berisi 7 entri Daftar Gambar tetapi nol objek gambar di `word/document.xml` dan nol berkas di `word/media/`, sedangkan cadangan `.bak` masih menyimpan 3 gambar dan 17 tabel; metadata dokumen kosong dengan creator "python-docx"; dan Caption Gambar 6.1 berbeda antara cadangan dan dokumen kirim. Artinya ada jalur build kedua yang tidak tercatat di repo | `22-proposal-docx-audit.md:49-59,295-297` | Naskah yang diserahkan juri tidak dapat diaudit, diregenerasi, atau dikoreksi deterministik; setiap perbaikan angka akan hilang pada build berikutnya | P0 |
| F-40 | Kernel proposal belum lengkap: nol abstrak, nol daftar singkatan, nol glosarium, nol lampiran, nol anggaran, nol identitas bertanda tangan, nol nama anggota tim, nol kontak, nol protokol eksperimen (tidak ada split, seed, ambang, atau prosedur evaluasi selain sebutan seed 20260707), nol metode statistik, nol persetujuan etika, nol batasan eksplisit studi, dan nol penanda sitasi dalam teks untuk 18 rujukan pustaka. Ditambah 13 kontradiksi internal naskah, footer tanpa field PAGE, Daftar Isi sebagai teks statis bukan field TOC, hanya satu style paragraf, dan penyampur pemisah desimal titik dengan koma | `22-proposal-docx-audit.md:71-92,244-289` | Unsur kernel yang menentukan kelayakan ilmiah tidak ada; pemeriksa akan membuka lampiran dan menemukan kekosongan | P0 |

---

## 3. Skor Kesiapan Proyek

Skala 1 sampai 5. Skor 5 berarti siap handed over. Skor 1 berarti belum ada sama sekali. Skor total maksimum 35.

| # | Dimensi | Skor | Dasar penilaian (ringkas) |
|---|---|---|---|
| 1 | Kesiapan proposal dan naskah | 3 | Revisi 1.0 jujur dan terstruktur, daftar angka terlarang sudah ada di `00-dashboard.md:46-52`, dan 10 kriteria akademik bernilai rata-rata 3,4 dari 5 (`02-proposal.md:39-56`). Tapi rujukan hukum salah kutip di 4 pasal dan 1 judul peraturan (F-24), 9 peraturan wajib tidak dicantumkan (F-25), 2 sitasi fiktif (F-32), 53 baris angka nasional tanpa sitasi primer (F-31), dan 12 dari 20 item checklist submit kosong (F-38). Audit DOCX menambah: dokumen kirim tidak reproducible dari skrip repo (F-39), kernel proposal tidak lengkap (F-40), 13 kontradiksi internal naskah, dan nol sitasi dalam teks untuk 18 rujukan. |
| 2 | Kualitas dan tata kelola data | 2 | Hitungan struktural 300 baris konsisten dan cocok corpus (Rp3.526.650.000, 240/24/36, Rp841.100.000, 12 kontradiksi, 40 pasien, 20 dokter, 10 faskes). Tapi definisi label belum final (F-12), 8 kolom leakage ikut terbawa (F-05), pemetaan sindikat salah 4 dari 9 (F-30), 32 baris `dokter_raw` terpotong, 28 baris `undefined`, 156 baris sentinel (F-28), dan tidak ada manifest atau checksum (F-15). |
| 3 | Metodologi ML dan validasi eksperimen | 2 | Protokol tertulis rapi di arsip (GroupKFold pada pasien, LOGO pada faskes, bootstrap dan Hanley-McNeil) dan implementasi PyTorch Geometric di repo terpisah nyata ada. Tapi benchmark utama in-sample (F-19), graf dibangun sebelum split dan memakai kolom terlarang (F-19), normalisasi di luar fold (F-33), skala 124 parameter per baris dan 94,4% sindikat unseen (F-20), klaim HeteroData tidak ada kodenya (F-18), dan SHAP yang diimplementasikan bukan SHAP (F-21). |
| 4 | Implementasi frontend dan aplikasi | 3 | Build produksi berjalan, aplikasi live di `aegisjkn.vercel.app`, dataset explorer 2.159 baris benar-benar fungsional. Tapi 24 grup angka hardcoded tanpa kualifikasi dan 5 di antaranya terlarang (F-13), empat skala ambang (F-12), tidak ada rule engine dan audit trail (F-11), dan typecheck gagal 8 error (F-35). |
| 5 | Kepatuhan regulasi dan bukti hukum | 1 | Struktur UU PDP Pasal 16, matriks de-identifikasi 18 identifier, dan Hybrid Safe-Mode tersedia di arsip. Tapi 4 dari 7 regulasi yang diperiksa memiliki isi yang salah, 4 pasal UU PDP disematkan keliru, judul satu peraturan salah kutip, HL7 FHIR disandarkan ke naskah yang tidak menyebutnya (F-24), 9 peraturan wajib hilang termasuk PP 33/2026 (F-25), kode medis dan tarif salah label (F-26), klaim privasi "aman" tanpa DPIA (F-23), ground truth dipublikasikan (F-04), serta 2 sitasi fiktif (F-32). |
| 6 | Reproduksibilitas dan artefak | 1 | Tidak ada `manifest.json`, `label_audit.csv`, `train.py`, `metrics.json`, `evaluation_report.md`, `configs/leakage.yaml`, `tests/test_leakage.py`, `edges_v2.1.json`, `features_300.parquet`, `graph_hetero.pt`, atau `CHECKSUMS.txt`. Generator 300 baris tidak ada di repo mana pun, notebook menyimpan 0 output, dan 9 dari 9 artefak wajib v2.1 hilang (F-15, F-07). Naskah DOCX yang dikirim pun tidak reproducible dari skrip builder karena ada jalur build kedua yang tidak tercatat (F-39). |
| 7 | Kesiapan demo-day | 2 | Grand Final 7 November 2026, sisa 16 hari; belum ada video demo, deck, atau naskah presentasi (`10-competition.md:400-401`), daftar berkas wajib belum diketahui (C13), akun portal belum terverifikasi (C15), demo berjalan di 100 klaim sementara proposal 300 klaim (F-38), dan alur demo masuk ke 36 klaim tereskalasi tidak selesai di bawah 2 menit (`18-ux.md:137-142`). |

**Total: 14 dari 35 (40,0 persen).**

Catatan pembanding: `10-competition.md:14` memberi skor siap 2,6 dari 5 (56 persen) dengan dasar yang sama. Selisihnya karena laporan tersebut menilai dari sisi apa yang sudah ada (arsitektur, tata kelola, aplikasi), sedangkan tabel di atas menilai dari sisi apa yang bisa dipertanggungjawabkan saat submit (artefak, bukti angka, kepatuhan). Keduanya konsisten bahwa posisi tim ada di jalur submit dengan perbaikan teks dan artefak, bukan jalur eksperimen baru. Penurunan skor kepatuhan dari 2 menjadi 1 murni karena temuan baru `11-compliance.md` yang menguji isi naskah peraturan, bukan hanya keberadaan rujukan.

---

## 4. Tiga Skenario Submit

Probabilitas gagal di sini didefinisikan sebagai peluang proposal tidak lolos seleksi project akhir (2-4 November 2026) atau ditolak juri karena temuan yang dapat dibuktikan sendiri dari repo dan corpus.

| Skenario | Apa yang diklaim | Risiko utama | Probabilitas gagal | Effort |
|---|---|---|---|---|
| A. Submit apa adanya dengan klaim diturunkan | Hanya yang terverifikasi: purwarupa 7-tier atas 300 klaim sintetis, 36 eskalasi, 60 anomali, total Rp3,53 Miliar, UI berjalan, arsitektur dan tata kelola PDP. Semua angka performa dan finansial dibuang dari naskah, deck, dan UI. | Juri membandingkan arsip dan index dengan dashboard dan menemukan klaim Tervalidasi yang masih hidup (F-17); menemukan `payload-aegis-jkn.json` yang memuat ground truth (F-04); menemukan 24 angka hardcoded di UI (F-13); dan menemukan 4 pasal UU PDP yang disematkan keliru (F-24). Menemukan dokumen yang dikirim tidak reproducible dari skrip repo dan tidak berisi satu pun gambar meski Daftar Gambar mendaftarkan 7 (F-39); menemukan kernel proposal kosong, termasuk nol protokol eksperimen dan nol sitasi dalam teks (F-40). Tidak ada video, deck, atau daftar berkas wajib saat submit. | Tinggi, sekitar 70 persen | 1,5 sampai 2 hari kerja (edit teks dan hapus angka di UI) |
| B. Submit setelah perbaikan P0 minimum dalam 2 hari | Skenario A ditambah: satu pipeline evaluasi minimal yang benar-benar jalan di atas 300 baris (split GroupKFold pada pasien dan LOGO pada faskes, adjacency dibangun di dalam fold, seed 20260707, satu file prediksi held-out, satu skrip metrik), satu `experiments/manifest.json`, satu `tests/test_leakage.py` yang memblokir 8 kolom terlarang, definisi label final tertulis, video demo 3-5 menit, dan deck maksimal 10 slide. Metrik yang dilaporkan hanya yang berasal dari pipeline itu, AUPRC pada prevalensi 12 persen, bukan klaim presisi tinggi. | Risiko angka hasil pipeline baru bisa jelek dan tidak ada waktu untuk menghasilkan baseline pembanding; daftar berkas wajib masih belum diketahui (C13); akun portal belum terverifikasi (C15); 10 hari kerja dari 22 Oktober sudah terpakai 2 hari oleh regresi; dan 4 temuan kepatuhan baru harus ditutup hanya dengan koreksi teks, bukan redesign. | Sedang, sekitar 45 persen | 2 hari kerja (48 jam) untuk 5 butir P0, sisanya paralel |
| C. Submit setelah perbaikan penuh | Skenario B ditambah: baseline XGBoost dan rule engine Tier-1 yang bisa dijalankan ulang, ledger overcharge per klaim dengan tarif acuan INA-CBG dan kode grup kasus, uji usability dengan n minimal 12 dan protokol tertulis, review klinis skenario, abrasi per-saluran dan eksperimen masking yang benar, artefak v2.1 lengkap (generator deterministik, manifest, checksum, split held-out), rotasi token Notion, rebuild dokumen proposal dari skrip repo dengan 7 gambar yang dikembalikan, field PAGE pada footer, penanda sitasi untuk 18 rujukan, dan abstrak, daftar singkatan, identitas bertanda tangan, serta bagian batasan eksplisit. | Novelty tetap menjadi kelemahan karena MHGSL sudah dipublikasikan (F-08); validasi klinis eksternal tidak mungkin selesai dalam 16 hari; pemeriksaan reseptif untuk 94,4 persen sindikat unseen akan sangat berat (F-20); risiko menumpuk jika dikerjakan serial. | Rendah, sekitar 25 persen | 8 sampai 12 hari kerja; hanya mungkin bila dikerjakan paralel 4 orang mulai 22 Oktober, dengan prioritas skenario B sebagai fallback |

Catatan: skenario B dan C memakai hasil yang sama, yaitu manifest dan pipeline. Yang membedakan adalah kedalaman baseline, ledger overcharge, uji multi-channel, dan studi usability. Bila harus memilih satu, pilih B, dan jadikan C sebagai daftar kerja lanjutan setelah submit. Skenario B wajib memuat koreksi hukum F-24 dan F-25 karena keduanya biaya rendah (perbaikan teks) dan dampak tinggi.

### 4.1 Status submit saat ini (checklist C1 sampai C20)

Checklist submit internal tim sudah ada di `10-competition.md:388-411` dengan 20 butir, tenggat, dan penanggung jawab. Tabel ini adalah pembacaan ulang checklist itu terhadap bukti aktual, bukan checklist baru. Hanya 3 dari 20 butir yang benar-benar siap.

| # | Artefak | Status aktual | Tenggat | Blocker |
|---|---|---|---|---|
| C1 | Manifest eksperimen (ID, dataset v2.1, seed 20260707, split GroupKFold+LOGO, fitur, threshold, file prediksi) | Tidak ada | 28 Okt | P0.3 |
| C2 | Skrip baseline (rule engine + XGBoost) yang bisa dijalankan ulang | Tidak ada | 28 Okt | Ya |
| C3 | Definisi label final (fraud-scenario, anomali, normal) | Tidak ada | 26 Okt | P0.1 |
| C4 | Penandaan versi 100-klaim versus 300-klaim; demo diarahkan ke 300 | Tidak ada | 25 Okt | P0.2 |
| C5 | Tabel SYND diregenerasi dari CSV (4 dari 9 baris salah pada pasien, 5 dari 9 pada skor) | Salah | 26 Okt | Ya |
| C6 | Metode tarif acuan dan kalkulasi overcharge per klaim | Tidak ada | 30 Okt | P0.4 |
| C7 | Rekonsiliasi angka proposal versus database riset, termasuk deadline | Tidak ada | 24 Okt | P0.5 |
| C8 | Paragraf posisi terhadap SmartClaim JKN, VPK, dan AAK | Tidak ada | 27 Okt | Paling kritik |
| C9 | Video demo 3 sampai 5 menit (voice-over, alur upcoding ke drilldown ke keputusan) | Tidak ada | 30 Okt | Ya |
| C10 | Deck presentasi maksimal 10 slide tanpa angka yang belum reproducible | Tidak ada | 31 Okt | Ya |
| C11 | Perbaikan URL clone di README dan tautan domain Vercel (hyphen = 404) | Repo publik, README masih salah | 25 Okt | Tidak |
| C12 | Link demo live yang stabil dan QR di slide, dengan label "data simulasi sintetis" | Ada, HTTP 200, 161.800 byte, diverifikasi 22 Okt 2026 | 28 Okt | Ya |
| C13 | Daftar berkas wajib Submit project akhir per Participant Guide | Belum diketahui, 403 untuk bot | 23 Okt | Paling urgent |
| C14 | Review klinis skenario | Tidak ada | 30 Okt | Tidak, tapi memperkuat |
| C15 | Akun portal Healthkathon (login, submit form, 2FA) | Tidak terverifikasi | 23 Okt | Ya |
| C16 | Bukti keaslian dan worksheet orisinalitas | Ada di arsip | 25 Okt | Ya |
| C17 | Naskah final yang menyebut Healthkathon dan kategori resmi | Revisi 0 hitungan "Healthkathon" | 30 Okt | Ya |
| C18 | Naskah final yang menghapus "Sindikat Kolusi Rujukan" dari klaim kategori | Belum | 26 Okt | Ya |
| C19 | Permintaan akses data dan mentoring ke BPJS lewat kanal coaching | Tidak ada | 30 Okt | Tidak, tapi nilai tinggi |
| C20 | Daftar sumber referensi yang benar-benar telah dibuka | Parsial | 31 Okt | Ya |

Tiga butir yang siap adalah C12 (demo live), C16 (bukti keaslian), dan sisanya masih menyisakan pekerjaan. C13 dan C15 adalah yang paling mengikat karena keduanya tenggat 23 Oktober, dua hari lagi, dan keduanya di luar kendali teknis. C8 juga diberi tanda paling kritik karena proposal tanpa posisi terhadap SmartClaim JKN, VPK, dan AAK akan terlihat seperti tidak memahami lanskap sistem yang berjalan.

### 4.2 Eksperimen minimum yang menghidupkan klaim

Audit graf (`06-graph-mhgsl.md:455-473`) sudah merancang 13 eksperimen minimum dengan protokol dan artefak wajib. Tabel ini adalah Version Ringkas, dipakai sebagai acuan teknis untuk skenario B dan C. Prasyarat yang berlaku untuk semua baris: hitung ulang adjacency per fold, scaler dan threshold di-fit hanya pada data train, dan simpan output ke berkas karena notebook sekarang menyimpan 0 karakter output.

| # | Eksperimen | Protokol inti | Artefak wajib | Klaim yang dihidupkan |
|---|---|---|---|---|
| E-01 | Benchmark out-of-fold yang benar | 5 kali repeated GroupKFold(5) by `pasien_id`, 10 run dengan seed 0 sampai 9, z-score dan theta di-fit pada train saja | `oof_predictions.csv`, `metrics_oof.json` | C-01, C-13 |
| E-02 | Split per-sindikat, yang benar untuk klaim sindikat | 9 fold, tiap fold menahan 1 sindikat, laporkan hit-rate sindikat yang belum pernah dilihat | `syndicate_holdout.csv` | C-04 |
| E-03 | Ablasi per-saluran | Empat konfigurasi: top-only, feat-only, sem-only, full-3-saluran, plus full tanpa-shared. A_homo bukan pengganti ablasi | `ablation_channels.csv` | C-21, C-10 |
| E-04 | Sensitivitas theta_feat | Sweep theta di {0,50, 0,65, 0,75, 0,85, 0,92, 0,95} di dalam fold, plot AUPRC terhadap theta, laporkan kurvanya | `theta_sensitivity.csv` | C-12 |
| E-05 | Eksperimen masking dan kamuflase | Mask X persen edge topologi dengan X di {0, 20, 40, 60}, pertahankan label, ukur degradasi AUPRC tiap model | `masking_results.csv` | C-05 |
| E-06 | LOGO(faskes) yang jujur | Jalankan LOGO(faskes) yang sudah ada, tetapi laporkan bahwa 94,4 persen kasus fraud berasal dari sindikat unseen | `logo_faskes.csv` | C-06 |
| E-07 | SHAP per-saluran yang valid | DeepExplainer pada logit dengan masker channel-group, verifikasi additivitas sum phi sama dengan logit dikurangi baseline dengan toleransi 1e-4 | `shap_per_channel.csv` | C-09 |
| E-08 | Reproduksi dataset publik | Jalankan pipeline yang sama pada dataset Healthcare Provider Fraud Detection (CC0) dari Kaggle | `public_benchmark.md` | C-01 |
| E-09 | Dasar tarif klaim keuangan | Angka Rp507.370.000 sudah rekonsiliasi dengan data, yang belum ada adalah tarif acuan INA-CBG per kode diagnosis dan kode grup kasus | `tariff_ledger.csv` | C-14 |
| E-10 | Verifikasi literatur Hong et al. 2024 | Baca full-text Heliyon DOI 10.1016/j.heliyon.2024.e30045, tetapkan tabel apa yang sama dan apa yang berbeda | `novelty_table.md` | C-16 |
| E-11 | Baseline relatif terhadap prevalensi | Setiap tabel wajib menampilkan AUPRC random-baseline 0,12 dan precision pada recall 0,9, dan ambang 0,85 dinyatakan sebagai titik Safari | `metrics_oof.json` | C-01, C-12 |
| E-12 | Benchmark throughput | Ukur klaim per detik pada 300, 30 ribu, dan 300 ribu klaim dengan sparse ops, bukan loop O(n kuadrat) Python | `throughput_benchmark.md` | C-06, C-19 |
| E-13 | Uji enrichment multi-channel | Untuk tiap kanal hitung pairs sindikat versus pairs acak dengan permutation test minimal 20.000 iterasi, plus densest-subgraph, max clique, dan komponen | `enrichment.json` | C-21 |

Eksperimen dengan rasio biaya terhadap dampak terbaik adalah E-03, E-11, E-13, dan E-04. Semuanya adalah pekerjaan harness kecil di atas data yang sudah ada, bukan riset baru. E-01 adalah yang paling mahal karena menuntut perbaikan harness secara menyeluruh, tetapi tanpa E-01 tidak ada satu pun metrik yang layak namanya. E-08 dan E-12 sebaiknya ditunda, karena keduanya butuh sumber data atau komputasi di luar jangkauan 16 hari.

### 4.3 Klaim yang paling pasti ditolak juri

Tabel overclaim dari `06-graph-mhgsl.md:425-451` memuat 21 klaim. Tabel ini mengambil yang paling merusak kalau dibiarkan di naskah, dengan bukti yang ada sekarang dan bukti yang dibutuhkan untuk menutupnya.

| # | Klaim | Bukti yang ada sekarang | Bukti yang dibutuhkan |
|---|---|---|---|
| C-01 | "Akurasi 93,0%, Presisi 94,12%, ROC-AUC 0,9825, AUPRC 0,9142, +28,6% versus XGBoost 0,71" | Nol. `12-archive-architecture.md:55` menyatakan metrik adaptasi literatur | Benchmark out-of-fold (E-01) plus baseline yang bisa dijalankan ulang (C2) |
| C-03 | "MHGSL AUPRC 0,91" ditampilkan sebagai hasil terukur di UI dan API | Tidak ada output notebook tersimpan; angka konstanta di `data.ts:264`, `comparison.tsx:377`, `backend/src/api/main.py:390` | Output eksperimen yang tersimpan di berkas |
| C-04 | "100% mendeteksi 9 pola sindikat terorganisir" | `cell 13:130-149` hit-rate in-sample, `cell 13:154` memakai `assert` sehingga hasil pasti lolos | Split per-sindikat (E-02) |
| C-05 | "Ketahanan kamuflase 89,4% pada tingkat masking rujukan 40%" | Tidak ada kode masking sama sekali | Eksperimen masking (E-05) |
| C-06 | "Memproses miliaran relasi antar-entitas" | Data hanya 300 klaim; `pipeline.py:270-275` membangun A_top dengan loop Python ganda | Benchmark throughput (E-12) |
| C-07 | "Tier-3 PyTorch Geometric HeteroData GCN" | `backend/src/models/mhgsl.py:15` memakai `GCNConv` homogen | Implementasi HeteroData, atau turunkan klaim ke GCN homogen |
| C-08 | "Nilai negatif W_top = -0,12 membuktikan saluran topologi direkayasa" | Bobot kanal lewat softmax dari bobot yang dipelajari, sehingga tidak mungkin negatif | Klaim ini dibuang; tidak ada eksperimen yang bisa menghidupkannya |
| C-09 | "SHAP Attribution Decomposition Engine" | Diimplementasikan sebagai `torch.norm` per kanal, tanpa additivitas terhadap logit | SHAP pada logit dengan masker kanal (E-07) |
| C-10 | "Deteksi Sindikat Fraud Ring: Sangat kuat, klaster padat" | "Subgraf padat" tidak terdefinisi di repo; densest-subgraph A_feat berisi 48 node tanpa satu pun kasus fraud | Definisi klaster dan uji enrichment (E-13) |
| C-11 | "Multi-Channel Attention Fusion" | Kedua dokumen menulis concat, tanpa mekanisme attention | Implementasi attention, atau turunkan ke "Multi-Channel Fusion" |
| C-12 | "Rasio fraud aktual 1% sampai 3%" | Data aktual 36 dari 300 = 12,0% | Koreksi naskah dan baseline acak 0,12 (E-11) |
| C-13 | "Keunggulan mutlak arsitektur MHGSL" | Tidak ada teorema, benchmark valid, maupun ablasi | E-01, E-03, E-11 |
| C-15 | "Penghematan ratusan miliar rupiah DJS setiap MSA" | Ekstrapolasi dari 300 klaim sintetis tanpa basis rate | Basis rate terverifikasi, atau hapus |
| C-16 | "MHGSL sebagai terobosan, state-of-the-art" | `12-archive-architecture.md:30` mengakui "diadaptasi dari" | Tabel novelty (E-10), atau posisikan sebagai adaptasi |
| C-17 | "Client-side MHGSL Inference" | `data-uploader.tsx:28-30` berkomentar "a simplified MHGSL-style fraud scoring demo" | Implementasi inferensi, atau turunkan ke "demo skoring" |
| C-19 | "Kecepatan 2 juta klaim per hari" | `pipeline.py:271-283` loop O(n kuadrat) Python | E-12 |
| C-21 | "Multi-channel lebih baik daripada satu kanal" | Tidak ada uji. A_sem tidak signifikan (p = 0,138) dan A_homo lebih buruk dari acak (p = 0,730) | E-03 dan E-13 |

---

## 5. Tabel Aksi 10 Teratas

| 1 | Bangun ulang dokumen proposal DOCX dari skrip repo, kembalikan 7 gambar, atau hapus seluruh entri Daftar Gambar, tambahkan field PAGE pada footer, dan dokumentasikan atau hilangkan jalur build kedua | Dev | `22-proposal-docx-audit.md:49-59,295-297` (F-39) | 8 jam | 24 Okt 2026 |
| 2 | Tambahkan kernel proposal yang hilang: abstrak, daftar singkatan, identitas bertanda tangan, protokol eksperimen ringkas, metode statistik, batasan eksplisit, dan penanda sitasi untuk 18 rujukan; atau pangkas daftar pustaka | Tim | `22-proposal-docx-audit.md:71-92,305-308` (F-40) | 8 jam | 26 Okt 2026 |
| 3 | Unduh Participant Guide secara manual (SharePoint 403 untuk bot) dan petakan daftar berkas wajib Submit project akhir; verifikasi akun portal Healthkathon termasuk 2FA | Tim | `10-competition.md:404,406,457` (C13, C15) | 2 jam | 23 Okt 2026 |
| 4 | Buang seluruh angka yang tidak reproducible dari naskah, deck, dan UI: 93,0%, 94,12%, 0,9825, 0,9142, 0,71, 89,4%, 10,6%, 45%, 3,2x, SUS 82,5, Rp507.370.000, dan Rp14,4 M; kualifikasi 93% sebagai akurasi leksikon sentimen (186 dari 200 uji); bila FPR 10,6% masih dipakai, wajib disebut bersamaan dengan presisi 56,25% pada ambang 0,14, dan tambahkan AUPRC acak 0,12 sebagai pembanding | Frontend + Tim | `10-competition.md:464`; `16-red-team.md:320`; `21-numbers-of-record.md:72-80` | 6 jam | 24 Okt 2026 |
| 5 | Hapus ground truth dari bundle: buang `gtSent`, `sentiment_gt`, `syndHit` dari `public/payload-aegis-jkn.json`, perbaiki `innerHTML` tanpa escaping seragam di `dashboard-aegis-jkn.html`, dan blokir 8 kolom terlarang di eksportir CSV | Dev | `09-security.md:309,319`; `16-red-team.md:61-62`; `08-frontend.md:217` | 4 jam | 25 Okt 2026 |
| 6 | Perbaiki rujukan hukum di corpus: judul resmi Permenkes 16/2019, hapus HL7 FHIR R4 dari dasar Permenkes 24/2022 dan arahkan ke Pasal 10 ayat (4) plus Permenkes 18/2022, koreksi Pasal 65 dan 66 menjadi 67 dan 68, "3x24 jam" ke Pasal 46 ayat (1), "Data Pribadi Spesifik" ke Pasal 4 ayat (2), dan tambahkan Pasal 34 sebagai deliverable DPIA | Tim | `11-compliance.md:413-417,431`; `05-evidence.md:126-127` | 5 jam | 25 Okt 2026 |
| 7 | Tulis definisi label final dengan satu fungsi ambang tunggal di satu file konfigurasi, kunci ambang 0,80 secara inklusif dengan kasus batas KLM115, dan hapus tiga skala ambang yang tersisa | Tim data | `04-data-quality.md:365,368`; `15-code-quality.md:25`; `19-consistency.md:554` | 6 jam | 26 Okt 2026 |
| 8 | Bangun pipeline evaluasi minimal: split GroupKFold pada `Pasien` plus LOGO pada `Faskes`, hitung adjacency dan scaler di dalam fold, seed 20260707, satu file prediksi held-out, satu skrip metrik, dan `experiments/manifest.json` per metrik yang dipublikasikan | ML | `10-competition.md:392-393,461`; `06-graph-mhgsl.md:329,376-400,457-461` | 12 jam | 28 Okt 2026 |
| 9 | Tulis `tests/test_leakage.py` dan `configs/leakage.yaml` yang benar-benar ada, jalankan, dan lampirkan log hijau; hapus tanda centang pada tabel yang file-nya tidak ada | ML | `15-code-quality.md:16,446`; `03-architecture.md:273-274`; `20-repo-artifact-integrity.md:90-91` | 4 jam | 28 Okt 2026 |
| 10 | Perbaiki angka dan kode yang tampil di layar: 240 rawat inap dan 60 jalan menjadi 189 dan 111, 8 dari 8 kontradiksi menjadi 12, 14 edge berlebih menjadi 13, Rp 3,53 M menjadi Rp 3,53 Miliar, 16 dari 16 menjadi proporsi sebenarnya, label 00,66 dan 93,90, insulin glargine di FORNAS, dan selisih 1000 kali pada `i18n.tsx:791` | Frontend + Tim | `18-ux.md:369`; `08-frontend.md:214-218`; `11-compliance.md:38-40,306,314,333`; `21-numbers-of-record.md:212` | 6 jam | 27 Okt 2026 |
| 11 | Buat video demo 3-5 menit (voice-over, alur upcoding sampai drilldown, keputusan), deck maksimal 10 slide tanpa angka yang belum reproducible, arahkan demo ke 300 klaim, perbaiki URL Vercel dan URL clone di README | Tim + Dev | `10-competition.md:400-403,463,467` (C9-C12, P0-7, P0-11) | 10 jam | 30 Okt 2026 |

---

## 6. Tabel Angka yang Wajib Dipantau

Kolom Status verifikasi memakai empat kategori: TERBUKTI (dicek ulang dengan skrip sendiri terhadap corpus atau API), TERVERIFIKASI (dicek dari sumber primer eksternal), TIDAK DIREPRODUSIBEL (sudah diuji dan gagal direproduksi), dan TANPA SUMBER (tidak ada artefak maupun sitasi). Tabel kanonik lengkap ada di `21-numbers-of-record.md` bagian 2 dan bagian 3.

| # | Angka yang diklaim | Nilai | Sumber di artefak publik | Status verifikasi | Tindakan |
|---|---|---|---|---|---|
| 1 | Akurasi model | 93,0% | PDF Colab p01, `oasis-data.ts:97`, `payload kpi.accuracy`, `00-dashboard.md:47` | TIDAK DIREPRODUSIBEL sebagai akurasi fraud; 93,0% = akurasi leksikon sentimen (186 dari 200 uji) dan deterministik dari bug substring ("lama" di "Pengalaman") | Ganti label menjadi "Akurasi leksikon sentimen (200 uji)" atau hapus dari KPI |
| 2 | Presisi | 94,12% | `00-dashboard.md:47`, `11-archive-proposal.md:15,30,327`, `14-index.md:490` | TIDAK DIREPRODUSIBEL; pencarian exhaustive atas 46 nilai unik `skor_fraud` menghasilkan nol ambang dengan presisi 94,12%. Terdekat 94,7368% di ambang 0,78, lalu 92,3077% di 0,74. Di ambang 0,80 presisi justru 100% dengan FPR 0% | Buang dari naskah, arsip, dan index |
| 3 | ROC-AUC | 0,9825 | `00-dashboard.md:47`, `11-archive-proposal.md:328` | TIDAK DIREPRODUSIBEL; AUC atas data aktif maksimum 1,000000 (kolom `Skor Fraud`, circular) | Buang |
| 4 | AUPRC | 0,9142 | `00-dashboard.md:47`, `11-archive-proposal.md:329` | TIDAK DIREPRODUSIBEL; nilai 0,9142 tidak ada di PDF Colab, notebook, payload, atau dataset, dan `04-evidence-matrix.md:34` menandainya belum tereproduksi | Buang; ganti dengan AUPRC hasil pipeline manifest (skenario B) |
| 5 | Baseline XGBoost AUPRC | 0,71 | `data.ts:253,261,264`, `backend/src/api/main.py:395`, `11-archive-proposal.md:338` | TIDAK DIREPRODUSIBEL; tidak ada skrip baseline, split, seed, atau file prediksi | Hilangkan baris baseline dari UI dan API, atau ganti dengan hasil run yang bisa direplikasi |
| 6 | Ketahanan masking | 89,4% | `11-archive-proposal.md:30,182,330`, `14-index.md:505` | TIDAK DIREPRODUSIBEL; nol kode masking di repo ML dan tidak ada definisi masking, proportion edge, atau protokol uji | Buang; bila sempat jalankan masking sweep di dalam fold |
| 7 | Penurunan waktu telaah | 45% | `11-archive-proposal.md:331,340`, `00-dashboard.md:49` | TIDAK DIREPRODUSIBEL; tidak ada load test, timing mentah, atau protokol. Naskah memakai 10-20 ke 3-5 menit, sedangkan PDF memakai 20 ke 3 menit yang setara 85 persen | Buang; pilih satu angka dan tempelkan load test |
| 8 | Throughput | 3,2x | `dokumen/section_bab_7_to_9.py:86,114`, `11-archive-proposal.md:333,350` | TIDAK DIREPRODUSIBEL; satu-satunya asal adalah skrip penghasil DOCX. 20 ke 3 menit adalah 6,667 kali, bukan 3,2 kali | Buang |
| 9 | Skor SUS | 82,5 | `dokumen/section_bab_7_to_9.py:88`, `11-archive-proposal.md:335,350` | TIDAK DIREPRODUSIBEL; tanpa jumlah responden, kuesioner, atau data mentah | Buang, atau jalankan studi usability dengan n minimal 12 dan lapor median |
| 10 | Total dataset | 300 klaim | `00-dashboard.md:29`, `01-proposal.md:9`, CSV corpus | TERBUKTI: 300 baris, KLM001-KLM300, ID tanpa celah | Pertahankan, dan tambahkan label "dataset simulasi, seed 20260707" |
| 11 | Total nominal klaim | Rp3,53 Miliar | `00-dashboard.md:35`, `01-proposal.md:66`, `dataset-explorer.tsx:764` | TERBUKTI: Rp3.526.650.000 (hitung ulang dari CSV). Perhatikan satuan UI salah tulis Rp 3,53 M (F-13) | Pertahankan; perbaiki satuan UI menjadi Miliar |
| 12 | Klaim fraud | 36 klaim | `01-proposal.md:37`, `00-dashboard.md:32-34` | TERBUKTI: 36 baris `Risiko=fraud`, `Status=escalate`, nilai Rp561.150.000, prevalensi 12,0 persen | Pertahankan sebagai "36 klaim dengan label fraud-scenario", bukan fraud terverifikasi |
| 13 | Klaim anomali | 60 klaim | `10-simulation-dataset.md:113`, `11-archive-proposal.md:348` | TERBUKTI: 60 baris non-auto_clear, nilai Rp841.100.000. Perhatikan 60 = 36 fraud + 14 high + 10 medium | Pertahankan dengan definisi eksplisit "36 + 14 + 10 = 60" |
| 14 | Penghematan overcharge | Rp507.370.000 | `11-archive-proposal.md:15,347-348`, `14-index.md:822-823` (Penyelamatan Riil) | TIDAK DIREPRODUSIBEL: 60,32 persen dari Rp841.100.000, tanpa tarif acuan, formula, atau ledger per klaim. Angka Rp8.456.167 per kasus adalah pembagian dengan 60, dan dikalikan 60 menghasilkan Rp507.370.020 | Buang dari naskah dan UI; sediakan ledger overcharge dengan tarif INA-CBG bila sempat |
| 15 | Penghematan bulanan dan tahunan | Rp1,2 M/bulan dan Rp14,4 M/tahun | `fraud-ring.tsx:415`, `i18n.tsx:443`, `roadmap.tsx:34` | TIDAK DIREPRODUSIBEL; `roadmap.tsx` menghitung 14,4 dari asumsi slider 20 ke 3 menit. Versi Inggris `i18n.tsx:791` menulis Rp 14,4 miliar, selisih 1000 kali | Ganti menjadi proyeksi berb_label "proyeksi berbasis asumsi" atau hapus |
| 16 | Tim terdaftar | 872 | `10-competition.md:72`, API `referensi/jumlahpeserta` | TERVERIFIKASI sebagai penghitung API live lintas kategori dengan rincian kategori 0/0/0; tidak boleh diklaim sebagai 872 tim di kategori Fasilitas Kesehatan | Jangan diklaim sebagai 872 tim kategori; bila perlu sebut "872 peserta terdaftar lintas kategori" |
| 17 | False positive rate | 10,6% | `11-archive-proposal.md:30,332`, `00-dashboard.md:48` | TIDAK DIREPRODUSIBEL sebagai pasangan metrik: angka 10,6 persen sendiri reachable di ambang 0,14 (FP 28 dari 264 negatif = 10,6061 persen), tetapi presisi pada ambang itu hanya 56,25 persen | Buang sebagai klaim; jika hanya FPR yang dipakai, tulis "10,61 persen pada ambang 0,14 di 300 klaim simulasi, presisi 56,25 persen" |
| 18 | Estimasi prevalensi fraud | 3-7% | `problem-section.tsx:97`, `12-archive-architecture.md:116` | TANPA SUMBER yang layak: berasal dari GAO-24-105833 (federal AS, non-kesehatan); sudah diberi label estimasi literatur | Pertahankan hanya sebagai estimasi literatur dengan nama sumber, jangan dipakai sebagai KPI |
| 19 | Deteksi fraud pada simulator | 14 dari 14 (100%) | `oasis-dashboard.tsx:546,697`, `payload kpi.det_rate` | TERBUKTI sebagai label by construction: himpunan fraud = ambang skor 0,80 pada 100 klaim generator FIXX | Ganti label menjadi deteksi by construction |
| 20 | Hit-rate sindikat | 100 persen (5 dari 5) | PDF Colab p01 dan p03, `payload syndHit` | TERBUKTI sebagai label by construction: seluruh 16 klaim sindikat sengaja masuk antrean 20, dan hit-rate dijaga `assert` di sel 13 | Sama seperti nomor 19 |
| 21 | Klaim kontradiksi | 8 dari 8 | `oasis-dashboard.tsx:721`, `oasis-data.ts:105` | SALAH: data 300 baris punya 12 klaim kontradiksi, dan flag tersebut adalah lookup dari `Modus` | Perbaiki menjadi 12 dan beri catatan bahwa flag berasal dari modus |
| 22 | Distribusi sentimen | 62 positif / 14 netral / 24 negatif | PDF Colab p01, `payload gtSent` | SALAH untuk dataset 300: 170 positif / 58 netral / 72 negatif. Angka PDF berlaku untuk 100 klaim generator FIXX | Perbaiki; dan pisahkan universe 100 klaim dari 300 klaim |
| 23 | Kapasitas verifikator | 6.667 berkas | `oasis-dashboard.tsx:345`, `oasis-data.ts:108`, PDF p01 dan p02, `payload kpi.capacity` | TERBUKTI sebagai turunan asumsi `round(1000*(20/3))`, bukan hasil pengukuran | Label "proyeksi asumsi 20 ke 3 menit per berkas" |
| 24 | Edge kanal fitur | 4.563 edge | `oasis-data.ts:98`, `oasis-dashboard.tsx:376`, PDF p01 | TERBUKTI sebagai 4.563 dari 4.950 pasangan pada eksperimen 100 klaim; pada 300 klaim hanya 2.192 edge dengan densitas 2,11 persen | Tampilkan Kepadatan edge, bukan edge dikonfirmasi, dan pisahkan kedua dataset |
| 25 | Antrean investigasi | 20 klaim | PDF p02, `payload queue` | TERBUKTI: `int(100*QUEUE_RATE)` dengan QUEUE_RATE 0,20 | Pertahankan; tambahkan subtitle "antrean 20 klaim dari eksekusi 100 klaim" |
| 26 | Distribusi layanan | 189 rawat inap / 111 rawat jalan | `notion-datasets.ts` (dump CSV corpus) | TERBUKTI dari hitung ulang CSV | Perbaiki UI yang menulis 240 rawat inap dan 60 jalan |
| 27 | Kerugian kasus KPK | Rp25 miliar | `13-archive-deep-research.md:3` | ANGKA SALAH: angka resmi hampir Rp35 miliar untuk 3 RS swasta | Koreksi menjadi Rp35 miliar dan tambahkan rujukan KPK primer |
| 28 | Volume klaim nasional | 2 juta per hari | `11-archive-proposal.md:22,128`, `data.ts:20` | TERVERIFIKASI (Kontan, 19 Sep 2025) | Pertahankan dengan sitasi; atau ganti dengan 650.000 berkas per hari plus 5 persen (Bloomberg Technoz, 11 Jun 2026) yang lebih baru |
| 29 | AI verifikasi BPJS | 650.000 berkas/hari, 5 persen terindikasi fraud | `10-competition.md:281,373` | TERVERIFIKASI (Dirjen TIK BPJS, Bloomberg Technoz, 11 Jun 2026) | Gunakan sebagai pembanding skala dan posisi terhadap sistem yang berjalan |
| 30 | Jumlah verifikator | 1.000 | `11-archive-proposal.md:22,128`, `data.ts:21` | SUMBER SIRKULAR: hanya repo sendiri yang menyebut angka ini | Turunkan jadi asumsi tim atau hapus |
| 31 | AUPRC dari kolom label | 1,0000 | `claims_v2_live.csv` kolom `Skor Fraud` | TERBUKTI: pemisahan kelas sempurna (fraud 0,80-0,95 dan non-fraud 0,04-0,79, tanpa tumpang tindih), sehingga AUPRC, ROC-AUC, dan akurasi di ambang 0,80 semuanya 1,0000 | Jadikan materi penjelasan pembulatan label, jangan pernah dipakai sebagai performa model |
| 32 | F1 terbaik fitur bersih | 0,3448 | 34 fitur cell 5 notebook, ambang tunggal | TERBUKTI: F1 terbaik 0,3448 pada `biaya_per_hari` lebih dari Rp4.950.000; inilah batas atas nyata fitur yang tidak bocor | Gunakan sebagai pembanding jujur saat melaporkan metrik pipeline baru |
| 33 | Prevalensi aktual dan baseline acak | 12,0 persen (36 dari 300) dan AUPRC acak 0,12 | `claims_v2_live.csv`; klaim 1-3 persen di `mhgsl-theory.md:191` | TERBUKTI: prevalensi aktual 12,0 persen, AUPRC model acak sama dengan prevalensi | Tulis setiap tabel metrik dengan baseline acak 0,12 dan koreksi klaim rasio 1-3 persen |
| 34 | Nominal sindikat | Rp542.560.000 versus Rp539.650.000 | `11-archive-proposal.md:348` versus hitung ulang CSV | BERTENTANGAN: selisih Rp2.910.000; nilai 542.560.000 tidak ada di CSV. Modus Upcoding juga berbeda, Rp127,68 juta versus Rp156.900.000 | Gunakan angka dari CSV, jangan dari arsip |
| 35 | Waktu telaah pada PDF | 20 ke 3 menit (85 persen) | PDF p01 dan p02 | BERTENTANGAN dengan naskah DOCX yang menyebut 10-20 ke 3-5 menit (45 persen) | Pilih satu sumber, tulis parameternya, hapus yang lain |
| 36 | PP 33/2026 sebagai aturan pelaksanaan UU PDP | ditetapkan 16 Juli 2026, berlaku 16 Januari 2027 | `11-compliance.md:43,398` | TERBUKTI melalui dua komentar hukum independen; laporan `11-compliance.md` sendiri menulis 15 Juli dan 15 Januari, jadi angka itu perlu dikoreksi | Koreksi tanggal di `11-compliance.md`, lalu cantumkan PP 33/2026 di proposal sebagai transisi kepatuhan |
| 37 | Label `Kontradiksi Narasi` | 12 klaim (TP 12, FP 0, FN 0, TN 288) | `13-text-channel.md:144-172` | TERBUKTI sebagai lookup dari `Modus`, bukan analisis narasi | Hapus klaim deteksi kontradiksi berbasis LLM, atau tulis eksplisit bahwa flag berasal dari modus |
| 38 | Teks unik pada 300 baris | 36 umpan balik, 40 narasi, 18 alasan | `13-text-channel.md:253-258` | TERBUKTI: 12,0 persen, 13,3 persen, dan 6,0 persen kelifecycle unik | Jangan klaim analisis teks pada data ini |
| 39 | Skala dan parameter model | 37.157 parameter untuk 300 baris, rasio 124 : 1 | `06-graph-mhgsl.md:261-264,490-492` | TERBUKTI dari hitung ulang definisi model | Sampaikan sebagai keterbatasan di naskah, bukan disembunyikan |
| 40 | Densitas kanal pada 300 klaim | A_top 7,63 persen, A_feat 2,11 persen, A_sem 11,17 persen, A_homo 13,85 persen | `06-graph-mhgsl.md:483-487` | TERBUKTI dari reproduksi sel 7; A_feat hanya 1.892 edge berarah | Hapus kata "klaster padat" dari naskah dan UI |

### 6.1 Tabel Angka-Angka PDF

Semua 16 halaman PDF `colab/Hasil simulasi dari 300 dataset notion.pdf` dibaca satu per satu. PDF tidak punya lapisan teks, jadi setiap halaman dibaca sebagai gambar render (`work22\21_pdf_p01.png` sampai `21_pdf_p16.png`). Angka berikut seluruhnya berasal dari generator FIXX (100 klaim, seed 20260707), bukan dari dataset 300 klaim.

| Halaman | Angka yang muncul | Arti dan status |
|---|---|---|
| p01 | 100 klaim sintetis, 20 pasien, 12 dokter, 6 FKRTL, seed 20260707, 300 langkah simulasi, 4 sampel LLM mistral-oasis 24b dengan fallback heuristik lokal, risiko 76 low / 4 medium / 6 high / 14 fraud, sentimen 62 positif / 14 negatif / 24 netral, gamma 0,10, theta_feat 0,85, edge fitur 4.563, deteksi 14 dari 14 = 100 persen pada antrean 20 klaim, prevalensi 14 persen oversampled, estimasi lapangan 3-7 persen, akurasi sentimen simulasi versus GT 93,0 persen (186 dari 200 klasifikasi), ROI HITL 20 ke 3 menit per berkas dengan kapasitas 6.667 berkas, hit-rate sindikat SYND-01 3/3 sampai SYND-05 2/2, kontradiksi 8 dari 8 klaim, kotak Protokol Validasi v2.1 SESUAI, dan URL ekspor Colab | Semua TERBUKTI sebagai reproduksi deterministik generator FIXX. Angka 300 di sini adalah jumlah langkah simulasi, bukan jumlah klaim. Akurasi 93 persen adalah akurasi leksikon sentimen (F-09), kapasitas 6.667 adalah turunan asumsi (F-29) |
| p02 | Antrean investigasi 20 klaim, 62 positif / 14 negatif / 24 netral, ROI 6.667, dan catatan nama berkas hasil ekspor | Akurasi 93 persen dan kapasitas 6.667 bukan metrik deteksi fraud; nama berkas pada PDF berbeda dari nama berkas aktual |
| p03 | Distribusi risiko per kanal 0,35 / 0,60 / 0,80, rumus `p_fused = p_graph + 0,10 * f_text * (1 - p_graph)`, `0_feat > 0,85`, dan hit-rate sindikat 100 persen lima kali | Dua skala ambang aktif berbeda antara PDF (0,35/0,60/0,80) dan UI (0,40/0,65/0,85),(Status by construction pada hit-rate) |
| p04 | 10 skor fused tertinggi: KLM003 0,955, KLM002 0,946, KLM005 0,946, KLM001 0,937, KLM004 0,937, KLM014 0,928, KLM012 0,892, KLM010 0,883, KLM011 0,874, KLM013 0,874 | Konsisten dengan dataset v1 100 klaim; bukan benchmark pada 300 baris |
| p05 | KLM021 0,680, KLM020 0,660, KLM019 0,620 | Skor generator, tanpa label ground truth independen; pada dataset 300 ketiganya berstatus review |
| p06 sampai p15 | Feed sosial KLM001 sampai KLM019, penanda Langkah ke-3 dari 300, dua baris beda GT Netral, 24 post Twitter dan 24 post Reddit | Feed statis 48 entri; tiap baris membawa `sentiment_gt` yang merupakan ground truth bocor (F-04), dan seluruh 48 entri berlabel heuristik-lokal |
| p16 | KLM019 tidak ada sinyal, kotak kejujuran (simulasi sintetis, prevalensi oversampled 14 persen, estimasi Laplacian 3-7 persen), instruksi ekspor dan integrasi | Kotak kejujuran sudah benar; namun angka utama di dalamnya masih salah label |

Yang tidak ada sama sekali di PDF: 0,9142, 0,9825, 0,71, 94,12 persen, 89,4 persen, 10,6 persen, 45 persen, 3,2 kali, 82,5, 507.370.000, 841.100.000, 8.456.167, 3,53 Miliar, 872, dan 300 klaim. Kesimpulannya tegas: PDF adalah sumber angka dashboard, sedangkan angka benchmark hanya hidup di naskah proposal dan index arsip, yang berarti hasil eksperimen benchmark tidak pernah disimpan di mana pun. Angka itu kemungkinan berasal dari satu eksekusi notebook yang tidak pernah diarsipkan, dan itu sendiri adalah temuan.

---

## 6.2 Audit Kepatuhan Regulasi

Audit regulasi memverifikasi isi naskah peraturan, bukan hanya keberadaan rujukannya. Empatteen sebutan regulasi diperiksa; 3 yang benar, 11 dengan masalah. Tabel ini meringkas temuan `11-compliance.md` bagian 1.2 dan 2.

| # | Sebutan di korpus | Nomor resmi | Nomor benar | Isi sesuai | Verdict |
|---|---|---|---|---|---|
| V-01 | "UU Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi" | UU 27/2022, ditetapkan 17 Okt 2022 | Ya | Ya | Tepat |
| V-02 | "UU Nomor 17 Tahun 2023 tentang Kesehatan" | UU 17/2023, berlaku 8 Agt 2023 | Ya | Ya | Tepat |
| V-03 | "Permenkes 16 Tahun 2019 tentang Pencegahan dan Penanganan Kecurangan serta Pengendalian Gratifikasi dalam Program Jaminan Kesehatan" | Permenkes 16/2019, berlaku 31 Jul 2019, judul resmi "...serta Pengenaan Sanksi Administrasi..." | Nomor dan tahun benar, judul salah | Tidak | Salah judul |
| V-04 | "Permenkes 24 Tahun 2022 tentang Rekam Medis" | Permenkes 24/2022, berlaku 31 Agt 2022 | Ya | Ya | Tepat |
| V-05 | "Dokumentasi SATUSEHAT terkait interoperabilitas klaim BPJS" | Bukan peraturan, dokumentasi teknis Kemenkes SATUSEHAT Platform v7.23 | Ya | Ya | Tepat sebagai rujukan teknis |
| V-06 | "Permenkes 24/2022 tentang Rekam Medis Elektronik, pertukaran data medis nasional menggunakan protokol HL7 FHIR R4" | Permenkes 24/2022 | Ya | Tidak ada dalam naskah | Salah isi |
| V-07 | "Permenkes 24/2022 mewajibkan RME; interoperabilitas nasional via SATUSEHAT memakai standar HL7 FHIR R4", status Terverifikasi | Permenkes 24/2022 | Ya | Tidak | Salah isi dan status keliru |
| V-08 | "Pasal 4 ayat (3) UU PDP untuk Data Pribadi Spesifik" | UU 27/2022 Pasal 4 | Ya | Ayat salah, yang benar ayat (2) | Salah ayat |
| V-09 | "Sanksi pidana 5 sampai 6 tahun dan denda miliaran (Pasal 65 dan 66)" | UU 27/2022 Pasal 67 dan 68 | Ya | Pasal salah | Salah pasal |
| V-10 | "Notifikasi kebocoran 3x24 jam" disematkan ke Pasal 4 ayat (2) | UU 27/2022 Pasal 46 ayat (1) | Ya | Pasal salah | Salah pasal |
| V-11 | "Prinsip UU PDP (Pasal 16)" | UU 27/2022 Pasal 16 | Ya | Ya | Tepat |
| V-12 | "Permenkes 26/2021" sebagai acuan tarif dan basis rule engine | Permenkes 26/2021, Pedoman INA-CBG | Ya | Ya | Tepat |
| V-13 | "Permenkes 3 Tahun 2023 tentang Standar Tarif Pelayanan Kesehatan" | Permenkes 3/2023, berlaku 9 Jan 2023 | Ya | Ya | Tepat |
| V-14 | "Permenkes 16/2019 ... serta Pengendalian Gratifikasi" di arsip dan index | Permenkes 16/2019 | Ya | Tidak | Salah judul |
| V-15 | "Salted SHA-256 pseudonymization", "de-identifikasi penuh data medis", "Kepatuhan Privasi Mutlak" | Tidak ada dasar regulasi untuk tokenisasi otomatis | Tidak berlaku | Tidak | Overclaim |
| V-16 | "Peraturan tentang Pelindungan Data Pribadi, rekam medis, dan pencegahan fraud JKN" tanpa nomor | Tidak ada | Tidak | Tidak | Gap dokumentasi |
| V-17 | "Formularium Nasional / FORNAS" sebagai acuan rule engine | Kepmenkes HK.01.07/MENKES/1199/2025, berlaku 1 Apr 2026, versi lama 2197/2023 sudah dicabut | Ya | Ya | Tepat, tapi nomor tidak disebut |
| V-18 | "Permenkes 22/2019" | Permenkes 22/2019, Jabatan Fungsional Asisten Penata Anestesi | Ya | Tidak diuji | Tidak dicantumkan |

Rekapitulasi hitungan dari `11-compliance.md:48-60`: dari 7 nomor regulasi berbeda yang dirujuk, 5 benar, 1 salah judul, 1 tanpa nomor. Empat kutipan pasal UU PDP salah ejaan. Dari 10 kode ICD-10 yang diperiksa, 6 tepat dan 4 tidak presisi, 0 salah kode. Dari 10 kode ICD-9-CM, 7 tepat dan 2 salah label, 0 salah kode. Dari 10 item FORNAS, 9 benar dan 1 salah. Empat item tidak dapat diverifikasi: status Permenkes 11/2017 di BPK, identitas Permenkes 33/2024, UU 13/2022 jo UU 1/2026, dan peraturan pengganti INA-CBG menuju iDRG.

Daftar regulasi yang wajib dicantumkan, dengan alasan konkret hubungannya dengan isi proposal, ada di `11-compliance.md:388-405` (R-01 sampai R-18). Delapan di antaranya tidak muncul di proposal saat ini: Permenkes 18/2022 sebagai dasar hukum sebenarnya SATUSEHAT, Kepmenkes 1199/2025, PP 28/2024, Permenkes 6/2026, Permenkes 3/2023, UU 13/2022 jo UU 1/2026, Peraturan BPJS 3/2024, dan Pasal 34 UU PDP. PP 71/2019 juga tidak dicantumkan, padahal rezim PSE itu mengikat karena hosting aplikasi demo berada di Vercel, yaitu di luar negeri.

Koreksi tanggal yang wajib disampaikan: PP 33/2026 ditetapkan dan diundangkan 16 Juli 2026 dengan masa berlaku 6 bulan menurut Pasal 225, sehingga berlaku 16 Januari 2027. Laporan `11-compliance.md` sendiri menulis 15 Juli dan 15 Januari, sehingga angka di sana perlu dikoreksi, dan dokumen ini memakai 16 Juli dan 16 Januari.

### 6.3 Angka hardcode di frontend tanpa artefak

Tabel dari `21-numbers-of-record.md:186-217`. Semua konstanta di bawah ditulis langsung di kode, bukan dibaca dari data. Kolom terakhir sengaja menandai angka yang bukan sekadar tidak terverifikasi, melainkan bertentangan dengan data yang sudah terverifikasi.

| Lokasi | Angka | Sifat | Artefak pendukung |
|---|---|---|---|
| `data.ts:253` | AUPRC XGBoost 0,71, GNN 0,78, Hybrid 0,85, MHGSL 0,91 | Tabel perbandingan | Tidak ada output eksperimen |
| `data.ts:259-264` | Bar chart AUPRC 0,58 / 0,62 / 0,71 / 0,78 / 0,85 / 0,91 | Grafik | Tidak ada, semua nilai karangan |
| `data.ts:274-289` | Radar 4 model, Precision 0,74-0,92, Recall 0,68-0,90, F1 0,71-0,91, AUPRC 0,71-0,91, Specificity 0,89-0,96 | Grafik | Tidak ada |
| `data.ts:295-300` | Tabel metrik 4 model termasuk ROC-AUC 0,83-0,95 | Tabel | Tidak ada |
| `data.ts:20` | "2.000.000+ klaim harian diproses" | Statistik sistem | Tidak ada sumber |
| `data.ts:21` | "Sekitar 1.000 verifikator manual" | Statistik sistem | Sumber sirkular, hanya repo sendiri |
| `data.ts:23`, `i18n.tsx:211,560` | "Lonjakan AUPRC 20% arsitektur hibrida" | Klaim performa | Tidak ada |
| `data.ts:101` | RS_A "Kelas B, 412 tempat tidur" | Profil faskes | Tidak ada, data bertentangan |
| `data.ts:104` | "00.66 INA-CBG Rp 58 juta" | Tarif | Tidak ada tabel tarif |
| `data.ts:105` | "44.13 INA-CBG Rp 3,2 juta" | Tarif | Tidak ada |
| `data.ts:127-136` | Bobot edge fitur 0,92 / 0,88 / 0,85 / 0,79 dan semantik 0,81 / 0,83 / 0,94 / 0,71 | Bobot graf | Tidak ada, bobot cell 5 berbeda |
| `data.ts:316,318` | "COS 0,92 / 0,88", "Rp 58 juta", "theta_feat = 0,8" | Narasi simulasi | Tidak ada |
| `data.ts:332-335` | "Probabilitas 0,94", kontribusi "semantik +41% / fitur +38% / topologi -12%" | Narasi SHAP | Tidak ada SHAP nyata di repo |
| `data.ts:391` | "20 menit" ke "3 menit" | Operasional | Tidak ada |
| `data.ts:392` | "1.000" ke "sekitar 6.700" kapasitas | Operasional | Tidak ada |
| `data.ts:418,438` | riskScore D01 0,94, "Rasio K29,7 ke PCI 100%", "+4,2 sigma", "4,2x peer" | Profil investigasi | Tidak ada, sigma dan 4,2x tanpa perhitungan |
| `data.ts:423` | "INA-CBG Rp 58 juta versus tarif gastritis Rp 3,2 juta" | Tarif | Tidak ada |
| `data.ts:435,437` | "2 klaim (SYND-01)" (aktual 3), "Rp 58.000.000" (aktual Rp 52.300.000) | Profil | Bertentangan dengan S2 |
| `data.ts:448,451,453,455,459,463,466` | RS_A riskScore 0,95, "19 klaim" (aktual 29), "78% tagihan PCI", "4,2x baseline", "+137% lonjakan", "8 klaim per bulan", "+3,8 sigma" | Profil dan linimasa | Tidak ada |
| `data.ts:481,492,494` | "COS rerata 0,89", "Rp 58.000.000", "LOS 3 hari" (aktual LOS 2) | Profil | Bertentangan dengan S2 |
| `data.ts:502-518` | featureEdges 4563, fraudClaimsV1 14, groundTruthSyndicates 5, socialPosts 48, syndicateHitRate 100, textContradictions 8 | Blok metrik | Sebagian terverifikasi untuk 100 klaim, salah untuk 300 klaim |
| `fraud-ring.tsx:275` | "14 edge berlebih" | Graf | Salah, graf simulasi punya 13 edge fraud-fraud dan 7 edge normal-normal |
| `fraud-ring.tsx:280` | "7 edge tersebar" | Graf | Tidak ada |
| `fraud-ring.tsx:415`, `i18n.tsx:443` | "Total penghematan estimasi Rp 1,2 juta per bulan, Rp 14,4 juta per tahun" | Finansial | Tidak ada artefak penghematan |
| `i18n.tsx:791` | "Total estimated savings Rp 1.2 B per month, Rp 14.4 B per year" | Finansial | Bertentangan dengan `i18n.tsx:443`, selisih 1000 kali karena penerjemahan satuan |
| `roadmap.tsx:34` | `useCountUp(14.4)` sehingga "Rp 14,4 juta" | Finansial | Sama dengan di atas |
| `i18n.tsx:211` | "+20%" | Performa | Tidak ada |
| `problem-section.tsx:88,97` | "sekitar 1.000" verifikator, "3-7%" prevalensi | Konteks | 3-7% adalah label literatur yang tidak dihitung |

Kesimpulan praktis: 24 grup angka ini sebaiknya diberi label eksplisit "ilustrasi" atau dihapus, bukan dipertahankan sebagai hasil model. Yang paling merusak adalah yang bertentangan dengan data yang sudah terverifikasi, karena itu menunjukkan angka itu tidak pernah dicek sama sekali.

### 6.4 Kualitas kanal teks dan spec gap

Kanal teks adalah salah satu dari tiga kontribusi arsitektur yang diklaim, sehingga paling perlu diperiksa. Cardinalitas string pada 300 baris (`13-text-channel.md:255-261`):

| Kolom | Non-kosong | Unik | Persen unik | Baris duplikat |
|---|---|---|---|---|
| Umpan Balik Pasien | 300 | 36 | 12,0% | 264 |
| Narasi Rekam Medis | 300 | 40 | 13,3% | 260 |
| Alasan Berobat | 300 | 18 | 6,0% | 282 |
| Rujukan | 300 | 188 | 62,7% | 112 |
| Catatan | 60 | 36 | 60,0% | 24 |

Tiga kolom pertama yang menjadi sumber analisis teks nyaris tidak berisi informasi unik. Dengan 18 string unik untuk 300 baris, analisis sentimen pada data ini tidak bisa lebih dari pencacah substring terhadap tabel. Itu menjelaskan mengapa akurasi leksikon 93,0 persen destruktif: kata "lama" cocok di "Pengalaman", "Pelayanan baik" cocok di banyak kalimat.

Dari 11 aspek spesifikasi kanal teks (`13-text-channel.md:385-399`), hanya 1 yang terdokumentasikan penuh, yaitu rumus fusion. Tujuh parsial, tiga tidak ada sama sekali: prosedur evaluasi, error handling, dan spesifikasi prompt. Yang paling merusak, `08-training-protocol.md` nol kali menyebut kanal teks, sehingga tidak ada prosedur evaluasi yang bisa diaudit. `configs/text.yaml` yang disebut sebagai toggle LLM juga tidak ada di disk. Dan tiga baris Umpan Balik, Narasi, serta Alasan adalah input eksternal yang menurut arsitektur dikirim ke LLM, tanpa satu pun kontrol prompt injection, klasifikasi data, atau PII egress.

Ada satu temuan yang layak ditambahkan di sini: 23 dari 36 klaim fraud (63,9 persen) punya sinyal teks negatif, sedangkan 13 dari 36 (36,1 persen) tidak punya sinyal teks negatif sama sekali. Artinya kanal teks, bahkan kalau sempurna, tidak bisa menjangkau lebih dari dua pertiga kasus fraud. Ini batas struktural data, bukan cacat implementasi, dan sebaiknya ditulis terbuka di naskah.


## 7. Metodologi Audit dan Batasan

1. Polling laporan dijalankan dengan interval 60 detik sampai tidak ada file baru selama 8 menit berturut-turut, pada elapsed 1445 detik, sesuai protokol. Log ada di `scripts\poll_log.txt`. Corpus akhir berisi 24 laporan, termasuk tiga laporan yang masuk pada tahap akhir: `11-compliance.md` (audit regulasi), `06-graph-mhgsl.md` (audit teori dan implementasi graf), dan `21-numbers-of-record.md` (tabel angka-of-record kanonik, 337 baris). Laporan dengan nomor 21 ada dua berkas, yaitu `21-colab-dashboard-provenance.md` dan `21-numbers-of-record.md`, dan satu laporan lagi bernomor 22, yaitu `22-proposal-docx-audit.md` yang mengaudit naskah DOCX yang benar-benar dikirim. Angka pada bagian 6 dan 6.1 merujuk `21-numbers-of-record.md` sebagai kanon, tanpa mengubah laporan itu.
2. Semua temuan bersumber dari 24 laporan yang sudah dibaca utuh, bukan hanya judul dan tabel severity. Temuan yang dilaporkan sama oleh beberapa laporan digabung ke satu F dengan seluruh sumber dicantumkan.
3. Klaim yang bisa diperiksa diulang dihitung ulang dengan skrip sendiri di `analysis\reports\scripts\` yang dijalankan dengan `python -I`, tanpa mengeksekusi skrip dari luar workspace. Hasil hitung ulang atas `analysis\corpus\claims_v2_live.csv`: 300 baris, total Rp3.526.650.000, risiko 240 low / 10 medium / 14 high / 36 fraud, status 240 auto_clear / 24 review / 36 escalate, Rp561.150.000 untuk 36 fraud, Rp841.100.000 untuk 60 non-auto_clear, 12 kontradiksi, sentimen 170 positif / 58 netral / 72 negatif, layanan 189 rawat inap / 111 rawat jalan, 40 pasien, 20 dokter, 10 faskes, 9 sindikat.
4. Identitas byte antarsumber diverifikasi lewat md5 dan sha256: `colab/payload-aegis-jkn.json`, `mechine-learning-deep-learning/colab/payload-aegis-jkn.json`, dan `Aegis-JKN/public/payload-aegis-jkn.json` identik (md5 `31cc9fe86f2c75d94cbec3860ffe8066`, sha256 `9c8cc58a697642e0199841b5045e2a829476e37740d7828e5777c478659af953`). `colab/dashboard-aegis-jkn.html` identik dengan `Aegis-JKN/public/dashboard-aegis-jkn.html` (md5 `61b5deec7d00e9faa864dbdd24dbd76d`, sha256 `a9803bc3316cb4526b03bca53569a896e24b09a7e5fb377238381316b95c6deb`).
5. Deadline dan angka peserta diambil dari API resmi Healthkathon `POST https://healthkathon.bpjs-kesehatan.go.id:8080/healthkathon/rest/referensi/siklus/list` pada 22 Oktober 2026. Pencarian internet untuk verifikasi regulasi memakai MCP SearXNG sesuai aturan proyek, dengan failover ke instance remote.
6. Koreksi terhadap laporan sumber: `11-compliance.md` menulis PP 33/2026 ditetapkan 15 Juli 2026 dan berlaku 15 Januari 2027. Dua komentar hukum independen yang diakses pada 22 Oktober 2026 menyebut peraturan itu ditetapkan dan diundangkan 16 Juli 2026 dengan masa berlaku 6 bulan (Pasal 225), sehingga berlaku 16 Januari 2027. Angka yang dipakai di dokumen ini adalah 16 Juli dan 16 Januari, dan `11-compliance.md` perlu dikoreksi.
7. Batasan: rubrik dan bobot penilaian resmi tidak ditemukan pada sumber publik yang dapat diakses, sehingga penilaian di bagian 3 memakai dimensi yang konsisten dengan pernyataan resmi BPJS dan dengan `10-competition.md`. Participant Guide tidak terbaca (403 untuk bot) sehingga daftar berkas wajib submit belum terverifikasi. Audit ini tidak melakukan review kode aplikasi secara statis menyeluruh, dan tidak memverifikasi klaim yang sepenuhnya berada di luar workspace.
8. Aturan editorial yang diterapkan pada dokumen ini: nol em-dash, hanya ASCII dan teks Indonesia normal, referensi sumber ditulis dengan nama berkas plus nomor baris atau heading, dan hanya berkas ini yang dibuat tanpa mengubah laporan lain.

---

## 8. Peta Sumber Temuan per Laporan

| Laporan | Temuan yang disumbangkan | Jumlah |
|---|---|---|
| `00-dashboard.md` | F-13 | 1 |
| `01-governance.md` | F-17 | 1 |
| `02-proposal.md` | F-01, F-03, F-12, F-17 | 4 |
| `03-architecture.md` | F-05, F-07, F-11, F-12, F-33 | 5 |
| `04-data-quality.md` | F-06, F-28, F-30 | 3 |
| `04-evidence-matrix.md` | F-08 | 1 |
| `05-evidence.md` | F-24, F-31, F-32 | 3 |
| `06-graph-mhgsl.md` | F-02, F-08, F-10, F-18, F-19, F-20, F-21, F-22, F-33 | 9 |
| `06-methodology.md` | F-06, F-33 | 2 |
| `06-research-notes.md` | F-08 | 1 |
| `07-generator.md` | F-15, F-16 | 2 |
| `08-frontend.md` | F-02, F-05, F-11, F-13, F-29, F-36 | 6 |
| `09-security.md` | F-04, F-13, F-35, F-36 | 4 |
| `10-competition.md` | F-03, F-30, F-31, F-34, F-38 | 5 |
| `11-archive-proposal.md` | F-17 | 1 |
| `11-compliance.md` | F-23, F-24, F-25, F-26 | 4 |
| `13-text-channel.md` | F-14, F-23, F-27 | 3 |
| `14-index.md` | F-17 | 1 |
| `14-language.md` | F-31, F-32 | 2 |
| `15-code-quality.md` | F-07, F-12, F-35 | 3 |
| `16-red-team.md` | F-01, F-02, F-03, F-05, F-07, F-08, F-09 | 7 |
| `17-roadmap.md` | F-03, F-19, F-34 | 3 |
| `18-ux.md` | F-13 | 1 |
| `19-consistency.md` | F-12, F-17, F-29, F-30 | 4 |
| `20-repo-artifact-integrity.md` | F-07, F-11, F-15, F-37 | 4 |
| `21-colab-dashboard-provenance.md` | F-01, F-04, F-09, F-10, F-30 | 5 |
| `21-numbers-of-record.md` | F-01, F-04, F-06, F-13, F-15, F-18, F-19, F-29 | 8 |
| `22-proposal-docx-audit.md` | F-01, F-03, F-15, F-19, F-24, F-29, F-30, F-31, F-32, F-33, F-39, F-40 | 12 |

---

## 9. Rekomendasi Akhir

Kerangka yang dipakai: kurangi klaim, tambah bukti. Sisa 16 hari tidak cukup untuk membangun pipeline analitik lengkap, memvalidasi ground truth secara klinis, dan menyiapkan demo yang meyakinkan sekaligus. Yang tersedia cukup untuk membuat proposal jujur, menambahkan satu pipeline evaluasi minimal yang bisa dijalankan ulang, dan menyiapkan submit yang lengkap secara administratif.

Tiga hal yang tidak boleh ditawar, apa pun skenario yang dipilih. Pertama, hapus ground truth dari bundle publik sebelum submit. Kedua, satukan definisi label di satu tempat dan kunci ambangnya. Ketiga, jangan pernah menyebut angka yang tidak punya artefak sebagai hasil, termasuk di arsip dan index.

Satu tambahan dari audit regulasi dan graf yang baru selesai: koreksi rujukan hukum adalah biaya terendah dengan dampak tertinggi di seluruh daftar, karena koreksi titel dan pasal hanya mengubah teks. Delapan kesalahan kutipan yang teridentifikasi pada `11-compliance.md` dapat diperbaiki dalam satu hari kerja, dan tidak ada satupun yang menuntut eksperimen baru. Sebaliknya, menguji Claims superiority multi-channel, membenahi evaluasi benchmark, dan menyiapkan ledger overcharge adalah pekerjaan berjam-jam yang tidak akan selesai, sehingga ketiganya sebaiknya dijawab dengan batasan eksplisit, bukan dengan usaha semaksimal mungkin.

Satu hal yang boleh ditunda: studi usability, ledger overcharge, baseline komparatif lengkap, dan eksperimen masking. Semuanya sebenarnya menambah nilai, tetapi semuanya bisa diganti dengan kalimat jujur yang menjelaskan keterbatasan, sedangkan tiga hal di atas tidak bisa diganti karena dampaknya fatal.
