# 04 - Audit Kualitas Data & Konformance Kamus Data
## Aegis-JKN Dataset v2 (300 klaim) vs Kamus Data Registry Rev 1.0

| Aspek | Nilai |
|---|---|
| Sumber kamus | `analysis/corpus/03-dataset-registry.md` §5 (data dictionary), §6 (pemeriksaan kualitas), §7 (anti-leakage), §8 (reproduksibilitas) |
| Sumber katalog | `analysis/corpus/07-dataset-v2-catalog.md` |
| Sumber skenario | `analysis/corpus/10-simulation-dataset.md` (v100 + catatan ekspansi v2.1) |
| Sumber angka dashboard | `analysis/corpus/00-dashboard.md` §3 |
| Data nyata (audit utama) | `analysis/corpus/claims_v2_live.csv` (300 baris × 29 kolom), `claims_v2_live.json` (300 objek, kunci identik dengan header CSV) |
| Data pembanding | `mechine-learning-deep-learning/datasets/claims_300_v2.1.csv` (300 baris × 31 kolom, SHA-256 `37cf22369ebf7a3c616219cb49b9c4406f00d75286b38cbf6c08b844e27fd4e8`), repo git `biezz-2/Aegis-JKN-mechine-learning-deep-learning` @ `00ca990` |
| Skrip audit | `analysis/reports/scripts/04_audit.py` + `04_audit_round2..9.py` + `04_audit_final_check.py` + `04_audit_compare_v21.py` + `04_audit_compare_check.py`; keluaran `04_audit_output.txt`, `04_audit_round2..9_output.txt`, `04_audit_final_check_output.txt`, `04_audit_compare_v21_output.txt`, `04_audit_compare_check_output.txt`, `04_audit_results.json` |
| Tanggal audit | 22 Oktober 2026 |
| Checksum SHA-256 | `claims_v2_live.csv` = `d6fb95b9fbfb6bf47e9a99bcf57df0e38b00a13758b6d3ac14779e64a6121119`<br>`claims_v2_live.json` = `837687edbf283b8bfd7fe4c46f564f200043699fa9bb20c317c52974ee1f23e2`<br>`claims_300_v2.1.csv` = `37cf22369ebf7a3c616219cb49b9c4406f00d75286b38cbf6c08b844e27fd4e8` |

Metodologi: seluruh angka dihitung ulang dengan Python stdlib (`csv`, `json`, `re`, `statistics`, `collections`, `datetime`, `hashlib`). Tidak ada estimasi manual; tidak ada pandas. Perintah replikasi:

```
python -X utf8 analysis/reports/scripts/04_audit.py
python -X utf8 analysis/reports/scripts/04_audit_round2.py   # s/d round9
python -X utf8 analysis/reports/scripts/04_audit_final_check.py
```

---

## 1. Ringkasan Eksekutif

Dataset v2 secara aritmetika **sangat rapi**: 300 ID unik tanpa sela, distribusi status dan label risiko persis seperti diklaim, total nominal dan pecahan per status cocok sampai rupiah, tidak ada duplikat payload tak sengaja, tidak ada biaya negatif, tidak ada kolom wajib kosong selain satu `Alasan`. Seluruh klaim angka di §3 dan §6 registry **terverifikasi** kecuali dua butir dan tiga butir campuran (§3 tabel di bawah). Perbandingan dengan salinan CSV v2.1 di repo ML (§9) menunjukkan keduanya berasal dari **dataset yang sama** - dari 26 kolom dump Notion yang punya pasangan di v2.1, **23 identik** pada 300 baris, 2 beda hanya format encoding, 1 beda isi (cacat truncasi); `Catatan` tidak ada di v2.1.

Masalah sesungguhnya bukan hitungan, melainkan **konsep dan provenance**. Enam temuan struktural:

1. **Skema v2.1 ada di repo ML, tidak di dump Notion.** Enam kolom yang dijanjikan `10-simulation-dataset.md`: pada **dump Notion** (`claims_v2_live.csv`) hanya `faskes_id` terderivasi (`RS_G`), sedangkan `pasien_id`, `dokter_id`, `seed`, `version`, `timestamp` tidak ada sebagai kolom - ID entitas hanya tersembunyi sebagai prefiks di dalam rich text (`P21 (Rahmat Fauzi)`, `D13 (dr. Mulyadi Santoso, Sp.B)`). Namun salinan CSV v2.1 di repo ML (`mechine-learning-deep-learning/datasets/claims_300_v2.1.csv`, 31 kolom) **memuat `pasien_id`, `dokter_id`, `faskes_id` sebagai kolom terpisah yang proper**, plus `diagnosis_code`, `prosedur_code`, dan `is_fraud`. Jadi GroupKFold/LeaveOneGroupOut **sudah diimplementasikan** pada salinan itu (notebook `Aegis-JKN.ipynb` sel 11: `gkf.split(df_claims, groups=df_claims['pasien_id'])`). Yang benar-benar hilang di kedua sumber hanya `seed`, `version`, `timestamp` → protokol checksum/seed §8 tetap belum terpenuhi. Lihat §9.
2. **Pemetaan entitas sindikat v2.1 meleset pada 4 dari 9 sindikat.** SYND-06/07/08/09 tidak memakai pasien yang didokumentasikan; SYND-09 bahkan memakai dokter D19, bukan D16. Dua klaim tunggal KLM121/KLM122 terpetakan ke faskes, dokter, dan pasien yang sama sekali berbeda dari tabel. **Terverifikasi identik di kedua sumber** - ini cacat desain generator, bukan artefak scraping.
3. **`Kontribusi Saluran` bukan penjelas skor.** Pada 42 baris `Skor Fraud` ≠ T+F+S (selisih sampai +0,17), dan pada 14 baris label `Risiko` **tidak dapat diturunkan** dari T+F+S dengan ambang mana pun. Kanal justru memberi label berbeda dari label yang tercantum. Identik di kedua sumber.
4. **Aturan LOS di kamus §5 tidak diimplementasikan.** Tidak ada satu pun sel LOS kosong; 109 baris bernilai `0`. Nilai `0` dipakai seragam untuk rawat jalan tanpa LOS (106 baris) **dan** sebagai sinyal fraud pada rawat inap (3 baris KLM008/KLM010/KLM012). Alasan pada 109 baris itu **tidak pernah** menyebut LOS. Identik di kedua sumber.
5. **Ambang 0,80 belum terkunci.** `03 §4` dan `10-simulation-dataset.md` berbeda redaksi (`> 0.8` vs `≥ 0.80`). Data hanya konsisten dengan interpretasi `≥`. Baris KLM115 (skor tepat 0,80) menjadi satu-satunya kasus batas yang membedakan kedua definisi - dan **nilai KLM115 identik di kedua sumber**.
6. **`dokter_raw` terpotong di 32 baris pada CSV v2.1** (D04 dan D16, spesialis `Sp.JP`). Akar cause: di Notion, field `Dokter` pada 32 baris tersimpan sebagai **3 segmen rich_text** (segmen tengah `Sp.JP` ber-`href` hyperlink), sedangkan 268 baris lain 1 segmen; parser v2.1 hanya mengambil segmen pertama sehingga `Sp.JP)` hilang. Dump Notion sendiri utuh. Temuan baru - lihat §9.

### Tabel severity

| Severity | Jumlah | Cakupan |
|---|---|---|
| KRITIS | 4 | Skema v2.1 parsial di dump Notion (seed/version/timestamp nol di semua artefak); pemetaan sindikat salah 4/9; kanal tidak menjelaskan skor (14 baris); LOS 0 menyatukan "tidak berlaku" dan "fraud" |
| TINGGI | 5 | Kontradiksi Narasi 12 vs klaim 8; ambang 0,80 ambigu (KLM115); 28 baris "undefined" di Rujukan; P11 punya 5 klaim vs tabel v100; **`dokter_raw` terpotong 32 baris di CSV v2.1** |
| SEDANG | 6 | SYND-05 skenario tidak sesuai modus; sentinel "—" pada Prosedur (156 baris); 44 baris biaya di atas pagar IQR; SHAP konstan per modus (7/13); nomor rujukan duplikat; duplikat near-identical (2 grup) |
| RINGAN | 4 | CSV tidak terurut; casing Modus vs Alasan tidak konsisten; manifest/checksum belum disertakan; `Umpan Balik Pasien` hanya 36 template untuk 300 baris |
| **Total** | **19** | |

---

## 2. Tabel Konformance Kamus (per kolom, 03 §5)

Semua 24 properti kamus **ada** di CSV. Kolom bisnis CSV = 27; selisih 3 kolom yang **tidak terdaftar** di kamus: `Alasan Berobat`, `Layanan`, `Rujukan`. Dua kolom `_notion_page_id` dan `_last_edited` adalah metadata Notion, bukan properti data.

