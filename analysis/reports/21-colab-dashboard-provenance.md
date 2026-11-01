# 21 - Audit Provenance Dashboard Oasis (PDF Colab) dan Rekonsiliasi Metrik Headline

**Tanggal audit:** 22 Oktober 2026
**Artefak utama:** `mechine-learning-deep-learning/colab/Hasil simulasi dari 300 dataset notion.pdf` (3.800.507 B, **16 halaman**, **image-only**, tanpa text layer)
**Sumber yang berhasil diidentifikasi:** `mechine-learning-deep-learning/colab/Aegis_JKN_FIXX.ipynb` (720.813 B, 6 sel) - dibuktikan lewat metadata PDF (`title = "Aegis-JKN-FIXX - Colab"`, `author = "Attabi ."`, `producer = Microsoft: Print To PDF`, `creationDate = D:20261007233139+07'00'`)
**Artefak pendukung:** `colab/payload-aegis-jkn.json` (26.703 B, payload dashboard), `colab/dashboard-aegis-jkn.html` (150.741 B)
**Checker:** `analysis/reports/scripts/_fixx_repro.py`, `_docparse.py`, `_entity.py`, `_entity2.py`, `_fragile.py`, `_env.py`, `_pdfmeta.py`, `_propcheck.py`, `_syncheck.py`, `_means.py`, `_prec.py`, `_degen.py`, `_metriccompat.py` (pustaka standar saja, tanpa pandas/numpy/sklearn)
**Spesifikasi acuan:** `analysis/corpus/00-dashboard.md` §4, `analysis/corpus/04-evidence-matrix.md` E-07 s.d. E-12, `analysis/corpus/10-simulation-dataset.md`, `analysis/corpus/11-archive-proposal.md`, `analysis/reports/17-roadmap.md:382,490`

> Catatan koreksi: nama berkas PDF menyebut "300 dataset", tetapi dashboard yang benar-benar dirender memakai **100 klaim v1**, bukan 300. Laporan ini menguraikan bukti, reproduksi, dan dampaknya.

---

## 1. Ringkasan Eksekutif

Berkas PDF yang dicatat di `17-roadmap.md:490` sebagai "*image-only tanpa text layer - belum dibaca siapa pun, tidak dapat diekstraksi*" ternyata **sudah dapat direproduksi secara deterministik**. Sumbernya adalah `Aegis_JKN_FIXX.ipynb`, dan seluruh angka pada dashboard dapat dihitung ulang tanpa Ollama, tanpa GPU, dan tanpa model apa pun. Temuan ini menutup celah G-31.

Temuan utama:

1. **Angka "93,0%" pada PDF adalah akurasi sentimen leksikon, bukan akurasi deteksi fraud.** PDF menampilkan KPI "Akurasi Sentimen Simulasi" = 93,0% dengan sublabel "klasifikasi leksikon vs ground truth (200 uji)". Angka identik muncul di `00-dashboard.md` §4 sebagai metrik performa model yang belum boleh disebut tervalidasi. Keduanya adalah kebetulan numerik yang berbahaya: angka yang sama dipakai untuk dua kuantitas berbeda, sehingga pembaca dapat menyimpulkan bahwa akurasi deteksi fraud = 93,0%.

2. **Nilai 93,0% adalah konsekuensi deterministik dari satu bug substring, bukan hasil pengukuran.** 14 dari 200 klasifikasi gagal, dan **14 gagal itu persis seluruhnya** post Reddit berlabel "Netral". Penyebabnya: kata negatif `"lama"` (bobot 1) adalah substring dari kata **"Pengalaman"** pada judul Reddit yang tetap (`"[Diskusi] Pengalaman klaim JKN di {faskes}"`). Skor = tanh(-1) = -0,7616 < -0,15 sehingga otomatis "Negatif". 93,0% = (200 - 14)/200 secara aritmetika.

3. **Klasifikasi Twitter 100% benar bukan kebetulan, melainkan tautologi yang dirancang.** Komentar kode sumber menyatakannya terbuka: *"Teks disusun agar klasifikasi leksikon ≡ ground truth (deterministik)."* `_core_text()` memilih kalimat kunci **berdasarkan `c["gt_sentimen"]`**, jadi setiap label GT punya frasa leksikon yang dijamin memicunya. Akurasi Twitter = 100/100, akurasi Reddit = 86/100, total 186/200. Angka 93,0% mengukur **seberapa baik leksikon cocok dengan template yang dibuat untuknya**, bukan kemampuan klasifikasi.

4. **Klasifikasi Reddit tidak pernah menghasilkan "Netral" sama sekali.** `rdSent` pada payload = **[62, 0, 38]** (positif/netral/negatif), bukan [62, 14, 24] seperti GT dan Twitter. Grafik pie Reddit di dashboard yang dipublikasikan menampilkan **0% Netral** - kategori yang justru menjadi tempat seluruh 14 kegagalan berada. Distribusi label Reddit hanya punya dua nilai, padahal leksikon punya ambang tiga nilai; ini konsekuensi bug substring yang membuat 14 teks Netral melompat ke "Negatif".

5. **"100% deteksi fraud" dan "100% hit-rate per sindikat" adalah hasil label-by-construction, bukan performa model.** Skor fraud pada generator v1 ditulis tangan dan label `risk = "fraud"` hanyalah ambang `skor > 0,80`. Karena itu "fraud" selalu menempati 14 peringkat teratas. Tidak ada model yang dilatih, tidak ada split, tidak ada file prediksi. AUC `p_fused` terhadap label fraud = 1,000 secara deterministik.

6. **Angka benchmark proposal berasal dari konstanta hardcode, bukan dari perbandingan model.** `backend/src/oasis/simulation.py:294-325` mendefinisikan `compare_with_baseline(..., baseline_auprc: float = 0.71)` dengan dict `benchmarks` berisi literal (Rule-based 0,58; Logistic Regression 0,62; XGBoost 0,71; GNN 0,78; Hybrid GNN+XGB 0,85; MHGSL 0,91). `backend/src/api/main.py:365-400` mengulang konstanta yang sama untuk radar chart dan `auprc_data`. **Tidak ada satu pun angka baseline yang dihitung.** Klaim "+28,6% dibanding baseline XGBoost" adalah hasil membagi konstanta 0,9142 dengan konstanta 0,71 (0,9142/0,71 - 1 = 28,7606%).

7. **Metrik headline proposal tidak ada di kode ML, hanya di generator DOCX.** Angka 0,9825 / 0,9142 / 94,12 / 89,4 / 10,6 hanya ditemukan di `dokumen/section_bab_7_to_9.py`, `dokumen/section_cover_preface.py`, `dokumen/section_bab_1_to_3.py`, `analysis/corpus/11-archive-proposal.md`, `analysis/corpus/14-index.md`, dan skrip audit. **Tidak ada** di `backend/src/`, **tidak ada** di notebook pelatihan.

