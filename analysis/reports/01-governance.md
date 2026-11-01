# Laporan Audit Tata Kelola Dokumen - Aegis-JKN (Healthkathon BPJS Kesehatan 2026)

**Tanggal audit:** 22 Oktober 2026
**Ruang lingkup:** 9 dokumen terkendali (00–08) + 6 dokumen arsip/agregat (09–14) + 2 ekspor basis data (`claims_v2_live.csv`, `claims_v2_live.json`, `dataset_research_live.csv`) di `N:\HEALTHKATHON\analysis\corpus\`
**Sumber kebenaran tata kelola:** `00-dashboard.md` §7 (L74–85), §9 (L90), §3 (L28–39)
**Metode:** pembacaan dokumen + hitung ulang angka dengan Python stdlib (`csv`, `json`, `re`, `collections`); `pandas` tidak tersedia di lingkungan ini dan tidak dipakai.

## 1. Ringkasan Eksekutif

Sembilan dokumen terkendali *secara editorial* sudah jauh lebih ketat daripada draf sumber: tidak ada satu pun dokumen terkendali yang memakai status "Tervalidasi", tidak ada em-dash di 15 berkas `.md` korpus, dan angka-angka reconciled pada `00-dashboard.md` §3 sebagian besar benar secara aritmetika. Namun governance *operasional*-nya longgar di empat tempat: (a) satu baris fakta rekonsiliasi yang salah secara faktual, (b) register bukti yang menandai sumber level C/D sebagai "Terverifikasi", (c) agregat `14-index.md` yang memuat ulang klaim "Tervalidasi" tanpa banner tingkat berkas, dan (d) gerbang kualitas yang tidak punya kriteriaclosure terukur, sehingga tidak ada satu pun item P0/P1/P2 yang dapat ditutup secara objektif.

Total temuan: **40** (BLOCKER 5, HIGH 15, MEDIUM 13, LOW 4, INFO 3).

| Severity | Jumlah | Arti |
|---|---|---|
| BLOCKER | 5 | Melanggar prinsip tata kelola yang tertulis eksplisit di `00-dashboard.md`; harus diperbaiki sebelum dokumen diserahkan |
| HIGH | 15 | Melanggar Standar Dokumen §7 atau gerbang publikasi `04-evidence-matrix.md` §9 |
| MEDIUM | 13 | Cakupan/pembagian yang tidak jelas, kontrol ada di kertas saja, atau data bertentangan dengan dokumen kendali |
| LOW | 4 | Ketidaktelitian redaksional dan cakupan tabel |
| INFO | 3 | Temuan lintas silang, tidak memerlukan tindakan terpisah |

Tidak ada temuan yang tidak disertai bukti (nama berkas + nomor baris, nomor baris CSV, atau kutipan teks). Angka yang direkomputasi ulang selalu menyebutkan sumber data yang dipakai.

## 2. Tabel Pelanggaran per Dokumen per Aturan

### 2.1 `00-dashboard.md` - Pusat Kendali (sumber kebenaran)

| Aturan dilanggar | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| §7 aturan 4 - bedakan fakta dari rancangan/hipotesis/hasil uji/estimasi | L36 `\| Kolom LOS hari kosong \| 109 baris \|` | Baris fakta yang salah; lihat B-1. Baris ini menjadi dasar item P1 "perlakuan nilai LOS kosong" (L66) |
| §7 aturan 4 - bedakan fakta dari estimasi | L39 menyebut overcharge Rp507.370.000 "belum dapat direproduksi" | Tidak konsisten dengan arsip yang menyebutnya "Penyelamatan Riil" (`11-archive-proposal.md` L347); lihat B-4 |
| §7 aturan 2 - awali dengan status, versi, tanggal, tujuan | L4–L6 hanya memuat "Status proyek", "Tanggal pembaruan", "Versi dokumentasi terkendali"; tidak ada field tujuan | Dashboard tidak memenuhi standar yang ia tetapkan sendiri untuk dokumen lain |
| §7 aturan 10 - perubahan substansial dicatat pada changelog | L86–L88 memuat satu baris versi 1.0, sementara L92–L95 menambahkan 07 dan 08 tanpa baris changelog baru | Kontrol versi tidak dapat dipakai untuk melacak penambahan dokumen terkendali baru |
| §9 L90 - status memakai kosakata baku | L4 `Status proyek: Purwarupa riset terapan` bukan salah satu dari lima status baku | Lihat H-1 |
| §2 - "Dokumen terkendali" harus menjadi daftar otoritatif | L12–L18 mendaftarkan 6 dokumen; L92–L95 menambahkan 07 dan 08 di bawah judul "# Dataset dan training AI" tanpa status/versi | Lihat M-3 |
| §3 / `03-dataset-registry.md` L15 - versi 100 klaim harus ditandai sebagai versi awal | L22 `Dokumentasi Dataset Simulasi, 100 Klaim` ditautkan tanpa penanda versi awal | Lihat M-4 |

### 2.2 `01-proposal.md` - Proposal Riset dan Inovasi

| Aturan dilanggar | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| §7 aturan 6 - semua klaim eksternal memiliki sitasi spesifik; `04-evidence-matrix.md` L39+L56 | L91 `Referensi teknis XGBoost, graph neural networks, SHAP, dan evaluasi model harus dicantumkan dengan metadata bibliografi lengkap` - daftar referensi L86–L90 tidak memuat satu pun dari sumber tersebut, padahal L43 menyebut XGBoost, L47 GroupKFold, L49 AUPRC/PR-AUC | Naskah handal tidak dapat ditransmisikan: metode kunci tidak punya sitasi |
| §7 aturan 2 - awali dengan status, versi, tanggal, tujuan | L4 `Status dokumen: Revisi editorial dan metodologis`; L5 `Tanggal revisi:`; tidak ada field "Versi" (versi hanya tersirat di judul L3) | Metadata tidak seragam antar dokumen; lihat M-10 |
| §9 L90 - status memakai kosakata baku | L4 | Lihat H-1 |
| §7 aturan 10 - changelog | Tidak ada bagian changelog; L92–L93 hanya `## Catatan editorial` | Riwayat perubahan substantive tidak tercatat |
| §7 aturan 4 / `04-evidence-matrix.md` §8 butir 5 - estimasi penghematan harus membedakan potensi koreksi, nilai diputuskan, dana menyelamatkan | L70 menyebut estimasi Rp507.370.000 sebagai "draf sebelumnya" tanpa sumber | Bagus secara tata kelola, tetapi belum harmonis dengan arsip (B-4) |
| §7 aturan 4 - bedakan non-fraud dari normal | L37 sudah benar: "Distribusi label risiko adalah 240 low, 10 medium, 14 high, dan 36 fraud" | Dokumen NIAGA benar; arsip melanggar (L344 "Klaim Normal (Auto-Clear) | 240 klaim") |

### 2.3 `02-architecture.md` - Spesifikasi Rekayasa

| Aturan dilanggar | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| §7 aturan 10 - perubahan substansial dicatat pada changelog | L115–L116 `## 9. Catatan Revisi` berupa prosa tanpa kolom versi/tanggal/perubahan | Perubahan tidak dapat dilacak per versi |
| §7 aturan 2 - "Dokumen induk" hanya ada di satu dokumen | L6 satu-satunya kemunculan `Dokumen induk:` di seluruh 9 dokumen kendali | Lihat H-4 |
| §9 L90 | L4 `Status: Rancangan teknis untuk purwarupa` | Lihat H-1 |
| Gerbang penerimaan MVP | L108–L114 D-01..D-06 seluruhnya "Terbuka" tanpa tenggat, tanpa kriteria closure, pemilik berupa tim | MVP tidak dapat dinyatakan siap walau 6 keputusan pembuka masih terbuka; lihat M-8 |

### 2.4 `03-dataset-registry.md` - Dataset Registry

| Aturan dilanggar | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| §3 Fakta Direkonsiliasi | L78 `109 baris memiliki kolom LOS hari kosong;` | Salah faktual (B-1) |
| §3 / `00-dashboard.md` L36 | L79 `satu baris tidak memiliki isi pada properti Alasan;` | Benar (KLM031) - tidak ada pelanggaran |
| §7 aturan 4 - bedakan fakta dari asumsi | L77 `tidak ditemukan ketidaksesuaian antara label risiko dan rentang skor yang tersimpan bila memakai ambang kategori versi aktif` | Klaim hanya benar bila ambang 0,80 inklusif, sedangkan skala yang tertulis di `10-simulation-dataset.md` L9 "lebih dari 0.8 fraud" dan `09-draft-hub.md` L116 "di atas 0.8 fraud" bersifat eksklusif; KLM115 (Skor Fraud 0.80, Risiko fraud) adalah satu-satunya kasus batas; lihat H-6 |
| §5 Data Dictionary - inventaris properti | L48–L72 memuat 24 properti; ekspor aktif `claims_v2_live.csv` memiliki 27 kolom data + 2 kolom metadata Notion; `Rujukan`, `Alasan Berobat`, `Layanan` tidak ada di kamus data | Kamus data yang L98 mewajibkan sebagai artefak tidak lengkap; see H-7 |
| §5 - kamus data harus mendefinisikan "Sentimen: Harus sesuai dengan definisi skor" | L70; komputasi ulang: 58 dari 300 baris ber-`Sentimen` `netral` dengan `Skor Sentimen` positif (0,05–0,15), mis. KLM278 0,14; KLM280 0,12; KLM273 0,09 | Aturan mutlak di L70 dilanggar 58 kali; see H-8 |
| §5 - `Kontradiksi Narasi` "Perlu aturan penetapan yang eksplisit" | L60; komputasi ulang: 12 baris bernilai true (KLM001–KLM006, KLM018, KLM024, KLM105, KLM106, KLM107, KLM108) | Lihat H-9 |
| §6 Pemeriksaan kualitas | L82 membenarkan perlakuan nilai LOS kosong, dan L109linic P1 "Tentukan perlakuan resmi untuk nilai LOS kosong" | Berpijak pada kondisi yang tidak ada di ekspor (B-1) |
| §5 - `Sindikat` | L65 "Kosong dibolehkan bila tidak terkait"; KLM121 dan KLM122 berstatus `escalate`/`fraud` tetapi `Sindikat` kosong, padahal `09-draft-hub.md` L146–L147 mendaftarkannya sebagai dua fraud tunggal (Biaya Markup, Drug Diversion) | Tabel sindikat di korpus tidak tercermin di data; lihat M-9 |
| §9 L90 | L4 `Status: Dokumentasi kontrol data` | Lihat H-1 |
| §7 aturan 5 - tabel menyatakan satuan dan denominator | L32–L36 tabel nominal tidak menyebut satuan/denominator di header kolom | Renal; lihat L-1 |

