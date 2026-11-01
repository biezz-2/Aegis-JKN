# Laporan Penilaian Kesiapan Kompetisi - Aegis-JKN untuk Healthkathon BPJS Kesehatan 2026

Tanggal audit: 22 Oktober 2026
Auditor: Konsultan kesiapan Healthkathon (mitra AIC)
Lingkup: `N:\HEALTHKATHON\analysis\corpus\` (21 dokumen + 4 berkas data), repositori `N:\HEALTHKATHON\Aegis-JKN\`, sumber publik.
Tanggal akses seluruh URL: 22 Oktober 2026.

---

## 1. Ringkasan Eksekutif

### 1.1 Skor kesiapan

**Skor kesiapan keseluruhan: 2,6 dari 5 (56%) - "belum layak demo day sebelum perbaikan bersifat wajib".**

Proposal revisi 1.0 (`01-proposal.md`) secara metodologis **jauh lebih aman dan kredibel** daripada draf arsip: ia menghapus klaim overclaim, mengakui batasan, dan memisahkan fakta dari rencana. Namun assessment ini menilai **kesiapan untuk menang**, bukan kualitas dokumen. Pada ukuran itu proposal gagal pada dua hal yang menentukan:

1. **Tidak ada pembeda dari sistem anti-fraud BPJS yang sudah ada.** Tidak ada pengakuan atas SmartClaim JKN, VPK, AAK, MedIDS, maupun AI verifikasi 650.000 berkas/hari yang sudah berjalan di BPJS. Ini kelemahan terbesar, dan juri BPJS akan langsung mengetahuinya.
2. **Belum ada satu pun artefak eksperimen yang dapat direproduksi**, padahal `00-dashboard.md` menandai lima butir P0 yang masih kosong. Grand Final hanya 16 hari lagi.

### 1.2 Tabel severity

| # | Temuan | Severity | Dampak |
|---|---|---|---|
| S1 | Nol pengakuan terhadap sistem anti-fraud BPJS yang sudah ada (SmartClaim JKN, VPK, AAK, MedIDS, AI 650k berkas/hari) | **Kritis** | Tuduhan "menciptakan ulang yang sudah ada"; differentiation collapse |
| S2 | Semua 5 butir P0 di `00-dashboard.md:58-63` masih unchecked, termasuk "Lampirkan manifest eksperimen dan skrip untuk seluruh metrik yang dipublikasikan" | **Kritis** | Tidak ada klaim performa yang boleh dipertahankan di Demo Day 7 Nov |
| S3 | Angka Rp507.370.000 dan 8 metrik lain draf lama **tidak dapat direproduksi** dari CSV (sudah dikonfirmasi dashboard, dibuktikan ulang di sini) | **Kritis** | Pelanggaran Standar Dokumen §7 aturan 6 dan 7 |
| S4 | Kategori Tidak Sejalan: klaim kategori menyebut "Sindikat Kolusi Rujukan" tetapi data **nol** sinyal kolusi rujukan (kata "kolusi" = 0 kemunculan) | **Kritis** | Kategori buram, klaim tidak didukung |
| S5 | Demo yang dideploy berjalan di **100 klaim** (`oasis-data.ts:89`, `det_rate: 100`), sedangkan proposal memakai 300 klaim v2.1 | **Tinggi** | Juri menemukan demo beda dengan proposal |
| S6 | Tabel SYND di `10-simulation-dataset.md:134-144`: **4 dari 9** baris salah pada pemetaan pasien, **5 dari 9** salah pada rentang skor, **1 dari 9** salah pada dokter; 2 baris fraud-tunggal salah pada faskes+dokter+pasien | **Tinggi** | Dokumen inti proposal salah |
| S7 | Angka KPK di `13-archive-deep-research.md:3` (Rp25 miliar) vs angka resmi Rp35 miliar | **Tinggi** | Factual error pada sumber primer |
| S8 | Dokumen "purwarupa" 7x, "sindikat" 52x, "kolusi" 18x di arsip vs "sindikat" 1x, "kolusi" 0x di revisi | **Sedang** | Terlihat sebagai pengosongan klaim, bukan perbaikan |
| S9 | Stale deadline 14 Sep di `dataset_research_live.json:378-381` **dan** artikel publik IDN Times (14 Agu 2026) | **Sedang** | Cacat dokumentasi lintas kanal |
| S10 | Tidak ada **video demo** maupun naskah presentasi di seluruh korpus. (Koreksi atas temuan awal: repo GitHub **sudah publik** - `github.com/biezz-2/Aegis-JKN`, HTTP 200, `private: false`, homepage `aegisjkn.vercel.app` - tetapi URL clone di README masih salah: `biezz-2/aegis-jkn-mhgsl` → **404**) | **Tinggi** | Persyaratan submit project akhir belum terpenuhi |

### 1.3 Skor per dimensi juri (skala 1–5)

| Dimensi | Skor | Dasar penilaian |
|---|---|---|
| Relevansi masalah | **4** | Masalah terdefinisi jelas; pendekatan problem-first sesuai arah-arah BPJS (Setiaji, IDN Times 14 Agu 2026). Skenario klinis upcoding dan phantom billing persis modus KPK. |
| Dampak | **2** | Dampak nyata secara potensial (beban verifikator, Rp35 miliar kasus KPK) tetapi **belum terukur**; semua angka dampak berstatus "belum boleh disebut hasil tervalidasi" (`00-dashboard.md:46-51`). |
| Novelty | **2** | Novelty **relatif terhadap BPJS** = rendah (lihat §6). Novelty **relatif terhadap peserta** = tinggi (graf heterogen + XAI). Karena juri adalah BPJS, skor efektifnya 2. |
| Bukti kerja | **3** | Kode aplikasi jalan dan live di aegisjkn.vercel.app (HTTP 200), 133 file ter-version, ada test. Tapi 0 manifest eksperimen, 0 skrip replikasi, dataset demo ≠ dataset proposal. |
| Kelayakan implementasi | **3** | Arsitektur 7-tier, human-in-the-loop, tata kelola PDP, rencana on-prem semua kuat dan realistis. Minus: nol uji dengan pengguna, nol validasi klinis, nol integrasi nyata. |
| Komunikasi | **3** | Revisi 1.0 ditulis jelas dan jujur; tapi kehilangan narasi/examples/analogi yang membuat proposal "bercerita" di depan juri non-teknis. |

---

## 2. Kriteria Penilaian Publik Healthkathon 2026

### 2.1 Status informasi: **rubrik, bobot, dan subkategori TIDAK ditemukan secara publik**

- Halaman resmi `https://healthkathon.bpjs-kesehatan.go.id/` diakses 22 Okt 2026: HTTP 200, tetapi seluruh konten dirender oleh JavaScript; teks yang terbaca hanya "Healthkathon 2026 BPJS Kesehatan".
- Bundle JS resmi `main.2f0e2e63f6591013.js` (2.125.592 byte, diakses 22 Okt 2026) **tidak memuat satu pun** string `rubrik`, `penilaian`, `juri`, `subkategori`, `hadiah`, `syarat`, `panduan`, `Efisiensi Risiko`, `Manipulasi diagnosis`, `upcoding`, `phantom`, `Grand Final`, `Participant Guide`, `webinar`, atau `coaching`. Hitungan nol untuk semua keyword.
- Semua endpoint `referensi/*/list` yang dicoba (kategori, subkategori, tantangan, rubrik, kriteria, nilai, hadiah, syarat, dokumen, provinsi, tema, juri, penilaian, artikel, faq, pedoman, konten, dan 12 nama lain) **mengembalikan HTTP 404** untuk GET maupun POST.
- `Participant Guide` (PDF di SharePoint) **HTTP 403 untuk bot** - dicatat sebagai **artefak primer tidak terbaca**, bukan isi yang diklaim.

**Kesimpulan eksplisit: bobot penilaian, rubrik juri, daftar hadiah, dan nomor subkategori resmi TIDAK ditemukan pada sumber publik yang dapat diakses.** Laporan ini tidak mengarangnya.

### 2.2 Yang terkonfirmasi publik