8. **Presisi 94,12% tidak dapat dicapai pada ambang mana pun di dataset 300.** Pemindaian exhaustif atas seluruh nilai unik `skor_fraud` menghasilkan **0 hit**. Presisi terdekat yang bisa dicapai: 94,7368% (ambang 0,78, FP = 2) dan 92,3077% (ambang 0,74, FP = 3). FPR 10,6% **dapat** direproduksi, tetapi hanya pada ambang 0,14 (28 FP dari 264 negatif), yang memberi presisi 56,25% - bukan 94,12%. Tidak ada satu ambang yang memenuhi kedua klaim itu.

9. **Saluran "fitur" MHGSL nyaris tidak informatif: kepadatan edge 92,18%.** 4.563 dari 4.950 pasangan klaim memenuhi cosine ≥ 0,85, karena 76 klaim normal memakai template identik sehingga pairwise cosine = 1,000 di antaranya. `synd_density` = 1,00 untuk kelima sindikat karena itu artefak duplikasi template.

10. **Tabel entitas pada `10-simulation-dataset.md` tidak cocok dengan data mana pun.** Tidak cocok dengan generator v1 yang menghasilkan PDF, tidak cocok dengan dataset 300 aktual. 6 dari 6 faskes, 10 dari 10 diagnosis, 12 dari 12 dokter, 20 dari 20 pasien tidak cocok pada jumlah klaim; skor maksimum juga berbeda pada 3 dari 10 diagnosis dan 9 dari 20 pasien.

11. **Angka Rp507.370.000 adalah haircut proporsional, bukan hasil kalkulasi tarif.** Pada dataset 300, 60 klaim non-`auto_clear` bernilai nominal Rp841.100.000; Rp507.370.000 = 60,32% dari nilai itu, dan "Rp8,46 juta per kasus" = target ÷ 60, bukan target ÷ 36 (Rp14.093.611).

12. **Kode kanal-teks "p_lead > 0.85" yang terbaca pada PDF tidak ada di sumber.** Baris HTML sumber berbunyi `p_fused = p_graph + γ·f_text·(1 − p_graph) · γ = 0.10 · θ_feat = 0.85`. Rerenderan bitmap 90° membuat `θ_feat` terbaca sebagai `p_lead`.

---

## 2. Tabel Severity

| Severity | Jumlah | Ringkasan |
|---|---|---|
| CRITICAL | 8 | (1) 93,0% = akurasi sentimen, dipakai sebagai akurasi fraud di corpus; (2) 93,0% deterministik dari bug substring; (3) teks disusun agar leksikon cocok dengan GT - akurasi 93,0% adalah tautologi; (4) klasifikasi Reddit tidak pernah menghasilkan "Netral" (rdSent = 62/0/38); (5) 100% deteksi & 100% hit-rate = label by construction, tanpa model; (6) angka baseline proposal hardcode, bukan hasil perbandingan; (7) metrik headline tidak ada di kode ML, hanya di generator DOCX; (8) tabel entitas `10-simulation-dataset.md` tidak cocok dengan data mana pun |
| HIGH | 5 | kepadatan edge 92,18%; toleransi antrian hanya 1 poin; ketergantungan 93,0% pada Ollama; PDF "300 dataset" sebenarnya 100 klaim; 10,6% FPR tidak konsisten dengan 94,12% presisi |
| MEDIUM | 4 | `synd_density` 1,00 non-informatif; ambang 0,80 terpilih agar pas; 4/100 klaim bisa kena LLM; komentar kode "1000 langkah" kedaluwarsa |
| LOW | 3 | flag kontradiksi tidak berkorelasi dengan peringkat; tidak ada `p_lead` di sumber; jumlah halaman PDF 16, bukan 17 |
| **Total** | **20** | |

---

## 3. Metrik Dashboard PDF vs Artefak yang Ada

Seluruh angka berikut tereproduksi persis oleh `analysis/reports/scripts/_fixx_repro.py` (deterministik, tanpa Ollama) dan cocok dengan `colab/payload-aegis-jkn.json` di field demi field (`kpi` = 100 klaim, 14 fraud, det_rate 100, queue 20, accuracy 93, feat_edges 4563, synd_density 1,0 ×5, kontra 8/8, capacity 6667, prevalensi 14; `meta` = v2.1, seed 20260707, theta_feat 0,85, gamma_text 0,10, model mistral-oasis:24b, steps 300).

| # | Angka pada PDF / payload | Sumber kode | Nilai reproduksi | Status |
|---|---|---|---|---|
| 1 | "Audit ground truth: 100 klaim" | `assert len(CLAIMS) == 100` | 100 | **Reproduksi** |
| 2 | Distribusi risiko 76 low · 4 med · 6 high · 14 fraud | `risk_label()` | 76/4/6/14 | **Reproduksi** |
| 3 | Sentimen GT 62 / 14 / 24 | `_gt_sent` | 62/14/24 | **Reproduksi** |
| 4 | 8 klaim kontradiksi | `assert sum(...) == 8` | 8 | **Reproduksi** |
| 5 | Akurasi sentimen 93,0% (186/200) | `accuracy = match/(2*len(CLAIMS))` | 93,0% (186/200) | **Reproduksi, bukan metrik fraud** |
| 5a | Akurasi Twitter (tersirat, tak dipisah) | `tw_label == gt_sentimen` | 100/100 = 100,00% | **Reproduksi, tautologi per desain** |
| 5b | Akurasi Reddit (tersirat, tak dipisah) | `rd_label == gt_sentimen` | 86/100 = 86,00% | **Reproduksi** |
| 6 | Deteksi fraud 14/14 = 100% | `det_rate` | 14/14 (100%) | **Reproduksi, label by construction** |
| 7 | Antrean investigasi 20 klaim (20%) | `int(len(CLAIMS)*QUEUE_RATE)` | 20 | **Reproduksi** |
| 8 | Hit-rate sindikat 100% × 5 | `synd_hit[s]["rate"]` | 100,0% × 5 | **Reproduksi, label by construction** |
| 9 | `feat_edges` 4.563 | loop cosine ≥ 0,85 | 4563 | **Reproduksi** |
| 10 | `synd_density` 1,00 × 5 | `synd_density` | 1,0 × 5 | **Reproduksi, non-informatif** |
| 11 | `capacity` ±6.667 berkas | `round(1000*(20/3))` | 6667 | **Reproduksi** (turunan asumsi 20 → 3 menit) |
| 12 | `prevalensi` 14% | `len(fraud)/len(CLAIMS)` | 0,14 | **Reproduksi, oversampled** |
| 13 | "Akurasi sentimen aktif pada 17 klaim" | `f_text` | 17 | **Reproduksi** |
| 14 | `twSent` = [62, 14, 24] | `sent_dist("tw_label")` | [62, 14, 24] | **Reproduksi** |
| 15 | `rdSent` = [62, **0**, 38] | `sent_dist("rd_label")` | [62, 0, 38] | **Reproduksi, kelas Netral hilang** |
| 16 | `p_lead > 0.85` | **tidak ada di sumber** | - | **Salah baca PDF** |
| 17 | 93,0% = akurasi fraud | tidak ada di sumber mana pun | - | **Tidak ada artefak** |
| 18 | Precision 94,12% | tidak ada di sumber komputasi | - | **Tidak ada artefak** |
| 19 | ROC-AUC 0,9825 | tidak ada di sumber komputasi | - | **Tidak ada artefak** |
| 20 | AUPRC 0,9142 | tidak ada di sumber komputasi | - | **Tidak ada artefak** |
| 21 | Ketahanan masking 89,4% | tidak ada di sumber komputasi | - | **Tidak ada artefak** |
| 22 | FPR 10,6% | tidak ada di sumber komputasi | - | **Tidak ada artefak** |