### 2.5 `04-evidence-matrix.md` - Register Evidence

| Aturan dilanggar | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| §3 L19–25 + §4 (E-04, E-05) vs isi `dataset_research_live.csv` | Baris 19 (blog `allalliedhealthschools.com`, Kritis), 21 (Kontan, Kritis), 26 (ResearchGate), 28 (law-firm blog), 31 (Kompas, "Terverifikasi"), 32 (Stabilitas, "Terverifikasi"), 34 (repo sendiri, Kritis) seluruhnya ber-`Status Verifikasi` = `Terverifikasi` | Register memuat 18 "Terverifikasi" (L12) yang majority-nya bertingkat C/D; lihat B-2 |
| §4 E-04 L31 `Hindari menjadikan repositori internal sebagai satu-satunya sumber` | Baris 25 "Kapasitas verifikasi ±1.000 verifikator (rasio 2.000:1)" bersumber hanya `https://github.com/biezz-2/Aegis-JKN` | Pelanggaran eksplisit aturan register sendiri |
| §7 Format Entri Sumber yang Wajib (12 field, L57–L69) | `dataset_research_live.csv` hanya punya 10 kolom (`Status Verifikasi, Relevansi, Sumber Riset, Deskripsi, Kategori, Pendekatan Deteksi/Teknis, Catatan Riset, Item, _notion_page_id, _last_edited`); tidak ada penulis/tahun/jurnal/tingkat A–D/kutipan/reviewer/tanggal verifikasi; 6 baris `Sumber Riset` kosong (baris 3, 7, 15, 16, 17, 18) | Register tidak dapat diaudit; lihat H-11 |
| §9 Gerbang Publikasi L79 "Setiap angka utama memiliki sumber atau artefak eksperimen" | `00-dashboard.md` L47–L51 dan `11-archive-proposal.md` L326–L330 | Gerbang tidak dioperasikan pada artefak agregat; lihat B-3 |
| §10 Prinsip Editorial L87 | `11-archive-proposal.md` L338 `membuktikan keunggulan mutlak`; L346 `Overcharge Terbukti`; L347 `Penyelamatan Riil` | Lihat B-3 dan B-4 |
| §9 L90 | L4 `Status: Register evidence dan kontrol referensi` | Lihat H-1 |
| Konsistensi kosakata register | L28–L39 memakai status "Perlu cek pasal spesifik", "Sebagian terverifikasi", "Belum tereproduksi pada audit ini", "Belum dibuktikan dengan artefak yang tersedia", "Belum dapat direproduksi per klaim" - tidak sama dengan nilai `Status Verifikasi` di CSV (Terverifikasi/Sebagian Terverifikasi/Perlu Verifikasi) maupun kosakata dokumen L90 | Lihat M-6 |

### 2.6 `05-decision-scope.md` - Analisis Keputusan

| Aturan dilanggar | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| §7 aturan 2 / §9 L90 | L4 `Status: Dokumen keputusan produk` | Lihat H-1 |
| §7 aturan 10 changelog | Tidak ada; L72–L77 `## 7. Keputusan yang Masih Perlu Dicatat` berisi 5 checkbox | Lihat H-3 |
| §7 aturan 4 - definisi "selesai" | L77 `- [ ] Tetapkan definisi selesai untuk demo, paper, dan presentasi.` | Item ini adalah kontrol yang tepat untuk mencegah klaim tervalidasi ala arsip, namun tidak memiliki kriteria closure dan belum dikerjakan; lihat M-5 |
| Angka bobot | L19 `Skor angka belum diberikan karena bobot dan penilaian belum melalui lokakarya tim yang terdokumentasi.` | Compliant - tidak ada temuan |

### 2.7 `06-research-notes.md` - Catatan Riset

| Aturan dil rewatch | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| §7 aturan 10 changelog / §9 L90 | L4 `Status: Catatan tinjauan literatur awal`; tidak ada changelog | Lihat H-1, H-3 |
| §7 aturan 6 - sitasi spesifik | L60 hanya satu URL (SATUSEHAT); L61–L63 menyebut "Peraturan tentang Pelindungan Data Pribadi, rekam medis, dan pencegahan fraud JKN", "Literatur ilmiah primer tentang XGBoost, graph neural networks, SHAP" dan "Laporan resmi BPJS" sebagai placeholder tanpa identitas sumber | Sumber yang dirujuk tidak dapat dibuka/diperiksa - melanggar gerbang L80 "Setiap sumber eksternal telah dibuka dan diperiksa" |
| §5 Matriks Bukti Awal | L42 `AUPRC MHGSL 0,9142 \| ... \| Belum dapat direproduksi dari artefak yang diperiksa`; L45 `Penghematan finansial \| ... \| Belum dapat direproduksi dari data biaya saja` | Compliant dan konsisten dengan `04` E-07/E-11; tidak ada temuan |

### 2.8 `07-dataset-v2-catalog.md` - Katalog DM Kontekstual

| Aturan dilanggar | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| §7 aturan 2 - awali dengan status, versi, tanggal, tujuan | Tidak ada blok header sama sekali; L3 adalah prosa, L4 adalah baris peringatan privasi | Dokumen kendali tanpa metadata; lihat H-2 |
| §7 aturan 1 - judul jelas | L5 `# Ringkasan ukuran data` adalah satu-satunya H1 dan tidak menyebut "katalog" atau nama dokumen; tidak ada H1 "07 | Dataset Registry…" seperti pada dokumen lain | Judul tidak menandai dokumen ini sebagai katalog data |
| §7 aturan 10 changelog | Tidak ada bagian changelog | Lihat H-3 |
| §9 L90 - status | Tidak ada field status | Lihat H-1, H-2 |
| Kebocoran artefak mentah Notion | L4 `> **{'type': 'emoji', 'emoji': '💡'}** Peringatan privasi: data kepesertaan ...` | Peringatan privasi yang paling penting di korpus tampil dalam bentuk literal dict; lihat M-2 |
| §7 aturan 5 - tabel satuan dan denominator | Tabel 2 (L17–35) dan Tabel 4 (L43–64) kolom "Kosong" hanya berisi angka tanpa denominator; denominator ada di Tabel 1 yang terpisah | Lihat L-1 |
| §7 aturan 3 - istilah konsisten | L6 "Tiga file Stata berisi total 6.514.039 baris" vs Tabel 1 (L9–L11) 143.496 + 6.362.523 + 8.020 = 6.514.039 | Konsisten; tidak ada temuan |

### 2.9 `08-training-protocol.md` - Protokol Training AI

| Aturan dilanggar | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| §7 aturan 1 - judul jelas | Tidak ada satu pun heading markdown di berkas ini; grep `^#{1,3} ` hanya menemukan 5 baris komentar di dalam blok Python (L55, L62, L77–L79) | Dokumen kendali tanpa judul; lihat H-2 |
| §7 aturan 2 - status, versi, tanggal, tujuan | Tidak ada blok header; L3 prosa, L4 daftar tautan, L5 baris dict Notion | Lihat H-2 |
| §7 aturan 10 changelog | Tidak ada; dokumen ini adalah dokumen kendali terbaru (dirujuk `00-dashboard.md` L95) tanpa versi | Lihat H-3 |
| §9 L90 - status | Tidak ada field status | Lihat H-1 |
| §7 aturan 4 - bedakan fakta dari rencana | L8 dan L20 menyatakan deskripsi database masih menyebut 100 klaim dan ground truth KLM001–KLM024, padahal 22 dari 36 baris `fraud` berada di luar KLM001–KLM024 (hingga KLM122) | Dokumen land untuk/definisikan, tetapi tidak ada butir P0/P1 yang menutup instance konkret; lihat H-14 |
| §3 L30–L35 Artefak Wajib vs repo | Wajib: `manifest.json` (L30), `label_audit.csv` (L31), `data_quality_report.md` (L32), `train.py` + `metrics.json` (L33), `evaluation_report.md` (L34), `review_log.csv` (L35). Tidak ada satu pun berkas tersebut di `N:\HEALTHKATHON\Aegis-JKN` (pencarian seluruh repo, termasuk `wiki/.config.yml` satu-satunya `.yaml`) | Gerbang eksperimen mustahil; lihat B-5 |
| §4 L22 vs data aktif | `Sinyal SHAP` dan `Kontribusi Saluran` terisi pada 300/300 baris; `Alasan` terisi 299/300 | Lihat H-13 |
| §5 L37 split | "gunakan cross-validation berulang atau stratified cross-validation setelah label diaudit" | Compliant; tidak ada temuan |

