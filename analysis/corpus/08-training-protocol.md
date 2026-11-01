<!-- source: notion page 4003e603-1ab7-8197-8715-f1de059e82ef -->

Dokumen ini mengatur prosedur pelatihan, validasi, dan dokumentasi model secara reproduktif. Tujuannya membantu tim membuat prototipe analitik yang dapat diaudit, bukan menghasilkan vonis fraud otomatis.
Sumber Notion: [Klaim Aegis-JKN v2, 300 baris](https://app.notion.com/p/c783afb3d0d4458295456180b7b7756b), [Dataset Registry DM Kontekstual](https://app.notion.com/p/07-Dataset-Registry-dan-Kamus-Data-DM-Kontekstual-4003e6031ab78179bcc7ca76a0b80fbc), dan [Arsitektur serta metodologi teknis](https://app.notion.com/p/02-Aegis-JKN-Arsitektur-Sistem-dan-Metodologi-Teknis-4003e6031ab781efbcdac7b0dbdd0cad).
> **{'type': 'emoji', 'emoji': '💡'}** Keputusan inti: dataset klaim sintetis dan dataset DM kontekstual adalah dua sumber berbeda. Jangan menggabungkannya hanya karena sama-sama berkaitan dengan JKN. Belum ada kunci relasi lintas sumber dan belum ada label fraud pada file DM.
1. Inventaris sumber dan kesiapan
| Sumber | Skala teramati | Label target | Peran yang disarankan | Batas utama |
| Klaim Aegis-JKN v2, database Notion aktif | 300 baris, KLM001 sampai KLM300 | Field Risiko dan Status tersedia, tetapi perlu audit asal label | Baseline prototipe setelah ground truth independen disahkan | Deskripsi database masih menyebut 100 klaim dan KLM001 sampai KLM024. |
| DM_kepesertaan.dta | 143.496 baris, 18 variabel | Tidak ada label fraud | Profil kepesertaan yang diizinkan | Memuat nomor peserta, tanggal lahir, lokasi, dan atribut sensitif. |
| DM20152020_fkrtldxsekunder.dta | 6.362.523 baris, 4 variabel | Tidak ada label fraud | Analisis distribusi kode diagnosis setelah audit kamus | Hanya FKL02 dan kode diagnosis. Tidak ada tanggal, biaya, atau nomor peserta. |
| DM20152020_fktpnonkapitasi.dta | 8.020 baris, 21 variabel | Tidak ada label fraud | QA data layanan dan eksplorasi anomali non-supervised | Biaya tagih dan biaya verifikasi identik pada semua baris. |
| Workbook ICD-10 dan Metadata | 4 kamus ICD-10, 979 label kategori | Bukan label outcome | Validasi kode dan decoding kategori | Kode 999 tanpa deskripsi ditemukan dalam 3 kamus. |
1. Tentukan tugas sebelum memilih model
| Tugas | Dataset | Target yang sah | Status saat ini | Hasil yang boleh dilaporkan |
| Klasifikasi fraud supervised | Klaim Aegis-JKN sintetis | ground_truth_fraud yang diperiksa manusia dan memiliki provenance | Belum disahkan | Metrik hanya setelah label dan leakage audit. |
| Pemeringkatan anomali | Data DM kontekstual | Tidak memerlukan label, tetapi tidak sama dengan ground truth fraud | Bisa dirancang, belum dilatih | Daftar observasi untuk ditinjau, bukan vonis fraud. |
| Prediksi selisih biaya verifikasi | FKTP nonkapitasi | PNK17 - PNK18 | Tidak layak pada ekstrak saat ini | Selisih 0 pada semua 8.020 baris. |
| Pemeriksaan konsistensi ICD-10 | Kamus ICD-10 dan kode diagnosis | Kecocokan kode dan deskripsi referensi | Layak sebagai QA setelah sentinel 999 diperiksa | Metrik kecocokan kode, bukan metrik fraud. |
1. Label dan pencegahan kebocoran
Database klaim aktif memuat 300 baris, tetapi deskripsinya masih menyebut versi 100 baris dan ground truth KLM001 sampai KLM024. Sebelum model dibuat, selaraskan deskripsi, jumlah record, versi dataset, definisi label, dan provenance setiap label. Jangan menyamakan field Risiko atau Status dengan label fraud yang telah diverifikasi, kecuali proses pembentukannya diaudit.
Buat kolom adjudikasi terpisah, minimal: ground_truth_fraud, evidence_source, reviewer_1, reviewer_2, adjudication_date, label_confidence, dan exclusion_reason. Kasus yang belum pasti harus berstatus unresolved, bukan dipaksa masuk kelas positif atau negatif.
Untuk eksperimen supervisi, keluarkan Skor Fraud, Risiko, Status, Sinyal SHAP, serta kolom yang dihitung langsung dari aturan label dari fitur awal. Jika label dibentuk dari skor, memasukkan skor tersebut membuat evaluasi sirkular dan tidak membuktikan kemampuan deteksi independen.
1. Kandidat fitur dan perlindungan privasi
| Sumber | Dapat dipertimbangkan setelah validasi | Dikecualikan dari fitur awal | Alasan |
| Klaim sintetis Aegis-JKN | Biaya, LOS, kategori layanan, diagnosis atau prosedur, rujukan, fitur narasi yang tidak dibentuk dari label | Skor Fraud, Risiko, Status, Sinyal SHAP, label turunan, dan kolom yang dihitung langsung dari aturan label | Mencegah model meniru target dan menghindari data leakage. |
| Data DM kontekstual | Frekuensi penggunaan agregat, kode diagnosis, interval kunjungan setelah validasi, kategori layanan dan tindakan | Nomor peserta, nomor keluarga, ID kunjungan mentah, tanggal lahir, lokasi sangat rinci, dan pengidentifikasi langsung | Mengurangi risiko memorisasi individu dan kebocoran identitas. |
| Diagnosis sekunder FKRTL | Frekuensi atau kombinasi kode setelah validasi FKL02 dan ICD-10 | Asumsi mengenai urutan diagnosis atau label fraud yang tidak ada pada file | Tidak ada tanggal, biaya, nomor peserta, atau outcome pada file ini. |
1. Tahapan training dan gerbang penerimaan
| Tahap | Aktivitas | Kriteria lulus | Artefak wajib |
| 0. Bekukan sumber | Catat file, versi, jumlah baris, hash SHA-256, waktu ekstraksi, dan izin penggunaan | Inventaris sumber stabil dan dapat diaudit | manifest.json |
| 1. Audit label | Audit definisi kasus positif, alasan, bukti, reviewer, dan adjudikasi | Label sintetis atau skor aturan tidak diperlakukan sebagai ground truth independen | label_audit.csv |
| 2. Siapkan fitur | Hapus identitas langsung, validasi tanggal, mapping kode, missingness, grain, dan leakage | Tidak ada identifier atau fitur pasca-keputusan yang bocor | data_quality_report.md |
| 3. Baseline | Bandingkan aturan sederhana, logistic regression, dan model pohon yang interpretable | Baseline, split, seed, dan metrik dapat diulang | train.py, metrics.json |
| 4. Evaluasi | Ukur PR-AUC, precision, recall, F1, confusion matrix, FPR, calibration, serta error analysis | Threshold ditetapkan berdasarkan kapasitas review dan validasi independen | evaluation_report.md |
| 5. Human review | Petugas memeriksa temuan; simpan alasan, keputusan, dan jejak perubahan | Tidak ada penolakan klaim otomatis berdasarkan skor model | review_log.csv |
1. Split data dan metrik evaluasi
Untuk dataset sintetis 300 baris, gunakan cross-validation berulang atau stratified cross-validation setelah label diaudit. Jika kasus berasal dari pola atau grup yang sama, split pada tingkat grup agar contoh terkait tidak tersebar antara training dan test. Sisihkan test set final dan jangan mengubah threshold berdasarkan hasil test.
Laporkan sekurangnya: PR-AUC, precision, recall, F1, confusion matrix, false positive rate, calibration, serta interval ketidakpastian bila memungkinkan. Tetapkan threshold sesuai kapasitas pemeriksaan manual dan biaya false positive. Jangan memakai Accuracy saja ketika kelas tidak seimbang.
Untuk data DM tanpa label, laporkan statistik deskriptif, konsistensi kode, atau anomali ranking. Jangan menyebut precision, recall, atau AUPRC fraud untuk eksperimen tanpa ground truth fraud independen.
1. Preprocessing khusus file DM
Pertahankan kode ICD-10 sebagai teks dan normalkan huruf besar tanpa menghilangkan nol atau karakter kode. Cocokkan terhadap kamus sebelum membangun fitur. Tandai kode 999 tanpa deskripsi sebagai sentinel yang menunggu klarifikasi, bukan kategori klinis valid.
Validasi periode: nama file menunjukkan 2015-2020, tetapi kolom PNK03 dan PNK04 memuat tanggal paling awal 2014-08-16. Catat temuan ini sebelum membatasi data menurut periode.
Validasi unit observasi pada PNK02 karena terdapat 4.939 ID kunjungan unik pada 8.020 baris. Pastikan apakah satu kunjungan boleh memiliki beberapa baris tindakan atau diagnosis. Jangan otomatis menghapus pengulangan.
PNK17 dan PNK18 identik pada 8.020 baris. Jangan menyatakan model memprediksi koreksi biaya dari kolom ini sampai tersedia sampel dengan variasi biaya yang sah atau target lain yang tervalidasi.
1. Template pemeriksaan data dengan Python
```python
from pathlib import Path
import pandas as pd

BASE = Path("data")
member_path = BASE / "DM_kepesertaan.dta"
noncap_path = BASE / "DM20152020_fktpnonkapitasi.dta"
secondary_path = BASE / "DM20152020_fkrtldxsekunder.dta"

# Dataset lebih kecil, periksa bentuk dan kolom.
member = pd.read_stata(member_path, convert_categoricals=False)
noncap = pd.read_stata(noncap_path, convert_categoricals=False)
assert len(member) == 143_496 and len(member.columns) == 18
assert len(noncap) == 8_020 and len(noncap.columns) == 21
assert (noncap["PNK17"] == noncap["PNK18"]).all()

# File diagnosis besar, proses per chunk agar hemat memori.
reader = pd.read_stata(
    secondary_path,
    iterator=True,
    chunksize=250_000,
    convert_categoricals=False,
    convert_dates=False,
)
rows_seen = 0
for chunk in reader:
    rows_seen += len(chunk)
    # Lakukan agregasi atau QA di sini.
    # Jangan simpan identifier mentah ke log atau prompt model.
assert rows_seen == 6_362_523

# Klasifikasi fraud hanya setelah label independen disahkan.
# Jangan memakai Risiko, Status, atau Skor Fraud sebagai ground truth
# tanpa audit provenance dan pemeriksaan kebocoran data.
```
Template di atas memvalidasi struktur dan satu temuan data, bukan melatih model. Untuk training supervisi, bangun pipeline terpisah setelah tersedia label target yang disahkan.
1. Referensi dan tata kelola
Dokumentasi operasional: [Dataset Registry DM Kontekstual](https://app.notion.com/p/07-Dataset-Registry-dan-Kamus-Data-DM-Kontekstual-4003e6031ab78179bcc7ca76a0b80fbc). Metodologi sistem: [Arsitektur Sistem dan Metodologi Teknis](https://app.notion.com/p/02-Aegis-JKN-Arsitektur-Sistem-dan-Metodologi-Teknis-4003e6031ab781efbcdac7b0dbdd0cad).
Setiap eksperimen harus menyimpan versi dataset, daftar fitur, preprocessing, seed, versi library, konfigurasi split, model artifact, metrik test, confusion matrix, dan batasan. Gunakan model sebagai alat prioritisasi pemeriksaan dengan human review, bukan pengganti keputusan klinis, administratif, atau investigasi.