---

## 4. Temuan CRITICAL

### C-1 - Angka "93,0%" pada PDF adalah akurasi sentimen, bukan akurasi deteksi fraud

**Bukti.** Payload dashboard (`colab/payload-aegis-jkn.json`) menyimpan metrik ini di `kpi.accuracy = 93`, dan HTML yang menghasilkannya memuat label KPI (`21_fixx_nb.txt:843`):

```
Akurasi Sentimen Simulasi
klasifikasi leksikon vs ground truth (200 uji)
```

Kode komputasinya (`21_fixx_nb.txt:664-667`):

```python
# Akurasi klasifikasi simulasi vs ground truth (200 klasifikasi: 100 TW + 100 RD)
match = sum(1 for c in CLAIMS if c["tw_label"] == c["gt_sentimen"]) + \
        sum(1 for c in CLAIMS if c["rd_label"] == c["gt_sentimen"])
accuracy = match / (2 * len(CLAIMS))
```

Tidak ada metrik klasifikasi fraud di seluruh notebook; `is_fraud` tidak pernah dipakai di FIXX. Output sel notebook mengonfirmasi labelnya sendiri: "Akurasi sentimen simulasi vs GT: 93.0% (186/200 klasifikasi)".

**Dampak.** `analysis/corpus/00-dashboard.md:47` mendaftarkan "Accuracy 93,0%" pada daftar "Belum boleh disebut hasil tervalidasi", yang mengimplikasikan akurasi model deteksi fraud. Dua artefak berbeda memakai angka identik untuk dua kuantitas berbeda, dan korpus tidak pernah menyatakan bahwa angka itu berasal dari akurasi sentimen. Setiap dokumen turunan yang mengutip "93,0%" tanpa kualifikasi sedang mengutip metrik leksikon.

**Rekomendasi.** Tambahkan kalimat eksplisit di `00-dashboard.md` §4: *"Angka 93,0% yang muncul pada dashboard Oasis adalah akurasi klasifikasi sentimen leksikon, bukan akurasi deteksi fraud; kuantitas ini tidak boleh dipindahkan ke konteks performa model."* Ubah label dashboard menjadi "Akurasi Sentimen (bukan akurasi fraud)".

### C-2 - 93,0% adalah bug substring, bukan pengukuran

**Bukti (reproduksi deterministik).** 14 dari 200 klasifikasi gagal; **seluruhnya** adalah post Reddit berlabel "Netral":

```
KLM015 KLM017 KLM019 KLM022 KLM032 KLM041 KLM050
KLM058 KLM066 KLM073 KLM081 KLM089 KLM092 KLM099
semua: gt=Netral -> got=Negatif, score=-0.762, signal=''
```

`reddit_template()` memakai judul konstan (`21_fixx_nb.txt:459-468`):

```python
title = f"[Diskusi] Pengalaman klaim JKN di {faskes}"
```

Leksikon negatif memuat `"lama": 1`. Substring `"lama"` muncul di dalam kata **"Pengalaman"** pada judul itu, sehingga setiap post Reddit mendapat skor -1 apa pun isinya. Post Netral tidak punya kata POS/NEG lain untuk mengompensasi, sehingga `tanh(-1) = -0,7616 < -0,15` menjadi "Negatif". Post Positif/Negatif punya kata tambahan yang menutupi -1, sehingga lolos.

Kode pencocokannya memakai operator `in` pada string mentah, tanpa batas kata (`21_fixx_nb.txt:392-394`):

```python
low = text.lower()
pos = sum(w for wd, w in POS_WORDS.items() if wd in low)
neg = sum(w for wd, w in NEG_WORDS.items() if wd in low)
```

Konsekuensinya: **93,0% = (200 - 14)/200** secara aritmetika, dan 7% itu adalah bug, bukan batas kemampuan. Perbaikan satu baris (batas kata / stemming) mengubah angka ini. Klaim "akurasi 93,0%" dengan demikian **tidak stabil terhadap perbaikan kode**.

**Dampak.** `public/dashboard-aegis-jkn.html` dan `src/data/oasis-data.ts` memakai "93.0%" sebagai KPI sorotan. Angka yang rapuh ini dipamerkan sebagai bukti kualitas sistem.

**Rekomendasi.** Perbaiki pencocokan leksikon (tokenezasi + batas kata), jalankan ulang, dan publikasikan angka hasil yang diperbaiki beserta skripnya. Sampai itu selesai, **hapus 93,0% dari semua KPI yang bersifat performa** dan ganti dengan "skor sentimen simulasi (indikator sintaks, bukan performa model)".

### C-3 - Teks simulasi dirancang agar leksikon cocok dengan label: akurasi 93,0% adalah tautologi

**Bukti.** Komentar kode di header bagian template (`21_fixx_nb.txt:414-416`) menyatakannya terbuka:

```python
# 3. TEMPLATE HEURISTIK LOKAL (fallback saluran teks - analog configs/text.yaml)
#    Teks disusun agar klasifikasi leksikon == ground truth (deterministik).
```

Dan `_core_text()` benar-benar débilkan ke `gt_sentimen` sebagai cabang (`:419-441`):

```python
def _core_text(c):
    if c["gt_sentimen"] == "Positif":
        return (f"Alhamdulillah layanan JKN di {faskes} sangat baik dan cepat. ... Terima kasih BPJS!")
    if c["gt_sentimen"] == "Netral":
        return (f"Hari ini kontrol rutin ke {faskes} untuk {dx}. "
                f"Pengobatan sesuai jadwal, tidak ada catatan khusus.")
    ...
```

Setiap label ground truth punya **keluaran template sendiri** yang memuat leksikon pemicu untuk label itu. Label "Positif" selalu mendapat frasa "sangat baik", "cepat", "lancar", "ramah"; label "Negatif" selalu mendapat "Kecewa!" atau "dirugikan"; label "Netral" mendapat "sesuai jadwal, tidak ada catatan khusus". Karena leksikon diuji terhadap teks yang dibuat untuknya, **kecocokan 100% pada jalur Twitter adalah konsekuensi definisi, bukan hasil pengukuran**.

Rincian per kanal (reproduksi `_fixx_repro.py`):

| Kanal | benar | akurasi | distribusi label |
|---|---|---|---|
| Twitter | 100/100 | **100,00%** | Positif 62, Negatif 24, Netral 14 (= identik GT) |
| Reddit | 86/100 | **86,00%** | Positif 62, Negatif 38, **Netral 0** |
| Gabungan | 186/200 | 93,00% | - |

**Dampak.** Angka 93,0% tidak mengukur kemampuan klasifikasi sama sekali. Yang diukur adalah seberapa konsisten leksikon dengan template yang ditulis untuknya. Klaim apa pun bertipe "akurasi sentimen 93% menunjukkan kanal teks bekerja" tidak dapat dibenarkan oleh artefak ini. Dan karena teks Reddit menambah prefiks konstan (lihat C-2), Twitter dan Reddit mengukur hal yang **berbeda**, sehingga menggabungkan keduanya ke satu angka 93,0% menutupi fakta bahwa Twitter = 100% dan Reddit = 86%.