| Fakta | Sumber | Akses |
|---|---|---|
| Tema: "Detect Smarter, Protect JKN" | `11-archive-proposal.md:7`; IDN Times 14 Agu 2026 | 22 Okt 2026 |
| Satu tantangan: "Efisiensi Risiko pada Pelayanan Kesehatan Program JKN"; 3 kategori: Peserta, Fasilitas Kesehatan, Pemberi Kerja | IDN Times, "Healthkathon 2026: AI dan Data untuk JKN", idntimes.com | 22 Okt 2026 |
| Pendekatan "problem-first": peserta diminta memahami persoalan **sebelum** menentukan teknologi | IDN Times, kutipan Dirjen TIK BPJS Setiaji | 22 Okt 2026 |
| AI untuk "deteksi potensi fraud sejak dini", keputusan akhir tetap manusia | IDN Times, kutipan Setiaji | 22 Okt 2026 |
| Pendaftaran 14 Agustus – **14 September 2026** (informasi publik) | IDN Times 14 Agu 2026 | 22 Okt 2026 - **SALAH, lihat §7.1** |
| Healthkathon 2024: 1.183 tim (416 Security, 408 Innovation System, 359 AI) | detik.com, "BPJS Kesehatan Umumkan Pemenang Lomba Healthkathon 2024" | 22 Okt 2026 |
| Healthkathon 2025: pemenang diumumkan 29 Nov 2025 | CNN Indonesia, 30 Nov 2025 | 22 Okt 2026 |
| Seminar learning journey: BINUS 25 Sep 2026, Garuda Spark 8 Okt 2026, webinar 28 Agu 2026 | Koordinasi (tidak terverifikasi independen; lihat catatan) | - |
| Penghitung peserta live: `jmlpeserta: 872`, rincian kategori `inovasi:0, sekuriti:0, ai:0` | API `GET .../referensi/jumlahpeserta` | 22 Okt 2026 |

> Catatan tentang 872: endpoint mengembalikan rincian kategori **semua nol**, sehingga angka ini **tidak dapat diatribusikan ke kategori Fasilitas Kesehatan** dan merupakan penghitung lintas kategori/peserta. Jangan diklaim sebagai "872 tim di kategori kita".

### 2.3 Fallback: kriteria hackathon generik yang dipakai untuk penilaian

Karena rubrik resmi tidak tersedia, penilaian memakai lima kriteria standar yang dipakai juri hackathon dan konsisten dengan pernyataan resmi BPJS di atas:

1. **Relevansi masalah** - apakah menyentuh masalah nyata JKN.
2. **Novelty** - apakah ada di luar yang sudah ada (termasuk di BPJS sendiri).
3. **Bukti kerja** - apakah ada prototipe yang benar-benar jalan dan terukur.
4. **Dampak** - apakah ada estimasi dampak kredibel dengan asumsi terbuka.
5. **Kualitas presentasi** - apakah mudah dipahami juri non-teknis.

Kriteria 1–4 sudah diuraikan di §1.3 dan §3–§6. Kriteria 5 dibahas di §4.

---

## 3. Audit Kategori dan Kesesuaian Ruang Lingkup

### 3.1 Pemetaan kategori

Proposal mendaftarkan kategori sebagai berikut (hanya ada di arsip, `11-archive-proposal.md:3`):

> "Sistem Pengawasan Fasilitas Kesehatan (Pencegahan Upcoding, Unbundling, Phantom Billing, dan **Sindikat Kolusi Rujukan**)"

**Pemetaan ke taksonomi resmi (nomor subkategori diberikan oleh koordinator, bukan terverifikasi independen karena endpoint publik tidak tersedia - lihat §2.1):**
- **Efisiensi Risiko pada Fasilitas Kesehatan, subkategori #4** - Manipulasi diagnosis dan/atau tindakan (**upcoding**).
- **Efisiensi Risiko pada Fasilitas Kesehatan, subkategori #6** - **Phantom billing**.

Kedua subkategori inti **tercakakup** oleh MVP `01-proposal.md:32`. Yang **tidak tercakup** adalah dua butir sisanya:

| Butir kategori | Status di revisi | Bukti |
|---|---|---|
| Pencegahan Upcoding | **TERCAKUP**, prioritas utama | `01-proposal.md:32` |
| Phantom Billing | **TERCAKUP**, prioritas utama | `01-proposal.md:32` |
| Unbundling | **Skenario tambahan, belum prioritas** | `01-proposal.md:32` ("dapat dipakai sebagai skenario tambahan setelah aturan dan labelnya terdokumentasi") |
| **Sindikat Kolusi Rujukan** | **TIDAK DIDUKUNG DATA** | Lihat §3.3 |

### 3.2 Konsistensi klaim vs bukti (tabel inti)

| Klaim dalam proposal | Sumber klaim | Bukti aktual | Verdict |
|---|---|---|---|
| Dataset 300 klaim aktif | `01-proposal.md:9,37` | CSV 300 baris, 29 kolom | **TERBUKTI** |
| 240 auto-clear / 24 review / 36 escalate | `01-proposal.md:9,37` | CSV: 240/24/36 | **TERBUKTI** |
| Risiko 240 low / 10 medium / 14 high / 36 fraud | `01-proposal.md:37` | CSV: 240/10/14/36 | **TERBUKTI** |
| Total nominal Rp3.526.650.000 | `01-proposal.md:66` | CSV = 3.526.650.000 | **TERBUKTI** |
| auto_clear Rp2.685.550.000 / review Rp279.950.000 / escalate Rp561.150.000 | `01-proposal.md:67-69` | CSV identik | **TERBUKTI** |
| 10 faskes, 20 dokter, 40 pasien | `10-simulation-dataset.md:145-150` | CSV: RS_A–RS_J (10), D01–D20 (20), P01–P40 (40) | **TERBUKTI** |
| 9 sindikat = 36 klaim | `10-simulation-dataset.md:132-144` | CSV Sindikat: 9 nilai, 36 baris | **TERBUKTI (jumlah) / TIDAK (isi, lihat §3.4)** |
| Metrik performa (AUPRC 0,9142 dll.) | `01-proposal.md:70` (draf lama) | Tidak ada artefak | **TIDAK DIREPRODUSIBEL** |
| Estimasi penyelamatan Rp507.370.000 | `01-proposal.md:70` | Tidak derivable (lihat §7.2) | **TIDAK DIREPRODUSIBEL** |
| "Sindikat Kolusi Rujukan" sebagai kapabilitas | `11-archive-proposal.md:3` | Nol sinyal (lihat §3.3) | **TIDAK DIDUKUNG** |
| 5.1 "Entitas terkait dapat mencakup ... dan rujukan" | `01-proposal.md:37` | Field Rujukan ada, tapi tidak dipakai untuk inferensi kolusi | **MISLEADING** |

### 3.3 Audit rujukan: berapa banyak baris benar-benar punya rujukan, dan adakah pola rujukan mencurigakan?

Data: `N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv`, kolom `Rujukan` (300 baris).

**Klasifikasi field `Rujuan` (hasil rekomputasi, 22 Okt 2026):**

| Kelas | Jumlah baris | Keterangan |
|---|---|---|
| `kunjungan langsung (tanpa rujukan)` | **111** | 37% baris, tidak ada rantai rujukan sama sekali |
| Rujukan bernama (Puskesmas + kota) | **161** | tersebar ke **10 nama Puskesmas**; 28 baris lagi berformat `undefined · RJ-... · tanggal` (rujukan ada, sumbernya tidak dikenal). Perhitungan ini dilakukan ulang pada 22 Okt 2026 dengan pemisahan field `Rujukan` pada separator `·` (U+00B7) - bukan em-dash - sehingga angka terdahulu (189 baris / 11 puskesmas) dikoreksi. |
| `undefined` (tanpa nama puskesmas) | **28** | 9,3% baris; seluruhnya punya nomor rujukan + tanggal, jadi rujukan tetap ada, hanya sumbernya tidak dikenal |
| Kosong | 0 | - |

**Uji pola rujukan mencurigakan (sinyal kolusi):**

| Uji | Hasil | Interpretasi |
|---|---|---|
| Puskesmas yang mengarahkan klaim ke **>1 faskes** | **0 dari 10** - setiap Puskesmas terikat pada tepat 1 faskes (Tlogo Sehat→RS_G, Balik Sehat→RS_J, Sanur Sehat→RS_H, Musi Sehat→RS_I, Bahari Sehat→RS_E, Sehat Sentosa→RS_A, Cibinong Medika→RS_D, Sehat Medan→RS_C, Giri Sehat→RS_F, Harapan Ibu→RS_B) | **NOL** sinyal puskesmas "steer" |
| Dokter yang praktik di **>1 faskes** | **0 dari 20** | Tidak ada pola dokter lintas faskes |
| Pasien yang berklaim di **>1 faskes** | 16 dari 40; **8 di antaranya punya klaim berlabel fraud** (11 baris, Rp254.580.000) | Ada sinyal lemah: pasien faskes-lintas memang berklaim fraud, **tapi** 12 dari 24 pasien satu-faskes juga punya klaim fraud. **Tidak diskriminatif.** |
| Klaim `escalate` **tanpa** rujukan bernama | **11 dari 36** (30,6%) - semuanya berstatus `kunjungan langsung (tanpa rujukan)`, bukan rujukan bernama yang hilang | 30% kasus fraud tier-tinggi punya **tanpa rantai rujukan sama sekali** (KLM013-014, 106, 108, 115-120, 122) |
| Kata **"kolusi"** di seluruh CSV | **0 kemunculan** | Tidak ada satu pun artefak yang merepresentasikan kolusi |
| Kata "rujukan" | 113 kemunculan | Field ada, tapi isinya rujukan administratif, bukan bukti kolusi |
| Kata "sindikat" | 5 kemunculan | 4 baris (KLM001-003) menyebut "pola terorganisir (sindikat)" dalam kolom `Alasan`; sisanya label `Sindikat` SYND-01..09 |

