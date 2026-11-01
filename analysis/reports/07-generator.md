# 07 - Audit Reproduksibilitas & Mutu Generator Dataset Sintetis Aegis-JKN

**Tanggal audit:** 22 Oktober 2026
**Data:** `analysis/corpus/claims_v2_live.csv` - 300 baris × 29 kolom
**SHA-256 CSV:** `d6fb95b9fbfb6bf47e9a99bcf57df0e38b00a13758b6d3ac14779e64a6121119`
**Spesifikasi acuan:** `analysis/corpus/10-simulation-dataset.md`, `analysis/corpus/07-dataset-v2-catalog.md`, `analysis/corpus/03-dataset-registry.md`
**Checker:** `analysis/reports/scripts/07_gen.py` (stdlib saja, tanpa pandas) → `analysis/reports/scripts/07_gen_results.json`

> Seluruh angka di laporan ini dapat direproduksi dengan `python 07_gen.py`. Laporan hanya memuat **masalah**; hal yang sesuai spesifikasi tidak dicatat kecuali sebagai pembanding di tabel rekonsiliasi.

---

## 1. Ringkasan Eksekutif

**Dataset 300 klaim ini tidak dapat direproduksi.** Skrip generator yang menghasilkan 300 baris **tidak ada di repositori mana pun** di workspace (`Aegis-JKN`, `mechine-learning-deep-learning`, `colab`). Yang ditemukan hanyalah generator **100 klaim v1** di `colab/Aegis_JKN_FIXX.ipynb` (`build_ground_truth()`), yang **tidak cocok** dengan data yang diaudit: dx, prosedur, LOS, biaya, skor, dan tanggal KLM001–KLM300 semuanya berbeda. Artinya data final adalah hasil **ekspor manual dari Notion**, bukan keluaran program - seed `20260707` yang diklaim di spesifikasi **tidak pernah dipakai** untuk menghasilkan baris data mana pun. Satu-satunya kemunculan nilai itu di workspace adalah `np.random.seed(20260707)` pada `pipeline.py` (fallback 100 baris dummy), `SEED = 20260707` di generator v1 notebook, dan **teks UI** (`Aegis-JKN/src/data/oasis-data.ts` → `seed: 20260707`; `src/components/mhgsl/data.ts` → label "Dataset v2.1 (300 klaim, seed 20260707)") - ketiganya hanya **menyalin/menampilkan** angka seed, tidak pernah memanggilnya untuk membangun 300 baris.

Selain itu ditemukan **ground truth yang saling bertentangan dengan data**: narasi rekam medis pada 6 baris SYND-02 justru **mengkonfirmasi** tindakan yang seharusnya didakwa phantom; 6 baris `anomali_frekuensi` mengklaim 3–5 episode padahal hanya ada 1–2; label sindikat v2.1 (pasien/dokter/faskes/skor) tidak sama dengan data untuk SYND-06 s.d. SYND-09 dan kedua fraud tunggal.

### Tabel severity

| Severity | Jumlah aturan gagal | Contoh utama |
|---|---|---|
| CRITICAL | 9 | Ground truth phantom-billing dibantah narasi (KLM004–006); episode anomali tidak ada (6 baris); seed/version/timestamp tidak ada di dataset; 9/9 artefak v2.1 hilang; generator tidak ada di repo |
| HIGH | 7 | Kontribusi Saluran ≠ Skor Fraud pada 42/300 baris; 46 baris low+prosedur tanpa angka rasio; narasi hanya 40 nilai unik untuk 300 baris; tidak ada kolom tarif acuan |
| MEDIUM | 7 | 28 baris rawat inap memuat literal `undefined`; 58 baris "netral" punya skor ≠ 0; 8 baris LOS tidak sinkron dengan jenis layanan; 1 baris Alasan kosong |
| LOW | 1 | KLM031 Alasan kosong (sudah didokumentasikan di registry §6) |
| **Total** | **24** (dari 53 aturan; 29 lulus) | |

**Rekonsiliasi spesifikasi vs data:** **18 ✓ OK / 3 ✗ SELISIH / 2 INFO** dari 23 metrik.

---

## 2. Generator: Ada di Repositori? + Parameter yang Hilang

### 2.1 Generator 300 baris tidak ada di repo - TEMUAN

| Lokasi yang diperiksa | Isi | Hasil |
|---|---|---|
| `Aegis-JKN/` (Next.js) | `src/data/notion-datasets.ts` berisi **300 objek klaim hard-coded** (9.404 baris TS, 451.132 karakter) dengan KLM001–KLM300; `src/data/oasis-data.ts`; `tests/` hanya berisi 3 skrip shell runtime | **Bukan generator** - data statis yang di-hardcode, tidak ada kode yang membentuknya |
| `mechine-learning-deep-learning/backend/src/data/pipeline.py` | satu-satunya `np.random.seed(20260707)` (line ~103) ada di dalam `_generate_fallback_dataset()` yang menghasilkan **100 baris dummy konstan**, bukan 300 baris | Bukan generator |
| `mechine-learning-deep-learning/notebooks/Aegis-JKN.ipynb` | `load_claims_dataset()` membaca CSV dari disk atau **memulihkan payload base64+gzip** yang di-embed di dalam notebook | Menyimpan output, bukan menghasilkan output |
| `mechine-learning-deep-learning/datasets/claims_300_v2.1.csv` | 300 baris, 31 kolom snake_case (`claim_id` … `is_fraud`), SHA-256 `37cf22369ebf7a3c616219cb49b9c4406f00d75286b38cbf6c08b844e27fd4e8` | **Konten identik** dengan CSV corpus (hanya `sindikat`=`none` vs `""`, `kontradiksi_narasi` 1/0 vs True/False, dan `catatan` tidak ikut diekspor) - ini **hasil**, bukan sumber |
| `colab/Aegis_JKN_FIXX.ipynb` | `build_ground_truth()` membuat **100** klaim v1 deterministik dengan `SEED = 20260707` | **Hanya generator v1 (100 baris)**, dan hasilnya tidak sama dengan CSV corpus (lihat 2.3) |
| `Aegis-JKN/src/data/oasis-data.ts`, `src/components/mhgsl/data.ts` | `seed: 20260707` pada metadata Oasis dan label UI "Dataset v2.1 (300 klaim, seed 20260707)" | **Hanya teks/metadata** - seed disalin ke UI, tidak dipakai membangkitkan baris |