**Rekomendasi.** Ganti 93,0% dengan dua angka terpisah per kanal, dan beri label "klasifikasi leksikon pada template sintetis (tautologi per desain, bukan evaluasi)". Evaluasi klasifikasi yang bermakna memerlukan teks yang **tidak** dibangun dari label - misalnya kalimat generik ber-netralitas terkontrol, atau data sosial nyata.

### C-4 - Klasifikasi Reddit tidak pernah menghasilkan "Netral": rdSent = [62, 0, 38]

**Bukti.** Payload yang dipublikasikan (`colab/payload-aegis-jkn.json` dan inline di `Aegis-JKN/public/dashboard-aegis-jkn.html:1071`) memuat:

```json
"gtSent": [62, 14, 24], "twSent": [62, 14, 24], "rdSent": [62, 0, 38]
```

`rdSent` adalah distribusi label Reddit dengan urutan (Positif, Netral, Negatif). Nilainya **tidak pernah menghasilkan Netral sama sekali**. Regresi `_fixx_repro.py` mengonfirmasi: label Reddit hanya punya dua nilai (`Counter({'Positif': 62, 'Negatif': 38})`), sedangkan ground truth punya tiga (`Positif 62, Negatif 24, Netral 14`).

Penyebabnya adalah bug substring C-2: 14 teks Reddit berlabel GT "Netral" semuanya mendapat skor -0,7616 dan melompat ke "Negatif", sehingga 24 + 14 = 38. Distribusi Reddit menjadi [62, 0, 38].

**Dampak visual pada artefak yang dipublikasikan.** Dashboard merender `D.rdSent` ke pie chart Reddit (`dashboard-aegis-jkn.html:143039`), sehingga PDF 16 halaman menampilkan pie Reddit dengan **slice "Netral" 0%** - kategori yang justru menjadi tempat seluruh 14 kegagalan berada, dan kategori yang justru hilang dari perbandingan visual antara Twitter (yang menunjukkan 14 Netral) dan Reddit. Pembaca yang membandingkan kedua pie akan menyimpulkan Reddit "tidak pernah netral", padahal 14 klaim memang berlabel netral. PDF adalah hasil `document.documentElement.cloneNode(true).outerHTML` dari DOM yang sama, jadi PDF dan HTML memuat angka yang identik.

**Rekomendasi.** Perbaiki bug substring (C-2) dan publikasikan ulang payload; sampai itu selesai, hapus chart Reddit atau beri anotasi bahwa kelas Netral tidak ter Klassifikasikan.

### C-5 - "100% deteksi fraud" dan "100% hit-rate sindikat" adalah label by construction

**Bukti.** Pada generator v1, skor fraud ditulis tangan dan label diturunkan dari ambang tetap (`21_fixx_nb.txt:253-332` dan `:335-343`):

```python
for i, (p, d, s) in enumerate([("P01","D01",0.93), ("P02","D01",0.94),
                               ("P03","D02",0.95)], start=1):
    mk(i, p, d, "RS_A", "K29.7", "00.66", 3, 58_000_000, 10, s, "SYND-01", ...)

def risk_label(skor):
    if skor < LOW_T: return "low"
    if skor < MED_T: return "medium"
    if skor <= HIGH_T: return "high"
    return "fraud"                      # <- fraud <=> skor > 0.80
```

Rentang skor per kelas (hasil reproduksi `_fixx_repro.py`):

| Label | n | skor min | skor max |
|---|---|---|---|
| low | 76 | 0,05 | 0,34 |
| medium | 4 | 0,41 | 0,55 |
| high | 6 | 0,62 | 0,79 |
| fraud | 14 | 0,84 | 0,95 |

Karena tidak ada kelas yang saling tumpang tindih, dan `p_fused = min(0.99, skor + 0.10·f_text·(1-skor))` monoton terhadap `skor`, maka:

- fraud menempati **peringkat 1-14** dari 100 (p_fused 0,856 ... 0,955);
- non-fraud tertinggi (KLM016) p_fused = 0,802 di peringkat 15;
- **AUC(p_fused vs label fraud) = 1,000** secara deterministik;
- antrean 20 klaim **pasti** memuat 14 fraud, sehingga det_rate = 100% dan hit-rate tiap sindikat = 100%.

Tidak ada model yang dilatih, tidak ada split, tidak ada file prediksi. Yang diukur adalah "apakah ambang 0,80 memisahkan dua kelompok yang memang dibuat terpisah".

**Dampak.** Ini akar dari ">20% lift AUPRC dibanding baseline" dan "100% mendeteksi 9 pola sindikat" yang diklaim `11-archive-proposal.md:30`. Angka itu terbukti benar secara aritmetika dan tanpa nilai informatif.

**Rekomendasi.** Hapus "100% deteksi" dan "100% hit-rate" dari materi presentasi, atau labeli eksplisit sebagai "konsistensi internal generator (label by construction, bukan performa model)".

### C-6 - Angka baseline proposal adalah konstanta hardcode, bukan hasil perbandingan model

**Bukti.** `mechine-learning-deep-learning/backend/src/oasis/simulation.py:294-325`:

```python
def compare_with_baseline(
    self,
    oasis_results: Dict[str, Any],
    baseline_auprc: float = 0.71
) -> Dict[str, Any]:
    """
    Compare OASIS simulation results with industry baseline models:
    - Rule-based: 0.58
    - Logistic Regression: 0.62
    - XGBoost: 0.71
    - GNN: 0.78
    - Hybrid GNN+XGB: 0.85
    - MHGSL: 0.91
    """
    ...
    "benchmarks": {
        "Rule-based": {"auprc": 0.58, "gap": round(oasis_detection_rate - 0.58, 2)},
        "Logistic Regression": {"auprc": 0.62, ...},
        "XGBoost": {"auprc": 0.71, ...},
        "GNN": {"auprc": 0.78, ...},
        "Hybrid GNN+XGB": {"auprc": 0.85, ...},
        "MHGSL": {"auprc": 0.91, ...}
    }
```

`backend/src/api/main.py:365-400` mengulang konstanta yang sama untuk radar chart (`radar_data`) dan `auprc_data`, termasuk `{"method": "MHGSL", "values": {"Precision": 0.92, "Recall": 0.90, "F1-Score": 0.91, "AUPRC": 0.91, "Specificity": 0.96}}`. **Tidak ada satupun nilai baseline yang dihitung dari data**; semuanya literal, dan `gap` hanyalah selisih aritmetika terhadap `oasis_detection_rate` yang juga berasal dari simulasi OASIS internal, bukan dari model yang dilatih pada dataset 300.

Konsekuensi: "baseline XGBoost 0,71" adalah konstanta, dan "+28,6% dibanding baseline XGBoost" = 0,9142/0,71 - 1 = 28,7606%, dibulatkan menjadi "+28,6%" di `dokumen/section_bab_7_to_9.py:94`. Klaim "membuktikan keunggulan mutlak arsitektur MHGSL" tidak memiliki dasar komputasi.