**Vonis: klaim "Sindikat Kolusi Rujukan" TIDAK DIDUKUNG oleh data.** Yang benar-benar ada adalah **9 skenario modus per-faskes yang deterministik** - setiap sindikat terkunci pada satu faskes dan satu dokter (lihat §3.4). Yang paling mendekati "kolusi rujukan" hanyalah 11 baris `escalate` yang berstatus kunjungan langsung tanpa rantai rujukan - yang justru *bukan* bukti kolusi, melainkan pola faskes yang menerima pasien walk-in.

> **Implikasi ke juri**: seorang juri BPJS yang membuka CSV akan melihat kata "kolusi" nol kali, sementara "kolusi" muncul di judul kategori proposal. Ini self-inflicted wound. Perbaiki dalam revisi 1.1: hapus "Sindikat Kolusi Rujukan" dari klaim kategori, ganti dengan "Pola Anomali Terstruktur Multi-Klaim" yang dapat dibuktikan, dan jadikan deteksi kolusi rujukan sebagai **rencana fase 2 yang jujur**.

### 3.4 Tabel sindikat: dokumen vs CSV aktual

`10-simulation-dataset.md:134-144` vs `claims_v2_live.csv` (kolom `Sindikat`, `Modus`, `Faskes`, `Dokter`, `Pasien`, `Skor Fraud`):

| ID | Dokumen (10-simulation-dataset.md) | CSV aktual | Status |
|---|---|---|---|
| SYND-01 | Upcoding, RS_A, D01+D02, KLM001-003, P01-P03 | upcoding, RS_A, D01+D02, KLM001-003, P01-P03 | ✅ BENAR |
| SYND-02 | Phantom Billing, RS_C, D05, KLM004-006, P08-P10 | phantom_billing, RS_C, D05, KLM004-006, P08-P10 | ✅ BENAR |
| SYND-03 | Unbundling, RS_B, D07, KLM007-012, P12-P14, skor 0,84-0,87 | unbundling, RS_B, D07, KLM007-012, P12-P14, skor **0,85-0,87** | ⚠️ benar sebagian (skor meleset) |
| SYND-04 | Drug Diversion, RS_E, D09, KLM013-014, P16-P17 | drug_diversion, RS_E, D09, KLM013-014, P16-P17 | ✅ BENAR |
| SYND-05 | Cloning, RS_F, D08, KLM016-017, P19-P20, skor 0,78-0,79 | cloning, RS_F, D08, KLM016-017, P19-P20, skor 0,78-0,79 - **status `review`, bukan `escalate`** | ⚠️ benar sebagian |
| SYND-06 | Repeat Billing, RS_G, D13, KLM101-104, **P21-P24**, skor 0,85-0,90 | repeat_billing, RS_G, D13, KLM101-104, **P21-P22** (2 pasien), skor **0,89-0,92** | ❌ SALAH |
| SYND-07 | Iur Biaya, RS_H, D14, KLM105-108, **P25-P28**, skor 0,82-0,87 | iur_biaya, RS_H, D14, KLM105-108, **P23-P24**, skor 0,82-0,85 | ❌ SALAH |
| SYND-08 | Readmission Berulang, RS_I, D15, KLM109-114, **P29-P34**, skor 0,75-0,80 | readmission_berulang, RS_I, D15, KLM109-114, **P25-P26**, skor **0,86-0,89** | ❌ SALAH |
| SYND-09 | Excessive Usage, RS_J, **D16**, KLM115-120, **P35-P40**, skor 0,78-0,83 | excessive_usage, RS_J, **D19**, KLM115-120, **P27** saja (1 pasien), skor 0,80-0,84 | ❌ SALAH |
| - | **Biaya Markup**, KLM121, RS_A, D03, P04, ≥0.85 · **Drug Diversion**, KLM122, RS_E, D09, P18, ≥0.80 | **biaya_markup KLM121** = RS_G, D13, P29, skor 0,81 · **drug_diversion KLM122** = RS_H, D14, P30, skor 0,82 - faskes, dokter, dan pasien **semuanya berbeda** | ❌ SALAH (3 dari 3 kolom) |

**Rekap per-kolom** (dihitung ulang dengan pembandingan programmatic tabel `10-simulation-dataset.md:134-144` vs CSV, 22 Okt 2026):

| Kolom | Salah | Rincian |
|---|---|---|
| Pemetaan **pasien** | **4 dari 9** | SYND-06 (doc P21-P24 → CSV P21-P22), SYND-07 (P25-P28 → P23-P24), SYND-08 (P29-P34 → P25-P26), SYND-09 (P35-P40 → P27) |
| Pemetaan **dokter** | **1 dari 9** | SYND-09: doc D16 → CSV **D19** |
| Pemetaan **faskes** | **0 dari 9** | 9/9 benar |
| **Rentang skor** | **5 dari 9** | SYND-03 (0,84-0,87 → 0,85-0,87), SYND-06 (0,85-0,90 → 0,89-0,92), SYND-07 (0,82-0,87 → 0,82-0,85), SYND-08 (0,75-0,80 → **0,86-0,89**), SYND-09 (0,78-0,83 → 0,80-0,84) |
| **Modus** | **0 dari 9** | 9/9 benar |
| Rentang **ID klaim** | **0 dari 9** | 9/9 benar |

Dua baris "fraud tunggal" (KLM121, KLM122) juga salah pada 3 dari 3 kolom yang diperiksa (faskes, dokter, pasien) - lihat baris terakhir tabel di atas. Ini bukan detail kecil: Tabel 7.2 arsip dan tabel `10-simulation-dataset.md` adalah **artefak inti** yang akan ditunjukkan ke juri.

### 3.5 Verifikasi modus vs rupiah

| Modus | Jumlah baris | Nominal (CSV) |
|---|---|---|
| upcoding | 5 | Rp212.800.000 |
| phantom_billing | 3 | Rp134.250.000 |
| prolonged_stay | 4 | Rp127.400.000 |
| overbilling | 4 | Rp65.950.000 |
| iur_biaya | 4 | Rp63.880.000 |
| repeat_billing | 4 | Rp61.600.000 |
| unbundling | 6 | Rp52.800.000 |
| drug_diversion | 3 | Rp26.030.000 |
| biaya_markup | 1 | Rp27.500.000 |
| readmission_berulang | 6 | Rp25.290.000 |
| anomali_frekuensi | 12 | Rp15.800.000 |
| cloning | 2 | Rp14.900.000 |
| excessive_usage | 6 | Rp12.900.000 |
| **Total 60 baris anomali** | 60 | **Rp841.100.000** |

> Arsip `11-archive-proposal.md:348` menyebut "Phantom Billing Rp134,25 Juta, Upcoding Rp127,68 Juta" - **Upcoding salah** (CSV: Rp212.800.000). Total 36 klaim sindikat = Rp539.650.000 (CSV), arsip menulis "Rp 542,56 Juta" - **selisih Rp2.910.000**. Semua selisih ini berasal dari Tabel 7.2/§8.4 yang stale.

### 3.6 Verifikasi klaim demo terhadap data

`N:\HEALTHKATHON\Aegis-JKN\src\components\mhgsl\data.ts:448-451` mengklaim faskes RS_A punya "**19 klaim**" dan "**78%** tagihan bedah mahal berasal dari dokter D01 & D02 pada klaster sindikat SYND-01". Data aktual:

- RS_A = **29 baris** (bukan 19).
- Baris RS_A ≥ Rp10 juta = **13 baris**; **13 dari 13 (100%)** berasal dari D01/D02 (bukan 78%).
- SYND-01 di RS_A = **3 baris** Rp156.900.000, bukan "klaster sindikat" yang menyumbang Rp470.600.000.

Angka di UI **tidak cocok dengan data** dan akan dilakukan cross-check berbasis data oleh juri.

---

## 4. Perspektif Juri Non-Teknis BPJS

### 4.1 Kekuatan (terbaca sebagai "wow factor")