| Properti (kamus §5) | Ada di CSV | Tipe aktual (sampel) | Aturan kualitas di kamus | Temuan data nyata | Status |
|---|---|---|---|---|---|
| Name | Ya | String, `KLM285` | Wajib unik | 300 ID unik, pola `KLM\d{3}` semua, rentang 1–300, tanpa duplikat | **PATUH** |
| Tanggal | Ya | String ISO `2026-06-12` | Format tanggal konsisten | 300/300 format `YYYY-MM-DD` valid, 138 tanggal unik, rentang 2026-01-01 … 2026-06-27 | **PATUH** |
| Pasien | Ya | Rich text `P21 (Rahmat Fauzi)` | Tidak menggunakan identitas nyata | 40 ID synthetic, 1 nama per ID, tidak ada NIK/nama riil | **PATUH** (tapi ID bukan kolom tersendiri di dump Notion → lihat §6, §9) |
| Dokter | Ya | Rich text `D13 (dr. Mulyadi Santoso, Sp.B)` | Relasi dan afiliasi konsisten | 20 dokter, 20 pasangan (dokter, faskes) unik, tidak ada dokter di >1 faskes | **PATUH** (dump Notion utuh; CSV v2.1 memotong 32 baris → §7-19) |
| Faskes | Ya | String `RS_G` | Nama dan kode konsisten | 10 kode RS_A–RS_J, lengkap | **PATUH** |
| Diagnosis ICD-10 | Ya | Rich text `K80.2 - Kolelitiasis, tanpa kolesistitis` | Kode serta istilah ditinjau | 13 kode unik, format `KODE - Deskripsi` seragam | **PATUH** |
| Prosedur ICD-9-CM | Ya | Rich text / sentinel `—` | Kode serta konteks tindakan ditinjau | 156 baris memakai sentinel `—`, bukan sel kosong; 8 kode + `—` | **PELANGGARAN** (sentinel menggantikan kosong, hlm. §7-5) |
| Obat | Ya | Rich text `M03 x 6 vial; M04 x 7 vial` | Satuan harus konsisten | Satuan terkontrol: vial/tablet/nebules/pen; 3 baris `Obat` = `—` (phantom billing, konsisten dgn SHAP) | **PATUH** |
| LOS hari | Ya | Number (0…14) | Nilai tidak berlaku dibedakan dari kosong | **0 baris kosong**; 109 baris bernilai `0`; 0 tidak membedakan N/A vs fraud; 3 rawat inap ber-LOS 0 | **PELANGGARAN** (hlm. §7-4) |
| Biaya Rp | Ya | Integer rupiah | Nonnegatif; definisi nominal jelas | 300/300 integer, 0 negatif, 0 nol, min Rp700.000 max Rp63.500.000 | **PATUH** |
| Narasi Rekam Medis | Ya | Rich text | Tidak dianggap catatan pasien nyata | 41 varian; 10 dari 13 dx hanya punya 1–3 template | **PATUH** |
| Kontradiksi Narasi | Ya | Checkbox `True`/`False` | Perlu aturan penetapan eksplisit | 12 `True` (bukan 8 seperti klaim v100) - aturan penetapan **tidak terdokumentasi** | **TIDAK TERDOKUMENTASI** |
| Skor Fraud | Ya | Float 0.04–0.95 | Wajib dokumentasikan sumber skor | 0.04–0.95; sumber skor **tidak** didokumentasi di §6/§8; 42 baris tidak = T+F+S | **TIDAK TERDOKUMENTASI** |
| Risiko | Ya | Select low/medium/high/fraud | Jangan dicampur dengan status alur kerja | 4 nilai, konsisten dengan skor pada interpretasi `≥` | **PATUH** |
| Status | Ya | Select auto_clear/review/escalate | Hanya gunakan opsi yang disetujui | 3 nilai; matriks Status×Risiko deterministik (lihat §5) | **PATUH** |
| Modus | Ya | Select snake_case | Kosong dibolehkan | 240 kosong, 13 modus terisi; casing snake_case ≠ Title Case di `Alasan` | **PATUH** (hlm. §7-15) |
| Sindikat | Ya | Select SYND-01…09 | Kosong dibolehkan | 264 kosong, 36 terisi (34 fraud + 2 high) | **PATUH** |
| Alasan | Ya | Rich text | Wajib bila review/escalate | 299 terisi; 1 kosong = KLM031 (status auto_clear, label low → **rule tetap terpenuhi**) | **PATUH** |
| Sinyal SHAP | Ya | Rich text | Hanya diisi bila berasal dari metode penjelasan yang benar | 33 nilai unik; 7 dari 13 modus punya **SHAP konstan** → bukan penjelasan per-baris | **PELANGGARAN** (hlm. §7-12) |
| Kontribusi Saluran | Ya | Rich text `T 0.03 · F 0.03 · S 0.04` | Jelaskan rumus dan satuan nilai | Rumus **tidak** didokumentasi; ≠ skor pada 42 baris; label tak derivable pada 14 baris | **PELANGGARAN** (hlm. §5, §7-3) |
| Skor Sentimen | Ya | Float −0.90…0.85 | Definisikan rentang dan polaritas | Semua dalam −1…1; partisi ketat: negatif [−0,90,−0,30], netral [0,05,0,15], positif [0,60,0,85]; **ambang antar kelas tidak didokumentasi** | **TIDAK TERDOKUMENTASI** (data konsisten) |
| Sentimen | Ya | Select positif/netral/negatif | Harus sesuai dengan definisi skor | 0 pelanggaran polaritas (negatif>0: 0; positif<0: 0) | **PATUH** |
| Umpan Balik Pasien | Ya | Rich text | Data simulasi, bukan testimoni nyata | 36 template; 42 baris `low` bersentimen negatif sebagai negative control | **PATUH** |
| Catatan | Ya | Rich text | Untuk konteks, bukan mengganti alasan utama | 60 terisi (semua baris non-`low`), 240 kosong | **PATUH** |
| *(tidak ada di kamus)* | - | `Alasan Berobat` | - | 300 terisi | **TIDAK TERDOKUMENTASI** |
| *(tidak ada di kamus)* | - | `Layanan` | - | 300 terisi: rawat inap 189 / rawat jalan 111 - kolom ini yang sebenarnya membedakan layanan, tetapi kamus tidak menyebutnya | **TIDAK TERDOKUMENTASI** |
| *(tidak ada di kamus)* | - | `Rujukan` | - | 300 terisi; **28 baris berisi literal `undefined`** | **PELANGGARAN** (hlm. §7-7) |

Ringkasan status: **14 PATUH · 4 PELANGGARAN · 5 TIDAK TERDOKUMENTASI · 3 kolom di luar kamus**.

---

## 3. Tabel Verifikasi Angka

| # | Klaim | Sumber | Hasil hitung ulang | ✓/✗ |
|---|---|---|---|---|
| 1 | Jumlah baris aktif 300 | 00 §3, 03 §6 | CSV 300 baris, JSON 300 objek, kunci JSON ≡ header CSV | ✓ |
| 2 | ID KLM001 → KLM300 tanpa sela/duplikat | 03 §6, 00 §4 | 300 ID unik, angka 1–300 lengkap, 0 angka hilang, 0 duplikat | ✓ |
| 3 | Kapitalisasi/padding ID seragam | 03 §5 | 300/300 cocok `^KLM\d{3}$`; 0 huruf kecil, 0 panjang ≠ 6 | ✓ |
| 4 | Status auto_clear = 240 | 03 §3.1, 00 §3 | 240 | ✓ |
| 5 | Status review = 24 | 03 §3.1, 00 §3 | 24 | ✓ |
| 6 | Status escalate = 36 | 03 §3.1, 00 §3 | 36 | ✓ |
| 7 | Risiko low = 240 | 03 §3.2 | 240 | ✓ |
| 8 | Risiko medium = 10 | 03 §3.2 | 10 | ✓ |
| 9 | Risiko high = 14 | 03 §3.2 | 14 | ✓ |
| 10 | Risiko fraud = 36 | 03 §3.2 | 36 | ✓ |
| 11 | 24 baris review mencakup medium + high | 03 §3.2 | review = medium 10 + high 14 = 24 | ✓ |
| 12 | 109 baris LOS hari kosong | 03 §6, 00 §3 | **Jumlah 109 benar**, tetapi **0 baris kosong**: semuanya berisi nilai `0` | ✓ (jumlah) / ✗ (semantik "kosong") |
| 13 | 1 baris Alasan kosong | 03 §6, 00 §3 | 1 → `KLM031` (status auto_clear, label low) | ✓ |
| 14 | 240 baris Modus kosong | 03 §6 | 240 | ✓ |
| 15 | 264 baris Sindikat kosong | 03 §6 | 264 | ✓ |
| 16 | Total nominal Rp3.526.650.000 | 03 §3.3, 00 §3 | Rp3.526.650.000 (Σ 300 `Biaya Rp`) | ✓ |
| 17 | Nominal auto_clear Rp2.685.550.000 | 03 §3.3 | Rp2.685.550.000 | ✓ |
| 18 | Nominal review Rp279.950.000 | 03 §3.3 | Rp279.950.000 | ✓ |
| 19 | Nominal escalate Rp561.150.000 | 03 §3.3 | Rp561.150.000 | ✓ |
| 20 | Σ per-status = total | konsistensi internal | 2.685.550.000 + 279.950.000 + 561.150.000 = 3.526.650.000 | ✓ |
| 21 | Tidak ditemukan ketidaksesuaian label risiko vs rentang skor | 03 §6 | 0 mismatch pada interpretasi `≥` batas bawah; **1 mismatch** pada interpretasi `>` (KLM115) | ✓ / ✗ |
| 22 | Kontradiksi Narasi = 8 klaim (KLM001-006, KLM018, KLM024) | 10-sim §Analisis Teks | Aktual **12**: KLM001-006, KLM018, KLM024, **KLM105, KLM106, KLM107, KLM108** | ✗ |
| 23 | Entitas v2.1: 40 pasien / 20 dokter / 10 faskes | 10-sim §Distribusi Entitas | 40 / 20 / 10 - lengkap P01–P40, D01–D20, RS_A–RS_J | ✓ |
| 24 | Skema v2.1: 6 kolom `pasien_id, faskes_id, dokter_id, seed, version, timestamp` ada | 10-sim §Struktur File | **Dump Notion: 1 dari 6** (`faskes_id` saja). **CSV v2.1 di repo ML: 3 dari 6** (`pasien_id`, `faskes_id`, `dokter_id`). `seed`/`version`/`timestamp` nol di keduanya | ✗ (dump Notion) / ✓-sebagian (CSV v2.1) - lihat §6, §9 |
| 25 | Tabel v100 (pasien/dokter/faskes: jumlah klaim & skor maks) cocok dengan data | 10-sim §Pasien/§Dokter/§Faskes | 38 dari 39 entitas cocok; **P11**: doc 4 klaim, aktual 5 | ✗ (1 entitas) |
| 26 | Distribusi label v100 (76/4/6/14) | 10-sim §Ringkasan | KLM001–KLM100: low 76 / medium 4 / high 6 / fraud 14 | ✓ |
| 27 | Distribusi sentimen v100 (62/14/24) | 10-sim §Analisis Teks | KLM001–KLM100: positif 62 / netral 14 / negatif 24 | ✓ |
| 28 | Sinkronisasi JSON ≡ CSV | pemeriksaan sendiri | 29 kunci identik, 0 key hanya di JSON, 0 key hanya di CSV | ✓ |
| 29 | Dump Notion ≡ `claims_300_v2.1.csv` (repo ML) | pemeriksaan sendiri | Dari 26 kolom dump Notion yang berpasangan: **23 identik** pada 300 baris, 2 beda format saja (`Kontradiksi Narasi` `True`↔`1`, `Sindikat` `""`↔`"none"`), 1 beda isi (`Dokter`/`dokter_raw` terpotong 32 baris). `Catatan` tidak ada di v2.1. Headline number identik | ✓ (dengan 1 cacat, §9.3) |