**Rekomendasi.** Ganti `benchmarks` dengan hasil evaluasi nyata per model pada split yang sama, atau hapus endpoint `/api/metrics` yang menyajikan perbandingan semu. Tambahkan `experiment_id` dan `split` ke setiap angka benchmark.

### C-7 - Metrik headline proposal tidak ada di kode ML, hanya di generator DOCX

**Bukti.** Pencarian seluruh repo `mechine-learning-deep-learning` (di luar `venv/` dan `site-packages`) terhadap pola `0.9825`, `0.9142`, `94.12`, `89.4`, `10.6` pada berkas `*.py`, `*.ipynb`, `*.yaml`, `*.json` menghasilkan **nol hit untuk kelima pola**. Yadanya satu-satunya pola yang cocok adalah `0.71`, dan semuanya literal:

```
./backend/src/oasis/simulation.py:297:        baseline_auprc: float = 0.71
./backend/src/oasis/simulation.py:303:        - XGBoost: 0.71
./backend/src/oasis/simulation.py:320:                "XGBoost": {"auprc": 0.71, "gap": round(oasis_detection_rate - 0.71, 2)},
./backend/src/api/main.py:374:                "values": {"Precision": 0.74, "Recall": 0.68, "F1-Score": 0.71, "AUPRC": 0.71, "Specificity": 0.89}
./backend/src/api/main.py:395:            {"method": "XGBoost", "auprc": 0.71},
./notebooks/03_oasis_simulation.ipynb:109:    "comparison = simulation.compare_with_baseline(all_results, baseline_auprc=0.71)\n",
```

Perhatikan `notebooks/03_oasis_simulation.ipynb:109`: argumen `baseline_auprc=0.71` ditulis **literal di dalam sel notebook** - bukan hasil evaluasi model pada data. Satu-satunya jalur yang "memakai" angka 0,71 adalah pathway yang mengirimnya sebagai konstanta.

Di luar repo ML, angka-angka itu hanya hidup di:

| Berkas | Peran |
|---|---|
| `dokumen/section_bab_7_to_9.py:80-97` | generator tabel metrik dan paragraf "+28,6%" |
| `dokumen/section_cover_preface.py:117,165` | generator ringkasan eksekutif proposal |
| `dokumen/section_bab_1_to_3.py:132` | tabel "Ketahanan Kamuflase" |
| `analysis/corpus/11-archive-proposal.md:30,326-330,347-348` | arsip Notion proposal |
| `analysis/corpus/14-index.md` | indeks arsip |
| `analysis/reports/scripts/_targets.py`, `_prec.py`, `_metriccompat.py`, `16_redteam.py` | skrip audit (angka target, bukan sumber) |

**Tidak ada** di `backend/src/`, **tidak ada** di notebook pelatihan, **tidak ada** di `backend/data/oasis_results.json`. Artinya metrik headline proposal adalah konstanta yang ditulis tangan di generator proposal, tanpa artefak komputasi yang menghasilkannya.

**Verifikasi tambahan - 94,12% tidak dapat dicapai di data mana pun.** Pemindaian exhaustif atas seluruh nilai unik `skor_fraud` pada dataset 300 (`_prec.py`) menghasilkan **0 ambang** dengan presisi tepat 94,12% (tp/(tp+fp) = 0,9412 tidak pernah terpenuhi untuk tp+fp ≤ 119). Presisi terdekat yang bisa dicapai:

| ambang | TP | FP | presisi | FPR |
|---|---|---|---|---|
| 0,78 | 36 | 2 | 94,7368% | 0,76% |
| 0,74 | 36 | 3 | 92,3077% | 1,14% |
| 0,79 | 36 | 1 | 97,2973% | 0,38% |
| **0,80** | **36** | **0** | **100,0000%** | **0,00%** |
| 0,14 | 36 | 28 | 56,2500% | 10,61% |

Konsekuensi praktis: pada data yang sama, `skor_fraud` **telah memberi** presisi 100% dan FPR 0% secara gratis di ambang 0,80. Klaim presisi 94,12% justru **lebih rendah** dari apa yang data tersebut memberi tanpa model apa pun, dan tidak dapat dicapai pada ambang mana pun.

### C-8 - Tabel entitas `10-simulation-dataset.md` tidak cocok dengan data mana pun

**Bukti.** `_docparse.py` mem-parsing tabel markdown dokumen lalu membandingkannya dengan generator v1 (100 klaim, sumber PDF) dan dataset 300 aktual. Ringkasan:

| Tabel | jumlah klaim tidak cocok vs v1 | vs v2 (300) | skor maks tidak cocok vs v1 | vs v2 |
|---|---|---|---|---|
| Faskes (6) | **6/6** | 6/6 | 0/6 | 0/6 |
| Dokter (12) | **9/12** | 12/12 | - | - |
| Pasien (20) | 8/20 | **20/20** | **9/20** | 0/20 |
| Diagnosis (10) | **10/10** | 10/10 | **3/10** | 5/10 |
| Prosedur (10) | 6/10 | 6/10 | - | - |

Contoh baris yang paling jelas:

```
RS_A   n_doc=19  n_v1=17  n_v2=29
K40.9  n_doc= 8  n_v1=77  n_v2=29  skor_doc=0.13  v1=0.41  v2=0.64
I21.9  n_doc= 8  n_v1= 1  n_v2=20  skor_doc=0.13  v1=0.62  v2=0.84
D06    n_doc= 0  n_v1= 6  n_v2= 2
```

Dua prosedur di dokumen **tidak ada di generator mana pun**: `36.13 Coronary artery bypass graft (CABG)` (tarif Rp78.000.000) dan `93.90 Terapi oksigen tekanan positif` (Rp640.000). Keduanya bercount 0 di v1 maupun v2. Sebaliknya `53.1` memiliki 77 klaim di v1 (dokumen menyebut 8).

Frasa penutup dokumen "Biaya Rujukan" juga tidak cocok dengan nominal dataset 300 (blok TARIF di `_docparse.py`): tarif `81.52` = Rp46.500.000 sedangkan nominal dataset 300 rentangnya Rp41.850.000 - Rp49.300.000, dengan 7 dari 18 baris di atas tarif. Untuk `96.04` semua 3 baris di atas tarif (Rp2.100.000 vs tarif Rp750.000). Untuk `74.1` baris tunggal tepat sama dengan tarif.

**Dampak.** `10-simulation-dataset.md` adalah acuan spesifikasi yang dipakai `08-training-protocol.md`, `13-text-channel.md`, dan `03-dataset-registry.md`. Tabel entitas yang tidak dapat direproduksi membuat spesifikasi turunan ikut tidak dapat diuji. Temuan ini **belum** tercatat di `07-generator.md` (yang hanya membandingkan baris data, bukan tabel entitas).

**Rekomendasi.** Tambahkan skrip `tests/test_entity_tables.py` yang menghitung ulang jumlah klaim dan skor maksimum per faskes/dokter/pasien/diagnosis/prosedur dari CSV dan membandingkannya dengan `10-simulation-dataset.md`. Until then, beri banner "TIDAK TEREKONSILIASI - belum dapat direproduksi dari artefak mana pun".