### 2.10 Dokumen arsip/agregat (`09`–`14`)

| Aturan dilanggar | Bukti kutipan + lokasi | Dampak |
|---|---|---|
| `00-dashboard.md` L46–L52 + `04-evidence-matrix.md` L87 | `11-archive-proposal.md` L30 `300 berkas klaim tervalidasi klinis ... membuktikan performa superior model MHGSL: Akurasi 93.0%, Presisi 94.12%, ROC-AUC 0.9825, dan AUPRC 0.9142`; L326–L330 `93.00% (Tervalidasi)`, `94.12% (Tervalidasi)`, `0.9825 (Tervalidasi)`, `89.40% (Tervalidasi)`; L342 `membuktikan potensi dampak ekonomi riil`; L347 `Rp 507.370.000 (Penyelamatan Riil)` | Lihat B-3, B-4 |
| `00-dashboard.md` L83 - tidak ada em-dash di dokumen formal | 15 berkas `.md` korpus: 0 kemunculan U+2014 (dihitung per berkas). Namun `claims_v2_live.csv` memuat 324 em-dash pada 293 dari 300 baris: `Alasan` 160, `Prosedur ICD-9-CM` 156, `Sinyal SHAP` 5, `Obat` 3 | Aturan berlaku untuk dokumen, bukan untuk data; tidak ada keputusan terdokumentasi yang mengaturnya; lihat M-1 |
| `00-dashboard.md` L3 + `03` L30 / `01` L37 | `11-archive-proposal.md` L344 `Klaim Normal (Auto-Clear) \| 240 klaim \| 80.00%`; L348 "Dari 60 klaim yang ditandai anomali" | Lihat H-15 |
| `04-evidence-matrix.md` L8 | `13-archive-deep-research.md` L3 `Kasus yang di report oleh BPJS tahun 2024 melibatkan 3 rumah sakit swasta di jawa tengah dan sumatra utara dengan total kerugian mencapat RP25 miliar.` - tidak ada di 33 entri `dataset_research_live.csv` maupun di register E-01..E-12 | Lihat H-13 |
| `04-evidence-matrix.md` L3 | `14-index.md` L505, L795–L805, L817, L821, L823–L824 memuat ulang klaim "Tervalidasi" tanpa banner tingkat berkas; banner `CATATAN EDITORIAL` hanya ada di L5, L479, L908, L1101 | Lihat B-3 |

## 3. Metadata Tidak Konsisten

Aturan sumber: `00-dashboard.md` L77 "Awali dengan status, versi, tanggal, dan tujuan" dan L90 (kosakata status).

| Dokumen | Status | Versi | Tanggal | Tujuan | Dokumen induk | Changelog |
|---|---|---|---|---|---|---|
| `00-dashboard.md` | L4 "Purwarupa riset terapan" (bukan kosakata baku) | L6 "Versi dokumentasi terkendali: 1.0" | L5 ada | tidak ada | - | L86–L88 ada (1 entri) |
| `01-proposal.md` | L4 "Revisi editorial dan metodologis" (bukan kosakata baku) | tidak ada (hanya di judul L3) | L5 "Tanggal revisi" | L6 "Jenis naskah" | tidak ada | tidak ada |
| `02-architecture.md` | L4 "Rancangan teknis untuk purwarupa" (bukan kosakata baku) | tidak ada | L5 "Terakhir direvisi" | tidak ada | L6 ada | L115–L116 (prosa, bukan tabel) |
| `03-dataset-registry.md` | L4 "Dokumentasi kontrol data" (bukan kosakata baku) | tidak ada | L5 ada | L6–L7 (sumber, jenis data) | tidak ada | L101–L104 ada |
| `04-evidence-matrix.md` | L4 "Register evidence dan kontrol referensi" (bukan kosakata baku) | tidak ada | L5 "Tanggal audit" | L6 (database sumber) | tidak ada | tidak ada |
| `05-decision-scope.md` | L4 "Dokumen keputusan produk" (bukan kosakata baku) | tidak ada | L5 ada | L6 (keputusan sementara) | tidak ada | tidak ada |
| `06-research-notes.md` | L4 "Catatan tinjauan literatur awal" (bukan kosakata baku) | tidak ada | L5 "Tanggal revisi" | L6 ada | tidak ada | tidak ada |
| `07-dataset-v2-catalog.md` | **tidak ada** | tidak ada | tidak ada | tidak ada | tidak ada | tidak ada |
| `08-training-protocol.md` | **tidak ada** | tidak ada | tidak ada | tidak ada | tidak ada | tidak ada |

Temuan turunan:

- **H-1 (HIGH)** - Kosakata status baku L90 (Rancangan / Dalam Implementasi / Siap Diuji / Tervalidasi / Diarsipkan) tidak dipakai sebagai nilai field status pada satu pun dari 9 dokumen. Enam dokumen (01, 03, 04, 05, 06, dan 00) memakai frasa bebas; 02 memakai frasa bebas yang memuat kata "Rancangan" di dalam kalimat (`Rancangan teknis untuk purwarupa`), bukan sebagai nilai status; 07 dan 08 tidak punya status sama sekali. Dampak: aturan pembaruan status L90 ("Pemilik setiap dokumen harus memperbarui status hanya setelah memeriksa artefak sumber") tidak dapat dioperasikan karena tidak ada field status yang seragam.
- **H-2 (HIGH)** - 07 dan 08 tidak memiliki blok metadata sama sekali, dan 08 tidak memiliki satu pun heading markdown. 01/03/04/05/06 tidak punya field "Versi". 00 tidak punya field tujuan. 08 adalah dokumen kendali terbaru (`00-dashboard.md` L95) sehingga kekosongan ini paling berisiko: ia mengatur prosedur pelatihan tanpa versi, tanpa tanggal, dan tanpa status.
- **H-3 (HIGH)** - Aturan changelog L85 dilanggar oleh 6 dari 9 dokumen (01, 04, 05, 06, 07, 08). Hanya 00, 02, 03 yang punya bagian revisi, dan 02 bentuknya prosa tanpa kolom versi/tanggal/perubahan. Karena 08 adalah dokumen baru yang wajib menjadi acuan, tidak ada catatan perubahan sama sekali.
- **H-4 (HIGH)** - `Dokumen induk` hanya ada di `02-architecture.md` L6. 01, 03, 04, 05, 06 tidak menyatakan induk; 07 dan 08 saling menautkan (07 L91 → 08; 08 L4 → 07, 03, 02) tetapi tidak menunjuk `00-dashboard.md` sebagai induk. Dampak: tidak ada graf dokumen, sehingga "perubahan substansial dicatat pada changelog" tidak punya titik rujukan.
- **M-3 (MEDIUM)** - Daftar "Dokumen terkendali" pada `00-dashboard.md` L12–L18 hanya berisi 6 entri; 07 dan 08 ditambahkan di L92–L95 dengan heading baru "# Dataset dan training AI" tanpa status, versi, atau penanda bahwa keduanya juga terkendali.
- **M-4 (MEDIUM)** - `03-dataset-registry.md` L15 mewajibkan "Dokumentasi harus menjelaskan bahwa versi 100 klaim adalah versi awal"; `00-dashboard.md` L22 menautkan "Dokumentasi Dataset Simulasi, 100 Klaim" tanpa penanda versi awal, dan `10-simulation-dataset.md` L4 baru menambahkan "CATATAN VERSI". Halaman hub yang-controlled justru tidak membawa penanda itu.
- **M-10 (MEDIUM)** - Nama field tanggal tidak seragam: "Tanggal pembaruan" (00 L5), "Tanggal revisi" (01 L5, 06 L5), "Terakhir direvisi" (02 L5), "Tanggal" (03 L5, 05 L5), "Tanggal audit" (04 L5). Tidak ada field tanggal di 07/08. Otomasi pemeriksaan metadata tidak mungkin ditulis tanpa memoisasi 6 nama field.
- **M-2 (MEDIUM)** - Pola literal Notion `{'type': 'emoji', 'emoji': '💡'}` bocor ke berkas terdokumentasi pada 07 L4, 08 L5, 09, 10, 11, 12, 13, 14. Di 07 L4 dan 08 L5 objek literal itu justru membungkus peringatan privasi dan keputusan inti anti-leakage, sehingga pesan dengan bobot keselamatan tertinggi tampil sebagai data mentah. Lihat juga H-13 untuk 08.
- **M-7 (MEDIUM)** - `04-evidence-matrix.md` L10 "Database berisi 33 entri" tanpa anchor versi: `03-dataset-registry.md` L91 membuat checksum dan waktu ekspor wajib, tetapi snapshot 33 entri tidak mengaitkan dirinya ke ekspor tertentu. Rekonsiliasi 18/11/4 dan 11/18/4 benar, tetapi tidak dapat diulang pada ekspor berbeda.

## 4. P0/P1/P2 Tanpa Closure Criteria Terukur

Sumber: `00-dashboard.md` L57–L73, judul bagian "Papan Kerja dan Gerbang Kualitas".