| # | Kekuatan | Mengapa ini terlihat kuat | Bukti |
|---|---|---|---|
| K1 | **Demo live dan bisa dibuka juri sekarang** | aegisjkn.vercel.app HTTP 200, panjang 161.800 byte (diukur ulang 22 Okt 2026), dimuat 8 Okt 2026 | Diverifikasi 22 Okt 2026 |
| K2 | **Visualisasi graf + drilldown per-klaim** | Tampilan "ini yang membedakan dari Excel" untuk juri non-teknis | `data.ts:237-242` (4 komponen: `multi-channel-graph.tsx`, `fraud-drilldown-modal.tsx`, `fraud-ring.tsx`, `data-uploader.tsx`) |
| K3 | **Cerita upcoding "gastritis ditagih PCI"** | Sangat konkret dan mudah diingat; secara medis masuk akal | CSV: KLM001-003, dx K29.7 + proc 00.66, Rp52.300.000, skor 0.93-0.95 |
| K4 | **Arah human-in-the-loop konsisten dengan messaging resmi BPJS** | Setiaji sendiri bilang "keputusan akhir tetap melibatkan pertimbangan manusia" | `01-proposal.md:13`; IDN Times 14 Agu 2026 |
| K5 | **Peta jalan 6 fase + kriteria selesai yang jelas** | Juri melihat langkah kerja yang terukur | `01-proposal.md:76-82` |
| K6 | **Kesimpulan "data sintetis" jujur dan di depan** | "Data simulasi dan tidak mewakili prevalensi atau kerugian aktual JKN" | `01-proposal.md:9` |
| K7 | **Bukti kerja nyata**: modularitas (Next.js 16), 133 file ter-version, git history bersih | Bukti kerja nyata, bukan mockup | README + git log (`f62b86d`, `232ce79`, `19c4110`, `28a773e`, `290d64e`) |
| K8 | **Perolehan bahasa "revisi 1.0" + Standar Dokumen §7** | Menunjukkan disiplin governance yang langka di hackathon | `00-dashboard.md:74-85` |

### 4.2 Kelemahan (red flags yang akan dibaca juri)

| # | Red flag | Persepsi juri | Bukti |
|---|---|---|---|
| R1 | **"Sindikat Kolusi Rujukan" tapi data tidak punya kolusi** | "Judulnya lebih besar dari isinya" | §3.3: "kolusi" = 0 |
| R2 | **Data sintetis 300 klaim, prevalensi 12%** | "Toy data; mana bukti di lapangan?" | `01-proposal.md:9,73`; `10-simulation-dataset.md:114-115` (v2 BELUM SESUAI, 10 kekurangan kritis) |
| R3 | **Angka 93,0% akurasi, AUPRC 0,9142, "Rp507 juta-saving"** | "Ini angka dari mana? Tidak ada lampiran." | `00-dashboard.md:46-51` |
| R4 | **Demo 100 klaim, proposal 300 klaim** | "Demo-nya beda dari proposal-nya." | `oasis-data.ts:89-92` (`total_claims:100`, `det_rate:100`, `accuracy:93` = **akurasi sentimen**, bukan klasifikasi klaim) |
| R5 | **Kata "purwarupa" 7x di proposal revisi** | "Ini masih purwarupa, bukan solusi" | `01-proposal.md` (7 kemunculan) |
| R6 | **Proposal 92 baris, tanpa tabel, tanpa kasus, tanpa analogi** | "Terlalu tipis untuk menjadi naskah presentasi" | `01-proposal.md` total 92 baris vs arsip 429 baris / 82KB |
| R7 | **Tidak menyebut sistem BPJS yang ada** | "BPJS sudah punya ini" | §6 |
| R8 | **"Aegis" branding tanpa Ultimate Differentiation** | "Nama keren, tapi apa bedanya?" | §6 |
| R9 | **Angka KPK Rp25 miliar (padahal Rp35 miliar)** | "Angka salah → sumber tidak dibaca." | `13-archive-deep-research.md:3` vs KPK/Metro TV/Tribun 25 Jul 2024 |
| R10 | **Angka 1.000 verifikator bersumber dari repo sendiri** | "Sirkular: dokumen yang mengutip dirinya sendiri." | `dataset_research_live.json:281-288` |
| R11 | **Tidak ada video demo maupun naskah presentasi; URL clone di README salah** | "Persyaratan submit final belum lengkap; orang pertama yang coba clone gagal." | Video/naskah: nol di seluruh korpus. Repo: **sudah publik** (`github.com/biezz-2/Aegis-JKN`, HTTP 200, push terakhir 21 Okt 2026 16:50 UTC) - tetapi `README.md:270` memberi `git clone https://github.com/biezz-2/aegis-jkn-mhgsl.git` yang **404 / repository not found**; yang benar `biezz-2/Aegis-JKN`. `aegis-jkn.vercel.app` (hyphen) juga **404**; yang hidup `aegisjkn.vercel.app` |
| R12 | **Kategori kompetisi masih di arsip saja, tidak di proposal revisi** | "Dokumen final yang di-submit tidak menyebut Healthkathon sama sekali." | "Healthkathon" = 0 kemunculan di `01-proposal.md` |

---

## 5. Risiko Tantangan Juri (klaim yang paling mungkin dikoreksi/dipertanyakan juri)

| # | Klaim berisiko | Alasan | Mitigasi wajib sebelum 1 Nov |
|---|---|---|---|
| K-1 | "**SmartClaim JKN sudah melakukan triase klaim berbasis AI**" | Fungsi identik dengan premis proposal; juri akan menyebut "ini fp yang sudah ada di BPJS" | Tulis 1 paragraf diferensiasi eksplisit di proposal: Aegis = **analisis relasional lintas-klaim lintas-faskes** (yang SmartClaim tidak lakukan), bukan deteksi per-klaim. Sebut SmartClaim sebagai **komplementer**, dan tegaskan: SmartClaim = clerical check per klaim, Aegis = jaringan. Verifikasi: RRI 3 Feb 2026; WASPADA; Radar Bali. |
| K-2 | "**AUPRC 0,9142 / akurasi 93,0% / +20% lonjakan**" | Tanpa manifest, split, seed, prediksi, ground truth → terlihat seperti fabrikasi. | Hapus dari semua materi presentasi, atau attach **manifest eksperimen** (ID, versi dataset, seed 20260707, skema split GroupKFold+LOGO, daftar fitur, threshold, file prediksi) sebagai lampiran. Status default: "hasil sementara". |
| K-3 | "**Menyelamatkan Rp507.370.000**" | Tidak ada tarif acuan, tidak ada formula, tidak reproducible per klaim | Buang dari slide. Ganti dengan: "Rp507 juta adalah **estimasi potensial** pada 300 klaim simulasi; belum dapat direproduksi per klaim." (rumusan yang sudah dipakai `01-proposal.md:70` dan `00-dashboard.md:39`) |
| K-4 | "**Efisiensi 45% waktu telaah, throughput 3,2x, SUS 82,5**" | Guna uji tidak ada, protokol tidak ada, partisipan tidak ada | Hapus. Ganti dengan target bertanda "akan diuji" + protokol yang didefinisikan (`01-proposal.md:74`) |
| K-5 | "**300 klaim tervalidasi klinis**" | Tidak ada review klinis; `00-dashboard.md:64` (P1) masih terbuka; `10-simulation-dataset.md:114-115` menyatakan dataset BELUM SESUAI | Ubah menjadi "300 klaim **sintetis terkonstruksi** dengan skenario klinis berbasis kode"; minta review klinis (P1) sebelum 1 Nov |
| K-6 | "**Sindikat Kolusi Rujukan**" | 0 bukti data (§3.3) | Hapus dari klaim kategori. Tulis ulang sebagai "9 pola anomali terstruktur multi-klaim" + rencanakan deteksi kolusi rujukan sebagai fase 2 |
| K-7 | "**Tidak ada acknowledgment atas sistem existing BPJS (Antrean Online, P-Care, SIPP, V-Claim)**" | Tidak ada satu pun acknowledgment | Tambahkan tabel posisi: apa yang sudah ada BPJS, apa yang belum, di mana Aegis mengisi. Ini justru **memperkuat** proposal |
| K-8 | "**Data sintetis tidak cukup untuk validasi lapangan**" | Validasi lapangan butuh data BPJS | Nyatakan terus terang bahwa ini **prototype untuk uji metode**, dan ajukan **kolaborasi akses data** sebagai langkah berikutnya - ini justru sinyal kematangan yang dewasa |
| K-9 | "**9 sindikat = 100% mendeteksi**" | Tabel 7.2 stale: 4/9 salah pada pasien, 5/9 salah pada skor (§3.4) | Regenerasi Tabel 7.2 langsung dari CSV (perintah tersedia), atau drop "9 pola" dan fokus 2 subkategori inti |
| K-10 | "**Nasional: ratusan miliar hingga triliunan**" | Eksapolasi dari 300 klaim sintetis; `05-decision-scope.md:63` melarang eksapolasi penghematan nasional | Hapus total. Ganti: "skala dampak akan dihitung bila data produksi tersedia" |
| K-11 | "**Branding 'Aegis'**" | Nama tanpa diferensiasi substansi | Satu kalimat diferensiasi di sampul: "bukan mendeteksi klaim mencurigakan, tetapi memetakan **jaringan**_Only satu kalimat. |

---

## 6. Analisis Diferensial terhadap Sistem Anti-Fraud BPJS yang Sudah Ada

**Ini kelemahan terbesar proposal dan tidak boleh diabaikan.** Sumber: pencarian SearXNG (22 Okt 2026) + pembacaan artikel primer.

### 6.1 Peta sistem yang sudah ada