**Bukti ketidakcocokan v1:** `build_ground_truth()` menetapkan KLM004 = dx `S72.0` / proc `81.52` / biaya 46.500.000 / skor 0.92; CSV corpus KLM004 = dx `S72.0` / proc `81.52` / biaya **44.750.000** / skor 0.92. KLM013 di notebook: proc `51.23`, biaya 3.200.000, qty 24, LOS 2; di corpus: proc **—**, biaya **9.450.000**, qty insulin 30, LOS **0**. KLM015 notebook: dx `E11.9`/proc `51.23`/LOS 2/biaya 1.100.000; corpus: dx `J18.9`/proc **—**/LOS **14**/biaya **8.900.000**. Dengan kata lain, **baris dengan ID sama tidak berisi klaim sama** - ID hanya kebetulan berurutan.

**Konsekuensi:** `03-dataset-registry.md` §8 ("Setiap ekspor dataset harus mencantumkan … checksum berkas … seed dan versi kode") **tidak dapat dipenuhi** karena tidak ada seed yang dipakai dan tidak ada checksum yang dilampirkan.

### 2.2 Di mana seed / versi / checksum seharusnya hidup (dan tidak ada)

| Artefak | Lokasi yang disyaratkan spec v2.1 | Status |
|---|---|---|
| Kolom `seed`, `version`, `timestamp` | `data/raw/claims_300_v2.1.csv` (spec: "+ kolom pasien_id, faskes_id, dokter_id, seed, version, timestamp") | **Hilang** - CSV corpus punya 29 kolom, tidak ada satu pun bernama seed/version/timestamp. Kolom penanda yang ada hanya `_notion_page_id` dan `_last_edited` (artefak ekspor Notion, bukan metadata dataset) |
| `data/processed/metadata.json` | Struktur file v2.1 | **Hilang** - tidak ada file `metadata.json` di bawah `N:\HEALTHKATHON` mana pun |
| Berkas checksum (`.sha256` / `CHECKSUMS.txt`) | `03-dataset-registry.md` §8 butir 4 | **Hilang** - tidak ada berkas checksum di workspace |
| `configs/leakage.yaml` | Struktur file v2.1 (blokir kolom leakage) | **Hilang** dari `Aegis-JKN/` (hanya ada `src/`, `prisma/`, `tests/` shell runtime) |
| `tests/test_leakage.py` | Struktur file v2.1 (unit test anti-leakage) | **Hilang** - `Aegis-JKN/tests/` berisi `database-runtime-build.sh`, `python-runtime-build.sh`, `python-runtime-container.sh` saja |
| `data/raw/edges_v2.1.json`, `data/raw/text_gt_v2.1.csv`, `data/raw/leakage_blocklist.yaml`, `data/processed/features_300.parquet`, `data/processed/graph_hetero.pt` | Struktur file v2.1 | **Hilang** - 0 dari 5 ada |

Total **9 dari 9** artefak wajib struktur v2.1 tidak ada.

### 2.3 Parameter yang hilang + inferensi generator per kolom non-trivial

Kolom yang isinya bisa diregenerasi hanya bila parameter berikut diketahui. Kolom "Biaya Rp" dan "Tanggal" sengaja tidak diuraikan karena deterministiknya jelas (lihat baris 2.3.1).

| Kolom | Parameter yang hilang | Inferensi dari 300 baris | Bisakah direplikasi? |
|---|---|---|---|
| `Skor Fraud` | rumus komposisi skor + bobot kanal | 46 nilai unik. Syndikat punya skor **bertangga tetap**: SYND-01 = 0.93/0.94/0.95, SYND-02 = 0.92/0.93/0.94, SYND-03 = 0.85–0.87, SYND-04 = 0.86/0.88, SYND-05 = 0.78/0.79, SYND-06 = 0.89–0.92, SYND-07 = 0.82–0.85, SYND-08 = 0.86–0.89, SYND-09 = 0.80–0.84. Baris `low` = 0.04–0.14 (11 nilai), `medium` = 0.40–0.53, `high` = 0.62–0.79, `fraud` = 0.80–0.95 | **Tidak** - skor ditulis manual per kasus skenario, tidak ada formula dari fitur |
| `Kontribusi Saluran` | rumus T/F/S dan cara pembulatan | Format `T a · F b · S c`. Untuk baris low, T/F/S ≈ 0.01–0.05 dan totalnya **tidak sama** dengan `Skor Fraud` pada 42/300 baris (mis. KLM133 total 0.32 vs skor 0.44; KLM129 0.55 vs 0.72). Total yang berulang konstan (0.32 ×6, 0.55 ×8, 0.80 ×5, 0.86 ×4) → nilai kanal ditulis dari templat, bukan diturunkan dari skor | **Tidak** - tidak ada aturan pembulatan yang menghasilkan 42 selisih |
| `Sinyal SHAP` | metode penjelasan (SHAP TreeExplainer/GradientSHAP) + ambang "sinyal dominan" | 240 dari 300 baris (semua baris `low`) berisi teks literal identik `"tidak ada sinyal dominan"`; hanya 60 baris anomali/fraud yang punya teks. Tidak ada nilai SHAP numerik per fitur | **Tidak** - string konstan, bukan keluaran model XAI |
| `Alasan` | templat per modus + parameter angka (rasio, Nx median, jumlah episode, hari) | 211 nilai unik dari 300 baris; setelah semua angka diganti `N` tersisa **51 templat**. 5 templat teratas mencakup 54+23+21+20+19 = 137 baris (45,7%). Klaim "rasio 1.03" ternyata = `Biaya / tarif paket` yang **ditabulasi manual** | **Tidak** - tarif acuan tidak ada di dataset (lihat R15) |
| `Alasan` - 3-tingkat | ambang/definisi tiap tingkat | NORMAL 239 (bukan 240), ANOMALI SEDANG 10, ANOMALI TINGGI 14, FRAUD 36, kosong 1 → total 300. Prefix `FRAUD (…)` memuat nama modus; `ANOMALI TINGGI (belum tentu fraud)` 14 baris | **Sebagian** - Ambang label `Risiko` terkunci (0.35/0.60/0.80) tapi prefix textual `ANOMALI SEDANG`/`TINGGI` tidak punya definisi tertulis |
| `LOS hari` | distribusi LOS per (dx, proc) | 12 nilai unik (0,1,2,…,9,12,14). Untuk dx tanpa prosedur, LOS = **median LOS grup dx** (mis. E11.9→0, J18.9→5, K35.8→3). 163/300 baris persis sama dengan median dx. Tapi 20 baris memakai templat hard-coded "LOS N hari = median dx" yang angkanya disalin dari kolom LOS, bukan dari median kelompok - 13 dari 20 salah (lihat 5.2) | **Tidak** - templat teks dan angka LOS tidak sinkron |
| `Obat` |Fq sampling obat per dx + satuan + dosis | 10 kode obat M01–M10, satuan `vial`/`tablet`/`pen isi ulang`, kuantitas per episode. Tidak ada baris obat untuk dx yang tidak butuh obat (mis. S72.0 fraktur) - konsisten dengan aturan "M09 insulin tidak untuk sprintf non-DM" | **Sebagian** - pola klinis konsisten, parameter dosis/random draw tidak terdokumentasi |
| `Narasi Rekam Medis` | generator narasi per diagnosis | **40 narasi unik untuk 300 baris (13,3%)**; 16 narasi untuk 240 baris `low`. Narasi ditentukan oleh dx saja (13 dx → 40 narasi, bukan 300). Angka dalam narasi ("138/84", "HbA1c 7,1") **tidak muncul di kolom mana pun** - 182 baris tanpa angka sama sekali | **Tidak** - narasi bertemplat per dx, bukan per pasien |
| `Kontradiksi Narasi` | aturan penetapan flag | 12 baris `True` (spec menyebut 8). Tidak ada kolom/tabel aturan yang mendefinisikan syarat flag | **Tidak** |
| `Umpan Balik Pasien` | generator umpan balik + aturan sentimen | 36 nilai unik; template teratas dipakai 39× ("Proses administrasi mudah dan ruangan bersih."). `Skor Sentimen` = nilai numerik dari template kata (positif/netral/negatif) | **Sebagian** |
| `Sentimen` | ambang `Skor Sentimen` → kategori | 58 baris kategori `netral` punya skor **≠ 0** (rentang 0,05–0,15); tidak ada ambang tertulis yang menentukan "netral" | **Tidak** |
| `Rujukan` | generator rujukan FKTP | 188 nilai unik, tapi 28 baris rawat inap memuat literal **`undefined`** (serialisasi JS yang gagal) | **Tidak** |
| `Biaya Rp` | tarif acuan + faktor pengali per modus | 140 nilai unik. Biaya low ≈ tarif paket (mis. 7.500.000 vs tarif 8.200.000 → rasio 0.91); baris fraud = 1,5×–4× tarif. **Tabel tarif acuan hanya ada di dokumen Notion**, tidak di dataset | **Tidak** - tarif acuan tidak ada di artefak data |
| `Tanggal` | generator tanggal (distribusi per bulan/pasien) | 138 tanggal unik pada 2026-01-01 … (rentang 2026). Tanggal sindikat sengaja dikunci (SYND-02 identik 3 baris, SYND-03 berpasangan) | **Sebagian** |
| `Status`, `Risiko` | ambang skor → label | Konsisten 300/300: <0.35 low, 0.35–0.60 medium, 0.60–0.80 high, ≥0.80 fraud (fraud mulai tepat di 0.80) | **Ya** |
| `Pasien`, `Dokter`, `Faskes` | tabel entitas + afiliasi | 40 pasien, 20 dokter, 10 faskes, ID konsisten; 1 dokter = 1 faskes | **Ya** |