| ID | Item (kutipan) | Lokasi | Closure criteria terukur? | Bukti kekosongan |
|---|---|---|---|---|
| P0-1 | `Tetapkan definisi label fraud-scenario, anomali, dan normal.` | L59 | **Tidak** | Tidak ada ambang, nama artefak, atau tanggal. Justru `02-architecture.md` L109 D-01 masih "Terbuka" |
| P0-2 | `Tandai dokumen 100 klaim sebagai versi awal dan dataset 300 klaim sebagai versi aktif.` | L60 | **Tidak** | Status "aktif" sudah ada di `03` L6 dan L13, tetapi dashboard L22 masih menautkan 100 klaim tanpa penanda; tidak ada kriteria "ditandai pada halaman X" |
| P0-3 | `Lampirkan manifest eksperimen dan skrip untuk seluruh metrik yang dipublikasikan.` | L61 | **Tidak** | Tidak ada nama file, ID eksperimen, atau path. `02-architecture.md` L77 sudah mewajibkan `experiment_manifest.json`, `08` L30–L35 mewajibkan 6 artefak, dan tidak satu pun ada di repo (B-5) |
| P0-4 | `Tambahkan tarif acuan dan metode perhitungan per klaim untuk estimasi overcharge.` | L62 | **Tidak** | Tidak ada tarif acuan, tidak ada formula, tidak ada rounding, tidak ada daftar baris. `04` E-11 (L38) statusnya "Belum dapat direproduksi per klaim" |
| P0-5 | `Samakan angka operasional yang berbeda di proposal dan database riset.` | L63 | **Tidak** | Tidak ada daftar pasangan angka yang harus sama, tidak ada ambang toleransi. Justru perbedaan yang terdeteksi justru menumpuk (lihat §6) |
| P1-1 | `Minta review klinis atas skenario dan kode diagnosis/prosedur.` | L65 | **Tidak** | Tidak ada jumlah skenario minimum, identitas reviewer, atau bentuk bukti review |
| P1-2 | `Selesaikan data dictionary dan perlakuan nilai LOS kosong.` | L66 | **Tidak** | Berpijak pada temuan yang salah (B-1): 109 baris bernilai 0, bukan kosong, sehingga tri-state `not_applicable`/`unknown`/hilang yang diminta `03` L82 tidak dapat diturunkan dari ekspor |
| P1-3 | `Periksa sumber regulasi pada situs resmi dan tulis pasal spesifik.` | L67 | **Tidak** | Tidak ada daftar peraturan, pasal, atau tanggal akses yang disyaratkan `04` L47 |
| P1-4 | `Lengkapi metadata bibliografi dan sitasi dekat dengan klaim.` | L68 | **Tidak** | Tidak ada daftar dokumen yang harus dilengkapi, tidak ada minimal field yang dianggap cukup (padahal `04` L57–L69 sudah menyediakan 12 field wajib) |
| P1-5 | `Tetapkan owner dan reviewer untuk data, eksperimen, keamanan, dan proposal.` | L69 | **Tidak** | Tidak ada nama owner, tidak ada SLA |
| P2-1 | `Uji penerimaan antarmuka dengan protokol yang terdokumentasi.` | L71 | **Tidak** | Tidak ada jumlah peserta, tugas, atau ambang kelulusan SUS (SUS 82,5 tetap diperlakukan sebagai belum tervalidasi di `00` L49) |
| P2-2 | `Buat release notes untuk setiap perubahan dataset atau model.` | L72 | **Tidak** | Tidak ada format, ambang perubahan, atau periode |
| P2-3 | `Pisahkan artefak pengembangan, hasil eksperimen, dan materi presentasi.` | L73 | **Tidak** | Tidak ada lokasi/namespace target |

Temuan turunan:

- **H-5 (HIGH)** - KetIGA belas item P0/P1/P2 (L59–L73) tidak satu pun memuat angka, ambang, nama artefak, ID eksperimen, atau tenggat. Bandingkan: satu-satunya tabel kriteria closure di seluruh korpus adalah `01-proposal.md` L76–L82 ("Kriteria selesai") yang isinya kualitatif ("Label dan nilai dapat ditelusuri", "Skrip dan metrik dapat diulang"). Dampak: bagian ini diberi nama "Gerbang Kualitas" (L57) tetapi tidak dapat dipakai sebagai gerbang - tidak ada keadaan yang dapat dibuktikan "selesai", sehingga `00` L90 ("Status Tervalidasi hanya boleh digunakan dengan bukti yang dapat ditinjau oleh orang lain") tidak pernah dapat diaktifkan secara sah.
- **H-6 (HIGH)** - Rekonsiliasi label di `03-dataset-registry.md` L77 bergantung pada ambang yang tidak pernah ditulis. Komputasi ulang: `Skor Fraud` per label risiko adalah low 0,04-0,14, medium 0,40–0,53, high 0,62–0,79, fraud 0,80–0,95; satu-satunya kasus batas adalah KLM115 (Skor Fraud 0.80 → Risiko `fraud`). Skala yang tertulis di `10-simulation-dataset.md` L9 dan `09-draft-hub.md` L116 berbunyi "lebih dari 0.8 fraud" / "di atas 0.8 fraud" (eksklusif), yang di bawahnya KLM115 adalah ketidaksesuaian. `03` L46 sendiri sudah menyinggung ambiguitas 0,80 tetapi L77 tetap menyatakan "tidak ditemukan ketidaksesuaian" tanpa menyebut ambang mana yang dipakai. Dampak: klaim "tidak ditemukan ketidaksesuaian" benar secara kebetulan, bukan berdasarkan aturan tertulis.
- **M-5 (MEDIUM)** - `05-decision-scope.md` L72–L77 memuat 5 checkbox terbuka tanpa kriteria, termasuk L77 `Tetapkan definisi selesai untuk demo, paper, dan presentasi` - kontrol yang tepat untuk mencegah klaim ala arsip, tetapi belum dikerjakan dan tanpa bentuk terukur.
- **M-6 (MEDIUM)** - `04-evidence-matrix.md` L28–L39 memakai lima label status yang tidak ada di kosakata `00` L90 maupun di nilai `Status Verifikasi` pada CSV. Akibatnya ada tiga kosakata status berbeda dalam satu sistem: kosakata dokumen (5 nilai), kosakata register (5 nilai lain), dan kosakata basis data riset (3 nilai).
- **M-8 (MEDIUM)** - `02-architecture.md` L108–L114: D-01..D-06 seluruhnya "Terbuka" tanpa tanggal target dan tanpa kriteria closure; pemilik ditulis sebagai entitas ("Tim data dan peninjau klinis", "Tim ML") bukan orang bernama. Karena `02` L96–L106 menetapkan 8 kriteria penerimaan MVP, dokumen ini tidak dapat dinyatakan memenuhi MVP selagi 6 keputusan pembuka belum ditutup.
- **I-4 (INFO)** - Tidak ada satu pun checkbox yang tercentang di seluruh korpus: `00-dashboard.md` 13, `03` 6, `04` 7, `05` 5, `06` 6, `14-index.md` 37 (0 tercentang di semua). Dengan demikian tidak ada satu pun artefak yang dinyatakan selesai, dan tidak ada dokumen yang saat ini berhak memakai status "Tervalidasi" (L90). Ini konsisten dengan `00` L46–L52, tetapi membuat status "Tervalidasi" tidak pernah terpakai sama sekali di korpus.

## 5. Status "Tervalidasi" dan Klaim "Terbukti"

Aturan: `00-dashboard.md` L7, L46–L52, L90; `04-evidence-matrix.md` L87 ("Hindari kata 'terbukti', 'riil', 'akurat secara superior', dan 'tervalidasi' sebelum syarat bukti dipenuhi"); `06-research-notes.md` L66.

Hasil greping `tervalidasi|terbukti|proven` (case-insensitive) di seluruh korpus `.md` (15 berkas) dan `dataset_research_live.csv`:

| Lokasi | Kutipan | Penilaian |
|---|---|---|
| `00-dashboard.md` L7, L46, L90 | "…tidak dinyatakan **tervalidasi** sebelum bukti pendukung dapat direproduksi"; "### Belum boleh disebut **hasil tervalidasi**"; "Status **Tervalidasi** hanya boleh digunakan dengan bukti yang dapat ditinjau" | **Compliant** - kutipan hanya menyatakan syarat, bukan bukti bahwa syarat terpenuhi. |
| `01-proposal.md` L7, L70, L84 | "…tidak dinyatakan sebagai **hasil tervalidasi**"; "…belum dinyatakan sebagai **hasil tervalidasi** dalam edisi ini"; "…hanya boleh menaikkan status… menjadi **hasil tervalidasi** setelah bukti pendukung tersedia" | **Compliant** |
| `04-evidence-matrix.md` L83, L87 | "Klaim yang belum **terbukti** ditandai sebagai hipotesis atau target"; "Hindari kata '**terbukti**'…" | **Compliant** (menyebut kata untuk melarangnya) |
| `06-research-notes.md` L66 | "…tidak menyatakan bahwa angka kinerja model Aegis-JKN telah **tervalidasi**…" | **Compliant** |
| `08-training-protocol.md` L15, L20 | "ground_truth_fraud … \| Belum disahkan"; "…jangan menyamakan field Risiko atau Status dengan label fraud yang telah diverifikasi" | **Compliant** |
| `09-draft-hub.md` L209, L421; `10-simulation-dataset.md` L206 | "⚠️ DESAIN **BELUM TERBUKTI UNGGUL**" | **Compliant** (k negated) |
| `11-archive-proposal.md` L30 | "300 berkas klaim **tervalidasi** klinis … **membuktikan** performa superior model MHGSL: Akurasi 93.0%, Presisi 94.12%, ROC-AUC 0.9825, dan AUPRC 0.9142" | **Pelanggaran** - 4 metrik tersebut yang `00` L47 masukkan daftar "Belum boleh disebut hasil tervalidasi" |
| `11-archive-proposal.md` L320–L321 | "## 7.5 Dataset Sintetis v2.1 **Tervalidasi** (300 Klaim INA-CBG/FHIR R4)"; "300 berkas klaim **tervalidasi** klinis dengan 31 fitur" | **Pelanggaran** - 300 baris di corpus memiliki 27 kolom data, bukan 31 fitur; dan tidak ada clinical review yang tercatat (L368 justru menyebut clinical validation sebagai GANJILITY masa depan) |
| `11-archive-proposal.md` L326–L330 | "93.00% (**Tervalidasi**)"; "94.12% (**Tervalidasi**)"; "0.9825 (**Tervalidasi**)"; "89.40% (**Tervalidasi**)" | **Pelanggaran** - status "Tervalidasi" disematkan pada metrik yang `04` E-07 tandai "Belum tereproduksi pada audit ini" dan `00` L47–L48 larang |
| `11-archive-proposal.md` L342, L346, L347 | "Analisis ini **membuktikan** potensi dampak ekonomi **riil**"; "Rp 394.950.000 (Overcharge **Terbukti**)"; "Rp 507.370.000 (Penyelamatan **Riil**)" | **Pelanggaran** - `04` L87 melarang kata "terbukti" dan "riil"; `04` L75 mewajibkan perbedaan antara potensi koreksi, nilai diputuskan, dan dana yang benar-benar diselamatkan |
| `12-archive-architecture.md` L115 | "Jenama Aegis-JKN (**tervalidasi** oleh purwarupa)" | **Pelanggaran** - "tervalidasi" untuk hal non-kinerja tanpa reviewer yang dapat meninjau |
| `14-index.md` L505, L553, L795–L805, L817, L821, L823, L843, L872 | Salinan utuh klaim di atas, termasuk "93.00% (**Tervalidasi**)", "Overcharge **Terbukti**", "Penyelamatan **Riil**", "platform beroperasi penuh skala nasional" | **Pelanggaran** - lihat B-3 |
| `13-archive-deep-research.md` L3 | "…total kerugian mencapat **RP25 miliar**" | **Pelanggaran** - lihat H-13 |

Temuan turunan:

- **B-3 (BLOCKER)** - `14-index.md` adalah agregat 1.940 baris yang menyalin ulang seluruh dokumen terkendali (00 mulai L1122, 01 mulai L1216, 02 mulai L1308, 03 mulai L1423, 04 mulai L1533, 05 mulai L1619, 06 mulai L1695, 07 mulai L1767, 08 mulai L1857) **dan** arsip tak terkendali (11 mulai L477, 12 mulai L906, 13 mulai L1099) secara verbatim. Banner `CATATAN EDITORIAL` hanya ada di L5, L479, L908, L1101 - tidak ada banner tingkat berkas yang menyatakan bahwa isi agregat bersifat historis. Akibatnya pembaca yang mendarat di agreget (entri corpus, salinan, atau hasil ekspor) bertemu "93.00% (Tervalidasi)" (L801), "0.9825 (Tervalidasi)" (L803), "Rp 394.950.000 (Overcharge Terbukti)" (L821), dan "platform beroperasi penuh skala nasional" (L877) tanpa penanda status, sehingga gerbang `00` L46–L52 dilewati tanpa jejak.
- **B-4 (BLOCKER)** - Klaim financial `11-archive-proposal.md` L344–L348: 240 auto_clear "Rp 0 (Klaim Layak Bayar)"; 24 review "Rp 112.420.000 (Potensi Koreksi)"; 36 escalate "Rp 394.950.000 (Overcharge Terbukti)"; total "Rp 507.370.000 (Penyelamatan Riil)"; dan L348 "sistem berhasil mendeteksi potensi kebocoran tarif (overcharge) sebesar Rp 507.370.000 (60,32% dari nominal klaim anomali, dengan rata-rata kerugian Rp 8.456.167 per klaim)". Komputasi ulang: 112.420.000 + 394.950.000 = 507.370.000 **tepat** (angka ini diturunkan dari dua angka yang tidak dapat direproduksi, bukan dihitung dari data). Ekspor aktif tidak memiliki kolom tarif; hanya 72 dari 300 baris memuat "rasio" yang dapat diurai, seluruhnya berlabel `low`, 34 di antaranya > 1,0 dengan total kelebihan Rp32.414.500; **0 dari 36** baris `fraud` dan **0 dari 24** baris `review` memuat "rasio" sama sekali. Hanya 3 baris menyebut tarif eksplisit (KLM121 4x, KLM123 2,6x, KLM019 5,6x) tanpa kolom acuan. Dengan demikian L348 menyatakan kemampuan deteksi yang tidak memiliki jejak perhitungan per klaim - persis yang `04` L38 (E-11) tandai "Belum dapat direproduksi per klaim" dan yang `00` L39 akui sendiri. Catatan kehati-hatian: uji subset-sum menunjukkan Rp507.370.000 **dapat** diekspresikan sebagai penjumlahan sebagian nilai `Biaya Rp` baris fraud (contoh: total fraud 561.150.000 − 507.370.000 = 53.780.000 = KLM007 15.500.000 + KLM107 4.350.000 + KLM112 4.280.000 + KLM115 2.150.000 + KLM121 27.500.000). Ini **bukan** bukti fabrikasi; ini bukti bahwa nilai tersebut dapat dibangkitkan dari data, sehingga yang hilang adalah jejak audit, bukan nilai.
- **H-13 (HIGH)** - `13-archive-deep-research.md` L3: "Kasus yang di report oleh BPJS tahun 2024 melibatkan 3 rumah sakit swasta di jawa tengah dan sumatra utara dengan total kerugian mencapat RP25 miliar." Klaim kuantitatif ini tidak memiliki entri di `dataset_research_live.csv` (33 entri, sudah diperiksa satu per satu) maupun ID register E-01..E-12 di `04` L28–L39, dan tidak ada di matriks bukti `06` L38–L45. Dampak: satu-satunya klaim kuantitatif dalam arsip tidak dapat ditelusuri ke sumber mana pun.
- **I-1 (INFO)** - Tidak ada dokumen kendali yang menyematkan status "Tervalidasi" pada field statusnya sendiri; seluruh pelanggaran "Tervalidasi" berada pada arsip/agregat dan pada basis data riset. Pelanggaran ini adalah masalah pen-copyan konten, bukan masalah status dokumen.

## 6. Perodoxy Angka Rekonsiliasi

Data sumber: `N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv` (300 baris, 29 kolom = 27 kolom data + `_notion_page_id` + `_last_edited`), dikonfirmasi silang dengan `claims_v2_live.json` (300 record, 29 key) dan `dataset_research_live.csv` (33 baris).

### 6.1 Tabel utama `00-dashboard.md` §3 (L29–L38)

| Indikator | Diklaim (sumber) | Dihitung ulang | ✓/✗ |
|---|---|---|---|
| Jumlah baris aktif = 300 klaim | `00` L30 | 300 baris | ✓ |
| Rentang ID KLM001–KLM300 | `00` L31 | 300 ID unik, min KLM001, max KLM300, tanpa celah | ✓ |
| auto_clear = 240 | `00` L32 | 240 | ✓ |
| review = 24 | `00` L33 | 24 | ✓ |
| escalate = 36 | `00` L34 | 36 | ✓ |
| Total nominal Rp3.526.650.000 | `00` L35 | 3.526.650.000 | ✓ |
| **Kolom LOS hari kosong = 109 baris** | `00` L36; `03` L78 | **0 baris kosong; 109 baris bernilai `0`** (`claims_v2_live.json`: 0 null, 0 string kosong, 109 = 0) | **✗** |
| Alasan kosong = 1 baris | `00` L37; `03` L79 | 1 (KLM031; status auto_clear, risiko low, LOS 8) | ✓ |
| Catatan riset = 33 entri | `00` L38 | 33 baris di `dataset_research_live.csv` | ✓ |

### 6.2 Angka silang antar dokumen