**Total: 29 butir → 24 ✓ · 2 ✗ · 3 campuran.** Rincian campuran: butir 12 ✓(jumlah)/✗(semantik "kosong"), butir 21 ✓/✗ (hanya berbeda pada interpretasi ambang `>`), butir 24 ✗(dump Notion)/✓-sebagian (CSV v2.1). Butir 29 dihitung ✓ dengan satu cacat (truncasi `dokter_raw`). Nol selisih rupiah pada butir 16–20.

---

## 4. Konsistensi Label Risiko vs Ambang Skor

### 4.1 Dua interpretasi ambang

| Interpretasi ambang | Definisi | Mismatch |
|---|---|---|
| A - batas bawah **inklusif** (`s ≥ 0.35` → medium, dst.) | `<0.35 low; 0.35–0.60 medium; 0.60–0.80 high; ≥0.80 fraud` | **0 dari 300** |
| B - batas bawah **eksklusif** (`s > 0.80` → fraud) | persis redaksi `10-simulation-dataset.md` §Ekspansi v2: "di atas 0.8 fraud" | **1 dari 300** → KLM115 |

Redaksi `03 §4` menyebut "skor 0,80 tidak termasuk kelas fraud" untuk versi 100 klaim, sedangkan `10-simulation-dataset.md` memakai "di atas 0.8 fraud". Data aktif **hanya konsisten dengan interpretasi A**. Ini persis kondisi yang diperingatkan §4: definisi belum dikunci.

### 4.2 Kasus batas (EDGE)

| Ambang | Baris dengan skor **tepat** di ambang | Label |
|---|---|---|
| 0,35 | **tidak ada** | - |
| 0,60 | **tidak ada** | - |
| 0,80 | **KLM115** (Skor Fraud = `0.80`, Risiko = `fraud`) | satu-satunya kasus batas di seluruh dataset |

Tidak ada baris pada 0,35 maupun 0,60, sehingga kedua ambang tersebut **tidak pernah diuji oleh data**. Yang membedakan interpretasi A dan B hanyalah satu baris.

### 4.3 Rentang skor implisit yang benar-benar ada

| Label | n | min | maks |
|---|---|---|---|
| low | 240 | 0.04 | 0.14 |
| medium | 10 | 0.40 | 0.53 |
| high | 14 | 0.62 | 0.79 |
| fraud | 36 | 0.80 | 0.95 |

Terdapat **celah data** pada 0.14–0.40 (antar low dan medium) dan 0.53–0.62 (antar medium dan high). practically, ambang 0,35 dan 0,60 tidak pernah menjadi batas decision aktual - label hanya dapat diturunkan dari skor dengan margin jauh. Konsekuensi: pengujian model pada ambang sungguhan tidak mungkin dilakukan dengan dataset ini.

### 4.4 Daftar baris menyimpang

| ID | Skor Fraud | Risiko | Status | Penyimpangan |
|---|---|---|---|---|
| KLM115 | 0.80 | fraud | escalate | satu-satunya baris yang melanggar interpretasi B (`> 0.8`); Sysndikat SYND-09 |

Tidak ada baris lain yang menyimpang dari ambang mana pun.

---

## 5. Konsistensi Lintas Kolom

### 5.1 Status × Risiko - deterministik penuh

| Status | low | medium | high | fraud | Total |
|---|---|---|---|---|---|
| auto_clear | 240 | 0 | 0 | 0 | 240 |
| review | 0 | 10 | 14 | 0 | 24 |
| escalate | 0 | 0 | 0 | 36 | 36 |

Hipotesis "auto_clear hanya low" **terbukti benar**. Konsekuensi yang lebih penting: `Status` adalah fungsi bijeksi dari `Risiko` (240/24/36 = 240 low / medium+high / fraud). Artinya Status **tidak membawa informasi tambahan** apa pun dan bukan variabel independen - tetapi `03 §7` dan `10-simulation-dataset.md` §v2.1 tetap memperlakukannya sebagai kolom dengan status alur kerja tersendiri.

### 5.2 Sindikat × Modus × Risiko

| Sindikat | n | Risiko | Modus | Faskes | Dokter | Pasien (aktual) | Skor aktual | Skor didokumentasikan |
|---|---|---|---|---|---|---|---|---|
| SYND-01 | 3 | fraud | upcoding | RS_A ✓ | D01, D02 ✓ | P01-P03 ✓ | 0,93–0,95 | ≥0,93 ✓ |
| SYND-02 | 3 | fraud | phantom_billing | RS_C ✓ | D05 ✓ | P08-P10 ✓ | 0,92–0,94 | ≥0,92 ✓ |
| SYND-03 | 6 | fraud | unbundling | RS_B ✓ | D07 ✓ | P12-P14 ✓ | 0,85–0,87 | 0,84–0,87 ✓ |
| SYND-04 | 2 | fraud | drug_diversion | RS_E ✓ | D09 ✓ | P16-P17 ✓ | 0,86–0,88 | 0,86–0,88 ✓ |
| SYND-05 | 2 | **high** | cloning | RS_F ✓ | D08 ✓ | P19-P20 ✓ | 0,78–0,79 | 0,78–0,79 ✓ |
| SYND-06 | 4 | fraud | repeat_billing | RS_G ✓ | D13 ✓ | **P21-P22** ✗ | **0,89–0,92** ✗ | 0,85–0,90 ✗ |
| SYND-07 | 4 | fraud | iur_biaya | RS_H ✓ | D14 ✓ | **P23-P24** ✗ | 0,82–0,85 | 0,82–0,87 ✓ |
| SYND-08 | 6 | fraud | readmission_berulang | RS_I ✓ | D15 ✓ | **P25-P26** ✗ | **0,86–0,89** ✗ | 0,75–0,80 ✗ |
| SYND-09 | 6 | fraud | excessive_usage | RS_J ✓ | **D19** ✗ | **P27** ✗ | **0,80–0,84** ✗ | 0,78–0,83 ✗ |
| - (tanpa sindikat) | 1 | fraud | biaya_markup | **RS_G** ✗ | **D13** ✗ | **P29** ✗ | 0,81 | ≥0,85 (KLM121) ✗ |
| - (tanpa sindikat) | 1 | fraud | drug_diversion | **RS_H** ✗ | **D14** ✗ | **P30** ✗ | 0,82 | ≥0,80 (KLM122) ✓ |
| SYND-05 | 2 | **high** | cloning | - | - | - | - | tabel v100 menyebut "high" ✓ |

Empat sindikat gagal pemetaan. Polanya sistematis: mulai SYND-06 generator hanya menganggarkan **2 pasien per sindikat** (P21-P22, P23-P24, P25-P26) dan **1 pasien** untuk SYND-09 (P27), sedangkan tabel v2.1 mengklaim 4/4/6/6. Akibatnya P28–P40 **tidak pernah muncul** di baris ber-Sindikat mana pun, meski 13 dari mereka ada di CSV sebagai pasien aktif.

SYND-05 (KLM016, KLM017) berlabel `high`, bukan `fraud`. Konsisten dengan rentang 0,78–0,79 dan dengan tabel v100, tetapi berarti **ada sindikat pada baris non-fraud** - perlu diperjelas di kamus bahwa sindikat bukan penanda fraud.

**Konsistensi internal sindikat** (yang benar): setiap sindikat punya satu modus tunggal; tidak ada sindikat tanpa modus; modus di dalam teks prefiks `FRAUD (...)` cocok 100% dengan kolom `Modus` (0 mismatch dari 60 baris fraud).

### 5.3 Skor Fraud vs Kontribusi Saluran - tidak explaining

Pada **240 baris `low`**, `Skor Fraud` = T+F+S **tepat** (selisih 0,000). Pada baris anomali/fraud, tidak:

| Label | n | Baris tanpa koinciden | Selisih min | Selisih maks |
|---|---|---|---|---|
| low | 240 | 0 | 0,000 | 0,000 |
| medium | 10 | 10 | −0,020 | **+0,160** |
| high | 14 | 9 | +0,010 | **+0,170** |
| fraud | 36 | 23 | −0,030 | +0,040 |
| **Total** | 300 | **42** | −0,030 | **+0,170** |

Dari 42 baris itu, 21 punya selisih > 0,02.

### 5.4 Baris yang label Risikonya TIDAK bisa diturunkan dari T+F+S

Dengan ambang mana pun (A maupun B), 14 baris berikut tidak konsisten bila label diturunkan dari penjumlahan kanal:

| ID | T+F+S | Risiko tercantum | Label dari kanal | Skor Fraud | Selisih |
|---|---|---|---|---|---|
| KLM133 | 0,32 | medium | low | 0,44 | +0,12 |
| KLM131 | 0,32 | medium | low | 0,46 | +0,14 |
| KLM136 | 0,32 | medium | low | 0,45 | +0,13 |
| KLM132 | 0,32 | medium | low | 0,42 | +0,10 |
| KLM134 | 0,32 | medium | low | 0,48 | +0,16 |
| KLM135 | 0,32 | medium | low | 0,40 | +0,08 |
| KLM125 | 0,55 | high | medium | 0,67 | +0,12 |
| KLM129 | 0,55 | high | medium | 0,72 | +0,17 |
| KLM123 | 0,55 | high | medium | 0,64 | +0,09 |
| KLM124 | 0,55 | high | medium | 0,71 | +0,16 |
| KLM126 | 0,55 | high | medium | 0,62 | +0,07 |
| KLM128 | 0,55 | high | medium | 0,63 | +0,08 |
| KLM127 | 0,55 | high | medium | 0,68 | +0,13 |
| KLM130 | 0,55 | high | medium | 0,62 | +0,07 |

Ringkas: **KLM123, KLM124, KLM125, KLM126, KLM127, KLM128, KLM129, KLM130, KLM131, KLM132, KLM133, KLM134, KLM135, KLM136**.