---

## 3. Tabel Rekonsiliasi Spesifikasi vs Data Aktual

Sumber: `07_gen_results.json` → `reconciliation`.

| Entitas/Metrik | Diklaim di spec | Aktual | Selisih | Verdict |
|---|---|---|---|---|
| Jumlah baris | 300 (v2/v2.1) | 300 | 0 | ✓ OK |
| Kelengkapan ID KLM001–KLM300 | 300 ID lengkap, unik | 300 unik, 300/300 ada | 0 | ✓ OK |
| Distribusi Risiko | fraud 36 / high 14 / medium 10 / low 240 | fraud 36 / high 14 / medium 10 / low 240 | 0 | ✓ OK |
| Distribusi Status | escalate 36 / review 24 / auto_clear 240 | escalate 36 / review 24 / auto_clear 240 | 0 | ✓ OK |
| **Jumlah modus** | **14 modus** | **13 modus** | **−1** | ✗ SELISIH |
| Jumlah sindikat | SYND-01..SYND-09 (9) | 9 (SYND-01 … SYND-09) | 0 | ✓ OK |
| Layanan | tidak dinyatakan di spec | rawat inap 189 / rawat jalan 111 | - | ℹ INFO |
| Rentang Biaya Rp | tidak dinyatakan di spec | min 700.000 / maks 63.500.000 / total 3.526.650.000 | - | ℹ INFO |
| **Rentang LOS hari** | registry §6 klaim **109 baris LOS kosong** | min 0 / maks 14; **109 baris bernilai 0**, 0 baris benar-benar kosong | 109 | ✗ SELISIH |
| Entitas Faskes | RS_A–RS_J (10 FKRTL) | 10 | 0 | ✓ OK |
| Entitas Pasien | P01–P40 (40) | 40 | 0 | ✓ OK |
| Entitas Dokter | D01–D20 (20) | 20 | 0 | ✓ OK |
| Entitas Diagnosis | 10 kode v1 + I10, J45.9, N39.0 (13) | 13 | 0 | ✓ OK |
| Entitas Prosedur | 8 kode terpakai; 36.13 & 93.90 tidak terpakai di v1 | 8 (00.66, 47.09, 51.23, 53.1, 74.1, 81.52, 96.04, 98.51) | 0 | ✓ OK |
| Entitas Obat | M01–M10 (10) | 10 | 0 | ✓ OK |
| **Kontradiksi Narasi = True** | **8 klaim** (spec §Analisis Teks & Sentimen; kriteria v2.1 §7) | **12** (KLM001–006, KLM018, KLM024 + KLM105–108) | **+4** | ✗ SELISIH |
| Distribusi Sentimen | v1: 62 positif / 14 netral / 24 negatif | v1: 62 pos / 14 net / 24 neg; total 300: 170/58/72 | 0 (v1) | ✓ OK |
| v1 jumlah klaim per faskes | RS_A19 RS_B13 RS_C10 RS_D10 RS_E22 RS_F26 | identik | 0 | ✓ OK |
| v1 jumlah klaim per pasien | 5/5/5/4/5/4/5/5/4/5/5/5/6/6/7/5/5/4/5/5 | identik | 0 | ✓ OK |
| v1 jumlah klaim per dokter | D01 2 D02 8 D03 9 D04 9 D05 10 D06 0 D07 13 D08 18 D09 14 D10 8 D11 1 D12 8 | identik | 0 | ✓ OK |
| v1 jumlah klaim per diagnosis | 10/11/8/8/9/15/8/10/8/13 | identik | 0 | ✓ OK |
| v1 jumlah klaim per prosedur | 12/11/8/10/1/10/3/8 | identik | 0 | ✓ OK |
| Kesesuaian label Risiko vs rentang skor | low<0.35, medium 0.35–0.6, high 0.6–0.8, fraud>0.8 | 300/300 konsisten | 0 | ✓ OK (catatan: batas bawah 0.80 masuk fraud, berbeda redaksi spec v1) |