---

## 5. Temuan HIGH

### H-1 - Kanal fitur MHGSL nyaris tidak informatif (kepadatan edge 92,18%)

`feat_edges = 4563` dari 4.950 pasangan yang mungkin (**92,18%**). Penyebabnya: 76 klaim normal dibangun dari template identik (`K40.9`, `53.1`, LOS 2-4, Rp5-11 jt, qty 2-5), sehingga vektor fitur `[los, log10(biaya), qty]` mereka saling identik dan pairwise cosine = 1,000.

Konsekuensi: `synd_density` = 1,00 untuk kelima sindikat hanya karena density global 0,92 (reproduksi `_entity2.py`: SYND-01 inner 3/3, SYND-02 3/3, SYND-03 15/15, SYND-04 1/1, SYND-05 1/1, semuanya 1,00 terhadap global 0,92). Angka itu tidak membedakan sindikat dari noise. Dimensi channel topologi (`deg/5`) juga jenuh: hampir semua klaim punya degree ≥ 5, sehingga `topo` = 1,00 di mana-mana.

### H-2 - Kriteria sindikat hanya lolos pada `QUEUE_RATE` ≥ 0,15

Sensitivitas (`_fragile.py`, bagian 2):

| queue | det_rate | SYND-01 | SYND-02 | SYND-03 | SYND-04 | SYND-05 | semua > 0 |
|---|---|---|---|---|---|---|---|
| 10 | 71,4% | 1,00 | 1,00 | 0,50 | 0,50 | 0,00 | ❌ |
| 12 | 85,7% | 1,00 | 1,00 | 0,67 | 1,00 | 0,00 | ❌ |
| 13 | 92,9% | 1,00 | 1,00 | 0,83 | 1,00 | 0,00 | ❌ |
| 14 | 100% | 1,00 | 1,00 | 1,00 | 1,00 | 0,00 | ❌ |
| **15** | 100% | 1,00 | 1,00 | 1,00 | 1,00 | 0,50 | ✅ |
| **20** | 100% | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | ✅ |

Argumen "sistem menemukan semua 5 sindikat" hanya berlaku pada queue ≥ 15. Dengan `QUEUE_RATE = 0.20` parameter tersebut berada **tepat 5 klaim di atas batas bawah kelayakan**. Mengubahnya menjadi 0,14 (pilihan lain yang wajar, dan masih memenuhi det_rate 100%) **menggagalkan** kriteria sindikat. SYND-05 (Cloning) menempati peringkat 15 dan 16 - satu slot di bawah batas antrean 20% bila queue = 14.

### H-3 - Angka 93,0% bergantung pada Ollama yang bisa hidup atau mati

`TOTAL_STEPS = 300` dengan `LLM_EVERY = 100` → cabang LLM hanya menyala pada langkah 1, 100, 200, 300, yaitu **4 panggilan** untuk 100 klaim. `llm_ptr` naik 4 kali, sehingga hanya 4 klaim yang bisa menerima teks LLM; **96 klaim selalu memakai template heuristik lokal**. Output notebook: "4 sampel LLM (mistral-oasis:24b) + fallback heuristik lokal; 24 log Twitter & 24 log Reddit dikompilasi."

Konsekuensi: bila Ollama hidup, 4 klaim mendapat teks bebas bentuk yang label sentimennya bisa berubah, sehingga 93,0% tidak harus sama. PDF yang dipublikasikan mencatat `model = mistral-oasis:24b`, jadi run yang terbit itu memakai teks LLM untuk 4 klaim (4/200 = 2% dari denominator).

Artinya angka utama dashboard berayun hanya berdasarkan apakah ada LLM lokal, dan tidak ada artefak yang menyimpan teks LLM yang dipakai, prompt, seed, atau versi model persis. Tidak ada yang bisa mereproduksi run yang dipublikasikan secara bit-exact. Sel 4 notebook juga mencatat `HTTPConnectionError: Read timed out. (read timeout=120)` saat menguji koneksi Ollama - jadi run yang terbit mungkin sebagian besar jatuh ke fallback.

Catatan tambahan: komentar kode masih berbunyi "tiap klaim diproses 10x (1000/100)" (`21_fixx_nb.txt:536`) padahal `TOTAL_STEPS = 300`, sehingga tiap klaim hanya dikunjungi 3x. Asumsi 1000 langkah di komentar sudah kedaluwarsa.

### H-4 - Nama berkas PDF menyesatkan: "300 dataset" sebenarnya 100 klaim

Nama berkas `Hasil simulasi dari 300 dataset notion.pdf` merujuk pada 300 **langkah simulasi**, bukan 300 klaim. Dashboard memakai 100 klaim v1. `10-simulation-dataset.md:4` sendiri sudah memberi catatan versi ("Halaman ini mendokumentasikan dataset sintetis 100 klaim sebagai versi demo awal. Dataset aktif saat ini adalah database Klaim Aegis-JKN v2 dengan 300 baris"), tetapi nama berkas tidak pernah diperbaiki dan sekarang dipakai sebagai bukti dataset aktif. Risiko: pembaca mengira ada bukti eksekusi atas 300 baris.

### H-5 - FPR 10,6% dan presisi 94,12% tidak dapat berasal dari ambang yang sama

Klaim FPR 10,6% **dapat** direproduksi: ambang `skor_fraud ≥ 0,14` pada dataset 300 menghasilkan tepat FP = 28 dari 264 negatif, yaitu FPR = 10,6061% yang dibulatkan 10,6%. Yang benar adalah sebagai berikut:

- FPR 10,6% **reachable**, tetapi hanya pada ambang 0,14, yang memberi presisi 56,25% - bukan 94,12%.
- Presisi 94,12% **tidak reachable** pada ambang mana pun (bagian C-5).
- Satu-satunya ambang dengan presisi 100% adalah 0,80, dan pada ambang itu FPR = 0%.

Artinya ketiga klaim proposal **tidak saling kompatibel** pada satu operating point mana pun, dan angka FPR yang "terlihat reasonable" justru berasal dari ambang dengan prediksi buruk. Klaim FPR 10,6% juga mengasumsikan populasi negatif 264 (seluruh non-fraud), bukan 60 anomali non-escalate yang disebut proposal di tempat lain.

---

## 6. Temuan MEDIUM

### M-1 - `synd_density` 1,00 bukan bukti kepadatan sindikat

Lihat H-1. Angka ini sebaiknya dihapus atau diganti dengan **lift** terhadap density global (1,00 / 0,92 = 1,08), yang jujur menyatakan hampir tidak ada lift.

### M-2 - Himpunan fraud adalah ambang skor 0,80 yang terpilih agar pas

Sensitivitas ambang pada antrean top-20 (`_fragile.py`, bagian 4): ambang > 0,70 → 17 klaim tertangkap; > 0,75 → 16; > 0,80 → 14; > 0,85 → 11. Semuanya 100% karena antrean 20 cukup besar untuk menampung semuanya dan tidak ada kelas yang tumpang tindih. Untuk menguji kemampuan model, ambang harus berasal dari nilai skor pada data yang belum pernah dilihat.