Semua 14 adalah baris non-fraud (6 medium + 8 high). Justru kelas fraud (36 baris) konsisten 100% dengan labelnya. Pola kanal juga bertemu: 6 baris medium berbagi pola identik `T 0.12 · F 0.11 · S 0.09` dengan 6 skor berbeda (0,40–0,48); 8 baris high berbagi `T 0.15 · F 0.22 · S 0.18` dengan 8 skor berbeda (0,62–0,72). Artinya `Kontribusi Saluran` bukan penjelas skor - ia **tidak deterministik terhadap** `Skor Fraud` di kelas non-fraud.

### 5.5 Skor Fraud vs Sinyal SHAP

`Sinyal SHAP` memiliki 33 nilai unik untuk 300 baris. Distribusi varian per modus:

| Modus | n baris | Varian SHAP |
|---|---|---|
| excessive_usage, iur_biaya, phantom_billing, readmission_berulang, repeat_billing, cloning, biaya_markup | 6, 4, 3, 6, 4, 2, 1 | **1 (konstan)** |
| unbundling | 6 | 2 |
| drug_diversion, upcoding | 3, 5 | 3 |
| anomali_frekuensi | 12 | 9 |
| overbilling, prolonged_stay | 4, 4 | 4 |

7 dari 13 modus memiliki SHAP yang **identik untuk semua barisnya** - SHAP di sana hanya mengulang label modus, bukan penjelasan per-baris. Klaim `10-simulation-dataset.md` §Validasi "SHAP sejalan dengan kolom Alasan" (kriteria 5 protokol "SESUAI") **belum dapat diuji**, karena 33 teks SHAP tidak pernah menyebut nilai kanal, nama fitur, atau besaran kontribusi.

### 5.6 Pairwise klinis: dx ↔ prosedur ↔ obat ↔ narasi

Pasangan dx → prosedur yang terobservasi:

| dx | prosedur | n | Penilaian |
|---|---|---|---|
| K35.8 | 47.09 Apendektomi | 31 | klinis wajar |
| K40.9 | 53.1 Reparasi hernia | 29 | klinis wajar |
| K80.2 | 51.23 Kolesistektomi | 29 | klinis wajar |
| S72.0 | 81.52 Hemiarthroplasty | 18 | klinis wajar |
| I21.9 | 00.66 PCI | 20 | klinis wajar |
| N20.0 | 98.51 ESWL | 9 | klinis wajar |
| **K29.7** | **00.66 PCI** | **3** | **anomali upcoding (SYND-01)** - sesuai skenario |
| **O80** | **74.1 Seksio sesarea** | **1** | **anomali (KLM024)** |
| **E11.9** | **00.66 PCI** | **1** | **anomali (KLM018)** |
| K80.2 | 96.04 Intubasi | 3 | unbundling (SYND-03) |
| E11.9, I10, J18.9, J45.9, K29.7, N39.0, O80 | `—` (tanpa prosedur) | 134 | terapi medis |

Tiga baris anomali dx→prosedur (KLM018, KLM024) **tidak** mengikuti skenario SYND-01 (K29.7 → 00.66) yang didokumentasikan, meski SHAP dan `Alasan` masing-masing konsisten secara internal. Keduanya adalah upcoding yang di luar templat sindikat.

**Baris dengan modus bertentangan dengan prosedur didokumentasikan:**

| ID | Modus | dx | prosedur | Catatan |
|---|---|---|---|---|
| KLM016 | cloning | K35.8 | 47.09 Apendektomi | Tabel v2.1 menyebut SYND-05 = "dua klaim identik … hemiarthroplasty"; aktual K35.8→47.09 |
| KLM017 | cloning | K35.8 | 47.09 Apendektomi | idem |
| KLM024 | upcoding | O80 | 74.1 Seksio sesarea | bukan skenario SYND-01 (K29.7→00.66) |
| KLM018 | upcoding | E11.9 | 00.66 PCI | bukan skenario SYND-01; SHAP sendiri menyebut "PCI tanpa indikasi kardiologis pada dx E11.9" |

dx → obat: 12 pasangan dx/obat yang konsisten dengan kamus v100 (M01 Metformin↔E11.9, M02 Amlodipin↔I10/E11.9, M03 Seftriakson↔J18.9/K35.8, M05 Salbutamol↔J45.9, M10 Klopidogrel↔I21.9 PCI, dst.). M09 insulin hanya pada E11.9 ✓. Tiga baris `Obat = -` (KLM004/KLM005/KLM006) **benar** dan konsisten dengan Phantom Billing "tanpa MedicationDispense".

Narasi Rekam Medis: 41 varian, 10 dari 13 diagnosis hanya memiliki 1–3 template. Narasi **tidak pernah** bertentangan dengan kode pada baris normal.

### 5.7 Pasien dalam sindikat vs klaim v2.1

Pasien P28–P40 (13 pasien) tidak pernah muncul pada baris ber-Sindikat mana pun, meski seluruhnya ada di CSV sebagai pasien dengan klaim aktif (P27 memiliki 12 klaim). Hipotesis "Distribusi Entitas v2.1: 40 pasien" terpenuhi secara aritmetika, tetapi secara semantik P28–P40 adalah "pasien latar" yang tidak pernah dipakai skenario anomali.

---

## 6. Gap Skema v2.1 vs Aktual + Hitung Entitas Unik

> **Revisi (22 Okt 2026, rev. 2).** Revisi 1 menyatakan "0 dari 6 kolom ada" dan "tidak dapat diimplementasikan". **Itu benar untuk dump Notion, keliru untuk artefak CSV v2.1.** Salinan CSV v2.1 di repo ML memuat 3 dari 6 kolom sebagai kolom terpisah yang proper. Tabel di bawah membedakan keduanya. Lihat juga §9.

### 6.1 Status kolom v2.1 - dump Notion vs CSV v2.1

| Kolom v2.1 yang diklaim | Di dump Notion | Di CSV v2.1 (repo ML) | Dampak |
|---|---|---|---|
| `pasien_id` | **Tidak** (hanya prefiks di rich text `Pasien`) | **Ya** (P01–P40, 40 nilai unik) | GroupKFold(group=pasien_id) **sudah dijalankan** di repo ML (notebook sel 11); pada dump Notion harus parsing ulang |
| `faskes_id` | **Ya** - kolom `Faskes` sudah berupa kode murni `RS_G` | **Ya** (RS_A–RS_J) | LeaveOneGroupOut(group=faskes_id) dapat berjalan di keduanya |
| `dokter_id` | **Tidak** (hanya prefiks di rich text `Dokter`) | **Ya** (D01–D20, 20 nilai unik) | Third grouping axis (per dokter) tersedia |
| `seed` | **Tidak** | **Tidak** | seed 20260707 tidak dapat diverifikasi dari artefak mana pun; protokol §8 butuh seed + versi kode |
| `version` | **Tidak** | **Tidak** | `version = v2.1` tidak dapat diverifikasi dari artefak - harus disimpulkan dari nama file |
| `timestamp` | **Tidak** | **Tidak** | "Waktu generasi" tidak ada; yang ada `_last_edited` (4 nilai berbeda: 00:24, 04:41, 04:50, 04:51) adalah timestamp *edit Notion*, bukan generasi |

**Ringkasan: dump Notion 1 dari 6 · CSV v2.1 3 dari 6 · keduanya 0 dari 3 untuk `seed`/`version`/`timestamp`.**

Perbedaan isi aktual vs klaim nama kolom:

| v2.1 menjanjikan | Dump Notion | CSV v2.1 | Konsekuensi |
|---|---|---|---|
| `pasien_id` (P01–P40) | kolom `Pasien` = `P21 (Rahmat Fauzi)` - ID + nama digabung | kolom `pasien_id` = `P21` (murni) + `pasien_raw` terpisah | **v2.1 memenuhi janji**; pemisahan ID/nama juga memenuhi anti-leakage §7 |
| `dokter_id` (D01–D20) | kolom `Dokter` = `D13 (dr. Mulyadi Santoso, Sp.B)` - ID + nama + spesialisasi | `dokter_id` = `D13` + `dokter_raw` terpisah | **v2.1 memenuhi janji**; tapi `dokter_raw` terpotong di 32 baris (§9.3) |
| `faskes_id` (RS_A–RS_J) | kolom `Faskes` = `RS_G` | `faskes_id` = `RS_G` | **sudah sesuai di keduanya** |
| - | - | `diagnosis_code`, `prosedur_code` (kode murni terpisah dari rich text) | tambahan di luar janji v2.1; memudahkan feature engineering tanpa parsing |
| - | - | `is_fraud` (0/1) | label biner eksplisit; dump Notion hanya punya `Risiko`/`Status` |

### 6.2 Hitung entitas unik aktual vs klaim

| Entitas | Dump Notion | CSV v2.1 | Klaim v2.1 | Status |
|---|---|---|---|---|
| Pasien | **40** (P01–P40 lengkap) | **40** (`pasien_id`) | 40 | ✓ |
| Dokter | **20** (D01–D20 lengkap) | **20** (`dokter_id`) | 20 | ✓ |
| Faskes | **10** (RS_A–RS_J lengkap) | **10** (`faskes_id`) | 10 | ✓ |
| Diagnosis ICD-10 | 13 | 13 (`diagnosis_code`) | "K29.7, K35.8, I10, J45.9, N39.0, dll." | ✓ (tidak ada angka target) |
| Prosedur ICD-9-CM | 8 kode + sentinel `—` | 8 kode + sentinel `—` (`prosedur_code`) | "00.66, 51.23, dll." | ✓ |
| Obat (FORNAS M01–M10) | 10 | 10 | 10 (tabel v100) | ✓ |
| Sindikat | 9 (SYND-01…09) | 9 + 264 nilai literal `none` | 9 + 2 fraud tunggal | ✓ |
| Modus | 13 | 13 | - | - |
| Diagnosis table v100 (10 kode) | 13 aktual (bertambah I10, J45.9, N39.0) | 13 | 10 | perlu update |

Semua id berurutan lengkap: P01–P40 (0 entitas hilang), D01–D20, RS_A–RS_J. Entitas=v2.1 terpenuhi **pada hitungan** di kedua sumber; yang gagal **pada skema** hanya di dump Notion (3 kolom ID hilang) dan di keduanya (`seed`/`version`/`timestamp` nol).

---

## 7. Temuan Kualitas Data per Kategori (dengan ID baris)