**Total: 18 ✓ / 3 ✗ / 2 ℹ.**

Tiga selisih dijelaskan:
1. **Jumlah modus 13 vs 14** - spec v2.1 menyebut "14 modus"; data hanya memuat 13: `anomali_frekuensi, biaya_markup, cloning, drug_diversion, excessive_usage, iur_biaya, overbilling, phantom_billing, prolonged_stay, readmission_berulang, repeat_billing, unbundling, upcoding`. Modus yang tidak ada, sementara v1 memakai label `Anomali`/Prolonged Stay yang disatukan menjadi 4 modus (`anomali_frekuensi`, `overbilling`, `prolonged_stay`). Spec sendiri tidak pernah mendaftar 14 nama modus secara eksplisit → target 14 tidak dapat diverifikasi.
2. **109 baris "LOS kosong"** - registry §6 menyatakan 109 baris punya `LOS hari` kosong; pada CSV aktual **nilai kosong tidak pernah ada** (`min 0`), 109 baris bernilai `0`. Encoding "tidak berlaku" dan "nihil" tercampur, melanggar aturan kualitas registry §5 ("Nilai tidak berlaku dibedakan dari kosong").
3. **Kontradiksi Narasi 12 vs 8** - 4 baris tambahan adalah KLM105–KLM108 (SYND-07 iur biaya) yang di-flag `True`; spec §7 v2.1 tetap menyebut "8 klaim kontradiksi", dan kriteria keputusan "Saluran Teks: 8 klaim kontradiksi masuk daftar prioritas" jadi tidak terpenuhi secara konsisten.

---

## 4. Audit Sindikat per Sindikat

Sumber: `07_gen_results.json` → `syndicate_audit`, `fraud_tunggal_audit`.

| Sindikat | Modus | Klaim | Faskes | Dokter | Pasien | Skor spec | Skor aktual | Verdict |
|---|---|---|---|---|---|---|---|---|
| SYND-01 | upcoding | KLM001–003 ✓ | RS_A ✓ | D01,D02 ✓ | P01–P03 ✓ | ≥0.93 | 0.93–0.95 ✓ | OK |
| SYND-02 | phantom_billing | KLM004–006 ✓ | RS_C ✓ | D05 ✓ | P08–P10 ✓ | ≥0.92 | 0.92–0.94 ✓ | OK |
| SYND-03 | unbundling | KLM007–012 ✓ | RS_B ✓ | D07 ✓ | P12–P14 ✓ | 0.84–0.87 | 0.85–0.87 ✓ | OK |
| SYND-04 | drug_diversion | KLM013–014 ✓ | RS_E ✓ | D09 ✓ | P16–P17 ✓ | 0.86–0.88 | 0.86–0.88 ✓ | OK |
| SYND-05 | cloning | KLM016–017 ✓ | RS_F ✓ | D08 ✓ | P19–P20 ✓ | 0.78–0.79 | 0.78–0.79 ✓ | OK |
| **SYND-06** | repeat_billing | KLM101–104 ✓ | RS_G ✓ | D13 ✓ | **P21,P22 (2) ≠ P21–P24 (4)** | 0.85–0.90 | **0.89–0.92** | ✗ GAGAL |
| **SYND-07** | iur_biaya | KLM105–108 ✓ | RS_H ✓ | D14 ✓ | **P23,P24 (2) ≠ P25–P28 (4)** | 0.82–0.87 | 0.82–0.85 | ✗ GAGAL |
| **SYND-08** | readmission_berulang | KLM109–114 ✓ | RS_I ✓ | D15 ✓ | **P25,P26 (2) ≠ P29–P34 (6)** | 0.75–0.80 | **0.86–0.89** | ✗ GAGAL |
| **SYND-09** | excessive_usage | KLM115–120 ✓ | RS_J ✓ | **D19 ≠ D16** | **P27 (1) ≠ P35–P40 (6)** | 0.78–0.83 | **0.80–0.84** | ✗ GAGAL |
| **KLM121** (biaya_markup) | - | - | **RS_G ≠ RS_A** | **D13 ≠ D03** | **P29 ≠ P04** | ≥0.85 | **0.81** | ✗ GAGAL |
| **KLM122** (drug_diversion) | - | - | **RS_H ≠ RS_E** | **D14 ≠ D09** | **P30 ≠ P18** | ≥0.80 | 0.82 | ✗ GAGAL |

**Masalah yang ditemukan:**

1. **4 dari 9 sindikat (SYND-06 s.d. SYND-09) tidak punya anggota sesuai tabel v2.1.** Entitas yang tercatat di spec (P21–P24, P25–P28, P29–P34, P35–P40) **tidak pernah muncul** di baris sindikat terkait: baris sindikat hanya memakai P01–P03, P08–P10, P12–P14, P16–P17, P19–P27. Jumlah baris per sindikat **cocok** (36 = 36, spec 3+3+6+2+2+4+4+6+6) - yang meleset adalah **identitas anggota**, bukan jumlah baris. Untuk SYND-09, dokter pun meleset: spec D16, data D19 (D16 memang ada di dataset, tetapi di 21 baris non-sindikat). Konsekuensi: kriteria keputusan spec "Per-Sindikat: Setiap SYND-01–SYND-09 hit-rate > 0" dan tabel ringkasan sindikat di proposal tidak dapat ditelusuri ke data.
2. **Rentang skor 4 sindikat meleset dari spec**: SYND-06 (0.89–0.92 vs 0.85–0.90), SYND-08 (0.86–0.89 vs 0.75–0.80 - **selisih 0.08**, bahkan label `high`/fraud bergeser), SYND-09 (0.80–0.84 vs 0.78–0.83), SYND-07 (bagian atas 0.85 vs batas 0.87).
3. **KLM121 "4x tarif paket" (spec ≥0.85) berlabel skor 0.81** dan faskes/dokter/pasien ≠ spec. Tarif acuan tidak ada di dataset sehingga klaim "4x" tidak dapat dihitung ulang dari artefak data (lihat R15/R17).
4. **Pasien P28–P40 (13 pasien) tidak pernah menjadi anggota sindikat mana pun**, padahal spec v2.1 mengalokasikan mereka ke SYND-07 (P25–P28), SYND-08 (P29–P34), dan SYND-09 (P35–P40). Di data, P28 dipakai baris `anomali_frekuensi`, P29 baris `biaya_markup` (KLM121), P30 baris `drug_diversion` (KLM122) - ketiganya justru **fraud tunggal** yang di spec harusnya milik sindikat. Artinya spec dan data memakai dua penomoran pasien yang berbeda untuk kelompok yang sama.
5. Yang **sesuai**: 9/9 sindikat berada pada 1 faskes (R25 lulus), tidak ada pasien anggota 2+ sindikat (R26 lulus), dan 5 sindikat v1 (SYND-01 s.d. SYND-05) cocok penuh di semua kolom.