| Indikator | Diklaim (sumber) | Dihitung ulang | ✓/✗ |
|---|---|---|---|
| Risiko low/medium/high/fraud = 240/10/14/36 | `01` L37; `03` L25–L28 | 240/10/14/36 | ✓ |
| Nominal auto_clear / review / escalate | `01` L67–L69; `03` L33–L35: Rp2.685.550.000 / Rp279.950.000 / Rp561.150.000 | identik | ✓ |
| Modus kosong = 240 | `03` L80 | 240 | ✓ |
| Sindikat kosong = 264 | `03` L81 | 264 | ✓ |
| Status verifikasi = Terverifikasi 18 / Sebagian 11 / Perlu 4 | `04` L12–L14 | 18/11/4 | ✓ |
| Relevansi = Kritis 11 / Tinggi 18 / Pendukung 4 | `04` L15–L17 | 11/18/4 | ✓ |
| Overcharge Rp507.370.000 belum direproduksi | `00` L39; `04` E-11 L38 | Benar tidak dapat direproduksi: tidak ada kolom tarif; 72 baris punya "rasio", semuanya `low`; total kelebihan yang dapat dihitung Rp32.414.500; 0 baris fraud/review punya rasio | ✓ (pengakuan jujur) |
| 8 klaim kontradiksi | `09` L110; `10` L203 | **12 baris** `Kontradiksi Narasi` = true: KLM001–KLM006, KLM018, KLM024, KLM105–KLM108 | **✗** |
| Ground truth anomali = KLM001–KLM024 | `10` L8; `08` L20 | 36 baris `fraud`; **22 di antaranya di luar KLM024** (KLM101–KLM122, termasuk KLM115, KLM121, KLM122). Anomali (medium+high+fraud) memang 24 dan semuanya di KLM001–KLM024 | **✗** (untuk fraud) |
| 100 klaim: risiko 76/4/6/14, sentimen 62/14/24 | `09` L111, L222; `10` L7 | Pada KLM001–KLM100: risiko 76/4/6/14, sentimen 62/14/24 | ✓ |
| Skala risiko "di atas 0.8 = fraud" | `09` L116; `10` L9 | KLM115 Skor Fraud 0.80 berlabel `fraud` | **✗** (kasus batas) |
| Entitas v2.1: 10 faskes / 20 dokter / 40 pasien | `09` L149–L151 | 10 faskes unik, 20 dokter unik, 40 pasien unik | ✓ |
| Entitas 20P / 12D / 6RS | `09` L121–L123, L221; `10` L6; `11` L397 | 40/20/10 | **✗** |
| `11` L321: "31 fitur standar INA-CBG/FHIR R4" | `11-archive-proposal.md` L321 | Ekspor aktif punya 27 kolom data | **✗** |
| `11` L344: "Klaim Normal (Auto-Clear) = 240" | `11` L344 | 240 auto_clear memuat 240 `low` secara angka, tetapi `01` L37 dan `03` L30 menegaskan 264 non-fraud ≠ normal (10 medium + 14 high) | **✗** (klasifikasi) |
| `11` L348: 60,32% dari Rp841.100.000 | `11` L348 | 507.370.000 / 841.100.000 = 60,32% ✓ aritmetika; 841.100.000 = 279.950.000 + 561.150.000 ✓ | ✓ (aritmetika) |
| `11` L348: rata-rata Rp8.456.167 per klaim | `11` L348 | 507.370.000 / 60 = 8.456.166,67 ✓ aritmetika | ✓ (aritmetika) |
| `11` L344–L346: 76,15% / 7,94% / 15,91% | `11` L344–L346 | 2.685.550.000 / 3.526.650.000 = 76,15%; 279.950.000 = 7,94%; 561.150.000 = 15,91% | ✓ (aritmetika) |
| `11` L346: Rp394.950.000 overcharge pada 36 escalate | `11` L346 | Tidak dapat direproduksi (lihat B-4) | **✗** |
| `11` L345: Rp112.420.000 koreksi pada 24 review | `11` L345 | Tidak dapat direproduksi | **✗** |
| `11` L350: SUS 82,5 | `11` L350 | Tidak ada artefak uji pengguna di korpus; `00` L49 Anxietymemasukkan masukkan daftar belum boleh | ✗ |
| `13` L3: RP25 miliar | `13` L3 | Tidak ada entri register/sumber | **✗** |
| `07` L35: PSTV18 kosong 133.228 peserta; `07` L47: PNK02 4.939 nilai unik | `07` L35, L47 | Berkas `.dta` tidak ada di korpus - tidak dapat diverifikasi lokal | ? (INFO-2) |

### 6.3 Temuan turunan

- **B-1 (BLOCKER)** - `00-dashboard.md` L36 "109 baris" dan `03-dataset-registry.md` L78 "109 baris memiliki kolom LOS hari kosong" adalah salah faktual pada tabel yang dijuluki "Fakta Dataset yang Telah Direkonsiliasi". Data sebenarnya: 0 baris kosong, 109 baris bernilai `0`, dikonfirmasi di dua ekspor (`claims_v2_live.csv` dan `claims_v2_live.json`, yang menunjukkan 0 null dan 109 nilai nol). Konsekuensi berantai: (1) butir P1-2 (`00` L66 "Selesaikan data dictionary dan perlakuan nilai LOS kosong") berpijak pada kondisi yang tidak ada; (2) `03` L82 membenarkan perlakuan kosong sebagai "mungkin tidak berlaku" - tidak dapat dibedakan dari nilai 0 yang berarti "rawat jalan tanpa LOS" bila ekspor menyimpan 0; (3) `02-architecture.md` L99 ("data tidak berlaku dibedakan dari data hilang") adalah kriteria penerimaan MVP yang mustahil diuji terhadap data aktif yang tidak merepresentasikan "kosong" sama sekali; (4) `08` L42 memvalidasi periode pada file DM, bukan LOS - tidak ada dokumen yang menetapkan perlakuan nilai 0.
- **H-7 (HIGH)** - `03-dataset-registry.md` §5 (L48–L72) mendefinisikan 24 properti, sedangkan ekspor aktif memiliki 27 kolom data. `Rujukan`, `Alasan Berobat`, dan `Layanan` tidak masuk kamus data; kolom metadata Notion `_notion_page_id` dan `_last_edited` juga tidak. `03` L98 mewajibkan "kamus data" sebagai bagian dari setiap ekspor, sehingga artefak yang diwajibkan memang ada tetapi tidak lengkap.
- **H-8 (HIGH)** - 58 dari 300 baris melanggar `03` L70 ("Sentimen: Harus sesuai dengan definisi skor"): `Sentimen` = `netral` dengan `Skor Sentimen` positif (0,05–0,15). Contoh: KLM278 (0,14), KLM280 (0,12), KLM273 (0,09), KLM272 (0,12), KLM292 (0,09). Subset 100 klaim pertama justru konsisten (62 positif / 14 netral / 24 negatif), sehingga pelanggaran seluruhnya berada pada 200 baris ekspansi v2 - bagian yang tidak pernah melewati pemeriksaan kualitas teroganisasi.
- **H-9 (HIGH)** - `Kontradiksi Narasi` bernilai true pada 12 baris, bukan 8 seperti tertulis di `09-draft-hub.md` L110 ("= 8 klaim") dan `10-simulation-dataset.md` L203 ("8 klaim kontradiksi masuk daftar prioritas"). Empat baris tambahan adalah KLM105–KLM108 - semuanya milik SYND-07 "Iur Biaya" (`09` L143). Karena `03` L60 menyatakan flag ini "Perlu aturan penetapan yang eksplisit", dua sumber berbeda dengan hitungan berbeda pada flag yang sama adalah temuan governance, bukan sekadar salah ketik. Dampak: metrik "8 klaim kontradiksi" pada `10` L203 tidak dapat dipakai sebagai kriteria penerimaan.
- **H-10 (HIGH)** - `09-draft-hub.md` L116 menyatakan "label anomali total 60 (20%)" dengan rincian 36 fraud + 14 high + 10 medium = 60 ✓, tetapi `11-archive-proposal.md` L348 memakai "60 klaim yang ditandai anomali (senilai Rp841,10 Juta)" - Rp841.100.000 adalah total nominal status `review` + `escalate` (24 + 36 = 60 baris), sedangkan anomali menurut label (60 baris) berisi komposisi berbeda (10 medium + 14 high + 36 fraud = 60). Dua himpunan berukuran sama dengan isi berbeda dipakai secara bergantian dalam argumen finansial. (Angka nominalnya sendiri ✓ hitung ulang.)
- **H-12 (HIGH)** - Konflik jumlah entitas: `09-draft-hub.md` L149–L151 (dan `src/components/mhgsl/data.ts` L363+) menyebut 10 faskes / 20 dokter / 40 pasien - cocok dengan hitung ulang (10/20/40 unik). Tetapi `09-draft-hub.md` L121–L123 (dalam blok "✅ Perubahan yang Sudah Diimplementasikan di v2.1") menulis "pasien_id (20 pasien → P01-P40)", "faskes_id (6 FKRTL → RS_A-RS_J)", "dokter_id (12 dokter → D01-D20)" - saling bertentangan dengan L149–L151 di berkas yang sama, dan dengan `10-simulation-dataset.md` L6 serta `11-archive-proposal.md` L397 ("20P, 12D, 6RS"). Dampak desain: LeaveOneGroupOut pada `faskes_id` memerlukan 10 kelompok, bukan 6.
- **H-14 (HIGH)** - `08-training-protocol.md` L8 dan L20 menandai cacat yang benar: deskripsi basis data aktif masih menyebut 100 klaim dan "ground truth KLM001 sampai KLM024", sementara 22 dari 36 baris `fraud` berada di KLM101–KLM122. Yang tidak ada adalah butir closure di `00-dashboard.md` L58–L73 untuk memperbaiki deskripsi itu dan menetapkan definisi label akhir (D-01 di `02` L109 masih "Terbuka"). Konsekuensi: P0-1 (`00` L59 "Tetapkan definisi label fraud-scenario, anomali, dan normal") tidak dapat ditutup sebelum cacat ini ditutup, dan tidak ada artefak yang mengikat keduanya.
- **H-15 (HIGH)** - `11-archive-proposal.md` L344–L345 mengelompokkan `auto_clear` = "Klaim Normal (Auto-Clear)" dan `review` = "Klaim Anomali Suspicious (Audit Review)", menyamakan status alur kerja dengan label risiko - persis yang dilarang `01` L37 ("klaim review tidak otomatis merupakan fraud") dan `03` L30 ("Jangan menyamakan seluruh 264 klaim non-fraud dengan klaim normal"). Dokumen kendali benar; arsip salah, dan arsip inilah yang menyalin ke agregat `14-index.md` L821.
- **H-11 (HIGH)** - `dataset_research_live.csv` tidak memenuhi format entri wajib `04` L57–L69: 12 field disyaratkan (judul, penulis/organisasi, tahun, jurnal, DOI/URL stabil, jenis sumber + **tingkat A–D**, klaim spesifik, kutipan/halaman/tabel, batasan, reviewer + tanggal verifikasi, status + alasan), sedangkan berkas hanya punya 10 kolom dan **tidak memuat kolom tingkat A–D, kutipan, reviewer, maupun tanggal verifikasi**. Akibatnya status `Terverifikasi` pada 18 baris tidak dapat diuji terhadap hierarki `04` L19–L25. Enam baris juga kehilangan `Sumber Riset` (baris 3, 7, 15, 16, 17, 18 - termasuk "Metrik operasional: 20 menit → 3 menit", "Fase 1", "Fase 2", "Federated Learning", "Human-in-the-Loop + Active Learning + DPO", "Fase 3"), dan baris 3 justru memuat klaim operasional 20→3 menit tanpa sumber.
- **H-13 (HIGH)** - lihat §5. Ditambah: `dataset_research_live.csv` baris 2 (SHAP) bersumber Springer (tingkat B, sah) tetapi kolom `Deskripsi`-nya menyajikan angka ilustratif rekaan ("durasi rawat +35% pada skor fraud 92%") yang tidak berasal dari paper - pola yang berulang pada baris 23 ("Contoh atribusi SHAP di dokumen sumber: durasi rawat +35% pada skor fraud 92%"). Angka presentasi seperti ini tidak boleh masuk basis bukti.
- **M-1 (MEDIUM)** - Aturan em-dash `00` L83 ("Dokumen formal tidak menggunakan em-dash") tidak mengatur data. Ekspor `claims_v2_live.csv` memuat 324 em-dash pada 293 dari 300 baris: `Alasan` 160, `Prosedur ICD-9-CM` 156, `Sinyal SHAP` 5, `Obat` 3. Karena `03` §6 "Pemeriksaan Kualitas yang Telah Dilakukan" (L74–L81) tidak memeriksa format, dan `09`/`10`/`11` mengutip nilai `Alasan` mentah, em-dash akan masuk ke dokumen formal begitu kutipan itu dipakai. Tidak ada keputusan terdokumentasi yang mengaturnya; lihat juga §5 untuk kepatuhan corpus `.md` (0 em-dash, compliant).
- **M-9 (MEDIUM)** - `09-draft-hub.md` L135–L147 mendaftarkan 9 sindikat + 2 fraud tunggal, termasuk "Biaya Markup - KLM121 - RS_A - D03 - P04" dan "Drug Diversion - KLM122 - RS_E - D09 - P18", tetapi pada data aktif kedua baris tersebut memiliki `Sindikat` **kosong** (terhitung 264 kosong; KLM121 dan KLM122 termasuk yang kosong) dan `Faskes` KLM121 = RS_G (bukan RS_A seperti tabel L146) serta `Pasien` KLM121 = P04 vs KLM122 = P18. Tabel sindikat di korpus tidak cocok dengan data. `08` L21 meminta kolom adjudikasi (`evidence_source`, `reviewer_1`, `reviewer_2`) untuk setiap kasus; tidak ada satu pun kolom itu di ekspor.
- **M-13 (MEDIUM)** - Keterkaitan database: `03` L84 dan `08` L22/L25 mengeksklusikan `Sinyal SHAP`, `Kontribusi Saluran`, `Modus`, `Sindikat`, `Alasan` dari fitur. Pada data aktif `Sinyal SHAP` dan `Kontribusi Saluran` terisi pada **300/300** baris, `Alasan` pada 299, `Modus` pada 60, `Sindikat` pada 36. Karena `configs/leakage.yaml` tidak ada (B-5), kontrol anti-leakage hanya berupa rekomendasi tekstual tanpa pengaman eksekusi.
- **I-2 (INFO)** - Temuan numerik `07-dataset-v2-catalog.md` (PSTV18 kosong 133.228 pada L35; PNK02 4.939 nilai unik pada L47; rentang tanggal 2014-08-16 pada L48–L50; PNK17=PNK18 pada L63–L64) tidak dapat diverifikasi ulang secara lokal karena berkas `.dta`/`.xlsx` tidak ada di korpus. Nilai-nilai ini harus diperlakukan sebagai belum terverifikasi sampai sumber unduhan dilampirkan - yang sama dengan `03` L98 ("checksum berkas") dan `08` L30 ("hash SHA-256").
- **I-3 (INFO)** - Hasil hitung ulang konsistensi label (yang dihopper H-6) menunjukkan `03` L77 benar secara faktual, tetapi kebenarannya bergantung pada ambang 0,80 inklusif yang tidak pernah ditulis. Ini bukan pelanggaran, melainkan celah dokumentasi yang menutupi potensi kontradiksi.