### 7-1 (KRITIS) Skema v2.1 tidak lengkap - 3 dari 6 kolom hilang di dump Notion, 3 dari 6 di CSV v2.1
Dump Notion `claims_v2_live.csv`: `pasien_id`, `dokter_id`, `seed`, `version`, `timestamp` tidak ada sebagai kolom. CSV v2.1 di repo ML: `seed`, `version`, `timestamp` tidak ada; `pasien_id`/`dokter_id`/`faskes_id` ada. Protokol §8 (checksum + seed + versi kode) tidak dapat diverifikasi dari artefak mana pun. Didokumentasikan di §6; perbandingan lengkap di §9.

### 7-2 (KRITIS) Pemetaan sindikat meleset - 20 baris
SYND-06 (KLM101, KLM102, KLM103, KLM104) - pasien P21-P22 (doc P21-P24); skor 0,89–0,92 (doc 0,85–0,90).
SYND-07 (KLM105, KLM106, KLM107, KLM108) - pasien P23-P24 (doc P25-P28).
SYND-08 (KLM109, KLM110, KLM111, KLM112, KLM113, KLM114) - pasien P25-P26 (doc P29-P34); skor 0,86–0,89 (doc 0,75–0,80).
SYND-09 (KLM115, KLM116, KLM117, KLM118, KLM119, KLM120) - dokter D19 (doc D16); pasien P27 (doc P35-P40); skor 0,80–0,84 (doc 0,78–0,83).
KLM121 - doc RS_A/D03/P04, aktual RS_G/D13/P29.
KLM122 - doc RS_E/D09/P18, aktual RS_H/D14/P30.

### 7-3 (KRITIS) Kontribusi Saluran tidak menjelaskan skor - 42 baris
Tepat 258 baris, tidak tepat 42 (medium 10, high 9, fraud 23). Selisih sampai +0,17. 14 baris label Risiko tidak derivable: KLM123, KLM124, KLM125, KLM126, KLM127, KLM128, KLM129, KLM130, KLM131, KLM132, KLM133, KLM134, KLM135, KLM136.

### 7-4 (KRITIS) LOS = 0 menyatukan "tidak berlaku" dan "sinyal fraud" - 109 baris
**Tidak ada satupun sel LOS kosong** (CSV: 0 string kosong; JSON: 0 `null`). 109 baris bernilai `0`.
- 106 baris rawat jalan dengan LOS 0 - tetapi **5 baris rawat jalan lain punya LOS 1** (KLM029, KLM044, KLM059, KLM074, KLM089): layanan identik, nilai LOS tidak.
- **3 baris rawat inap dengan LOS 0**: KLM008, KLM010, KLM012 (semua SYND-03, prosedur 96.04 intubasi, dx K80.2). Rawat inap nol hari secara klinis mustahil; SHAP-justified memakai "LOS 0 padat kunjungan bedah mayor" sebagai sinyal deteksi.
- **Alasan pada 109 baris LOS-0 tidak pernah menyebut LOS** (0 dari 109 memuat kata "LOS"). Aturan kamus "nilai tidak berlaku dibedakan dari kosong" **tidak dijalankan**.
- Total biaya pada baris LOS-0: Rp153.310.000 - biaya/hari tak terdefinisi.
- Kolom `Layanan` yang sebenarnya membedakan layanan **tidak ada di kamus §5**.

### 7-5 (TINGGI) Kontradiksi Narasi = 12, bukan 8
Tambahan: **KLM105, KLM106, KLM107, KLM108** (SYND-07, iur biaya). Klaim v100 menyebut 8 (KLM001-006, KLM018, KLM024). Kriteria protokol v2.1 "8 klaim kontradiksi masuk daftar prioritas" harus dihitung ulang menjadi 12.

### 7-6 (TINGGI) Ambang 0,80 belum terkunci - KLM115
Satu-satunya baris pada batas. `03 §4` dan `10-simulation-dataset.md` berbeda redaksi; data konsisten dengan `≥` saja.

### 7-7 (TINGGI) 28 baris berisi literal `undefined` pada kolom `Rujukan`
KLM146, KLM147, KLM154, KLM155, KLM156, KLM158, KLM170, KLM173, KLM176, KLM188, KLM199, KLM207, KLM212, KLM213, KLM225, KLM235, KLM251, KLM255, KLM256, KLM262, KLM268, KLM276, KLM278, KLM282, KLM283, KLM295, KLM297, KLM298.
Contoh nilai: `undefined · RJ-2026-436 · 2026-06-03`. Ini kebocoran nilai JavaScript ke data, bukan FKTP yang tidak dikenal. Rasio lain: 161 baris "Puskesmas … · RJ-… · tanggal", 111 baris "kunjungan langsung (tanpa rujukan)".

### 7-8 (TINGGI) P11 memiliki 5 klaim, tabel v100 menyebut 4
Terdeteksi saat memverifikasi 38 entitas tabel v100 (Pasien/Dokter/Faskes) terhadap KLM001–KLM100: semua cocok kecuali P11.

### 7-9 (SEDANG) SYND-05: modus `cloning` tanpa prosedur hemiarthroplasty - KLM016, KLM017
Keduanya K35.8 → 47.09 Apendektomi, LOS 3, Rp7.450.000. Tabel v2.1 mendeskripsikan SYND-05 sebagai "dua klaim identik … (tanggal, dx, prosedur, LOS, biaya)". Yang ada: 20 dari 27 kolom data identik antara KLM016 dan KLM017; berbeda hanya `Name` (harus berbeda), `Skor Sentimen`, `Rujukan`, `Skor Fraud`, `Umpan Balik Pasien`, `Pasien`, `Catatan`. Sinyal "kloning" secara faktual benar (identik 20 kolom), tetapi **bukan skenario hemiarthroplasty** yang didokumentasikan.

### 7-10 (SEDANG) Sentinel `—` menggantikan sel kosong - 156 baris
`Prosedur ICD-9-CM` = `—` pada 156 baris (52%); `Obat` = `—` pada 3 baris (KLM004-006). Selain menutupi perbedaan "tidak ada prosedur" vs "prosedur tidak direkam", ini membuat filter `IS EMPTY` pada Notion tidak bekerja, dan melanggar aturan "nilai tidak berlaku dibedakan dari kosong" yang ditulis untuk LOS.

### 7-11 (SEDANG) Outlier biaya - 44 baris di atas pagar IQR
Median Rp4.475.000; Q1 Rp1.150.000; Q3 Rp9.337.500; pagar atas IQR Rp21.618.750; MAD Rp3.425.000 (robust z>3,5 juga menandai 44 baris - konsisten). 23 baris > Rp50.000.000. Rasio biaya terhadap tarif paket acuan (dari tabel v100): median 1,00, min 0,86, maks 5,59.
Baris dengan rasio > 1,5 (semua sudah diberi label anomali): KLM019 (5,59×, high), KLM121 (4,04×, fraud), KLM008/KLM010/KLM012 (2,80×, fraud), KLM123 (2,56×, high).
Rasio < 0,5: **tidak ada** - konsistensi internal terjaga.
29 baris biaya < Rp1.000.000 (Rp700.000–Rp950.000).

### 7-12 (SEDANG) `Sinyal SHAP` konstan per modus - 7 dari 13 modus
excessive_usage (6 baris), iur_biaya (4), phantom_billing (3), readmission_berulang (6), repeat_billing (4), cloning (2), biaya_markup (1) - masing-masing satu teks SHAP untuk seluruh barisnya. SHAP tidak pernah menyebut nilai kanal atau fitur terukur.

### 7-13 (SEDANG) Nomor rujukan duplikat - 2 grup
`RJ-2026-401`: KLM101 & KLM102 (P21, 2026-03-09). `RJ-2026-402`: KLM103 & KLM104 (P22, 2026-03-10). Keduanya memang skenario Repeat Billing SYND-06, jadi ** disengaja**, bukan cacat - dicatat agar tidak salah dibaca sebagai duplikasi tak sengaja.

### 7-14 (SEDANG) Duplikat near-identical - 2 grup
KLM101/KLM102 dan KLM103/KLM104: 25 dari 27 kolom data identik; yang berbeda hanya `Skor Fraud` (dan `Name`, yang memang harus berbeda). Keduanya (tanggal, pasien, dx, prosedur, LOS, biaya, narasi, obat, rujukan, SHAP, alasan, sentimen) identik penuh. Ini "repeat billing" yang disengaja, tetapi secara literal berarti **baris kedua bukan klaim baru** - ia duplikat dengan skor berbeda. Dampak: hit-rate per sindikat SYND-06 terhitung pada 4 klaim yang sebenarnya 2 klaim.
Duplikat payload penuh (seluruh 27 kolom data, `Name` diabaikan): **0 grup**. Duplikat (tanggal,pasien,dx,proc,LOS,biaya): **2 grup** (di atas).

### 7-15 (RINGAN) Casing nilai tidak konsisten
Kolom `Modus` memakai snake_case (`anomali_frekuensi`, `readmission_berulang`); kolom `Alasan` memakai Title Case (`FRAUD (Readmission Berulang)`, `FRAUD (Iur Biaya)`). Kolom `Sindikat` memakai `SYND-0n`. Tiga konvensi casing dalam tiga kolom terkait.

### 7-16 (RINGAN) Tidak ada manifest / checksum / seed dalam artefak
`03 §8` mewajibkan nama+versi, waktu ekspor, jumlah baris, checksum, kamus data, daftar kolom, definisi target & ambang, aturan pembersihan, split ID, seed+versi kode. Yang tersedia di CSV: jumlah baris dan `_last_edited` (4 nilai: 00:24, 04:41, 04:50, 04:51 - semuanya 2026-10-07). Checksum dihitung untuk laporan ini (lihat header) tetapi belum disertakan sebagai artefak.
Bonus: **`_last_edited` KLM031 = 2026-10-07T00:24**, satu-satunya baris pada waktu itu dan **satu-satunya baris dengan `Alasan` kosong** - indikasi strong bahwa KLM031 pernah diedit manual lalu `Alasan`-nya terhapus.

### 7-17 (RINGAN) Urutan baris CSV tidak deterministik
CSV tidak terurut menurut `Name` (dimulai KLM285, KLM278, KLM264…) maupun `Tanggal`. `_notion_page_id` juga tidak terurut. Baris tersusun per blok skenario (KLM101-104, KLM105-108, … lalu KLM001-003 di akhir). Tidak merusak data, tetapi menyulitkan diff antar-versi.