---

## 5. Hasil Checker Modus Fraud

Checker: `07_gen.py` (aturan R1–R40). **53 aturan, 29 lulus, 24 gagal** (9 CRITICAL / 7 HIGH / 7 MEDIUM / 1 LOW).

### 5.1 Aturan yang gagal

| Aturan | Severity | Baris gagal | ID KLM | Ringkasan |
|---|---|---|---|---|
| R2d phantom SYND-02: narasi **tidak** mengkonfirmasi tindakan yang ditagih | CRITICAL | 3/3 | KLM004, KLM005, KLM006 | Narasi berbunyi "Fraktur kolum femur; **dilakukan hemiarthroplasty**… pasien pulang dalam kondisi stabil" - justru **membantah** ground truth phantom. Tidak ada MedicationDispense, tetapi rekam medis menyatakan operasi benar-benar dilakukan |
| R3b unbundling SYND-03: narasi baris intubasi menyebut intubasi | CRITICAL | 3/3 | KLM008, KLM010, KLM012 | Baris prosedur `96.04` (Intubasi endotrakeal) justru bernarasi "Kolelitiasis; **dilakukan kolesistektomi laparoskopik**". Modus unbundling tidak terlihat dari narasi |
| R11 prolonged_stay: LOS > median LOS kelompok dx+proc yang sama | CRITICAL | 1 | KLM129 | LOS 2 vs median grup S72.0/81.52 = 6,5 |
| R11b prolonged_stay: Alasan menjelaskan perpanjangan rawat | CRITICAL | 1 | KLM129 | Alasan menyebut "**dipulangkan 2 hari setelah hemiarthroplasty**" - pemulangan dini, bukan rawat diperpanjang |
| R13 anomali_frekuensi: jumlah episode & rentang hari dalam Alasan cocok dengan data | CRITICAL | 6 | KLM133, KLM126, KLM131, KLM136, KLM132, KLM134 | KLM133 klaim "3 episode dalam 30 hari" → aktual **1 episode**; KLM126 klaim 5 ep/34h → aktual 2 ep/32h; KLM131 klaim 4 ep/28h → aktual 2 ep/span **138h**; KLM136/KLM132/KLM134 klaim 3 ep → aktual 1 ep |
| R13b anomali_frekuensi: ≥2 episode pada pasien sama dalam jendela yang diklaim | CRITICAL | 6 | KLM133, KLM131, KLM136, KLM132, KLM134, KLM135 | Hanya **P15 (KLM020–023)** yang benar-benar punya pola 4 episode/7 hari; sisanya tidak punya episode pendukung |
| R14 "Nx median" dalam Alasan dapat dihitung ulang dari kolom dataset | CRITICAL | 1 | KLM130 | "3x median" tidak dapat dihitung ulang - tidak ada bar pembanding (dx J18.9, layanan rawat jalan, n=0). Dengan median rawat jalan Rp1.050.000 hasilnya 3,67x, bukan 3x |
| R37 kolom seed / version / timestamp ada di dataset | CRITICAL | - | seed, version, timestamp | Tidak ada satu pun kolom tersebut; seed 20260707 & version v2.1 hanya tertulis di dokumen |
| R38 artefak wajib struktur file v2.1 tersedia di repo | CRITICAL | 9/9 | `claims_300_v2.1.csv`, `edges_v2.1.json`, `text_gt_v2.1.csv`, `leakage_blocklist.yaml`, `features_300.parquet`, `graph_hetero.pt`, `metadata.json`, `configs/leakage.yaml`, `tests/test_leakage.py` | Tidak ada yang tersedia di `Aegis-JKN/` |
| R4c drug_diversion SYND-04: ada refill insulin pasien sama berjarak ~7 hari | HIGH | 2 | KLM013, KLM014 | Hanya satu episode insulin per pasien (P16 pada 2026-05-04, P17 pada 2026-05-11) - **tidak ada pola refill mingguan** seperti diklaim spec, dan 2 pasien berbeda bukan "refill" |
| R5c cloning SYND-05: klaim "umur & gender berbeda" dapat diverifikasi | HIGH | 2 | KLM016, KLM017 | Tidak ada kolom umur/gender di 27 kolom data → klaim narasi tidak dapat diverifikasi |
| R15 kolom tarif acuan tersedia di dataset | HIGH | - | - | Tabel Biaya Rujukan hanya ada di dokumen Notion; kolom `tarif` tidak ada di CSV |
| R17 low+prosedur: Alasan memuat angka rasio terukur | HIGH | 46 | KLM080, KLM093, KLM097, KLM086, KLM091, KLM095, KLM060, KLM071, … (20 di antaranya biaya > tarif acuan) | 46 baris menulis "biaya ≈ tarif paket" **tanpa angka rasio**; 20 di antaranya justru melampaui tarif acuan tanpa bukti terukur |
| R18 Kontribusi Saluran T+F+S = Skor Fraud (toleransi 0,005) | HIGH | 42/300 | KLM133, KLM129, KLM111, KLM114, KLM123, KLM118, KLM110, KLM102, … | Total kanal tidak sama dengan skor (selisih sampai +0,17). Total berulang konstan (0.32×6, 0.55×8, 0.80×5, 0.86×4) → kanal ditulis dari templat, bukan turunan Skor Fraud |
| R31 narasi memuat diagnosis & prosedur yang ditagih | HIGH | 5 | KLM013, KLM014 (dx E11.9 tidak disebut); KLM008, KLM010, KLM012 (prosedur 96.04 tidak disebut) | Narasi dan kode billing tidak saling menyebut |
| R34 keragaman narasi ≥1 nilai unik per baris | HIGH | 300 | - | Hanya **40 narasi unik untuk 300 baris (13,3%)**; 16 narasi untuk 240 baris `low` |
| R35 Umpan Balik Pasien tidak didominasi satu template | HIGH | - | - | Template dipakai 39× ("Proses administrasi mudah dan ruangan bersih."); total hanya 36 nilai unik |
| R5c/R12 klaim usia/gender dapat diverifikasi (KLM129 "pasien usia 70 tahun") | MEDIUM | 1 | KLM129 | Tidak ada kolom umur/gender |
| R21 label Sentimen konsisten dengan tanda Skor Sentimen | MEDIUM | 58 | KLM278, KLM280, KLM273, KLM272, KLM292, KLM295, KLM288, KLM270, … | 58 baris kategori `netral` punya skor ≠ 0 (0,05–0,15) tanpa ambang terdokumentasi |
| R22 kolom Rujukan bebas artefak `undefined` | MEDIUM | 28 | KLM278, KLM276, KLM282, KLM268, KLM298, KLM297, KLM295, KLM262, … | Literal `undefined` = serialisasi JavaScript gagal; kode FKTP hilang |
| R23 konsistensi LOS vs jenis layanan | MEDIUM | 8 | KLM089, KLM059, KLM074, KLM029, KLM044 (rajal dengan LOS>0); KLM008, KLM010, KLM012 (rawat inap dengan LOS=0) | Rawat inap dengan LOS 0 tidak mungkin |
| R30 prefix Alasan 3-tingkat FRAUD 36 / ANOMALI 24 / NORMAL 240 | MEDIUM | - | - | Aktual FRAUD 36 / ANOMALI 24 / NORMAL **239** / kosong 1 |
| R28 Alasan terisi untuk semua baris | LOW | 1 | KLM031 | Alasan kosong - sudah didokumentasikan di `03-dataset-registry.md` §6 |