## 7. Rekomendasi Terurut

Prioritas P0 (harus selesai sebelum dokumen diserahkan; kriteria penyelesaian, ditulis dalam kurung):

1. **Perbaiki baris LOS di `00-dashboard.md` L36 dan `03-dataset-registry.md` L78, dan ganti seluruh bahasa "kosong" dengan bahasa yang representatif** - menyebut bahwa 109 baris bernilai `0` dan 0 baris kosong, atau memperbaiki ekspor agar `null` tersimpan sebagai null (`00` L36; `03` L78; `08` L41; `02` L99).
2. **Tambah blok metadata (status baku, versi, tanggal, tujuan, dokumen induk) dan judul ke `07` dan `08`; ubah 6 status bebas menjadi nilai dari kosakata `00` L90; samakan nama field tanggal; tambahkan changelog versi pada 01, 04, 05, 06, 07, 08** (kriteria: setiap dokumen kendali memiliki 5 field terisi, status ∈ 5 nilai baku, dan tabel changelog dengan ≥1 baris).
3. **Operasikan gerbang `04` §9 pada `14-index.md`: pasang banner tingkat berkas yang menyatakan agregat ini historis dan menautkan ke versi terkendali, atau keluarkan dari korpus** (kriteria: setiap kemunculan "Tervalidasi"/"Terbukti" pada `14-index.md` berada di dalam blok ber-banner yang eksplisit; L801–L805, L821, L823, L877, L505).
4. **Bubarkan basis data riset: turunkan status baris bersumber level C/D, lengkapi 12 field wajib `04` L57–L69, dan karbonkan 6 baris tanpa sumber** (kriteria: 0 baris berstatus `Terverifikasi` dengan sumber level C/D tanpa sumber primer pendukung; 0 baris tanpa sumber; 33 baris punya tingkat A–D, reviewer, dan tanggal verifikasi).
5. **Hapus atau turunkan klaim finansial arsip `11` L344–L348 dan `14-index.md` L821–L824 menjadi "perkiraan belum dapat direproduksi"** (kriteria: tidak ada lagi "Overcharge Terbukti", "Penyelamatan Riil", atau "membuktikan" di mana pun yang merujuk Rp507.370.000 / Rp394.950.000 / Rp112.420.000).

Prioritas P1:

6. **Tulis closure criteria terukur untuk 13 item P0/P1/P2** - minimal satu angka, nama artefak, atau tenggat per item; tambahkan P0-6 "Perbaiki deskripsi basis data aktif (100 klaim → 300 klaim) dan definisi ground truth" (kriteria: setiap item P0/P1/P2 punya ≥1 kriteria terukur; 13/13 tercentang).
7. **Tetapkan ambang label secara tertulis dan konfirmasi** (kriteria: satu tabel ambang di `03` §4; 0 baris berada di luar rentang tabel itu).
8. **Perbaiki kamus data `03` §5 agar mencakup 27 kolom data + 2 kolom metadata, dan tetapkan aturan konsistensi `Sentimen`/`Skor Sentimen` yang dapat diuji** (kriteria: 27/27 kolom terdefinisi; 0 baris `netral` dengan skor positif setelah redefinisi).
9. **Selaraskan hitungan `Kontradiksi Narasi` antara `09` L110, `10` L203, dan data (12 baris), dan tetapkan aturan penetapannya** (kriteria: satu angka, satu sumber, satu aturan).
10. **Selaraskan tabel sindikat `09` L135–L147 dengan data aktual** (Faskes/Pasien/Sindikat KLM121–KLM122) (kriteria: 36 baris fraud terpetakan ke sindikat dengan Faskes/Pasien yang cocok).
11. **Tambahkan sitasi bibliografis lengkap untuk XGBoost, GNN, SHAP, dan evaluasi kelas tidak seimbang ke `01` §Referensi sesuai `04` L48–L56** (kriteria: setiap metode yang disebut punya sitasi dengan penulis, tahun, dan DOI/URL stabil).
12. **Tetapkan unit Lookup: rekonsiliasi satu sumber angka tunggal** - pertahankan tabel `00` §3 sebagai satu-satunya sumber angka, danhilangkan angka duplikat dari `01` L66–L70, `03` §3, dan `11` L344–L348 (kriteria: 1 kemunculan per angka di korpus).