| Sistem | Fungsi | Sumber | Akses |
|---|---|---|---|
| **SmartClaim JKN** | "Sistem verifikasi klaim berbasis AI yang membantu verifikator mempercepat proses verifikasi klaim JKN" - *clerical check / pemeriksaan administrative dasar* | RRI, 3 Feb 2026; WASPADA; Radar Bali | 22 Okt 2026 |
| **SISCA JKN** | Bedah AI untuk layanan; dilepas 3 Feb 2026 oleh Dirut Ghufron Mukti | RRI, 3 Feb 2026 | 22 Okt 2026 |
| **AI dalam fungsi kontrol klaim** | SETIAJI (Dirjen TIK BPJS): ±650.000 berkas klaim/hari dianalisis, **"kurang lebih 5% itu terindikasi fraud"**; modus termasuk pasien tidak datang tetap diklaim dan manipulasi diagnosis | Bloomberg Technoz, 11 Jun 2026 | 22 Okt 2026 |
| **VPK (Verifikasi Pasca Klaim) + AAK (Audit Administrasi Klaim)** | Lapisan verifikasi pasca-pembayaran dengan pemeriksaan detail dan konfirmasi lanjutan ke faskes dan peserta | CNN Indonesia, 25 Jul 2024; Kontan, 25 Jul 2024 | 22 Okt 2026 |
| **Tim PK-JKN** | Tim anti-fraud nasional/provinsi/kab-kota (Kemenkes, BPKP, KPK, BPJS); tugas deteksi, penyelesaian, monitoring, pelaporan | CNN Indonesia, 25 Jul 2024 | 22 Okt 2026 |
| **Permenkes 26/2021** | Tugas verifikator: verifikasi kelengkapan berkas dan kesesuaian diagnosis vs tindakan di resume medis | Kontan, 25 Jul 2024 | 22 Okt 2026 |
| **Tim PK-JKN gabungan** | Investigasi 3 RS (Sumut A: Rp1-3 M; Sumut B: Rp4-10 M; Jateng C: Rp20-30 M), hasil **audit klaim BPJS Kesehatan**; total 25.011 klaim fiktif | Kontan, 25 Jul 2024; Tribun (kutipan Juru Bicara KPK Pahala Mansur), 25 Jul 2024; Wahana News, 25 Jul 2024 | 22 Okt 2026 |

### 6.2 Verifikasi silang: modus KPK

Kasus KPK (Metro TV dan Tribun, 25 Jul 2024) mengonfirmasi **modus yang sama persis** dengan skenario Aegis:

- **Phantom billing** - "merekayasa seluruh dokumen pendukung klaim JKN" (Metro TV, 25 Jul 2024).
- **Upcoding / mark-up operasi katarak** - Tribun, 25 Jul 2024: "3.000 tagihan fiktif hingga mark-up operasi katarak".
- **Kolusi** - "kongkalikong dari pemilik rumah sakit hingga dokter-dokternya berkomplot melakukan klaim BPJS fiktif" (Metro TV).
- **Kerugian resmi: hampir Rp35 miliar** (bukan Rp25 miliar seperti tertulis di `13-archive-deep-research.md:3`).

Rincian resmi per rumah sakit (Kompas 26 Jul 2024 mengutip pernyataan Dinas Kesehatan setempat; Tribun 25 Jul 2024 mengutip Juru Bicara KPK Pahala Mansur):

| RS | Kerugian | Modus |
|---|---|---|
| RS A (Sumut) | Rp1-3 miliar | **phantom billing** |
| RS B (Sumut) | Rp4-10 miliar | hasil audit klaim BPJS Kesehatan |
| RS C (Jateng) | Rp20-30 miliar | **merekayasa seluruh dokumen pendukung klaim** |

Total: **25.011 klaim fiktif** (Juru Bicara KPK Tessa Mahardika, Wahana News 25 Jul 2024). **Artinya: proposal punya kasus validasi yang nyata dan bisa disandarkan - tinggal mengoreksi angkanya.** Ini peluang untuk impress, bukan sekadar risiko.

### 6.3 Penilaian diferensiasi (kasar tapi jujur)

| Dimensi | Yang sudah ada BPJS | Yang Aegis tawarkan | Nilai differensiasi |
|---|---|---|---|
| Skala & kecepatan | 650.000 berkas/hari, AI sudah terpasang | 300 klaim sintetis | **Tidak ada** - BPJS jauh lebih besar skalanya |
| Pemeriksaan per-klaim | SmartClaim JKN: clerical check otomatis | Rule engine Tier-1 | **Tidak ada** |
| Post-pembayaran | VPK + AAK + konfirmasi faskes/peserta | Di luar lingkup (`05-decision-scope.md:64`) | **Tidak ada** |
| Relasional lintas-klaim lintas-faskes | **Tidak ditemukan publik** | Inti MHGSL: graf heterogen 3 kanal | **Ini satu-satunya celah yang ada** |
| XAI per-kanal | Tidak ditemukan publik | SHAP multi-saluran + audit trail | **Celah yang mungkin** |
| Deteksi pola terstruktur/sindikat | Tersirat (5% terindikasi fraud) | 9 skenario modus | **Celah yang mungkin** |

### 6.4 Verdict dan rekomendasi

**Konsekuensi #1 (paling penting).** Saat ini cara baca juri atas proposal ini adalah: "kami membuat sistem deteksi fraud klaim JKN" - persis deskripsi SmartClaim JKN. Tanpa Statement Posisi, proposal **tidak punya alasan untuk menang**.

**Rekomendasi (wajib, masuk proposal revisi 1.1 sebagai sub-bagian baru, mis. §2.2 "Posisi terhadap Sistem Verifikasi yang Sudah Berjalan"):**

> *"Aegis-JKN bukan pengganti SmartClaim JKN, VPK, atau AAK. SmartClaim JKN melakukan pemeriksaan administratif per berkas; VPK dan AAK melakukan pemeriksaan pasca-pembayaran berbasis sampel. Yang belum dilayani adalah analisis **relasional lintas-klaim dan lintas-faskes**: pola yang terbentuk ketika banyak klaim, banyak dokter, dan banyak rujukan dianalisis bersama sebagai satu jaringan. Kontribusi Aegis-JKN adalah (1) graf heterogen multi-kanal sebagai cara menguji apakah nilai tambah relasional benar-benar ada, (2) penjelasan per-kanal yang dapat diuji, (3) protokol evaluasi anti-leakage yang dapat direplikasi. Modus yang menjadi target MVP (upcoding dan phantom billing) dipilih karena keduanya terbukti dalam kasus KPK 2024."*

**Konsekuensi #2 - hilangkan klaim "kami yang pertama".** Gunakan framing "pelengkap", dan jadikan "mengenal sistem yang sudah ada" sebagai **kelebihan**, bukan kelemahan: proposal sudah tahu lanskap existing. Juri menghargai proposal yang sudah mengenal sistem yang ada.

**Konsekuensi #3 - ubah demo agar terlihat Know-how.** Alur demo wajib menampilkan: "SmartClaim sudah jalan; Aegis melihat apa yang SmartClaim tidak bisa: klaim 003 dari puskesmas yang sama, dokter yang sama, 1 bulan lalu, Rp52,3 juta, dx gastritis, proc PCI." Itu momen yang membedakan.

**Bukti independen dari kompetitor di kategori yang sama.** Repo `github.com/NalarAI/nalar-core` (HTTP 200, diakses 22 Okt 2026) secara eksplisit **menolak mencantumkan angka rupiah** di tabel hasilnya, dengan alasan: "Angka rupiah sengaja tidak ditaruh di tabel ini. Ia bergeser empat puluh persen antar benih acak, jadi angka rupiah tidak boleh dikutip sendirian." Ini konfirmasi independen bahwa **nominal rupiah dari data sintetis memang tidak stabil** - sehingga temuan §7.2 (Rp507.370.000 tidak reproducible) bukan sekadar catatan pedantik, melainkan cacat metodologis nyata yang akan diakui juri teknis. Rekomendasi: adopsi kebijakan yang sama - tulis nominal sebagai "estimasi pada 300 klaim simulasi", sertakan seed, dan nyatakan rentang antar-seed.

---

## 7. Timeline dan Kesiapan Submit

### 7.1 Status Kompetisi per 22 Oktober 2026

Sumber: API resmi `POST https://healthkathon.bpjs-kesehatan.go.id:8080/healthkathon/rest/referensi/siklus/list` (diakses 22 Okt 2026; respons verbatim tersimpan di `N:\HEALTHKATHON\analysis\corpus\scripts\_hk_siklus.json`).