### 5.2 Temuan klinis tambahan (di luar tabel aturan)

- **Templat LOS "= median dx" salah 13 dari 20.** 21 baris menyebut "median dx"; 20 di antaranya memakai kalimat "LOS N hari = median dx" dan angka N **selalu identik dengan kolom `LOS hari`** (20/20), tetapi **hanya 7 baris** yang N-nya sama dengan median LOS kelompok diagnosis. 13 baris salah, semuanya dx J18.9: 7 baris menulis N=4 (KLM281, KLM226, KLM245, KLM188, KLM208, KLM171) dan 6 baris menulis N=6 (KLM197, KLM183, KLM199, KLM207, KLM214, KLM156, KLM142) sementara median J18.9 = 5,0. Baris yang benar (N=5): KLM280, KLM265, KLM279, KLM296, KLM240, KLM203, KLM168. Baris ke-21 (KLM128, dx J45.9) menyebut "median dx" tanpa angka; median J45.9 = 0 dan LOS-nya 0, jadi konsisten. Median LOS per dx: E11.9 = 0, I10 = 0, J45.9 = 0, K29.7 = 0, N39.0 = 0, O80 = 2, K35.8 = 3, K40.9 = 3, K80.2 = 3,0, N20.0 = 3, I21.9 = 5,0, J18.9 = 5,0, S72.0 = 6,5.
- **"Nx median" yang bisa direproduksi hanya 7 dari 8.** Delapan baris mengutip rasio terhadap median: KLM115/116/117/118/119/120 (SYND-09, dx J45.9 rawat jalan) klaim 2x → aktual **2,05x** (median Rp1.050.000, n=15) ✓; KLM128 klaim 3x → aktual **2,95x** (n=14) ✓; KLM130 klaim 3x → **tidak dapat dihitung**, tidak ada bar pembanding rawat jalan dx J18.9 (R14). Klaim "5,6x tarif" (KLM019) dan "2,6x tarif paket" (KLM123) **bukan** rasio median melainkan rasio Biaya ÷ tarif acuan: 38.000.000/6.800.000 = **5,59x** ✓ dan 21.000.000/8.200.000 = **2,56x** ✓ - keduanya benar, tetapi hanya bisa diverifikasi dengan tabel tarif eksternal yang tidak ada di dataset.
- **Angka "rasio" 72 dari 72 dapat dihitung ulang** hanya karena tabel tarif acuan diambil dari dokumen Notion - bukan karena ada di dataset. Dua baris lain (KLM122 "6x kebutuhan klinis", KLM125 "3x kebutuhan rasional") memakai rasio dosis klinis yang tidak punya acuan dan tidak bisa dihitung ulang.
- **Upcoding SYND-01 & 2 fraud tunggal** secara konsisten klinis: dx K29.7 + prosedur 00.66 tanpa obat kardiovaskular (R1 lulus), KLM018 dx E11.9 + PCI tanpa antiplatelet, KLM024 O80 + 74.1 tanpa indikasi seksio. Biaya SYND-01 seragam Rp52.300.000 (bukan tarif paket Rp58.000.000) - konsisten dengan klaim upcoding.

---

## 6. Audit Narasi vs Kode

**Metode:** seluruh 300 baris (bukan sampel 40) dianalisis, karena tidak ada baris yang perlu disampel untuk menghitung keunikan.

| Metrik | Nilai | Problems |
|---|---|---|
| Baris | 300 | - |
| Narasi unik | **40 (13,3%)** | 260 baris memakai narasi yang identik dengan baris lain |
| Narasi unik pada baris `low` | **16** untuk 240 baris (6,7%) | - |
| Narasi unik per diagnosis | 13 dx → total 40 narasi | Narasi ditentukan oleh diagnosis, bukan pasien/episode |
| Umpan Balik unik | 36 | Template teratas 39× (13%) |
| Alasan unik | 211 | 12 unik pada 36 baris fraud; 179 pada 240 baris low |
| Rujukan unik | 188 | 28 baris berisi literal `undefined` |
| Alasan Berobat unik | 18 | - |

**Templat narasi teratas (pemakaian):**