Prioritas P2:

13. **Buat `configs/leakage.yaml`, `manifest.json`, `label_audit.csv`, `data_quality_report.md`, `train.py`, `metrics.json`, `evaluation_report.md`, `review_log.csv` sesuai `08` L30–L35 dan `02` L77–L86, atau turunkan UI yang mengutip `configs/leakage.yaml`** (`src/components/mhgsl/data.ts` L363; `i18n.tsx` L470, L817) (kriteria: 8/8 artefak ada di repo, atau 3 rujukan UI dihapus).
14. **Dokumentasikan perlakuan nilai LOS `0` dan tetapkan status `not_applicable`/`unknown`/hilang** sebagai bagian dari kamus data (kriteria: kamus data menyatakan makna 0; P1-2 tercentang).
15. **Lengkapi `dataset_research_live.csv` dengan kolom DATE, tahun, penulis, tingkat A–D, reviewer, tanggal verifikasi, kutipan** dan hapus angka presentasi rekaan pada baris 2 dan 23 (kriteria: 33 baris lengkap per `04` L57–L69).
16. **Beri banner "induk tidak terkendali" pada `09`–`13` dan perjelas peran `14-index.md` sebagai agregat** (kriteria: setiap berkas arsip punya banner di 5 baris pertama yang menyebut naskah terkendali pengganti).



17. **Perbaiki kebocoran literal Notion** `{'type': 'emoji', 'emoji': '💡'}` di `07` L4, `08` L5, dan berkas arsip (kriteria: 0 kemunculan pola `{'type': 'emoji'` pada dokumen kendali).
18. **Tambahkan unit dan denominator pada header tabel `03` L32–L36 dan `07` Tabel 2/4** (kriteria: setiap tabel memuat kolom satuan/denominator).
19. **Selaraskan statement entitas 20P/12D/6RS vs 40P/20D/10RS** di `09` L121–L123, `10` L6, `11` L397 (kriteria: satu angka berlaku seragam).
20. **Tambahkan baris changelog `00` L87–L88 untuk penambahan 07 dan 08, dan ubah `02` L115 menjadi tabel versi** (kriteria: changelog `00` memuat entri untuk penambahan 07/08).

## Lampiran A - Metode dan Batas Verifikasi

- Semua angka "dihitung ulang" berasal dari `N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv` (300 baris, dibaca dengan `csv.DictReader`), `claims_v2_live.json` (300 record), dan `dataset_research_live.csv` (33 baris). `pandas` tidak tersedia di lingkungan audit sehingga tidak dipakai.
- Uji subset-sum untuk Rp507.370.000 (mitm) dijalankan terhadap 36 nilai `Biaya Rp` berlabel `fraud`; hasilnya dilaporkan di B-4 sebagai temuan ketiadaan jejak audit, bukan sebagai klaim fabrikasi.
- Dokumen yang tidak dapat diverifikasi lokal: seluruh dokumen sumber dataset DM (`.dta`/`.xlsx`) tidak ada di korpus, sehingga temuan `07` §Temuan Kualitas dicatat sebagai INFO-2.
- Tidak ada akses Notion yang dilakukan; seluruh temuan bersumber dari dump lokal.
- Fuente: `00-dashboard.md` adalah sumber kebenaran tata kelola; `04-evidence-matrix.md` §3/§7/§9/§10 adalah sumber kebenaran bukti.

## Lampiran B - Rekapitulasi Temuan

| ID | Severity | Ringkasan | Bukti utama |
|---|---|---|---|
| B-1 | BLOCKER | 109 baris LOS bukan "kosong" melainkan bernilai 0 | `00` L36; `03` L78; ekspor CSV/JSON |
| B-2 | BLOCKER | Register bukti menandai sumber level C/D sebagai "Terverifikasi" | `04` L19–L25, L31; CSV baris 19, 21, 26, 28, 31, 32, 34 |
| B-3 | BLOCKER | `14-index.md` mucous ulang klaim "Tervalidasi"/"Terbukti" tanpa banner tingkat berkas | `14` L5/479/908/1101 vs L505, L801–L805, L817, L821, L823, L877 |
| B-4 | BLOCKER | Overcharge Rp507.370.000 tidak dapat direproduksi, tetapi arsip menyebutnya "Penyelamatan Riil" | `11` L344–L348; `00` L39; `04` E-11 L38; hitung ulang rasio/tarif |
| B-5 | BLOCKER | Artefak wajib `08` L30–L35 / `02` L77–L86 tidak ada di repo; `configs/leakage.yaml` hanya string UI | Repo `N:\HEALTHKATHON\Aegis-JKN`; `data.ts` L363; `i18n.tsx` L470, L817 |
| H-1 | HIGH | Tidak ada dokumen kendali yang memakai kosakata status baku | `00` L90 vs 9 header dokumen |
| H-2 | HIGH | 07 dan 08 tanpa blok metadata; 08 tanpa judul | `07` L3–L4; `08` L3–L5 |
| H-3 | HIGH | 6 dari 9 dokumen tanpa changelog | `01`, `04`, `05`, `06`, `07`, `08` |
| H-4 | HIGH | "Dokumen induk" hanya di 02 | `02` L6; grep `Dokumen induk` |
| H-5 | HIGH | 13 item P0/P1/P2 tanpa closure criteria terukur | `00` L59–L73 |
| H-6 | HIGH | Rekonsiliasi label bergantung ambang 0,80 yang tidak tertulis | `03` L46 vs L77; `10` L9; KLM115 |
| H-7 | HIGH | Kamus data tidak mencakup 3 kolom data + 2 kolom metadata | `03` L48–L72 vs 29 kolom CSV |
| H-8 | HIGH | 58 baris `netral` dengan skor sentimen positif | `03` L70; KLM278, KLM280, KLM273 |
| H-9 | HIGH | Hitungan kontradiksi 8 vs data 12 | `09` L110; `10` L203; KLM105–KLM108 |
| H-10 | HIGH | "60 anomali" dipakai bergantian dengan "60 status review+escalate" | `09` L116 vs `11` L348 |
| H-11 | HIGH | Register riset tidak memenuhi 12 field wajib; 6 baris tanpa sumber | `04` L57–L69; CSV 10 kolom; baris 3, 7, 15, 16, 17, 18 |
| H-12 | HIGH | Konflik jumlah entitas 40/20/10 vs 20/12/6 | `09` L121–L123 vs L149–L151; `10` L6; `11` L397 |
| H-13 | HIGH | Klaim RP25 miliar tanpa entri register/sumber | `13` L3; `14` L1100 |
| H-14 | HIGH | Cacat ground truth KLM001–KLM024 tidak punya butir closure | `08` L20; `00` L58–L73; `02` L109 |
| H-15 | HIGH | Arsip menyamakan auto_clear dengan "normal" | `11` L344 vs `01` L37; `03` L30 |
| M-1 | MEDIUM | 324 em-dash di data, tidak ada keputusan yang mengaturnya | `claims_v2_live.csv` 293/300 baris |
| M-2 | MEDIUM | Literal dict Notion membungkus peringatan privasi | `07` L4; `08` L5 |
| M-3 | MEDIUM | Daftar dokumen terkendali tidak memuat 07/08 | `00` L12–L18 vs L92–L95 |
| M-4 | MEDIUM | Halaman hub tidak menandai versi 100 klaim sebagai versi awal | `00` L22; `03` L15; `10` L4 |
| M-5 | MEDIUM | 5 item terbuka di `05` tanpa kriteria | `05` L72–L77 |
| M-6 | MEDIUM | Tiga kosakata status berbeda dalam satu sistem | `00` L90; `04` L28–L39; CSV `Status Verifikasi` |
| M-7 | MEDIUM | Snapshot 33 entri tanpa anchor versi/ekspor | `04` L10; `03` L91 |
| M-8 | MEDIUM | D-01..D-06 terbuka tanpa tenggat/kriteria | `02` L108–L114 |
| M-9 | MEDIUM | Tabel sindikat tidak cocok dengan data | `09` L135–L147; KLM121, KLM122 |
| M-10 | MEDIUM | 6 nama field tanggal berbeda; 7/08 tanpa tanggal | header 9 dokumen |
| M-11 | MEDIUM | `14-index.md` bukan dokumen terkendali tetapi menyalin utuh 9 dokumen | `00` L92–L95 vs `14` L1122–1857 |
| M-12 | MEDIUM | Kolom leakage terisi penuh tanpa blocklist yang ada | `03` L84; `08` L22; ekspor |
| L-1 | LOW | Tabel tanpa satuan/denominator | `03` L32–L36; `07` Tabel 2/4 |
| L-2 | LOW | Template Python `08` tidak mengikat seed/checksum | `08` L46–L80 |
| L-3 | LOW | "31 fitur" vs 27 kolom data | `11` L321 |
| L-4 | LOW | `13` tanpa metadata, gaya kalimat mentah | `13` L1–L4 |
| I-1 | INFO | Tidak ada dokumen kendali berstatus "Tervalidasi" | §5 |
| I-2 | INFO | Temuan `07` tidak dapat diverifikasi lokal (berkas sumber tidak ada) | `07` L35, L47, L48–L50, L63–L64 |
| I-3 | INFO | Rekonsiliasi label benar hanya pada ambang tak tertulis | `03` L77 |
| I-4 | INFO | 0 dari 37 checkbox korpus tercentang | `00`, `03`, `04`, `05`, `06`, `14` |