### M-3 - 4 dari 100 klaim bisa terkena teks LLM, sehingga 93,0% environment-dependent

Lihat H-3.

### M-4 - Komentar kode "1000 langkah" sudah kedaluwarsa

`TOTAL_STEPS = 300`; komentar menyatakan "tiap klaim diproses 10x (1000/100)". Konsisten dengan H-3.

---

## 7. Temuan LOW

### L-1 - Flag kontradiksi tidak berkorelasi dengan peringkat antrean

Antrean 20 memuat 7 klaim `kontradiksi = True`: KLM001-006 dan KLM018. Enam di antaranya adalah peringkat 1-6, sedangkan KLM018 (Prolonged Stay) berada di peringkat 17. Jadi flag kontradiksi **tidak berkorelasi** dengan peringkat antrean: klaim yang paling kontradiktif secara narasi belum tentu yang paling ganjil secara fusion. Konsisten dengan C-5 (peringkat ditentukan `skor` yang ditulis tangan, bukan bukti narasi).

### L-2 - "p_lead > 0.85" tidak ada di sumber

Baris HTML sumber (`21_fixx_nb.txt:877`): `p_fused = p_graph + γ·f_text·(1 − p_graph) · γ = 0.10 · θ_feat = 0.85`. Rerenderan bitmap 90° menukar glyph **θ_feat** menjadi **p_lead**. Pencarian `p_lead` di seluruh workspace: nol hit di luar skrip audit ini.

### L-3 - Jumlah halaman PDF adalah 16, bukan 17

`17-roadmap.md:382` menulis "3.800.507 B, 17 hlm, IMAGE-ONLY" dan `:490` menulis "(3.800.507 B, 17 halaman)". `_pdfmeta.py` membaca `/Count 16` dari pohon halaman: **PDF ini 16 halaman**. Selisih ini kecil, tapi menunjukkan bahwa baris roadmap itu ditulis dari perkiraan, bukan dari pembacaan metadata.

---

## 8. Rekonsiliasi Angka Finansial

| Pernyataan | Sumber | Nilai reproduksi | Status |
|---|---|---|---|
| Total nominal 300 klaim | `00-dashboard.md` §3 | Rp3.526.650.000 | ✅ cocok |
| Nominal 36 fraud / 24 review / 240 auto_clear | idem | Rp561.150.000 / Rp279.950.000 / Rp2.685.550.000 | ✅ cocok |
| Nominal 60 klaim non-auto_clear | idem | Rp841.100.000 | ✅ |
| Rata-rata skor per status: auto_clear 0,086 / review 0,591 / escalate 0,869 | `dokumen/section_bab_7_to_9.py:94` | 0,0862 / 0,5908 / 0,8689 | ✅ cocok |
| Estimasi overcharge Rp507.370.000 | `11-archive-proposal.md:347` | **tidak dapat direproduksi** | ❌ |
| "rata-rata Rp8,46 juta per kasus fraud" | `11-archive-proposal.md:30` | target ÷ 60 = Rp8.456.167; **target ÷ 36 = Rp14.093.611** | ❌ penyebut keliru |
| 60 klaim anomali | `11-archive-proposal.md:30` | dataset punya 60 non-auto_clear, tetapi 36 yang `is_fraud = 1` | ⚠️ ambigu |
| "SYND-01..09 menguasai 36 klaim (60% dari kasus fraud) senilai Rp542,56 Juta" | `11-archive-proposal.md:348` | sindikat mencakup **36 klaim** tetapi hanya **34** yang `is_fraud = 1` (2 klaim fraud tunggal tanpa sindikat); nominal sindikat = **Rp539.650.000** | ❌ jumlah dan nominal salah |
| "Upcoding Rp127,68 Juta" | `11-archive-proposal.md:348` | upcoding = **Rp156.900.000** (Rp156,90 Juta) | ❌ |
| "Phantom Billing Rp134,25 Juta" | idem | Rp134.250.000 | ✅ cocok |
| "Repeat Billing Rp61,60 Juta" | idem | Rp61.600.000 | ✅ cocok |

Rp507.370.000 = 60,3222% × Rp841.100.000. Tidak ada tarif acuan, tidak ada formula, tidak ada ledger per klaim yang menghasilkannya. Bandingkan dengan tarif acuan `10-simulation-dataset.md`: untuk `96.04` (tarif Rp750.000) seluruh 3 baris dataset berada **di atas** tarif, `81.52` 7 dari 18 baris di atas tarif. Artinya overcharge riil yang dapat dihitung dari tarif yang tersedia tidak mendekati 60% dari nominal. Lihat juga `04-evidence-matrix.md` E-11 dan `16-red-team.md` #4.

**Angka proposal yang justru COCOK dan harus diberi kredit:** rata-rata skor per status (0,086 / 0,591 / 0,869) reproduksi persis dari dataset 300 - mean 0,0862 / 0,5908 / 0,8689 pada kedua salinan data (`claims_300_v2.1.csv` dan `claims_v2_live.csv`). Ini satu-satunya metrik proposal dalam laporan ini yang punya artefak komputasi nyata.

---

## 9. Angka "Rp507.370.000" dan 60 Klaim: Rekonsiliasi terhadap Tarif

Tabel tarif acuan pada `10-simulation-dataset.md` (mis. `81.52` = Rp46.500.000) **tidak cocok** dengan nominal klaim pada dataset 300 (`81.52` = Rp44.750.000, yaitu **di bawah** tarif). Audit paralel `16-red-team.md` #4 sudah menghitung total overcharge dari tarif resmi = **Rp31.350.000**, yaitu 6,2% dari klaim Rp507.370.000. Laporan ini mengonfirmasi: nilai dataset 300 yang dipakai adalah `claims_300_v2.1.csv` (SHA-256 `37cf2236...fd4e8`, byte-identik dengan payload base64 yang tertanam di `notebooks/Aegis-JKN.ipynb`), sehingga kedua audit menghitung atas data yang sama.

---

## 10. Rekomendasi Konsolidasi