| Narasi | Baris |
|---|---|
| Kontrol DM tipe 2; HbA1c 7,1 persen. Terapi metformin dilanjutkan, edukasi diet dan aktivitas fisik diberikan. | 33 |
| Kolelitiasis; dilakukan kolesistektomi laparoskopik. Toleransi oral baik, pasien pulang dengan kontrol poliklinik. | 32 |
| Apendisitis akut; dilakukan apendektomi. Toleransi oral baik, luka operasi bersih, pasien pulang stabil. | 29 |
| Pneumonia komunitas; antibiotik intravena dan nebulizer. Perbaikan klinis bertahap, pulang setelah perbaikan radiologis. | 28 |
| Reparasi hernia inguinalis dengan mesh. Perawatan post-operatif tanpa komplikasi. | 21 |
| Kontrol hipertensi; tekanan darah 138/84 mmHg. Terapi amlodipin dilanjutkan, edukasi garam diberikan. | 19 |
| Fraktur kolum femur; dilakukan hemiarthroplasty. Mobilisasi dengan fisioterapi, pulang dengan alat bantu jalan. | 14 |
| Asma stabil; diberikan nebulizer dan edukasi teknik inhaler. Kontrol berkala berikutnya. | 13 |
| Infeksi saluran kemih; antibiotik dan anjuran minum banyak. Perbaikan gejala dalam 3 hari. | 13 |
| Gastritis tanpa perdarahan; diberikan terapi PPI. Pasien dianjurkan menghindari kopi dan makanan pedas. | 13 |

**Templat Alasan teratas** (angka diganti `N`): 5 templat pertama mencakup **137 dari 300 baris (45,7%)**:
1. `NORMAL: dx KN ditindaki N - pasangan klinis standar; biaya RpN ≈ tarif paket (rasio N); LOS N hari dalam rentang median; obat dispensed sesuai dx; narasi rekam medis konsisten dengan penagihan; tidak ada kontradiksi` - **54 baris**
2. `NORMAL: dx KN ditangani dengan prosedur N - … biaya RpN dalam rentang tarif paket; …` - 23 baris
3. `NORMAL: dx EN ditangani konservatif tanpa prosedur (sesuai guideline); biaya rawat jalan RpN dalam rentang median; …` - 21 baris
4. `NORMAL: pneumonia (JN) diterapi medis tanpa prosedur invasif - konsisten; biaya RpN dalam rentang; LOS N hari = median dx; obat (antibiotik + nebulizer) sesuai; …` - 20 baris (semua dx J18.9; lihat 5.2)
5. `NORMAL: dx IN ditangani konservatif tanpa prosedur (sesuai guideline); …` - 19 baris

**Masalah yang ditemukan:**

1. **Templat narasi memuat angka yang tidak ada di kolom mana pun.** "tekanan darah 138/84 mmHg" dan "HbA1c 7,1 persen" muncul di 19 dan 33 baris, tapi **tidak ada kolom tekanan darah maupun HbA1c** di 29 kolom dataset. Angka narasi tidak dapat diverifikasi atau diregenerasi dari data → narasi bukan representasi rekam medis, melainkan literal yang disalin.
2. **182 dari 300 baris narasi tidak memuat satu pun angka** - tidak ada kuantisasi episode/LOS/biaya yang bisa diverifikasi.
3. **Narasi bertentangan dengan kode pada 6 baris sindikat** (R3b, R2d) - bukan sekadar duplikasi template, tapi **membantah label modus**.
4. **Templat "LOS N hari = median dx" (20 baris)**: angka N selalu identik dengan kolom `LOS hari`, tetapi 13 dari 20 tidak sama dengan median LOS kelompok diagnosis sebenarnya (lihat 5.2).
5. **Umpan Balik didominasi satu kalimat** (39×) sehingga umpan balik tidak unfit sebagai ground truth sentimen per-claim; label sentimen kemungkinan diturunkan dari template kata, bukan dari pengalaman pasien.

---

## 7. Audit Kolom Alasan

### 7.1 Distribusi prefix 3-tingkat

Spec v2.1: **FRAUD 36 / ANOMALI 24 / NORMAL 240**.

| Prefix | Aktual | Selisih vs spec |
|---|---|---|
| `NORMAL` | **239** | −1 |
| `ANOMALI SEDANG` | 10 | - |
| `ANOMALI TINGGI (belum tentu fraud)` | 14 | - |
| `FRAUD (...)` total | **36** | 0 ✓ |
| - rincian FRAUD: Upcoding 3, Phantom Billing 3, Unbundling 3, Unbundling - klaim pecahan 3, Drug Diversion 3, Repeat Billing 4, Iur Biaya 4, Readmission Berulang 6, Excessive Usage 6, Biaya Markup 1 | 36 | ✓ |
| (KOSONG) | **1** | KLM031 |

Total 239 + 10 + 14 + 36 + 1 = 300 ✓. Alasan terisi pada **60/60** baris `review`/`escalate` (R27 lulus) - jadi **KLM031 adalah baris `low`**, dan kekosongannya memang pada baris normal (registry §6 mendokumentasikan ini).

### 7.2 Verifikasi kemandirian angka dalam Alasan

| Klaim dalam Alasan | Jumlah | Dapat dihitung ulang? | Verdict |
|---|---|---|---|
| "rasio N" (Biaya ÷ tarif paket) | 72 baris | **Ya - 72 dari 72** cocok persis dengan `round(Biaya Rp / tarif acuan, 2)` | **Tidak mandiri**: tarif acuan **tidak ada di dataset** (R15). Tabel acuan ada di bagian Biaya Rujukan dokumen Notion `10-simulation-dataset.md`. Auditor ketiga tanpa akses ke dokumen itu **tidak dapat memverifikasi rasio mana pun** |
| Rasio dosis klinis (bukan biaya÷tarif) | 2 baris (KLM122 "6x kebutuhan klinis", KLM125 "3x kebutuhan rasional") | Tidak - ini rasio dosis, tidak ada kolom dosis harian; kata "rasio" di kedua baris ini hanya substring dari "rasional", bukan angka rasio | Tidak dapat diverifikasi |
| "Nx median" | 8 baris (KLM115–120, KLM128, KLM130) | **7 dari 8** dapat dihitung ulang dari kolom dataset (6 baris SYND-09: klaim 2x vs aktual 2,05x; KLM128 klaim 3x vs aktual 2,95x). **KLM130 tidak dapat dihitung** - tidak ada bar pembanding (dx J18.9 rawat jalan, n=0), R14 | Sebagian mandiri, bergantung pada definisi "median" yang tidak didokumentasikan |
| "N episode dalam M hari" | 12 baris `anomali_frekuensi` | **Hanya 1 dari 12 benar** (P15/KLM020–023). 6 baris outright salah (R13), 6 baris tidak punya episode kedua (R13b) | **Tidak mandiri** - narasi numerik bertentangan dengan data |
| "N pen insulin vs 1–2 pen/bulan" | 3 baris drug_diversion | Qty insulin **terbaca** dari kolom `Obat` (24, 30, 12 pen) → bagian ini konsisten | Sebagian mandiri |
| "LOS N hari" | semua baris NORMAL | Ambang median kelompok **dapat dihitung**, tapi angka LOS yang tertulis di Alasan sering berbeda dari kolom `LOS hari` | Tidak konsisten |
| "4x tarif paket" (KLM121) | 1 baris | Tidak - tarif paket tidak ada di dataset | Tidak dapat diverifikasi |
| "2,6x tarif" (KLM129) | 1 baris | Tidak - tarif tidak ada | Tidak dapat diverifikasi |
| "biaya RpN" | semua baris NORMAL | Ya - Biaya Rp ada di kolom | Mandiri ✓ |