| Kode | Siklus | Mulai | Selesai | Aktif |
|---|---|---|---|---|
| 1 | Pendaftaran | 14 Agu 2026 | **11 Okt 2026** | 0 |
| 2 | Submit Proposal | 14 Agu 2026 | **11 Okt 2026** | 0 |
| 3 | Seleksi Proposal | 12 Okt 2026 | 18 Okt 2026 | 0 |
| 4 | **Submit project akhir** | **19 Okt 2026** | **1 Nov 2026** | **1 (aktif)** |
| 5 | Seleksi project akhir | 2 Nov 2026 | 4 Nov 2026 | 0 |
| 6 | **Coaching & Development** | **19 Okt 2026** | **30 Okt 2026** | **1 (aktif)** |
| 7 | **Demo day / Grand Final** | **7 Nov 2026** | - | 0 |
| 8 | Pengumuman Pemenan | - | - | 0 |

**Konsekuensi langsung:**

1. **Tidak ada roadmap yang boleh bilang "pendaftaran masih dibuka."** Pendaftaran dan submit proposal **sudah ditutup 11 Okt 2026** (aktif=0). Seleksi proposal **sudah selesai 18 Okt**. Tim ada di fase "Submit project akhir" sampai 1 Nov.
2. **Lima butir P0 di `00-dashboard.md:58-63` sekarang adalah blocker submit, bukan backlog:**
   - P0.1 Definisi label fraud-scenario/anomali/normal → **belum ada** (blokir: label ground truth untuk benchmark).
   - P0.2 Tandai 100-klaim vs 300-klaim → **belum ada** (blokir: demo & proposal harus menunjuk versi yang sama).
   - P0.3 Lampirkan manifest eksperimen + skrip → **belum ada** (blokir: tanpa ini tidak ada satu pun angka yang boleh tampil sebagai hasil).
   - P0.4 Tarif acuan + metode overcharge per klaim → **belum ada** (blokir: semua angka rupiah/estimasi-saving).
   - P0.5 Samakan angka operasional proposal vs database riset → **belum ada** (blokir: konsistensi dokumen submit).
3. **Hari ke-16 menuju Grand Final.** Demo Day 7 Nov 2026 = 16 hari dari hari ini. Skenario terburuk: tim masih menjalankan eksperimen *selama* masa final.
4. **Coachings 19–30 Okt adalah aset, bukan admin.** Fase ini persis untuk menutup P0.1–P0.5. Manfaatkan: ajukan review metodologi, review klinis skenario, dan review kelengkapan dokumen ke coach.
5. **Seminar yang sudah dilewati** (BINUS 25 Sep, Garuda Spark 8 Okt, webinar 28 Agu) - pastikan rekaman/replay diakses, karena rekaman sering memuat slide rubrik dan template.
6. **`Participant Guide` (PDF SharePoint) HTTP 403 untuk bot** - dicatat sebagai **artefak primer tidak terbaca**. Jika tim memiliki akses manual, **wajib** mengunduh dan mencocokkan daftar berkas submit project akhir.
7. **Cacat dokumentasi lintas kanal:** baris Notion `dataset_research_live.json:378-381` menyatakan "Pendaftaran 14 Agustus–14 September 2026 ... Pendaftaran sudah ditutup 14 Sep 2026" dengan status "Terverifikasi" - **SALAH** terhadap API resmi (sebenarnya 11 Okt). Galat yang sama muncul di **artikel publik IDN Times (14 Agu 2026)**, yang menulis "pendaftaran berlangsung 14 Agustus–14 September 2026" (diverifikasi ulang 22 Okt 2026), sehingga koreksi harus diambil ke kanal publik juga. Catatan: baris Notion itu mengutip **Liputan6** (`dataset_research_live.json:377`), bukan IDN Times - kedua kanal publik membawa tanggal yang sama. Ini persis butir P0.5 (`00-dashboard.md:63`).
8. **Angka 872 peserta** adalah penghitung API live lintas kategori; rincian kategori 0/0/0. Jangan diklaim sebagai 872 tim di kategori Fasilitas Kesehatan.

### 7.2 Verifikasi angka finansial