| Prioritas | Tindakan | Sumber |
|---|---|---|
| **P0** | Tambahkan kalimat di `00-dashboard.md` §4 bahwa 93,0% adalah akurasi **sentimen**, bukan fraud | C-1 |
| **P0** | Perbaiki bug substring leksikon ("lama" vs "Pengalaman"), jalankan ulang, publikasikan angka baru + skrip | C-2 |
| **P0** | Pecah 93,0% jadi dua angka per kanal (Twitter 100%, Reddit 86%) dan beri label "tautologi per desain" | C-3 |
| **P0** | Perbaiki payload/dashboard agar `rdSent` kembali 3 kelas, atau hapus pie chart Reddit | C-4 |
| **P0** | Hapus "100% deteksi fraud" / "100% hit-rate sindikat" dari materi presentasi, atau labeli "label by construction" | C-5 |
| **P0** | Ganti `benchmarks` hardcode di `backend/src/oasis/simulation.py` dan `api/main.py` dengan hasil evaluasi nyata, atau hapus endpoint `/api/metrics` | C-6 |
| **P0** | Hapus label "(Tervalidasi)" dari metrik yang tidak punya artefak komputasi di `dokumen/section_bab_7_to_9.py` | C-7 |
| **P0** | Tandai `10-simulation-dataset.md` dengan banner "tabel entitas tidak terekonsiliasi" dan tambahkan `tests/test_entity_tables.py` | C-8 |
| **P1** | Hapus 93,0% dari KPI dashboard (`src/data/oasis-data.ts`, `public/dashboard-aegis-jkn.html`) atau ganti labelnya | C-2, H-3 |
| **P1** | Hapus `synd_density` 1,00; ganti dengan lift terhadap density global (1,08) | M-1, H-1 |
| **P1** | Simpan artefak run: teks LLM yang dipakai, prompt, seed, versi model, hash; jika tidak, nyatakan "reproduksi parsial" | H-3 |
| **P1** | Koreksi nama berkas PDF agar menyebut 100 klaim, atau tambahkan README di folder `colab/` | H-4 |
| **P1** | Koreksi "Rp8,46 juta per kasus fraud" menjadi hitung terhadap 36 (Rp14.093.611) | §8 |
| **P1** | Koreksi angka sindikat/modus di `11-archive-proposal.md:348` (34 klaim sindikat, Rp539.650.000, upcoding Rp156,90 Juta) | §8 |
| **P2** | Tambahkan uji sensitivitas `QUEUE_RATE` ke skrip validasi, agar kriteria sindikat tidak rapuh | H-2 |
| **P2** | Perbarui `17-roadmap.md:382,490` - PDF sudah dibaca dan direproduksi (16 hlm, bukan 17), bukan "tidak dapat diekstraksi" (tutup G-31) | laporan ini |
| **P2** | Sinkronkan angka sindikat/modus proposal dengan data (`dokumen/section_bab_7_to_9.py`) | §8 |

---

## 11. Lampiran: Cara Menjalankan

```bash
cd N:/HEALTHKATHON/analysis/reports/scripts
python -I _fixx_repro.py     # rekonstruksi 100 klaim v1 + semua metrik dashboard
python -I _docparse.py        # parse tabel entitas 10-simulation-dataset.md vs v1 vs 300 + tarif
python -I _entity.py          # tabel entitas 10-simulation-dataset.md vs generator v1
python -I _entity2.py         # tabel entitas vs dataset 300 + density edge + root cause bug
python -I _fragile.py         # 14 kegagalan sentimen + sensitivitas QUEUE_RATE + ambang fraud
python -I _env.py             # coupling LLM + kontradiksi + distribusi sentimen
python -I _propcheck.py       # rekonsiliasi nominal & status vs klaim proposal
python -I _syncheck.py        # rekonsiliasi per-sindikat & per-modus vs klaim proposal
python -I _means.py           # rata-rata skor per status (0,086 / 0,591 / 0,869)
python -I _prec.py            # kurva presisi atas SEMUA ambang (bukti 94,12% unreachable)
python -I _degen.py           # separasi label skor + threshold sweep
python -I _metriccompat.py    # kompatibilitas metrik proposal & aritmetika +28,6%
python -I _pdfmeta.py         # metadata PDF: judul, producer, jumlah halaman
```

Semua skrip memakai pustaka standar saja (tanpa pandas/numpy/sklearn) dan dapat dijalankan di laptop tanpa GPU, tanpa Ollama, dan tanpa akses jaringan.

**Ekstraksi dataset 300 dari notebook** (payload base64 gzip tertanam di `notebooks/Aegis-JKN.ipynb`):

```
sha256(claims_300_v2.1.csv di datasets/) = 37cf22369ebf7a3c616219cb49b9c4406f00d75286b38cbf6c08b844e27fd4e8
sha256(payload base64 di notebook)      = 37cf22369ebf7a3c616219cb49b9c4406f00d75286b38cbf6c08b844e27fd4e8
=> byte-identik
```

CSV turunan yang dipakai skrip ini (`analysis/reports/work22/claims_300_nb.csv`) berisi 31 kolom dan identik dengan `claims_300_v2.1.csv`; `analysis/corpus/claims_v2_live.csv` menghasilkan angka identik untuk seluruh metrik di laporan ini (keduanya sha256 berbeda, isi metrik sama).

---

## 12. Referensi Baris

| Sumber | Baris | Isi |
|---|---|---|
| `colab/Aegis_JKN_FIXX.ipynb` sel 5 | 195-196 | `HONESTY_LABEL` "prevalensi oversampled (14%)" |
| " | 253-332 | `build_ground_truth()` - skor fraud ditulis tangan |
| " | 335-343 | `risk_label()` - fraud ⇔ skor > 0,80 |
| " | 353-357 | assert 100 klaim / 62-14-24 / 76-4-6-14 / 8 kontradiksi |
| " | 364-370 | leksikon POS/NEG, `FRAUD_PHRASES` |
| " | 385-404 | `analyze_sentiment()` - `if wd in low` (bug substring) |
| " | 414-416 | komentar "Teks disusun agar klasifikasi leksikon == ground truth" |
| " | 418-455 | `_core_text()` - cabang template per `gt_sentimen` (tautologi) |
| " | 459-468 | `reddit_template()` - judul konstan berisi "Pengalaman" |
| " | 536 | komentar "tiap klaim diproses 10x (1000/100)" (kedaluwarsa) |
| " | 616-621 | loop `feat_edges` (cosine ≥ 0,85) |
| " | 636-649 | `channel_contrib()` |
| " | 653-662 | late fusion `p_fused` |
| " | 664-667 | `accuracy = match / (2*len(CLAIMS))` - **akurasi sentimen** |
| " | 703-710 | `sent_dist()` -> `twSent`, `rdSent` |
| " | 670-695 | queue, det_rate, synd_hit, criteria "SESUAI" |
| " | 697-700 | `CAPACITY_GAIN = 20/3`, `VERIFICATOR_CAPACITY = 6667` |
| " | 843-845 | label KPI "Akurasi Sentimen Simulasi" |
| " | 877 | baris `θ_feat = 0.85` (bukan "p_lead") |
| `backend/src/oasis/simulation.py` | 294-325 | `compare_with_baseline` + `benchmarks` hardcode |
| `backend/src/api/main.py` | 365-400 | `radar_data` / `auprc_data` konstanta hardcode |
| `dokumen/section_bab_7_to_9.py` | 80-97 | tabel metrik proposal + paragraf "+28,6%" |
| `dokumen/section_cover_preface.py` | 117, 165 | ringkasan eksekutif proposal |
| `dokumen/section_bab_1_to_3.py` | 132 | tabel "Ketahanan Kamuflase" |
| `corpus/00-dashboard.md` | 47-48 | daftar metrik "belum boleh disebut hasil tervalidasi" |
| `corpus/10-simulation-dataset.md` | 20-99 | tabel Faskes / Dokter / Pasien / Diagnosis / Prosedur |
| `corpus/04-evidence-matrix.md` | 34-37 | E-07 s.d. E-11 |
| `corpus/11-archive-proposal.md` | 30, 326-330, 347-348 | klaim "Tervalidasi" + Rp507.370.000 + angka modus |
| `reports/17-roadmap.md` | 382, 490 | PDF dicatat sebagai "belum dibaca" (G-31) |