**Kesimpulan §7:** kolom `Alasan` **tidak dapat diverifikasi secara mandiri** dari artefak data. 72 dari 300 baris mengutip "rasio" yang butuh tabel tarif eksternal; angka tersebut memang cocok hitungannya, tetapi sumber acuan tidak pernah dipaketkan bersama dataset - melanggar aturan `03-dataset-registry.md` §8 butir 6 ("kamus data") dan §11 ("Tambahkan tarif acuan dan perhitungan per klaim bila mengklaim overcharge"). Selain itu, 51 templat hanya berbeda pada angka, sehingga **Alasan secara substantif hanya membedakan 51 kasus, bukan 300**.

---

## 8. Rekomendasi Perbaikan Generator (Prioritas)

**P0 - Blocking (tanpa ini dataset tidak bisa dipakai sebagai ground truth):**

1. **Buat generator 300 baris yang deterministik dan simpan di repo** (mis. `scripts/generate_claims.py`, `SEED = 20260707`), dengan fungsi terpisah per modus; outputkan `data/raw/claims_300_v2.1.csv` + `data/processed/metadata.json` (nama & versi dataset, waktu ekspor, jumlah baris, SHA-256 berkas, kamus data, daftar kolom dipakai/dikecualikan, definisi target & ambang, aturan pembersihan, ID split train/val/test, seed, versi kode - 10 butir `03-dataset-registry.md` §8). Saat ini **0 dari 10 butir** dapat dipenuhi.
2. **Perbaiki ground truth yang dibantah data.** (a) SYND-02 phantom: ganti narasi KLM004–006 agar tidak mengklaim hemiarthroplasty dilakukan (mis. "resume medis tidak ditemukan; pasien menyatakan tidak pernah dioperasi"), atau turunkan label phantom. (b) SYND-03: narasi KLM008/010/012 harus menyebut intubasi. (c) 12 baris `anomali_frekuensi`: generate episode pengitudinal nyata per pasien (tanggal berbeda, ±1 hari), atau turunkan klaim jumlah episode di Alasan.
3. **Selaraskan tabel sindikat v2.1 dengan data** (SYND-06 s.d. SYND-09 + KLM121/KLM122): gunakan entitas yang benar-benar muncul (P21–P29, D13/D14/D15/D19, RS_G/RS_H/RS_I/RS_J) dan perbaiki rentang skor; atau ubah data agar sesuai tabel. Tanpa ini kriteria "Setiap SYND-01–SYND-09 hit-rate > 0" tidak terukur.
4. **Perbaiki KLM129**: prolonged_stay dengan LOS 2 < median 6,5 dan Alasan "dipulangkan 2 hari" → ubah ke baris LOS panjang (mis. 9–12 hari) atau ubah modus ke `early_discharge`.

**P1 - Kualitas & validitas ilmiah:**

5. **Turunkan `Kontribusi Saluran` dari `Skor Fraud`** dengan satu rumus tertulis (mis. bobot tetap 0,4/0,35/0,25 + pembulatan 2 desimal) sehingga T+F+S = skor pada 300/300 baris. Saat ini 42 baris tidak konsisten dan total kanal tertulis dari templat.
6. **Masukkan tabel tarif acuan sebagai kolom** (`tarif_acuan_rp`) atau file `data/raw/tarif_acuan_v2.1.csv`, lalu buat generator Alasan menghitung rasio/Nx median darinya. Target: 72/72 "rasio" dan 7/8 "Nx median" dapat diverifikasi dari artefak saja.
7. **Turunkan narasi & Alasan dari data, bukan sebaliknya**: minimal 1 narasi unik per baris atau per episode (saat ini 40/300), hapus angka yang tidak ada di kolom (tekanan darah, HbA1c) atau tambahkan kolomnya.
8. **Tambahkan kolom `seed`, `version`, `timestamp`** ke CSV hasil generator (spec v2.1 mensyaratkan) dan berkas checksum untuk setiap artefak.
9. **Perbaiki artefak serialisasi**: 28 baris `undefined` di kolom `Rujukan`; 8 baris LOS tidak sinkron dengan jenis layanan (rajal LOS>0, inap LOS=0); 58 baris `netral` dengan skor ≠ 0 → tetapkan ambang sentimen tertulis.
10. **Selaraskan 3 selisih rekonsiliasi**: jumlah modus (14 vs 13 - daftarkan 14 nama modus), encoding LOS (109 baris "kosong" → pisahkan `not_applicable` vs `0`), dan Kontradiksi Narasi (8 vs 12 - perbarui spec §7 & kriteria "8 klaim kontradiksi").

**P2 - Reproduktivitas & audit trail:**

11. **Buat `configs/leakage.yaml` + `tests/test_leakage.py`** di `Aegis-JKN/` (keduanya tidak ada) - saat ini aturan anti-leakage hanya tertulis di Notion, tanpa enforcement.
12. **Perbaiki ground truth sentimen**: 58 baris "netral" tidak konsisten, dan 240 baris `low` memakai 16 nilai umpan balik yang sama - buat ground truth teks per klaim (saat ini hanya 36 nilai umpan balik untuk 300 klaim).
13. **Tutup 3 item undone** dari `03-dataset-registry.md` §11 (owner dataset, perlakuan resmi LOS kosong, tarif acuan + checksum per benchmark).

---

## Lampiran - Reproduksi

```bash
cd N:\HEALTHKATHON\analysis\reports\scripts
python 07_gen.py                      # stdlib saja; tanpa pandas
# → Reconciliation: 18 OK / 3 SELISIH / 2 INFO
# → Checker: 29 lulus / 24 gagal
# → Gagal per severity: {'CRITICAL': 9, 'HIGH': 7, 'MEDIUM': 7, 'LOW': 1}
# → menulis 07_gen_results.json
```

Semua angka dalam laporan ini berasal dari `07_gen_results.json` (dihasilkan perintah di atas) atau dari pembacaan langsung CSV corpus (`d6fb95b9…`). Tidak ada estimasi atau angka tebakan.