### 7-18 (RINGAN) `Umpan Balik Pasien` hanya 36 template untuk 300 baris
Distribusi: 1 teks dipakai 19×, 3 teks dipakai 3×, sisanya 1–2×. Negatif control bekerja (42 baris `low` bersentimen negatif), tetapi pengulangan template tinggi menambah risiko kebocoran label bila umpan balik dipakai sebagai fitur.

### 7-19 (TINGGI) `dokter_raw` terpotong 32 baris pada CSV v2.1 - hanya di repo ML, tidak di dump Notion
**32 dari 300 baris** pada `claims_300_v2.1.csv` kehilangan sufiks spesialisasi `Sp.JP)`:
- D04 (`D04 (dr. Danur Wibisono, ` - tanpa `Sp.JP)`) pada **11 baris**: KLM018, KLM027, KLM037, KLM047, KLM057, KLM067, KLM077, KLM087, KLM097, KLM211, KLM274.
- D16 (`D16 (dr. Prasetyo Utomo, ` - tanpa `Sp.JP)`) pada **21 baris**: KLM125, KLM127, KLM139, KLM140, KLM141, KLM157, KLM161, KLM162, KLM164, KLM169, KLM174, KLM182, KLM189, KLM195, KLM217, KLM227, KLM232, KLM244, KLM249, KLM273, KLM284.

Semua nilai terpotong **tepat 25 karakter mentah / 24 setelah `strip()`** (dua prefiks: `D04 (dr. Danur Wibisono, ` dan `D16 (dr. Prasetyo Utomo, `). Dump Notion sendiri **utuh** - `D04 (dr. Danur Wibisono, Sp.JP)` dan `D16 (dr. Prasetyo Utomo, Sp.JP)` pada kedua baris tersebut.

**Akar cause (terverifikasi dari `claims_db.json`):** di Notion, field `Dokter` pada 32 baris itu tersimpan sebagai **3 segmen `rich_text`**, bukan 1:

```
segmen 1: "D04 (dr. Danur Wibisono, "   (25 char, href=null)
segmen 2: "Sp.JP"                       (5 char, href="http://sp.jp/")   ← hyperlink
segmen 3: ")"                           (1 char, href=null)
```

Distribusi jumlah segmen `rich_text` pada kolom `Dokter` di `claims_db.json`: `{1 segmen: 268 baris, 3 segmen: 32 baris}` - **tepat 32 baris multi-segmen = 32 baris terpotong**. `Dokter` adalah satu-satunya properti multi-segmen di seluruh `claims_db.json` (semua properti lain 100% satu segmen).

**Uji 4 varian parser (semua 32 baris multi-segmen):**

| Varian parser | Cocok dengan `claims_300_v2.1.csv` |
|---|---|
| `rich_text[0]` saja (tanpa iterasi) | **32/32 ← producer yang sebenarnya** |
| `" ".join(rt['text']['content'])` - gaya `backend/src/data/notion_client.py:60` | 0/32 |
| `"".join(rt['plain_text'])` - gaya `Notion-docs/fetch_corpus.py:43-50` | 0/32 |
| markdown-link `[{text}]({href})` - gaya `fetch_corpus.py` + `href` | 0/32 |

Jadi ini **bukan** bug scraping Notion (`fetch_corpus.py` dan `notion_client.py` sudah benar mengonkatensasi seluruh segmen) - melainkan **bug eksportir CSV v2.1** yang hanya mengambil segmen pertama. Skrip pembuat CSV tidak ada di kedua repo: payload-nya di-embed sebagai base64+gzip di `notebooks/Aegis-JKN.ipynb` sel 3 (`EMBEDDED_CLAIMS_CSV_B64`), yang hasil dekompresinya **identik byte-per-byte** dengan `datasets/claims_300_v2.1.csv` (SHA-256 `37cf2236…27fd4e8`).

Dampak: kolom `dokter_raw` bukan representasi jujur dari `Dokter` di Notion, dan 32 baris kehilangan informasi spesialisasi. Di repo ML, `dokter_raw` dipakai sebagai `name` untuk FHIR `Practitioner` (`backend/src/oasis/agent_mapper.py:47`) - jadi 32 agent dokter kehilangan `Sp.JP` di display name. Lihat §9.3.

### Hal yang **terverifikasi bersih** (tidak menjadi temuan)
- Tidak ada duplikat payload penuh (0 grup).
- Tidak ada biaya negatif, nol, non-integer, atau di luar rentang wajar.
- Tidak ada kolom wajib kosong selain `Alasan` KLM031; `Alasan` pada seluruh 60 baris review/escalate terisi (aturan kamus terpenuhi).
- Tanggal: 300/300 valid ISO-8601; tidak ada tanggal klaim yang mendahului tanggal rujukan.
- `Sentimen` 100% konsisten dengan polaritas `Skor Sentimen`; semua skor dalam −1…1.
- Afiliasi dokter-faskes: 20 pasangan unik, 0 dokter di >1 faskes.
- 1 nama unik per ID pasien (40) dan dokter (20).
- Rasio biaya yang diklaim di dalam `Alasan`: **72 dari 72 cocok** dengan tarif acuan tabel v100 (toleransi 0,015). Golongan tanpa prosedur (72 baris) tidak menyebut rasio sama sekali.
- Median LOS yang diklaim di `Alasan` (pneumonia 5 hari, PCI 5 hari) cocok dengan median aktual (J18.9 = 5, I21.9 = 5).
- `Catatan` terisi pada seluruh 60 baris non-`low`, kosong pada 240 baris `low`.
- 72 dari 144 baris ber-prosedur-acuan menyebut "rasio"; 72 sisanya (baris tanpa prosedur) tidak punya tarif acuan - konsisten.
- Tabel v100 (Pasien 20, Dokter 12, Faskes 6): jumlah klaim & skor maks cocok pada 38 dari 39 entitas.

---

## 8. Rekomendasi (terurut)

### Prioritas P0 - sebelum dataset dipakai untuk validasi apa pun

1. **Kunci ambang risiko dan tulis di satu tempat berversi.** Putuskan `≥0.80` (konsisten dengan data) atau `>0.80` (redaksi 10-sim). Perbaiki redaksi `10-simulation-dataset.md` §Ekspansi v2 dan `03 §4` agar identik, lalu tambahkan baris KLM115 sebagai kasus uji batas pada test. **Perbaikan generator:** tetapkan `RISK_BANDS = [(0.00, 0.35, 'low'), (0.35, 0.60, 'medium'), (0.60, 0.80, 'high'), (0.80, 1.00, 'fraud')]` dengan operator **inklusif di batas bawah**, laluhasilkan label dari skor, bukan sebaliknya. Tambahkan test assertion untuk setiap baris.
2. **Lengkapi 3 kolom v2.1 yang benar-benar belum ada, dan salurkan ke dump Notion.** `pasien_id`, `dokter_id`, `faskes_id` **sudah ada** sebagai kolom terpisah di `mechine-learning-deep-learning/datasets/claims_300_v2.1.csv` (§9) - salinan itu tidak perlu dibuat ulang, cukup dirujuk. Yang belum ada di **artefak mana pun** adalah `seed` (20260707), `version` (v2.1), `timestamp` (ISO-8601 generasi). Tambahkan ketiganya ke CSV v2.1 **dan** ke dump Notion (`03 §5`), lalu tambahkan `metadata.json` berisi checksum SHA-256. Perhatikan juga bahwa `Catatan` (60 baris terisi) ada di Notion tapi hilang di v2.1 - putuskan apakah itu disengaja.
3. **Perbaiki generator agar `Kontribusi Saluran` menjumlah menjadi `Skor Fraud` persis, dan label diturunkan dari skor.** Terapkan aturan: `Skor Fraud = T + F + S` (tanpa toleransi), `Risiko = band(Skor Fraud)`, `Status = map(Risiko)`. Saat ini 42 baris melanggar aturan pertama dan 14 melanggar aturan kedua. Karena itu, hapus `Kontribusi Saluran` sebagai variabel independen dan hitung ulang dari skor.
4. **Perbaiki pemetaan sindikat sesuai tabel v2.1.** Alokasikan 4/4/6/6 pasien untuk SYND-06/07/08/09 (P21-P24, P25-P28, P29-P34, P35-P40), gunakan D16 untuk SYND-09, dan samakan KLM121 (RS_A/D03/P04) serta KLM122 (RS_E/D09/P18). Perbaiki juga rentang skor SYND-06 (0,85–0,90), SYND-08 (0,75–0,80), SYND-09 (0,78–0,83). Saat ini P28-P40 tidak pernah dipakai skenario apa pun.

### Prioritas P1 - kualitas & semantik data

5. **Pisahkan "tidak berlaku" dari "kosong" pada LOS.** Ganti `0` dengan `NULL` (kosong) untuk 106 baris rawat jalan dan tambahkan kolom `alasan_tidak_berlaku` atau enum `los_status ∈ {inap, jalan, not_applicable}`. Untuk 3 baris rawat inap LOS-0 (KLM008/KLM010/KLM012), **perbaiki data**: rawat inap harus LOS ≥ 1, atau ubah `Layanan`-nya menjadi `rawat jalan`. Tambahkan `Layanan` ke kamus §5 sebagai kolom wajib terdefinisi.
6. **Ganti sentinel `—` dengan sel kosong** pada `Prosedur ICD-9-CM` (156 baris) dan `Obat` (3 baris), atau tambahkan kolom status eksplisit bila `—` memang bermakna "tidak ada prosedur".
7. **Hapus literal `undefined` dari `Rujukan`** (28 baris). Gunakan `kunjungan langsung (tanpa rujukan)` atau nama FKTP yang benar, dan tambahkan validator yang menolak nilai string `undefined`/`null`/`NaN` di semua kolom.
8. **Isi `Alasan` KLM031** (satu-satunya baris kosong) dan tambahkan **test non-null untuk baris `review`/`escalate`** di pipeline generator.
9. **Selaraskan `Kontradiksi Narasi` dengan data.** Update 10-sim §Analisis Teks menjadi 12 klaim (tambah KLM105–KLM108) dan perbarui kriteria protokol v2.1 "8 klaim kontradiksi" → 12. Tambahkan test yang membandingkan jumlah `True` dengan konstanta yang didokumentasikan.
10. **Perbaiki tabel v100: P11 = 5 klaim** (bukan 4), dan tambahkan I10, J45.9, N39.0 ke tabel Diagnosis (13 aktual vs 10 didokumentasikan).
11. **Tetapkan aturan penetapan `Kontradiksi Narasi` dan definisi `Skor Sentimen`** (ambang antar kelas) dalam kamus §5 - keduanya kini berstatus TIDAK TERDOKUMENTASI.
11b. **Perbaiki parser `rich_text` di ekspor CSV v2.1** agar konkatenasi seluruh segmen, bukan hanya `rich_text[0]` - 32 baris kehilangan sufiks `Sp.JP)` (§7-19, §9.3). Tambahkan assertion panjang nilai pada 300 baris.