| Angka | Sumber dalam korpus | Status | Verifikasi |
|---|---|---|---|
| **2.000.000 klaim/hari** | `dataset_research_live.json:233-238` | "Terverifikasi" | **TERVERIFIKASI** - Kontan 19 Sep 2025 (https://keuangan.kontan.co.id/news/klaim-layanan-bpjs-kesehatan-tembus-2-juta-per-hari); juga dikonfirmasi mabur.co ("sekitar 2 juta transaksi layanan kesehatan" per hari) |
| **±1.000 verifikator** | `dataset_research_live.json:281-288` | "Sebagian Terverifikasi" | **SUMBER SIRKULAR** - source = `https://github.com/biezz-2/Aegis-JKN` (repo sendiri); catatan admits "belum ditemukan rilis resmi BPJS independen yang menyebut angka persis ini". **Jangan tampilkan sebagai fakta.** |
| Rasio 2.000:1 | README:27; `11-archive-proposal.md:22` | Turunan | Bergantung pada 1.000 verifikator → **ikut tidak terverifikasi** |
| **650.000 berkas/hari + 5% terindikasi fraud** | - | - | **TERVERIFIKASI** - Bloomberg Technoz 11 Jun 2026 (Dirjen TIK Setiaji). **Angka ini lebih baru dan lebih kuat dari 2 juta; pakai ini, bukan 2 juta.** |
| **Rp500 M/hari; Rp113,47 T/tahun** | `dataset_research_live.json:369-370` | "Perlu Verifikasi" | **TIDAK DAPAT DIVERIFIKASI** - sumber sekunder (Stabilitas; manajemen-pembiayaankesehatan.net) tanpa primer. Jangan tampilkan. |
| Prevalensi fraud 3–7% | `04-evidence-matrix.md:32` (E-05) | "Perlu verifikasi" | Jangan tampilkan sebagai statistik faktual |
| **Kerugian KPK: Rp35 miliar** | `13-archive-deep-research.md:3` menulis **Rp25 miliar** | - | **ANGKA SALAH.** Resmi: "hampir Rp35 miliar" (Metro TV & Tribun, 25 Jul 2024). Rincian per RS: Sumut A Rp1-3 M, Sumut B Rp4-10 M, Jateng C Rp20-30 M; 25.011 klaim fiktif. **Koreksi ke Rp35 miliar.** |
| **Rincian kerugian KPK per RS** | - | - | **TERVERIFIKASI** - RS A (Sumut) Rp1-3 M *phantom billing*; RS B (Sumut) Rp4-10 M hasil audit klaim BPJS; RS C (Jateng) Rp20-30 M *merekayasa dokumen pendukung klaim*; total **25.011 klaim fiktif**. Sumber: Kompas Regional 26 Jul 2024, Tribun 25 Jul 2024, Wahana News 25 Jul 2024 |
| **Rp507.370.000** | `11-archive-proposal.md:348`; `01-proposal.md:70` | "Belum dapat direproduksi" | **DIBUKTI TIDAK REPRODUSIBEL.** CSV: 29 kolom, **tidak ada kolom tarif acuan**. Tidak equal satu baris; tidak equal jumlah modus mana pun; **tidak dapat dibentuk sebagai subset-sum ≤4 baris** dari 60 baris anomali (Rp841.100.000). Match dengan `00-dashboard.md:39`. |
| Rp112.420.000 (overcharge review) | `11-archive-proposal.md:348` | - | Tidak reproducible (subset-sum ≤4 dari 24 baris review: gagal) |
| Rp394.950.000 (overcharge escalate) | `11-archive-proposal.md:348` | - | Tidak reproducible (subset-sum ≤4 dari 36 baris escalate: gagal) |
| Rp841.100.000 (60 anomali) | `11-archive-proposal.md:348` | - | **TERBUKTI** - CSV: 60 baris, Rp841.100.000 ✓ |
| Upcoding Rp127,68 Juta | `11-archive-proposal.md:348` | - | **SALAH** - CSV: Rp212.800.000 |
| Sindikat Rp542,56 Juta | `11-archive-proposal.md:348` | - | **SALAH** - CSV: Rp539.650.000 (selisih Rp2.910.000) |
| Separabilitas 0,086 / 0,591 / 0,869 | `11-archive-proposal.md:337` | - | **TERBUKTI** - rata-rata `Skor Fraud` CSV: auto_clear 0,0862 / review 0,5908 / escalate 0,8689 ✓ (satu-satunya metrik draf lama yang cocok) |
| 264 klaim normal (88%) | `11-archive-proposal.md:321` | - | **SALAH** - CSV: 240 auto_clear (80%), 24 review (8%), 36 escalate (12%) |
| "Ratusan miliar hingga triliunan/tahun" | `11-archive-proposal.md:348` | - | **DILARANG** oleh `05-decision-scope.md:63` |

### 7.3 Checklist submit: apa yang harus ADA hari ini (22 Okt 2026)

| # | Artefak | Status | Owner | Deadline | Blocker? |
|---|---|---|---|---|---|
| C1 | Manifest eksperimen (ID, dataset v2.1, seed 20260707, split GroupKFold+LOGO, fitur, threshold, file prediksi) | ❌ tidak ada | ML | **28 Okt** | **YA - P0.3** |
| C2 | Skrip baseline (rule engine + XGBoost) yang bisa dijalankan ulang | ❌ tidak ada | ML | 28 Okt | YA |
| C3 | Definisi label final (fraud-scenario / anomali / normal) | ❌ tidak ada | Tim | **26 Okt** | **YA - P0.1** |
| C4 | Penandaan versi 100-klaim vs 300-klaim; demo diarahkan ke 300 | ❌ tidak ada | Tim | 25 Okt | YA - P0.2 |
| C5 | Tabel SYND di-regenerate dari CSV (4/9 baris salah pada pasien, 5/9 pada skor) | ❌ salah | Tim | 26 Okt | YA |
| C6 | Metode tarif acuan + kalkulasi overcharge per klaim | ❌ tidak ada | Tim | 30 Okt | YA - P0.4 |
| C7 | Rekonsiliasi angka proposal vs database riset (termasuk deadline 11 Okt) | ❌ tidak ada | Tim | 24 Okt | YA - P0.5 |
| C8 | Paragraf posisi terhadap SmartClaim JKN / VPK / AAK | ❌ tidak ada | Tim | 27 Okt | **YA (paling kritik)** |
| C9 | Video demo 3–5 menit (voice-over, alur upcoding→drilldown→SHAP→keputusan) | ❌ tidak ada | Tim | 30 Okt | YA |
| C10 | Deck presentasi (maks 10 slide) dengan **tanpa** angka yang belum reproducible | ❌ tidak ada | Tim | 31 Okt | YA |
| C11 | Perbaiki **URL clone di README** (`biezz-2/aegis-jkn-mhgsl` → `biezz-2/Aegis-JKN`, keduanya lowercase e-biru) dan tautan `aegis-jkn.vercel.app` → `aegisjkn.vercel.app` (hyphen = 404) | ⚠️ repo sudah publik, README masih salah | Dev | 25 Okt | YA |
| C12 | Link demo live yang stabil + QR di slide, dengan label **"data simulasi sintetis"** | ✅ ada (aegisjkn.vercel.app, HTTP 200, 161.800 byte, diverifikasi 22 Okt 2026) | Dev | 28 Okt | YA |
| C13 | Daftar berkas wajib "Submit project akhir" per Participant Guide (403 → unduh manual) | ❌ belum diketahui | Tim | **23 Okt** | **YA - paling urgent** |
| C14 | Review klinis skenario (P1 `00-dashboard.md:64`) | ❌ tidak ada | Tim | 30 Okt | Tidak, tapi memperkuat |
| C15 | Akun portal Healthkathon (login, submit form, 2FA) | ❓ tidak terverifikasi | Tim | **23 Okt** | **YA** |
| C16 | Bukti keaslian &/worksheet orisinalitas (arsip L10-19 sudah ada - pastikan sesuai form final) | ✅ ada di arsip | Tim | 25 Okt | YA |
| C17 | Naskah proposal final yang menyebut **Healthkathon** dan kategori resmi + subkategori #4/#6 | ❌ proposal revisi 0 hitungan "Healthkathon" | Tim | 30 Okt | YA |
| C18 | Naskah proposal final yang menghapus "Sindikat Kolusi Rujukan" dari klaim kategori | ❌ belum | Tim | 26 Okt | YA |
| C19 | Permintaan akses data/mentoring ke BPJS (lewat kanal coaching) | ❌ tidak ada | Tim | 30 Okt | Tidak, tapi nilai tinggi |
| C20 | Daftar sumber referensi yang benar-benar telah dibuka (§9 Gerbang Publikasi `04-evidence-matrix.md:78-85`) | ⚠️ parsial | Tim | 31 Okt | YA |

---

## 8. Apa yang Hilang Saat Revisi, dan Rekomendasi Restore

Revisi 1.0 memangkas `11-archive-proposal.md` (429 baris / 82KB) menjadi 92 baris. Yang hilang banyak, tapi sebagian hilang memang benar (overclaim). Yang hilang **mengandung nilai argumentatif**.

| # | Yang hilang | Lokasi arsip | Nilai untuk juri | Rekomendasi |
|---|---|---|---|---|
| A1 | **Empat ilustrasi klinis upcoding/phantom/unbundling** | `11-archive-proposal.md:130-135` | Tinggi - konkret, medis, instantly credible | **RESTORE** dalam 1 paragraf + tabel ringkas |
| A2 | **Konsep "Topological Camouflage"** | `:136-138` | Tinggi - ini *thesis* pembeda dari SmartClaim | **RESTORE** (dengan bukti, bukan klaim) |
| A3 | **Analisis 5-Whys (Tabel 2.1)** | `:151-158` | Sedang - menunjukkan proses "mengapa" yang matang | RESTORE ringkas (5 baris) |
| A4 | **Fishbone 4 dimensi (Tabel 2.2)** | `:159-165` | Sedang | Condense ke 4 butir |
| A5 | **Thesis "kecurangan terorganisir = masalah jaringan, bukan masalah baris data"** | `:166` | **Sangat tinggi** - ini kalimat yang membedakan dari SmartClaim | **RESTORE sebagai kalimat pembuka abstrak** |
| A6 | **Tabel 3.1 perbandingan 5 pendekatan × 7 sumbu** | `:177-186` | **Tinggi** - ini yang paling effective bagi juri non-teknis | **RESTORE**, TAPI perbaiki baris "Aegis 89,4% akurasi" → "target" |
| A7 | **Aturan Tier-1 deterministik (4 aturan)** | `:198-203` | Tinggi - menunjukkan engineering discipline | RESTORE |
| A8 | **Formulasi graf & bobot kanal** | `:207-220` | Sedang (juri teknis = nilai tambah besar) | RESTORE ringkas |
| A9 | **Matriks UU PDP Pasal 16 (6 prinsip)** | `:244-252` | Tinggi - kepatuhan regulasi = lebih dari sekadar "aman" | RESTORE sebagai tabel |
| A10 | **De-identification 18 identifier + salted SHA-256 + HSM** | `:253-254` | Tinggi | RESTORE |
| A11 | **Matriks AI vs Verifikator + Safe-Mode (override >30%/24h) + anti alert-fatigue** | `:270-288` | **Sangat tinggi** - tie langsung ke pendekatan resmi BPJS | **RESTORE** (Safe-Mode =wow factor) |
| A12 | **9 katalog sindikat (Tabel 7.2)** | `:293-304` | Tinggi **jika diperbaiki** | **REGENERATE dari CSV, bukan restore** |
| A13 | **Katalog 9 + tabel scope in/out** | `:311-319` | Sedang | RESTORE tabel in/out scope |
| A14 | **Tabel 8.1 KPI 4 dimensi (Target vs Capaian)** | `:323-336` | **Sangat tinggi** - pemisahan target/capaian adalah *persis* yang juri cari | **RESTORE dengan kolom Capaian dikosongkan** |
| A15 | **Economic portfolio Tabel 8.2** | `:341-347` | Sedang | RESTORE **tanpa** kolom "Penyelamatan Riil"; ganti "Overcharge Terbukti" → "overcharge estimasi (belum reproducible)" |
| A16 | **Struktur biaya & Cost-to-Impact 1:15** | `:362-363` | Sedang | RESTORE sebagai target |
| A17 | **Matriks risiko 12 baris + Protokol tanggap darurat** | `:371-388` | Sedang | RESTORE ringkas (tabel 12 baris terlalu panjang) |
| A18 | **Roadmap Stage-Gate 7 tahap / 12 bulan + Gate 1-3** | `:391-404` | **Tinggi** - gate criteria = "problem-first" | RESTORE tabel gate (3 baris) |
| A19 | **Struktur tim & peran** | `:364-368` | Sedang | RESTORE |
| A20 | **Lembar Pernyataan Orisinalitas** | `:10-19` | **Wajib** | RESTORE - ini berkas formulir |
| A21 | **Komitmen bab 12.1 "Detect Smarter, Protect JKN"** | `:406-411` | Sedang | Restore sebagai penutup |
| A22 | **"300 klaim tervalidasi klinis"** | `:410` | - | **JANGAN RESTORE** - overclaim |
| A23 | **"ratusan miliar hingga triliunan"** | `:348` | - | **JANGAN RESTORE** |
| A24 | **"membuktikan keunggulan mutlak"** | `:337` | - | **JANGAN RESTORE** |
| A25 | **"100% mendeteksi 9 pola sindikat"** | `:337` | - | **JANGAN RESTORE** |

**Kaidah restore** (dari `00-dashboard.md:84`, Standar Dokumen §7 aturan 9 - "Revisi tidak menghapus konten sumber yang masih diperlukan sebagai rekam jejak"): restore **nilai argumentatif**, buang **nilai klaim**. Praktisnya: semua tabel arsip kembali, tapi setiap angka Claims jadi "Target/rencana" atau diberi status "belum tervalidasi".

---

## 9. Rekomendasi Prioritas

### P0 - wajib selesai sebelum 1 Nov 2026 (blocker submit)

| # | Aksi | Sumber masalah | Output |
|---|---|---|---|
| P0-1 | **Unduh Participant Guide secara manual** (SharePoint 403 untuk bot), petakan daftar berkas wajib "Submit project akhir" | §7.1.6 | Checklist C13 terisi |
| P0-2 | **Tulis §2.2 baru: "Posisi terhadap Sistem Verifikasi yang Sudah Berjalan"** - SmartClaim JKN, VPK, AAK, AI 650k/hari & 5%, Tim PK-JKN, Permenkes 26/2021, plus 1 kalimat diferensiasi relasional | §6, C8 | Paragraf + tabel posisi |
| P0-3 | **Hapus "Sindikat Kolusi Rujukan" dari klaim kategori**; ganti "Pola Anomali Terstruktur Multi-Klaim" | §3.3, C18 | Kategori di proposal revisi 1.1 |
| P0-4 | **Regenerasi Tabel SYND dari CSV** (4/9 baris salah pada pasien, 5/9 pada skor) dan jalankan 1 skrip yang menghasilkannya | §3.4, C5 | Tabel 7.2 baru |
| P0-5 | **Buat manifest eksperimen + skrip baseline yang bisa dijalankan ulang** (rule engine + XGBoost, GroupKFold + LOGO, seed 20260707) | §5, C1-C2 | `experiments/manifest.yaml` + 2 skrip |
| P0-6 | **Tetapkan definisi label final** (fraud-scenario / anomali / normal) dan rekonsiliasi 240/24/36 vs 264 | P0.1, C3 | `labels.md` |
| P0-7 | **Arahkan demo ke 300 klaim** (atau revise proposal ke 100) + beri label "Dataset simulasi" di UI | §4.2 R4, P0.2, C4 | Demo + naskah konsisten |
| P0-8 | **Buang semua angka yang tidak reproducible** dari deck & demo: AUPRC 0,9142, akurasi 93,0%, ROC-AUC 0,9825, masking 89,4%, FPR 10,6%, −45% waktu, 3,2x, SUS 82,5, Rp507.370.000, Rp25 miliar→Rp35 miliar, "ratusan miliar hingga triliunan". Pengecualian FPR 10,6%: angka ini boleh tetap tampil **hanya** dengan menyebut ambang 0,14 dan presisi 56,25% pada ambang itu, karena presisi 94,12% yang biasa dipasangkan dengannya tidak berlaku di sana | §7.2 | Deck bersih |
| P0-9 | **Rekonsiliasi angka operasional** proposal vs database riset + koreksi deadline di Notion & catatan (11 Okt, bukan 14 Sep) | P0.5, §7.1.7 | Changelog |
| P0-10 | **Koreksi `13-archive-deep-research.md:3`**: Rp25 miliar → **Rp35 miliar**, tambahkan rincian 3 RS, dan tambahkan rujukan KPK primer | §7.2 | Dokumen arsip dikoreksi |
| P0-11 | **Buat video demo 3–5 menit + deck maks 10 slide + perbaiki URL clone di README dan URL Vercel** (repo sudah publik, tidak perlu dibuat) | §4.2 R11, C9-C12 | Bundle submit |
| P0-12 | **Finalisasi naskah proposal: sebut Healthkathon, kategori resmi, subkategori #4 & #6** | C17 | `01-proposal.md` revisi 1.1 |

### P1 - menguatkan submit (30 Okt - 4 Nov)

| # | Aksi |
|---|---|
| P1-1 | **Restore 12 item bernilai argumentatif dari arsip** (A1, A2, A5, A6, A9, A10, A11, A13, A14, A16, A18, A20) dengan pemisahan tegas fakta vs target |
| P1-2 | **Review klinis skenario** (`00-dashboard.md:64`) - P1, dan perbaiki demo agar label "paling awal" |
| P1-3 | **Aktifkan coaching 19–30 Okt secara agresif**: ajukan review metodologi, review klinis, review kelengkapan dokumen |
| P1-4 | **Rekonsiliasi demo app ↔ data** (`data.ts:448-451`: 19 klaim → 29; 78% → 100%; SYND-01 Rp470,6 M → Rp156,9 M) |
| P1-5 | **Koreksi 264 normal (88%) → 240 auto-clear (80%)**; koreksi Upcoding Rp127,68 M → Rp212,8 M; sindikat Rp542,56 M → Rp539,65 M |
| P1-6 | **Ajukan permintaan akses data / pendampingan** ke BPJS lewat kanal coaching sebagai langkah eksplisit |
| P1-7 | **Ganti angka "2 juta klaim/hari"** dengan **"±650.000 berkas/hari, ±5% terindikasi fraud"** (Bloomberg Technoz 11 Jun 2026) - lebih baru, lebih kuat, dan diakui luas |
| P1-8 | **Hapus angka "1.000 verifikator" dan rasio 2.000:1** dari semua materi (sumber sirkular) atau ganti "±1.000" → "jumlah verifikator tidak dipublikasikan" |
| P1-9 | **Aktifkan `09-draft-hub.md:6-7`**: hapus blok "100 klaim / prevalensi 14%" yang masih tercantum di halaman index |

### P2 - setelah Grand Final (nilai untuk kemitraan dengan BPJS)

P2-1 Roadmap 12 bulan + Stage-Gate (A18) sebagai lampiran proposal. P2-2 Realitas data: rencanakan UAT bersama verifikator. P2-3 Publikasi metodologi (paper) sebagai output. P2-4 Integrasi SATUSEHAT FHIR R4 & ekspor V-Claim sesuai `05-decision-scope.md:64` (hanya setelah izin).

---

## 10. Daftar Sumber

**Primer internal (semua di `N:\HEALTHKATHON\analysis\corpus\`):**
`00-dashboard.md`, `01-proposal.md`, `04-evidence-matrix.md`, `05-decision-scope.md`, `10-simulation-dataset.md`, `11-archive-proposal.md`, `13-archive-deep-research.md`, `claims_v2_live.csv` (300 baris, 29 kolom), `dataset_research_live.json`, `scripts/_hk_siklus.json`.
**Repositori:** `N:\HEALTHKATHON\Aegis-JKN\README.md`, `src\components\mhgsl\data.ts`, `src\data\oasis-data.ts`, git log.
**API resmi (akses 22 Okt 2026):** `POST https://healthkathon.bpjs-kesehatan.go.id:8080/healthkathon/rest/referensi/siklus/list`, `GET .../referensi/jumlahpeserta`, `GET https://healthkathon.bpjs-kesehatan.go.id/`, bundle `main.2f0e2e63f6591013.js`.
**Publik (akses 22 Okt 2026, via SearXNG):**
IDN Times "BPJS Kesehatan Gelar Healthkathon 2026" (14 Agu 2026) · RRI "BPJS Kesehatan Luncurkan Empat Inovasi Layanan Digital Berbasis AI" (3 Feb 2026) · WASPADA "SISCA JKN Diluncurkan" · Radar Bali "4 Inovasi AI Terbaru 2026" · Bloomberg Technoz "AI Mampu Deteksi Potensi Fraud Triliunan di BPJS Kesehatan" (11 Jun 2026) · Kontan "BPJS Kesehatan Minta Faskes Bentuk Tim Anti Kecurangan" (25 Jul 2024) · CNN Indonesia "Tim PK-JKN" (25 Jul 2024) · Metro TV "KPK Bongkar 3 Rumah Sakit Lakukan Fraud Klaim BPJS hingga Rp35 M" (25 Jul 2024) · Tribun "Mantan Dokter hingga Dirut Rumah Sakit Diduga Terlibat Kasus Klaim Fiktif BPJS" (25 Jul 2024, **403 untuk bot - kutipan terverifikasi via snippet mesin pencari**) · Kompas Regional "Dinkes Benarkan Ada RS di Jateng Ajukan Klaim Palsu" (26 Jul 2024) · Wahana News "Terbongkar, Begini Modus RS di Jateng dan Sumut" (25 Jul 2024, 25.011 klaim fiktif) · Kompas "Ketika Agen AI Mengubah Cara Kerja BPJS Kesehatan" (15 Jun 2026, 650 berkas/verifikator/hari) · detik.com "Pemenang Healthkathon 2024" · CNN Indonesia "Pemenang Healthkathon 2025" (30 Nov 2025) · Kontan "Klaim layanan BPJS tembus 2 juta per hari" (19 Sep 2025) · JIMAT "BPJS Kesehatan Dorong Implementasi AI Melalui Healthkathon 2026" (14 Agu 2026) · NalarAI/nalar-core README (kompetitor kategori sama, pembanding).
**Tidak terbaca / tidak ditemukan:** `Participant Guide` Healthkathon (SharePoint PDF, HTTP 403) · rubrik & bobot penilaian (tidak ada endpoint publik) · ResearchGate 372079501 (403).