### Prioritas P2 - traceability & reproducibility

12. **Buat manifest artefak** berisi nama+versi, waktu ekspor, jumlah baris, checksum SHA-256, kamus data, daftar kolom dipakai/dikecualikan, definisi target+ambang, aturan pembersihan, split ID, dan seed+versi kode - sesuai `03 §8` (9 butir). Sertakan `data/raw/claims_300_v2.1.csv`, `edges_v2.1.json`, `text_gt_v2.1.csv`, `leakage_blocklist.yaml` sesuai struktur yang dijanjikan; saat ini tidak ada satu pun file itu.
13. **Konsistenkan casing** kolom `Modus` (snake_case) dengan prefiks `Alasan` (Title Case), atau tetapkan satu konvensi dan normalkan. Tambahkan kolom `modus_label` yang memetakan ke tabel sindikat sebagai daftar tertutup.
14. **Urutkan ekspor** menurut `Name` (atau `Tanggal`) agar diff antar-versi stabil, dan selaraskan `_notion_page_id` dengan urutan itu.
15. **Konsolidasikan `Umpan Balik Pasien`** - 36 template untuk 300 baris memakai 1 teks hingga 19×. Bila akan dipakai sebagai fitur NLP, diasingkan agar frasa negatif yang menunjuk fraud (KLM121 "Tagihan operasi terasa sangat besar") tidak muncul di baris `low` - sekarang pola ini dipakai juga pada baris `low` sehingga berisiko membocorkan label.

---

## 9. Perbandingan: Dump Notion vs `claims_300_v2.1.csv` (repo ML)

> **Tujuan.** Menjawab pertanyaan reprodusi data: apakah angka metrik yang dipresentasikan berasal dari dataset yang bisa diaudit, dan apakah dua salinan data bisa saling dipertanggungjawabkan? Sumber: `N:\HEALTHKATHON\mechine-learning-deep-learning\datasets\claims_300_v2.1.csv` (248.154 byte, SHA-256 `37cf2236…27fd4e8`, tracked di git repo `biezz-2/Aegis-JKN-mechine-learning-deep-learning` @ `00ca990`).

### 9.1 Keter Provenance - apakah keduanya dataset yang sama?

**Ya, artefak yang sama, diturunkan satu dari yang lain.** Bukti:

| Bukti | Hasil |
|---|---|
| `claims_db.json` (repo ML) ≡ dump Notion? | **Ya, identik.** 300 record, `Name` (KLM001–KLM300) cocok persis; 8 properti (`Tanggal`, `Biaya Rp`, `Risiko`, `Status`, `Sindikat`, `Skor Fraud`, `LOS hari`, `Faskes`) → **0 sel berbeda** |
| `claims_300_v2.1.csv` = turunan `claims_db.json`? | **Ya.** Dari 26 kolom dump Notion yang berpasangan: **23 identik** pada 300 baris, 2 beda hanya format (lihat §9.2), 1 kolom beda isi (truncasi, §9.3). `Catatan` dibuang |
| Headline number di CSV v2.1 | Total biaya Rp3.526.650.000 ✓; status 240/24/36 ✓; risiko 240/10/14/36 ✓; nominal per status Rp2.685.550.000 / Rp279.950.000 / Rp561.150.000 ✓ - **semuanya cocok** |

Artinya: **angka-angka di repo ML berasal dari dataset yang sama dengan yang diaudit di sini.** Tidak ada dataset bayangan yang berbeda. Yang berbeda hanya tingkat kelengkapan representasi.

### 9.2 Tabel per-kolom: Notion vs v2.1

| Kolom Notion | Kolom v2.1 | Sama? | Selisih contoh | Implikasi |
|---|---|---|---|---|
| `Name` | `claim_id` | **300/300 ✓** | - | Kunci baris konsisten; `claim_id` urut menaik (v2.1) sedangkan Notion tidak (§7-17) |
| `Tanggal` | `tanggal` | **300/300 ✓** | - | - |
| `Pasien` | `pasien_raw` | **300/300 ✓** | - | Rich text utuh di kedua sumber |
| `Pasien` (prefiks) | `pasien_id` | **300/300 ✓** | - | **Kolom ID murni tersedia di v2.1** - sumbu GroupKFold |
| `Dokter` | `dokter_raw` | **268/300** | 32 baris terpotong `Sp.JP)` (§9.3) | **CACAT** - v2.1 kehilangan spesialisasi |
| `Dokter` (prefiks) | `dokter_id` | **300/300 ✓** | - | ID murni tersedia |
| `Faskes` | `faskes_id` | **300/300 ✓** | - | Sudah bentuk kode murni di keduanya |
| `Diagnosis ICD-10` | `diagnosis_raw` | **300/300 ✓** | - | - |
| `Diagnosis ICD-10` (prefiks) | `diagnosis_code` | **300/300 ✓** | - | Kode murni tersedia (tambahan di luar janji) |
| `Prosedur ICD-9-CM` | `prosedur_raw` | **300/300 ✓** | - | - |
| `Prosedur ICD-9-CM` (prefiks) | `prosedur_code` | **300/300 ✓** | - | Kode murni tersedia |
| `Obat` | `obat` | **300/300 ✓** | - | - |
| `LOS hari` | `los_hari` | **300/300 ✓** | - | Aturan LOS **berlaku sama** di kedua sumber (§9.4) |
| `Biaya Rp` | `biaya_rp` | **300/300 ✓** | - | - |
| `Narasi Rekam Medis` | `narasi_rekam_medis` | **300/300 ✓** | - | - |
| `Kontradiksi Narasi` | `kontradiksi_narasi` | **0/300 (format)** | Notion `True`/`False` vs v2.1 `1`/`0` | Semantik identik (0 baris beda) - hanya encoding |
| `Skor Fraud` | `skor_fraud` | **300/300 ✓** | - | - |
| `Risiko` | `risiko` | **300/300 ✓** | - | - |
| `Status` | `status` | **300/300 ✓** | - | - |
| `Modus` | `modus` | **300/300 ✓** | - | - |
| `Sindikat` | `sindikat` | **36/300 (format)** | Notion `""` vs v2.1 `"none"` | Semantik identik: himpunan ID sama persis (264) - hanya encoding |
| `Alasan` | `alasan` | **300/300 ✓** | - | - |
| `Sinyal SHAP` | `sinyal_shap` | **300/300 ✓** | - | - |
| `Kontribusi Saluran` | `kontribusi_saluran` | **300/300 ✓** | - | - |
| `Skor Sentimen` | `skor_sentimen` | **300/300 ✓** | - | - |
| `Sentimen` | `sentimen` | **300/300 ✓** | - | - |
| `Umpan Balik Pasien` | `umpan_balik_pasien` | **300/300 ✓** | - | - |
| `Alasan Berobat` | `alasan_berobat` | **300/300 ✓** | - | - |
| `Layanan` | `layanan` | **300/300 ✓** | - | - |
| `Rujukan` | `rujukan` | **300/300 ✓** | - | - |
| - | `is_fraud` | **kolom baru** | 36 `"1"` / 264 `"0"` | Label biner eksplisit; **deterministik** = `risiko == "fraud"` (0 baris beda, baik lintas sumber maupun internal v2.1) |
| - | `Catatan` | **hilang di v2.1** | - | `Catatan` ada di Notion (60 baris terisi) tapi tidak ada di CSV v2.1 - konteks auditor hilang |
| - | `_notion_page_id`, `_last_edited` | **hanya di Notion** | - | Metadata Notion; v2.1 lebih bersih untuk ML, tapi tanpa jejak edit |

**Total sel berbeda: 596** - seluruhnya bisa dijelaskan: 264 (format `""`↔`"none"`) + 300 (format `True`↔`1`) + 32 (truncasi `dokter_raw`). **Tidak ada satu pun sel yang berbeda karena nilai substantif.**

**Rekap kolom:** dump Notion punya 27 kolom data + 2 metadata Notion. Yang berpasangan dengan v2.1: **26** (semua kecuali `Catatan`). Di antara 26 itu: **23 identik** pada 300 baris, **2 beda format** (`Kontradiksi Narasi`, `Sindikat`), **1 beda isi** (`Dokter` → `dokter_raw`). `Catatan` hilang di v2.1; v2.1 menambah 5 kolom (`pasien_id`, `dokter_id`, `diagnosis_code`, `prosedur_code`, `is_fraud`) yang tidak berpasangan langsung.

### 9.3 Temuan baru: `dokter_raw` terpotong di 32 baris (KRITIS untuk dataset v2.1)

Rinci di §7-19. Ringkas:

| Aspek | Detail |
|---|---|
| Baris terdampak | 32 dari 300 - **D04 (11 baris)** dan **D16 (21 baris)**, keduanya spesialis `Sp.JP` |
| Gejala | `D04 (dr. Danur Wibisono, ` - sufiks `Sp.JP)` hilang |
| Di dump Notion | **Utuh** - `D04 (dr. Danur Wibisono, Sp.JP)` |
| Akar cause | Field Notion `Dokter` pada 32 baris = **3 segmen `rich_text`** (segmen tengah `Sp.JP` ber-`href="http://sp.jp/"`); parser v2.1 ambil `rich_text[0]` saja |
| Bukti | `claims_db.json`: `{1 segmen: 268, 3 segmen: 32}` - **32 = 32**, persis. `Dokter` satu-satunya properti multi-segmen di seluruh DB |
| Uji 4 varian parser | `rich_text[0]` saja → **32/32 cocok**; `" ".join(text.content)` (`notion_client.py:60`) → 0/32; `"".join(plain_text)` (`fetch_corpus.py:43-50`) → 0/32; markdown-link + `href` → 0/32 |
| Sumber bug | **Eksportir CSV v2.1**, bukan scraper Notion - `fetch_corpus.py` dan `notion_client.py` sudah mengonkatensasi seluruh segmen dengan benar. Skrip pembuat CSV tidak ada di kedua repo: payload-nya di-embed base64+gzip di `notebooks/Aegis-JKN.ipynb` sel 3 (`EMBEDDED_CLAIMS_CSV_B64`), hasil dekompresinya identik byte-per-byte dengan `datasets/claims_300_v2.1.csv` |
| Dampak | `dokter_raw` salah merepresentasikan sumber; 32 baris kehilangan informasi spesialisasi. Di repo ML, `dokter_raw` menjadi `name` FHIR `Practitioner` (`backend/src/oasis/agent_mapper.py:47`) → 32 agent dokter kehilangan `Sp.JP` di display name |
| Perbaikan | Konkatenasi seluruh segmen: `''.join(x['plain_text'] for x in rich_text)` |

### 9.4 Verifikasi ulang temuan utama terhadap CSV v2.1

Pertanyaan yang dijawab di sini: apakah temuan §7-4 (LOS), §7-3 (Kontribusi Saluran), §7-2 (sindikat), §7-5 (Kontradiksi Narasi), §7-7 (`undefined`), §7-10 (sentinel `—`), §7-12 (SHAP konstan) adalah **artefak scraping Notion** atau **fitur desain generator**. Jawabannya: **fitur desain generator** - keduanya identik baris-per-baris.

| Temuan | Dump Notion | CSV v2.1 | Himpunan ID sama? | Interpretasi |
|---|---|---|---|---|
| LOS `0` (bukan kosong) | 109 baris, 0 kosong | 109 baris, 0 kosong | **Ya** (identik) | Cacat desain generator |
| `Kontribusi Saluran` ≠ Skor | 42 baris (selisih s/d +0,17) | 42 baris (sama persis) | **Ya** (identik) | Cacat desain generator |
| Sindikat: 4 dari 9 salah mapping | 20 baris | 20 baris, entitas identik | **Ya** (identik) | Cacat desain generator |
| `Kontradiksi Narasi` = 12 (bukan 8) | 12 | 12 | **Ya** (identik) | Cacat desain generator |
| `Rujukan` berisi `undefined` | 28 baris | 28 baris | **Ya** (identik) | Cacat desain generator |
| Sentinel `—` pada Prosedur | 156 baris | 156 baris | **Ya** (identik) | Cacat desain generator |
| Sentinel `—` pada Obat | 3 baris | 3 baris | **Ya** (identik) | Cacat desain generator |
| SHAP konstan per modus | 7 dari 13 modus | 7 dari 13 modus (nilai identik) | **Ya** (identik) | Cacat desain generator |
| `Alasan` kosong | 1 (KLM031) | 1 (KLM031) | **Ya** (identik) | Cacat desain generator |
| `Modus` kosong | 240 | 240 | **Ya** (identik) | Cacat desain generator |
| Skor tepat 0,80 (KLM115) | `0.8` → `fraud` | `0.8` → `fraud`, `is_fraud=1` | **Ya** | Kasus pembeda ambang **tidak berubah** |

**Konsekuensi: tidak ada temuan yang bisa dibuang sebagai artefak scraping.** Semuanya harus diperbaiki di generator.

### 9.5 KLM115 - kasus pembeda ambang 0,80

| Sumber | `skor_fraud` | `risiko` | `status` | `is_fraud` | `sindikat` | `modus` |
|---|---|---|---|---|---|---|
| Dump Notion | 0,8 | fraud | escalate | - | SYND-09 | excessive_usage |
| CSV v2.1 | 0,8 | fraud | escalate | 1 | SYND-09 | excessive_usage |

Identik. **Ambang `≥0,80` adalah satu-satunya interpretasi yang konsisten dengan kedua sumber.** Tidak ada baris lain dengan skor tepat 0,35 atau 0,60, jadi kedua ambang bawah itu tetap **tidak teruji** oleh data (celah data 0,14–0,40 dan 0,53–0,62).

### 9.6 Struktur v2.1 untuk evaluasi grup - dan definisi label yang dipakai

Sumbu grup di CSV v2.1: `pasien_id` (40), `faskes_id` (10), `dokter_id` (20).

| Sumbu | Klaim per grup | Terminal state |
|---|---|---|
| `pasien_id` | 6–12 (median 7) | GroupKFold(5) - **sudah diimplementasikan** (notebook `Aegis-JKN.ipynb` sel 11) |
| `faskes_id` | 14–45 | LeaveOneGroupOut(10) - tersedia |
| `dokter_id` | 2–33 | sumbu tambahan tersedia |

Catatan konformitas label (bukan evaluasi model): notebook mendefinisikan target sebagai
`y_target = (is_fraud == 1) | (sindikat != 'none')` → **38 baris positif**, bukan 36.
Selisih 2 adalah **KLM016 & KLM017** (label `high`, `Sindikat=SYND-05`). Jadi target eksperimen bukan label fraud murni, dan ini konsisten dengan kamus §7 yang melarang `Sindikat` sebagai fitur input. Catatan: 16 dari 40 pasien tercatat di lebih dari 1 faskes (pasien berpindah fasilitas), sedangkan 0 dokter berpindah faskes - jadi LeaveOneGroupOut per faskes tidak identik dengan pemisahan per dokter.

### 9.7 Rekomendasi tambahan (hasil perbandingan)

16. **Perbaiki parser `rich_text` di pipeline ekspor v2.1** agar konkatenasi seluruh segmen, bukan hanya `rich_text[0]`. Tambahkan assertion `assert len(dokter_raw) == len(notion_dokter)` pada 300 baris. Tanpa ini, `dokter_raw` pada 32 baris ≠ sumber.
17. **Kirim ulang CSV v2.1 dengan `seed`, `version`, `timestamp`** - satu-satunya 3 dari 6 kolom yang benar-benar belum ada di artefak mana pun. Tambahkan `metadata.json` berisi SHA-256.
18. **Pertahankan `Catatan` di CSV v2.1** (atau dokumentasikan bahwa sengaja dibuang) - 60 baris konteks auditor hilang tanpa jejak.
19. **Dokumentasikan konvensi encoding** `is_fraud ∈ {0,1}`, `sindikat = "none"` (bukan kosong), `kontradiksi_narasi ∈ {0,1}` di kamus §5 - tiga perbedaan format yang "G/S/0" dan "none" ini harus didokumentasikan, meski harmonis dengan Notion.

---

## Lampiran A - Reproduksi

```
python -X utf8 analysis/reports/scripts/04_audit.py         # skema, angka, ambang, lintas kolom, entitas
python -X utf8 analysis/reports/scripts/04_audit_round2.py  # LOS, sindikat, rasio, tanggal, kloning
python -X utf8 analysis/reports/scripts/04_audit_round3.py  # rasio (parsing ID), tabel v100, kanal vs skor
python -X utf8 analysis/reports/scripts/04_audit_round4.py  # kanal konstan, median LOS, template
python -X utf8 analysis/reports/scripts/04_audit_round5.py  # kolom kamus, _last_edited, sentimen
python -X utf8 analysis/reports/scripts/04_audit_round6.py  # pemetaan sindikat, sentinel, rujukan
python -X utf8 analysis/reports/scripts/04_audit_round7.py  # pemetaan sindikat final + checksum
python -X utf8 analysis/reports/scripts/04_audit_round8.py  # presisi: pola kanal, selisih, label non-derivabel
python -X utf8 analysis/reports/scripts/04_audit_round9.py  # diagnosis 4 kegagalan harness (bug skrip, bukan data)
python -X utf8 analysis/reports/scripts/04_audit_final_check.py  # harness: 120 asersi angka laporan
python -X utf8 analysis/reports/scripts/04_audit_compare_v21.py  # dump Notion vs claims_300_v2.1.csv
python -X utf8 analysis/reports/scripts/04_audit_compare_check.py  # harness: 150 asersi perbandingan
```

Keluaran teks tiap skrip tersimpan berdampingan di `analysis/reports/scripts/` sebagai `04_audit_output.txt`, `04_audit_round2_output.txt`, …, `04_audit_round9_output.txt`, `04_audit_final_check_output.txt`, `04_audit_compare_v21_output.txt`, `04_audit_compare_check_output.txt`. Ringkasan terstruktur tersimpan di `04_audit_results.json`.

`04_audit_final_check.py` adalah harness verifikasi: ia memuat 120 asersi (`chk(label, got, exp)`) atas setiap angka yang dikutip di laporan ini - jumlah baris, checksum total nominal dan per status, hitungan label, ambang, matriks Status×Risiko, pola kanal, rentang skor sindikat, entity count, duplikat, dan seterusnya. Hasil: **120/120 OK**. Empat kegagalan pada versi pertama harness adalah defect skrip (urutan duplikat, artefak floating point pada ambang 0,02, dan parsing desimal berganda pada rasio "1,03" vs "1.03"), bukan Temuan data; diagnosisnya ada di `04_audit_round9_output.txt`.

`04_audit_compare_check.py` adalah harness kedua, khusus seksi §9: **150 asersi** atas perbandingan dump Notion vs `claims_300_v2.1.csv` - kolom identik per-kolom (termasuk rekap jumlah kolom 23 identik / 2 format / 1 isi), kesetaraan semantik `True`/`1` dan `""`/`none`, konsistensi `is_fraud`, KLM115, aturan LOS, ke-7 pola bermasalah, pemetaan entitas sindikat, jumlah sel berbeda, akar cause truncasi `dokter_raw` (termasuk **uji 4 varian parser**), sumbu evaluasi grup, dan re-verifikasi headline number pada CSV v2.1. Hasil: **150/150 OK**.

Setiap angka pada laporan ini dapat ditelusuri ke salah satu dari: (a) blok keluaran yang ditandai header seksi di file output, (b) baris kode yang menghasilkannya di skrip terkait. Tidak ada angka yang/plugin dari sumber dokumentasi tanpa dihitung ulang.
